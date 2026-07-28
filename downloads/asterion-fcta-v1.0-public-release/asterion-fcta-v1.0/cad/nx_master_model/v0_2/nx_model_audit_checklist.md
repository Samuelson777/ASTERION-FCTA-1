# NX Master-Skeleton Audit Checklist

## Identity and units

- [ ] Part name is `AST-0001-MASTER-SKELETON.prt`.
- [ ] Modelling units are millimetres.
- [ ] +X forward, +Y starboard, +Z up.
- [ ] Project version attribute equals 0.2.

## Parameters

- [ ] All required named expressions exist.
- [ ] Derived values remain formula-driven.
- [ ] No duplicate expressions with different units.
- [ ] A 5% ring-diameter change updates both rings and all sector geometry.

## Datums and geometry

- [ ] All eight station planes exist and are named correctly.
- [ ] Ring centres remain at STA_30 and STA_40.
- [ ] Solar wing tips produce a nominal 58 m deployed span.
- [ ] Propulsion pod axes form an equal six-position pattern.
- [ ] Skimmer docking interface is located at STA_70.

## Associativity

- [ ] Detailed parts consume skeleton geometry through WAVE links.
- [ ] No detailed part drives the master skeleton.
- [ ] Imported neutral geometry is reference-only.
- [ ] Broken or out-of-date links are zero.

## Clearance and release

- [ ] Deployed arrays do not intersect ring envelopes.
- [ ] Nominal thruster plume cones do not intersect solar or radiator envelopes.
- [ ] Hard-interference count is zero for envelope assembly.
- [ ] Stowed and deployed arrangements regenerate without errors.
- [ ] Neutral export, screenshots and audit record are committed.
