# Electronics

Electronics documentation for the biped platform.

Core artifacts:
- full wiring diagram image (`hardware/electronics/wiring_diagram.png`)
- connector and pin mapping (`hardware/electronics/connectors.md`)
- power distribution notes
- controller and actuator bus topology

Motor pre-assembly commissioning:
- detailed workflow: `docs/electronics/motor_commissioning.md`
- tool: `hardware/config/commission_motor.py`
- recommended entrypoint: `wizard` command
- covers protocol detection, MIT switch, model-based ID assignment, and motion check

Implementation note:
- this script embeds only the CAN functions it uses; it does not import `robstride_toolkit`.

Bring-up runbooks:
- `docs/electronics/check_wiring.md`
- `docs/electronics/first_power_on.md`
