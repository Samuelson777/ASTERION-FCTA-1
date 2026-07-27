# ASTERION FCTA-1

**A modular, orbit-assembled deep-space spacecraft and detachable lifting-body aeroshuttle CAD/CAM/CAE portfolio project.**

[![Release](https://img.shields.io/badge/release-v1.0.0-4c9ffe)](#release-status)
[![Licence](https://img.shields.io/badge/licence-MIT-green)](LICENSE)
[![Project type](https://img.shields.io/badge/type-engineering%20demonstrator-orange)](docs/v1_0/governance/CLAIMS_AND_LIMITATIONS.md)

ASTERION FCTA-1 demonstrates a complete aerospace engineering workflow across Siemens NX, ANSYS, NX CAM, Python calculations, neutral CAD publication, manufacturing planning, verification records and an interactive GitHub Pages portfolio.

## Release status

Version **1.0.0** is the first public, GitHub-ready baseline. It packages all generated neutral models, calculations, CAM planning data, validation templates, reports and presentation assets developed from Versions 0.1–0.9.

The repository is complete as an **open-source portfolio baseline**. Native Siemens NX parts/assemblies and solved ANSYS databases remain owner-generated evidence because those proprietary applications are not installed in this environment.

## Engineering scope

- Parametric master skeleton and top-down assembly strategy
- Central truss, twin counter-rotating habitation rings and subsystem interfaces
- Full spacecraft assembly and detachable Skimmer lifting-body aeroshuttle
- Static, modal, buckling, thermal and CFD analysis preparation
- Independent Python structural, thermal and aerodynamic screening
- NX CAM planning for four representative aerospace components
- Drawings, tooling, fixtures, inspection plans and printable prototypes
- Requirements traceability, risks, design review and release governance
- Interactive browser-based GLB model viewer

## Key configuration values

| Parameter | Public baseline |
|---|---:|
| Full docked geometry envelope | 51.7 m |
| Deployed solar span | 57.8 m |
| Habitation ring diameter | 26 m |
| Updated dry docked mass | 53,223 kg |
| First supported screening mode | 0.1964 Hz |
| Electric-propulsion pods | 6 |
| Habitation sectors | 24 |
| NX CAM demonstrators | 4 |

## Start here

1. Read the [portfolio summary](docs/v1_0/portfolio/PORTFOLIO_SUMMARY.md).
2. Review [claims and limitations](docs/v1_0/governance/CLAIMS_AND_LIMITATIONS.md).
3. Open `web-viewer/v1_0/index.html` through a local web server or deploy it with the included GitHub Pages workflow.
4. Use the [native execution evidence checklist](docs/v1_0/evidence/NATIVE_EXECUTION_EVIDENCE_CHECKLIST.md) while rebuilding and solving the project in Siemens NX and ANSYS.
5. Run `python scripts/release/validate_release.py` before publishing a modified release.

## Repository map

```text
cad/                 neutral CAD, NX parameters and drawings
analysis/            ANSYS setup data, APDL templates and result records
calculations/        mass, CG, screening and optimisation results
cam/                 NX CAM tools, operations, fixtures and inspection plans
prototype/           printable demonstrators and test planning
docs/                engineering reports, governance and release guidance
media/               figures, renders, plots, animation and presentation assets
scripts/             reproducibility, screening and release validation tools
verification/        requirements matrices and release validation evidence
web-viewer/           interactive GitHub Pages portfolio
```

## Boundary of claims

ASTERION is an engineering demonstrator—not a certified spacecraft, operational aircraft, flight-qualified propulsion system or unrestricted-travel claim. Reduced-order results are screening calculations. Native NX/ANSYS evidence must be generated and reviewed on the project owner's workstation.

## Citation

Use the metadata in [`CITATION.cff`](CITATION.cff). Author credit: **Samuelson G**.

## Licence

Original repository code and documentation are released under the MIT Licence. Third-party runtime dependencies and proprietary software remain under their own licences; see [`LICENSES/THIRD_PARTY_NOTICES.md`](LICENSES/THIRD_PARTY_NOTICES.md).
