# Version 0.6 Thermal and CFD Analysis Plan

## Workbench systems

1. Steady-State Thermal — radiator system.
2. Transient Thermal — radiator deployment/heat step.
3. Steady-State Thermal — electronics cold plate.
4. Steady-State Thermal — habitat wall coupon.
5. Steady-State Thermal linked to Static Structural — thruster bracket.
6. Fluent — cabin nominal and degraded ventilation.
7. Fluent transient — cabin fan-loss case.
8. Fluent — Skimmer Mach 0.3.
9. Fluent — Skimmer Mach 0.8.
10. Fluent — Skimmer Mach 2.0.

## Execution order

- Validate geometry scale and named selections.
- Execute a coarse model and close mass/energy balances.
- Run the medium model and compare against the screening ranges.
- Run the fine model only after boundary conditions and monitors are stable.
- Populate the result templates and retain solver logs, residual histories and mesh statistics.
- Record discrepancies instead of tuning the model silently to match the screening calculation.

## Minimum evidence per case

- geometry screenshot;
- mesh and quality statistics;
- boundary-condition table;
- residual or convergence history;
- conservation error;
- principal contour and engineering interpretation;
- medium-to-fine mesh comparison;
- comparison with the supplied reduced-order calculation.
