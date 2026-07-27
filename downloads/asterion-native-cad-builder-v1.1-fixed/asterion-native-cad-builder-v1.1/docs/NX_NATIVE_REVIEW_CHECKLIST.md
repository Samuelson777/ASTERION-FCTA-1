# NX native output review checklist

## Parts

- [ ] Every `.prt` opens without a missing-reference warning.
- [ ] Units are millimetres.
- [ ] Imported facet/convergent bodies are visible.
- [ ] Geometry extents match the source model.
- [ ] No component is accidentally scaled by 1,000 or 0.001.
- [ ] Critical bodies pass Examine Geometry or the appropriate facet-body check.

## Assembly

- [ ] `AST-0000-ASTERION-FCTA-1-ASSY.prt` opens all components.
- [ ] Eleven subsystem components appear in the Assembly Navigator.
- [ ] All components are placed at the absolute origin.
- [ ] The full vehicle matches the Version 0.4/1.0 reference renders.
- [ ] Solar span, ring diameter and vehicle centreline are consistent.
- [ ] Reference sets and component names are suitable for your NX release.

## Drawings

- [ ] Drawing files use the `-DRW.prt` suffix.
- [ ] Each drawing contains its linked master-model component.
- [ ] A3 sheet exists.
- [ ] Front, top and right views are present.
- [ ] View scale is appropriate.
- [ ] Add title block, border, projection symbol, units, revision and author.
- [ ] Add dimensions and GD&T only from controlled engineering definitions—not by measuring a coarse STL blindly.

## Portfolio evidence

- [ ] Capture NX Part Navigator screenshots.
- [ ] Capture Assembly Navigator screenshot.
- [ ] Capture drawing sheets.
- [ ] Record NX version and licence configuration.
- [ ] Commit only files that your licence permits you to distribute.
