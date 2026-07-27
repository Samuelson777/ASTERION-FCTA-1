from __future__ import annotations

from pathlib import Path
import json
import mimetypes
import sys

ROOT = Path(__file__).resolve().parents[1]

THREE_STUB = r'''
export const SRGBColorSpace='srgb';
export const ACESFilmicToneMapping='aces';
export class Vector3{constructor(x=0,y=0,z=0){this.x=x;this.y=y;this.z=z}set(x,y,z){this.x=x;this.y=y;this.z=z;return this}setScalar(v){this.x=this.y=this.z=v;return this}clone(){return new Vector3(this.x,this.y,this.z)}copy(v){this.x=v.x;this.y=v.y;this.z=v.z;return this}sub(v){this.x-=v.x;this.y-=v.y;this.z-=v.z;return this}add(v){this.x+=v.x;this.y+=v.y;this.z+=v.z;return this}addScaledVector(v,s){this.x+=v.x*s;this.y+=v.y*s;this.z+=v.z*s;return this}multiplyScalar(s){this.x*=s;this.y*=s;this.z*=s;return this}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z}length(){return Math.sqrt(this.lengthSq())}normalize(){const l=this.length()||1;return this.multiplyScalar(1/l)}}
export class Color{constructor(v=0){this.value=v}clone(){return new Color(this.value)}copy(v){this.value=v.value;return this}setHex(v){this.value=v;return this}}
class Euler{constructor(){this.x=0;this.y=0;this.z=0}}
class Scale extends Vector3{constructor(){super(1,1,1)}}
export class Object3D{constructor(){this.children=[];this.parent=null;this.position=new Vector3();this.rotation=new Euler();this.scale=new Scale();this.userData={};this.name=''}add(...items){for(const item of items){if(!item)continue;item.parent=this;this.children.push(item)}return this}remove(item){this.children=this.children.filter(x=>x!==item);item.parent=null;return this}clear(){for(const c of this.children)c.parent=null;this.children=[]}traverse(fn){fn(this);for(const child of this.children)child.traverse?child.traverse(fn):fn(child)}updateMatrixWorld(){}worldToLocal(v){return v}}
export class Group extends Object3D{}
export class Scene extends Group{constructor(){super();this.background=null;this.fog=null;this.environment=null}}
export class PerspectiveCamera extends Object3D{constructor(fov=42,aspect=1,near=.01,far=3000){super();this.fov=fov;this.aspect=aspect;this.near=near;this.far=far}updateProjectionMatrix(){}}
export class FogExp2{constructor(color,density){this.color=color;this.density=density}}
export class Material{constructor(opts={}){Object.assign(this,opts);this.opacity=opts.opacity??1;this.transparent=!!opts.transparent;this.wireframe=!!opts.wireframe;this.color=new Color(opts.color??0);this.emissive=new Color(opts.emissive??0);this.userData={}}clone(){const m=new this.constructor();Object.assign(m,this);m.color=this.color.clone();m.emissive=this.emissive.clone();m.userData={...this.userData};return m}dispose(){}}
export class MeshStandardMaterial extends Material{}
export class PointsMaterial extends Material{}
export class LineBasicMaterial extends Material{}
export class BufferGeometry{constructor(){this.userData={}}setAttribute(){return this}setFromPoints(){return this}dispose(){}}
export class Float32BufferAttribute{constructor(array,size){this.array=array;this.itemSize=size}}
for(const name of ['CylinderGeometry','TorusGeometry','BoxGeometry','ConeGeometry']){globalThis[name]=class extends BufferGeometry{constructor(...args){super();this.args=args}}}
export const CylinderGeometry=globalThis.CylinderGeometry;
export const TorusGeometry=globalThis.TorusGeometry;
export const BoxGeometry=globalThis.BoxGeometry;
export const ConeGeometry=globalThis.ConeGeometry;
export class Mesh extends Object3D{constructor(geometry=new BufferGeometry(),material=new Material()){super();this.geometry=geometry;this.material=material;this.isMesh=true}}
export class Points extends Object3D{constructor(geometry,material){super();this.geometry=geometry;this.material=material}}
export class Line extends Object3D{constructor(geometry,material){super();this.geometry=geometry;this.material=material}}
export class HemisphereLight extends Object3D{constructor(){super()}}
export class DirectionalLight extends Object3D{constructor(){super()}}
export class GridHelper extends Object3D{constructor(){super();this.material=new Material()}}
export class ArrowHelper extends Object3D{constructor(){super()}}
export class Plane{constructor(normal,constant){this.normal=normal;this.constant=constant}}
export class Box3{constructor(){this.min=new Vector3(-20,-10,-5);this.max=new Vector3(20,10,5)}setFromObject(object){const b=object?.userData?.bounds;if(b){this.min=new Vector3(...b[0]);this.max=new Vector3(...b[1])}else{this.min=new Vector3(-20,-10,-5);this.max=new Vector3(20,10,5)}return this}getSize(target){return target.set(this.max.x-this.min.x,this.max.y-this.min.y,this.max.z-this.min.z)}getCenter(target){return target.set((this.max.x+this.min.x)/2,(this.max.y+this.min.y)/2,(this.max.z+this.min.z)/2)}}
export class PMREMGenerator{constructor(){}fromScene(){return {texture:{}}}dispose(){}}
export class WebGLRenderer{constructor(){this.domElement=document.createElement('canvas');this.localClippingEnabled=false}setPixelRatio(){}setSize(w,h){this.domElement.width=w;this.domElement.height=h}render(){}dispose(){}}
export class Clock{constructor(){this.last=performance.now()}getDelta(){const n=performance.now();const d=(n-this.last)/1000;this.last=n;return d}}
export const MathUtils={degToRad:(d)=>d*Math.PI/180};
'''

ORBIT_STUB = r'''
import {Vector3} from 'three';
export class OrbitControls{constructor(camera,element){this.camera=camera;this.element=element;this.target=new Vector3();this.enableDamping=false;this.dampingFactor=0;this.screenSpacePanning=false;this.zoomToCursor=false}update(){}}
'''

ROOM_STUB = r'''
import {Group} from 'three';
export class RoomEnvironment extends Group{}
'''

GLTF_STUB = r'''
import {Group,Mesh,BoxGeometry,MeshStandardMaterial} from 'three';
export class GLTFLoader{load(path,onLoad,onProgress,onError){const delay=path.includes('v0.2')?180:path.includes('v0.8')?15:30;setTimeout(()=>{try{onProgress?.({loaded:1,total:1});const root=new Group();root.name=path;const mesh=new Mesh(new BoxGeometry(40,20,10),new MeshStandardMaterial({color:0x66c9ff}));mesh.name=path.toUpperCase();root.add(mesh);root.userData.bounds=path.includes('v0.4')?[[-29000,-29000,-22000],[29000,29000,29400]]:[[-21000,-12000,-12000],[21000,12000,12000]];onLoad({scene:root})}catch(e){onError?.(e)}},delay)}}
'''


def content_type(path: Path) -> str:
    custom = {
        '.js': 'text/javascript', '.glb': 'model/gltf-binary', '.webmanifest': 'application/manifest+json',
        '.svg': 'image/svg+xml', '.md': 'text/markdown', '.zip': 'application/zip',
        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    }
    return custom.get(path.suffix.lower(), mimetypes.guess_type(path.name)[0] or 'application/octet-stream')


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(json.dumps({'status': 'SKIP', 'reason': 'playwright is not installed'}, indent=2))
        return 0

    errors: list[str] = []
    console_errors: list[str] = []
    index = (ROOT / 'index.html').read_text(encoding='utf-8')
    index = index.replace('<head>', '<head><base href="https://asterion.test/"><script>HTMLCanvasElement.prototype.getContext=function(){return {};};</script>', 1)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 1440, 'height': 1000}, accept_downloads=True)
        page.on('pageerror', lambda exc: errors.append(str(exc)))
        page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)

        def local_route(route):
            url = route.request.url
            relative = url.split('https://asterion.test/', 1)[1].split('?', 1)[0].split('#', 1)[0]
            relative = relative or 'index.html'
            path = (ROOT / relative).resolve()
            try:
                path.relative_to(ROOT.resolve())
            except ValueError:
                route.fulfill(status=403, body='forbidden')
                return
            if path.is_dir():
                path = path / 'index.html'
            if not path.exists():
                route.fulfill(status=404, body='not found')
                return
            route.fulfill(status=200, body=path.read_bytes(), content_type=content_type(path))

        page.route('https://asterion.test/**', local_route)
        page.route('https://cdn.jsdelivr.net/npm/three@0.185.1/build/three.module.js', lambda route: route.fulfill(status=200, body=THREE_STUB, content_type='text/javascript'))
        page.route('https://cdn.jsdelivr.net/npm/three@0.185.1/examples/jsm/controls/OrbitControls.js', lambda route: route.fulfill(status=200, body=ORBIT_STUB, content_type='text/javascript'))
        page.route('https://cdn.jsdelivr.net/npm/three@0.185.1/examples/jsm/loaders/GLTFLoader.js', lambda route: route.fulfill(status=200, body=GLTF_STUB, content_type='text/javascript'))
        page.route('https://cdn.jsdelivr.net/npm/three@0.185.1/examples/jsm/environments/RoomEnvironment.js', lambda route: route.fulfill(status=200, body=ROOM_STUB, content_type='text/javascript'))

        page.set_content(index, wait_until='load')
        page.wait_for_function('window.__ASTERION_APP_READY__ === true', timeout=20000)
        page.wait_for_function("document.querySelector('#load-status b').textContent.includes('loaded')", timeout=20000)

        assert page.locator('.version-button').count() == 10
        assert page.locator('canvas').count() == 1
        assert page.locator('#detail-version').inner_text() == 'v1.0'
        assert page.locator('#hud-size').inner_text().endswith('m')

        page.locator('.version-button').nth(1).click()
        page.locator('.version-button').nth(7).click()
        page.wait_for_function("document.querySelector('#detail-version').textContent === 'v0.8'", timeout=20000)
        page.wait_for_timeout(250)
        assert page.locator('#detail-version').inner_text() == 'v0.8'

        page.locator('#wireframe').click()
        assert page.locator('#wireframe').get_attribute('aria-pressed') == 'true'
        page.locator('#xray').click()
        assert page.locator('#xray').get_attribute('aria-pressed') == 'true'
        page.locator('.subsystem[data-subsystem="structure"]').click()
        assert page.locator('.subsystem.active').inner_text() == 'Structure'

        previous_theme = page.locator('html').get_attribute('data-theme')
        page.locator('#theme-toggle').click()
        assert page.locator('html').get_attribute('data-theme') != previous_theme

        page.locator('.version-button').nth(6).click()
        page.wait_for_function("document.querySelector('#detail-version').textContent === 'v0.7'", timeout=20000)
        page.wait_for_function("document.querySelector('#load-status b').textContent.includes('loaded')", timeout=20000)
        assert page.locator('#hud-size').inner_text() == 'Normalised part layout'

        try:
            with page.expect_download(timeout=5000) as download_info:
                page.locator('#capture').click()
            assert download_info.value.suggested_filename == 'asterion-v0.7-snapshot.png'
        except Exception as exc:
            errors.append(f'snapshot contract failed: {exc}')

        page.set_viewport_size({'width': 390, 'height': 844})
        page.wait_for_timeout(100)
        overflow = page.evaluate('document.documentElement.scrollWidth - window.innerWidth')
        if overflow > 2:
            errors.append(f'mobile layout has {overflow}px horizontal overflow')

        failure_page = browser.new_page(viewport={'width': 800, 'height': 600})
        failure_page.route('https://asterion.test/**', local_route)
        failure_index = (ROOT / 'index.html').read_text(encoding='utf-8').replace('<head>', '<head><base href="https://asterion.test/">', 1)
        failure_page.set_content(failure_index, wait_until='load')
        failure_page.wait_for_function("document.querySelector('#load-status b').textContent.includes('WebGL')", timeout=10000)
        if failure_page.locator('.viewer-fallback-error').count() != 1:
            errors.append('WebGL startup failure did not produce one recovery panel')
        failure_page.close()

        browser.close()

    report = {
        'status': 'FAIL' if errors or console_errors else 'PASS',
        'page_errors': errors,
        'console_errors': console_errors,
        'checks': 15
    }
    print(json.dumps(report, indent=2))
    return 1 if report['status'] == 'FAIL' else 0


if __name__ == '__main__':
    sys.exit(main())
