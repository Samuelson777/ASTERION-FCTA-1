# System Requirements Baseline — Version 0.1

Requirement identifiers are intentionally stable. Changes should be recorded through Git commits and a change log.

## Mission and architecture

| ID | Requirement | Verification |
|---|---|---|
| SYS-001 | The vehicle shall use a modular, orbit-assembled architecture. | CAD inspection |
| SYS-002 | The complete vehicle shall not require atmospheric launch or landing as one assembly. | Architecture review |
| SYS-003 | The design shall include replaceable power, propulsion, habitation, thermal, and mission modules. | Interface review |
| SYS-004 | The design shall include a detachable lifting-body atmospheric demonstrator. | CAD inspection |
| SYS-005 | The baseline vehicle length shall remain within 38–46 m during Version 0.x. | NX measurement |

## Human factors

| ID | Requirement | Verification |
|---|---|---|
| HUM-001 | The baseline crew capacity shall be four. | Layout review |
| HUM-002 | The vehicle shall include two counter-rotating habitation rings. | Assembly inspection |
| HUM-003 | The occupied ring radius shall be nominally 12 m. | NX measurement |
| HUM-004 | The nominal artificial-gravity target shall be approximately 0.25 g. | Calculation |
| HUM-005 | The design shall include an internal radiation refuge zone. | Layout review |

## Structure and mechanisms

| ID | Requirement | Verification |
|---|---|---|
| STR-001 | The central spine shall provide the primary propulsion and docking load path. | FEA and inspection |
| STR-002 | Major deployable structures shall include locked and stowed configurations. | Motion review |
| STR-003 | Selected metallic components shall maintain a preliminary yield factor of safety of at least 1.5 for defined portfolio load cases. | FEA |
| STR-004 | Critical slender members shall be checked for linear buckling. | FEA and hand calculation |
| STR-005 | The first structural modes shall be identified and assessed against plausible excitation sources. | Modal analysis |

## Power, propulsion, and thermal

| ID | Requirement | Verification |
|---|---|---|
| PPT-001 | The baseline spacecraft shall use modular electric-propulsion pods. | Architecture inspection |
| PPT-002 | The reference propulsion power demand shall be approximately 144 kW. | Power budget |
| PPT-003 | Total electrical generation at 1 AU shall target 200–300 kW. | Power budget |
| PPT-004 | Thruster plumes shall not directly impinge on radiator or solar-array envelopes in the nominal configuration. | Clearance analysis |
| THM-001 | The design shall include deployable radiator surfaces with independent support structure. | CAD inspection |
| THM-002 | At least one radiator panel shall be analysed structurally and thermally. | FEA |
| THM-003 | Thermal analyses shall include explicit energy-balance checks. | Calculation and result review |

## Aeronautics

| ID | Requirement | Verification |
|---|---|---|
| AER-001 | The Skimmer shall use a blended lifting-body configuration. | Geometry inspection |
| AER-002 | The Skimmer shall include controllable pitch and yaw surfaces. | CAD and CFD |
| AER-003 | External aerodynamic studies shall include Mach 0.3, 0.8, and 2.0 cases. | CFD report |
| AER-004 | The aerodynamic model shall report lift, drag, pitching moment, and surface pressure. | CFD report |
| AER-005 | Full chemically reacting re-entry simulation is outside the baseline scope. | Scope review |

## CAD, CAM, and digital engineering

| ID | Requirement | Verification |
|---|---|---|
| CAD-001 | The NX assembly shall use a master skeleton with named datums and expressions. | Model audit |
| CAD-002 | The project shall demonstrate top-down associative modelling. | Model audit |
| CAD-003 | The project shall include advanced surface modelling on the Skimmer. | Feature audit |
| CAD-004 | The final assembly shall contain no unresolved hard interferences. | NX clearance report |
| CAM-001 | At least four representative parts shall receive NX CAM process plans. | CAM review |
| CAM-002 | Each CAM study shall include setup, tool list, simulation, and collision review. | CAM evidence |
| DOC-001 | The release shall include drawings, BOM, interface definitions, and verification records. | Documentation audit |

## Computation and openness

| ID | Requirement | Verification |
|---|---|---|
| HPC-001 | Individual ANSYS models shall be reduced to fit student or home-PC resource limits. | Mesh report |
| HPC-002 | Critical models shall use mesh-sensitivity checks with less than 5% change in the selected result metric. | Convergence report |
| VAL-001 | Major analyses shall be compared with a hand calculation, benchmark, or independent estimate. | Validation report |
| OSS-001 | Public releases shall include neutral formats and avoid restricted proprietary content. | Release audit |
| OSS-002 | Assumptions, uncertainties, and unsupported technology extrapolations shall be clearly labelled. | Report review |
