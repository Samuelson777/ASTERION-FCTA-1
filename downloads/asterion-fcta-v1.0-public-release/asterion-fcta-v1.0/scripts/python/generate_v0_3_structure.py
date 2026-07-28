#!/usr/bin/env python3
"""Generate ASTERION FCTA-1 Version 0.3 preliminary primary structure.

Outputs a neutral mesh, ANSYS line-model input tables, APDL includes,
engineering calculations, drawings, and validation metadata.
Units in CAD outputs and ANSYS line model are millimetres, newtons, seconds.
"""
from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[2]
CAD = ROOT / "cad" / "primary_structure" / "v0_3"
NEUTRAL = CAD / "neutral"
DRAW = CAD / "drawings"
ANSYS = ROOT / "analysis" / "ansys" / "v0_3"
MODEL = ANSYS / "model"
APDL = ANSYS / "apdl"
CALC = ROOT / "calculations" / "v0_3"
MEDIA = ROOT / "media" / "renders"
WEB = ROOT / "web-viewer" / "models"
for p in (NEUTRAL, DRAW, MODEL, APDL, CALC, MEDIA, WEB):
    p.mkdir(parents=True, exist_ok=True)

# ------------------------- baseline parameters -------------------------
SPINE_HALF = 21_000.0
TRUSS_R = 1_200.0
LONGERON_COUNT = 8
RING_X = (-2_500.0, 2_500.0)
RING_R = 12_000.0
RING_SECTORS = 12
PROP_X = -16_000.0
DOCK_X = 21_000.0
OMEGA_RPM = 4.3
OMEGA = OMEGA_RPM * 2.0 * math.pi / 60.0
RING_DESIGN_MASS_KG = 12_000.0
RHO_AL = 2_810.0  # kg/m^3
E_AL_MPA = 71_700.0
NU_AL = 0.33
YIELD_AL_MPA = 503.0  # conceptual 7075-T6 room-temperature value

# section IDs are used directly in APDL.
SECTIONS = {
    1: {"name": "LONGERON", "od_mm": 160.0, "t_mm": 6.0},
    2: {"name": "FRAME", "od_mm": 120.0, "t_mm": 5.0},
    3: {"name": "DIAGONAL", "od_mm": 90.0, "t_mm": 4.0},
    4: {"name": "RING_BEAM", "od_mm": 200.0, "t_mm": 6.0},
    5: {"name": "RING_SPOKE", "od_mm": 120.0, "t_mm": 5.0},
    6: {"name": "INTERFACE_BOOM", "od_mm": 140.0, "t_mm": 5.0},
    7: {"name": "DOCK_FRAME", "od_mm": 140.0, "t_mm": 5.0},
}

@dataclass
class Node:
    id: int
    x: float
    y: float
    z: float
    group: str

@dataclass
class Element:
    id: int
    n1: int
    n2: int
    section_id: int
    group: str

nodes: list[Node] = []
elements: list[Element] = []
node_lookup: dict[tuple[str, int, int], int] = {}

def add_node(x: float, y: float, z: float, group: str) -> int:
    nid = len(nodes) + 1
    nodes.append(Node(nid, float(x), float(y), float(z), group))
    return nid

def add_element(n1: int, n2: int, section_id: int, group: str) -> int:
    if n1 == n2:
        raise ValueError("Zero-length element")
    eid = len(elements) + 1
    elements.append(Element(eid, n1, n2, section_id, group))
    return eid

# Nominal 2.5 m bays, enriched with stable interface stations.
x_stations = set(float(x) for x in range(-21_000, 19_001, 2_500))
x_stations.update([-21_000.0, -16_000.0, -2_500.0, 2_500.0, 9_000.0, 15_000.0, 21_000.0])
x_list = sorted(x_stations)

# 8-longeron truss nodes.
truss_nodes: dict[tuple[int, int], int] = {}
for ix, x in enumerate(x_list):
    for j in range(LONGERON_COUNT):
        th = 2 * math.pi * j / LONGERON_COUNT
        nid = add_node(x, TRUSS_R * math.cos(th), TRUSS_R * math.sin(th), "SPINE")
        truss_nodes[(ix, j)] = nid

# Longeron, octagonal frame, and alternating diagonals.
for ix in range(len(x_list)):
    for j in range(LONGERON_COUNT):
        add_element(truss_nodes[(ix, j)], truss_nodes[(ix, (j + 1) % LONGERON_COUNT)], 2, "SPINE_FRAME")
    if ix < len(x_list) - 1:
        for j in range(LONGERON_COUNT):
            add_element(truss_nodes[(ix, j)], truss_nodes[(ix + 1, j)], 1, "SPINE_LONGERON")
            step = 1 if ix % 2 == 0 else -1
            add_element(truss_nodes[(ix, j)], truss_nodes[(ix + 1, (j + step) % LONGERON_COUNT)], 3, "SPINE_DIAGONAL")

# Ring support structures: 12 outer beam segments, 12 spokes, 12 connector links.
ring_outer_nodes: dict[tuple[int, int], int] = {}
for ir, x in enumerate(RING_X):
    # nearest exact station is included.
    ix = x_list.index(x)
    for j in range(RING_SECTORS):
        th = 2 * math.pi * j / RING_SECTORS
        nearest = int(round(j * LONGERON_COUNT / RING_SECTORS)) % LONGERON_COUNT
        truss_nid = truss_nodes[(ix, nearest)]
        truss_node = nodes[truss_nid - 1]
        iy = TRUSS_R * math.cos(th)
        iz = TRUSS_R * math.sin(th)
        # Reuse the truss node when the 12-sector hub angle coincides with an
        # 8-longeron node; otherwise create a hub node and a connector beam.
        if math.hypot(iy - truss_node.y, iz - truss_node.z) < 1e-6:
            inner = truss_nid
        else:
            inner = add_node(x, iy, iz, f"RING{ir+1}_INNER")
            add_element(inner, truss_nid, 6, f"RING{ir+1}_HUB_LINK")
        outer = add_node(x, RING_R * math.cos(th), RING_R * math.sin(th), f"RING{ir+1}_OUTER")
        ring_outer_nodes[(ir, j)] = outer
        add_element(inner, outer, 5, f"RING{ir+1}_SPOKE")
    for j in range(RING_SECTORS):
        add_element(ring_outer_nodes[(ir, j)], ring_outer_nodes[(ir, (j + 1) % RING_SECTORS)], 4, f"RING{ir+1}_CIRCUMFERENCE")

# Propulsion load-transfer booms: six radial attachment nodes.
prop_ix = x_list.index(PROP_X)
prop_mounts: list[int] = []
for j in range(6):
    th = 2 * math.pi * j / 6
    mount = add_node(PROP_X, 3_200.0 * math.cos(th), 3_200.0 * math.sin(th), "PROP_MOUNT")
    prop_mounts.append(mount)
    for offset in (0, 1):
        nearest = (int(round(j * LONGERON_COUNT / 6)) + offset) % LONGERON_COUNT
        add_element(truss_nodes[(prop_ix, nearest)], mount, 6, "PROP_BOOM")

# Forward docking frame: 8-node 800 mm radius ring linked to truss end.
dock_ix = x_list.index(DOCK_X)
dock_nodes: list[int] = []
for j in range(8):
    th = 2 * math.pi * j / 8
    dn = add_node(DOCK_X + 400.0, 800.0 * math.cos(th), 800.0 * math.sin(th), "DOCK_FRAME")
    dock_nodes.append(dn)
    add_element(truss_nodes[(dock_ix, j)], dn, 7, "DOCK_LINK")
for j in range(8):
    add_element(dock_nodes[j], dock_nodes[(j + 1) % 8], 7, "DOCK_RING")

node_map = {n.id: n for n in nodes}

def element_length_mm(e: Element) -> float:
    a, b = node_map[e.n1], node_map[e.n2]
    return math.dist((a.x, a.y, a.z), (b.x, b.y, b.z))

def tube_properties(od: float, t: float) -> dict[str, float]:
    inner = od - 2 * t
    area = math.pi / 4 * (od**2 - inner**2)
    inertia = math.pi / 64 * (od**4 - inner**4)
    polar = 2 * inertia
    rg = math.sqrt(inertia / area)
    return {"id_mm": inner, "area_mm2": area, "I_mm4": inertia, "J_mm4": polar, "rg_mm": rg}

section_summary: dict[int, dict[str, float | str]] = {}
for sid, sec in SECTIONS.items():
    props = tube_properties(sec["od_mm"], sec["t_mm"])
    length_mm = sum(element_length_mm(e) for e in elements if e.section_id == sid)
    volume_m3 = props["area_mm2"] * length_mm * 1e-9
    mass_kg = volume_m3 * RHO_AL
    section_summary[sid] = {**sec, **props, "length_mm": length_mm, "mass_kg": mass_kg}

primary_mass_kg = sum(float(v["mass_kg"]) for v in section_summary.values())

# ------------------------- write tabular inputs -------------------------
with (MODEL / "beam_nodes.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["node_id", "x_mm", "y_mm", "z_mm", "group"])
    for n in nodes:
        w.writerow([n.id, f"{n.x:.3f}", f"{n.y:.3f}", f"{n.z:.3f}", n.group])

with (MODEL / "beam_elements.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["element_id", "node_1", "node_2", "section_id", "group", "length_mm"])
    for e in elements:
        w.writerow([e.id, e.n1, e.n2, e.section_id, e.group, f"{element_length_mm(e):.3f}"])

with (MODEL / "beam_sections.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["section_id", "name", "outer_diameter_mm", "wall_mm", "inner_diameter_mm", "area_mm2", "I_mm4", "J_mm4", "radius_gyration_mm", "total_length_mm", "estimated_mass_kg"])
    for sid, s in section_summary.items():
        w.writerow([sid, s["name"], s["od_mm"], s["t_mm"], f"{s['id_mm']:.3f}", f"{s['area_mm2']:.3f}", f"{s['I_mm4']:.3f}", f"{s['J_mm4']:.3f}", f"{s['rg_mm']:.3f}", f"{s['length_mm']:.3f}", f"{s['mass_kg']:.3f}"])

with (MODEL / "material_properties.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["material_id", "designation", "elastic_modulus_MPa", "poisson_ratio", "density_kg_m3", "yield_strength_MPa", "status"])
    w.writerow([1, "Aluminium 7075-T6 conceptual baseline", E_AL_MPA, NU_AL, RHO_AL, YIELD_AL_MPA, "Preliminary; verify against selected supplier and temperature"])

# Centrifugal and braking calculations.
ring_accel = OMEGA**2 * RING_R / 1000.0
ring_total_radial_N = RING_DESIGN_MASS_KG * ring_accel
ring_nodal_radial_N = ring_total_radial_N / RING_SECTORS
ring_velocity = OMEGA * RING_R / 1000.0
ring_hoop_tension_N = RING_DESIGN_MASS_KG * ring_velocity**2 / (2 * math.pi * (RING_R / 1000.0))
ring_inertia = RING_DESIGN_MASS_KG * (RING_R / 1000.0) ** 2
brake_time_s = 120.0
brake_torque_Nm = ring_inertia * OMEGA / brake_time_s

load_cases = [
    ["LC-STR-01", "Docking compression", "25,000 N total -X at forward docking frame", "Aft frame constrained", "Static Structural"],
    ["LC-STR-02", "Emergency axial manoeuvre", "12,000 N total +X at propulsion mounts", "Forward docking frame constrained", "Static Structural"],
    ["LC-STR-03", "Twin-ring centrifugal", f"{ring_nodal_radial_N:.2f} N radial per outer node per ring", "Spine free except stabilising constraints", "Static Structural"],
    ["LC-STR-04", "Single-sector imbalance", "500 kg equivalent mass at one outer node", "Spine stabilised", "Static Structural"],
    ["LC-STR-05", "Ring emergency braking", f"{brake_torque_Nm:.2f} N m total torque per ring", "Spine stabilised", "Static Structural"],
    ["LC-MOD-01", "Free-free modal", "No applied force", "No supports; expect six rigid-body modes", "Modal"],
    ["LC-MOD-02", "Ground-test modal", "No applied force", "Aft frame constrained", "Modal"],
    ["LC-BUC-01", "Docking compression buckling", "25,000 N total -X", "Aft frame constrained", "Eigenvalue Buckling"],
]
with (MODEL / "load_cases.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["load_case_id", "title", "load_definition", "boundary_condition", "analysis_system"])
    w.writerows(load_cases)

# Named selections in a solver-neutral table.
with (MODEL / "named_selections.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["selection_name", "entity_type", "selection_rule", "purpose"])
    w.writerow(["NS_AFT_END", "nodes", "x = -21000 mm", "ground-test/fixed support"])
    w.writerow(["NS_FORWARD_DOCK", "nodes", "group = DOCK_FRAME", "docking load"])
    w.writerow(["NS_PROP_MOUNTS", "nodes", "group = PROP_MOUNT", "propulsion/manoeuvre load"])
    w.writerow(["NS_RING_1_OUTER", "nodes", "group = RING1_OUTER", "centrifugal load"])
    w.writerow(["NS_RING_2_OUTER", "nodes", "group = RING2_OUTER", "centrifugal load"])
    w.writerow(["NS_SPINE_LONGERONS", "elements", "group = SPINE_LONGERON", "stress and buckling review"])
    w.writerow(["NS_RING_SPOKES", "elements", "group contains _SPOKE", "ring support review"])

# ------------------------- APDL files -------------------------
apdl_lines = [
    "! ASTERION FCTA-1 v0.3 preliminary BEAM188 line model",
    "! Units: mm, N, s, MPa; density in tonne/mm^3",
    "/PREP7",
    "ET,1,BEAM188",
    f"MP,EX,1,{E_AL_MPA}",
    f"MP,PRXY,1,{NU_AL}",
    "MP,DENS,1,2.81E-9",
]
for sid, sec in SECTIONS.items():
    ri = (sec["od_mm"] - 2 * sec["t_mm"]) / 2
    ro = sec["od_mm"] / 2
    apdl_lines += [f"SECTYPE,{sid},BEAM,CTUBE,{sec['name']}", f"SECDATA,{ri:.6f},{ro:.6f},16"]
apdl_lines.append("! Nodes")
for n in nodes:
    apdl_lines.append(f"N,{n.id},{n.x:.6f},{n.y:.6f},{n.z:.6f}")
apdl_lines.append("! Elements")
for e in elements:
    apdl_lines += [f"SECNUM,{e.section_id}", f"E,{e.n1},{e.n2}"]
apdl_lines += ["ALLSEL,ALL", "FINISH"]
(APDL / "asterion_line_model.inc").write_text("\n".join(apdl_lines) + "\n", encoding="utf-8")

(APDL / "solve_static_docking.mac").write_text(f"""! ASTERION v0.3 static docking demonstrator
/CLEAR
/FILNAME,asterion_static_docking
/INPUT,asterion_line_model,inc
/SOLU
ANTYPE,STATIC
! Constrain aft end
NSEL,S,LOC,X,{-SPINE_HALF:.1f}
D,ALL,ALL,0
! Apply total 25 kN compression at forward docking frame
ALLSEL,ALL
NSEL,S,LOC,X,{DOCK_X+400.0:.1f}
*GET,NCOUNT,NODE,0,COUNT
F,ALL,FX,-25000/NCOUNT
ALLSEL,ALL
OUTRES,ALL,ALL
SOLVE
FINISH
/POST1
SET,LAST
PLDISP,2
PLNSOL,U,SUM
PLNSOL,S,EQV
FINISH
""", encoding="utf-8")

(APDL / "solve_modal_free_free.mac").write_text("""! ASTERION v0.3 free-free modal demonstrator
/CLEAR
/FILNAME,asterion_modal_freefree
/INPUT,asterion_line_model,inc
/SOLU
ANTYPE,MODAL
MODOPT,LANB,16
MXPAND,16,,,YES
OUTRES,ALL,ALL
SOLVE
FINISH
/POST1
SET,LIST
FINISH
""", encoding="utf-8")

(APDL / "solve_buckling_docking.mac").write_text(f"""! ASTERION v0.3 linear eigenvalue buckling demonstrator
/CLEAR
/FILNAME,asterion_buckling
/INPUT,asterion_line_model,inc
/SOLU
ANTYPE,STATIC
PSTRES,ON
NSEL,S,LOC,X,{-SPINE_HALF:.1f}
D,ALL,ALL,0
ALLSEL,ALL
NSEL,S,LOC,X,{DOCK_X+400.0:.1f}
*GET,NCOUNT,NODE,0,COUNT
F,ALL,FX,-25000/NCOUNT
ALLSEL,ALL
SOLVE
FINISH
/SOLU
ANTYPE,BUCKLE
BUCOPT,LANB,10
MXPAND,10
SOLVE
FINISH
/POST1
SET,LIST
FINISH
""", encoding="utf-8")

# ------------------------- neutral geometry -------------------------
def cylinder_between(a: np.ndarray, b: np.ndarray, radius: float, sections: int = 8) -> trimesh.Trimesh:
    vec = b - a
    length = float(np.linalg.norm(vec))
    mesh = trimesh.creation.cylinder(radius=radius, height=length, sections=sections)
    transform = trimesh.geometry.align_vectors([0, 0, 1], vec / length)
    mesh.apply_transform(transform)
    mesh.apply_translation((a + b) / 2)
    return mesh

meshes_by_group: dict[str, list[trimesh.Trimesh]] = {}
for e in elements:
    a = node_map[e.n1]
    b = node_map[e.n2]
    radius = SECTIONS[e.section_id]["od_mm"] / 2
    m = cylinder_between(np.array([a.x, a.y, a.z]), np.array([b.x, b.y, b.z]), radius)
    family = (
        "spine" if e.group.startswith("SPINE") else
        "ring_supports" if e.group.startswith("RING") else
        "propulsion_frame" if e.group.startswith("PROP") else
        "docking_frame"
    )
    meshes_by_group.setdefault(family, []).append(m)

combined_parts = []
scene = trimesh.Scene()
for family, mlist in meshes_by_group.items():
    part = trimesh.util.concatenate(mlist)
    part.export(NEUTRAL / f"asterion_v0_3_{family}.stl")
    scene.add_geometry(part, node_name=family, geom_name=family)
    combined_parts.append(part)
combined = trimesh.util.concatenate(combined_parts)
combined.export(NEUTRAL / "asterion_v0_3_primary_structure.stl")
combined.export(NEUTRAL / "asterion_v0_3_primary_structure.obj")
scene.export(NEUTRAL / "asterion_v0_3_primary_structure.glb")
scene.export(WEB / "asterion_v0_3_primary_structure.glb")

# ------------------------- engineering calculations -------------------------
# Conservative longest unsupported longeron length in the generated station list.
max_bay_mm = max(b - a for a, b in zip(x_list[:-1], x_list[1:]))
long_prop = section_summary[1]
I = float(long_prop["I_mm4"])
A = float(long_prop["area_mm2"])
euler_pinned_N = math.pi**2 * E_AL_MPA * I / max_bay_mm**2
euler_fixed_pinned_N = math.pi**2 * E_AL_MPA * I / (0.7 * max_bay_mm) ** 2
longeron_load_docking_N = 25_000.0 / LONGERON_COUNT
compressive_stress = longeron_load_docking_N / A
fos_yield = YIELD_AL_MPA / compressive_stress
buckling_fos_pinned = euler_pinned_N / longeron_load_docking_N

report = {
    "version": "0.3.0",
    "units": "mm-N-s for geometry/FEA; SI for human-readable dynamics",
    "node_count": len(nodes),
    "element_count": len(elements),
    "x_station_count": len(x_list),
    "primary_structure_estimated_mass_kg": primary_mass_kg,
    "ring_rotation_rpm": OMEGA_RPM,
    "ring_acceleration_m_s2": ring_accel,
    "ring_acceleration_g": ring_accel / 9.80665,
    "ring_design_mass_each_kg": RING_DESIGN_MASS_KG,
    "ring_total_radial_force_each_N": ring_total_radial_N,
    "ring_nodal_radial_force_N": ring_nodal_radial_N,
    "ring_uniform_hoop_tension_N": ring_hoop_tension_N,
    "ring_emergency_braking_torque_Nm": brake_torque_Nm,
    "maximum_spine_bay_mm": max_bay_mm,
    "longeron_docking_load_each_N": longeron_load_docking_N,
    "longeron_compressive_stress_MPa": compressive_stress,
    "longeron_yield_factor_of_safety": fos_yield,
    "longeron_euler_pinned_N": euler_pinned_N,
    "longeron_euler_fixed_pinned_N": euler_fixed_pinned_N,
    "longeron_buckling_fos_pinned": buckling_fos_pinned,
    "mesh_faces": int(len(combined.faces)),
    "mesh_vertices": int(len(combined.vertices)),
    "sections": section_summary,
}
(CALC / "v0_3_structural_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

md = f"""# ASTERION Version 0.3 Preliminary Structural Sizing

## Status

These calculations define a **portfolio-level preliminary structure**. They are not flight certification, pressure-vessel substantiation, fracture-control approval, or human-rating evidence.

## Baseline model

- Eight aluminium longerons around a 1.2 m truss radius.
- Nominal 2.5 m truss bays, with added stable interface stations.
- Octagonal transverse frames and alternating diagonal braces.
- Two 12-sector rotating-ring frames at X = -2.5 m and +2.5 m.
- Twelve spokes per ring, with local hub links to the central truss.
- Six propulsion load-transfer booms at X = -16 m.
- Dedicated forward docking frame at X = +21.4 m.

## Generated line model

| Metric | Value |
|---|---:|
| Nodes | {len(nodes)} |
| BEAM188 elements | {len(elements)} |
| Spine/interface stations | {len(x_list)} |
| Maximum bay length | {max_bay_mm/1000:.3f} m |
| Estimated idealised tube mass | {primary_mass_kg:,.1f} kg |

The mass excludes joints, fittings, bearing races, pressure shells, fasteners, harnesses, local reinforcement, coatings, mechanisms and manufacturing allowances. Apply a maturity allowance before using it in a system mass budget.

## Rotating-ring dynamics

For radius r = 12 m and rotation rate 4.3 rpm:

- Angular speed: {OMEGA:.5f} rad/s
- Tangential speed: {ring_velocity:.3f} m/s
- Centrifugal acceleration: {ring_accel:.3f} m/s² = {ring_accel/9.80665:.3f} g
- Design rotating mass per ring: {RING_DESIGN_MASS_KG:,.0f} kg
- Total distributed radial force per ring: {ring_total_radial_N:,.1f} N
- Equivalent radial force per outer node: {ring_nodal_radial_N:,.1f} N
- Uniform-ring hoop tension estimate: {ring_hoop_tension_N:,.1f} N
- 120 s emergency braking torque: {brake_torque_Nm:,.1f} N·m

The spoke analysis must also include local cabin-sector masses and imbalance; the uniform-ring equation alone is not sufficient for detailed design.

## Longeron screening calculation

Selected conceptual longeron: 160 mm outside diameter, 6 mm wall aluminium tube.

| Quantity | Value |
|---|---:|
| Area | {A:,.1f} mm² |
| Second moment of area | {I:,.3e} mm⁴ |
| Radius of gyration | {float(long_prop['rg_mm']):.2f} mm |
| Docking load per longeron | {longeron_load_docking_N:,.1f} N |
| Direct compressive stress | {compressive_stress:.3f} MPa |
| Yield screening factor | {fos_yield:.1f} |
| Euler pinned-pinned critical load | {euler_pinned_N/1000:,.1f} kN |
| Euler buckling screening factor | {buckling_fos_pinned:.1f} |

This simple screening ignores joint eccentricity, imperfections, local shell buckling, load redistribution and combined bending. ANSYS model correlation and local joint submodels are required before any design claim.

## Required Version 0.5 correlation

1. Compare beam-model axial displacement with a hand truss calculation.
2. Complete mesh/refinement studies for line, shell and local solid models.
3. Check free-free modes and identify the first six rigid-body modes.
4. Replace ideal rigid joints with realistic joint stiffness sensitivity cases.
5. Run linear buckling, then nonlinear imperfection sensitivity on critical members.
6. Perform local stress checks at ring hubs, propulsion booms and docking links.
"""
(CALC / "preliminary_structural_sizing.md").write_text(md, encoding="utf-8")

# ------------------------- drawings and previews -------------------------
try:
    import matplotlib.pyplot as plt

    def plot_view(path: Path, axes: tuple[int, int], title: str, limits: tuple[tuple[float,float], tuple[float,float]]):
        fig, ax = plt.subplots(figsize=(12, 7))
        coords = [(n.x, n.y, n.z) for n in nodes]
        for e in elements:
            a, b = node_map[e.n1], node_map[e.n2]
            va = (a.x, a.y, a.z); vb = (b.x, b.y, b.z)
            ax.plot([va[axes[0]]/1000, vb[axes[0]]/1000], [va[axes[1]]/1000, vb[axes[1]]/1000], linewidth=0.45)
        ax.set_aspect("equal", adjustable="box")
        labels = ["X (m)", "Y (m)", "Z (m)"]
        ax.set_xlabel(labels[axes[0]])
        ax.set_ylabel(labels[axes[1]])
        ax.set_title(title)
        ax.grid(True, linewidth=0.3)
        ax.set_xlim(*limits[0]); ax.set_ylim(*limits[1])
        fig.tight_layout()
        fig.savefig(path, dpi=180)
        plt.close(fig)

    plot_view(MEDIA / "v0_3_primary_structure_plan.png", (0,1), "ASTERION FCTA-1 v0.3 Primary Structure — Plan", ((-23,23),(-14,14)))
    plot_view(MEDIA / "v0_3_primary_structure_front.png", (1,2), "ASTERION FCTA-1 v0.3 Primary Structure — Front", ((-14,14),(-14,14)))
    plot_view(DRAW / "asterion_v0_3_structure_plan.svg", (0,1), "ASTERION v0.3 Structure Plan Reference", ((-23,23),(-14,14)))
    plot_view(DRAW / "asterion_v0_3_structure_front.svg", (1,2), "ASTERION v0.3 Structure Front Reference", ((-14,14),(-14,14)))
except Exception as exc:
    (CALC / "plot_warning.txt").write_text(str(exc), encoding="utf-8")

print(json.dumps({
    "nodes": len(nodes),
    "elements": len(elements),
    "estimated_primary_mass_kg": round(primary_mass_kg, 2),
    "ring_acceleration_g": round(ring_accel / 9.80665, 4),
    "mesh_faces": int(len(combined.faces)),
    "mesh_vertices": int(len(combined.vertices)),
}, indent=2))
