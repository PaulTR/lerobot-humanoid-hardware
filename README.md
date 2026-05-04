# lerobot-humanoid-hardware

Hardware repository for **LeRobot Humanoid**.

This repo stores the practical build assets needed to reproduce the robot hardware:
- mechanical assembly documentation
- manufacturing files and notes
- electronics wiring and connector mapping
- bill of materials (BOM)
- motor pre-assembly commissioning tooling

## Current scope

- `IN`: biped platform hardware
- `OUT` (for now): upper-body hardware

The Onshape document currently contains an upper-body model as well, but this repository iteration tracks only the biped platform assets.

## CAD source of truth

Primary CAD source (Onshape):
- **Public Onshape CAD (open this first):** https://cad.onshape.com/documents/fb645318a27646d1d8840be6/w/d1cae8805fb652b4d1614997/e/804a1da43f242001a05129b4

Referenced IDs:
- Document ID: `fb645318a27646d1d8840be6`
- Workspace ID: `d1cae8805fb652b4d1614997`
- Element ID: `804a1da43f242001a05129b4`

## Repository layout

- `docs/`: architecture, guides, and procedures
- `hardware/cad/`: Onshape source reference and exported STL geometry
- `hardware/bom/`: BOM in machine-readable and human-readable formats
- `hardware/config/`: motor commissioning utilities
- `hardware/electronics/`: wiring and connector mapping

## CAD organization

`hardware/cad/stl/` is split by side and subassembly:
- `biped_platform/left_leg/{hipx,hipz,thigh,knee_mechanism,shin,ankle_mechanism,ankle,foot}`
- `biped_platform/right_leg/{hipx,hipz,thigh,knee_mechanism,shin,ankle_mechanism,ankle,foot}`
- `biped_platform/torso`

This mirrors the assembly view and makes part export placement explicit.

## Runtime integration

Runtime repository (robot model and control runtime) lives in:
- `../lerobot_humanoid_runtime`

Motor commissioning script in this repo is self-contained and does **not** depend on `robstride_toolkit`.

Main scripts:
- `hardware/config/commission_motor.py`

## Working model

1. Modify design in Onshape.
2. Export manufacturing/build assets to this repository.
3. Update BOM/config/docs in the same commit.
4. Keep all biped-platform changes traceable to a CAD revision.

## Cost estimate (Biped Platform, April 30 2026)

Scope of this estimate:
- all buy items in `hardware/bom/bom_buy.csv`
- plus PLA+ filament for printing (`~3.5 kg` used for estimate, target range `3-4 kg`)

Assumptions:
- currency: `USD`
- prices are indicative and vendor-dependent
- excludes shipping, import duties, and local taxes
- fastener prices use bulk-piece estimates
- `hipx` M3 screw line is optional and can be removed without issue

| Subassembly | Category | Name | Specification | Qty (robot) | Unit est. (USD) | Subtotal est. (USD) |
|---|---|---|---|---:|---:|---:|
| torso | electronics_controller | Raspberry Pi 5 | single-board computer | 1 | 130.00 | 130.00 |
| torso | electronics_imu | IMU | BNO055 or BNO085 | 1 | 64.00 | 64.00 |
| torso | electronics_canfd_adapter | SAVVYCANFD 2CH CANFD adapter | USB, dual CAN FD, 12 Mbps max | 1 | 59.00 | 59.00 |
| torso | cable_power | Power cable red | diameter >= 2.5 mm, 5 m | 1 | 15.00 | 15.00 |
| torso | cable_power | Power cable black | diameter >= 2.5 mm, 5 m | 1 | 15.00 | 15.00 |
| torso | cable_communication | Communication cable color 1 | 5 m | 1 | 8.00 | 8.00 |
| torso | cable_communication | Communication cable color 2 | 5 m | 1 | 8.00 | 8.00 |
| torso | motor | RobStride O0 | actuator | 2 | 125.00 | 250.00 |
| torso | fastener_screw | M2 screw | M2 x 5 cyl head | 4 | 0.10 | 0.40 |
| torso | fastener_screw | M2.5 screw | M2.5 x 20 cyl head | 9 | 0.12 | 1.08 |
| torso | fastener_screw | M3 screw | M3 x 8 cyl head | 12 | 0.10 | 1.20 |
| torso | fastener_screw | M4 screw | M4 x 20 cyl head | 16 | 0.14 | 2.24 |
| torso | fastener_screw | M5 screw | M5 x 10 cyl head | 5 | 0.20 | 1.00 |
| hipx | fastener_screw | M3 screw | M3 x 8 cyl head | 6 | 0.10 | 0.60 |
| hipx | fastener_screw | M4 screw | M4 x 40 cyl head | 12 | 0.17 | 2.04 |
| hipx | fastener_screw | M4 screw | M4 x 40-50 cyl head | 18 | 0.20 | 3.60 |
| hipx | fastener_screw | M4 screw | M4 x 8 cyl head | 16 | 0.10 | 1.60 |
| hipz | motor | RobStride O2 | actuator | 2 | 145.00 | 290.00 |
| hipz | bearing | Bearing | 35x72x17 | 4 | 12.00 | 48.00 |
| hipz | fastener_screw | M4 screw | M4 x 10 cyl head | 16 | 0.11 | 1.76 |
| hipz | fastener_screw | M4 screw | M4 x 20 cyl head | 16 | 0.14 | 2.24 |
| thigh | motor | RobStride O3 | actuator | 4 | 225.00 | 900.00 |
| thigh | bearing | Bearing | 15x21x4 | 2 | 3.00 | 6.00 |
| thigh | bearing | Bearing | 5x16x5 | 4 | 2.14 | 8.56 |
| thigh | fastener_screw | M2.5 screw | M2.5 x 6 cyl head | 6 | 0.09 | 0.54 |
| thigh | fastener_screw | M4 screw | M4 x 10 cyl head | 8 | 0.11 | 0.88 |
| thigh | fastener_screw | M4 screw | M4 x 23.5 cyl head | 8 | 0.16 | 1.28 |
| thigh | fastener_screw | M4 screw | M4 x 8 cyl head | 20 | 0.10 | 2.00 |
| knee_mechanism | bearing | Bearing | 15x21x4 | 4 | 3.00 | 12.00 |
| knee_mechanism | fastener_screw | M3 screw | M3 x 10-15 cyl head | 6 | 0.11 | 0.66 |
| knee_mechanism | fastener_screw | M4 screw | M4 x 16 cyl head | 16 | 0.12 | 1.92 |
| shin | motor | RobStride O5 | actuator | 4 | 110.00 | 440.00 |
| shin | bearing | Bearing | 15x21x4 | 8 | 3.00 | 24.00 |
| shin | fastener_screw | M2.5 screw | M2.5 x 6-10 cyl head | 6 | 0.10 | 0.60 |
| shin | fastener_screw | M3 screw | M3 x 15-20 cyl head | 8 | 0.12 | 0.96 |
| shin | fastener_screw | M3 screw | M3 x 8-12 cyl head | 48 | 0.10 | 4.80 |
| shin | fastener_screw | M4 screw | M4 x 18 cyl head | 32 | 0.14 | 4.48 |
| shin | fastener_screw | M4 screw | M4 x 8-12 cyl head | 18 | 0.11 | 1.98 |
| shin | fastener_nut | Nut M4 | M4 nut | 6 | 0.08 | 0.48 |
| shin | fastener_insert | Heat-set insert M3 | brass threaded insert M3 | 8 | 0.10 | 0.80 |
| ankle_mechanism | fastener_screw | M5 screw | M5 x 15 cyl head | 8 | 0.24 | 1.92 |
| ankle | fastener_screw | M2.5 screw | M2.5 x 6-10 cyl head | 12 | 0.10 | 1.20 |
| foot | bearing | Bearing | 5x16x5 | 4 | 2.14 | 8.56 |
| foot | fastener_screw | M2.5 screw | M2.5 x 6-10 cyl head | 6 | 0.10 | 0.60 |
| foot | fastener_nut | Nut M4 | M4 nut | 6 | 0.08 | 0.48 |
| assembly_pins | fastener_pin | Pin d3mm | d3 pin (goupille) | 8 | 0.45 | 3.60 |
| assembly_pins | fastener_pin | Pin d4mm | d4 pin (goupille) | 18 | 0.55 | 9.90 |
| tools | tool | Allen key | 2.5 mm | 1 | 3.00 | 3.00 |
| manufacturing | consumable_filament | PLA+ filament | ~3.5 kg total (target range 3-4 kg) | 1 | 56.00 | 56.00 |

| Cost block | Estimate (USD) |
|---|---:|
| ankle subtotal | 1.20 |
| ankle_mechanism subtotal | 1.92 |
| assembly_pins subtotal | 13.50 |
| foot subtotal | 9.64 |
| hipx subtotal | 7.84 |
| hipz subtotal | 342.00 |
| knee_mechanism subtotal | 14.58 |
| shin subtotal | 478.10 |
| thigh subtotal | 919.26 |
| tools subtotal | 3.00 |
| torso subtotal | 554.92 |
| BOM-to-buy subtotal (without filament) | 2345.96 |
| PLA+ subtotal (~3.5 kg) | 56.00 |
| **Estimated total** | **2401.96** |

Price anchors used for key components:
- RobStride motor market listing (O0/O2/O3/O5): https://aifitlab.com/collections/robstride-motor
- RobStride O0: https://aifitlab.com/products/robstride-00-motor
- RobStride O2: https://aifitlab.com/products/robstride-02-motor
- RobStride O5: https://aifitlab.com/products/robstride-05-motor
- Raspberry Pi 5 (8GB): https://www.sparkfun.com/products/23551
- IMU BNO085: https://www.ardusimple.com/product/adafruit-9-dof-orientation-imu-fusion-breakout-bno085/
- SAVVYCANFD adapter: https://www.pibiger-tech.com/product/savvycan-fd-c/
- Bearing 5x16x5 reference price: https://www.123bearing.com/bearing-housing/deep-groove-bearing/single-row/625
- Bearing 35x72x17 reference price: https://roulement.net/en-us/products/6207-du-nsk
- PLA+ reference price: https://us.elegoo.com/products/elegoo-rapid-pla-plus-filament-1-75mm-colored-1kg
