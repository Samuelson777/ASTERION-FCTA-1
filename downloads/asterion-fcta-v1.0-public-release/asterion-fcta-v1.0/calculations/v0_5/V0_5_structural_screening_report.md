# ASTERION FCTA-1 V0.5 Structural Screening Report

## Status and scope

The numerical values below were produced by the included independent Python linear 3-D Euler–Bernoulli frame solver. They are **screening results**, not ANSYS results and not certification evidence. The model uses ideal rigid joints, linear aluminium tubes, simplified mass placement and an aft-fixed ground-test support.

## Screening summary

| Load case | Max translation (mm) | Max screening stress (MPa) | Min yield factor | Min member Euler factor | Finding |
|---|---:|---:|---:|---:|---|
| LC-STR-01 | 0.810 | 3.953 | 127.24 | 328.62 | SCREENING PASS |
| LC-STR-02 | 13.788 | 43.135 | 11.66 | 195.04 | SCREENING PASS — near displacement limit |
| LC-STR-03 | 0.176 | 4.428 | 113.59 | 18.03 | SCREENING PASS |
| LC-STR-04 | 6.610 | 2.977 | 168.97 | 15.53 | SCREENING PASS |
| LC-STR-05 | 105.147 | 9.941 | 50.60 | 27.31 | REDESIGN FLAG — excessive ring tangential flexibility |
| LC-STR-06 | 13.788 | 43.135 | 11.66 | 18.03 | SCREENING PASS — propulsion displacement governs |
| LC-STR-07 | 52.823 | 11.151 | 45.11 | 42.29 | REDESIGN FLAG — forward bending flexibility |

## Modal screening

The aft-supported screening model predicts the first twelve flexible frequencies shown in `python_screening/supported_modal_screening.csv`. The first predicted supported frequency is approximately **0.131 Hz**. This passes the provisional 0.10 Hz portfolio criterion, but it is low enough that attitude-control, ring-drive, solar-array and docking excitation spectra must be assessed before the configuration is considered dynamically mature.

## Main engineering findings

1. **Emergency ring braking governs displacement.** The screening model predicts about 105 mm maximum translation for the 120-second stop torque. Add tangential cross-bracing, a wider torque-reaction path, or multiple distributed drive/brake stations; then repeat LC-STR-05.
2. **Misaligned docking exposes forward-spine bending flexibility.** The screening result is about 52.8 mm. A forward load-spreading frame, deeper truss section, or additional diagonal bays should be evaluated.
3. **Propulsion-boom stiffness is acceptable only provisionally.** The 12 kN load produces about 13.8 mm maximum displacement and 43.1 MPa screening stress. The displacement is close to the preliminary 15 mm limit and should be checked with joint flexibility and gimbal alignment requirements.
4. **Stress and member Euler margins are high in the idealised beam model.** This is expected because local joints, shell effects, bolt groups, welds, cut-outs and imperfections are absent. These global margins must not be applied to detailed hardware.
5. **The global first supported frequency is low.** Structural stiffening and realistic remote inertias may change mode order substantially. Free-free ANSYS analysis and MAC-based mesh correlation are mandatory.

## Required ANSYS correlation

- Global mass within 1% of the controlled mass ledger.
- Static displacement within 10% of the independent frame screening for matching assumptions.
- Member axial force within 10% at selected longerons.
- Final mesh displacement change below 2% and non-singular stress change below 5%.
- First ten flexible modal frequencies changing by less than 2% between final meshes.
- Six free-free rigid-body modes below 0.001 Hz.
- First physical buckling multiplier at least 2.0, followed by nonlinear imperfection sensitivity.

## Current design decision

Version 0.5 does not freeze the ring braking structure or forward docking load path. Both are explicitly carried as redesign actions into Version 0.8 optimisation. Version 0.6 may proceed because its thermal and CFD work is largely subsystem-based and does not depend on falsely declaring these structural issues solved.
