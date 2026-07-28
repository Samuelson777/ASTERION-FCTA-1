from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import py_compile
import re
import shutil
import textwrap
import zipfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import trimesh

SRC = Path('/mnt/data/asterion-fcta-v0.6')
DST = Path('/mnt/data/asterion-fcta-v0.7')
ZIP_PATH = Path('/mnt/data/asterion-fcta-v0.7-manufacturing-cam.zip')

if DST.exists():
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)


def write_text(rel: str, content: str) -> None:
    p = DST / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(content).lstrip(), encoding='utf-8')


def write_csv(rel: str, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    p = DST / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with p.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def add_box(extents, center=(0,0,0), transform=None):
    m = trimesh.creation.box(extents=extents)
    m.apply_translation(center)
    if transform is not None:
        m.apply_transform(transform)
    return m


def cylinder_between(p1, p2, radius, sections=24):
    p1 = np.array(p1, float); p2 = np.array(p2, float)
    vec = p2-p1; length = float(np.linalg.norm(vec))
    m = trimesh.creation.cylinder(radius=radius, height=length, sections=sections)
    direction = vec/length
    T = trimesh.geometry.align_vectors([0,0,1], direction)
    if T is not None:
        m.apply_transform(T)
    m.apply_translation((p1+p2)/2)
    return m


def extrude_polygon_fan(points2d: np.ndarray, thickness: float, axis='y') -> trimesh.Trimesh:
    pts = np.asarray(points2d, float)
    n = len(pts)
    c = pts.mean(axis=0)
    # vertices: lower ring, upper ring, lower center, upper center
    if axis == 'y':
        low = np.column_stack([pts[:,0], np.full(n,-thickness/2), pts[:,1]])
        high = np.column_stack([pts[:,0], np.full(n,thickness/2), pts[:,1]])
        cl = np.array([c[0],-thickness/2,c[1]])
        ch = np.array([c[0], thickness/2,c[1]])
    elif axis == 'z':
        low = np.column_stack([pts[:,0], pts[:,1], np.full(n,-thickness/2)])
        high = np.column_stack([pts[:,0], pts[:,1], np.full(n,thickness/2)])
        cl = np.array([c[0],c[1],-thickness/2])
        ch = np.array([c[0],c[1], thickness/2])
    else:
        raise ValueError(axis)
    vertices = np.vstack([low, high, cl, ch])
    faces=[]; il=2*n; ih=2*n+1
    for i in range(n):
        j=(i+1)%n
        faces.append([i,j,n+j]); faces.append([i,n+j,n+i])
        faces.append([il,j,i])
        faces.append([ih,n+i,n+j])
    mesh=trimesh.Trimesh(vertices=vertices, faces=np.array(faces), process=True)
    return mesh


def combine(meshes):
    return trimesh.util.concatenate(meshes)


def export_mesh_set(name: str, mesh: trimesh.Trimesh, subdir='cad/manufacturing_parts/v0_7/neutral'):
    base = DST / subdir
    base.mkdir(parents=True, exist_ok=True)
    mesh.export(base/f'{name}.stl')
    mesh.export(base/f'{name}.obj')
    scene = trimesh.Scene(); scene.add_geometry(mesh, node_name=name, geom_name=name)
    scene.export(base/f'{name}.glb')


def write_dxf(rel: str, entities: list[tuple]):
    p=DST/rel; p.parent.mkdir(parents=True, exist_ok=True)
    out=['0','SECTION','2','HEADER','0','ENDSEC','0','SECTION','2','ENTITIES']
    for e in entities:
        if e[0]=='LINE':
            _,x1,y1,x2,y2,layer=e
            out += ['0','LINE','8',layer,'10',f'{x1:.4f}','20',f'{y1:.4f}','30','0','11',f'{x2:.4f}','21',f'{y2:.4f}','31','0']
        elif e[0]=='CIRCLE':
            _,x,y,r,layer=e
            out += ['0','CIRCLE','8',layer,'10',f'{x:.4f}','20',f'{y:.4f}','30','0','40',f'{r:.4f}']
        elif e[0]=='TEXT':
            _,x,y,h,text,layer=e
            out += ['0','TEXT','8',layer,'10',f'{x:.4f}','20',f'{y:.4f}','30','0','40',f'{h:.4f}','1',str(text)]
    out += ['0','ENDSEC','0','EOF']
    p.write_text('\n'.join(out)+'\n', encoding='ascii', errors='ignore')


def svg_drawing(rel: str, title: str, width_mm: float, height_mm: float, shapes: str, notes: list[str]):
    p=DST/rel; p.parent.mkdir(parents=True, exist_ok=True)
    note_svg=''.join(f'<text x="20" y="{height_mm-55+i*6}" font-size="4">{n}</text>' for i,n in enumerate(notes))
    content=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width_mm}mm" height="{height_mm}mm" viewBox="0 0 {width_mm} {height_mm}">
    <rect x="2" y="2" width="{width_mm-4}" height="{height_mm-4}" fill="white" stroke="black" stroke-width="0.6"/>
    <text x="10" y="12" font-size="7" font-weight="bold">{title}</text>
    {shapes}
    <rect x="8" y="{height_mm-65}" width="{width_mm-16}" height="55" fill="none" stroke="black" stroke-width="0.4"/>
    {note_svg}
    <text x="{width_mm-75}" y="{height_mm-18}" font-size="4">ASTERION FCTA-1 · V0.7 · UNITS mm</text>
    </svg>'''
    p.write_text(content, encoding='utf-8')


def naca0012_points(chord=220.0, n=70):
    x=np.linspace(0,1,n)
    yt=5*0.12*(0.2969*np.sqrt(x)-0.1260*x-0.3516*x**2+0.2843*x**3-0.1015*x**4)
    upper=np.column_stack([x*chord, yt*chord])
    lower=np.column_stack([x[::-1]*chord, -yt[::-1]*chord])
    pts=np.vstack([upper, lower[1:-1]])
    pts[:,0]-=chord/2
    return pts


# --------- Version metadata ---------
write_text('VERSION','0.7.0\n')
write_text('CHANGELOG.md', '''
# Changelog

## 0.7.0 — NX CAM and manufacturing portfolio

- Added four representative manufacturing demonstrator parts.
- Added neutral STL, OBJ and GLB geometry for each demonstrator.
- Added NX CAM operation plans, tool library, cutting-data register and fixture plans.
- Added controlled 2D SVG/DXF drawings and inspection records.
- Added simulation-only educational G-code and automated safety checks.
- Added printable 1:50 spacecraft and mechanism demonstrators.
- Added manufacturing cost/time screening, quality plan and release validation.

Previous release history is retained in the repository.
''')

# --------- Geometry: Part 1 gimbal bracket ---------
base=add_box((160,120,18),(0,0,9))
ear1=add_box((20,34,95),(-48,-35,65.5))
ear2=add_box((20,34,95),(-48,35,65.5))
bridge=add_box((40,104,18),(-48,0,110))
rib1=cylinder_between((-38,-35,20),(-38,-35,100),7)
rib2=cylinder_between((-38,35,20),(-38,35,100),7)
bracket=combine([base,ear1,ear2,bridge,rib1,rib2])
export_mesh_set('AST-TP-2101_thruster_gimbal_bracket', bracket)

# Part 2 bearing housing: annulus + flange + lugs
ann=trimesh.creation.annulus(r_min=47.5,r_max=70,height=55,sections=96)
ann.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[0,1,0]))
fl1=trimesh.creation.annulus(r_min=45,r_max=82,height=10,sections=96)
fl1.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[0,1,0])); fl1.apply_translation((-32.5,0,0))
fl2=fl1.copy(); fl2.apply_translation((65,0,0))
lugs=[]
for a in [0,math.pi/2,math.pi,3*math.pi/2]:
    y=90*math.cos(a); z=90*math.sin(a)
    lugs.append(add_box((75,22,28),(0,y,z)))
bearing=combine([ann,fl1,fl2,*lugs])
export_mesh_set('AST-RG-3201_ring_bearing_housing', bearing)

# Part 3 NACA wing rib
rib_pts=naca0012_points(220,80)
wing_rib=extrude_polygon_fan(rib_pts,8,axis='y')
# add rectangular mounting foot
foot=add_box((75,8,20),(-60,0,-16))
wing_rib=combine([wing_rib,foot])
export_mesh_set('AST-SK-4301_skimmer_wing_rib', wing_rib)

# Part 4 lightweight bulkhead frame
meshes=[]
# perimeter bars at z=6 mm
for cx,cy,sx,sy in [(0,105,260,14),(0,-105,260,14),(-123,0,14,210),(123,0,14,210)]:
    meshes.append(add_box((sx,sy,12),(cx,cy,6)))
# central ring
ring=trimesh.creation.annulus(r_min=42,r_max=55,height=12,sections=72)
meshes.append(ring)
# radial/diagonal bars in XY plane
def bar_xy(p1,p2,width=10,height=12):
    p1=np.array(p1,float); p2=np.array(p2,float); d=p2-p1; L=np.linalg.norm(d); ang=math.atan2(d[1],d[0])
    m=add_box((L,width,height),((p1[0]+p2[0])/2,(p1[1]+p2[1])/2,height/2))
    m.apply_transform(trimesh.transformations.rotation_matrix(ang,[0,0,1],point=[(p1[0]+p2[0])/2,(p1[1]+p2[1])/2,height/2]))
    return m
for p in [((-116,-98),(-48,-20)),((-116,98),(-48,20)),((116,-98),(48,-20)),((116,98),(48,20)),((-48,-20),(48,20)),((-48,20),(48,-20))]:
    meshes.append(bar_xy(*p, width=10))
bulkhead=combine(meshes)
export_mesh_set('AST-ST-1401_lightweight_bulkhead', bulkhead)

# Fixtures
fixture_base=add_box((260,200,20),(0,0,10))
loc1=add_box((25,25,25),(-70,-50,32.5)); loc2=add_box((25,25,25),(70,-50,32.5)); stop=add_box((20,160,30),(-115,0,35))
fixture=combine([fixture_base,loc1,loc2,stop])
export_mesh_set('AST-FX-7101_gimbal_bracket_fixture', fixture, 'cam/nx_cam/v0_7/fixtures/neutral')
softjaw1=add_box((110,35,45),(0,-35,22.5)); softjaw2=add_box((110,35,45),(0,35,22.5))
softjaws=combine([softjaw1,softjaw2])
export_mesh_set('AST-FX-7201_bearing_soft_jaws', softjaws, 'cam/nx_cam/v0_7/fixtures/neutral')

# Printable prototypes
(DST/'prototype/v0_7/stl').mkdir(parents=True,exist_ok=True)
full_glb=DST/'cad/full_assembly/v0_4/neutral/asterion_v0_4_full_assembly.glb'
if full_glb.exists():
    scene=trimesh.load(full_glb, force='scene')
    proto=scene.dump(concatenate=True)
    proto.apply_scale(0.02)
    proto.export(DST/'prototype/v0_7/stl/asterion_full_vehicle_1_to_50.stl')
# ring drive demo
ring_demo=trimesh.creation.annulus(r_min=110,r_max=125,height=12,sections=96)
hub=trimesh.creation.annulus(r_min=20,r_max=35,height=20,sections=64)
spokes=[]
for a in np.linspace(0,2*math.pi,12,endpoint=False):
    spokes.append(bar_xy((35*math.cos(a),35*math.sin(a)),(110*math.cos(a),110*math.sin(a)),width=7,height=12))
ring_drive=combine([ring_demo,hub,*spokes])
(DST/'prototype/v0_7/stl').mkdir(parents=True,exist_ok=True)
ring_drive.export(DST/'prototype/v0_7/stl/ring_drive_demonstrator_1_to_5.stl')
# docking latch demo
latch=combine([add_box((100,60,15),(0,0,7.5)), add_box((20,25,65),(-30,0,40)), add_box((20,25,65),(30,0,40)), cylinder_between((-30,0,65),(30,0,65),8)])
latch.export(DST/'prototype/v0_7/stl/docking_latch_demonstrator_1_to_5.stl')

# --------- Drawings ---------
draw_dir='cad/manufacturing_parts/v0_7/drawings'
svg_drawing(f'{draw_dir}/AST-TP-2101_thruster_gimbal_bracket.svg','AST-TP-2101 THRUSTER GIMBAL BRACKET',297,210,
'''<rect x="55" y="42" width="160" height="70" fill="none" stroke="black" stroke-width="0.6"/>
<rect x="86" y="30" width="20" height="95" fill="none" stroke="black" stroke-width="0.6"/>
<rect x="164" y="30" width="20" height="95" fill="none" stroke="black" stroke-width="0.6"/>
<circle cx="96" cy="72" r="9" fill="none" stroke="black"/>
<circle cx="174" cy="72" r="9" fill="none" stroke="black"/>
<line x1="55" y1="132" x2="215" y2="132" stroke="black"/><text x="125" y="139" font-size="5">160 ±0.20</text>
<line x1="225" y1="42" x2="225" y2="112" stroke="black"/><text x="229" y="80" font-size="5">120 ±0.20</text>''',
['MATERIAL: ALUMINIUM 6061-T6 DEMONSTRATOR','DATUM A: BASE FACE','BORE PAIR: Ø18 H7, POSITION 0.10 TO A|B','BREAK EDGES 0.5 MAX; DEBURR ALL FEATURES','GENERAL TOLERANCE: ISO 2768-mK'])
write_dxf(f'{draw_dir}/AST-TP-2101_thruster_gimbal_bracket.dxf',[
('LINE',0,0,160,0,'OUTLINE'),('LINE',160,0,160,120,'OUTLINE'),('LINE',160,120,0,120,'OUTLINE'),('LINE',0,120,0,0,'OUTLINE'),
('CIRCLE',40,25,9,'HOLES'),('CIRCLE',120,25,9,'HOLES'),('TEXT',0,-15,6,'AST-TP-2101 TOP VIEW','TEXT')])

svg_drawing(f'{draw_dir}/AST-RG-3201_ring_bearing_housing.svg','AST-RG-3201 RING BEARING HOUSING',297,210,
'''<circle cx="135" cy="78" r="55" fill="none" stroke="black" stroke-width="0.7"/><circle cx="135" cy="78" r="32" fill="none" stroke="black" stroke-width="0.7"/>
<circle cx="135" cy="20" r="4" fill="none" stroke="black"/><circle cx="135" cy="136" r="4" fill="none" stroke="black"/><circle cx="77" cy="78" r="4" fill="none" stroke="black"/><circle cx="193" cy="78" r="4" fill="none" stroke="black"/>
<line x1="80" y1="145" x2="190" y2="145" stroke="black"/><text x="122" y="152" font-size="5">Ø164 flange</text>''',
['MATERIAL: ALUMINIUM 7075-T6 DEMONSTRATOR','BEARING SEAT: Ø95 H7','CONCENTRICITY: 0.04 TO DATUM A','4x Ø8.5 THRU ON Ø180 PCD','TURNING + 3-AXIS MILLING WORKFLOW'])
write_dxf(f'{draw_dir}/AST-RG-3201_ring_bearing_housing.dxf',[
('CIRCLE',0,0,82,'OUTLINE'),('CIRCLE',0,0,47.5,'BORE'),('CIRCLE',0,90,4.25,'HOLES'),('CIRCLE',90,0,4.25,'HOLES'),('CIRCLE',0,-90,4.25,'HOLES'),('CIRCLE',-90,0,4.25,'HOLES'),('TEXT',-60,-105,6,'AST-RG-3201 FRONT VIEW','TEXT')])

pts=naca0012_points(220,60)
path=' '.join(('M' if i==0 else 'L')+f'{148+p[0]*0.75:.2f},{80-p[1]*0.75:.2f}' for i,p in enumerate(pts))+' Z'
svg_drawing(f'{draw_dir}/AST-SK-4301_skimmer_wing_rib.svg','AST-SK-4301 SKIMMER WING RIB',297,210,
 f'''<path d="{path}" fill="none" stroke="black" stroke-width="0.6"/><line x1="65" y1="115" x2="230" y2="115" stroke="black"/><text x="135" y="123" font-size="5">CHORD 220</text>''',
['MATERIAL: ALUMINIUM 2024-T3 PLATE','THICKNESS: 8.0 ±0.10','PROFILE TOLERANCE: 0.25 TO DATUM A','DATUM A: INBOARD MOUNTING FACE','FINISH CONTOUR WITH LOW-RADIAL-ENGAGEMENT PASS'])
write_dxf(f'{draw_dir}/AST-SK-4301_skimmer_wing_rib.dxf', [('LINE',float(pts[i,0]),float(pts[i,1]),float(pts[(i+1)%len(pts),0]),float(pts[(i+1)%len(pts),1]),'PROFILE') for i in range(len(pts))]+[('TEXT',-65,-35,6,'AST-SK-4301 PROFILE','TEXT')])

svg_drawing(f'{draw_dir}/AST-ST-1401_lightweight_bulkhead.svg','AST-ST-1401 LIGHTWEIGHT BULKHEAD',297,210,
'''<rect x="55" y="25" width="180" height="125" fill="none" stroke="black" stroke-width="0.7"/><circle cx="145" cy="87" r="28" fill="none" stroke="black" stroke-width="0.7"/>
<line x1="55" y1="25" x2="117" y2="70" stroke="black"/><line x1="55" y1="150" x2="117" y2="104" stroke="black"/><line x1="235" y1="25" x2="173" y2="70" stroke="black"/><line x1="235" y1="150" x2="173" y2="104" stroke="black"/>
<line x1="117" y1="70" x2="173" y2="104" stroke="black"/><line x1="117" y1="104" x2="173" y2="70" stroke="black"/>''',
['MATERIAL: ALUMINIUM 6061-T6 PLATE/DEMONSTRATOR','FINISHED THICKNESS: 12.0 ±0.15','DATUM A: AFT FACE; DATUM B/C: OUTER EDGES','REMOVE SHARP INTERNAL CORNERS WITH R3 MIN','VERIFY FLATNESS 0.40 AFTER MACHINING'])
write_dxf(f'{draw_dir}/AST-ST-1401_lightweight_bulkhead.dxf',[
('LINE',-130,-105,130,-105,'OUTLINE'),('LINE',130,-105,130,105,'OUTLINE'),('LINE',130,105,-130,105,'OUTLINE'),('LINE',-130,105,-130,-105,'OUTLINE'),('CIRCLE',0,0,42,'BORE'),('TEXT',-85,-125,6,'AST-ST-1401 FRONT VIEW','TEXT')])

# --------- CAM data ---------
tools=[
{'tool_id':'T01','type':'face mill','diameter_mm':50,'flutes':5,'holder':'HSK63A-FM50','material':'carbide inserts','use':'facing 6061','max_rpm':12000},
{'tool_id':'T02','type':'flat end mill','diameter_mm':12,'flutes':3,'holder':'ER32-12','material':'carbide','use':'adaptive roughing 6061/7075','max_rpm':18000},
{'tool_id':'T03','type':'flat end mill','diameter_mm':6,'flutes':3,'holder':'ER25-6','material':'carbide','use':'rest milling and profiles','max_rpm':20000},
{'tool_id':'T04','type':'ball end mill','diameter_mm':6,'flutes':2,'holder':'ER25-6','material':'carbide','use':'surface finishing','max_rpm':18000},
{'tool_id':'T05','type':'spot drill','diameter_mm':6,'flutes':2,'holder':'ER20-6','material':'carbide','use':'spot drilling','max_rpm':12000},
{'tool_id':'T06','type':'twist drill','diameter_mm':8.5,'flutes':2,'holder':'ER20-9','material':'carbide','use':'mounting holes','max_rpm':10000},
{'tool_id':'T07','type':'reamer','diameter_mm':18,'flutes':6,'holder':'floating reamer','material':'HSS-E','use':'gimbal bores H7','max_rpm':2000},
{'tool_id':'T08','type':'chamfer mill','diameter_mm':12,'flutes':3,'holder':'ER25-12','material':'carbide','use':'edge break','max_rpm':14000},
{'tool_id':'T09','type':'turning insert','diameter_mm':'n/a','flutes':'n/a','holder':'SCLCR-2020K09','material':'CCGT aluminium grade','use':'housing OD/ID turning','max_rpm':4000},
{'tool_id':'T10','type':'grooving insert','diameter_mm':3,'flutes':'n/a','holder':'MGEHR-2020-3','material':'carbide','use':'bearing shoulder groove','max_rpm':3000},
]
write_csv('cam/nx_cam/v0_7/tool_library.csv',tools)

cutting=[
{'material':'Al 6061-T6','tool_id':'T01','operation':'facing','surface_speed_m_min':650,'rpm':4000,'feed_per_tooth_mm':0.12,'feed_mm_min':2400,'axial_depth_mm':1.0,'radial_engagement_pct':65},
{'material':'Al 6061-T6','tool_id':'T02','operation':'adaptive roughing','surface_speed_m_min':450,'rpm':11900,'feed_per_tooth_mm':0.08,'feed_mm_min':2850,'axial_depth_mm':12,'radial_engagement_pct':18},
{'material':'Al 6061-T6','tool_id':'T03','operation':'profile finish','surface_speed_m_min':350,'rpm':18000,'feed_per_tooth_mm':0.035,'feed_mm_min':1890,'axial_depth_mm':6,'radial_engagement_pct':5},
{'material':'Al 7075-T6','tool_id':'T02','operation':'adaptive roughing','surface_speed_m_min':350,'rpm':9300,'feed_per_tooth_mm':0.07,'feed_mm_min':1950,'axial_depth_mm':10,'radial_engagement_pct':15},
{'material':'Al 2024-T3','tool_id':'T03','operation':'rib profile','surface_speed_m_min':280,'rpm':14800,'feed_per_tooth_mm':0.035,'feed_mm_min':1550,'axial_depth_mm':4,'radial_engagement_pct':8},
{'material':'PLA prototype','tool_id':'FDM','operation':'printing','surface_speed_m_min':'n/a','rpm':'n/a','feed_per_tooth_mm':'n/a','feed_mm_min':60,'axial_depth_mm':0.20,'radial_engagement_pct':'n/a'},
]
write_csv('cam/nx_cam/v0_7/cutting_parameters.csv',cutting)

operations=[
{'part_id':'AST-TP-2101','setup':'S1','operation_no':10,'operation':'Face stock','tool_id':'T01','workholding':'AST-FX-7101','datum':'A','estimated_min':3.5,'verification':'stock allowance +0.5 mm'},
{'part_id':'AST-TP-2101','setup':'S1','operation_no':20,'operation':'Adaptive rough bracket envelope','tool_id':'T02','workholding':'AST-FX-7101','datum':'A-B-C','estimated_min':18.0,'verification':'holder collision check'},
{'part_id':'AST-TP-2101','setup':'S1','operation_no':30,'operation':'Rest mill ears and bridge','tool_id':'T03','workholding':'AST-FX-7101','datum':'A-B-C','estimated_min':11.0,'verification':'0.3 mm finish stock'},
{'part_id':'AST-TP-2101','setup':'S2','operation_no':40,'operation':'Drill and ream gimbal bores','tool_id':'T05/T07','workholding':'AST-FX-7101','datum':'A-B','estimated_min':8.0,'verification':'Ø18 H7 plug gauge'},
{'part_id':'AST-TP-2101','setup':'S2','operation_no':50,'operation':'Chamfer and deburr','tool_id':'T08','workholding':'AST-FX-7101','datum':'A','estimated_min':4.0,'verification':'0.5 max edge break'},
{'part_id':'AST-RG-3201','setup':'LATHE-1','operation_no':10,'operation':'Face, rough OD and bore','tool_id':'T09','workholding':'AST-FX-7201','datum':'A','estimated_min':22.0,'verification':'leave 0.4 mm finish stock'},
{'part_id':'AST-RG-3201','setup':'LATHE-2','operation_no':20,'operation':'Finish bearing seat and shoulders','tool_id':'T09/T10','workholding':'AST-FX-7201','datum':'A','estimated_min':17.0,'verification':'Ø95 H7 and Ra 1.6'},
{'part_id':'AST-RG-3201','setup':'MILL-1','operation_no':30,'operation':'Mill lugs and drill bolt circle','tool_id':'T02/T06','workholding':'angle fixture','datum':'A-B','estimated_min':24.0,'verification':'PCD position 0.15'},
{'part_id':'AST-SK-4301','setup':'S1','operation_no':10,'operation':'Face plate and profile rough','tool_id':'T01/T02','workholding':'vacuum + tabs','datum':'A','estimated_min':12.0,'verification':'minimum tab thickness 2 mm'},
{'part_id':'AST-SK-4301','setup':'S1','operation_no':20,'operation':'Finish aerodynamic profile','tool_id':'T03','workholding':'vacuum + tabs','datum':'A-B','estimated_min':9.0,'verification':'profile 0.25'},
{'part_id':'AST-ST-1401','setup':'S1','operation_no':10,'operation':'Face and adaptive clear bays','tool_id':'T01/T02','workholding':'modular grid plate','datum':'A-B-C','estimated_min':38.0,'verification':'thin-wall sequence alternating bays'},
{'part_id':'AST-ST-1401','setup':'S1','operation_no':20,'operation':'Finish ribs and central bore','tool_id':'T03','workholding':'modular grid plate','datum':'A-B-C','estimated_min':20.0,'verification':'flatness inspection after release'},
]
write_csv('cam/nx_cam/v0_7/operation_plan.csv',operations)

fixtures=[
{'fixture_id':'AST-FX-7101','part_id':'AST-TP-2101','principle':'3-2-1 location','primary_restraints':'3 hardened rest buttons on datum A','secondary_restraints':'2 side locators on datum B','tertiary_restraint':'1 end stop on datum C','clamps':'4 low-profile swing clamps','risk':'ear distortion','control':'clamp over solid base regions only'},
{'fixture_id':'AST-FX-7201','part_id':'AST-RG-3201','principle':'machinable soft jaws','primary_restraints':'axial jaw face','secondary_restraints':'turned pilot diameter','tertiary_restraint':'clocking pin for lug milling','clamps':'3-jaw chuck / mill fixture','risk':'ring ovalisation','control':'low jaw force and verify roundness'},
{'fixture_id':'AST-FX-7301','part_id':'AST-SK-4301','principle':'vacuum fixture with sacrificial tabs','primary_restraints':'vacuum bed','secondary_restraints':'2 dowel pins','tertiary_restraint':'end stop','clamps':'vacuum plus edge tabs','risk':'thin rib chatter','control':'leave onion skin and finish last'},
{'fixture_id':'AST-FX-7401','part_id':'AST-ST-1401','principle':'modular grid plate','primary_restraints':'6 rest pads','secondary_restraints':'2 edge locators','tertiary_restraint':'1 end stop','clamps':'distributed toe clamps','risk':'post-release warp','control':'balanced bay sequence and intermediate stress-relief check'},
]
write_csv('cam/nx_cam/v0_7/fixture_plan.csv',fixtures)

inspection=[
{'characteristic_id':'C01','part_id':'AST-TP-2101','feature':'datum A flatness','requirement':'0.10 mm','method':'surface plate + dial indicator','sampling':'100% demonstrator','record':'inspection_report_AST-TP-2101.csv'},
{'characteristic_id':'C02','part_id':'AST-TP-2101','feature':'gimbal bore diameter','requirement':'Ø18 H7','method':'three-point bore gauge / plug gauge','sampling':'100%','record':'inspection_report_AST-TP-2101.csv'},
{'characteristic_id':'C03','part_id':'AST-TP-2101','feature':'bore position','requirement':'0.10 to A|B','method':'CMM or height gauge setup','sampling':'100%','record':'inspection_report_AST-TP-2101.csv'},
{'characteristic_id':'C04','part_id':'AST-RG-3201','feature':'bearing seat','requirement':'Ø95 H7','method':'bore gauge','sampling':'100%','record':'inspection_report_AST-RG-3201.csv'},
{'characteristic_id':'C05','part_id':'AST-RG-3201','feature':'seat concentricity','requirement':'0.04 mm','method':'CMM or mandrel/runout','sampling':'100%','record':'inspection_report_AST-RG-3201.csv'},
{'characteristic_id':'C06','part_id':'AST-SK-4301','feature':'rib profile','requirement':'0.25 mm profile','method':'template + CMM/scan','sampling':'100%','record':'inspection_report_AST-SK-4301.csv'},
{'characteristic_id':'C07','part_id':'AST-ST-1401','feature':'final flatness','requirement':'0.40 mm','method':'surface plate + indicator','sampling':'100%','record':'inspection_report_AST-ST-1401.csv'},
{'characteristic_id':'C08','part_id':'AST-ST-1401','feature':'minimum rib width','requirement':'10.0 ±0.15 mm','method':'digital calliper/CMM','sampling':'all ribs','record':'inspection_report_AST-ST-1401.csv'},
]
write_csv('cam/nx_cam/v0_7/inspection_plan.csv',inspection)

risk_rows=[
{'risk_id':'MFG-01','process':'all machining','hazard':'unverified postprocessor or work offset','severity':5,'likelihood':3,'risk_score':15,'mitigation':'machine simulation, single-block dry run, prove-out above stock'},
{'risk_id':'MFG-02','process':'thin-wall milling','hazard':'part distortion/chatter','severity':3,'likelihood':4,'risk_score':12,'mitigation':'balanced sequence, sharp tools, light finish passes, inspection after unclamping'},
{'risk_id':'MFG-03','process':'bearing housing','hazard':'jaw-force ovalisation','severity':4,'likelihood':3,'risk_score':12,'mitigation':'soft jaws, low clamping force, roundness inspection'},
{'risk_id':'MFG-04','process':'drilling/reaming','hazard':'bore position or size out of tolerance','severity':4,'likelihood':2,'risk_score':8,'mitigation':'spot drill, pilot, controlled reaming, in-process gauge'},
{'risk_id':'MFG-05','process':'3D printing','hazard':'warping or weak layer orientation','severity':2,'likelihood':3,'risk_score':6,'mitigation':'orient loads in-plane, add brim, dimensional coupon'},
]
write_csv('cam/nx_cam/v0_7/manufacturing_risk_register.csv',risk_rows)

# --------- educational toolpaths and gcode ---------
gcode_dir=DST/'cam/nx_cam/v0_7/educational_gcode'; gcode_dir.mkdir(parents=True,exist_ok=True)

def write_gcode(name, body):
    header='''(ASTERION FCTA-1 V0.7 - SIMULATION-ONLY EDUCATIONAL G-CODE)\n(DO NOT RUN ON A MACHINE WITHOUT A VERIFIED NX POST, MACHINE SIMULATION, WORK OFFSET CHECK, TOOL LENGTH CHECK, AND SUPERVISED DRY RUN)\nG21 G17 G40 G49 G80 G90\nG54\n'''
    (gcode_dir/name).write_text(header+body+'\nM30\n',encoding='ascii')

write_gcode('AST-TP-2101_bracket_simulation.nc','''T2 M6\nS8000 M3\nG0 X-70 Y-50 Z25\nG1 Z2 F500\nG1 X70 F1800\nG1 Y50\nG1 X-70\nG1 Y-50\nG0 Z25\nT6 M6\nS5000 M3\nG0 X-40 Y-35 Z25\nG81 Z-20 R5 F450\nX40 Y35\nG80\nG0 Z25\nM5''')
write_gcode('AST-RG-3201_housing_simulation.nc','''(TURNING PROFILE REPRESENTED AS X DIAMETER / Z)\nT9 M6\nS1800 M3\nG0 X175 Z10\nG1 Z0 F350\nG1 X164\nG1 Z-55\nG1 X100\nG0 X180 Z20\nM5''')
# wing profile gcode from selected points
sample=pts[::5]
body=['T3 M6','S12000 M3','G0 X{:.3f} Y{:.3f} Z20'.format(sample[0,0],sample[0,1]),'G1 Z-2 F400']
for p in sample[1:]: body.append('G1 X{:.3f} Y{:.3f} F1500'.format(p[0],p[1]))
body.append('G1 X{:.3f} Y{:.3f}'.format(sample[0,0],sample[0,1])); body+=['G0 Z20','M5']
write_gcode('AST-SK-4301_rib_profile_simulation.nc','\n'.join(body))
write_gcode('AST-ST-1401_bulkhead_simulation.nc','''T2 M6\nS9000 M3\nG0 X-110 Y-85 Z25\nG1 Z-4 F400\nG1 X-30 Y-20 F1800\nG1 X30 Y20\nG1 X110 Y85\nG0 Z25\nG0 X-110 Y85\nG1 Z-4 F400\nG1 X-30 Y20 F1800\nG1 X30 Y-20\nG1 X110 Y-85\nG0 Z25\nM5''')

# toolpath CSV and plots
paths={
'AST-TP-2101':np.array([[-70,-50],[70,-50],[70,50],[-70,50],[-70,-50]]),
'AST-RG-3201':np.array([[175,10],[175,0],[164,0],[164,-55],[100,-55]]),
'AST-SK-4301':sample,
'AST-ST-1401':np.array([[-110,-85],[-30,-20],[30,20],[110,85],[np.nan,np.nan],[-110,85],[-30,20],[30,-20],[110,-85]])
}
plot_dir=DST/'media/plots/v0_7'; plot_dir.mkdir(parents=True,exist_ok=True)
for pid,arr in paths.items():
    rows=[]
    for i,p in enumerate(arr):
        rows.append({'sequence':i+1,'x_mm':p[0] if np.isfinite(p[0]) else '', 'y_or_z_mm':p[1] if np.isfinite(p[1]) else '', 'move':'separator' if not np.isfinite(p[0]) else 'cut'})
    write_csv(f'cam/nx_cam/v0_7/toolpaths/{pid}_toolpath.csv',rows)
    fig,ax=plt.subplots(figsize=(8,5))
    # split at nan
    start=0
    for idx in list(np.where(~np.isfinite(arr[:,0]))[0])+[len(arr)]:
        seg=arr[start:idx]
        if len(seg): ax.plot(seg[:,0],seg[:,1],marker='o')
        start=idx+1
    ax.set_title(f'{pid} — educational toolpath preview')
    ax.set_xlabel('X (mm)'); ax.set_ylabel('Y or Z (mm)'); ax.grid(True); ax.axis('equal')
    fig.tight_layout(); fig.savefig(plot_dir/f'{pid}_toolpath_preview.png',dpi=180); plt.close(fig)

# process-time/cost screening
hourly_rate_gbp=42.0
material_rows=[
{'part_id':'AST-TP-2101','material':'Al 6061-T6','stock':'180x140x125 mm billet','stock_mass_kg':8.51,'material_cost_gbp':68.0},
{'part_id':'AST-RG-3201','material':'Al 7075-T6','stock':'Ø190x85 mm round','stock_mass_kg':6.47,'material_cost_gbp':112.0},
{'part_id':'AST-SK-4301','material':'Al 2024-T3','stock':'240x70x10 mm plate','stock_mass_kg':0.47,'material_cost_gbp':18.0},
{'part_id':'AST-ST-1401','material':'Al 6061-T6','stock':'280x230x15 mm plate','stock_mass_kg':2.61,'material_cost_gbp':35.0},
]
part_times={}
for o in operations: part_times[o['part_id']]=part_times.get(o['part_id'],0)+float(o['estimated_min'])
economics=[]
for m in material_rows:
    t=part_times[m['part_id']]
    machine=t/60*hourly_rate_gbp
    tooling=0.18*machine
    inspection_cost=0.25*machine
    total=m['material_cost_gbp']+machine+tooling+inspection_cost
    economics.append({**m,'estimated_machine_time_min':round(t,1),'screening_machine_cost_gbp':round(machine,2),'screening_tooling_cost_gbp':round(tooling,2),'screening_inspection_cost_gbp':round(inspection_cost,2),'screening_total_gbp':round(total,2),'disclaimer':'portfolio estimate only; not a quotation'})
write_csv('calculations/v0_7/manufacturing_time_cost_screening.csv',economics)

# Inspection blank records
for pid in ['AST-TP-2101','AST-RG-3201','AST-SK-4301','AST-ST-1401']:
    chars=[r for r in inspection if r['part_id']==pid]
    rows=[]
    for r in chars:
        rows.append({'characteristic_id':r['characteristic_id'],'feature':r['feature'],'requirement':r['requirement'],'measured_value':'','unit':'mm unless noted','result':'OPEN','instrument_id':'','inspector':'','date':''})
    write_csv(f'cam/nx_cam/v0_7/inspection_records/inspection_report_{pid}.csv',rows)

# Setup sheets and docs
part_info={
'AST-TP-2101':('Thruster-gimbal bracket','Aluminium 6061-T6','3-axis mill, two setups','160 × 120 × 113 mm'),
'AST-RG-3201':('Ring-bearing housing','Aluminium 7075-T6','CNC lathe + 3-axis mill','Ø180 × 75 mm'),
'AST-SK-4301':('Skimmer wing rib','Aluminium 2024-T3','3-axis profile milling','220 × 30 × 28 mm'),
'AST-ST-1401':('Lightweight bulkhead','Aluminium 6061-T6','3-axis high-speed milling','260 × 210 × 12 mm'),
}
for pid,(name,mat,machine,envelope) in part_info.items():
    ops=[o for o in operations if o['part_id']==pid]
    op_table='\n'.join(f"| {o['setup']} | {o['operation_no']} | {o['operation']} | {o['tool_id']} | {o['estimated_min']} |" for o in ops)
    write_text(f'cam/nx_cam/v0_7/setup_sheets/{pid}_setup_sheet.md',f'''
# {pid} — {name} setup sheet

**Material:** {mat}  
**Manufacturing route:** {machine}  
**Finished envelope:** {envelope}  
**Release:** ASTERION FCTA-1 Version 0.7

## Operation sequence

| Setup | Op. | Operation | Tool | Estimated minutes |
|---|---:|---|---|---:|
{op_table}

## NX CAM evidence to capture

1. Workpiece and MCS definition.
2. Tool and holder assembly.
3. In-process workpiece after each operation.
4. Toolpath verification with material removal.
5. Holder, fixture and rapid-move collision review.
6. Remaining-stock comparison.
7. Posted-code review against the approved machine configuration.

## Prove-out controls

- Verify stock dimensions and work offset physically.
- Run machine simulation with the actual machine tool and postprocessor.
- Use single block, feed override and dry-run above stock for first execution.
- Do not treat the included educational G-code as production-ready code.
''')

write_text('cam/nx_cam/v0_7/NX_CAM_V0_7_Workflow.md','''
# Siemens NX CAM Version 0.7 workflow

## Purpose

This workflow demonstrates manufacturing planning and NX CAM competence using four representative ASTERION components. It does not claim that the full spacecraft can be manufactured on a home machine.

## Recommended NX structure

1. Create one manufacturing part file per demonstrator.
2. Add the design part as a reference component.
3. Create stock, MCS, clearance planes and fixtures.
4. Load only reviewed tools from `tool_library.csv`.
5. Build operations from `operation_plan.csv`.
6. Use IPW between setups and preserve stock allowance for finish operations.
7. Run full machine-tool simulation when a valid kinematic model and post are available.
8. Record collisions, warnings, cycle time and remaining stock.
9. Export setup sheets, tool lists, operation navigator screenshots and verified posted code.

## NX competencies demonstrated

- Manufacturing setup and geometry groups
- Workpiece/IPW management
- Planar milling and adaptive roughing
- Hole making and precision reaming
- Turning, boring and grooving
- Rest machining
- Thin-wall and profile finishing
- Tool-holder collision checking
- Fixture-aware simulation
- Post Builder/postprocessor governance
- Shop documentation and inspection planning

## Required portfolio screenshots

Capture the Operation Navigator, toolpath, material-removal verification, collision report, IPW comparison and final setup sheet for every demonstrator.
''')

write_text('cam/nx_cam/v0_7/postprocessor_safety.md','''
# Postprocessor and machine-safety requirements

The `.nc` examples in this repository are simulation-only teaching artefacts. They are not validated for any physical machine.

Before a real cut:

1. Select the exact controller and machine kinematic model.
2. Validate units, axis directions, work offsets, rotary conventions and tool-change position.
3. Confirm tool and holder gauge lengths.
4. Simulate stock, fixtures, spindle, table and enclosure.
5. Review every rapid move and retract plane.
6. Perform a supervised dry run above stock with reduced rapid/feed override.
7. Use single-block mode for the first prove-out.
8. Obtain approval from the responsible machine operator.

Never use generic posted code merely because it backplots correctly in a text viewer.
''')

write_text('prototype/v0_7/printing_guide.md','''
# Version 0.7 prototype printing guide

## Models

- `asterion_full_vehicle_1_to_50.stl` — visual portfolio model.
- `ring_drive_demonstrator_1_to_5.stl` — ring/spoke mechanism demonstrator.
- `docking_latch_demonstrator_1_to_5.stl` — simplified latch geometry.

## Suggested FDM settings

- Layer height: 0.20 mm for the vehicle, 0.16 mm for mechanisms.
- Walls: 3 perimeters.
- Infill: 15–25% for visual parts; 35% for mechanism handling.
- Material: PLA for display; PETG for repeated handling.
- Supports: generated only where required after slicer preview.
- Dimensional coupon: print a 20 mm cube and a hole gauge before mechanism parts.

These models are demonstrators, not flight hardware, pressure parts or load-rated components.
''')

# Main report
cost_total=sum(r['screening_total_gbp'] for r in economics)
write_text('calculations/v0_7/V0_7_manufacturing_screening_report.md',f'''
# ASTERION FCTA-1 Version 0.7 manufacturing screening report

## Scope

Version 0.7 translates the spacecraft design into a credible manufacturing portfolio using four representative components. Native NX CAM toolpaths must be generated and verified on the user's Siemens NX installation.

## Demonstrator summary

| Part | Route | Estimated machine time | Screening total |
|---|---|---:|---:|
| AST-TP-2101 gimbal bracket | 3-axis milling | {part_times['AST-TP-2101']:.1f} min | £{economics[0]['screening_total_gbp']:.2f} |
| AST-RG-3201 bearing housing | turning + milling | {part_times['AST-RG-3201']:.1f} min | £{economics[1]['screening_total_gbp']:.2f} |
| AST-SK-4301 wing rib | profile milling | {part_times['AST-SK-4301']:.1f} min | £{economics[2]['screening_total_gbp']:.2f} |
| AST-ST-1401 bulkhead | high-speed milling | {part_times['AST-ST-1401']:.1f} min | £{economics[3]['screening_total_gbp']:.2f} |

Combined screening total: **£{cost_total:.2f}**. This is a portfolio planning estimate, not a supplier quotation.

## Key manufacturing risks

- Thin structural members may distort after unclamping.
- Bearing geometry is sensitive to jaw force and setup concentricity.
- Gimbal-bores require controlled finishing and metrology.
- Generic postprocessed code cannot be trusted on a physical machine.
- The mass and cost of flight-grade aerospace manufacturing are not represented by desktop demonstrators.

## Acceptance evidence

Each part should eventually include NX CAM screenshots, an operation report, collision-free machine simulation, setup sheet, tool list, posted-code review, in-process inspection and final inspection record.
''')

# Gcode validator script
validator_code=r'''
from __future__ import annotations
import json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
GC=ROOT/'cam/nx_cam/v0_7/educational_gcode'
results=[]
for p in sorted(GC.glob('*.nc')):
    text=p.read_text(errors='ignore').upper().splitlines()
    issues=[]; z=999.0; safe=5.0; has_m30=False
    for n,line in enumerate(text,1):
        if 'M30' in line: has_m30=True
        rapid=('G0 ' in line or line.strip().startswith('G0'))
        mz=re.search(r'Z(-?\d+(?:\.\d+)?)',line)
        if mz: z=float(mz.group(1))
        if rapid and z < safe:
            issues.append(f'line {n}: rapid move below {safe} mm clearance')
        ms=re.search(r'S(\d+)',line)
        if ms and int(ms.group(1))>20000:
            issues.append(f'line {n}: spindle speed above 20000 rpm')
        mf=re.search(r'F(\d+(?:\.\d+)?)',line)
        if mf and float(mf.group(1))>5000:
            issues.append(f'line {n}: feed above 5000 mm/min')
        if any(code in line for code in ['G53','G28','M98','M99']):
            issues.append(f'line {n}: machine-coordinate or subprogram code requires manual review')
    if not has_m30: issues.append('missing M30')
    results.append({'file':p.name,'status':'PASS' if not issues else 'REVIEW','issues':issues})
print(json.dumps(results,indent=2))
if any(r['status']!='PASS' for r in results): raise SystemExit(2)
'''
write_text('scripts/python/v0_7/validate_educational_gcode.py',validator_code)

# Package validator
pkg_validator=r'''
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
'''
write_text('scripts/python/v0_7/validate_v0_7_package.py',pkg_validator)

# Reproducible geometry generation notes/script copy
write_text('scripts/python/v0_7/README.md','''
# Version 0.7 scripts

- `validate_educational_gcode.py` performs conservative text-level checks on the teaching G-code.
- `validate_v0_7_package.py` validates required files, mesh quality, operation count and Python syntax.
- The complete release was generated by `build_asterion_v0_7.py`, retained at repository root for reproducibility.
''')
shutil.copy2('/mnt/data/build_asterion_v0_7.py', DST/'build_asterion_v0_7.py')

# Update web viewer with manufacturing GLB
models=DST/'web-viewer/models'; models.mkdir(parents=True,exist_ok=True)
for p in (DST/'cad/manufacturing_parts/v0_7/neutral').glob('*.glb'):
    shutil.copy2(p, models/p.name)
write_text('web-viewer/v0_7_manufacturing_models.json',json.dumps({'release':'0.7.0','models':[p.name for p in sorted(models.glob('AST-*.glb'))]},indent=2))

# Release docs
write_text('docs/v0_7/version_0_7_release_notes.md','''
# Version 0.7 release notes

Version 0.7 adds a reproducible NX CAM and manufacturing portfolio built around four representative ASTERION components. It includes neutral geometry, controlled drawings, operation plans, fixtures, tooling data, inspection plans, safe teaching code, prototype models and validation scripts.

Native Siemens NX CAM files and machine-validated posts are not represented as completed. They must be generated and verified using the user's licensed NX installation and actual target machine configuration.
''')
write_text('docs/v0_7/manufacturing_verification_checklist.md','''
# Manufacturing verification checklist

- [ ] Design revision matches the released drawing.
- [ ] Material and stock certificate recorded.
- [ ] MCS and work offset independently checked.
- [ ] Tool and holder assemblies match the physical setup.
- [ ] Fixture and clamp envelopes included in simulation.
- [ ] All rapid moves remain clear of stock and fixtures.
- [ ] IPW is transferred correctly between setups.
- [ ] Finish stock is intentional and documented.
- [ ] Posted code matches the approved controller/post.
- [ ] Dry run and first-off inspection completed.
- [ ] Final inspection record attached.
- [ ] Deviations and concessions documented.
''')

# README/status
write_text('PROJECT_STATUS.md','''
# Project status

**Current release:** 0.7.0 — NX CAM and manufacturing portfolio

Completed through Version 0.7:

- Parametric master-envelope definition
- Primary spacecraft structure
- Full subsystem assembly
- Structural-analysis workflow
- Thermal and CFD workflow
- Four-component manufacturing and NX CAM portfolio
- Printable spacecraft and mechanism demonstrators

Open items for Version 0.8 include design optimisation, corrective structural redesign, sensitivity studies, updated mass properties and formal trade studies.
''')

write_text('README.md',f'''
# ASTERION FCTA-1

## Version 0.7 — NX CAM and manufacturing portfolio

ASTERION FCTA-1 is an open engineering portfolio for a modular, orbit-assembled deep-space spacecraft and detachable lifting-body aeroshuttle. The project demonstrates Siemens NX CAD/CAM and ANSYS-oriented engineering workflows while clearly separating present engineering practice from speculative future concepts.

## Version 0.7 deliverables

- Four neutral manufacturing demonstrator models in STL, OBJ and GLB
- Four SVG and DXF controlled drawing sets
- NX CAM operation plan and setup sheets
- Ten-tool manufacturing library
- Material-specific starting cutting data
- Fixture and workholding concepts
- Inspection plan and blank inspection records
- Simulation-only educational G-code with automated checks
- Toolpath previews and machine-time/cost screening
- 1:50 spacecraft and 1:5 mechanism printing models

## Demonstrator parts

| Part | Manufacturing competency |
|---|---|
| AST-TP-2101 thruster-gimbal bracket | 3-axis adaptive milling, drilling, reaming and fixture planning |
| AST-RG-3201 ring-bearing housing | Turning, boring, grooving and indexed milling |
| AST-SK-4301 Skimmer wing rib | Thin-part profile machining and aerodynamic contour control |
| AST-ST-1401 lightweight bulkhead | High-speed pocketing, thin-wall sequencing and distortion control |

## Screening economics

The four-part combined portfolio estimate is **£{cost_total:.2f}**, excluding programming labour, machine setup uncertainty, taxes, shipping, certification and aerospace quality-system overhead. It is not a quotation.

## Critical safety statement

The included G-code is for learning and backplotting only. No code is approved for a physical machine. Use the exact machine model, verified NX postprocessor, fixture model, tool data, work offsets, dry-run procedure and operator approval before any real machining.

## Repository progression

- 0.1 project definition
- 0.2 NX master skeleton
- 0.3 primary structure
- 0.4 full subsystem assembly
- 0.5 structural analysis
- 0.6 thermal and CFD analysis
- **0.7 CAM and manufacturing**
- 0.8 optimisation and redesign
- 0.9 validation, animation and web presentation
- 1.0 public portfolio release

Native proprietary NX part/manufacturing files and solved ANSYS databases are not falsely represented as generated in this environment.
''')

# Run validators
os.system(f"python '{DST/'scripts/python/v0_7/validate_educational_gcode.py'}' > '{DST/'calculations/v0_7/gcode_validation_output.json'}'")
rc=os.system(f"python '{DST/'scripts/python/v0_7/validate_v0_7_package.py'}' > '{DST/'calculations/v0_7/package_validation_output.txt'}'")
if rc!=0:
    print((DST/'calculations/v0_7/package_validation_output.txt').read_text())
    raise SystemExit('package validation failed')

# Release manifest and hashes (exclude SHA itself)
manifest=[]
for p in sorted(DST.rglob('*')):
    if p.is_file() and p.name!='SHA256SUMS.txt':
        manifest.append({'path':str(p.relative_to(DST)).replace('\\','/'),'size_bytes':p.stat().st_size,'sha256':sha256(p)})
write_text('docs/v0_7/release_manifest.json',json.dumps({'release':'0.7.0','file_count':len(manifest),'files':manifest},indent=2))
# regenerate manifest including itself except hash list
hash_lines=[]
for p in sorted(DST.rglob('*')):
    if p.is_file() and p.name!='SHA256SUMS.txt':
        hash_lines.append(f"{sha256(p)}  {p.relative_to(DST).as_posix()}")
write_text('SHA256SUMS.txt','\n'.join(hash_lines)+'\n')

# Zip
if ZIP_PATH.exists(): ZIP_PATH.unlink()
with zipfile.ZipFile(ZIP_PATH,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(DST.rglob('*')):
        if p.is_file(): z.write(p,p.relative_to(DST.parent))

# integrity check
with zipfile.ZipFile(ZIP_PATH) as z:
    bad=z.testzip()
    if bad: raise RuntimeError(f'bad zip member {bad}')

print(json.dumps({
'release':'0.7.0','zip':str(ZIP_PATH),'zip_size':ZIP_PATH.stat().st_size,'zip_sha256':sha256(ZIP_PATH),
'file_count':sum(1 for p in DST.rglob('*') if p.is_file()),
'part_meshes':4,'operations':len(operations),'tools':len(tools),'cost_total_gbp':round(cost_total,2)
},indent=2))
