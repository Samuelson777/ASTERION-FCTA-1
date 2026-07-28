# Verification Matrix — Version 0.3

| Requirement ID | Verification method | Current evidence | Version 0.3 result | Status |
|---|---|---|---|---|
| HUM-002 | Inspection | Twin ring-support structures in GLB/STL and line model | Two ring supports generated | Preliminary pass |
| HUM-003 | Measurement | Ring outer-node coordinates | 12 m centroid radius | Pass |
| HUM-004 | Calculation | `calculations/v0_3/preliminary_structural_sizing.md` | 0.248 g at 4.3 rpm | Pass for baseline |
| STR-001 | Inspection/analysis | Spine, docking frame and propulsion booms | Continuous preliminary load path | Preliminary pass |
| STR-003 | Analysis | Longeron direct-stress screening | Above 1.5 for defined docking screening case | Hand-screen pass; FEA pending |
| STR-004 | Hand calculation | Euler longeron calculation | Completed | Preliminary pass |
| STR-005 | Modal analysis | APDL and Workbench procedure | Solver execution pending | Open |
| CAD-001 | Model audit | NX expressions and Version 0.2 master skeleton | Native NX rebuild pending | Open |
| CAD-002 | Model audit | WAVE/top-down build tutorial | Native NX audit pending | Open |
| CAD-004 | Clearance report | Neutral structure topology validation | Native assembly clearance pending | Open |
| HPC-002 | Mesh convergence | Acceptance criteria and run templates | Solver study pending | Open |
| OSS-001 | Release audit | Neutral formats, scripts and documentation | Included | Pass |
| OSS-002 | Report review | Limitations and assumptions throughout release | Included | Pass |
