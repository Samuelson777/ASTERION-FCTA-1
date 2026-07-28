import * as THREE from 'https://unpkg.com/three@0.161.0/build/three.module.js';
import { OrbitControls } from 'https://unpkg.com/three@0.161.0/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'https://unpkg.com/three@0.161.0/examples/jsm/loaders/GLTFLoader.js';

const viewer = document.getElementById('viewer');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x07101c);
const camera = new THREE.PerspectiveCamera(45, viewer.clientWidth / viewer.clientHeight, 0.1, 1000);
camera.position.set(55, 32, 55);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(viewer.clientWidth, viewer.clientHeight);
viewer.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
scene.add(new THREE.HemisphereLight(0xffffff, 0x223344, 2.2));
const key = new THREE.DirectionalLight(0xffffff, 2.5); key.position.set(20, 40, 30); scene.add(key);
const loader = new GLTFLoader();
let current;
function loadModel(path){
  if(current) scene.remove(current);
  loader.load(path, (gltf)=>{
    current = gltf.scene;
    current.rotation.y = Math.PI * 0.12;
    scene.add(current);
    const box = new THREE.Box3().setFromObject(current);
    const center = box.getCenter(new THREE.Vector3());
    current.position.sub(center);
    controls.target.set(0,0,0); controls.update();
  });
}
document.querySelectorAll('[data-model]').forEach(btn => btn.addEventListener('click', () => loadModel(btn.dataset.model)));
loadModel('assets/asterion_full_assembly.glb');
function resize(){ camera.aspect = viewer.clientWidth/viewer.clientHeight; camera.updateProjectionMatrix(); renderer.setSize(viewer.clientWidth, viewer.clientHeight); }
window.addEventListener('resize', resize);
function animate(){ requestAnimationFrame(animate); controls.update(); if(current) current.rotation.y += 0.0015; renderer.render(scene,camera); }
animate();
