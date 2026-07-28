#!/usr/bin/env python3
from pathlib import Path
import json, sys, zipfile
import pandas as pd
import trimesh

root = Path(__file__).resolve().parents[3]
errors=[]
required=[
 'VERSION','README.md','calculations/v0_8/optimization_doe.csv',
 'calculations/v0_8/python_screening/static_screening_summary.csv',
 'analysis/ansys/v0_8/model/optimized_beam_nodes.csv',
 'analysis/ansys/v0_8/model/optimized_beam_elements.csv',
 'cad/primary_structure/v0_8/neutral/asterion_v0_8_optimized_structure.glb'
]
for rel in required:
 if not (root/rel).exists(): errors.append(f'missing: {rel}')
if (root/'VERSION').read_text().strip()!='0.8.0': errors.append('incorrect VERSION')
n=pd.read_csv(root/'analysis/ansys/v0_8/model/optimized_beam_nodes.csv')
e=pd.read_csv(root/'analysis/ansys/v0_8/model/optimized_beam_elements.csv')
s=pd.read_csv(root/'analysis/ansys/v0_8/model/optimized_beam_sections.csv')
if len(n)!=222: errors.append(f'node count {len(n)} != 222')
if len(e)!=648: errors.append(f'element count {len(e)} != 648')
ids=set(n.node_id.astype(int))
if not set(e.node_1.astype(int)).issubset(ids) or not set(e.node_2.astype(int)).issubset(ids): errors.append('invalid element node reference')
if (e.length_mm<=0).any(): errors.append('nonpositive element length')
mass=float(s.estimated_mass_kg.sum())
if not 10350 <= mass <= 10500: errors.append(f'structural mass outside control range: {mass}')
r=pd.read_csv(root/'calculations/v0_8/python_screening/static_screening_summary.csv').set_index('load_case_id')
checks={'LC-STR-02':5.0,'LC-STR-07':25.0,'LC-STR-08':10.0,'LC-STR-09':15.0}
for c,lim in checks.items():
 if c not in r.index or float(r.loc[c,'max_translation_mm'])>lim: errors.append(f'{c} failed')
modal=pd.read_csv(root/'calculations/v0_8/python_screening/supported_modal_screening.csv')
if float(modal.iloc[0].frequency_Hz)<0.15: errors.append('modal criterion failed')
scene=trimesh.load(root/'cad/primary_structure/v0_8/neutral/asterion_v0_8_optimized_structure.glb',force='scene')
if len(scene.geometry)<600: errors.append('GLB geometry count too low')
report={'status':'PASS' if not errors else 'FAIL','errors':errors,'nodes':len(n),'elements':len(e),'structural_mass_kg':mass,'first_mode_Hz':float(modal.iloc[0].frequency_Hz)}
(root/'calculations/v0_8/v0_8_validation_report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
sys.exit(1 if errors else 0)
