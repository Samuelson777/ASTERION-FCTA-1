import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.164.1/build/three.module.js";
import { OrbitControls } from "https://cdn.jsdelivr.net/npm/three@0.164.1/examples/jsm/controls/OrbitControls.js";
import { GLTFLoader } from "https://cdn.jsdelivr.net/npm/three@0.164.1/examples/jsm/loaders/GLTFLoader.js";

const canvas = document.querySelector("#viewer");
const status = document.querySelector("#status");
const renderer = new THREE.WebGLRenderer({canvas, antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0b1020);
const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 200000);
camera.position.set(48000, 41000, 36000);
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.target.set(0, 0, 0);
scene.add(new THREE.HemisphereLight(0xffffff, 0x29324c, 2.2));
const key = new THREE.DirectionalLight(0xffffff, 2.5); key.position.set(30000,30000,50000); scene.add(key);
const grid = new THREE.GridHelper(80000, 40, 0x334155, 0x1e293b); grid.rotation.z = Math.PI/2; scene.add(grid);

new GLTFLoader().load("models/asterion_v0_8_optimized_structure.glb", gltf => {
  scene.add(gltf.scene);
  status.textContent = "Drag to orbit · scroll to zoom · right-drag to pan";
}, undefined, err => {
  console.error(err); status.textContent = "Model failed to load. Serve this folder through a local web server.";
});

function resize(){
  const w=canvas.clientWidth, h=canvas.clientHeight;
  if(canvas.width!==w || canvas.height!==h){renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();}
}
function animate(){resize();controls.update();renderer.render(scene,camera);requestAnimationFrame(animate)}
animate();
