# NX Layers and Reference Sets

## Layers

| Layer | Purpose |
|---:|---|
| 1 | Current solid or active construction geometry |
| 10 | Vehicle axes, station references, global datums |
| 20 | Habitation-ring envelopes and rotation axes |
| 30 | Solar-array hinges, panels, swept envelopes |
| 40 | Propulsion interfaces, pod axes, plume keep-outs |
| 50 | Skimmer envelope, control surfaces, docking geometry |
| 60 | Radiator envelopes and thermal interfaces |
| 70 | Maintenance, robotic-access and removal envelopes |
| 80 | Interface-control geometry and bolt circles |
| 90 | Imported neutral reference geometry |
| 200–219 | Construction and temporary geometry |

## Reference sets

- `EMPTY`: no visible geometry.
- `SKELETON`: approved datums, axes, curves, points and interface sketches.
- `ENVELOPES`: simplified subsystem and keep-out bodies.
- `INTERFACES`: interface points, planes and bolt circles only.
- `MODEL`: all approved master-model objects.

Neutral STL/OBJ geometry must remain on reference layer 90 and must never become the associative design authority.
