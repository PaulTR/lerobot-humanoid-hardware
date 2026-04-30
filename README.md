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

The Onshape document currently contains an upper-body model (`v1`) as well, but this repository iteration tracks only the biped platform assets.

## CAD source of truth

Primary CAD source (Onshape):
- https://cad.onshape.com/documents/fb645318a27646d1d8840be6/w/d1cae8805fb652b4d1614997/e/804a1da43f242001a05129b4

Referenced IDs:
- Document ID: `fb645318a27646d1d8840be6`
- Workspace ID: `d1cae8805fb652b4d1614997`
- Element ID: `804a1da43f242001a05129b4`

## Repository layout

- `docs/`: architecture, guides, and procedures
- `hardware/cad/`: CAD source notes and exported geometry (`step`, `stl`)
- `hardware/bom/`: BOM in machine-readable and human-readable formats
- `hardware/config/`: motor commissioning utilities
- `hardware/electronics/`: wiring and connector mapping

## CAD organization

`hardware/cad/` is now split by side and subassembly:
- `biped_platform/left_leg/{hipx_subassembly,hipy_subassembly,thigh_subassembly,shin_subassembly,ankle_subassembly,foot_subassembly,frames}`
- `biped_platform/right_leg/{hipx_subassembly,hipy_subassembly,thigh_subassembly,shin_subassembly,ankle_subassembly,foot_subassembly,frames}`
- `biped_platform/torso_subassembly`

This mirrors the assembly view and makes part export placement explicit.

## Runtime integration

Runtime repository (model and full-robot calibration) lives in:
- `../lerobot_humanoid_runtime`

Motor commissioning script in this repo is self-contained and does **not** depend on `robstride_toolkit`.

Main scripts:
- `hardware/config/commission_motor.py`

## Working model

1. Modify design in Onshape.
2. Export manufacturing/build assets to this repository.
3. Update BOM/config/docs in the same commit.
4. Keep all biped-platform changes traceable to a CAD revision.
