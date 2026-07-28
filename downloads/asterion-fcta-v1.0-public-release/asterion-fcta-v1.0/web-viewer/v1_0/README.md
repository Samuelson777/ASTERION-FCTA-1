# Version 1.0 Web Viewer

Serve this folder through a local web server or deploy it using `.github/workflows/pages.yml`.

```bash
python -m http.server 8000 --directory web-viewer/v1_0
```

The page loads Three.js from a public CDN and therefore requires internet access unless those modules are vendored locally.
