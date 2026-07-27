# ANSYS Mechanical Thermal Guide — ASTERION V0.6

## Radiator model

1. Import `radiator_panel_6m_x_2m.stl` or rebuild a mid-surface panel in SpaceClaim/NX.
2. Use shell or thin-solid elements; model one panel first and scale to six.
3. Apply emissivity 0.88 to both radiating faces and a 3 K ambient radiation sink.
4. Apply the internal heat share and the solar heat flux from `thermal_boundary_conditions.csv`.
5. Request temperature, directional heat flux, total heat flow and thermal balance.
6. Compare the full-system equivalent result with **361.38 K**.

## Cold plate

1. Replace the block geometry with explicit channels when available.
2. Apply 1.8 kW at the electronics interface.
3. Use either convection to a 303 K bulk coolant or couple to Fluent for conjugate heat transfer.
4. Add contact resistance studies at the electronics interface.
5. Compare hotspot temperature with the reduced-order value of **324.60 K**.

## Habitat wall

1. Create separate bonded layers so interface temperatures can be extracted.
2. Use at least three elements through each ordinary solid layer.
3. Treat the MLI layer as an equivalent model only.
4. Compare mean heat flux with **1.298 W/m²**.

## Thruster bracket thermal stress

1. Solve the thermal field first.
2. Transfer temperature to Static Structural.
3. Apply realistic attachment constraints, bolt preload and contact when available.
4. Compare the restrained screening stress of **22.85 MPa**, while recognising that real local peak stresses may be higher.

## Acceptance

- heat-balance error below 2% for steady cases;
- medium-to-fine key-result change below 2% for temperature and 5% for local stress;
- no unreviewed singular peak used for design margin;
- all assumed material properties documented.
