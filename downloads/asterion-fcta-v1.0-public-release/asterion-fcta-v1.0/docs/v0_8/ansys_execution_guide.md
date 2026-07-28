# ANSYS Mechanical Version 0.8 Execution Guide

## Import

Use `analysis/ansys/v0_8/apdl/asterion_v0_8_optimized_line_model.inc` or reconstruct line bodies from the CSV node and element tables. Assign BEAM188 circular-tube sections and the controlled aluminium screening material.

## Connections and masses

Do not leave subsystem masses as free MASS21 elements. Couple each remote mass to its reviewed attachment frame. Run a joint-stiffness sensitivity with rigid, nominal and reduced-stiffness connections.

## Required analyses

1. LC-STR-02 propulsion thrust.
2. LC-STR-07 misaligned docking.
3. LC-STR-08 balanced counter-rotating ring braking.
4. LC-STR-09 single-ring brake fault.
5. Aft-supported modal analysis.
6. Free-free modal analysis.
7. Pre-stressed modal sensitivity for powered rotating operation.
8. Linear buckling screening followed by nonlinear local submodels where required.

## Mesh study

Use at least three beam subdivisions per 2.5 m bay for the first run. Refine until the controlling displacement and first flexible frequency change by less than 5%. Local joint submodels require shell or solid refinement independent of the global line model.

## Required result evidence

- deformation contours;
- beam axial force, bending moment and torsion;
- reaction-force balance;
- modal effective mass and mode descriptions;
- mesh-convergence table;
- analytical or Python correlation;
- solver warnings and unit audit;
- signed engineering interpretation.

The included Python values are correlation targets, not substitute ANSYS results.
