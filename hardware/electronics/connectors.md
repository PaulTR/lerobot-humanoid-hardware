# Connectors

## Connector map (biped platform)

| Connector ID | Function | Board Side | Device Side | Pinout Status | Notes |
|---|---|---|---|---|---|
| CONN-CANFD-ADAPTER-01 | USB to dual CAN-FD interface | USB-A host | USB-A plug | defined | SAVVYCANFD 2CH CANFD adapter |
| CONN-CANFD-CH0-DB9 | CAN channel 0 (torso/left bus split as needed) | DB9 female on adapter (`CAN0`) | DB9 harness | partial | Known pins: `2=CAN-L`, `3=GND`, `7=CAN-H` |
| CONN-CANFD-CH1-DB9 | CAN channel 1 (torso/right bus split as needed) | DB9 female on adapter (`CAN1`) | DB9 harness | partial | Known pins: `2=CAN-L`, `3=GND`, `7=CAN-H` |
| CONN-PWR-01 | Main power in | TODO | TODO | TODO | Add fuse and wire gauge |
| CONN-CAN-01 | Actuator bus | TODO | TODO | TODO | Add termination notes |
| CONN-ENC-01 | Encoder input | TODO | TODO | TODO | Validate polarity |

## To complete

- fill exact connector references and footprints
- add pin numbering and signal names
- add wire gauge and maximum current per line
- validate CAN bus termination placement (`120 ohm` at both ends)
