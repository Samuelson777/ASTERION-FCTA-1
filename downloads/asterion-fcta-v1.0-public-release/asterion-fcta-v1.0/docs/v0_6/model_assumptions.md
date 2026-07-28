# Version 0.6 Model Assumptions

## General

- All calculations are preliminary portfolio-level engineering studies.
- SI units are used in analysis tables; neutral STL geometry is authored in millimetres.
- Material properties are constant screening values unless the ANSYS user replaces them with temperature-dependent data.
- Solver results must be independently reviewed and recorded in the supplied templates.

## Thermal

- Radiator effective emitting area assumes both panel faces have an unobstructed view to space.
- The solar load is a low-incidence operational case, not worst-case Sun pointing.
- Spacecraft internal heat is distributed evenly for the first model.
- MLI is initially represented by an equivalent conductivity and must later be correlated.
- Contact resistance and coolant manifolds are simplified until detailed CAD is available.

## Cabin CFD

- The first zonal calculation assumes perfect mixing; Fluent is required to resolve local pockets.
- CO₂ generation is set to 20 L/h per crew member for screening.
- Two supply diffusers share the nominal volumetric flow.
- Cabin walls are controlled near 295 K in the first CFD case.
- The rotating-ring case uses 4.3 rpm and a 12 m occupied radius.

## Skimmer CFD

- The lifting-body surface is a concept loft, not a certified aerodynamic shape.
- Air is treated as calorically perfect for Mach 0.3, 0.8 and 2.0 cases.
- Mach 2 is a simplified supersonic study, not high-enthalpy re-entry.
- Surface roughness, transition, real-gas chemistry and ablation are excluded.
- Forces are normalised to 24 m² reference area and 8 m reference length.
