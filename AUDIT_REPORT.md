# ASTERION Live 3D Website Audit — v1.1

## Audit scope

The audit covered:

- HTML structure and unique element IDs
- CSS responsiveness and reduced-motion behaviour
- JavaScript syntax and interactive controls
- Version 0.1–1.0 data integrity
- Local image, document, model and download references
- Nine GLB headers and scene geometry
- Three downloadable ZIP archives
- PowerPoint and PDF container integrity
- Web manifest and PWA icons
- Service-worker update and caching behaviour
- GitHub Pages deployment workflow
- Local HTTP MIME delivery
- Browser interaction contract at desktop and mobile widths

## Corrected defects

1. **Mixed model units** — Versions 0.2, 0.3, 0.4 and 0.6 used millimetre geometry while Version 0.8 and the procedural concept used metre-scale values. The viewer now detects and converts large millimetre models to metres before fitting, clipping and displaying extents.
2. **Asynchronous model race** — Rapid version selection could allow an older request to finish last and replace the current model. A generation token now rejects stale loads.
3. **Persistent error overlay** — A failed model message could remain over a later successful model. Successful loads now clear all fallback panels.
4. **Uncaught startup failures** — WebGL or CDN import failures previously left the viewer on “Preparing”. A bootstrap loader now shows a recovery panel and reload action.
5. **Unbounded model wait** — GLB requests now have a 45-second timeout.
6. **Weak snapshot handling** — Snapshot download creation now uses a temporary DOM anchor and reports exceptions.
7. **Service-worker stale/error caching** — Navigation uses network-first behaviour, assets use cache-first behaviour, failed responses are not cached, and the pinned CDN is cacheable after first use.
8. **PWA icon coverage** — Added 192 px and 512 px PNG icons alongside the SVG mark.
9. **404 behaviour** — Added a compact redirect page suitable for GitHub project pages.
10. **Accessibility** — Added focus-visible styling, progressbar semantics, selected-step state, persistent theme labels, reduced-motion behaviour and disabled states during model loading.

## Test results

| Test | Result |
|---|---|
| Static repository validator | PASS |
| JavaScript syntax checks | PASS |
| GLB header and scene parsing | PASS |
| Download ZIP integrity | PASS |
| PowerPoint container integrity | PASS |
| PDF signature check | PASS |
| HTTP asset and MIME smoke test | PASS |
| Browser interaction contract | PASS |
| Mobile horizontal-overflow check | PASS |
| WebGL failure-recovery check | PASS |

## Browser test boundary

The execution environment blocks a normal GPU/WebGL plus public-CDN browser session. The browser contract therefore uses deterministic Three.js and GLTF test doubles to exercise the real application code and user controls. The actual GLB files are separately loaded and inspected through the repository validator. A final visual GPU check should still be run on the deployment computer using Chrome, Edge or Firefox.
