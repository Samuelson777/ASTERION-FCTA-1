# Reproducibility Guide

## Requirements

- Python 3.10 or newer for validation and screening scripts
- A modern browser for the GLB viewer
- Optional Siemens NX for native CAD/CAM reconstruction
- Optional ANSYS Mechanical and Fluent for authoritative analyses

## Validate the release

From the repository root:

```bash
python scripts/release/validate_release.py
```

The validator checks required files, published model assets, version metadata, artefact-status categories and checksum consistency.

## Serve the interactive portfolio locally

```bash
python -m http.server 8000 --directory web-viewer/v1_0
```

Then open `http://localhost:8000`.

## Re-run screening studies

Version-specific scripts remain under `scripts/python/`. Their Markdown reports document assumptions and expected outputs. Run them from the repository root unless their local README states otherwise.

## Rebuild native evidence

Follow the Siemens NX and ANSYS tutorials under `cad/` and `analysis/`. Record software version, mesh settings, solver settings, warnings and deviations from the baseline.
