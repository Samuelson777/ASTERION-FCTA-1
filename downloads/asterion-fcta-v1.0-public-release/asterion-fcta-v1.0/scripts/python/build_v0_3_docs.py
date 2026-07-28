#!/usr/bin/env python3
from __future__ import annotations
import csv, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
report=json.loads((ROOT/'calculations/v0_3/v0_3_structural_report.json').read_text())
mass=report['primary_structure_estimated_mass_kg']
nodes=report['node_count']; elems=report['element_count']
ring_g=report['ring_acceleration_g']; radial=report['ring_total_radial_force_each_N']; torque=report['ring_emergency_braking_torque_Nm']

(ROOT/'README.md').write_text(f'''# ASTERION FCTA-1

**Field-Coupled Transit Architecture — modular, multi-regime spacecraft CAD/CAM/CAE demonstrator**

> ASTERION is a constraint-reduced portfolio concept, not a reactionless, faster-than-light, or unrestricted spacecraft. It remains subject to conservation laws, available power, thermal rejection, radiation, structural mass, and human-factors limits.

## Current release: Version 0.3.0

Version 0.3 establishes the preliminary primary structure for Siemens NX reconstruction and ANSYS analysis:

- eight-longeron central space truss with transverse frames and diagonals;
- twin 12-sector rotating-ring frames and spoke supports;
- propulsion load-transfer structure and forward docking frame;
- neutral GLB, STL and OBJ structural geometry;
- {nodes} nodes and {elems} BEAM188-ready elements;
- solver-neutral node, element, section, material and load-case tables;
- APDL line-model, static docking, modal and buckling templates;
- hand calculations for centrifugal loading, braking torque and Euler buckling;
- NX expression seed, assembly tree and build tutorial; and
- structural drawings, model checks, verification plan and release validator.

## Vehicle and structural baseline

| Parameter | Baseline |
|---|---:|
| Core structural length | 42 m |
| Habitation-ring outer diameter | 26 m |
| Occupied ring radius | 12 m |
| Ring centres | X = -2.5 m and +2.5 m |
| Ring speed | 4.3 rpm |
| Approximate artificial gravity | {ring_g:.3f} g |
| Central-truss longerons | 8 |
| Nominal truss bay | 2.5 m |
| Primary beam idealisation mass | {mass:,.1f} kg |
| Coordinate convention | +X forward, +Y starboard, +Z up |

## Start here

1. Read `docs/v0_3/design_basis.md` and `docs/v0_3/load_path_definition.md`.
2. Open `cad/primary_structure/v0_3/neutral/asterion_v0_3_primary_structure.glb`.
3. Rebuild the associative structure in NX using `cad/primary_structure/v0_3/nx_primary_structure_tutorial.md`.
4. Import or execute the ANSYS inputs under `analysis/ansys/v0_3/`.
5. Review `calculations/v0_3/preliminary_structural_sizing.md` before interpreting solver results.
6. Run `python scripts/python/validate_v0_3_package.py` from the repository root.

## Native-file limitation

No native NX `.prt`, `.asm`, ANSYS Workbench `.wbpj`, Mechanical database, or solved result file is represented as completed. Siemens NX and ANSYS are not installed in the generation environment. Neutral geometry, data tables, APDL templates, calculations and procedures are supplied to create and validate those native files on the project computer.

## Roadmap

- **0.1:** requirements and project definition — complete
- **0.2:** NX master skeleton and neutral envelope — complete
- **0.3:** spine and rotating-ring primary structure — complete
- **0.4:** full subsystem assembly
- **0.5:** structural, modal and buckling analyses
- **0.6:** thermal and CFD analyses
- **0.7:** NX CAM and prototypes
- **0.8:** optimisation
- **0.9:** validation and presentation
- **1.0:** public portfolio release

## Licence

Code and original documentation are released under the repository licence. Confirm all Siemens, ANSYS and third-party licence terms before publishing proprietary-format data.
''', encoding='utf-8')

(ROOT/'PROJECT_STATUS.md').write_text(f'''# Project Status

## Release

- Project: ASTERION FCTA-1
- Version: 0.3.0
- Stage: preliminary primary-structure definition
- Status: generated and package-validated

## Completed

- Controlled master coordinate system and stable vehicle stations
- Neutral master envelope from Version 0.2
- Eight-longeron central truss
- Transverse frames and alternating diagonals
- Twin 12-sector ring circumference structures
- Twelve ring-support spokes per ring
- Propulsion load-transfer booms
- Forward docking load frame
- ANSYS BEAM188 line-model input: {nodes} nodes, {elems} elements
- Preliminary structural calculations and load cases
- NX reconstruction tutorial and expression table
- GLB, OBJ and STL exports
- Structural plan and front references

## Open engineering work

- Joint stiffness and fitting detail
- Local shell and solid submodels
- Bearing and rotary-interface design
- Pressure shell and micrometeoroid protection
- Nonlinear imperfection-sensitive buckling
- Fatigue, fracture control and thermal-distortion evaluation
- Workbench execution and result correlation on the project PC
- Formal mass maturity allowance and centre-of-gravity update

## Next release

Version 0.4 will add the non-structural subsystem assembly: habitation sectors, service modules, solar wings, radiators, propulsion pods, tanks, docking systems and Skimmer interface geometry.
''', encoding='utf-8')

ch=(ROOT/'CHANGELOG.md').read_text(encoding='utf-8') if (ROOT/'CHANGELOG.md').exists() else '# Changelog\n'
entry=f'''\n## [0.3.0] - 2026-07-27\n\n### Added\n- Primary structural line model with {nodes} nodes and {elems} beam elements.\n- Neutral GLB, STL and OBJ primary-structure geometry.\n- Seven beam-section definitions and preliminary aluminium material card.\n- Eight structural/modal/buckling load cases and named-selection map.\n- APDL model include and three solver templates.\n- Ring centrifugal, braking and longeron buckling hand calculations.\n- NX primary-structure reconstruction tutorial, expressions and assembly tree.\n- Version 0.3 validation script, release manifest and drawing references.\n\n### Corrected\n- Reused coincident truss nodes at ring-hub intersections to prevent zero-length beam elements.\n'''
if '## [0.3.0]' not in ch:
    ch=ch.rstrip()+entry+'\n'
(ROOT/'CHANGELOG.md').write_text(ch, encoding='utf-8')

v03=ROOT/'docs/v0_3'; v03.mkdir(parents=True, exist_ok=True)
(v03/'design_basis.md').write_text(f'''# Version 0.3 Structural Design Basis

## Purpose

Define a lightweight, modular primary structure that can be rebuilt in Siemens NX and analysed on a home PC with ANSYS Student-class model limits.

## Design philosophy

1. Use orbit assembly; do not design the complete vehicle as a single launch stack.
2. Keep the first global model beam-dominant and auditable.
3. Separate global load-path verification from local joint, shell and contact models.
4. Make interfaces replaceable and parameter-driven.
5. Treat all material properties and load levels as preliminary until source-controlled project values are selected.

## Structural arrangement

- Central truss: eight longerons at 1.2 m radius.
- Bay spacing: nominally 2.5 m, with extra interface stations.
- Frames: octagonal beam frames at each station.
- Bracing: alternating diagonal lattice between stations.
- Rotating rings: 12-segment circumference frames at 12 m occupied radius.
- Ring supports: 12 radial spokes per ring with hub links to the central truss.
- Propulsion frame: six radial mounts at X = -16 m.
- Docking frame: eight linked nodes at X = +21.4 m.

## Preliminary material

The model uses a conceptual aluminium 7075-T6 isotropic card:

- Elastic modulus: 71.7 GPa
- Poisson ratio: 0.33
- Density: 2810 kg/m³
- Screening yield strength: 503 MPa

These values are not a procurement specification. Update them for temperature, product form, thickness, direction, joining process and supplier certification.

## Mass statement

The beam idealisation mass is {mass:,.1f} kg. It excludes joints, fittings, bearing hardware, pressure shells, fasteners, mechanisms, harnesses, coatings, local reinforcement and manufacturing allowances. It must not be quoted as complete spacecraft structural mass.
''', encoding='utf-8')

(v03/'load_path_definition.md').write_text(f'''# Primary Load-Path Definition

## Docking load

A preliminary 25 kN axial compression is introduced at the forward docking frame and transferred through eight docking links into the longerons, frames and diagonals. The demonstration support is placed at the aft end for a ground-test-style static case. A flight free-body treatment must use inertial relief or balanced loads rather than an artificial fixed support.

## Propulsion and manoeuvre load

Six propulsion mounts transfer thrust and gimbal reactions into the frame at X = -16 m. The current line model includes mount booms but does not yet model gimbal stiffness, pod mass or thrust-vector eccentricity.

## Rotating-ring load

Each ring uses a 12,000 kg conceptual rotating mass. At 4.3 rpm and 12 m radius, the distributed radial force is {radial:,.1f} N per ring. It is divided across 12 outer nodes for the first global case. Sector-by-sector mass, bearing compliance and imbalance must be added later.

## Emergency braking

Stopping one ring in 120 seconds requires an idealised torque of approximately {torque:,.1f} N·m. Counter-rotating rings cancel nominal angular momentum only when their inertias and rates match; transient mismatch still loads the spine and attitude-control system.

## Local submodels required

- Ring spoke-to-hub fittings
- Bearing support and race
- Docking-link lugs
- Propulsion boom joints
- Longeron/frame node fittings
- Solar and radiator deployment hinges

Global beam stresses must not be used to approve these local features.
''', encoding='utf-8')

(v03/'model_acceptance_criteria.md').write_text('''# Version 0.3 Model Acceptance Criteria

| Check | Acceptance criterion |
|---|---|
| Zero-length elements | None |
| Duplicate unmerged structural nodes | None unless intentionally connected by a joint element |
| Beam section assignment | Every element has one valid section ID |
| Material assignment | Every active element uses a reviewed material card |
| Geometry units | Millimetres |
| Solver force units | Newtons |
| Free-free modal check | First six modes behave as rigid-body modes near zero frequency |
| Supported modal check | No unintended mechanism modes |
| Static equilibrium | Reaction-force balance within 1% |
| Mesh refinement | Key displacement and load-path measures change by less than 5% |
| Hand correlation | Selected benchmark results within 10% |
| Buckling interpretation | Eigenvalue result labelled as ideal linear screening only |
| Stress reporting | Beam stress kept separate from local joint stress claims |
''', encoding='utf-8')

(v03/'version_0_3_release_notes.md').write_text(f'''# Version 0.3 Release Notes

Version 0.3 converts the Version 0.2 envelope into a first analysable primary structure. The generated structure contains {nodes} nodes and {elems} beam elements and exports as GLB, OBJ and STL. Solver inputs include CSV tables and APDL templates for static docking, free-free modal and linear buckling demonstrations.

## Main limitations

- Geometry is preliminary beam/tube representation, not manufacturing detail.
- No solved ANSYS database is included.
- Bearings, joint stiffness, pressure shells and local contacts are simplified or absent.
- Linear elastic isotropic aluminium is used throughout the initial line model.
- Load cases are portfolio design cases, not certified mission or launch requirements.
''', encoding='utf-8')

# NX files
nxdir=ROOT/'cad/primary_structure/v0_3'
(nxdir/'nx_expressions_v0_3.txt').write_text('''# ASTERION PRIMARY STRUCTURE EXPRESSIONS — VERSION 0.3
# Apply explicit units inside Siemens NX.

spine_half_length = 21000 mm
spine_truss_radius = 1200 mm
spine_longeron_count = 8
spine_frame_angle = 360 deg / spine_longeron_count
nominal_bay_pitch = 2500 mm

longeron_od = 160 mm
longeron_wall = 6 mm
frame_od = 120 mm
frame_wall = 5 mm
diagonal_od = 90 mm
diagonal_wall = 4 mm

ring_support_count = 2
ring_support_x_1 = -2500 mm
ring_support_x_2 = 2500 mm
ring_sector_count = 12
ring_sector_angle = 360 deg / ring_sector_count
ring_centroid_radius = 12000 mm
ring_beam_od = 200 mm
ring_beam_wall = 6 mm
ring_spoke_od = 120 mm
ring_spoke_wall = 5 mm

propulsion_frame_x = -16000 mm
propulsion_mount_count = 6
propulsion_mount_radius = 3200 mm
propulsion_boom_od = 140 mm
propulsion_boom_wall = 5 mm

docking_frame_x = 21400 mm
docking_frame_radius = 800 mm
docking_node_count = 8
docking_link_od = 140 mm
docking_link_wall = 5 mm
''', encoding='utf-8')

(nxdir/'nx_primary_structure_tutorial.md').write_text('''# Siemens NX Primary-Structure Build Tutorial

## 1. Create the controlled parts

Create these native files on the NX workstation:

- `AST-1000-PRIMARY-STRUCTURE-ASM.prt`
- `AST-1100-SPINE-TRUSS.prt`
- `AST-1200-RING-SUPPORT-A.prt`
- `AST-1210-RING-SUPPORT-B.prt`
- `AST-1300-PROPULSION-FRAME.prt`
- `AST-1400-FORWARD-DOCK-FRAME.prt`

Keep `AST-0001-MASTER-SKELETON.prt` from Version 0.2 as the top-level geometry authority.

## 2. Import expressions

Create the expressions listed in `nx_expressions_v0_3.txt`. Preserve meaningful names and units. Do not dimension structural features with anonymous sketch dimensions when a controlled expression exists.

## 3. Spine truss

1. WAVE-link the vehicle centreline, truss-radius circle and station planes.
2. At the aft station create eight points on the truss-radius circle.
3. Use associative curves parallel to +X for the longeron axes.
4. Trim or divide them at each station plane.
5. Create transverse octagonal frames at all structural stations.
6. Add alternating diagonal curves between adjacent stations.
7. Use `Tube` for presentation solids, or retain centreline curves for idealisation.
8. Put centreline, simplified tube and interface geometry in separate reference sets.

## 4. Ring supports

1. WAVE-link the ring centre plane and 12 m centroid circle.
2. Pattern 12 outer nodes at 30-degree intervals.
3. Create 12 circumference segments and 12 radial spokes.
4. Connect the hub ring to the nearest central-truss nodes.
5. Keep bearing race, drive hardware and pressure-shell interfaces as separate future components.

## 5. Propulsion frame

Create six mount coordinate systems at 60-degree intervals and 3.2 m radius on X = -16 m. Build paired booms from nearby truss nodes to each mount. Publish each mount CSYS for propulsion-pod WAVE linking.

## 6. Docking frame

Create an eight-node, 800 mm radius frame 400 mm forward of the main truss end. Link each docking node to one longeron endpoint. Publish the docking axis, mating plane and keep-out cylinder.

## 7. Validation in NX

- Run Examine Geometry and Assembly Clearance.
- Check all tube centreline intersections.
- Confirm no zero-length or duplicate members.
- Measure mass using assigned preliminary material.
- Verify the ring and docking coordinate systems.
- Export Parasolid or STEP from the locally built native structure for ANSYS if permitted by the installed licence.
''', encoding='utf-8')

(nxdir/'assembly_tree_v0_3.md').write_text('''# NX Assembly Tree — Version 0.3

```text
AST-1000-PRIMARY-STRUCTURE-ASM
├── AST-0001-MASTER-SKELETON
├── AST-1100-SPINE-TRUSS
│   ├── AST-1110-LONGERON-FAMILY
│   ├── AST-1120-TRANSVERSE-FRAME-FAMILY
│   └── AST-1130-DIAGONAL-BRACE-FAMILY
├── AST-1200-RING-SUPPORT-A
│   ├── AST-1201-RING-CIRCUMFERENCE
│   ├── AST-1202-SPOKE-FAMILY
│   └── AST-1203-HUB-LINK-FAMILY
├── AST-1210-RING-SUPPORT-B
├── AST-1300-PROPULSION-FRAME
└── AST-1400-FORWARD-DOCK-FRAME
```

Use arrangements for presentation solids, beam-centreline export and subsystem interface review.
''', encoding='utf-8')

# ANSYS guide
ans=ROOT/'analysis/ansys/v0_3'
(ans/'ansys_workbench_guide.md').write_text('''# ANSYS Workbench Guide — Version 0.3

## Preferred workflow

1. Start with a Mechanical line-body model reconstructed from `model/beam_nodes.csv` and `model/beam_elements.csv`, or execute the supplied APDL include.
2. Confirm millimetre, newton, second unit consistency.
3. Create the seven circular-tube beam sections from `beam_sections.csv`.
4. Apply the preliminary aluminium material from `material_properties.csv`.
5. Create named selections using `named_selections.csv`.
6. Solve one load case at a time and export result tables and screenshots into a new `results/` folder.

## Static docking demonstration

- Aft frame fixed only for a ground-test-style benchmark.
- Apply 25 kN total compression to the forward docking-frame nodes.
- Request total deformation, directional deformation, beam axial force, bending moment, reaction force and safety-factor screening.
- Verify reaction-force balance before interpreting stress.

## Free-free modal demonstration

Use no supports. Extract at least 16 modes. The first six should represent rigid-body behaviour near zero frequency. Review mode shapes rather than only reading frequencies.

## Buckling demonstration

Use the docking static solution as the prestress state and extract ten eigenvalue buckling modes. Label the factors as ideal linear screening. Later work must introduce geometric imperfections and nonlinear material/contact behaviour where relevant.

## Home-PC strategy

- Keep the global structure as line bodies.
- Use shell submodels only for selected panels.
- Use solid meshes only at joints and interfaces.
- Avoid merging every future subsystem into one Mechanical model.
- Maintain a mesh/refinement log for every reported result.
''', encoding='utf-8')

(ans/'results_templates/solver_run_record.csv').write_text('''run_id,date,software_version,analysis_type,load_case,model_revision,node_count,element_count,max_element_size_mm,min_element_size_mm,result_metric,result_value,result_unit,equilibrium_error_percent,notes\n''', encoding='utf-8')
(ans/'results_templates/modal_results.csv').write_text('''mode,frequency_hz,classification,dominant_subsystem,participation_x,participation_y,participation_z,engineering_interpretation\n''', encoding='utf-8')
(ans/'results_templates/static_results.csv').write_text('''load_case,max_total_deformation_mm,max_equivalent_stress_MPa,min_screening_factor,reaction_force_N,force_balance_error_percent,critical_location,notes\n''', encoding='utf-8')
(ans/'results_templates/buckling_results.csv').write_text('''mode,load_multiplier,critical_member,mode_description,acceptable_for_screening,notes\n''', encoding='utf-8')

# Preliminary structural BOM
bom=ROOT/'calculations/v0_3/preliminary_structural_bom.csv'
with bom.open('w', newline='', encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['section_id','family','outer_diameter_mm','wall_mm','total_length_m','idealised_mass_kg','material','status'])
    for sid,s in report['sections'].items():
        w.writerow([sid,s['name'],s['od_mm'],s['t_mm'],round(s['length_mm']/1000,3),round(s['mass_kg'],3),'Aluminium 7075-T6 conceptual','Beam idealisation only'])

# Web viewer update
(ROOT/'web-viewer/app.js').write_text((ROOT/'web-viewer/app.js').read_text().replace('models/asterion_master_envelope.glb','models/asterion_v0_3_primary_structure.glb'), encoding='utf-8')
idx=(ROOT/'web-viewer/index.html').read_text()
idx=idx.replace('V0.2 Master Skeleton','V0.3 Primary Structure').replace('Version 0.2 master-envelope viewer — Siemens NX and ANSYS project baseline.','Version 0.3 primary-structure viewer — Siemens NX reconstruction and ANSYS beam-model baseline.').replace('Version 0.2 scope','Version 0.3 scope').replace('This model is a simplified interface and keep-out envelope for rebuilding as a native, associative Siemens NX master skeleton. It is not flight-ready or manufacturing geometry.','This model shows the preliminary eight-longeron truss, twin rotating-ring supports, propulsion frame and docking frame. It is not flight-ready, certified or manufacturing geometry.')
(ROOT/'web-viewer/index.html').write_text(idx, encoding='utf-8')

print('Version 0.3 documentation built.')
