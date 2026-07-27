"""ASTERION FCTA-1 native Siemens NX builder.

Run INSIDE Siemens NX through Developer/Tools > Journal > Play.

Outputs native NX .prt files for:
  * individual imported facet-body parts;
  * the top-level assembly (NX assemblies also use .prt);
  * separate master-model drawing parts with A3 sheets and base views.

The source files are STL meshes. The resulting NX parts contain convergent/facet
bodies, not recovered parametric feature history. Rebuild critical parts from the
provided dimensions and tutorials when editable design intent is required.

Tested here only by static validation because Siemens NX is not installed in the
artifact-generation environment. The script uses long-established NXOpen APIs
and writes a detailed build log. API availability and licences can vary by NX
release and installation.
"""
from __future__ import annotations

import csv
import os
import sys
import subprocess
import traceback
from datetime import datetime
from pathlib import Path


def _package_root() -> Path:
    return Path(__file__).resolve().parents[1]


PACKAGE_ROOT = Path(os.environ.get("ASTERION_BUILDER_ROOT", str(_package_root()))).resolve()
SOURCE_ROOT = PACKAGE_ROOT
OUTPUT_ROOT = Path(
    os.environ.get("ASTERION_NX_OUTPUT", str(PACKAGE_ROOT / "native_output" / "NX_NATIVE"))
).resolve()
OVERWRITE = os.environ.get("ASTERION_OVERWRITE", "0").strip() in {"1", "true", "TRUE", "yes", "YES"}

COMPONENT_MANIFEST = PACKAGE_ROOT / "config" / "nx_component_manifest.csv"
DRAWING_MANIFEST = PACKAGE_ROOT / "config" / "drawing_manifest.csv"
LOG_PATH = OUTPUT_ROOT / "ASTERION_NX_BUILD_LOG.csv"


def _outside_nx_help() -> str:
    return (
        "NXOpen is provided by Siemens NX and is not available in ordinary Python.\n"
        "Do not run this file with python.exe, VS Code Run Python File, or IDLE.\n\n"
        "Use one of these supported launch methods:\n"
        "  1. Double-click RUN_ASTERION_BUILDER.bat in the package root.\n"
        "  2. In Siemens NX: Developer/Tools > Journal > Play, then select this file.\n"
        "  3. From an NX Command Prompt: run_journal.exe <this-script>.\n\n"
        "Do not install the unrelated PyPI package named nxopen; it is not the Siemens NX API."
    )


def _try_relaunch_through_nx() -> bool:
    """Relaunch this journal through Siemens NX when started by normal Python.

    Returns True after a launcher was invoked. The launcher performs NX discovery,
    sets ASTERION paths, and calls Siemens run_journal.exe.
    """
    if os.name != "nt" or os.environ.get("ASTERION_NX_RELAUNCHED") == "1":
        return False

    launcher = PACKAGE_ROOT / "nxopen" / "run_asterion_builder.ps1"
    if not launcher.is_file():
        return False

    powershell = os.environ.get("SystemRoot", r"C:\Windows") + r"\System32\WindowsPowerShell\v1.0\powershell.exe"
    if not Path(powershell).is_file():
        powershell = "powershell.exe"

    command = [
        powershell,
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(launcher),
    ]
    if OVERWRITE:
        command.append("-Overwrite")

    print("NXOpen was not found in this Python interpreter.")
    print("Attempting to relaunch the builder through Siemens NX...")
    completed = subprocess.run(command, cwd=str(PACKAGE_ROOT), check=False)
    if completed.returncode != 0:
        raise SystemExit(
            f"The Siemens NX launcher returned exit code {completed.returncode}.\n\n"
            + _outside_nx_help()
        )
    return True


class BuildFailure(RuntimeError):
    pass


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _safe_remove(path: Path) -> None:
    if path.exists():
        if not OVERWRITE:
            raise BuildFailure(f"Output already exists: {path}. Set ASTERION_OVERWRITE=1 to replace it.")
        path.unlink()


def _identity_matrix(NXOpen):
    matrix = NXOpen.Matrix3x3()
    matrix.Xx, matrix.Xy, matrix.Xz = 1.0, 0.0, 0.0
    matrix.Yx, matrix.Yy, matrix.Yz = 0.0, 1.0, 0.0
    matrix.Zx, matrix.Zy, matrix.Zz = 0.0, 0.0, 1.0
    return matrix


def _write_log(rows: list[dict[str, str]]) -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    fields = ["timestamp", "stage", "item", "status", "message"]
    with LOG_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _log(rows, stage, item, status, message=""):
    rows.append({
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "stage": stage,
        "item": item,
        "status": status,
        "message": str(message).replace("\n", " | ")[:1500],
    })
    _write_log(rows)


def _import_stl_into_part(NXOpen, part, source_stl: Path):
    """Import an STL using the standard NXOpen STLImporter."""
    importer = part.ImportManager.CreateStlImporter()
    try:
        importer.FileName = str(source_stl)
        importer.FileUnits = NXOpen.STLImporter.FileUnitsType.Millimeters
        importer.AngularTolerance = NXOpen.STLImporter.AngularToleranceType.Fine
        importer.HideSmoothEdges = True
        importer.DisplayInformation = False
        importer.Commit()
    finally:
        importer.Destroy()


def _new_metric_part(NXOpen, session, output_path: Path):
    _safe_remove(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return session.Parts.NewDisplay(str(output_path), NXOpen.Part.Units.Millimeters)


def _save_part(part, output_path: Path):
    status = part.SaveAs(str(output_path))
    try:
        status.Dispose()
    except Exception:
        pass


def build_native_parts(NXOpen, session, rows, manifest):
    created: dict[str, Path] = {}
    for item in manifest:
        part_name = item["nx_part_name"].strip()
        source_path = SOURCE_ROOT / item["source_stl"].strip()
        output_path = OUTPUT_ROOT / "parts" / part_name
        try:
            if not source_path.is_file():
                raise BuildFailure(f"Missing source STL: {source_path}")
            part = _new_metric_part(NXOpen, session, output_path)
            _import_stl_into_part(NXOpen, part, source_path)
            try:
                part.SetUserAttribute("ASTERION_ID", -1, item["id"], NXOpen.Update.Option.Now)
                part.SetUserAttribute("ASTERION_SOURCE_STL", -1, item["source_stl"], NXOpen.Update.Option.Now)
                part.SetUserAttribute("ASTERION_DESCRIPTION", -1, item["description"], NXOpen.Update.Option.Now)
            except Exception:
                # Attributes are useful but non-critical across NX releases.
                pass
            _save_part(part, output_path)
            created[part_name] = output_path
            _log(rows, "PART", part_name, "PASS", f"Imported {source_path.name}")
        except Exception as exc:
            _log(rows, "PART", part_name, "FAIL", f"{type(exc).__name__}: {exc}")
            raise
    return created


def build_top_assembly(NXOpen, session, rows, manifest, created_parts):
    assembly_name = "AST-0000-ASTERION-FCTA-1-ASSY.prt"
    output_path = OUTPUT_ROOT / "assemblies" / assembly_name
    assembly = _new_metric_part(NXOpen, session, output_path)
    component_assembly = assembly.ComponentAssembly
    origin = NXOpen.Point3d(0.0, 0.0, 0.0)
    orientation = _identity_matrix(NXOpen)

    included = [m for m in manifest if m["include_in_top_assembly"].strip() == "1"]
    for item in included:
        part_path = created_parts[item["nx_part_name"].strip()]
        component_name = item["component_name"].strip()
        try:
            result = component_assembly.AddComponent(
                str(part_path), "Entire Part", component_name, origin, orientation, -1
            )
            # Python wrappers commonly return (component, PartLoadStatus).
            if isinstance(result, tuple) and len(result) > 1:
                load_status = result[1]
                try:
                    load_status.Dispose()
                except Exception:
                    pass
            _log(rows, "ASSEMBLY_COMPONENT", component_name, "PASS", part_path.name)
        except Exception as exc:
            _log(rows, "ASSEMBLY_COMPONENT", component_name, "FAIL", f"{type(exc).__name__}: {exc}")
            raise

    try:
        assembly.SetUserAttribute("ASTERION_CONFIGURATION", -1, "FCTA-1 V1.0", NXOpen.Update.Option.Now)
    except Exception:
        pass
    _save_part(assembly, output_path)
    _log(rows, "ASSEMBLY", assembly_name, "PASS", f"{len(included)} components at absolute origin")
    return output_path


def _find_model_view(part, wanted: str):
    wanted_upper = wanted.upper()
    candidates = []
    try:
        candidates = list(part.ModelingViews.ToArray())
    except Exception:
        candidates = list(part.ModelingViews)
    for view in candidates:
        name = getattr(view, "Name", "")
        if str(name).upper() == wanted_upper:
            return view
    # Fallback to FindObject for installations using standard names.
    for name in (wanted, wanted.upper(), wanted.capitalize()):
        try:
            return part.ModelingViews.FindObject(name)
        except Exception:
            pass
    raise BuildFailure(f"Could not find standard modeling view: {wanted}")


def _insert_a3_sheet(NXOpen, drawing_part, sheet_name: str, scale_denominator: float):
    return drawing_part.DrawingSheets.InsertSheet(
        sheet_name,
        NXOpen.Drawings.DrawingSheet.StandardSheetSize.A3,
        1.0,
        float(scale_denominator),
        NXOpen.Drawings.DrawingSheet.ProjectionAngleType.ThirdAngle,
    )


def _add_standard_views(NXOpen, drawing_part, sheet, denominator: float):
    scale = 1.0 / float(denominator)
    views = sheet.SheetDraftingViews
    front = _find_model_view(drawing_part, "Front")
    top = _find_model_view(drawing_part, "Top")
    right = _find_model_view(drawing_part, "Right")
    iso = None
    for iso_name in ("Trimetric", "Isometric", "TFR-ISO"):
        try:
            iso = _find_model_view(drawing_part, iso_name)
            break
        except Exception:
            continue

    views.CreateBaseView(front, NXOpen.Point3d(115.0, 105.0, 0.0), scale, False)
    views.CreateBaseView(top, NXOpen.Point3d(115.0, 205.0, 0.0), scale, False)
    views.CreateBaseView(right, NXOpen.Point3d(265.0, 105.0, 0.0), scale, False)
    if iso is not None:
        views.CreateBaseView(iso, NXOpen.Point3d(270.0, 205.0, 0.0), scale * 0.75, False)


def build_drawing_parts(NXOpen, session, rows, drawing_manifest, model_paths):
    drawing_dir = OUTPUT_ROOT / "drawings"
    drawing_dir.mkdir(parents=True, exist_ok=True)
    for item in drawing_manifest:
        model_name = item["model_prt"].strip()
        drawing_name = item["drawing_prt"].strip()
        output_path = drawing_dir / drawing_name
        model_path = model_paths.get(model_name)
        if model_path is None:
            _log(rows, "DRAWING", drawing_name, "FAIL", f"Model not built: {model_name}")
            continue
        try:
            drawing_part = _new_metric_part(NXOpen, session, output_path)
            origin = NXOpen.Point3d(0.0, 0.0, 0.0)
            orientation = _identity_matrix(NXOpen)
            result = drawing_part.ComponentAssembly.AddComponent(
                str(model_path), "Entire Part", "MASTER_MODEL", origin, orientation, -1
            )
            if isinstance(result, tuple) and len(result) > 1:
                try:
                    result[1].Dispose()
                except Exception:
                    pass

            sheet = _insert_a3_sheet(
                NXOpen, drawing_part, item["sheet_name"].strip(), float(item["scale_denominator"])
            )
            _add_standard_views(NXOpen, drawing_part, sheet, float(item["scale_denominator"]))
            try:
                drawing_part.SetUserAttribute("ASTERION_DRAWING_TITLE", -1, item["title"], NXOpen.Update.Option.Now)
                drawing_part.SetUserAttribute("ASTERION_MASTER_MODEL", -1, model_name, NXOpen.Update.Option.Now)
            except Exception:
                pass
            _save_part(drawing_part, output_path)
            _log(rows, "DRAWING", drawing_name, "PASS", f"A3 sheet linked to {model_name}")
        except Exception as exc:
            # Save a linked drawing/master-model part where possible, then continue.
            try:
                _save_part(drawing_part, output_path)
            except Exception:
                pass
            _log(
                rows,
                "DRAWING",
                drawing_name,
                "PARTIAL",
                f"Linked model saved, but sheet/view creation needs manual completion: {type(exc).__name__}: {exc}",
            )


def main():
    try:
        import NXOpen
        import NXOpen.Drawings
    except ImportError:
        if _try_relaunch_through_nx():
            return
        raise SystemExit(_outside_nx_help())

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    _log(rows, "BUILD", "ASTERION", "START", f"Output={OUTPUT_ROOT}; overwrite={OVERWRITE}")

    component_manifest = _read_csv(COMPONENT_MANIFEST)
    drawing_manifest = _read_csv(DRAWING_MANIFEST)
    session = NXOpen.Session.GetSession()
    listing = session.ListingWindow
    listing.Open()
    listing.WriteFullline("ASTERION native NX build started")
    listing.WriteFullline(f"Output folder: {OUTPUT_ROOT}")

    try:
        created_parts = build_native_parts(NXOpen, session, rows, component_manifest)
        assembly_path = build_top_assembly(NXOpen, session, rows, component_manifest, created_parts)
        model_paths = dict(created_parts)
        model_paths[assembly_path.name] = assembly_path
        build_drawing_parts(NXOpen, session, rows, drawing_manifest, model_paths)
        _log(rows, "BUILD", "ASTERION", "COMPLETE", "Review build log and native files.")
        listing.WriteFullline("ASTERION native NX build completed. Review ASTERION_NX_BUILD_LOG.csv")
    except Exception as exc:
        _log(rows, "BUILD", "ASTERION", "FAIL", traceback.format_exc())
        listing.WriteFullline(f"ASTERION build failed: {type(exc).__name__}: {exc}")
        raise
    finally:
        listing.Close()


if __name__ == "__main__":
    main()
