# Overview

This repository is the build reference for **LeRobot Humanoid hardware**.

## Scope boundary

Current tracked hardware scope:
- biped platform (legs + base-related hardware)

Not yet tracked in this repo iteration:
- upper-body hardware present in the current Onshape document

## Source systems

- CAD source of truth: Onshape document (`fb645318a27646d1d8840be6`)
- Build source of truth: this repository
- Runtime control/calibration source: `../lerobot_humanoid_runtime`

## CAD split

The biped CAD tree is organized by side and subassembly:
- `hardware/cad/source/biped_platform/left_leg/*`
- `hardware/cad/source/biped_platform/right_leg/*`
- `hardware/cad/source/biped_platform/torso_subassembly`

The same split is mirrored under:
- `hardware/cad/step/biped_platform/*`
- `hardware/cad/stl/biped_platform/*`

## Traceability rules

For every hardware change:
1. Link it to a CAD revision/context in commit message or PR notes.
2. Update BOM (`hardware/bom/bom.csv`) if parts change.
3. If geometry/kinematics change, update runtime calibration/model artifacts in `../lerobot_humanoid_runtime`.
4. Update assembly/manufacturing docs if process changes.
