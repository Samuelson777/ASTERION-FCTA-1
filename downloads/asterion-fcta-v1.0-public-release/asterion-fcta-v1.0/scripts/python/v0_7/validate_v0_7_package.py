from __future__ import annotations
import csv, json, py_compile
from pathlib import Path
import trimesh
ROOT=Path(__file__).resolve().parents[3]
required=[
'VERSION','calculations/v0_7/V0_7_manufacturing_screening_report.md',
'cam/nx_cam/v0_7/tool_library.csv','cam/nx_cam/v0_7/operation_plan.csv',
'cam/nx_cam/v0_7/inspection_plan.csv','cam/nx_cam/v0_7/NX_CAM_V0_7_Workflow.md',
'prototype/v0_7/stl/asterion_full_vehicle_1_to_50.stl']
errors=[]
for r in required:
    if not (ROOT/r).exists(): errors.append('missing '+r)
if (ROOT/'VERSION').read_text().strip()!='0.7.0': errors.append('wrong version')
parts=list((ROOT/'cad/manufacturing_parts/v0_7/neutral').glob('*.stl'))
if len(parts)!=4: errors.append(f'expected 4 part STL files, found {len(parts)}')
for p in parts:
    m=trimesh.load_mesh(p)
    if len(m.faces)<100: errors.append(f'{p.name}: mesh too coarse')
    if not m.is_watertight: errors.append(f'{p.name}: not watertight')
with (ROOT/'cam/nx_cam/v0_7/operation_plan.csv').open() as f:
    ops=list(csv.DictReader(f))
if len(ops)<12: errors.append('operation plan too short')
for p in (ROOT/'scripts/python/v0_7').glob('*.py'):
    py_compile.compile(str(p),doraise=True)
report={'status':'PASS' if not errors else 'FAIL','errors':errors,'part_stl_count':len(parts),'operation_count':len(ops)}
(ROOT/'calculations/v0_7/v0_7_validation_report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
if errors: raise SystemExit(1)
