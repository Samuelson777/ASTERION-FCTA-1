#!/usr/bin/env python3
"""Independent linear 3-D frame screening model for ASTERION FCTA-1 V0.8.

This is an engineering cross-check, not a substitute for an ANSYS Mechanical
model. It uses Euler-Bernoulli beam elements, ideal rigid joints, linear elastic
material, circular tubes, and simplified lumped masses.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Dict, Iterable, Tuple

import numpy as np
import pandas as pd
from scipy.linalg import eigh
from scipy.sparse import coo_matrix, csc_matrix
from scipy.sparse.linalg import spsolve

DOF_PER_NODE = 6
G0 = 9.80665


def _rotation_matrix(p1: np.ndarray, p2: np.ndarray) -> Tuple[np.ndarray, float]:
    delta = p2 - p1
    length = float(np.linalg.norm(delta))
    if length <= 1e-12:
        raise ValueError("Zero-length element")
    ex = delta / length
    reference = np.array([0.0, 0.0, 1.0])
    if abs(float(np.dot(ex, reference))) > 0.90:
        reference = np.array([0.0, 1.0, 0.0])
    ey = np.cross(reference, ex)
    ey /= np.linalg.norm(ey)
    ez = np.cross(ex, ey)
    rotation = np.vstack((ex, ey, ez))
    return rotation, length


def _local_stiffness(E: float, G: float, A: float, I: float, J: float, L: float) -> np.ndarray:
    k = np.zeros((12, 12), dtype=float)
    a = E * A / L
    t = G * J / L
    by = E * I
    bz = E * I

    k[0, 0] = k[6, 6] = a
    k[0, 6] = k[6, 0] = -a
    k[3, 3] = k[9, 9] = t
    k[3, 9] = k[9, 3] = -t

    # Bending in local x-y plane (v, rz), about local z.
    ids = [1, 5, 7, 11]
    block = bz * np.array([
        [12/L**3,  6/L**2, -12/L**3,  6/L**2],
        [ 6/L**2,  4/L,     -6/L**2,  2/L],
        [-12/L**3, -6/L**2, 12/L**3, -6/L**2],
        [ 6/L**2,  2/L,     -6/L**2,  4/L],
    ])
    k[np.ix_(ids, ids)] += block

    # Bending in local x-z plane (w, ry), about local y.
    ids = [2, 4, 8, 10]
    block = by * np.array([
        [12/L**3, -6/L**2, -12/L**3, -6/L**2],
        [-6/L**2,  4/L,      6/L**2,  2/L],
        [-12/L**3, 6/L**2,  12/L**3,  6/L**2],
        [-6/L**2,  2/L,      6/L**2,  4/L],
    ])
    k[np.ix_(ids, ids)] += block
    return k


def _transform(rotation: np.ndarray) -> np.ndarray:
    T = np.zeros((12, 12), dtype=float)
    for start in (0, 3, 6, 9):
        T[start:start+3, start:start+3] = rotation
    return T


def _node_dofs(index: int) -> np.ndarray:
    start = index * DOF_PER_NODE
    return np.arange(start, start + DOF_PER_NODE, dtype=int)


def load_model(root: Path):
    model_dir = root / "analysis/ansys/v0_8/model"
    nodes = pd.read_csv(model_dir / "optimized_beam_nodes.csv")
    elements = pd.read_csv(model_dir / "optimized_beam_elements.csv")
    sections = pd.read_csv(model_dir / "optimized_beam_sections.csv").set_index("section_id")
    material = pd.read_csv(model_dir / "material_properties.csv").iloc[0]
    remote = pd.read_csv(model_dir / "remote_mass_definitions.csv")
    return nodes, elements, sections, material, remote


def assemble(root: Path):
    nodes, elements, sections, material, remote = load_model(root)
    id_to_index = {int(nid): i for i, nid in enumerate(nodes.node_id)}
    coords = nodes[["x_mm", "y_mm", "z_mm"]].to_numpy(float) / 1000.0
    ndof = len(nodes) * DOF_PER_NODE
    rows, cols, values = [], [], []
    mass_diag = np.zeros(ndof, dtype=float)

    E = float(material.elastic_modulus_MPa) * 1e6
    nu = float(material.poisson_ratio)
    G = E / (2.0 * (1.0 + nu))
    rho = float(material.density_kg_m3)

    element_cache = []
    for row in elements.itertuples(index=False):
        i = id_to_index[int(row.node_1)]
        j = id_to_index[int(row.node_2)]
        p1, p2 = coords[i], coords[j]
        R, L = _rotation_matrix(p1, p2)
        section = sections.loc[int(row.section_id)]
        A = float(section.area_mm2) * 1e-6
        I = float(section.I_mm4) * 1e-12
        J = float(section.J_mm4) * 1e-12
        k_local = _local_stiffness(E, G, A, I, J, L)
        T = _transform(R)
        k_global = T.T @ k_local @ T
        dofs = np.concatenate((_node_dofs(i), _node_dofs(j)))
        rr, cc = np.meshgrid(dofs, dofs, indexing="ij")
        rows.extend(rr.ravel().tolist())
        cols.extend(cc.ravel().tolist())
        values.extend(k_global.ravel().tolist())

        beam_mass = rho * A * L
        for node_index in (i, j):
            d = _node_dofs(node_index)
            mass_diag[d[0:3]] += beam_mass / 2.0
            # Positive approximate rotary inertia for a robust screening modal model.
            mass_diag[d[3:6]] += beam_mass * L * L / 24.0
        element_cache.append((row, i, j, R, L, k_local, T, A, I, J))

    K = coo_matrix((values, (rows, cols)), shape=(ndof, ndof)).tocsc()

    # Place non-structural mass at the nearest structural node. ANSYS V0.5 uses
    # reviewed remote-point couplings instead; this is only a screening model.
    for row in remote.itertuples(index=False):
        xyz = np.array([float(row.x_mm), float(row.y_mm), float(row.z_mm)]) / 1000.0
        idx = int(np.argmin(np.linalg.norm(coords - xyz, axis=1)))
        m = float(row.mass_kg)
        d = _node_dofs(idx)
        mass_diag[d[0:3]] += m
        mass_diag[d[3:6]] += max(0.01, m * 0.25)

    mass_diag[mass_diag <= 0.0] = 1e-9
    return nodes, elements, sections, material, coords, id_to_index, K, mass_diag, element_cache


def constraints(nodes: pd.DataFrame, mode: str) -> np.ndarray:
    if mode == "aft_fixed":
        idx = np.where(np.isclose(nodes.x_mm.to_numpy(float), -21000.0))[0]
    elif mode == "stabilised":
        # Engineering-minimum stabilisation at three aft nodes. Do not use this
        # support set for final flight load-path claims.
        aft = nodes[np.isclose(nodes.x_mm, -21000.0)].sort_values("node_id")
        idx = aft.index.to_numpy()[:3]
    else:
        raise ValueError(f"Unknown constraint mode: {mode}")
    fixed = np.concatenate([_node_dofs(int(i)) for i in idx])
    return np.unique(fixed)


def build_load(nodes: pd.DataFrame, coords: np.ndarray, case: str) -> Tuple[np.ndarray, str]:
    F = np.zeros(len(nodes) * DOF_PER_NODE, dtype=float)
    group = nodes.group.astype(str)

    if case == "LC-STR-01":
        ids = np.where(group == "DOCK_FRAME")[0]
        for i in ids:
            F[_node_dofs(i)[0]] += -25000.0 / len(ids)
        support = "aft_fixed"
    elif case == "LC-STR-02":
        ids = np.where(group == "PROP_MOUNT")[0]
        for i in ids:
            F[_node_dofs(i)[0]] += 12000.0 / len(ids)
        support = "aft_fixed"
    elif case == "LC-STR-03":
        ids = np.where(group.isin(["RING1_OUTER", "RING2_OUTER"]))[0]
        for i in ids:
            radial = np.array([0.0, coords[i, 1], coords[i, 2]])
            radial /= np.linalg.norm(radial)
            F[_node_dofs(i)[0:3]] += 2433.19 * radial
        support = "aft_fixed"
    elif case == "LC-STR-04":
        ids = np.where(group == "RING1_OUTER")[0]
        target = ids[int(np.argmax(coords[ids, 1]))]
        radial = np.array([0.0, coords[target, 1], coords[target, 2]])
        radial /= np.linalg.norm(radial)
        F[_node_dofs(target)[0:3]] += 500.0 * 2.43319 * radial
        support = "aft_fixed"
    elif case == "LC-STR-05":
        for ring_group in ("RING1_OUTER", "RING2_OUTER"):
            ids = np.where(group == ring_group)[0]
            radius = np.mean(np.sqrt(coords[ids, 1]**2 + coords[ids, 2]**2))
            force_each = 6484.25 / (radius * len(ids))
            for i in ids:
                y, z = coords[i, 1], coords[i, 2]
                tangent = np.array([0.0, -z, y])
                tangent /= np.linalg.norm(tangent)
                F[_node_dofs(i)[0:3]] += force_each * tangent
        support = "aft_fixed"
    elif case == "LC-STR-06":
        # Combined powered-ring operation: propulsion + both ring centrifugal loads.
        ids = np.where(group == "PROP_MOUNT")[0]
        for i in ids:
            F[_node_dofs(i)[0]] += 12000.0 / len(ids)
        ids = np.where(group.isin(["RING1_OUTER", "RING2_OUTER"]))[0]
        for i in ids:
            radial = np.array([0.0, coords[i, 1], coords[i, 2]])
            radial /= np.linalg.norm(radial)
            F[_node_dofs(i)[0:3]] += 2433.19 * radial
        support = "aft_fixed"
    elif case == "LC-STR-07":
        ids = np.where(group == "DOCK_FRAME")[0]
        for i in ids:
            F[_node_dofs(i)[0]] += -25000.0 / len(ids)
            F[_node_dofs(i)[1]] += 2500.0 / len(ids)
        support = "aft_fixed"
    elif case == "LC-STR-08":
        # Balanced 120 s braking of counter-rotating rings. Opposite torques cancel globally.
        for ring_group, sign in (("RING1_OUTER", 1.0), ("RING2_OUTER", -1.0)):
            ids = np.where(group == ring_group)[0]
            radius = np.mean(np.sqrt(coords[ids, 1]**2 + coords[ids, 2]**2))
            force_each = 6484.25 / (radius * len(ids))
            for i in ids:
                y, z = coords[i, 1], coords[i, 2]
                tangent = np.array([0.0, -z, y])
                tangent /= np.linalg.norm(tangent)
                F[_node_dofs(i)[0:3]] += sign * force_each * tangent
        support = "aft_fixed"
    elif case == "LC-STR-09":
        # Single-ring braking fault with a controlled 180 s stop.
        ids = np.where(group == "RING1_OUTER")[0]
        radius = np.mean(np.sqrt(coords[ids, 1]**2 + coords[ids, 2]**2))
        force_each = 4322.83 / (radius * len(ids))
        for i in ids:
            y, z = coords[i, 1], coords[i, 2]
            tangent = np.array([0.0, -z, y])
            tangent /= np.linalg.norm(tangent)
            F[_node_dofs(i)[0:3]] += force_each * tangent
        support = "aft_fixed"
    else:
        raise ValueError(f"Unknown load case {case}")
    return F, support


def solve_static(K: csc_matrix, F: np.ndarray, fixed: np.ndarray) -> np.ndarray:
    all_dofs = np.arange(K.shape[0])
    free = np.setdiff1d(all_dofs, fixed)
    u = np.zeros(K.shape[0], dtype=float)
    u[free] = spsolve(K[free][:, free], F[free])
    return u


def element_results(u: np.ndarray, cache, material, sections) -> pd.DataFrame:
    E = float(material.elastic_modulus_MPa) * 1e6
    yield_pa = float(material.yield_strength_MPa) * 1e6
    rows = []
    for row, i, j, R, L, k_local, T, A, I, J in cache:
        dofs = np.concatenate((_node_dofs(i), _node_dofs(j)))
        u_local = T @ u[dofs]
        forces = k_local @ u_local
        c = float(sections.loc[int(row.section_id)].outer_diameter_mm) / 2000.0
        values = []
        for offset in (0, 6):
            axial = forces[offset + 0]
            torsion = forces[offset + 3]
            my = forces[offset + 4]
            mz = forces[offset + 5]
            sigma = abs(axial) / A + c * math.hypot(my, mz) / I
            tau = abs(torsion) * c / J
            vm = math.sqrt(sigma * sigma + 3.0 * tau * tau)
            values.append((axial, torsion, my, mz, vm))
        critical = max(values, key=lambda x: x[4])
        axial_min = min(values[0][0], values[1][0])
        pcr = math.pi**2 * E * I / (L**2)
        buckling_factor = pcr / abs(axial_min) if axial_min < -1e-6 else math.inf
        rows.append({
            "element_id": int(row.element_id),
            "group": str(row.group),
            "section_id": int(row.section_id),
            "length_m": L,
            "axial_force_N": critical[0],
            "torsion_Nm": critical[1],
            "bending_My_Nm": critical[2],
            "bending_Mz_Nm": critical[3],
            "screening_von_mises_MPa": critical[4] / 1e6,
            "yield_factor": yield_pa / critical[4] if critical[4] > 1e-9 else math.inf,
            "member_euler_factor": buckling_factor,
        })
    return pd.DataFrame(rows)


def modal_supported(K: csc_matrix, mass_diag: np.ndarray, fixed: np.ndarray, count: int = 12):
    all_dofs = np.arange(K.shape[0])
    free = np.setdiff1d(all_dofs, fixed)
    Kff = K[free][:, free].toarray()
    Mff = np.diag(mass_diag[free])
    # Dense subset eigensolution is stable for this small screening model.
    eigvals, eigvecs = eigh(Kff, Mff, subset_by_index=[0, min(count + 8, len(free)-1)])
    positive = eigvals[eigvals > 1e-5]
    frequencies = np.sqrt(positive) / (2.0 * math.pi)
    return frequencies[:count]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    root = args.root.resolve()
    output = (args.output or (root / "calculations/v0_8/python_screening")).resolve()
    output.mkdir(parents=True, exist_ok=True)

    nodes, elements, sections, material, coords, id_to_index, K, mass_diag, cache = assemble(root)
    summaries = []
    displacement_rows = []
    for case in ["LC-STR-01","LC-STR-02","LC-STR-03","LC-STR-04","LC-STR-06","LC-STR-07","LC-STR-08","LC-STR-09"]:
        F, support = build_load(nodes, coords, case)
        fixed = constraints(nodes, support)
        u = solve_static(K, F, fixed)
        nodal = u.reshape((-1, DOF_PER_NODE))
        trans = nodal[:, :3]
        mag = np.linalg.norm(trans, axis=1)
        critical_node = int(np.argmax(mag))
        eres = element_results(u, cache, material, sections)
        critical_element = eres.loc[eres.screening_von_mises_MPa.idxmax()]
        finite_buckling = eres[np.isfinite(eres.member_euler_factor)]
        min_buckling = float(finite_buckling.member_euler_factor.min()) if len(finite_buckling) else math.inf
        summaries.append({
            "load_case_id": case,
            "support_model": support,
            "result_source": "Independent Python Euler-Bernoulli frame screening",
            "max_translation_mm": float(mag[critical_node] * 1000.0),
            "critical_node_id": int(nodes.iloc[critical_node].node_id),
            "max_screening_von_mises_MPa": float(critical_element.screening_von_mises_MPa),
            "critical_element_id": int(critical_element.element_id),
            "minimum_yield_factor": float(critical_element.yield_factor),
            "minimum_member_euler_factor": min_buckling,
        })
        for i, node in nodes.iterrows():
            displacement_rows.append({
                "load_case_id": case,
                "node_id": int(node.node_id),
                "x_m": float(node.x_mm / 1000.0),
                "ux_mm": float(trans[i, 0] * 1000.0),
                "uy_mm": float(trans[i, 1] * 1000.0),
                "uz_mm": float(trans[i, 2] * 1000.0),
                "translation_mm": float(mag[i] * 1000.0),
            })
        eres.to_csv(output / f"{case.lower()}_element_screening.csv", index=False)

    modal_fixed = constraints(nodes, "aft_fixed")
    frequencies = modal_supported(K, mass_diag, modal_fixed, count=12)
    modal_df = pd.DataFrame({
        "mode": np.arange(1, len(frequencies) + 1),
        "frequency_Hz": frequencies,
        "source": "Independent Python frame screening; approximate lumped mass",
    })
    modal_df.to_csv(output / "supported_modal_screening.csv", index=False)

    summary_df = pd.DataFrame(summaries)
    summary_df.to_csv(output / "static_screening_summary.csv", index=False)
    pd.DataFrame(displacement_rows).to_csv(output / "nodal_displacements.csv", index=False)

    report = {
        "status": "screening_only",
        "solver": "custom linear 3-D Euler-Bernoulli frame",
        "nodes": int(len(nodes)),
        "elements": int(len(elements)),
        "structural_tube_mass_kg": float(sections.estimated_mass_kg.sum()),
        "approximate_total_lumped_mass_kg": float(mass_diag.reshape((-1, 6))[:, 0].sum()),
        "static_cases": summaries,
        "supported_modal_frequencies_Hz": [float(v) for v in frequencies],
        "limitations": [
            "Ideal rigid beam joints",
            "No shear deformation or warping",
            "Simplified nearest-node placement for subsystem mass",
            "Approximate positive rotary lumped mass",
            "No contact, geometric nonlinearity, joint flexibility or imperfections",
            "ANSYS Mechanical results are required for final portfolio claims",
        ],
    }
    (output / "screening_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
