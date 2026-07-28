# Siemens NX Master Skeleton — Version 0.2

This package defines the controlled top-down geometry for ASTERION FCTA-1.

## Included

- Named expression seed file
- Stable vehicle station table
- Coordinate-system table
- Interface-point table
- Keep-out envelope table
- WAVE publication map
- NX assembly and layer standards
- Detailed NX build tutorial
- NXOpen wireframe journal starter
- Neutral GLB, STL, and OBJ envelope geometry
- Separate subsystem STL envelopes
- Plan and front-view DXF/SVG references
- Model-audit checklist

## Correct use

1. Create a new metric NX part named `AST-0000-MASTER-SKELETON.prt`.
2. Build native NX datums and expressions using the tutorial.
3. Use the included journal only as a wireframe accelerator, not as the final feature tree.
4. Import neutral geometry into a reference-only part or reference set.
5. Create detailed parts by WAVE-linking approved skeleton objects.
6. Do not let detailed parts drive master geometry.

## Limitation

Native `.prt` files cannot be authored or validated here because Siemens NX is not installed in this environment. The neutral geometry and NXOpen journal provide reproducible inputs for the native build on your PC.
