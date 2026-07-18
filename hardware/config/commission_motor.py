#!/usr/bin/env python3
from __future__ import annotations

"""Commission one RobStride motor before assembly.

This utility is self-contained (no robstride_toolkit import).

Wizard flow:
1) Detect current motor ID and protocol.
2) Switch motor to MIT protocol (with reboot checkpoints).
3) Set target ID (based on motor model map).
4) Reboot and verify final ID/protocol.
5) Motion check: gentle sway between -180 and 180 deg at 0.1Hz, return to 0.
"""

import argparse
import math
import sys
import time
from enum import IntEnum
from typing import Any, Optional

try:
    import can  # type: ignore
except Exception as exc:  # pragma: no cover - runtime dependency
    can = None
    _CAN_IMPORT_ERROR = exc
else:
    _CAN_IMPORT_ERROR = None

PROTOCOLS = ("canopen", "private", "mit")
DEFAULT_PROTOCOL_ORDER = ("canopen", "private", "mit")

CAN_CMD_CLEAR_FAULT = 0xFB
CAN_CMD_ENABLE = 0xFC
CAN_CMD_DISABLE = 0xFD
CAN_CMD_SET_ZERO = 0xFE

MOTOR_MODEL_ID_MAP: dict[str, tuple[int, ...]] = {
    "o0": (1, 7),
    "o2": (2, 8),
    "o3": (3, 4, 9, 10),
    "o5": (5, 6, 11, 12),
}


class CommMode(IntEnum):
    PRIVATE = 0
    CANOPEN = 1
    MIT = 2


def _require_can() -> None:
    if can is None:
        raise RuntimeError(
            "python-can is required for motor commissioning. "
            "Install it with: pip install python-can"
        ) from _CAN_IMPORT_ERROR


def _open_bus(interface: str, channel: str):
    _require_can()
    # Explicitly set 1Mbps for RobStride defaults
    return can.interface.Bus(interface=interface, channel=channel, bitrate=1000000)


def _shutdown_bus(bus: Any) -> None:
    try:
        bus.shutdown()
    except Exception:
        pass


def _flush_bus(bus: Any, max_msgs: int = 1000) -> int:
    count = 0
    while count < max_msgs:
        msg = bus.recv(0.0005)
        if msg is None:
            break
        count += 1
    return count


def make_ext_id(comm_type: int, host_id: int, target_id: int) -> int:
    return ((comm_type & 0x1F) << 24) | ((host_id & 0xFF) << 8) | (target_id & 0xFF)


def parse_reply_id(arbitration_id: int) -> tuple[int, int, int]:
    comm_type = (arbitration_id >> 24) & 0x1F
    host_field = (arbitration_id >> 8) & 0xFF
    target_field = arbitration_id & 0xFF
    return comm_type, host_field, target_field


# --- The Logic from the script that worked ---

def ping_private(bus: Any, motor_id: int) -> bool:
    arb_id = make_ext_id(0x00, 0xFD, motor_id)
    bus.send(can.Message(arbitration_id=arb_id, data=[0]*8, is_extended_id=True))
    deadline = time.monotonic() + 0.05
    while time.monotonic() < deadline:
        msg = bus.recv(timeout=0.01)
        if msg and msg.is_extended_id: return True
    return False


def ping_mit(bus: Any, motor_id: int) -> bool:
    bus.send(can.Message(arbitration_id=motor_id, data=[0xFF]*7 + [CAN_CMD_CLEAR_FAULT], is_extended_id=False))
    deadline = time.monotonic() + 0.05
    while time.monotonic() < deadline:
        msg = bus.recv(timeout=0.01)
        if msg and not msg.is_extended_id: return True
    return False


def ping_canopen(bus: Any, motor_id: int) -> bool:
    req_id = 0x600 + motor_id
    data = [0x40, 0x00, 0x10, 0x00, 0, 0, 0, 0]
    bus.send(can.Message(arbitration_id=req_id, data=data, is_extended_id=False))
    deadline = time.monotonic() + 0.05
    while time.monotonic() < deadline:
        msg = bus.recv(timeout=0.01)
        if msg and not msg.is_extended_id and msg.arbitration_id == (0x580 + motor_id): return True
    return False


def detect_motor(bus: Any, start_id: int, end_id: int, timeout_s: float = 1.0) -> tuple[Optional[int], Optional[str]]:
    """Exact detection logic from working script, integrated with range arguments."""
    deadline = time.monotonic() + timeout_s
    # 1. Passive
    while time.monotonic() < deadline:
        msg = bus.recv(timeout=0.1)
        if msg:
            if not msg.is_extended_id:
                mid = msg.arbitration_id
                if start_id <= mid <= end_id: return mid, "mit"
            elif msg.is_extended_id and (msg.arbitration_id & 0xFFFF00) == 0:
                target = msg.arbitration_id & 0xFF
                mid = (0 if target == 0 else target)
                if mid == 0xFE: mid = 127
                if start_id <= mid <= end_id: return mid, "private"

    # 2. Active Range Scan (Fast 50ms pings)
    for mid in range(start_id, end_id + 1):
        if ping_private(bus, mid): return mid, "private"
        if ping_mit(bus, mid): return mid, "mit"
        if ping_canopen(bus, mid): return mid, "canopen"
    return None, None


def switch_private_to_mit(bus: Any, motor_id: int) -> bool:
    print(f"Sending MIT protocol switch to ID {motor_id}...")
    arb_id = make_ext_id(0x19, 0xFD, motor_id)
    data = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 2, 0x00]
    bus.send(can.Message(arbitration_id=arb_id, data=data, is_extended_id=True))
    time.sleep(0.1)
    bus.send(can.Message(arbitration_id=make_ext_id(0x07, 0xFD, motor_id), data=[0]*8, is_extended_id=True))
    time.sleep(0.2)
    return True


def change_motor_id(bus: Any, old_id: int, new_id: int) -> bool:
    print(f"Changing MIT ID {old_id} -> {new_id}...")
    bus.send(can.Message(arbitration_id=old_id, data=[0xFF]*6 + [new_id & 0xFF, 0xFA], is_extended_id=False))
    time.sleep(0.2)
    # Flash Registration Sequence
    bus.send(can.Message(arbitration_id=new_id, data=[0x70, 0x05, 0, 0, 0, 0, 0, new_id & 0xFF], is_extended_id=False))
    time.sleep(0.1)
    bus.send(can.Message(arbitration_id=new_id, data=[0x70, 0xFF, 0, 0, 0, 0, 0, 0], is_extended_id=False))
    time.sleep(0.2)
    return True


# --- Motion Test ---

def _float_to_uint(x: float, x_min: float, x_max: float, bits: int) -> int:
    x_clamped = max(float(x_min), min(float(x_max), float(x)))
    span = float(x_max - x_min)
    return int(((x_clamped - x_min) / span) * ((1 << bits) - 1))


def mit_position_command(bus: Any, motor_id: int, pos_deg: float, kp: float = 5.0, kd: float = 0.15):
    p_rad = math.radians(pos_deg)
    q = _float_to_uint(p_rad, -12.57, 12.57, 16)
    kp_uint = _float_to_uint(kp, 0.0, 500.0, 12)
    kd_uint = _float_to_uint(kd, 0.0, 5.0, 12)
    v_uint = 2048  # Center
    t_uint = 2048  # Center

    data = [0] * 8
    data[0] = (q >> 8) & 0xFF
    data[1] = q & 0xFF
    data[2] = (v_uint >> 4) & 0xFF
    data[3] = ((v_uint & 0x0F) << 4) | ((kp_uint >> 8) & 0x0F)
    data[4] = kp_uint & 0xFF
    data[5] = (kd_uint >> 4) & 0xFF
    data[6] = ((kd_uint & 0x0F) << 4) | ((t_uint >> 8) & 0x0F)
    data[7] = t_uint & 0xFF
    bus.send(can.Message(arbitration_id=motor_id, data=data, is_extended_id=False))


def _run_motion_test(bus: Any, motor_id: int, duration_s: float):
    print(f"Starting gentle sway test (-180 to 180) on ID {motor_id}...")
    bus.send(can.Message(arbitration_id=motor_id, data=[0xFF]*7 + [CAN_CMD_ENABLE], is_extended_id=False))
    time.sleep(0.2)
    
    start_time = time.monotonic()
    frequency = 0.1  # 0.1 Hz
    try:
        while (time.monotonic() - start_time) < duration_s:
            elapsed = time.monotonic() - start_time
            target = 180.0 * math.sin(2 * math.pi * frequency * elapsed)
            mit_position_command(bus, motor_id, target)
            time.sleep(0.02)
        
        print("Returning to 0.0 degrees...")
        ret_start = time.monotonic()
        while (time.monotonic() - ret_start) < 2.0:
            mit_position_command(bus, motor_id, 0.0)
            time.sleep(0.02)
    except KeyboardInterrupt: pass
    finally:
        bus.send(can.Message(arbitration_id=motor_id, data=[0xFF]*7 + [CAN_CMD_DISABLE], is_extended_id=False))
    print("Motion test complete. Motor disabled.")


# --- Wizard and CLI ---

def _wait_reboot(*, assume_yes: bool = False) -> None:
    if assume_yes:
        time.sleep(3.0)
        return
    input(">>> Reboot motor now (Power Cycle), then press Enter to continue...")


def _cmd_scan(args):
    bus = _open_bus(args.interface, args.channel)
    try:
        print(f"Scanning IDs {args.start_id}-{args.end_id}...")
        for mid in range(args.start_id, args.end_id + 1):
            if ping_mit(bus, mid): print(f"  ID {mid:>3}: mit")
            if ping_private(bus, mid): print(f"  ID {mid:>3}: private")
            if ping_canopen(bus, mid): print(f"  ID {mid:>3}: canopen")
        return 0
    finally:
        _shutdown_bus(bus)


def _cmd_wizard(args: argparse.Namespace) -> int:
    bus = _open_bus(args.interface, args.channel)
    try:
        _flush_bus(bus)
        print("Scanning for motor...")
        motor_id, protocol = detect_motor(bus, args.start_id, args.end_id)

        if motor_id is None:
            print("No motor detected. Check wiring and power."); return 1
        print(f"Detected motor id={motor_id}, protocol={protocol}")

        # 1. Ensure MIT Protocol
        if protocol != "mit":
            if protocol == "private":
                switch_private_to_mit(bus, motor_id)
            elif protocol == "canopen":
                bus.send(can.Message(arbitration_id=make_ext_id(0x19, 0xFD, motor_id), data=[0]*8, is_extended_id=True))
            
            _wait_reboot(assume_yes=args.yes)
            _flush_bus(bus)
            # RE-DETECT: Find where the motor ended up after protocol switch (likely ID 0)
            motor_id, protocol = detect_motor(bus, 0, 127, timeout_s=3.0)
            if protocol != "mit":
                print(f"Verification failed. Found {protocol}."); return 1

        # 2. Change ID
        if motor_id != args.new_id:
            change_motor_id(bus, motor_id, args.new_id)
            _wait_reboot(assume_yes=args.yes)
            _flush_bus(bus)
            # RE-DETECT: Verify motor is at the NEW ID
            motor_id, protocol = detect_motor(bus, args.start_id, args.end_id, timeout_s=3.0)
            if motor_id != args.new_id:
                print(f"Verification failed. Motor at ID {motor_id}."); return 1

        print(f"Commissioning complete. Motor is ID {motor_id} in MIT mode.")
        if not args.skip_motion_test:
            duration = max(args.motion_duration_s, 10.0)
            _run_motion_test(bus, motor_id, duration)
        return 0
    finally:
        _shutdown_bus(bus)


def main() -> int:
    parser = argparse.ArgumentParser(description="RobStride Commissioning Utility")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_scan = sub.add_parser("scan")
    p_scan.add_argument("--interface", default="socketcan")
    p_scan.add_argument("--channel", default="can0")
    p_scan.add_argument("--start-id", type=int, default=0)
    p_scan.add_argument("--end-id", type=int, default=127)

    p_wizard = sub.add_parser("wizard")
    p_wizard.add_argument("--interface", default="socketcan")
    p_wizard.add_argument("--channel", default="can0")
    p_wizard.add_argument("--new-id", type=int, required=True)
    p_wizard.add_argument("--motor-model", choices=("o0", "o2", "o3", "o5"), required=True)
    p_wizard.add_argument("--start-id", type=int, default=0)
    p_wizard.add_argument("--end-id", type=int, default=127)
    p_wizard.add_argument("--skip-motion-test", action="store_true")
    p_wizard.add_argument("--motion-duration-s", type=float, default=10.0)
    p_wizard.add_argument("--yes", action="store_true")

    args = parser.parse_args()
    try:
        if args.cmd == "scan": return _cmd_scan(args)
        if args.cmd == "wizard": return _cmd_wizard(args)
    except KeyboardInterrupt: return 130
    except Exception as e: print(f"Error: {e}"); return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())