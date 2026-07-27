# ANSYS Analysis Matrix

| Study ID | Model | Physics | Main outputs | Validation | Home-PC reduction |
|---|---|---|---|---|---|
| ANS-001 | Central spine | Static structural | Stress, deformation, reactions, FoS | Beam theory | Beam/shell idealisation |
| ANS-002 | Central spine | Modal | First 10 modes, participation | Simple beam frequency | Reduced mass model |
| ANS-003 | Solar mast | Linear buckling | Buckling factors and modes | Euler buckling | One mast only |
| ANS-004 | Habitation ring | Rotating structural | Hoop stress, spoke forces, distortion | Thin-ring estimate | Cyclic sector or simplified ring |
| ANS-005 | Radiator panel | Thermal + structural | Temperature, heat flow, thermal stress | Energy balance | One panel |
| ANS-006 | Cabin module | Internal CFD | Velocity, temperature, recirculation | Flow balance | Single representative cabin |
| ANS-007 | Skimmer | External CFD | CL, CD, Cm, pressure, shocks | Hand estimate / literature trend | Half model and staged mesh |
| ANS-008 | Docking interface | Transient structural | Contact force, deformation, energy | Energy balance | Local model only |
| ANS-009 | Gimbal bracket | Static + optimisation | Stress, mass, sensitivity | Closed-form bracket estimate | Local solid model |
| ANS-010 | Skimmer rib | Static + buckling | Stress, deflection, buckling | Beam/plate estimate | One rib |

## Standard result package

Each study should contain:

- Geometry assumptions
- Material model
- Boundary conditions
- Mesh statistics
- Mesh-sensitivity comparison
- Solver controls
- Convergence evidence
- Result contours
- Tabulated peak values
- Hand calculation or benchmark
- Engineering interpretation
- Limitations
