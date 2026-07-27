# ASTERION FCTA-1 Native CAD Builder v1.1

This package converts the supplied ASTERION STL design geometry into **genuine native Siemens NX `.prt` files when the included NXOpen journal is run inside an installed and licensed copy of Siemens NX**.

## Correct Siemens NX file types

Siemens NX uses the `.prt` extension for:

- individual component parts;
- assembly master parts;
- drawings, whether stored with the model or as separate master-model drawing parts.

Therefore the NX outputs are named:

- `... .prt` — components;
- `AST-0000-ASTERION-FCTA-1-ASSY.prt` — assembly;
- `...-DRW.prt` — drawings.

Separate `.asm` and `.drw` files are not Siemens NX native formats. A Creo reference map is included for cases where PTC Creo was intended.

## What is included

- 16 controlled STL source files
- NX component manifest
- NX drawing manifest
- NXOpen native-file builder
- PowerShell NX launcher
- Native-output review checklist
- Expected output file list
- PTC Creo naming reference
- Package validator and checksums

## What is not included

No fake or renamed `.prt`, `.asm`, or `.drw` files are included. Native proprietary binary files cannot be produced without the corresponding CAD application. The NX journal performs the actual native save on your computer.

## Start here

Double-click `RUN_ASTERION_BUILDER.bat`. It discovers Siemens NX and runs the builder through the NX runtime.

Do **not** execute the journal with normal Python or VS Code's Run Python button. See [FIX_NXOPEN_MODULE_ERROR.md](docs/FIX_NXOPEN_MODULE_ERROR.md) and [RUN_IN_SIEMENS_NX.md](docs/RUN_IN_SIEMENS_NX.md).
