#!/usr/bin/env python3
from __future__ import annotations
import csv, json, py_compile, sys
from pathlib import Path
import trimesh
ROOT=Path(__file__).resolve().parents[2]
required=[
 'VERSION','README.md','PROJECT_STATUS.md',
 'calculations/v0_6/screening_report.json',
 'calculations/v0_6/thermal_screening_summary.csv',
 'calculations/v0_6/cabin_zonal_summary.csv',
 'calculations/v0_6/skimmer_aero_summary.csv',
 'analysis/ansys/v0_6/thermal/thermal_case_matrix.csv',
 'analysis/ansys/v0_6/fluent/cfd_case_matrix.csv',
 'cad/analysis_models/v0_6/neutral/skimmer_lifting_body_cfd_surface.stl',
 'media/plots/v0_6/v0_6_radiator_equilibrium_temperature.png',
]
errors=[]
for rel in required:
    if not (ROOT/rel).exists(): errors.append(f"missing {rel}")
if (ROOT/'VERSION').read_text().strip()!='0.6.0': errors.append('VERSION mismatch')
rep=json.loads((ROOT/'calculations/v0_6/screening_report.json').read_text())
T=rep['thermal']['radiator_nominal_equilibrium_K']
if not (350<T<380): errors.append(f'radiator T outside screening range: {T}')
C=rep['cabin']['normal_steady_CO2_ppm']
if not (500<C<700): errors.append(f'nominal CO2 outside screening range: {C}')
mesh=trimesh.load(ROOT/'cad/analysis_models/v0_6/neutral/skimmer_lifting_body_cfd_surface.stl',force='mesh')
if not mesh.is_watertight: errors.append('Skimmer STL is not watertight')
if len(mesh.faces)<1000: errors.append('Skimmer mesh unexpectedly coarse')
for p in (ROOT/'scripts/python').rglob('*.py'):
    try: py_compile.compile(str(p),doraise=True)
    except Exception as e: errors.append(f'compile {p.relative_to(ROOT)}: {e}')
status={'version':'0.6.0','errors':errors,'skimmer_faces':int(len(mesh.faces)),'radiator_temperature_K':T,'nominal_CO2_ppm':C}
out=ROOT/'calculations/v0_6/v0_6_validation_report.json'
out.write_text(json.dumps(status,indent=2))
print(json.dumps(status,indent=2))
sys.exit(1 if errors else 0)
