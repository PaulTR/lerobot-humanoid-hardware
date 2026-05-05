# Assembly Guide

Assembly order:
1. Configure all motors (`docs/electronics/motor_commissioning.md`).
2. Print all STL parts (`docs/manufacturing/printing_guide.md`).
3. Build torso first.
4. Build upper legs in order: `hipx -> hipy (hipz in repo naming) -> thigh` (left and right).
5. In parallel, build lower legs in order: `foot -> ankle -> knee_mechanism -> shin -> ankle_mechanism` (left and right).
6. Assemble upper and lower leg modules.
7. Integrate both legs to torso and run wiring checks.

Common assembly rules:
- For each subassembly, insert bearings first (press or gentle hammer).
- Place motor goupille/pin during the same phase as bearing insertion.
- Exception: in `knee_mechanism` and `ankle`, one interface should stay slightly loose but still movable.
- For subassembly goupilles: place them during assembly except on `thigh` (keep thigh demountable).
- Motor orientation is critical: follow the Onshape assembly orientation relative to each motor connector, otherwise cable length can become insufficient.
- Default thread strategy is direct screw in plastic; use around `5 Nm` for non-structural plastic threads.
- For motor threaded holes and structural insert zones, use higher torque appropriate to the thread/material.
- Some fits are intentionally tight; if required, gently ream/drill with a metal bit at low speed.
- Pins are not a standalone assembly stage: install them inside each motor/subassembly during build.
- Tools are prerequisites only (not assemblies).

Reference files:
- `hardware/bom/bom.csv`
- `hardware/bom/bom_buy.csv`
- `docs/manufacturing/printing_guide.md`
- `docs/electronics/motor_commissioning.md`
- `hardware/electronics/cabling/README.md`

Leg cabling note:
- Left and right legs use the same sub-cable design and routing logic.
- Cable legend: red = power, green = CAN, blue = CAN + power.

Leg cabling integration order (both legs):
1. Prepare three sub-cables using `hardware/electronics/cabling/README.md`: shin, thigh, hip pass-through.
2. Install the shin sub-cable during `shin` assembly, before final closure.
3. Install the thigh sub-cable during `thigh` assembly, before final tightening.
4. Route the hip pass-through sub-cable during `hipz` integration.
5. Join leg cables to torso harness during final leg-to-torso integration.

Spacer coverage check:
- Spacers are documented via STL lists in each relevant subassembly section.
- Spacer STL subassemblies: `shin`, `ankle_mechanism`, `ankle`, `foot`.
- Non-spacer STL subassemblies: `torso`, `hipx`, `hipz`, `thigh`, `knee_mechanism`.

Mounted robot photo references (explicit names):
- `docs/assembly/photos/leg_full_view.jpg`
- `docs/assembly/photos/torso_detail.jpg`
- `docs/assembly/photos/hipy_detail.jpg`
- `docs/assembly/photos/hipz_detail.jpg`
- `docs/assembly/photos/thigh_detail.jpg`
- `docs/assembly/photos/knee_detail.jpg`
- `docs/assembly/photos/knee_mechanism_view_1.jpg`
- `docs/assembly/photos/knee_mechanism_view_2.jpg`
- `docs/assembly/photos/knee_mechanism_view_3.jpg`

## torso

Components:
| Category | Name | Specification | Qty / Subassembly | Qty / Robot |
|---|---|---|---:|---:|
| electronics_controller | Raspberry Pi 5 | single-board computer | 1 | 1 |
| electronics_imu | IMU | BNO055 or BNO085 | 1 | 1 |
| electronics_canfd_adapter | SAVVYCANFD 2CH CANFD adapter | USB, dual CAN FD, 12 Mbps max | 1 | 1 |
| cable_power | Power cable red | diameter >= 2.5 mm, 5 m | 1 | 1 |
| cable_power | Power cable black | diameter >= 2.5 mm, 5 m | 1 | 1 |
| cable_communication | Communication cable color 1 | 5 m | 1 | 1 |
| cable_communication | Communication cable color 2 | 5 m | 1 | 1 |
| motor | RobStride O0 | actuator | 2 | 2 |
| fastener_screw | M2 screw | M2 x 5 cyl head | 4 | 4 |
| fastener_screw | M2.5 screw | M2.5 x 20 cyl head | 9 | 9 |
| fastener_screw | M3 screw | M3 x 8 cyl head | 12 | 12 |
| fastener_screw | M4 screw | M4 x 20 cyl head | 16 | 16 |
| fastener_screw | M5 screw | M5 x 10 cyl head | 5 | 5 |

STL To Print:
| Name | Quantity |
|---|---:|
| torso/torso_can_holder.stl | 1 |
| torso/torso_imu_holder.stl | 1 |
| torso/torso_torso13.stl | 1 |
| torso/torso_torso23.stl | 1 |
| torso/torso_torso33.stl | 1 |
| torso/torso_uper_torso_22.stl | 1 |
| torso/torso_upper_torso_12.stl | 1 |

> Comment: cheaper or better CAN-FD adapters may exist, but this one is currently the only adapter proven in this project to handle the RobStride CAN protocol.

Assembly steps:
1. Assemble each torso motor on its motor support and screw it.
2. Place each motor-support subassembly on top of the bearing stack and screw it.
3. Verify both torso motor outputs rotate freely after tightening.

## hipx

Components:
| Category | Name | Specification | Qty / Subassembly | Qty / Robot |
|---|---|---|---:|---:|
| fastener_screw | M3 screw | M3 x 8 cyl head | 3 | 6 |
| fastener_screw | M4 screw | M4 x 40 cyl head | 6 | 12 |
| fastener_screw | M4 screw | M4 x 45 cyl head | 9 | 18 |
| fastener_screw | M4 screw | M4 x 8 cyl head | 8 | 16 |

> Comment: the `hipx` M3 screw line is optional and can be removed without issue.

STL To Print:
| Name | Quantity |
|---|---:|
| left_leg/hipx/hipx_2_hipxy_sym.stl | 1 |
| right_leg/hipx/hipx_2_hipxy.stl | 1 |

Assembly steps:
1. Start by inserting the hip axis and fixing it to the motor.
2. Align hipx parts on the previous subassembly and screw the full assembly.
3. Verify hipx motion is free with no hard point.

## hipz

Components:
| Category | Name | Specification | Qty / Subassembly | Qty / Robot |
|---|---|---|---:|---:|
| motor | RobStride O2 | actuator | 1 | 2 |
| bearing | Bearing | 35x72x17 | 2 | 4 |
| fastener_screw | M4 screw | M4 x 10 cyl head | 8 | 16 |
| fastener_screw | M4 screw | M4 x 20 cyl head | 8 | 16 |

STL To Print:
| Name | Quantity |
|---|---:|
| left_leg/hipz/hip_z_hipz12_sym.stl | 1 |
| left_leg/hipz/hip_z_hipz22_sym.stl | 1 |
| right_leg/hipz/hip_z_hipz12.stl | 1 |
| right_leg/hipz/hip_z_hipz22.stl | 1 |

Assembly steps:
1. Insert hipz bearings.
2. Start by inserting the axis and fixing it to the motor (`hipz` naming in this repo corresponds to the hipy joint).
3. Place and screw the motor.
4. Route the hip pass-through sub-cable through hipz according to `hardware/electronics/cabling/README.md`.
5. Assemble the bearing to the hipz assembly and verify free motion.

## thigh

Components:
| Category | Name | Specification | Qty / Subassembly | Qty / Robot |
|---|---|---|---:|---:|
| motor | RobStride O3 | actuator | 2 | 4 |
| bearing | Bearing | 15x21x4 | 1 | 2 |
| bearing | Bearing | 5x16x5 | 2 | 4 |
| fastener_screw | M2.5 screw | M2.5 x 6 cyl head | 3 | 6 |
| fastener_screw | M4 screw | M4 x 10 cyl head | 4 | 8 |
| fastener_screw | M4 screw | M4 x 23.5 cyl head | 4 | 8 |
| fastener_screw | M4 screw | M4 x 8 cyl head | 10 | 20 |
| fastener_axis | Shoulder screw 07534-05X40 | ISO7379, D1=5, L1=40, B=8, M4, SW=2.5, steel 12.9 | 1 | 2 |

STL To Print:
| Name | Quantity |
|---|---:|
| left_leg/thigh/femur_v2_femur_12_sym_1.stl | 1 |
| left_leg/thigh/femur_v2_femur_22_sym_1.stl | 1 |
| left_leg/thigh/femur_v2_hat_femur_2.stl | 1 |
| right_leg/thigh/femur_v2_femur_12_1.stl | 1 |
| right_leg/thigh/femur_v2_femur_22_1.stl | 1 |
| right_leg/thigh/femur_v2_hat_femur_2.stl | 1 |

Assembly steps:
1. Insert the exterior thigh shell (`femur_22`) into the hipy joint side first (`hipz` naming in this repo).
2. Fix `femur_12` to the hipy/hipz side.
3. Install and route the thigh sub-cable before final closing (`hardware/electronics/cabling/README.md`).
4. Screw `femur_12` and `femur_22` together once joint alignment is correct.
5. Do not lock thigh with permanent goupilles if you want it demountable.

## foot

Components:
| Category | Name | Specification | Qty / Subassembly | Qty / Robot |
|---|---|---|---:|---:|
| bearing | Bearing | 5x16x5 | 2 | 4 |
| fastener_screw | M2.5 screw | M2.5 x 8 cyl head | 3 | 6 |
| fastener_nut | Nut M4 | M4 nut | 3 | 6 |

STL To Print:
| Name | Quantity |
|---|---:|
| left_leg/foot/bearing_spacer14_5_7_3.stl | 1 |
| left_leg/foot/bearing_spacer24_5_7_3.stl | 1 |
| left_leg/foot/bearing_spacer34_5_7_3.stl | 1 |
| left_leg/foot/bearing_spacer44_5_7_3.stl | 1 |
| left_leg/foot/foot_foot.stl | 1 |
| left_leg/foot/foot_hat_small.stl | 1 |
| right_leg/foot/bearing_spacer14_5_7_3.stl | 1 |
| right_leg/foot/bearing_spacer24_5_7_3.stl | 1 |
| right_leg/foot/bearing_spacer34_5_7_3.stl | 1 |
| right_leg/foot/bearing_spacer44_5_7_3.stl | 1 |
| right_leg/foot/foot_foot.stl | 1 |
| right_leg/foot/foot_hat_small.stl | 1 |

Assembly steps:
1. Insert foot bearings and pins/goupilles.
2. Assemble and screw foot parts.
3. Check foot alignment before full tightening.
## ankle

Components:
| Category | Name | Specification | Qty / Subassembly | Qty / Robot |
|---|---|---|---:|---:|
| fastener_screw | M2.5 screw | M2.5 x 8 cyl head | 6 | 12 |
| fastener_axis | Shoulder screw 07534-05X40 | ISO7379, D1=5, L1=40, B=8, M4, SW=2.5, steel 12.9 | 1 | 2 |

STL To Print:
| Name | Quantity |
|---|---:|
| left_leg/ankle/ujoint_hat_small_12.stl | 1 |
| left_leg/ankle/ujoint_hat_small_22.stl | 1 |
| left_leg/ankle/ujoint_spacer_12_ujoint.stl | 1 |
| left_leg/ankle/ujoint_spacer_22_ujoint.stl | 1 |
| left_leg/ankle/ujoint_ujoint.stl | 1 |
| right_leg/ankle/ujoint_hat_small_12.stl | 1 |
| right_leg/ankle/ujoint_hat_small_22.stl | 1 |
| right_leg/ankle/ujoint_spacer_12_ujoint.stl | 1 |
| right_leg/ankle/ujoint_spacer_22_ujoint.stl | 1 |
| right_leg/ankle/ujoint_ujoint.stl | 1 |

Assembly steps:
1. Assemble U-joint parts and install pins/goupilles.
2. Insert the assembled U-joint into shin bearings (bearings are installed in the shin subassembly, not in ankle STL parts).
3. Keep one ankle interface slightly loose but still movable.
4. Verify free ankle motion after tightening.

## knee_mechanism

Components:
| Category | Name | Specification | Qty / Subassembly | Qty / Robot |
|---|---|---|---:|---:|
| bearing | Bearing | 15x21x4 | 2 | 4 |
| fastener_screw | M3 screw | M3 x 12.5 cyl head | 3 | 6 |
| fastener_screw | M4 screw | M4 x 16 cyl head | 8 | 16 |

STL To Print:
| Name | Quantity |
|---|---:|
| left_leg/knee_mechanism/femur_v2_knee_actuation_2.stl | 1 |
| left_leg/knee_mechanism/femur_v2_knee_rod12_sym_1.stl | 1 |
| left_leg/knee_mechanism/femur_v2_knee_rod22_sym_1.stl | 1 |
| right_leg/knee_mechanism/femur_v2_knee_actuation_1.stl | 1 |
| right_leg/knee_mechanism/femur_v2_knee_rod12_1.stl | 1 |
| right_leg/knee_mechanism/femur_v2_knee_rod22_1.stl | 1 |

Assembly steps:
1. Pre-assemble the knee mechanism with its motor and rods.
2. Keep the knee interface slightly loose but still movable.
3. Integrate this knee mechanism inside the shin assembly first.
4. Fix the knee motor to the thigh at the end of leg integration.
5. Check that knee motion is smooth and not binding.

## shin

Components:
| Category | Name | Specification | Qty / Subassembly | Qty / Robot |
|---|---|---|---:|---:|
| motor | RobStride O5 | actuator | 2 | 4 |
| bearing | Bearing | 15x21x4 | 4 | 8 |
| fastener_screw | M2.5 screw | M2.5 x 8 cyl head | 3 | 6 |
| fastener_screw | M3 screw | M3 x 17.5 cyl head | 4 | 8 |
| fastener_screw | M3 screw | M3 x 10 cyl head | 24 | 48 |
| fastener_screw | M4 screw | M4 x 18 cyl head | 16 | 32 |
| fastener_screw | M4 screw | M4 x 10 cyl head | 9 | 18 |
| fastener_nut | Nut M4 | M4 nut | 3 | 6 |
| fastener_insert | Heat-set insert M3 | brass threaded insert M3 | 4 | 8 |

STL To Print:
| Name | Quantity |
|---|---:|
| left_leg/shin/spacer12_5_9_4_5.stl | 1 |
| left_leg/shin/spacer22_5_9_4_5.stl | 1 |
| left_leg/shin/tibias2_hat_big.stl | 1 |
| left_leg/shin/tibias2_shin_spacer_2.stl | 1 |
| left_leg/shin/tibias2_tibias12_sym_4.stl | 1 |
| left_leg/shin/tibias2_tibias22_sym_4.stl | 1 |
| right_leg/shin/spacer12_5_9_4_5.stl | 1 |
| right_leg/shin/spacer22_5_9_4_5.stl | 1 |
| right_leg/shin/tibias2_hat_big.stl | 1 |
| right_leg/shin/tibias2_shin_spacer_2.stl | 1 |
| right_leg/shin/tibias2_tibias12.stl | 1 |
| right_leg/shin/tibias2_tibias22.stl | 1 |

Assembly steps:
1. Install M3 inserts first (`4` per shin).
2. Insert bearings and pins/goupilles.
3. Mandatory: place the full knee mechanism (including motor) inside before final shin closure.
4. For re-assembly in tight fit conditions: gently shift the bearing with light hammer taps to create spacer clearance, insert spacer, then re-seat bearing.
5. Install and route the shin sub-cable before closure (`hardware/electronics/cabling/README.md`).
6. Preferable: place ankle module now (recommended, not mandatory).
7. Close and screw shin structure, then verify internal parts still move.

## ankle_mechanism

Components:
| Category | Name | Specification | Qty / Subassembly | Qty / Robot |
|---|---|---|---:|---:|
| fastener_screw | M5 screw | M5 x 15 cyl head | 4 | 8 |
| joint_spherical | Spherical joint 27628-01-05 | Norelem | 4 | 8 |
| fastener_axis | Shoulder screw 07534-05X20 | ISO7379, D1=5, L1=20, B=8, M4, steel 12.9 | 4 | 8 |

STL To Print:
| Name | Quantity |
|---|---:|
| left_leg/ankle_mechanism/bearing_spacer14_5_7_3.stl | 1 |
| left_leg/ankle_mechanism/bearing_spacer24_5_7_3.stl | 1 |
| left_leg/ankle_mechanism/bearing_spacer34_5_7_3.stl | 1 |
| left_leg/ankle_mechanism/bearing_spacer44_5_7_3.stl | 1 |
| left_leg/ankle_mechanism/tibias2_rod_long.stl | 1 |
| left_leg/ankle_mechanism/tibias2_rod_small.stl | 1 |
| left_leg/ankle_mechanism/tibias_actuation_ankle_12.stl | 1 |
| left_leg/ankle_mechanism/tibias_actuation_ankle_22.stl | 1 |
| right_leg/ankle_mechanism/bearing_spacer14_5_7_3.stl | 1 |
| right_leg/ankle_mechanism/bearing_spacer24_5_7_3.stl | 1 |
| right_leg/ankle_mechanism/bearing_spacer34_5_7_3.stl | 1 |
| right_leg/ankle_mechanism/bearing_spacer44_5_7_3.stl | 1 |
| right_leg/ankle_mechanism/tibias2_rod_long.stl | 1 |
| right_leg/ankle_mechanism/tibias2_rod_small.stl | 1 |
| right_leg/ankle_mechanism/tibias_actuation_ankle_12.stl | 1 |
| right_leg/ankle_mechanism/tibias_actuation_ankle_22.stl | 1 |

Assembly steps:
1. Install spherical joints on rods (`2` per rod, `4` per leg, `8` per robot).
2. Assemble rods, spacers, and ankle actuation parts, then screw.
3. Verify mechanism moves freely through its range.
