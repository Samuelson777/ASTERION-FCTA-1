# Version 0.3 Structural Design Basis

## Purpose

Define a lightweight, modular primary structure that can be rebuilt in Siemens NX and analysed on a home PC with ANSYS Student-class model limits.

## Design philosophy

1. Use orbit assembly; do not design the complete vehicle as a single launch stack.
2. Keep the first global model beam-dominant and auditable.
3. Separate global load-path verification from local joint, shell and contact models.
4. Make interfaces replaceable and parameter-driven.
5. Treat all material properties and load levels as preliminary until source-controlled project values are selected.

## Structural arrangement

- Central truss: eight longerons at 1.2 m radius.
- Bay spacing: nominally 2.5 m, with extra interface stations.
- Frames: octagonal beam frames at each station.
- Bracing: alternating diagonal lattice between stations.
- Rotating rings: 12-segment circumference frames at 12 m occupied radius.
- Ring supports: 12 radial spokes per ring with hub links to the central truss.
- Propulsion frame: six radial mounts at X = -16 m.
- Docking frame: eight linked nodes at X = +21.4 m.

## Preliminary material

The model uses a conceptual aluminium 7075-T6 isotropic card:

- Elastic modulus: 71.7 GPa
- Poisson ratio: 0.33
- Density: 2810 kg/m³
- Screening yield strength: 503 MPa

These values are not a procurement specification. Update them for temperature, product form, thickness, direction, joining process and supplier certification.

## Mass statement

The beam idealisation mass is 7,742.3 kg. It excludes joints, fittings, bearing hardware, pressure shells, fasteners, mechanisms, harnesses, coatings, local reinforcement and manufacturing allowances. It must not be quoted as complete spacecraft structural mass.
