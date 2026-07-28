# ASTERION Version 0.3 Preliminary Structural Sizing

## Status

These calculations define a **portfolio-level preliminary structure**. They are not flight certification, pressure-vessel substantiation, fracture-control approval, or human-rating evidence.

## Baseline model

- Eight aluminium longerons around a 1.2 m truss radius.
- Nominal 2.5 m truss bays, with added stable interface stations.
- Octagonal transverse frames and alternating diagonal braces.
- Two 12-sector rotating-ring frames at X = -2.5 m and +2.5 m.
- Twelve spokes per ring, with local hub links to the central truss.
- Six propulsion load-transfer booms at X = -16 m.
- Dedicated forward docking frame at X = +21.4 m.

## Generated line model

| Metric | Value |
|---|---:|
| Nodes | 222 |
| BEAM188 elements | 580 |
| Spine/interface stations | 21 |
| Maximum bay length | 2.500 m |
| Estimated idealised tube mass | 7,742.3 kg |

The mass excludes joints, fittings, bearing races, pressure shells, fasteners, harnesses, local reinforcement, coatings, mechanisms and manufacturing allowances. Apply a maturity allowance before using it in a system mass budget.

## Rotating-ring dynamics

For radius r = 12 m and rotation rate 4.3 rpm:

- Angular speed: 0.45029 rad/s
- Tangential speed: 5.404 m/s
- Centrifugal acceleration: 2.433 m/s² = 0.248 g
- Design rotating mass per ring: 12,000 kg
- Total distributed radial force per ring: 29,198.2 N
- Equivalent radial force per outer node: 2,433.2 N
- Uniform-ring hoop tension estimate: 4,647.0 N
- 120 s emergency braking torque: 6,484.2 N·m

The spoke analysis must also include local cabin-sector masses and imbalance; the uniform-ring equation alone is not sufficient for detailed design.

## Longeron screening calculation

Selected conceptual longeron: 160 mm outside diameter, 6 mm wall aluminium tube.

| Quantity | Value |
|---|---:|
| Area | 2,902.8 mm² |
| Second moment of area | 8.619e+06 mm⁴ |
| Radius of gyration | 54.49 mm |
| Docking load per longeron | 3,125.0 N |
| Direct compressive stress | 1.077 MPa |
| Yield screening factor | 467.2 |
| Euler pinned-pinned critical load | 975.8 kN |
| Euler buckling screening factor | 312.3 |

This simple screening ignores joint eccentricity, imperfections, local shell buckling, load redistribution and combined bending. ANSYS model correlation and local joint submodels are required before any design claim.

## Required Version 0.5 correlation

1. Compare beam-model axial displacement with a hand truss calculation.
2. Complete mesh/refinement studies for line, shell and local solid models.
3. Check free-free modes and identify the first six rigid-body modes.
4. Replace ideal rigid joints with realistic joint stiffness sensitivity cases.
5. Run linear buckling, then nonlinear imperfection sensitivity on critical members.
6. Perform local stress checks at ring hubs, propulsion booms and docking links.
