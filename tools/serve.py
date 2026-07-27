from __future__ import annotations

from argparse import ArgumentParser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import mimetypes
import webbrowser

ROOT = Path(__file__).resolve().parents[1]
mimetypes.add_type('model/gltf-binary', '.glb')
mimetypes.add_type('application/manifest+json', '.webmanifest')
mimetypes.add_type('text/javascript', '.js')


def main() -> None:
    parser = ArgumentParser(description='Serve the ASTERION GitHub Pages app locally.')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()

    handler = partial(SimpleHTTPRequestHandler, directory=str(ROOT))
    try:
        server = ThreadingHTTPServer((args.host, args.port), handler)
    except OSError as exc:
        raise SystemExit(f'Could not start server on {args.host}:{args.port}: {exc}') from exc

    url = f'http://{args.host}:{server.server_port}/'
    print(f'ASTERION Live 3D App: {url}')
    print('Press Ctrl+C to stop the server.')
    if not args.no_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped.')
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
