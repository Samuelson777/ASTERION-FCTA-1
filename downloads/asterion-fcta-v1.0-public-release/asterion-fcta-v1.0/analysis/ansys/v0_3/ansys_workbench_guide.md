# ANSYS Workbench Guide — Version 0.3

## Preferred workflow

1. Start with a Mechanical line-body model reconstructed from `model/beam_nodes.csv` and `model/beam_elements.csv`, or execute the supplied APDL include.
2. Confirm millimetre, newton, second unit consistency.
3. Create the seven circular-tube beam sections from `beam_sections.csv`.
4. Apply the preliminary aluminium material from `material_properties.csv`.
5. Create named selections using `named_selections.csv`.
6. Solve one load case at a time and export result tables and screenshots into a new `results/` folder.

## Static docking demonstration

- Aft frame fixed only for a ground-test-style benchmark.
- Apply 25 kN total compression to the forward docking-frame nodes.
- Request total deformation, directional deformation, beam axial force, bending moment, reaction force and safety-factor screening.
- Verify reaction-force balance before interpreting stress.

## Free-free modal demonstration

Use no supports. Extract at least 16 modes. The first six should represent rigid-body behaviour near zero frequency. Review mode shapes rather than only reading frequencies.

## Buckling demonstration

Use the docking static solution as the prestress state and extract ten eigenvalue buckling modes. Label the factors as ideal linear screening. Later work must introduce geometric imperfections and nonlinear material/contact behaviour where relevant.

## Home-PC strategy

- Keep the global structure as line bodies.
- Use shell submodels only for selected panels.
- Use solid meshes only at joints and interfaces.
- Avoid merging every future subsystem into one Mechanical model.
- Maintain a mesh/refinement log for every reported result.
