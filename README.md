# ASTERION FCTA-1

## Field-Coupled Transit Architecture  
### A Modular Multi-Regime Spacecraft CAD/CAM/CAE Demonstrator

![Project Status](https://img.shields.io/badge/status-v1.0%20public%20release-success)
![CAD](https://img.shields.io/badge/CAD-Siemens%20NX-blue)
![CAE](https://img.shields.io/badge/CAE-ANSYS-orange)
![CAM](https://img.shields.io/badge/CAM-NX%20CAM-lightgrey)
![Web](https://img.shields.io/badge/web-HTML%20%7C%20CSS%20%7C%20JavaScript-yellow)
![License](https://img.shields.io/badge/license-MIT-green)
![Project Type](https://img.shields.io/badge/type-open--source%20engineering%20portfolio-purple)
[ASTERION FCTA-1 Web](https://samuelson777.github.io/ASTERION-FCTA-1/)
[License](https://github.com/Samuelson777/ASTERION-FCTA-1/blob/main/LICENSE)

**Author:** Samuelson G  
**Project version:** 1.0  
**Project domain:** Aerospace engineering, aeronautics, spacecraft systems, CAD, CAM, CAE, simulation, optimisation, digital manufacturing, and interactive 3D visualisation

---

## Overview

**ASTERION FCTA-1** is an open-source multidisciplinary aerospace engineering project developed to demonstrate a complete spacecraft design workflow using **Siemens NX**, **ANSYS**, **NX CAM**, Python, HTML, CSS, JavaScript, and browser-based 3D technologies.

The project explores a modular, orbit-assembled, multi-regime spacecraft intended for long-duration operations beyond low Earth orbit. It combines:

- A central non-rotating structural spine
- Twin counter-rotating habitation rings
- Modular electric-propulsion pods
- Large deployable solar-power wings
- Deployable thermal-control radiators
- Radiation-protection and storm-shelter systems
- Docking, logistics, robotics, and maintenance systems
- A detachable lifting-body aeroshuttle named **Skimmer**
- Parametric CAD, structural analysis, thermal analysis, CFD, CAM, optimisation, and manufacturing documentation

ASTERION is presented as a **conceptual CAD/CAM/CAE demonstrator and engineering portfolio**, not as a flight-qualified spacecraft or a proven reactionless-propulsion system.

---

## Project Objectives

The main objectives of ASTERION FCTA-1 are to:

1. Demonstrate advanced Siemens NX modelling and assembly skills.
2. Demonstrate ANSYS structural, thermal, modal, buckling, and CFD workflows.
3. Demonstrate NX CAM process planning and manufacturing preparation.
4. Integrate spacecraft systems engineering with aeronautical vehicle design.
5. Build a reproducible engineering project that can be developed on a home PC.
6. Publish neutral CAD geometry, technical documentation, scripts, drawings, and results openly.
7. Present the complete project through an interactive GitHub Pages 3D application.
8. Clearly separate verified artefacts, reduced-order screening results, conceptual assumptions, and native-software work still requiring execution.

---

## Engineering Concept

ASTERION is based on the idea that a deep-space vehicle should not be treated as a single-use rocket.

Instead, the spacecraft is divided into serviceable modules that can be launched separately, assembled in orbit, upgraded, repaired, and reconfigured for different missions.

### Main configuration

| Parameter | Baseline value |
|---|---:|
| Overall docked length | Approximately 51.7 m |
| Habitation-ring diameter | 26 m |
| Occupied ring radius | 12 m |
| Ring speed | Approximately 4.3 rpm |
| Artificial gravity | Approximately 0.248 g |
| Deployed solar span | Approximately 57.8 m |
| Propulsion pods | 6 |
| Solar wings | 4 |
| Radiator assemblies | 6 |
| Habitation sectors | 24 |
| Reference crew | 4 |
| Dry docked mass after redesign | Approximately 53.2 tonnes |
| Full-propellant mass | Approximately 65.2 tonnes |
| Primary propulsion | Modular electric propulsion |
| Atmospheric vehicle | Detachable Skimmer lifting body |

These values are preliminary design targets and are not certification data.

---

## System Architecture

### Central structural spine

The non-rotating central spine provides:

- Primary spacecraft load transfer
- Module attachment stations
- Docking interfaces
- Propulsion load paths
- Power and data routing
- Thermal-fluid routing
- Robotic servicing access
- Solar-array and radiator support
- Reaction-control-system mounting

### Counter-rotating habitation rings

Two habitation rings rotate in opposite directions to reduce net angular momentum.

The rings contain conceptual provisions for:

- Crew cabins
- Exercise facilities
- Medical support
- Hygiene systems
- Food storage
- Workstations
- Hydroponics
- Water shielding
- Radiation-refuge access
- Emergency braking and bearing systems

### Propulsion system

The propulsion architecture uses detachable electric-propulsion pods.

Each pod conceptually includes:

- Electric thrusters
- Gimbal mechanism
- Power-processing equipment
- Propellant storage
- Local thermal control
- Service interfaces
- Structural load-transfer attachments

### Power and thermal control

The spacecraft uses:

- Four deployable solar wings
- Distributed electrical buses
- Battery and emergency-power provisions
- Six radiator assemblies
- Electronics cold plates
- Coolant manifolds
- Degraded-operation modes

### Skimmer aeroshuttle

The Skimmer is a detachable lifting-body aeroshuttle included to demonstrate aeronautical design skills.

Reference dimensions:

| Parameter | Value |
|---|---:|
| Length | 8.0 m |
| Maximum width | 5.5 m |
| Height | Approximately 2.1 m |
| Reference area | Approximately 24 m² |
| Control surfaces | Elevons and split rudders |
| Configuration | Blended lifting body |

---

## Software and Technologies

### CAD and digital mock-up

- Siemens NX
- NXOpen Python journals
- STEP, STL, OBJ, GLB, DXF, and SVG
- Parametric expressions
- WAVE geometry linking
- Top-down assembly design
- Reference sets and arrangements
- Product and Manufacturing Information
- Engineering drawings and BOMs

### CAE and simulation

- ANSYS Mechanical
- ANSYS Fluent
- ANSYS APDL
- Python-based independent screening models
- Static structural analysis
- Modal analysis
- Linear buckling
- Thermal analysis
- Thermal-stress analysis
- Cabin ventilation CFD
- CO₂ transport screening
- External aerodynamics

### CAM and manufacturing

- Siemens NX CAM
- Milling and turning process plans
- Tool libraries
- Fixture and workholding concepts
- Setup sheets
- Inspection planning
- Toolpath verification
- Educational simulation-only G-code
- Additive-manufacturing prototypes

### Web application

- HTML5
- CSS3
- JavaScript
- Three.js
- GLTFLoader
- OrbitControls
- GitHub Pages
- GitHub Actions
- Progressive Web App assets
- Responsive mobile and desktop layouts

---

## Project Development Roadmap

| Version | Main milestone |
|---|---|
| 0.1 | Project definition, requirements, risk register, and baseline calculations |
| 0.2 | NX master skeleton, station system, interfaces, and neutral envelope geometry |
| 0.3 | Primary structure, beam idealisation, materials, and preliminary sizing |
| 0.4 | Full subsystem assembly, mass budget, CG model, and interface definitions |
| 0.5 | Static, modal, buckling, and structural screening workflow |
| 0.6 | Thermal analysis, cabin ventilation CFD, and Skimmer aerodynamics |
| 0.7 | NX CAM, manufacturing drawings, inspection plans, and prototypes |
| 0.8 | Structural redesign, optimisation, mass updates, and comparison studies |
| 0.9 | Validation, reporting, presentation, and GitHub Pages integration |
| 1.0 | Public open-source release, manifests, checksums, and repository cleanup |

---

## Key Engineering Results

### Structural redesign

The Version 0.8 redesign added:

- Ring torque bracing
- Forward docking load spreaders
- Longitudinal propulsion struts
- Increased central-spine depth
- Updated truss members
- Corrected counter-rotating braking load application

Screening improvements included:

| Metric | Earlier design | Optimised design | Change |
|---|---:|---:|---:|
| Propulsion-load translation | 13.788 mm | 0.215 mm | 98.4% reduction |
| Misaligned-docking translation | 52.823 mm | 22.870 mm | 56.7% reduction |
| First supported flexible mode | 0.1308 Hz | 0.1964 Hz | 50.2% increase |
| Idealised structural mass | 7,742 kg | 10,423 kg | Increased for stiffness |

### Ring dynamics

At a 12 m occupied radius and approximately 4.3 rpm:

- Artificial gravity is approximately **0.248 g**
- Balanced counter-rotating emergency braking produced approximately **1.846 mm** screening translation
- A single-ring braking fault produced approximately **3.487 mm** screening translation

### Thermal screening

| Study | Screening result |
|---|---:|
| Effective radiator emitting area | 144 m² |
| Nominal 120 kW radiator equilibrium | Approximately 361.4 K |
| Five-panel degraded equilibrium | Approximately 377.9 K |
| Electronics cold-plate hotspot | Approximately 324.6 K |
| Habitat-wall heat leak | Approximately 1.30 W/m² |
| Thruster-bracket peak temperature | Approximately 334.4 K |

### Cabin ventilation screening

| Condition | Airflow | Predicted well-mixed CO₂ |
|---|---:|---:|
| Normal | 240 m³/h | Approximately 587 ppm |
| Degraded | 80 m³/h | Approximately 920 ppm |
| Fan loss | 0 m³/h | 1000 ppm after approximately 27.9 minutes |

### Skimmer aerodynamic screening

At approximately 5° angle of attack:

| Case | Screening lift-to-drag ratio |
|---|---:|
| Mach 0.3 | Approximately 7.9 |
| Mach 0.8 | Approximately 4.5 |
| Mach 2.0 | Approximately 2.2 |

These values are reduced-order screening results and must be replaced or correlated with native ANSYS Fluent results.

---

## Repository Structure

```text
asterion-fcta/
├── README.md
├── LICENSE
├── CITATION.cff
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── RELEASE_NOTES.md
│
├── cad/
│   ├── nx_master_model/
│   ├── primary_structure/
│   ├── full_assembly/
│   ├── manufacturing_parts/
│   ├── neutral/
│   └── drawings/
│
├── analysis/
│   └── ansys/
│       ├── structural/
│       ├── modal/
│       ├── buckling/
│       ├── thermal/
│       ├── fluent/
│       └── apdl/
│
├── cam/
│   └── nx_cam/
│       ├── operation_plans/
│       ├── tool_libraries/
│       ├── fixture_plans/
│       ├── setup_sheets/
│       ├── inspection/
│       └── educational_gcode/
│
├── calculations/
│   ├── mass_budget/
│   ├── centre_of_gravity/
│   ├── structural_screening/
│   ├── thermal_screening/
│   ├── cfd_screening/
│   └── optimisation/
│
├── docs/
│   ├── requirements/
│   ├── architecture/
│   ├── tutorials/
│   ├── final_report/
│   ├── portfolio/
│   ├── evidence/
│   └── governance/
│
├── prototype/
│   ├── stl/
│   ├── printing_guides/
│   └── test_plans/
│
├── scripts/
│   ├── python/
│   ├── nxopen/
│   └── release/
│
├── media/
│   ├── renders/
│   ├── plots/
│   ├── drawings/
│   └── presentation/
│
├── verification/
│   ├── requirements_matrix/
│   ├── artefact_status/
│   ├── manifests/
│   └── checksums/
│
└── web-viewer/
    ├── index.html
    ├── css/
    ├── js/
    ├── models/
    ├── data/
    └── assets/
```

---

## Running the Live 3D Website

Do not open `index.html` directly from Windows Explorer because browser security restrictions may block JavaScript modules and GLB loading.

### Windows

Run:

```bat
START_ASTERION.bat
```

### Python local server

```bash
python tools/serve.py
```

Open:

```text
http://127.0.0.1:8000/
```

### GitHub Pages

1. Create a GitHub repository.
2. Upload the website files to the repository root.
3. Push the files to the `main` branch.
4. Open **Settings → Pages**.
5. Select **GitHub Actions** as the deployment source.
6. Run the included Pages workflow.
7. Open the generated GitHub Pages URL.

---

## Siemens NX Workflow

The native Siemens NX files should be reconstructed using the included:

- Master-model expressions
- Station tables
- Coordinate-system definitions
- Component manifests
- WAVE-link maps
- NXOpen journals
- Neutral geometry
- Tutorial drawings
- Assembly and drawing checklists

Typical native file naming:

```text
AST-0000-ASTERION-FCTA-1-ASSY.prt
AST-0000-ASTERION-FCTA-1-ASSY-DRW.prt
AST-1100-CENTRAL-SPINE.prt
AST-3200-HABITATION-RING-ASSY.prt
AST-4300-SKIMMER-ASSY.prt
```

Siemens NX stores parts, assemblies, and drawing parts using the `.prt` extension.

---

## ANSYS Workflow

The project includes preparation data for:

- Static docking loads
- Propulsion thrust loads
- Ring centrifugal loading
- Ring braking
- Modal analysis
- Linear buckling
- Radiator thermal analysis
- Cold-plate analysis
- Habitat-wall heat transfer
- Thruster-bracket thermal stress
- Cabin airflow and CO₂ transport
- Skimmer external aerodynamics

The included Python and APDL outputs are intended for model verification and correlation. ANSYS Mechanical and Fluent results executed on the user’s own computer remain the authoritative simulation evidence.

---

## NX CAM Demonstrators

Four representative manufacturing parts are included:

1. Thruster-gimbal bracket
2. Ring-bearing housing
3. Skimmer wing rib
4. Lightweight structural bulkhead

The manufacturing package contains:

- Neutral 3D models
- Engineering drawings
- Operation plans
- Tool libraries
- Cutting-parameter tables
- Fixture concepts
- Setup sheets
- Inspection plans
- Toolpath previews
- Simulation-only educational G-code
- Additive-manufacturing prototypes

The supplied G-code is not production-ready. Machine-specific postprocessing, simulation, work-offset verification, dry runs, and supervised prove-out are mandatory before machining.

---

## Tutorial Drawings

The project includes a complete tutorial drawing package covering:

- General arrangement views
- Coordinate systems and station planes
- Primary structure
- Habitation rings
- Ring bearing and braking systems
- Solar wings
- Radiators
- Propulsion pods
- Docking interfaces
- Robotics
- Skimmer aeroshuttle
- Manufacturing demonstrator parts
- NX modelling and drafting procedures
- ANSYS and NX CAM workflows

The tutorial drawings are conceptual engineering references and must not be treated as approved manufacturing drawings.

---

## Validation and Reproducibility

The public release includes:

- Requirements-verification matrix
- Artefact-status ledger
- Release manifest
- SHA-256 checksums
- Python validation scripts
- GLB model checks
- STL geometry checks
- Mass and CG checks
- Structural connectivity checks
- G-code text-level safety checks
- GitHub Pages reference validation
- Native-software evidence checklist

Run the release validator with:

```bash
python scripts/release/validate_release.py
```

---

## Claims and Limitations

ASTERION FCTA-1 is:

- A conceptual spacecraft architecture
- A CAD/CAM/CAE portfolio project
- An educational engineering demonstrator
- An open-source technical communication project
- A basis for future native CAD and simulation work

ASTERION FCTA-1 is not:

- A flight-qualified spacecraft
- A certified pressure vessel
- A validated human-rated vehicle
- A proven reactionless-propulsion system
- A faster-than-light spacecraft
- A replacement for professional aerospace certification
- A source of machine-ready production G-code
- A completed native Siemens NX or solved ANSYS project unless those files are executed and added separately

---

## Conclusion

ASTERION FCTA-1 demonstrates a complete multidisciplinary aerospace-development workflow covering spacecraft systems engineering, aeronautical design, CAD, CAE, CAM, optimisation, manufacturing planning, validation, documentation, and interactive 3D presentation.

The project successfully transforms an unconventional deep-space transportation concept into a structured and technically reviewable engineering portfolio. Instead of making unsupported claims about unrestricted travel, the design uses a modular orbit-assembled architecture with electric propulsion, replaceable subsystems, counter-rotating habitation rings, large power systems, thermal-control radiators, radiation protection, robotics, docking systems, and a detachable lifting-body aeroshuttle.

The development process produced measurable engineering improvements. Structural redesign substantially reduced propulsion and docking deformation while increasing the first supported natural frequency. Thermal and ventilation studies identified radiator performance, degraded cooling behaviour, cabin heat-removal needs, and ventilation redundancy requirements. Aerodynamic studies established a preliminary Skimmer performance baseline, while the CAM package demonstrated representative machining, inspection, workholding, and additive-manufacturing workflows.

The final public release integrates neutral geometry, scripts, engineering drawings, analyses, documentation, manufacturing plans, validation records, and a live GitHub Pages 3D application. It therefore serves as a strong portfolio for Siemens NX, ANSYS, aerospace systems engineering, digital manufacturing, software development, and open-source technical communication.

The project remains conceptual. Its strongest value is not a claim that the spacecraft is ready to fly, but the transparent integration of requirements, assumptions, calculations, CAD, simulation, optimisation, manufacturing preparation, and reproducible documentation into one coherent engineering project.

---

## Future Enhancements

### Native Siemens NX development

- Rebuild neutral geometry as fully parametric NX parts
- Add editable sketches and feature history
- Complete WAVE-linked top-down assemblies
- Add assembly constraints and arrangements
- Add routing for power, data, coolant, and propellant
- Produce native NX drawings and PMI
- Maintain automatic mass and centre-of-gravity updates

### High-fidelity structural analysis

- Replace selected beam regions with shell and solid submodels
- Model joints, bolts, bearings, contacts, and preload
- Include nonlinear material and geometric behaviour
- Perform fatigue and damage-tolerance studies
- Add random-vibration and shock cases
- Correlate analytical, Python, and ANSYS results

### Artificial-gravity and ring dynamics

- Simulate spin-up and spin-down
- Study gyroscopic effects
- Model bearing friction and heating
- Evaluate crew and cargo imbalance
- Investigate Coriolis effects
- Analyse emergency braking and control
- Build and test an instrumented rotating-ring demonstrator

### Propulsion and mission analysis

- Add validated thruster performance maps
- Compare xenon, krypton, and argon
- Model plume interaction and erosion
- Couple power, thrust, and thermal performance
- Add Earth-orbit assembly and deep-space mission scenarios
- Integrate Orekit, GMAT, poliastro, or custom Python mission tools
- Evaluate lunar, asteroid, Mars cargo, and Mars crew missions

### Thermal and life-support development

- Build a coupled thermal-fluid network
- Add pumps, manifolds, cold plates, and rotary joints
- Model eclipse and solar-distance effects
- Add humidity and contaminant transport
- Simulate ventilation failures and emergency scrubbing
- Investigate fire, smoke, and cabin acoustic behaviour

### Skimmer aeronautical development

- Refine lifting-body geometry
- Calculate stability and control derivatives
- Optimise control surfaces
- Study transonic shocks and supersonic heating
- Couple aerodynamics with trajectory analysis
- Add landing-gear and runway-performance studies
- Manufacture and wind-tunnel test a physical model

### Radiation, debris, and pressure systems

- Model pressure-shell fatigue
- Add hatch and window reinforcement
- Analyse Whipple shielding
- Study micrometeoroid and orbital-debris impact
- Improve solar-particle-event shelter design
- Compare water, polyethylene, and multifunctional shielding

### Manufacturing and testing

- Develop machine-specific NX CAM postprocessors
- Add complete machine-tool digital twins
- Perform multi-axis manufacturing studies
- Add hybrid and additive-manufacturing workflows
- Create first-article inspection reports
- Manufacture selected demonstrator components
- Record physical test data and correlate it with simulations

### Live 3D application

- Add component selection and isolation
- Add model-to-drawing cross-selection
- Add animated deployments and ring rotation
- Add live centre-of-gravity visualisation
- Add measurement and sectioning tools
- Add simulation-result contour overlays
- Add mission trajectory visualisation
- Add searchable BOM, requirements, and risk databases
- Add WebXR or virtual-reality support
- Add collaborative design submissions and comparison tools

### Open-source development

- Expand contribution guidelines
- Add issue templates for CAD, CAE, CAM, web, and documentation work
- Add continuous integration for geometry and data validation
- Publish versioned datasets
- Add educational challenges
- Encourage community model correlation
- Maintain transparent limitations and evidence requirements

---

## Contributing

Contributions are welcome in the following areas:

- Siemens NX modelling
- NXOpen automation
- ANSYS Mechanical
- ANSYS Fluent
- APDL development
- Python engineering tools
- Mission analysis
- Thermal control
- Life-support modelling
- Aerodynamics
- NX CAM
- Additive manufacturing
- Web development
- Documentation
- Physical prototyping and testing

Before contributing, read:

- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `docs/governance/CLAIMS_AND_LIMITATIONS.md`
- `docs/evidence/NATIVE_EXECUTION_EVIDENCE_CHECKLIST.md`

---

## Citation

When using or referencing this project, cite:

```bibtex
@software{samuelson_g_asterion_fcta_1,
  author  = {Samuelson G},
  title   = {ASTERION FCTA-1: A Modular Multi-Regime Spacecraft CAD/CAM/CAE Demonstrator},
  version = {1.0},
  year    = {2026},
  note    = {Open-source aerospace engineering portfolio project}
}
```

A machine-readable citation is also provided in `CITATION.cff`.

---

## Licence

This project is released under the **MIT Licence**, except where individual files contain separate third-party notices or restrictions.

See:

- `LICENSE`
- `THIRD_PARTY_NOTICES.md`
- `docs/governance/CLAIMS_AND_LIMITATIONS.md`

---

## Author

**Samuelson G**

Project focus:

- Aerospace engineering
- Aeronautics
- Spacecraft systems
- Siemens NX
- ANSYS
- CAD/CAM/CAE
- Simulation and optimisation
- Digital manufacturing
- Open-source engineering
- Interactive technical visualisation

---

## Acknowledgements

This project draws on established principles from:

- Aerospace systems engineering
- Spacecraft structural design
- Electric propulsion
- Artificial-gravity research
- Thermal control
- Computational fluid dynamics
- Aeronautical configuration design
- Digital manufacturing
- Verification and validation
- Open-source software development

All project claims should be evaluated against the supplied assumptions, limitations, validation records, and native-software evidence.
