#!/usr/bin/env python3
"""Recompute ASTERION V0.6 reduced-order thermal and CFD screening data.

This script intentionally does not call ANSYS. It provides independent algebraic
checks for correlation with user-run Mechanical and Fluent models.
"""
from __future__ import annotations
import math
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "calculations" / "v0_6"
OUT.mkdir(parents=True, exist_ok=True)
SIGMA = 5.670374419e-8
EPS = 0.88
AREA = 144.0
Q = 120000.0
SOLAR = 0.15*1361.0*72.0*math.sin(math.radians(10.0))
T = ((Q+SOLAR)/(EPS*SIGMA*AREA))**0.25
print(f"Radiator equilibrium: {T:.3f} K")
V=45.0; G=0.040; CIN=420.0
for flow in (240.0,80.0):
    css=CIN+1e6*G/flow
    print(f"Cabin flow {flow:.0f} m3/h: {css:.1f} ppm steady CO2")
print("Use the complete repository data tables for the aerodynamic sweeps.")
