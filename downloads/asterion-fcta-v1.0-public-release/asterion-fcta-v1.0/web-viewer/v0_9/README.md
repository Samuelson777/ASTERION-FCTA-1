# ASTERION FCTA-1 GitHub Pages Viewer

This folder is a single-page interactive 3D portfolio viewer using Three.js. Open `index.html` through a local server or publish it through GitHub Pages.

Example local command:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000/web-viewer/v0_9/`.

The viewer uses CDN-hosted Three.js by default. For strict offline publication, vendor the Three.js modules locally and update the import paths in `js/app.js`.
