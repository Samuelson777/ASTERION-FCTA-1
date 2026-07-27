# ANSYS Fluent Guide — ASTERION V0.6

## Cabin sector

1. Import the enclosure and obstruction STLs into SpaceClaim or Fluent Meshing.
2. Create a watertight internal fluid volume and named supply, return, crew, equipment and wall boundaries.
3. Use pressure-based coupled or SIMPLEC initially; enable energy and species transport.
4. Represent CO₂ as a dilute species in air.
5. For the rotating habitat case, use a rotating reference frame of 4.3 rpm about the spacecraft X-axis and confirm the radial acceleration direction.
6. Apply nominal 240 m³/h total supply, 291 K inlet temperature and 420 ppm CO₂.
7. Apply two 100 W crew heat sources, 600 W equipment heat, and total crew CO₂ generation of 40 L/h.
8. Monitor outlet mass flow, species balance, maximum CO₂ and occupied-zone values.
9. Compare the well-mixed nominal level with **587 ppm**, but expect local Fluent maxima to be higher.

## Skimmer

1. Import `skimmer_lifting_body_cfd_surface.stl` and create a half-model far field.
2. Place inlet/far-field boundaries at least 10 body lengths upstream and radially, and 20 lengths downstream for initial verification.
3. Use compressible air and the energy equation. Start with SST k-omega.
4. Use the static atmospheric properties in `skimmer_boundary_conditions.csv`.
5. Set reference area to 24 m² and reference length to 8 m.
6. Run -5°, 0°, 5°, 10° and 15° angle-of-attack cases.
7. Record CL, CD, Cm, L/D, residual histories and force-monitor stability.
8. At Mach 0.8 and Mach 2.0, refine shocks using density-gradient adaptation if cell limits permit.

## Convergence and quality

- global mass imbalance below 0.5%;
- energy imbalance below 1% when energy is active;
- stable force monitors, preferably below 0.5% variation over the final iterations;
- mesh-independent CL within 2% and CD within 5%;
- document y-plus and wall-treatment compatibility.
