# First Power-On Procedure

## Phase 1: logic power only

1. Power controller logic rails only.
2. Confirm expected idle current.
3. Confirm communication with all controller nodes.
4. Verify watchdog/heartbeat behavior.

## Phase 2: actuator power with safety limits

1. Set low current/torque limits.
2. Enable one actuator at a time.
3. Verify sign/direction and encoder consistency.
4. Disable immediately if unexpected motion occurs.

## Phase 3: low-amplitude validation

1. Execute tiny motion commands around neutral position.
2. Confirm software limits are enforced.
3. Log offsets and update calibration YAML.

Stop criteria:
- unexpected heating, smell, noise, or oscillation
- communication instability under load
- any limit/safety mismatch
