#!/usr/bin/env python3
"""Validate ASTERION FCTA-1 Version 0.3 release package."""
from __future__ import annotations
import csv, hashlib, json, math, py_compile, sys
from pathlib import Path
import trimesh

ROOT=Path(__file__).resolve().parents[2]
errors=[]; warnings=[]; checks=[]

def ok(name, condition, detail=''):
    checks.append({'check':name,'passed':bool(condition),'detail':detail})
    if not condition: errors.append(f'{name}: {detail}')

required=[
'README.md','VERSION','PROJECT_STATUS.md','CHANGELOG.md',
'cad/primary_structure/v0_3/neutral/asterion_v0_3_primary_structure.glb',
'cad/primary_structure/v0_3/neutral/asterion_v0_3_primary_structure.stl',
'cad/primary_structure/v0_3/neutral/asterion_v0_3_primary_structure.obj',
'cad/primary_structure/v0_3/nx_primary_structure_tutorial.md',
'cad/primary_structure/v0_3/nx_expressions_v0_3.txt',
'analysis/ansys/v0_3/model/beam_nodes.csv',
'analysis/ansys/v0_3/model/beam_elements.csv',
'analysis/ansys/v0_3/model/beam_sections.csv',
'analysis/ansys/v0_3/model/load_cases.csv',
'analysis/ansys/v0_3/apdl/asterion_line_model.inc',
'analysis/ansys/v0_3/apdl/solve_static_docking.mac',
'analysis/ansys/v0_3/apdl/solve_modal_free_free.mac',
'analysis/ansys/v0_3/apdl/solve_buckling_docking.mac',
'calculations/v0_3/preliminary_structural_sizing.md',
'calculations/v0_3/v0_3_structural_report.json',
'media/renders/v0_3_primary_structure_plan.png',
'media/renders/v0_3_primary_structure_front.png',
'web-viewer/models/asterion_v0_3_primary_structure.glb',
]
for rel in required:
    ok(f'required:{rel}',(ROOT/rel).is_file(),'missing' if not (ROOT/rel).is_file() else '')

ok('version', (ROOT/'VERSION').read_text().strip()=='0.3.0', (ROOT/'VERSION').read_text().strip())

with (ROOT/'analysis/ansys/v0_3/model/beam_nodes.csv').open(newline='',encoding='utf-8') as f:
    nodes={int(r['node_id']):(float(r['x_mm']),float(r['y_mm']),float(r['z_mm']),r['group']) for r in csv.DictReader(f)}
with (ROOT/'analysis/ansys/v0_3/model/beam_elements.csv').open(newline='',encoding='utf-8') as f:
    elements=list(csv.DictReader(f))
with (ROOT/'analysis/ansys/v0_3/model/beam_sections.csv').open(newline='',encoding='utf-8') as f:
    sections={int(r['section_id']):r for r in csv.DictReader(f)}
report=json.loads((ROOT/'calculations/v0_3/v0_3_structural_report.json').read_text())

ok('node_count',len(nodes)==report['node_count'],f"csv={len(nodes)} report={report['node_count']}")
ok('element_count',len(elements)==report['element_count'],f"csv={len(elements)} report={report['element_count']}")
ok('unique_node_ids',len(nodes)==len(set(nodes)),'')

zero=[]; badrefs=[]; badsec=[]; calc_len_mismatch=[]
for r in elements:
    eid=int(r['element_id']); n1=int(r['node_1']); n2=int(r['node_2']); sid=int(r['section_id'])
    if n1 not in nodes or n2 not in nodes: badrefs.append(eid); continue
    if sid not in sections: badsec.append(eid)
    a=nodes[n1][:3]; b=nodes[n2][:3]
    L=math.dist(a,b)
    if L < 1e-6: zero.append(eid)
    if abs(L-float(r['length_mm']))>0.01: calc_len_mismatch.append(eid)
ok('element_node_references',not badrefs,str(badrefs[:10]))
ok('section_references',not badsec,str(badsec[:10]))
ok('zero_length_elements',not zero,str(zero[:10]))
ok('element_length_table',not calc_len_mismatch,str(calc_len_mismatch[:10]))

outer1=sum(1 for v in nodes.values() if v[3]=='RING1_OUTER')
outer2=sum(1 for v in nodes.values() if v[3]=='RING2_OUTER')
ok('ring_outer_node_counts',outer1==12 and outer2==12,f'{outer1},{outer2}')
prop=sum(1 for v in nodes.values() if v[3]=='PROP_MOUNT')
dock=sum(1 for v in nodes.values() if v[3]=='DOCK_FRAME')
ok('interface_node_counts',prop==6 and dock==8,f'prop={prop}, dock={dock}')

xs=[v[0] for v in nodes.values()]; ys=[v[1] for v in nodes.values()]; zs=[v[2] for v in nodes.values()]
ok('geometry_x_extent',min(xs)<=-21000 and max(xs)>=21400,f'{min(xs)}..{max(xs)}')
ok('geometry_ring_extent',max(abs(y) for y in ys)>=12000 and max(abs(z) for z in zs)>=12000,'')

mesh=trimesh.load(ROOT/'cad/primary_structure/v0_3/neutral/asterion_v0_3_primary_structure.glb',force='scene')
geom_count=len(mesh.geometry)
face_count=sum(len(g.faces) for g in mesh.geometry.values())
ok('glb_geometry',geom_count>=4 and face_count>1000,f'geometries={geom_count}, faces={face_count}')

apdl=(ROOT/'analysis/ansys/v0_3/apdl/asterion_line_model.inc').read_text()
n_cmd=sum(1 for line in apdl.splitlines() if line.startswith('N,'))
e_cmd=sum(1 for line in apdl.splitlines() if line.startswith('E,'))
ok('apdl_node_count',n_cmd==len(nodes),f'{n_cmd}')
ok('apdl_element_count',e_cmd==len(elements),f'{e_cmd}')
ok('apdl_sections',all(f'SECTYPE,{sid},' in apdl for sid in sections),'')

for py in ROOT.rglob('*.py'):
    try: py_compile.compile(str(py),doraise=True)
    except Exception as exc: errors.append(f'python syntax {py.relative_to(ROOT)}: {exc}')
ok('python_syntax',not any(e.startswith('python syntax') for e in errors),'')

# Write validation records before the checksum manifest so their final bytes are hashed.
result={'version':'0.3.0','passed':not errors,'checks':checks,'warnings':warnings,'errors':errors,'summary':{'nodes':len(nodes),'elements':len(elements),'sections':len(sections),'glb_geometries':geom_count,'glb_faces':face_count}}
(ROOT/'calculations/v0_3/v0_3_validation_report.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
(ROOT/'calculations/v0_3/v0_3_validation_output.txt').write_text(('PASS' if not errors else 'FAIL')+'\n'+json.dumps(result['summary'],indent=2)+'\n'+('\n'.join(errors) if errors else 'No validation errors.\n'),encoding='utf-8')

# Rebuild manifest excluding the manifest itself and volatile cache/console files.
manifest=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or p.name=='SHA256SUMS.txt' or '__pycache__' in p.parts or p.name=='validation_console.json': continue
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    manifest.append(f'{h}  {p.relative_to(ROOT).as_posix()}')
(ROOT/'SHA256SUMS.txt').write_text('\n'.join(manifest)+'\n',encoding='utf-8')

print(json.dumps(result,indent=2))
sys.exit(0 if not errors else 1)
