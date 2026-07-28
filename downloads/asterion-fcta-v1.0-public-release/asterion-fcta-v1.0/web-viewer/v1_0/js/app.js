import * as THREE from 'https://unpkg.com/three@0.161.0/build/three.module.js';
import { OrbitControls } from 'https://unpkg.com/three@0.161.0/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'https://unpkg.com/three@0.161.0/examples/jsm/loaders/GLTFLoader.js';

const viewer = document.getElementById('viewer');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x07101c);
const camera = new THREE.PerspectiveCamera(42, viewer.clientWidth / viewer.clientHeight, 0.01, 2000);
camera.position.set(58, 34, 58);
const renderer = new THREE.WebGLRenderer({antialias:true, alpha:true});
renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
renderer.setSize(viewer.clientWidth,viewer.clientHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
viewer.replaceChildren(renderer.domElement);
const controls = new OrbitControls(camera,renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.055;
scene.add(new THREE.HemisphereLight(0xeaf6ff,0x1a2434,2.2));
const key = new THREE.DirectionalLight(0xffffff,3.0); key.position.set(32,55,38); scene.add(key);
const rim = new THREE.DirectionalLight(0x72c9ff,2.0); rim.position.set(-35,15,-28); scene.add(rim);
const loader = new GLTFLoader();
let current = null;
let rotate = true;

function frameModel(object){
  const box = new THREE.Box3().setFromObject(object);
  const center = box.getCenter(new THREE.Vector3());
  const size = box.getSize(new THREE.Vector3());
  object.position.sub(center);
  const maxDim = Math.max(size.x,size.y,size.z) || 1;
  const distance = maxDim / (2 * Math.tan(THREE.MathUtils.degToRad(camera.fov/2)));
  camera.position.set(distance*.9,distance*.55,distance*.9);
  camera.near = Math.max(maxDim/1000,.01); camera.far = maxDim*30;
  camera.updateProjectionMatrix(); controls.target.set(0,0,0); controls.update();
}
function loadModel(path,button){
  document.querySelectorAll('[data-model]').forEach(b=>b.classList.remove('active'));
  if(button) button.classList.add('active');
  loader.load(path,(gltf)=>{
    if(current){scene.remove(current); current.traverse(o=>{if(o.geometry)o.geometry.dispose();});}
    current=gltf.scene; scene.add(current); frameModel(current);
  },undefined,(error)=>{console.error(error); viewer.insertAdjacentHTML('beforeend','<p class="loading">Model could not be loaded. Serve this folder through a local HTTP server.</p>');});
}
document.querySelectorAll('[data-model]').forEach(btn=>btn.addEventListener('click',()=>loadModel(btn.dataset.model,btn)));
renderer.domElement.addEventListener('pointerdown',()=>{rotate=false;});
function resize(){const w=viewer.clientWidth,h=viewer.clientHeight;camera.aspect=w/h;camera.updateProjectionMatrix();renderer.setSize(w,h);}window.addEventListener('resize',resize);
function animate(){requestAnimationFrame(animate);controls.update();if(current&&rotate)current.rotation.y+=.0012;renderer.render(scene,camera);}animate();
loadModel('assets/asterion_full_assembly.glb',document.querySelector('[data-model]'));
