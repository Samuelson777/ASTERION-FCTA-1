#!/usr/bin/env python3
"""Generate the neutral ASTERION V0.6 analysis preparation geometry.
Requires numpy and trimesh. STL output uses millimetres.
"""
from pathlib import Path
import math
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'cad'/'analysis_models'/'v0_6'/'neutral'
OUT.mkdir(parents=True,exist_ok=True)
trimesh.creation.box(extents=[6000,2000,40]).export(OUT/'radiator_panel_6m_x_2m.stl')
trimesh.creation.box(extents=[800,500,20]).export(OUT/'electronics_cold_plate.stl')
print(f"Wrote geometry to {OUT}")
