#!/usr/bin/env python3
"""Recompute ASTERION V0.4 mass and centre of gravity from the CSV ledger."""
from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[2]
path=ROOT/'calculations/v0_4/component_mass_properties.csv'
with path.open(encoding='utf-8') as f:
    rows=list(csv.DictReader(f))
total=sum(float(r['mass_kg']) for r in rows)
cg=[]
for axis in ('x_m','y_m','z_m'):
    cg.append(sum(float(r['mass_kg'])*float(r[axis]) for r in rows)/total)
print(f"items={len(rows)}")
print(f"dry_mass_kg={total:.3f}")
print(f"cg_m=({cg[0]:.6f}, {cg[1]:.6f}, {cg[2]:.6f})")
