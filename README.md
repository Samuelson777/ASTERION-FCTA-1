# ASTERION FCTA-1 Live 3D App v1.1

A single-page GitHub Pages application presenting the ASTERION CAD/CAM/CAE project from version 0.1 through 1.0.

## Main features

- Ten-stage interactive version timeline
- Three.js GLB viewer with orbit, fit, wireframe, X-ray, explode and section controls
- Procedural Version 0.1 concept model
- Version-specific CAD, structural, multiphysics and manufacturing scenes
- Subsystem highlighting for structure, habitat, propulsion, power, thermal, Skimmer, docking and robotics
- Engineering maturity and result dashboards
- Evidence gallery and downloadable report, drawings, presentation and release packages
- Responsive desktop/mobile layout and persistent light/dark appearance
- Installable web-app manifest and service-worker caching
- Automatic GitHub Pages deployment workflow

## Reliability fixes in v1.1

- Automatically normalises millimetre-based and metre-based GLB files into a consistent metre-scale viewer
- Prevents stale model requests from replacing the currently selected version
- Removes failed-load overlays after a successful retry
- Adds clear recovery messages for WebGL, Three.js and model-loading failures
- Adds a 45-second model-load timeout
- Improves snapshot creation and reports failures instead of silently stopping
- Adds reduced-motion handling and stronger keyboard/focus accessibility
- Adds project-site 404 redirection
- Adds PNG PWA icons, safer service-worker caching and offline navigation fallback
- Expands validation to GLB structure, ZIP integrity, JavaScript syntax, HTTP delivery and browser interaction contracts

## Run locally

Do not open `index.html` directly because browsers restrict JavaScript modules and GLB loading from `file://` paths.

On Windows, double-click `START_ASTERION.bat`, or run:

```bash
python tools/serve.py
```

Then open:

```text
http://127.0.0.1:8000/
```

Alternative port:

```bash
python tools/serve.py --port 8080
```

## Validate everything

On Windows, double-click `RUN_TESTS.bat`. You can also run the complete test sequence:

```bash
npm test
```

Or run each test separately:

```bash
python tools/validate_site.py
python tools/http_smoke_test.py
python tools/browser_contract_test.py
```

`browser_contract_test.py` uses Playwright when available. It tests the user-interface contract with deterministic Three.js/GLTF test doubles, including rapid version changes, controls, snapshot naming, theme changes, mobile overflow and WebGL failure recovery. The actual GLB binaries are independently parsed by the main validator.

## Publish on GitHub Pages

1. Create a GitHub repository.
2. Upload every file in this folder to the repository root.
3. Push to the `main` branch.
4. Open **Settings → Pages**.
5. Select **GitHub Actions** as the source.
6. The included `.github/workflows/pages.yml` workflow deploys the site.

The application is static and does not require a server-side database. Three.js is pinned through the import map. After a successful online load, the service worker can cache the application and CDN modules for later use.

## Claim boundary

This site presents conceptual engineering geometry and reduced-order screening. It does not claim a certified spacecraft, production aircraft, solved proprietary ANSYS database or fully parametric native Siemens NX release.
