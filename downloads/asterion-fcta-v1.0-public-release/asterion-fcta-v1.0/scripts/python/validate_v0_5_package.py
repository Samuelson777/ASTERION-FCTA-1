#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, math, py_compile, sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = [
    'README.md','VERSION','PROJECT_STATUS.md','CHANGELOG.md',
    'analysis/ansys/v0_3/model/beam_nodes.csv',
    'analysis/ansys/v0_3/model/beam_elements.csv',
    'analysis/ansys/v0_4/model/remote_mass_definitions.csv',
    'analysis/ansys/v0_5/model/load_case_definitions.csv',
    'analysis/ansys/v0_5/model/boundary_conditions.csv',
    'analysis/ansys/v0_5/model/acceptance_criteria.csv',
    'analysis/ansys/v0_5/model/mesh_convergence_plan.csv',
    'analysis/ansys/v0_5/workbench/ANSYS_Workbench_V0_5_Guide.md',
    'calculations/v0_5/V0_5_structural_screening_report.md',
    'calculations/v0_5/python_screening/static_screening_summary.csv',
    'calculations/v0_5/python_screening/supported_modal_screening.csv',
    'scripts/python/v0_5/asterion_frame_screening.py',
    'media/plots/v0_5/v0_5_static_displacement_screening.png',
    'media/plots/v0_5/v0_5_static_stress_screening.png',
    'media/plots/v0_5/v0_5_supported_modal_screening.png',
]

def check(cond, message):
    if not cond:
        raise AssertionError(message)

for rel in REQUIRED:
    check((ROOT/rel).is_file(), f'Missing required file: {rel}')
check((ROOT/'VERSION').read_text().strip() == '0.5.0', 'VERSION mismatch')

nodes=pd.read_csv(ROOT/'analysis/ansys/v0_3/model/beam_nodes.csv')
elems=pd.read_csv(ROOT/'analysis/ansys/v0_3/model/beam_elements.csv')
remote=pd.read_csv(ROOT/'analysis/ansys/v0_4/model/remote_mass_definitions.csv')
static=pd.read_csv(ROOT/'calculations/v0_5/python_screening/static_screening_summary.csv')
modal=pd.read_csv(ROOT/'calculations/v0_5/python_screening/supported_modal_screening.csv')
loads=pd.read_csv(ROOT/'analysis/ansys/v0_5/model/load_case_definitions.csv')

check(len(nodes)==222, f'Expected 222 nodes, got {len(nodes)}')
check(len(elems)==580, f'Expected 580 elements, got {len(elems)}')
check(nodes.node_id.is_unique, 'Duplicate node IDs')
check(elems.element_id.is_unique, 'Duplicate element IDs')
valid=set(nodes.node_id)
check(set(elems.node_1).issubset(valid) and set(elems.node_2).issubset(valid),'Invalid element node reference')
check((elems.length_mm>0).all(),'Non-positive element length')
check(abs(remote.mass_kg.sum() - 42800.0) < 1e-6, f'Remote mass ledger expected 42,800 kg, got {remote.mass_kg.sum()}')
check(len(static)==7, 'Expected seven Python static screening cases')
check(set(static.load_case_id)=={f'LC-STR-{i:02d}' for i in range(1,8)},'Static case IDs mismatch')
check(len(modal)>=10 and (modal.frequency_Hz>0).all(),'Modal screening missing/invalid')
check(float(modal.frequency_Hz.iloc[0])>0.10,'First supported screening frequency below provisional 0.10 Hz')
ring=static.loc[static.load_case_id=='LC-STR-05'].iloc[0]
dock=static.loc[static.load_case_id=='LC-STR-07'].iloc[0]
check(ring.max_translation_mm>25.0,'Expected ring braking redesign flag not present')
check(dock.max_translation_mm>25.0,'Expected misaligned docking redesign flag not present')
check(static.minimum_yield_factor.min()>1.5,'Screening yield factor below criterion')
check(static.minimum_member_euler_factor.min()>2.0,'Screening member Euler factor below criterion')
check({'LC-MOD-01','LC-MOD-02','LC-BUC-01'}.issubset(set(loads.load_case_id)),'Analysis matrix incomplete')

for py in ROOT.rglob('*.py'):
    py_compile.compile(str(py),doraise=True)

report={
 'version':'0.5.0','required_files':len(REQUIRED),'nodes':len(nodes),'elements':len(elems),
 'remote_mass_kg':float(remote.mass_kg.sum()),'static_cases':len(static),
 'first_supported_screening_frequency_Hz':float(modal.frequency_Hz.iloc[0]),
 'governing_displacement_case':str(static.loc[static.max_translation_mm.idxmax(),'load_case_id']),
 'governing_displacement_mm':float(static.max_translation_mm.max()),
 'status':'PASS'
}
out=ROOT/'calculations/v0_5/v0_5_validation_report.json'
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
