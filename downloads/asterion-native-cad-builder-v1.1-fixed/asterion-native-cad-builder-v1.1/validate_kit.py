from __future__ import annotations
import csv
import hashlib
import json
import py_compile
from pathlib import Path

root = Path(__file__).resolve().parent
errors = []
component_manifest = root / "config" / "nx_component_manifest.csv"
drawing_manifest = root / "config" / "drawing_manifest.csv"

with component_manifest.open(newline="", encoding="utf-8-sig") as f:
    components = list(csv.DictReader(f))
with drawing_manifest.open(newline="", encoding="utf-8-sig") as f:
    drawings = list(csv.DictReader(f))

for row in components:
    source = root / row["source_stl"]
    if not source.is_file():
        errors.append(f"Missing source: {source}")
    elif source.stat().st_size < 100:
        errors.append(f"Source is too small: {source}")

if len(components) != 16:
    errors.append(f"Expected 16 component rows, found {len(components)}")
if sum(r["include_in_top_assembly"] == "1" for r in components) != 11:
    errors.append("Expected 11 top-assembly components")
if len(drawings) != 8:
    errors.append(f"Expected 8 drawing rows, found {len(drawings)}")

try:
    py_compile.compile(str(root / "nxopen" / "asterion_nx_native_builder.py"), doraise=True)
except Exception as e:
    errors.append(f"NXOpen script syntax error: {e}")

checksums = []
for path in sorted(p for p in root.rglob("*") if p.is_file() and p.name != "SHA256SUMS.txt"):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    checksums.append(f"{digest}  {path.relative_to(root).as_posix()}")
(root / "SHA256SUMS.txt").write_text("\n".join(checksums) + "\n", encoding="utf-8")

report = {
    "status": "PASS" if not errors else "FAIL",
    "component_rows": len(components),
    "assembly_components": sum(r["include_in_top_assembly"] == "1" for r in components),
    "drawing_rows": len(drawings),
    "source_stl_files": len(list((root / "source_stl").glob("*.stl"))),
    "errors": errors,
}
(root / "VALIDATION_REPORT.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
raise SystemExit(1 if errors else 0)
