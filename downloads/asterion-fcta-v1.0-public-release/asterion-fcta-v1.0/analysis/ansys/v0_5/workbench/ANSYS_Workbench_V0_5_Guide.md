# ASTERION FCTA-1 V0.5 — ANSYS Workbench Structural Analysis Guide

## Purpose

This guide converts the V0.3 BEAM188 primary-structure model and V0.4 subsystem mass state into a controlled V0.5 structural-analysis project. The supplied project contains no claimed solved ANSYS database. Results must be generated and reviewed on the user's licensed ANSYS installation.

## Recommended project systems

Create one Engineering Data cell and connect it to:

1. Static Structural — docking compression.
2. Static Structural — electric-propulsion thrust.
3. Static Structural — twin-ring centrifugal loading.
4. Static Structural — ring emergency braking.
5. Static Structural — misaligned docking.
6. Modal — free-free flight model.
7. Modal — aft-supported ground-test model.
8. Eigenvalue Buckling — linked from docking static pre-stress.

Duplicate systems for mesh and joint-stiffness sensitivity instead of overwriting evidence.

## Units and material

Use mm, N, s and tonne consistently in APDL imports. The preliminary material is aluminium 7075-T6 with E = 71,700 MPa, ν = 0.33, density = 2.81×10⁻⁹ tonne/mm³ and room-temperature yield screening strength = 503 MPa. Replace this with temperature- and product-form-specific allowables before making design claims.

## Global line model

Import or execute `analysis/ansys/v0_3/apdl/asterion_line_model.inc`. Confirm:

- 222 structural nodes;
- 580 BEAM188 elements;
- seven tube section families;
- no zero-length or duplicate elements;
- beam orientation is consistent; and
- section assignment matches `beam_sections.csv`.

## Non-structural masses

Use `analysis/ansys/v0_4/model/remote_mass_definitions.csv` as the mass ledger. Prefer Mechanical Remote Mass objects connected to reviewed attachment frames. The included MASS21 macro is a seed only; uncoupled mass nodes are invalid.

For the rotating habitation sectors, place mass at the ring nodes and include centrifugal acceleration. For modal analysis, include suitable rotary inertia estimates once the subsystem geometry is available.

## Supports

The aft-fixed support is a ground-test/screening boundary condition. It is not a realistic flight condition. For flight static studies, use a minimum 3-2-1 stabilisation scheme or inertia relief and confirm reactions do not dominate the reported load path.

## Required result objects

For every static case request:

- total deformation;
- directional deformation X/Y/Z;
- equivalent stress;
- beam axial force;
- beam bending moment and torsion;
- reaction forces and moments;
- interface loads; and
- factor-of-safety user result.

For modal studies request at least 16 modes, participation factors and effective mass. For free-free analysis, the first six modes must be rigid-body modes near zero frequency.

## Mesh convergence

Run B1, B2 and B3 from `mesh_convergence_plan.csv`. Compare a physically meaningful displacement, member force, first ten flexible frequencies and non-singular stress. A converged contour picture alone is not sufficient.

## Buckling

Link Eigenvalue Buckling to LC-STR-01 pre-stress. Inspect mode shapes and reject local numerical artefacts. A positive eigenvalue above the criterion does not prove stability; follow with geometric nonlinearity and seeded imperfections in V0.8.

## Evidence capture

Complete the CSV templates in `results_templates/`. Save screenshots showing model tree, mesh statistics, boundary conditions, solver messages, deformation scale, legends and probe locations. Record the exact ANSYS release and project checksum.

## Student-computer strategy

Keep the global model as beams. Use shells only for ring hubs and docking frames, then solids only as local submodels. Do not solve the complete spacecraft as a detailed solid mesh.
