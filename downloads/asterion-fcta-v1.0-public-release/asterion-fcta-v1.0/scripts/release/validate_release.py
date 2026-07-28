from __future__ import annotations
import csv, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
required = [
    'VERSION','README.md','RELEASE_NOTES.md','CITATION.cff','LICENSE',
    'docs/v1_0/portfolio/PORTFOLIO_SUMMARY.md',
    'docs/v1_0/governance/CLAIMS_AND_LIMITATIONS.md',
    'docs/v1_0/evidence/NATIVE_EXECUTION_EVIDENCE_CHECKLIST.md',
    'verification/v1_0/ARTIFACT_STATUS.csv',
    'web-viewer/v1_0/index.html','web-viewer/v1_0/css/style.css','web-viewer/v1_0/js/app.js',
    'web-viewer/v1_0/assets/asterion_full_assembly.glb',
    'web-viewer/v1_0/assets/asterion_optimized_structure.glb',
]
errors=[]
for rel in required:
    p=ROOT/rel
    if not p.is_file() or p.stat().st_size==0: errors.append(f'missing or empty: {rel}')
if (ROOT/'VERSION').read_text().strip()!='1.0.0': errors.append('VERSION must be 1.0.0')
with (ROOT/'verification/v1_0/ARTIFACT_STATUS.csv').open(newline='',encoding='utf-8') as f:
    rows=list(csv.DictReader(f))
if len(rows)<10: errors.append('artefact ledger has fewer than 10 records')
statuses={r['status'] for r in rows}
for expected in {'Generated and validated','Independent screening','Owner execution required'}:
    if expected not in statuses: errors.append(f'missing artefact status: {expected}')
for rel in ['web-viewer/v1_0/assets/asterion_full_assembly.glb','web-viewer/v1_0/assets/asterion_optimized_structure.glb']:
    if (ROOT/rel).stat().st_size<100_000: errors.append(f'GLB unexpectedly small: {rel}')
report={'version':'1.0.0','required_files_checked':len(required),'artefact_records':len(rows),'status':'FAIL' if errors else 'PASS','errors':errors}
out=ROOT/'verification/v1_0/release_validation_report.json'
out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
sys.exit(1 if errors else 0)
