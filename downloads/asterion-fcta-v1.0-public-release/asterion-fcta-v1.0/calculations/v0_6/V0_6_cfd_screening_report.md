# ASTERION V0.6 CFD Screening Report

## Status and limitation

The cabin results are well-mixed-zone calculations. The Skimmer results use a reduced-order coefficient model. Neither is a solved Fluent result. They provide numerical checks and expected ranges for the ANSYS Fluent studies.

## Cabin ventilation and CO₂

The reference sector volume is 45.0 m³ with two crew members, each producing 20 L/h CO₂ in the screening case.

| Condition | Flow | Predicted steady CO₂ |
|---|---:|---:|
| Normal | 240 m³/h | 587 ppm |
| Degraded | 80 m³/h | 920 ppm |
| Fan loss | 0 m³/h | 1000 ppm reached about 27.9 min after loss from nominal steady state |

At the nominal flow, two 0.12 m² supply diffusers produce an average inlet speed of **0.278 m/s**. An air-only energy balance for 800 W gives a **10.1 K** rise, showing that cooled walls or a dedicated heat exchanger must remove much of the sensible heat.

The Fluent cabin model should use species transport for CO₂, energy, heat sources and the ring rotating frame. Report occupied-zone distributions rather than only domain averages.

## Skimmer external aerodynamics

The reference lifting-body area is 24.0 m² and length is 8.0 m. The coefficient model is intended only to seed expected force ranges.

| case_id   |   mach |   altitude_km |   static_temperature_K |   static_pressure_Pa |   density_kg_m3 |   velocity_m_s |   dynamic_pressure_Pa |   Reynolds_number_L8m |   alpha_reference_deg |   CL_screening |   CD_screening |   L_over_D_screening |   lift_kN |   drag_kN |   stagnation_temperature_K |
|:----------|-------:|--------------:|-----------------------:|---------------------:|----------------:|---------------:|----------------------:|----------------------:|----------------------:|---------------:|---------------:|---------------------:|----------:|----------:|---------------------------:|
| CFD-SK-01 |    0.3 |            10 |                  223.1 |            2.644e+04 |         0.4127  |          89.84 |                  1665 |             2.036e+07 |                     5 |         0.2967 |        0.03732 |                7.949 |     11.86 |     1.492 |                      227.2 |
| CFD-SK-02 |    0.8 |            15 |                  216.7 |            1.204e+04 |         0.1937  |         236.1  |                  5396 |             2.573e+07 |                     5 |         0.2793 |        0.06248 |                4.47  |     36.16 |     8.091 |                      244.4 |
| CFD-SK-03 |    2   |            25 |                  221.7 |         2511         |         0.03947 |         596.9  |                  7031 |             1.301e+07 |                     5 |         0.192  |        0.08737 |                2.197 |     32.4  |    14.74  |                      399   |

The Mach 0.8 case includes a provisional drag-rise term and therefore has lower lift-to-drag ratio than the low-subsonic case. The Mach 2 model is not a re-entry solution: chemistry, ablation, radiative heating and high-enthalpy effects are excluded.

## Design actions

1. Improve vent placement if Fluent identifies recirculation or CO₂ pockets near bunks and exercise equipment.
2. Provide at least two independently powered flow paths and emergency CO₂ scrubbing.
3. Use a half-model far field for the Skimmer to stay within home-PC mesh limits.
4. Run angle-of-attack sweeps at -5°, 0°, 5°, 10° and 15° before adding control-surface deflections.
5. Treat Mach 0.8 as the most mesh-sensitive case because shock location and drag rise are sensitive to surface resolution.
6. Do not describe the Mach 2 case as validated re-entry aerothermodynamics.
