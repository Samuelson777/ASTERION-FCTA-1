#!/usr/bin/env python3
from pathlib import Path
import csv, json, math, sys
import trimesh
ROOT=Path(__file__).resolve().parents[2]
required=[
 'VERSION','README.md','cad/full_assembly/v0_4/neutral/asterion_v0_4_full_assembly.glb',
 'cad/full_assembly/v0_4/neutral/asterion_v0_4_full_assembly.stl',
 'calculations/v0_4/component_mass_properties.csv','calculations/v0_4/cg_loading_cases.csv',
 'analysis/ansys/v0_4/model/subsystem_interfaces.csv','docs/v0_4/interface_control_document.md']
errors=[]
for rel in required:
    if not (ROOT/rel).exists(): errors.append(f'Missing {rel}')
if not errors:
    mesh=trimesh.load(ROOT/'cad/full_assembly/v0_4/neutral/asterion_v0_4_full_assembly.stl',force='mesh')
    ext=mesh.bounds
    if ext[0,0] > -22000 or ext[1,0] < 29000: errors.append(f'Unexpected X extent {ext[:,0]}')
    if max(abs(ext[0,1]),abs(ext[1,1]),abs(ext[0,2]),abs(ext[1,2])) < 28500: errors.append('Solar deployed span below baseline')
    with (ROOT/'calculations/v0_4/component_mass_properties.csv').open() as f: rows=list(csv.DictReader(f))
    mass=sum(float(r['mass_kg']) for r in rows)
    if not (50000 <= mass <= 51000): errors.append(f'Dry mass {mass} outside controlled range')
    mx=sum(float(r['mass_kg'])*float(r['x_m']) for r in rows)/mass
    if not (1.5 <= mx <= 2.5): errors.append(f'Dry CG X {mx} outside expected range')
    with (ROOT/'calculations/v0_4/cg_loading_cases.csv').open() as f: cases=list(csv.DictReader(f))
    if len(cases) < 6: errors.append('Insufficient loading cases')
    if len(list((ROOT/'cad/full_assembly/v0_4/neutral/subsystems').glob('*.stl'))) < 10: errors.append('Subsystem exports missing')
status='PASS' if not errors else 'FAIL'
print(json.dumps({'status':status,'errors':errors},indent=2))
sys.exit(0 if not errors else 1)
