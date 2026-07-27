from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit
from html.parser import HTMLParser
import hashlib
import json
import re
import shutil
import struct
import subprocess
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
WARNINGS: list[str] = []


def error(message: str) -> None:
    ERRORS.append(message)


def warning(message: str) -> None:
    WARNINGS.append(message)


def local_path(reference: str) -> Path | None:
    parsed = urlsplit(reference)
    if parsed.scheme or reference.startswith(('#', 'mailto:', 'tel:', 'data:', 'blob:')):
        return None
    clean = parsed.path.lstrip('/')
    if not clean:
        clean = 'index.html'
    candidate = (ROOT / clean).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        error(f'path escapes repository: {reference}')
        return None
    return candidate


def check_file_reference(reference: str, source: str) -> None:
    path = local_path(reference)
    if path is not None and not path.exists():
        error(f'broken reference in {source}: {reference}')


class SiteHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.references: set[str] = set()
        self.script_sources: list[str] = []
        self.meta_names: set[str] = set()
        self.link_rels: list[list[str]] = []
        self.subsystem_buttons = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or '' for key, value in attrs}
        if values.get('id'):
            self.ids.append(values['id'])
        attribute = 'href' if tag in {'a', 'link'} else 'src' if tag in {'script', 'img'} else None
        if attribute and values.get(attribute):
            self.references.add(values[attribute])
        if tag == 'script' and values.get('src'):
            self.script_sources.append(values['src'])
        if tag == 'meta' and values.get('name'):
            self.meta_names.add(values['name'])
        if tag == 'link' and values.get('rel'):
            self.link_rels.append(values['rel'].split())
        if tag == 'button' and 'subsystem' in values.get('class', '').split():
            self.subsystem_buttons += 1


def validate_html() -> set[str]:
    path = ROOT / 'index.html'
    parser = SiteHTMLParser()
    parser.feed(path.read_text(encoding='utf-8'))
    duplicate_ids = sorted({value for value in parser.ids if parser.ids.count(value) > 1})
    if duplicate_ids:
        error(f'duplicate HTML ids: {duplicate_ids}')

    for reference in parser.references:
        check_file_reference(reference, 'index.html')

    if 'js/bootstrap.js' not in parser.script_sources:
        error('index.html must load js/bootstrap.js')
    if 'js/app.js' in parser.script_sources:
        error('index.html should not load app.js directly; bootstrap must handle startup failures')
    if 'viewport' not in parser.meta_names:
        error('viewport meta tag missing')
    if not any('manifest' in rels for rels in parser.link_rels):
        error('web manifest link missing')
    if parser.subsystem_buttons != 9:
        error('expected nine subsystem controls')
    return parser.references


def validate_versions() -> set[str]:
    text = (ROOT / 'js/versions.js').read_text(encoding='utf-8')
    ids = re.findall(r"\bid\s*:\s*['\"](v\d+\.\d+)['\"]", text)
    if len(ids) != 10:
        error(f'expected 10 version records, found {len(ids)}')
    if len(set(ids)) != len(ids):
        error('duplicate version ids in versions.js')
    expected = [f'v0.{number}' for number in range(1, 10)] + ['v1.0']
    if ids != expected:
        error(f'version order mismatch: {ids}')

    refs = set(re.findall(r"['\"]((?:assets|downloads)/[^'\"]+)['\"]", text))
    for reference in refs:
        check_file_reference(reference, 'js/versions.js')
    return refs


def validate_manifest() -> set[str]:
    path = ROOT / 'manifest.webmanifest'
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        error(f'invalid manifest JSON: {exc}')
        return set()
    for field in ('id', 'name', 'short_name', 'start_url', 'scope', 'display', 'icons'):
        if field not in data:
            error(f'manifest field missing: {field}')
    refs: set[str] = set()
    for icon in data.get('icons', []):
        source = icon.get('src')
        if source:
            refs.add(source)
            check_file_reference(source, 'manifest.webmanifest')
    return refs


def validate_service_worker() -> set[str]:
    text = (ROOT / 'sw.js').read_text(encoding='utf-8')
    if "asterion-live-v1.1" not in text:
        error('service-worker cache version was not updated to v1.1')
    refs = set(re.findall(r"['\"](\./[^'\"]+)['\"]", text))
    for reference in refs:
        check_file_reference(reference[2:], 'sw.js')
    if 'response.ok' not in text:
        error('service worker must avoid caching failed responses')
    return refs


def validate_javascript() -> None:
    node = shutil.which('node')
    if not node:
        warning('Node.js unavailable; JavaScript syntax checks skipped')
        return
    for path in [ROOT / 'js/app.js', ROOT / 'js/bootstrap.js', ROOT / 'js/versions.js', ROOT / 'sw.js']:
        result = subprocess.run([node, '--check', str(path)], text=True, capture_output=True)
        if result.returncode:
            error(f'JavaScript syntax failure in {path.relative_to(ROOT)}: {result.stderr.strip()}')


def validate_glb(path: Path) -> dict[str, int]:
    data = path.read_bytes()
    if len(data) < 12:
        error(f'GLB too short: {path.name}')
        return {'bytes': len(data), 'version': 0}
    magic, version, declared_length = struct.unpack('<4sII', data[:12])
    if magic != b'glTF':
        error(f'invalid GLB magic: {path.name}')
    if version != 2:
        error(f'unsupported GLB version {version}: {path.name}')
    if declared_length != len(data):
        error(f'GLB length mismatch: {path.name} declares {declared_length}, actual {len(data)}')
    return {'bytes': len(data), 'version': version}


def validate_assets() -> tuple[int, int]:
    model_paths = sorted((ROOT / 'assets/models').glob('*.glb'))
    if len(model_paths) != 9:
        error(f'expected 9 GLB assets, found {len(model_paths)}')
    for path in model_paths:
        validate_glb(path)

    try:
        import trimesh  # type: ignore
        for path in model_paths:
            scene = trimesh.load(path, force='scene')
            if not scene.geometry:
                error(f'GLB contains no geometry: {path.name}')
    except ImportError:
        warning('trimesh unavailable; semantic GLB checks skipped')
    except Exception as exc:
        error(f'trimesh GLB validation failed: {exc}')

    image_count = 0
    try:
        from PIL import Image
        for path in sorted((ROOT / 'assets').rglob('*.png')):
            with Image.open(path) as image:
                image.verify()
            image_count += 1
    except ImportError:
        warning('Pillow unavailable; PNG validation skipped')
    except Exception as exc:
        error(f'PNG validation failed: {exc}')
    return len(model_paths), image_count


def validate_downloads() -> int:
    archives = sorted((ROOT / 'downloads').glob('*.zip'))
    if len(archives) != 3:
        error(f'expected three downloadable ZIP archives, found {len(archives)}')
    for path in archives:
        try:
            with zipfile.ZipFile(path) as archive:
                bad = archive.testzip()
                if bad:
                    error(f'corrupt member {bad} in {path.name}')
        except Exception as exc:
            error(f'cannot open ZIP {path.name}: {exc}')

    pptx = ROOT / 'assets/docs/ASTERION_FCTA_1_v0_9_Design_Review.pptx'
    try:
        with zipfile.ZipFile(pptx) as archive:
            if archive.testzip():
                error('PowerPoint archive contains a corrupt member')
    except Exception as exc:
        error(f'cannot open PowerPoint file: {exc}')

    pdf = ROOT / 'assets/docs/ASTERION_FCTA_1_Full_Tutorial_Drawings.pdf'
    if not pdf.read_bytes().startswith(b'%PDF-'):
        error('tutorial drawings file is not a valid PDF header')
    return len(archives)


def validate_workflow() -> None:
    text = (ROOT / '.github/workflows/pages.yml').read_text(encoding='utf-8')
    required = ['actions/checkout@v4', 'actions/configure-pages@v5', 'actions/upload-pages-artifact@v3', 'actions/deploy-pages@v4']
    for item in required:
        if item not in text:
            error(f'GitHub Pages workflow missing {item}')
    if 'path: .' not in text:
        error('GitHub Pages workflow must upload the repository root')


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()



def validate_checksums() -> int:
    checksum_file = ROOT / 'SHA256SUMS.txt'
    if not checksum_file.exists():
        error('SHA256SUMS.txt is missing')
        return 0
    records: dict[str, str] = {}
    for line_number, line in enumerate(checksum_file.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        if not match:
            error(f'invalid checksum line {line_number}')
            continue
        digest, relative = match.groups()
        records[relative] = digest
    expected = {path.relative_to(ROOT).as_posix() for path in ROOT.rglob('*') if path.is_file() and path != checksum_file}
    missing = sorted(expected - records.keys())
    extra = sorted(records.keys() - expected)
    if missing:
        error(f'checksum entries missing for {missing[:10]}')
    if extra:
        error(f'checksum entries reference missing files {extra[:10]}')
    for relative in sorted(expected & records.keys()):
        if sha256(ROOT / relative) != records[relative]:
            error(f'checksum mismatch: {relative}')
    return len(records)

def main() -> int:
    required = [
        'index.html', '404.html', 'css/styles.css', 'js/bootstrap.js', 'js/app.js', 'js/versions.js',
        'sw.js', 'manifest.webmanifest', '.github/workflows/pages.yml', '.nojekyll',
        'assets/icons/icon-192.png', 'assets/icons/icon-512.png'
    ]
    for relative in required:
        if not (ROOT / relative).exists():
            error(f'missing required file: {relative}')

    html_refs = validate_html()
    version_refs = validate_versions()
    manifest_refs = validate_manifest()
    sw_refs = validate_service_worker()
    validate_javascript()
    model_count, image_count = validate_assets()
    archive_count = validate_downloads()
    validate_workflow()
    checksum_entries = validate_checksums()

    file_count = sum(1 for path in ROOT.rglob('*') if path.is_file())
    report = {
        'status': 'FAIL' if ERRORS else 'PASS',
        'files': file_count,
        'html_references': len(html_refs),
        'version_references': len(version_refs),
        'manifest_references': len(manifest_refs),
        'service_worker_references': len(sw_refs),
        'glb_assets': model_count,
        'png_assets': image_count,
        'download_archives': archive_count,
        'checksum_entries': checksum_entries,
        'warnings': WARNINGS,
        'errors': ERRORS,
        'index_sha256': sha256(ROOT / 'index.html')
    }
    print(json.dumps(report, indent=2))
    return 1 if ERRORS else 0


if __name__ == '__main__':
    sys.exit(main())
