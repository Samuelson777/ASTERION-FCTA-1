import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { versions, subsystemPatterns } from './versions.js';

const $ = (selector, parent = document) => parent.querySelector(selector);
const $$ = (selector, parent = document) => [...parent.querySelectorAll(selector)];
const viewer = $('#viewer');
const loadStatus = $('#load-status');
const viewerButtons = $$('.viewer-toolbar button, .subsystem');

let selectedIndex = versions.findIndex((version) => location.hash === `#${version.id}`);
if (selectedIndex < 0) selectedIndex = versions.length - 1;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x050a12);
scene.fog = new THREE.FogExp2(0x050a12, 0.0022);

const camera = new THREE.PerspectiveCamera(42, 1, 0.01, 3000);
camera.position.set(60, 36, 60);

let renderer;
try {
  renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: false,
    preserveDrawingBuffer: true,
    powerPreference: 'high-performance'
  });
} catch (error) {
  throw new Error(`WebGL renderer could not start: ${error.message}`);
}

renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.12;
renderer.localClippingEnabled = true;
renderer.domElement.setAttribute('aria-label', 'Interactive ASTERION 3D model canvas');
renderer.domElement.addEventListener('webglcontextlost', (event) => {
  event.preventDefault();
  status('WebGL context lost — reload the page', 'error');
  showViewerFallback('3D graphics paused', 'The browser lost its WebGL context. Reload the page to restore the viewer.');
});
viewer.replaceChildren(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.screenSpacePanning = true;
controls.zoomToCursor = true;

const pmrem = new THREE.PMREMGenerator(renderer);
const environmentTarget = pmrem.fromScene(new RoomEnvironment(), 0.03);
scene.environment = environmentTarget.texture;
pmrem.dispose();

scene.add(new THREE.HemisphereLight(0xdff4ff, 0x132033, 2.2));
const keyLight = new THREE.DirectionalLight(0xffffff, 4);
keyLight.position.set(48, 72, 40);
scene.add(keyLight);
const rimLight = new THREE.DirectionalLight(0x65caff, 2.2);
rimLight.position.set(-50, 18, -32);
scene.add(rimLight);
const fillLight = new THREE.DirectionalLight(0xa9ffd4, 1.2);
fillLight.position.set(12, -25, 40);
scene.add(fillLight);

const world = new THREE.Group();
const overlayGroup = new THREE.Group();
scene.add(world, overlayGroup);

const grid = new THREE.GridHelper(180, 36, 0x29425b, 0x152336);
grid.rotation.z = Math.PI / 2;
grid.position.x = -30;
grid.material.opacity = 0.26;
grid.material.transparent = true;
scene.add(grid);

const stars = new THREE.Points(
  new THREE.BufferGeometry(),
  new THREE.PointsMaterial({ color: 0x8dcfff, size: 0.22, transparent: true, opacity: 0.75 })
);
{
  const points = [];
  for (let index = 0; index < 1600; index += 1) {
    const radius = 400 + Math.random() * 600;
    const angle = Math.random() * Math.PI * 2;
    const z = (Math.random() - 0.5) * 850;
    points.push(Math.cos(angle) * radius, Math.sin(angle) * radius, z);
  }
  stars.geometry.setAttribute('position', new THREE.Float32BufferAttribute(points, 3));
  scene.add(stars);
}

const loader = new GLTFLoader();
const clippingPlane = new THREE.Plane(new THREE.Vector3(-1, 0, 0), 100000);
const reducedMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false;

let currentRoot = null;
let currentMeshes = [];
let currentBox = new THREE.Box3();
let currentSize = new THREE.Vector3();
let currentExtentLabel = 'm';
let activeSubsystem = 'all';
let explodeFactor = 0;
let wireframe = false;
let xray = false;
let autoRotate = !reducedMotion;
let baseCameraPosition = new THREE.Vector3(60, 36, 60);
let baseTarget = new THREE.Vector3();
let fpsCounter = 0;
let fpsTime = performance.now();
let loadGeneration = 0;

function status(text, mode = 'ready') {
  if (!loadStatus) return;
  loadStatus.className = `load-status ${mode === 'loading' ? 'loading' : mode === 'error' ? 'error' : ''}`;
  const label = $('b', loadStatus);
  if (label) label.textContent = text;
}

function removeViewerFallback() {
  $$('.viewer-fallback', viewer).forEach((element) => element.remove());
}

function showViewerFallback(title, message) {
  removeViewerFallback();
  const fallback = document.createElement('div');
  fallback.className = 'viewer-fallback viewer-fallback-error';
  const heading = document.createElement('strong');
  heading.textContent = title;
  const text = document.createElement('span');
  text.textContent = message;
  const retry = document.createElement('button');
  retry.className = 'viewer-retry';
  retry.type = 'button';
  retry.textContent = 'Retry model';
  retry.addEventListener('click', () => loadVersion(selectedIndex, { updateHash: false }));
  fallback.append(heading, text, retry);
  viewer.append(fallback);
}

function setViewerControlsDisabled(disabled) {
  viewerButtons.forEach((button) => {
    button.disabled = disabled;
  });
  $('#explode').disabled = disabled;
  $('#clip').disabled = disabled;
}

function disposeObject(object) {
  object.traverse((node) => {
    node.geometry?.dispose?.();
    if (!node.material) return;
    const materials = Array.isArray(node.material) ? node.material : [node.material];
    materials.forEach((material) => material.dispose?.());
  });
}

function clearWorld() {
  overlayGroup.clear();
  if (currentRoot) {
    world.remove(currentRoot);
    disposeObject(currentRoot);
    currentRoot = null;
  }
  currentMeshes = [];
}

function cloneMaterials(root) {
  root.traverse((node) => {
    if (!node.isMesh || !node.material) return;
    node.material = Array.isArray(node.material)
      ? node.material.map((material) => material.clone())
      : node.material.clone();
    const materials = Array.isArray(node.material) ? node.material : [node.material];
    materials.forEach((material) => {
      material.userData.base = {
        opacity: material.opacity,
        transparent: material.transparent,
        color: material.color?.clone(),
        emissive: material.emissive?.clone(),
        wireframe: Boolean(material.wireframe)
      };
      material.clippingPlanes = [clippingPlane];
      material.clipShadows = true;
    });
    node.userData.basePosition = node.position.clone();
    node.userData.displayName = (node.name || node.parent?.name || 'component').toUpperCase();
  });
}

function createProceduralConcept() {
  const group = new THREE.Group();
  group.name = 'ASTERION_V0_1_CONCEPT';
  const metal = new THREE.MeshStandardMaterial({ color: 0xb8cad8, metalness: 0.75, roughness: 0.3 });
  const cyan = new THREE.MeshStandardMaterial({ color: 0x4cc8ff, metalness: 0.2, roughness: 0.35, emissive: 0x062b40 });
  const green = new THREE.MeshStandardMaterial({ color: 0x75e7b0, metalness: 0.15, roughness: 0.4, emissive: 0x083523 });
  const dark = new THREE.MeshStandardMaterial({ color: 0x1e3753, metalness: 0.25, roughness: 0.45 });

  const spine = new THREE.Mesh(new THREE.CylinderGeometry(1.25, 1.25, 42, 24), metal);
  spine.rotation.z = Math.PI / 2;
  spine.name = 'central_spine';
  group.add(spine);

  [-2.5, 2.5].forEach((x, index) => {
    const ring = new THREE.Mesh(new THREE.TorusGeometry(12, 1, 18, 96), index ? green : cyan);
    ring.rotation.y = Math.PI / 2;
    ring.position.x = x;
    ring.name = `habitat_ring_${index + 1}`;
    group.add(ring);
  });

  [[0, 28, 0], [0, -28, 0], [0, 0, 28], [0, 0, -28]].forEach((position, index) => {
    const panel = new THREE.Mesh(new THREE.BoxGeometry(12, 0.22, 5), dark);
    panel.position.set(...position);
    if (index > 1) panel.rotation.x = Math.PI / 2;
    panel.name = `solar_array_${index + 1}`;
    group.add(panel);
  });

  for (let index = 0; index < 6; index += 1) {
    const angle = index * Math.PI / 3;
    const pod = new THREE.Mesh(new THREE.CylinderGeometry(0.75, 0.9, 4, 20), metal);
    pod.rotation.z = Math.PI / 2;
    pod.position.set(-18, Math.cos(angle) * 3.4, Math.sin(angle) * 3.4);
    pod.name = `propulsion_pod_${index + 1}`;
    group.add(pod);
  }

  const skimmer = new THREE.Mesh(new THREE.ConeGeometry(3.4, 8, 4), dark);
  skimmer.rotation.z = -Math.PI / 2;
  skimmer.position.x = 25;
  skimmer.name = 'skimmer_concept';
  group.add(skimmer);
  return group;
}

function loadSingle(path, generation) {
  return new Promise((resolve, reject) => {
    let settled = false;
    const timeout = window.setTimeout(() => {
      if (settled) return;
      settled = true;
      reject(new Error(`Timed out while loading ${path}`));
    }, 45000);

    loader.load(
      path,
      (gltf) => {
        if (settled) {
          disposeObject(gltf.scene);
          return;
        }
        settled = true;
        clearTimeout(timeout);
        if (generation !== loadGeneration) {
          disposeObject(gltf.scene);
          resolve(null);
          return;
        }
        resolve(gltf.scene);
      },
      (event) => {
        if (generation !== loadGeneration) return;
        if (event.total) status(`Loading ${Math.round((event.loaded / event.total) * 100)}%`, 'loading');
      },
      (error) => {
        if (settled) return;
        settled = true;
        clearTimeout(timeout);
        reject(error instanceof Error ? error : new Error(String(error)));
      }
    );
  });
}

async function loadManufacturing(paths, generation) {
  const group = new THREE.Group();
  group.name = 'V0_7_MANUFACTURING_PORTFOLIO';
  const roots = await Promise.all(paths.map((path) => loadSingle(path, generation)));
  if (generation !== loadGeneration || roots.some((root) => root === null)) {
    roots.filter(Boolean).forEach(disposeObject);
    return null;
  }

  const positions = [[-3.5, 3.2, 0], [3.5, 3.2, 0], [-3.5, -3.2, 0], [3.5, -3.2, 0]];
  roots.forEach((root, index) => {
    const box = new THREE.Box3().setFromObject(root);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());
    root.position.sub(center);
    const scale = 4.5 / (Math.max(size.x, size.y, size.z) || 1);
    root.scale.setScalar(scale);
    root.position.add(new THREE.Vector3(...positions[index]));
    group.add(root);
  });
  return group;
}

function normaliseModelUnits(root, version) {
  root.updateMatrixWorld(true);
  const rawBox = new THREE.Box3().setFromObject(root);
  const rawSize = rawBox.getSize(new THREE.Vector3());
  const rawMax = Math.max(rawSize.x, rawSize.y, rawSize.z);

  if (version.modelMode === 'manufacturing') {
    currentExtentLabel = 'normalised';
    return;
  }

  const scale = Number.isFinite(version.unitScale)
    ? version.unitScale
    : rawMax > 1000
      ? 0.001
      : 1;

  if (scale !== 1) {
    root.scale.multiplyScalar(scale);
    root.updateMatrixWorld(true);
  }
  currentExtentLabel = 'm';
}

function prepareRoot(root, version) {
  normaliseModelUnits(root, version);
  cloneMaterials(root);
  currentRoot = root;
  world.add(root);
  currentMeshes = [];
  root.traverse((node) => {
    if (node.isMesh) currentMeshes.push(node);
  });

  currentBox.setFromObject(root);
  const center = currentBox.getCenter(new THREE.Vector3());
  root.position.sub(center);
  root.updateMatrixWorld(true);
  currentBox.setFromObject(root);
  currentSize = currentBox.getSize(new THREE.Vector3());

  currentMeshes.forEach((mesh) => {
    const meshBox = new THREE.Box3().setFromObject(mesh);
    const meshCenter = meshBox.getCenter(new THREE.Vector3());
    const localCenter = mesh.parent.worldToLocal(meshCenter.clone());
    const basePosition = mesh.position.clone();
    const direction = localCenter.sub(basePosition);
    if (direction.lengthSq() > 1e-12) direction.normalize();
    mesh.userData.basePosition = basePosition;
    mesh.userData.explodeVector = direction.multiplyScalar(Math.max(currentSize.length() * 0.08, 1));
  });

  removeViewerFallback();
  applyDisplayState({ announce: false });
  fitView();
  $('#hud-model').textContent = version.id.toUpperCase();
  $('#hud-size').textContent = currentExtentLabel === 'm'
    ? `${currentSize.x.toFixed(1)} × ${currentSize.y.toFixed(1)} × ${currentSize.z.toFixed(1)} m`
    : 'Normalised part layout';
  $('#hud-objects').textContent = String(currentMeshes.length);
}

function frameDistance() {
  const maxDimension = Math.max(currentSize.x, currentSize.y, currentSize.z) || 20;
  return maxDimension / (2 * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2))) * 1.25;
}

function fitView() {
  const distance = frameDistance();
  camera.position.set(distance * 0.85, distance * 0.55, distance * 0.85);
  camera.near = Math.max(distance / 1000, 0.01);
  camera.far = Math.max(distance * 40, 100);
  camera.updateProjectionMatrix();
  controls.target.set(0, 0, 0);
  controls.update();
  baseCameraPosition = camera.position.clone();
  baseTarget = controls.target.clone();
}

function resetView() {
  camera.position.copy(baseCameraPosition);
  controls.target.copy(baseTarget);
  controls.update();
}

function addArrow(origin, direction, length, colour, label) {
  const arrow = new THREE.ArrowHelper(
    direction.clone().normalize(),
    origin,
    length,
    colour,
    Math.min(length * 0.22, 2),
    Math.min(length * 0.1, 1)
  );
  arrow.name = label;
  overlayGroup.add(arrow);
}

function addOverlay(version) {
  overlayGroup.clear();
  if (version.overlay === 'loads') {
    addArrow(new THREE.Vector3(22, 0, 0), new THREE.Vector3(-1, 0, 0), 12, 0x66c9ff, 'Docking compression');
    addArrow(new THREE.Vector3(-20, 0, 0), new THREE.Vector3(1, 0, 0), 15, 0xa7ffd0, 'Propulsion thrust');
    addArrow(new THREE.Vector3(0, 11, 0), new THREE.Vector3(0, 0, 1), 8, 0xffb36c, 'Ring braking');
  } else if (version.overlay === 'optimised') {
    const material = new THREE.LineBasicMaterial({ color: 0xa7ffd0, transparent: true, opacity: 0.85 });
    const points = [];
    for (let index = 0; index < 80; index += 1) {
      const angle = index / 79 * Math.PI * 2;
      points.push(new THREE.Vector3(0, 13.5 * Math.cos(angle), 13.5 * Math.sin(angle)));
    }
    const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints(points), material);
    line.rotation.y = Math.PI / 2;
    overlayGroup.add(line);
  }
}

async function loadVersion(index, { updateHash = true } = {}) {
  const generation = ++loadGeneration;
  selectedIndex = (index + versions.length) % versions.length;
  const version = versions[selectedIndex];

  if (updateHash && location.hash !== `#${version.id}`) location.hash = version.id;
  status(`Loading ${version.id}…`, 'loading');
  setViewerControlsDisabled(true);
  clearWorld();
  removeViewerFallback();
  activeSubsystem = 'all';
  explodeFactor = 0;
  $('#explode').value = '0';
  $('#clip').value = '1';
  $$('.subsystem').forEach((button) => button.classList.toggle('active', button.dataset.subsystem === 'all'));
  updateVersionUI(version);

  try {
    let root;
    if (version.modelMode === 'procedural') root = createProceduralConcept();
    else if (version.modelMode === 'manufacturing') root = await loadManufacturing(version.models, generation);
    else root = await loadSingle(version.model, generation);

    if (generation !== loadGeneration || !root) return;
    prepareRoot(root, version);
    addOverlay(version);
    status(`${version.id} loaded`);
  } catch (error) {
    if (generation !== loadGeneration) return;
    console.error(error);
    status('Model failed to load', 'error');
    showViewerFallback(
      '3D model unavailable',
      'Check your connection, then run the site through a local HTTP server or GitHub Pages and retry.'
    );
  } finally {
    if (generation === loadGeneration) setViewerControlsDisabled(false);
  }
}

function applyDisplayState({ announce = true } = {}) {
  const patterns = subsystemPatterns[activeSubsystem] || [];
  let selectedCount = 0;

  currentMeshes.forEach((mesh) => {
    const name = mesh.userData.displayName || '';
    const selected = activeSubsystem === 'all' || patterns.some((pattern) => name.includes(pattern));
    if (selected) selectedCount += 1;
    const materials = Array.isArray(mesh.material) ? mesh.material : [mesh.material];

    materials.forEach((material) => {
      const base = material.userData.base || {};
      material.wireframe = wireframe;
      material.transparent = xray || !selected || Boolean(base.transparent);
      material.opacity = xray
        ? selected ? 0.72 : 0.10
        : selected ? (base.opacity ?? 1) : 0.08;
      if (material.color && base.color) material.color.copy(base.color);
      if (material.emissive && base.emissive) material.emissive.copy(base.emissive);
      if (selected && activeSubsystem !== 'all' && material.emissive) material.emissive.setHex(0x0d4a61);
      material.needsUpdate = true;
    });

    const basePosition = mesh.userData.basePosition || new THREE.Vector3();
    const explodeVector = mesh.userData.explodeVector || new THREE.Vector3();
    mesh.position.copy(basePosition).addScaledVector(explodeVector, explodeFactor);
  });

  const maxX = Math.max(currentSize.x / 2, 1);
  clippingPlane.constant = Number($('#clip').value) * maxX;

  if (announce && activeSubsystem !== 'all') {
    status(selectedCount
      ? `${selectedCount} ${activeSubsystem} object${selectedCount === 1 ? '' : 's'} highlighted`
      : `No named ${activeSubsystem} objects in this model`,
    selectedCount ? 'ready' : 'error');
  }
}

function safeText(value) {
  return String(value ?? '');
}

function progressHTML(label, value, suffix) {
  const numericValue = Number(value);
  const width = Math.min(Math.max(Number.isFinite(numericValue) ? numericValue : 0, 0), 100);
  return `<div class="progress-row"><div class="progress-label"><span>${safeText(label)}</span><b>${safeText(value)}${safeText(suffix)}</b></div><div class="progress-track" role="progressbar" aria-label="${safeText(label)}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${width}"><div class="progress-fill" style="width:${width}%"></div></div></div>`;
}

function updateVersionUI(version) {
  $$('.version-button').forEach((button, index) => {
    const active = index === selectedIndex;
    button.classList.toggle('active', active);
    button.setAttribute('aria-current', active ? 'step' : 'false');
  });

  $('#detail-version').textContent = version.id;
  $('#detail-phase').textContent = version.phase;
  $('#detail-title').textContent = version.title;
  $('#detail-summary').textContent = version.summary;
  $('#detail-status').textContent = version.status;
  $('#skills').replaceChildren(...version.skills.map((skill) => {
    const item = document.createElement('span');
    item.textContent = skill;
    return item;
  }));

  $('#version-metrics').replaceChildren(...version.metrics.map(([label, value, note]) => {
    const item = document.createElement('div');
    item.className = 'version-metric';
    const labelElement = document.createElement('span');
    labelElement.textContent = label;
    const valueElement = document.createElement('b');
    valueElement.textContent = value;
    const noteElement = document.createElement('small');
    noteElement.textContent = note;
    item.append(labelElement, valueElement, noteElement);
    return item;
  }));

  $('#results-title').textContent = `${version.id} — ${version.title}`;
  $('#results-intro').textContent = version.summary;
  const disciplines = [
    ['CAD', version.progress.cad],
    ['CAE', version.progress.cae],
    ['CAM', version.progress.cam],
    ['Documentation', version.progress.docs]
  ];
  $('#discipline-progress').innerHTML = disciplines.map(([label, value]) => progressHTML(label, value, '%')).join('');
  $('#stage-results').innerHTML = version.results.map((result) => progressHTML(result.label, result.value, result.suffix)).join('');

  $('#engineering-notes').replaceChildren(...version.notes.map((note) => {
    const item = document.createElement('li');
    item.textContent = note;
    return item;
  }));

  const gallery = $('#gallery');
  gallery.replaceChildren();
  if (version.gallery.length) {
    version.gallery.forEach((source, index) => {
      const figure = document.createElement('figure');
      const image = document.createElement('img');
      image.src = source;
      image.alt = `${version.id} engineering evidence ${index + 1}`;
      image.loading = 'lazy';
      image.decoding = 'async';
      const caption = document.createElement('figcaption');
      caption.textContent = `${version.title} evidence ${index + 1}`;
      figure.append(image, caption);
      gallery.append(figure);
    });
  } else {
    const empty = document.createElement('p');
    empty.className = 'empty-state';
    empty.textContent = 'This phase is represented by the live procedural 3D concept and its requirements data.';
    gallery.append(empty);
  }

  const deliverables = $('#version-deliverables');
  deliverables.replaceChildren();
  const label = document.createElement('strong');
  label.textContent = `${version.id} resources:`;
  deliverables.append(label);
  version.deliverables.forEach(([text, href]) => {
    const link = document.createElement('a');
    link.href = href;
    link.textContent = text;
    deliverables.append(link);
  });
}

function buildVersionList() {
  const list = $('#version-list');
  list.replaceChildren(...versions.map((version, index) => {
    const button = document.createElement('button');
    button.className = 'version-button';
    button.type = 'button';
    button.dataset.index = String(index);
    button.setAttribute('aria-label', `Open version ${version.label}: ${version.title}`);

    const number = document.createElement('span');
    number.className = 'number';
    number.textContent = version.label;
    const text = document.createElement('span');
    const title = document.createElement('b');
    title.textContent = version.title;
    const phase = document.createElement('small');
    phase.textContent = version.phase;
    text.append(title, phase);
    button.append(number, text);
    button.addEventListener('click', () => loadVersion(index));
    return button;
  }));
}

function togglePressed(button, value) {
  button.classList.toggle('active', value);
  button.setAttribute('aria-pressed', String(value));
}

function getInitialTheme() {
  try {
    const saved = localStorage.getItem('asterion-theme');
    if (saved === 'light' || saved === 'dark') return saved;
  } catch {
    // Storage may be unavailable in privacy-restricted contexts.
  }
  return window.matchMedia?.('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
}

function setTheme(theme) {
  document.documentElement.dataset.theme = theme;
  const button = $('#theme-toggle');
  const next = theme === 'light' ? 'dark' : 'light';
  button.textContent = theme === 'light' ? '☾' : '☀';
  button.setAttribute('aria-label', `Switch to ${next} theme`);
  button.title = `Switch to ${next} theme`;
  try {
    localStorage.setItem('asterion-theme', theme);
  } catch {
    // Ignore storage failures.
  }
}

$('#reset-view').addEventListener('click', resetView);
$('#fit-view').addEventListener('click', fitView);
$('#auto-rotate').addEventListener('click', (event) => {
  autoRotate = !autoRotate;
  togglePressed(event.currentTarget, autoRotate);
});
$('#wireframe').addEventListener('click', (event) => {
  wireframe = !wireframe;
  togglePressed(event.currentTarget, wireframe);
  applyDisplayState({ announce: false });
});
$('#xray').addEventListener('click', (event) => {
  xray = !xray;
  togglePressed(event.currentTarget, xray);
  applyDisplayState({ announce: false });
});
$('#explode').addEventListener('input', (event) => {
  explodeFactor = Number(event.target.value);
  applyDisplayState({ announce: false });
});
$('#clip').addEventListener('input', () => applyDisplayState({ announce: false }));
$('#capture').addEventListener('click', () => {
  try {
    renderer.render(scene, camera);
    const anchor = document.createElement('a');
    anchor.download = `asterion-${versions[selectedIndex].id}-snapshot.png`;
    anchor.href = renderer.domElement.toDataURL('image/png');
    document.body.append(anchor);
    anchor.click();
    anchor.remove();
    status('Snapshot saved');
  } catch (error) {
    console.error(error);
    status('Snapshot could not be created', 'error');
  }
});
$('#previous-version').addEventListener('click', () => loadVersion(selectedIndex - 1));
$('#next-version').addEventListener('click', () => loadVersion(selectedIndex + 1));
$$('.subsystem').forEach((button) => button.addEventListener('click', () => {
  activeSubsystem = button.dataset.subsystem;
  $$('.subsystem').forEach((item) => item.classList.toggle('active', item === button));
  applyDisplayState();
}));
$('#theme-toggle').addEventListener('click', () => {
  const nextTheme = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
  setTheme(nextTheme);
});

window.addEventListener('keydown', (event) => {
  if (event.target.matches('input, button, a, select, textarea')) return;
  const key = event.key.toLowerCase();
  if (key === 'r') resetView();
  if (key === 'w') $('#wireframe').click();
  if (key === 'a') $('#auto-rotate').click();
});

window.addEventListener('hashchange', () => {
  const index = versions.findIndex((version) => location.hash === `#${version.id}`);
  if (index >= 0 && index !== selectedIndex) loadVersion(index, { updateHash: false });
});

function resize() {
  const width = Math.max(viewer.clientWidth, 1);
  const height = Math.max(viewer.clientHeight, 1);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  renderer.setSize(width, height, false);
}
new ResizeObserver(resize).observe(viewer);

const clock = new THREE.Clock();
function animate(now) {
  requestAnimationFrame(animate);
  const delta = Math.min(clock.getDelta(), 0.1);
  controls.update(delta);
  if (currentRoot && autoRotate && !document.hidden) currentRoot.rotation.y += delta * 0.072;
  stars.rotation.x += delta * 0.0012;
  renderer.render(scene, camera);

  fpsCounter += 1;
  if (now - fpsTime > 700) {
    const fps = Math.round(fpsCounter * 1000 / (now - fpsTime));
    fpsCounter = 0;
    fpsTime = now;
    $('#hud-fps').textContent = String(fps);
  }
}
requestAnimationFrame(animate);

if ('serviceWorker' in navigator && ['http:', 'https:'].includes(location.protocol)) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js').catch((error) => console.warn('Service worker registration failed', error));
  });
}

setTheme(getInitialTheme());
togglePressed($('#auto-rotate'), autoRotate);
buildVersionList();
loadVersion(selectedIndex, { updateHash: false });
window.__ASTERION_APP_READY__ = true;
window.dispatchEvent(new CustomEvent('asterion-ready'));
