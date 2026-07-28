"""Regenerate the Version 0.2 neutral master-envelope meshes.

Requires Python 3.10+, numpy and trimesh. Run from the repository root.
The official release meshes were produced by the project packager; this script
is provided as a concise reproducibility reference.
"""
from pathlib import Path
import math
import numpy as np
import trimesh

OUT = Path("cad/nx_master_model/v0_2/neutral/regenerated")
OUT.mkdir(parents=True, exist_ok=True)


def cyl_x(radius, length, centre):
    m = trimesh.creation.cylinder(radius=radius, height=length, sections=32)
    m.apply_transform(trimesh.geometry.align_vectors([0,0,1],[1,0,0]))
    m.apply_translation(centre)
    return m

meshes = [cyl_x(900, 42000, [0,0,0])]
for x in (-2500, 2500):
    ring = trimesh.creation.torus(major_radius=12000, minor_radius=1000,
                                  major_sections=96, minor_sections=24)
    ring.apply_transform(trimesh.geometry.align_vectors([0,0,1],[1,0,0]))
    scale = np.eye(4); scale[0,0] = 1.6
    ring.apply_transform(scale); ring.apply_translation([x,0,0])
    meshes.append(ring)

joined = trimesh.util.concatenate(meshes)
joined.export(OUT / "asterion_core_envelope.stl")
print(f"Wrote {OUT / 'asterion_core_envelope.stl'}")
