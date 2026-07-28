from pathlib import Path
import csv, sys
root = Path(__file__).resolve().parents[3]
req = root / 'verification/v0_9/requirements_verification_matrix.csv'
rows = list(csv.DictReader(req.open(encoding='utf-8')))
assert len(rows) >= 20, f'Expected at least 20 requirements, found {len(rows)}'
closed = sum(1 for r in rows if r['status'].lower().startswith('closed'))
assert closed == len(rows), f'Not all requirements closed in v0.9 package: {closed}/{len(rows)}'
expected = [
 'docs/v0_9/final_report/ASTERION_FCTA_1_Final_Engineering_Report_v0_9.md',
 'prototype/v0_9/test_plan/physical_prototype_test_plan.md',
 'media/presentation/v0_9/demo_video_storyboard.md',
 'web-viewer/v0_9/index.html'
]
for item in expected:
    assert (root/item).exists(), f'Missing {item}'
print('ASTERION v0.9 package validation PASS')
print(f'Requirements closed: {closed}/{len(rows)}')
