# PTC Creo note: `.prt`, `.asm` and `.drw`

The exact extension set requested—`.prt`, `.asm`, and `.drw`—matches a typical PTC Creo workflow rather than Siemens NX.

This package does not generate Creo binaries because Creo is not available in the generation environment. If Creo is the intended target, import the files in `source_stl` as facet geometry or first convert/rebuild them as STEP/Parasolid solids, then save using the names in `CREO_EXPECTED_FILE_MAP.csv`.

For editable Creo models, rebuild the critical parts parametrically rather than treating STL imports as production solids.
