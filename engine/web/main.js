// OUTRA REALIDADE — motor de "placas" 3D toon (three.js r160)
// Mundo 3D com texturas pintadas, contorno de tinta (ink) e exportação de cor + profundidade.
// Uso (via Playwright): await window.ready; await window.renderPlate(spec) -> {color, depth, cam}
import * as THREE from 'three';
import { SETS } from './sets.js';

const renderer = new THREE.WebGLRenderer({ antialias: false, preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
document.body.appendChild(renderer.domElement);

// gradient map de 3 tons (toon)
const gdata = new Uint8Array([90, 90, 90, 255, 175, 175, 175, 255, 255, 255, 255, 255]);
export const GRAD = new THREE.DataTexture(gdata, 3, 1, THREE.RGBAFormat);
GRAD.minFilter = THREE.NearestFilter; GRAD.magFilter = THREE.NearestFilter; GRAD.needsUpdate = true;

export const LIGHTS = {
  //            sky top     sky bottom   key color  key int  az   el   hemi sky   hemi ground  hemi int  amb  fog
  night:    { top: '#0d1240', bot: '#3a2c6e', key: '#9fb4ff', ki: 1.1, az: 140, el: 40, hs: '#5f6fd0', hg: '#2a2140', hi: 1.3, fog: '#2c2560', stars: 1, exp: 1.0 },
  dawn:     { top: '#4a6fc0', bot: '#ffb48a', key: '#ffc890', ki: 2.4, az: 80, el: 12, hs: '#a8c0ff', hg: '#6a4a50', hi: 1.2, fog: '#e8a890', stars: 0, exp: 1.0 },
  day:      { top: '#3d8fe8', bot: '#bfe3ff', key: '#fff1d8', ki: 2.8, az: 140, el: 50, hs: '#cfe6ff', hg: '#9a8a6a', hi: 1.4, fog: '#bfe0ff', stars: 0, exp: 1.0 },
  golden:   { top: '#5a5cb0', bot: '#ffb070', key: '#ffb060', ki: 2.8, az: 250, el: 14, hs: '#ffd0a0', hg: '#5a3a4a', hi: 1.1, fog: '#f0a070', stars: 0, exp: 1.0 },
  overcast: { top: '#7d889c', bot: '#c9ced8', key: '#e4e8f0', ki: 1.4, az: 160, el: 60, hs: '#d8deea', hg: '#7a7a86', hi: 1.6, fog: '#c4c9d4', stars: 0, exp: 1.0 },
  storm:    { top: '#262c3e', bot: '#59607a', key: '#aab4d0', ki: 1.2, az: 200, el: 45, hs: '#7a84a0', hg: '#2c2c38', hi: 1.3, fog: '#4a5068', stars: 0, exp: 1.0 },
  space:    { top: '#05061a', bot: '#120d30', key: '#fff4e0', ki: 3.2, az: 60, el: 20, hs: '#3a3a80', hg: '#101030', hi: 0.5, fog: '#000000', stars: 2, exp: 1.0 },
  interior: { top: '#0d1240', bot: '#3a2c6e', key: '#ffd8a0', ki: 1.6, az: 120, el: 55, hs: '#ffe2c0', hg: '#6a5060', hi: 1.3, fog: '#3a2c50', stars: 1, exp: 1.0 },
  interior_day: { top: '#3d8fe8', bot: '#bfe3ff', key: '#fff1d8', ki: 2.0, az: 120, el: 55, hs: '#fff4e0', hg: '#8a7a70', hi: 1.5, fog: '#d0d8e8', stars: 0, exp: 1.0 },
};

// ----------------------------------------------------------- render targets / passes
let W = 1920, H = 1080;
function makeRT(w, h, type = THREE.HalfFloatType, samples = 0) {
  const rt = new THREE.WebGLRenderTarget(w, h, { type, samples, depthBuffer: true });
  rt.texture.minFilter = THREE.LinearFilter; rt.texture.magFilter = THREE.LinearFilter;
  return rt;
}
let rtColor, rtND;
const ndMat = new THREE.ShaderMaterial({
  vertexShader: `varying vec3 vN; varying float vZ;
    void main(){ vec4 mv = modelViewMatrix*vec4(position,1.0); vN = normalize(normalMatrix*normal); vZ = -mv.z; gl_Position = projectionMatrix*mv; }`,
  fragmentShader: `varying vec3 vN; varying float vZ; uniform float isCard;
    void main(){ gl_FragColor = vec4(normalize(vN)*0.5+0.5, vZ); }`,
  uniforms: { isCard: { value: 0 } }, side: THREE.DoubleSide,
});
const postScene = new THREE.Scene();
const postCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
const postMat = new THREE.ShaderMaterial({
  uniforms: { tC: { value: null }, tND: { value: null }, px: { value: new THREE.Vector2() }, ink: { value: 2.6 },
    inkCol: { value: new THREE.Color('#1a1024') }, sat: { value: 1.18 }, vig: { value: 0.28 }, mode: { value: 0 }, far: { value: 600 }, inkFar: { value: 420 } },
  vertexShader: `varying vec2 vUv; void main(){ vUv=uv; gl_Position=vec4(position.xy,0.,1.); }`,
  fragmentShader: `uniform sampler2D tC; uniform sampler2D tND; uniform vec2 px; uniform float ink; uniform vec3 inkCol;
    uniform float sat; uniform float vig; uniform int mode; uniform float far; uniform float inkFar; varying vec2 vUv;
    vec4 nd(vec2 o){ return texture2D(tND, vUv + o*px*ink); }
    void main(){
      vec4 c0 = nd(vec2(0.));
      if(mode==1){ float d = clamp(c0.a/far,0.,1.); if(c0.a<=0.0) d=1.0; vec3 e = vec3(floor(d*255.)/255., fract(d*255.), fract(d*65025.)); gl_FragColor=vec4(e,1.); return; }
      vec3 col = pow(max(texture2D(tC, vUv).rgb,0.0), vec3(1.0/2.2));
      float edge = 0.0;
      vec2 offs[4]; offs[0]=vec2(1.,0.); offs[1]=vec2(-1.,0.); offs[2]=vec2(0.,1.); offs[3]=vec2(0.,-1.);
      for(int i=0;i<4;i++){
        vec4 s = nd(offs[i]);
        if(c0.a<=0.0 && s.a<=0.0) continue;
        float z0 = c0.a<=0.0 ? 1e4 : c0.a; float z1 = s.a<=0.0 ? 1e4 : s.a;
        float dz = (z1 - z0)/max(z0,0.01);
        if(dz > 0.06 && z0 < inkFar) edge = max(edge, 1.0);          // lado de perto do salto de profundidade
        float nd_ = dot(normalize(c0.rgb*2.-1.), normalize(s.rgb*2.-1.));
        if(c0.a>0.0 && s.a>0.0 && nd_ < 0.82 && z0 < inkFar) edge = max(edge, 0.85); // vincos
      }
      float fade = 1.0 - smoothstep(inkFar*0.35, inkFar, c0.a<=0.0?1e4:c0.a);
      col = mix(col, inkCol, edge*fade*0.92);
      float l = dot(col, vec3(0.299,0.587,0.114)); col = mix(vec3(l), col, sat);
      vec2 q = vUv-0.5; col *= 1.0 - vig*dot(q,q)*2.0;
      gl_FragColor = vec4(col,1.);
    }`,
});
postScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), postMat));

// ----------------------------------------------------------- sky
function skyDome(L) {
  const g = new THREE.SphereGeometry(900, 32, 16);
  const m = new THREE.ShaderMaterial({ side: THREE.BackSide, depthWrite: false, fog: false,
    uniforms: { top: { value: new THREE.Color(L.top) }, bot: { value: new THREE.Color(L.bot) } },
    vertexShader: `varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
    fragmentShader: `uniform vec3 top; uniform vec3 bot; varying vec3 vP; void main(){ float t = clamp(vP.y*1.6+0.08,0.,1.); gl_FragColor = vec4(mix(bot,top,pow(t,0.8)),1.); }` });
  const s = new THREE.Mesh(g, m); s.userData.sky = true; s.renderOrder = -10; return s;
}
function stars(n, r = 850) {
  const g = new THREE.BufferGeometry(); const p = []; let seed = 7;
  const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  for (let i = 0; i < n; i++) { const u = rnd() * 2 - 1, th = rnd() * Math.PI * 2; const y = Math.abs(u) * 0.95 + 0.03; const rr = Math.sqrt(1 - y * y);
    p.push(Math.cos(th) * rr * r, y * r, Math.sin(th) * rr * r); }
  g.setAttribute('position', new THREE.Float32BufferAttribute(p, 3));
  const pts = new THREE.Points(g, new THREE.PointsMaterial({ color: 0xfff6dd, size: 2.2, sizeAttenuation: false, fog: false }));
  pts.userData.sky = true; return pts;
}

// ----------------------------------------------------------- plate render
const cache = {};
window.renderPlate = async (spec) => {
  W = spec.w; H = spec.h;
  renderer.setSize(W, H, false);
  if (!rtColor || rtColor.width !== W) { rtColor = makeRT(W, H, THREE.HalfFloatType, 4); rtND = makeRT(W, H, THREE.FloatType, 0); }
  const L = Object.assign({}, LIGHTS[spec.light || 'day'], spec.lightOverride || {});
  const scene = new THREE.Scene();
  scene.fog = new THREE.Fog(spec.fogColor || L.bot, spec.fogNear ?? 120, spec.fogFar ?? 700);
  scene.add(skyDome(L));
  if (L.stars) scene.add(stars(L.stars > 1 ? 2600 : 1400));
  const hemi = new THREE.HemisphereLight(L.hs, L.hg, L.hi); scene.add(hemi);
  const key = new THREE.DirectionalLight(L.key, L.ki);
  const az = THREE.MathUtils.degToRad(L.az), el = THREE.MathUtils.degToRad(L.el);
  const tgt = new THREE.Vector3(...(spec.cam.look));
  key.position.set(tgt.x + Math.cos(az) * Math.cos(el) * 120, tgt.y + Math.sin(el) * 120, tgt.z + Math.sin(az) * Math.cos(el) * 120);
  key.target.position.copy(tgt); scene.add(key.target);
  key.castShadow = true; key.shadow.mapSize.set(2048, 2048);
  const sc = key.shadow.camera; const R = spec.shadowR ?? 40; sc.left = -R; sc.right = R; sc.top = R; sc.bottom = -R; sc.near = 1; sc.far = 400;
  key.shadow.bias = -0.0005; key.shadow.normalBias = 0.04;
  scene.add(key);
  const world = SETS[spec.set](spec.opts || {}, L);
  scene.add(world);
  const cam = new THREE.PerspectiveCamera(spec.cam.fov || 40, W / H, 0.1, 1200);
  cam.position.set(...spec.cam.pos); cam.lookAt(tgt);
  if (spec.cam.roll) cam.rotateZ(THREE.MathUtils.degToRad(spec.cam.roll));
  cam.updateMatrixWorld(); cam.updateProjectionMatrix();
  // 1) cor
  renderer.setRenderTarget(rtColor); renderer.setClearColor(L.fog, 1); renderer.clear(); renderer.render(scene, cam);
  // 2) normal + profundidade (céu fora)
  const hidden = []; scene.traverse(o => { if (o.userData.sky || o.userData.noInk) { if (o.visible) { hidden.push(o); o.visible = false; } } });
  scene.overrideMaterial = ndMat; const fog = scene.fog; scene.fog = null;
  renderer.setRenderTarget(rtND); renderer.setClearColor(0x000000, 0); renderer.clear(); renderer.render(scene, cam);
  scene.overrideMaterial = null; scene.fog = fog; hidden.forEach(o => o.visible = true);
  // 3) final
  postMat.uniforms.tC.value = rtColor.texture; postMat.uniforms.tND.value = rtND.texture;
  postMat.uniforms.px.value.set(1 / W, 1 / H); postMat.uniforms.ink.value = spec.ink ?? Math.max(1.6, W / 820);
  postMat.uniforms.mode.value = 0; renderer.setRenderTarget(null); renderer.render(postScene, postCam);
  const color = renderer.domElement.toDataURL('image/png');
  postMat.uniforms.mode.value = 1; renderer.render(postScene, postCam);
  const depth = renderer.domElement.toDataURL('image/png');
  // matriz pra projetar pontos do mundo no Python
  const P = new THREE.Matrix4().multiplyMatrices(cam.projectionMatrix, cam.matrixWorldInverse);
  world.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material) { (Array.isArray(o.material) ? o.material : [o.material]).forEach(m => { if (m.map) m.map.dispose(); m.dispose(); }); } });
  return { color, depth, P: P.elements, far: 600, w: W, h: H, campos: spec.cam.pos };
};
window.ready = true;
