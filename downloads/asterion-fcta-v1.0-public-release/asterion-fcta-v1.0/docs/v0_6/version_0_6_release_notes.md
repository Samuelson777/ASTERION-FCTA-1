# ASTERION FCTA-1 Version 0.6 Release Notes

Version 0.6 adds the thermal-control and fluid-dynamics execution package.

## Added

- Six-panel radiator heat-rejection screening and degradation case.
- Electronics cold-plate, habitat-wall and thruster-bracket thermal checks.
- Cabin CO₂ transient and ventilation flow screening.
- Skimmer Mach 0.3, 0.8 and 2.0 aerodynamic coefficient and force estimates.
- ANSYS Mechanical and Fluent case matrices, boundary conditions, mesh plans and result templates.
- Neutral thermal and CFD preparation geometry.
- Four engineering plots and reproducible Python scripts.

## Principal findings

- Nominal radiator equilibrium: **361.38 K**.
- Five-panel degraded radiator equilibrium: **377.91 K**.
- Nominal cabin well-mixed CO₂: **587 ppm**.
- Degraded cabin well-mixed CO₂: **920 ppm**.
- Fan loss reaches 1000 ppm about **27.9 minutes** after loss from nominal steady state.
- The Mach 0.8 Skimmer case is expected to be the most drag- and mesh-sensitive of the three initial external-flow cases.

## Limitations

No solved ANSYS Mechanical or Fluent database is represented as completed. All numerical outputs in `calculations/v0_6` are independent reduced-order screening results.
