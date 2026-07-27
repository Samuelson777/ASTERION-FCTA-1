from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.request import Request, urlopen
import json
import mimetypes
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
mimetypes.add_type('model/gltf-binary', '.glb')
mimetypes.add_type('application/manifest+json', '.webmanifest')
mimetypes.add_type('text/javascript', '.js')


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        return


def collect_paths() -> set[str]:
    paths = {
        '', 'index.html', 'css/styles.css', 'js/bootstrap.js', 'js/app.js', 'js/versions.js',
        'manifest.webmanifest', 'sw.js', 'assets/asterion-mark.svg'
    }
    for source in ['index.html', 'js/versions.js', 'manifest.webmanifest', 'sw.js']:
        text = (ROOT / source).read_text(encoding='utf-8')
        for reference in re.findall(r"(?:src|href)=['\"]([^'\"#]+)|['\"]((?:\./)?(?:assets|downloads|css|js)/[^'\"]+)['\"]", text):
            value = next((part for part in reference if part), '')
            if value and not value.startswith(('http:', 'https:', 'mailto:', 'data:', 'blob:')):
                paths.add(value.removeprefix('./').split('?', 1)[0])
    return paths


def main() -> int:
    handler = partial(QuietHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f'http://127.0.0.1:{server.server_port}/'
    errors: list[str] = []
    checked = 0

    try:
        for relative in sorted(collect_paths()):
            method = 'HEAD' if relative.startswith('downloads/') or relative.endswith(('.pdf', '.pptx')) else 'GET'
            request = Request(base + relative, method=method)
            try:
                with urlopen(request, timeout=20) as response:
                    checked += 1
                    if response.status != 200:
                        errors.append(f'{relative}: HTTP {response.status}')
                    content_type = response.headers.get_content_type()
                    if relative.endswith('.js') and content_type not in {'text/javascript', 'application/javascript'}:
                        errors.append(f'{relative}: incorrect JavaScript MIME {content_type}')
                    if relative.endswith('.glb') and content_type not in {'model/gltf-binary', 'application/octet-stream'}:
                        errors.append(f'{relative}: incorrect GLB MIME {content_type}')
                    if method == 'GET':
                        payload = response.read()
                        if relative.endswith('.glb') and not payload.startswith(b'glTF'):
                            errors.append(f'{relative}: invalid GLB response header')
            except Exception as exc:
                errors.append(f'{relative}: {exc}')
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    report = {'status': 'FAIL' if errors else 'PASS', 'checked': checked, 'errors': errors}
    print(json.dumps(report, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
