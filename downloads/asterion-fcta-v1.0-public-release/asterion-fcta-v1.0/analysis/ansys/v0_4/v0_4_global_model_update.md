# ANSYS global-model update — Version 0.4

Version 0.4 adds subsystem mass and interface definitions to the Version 0.3 BEAM188 model. It does not contain solved Workbench databases.

## Recommended workflow

1. Import or execute the Version 0.3 line model.
2. Create named selections for each physical attachment frame.
3. Import `remote_mass_definitions.csv` and distribute each mass to the appropriate interface rather than coupling every mass to one spine node.
4. Use `asterion_v0_4_remote_masses.mac` only as a coordinate and mass seed. Replace free-standing MASS21 elements with reviewed coupling equations or Workbench Remote Mass objects.
5. Run free-free modal analysis first. Confirm six rigid-body modes and inspect local mass-decoupled modes.
6. Repeat docking, thrust, ring-rotation and emergency-braking load cases with the V0.4 mass state.
7. Perform sensitivity runs for joint stiffness, ring-bearing stiffness and solar/radiator stowed versus deployed states.

## Mass checkpoints

- Dry docked estimate: 50542.0 kg
- Full-propellant estimate: 62542.0 kg
- Dry CG: (2.0775, -0.0001, 0.0001) m
- Full-propellant CG X: -0.0480 m

The point-mass model is appropriate for global load-path and modal screening only. Local brackets, pressure shells, deployment hinges, bearings and tank saddles require separate shell/solid submodels.
