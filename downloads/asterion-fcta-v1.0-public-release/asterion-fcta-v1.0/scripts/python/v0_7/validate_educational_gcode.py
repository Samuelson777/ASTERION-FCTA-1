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
