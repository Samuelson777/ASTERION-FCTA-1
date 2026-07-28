"""Validate the minimum ASTERION Version 0.2 release content."""
from pathlib import Path
import json
import sys
import trimesh

ROOT = Path(__file__).resolve().parents[2]
required = [
    ROOT / "cad/nx_master_model/v0_2/nx_expressions_v0_2.txt",
    ROOT / "cad/nx_master_model/v0_2/station_table.csv",
    ROOT / "cad/nx_master_model/v0_2/neutral/asterion_master_envelope.glb",
    ROOT / "cad/nx_master_model/v0_2/neutral/asterion_master_envelope.stl",
    ROOT / "cad/nx_master_model/v0_2/drawings/asterion_plan_view.dxf",
    ROOT / "calculations/v0_2_geometry_report.json",
]
missing = [str(p) for p in required if not p.exists()]
if missing:
    print("Missing files:")
    print("\n".join(missing))
    sys.exit(1)

mesh = trimesh.load_mesh(required[3], force="mesh")
if len(mesh.vertices) < 1000 or len(mesh.faces) < 1000:
    raise SystemExit("Envelope mesh appears unexpectedly small.")
report = json.loads(required[5].read_text(encoding="utf-8"))
assert report["version"] == "0.2.0"
assert report["coordinate_system"]["x"] == "forward"
print("ASTERION Version 0.2 package validation passed.")
print(f"Vertices: {len(mesh.vertices):,}; faces: {len(mesh.faces):,}")
