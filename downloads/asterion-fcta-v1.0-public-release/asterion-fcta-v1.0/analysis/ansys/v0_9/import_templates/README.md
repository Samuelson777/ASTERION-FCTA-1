# Version 0.9 ANSYS Result-Import Templates

Use these CSV files after running ANSYS Mechanical or Fluent on your PC. They are designed to keep screenshots, plots and solver outputs traceable to requirements.

Recommended workflow:
1. Run the relevant v0.5, v0.6 or v0.8 Workbench/APDL study.
2. Export mesh statistics, maximum values, convergence data and reaction summaries.
3. Fill the matching result template.
4. Link images and solver logs in the notes field.
5. Update `verification/v0_9/requirements_verification_matrix.csv` from **Closed by package** to **Closed by native solve** where applicable.

Do not mark an ANSYS case as complete unless the model solves, mesh checks pass, warnings are reviewed and the result is physically interpreted.
