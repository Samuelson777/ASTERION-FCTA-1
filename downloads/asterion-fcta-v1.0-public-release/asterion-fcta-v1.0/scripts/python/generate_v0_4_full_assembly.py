#!/usr/bin/env python3
"""Regenerate ASTERION FCTA-1 V0.4 neutral full-assembly geometry.

Requires Python, NumPy and trimesh. The V0.3 primary-structure STL must already
exist in this repository. Outputs are reference geometry, not native NX parts.
"""
from __future__ import annotations
import math
import shutil
from pathlib import Path
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[2]
CAD = ROOT / "cad" / "full_assembly" / "v0_4"
NEUTRAL = CAD / "neutral"
SUBSYS = NEUTRAL / "subsystems"
DRAW = CAD / "drawings"
NXOPEN = CAD / "nxopen"
ANSYS = ROOT / "analysis" / "ansys" / "v0_4"
MODEL = ANSYS / "model"
APDL = ANSYS / "apdl"
CALC = ROOT / "calculations" / "v0_4"
DOCS = ROOT / "docs" / "v0_4"
MEDIA = ROOT / "media" / "renders"
WEBMODELS = ROOT / "web-viewer" / "models"
for p in [NEUTRAL, SUBSYS, DRAW, NXOPEN, MODEL, APDL, CALC, DOCS, MEDIA, WEBMODELS]:
    p.mkdir(parents=True, exist_ok=True)

# ---------- geometry helpers ----------
COLORS = {
    'structure': [135, 145, 160, 255],
    'habitat': [230, 230, 225, 255],
    'modules': [190, 205, 220, 255],
    'solar': [35, 75, 145, 255],
    'radiator': [175, 195, 210, 255],
    'propulsion': [85, 90, 100, 255],
    'tanks': [210, 165, 90, 255],
    'dock': [160, 170, 180, 255],
    'robotic': [205, 145, 70, 255],
    'skimmer': [225, 225, 230, 255],
    'avionics': [110, 150, 120, 255],
}

def colour(mesh: trimesh.Trimesh, rgba):
    mesh.visual.face_colors = np.tile(np.array(rgba, dtype=np.uint8), (len(mesh.faces), 1))
    return mesh

def transform_mesh(mesh, matrix):
    mesh.apply_transform(matrix)
    return mesh

def translation(x, y, z):
    T = np.eye(4)
    T[:3, 3] = [x, y, z]
    return T

def rx(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1,0,0,0],[0,c,-s,0],[0,s,c,0],[0,0,0,1]], dtype=float)

def ry(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c,0,s,0],[0,1,0,0],[-s,0,c,0],[0,0,0,1]], dtype=float)

def rz(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c,-s,0,0],[s,c,0,0],[0,0,1,0],[0,0,0,1]], dtype=float)

def box(extents, center=(0,0,0), R=None, rgba=None):
    m = trimesh.creation.box(extents=extents)
    M = translation(*center)
    if R is not None:
        M = M @ R
    m.apply_transform(M)
    return colour(m, rgba or COLORS['modules'])

def cylinder_x(radius, length, center, rgba=None, sections=32):
    m = trimesh.creation.cylinder(radius=radius, height=length, sections=sections)
    m.apply_transform(translation(*center) @ ry(math.pi/2))
    return colour(m, rgba or COLORS['modules'])

def cone_x(r1, r2, length, center, rgba=None, sections=32):
    # Frustum built along local Z, then rotated to X.
    angles = np.linspace(0.0, 2.0*math.pi, sections, endpoint=False)
    verts = []
    for z, r in [(-length/2.0, r1), (length/2.0, r2)]:
        verts.extend([[r*math.cos(a), r*math.sin(a), z] for a in angles])
    verts.extend([[0.0,0.0,-length/2.0],[0.0,0.0,length/2.0]])
    faces=[]
    for i in range(sections):
        j=(i+1)%sections
        faces.extend([[i,j,sections+j],[i,sections+j,sections+i]])
        faces.append([2*sections,i,j])
        faces.append([2*sections+1,sections+j,sections+i])
    m=trimesh.Trimesh(vertices=np.asarray(verts), faces=np.asarray(faces), process=True)
    m.apply_transform(translation(*center) @ ry(math.pi/2))
    return colour(m, rgba or COLORS['propulsion'])

def sphere(radius, center, rgba=None, subdivisions=2):
    m = trimesh.creation.icosphere(subdivisions=subdivisions, radius=radius)
    m.apply_translation(center)
    return colour(m, rgba or COLORS['tanks'])

def cylinder_between(p0, p1, radius, rgba=None, sections=20):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    vec = p1-p0
    length = np.linalg.norm(vec)
    m = trimesh.creation.cylinder(radius=radius, height=length, sections=sections)
    direction = vec/length
    T = trimesh.geometry.align_vectors([0,0,1], direction)
    T[:3,3] = (p0+p1)/2
    m.apply_transform(T)
    return colour(m, rgba or COLORS['robotic'])

scene = trimesh.Scene()
groups: dict[str, list[trimesh.Trimesh]] = {k: [] for k in COLORS}

def add(mesh, group, name):
    groups[group].append(mesh)
    scene.add_geometry(mesh, node_name=name, geom_name=name)

# Existing primary structure
structure_path = ROOT / 'cad' / 'primary_structure' / 'v0_3' / 'neutral' / 'asterion_v0_3_primary_structure.stl'
structure = trimesh.load_mesh(structure_path, process=False)
colour(structure, COLORS['structure'])
add(structure, 'structure', 'AST-1000-PRIMARY-STRUCTURE')

# Habitation rings: 12 sector modules per ring + drive torus
ring_xs = (-2500.0, 2500.0)
ring_r = 12000.0
sector_tangent = 5100.0
for ir, x in enumerate(ring_xs, start=1):
    tor = trimesh.creation.torus(major_radius=11800.0, minor_radius=240.0, major_sections=72, minor_sections=16)
    tor.apply_transform(translation(x,0,0) @ ry(math.pi/2))
    add(colour(tor, COLORS['structure']), 'structure', f'AST-21{ir}0-RING-DRIVE')
    for j in range(12):
        th = 2*math.pi*j/12
        c = (x, ring_r*math.cos(th), ring_r*math.sin(th))
        # local X axial, local Z radial; local Y tangent
        m = box((3200.0, sector_tangent, 2100.0), c, rx(th-math.pi/2), COLORS['habitat'])
        add(m, 'habitat', f'AST-22{ir}{j+1:02d}-HAB-SECTOR')
        # external bumper panel
        c2 = (x, 13120.0*math.cos(th), 13120.0*math.sin(th))
        bumper = box((3000.0, sector_tangent*0.92, 90.0), c2, rx(th-math.pi/2), COLORS['modules'])
        add(bumper, 'habitat', f'AST-23{ir}{j+1:02d}-WHIPPLE-PANEL')

# Axial modules
module_specs = [
    ('AST-3100-SERVICE-MODULE', -10000.0, 5600.0, 2450.0, 'modules'),
    ('AST-3200-RADIATION-REFUGE', 7000.0, 4200.0, 2650.0, 'modules'),
    ('AST-3300-COMMAND-MODULE', 12000.0, 5000.0, 2300.0, 'modules'),
    ('AST-3400-LOGISTICS-MODULE', 17000.0, 3600.0, 2100.0, 'modules'),
    ('AST-3500-FORWARD-DOCK', 21400.0, 1600.0, 1100.0, 'dock'),
]
for name, x, L, r, grp in module_specs:
    add(cylinder_x(r, L, (x,0,0), COLORS[grp]), grp, name)

# End caps for selected pressure modules
for x, r in [(-12800,2450),(-7200,2450),(4900,2650),(9100,2650),(9500,2300),(14500,2300)]:
    add(sphere(r*0.98, (x,0,0), COLORS['modules'], subdivisions=2), 'modules', f'CAP-{x}')

# Propellant tanks and support saddles
for j in range(4):
    th = 2*math.pi*j/4 + math.pi/4
    y, z = 1750*math.cos(th), 1750*math.sin(th)
    add(cylinder_x(820, 4600, (-9000,y,z), COLORS['tanks']), 'tanks', f'AST-410{j+1}-PROPELLANT-TANK')
    add(sphere(820, (-11300,y,z), COLORS['tanks']), 'tanks', f'AST-411{j+1}-TANK-AFT-DOME')
    add(sphere(820, (-6700,y,z), COLORS['tanks']), 'tanks', f'AST-412{j+1}-TANK-FWD-DOME')

# Propulsion pods: 6 around aft truss
for j in range(6):
    th = 2*math.pi*j/6
    y, z = 4800*math.cos(th), 4800*math.sin(th)
    add(cylinder_x(720, 5600, (-17600,y,z), COLORS['propulsion']), 'propulsion', f'AST-510{j+1}-PROPULSION-POD')
    add(cone_x(950, 380, 1500, (-21150,y,z), COLORS['propulsion']), 'propulsion', f'AST-511{j+1}-THRUSTER-BELL')
    # two thruster apertures per pod
    for dz in (-260,260):
        add(cylinder_x(160, 450, (-22100,y,z+dz), COLORS['propulsion'], sections=20), 'propulsion', f'AST-512{j+1}-{dz}-THRUSTER')

# Solar wings: four radial segmented arrays
solar_segments = 4
seg_len = 6800.0
inner = 1700.0
for wing_idx, axis in enumerate(['+Y','-Y','+Z','-Z'], start=1):
    sign = 1 if axis[0]=='+' else -1
    for s in range(solar_segments):
        radial_c = inner + seg_len/2 + s*seg_len
        if axis[-1]=='Y':
            c=(3500.0, sign*radial_c, 0.0)
            ex=(11800.0, seg_len-180.0, 70.0)
        else:
            c=(3500.0, 0.0, sign*radial_c)
            ex=(11800.0, 70.0, seg_len-180.0)
        add(box(ex, c, None, COLORS['solar']), 'solar', f'AST-61{wing_idx}{s+1}-SOLAR-PANEL')
    # mast
    p0=(3500, 0,0)
    if axis[-1]=='Y': p1=(3500, sign*(inner+solar_segments*seg_len),0)
    else: p1=(3500,0,sign*(inner+solar_segments*seg_len))
    add(cylinder_between(p0,p1,90,COLORS['structure']), 'structure', f'AST-610{wing_idx}-SOLAR-MAST')

# Radiators: six around service/ring zone
for j in range(6):
    th=2*math.pi*j/6 + math.pi/6
    c=(-3500.0, 7900*math.cos(th), 7900*math.sin(th))
    add(box((6200.0, 3600.0, 80.0), c, rx(th-math.pi/2), COLORS['radiator']), 'radiator', f'AST-710{j+1}-RADIATOR')
    root=(-3500.0, 1500*math.cos(th), 1500*math.sin(th))
    add(cylinder_between(root,c,100,COLORS['structure']), 'structure', f'AST-711{j+1}-RADIATOR-BOOM')

# RCS pods around forward service area
for j in range(4):
    th=2*math.pi*j/4
    y,z=2600*math.cos(th),2600*math.sin(th)
    add(box((900,700,700),(8000,y,z),rx(th),COLORS['propulsion']), 'propulsion', f'AST-520{j+1}-RCS-POD')

# Avionics bay
add(box((2500,1800,1200),(5000,-900,-550),None,COLORS['avionics']), 'avionics','AST-3600-AVIONICS-BAY')

# Robotic servicing arm
arm_pts=[(15800,1800,1200),(17500,3300,2600),(19300,4200,3300),(20800,3300,2500)]
for idx,(a,b) in enumerate(zip(arm_pts[:-1],arm_pts[1:]),start=1):
    add(cylinder_between(a,b,180,COLORS['robotic']), 'robotic', f'AST-810{idx}-ROBOT-ARM')
for idx,p in enumerate(arm_pts,start=1):
    add(sphere(280,p,COLORS['robotic'],subdivisions=2), 'robotic', f'AST-811{idx}-ROBOT-JOINT')

# Skimmer convex-hull lifting body, docked forward
pts=np.array([
    [29400,0,0], [28200,1200,350],[28200,-1200,350],[28200,1000,-450],[28200,-1000,-450],
    [25000,2850,0],[25000,-2850,0],[25000,1400,1150],[25000,-1400,1150],[25000,1500,-850],[25000,-1500,-850],
    [21600,1650,500],[21600,-1650,500],[21600,1200,-650],[21600,-1200,-650]
],float)
skimmer=trimesh.convex.convex_hull(pts)
add(colour(skimmer,COLORS['skimmer']),'skimmer','AST-9000-SKIMMER-AEROSHUTTLE')
# elevons
add(box((2200,1700,110),(22800,2250,150),rz(-0.08),COLORS['skimmer']),'skimmer','AST-9011-SKIMMER-ELEVON-R')
add(box((2200,1700,110),(22800,-2250,150),rz(0.08),COLORS['skimmer']),'skimmer','AST-9012-SKIMMER-ELEVON-L')
# dorsal fins
add(box((1500,130,1200),(22500,800,900),None,COLORS['skimmer']),'skimmer','AST-9021-SKIMMER-FIN-R')
add(box((1500,130,1200),(22500,-800,900),None,COLORS['skimmer']),'skimmer','AST-9022-SKIMMER-FIN-L')

# Export GLB scene and combined neutral files
GLB = NEUTRAL / 'asterion_v0_4_full_assembly.glb'
GLB.write_bytes(scene.export(file_type='glb'))
all_meshes=[m for gl in groups.values() for m in gl]
combined=trimesh.util.concatenate(all_meshes)
combined.export(NEUTRAL/'asterion_v0_4_full_assembly.stl')
combined.export(NEUTRAL/'asterion_v0_4_full_assembly.obj')
for grp, meshes in groups.items():
    if meshes:
        trimesh.util.concatenate(meshes).export(SUBSYS/f'asterion_v0_4_{grp}.stl')
shutil.copy2(GLB, WEBMODELS/GLB.name)


print(f"Generated {GLB}")
print(f"Combined mesh: {len(combined.vertices)} vertices, {len(combined.faces)} faces")
