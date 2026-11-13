// Cenários 3D do canal (texturas pintadas em canvas + materiais toon).
// Unidades em metros, y pra cima. Cada set recebe opts e o preset de luz L.
import * as THREE from 'three';

const gd = new Uint8Array([95, 95, 95, 255, 178, 178, 178, 255, 255, 255, 255, 255]);
const GRAD = new THREE.DataTexture(gd, 3, 1, THREE.RGBAFormat);
GRAD.minFilter = GRAD.magFilter = THREE.NearestFilter; GRAD.needsUpdate = true;

// ---------------------------------------------------------------- random determinístico
let _s = 1; const srand = (s) => { _s = s; }; const rnd = () => (_s = (_s * 16807) % 2147483647) / 2147483647;
const pick = (a) => a[Math.floor(rnd() * a.length)];

// ---------------------------------------------------------------- texturas pintadas
const TEX = {};
function canvasTex(key, w, h, paint, rx = 1, ry = 1) {
  const k = key + rx + 'x' + ry;
  if (TEX[k]) return TEX[k];
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  const g = c.getContext('2d'); paint(g, w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rx, ry); t.anisotropy = 4;
  TEX[k] = t; return t;
}
function speckle(g, w, h, cols, n, rmin, rmax, seed, am = 1) {
  srand(seed); for (let i = 0; i < n; i++) { g.fillStyle = pick(cols); g.globalAlpha = (0.25 + rnd() * 0.5) * am;
    g.beginPath(); g.ellipse(rnd() * w, rnd() * h, rmin + rnd() * (rmax - rmin), (rmin + rnd() * (rmax - rmin)) * 0.7, rnd() * 3, 0, 7); g.fill(); } g.globalAlpha = 1;
}
const P = {
  sand: (base = '#e8cf98', dark = '#cfae74') => (g, w, h) => { g.fillStyle = base; g.fillRect(0, 0, w, h); speckle(g, w, h, [dark, '#f4e2b8', '#d8bb84'], 900, 2, 9, 3);
    g.strokeStyle = dark; g.globalAlpha = 0.35; g.lineWidth = 3; for (let i = 0; i < 18; i++) { g.beginPath(); const y = rnd() * h; g.moveTo(0, y); for (let x = 0; x < w; x += 32) g.lineTo(x, y + Math.sin(x / 40 + i) * 6); g.stroke(); } g.globalAlpha = 1; },
  water: (a = '#2f7fc4', b = '#4aa3df') => (g, w, h) => { g.fillStyle = a; g.fillRect(0, 0, w, h); srand(5);
    for (let i = 0; i < 140; i++) { g.strokeStyle = rnd() < 0.5 ? b : '#9fd2f5'; g.globalAlpha = 0.5; g.lineWidth = 3 + rnd() * 4; const x = rnd() * w, y = rnd() * h, l = 20 + rnd() * 60;
      g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + l / 2, y - 6, x + l, y); g.stroke(); } g.globalAlpha = 1; },
  plaster: (c, d) => (g, w, h) => { g.fillStyle = c; g.fillRect(0, 0, w, h); speckle(g, w, h, [d, '#ffffff'], 70, 3, 10, 9, 0.35); },
  planks: (c = '#b07a48', d = '#7a4f2c') => (g, w, h) => { const n = 8; for (let i = 0; i < n; i++) { g.fillStyle = i % 2 ? c : shade(c, -10); g.fillRect(0, i * h / n, w, h / n);
    g.fillStyle = d; g.fillRect(0, i * h / n, w, 4); srand(i + 3); for (let k = 0; k < 6; k++) { g.globalAlpha = 0.25; g.fillRect(rnd() * w, i * h / n + 10 + rnd() * (h / n - 20), 40 + rnd() * 120, 3); } g.globalAlpha = 1;
    g.fillRect(((i * 97) % w), i * h / n, 4, h / n); } },
  checker: (a = '#2fb3a7', b = '#f4f1e6', n = 8) => (g, w, h) => { for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) { g.fillStyle = (i + j) % 2 ? a : b; g.fillRect(i * w / n, j * h / n, w / n, h / n); }
    g.strokeStyle = 'rgba(0,0,0,.18)'; g.lineWidth = 3; for (let i = 0; i <= n; i++) { g.beginPath(); g.moveTo(i * w / n, 0); g.lineTo(i * w / n, h); g.stroke(); g.beginPath(); g.moveTo(0, i * h / n); g.lineTo(w, i * h / n); g.stroke(); } },
  stone: (c = '#9a94a0', d = '#6e6878') => (g, w, h) => { g.fillStyle = d; g.fillRect(0, 0, w, h); srand(11); const rows = 6;
    for (let r = 0; r < rows; r++) { let x = -rnd() * 60; while (x < w) { const bw = 60 + rnd() * 70; g.fillStyle = shade(c, (rnd() - 0.5) * 30); g.fillRect(x + 3, r * h / rows + 3, bw - 6, h / rows - 6); x += bw; } } },
  grass: () => (g, w, h) => { g.fillStyle = '#5fae4c'; g.fillRect(0, 0, w, h); speckle(g, w, h, ['#4a9640', '#7cc65e', '#3f8436'], 700, 3, 10, 21); },
  asphalt: () => (g, w, h) => { g.fillStyle = '#4a4a58'; g.fillRect(0, 0, w, h); speckle(g, w, h, ['#3a3a46', '#5c5c6a'], 600, 2, 6, 31);
    g.fillStyle = '#f2d14a'; for (let x = 0; x < w; x += 140) g.fillRect(x, h / 2 - 5, 80, 10); },
  roof: () => (g, w, h) => { g.fillStyle = '#c8553d'; g.fillRect(0, 0, w, h); g.strokeStyle = '#8e3426'; g.lineWidth = 5;
    for (let y = 0; y < h; y += 28) { g.beginPath(); g.moveTo(0, y); g.lineTo(w, y); g.stroke(); for (let x = (y / 28) % 2 * 20; x < w; x += 40) { g.beginPath(); g.moveTo(x, y); g.lineTo(x, y + 28); g.stroke(); } } },
  wetsand: () => (g, w, h) => { g.fillStyle = '#8a7a66'; g.fillRect(0, 0, w, h); speckle(g, w, h, ['#6e604f', '#a08e76', '#5e5246'], 600, 3, 14, 41);
    g.strokeStyle = '#6a5c4c'; g.lineWidth = 4; g.globalAlpha = 0.5; for (let y = 10; y < h; y += 30) { g.beginPath(); for (let x = 0; x < w; x += 20) g.lineTo(x, y + Math.sin(x / 30) * 5); g.stroke(); } g.globalAlpha = 1; },
  snow: () => (g, w, h) => { g.fillStyle = '#f4f7fc'; g.fillRect(0, 0, w, h); speckle(g, w, h, ['#dfe6f2', '#ffffff', '#cfd8e8'], 500, 4, 18, 51); },
};
function shade(hex, amt) { const c = new THREE.Color(hex); c.offsetHSL(0, 0, amt / 255); return '#' + c.getHexString(); }
function facade(key, base, lit, cols = 6, rows = 10, night = true) {
  // retorna {map, emi}
  const paint = (g, w, h, emissive) => {
    g.fillStyle = emissive ? '#000' : base; g.fillRect(0, 0, w, h);
    if (!emissive) speckle(g, w, h, [shade(base, -18), shade(base, 14)], 120, 6, 20, 13);
    srand(key.length * 7 + cols); const cw = w / cols, rh = h / rows;
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) { const on = rnd() < lit;
      const x = c * cw + cw * 0.2, y = r * rh + rh * 0.22, ww = cw * 0.6, hh = rh * 0.56;
      if (emissive) { g.fillStyle = on && night ? '#ffcf5a' : '#000'; g.fillRect(x, y, ww, hh); }
      else { g.fillStyle = '#1d1a33'; g.fillRect(x - 3, y - 3, ww + 6, hh + 6); g.fillStyle = on && night ? '#ffd772' : (night ? '#2b2f58' : '#9fd0f0'); g.fillRect(x, y, ww, hh);
        g.fillStyle = 'rgba(255,255,255,.25)'; if (!night) g.fillRect(x + 4, y + 4, ww * 0.3, hh * 0.5); } }
  };
  const map = canvasTex(key + 'm' + night, 512, 1024, (g, w, h) => paint(g, w, h, false));
  const emi = canvasTex(key + 'e' + night, 512, 1024, (g, w, h) => paint(g, w, h, true));
  return { map, emi };
}
function signTex(text, bg = '#ffffff', fg = '#1d1d2b', w = 1024, h = 256, font = 'bold 120px sans-serif') {
  return canvasTex('sign' + text + bg + fg + w + h, w, h, (g) => { g.fillStyle = bg; g.fillRect(0, 0, w, h); g.strokeStyle = '#1d1a33'; g.lineWidth = 16; g.strokeRect(8, 8, w - 16, h - 16);
    g.fillStyle = fg; g.textAlign = 'center'; g.textBaseline = 'middle'; let sz = parseInt(font.match(/(\d+)px/)[1]); g.font = font;
    const lines = text.split('\n'); while (Math.max(...lines.map(l => g.measureText(l).width)) > w * 0.9 && sz > 20) { sz -= 4; g.font = font.replace(/\d+px/, sz + 'px'); }
    lines.forEach((l, i) => g.fillText(l, w / 2, h / 2 + (i - (lines.length - 1) / 2) * sz * 1.1)); });
}
function screenTex(kind, text) {
  return canvasTex('scr' + kind + text, 512, 320, (g, w, h) => {
    g.fillStyle = kind === 'news' ? '#16306a' : '#0b1a24'; g.fillRect(0, 0, w, h);
    if (kind === 'news') { g.fillStyle = '#d42a2a'; g.fillRect(0, h - 90, w, 60); g.fillStyle = '#fff'; g.font = 'bold 38px sans-serif'; g.fillText(text, 16, h - 48);
      g.fillStyle = '#ffd23f'; g.fillRect(0, h - 120, 170, 32); g.fillStyle = '#1d1d2b'; g.font = 'bold 24px sans-serif'; g.fillText('URGENTE', 16, h - 96);
      g.fillStyle = '#2a4a90'; g.beginPath(); g.arc(w * 0.7, h * 0.35, 70, 0, 7); g.fill(); g.strokeStyle = '#fff'; g.setLineDash([12, 10]); g.lineWidth = 6; g.stroke(); g.setLineDash([]);
      g.fillStyle = '#fff'; g.font = 'bold 90px sans-serif'; g.fillText('?', w * 0.7 - 25, h * 0.35 + 32); }
    else { g.strokeStyle = '#5fe0a0'; g.lineWidth = 4; g.beginPath(); for (let x = 0; x < w; x += 8) g.lineTo(x, h * 0.5 + Math.sin(x / 30) * 40 * (x / w) + Math.sin(x / 7) * 6); g.stroke();
      g.strokeStyle = '#2a4a5a'; g.lineWidth = 1; for (let x = 0; x < w; x += 40) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, h); g.stroke(); }
      g.fillStyle = '#ffd23f'; g.font = 'bold 30px monospace'; g.fillText(text || 'EIXO: 23.4°', 14, 40); }
  });
}

// ---------------------------------------------------------------- primitivas
function M(c, o = {}) {
  const m = new THREE.MeshToonMaterial({ color: c instanceof THREE.Texture ? 0xffffff : c, map: c instanceof THREE.Texture ? c : null, gradientMap: GRAD, ...o });
  return m;
}
function mesh(geo, m, x = 0, y = 0, z = 0, ry = 0, cast = true) { const o = new THREE.Mesh(geo, m); o.position.set(x, y, z); o.rotation.y = ry; o.castShadow = cast; o.receiveShadow = true; return o; }
function box(G, w, h, d, m, x, y, z, ry = 0) { const o = mesh(new THREE.BoxGeometry(w, h, d), m, x, y + h / 2, z, ry); G.add(o); return o; }
function cyl(G, rt, rb, h, m, x, y, z, seg = 18) { const o = mesh(new THREE.CylinderGeometry(rt, rb, h, seg), m, x, y + h / 2, z); G.add(o); return o; }
function sph(G, r, m, x, y, z, seg = 24) { const o = mesh(new THREE.SphereGeometry(r, seg, Math.max(8, seg / 2)), m, x, y, z); G.add(o); return o; }
function cone(G, r, h, m, x, y, z, seg = 18) { const o = mesh(new THREE.ConeGeometry(r, h, seg), m, x, y + h / 2, z); G.add(o); return o; }
function plane(G, w, d, m, x, y, z, rx = -Math.PI / 2) { const o = mesh(new THREE.PlaneGeometry(w, d), m, x, y, z, 0, false); o.rotation.x = rx; G.add(o); return o; }
function glow(G, color, x, y, z, s) { const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d');
  const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, color); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
  const t = new THREE.CanvasTexture(c); const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, fog: false }));
  sp.position.set(x, y, z); sp.scale.set(s, s, 1); sp.userData.noInk = true; G.add(sp); return sp; }

function palm(G, x, z, h = 9) {
  const trunk = M('#9a6a3e');
  for (let i = 0; i < 6; i++) { const s = mesh(new THREE.CylinderGeometry(0.28 - i * 0.02, 0.32 - i * 0.02, h / 6, 10), trunk, x + Math.sin(i * 0.4) * 0.3, h / 12 + i * h / 6, z); G.add(s); }
  const leaf = M('#3f9a55');
  for (let i = 0; i < 7; i++) { const a = i / 7 * Math.PI * 2; const l = mesh(new THREE.ConeGeometry(0.5, 5, 4), leaf, x + Math.cos(a) * 2.2, h - 0.6, z + Math.sin(a) * 2.2);
    l.rotation.z = Math.cos(a) * -1.9; l.rotation.x = Math.sin(a) * 1.9; l.scale.set(1, 1, 0.25); G.add(l); }
  sph(G, 0.6, M('#6a4a2a'), x, h - 0.2, z, 10);
}
function lamp(G, x, z, night, h = 6) { cyl(G, 0.12, 0.16, h, M('#3a3a4e'), x, 0, z, 8); box(G, 1.4, 0.15, 0.2, M('#3a3a4e'), x + 0.6, h, z);
  const b = sph(G, 0.3, M(night ? '#fff1b0' : '#e8e8e8', { emissive: night ? '#ffd27a' : '#000', emissiveIntensity: 1.2 }), x + 1.2, h - 0.2, z, 12);
  if (night) { const pl = new THREE.PointLight('#ffc870', 18, 16, 1.6); pl.position.set(x + 1.2, h - 0.6, z); G.add(pl); glow(G, 'rgba(255,210,120,0.9)', x + 1.2, h - 0.2, z, 4); } }
function canoe(G, x, z, ry = 0, name = 'DONA CIDA', tilt = 0) {
  const g = new THREE.Group(); const hull = M('#f2ece0'), red = M('#d9483b');
  const shape = new THREE.Shape(); shape.moveTo(-3, 0.9); shape.lineTo(3, 0.9); shape.quadraticCurveTo(2.6, 0, 1.8, 0); shape.lineTo(-1.8, 0); shape.quadraticCurveTo(-2.6, 0, -3, 0.9);
  const geo = new THREE.ExtrudeGeometry(shape, { depth: 1.3, bevelEnabled: false }); geo.translate(0, 0, -0.65);
  const m = new THREE.Mesh(geo, [red, hull]); m.castShadow = m.receiveShadow = true; g.add(m);
  const st = mesh(new THREE.BoxGeometry(5.6, 0.22, 1.34), red, 0, 0.62, 0); g.add(st);
  const nm = new THREE.Mesh(new THREE.PlaneGeometry(2.4, 0.5), M(signTex(name, '#f2ece0', '#1d3a8a', 1024, 220))); nm.position.set(0.2, 0.35, 0.67); g.add(nm);
  const oar = M('#a0703a'); const o1 = mesh(new THREE.CylinderGeometry(0.05, 0.05, 3.2, 6), oar, -0.6, 1.3, 0.2); o1.rotation.z = 1.1; g.add(o1);
  g.position.set(x, 0, z); g.rotation.y = ry; g.rotation.z = tilt; G.add(g); return g;
}
function moonMesh(G, L, az = 258, el = 16, dist = 700, r = 26) {
  const a = THREE.MathUtils.degToRad(az), e = THREE.MathUtils.degToRad(el);
  const mx = Math.cos(a) * Math.cos(e) * dist, my = Math.sin(e) * dist, mz = Math.sin(a) * Math.cos(e) * dist;
  const tex = canvasTex('moon', 512, 256, (g, w, h) => { g.fillStyle = '#fff4c4'; g.fillRect(0, 0, w, h); speckle(g, w, h, ['#e3d398', '#d6c486'], 60, 10, 40, 77); });
  const m = new THREE.Mesh(new THREE.SphereGeometry(r, 32, 16), new THREE.MeshBasicMaterial({ map: tex, fog: false }));
  m.position.set(mx, my, mz); m.userData.sky = true; G.add(m);
  const gl = glow(G, 'rgba(255,240,190,0.55)', mx, my, mz, r * 5.5); gl.userData.sky = true;
}

// ---------------------------------------------------------------- SETS
export const SETS = {};
const isNight = (L) => L.stars === 1;

// Praia de Santos: mar em -z, prédios em +z, faixa de areia ao longo de x
SETS.beach = (o, L) => {
  const G = new THREE.Group(); const night = isNight(L) || o.night;
  const snow = !!o.snow;
  plane(G, 900, 900, M(canvasTex(snow ? 'snow' : 'sand', 512, 512, snow ? P.snow() : P.sand(), 60, 60)), 0, 0, 0);
  const shore = o.receded ? -32 : (o.shore ?? -10);
  plane(G, 900, 60, M(canvasTex('wet', 512, 256, P.wetsand(), 50, 4)), 0, 0.02, -36);
  const seaC = o.storm ? ['#2c4a66', '#4a6a88'] : night ? ['#1f3f7a', '#3462a8'] : snow ? ['#4a6688', '#6a86a8'] : ['#2f8fcf', '#5ab8e8'];
  plane(G, 1400, 900, M(canvasTex('sea' + seaC[0], 512, 512, P.water(...seaC), 70, 45)), 0, 0.06, shore - 450);
  // espuma da beira
  for (let i = 0; i < 3; i++) box(G, 1400, 0.08, 0.5 - i * 0.12, M('#f4fbff', { emissive: '#203040', emissiveIntensity: 0.2 }), 0, 0.03, shore + 0.3 - i * 1.8);
  if (o.storm) { srand(99); for (let i = 0; i < 40; i++) { const w = mesh(new THREE.ConeGeometry(2 + rnd() * 3, 1.2 + rnd() * 2, 4), M('#5a7c9e'), -150 + rnd() * 300, 0.3, shore - 10 - rnd() * 120); w.scale.set(3, 1, 0.5); G.add(w); } }
  // ilha + farol
  const isl = mesh(new THREE.SphereGeometry(40, 24, 12), M(snow ? '#e8eef8' : '#3d7a52'), -120, -6, -260); isl.scale.set(1.8, 0.75, 1.0); G.add(isl);
  const isl2 = mesh(new THREE.SphereGeometry(22, 18, 10), M(snow ? '#dfe6f2' : '#4c8c5c'), -70, -4, -240); isl2.scale.set(1.5, 0.8, 1); G.add(isl2);
  cyl(G, 1.2, 1.6, 9, M('#f2ece0'), -112, 22, -250, 12); cone(G, 1.6, 2.2, M('#d9483b'), -112, 31, -250, 12);
  if (night) glow(G, 'rgba(255,230,140,0.9)', -112, 30, -248, 10);
  // jardim da orla, calçadão, avenida, prédios
  plane(G, 900, 8, M(canvasTex(snow ? 'snow' : 'grass', 256, 256, snow ? P.snow() : P.grass(), 90, 1)), 0, 0.04, 22);
  box(G, 900, 0.7, 0.8, M(canvasTex('mureta', 512, 128, P.stone('#c9c3cf', '#8e8898'), 120, 1)), 0, 0, 17.6); // mureta
  plane(G, 900, 4, M(canvasTex('calc', 256, 256, P.plaster('#e6e0d6', '#cfc7ba'), 120, 1)), 0, 0.05, 28);
  plane(G, 900, 12, M(canvasTex('asf', 512, 128, P.asphalt(), 60, 1)), 0, 0.05, 36);
  plane(G, 900, 6, M(canvasTex('calc2', 256, 256, P.plaster('#d8d2c8', '#bfb7aa'), 120, 1)), 0, 0.05, 45);
  srand(17); let x = -260;
  const cols = ['#6f7fd0', '#e08a6a', '#7ac0b8', '#d8c070', '#a07ad0', '#e8e0d0', '#8ab0e0', '#d0907a'];
  while (x < 260) { const w = 14 + rnd() * 10, h = 18 + rnd() * 34, d = 14; const c = pick(cols);
    const f = facade('b' + Math.round(x), c, night ? 0.5 : 0, 5, Math.round(h / 3.2), night);
    const mat = M(f.map, night ? { emissive: '#ffffff', emissiveMap: f.emi, emissiveIntensity: 0.9 } : {});
    box(G, w, h, d, [M(c), M(c), M(snow ? '#f4f7fc' : '#8a8aa0'), M(c), mat, M(c)].length ? mat : mat, x + w / 2, 0, 55);
    if (snow) box(G, w + 0.4, 0.6, d + 0.4, M('#f6f9ff'), x + w / 2, h, 55);
    x += w + 2 + rnd() * 3; }
  for (let i = -8; i <= 8; i++) { palm(G, i * 14 + 3, 22, 8 + (i % 3)); if (i % 2 === 0) lamp(G, i * 14 - 3, 26, night); }
  // quiosques
  for (const qx of (o.kiosks ?? [-46, 18, 70])) { box(G, 5, 2.6, 4, M('#f2ece0'), qx, 0, 12); box(G, 6, 0.4, 5, M('#d9483b'), qx, 2.6, 12); box(G, 5.4, 0.6, 0.3, M(signTex('QUIOSQUE', '#ffd23f', '#1d1d2b', 512, 128)), qx, 1.9, 9.9);
    if (night) { glow(G, 'rgba(255,200,120,0.8)', qx, 2.2, 9.6, 8); const pl = new THREE.PointLight('#ffc070', 25, 18, 1.5); pl.position.set(qx, 2.4, 9); G.add(pl); } }
  // guarda-sóis
  if (!night && !o.noUmbrella) { srand(23); for (let i = 0; i < 10; i++) { const ux = -80 + i * 17 + rnd() * 5, uz = -2 + rnd() * 10; cyl(G, 0.06, 0.06, 2.6, M('#eeeeee'), ux, 0, uz, 6);
    const u = cone(G, 1.8, 0.8, M(pick(['#e04848', '#3a8dde', '#ffd23f', '#5cbf6a'])), ux, 2.3, uz, 10); if (o.windy) u.rotation.z = 0.6; } }
  // canoas
  const cz = o.receded ? -20 : shore + 2;
  canoe(G, o.canoeX ?? 4, o.canoeZ ?? cz, 0.15, 'DONA CIDA', o.canoeTilt ?? 0);
  canoe(G, -12, cz + 3, -0.3, 'ESTRELA');
  canoe(G, 22, cz + 1.5, 0.4, 'SÃO PEDRO');
  if (o.moon) moonMesh(G, L, o.moonAz, o.moonEl);
  if (o.sun) { const s = sph(G, 30, new THREE.MeshBasicMaterial({ color: '#ffe08a', fog: false }), Math.cos(o.sunAz) * 650, o.sunEl ?? 60, Math.sin(o.sunAz) * 650); s.userData.sky = true; glow(G, 'rgba(255,220,140,0.8)', s.position.x, s.position.y, s.position.z, 220).userData.sky = true; }
  if (o.snowman) { sph(G, 1.1, M('#ffffff'), o.snowman[0], 1.0, o.snowman[1]); sph(G, 0.75, M('#ffffff'), o.snowman[0], 2.6, o.snowman[1]); }
  return G;
};

// Cozinha da casa do Seu Dito
SETS.kitchen = (o, L) => {
  const G = new THREE.Group(); const night = isNight(L);
  const wall = M(canvasTex('kwall', 256, 256, P.plaster('#f2d36b', '#e0bd52'), 3, 2));
  plane(G, 10, 8, M(canvasTex('kfloor', 512, 512, P.checker('#2fb3a7', '#f4f1e6', 8), 2, 2)), 0, 0, 0);
  const back = mesh(new THREE.BoxGeometry(10, 3.4, 0.2), wall, 0, 1.7, -4); G.add(back);
  const left = mesh(new THREE.BoxGeometry(0.2, 3.4, 8), wall, -5, 1.7, 0); G.add(left);
  const right = mesh(new THREE.BoxGeometry(0.2, 3.4, 8), wall, 5, 1.7, 0); G.add(right);
  plane(G, 10, 8, M('#f8f4ea'), 0, 3.4, 0, Math.PI / 2);
  // janela com céu
  const sky = new THREE.Mesh(new THREE.PlaneGeometry(1.8, 1.3), new THREE.MeshBasicMaterial({ color: night ? '#141a52' : '#9fd6ff', fog: false })); sky.position.set(-1.5, 1.9, -3.88); G.add(sky);
  if (night) { srand(4); for (let i = 0; i < 14; i++) { const s = new THREE.Mesh(new THREE.CircleGeometry(0.018, 6), new THREE.MeshBasicMaterial({ color: '#fff' })); s.position.set(-2.3 + rnd() * 1.6, 1.35 + rnd() * 1.1, -3.87); G.add(s); } }
  box(G, 2.0, 0.08, 0.12, M('#ffffff'), -1.5, 1.22, -3.85); box(G, 2.0, 0.08, 0.12, M('#ffffff'), -1.5, 2.56, -3.85);
  box(G, 0.08, 1.4, 0.12, M('#ffffff'), -2.5, 1.22, -3.85); box(G, 0.08, 1.4, 0.12, M('#ffffff'), -0.5, 1.22, -3.85); box(G, 0.06, 1.4, 0.12, M('#ffffff'), -1.5, 1.22, -3.85);
  // armários + bancada + pia
  box(G, 4.2, 0.95, 0.7, M('#3fb8b0'), 2.6, 0, -3.5); box(G, 4.3, 0.08, 0.8, M('#f4f1e6'), 2.6, 0.95, -3.5);
  for (let i = 0; i < 4; i++) box(G, 0.9, 0.7, 0.04, M('#5ccdc4'), 1.1 + i * 1.0, 0.12, -3.14);
  box(G, 3.0, 0.8, 0.45, M('#3fb8b0'), 3.0, 2.2, -3.7);
  box(G, 0.9, 2.0, 0.8, M('#e9edf2'), -3.9, 0, -3.4); box(G, 0.04, 0.5, 0.04, M('#888'), -3.5, 1.1, -2.98);
  // TV
  box(G, 1.4, 0.75, 0.6, M('#8a5a3a'), 4.3, 0, -1.2);
  const tv = box(G, 1.3, 0.8, 0.12, M('#202030'), 4.3, 0.78, -1.2); tv.rotation.y = -Math.PI / 2;
  const scr = new THREE.Mesh(new THREE.PlaneGeometry(1.15, 0.68), new THREE.MeshBasicMaterial({ map: screenTex('news', o.tv || 'A LUA SUMIU'), fog: false }));
  scr.position.set(4.23, 1.18, -1.2); scr.rotation.y = -Math.PI / 2; G.add(scr);
  // mesa e cadeiras
  box(G, 1.6, 0.08, 1.0, M(canvasTex('mesa', 256, 256, P.planks('#c48a52', '#8a5a30'))), 0.4, 0.74, 0.2);
  for (const [lx, lz] of [[-0.3, -0.2], [1.1, -0.2], [-0.3, 0.6], [1.1, 0.6]]) box(G, 0.07, 0.74, 0.07, M('#8a5a30'), lx, 0, lz);
  for (const cx of [-0.8, 1.6]) { box(G, 0.5, 0.06, 0.5, M('#e04848'), cx, 0.45, 0.2); box(G, 0.06, 0.6, 0.5, M('#e04848'), cx + (cx < 0 ? -0.22 : 0.22), 0.45, 0.2); }
  // relógio e calendário
  const clk = new THREE.Mesh(new THREE.CircleGeometry(0.25, 24), M(canvasTex('clock', 256, 256, (g) => { g.fillStyle = '#fff'; g.beginPath(); g.arc(128, 128, 124, 0, 7); g.fill(); g.lineWidth = 12; g.strokeStyle = '#1d1a33'; g.stroke(); g.lineWidth = 10; g.beginPath(); g.moveTo(128, 128); g.lineTo(128, 50); g.moveTo(128, 128); g.lineTo(185, 150); g.stroke(); })));
  clk.position.set(0.8, 2.6, -3.88); G.add(clk);
  if (o.varal) { box(G, 6, 0.02, 0.02, M('#eee'), 0, 2.6, 1.6); srand(8); for (let i = 0; i < 7; i++) box(G, 0.45, 0.6, 0.02, M(pick(['#e04848', '#3a8dde', '#ffd23f', '#9d7ad6', '#5cbf6a'])), -2.4 + i * 0.8, 1.95, 1.6); }
  if (o.bacia) { cyl(G, 0.32, 0.24, 0.18, M('#5ab0e8'), 2.0, 0.99, -3.4, 20); }
  // luminária pendente
  cyl(G, 0.01, 0.01, 0.9, M('#333'), 0.4, 2.5, 0.2, 4); cone(G, 0.35, 0.3, M('#2fb3a7'), 0.4, 2.35, 0.2, 16);
  const pl = new THREE.PointLight('#ffd9a0', 9, 9, 1.4); pl.position.set(0.4, 2.2, 0.2); pl.castShadow = false; G.add(pl);
  glow(G, 'rgba(255,220,160,0.7)', 0.4, 2.3, 0.2, 1.4);
  return G;
};

// Observatório da doutora Lia
SETS.lab = (o, L) => {
  const G = new THREE.Group();
  plane(G, 20, 20, M(canvasTex('labfloor', 512, 512, P.planks('#6a5a8a', '#4a3e66'), 4, 4)), 0, 0, 0);
  const dome = new THREE.Mesh(new THREE.SphereGeometry(9, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2), M('#8a92c8', { side: THREE.BackSide })); dome.position.y = 3; dome.receiveShadow = true; G.add(dome);
  const wall = new THREE.Mesh(new THREE.CylinderGeometry(9, 9, 3, 32, 1, true), M(canvasTex('labwall', 256, 256, P.plaster('#7a82b8', '#6870a4'), 6, 1), { side: THREE.BackSide })); wall.position.y = 1.5; G.add(wall);
  // fresta da cúpula com céu
  const slit = new THREE.Mesh(new THREE.PlaneGeometry(2.2, 9), new THREE.MeshBasicMaterial({ color: '#0d1240', side: THREE.DoubleSide, fog: false })); slit.position.set(0, 9.2, -3.2); slit.rotation.x = -0.9; G.add(slit);
  // telescópio
  cyl(G, 0.5, 0.7, 1.4, M('#3a3a4e'), 0, 0, -2, 16); sph(G, 0.45, M('#555a70'), 0, 1.7, -2, 16);
  const tube = mesh(new THREE.CylinderGeometry(0.45, 0.55, 4.2, 20), M('#f2ece0'), 0, 3.1, -2.6); tube.rotation.x = -0.75; G.add(tube);
  const ring = mesh(new THREE.TorusGeometry(0.5, 0.08, 8, 20), M('#d9483b'), 0, 3.9, -3.3); ring.rotation.x = -0.75 + Math.PI / 2; G.add(ring);
  // mesa com monitores
  box(G, 3.2, 0.08, 1.0, M('#c48a52'), 3.4, 0.76, 1.2); for (const [lx, lz] of [[2.0, 0.8], [4.8, 0.8], [2.0, 1.6], [4.8, 1.6]]) box(G, 0.07, 0.76, 0.07, M('#8a5a30'), lx, 0, lz);
  for (let i = 0; i < 2; i++) { box(G, 0.9, 0.6, 0.06, M('#222230'), 2.8 + i * 1.1, 1.0, 0.9);
    const s = new THREE.Mesh(new THREE.PlaneGeometry(0.82, 0.52), new THREE.MeshBasicMaterial({ map: screenTex('graph', i ? (o.screen2 || 'SINAL: ---') : (o.screen || 'EIXO: 23.4°')), fog: false })); s.position.set(2.8 + i * 1.1, 1.3, 0.94); G.add(s); }
  // papéis e pôster de estrelas
  for (let i = 0; i < 5; i++) { const p = new THREE.Mesh(new THREE.PlaneGeometry(0.3, 0.4), M('#fffdf2')); p.rotation.x = -Math.PI / 2; p.rotation.z = i * 0.4; p.position.set(3.4 + (i - 2) * 0.25, 0.81, 1.4); G.add(p); }
  const poster = new THREE.Mesh(new THREE.PlaneGeometry(2.2, 1.5), M(canvasTex('starmap', 512, 360, (g, w, h) => { g.fillStyle = '#121a4a'; g.fillRect(0, 0, w, h); srand(3); g.fillStyle = '#fff'; for (let i = 0; i < 90; i++) { g.beginPath(); g.arc(rnd() * w, rnd() * h, 1 + rnd() * 3, 0, 7); g.fill(); }
    g.strokeStyle = '#ffd23f'; g.lineWidth = 3; g.setLineDash([10, 8]); g.beginPath(); g.arc(w * 0.7, h * 0.4, 60, 0, 7); g.stroke(); g.setLineDash([]); g.fillStyle = '#ffd23f'; g.font = 'bold 34px sans-serif'; g.fillText('LUA ?', w * 0.62, h * 0.82); })));
  poster.position.set(-5.5, 1.8, -6.8); poster.lookAt(0, 1.8, 0); G.add(poster);
  const pl = new THREE.PointLight('#ffd9a0', 10, 12, 1.4); pl.position.set(3, 2.6, 1.6); G.add(pl); glow(G, 'rgba(120,255,190,0.4)', 3.3, 1.3, 1.0, 2.0);
  return G;
};

// Rua de Santos (comércio)
SETS.street = (o, L) => {
  const G = new THREE.Group(); const night = isNight(L);
  plane(G, 400, 14, M(canvasTex('asf', 512, 128, P.asphalt(), 30, 1)), 0, 0, 0);
  plane(G, 400, 5, M(canvasTex('calcs', 256, 256, P.plaster('#ddd6ca', '#c6beb0'), 80, 1)), 0, 0.12, -9.5);
  plane(G, 400, 5, M(canvasTex('calcs', 256, 256, P.plaster('#ddd6ca', '#c6beb0'), 80, 1)), 0, 0.12, 9.5);
  box(G, 400, 0.12, 5, M('#cfc7ba'), 0, 0, -9.5); box(G, 400, 0.12, 5, M('#cfc7ba'), 0, 0, 9.5);
  srand(o.seed || 5); const cols = ['#f08a5d', '#7ab8e8', '#f2c230', '#9d7ad6', '#5cbf9a', '#e86a8a', '#f4e6c8'];
  for (const side of [-1, 1]) { let x = -120; while (x < 120) { const w = 7 + rnd() * 4, h = 6 + rnd() * 5, c = pick(cols);
      const f = facade('h' + side + Math.round(x), c, night ? 0.6 : 0, 3, 2, night);
      const m = M(f.map, night ? { emissive: '#fff', emissiveMap: f.emi, emissiveIntensity: 0.9 } : {});
      const b = box(G, w, h, 8, m, x + w / 2, 0, side * 16); box(G, w + 0.6, 0.5, 8.6, M(o.snow ? '#f6f9ff' : '#c8553d'), x + w / 2, h, side * 16);
      box(G, 1.4, 2.4, 0.1, M('#6a3e2a'), x + w / 2, 0.1, side * 16 - side * 4.05); x += w + 0.2; } }
  for (let i = -6; i <= 6; i++) lamp(G, i * 16, -7.4, night, 5.5);
  if (o.stall) { box(G, 4, 0.9, 1.6, M('#a0703a'), o.stall[0], 0, o.stall[1]); cyl(G, 0.05, 0.05, 2.6, M('#666'), o.stall[0] - 1.9, 0, o.stall[1] - 0.7, 6); cyl(G, 0.05, 0.05, 2.6, M('#666'), o.stall[0] + 1.9, 0, o.stall[1] - 0.7, 6);
    box(G, 4.4, 0.1, 2.0, M('#e04848'), o.stall[0], 2.6, o.stall[1]); srand(3); for (let i = 0; i < 18; i++) sph(G, 0.14, M('#e8392e'), o.stall[0] - 1.6 + (i % 9) * 0.4, 1.02, o.stall[1] - 0.4 + Math.floor(i / 9) * 0.4, 10);
    const s = new THREE.Mesh(new THREE.PlaneGeometry(1.8, 0.6), M(signTex(o.stallText || 'TOMATE\nR$ 49,90', '#fff7d6', '#c42a2a', 512, 180))); s.position.set(o.stall[0], 1.5, o.stall[1] + 0.82); G.add(s); }
  if (o.shop) { const s = new THREE.Mesh(new THREE.PlaneGeometry(6, 1.1), M(signTex(o.shop, '#ffd23f', '#1d1d2b', 1024, 190))); s.position.set(o.shopX || 0, 4.2, -11.9); G.add(s); }
  if (o.queue) { /* fila desenhada em 2D */ }
  // carro
  const car = new THREE.Group(); box(car, 4, 0.9, 1.8, M('#e04848'), 0, 0.35, 0); box(car, 2.2, 0.7, 1.6, M('#e04848'), -0.2, 1.25, 0); box(car, 2.0, 0.55, 1.62, M('#9fd0f0'), -0.2, 1.3, 0);
  for (const [wx, wz] of [[-1.3, 0.9], [1.3, 0.9], [-1.3, -0.9], [1.3, -0.9]]) { const w = mesh(new THREE.CylinderGeometry(0.38, 0.38, 0.3, 14), M('#222'), wx, 0.38, wz); w.rotation.x = Math.PI / 2; car.add(w); }
  car.position.set(o.carX ?? 14, 0, -4.5); G.add(car);
  if (o.moonGhost) moonMesh(G, L);
  return G;
};

// Espaço: Terra, órbita, Lua opcional
SETS.space = (o, L) => {
  const G = new THREE.Group();
  const et = canvasTex('earth', 1024, 512, (g, w, h) => { g.fillStyle = '#2f78c4'; g.fillRect(0, 0, w, h); srand(42);
    for (let k = 0; k < 9; k++) { const cx = rnd() * w, cy = h * 0.2 + rnd() * h * 0.6, s = 50 + rnd() * 90; g.fillStyle = '#5cbf6a'; g.beginPath();
      for (let i = 0; i < 16; i++) { const a = i / 16 * 6.283, r = s * (0.6 + rnd() * 0.6); g.lineTo(cx + Math.cos(a) * r * 1.4, cy + Math.sin(a) * r); } g.closePath(); g.fill(); g.strokeStyle = '#2a6a3a'; g.lineWidth = 4; g.stroke();
      g.fillStyle = '#e8cf8a'; g.beginPath(); g.arc(cx + s * 0.3, cy, s * 0.3, 0, 7); g.fill(); }
    g.fillStyle = '#f4f8ff'; g.fillRect(0, 0, w, 40); g.fillRect(0, h - 40, w, 40); });
  const earth = new THREE.Mesh(new THREE.SphereGeometry(10, 64, 32), M(et)); earth.rotation.z = THREE.MathUtils.degToRad(-(o.tilt ?? 23.4)); earth.rotation.y = o.spin ?? 0; earth.castShadow = earth.receiveShadow = true; G.add(earth);
  const clouds = new THREE.Mesh(new THREE.SphereGeometry(10.25, 48, 24), new THREE.MeshToonMaterial({ color: '#ffffff', transparent: true, opacity: 0.25, gradientMap: GRAD })); G.add(clouds); clouds.userData.noInk = true;
  glow(G, 'rgba(110,170,255,0.55)', 0, 0, 0, 30);
  // eixo
  const ax = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 30, 8), new THREE.MeshBasicMaterial({ color: o.axisGlow ? '#ffd23f' : '#ffffff' })); ax.rotation.z = THREE.MathUtils.degToRad(-(o.tilt ?? 23.4)); G.add(ax);
  // órbita
  const orb = new THREE.Mesh(new THREE.TorusGeometry(38, 0.08, 6, 160), new THREE.MeshBasicMaterial({ color: '#c8c8ff', transparent: true, opacity: o.moon ? 0.5 : 0.3 })); orb.rotation.x = Math.PI / 2 + 0.1; G.add(orb); orb.userData.noInk = true;
  if (o.moon) { const mt = canvasTex('moonS', 512, 256, (g, w, h) => { g.fillStyle = '#d9d4c8'; g.fillRect(0, 0, w, h); speckle(g, w, h, ['#a8a298', '#bdb6aa'], 90, 8, 30, 12); });
    const mm = new THREE.Mesh(new THREE.SphereGeometry(2.7, 32, 16), M(mt)); mm.position.set(Math.cos(o.moonA ?? 0.6) * 38, 0, Math.sin(o.moonA ?? 0.6) * 38); G.add(mm); }
  if (o.farMoon) { const mm = new THREE.Mesh(new THREE.SphereGeometry(1.2, 24, 12), M('#d9d4c8')); mm.position.set(...o.farMoon); G.add(mm); glow(G, 'rgba(255,255,230,0.6)', ...o.farMoon, 8); }
  if (o.mars) { const m2 = new THREE.Mesh(new THREE.SphereGeometry(3, 32, 16), M('#d0603a')); m2.position.set(...o.mars); G.add(m2); }
  if (o.probe) { const pg = new THREE.Group(); box(pg, 1, 1, 1, M('#d8d8e0'), 0, -0.5, 0); box(pg, 4, 0.05, 1, M('#3a5ac8'), 0, 0, 0); pg.position.set(...o.probe); G.add(pg); }
  return G;
};

// Porto / colônia de pescadores
SETS.harbor = (o, L) => {
  const G = new THREE.Group(); const night = isNight(L);
  const low = !!o.lowtide;
  plane(G, 900, 900, M(canvasTex('wet', 512, 256, P.wetsand(), 120, 120)), 0, -0.6, 0);
  const seaC = o.storm ? ['#2c4a66', '#4a6a88'] : night ? ['#1f3f7a', '#3462a8'] : ['#2f8fcf', '#5ab8e8'];
  plane(G, 900, 900, M(canvasTex('sea' + seaC[0], 512, 512, P.water(...seaC), 70, 70)), 0, low ? -0.9 : 0.2, -450 + (low ? -20 : 0));
  // píer
  plane(G, 4, 40, M(canvasTex('pier', 256, 512, P.planks('#b88a58', '#7a5530'), 1, 6)), 0, 1.6, -8);
  box(G, 4, 0.3, 40, M('#9a6e42'), 0, 1.3, -8);
  for (let z = 10; z > -28; z -= 4) for (const sx of [-1.9, 1.9]) cyl(G, 0.18, 0.18, 3, M('#6a4a2a'), sx, -1.2, z, 8);
  // galpão da colônia
  box(G, 14, 5, 8, M(canvasTex('galpao', 256, 256, P.plaster('#5cbfb0', '#4aa89a'), 2, 1)), -12, 0, 14);
  const roof = mesh(new THREE.BoxGeometry(15, 0.4, 9.5), M(canvasTex('roof', 256, 256, P.roof(), 3, 2)), -12, 5.4, 14); roof.rotation.x = 0.08; G.add(roof);
  const sg = new THREE.Mesh(new THREE.PlaneGeometry(8, 1.3), M(signTex('COLÔNIA DE PESCADORES', '#fff7d6', '#1d3a8a', 1024, 170))); sg.position.set(-12, 4.0, 9.95); G.add(sg);
  box(G, 2, 2.8, 0.1, M('#7a4a2a'), -12, 0, 9.95);
  plane(G, 60, 20, M(canvasTex('sand', 512, 512, P.sand(), 6, 2)), -10, 0.01, 16);
  box(G, 40, 1.6, 0.6, M(canvasTex('mureta', 512, 128, P.stone('#c9c3cf', '#8e8898'), 8, 1)), -10, 0, 6.2); // mureta da colônia
  // barcos
  srand(13); for (let i = 0; i < 4; i++) { canoe(G, -10 + i * 7, low ? -6 - i * 3 : -9 - i * 3, 0.2 * i, pick(['MARÉ BOA', 'ZÉ GALINHA', 'ESTRELA', 'DONA CIDA']), low ? 0.12 : 0).position.y = low ? -0.6 : 0.1; }
  // navios na fila
  if (o.ships) { for (let i = 0; i < 5; i++) { const sx = -140 + i * 60, sz = -180 - (i % 2) * 40; box(G, 40, 6, 9, M('#3a4a6a'), sx, 0, sz); box(G, 8, 8, 8, M('#f2ece0'), sx - 14, 6, sz);
      for (let k = 0; k < 6; k++) box(G, 4, 3, 7, M(pick(['#e04848', '#3a8dde', '#ffd23f', '#5cbf6a'])), sx - 6 + k * 4.4, 6, sz); } }
  for (let i = 0; i < 3; i++) lamp(G, -18 + i * 9, 9, night, 5);
  return G;
};

// Estúdio de rádio
SETS.radio = (o, L) => {
  const G = new THREE.Group(); const night = isNight(L);
  plane(G, 10, 8, M(canvasTex('rfloor', 256, 256, P.planks('#7a5a8a', '#5a3e6a'), 2, 2)), 0, 0, 0);
  const wall = M(canvasTex('rwall', 256, 256, P.plaster('#e8735a', '#d0604a'), 3, 2));
  box(G, 10, 3.4, 0.2, wall, 0, 0, -4); box(G, 0.2, 3.4, 8, wall, -5, 0, 0); box(G, 0.2, 3.4, 8, wall, 5, 0, 0);
  // painéis acústicos
  for (let i = 0; i < 5; i++) for (let j = 0; j < 2; j++) box(G, 0.9, 0.9, 0.12, M((i + j) % 2 ? '#3a3a5a' : '#4a4a72'), -3.8 + i * 1.0, 1.0 + j * 1.0, -3.85);
  // janela pro mar
  const win = new THREE.Mesh(new THREE.PlaneGeometry(2.4, 1.4), new THREE.MeshBasicMaterial({ color: night ? '#16205a' : o.storm ? '#4a5068' : '#7fc8f8', fog: false })); win.position.set(2.8, 1.9, -3.88); G.add(win);
  box(G, 2.6, 0.1, 0.15, M('#f2ece0'), 2.8, 1.15, -3.85); box(G, 2.6, 0.1, 0.15, M('#f2ece0'), 2.8, 2.6, -3.85);
  // mesa de som e microfones
  box(G, 3.6, 0.8, 1.1, M('#3a3a4e'), 0, 0, -1.2); const mix = box(G, 2.4, 0.12, 0.8, M('#22222e'), 0, 0.8, -1.2);
  srand(2); for (let i = 0; i < 16; i++) box(G, 0.06, 0.1, 0.06, M(pick(['#e04848', '#ffd23f', '#5cbf6a', '#ffffff'])), -1.0 + (i % 8) * 0.28, 0.92, -1.4 + Math.floor(i / 8) * 0.3);
  for (const mx of [-1.0, 1.0]) { cyl(G, 0.02, 0.02, 0.5, M('#444'), mx, 0.92, -0.85, 6); sph(G, 0.1, M('#55586a'), mx, 1.48, -0.8, 12); }
  const onair = box(G, 1.4, 0.45, 0.08, M(signTex('NO AR', '#d42a2a', '#ffffff', 512, 160), { emissive: '#ff3030', emissiveIntensity: 0.6 }), -2.6, 2.5, -3.85);
  const logo = new THREE.Mesh(new THREE.PlaneGeometry(2.4, 0.7), M(signTex('RÁDIO MAR FM', '#1d3a8a', '#ffd23f', 1024, 280))); logo.position.set(-1.4, 3.0, -3.88); G.add(logo);
  const pl = new THREE.PointLight('#ffd9a0', 10, 10, 1.4); pl.position.set(0, 2.8, 0.5); G.add(pl);
  return G;
};

// Estúdio de TV (entrevista)
SETS.studio = (o, L) => {
  const G = new THREE.Group();
  plane(G, 16, 12, M(canvasTex('sfloor', 512, 512, P.checker('#3a3f8a', '#4a50a8', 8), 2, 2)), 0, 0, 0);
  const bg = M(canvasTex('sbg', 512, 256, (g, w, h) => { const gr = g.createLinearGradient(0, 0, w, 0); gr.addColorStop(0, '#ff7a59'); gr.addColorStop(1, '#ffb347'); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    g.fillStyle = 'rgba(255,255,255,.15)'; for (let i = 0; i < 8; i++) { g.beginPath(); g.arc(i * 80, h, 60 + i * 10, 0, 7); g.fill(); } }));
  const back = mesh(new THREE.CylinderGeometry(7, 7, 4.5, 40, 1, true, Math.PI * 0.75, Math.PI * 0.5), bg, 0, 2.25, 1); back.material.side = THREE.BackSide; G.add(back);
  const scr = new THREE.Mesh(new THREE.PlaneGeometry(3.6, 2.0), new THREE.MeshBasicMaterial({ map: signTex(o.screen || 'PROGRAMA DA\nMANHÃ', '#1d3a8a', '#ffd23f', 1024, 560), fog: false })); scr.position.set(0, 2.5, -5.6); G.add(scr);
  box(G, 2.2, 0.75, 0.9, M('#f2ece0'), 0, 0, -1.0); box(G, 2.4, 0.08, 1.1, M('#ffd23f'), 0, 0.75, -1.0);
  for (const cx of [-1.6, 1.6]) { box(G, 0.9, 0.45, 0.9, M('#e04848'), cx, 0, -0.4); box(G, 0.9, 0.7, 0.2, M('#e04848'), cx, 0.45, -0.8); }
  cyl(G, 0.3, 0.3, 0.12, M('#a0703a'), 0, 0.83, -1.0, 16); // tampo do pião
  const pl = new THREE.PointLight('#fff0d8', 14, 14, 1.3); pl.position.set(0, 3.4, 2); G.add(pl);
  return G;
};

// Sala de aula
SETS.classroom = (o, L) => {
  const G = new THREE.Group();
  plane(G, 12, 10, M(canvasTex('cfloor', 256, 256, P.planks('#c89a62', '#9a6e42'), 2, 3)), 0, 0, 0);
  const wall = M(canvasTex('cwall', 256, 256, P.plaster('#9fd6c8', '#86c0b2'), 3, 2));
  box(G, 12, 3.4, 0.2, wall, 0, 0, -5); box(G, 0.2, 3.4, 10, wall, -6, 0, 0); box(G, 0.2, 3.4, 10, wall, 6, 0, 0);
  const board = new THREE.Mesh(new THREE.PlaneGeometry(4.2, 1.6), M(canvasTex('lousa' + (o.board || ''), 1024, 400, (g, w, h) => { g.fillStyle = '#2f5a46'; g.fillRect(0, 0, w, h); g.strokeStyle = '#8a5a30'; g.lineWidth = 24; g.strokeRect(0, 0, w, h);
    if (o.board) { g.fillStyle = '#f4f4ea'; g.font = 'bold 80px sans-serif'; o.board.split('\n').forEach((ln, i) => g.fillText(ln, 60, 130 + i * 110)); return; }
    g.fillStyle = '#f4f4ea'; g.font = 'bold 90px sans-serif'; g.fillText('A LUA', 60, 140); g.strokeStyle = '#f4f4ea'; g.lineWidth = 8; for (let i = 0; i < 4; i++) { g.beginPath(); g.arc(560 + i * 120, 200, 46, 0, 7); g.stroke(); g.beginPath(); g.arc(560 + i * 120 + (i - 1.5) * 20, 200, 46, -1.57, 1.57, i < 2); g.fill(); } })));
  board.position.set(-1.5, 1.8, -4.88); G.add(board);
  const mural = new THREE.Mesh(new THREE.PlaneGeometry(2.4, 1.6), M(canvasTex('mural', 512, 340, (g, w, h) => { g.fillStyle = '#f4e6c8'; g.fillRect(0, 0, w, h); g.fillStyle = '#d9483b'; g.font = 'bold 34px sans-serif'; g.fillText('COISAS QUE A', 20, 50); g.fillText('GENTE TINHA', 20, 92);
    srand(6); for (let i = 0; i < 6; i++) { g.fillStyle = '#fff'; g.save(); g.translate(40 + (i % 3) * 150, 130 + Math.floor(i / 3) * 100); g.rotate((rnd() - 0.5) * 0.3); g.fillRect(0, 0, 120, 80); g.fillStyle = '#ffe9a0'; g.beginPath(); g.arc(60, 40, 26, 0, 7); g.fill(); g.restore(); } })));
  mural.position.set(2.6, 1.8, -4.88); G.add(mural);
  srand(9); for (let r = 0; r < 3; r++) for (let c = 0; c < 4; c++) { const x = -3.6 + c * 2.2, z = -1.6 + r * 1.8; box(G, 1.0, 0.06, 0.6, M('#e8c08a'), x, 0.7, z); for (const [dx, dz] of [[-0.45, -0.25], [0.45, -0.25], [-0.45, 0.25], [0.45, 0.25]]) box(G, 0.05, 0.7, 0.05, M('#5a5a6a'), x + dx, 0, z + dz);
    box(G, 0.5, 0.05, 0.5, M(pick(['#e04848', '#3a8dde', '#ffd23f'])), x, 0.42, z + 0.6); }
  const sun = new THREE.Mesh(new THREE.PlaneGeometry(2, 1.4), new THREE.MeshBasicMaterial({ color: '#bfe8ff', fog: false })); sun.position.set(-5.88, 1.9, 0); sun.rotation.y = Math.PI / 2; G.add(sun);
  return G;
};

// Quarto do Caio (cap. 7)
SETS.bedroom = (o, L) => {
  const G = new THREE.Group(); const night = isNight(L);
  plane(G, 8, 7, M(canvasTex('bfloor', 256, 256, P.planks('#b88a58', '#8a5a30'), 2, 2)), 0, 0, 0);
  const wall = M(canvasTex('bwall', 256, 256, P.plaster('#7fa0e0', '#6a8ad0'), 2, 2));
  box(G, 8, 3, 0.2, wall, 0, 0, -3.5); box(G, 0.2, 3, 7, wall, -4, 0, 0);
  box(G, 2.0, 0.5, 1.0, M('#f2ece0'), -2.6, 0, -2.8); box(G, 2.0, 0.08, 1.05, M('#3a8dde'), -2.6, 0.5, -2.8);
  box(G, 1.8, 0.08, 0.8, M('#c48a52'), 1.6, 0.76, -3.0); for (const lx of [0.8, 2.4]) box(G, 0.07, 0.76, 0.07, M('#8a5a30'), lx, 0, -3.0);
  // pião, foto, caderno
  const top = cone(G, 0.12, 0.25, M('#e04848'), 1.0, 0.84, -3.0, 12); top.rotation.x = Math.PI;
  const ph = new THREE.Mesh(new THREE.PlaneGeometry(0.4, 0.3), M(canvasTex('foto', 256, 192, (g, w, h) => { g.fillStyle = '#fff'; g.fillRect(0, 0, w, h); g.fillStyle = '#16205a'; g.fillRect(12, 12, w - 24, h - 40); g.fillStyle = '#fff3b0'; g.beginPath(); g.arc(w / 2, h / 2 - 12, 40, 0, 7); g.fill(); })));
  ph.position.set(1.6, 0.98, -3.25); ph.rotation.x = -0.25; G.add(ph);
  box(G, 0.4, 0.05, 0.3, M('#7a5a3a'), 2.1, 0.8, -2.9);
  const win = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 1.2), new THREE.MeshBasicMaterial({ color: night ? '#141a52' : '#9fd6ff', fog: false })); win.position.set(-0.6, 1.8, -3.38); G.add(win);
  const pl = new THREE.PointLight('#ffd9a0', 6, 8, 1.4); pl.position.set(1.6, 2.2, -2.2); G.add(pl);
  return G;
};

// Estádio (campo, gols, arquibancadas com torcida, refletores, placar). opts: score, crowd (cores), confetti
SETS.stadium = (o, L) => {
  const G = new THREE.Group(); const night = isNight(L);
  const field = canvasTex('field', 1024, 1024, (g, w, h) => { for (let i = 0; i < 12; i++) { g.fillStyle = i % 2 ? '#4fa844' : '#5cb84f'; g.fillRect(0, i * h / 12, w, h / 12); }
    speckle(g, w, h, ['#459a3c', '#69c45a'], 900, 2, 6, 77, 0.5);
    g.strokeStyle = '#f6f6ee'; g.lineWidth = 7; g.strokeRect(24, 24, w - 48, h - 48); g.beginPath(); g.moveTo(24, h / 2); g.lineTo(w - 24, h / 2); g.stroke();
    g.beginPath(); g.arc(w / 2, h / 2, 95, 0, 7); g.stroke(); g.strokeRect(w / 2 - 210, 24, 420, 170); g.strokeRect(w / 2 - 210, h - 194, 420, 170);
    g.strokeRect(w / 2 - 100, 24, 200, 60); g.strokeRect(w / 2 - 100, h - 84, 200, 60); });
  plane(G, 70, 105, M(field), 0, 0, 0);
  plane(G, 400, 400, M(canvasTex('pista', 256, 256, P.plaster('#c8553d', '#a8442f'), 40, 40)), 0, -0.02, 0);
  // gols (z = ±52.5)
  for (const zs of [-1, 1]) { const z = zs * 52.5; const wm = M('#ffffff');
    cyl(G, 0.09, 0.09, 2.44, wm, -3.66, 0, z, 10); cyl(G, 0.09, 0.09, 2.44, wm, 3.66, 0, z, 10);
    const bar = mesh(new THREE.CylinderGeometry(0.09, 0.09, 7.5, 10), wm, 0, 2.44, z); bar.rotation.z = Math.PI / 2; G.add(bar);
    const net = new THREE.Mesh(new THREE.PlaneGeometry(7.3, 2.4), new THREE.MeshToonMaterial({ map: canvasTex('net', 256, 128, (g, w, h) => { g.clearRect(0, 0, w, h); g.strokeStyle = 'rgba(255,255,255,0.85)'; g.lineWidth = 2;
      for (let x = 0; x <= w; x += 12) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, h); g.stroke(); } for (let y = 0; y <= h; y += 12) { g.beginPath(); g.moveTo(0, y); g.lineTo(w, y); g.stroke(); } }), transparent: true, gradientMap: GRAD, side: THREE.DoubleSide }));
    net.position.set(0, 1.22, z + zs * 1.6); net.userData.noInk = true; G.add(net); }
  // arquibancadas com torcida
  const cols = o.crowd || ['#ffd23f', '#2f9e4a', '#ffffff', '#3a8dde', '#ffd23f', '#e04848'];
  const crowd = canvasTex('crowd' + cols.join(''), 1024, 256, (g, w, h) => { g.fillStyle = '#3a3a52'; g.fillRect(0, 0, w, h); srand(9);
    for (let r = 0; r < 10; r++) for (let i = 0; i < 90; i++) { const x = i * 11.4 + (r % 2) * 5, y = 14 + r * 24; g.fillStyle = pick(cols); g.beginPath(); g.arc(x, y, 6, 0, 7); g.fill(); g.fillStyle = pick(['#f2d2b4', '#c99068', '#8a5a3e', '#e0b088']); g.beginPath(); g.arc(x, y - 8, 4, 0, 7); g.fill(); } }, 4, 1);
  for (const [x, z, ry, len] of [[-50, 0, Math.PI / 2, 150], [50, 0, -Math.PI / 2, 150], [0, -75, 0, 120], [0, 75, Math.PI, 120]]) {
    for (let k = 0; k < 6; k++) { const st = mesh(new THREE.BoxGeometry(len, 2.2, 3), M(crowd), 0, 0, 0); const d = 4 + k * 3;
      st.position.set(x + Math.sin(ry) * -d * 0 + (x ? Math.sign(x) * d : 0), 1.1 + k * 2.2, z + (z ? Math.sign(z) * d : 0)); st.rotation.y = ry; G.add(st); } }
  // refletores
  for (const [x, z] of [[-46, -68], [46, -68], [-46, 68], [46, 68]]) { cyl(G, 0.5, 0.7, 34, M('#8a8aa0'), x, 0, z, 8); box(G, 7, 3.5, 1, M('#e8e8f0'), x, 34, z);
    if (night) glow(G, 'rgba(255,250,220,0.95)', x, 35.5, z, 22); }
  // placar
  if (o.score) { const sb = new THREE.Mesh(new THREE.PlaneGeometry(22, 7), new THREE.MeshBasicMaterial({ map: signTex(o.score, '#1d1d2b', '#ffd23f', 1024, 330, 'bold 130px sans-serif'), fog: false }));
    sb.position.set(0, 26, -88); G.add(sb); box(G, 23, 8, 1, M('#2a2a3a'), 0, 22, -88.8); }
  // bola
  if (o.ball) { const b = sph(G, 0.22, M(canvasTex('ball', 128, 64, (g, w, h) => { g.fillStyle = '#fff'; g.fillRect(0, 0, w, h); g.fillStyle = '#1d1d2b'; for (let i = 0; i < 6; i++) { g.beginPath(); g.arc(10 + i * 22, 20 + (i % 2) * 24, 7, 0, 7); g.fill(); } })), o.ball[0], 0.22, o.ball[1], 18); }
  if (night) { const pl = new THREE.PointLight('#fff6e0', 40, 160, 1.2); pl.position.set(0, 40, 0); G.add(pl); }
  return G;
};

// Vestiário (azulejo, armários, bancos, microfone)
SETS.locker = (o, L) => {
  const G = new THREE.Group();
  plane(G, 12, 10, M(canvasTex('lfloor', 512, 512, P.checker('#d9dde6', '#c4c9d6', 10), 2, 2)), 0, 0, 0);
  const tile = M(canvasTex('ltile', 256, 256, (g, w, h) => { g.fillStyle = '#e8f1f4'; g.fillRect(0, 0, w, h); g.strokeStyle = '#b9c8d0'; g.lineWidth = 3; for (let i = 0; i <= 8; i++) { g.beginPath(); g.moveTo(i * 32, 0); g.lineTo(i * 32, h); g.stroke(); g.beginPath(); g.moveTo(0, i * 32); g.lineTo(w, i * 32); g.stroke(); } }, 4, 2));
  box(G, 12, 3.6, 0.2, tile, 0, 0, -5); box(G, 0.2, 3.6, 10, tile, -6, 0, 0); box(G, 0.2, 3.6, 10, tile, 6, 0, 0);
  box(G, 12, 0.2, 10, M('#f4f6f8'), 0, 3.6, 0); // teto
  for (const lx of [-3, 0, 3]) { box(G, 1.6, 0.06, 0.3, M('#ffffff', { emissive: '#fff8e0', emissiveIntensity: 0.8 }), lx, 3.52, -1.5); }
  for (let i = 0; i < 9; i++) { const x = -4.8 + i * 1.2; box(G, 1.1, 2.2, 0.6, M(i % 2 ? '#ffffff' : '#f2f2f2'), x, 0, -4.6); box(G, 0.9, 0.5, 0.05, M('#e8e8e8'), x, 1.4, -4.28);
    const sh = new THREE.Mesh(new THREE.PlaneGeometry(0.8, 0.5), M(signTex(String(i + 2 === 10 ? 10 : i + 2), '#ffffff', '#1d1d2b', 256, 160, 'bold 110px sans-serif'))); sh.position.set(x, 1.65, -4.27); G.add(sh);
    const shirt = new THREE.Mesh(new THREE.PlaneGeometry(0.8, 0.9), M(i === 4 ? '#ffd23f' : '#ffffff')); shirt.position.set(x, 0.9, -4.28); G.add(shirt); }
  box(G, 9, 0.45, 0.6, M('#c48a52'), 0, 0, -3.4);
  const ban = new THREE.Mesh(new THREE.PlaneGeometry(4.2, 0.9), M(signTex(o.banner || 'VESTIÁRIO', '#1d3a8a', '#ffd23f', 1024, 220))); ban.position.set(0, 3.0, -4.88); G.add(ban);
  // pedestal com microfones (entrevista)
  cyl(G, 0.03, 0.03, 1.4, M('#333'), 0.9, 0, -1.2, 6); for (const [mx, mc] of [[0.8, '#e04848'], [0.95, '#3a8dde'], [1.05, '#ffd23f']]) sph(G, 0.08, M(mc), mx, 1.45, -1.15, 10);
  const pl = new THREE.PointLight('#fff0d8', 12, 14, 1.3); pl.position.set(0, 3.2, 1); G.add(pl);
  return G;
};

// Consultório médico (Novembro Azul): maca, mesa da médica, cartaz do corpo humano, porta com placa
SETS.clinic = (o, L) => {
  const G = new THREE.Group();
  plane(G, 10, 9, M(canvasTex('clfloor', 512, 512, P.checker('#dfe9f2', '#f6f8fb', 10), 2, 2)), 0, 0, 0);
  const wall = M(canvasTex('clwall', 256, 256, P.plaster('#cfe8ef', '#b9d8e2'), 3, 2));
  box(G, 10, 3.2, 0.2, wall, 0, 0, -3.6); box(G, 0.2, 3.2, 9, wall, -4.6, 0, 0.5); box(G, 0.2, 3.2, 9, wall, 4.6, 0, 0.5);
  box(G, 10, 0.18, 0.06, M('#3a8dde'), 0, 1.0, -3.48); // faixa azul na parede
  box(G, 10, 0.2, 9, M('#cfdde6'), 0, 3.2, 0.5); // teto
  // maca
  box(G, 2.1, 0.75, 0.85, M('#e8eef4'), -2.4, 0, -2.7); box(G, 2.1, 0.14, 0.85, M('#2f9e95'), -2.4, 0.75, -2.7);
  box(G, 2.1, 0.02, 0.55, M('#ffffff'), -2.4, 0.89, -2.7); const pil = box(G, 0.5, 0.16, 0.6, M('#ffffff'), -3.15, 0.89, -2.7);
  box(G, 0.5, 0.3, 0.5, M('#c9d3dc'), -1.0, 0, -2.4); // degrau
  // mesa da médica + computador
  box(G, 1.8, 0.08, 0.85, M('#c48a52'), 2.2, 0.76, -2.7); for (const lx of [1.4, 3.0]) box(G, 0.07, 0.76, 0.07, M('#8a5a30'), lx, 0, -2.7);
  box(G, 0.7, 0.45, 0.06, M('#22222e'), 2.5, 0.84, -2.95); box(G, 0.12, 0.1, 0.12, M('#22222e'), 2.5, 0.84, -2.9);
  const scr = new THREE.Mesh(new THREE.PlaneGeometry(0.6, 0.36), new THREE.MeshBasicMaterial({ color: '#9fd6ff', fog: false })); scr.position.set(2.5, 1.09, -2.91); G.add(scr);
  box(G, 0.3, 0.04, 0.22, M('#ffffff'), 1.8, 0.84, -2.6); cyl(G, 0.05, 0.05, 0.12, M('#3a8dde'), 1.55, 0.84, -2.5, 10);
  // cartaz do corpo humano
  const body = new THREE.Mesh(new THREE.PlaneGeometry(1.0, 1.4), M(canvasTex('corpo', 360, 504, (g, w, h) => { g.fillStyle = '#ffffff'; g.fillRect(0, 0, w, h); g.strokeStyle = '#3a8dde'; g.lineWidth = 12; g.strokeRect(0, 0, w, h);
    g.fillStyle = '#f2c8a8'; g.beginPath(); g.arc(w / 2, 90, 44, 0, 7); g.fill(); g.fillRect(w / 2 - 55, 140, 110, 190); g.fillRect(w / 2 - 95, 145, 34, 150); g.fillRect(w / 2 + 61, 145, 34, 150); g.fillRect(w / 2 - 50, 330, 40, 130); g.fillRect(w / 2 + 10, 330, 40, 130);
    g.fillStyle = '#e04848'; g.beginPath(); g.ellipse(w / 2 - 12, 190, 18, 22, 0, 0, 7); g.fill(); g.fillStyle = '#f08a5d'; g.beginPath(); g.ellipse(w / 2 + 8, 250, 26, 18, 0, 0, 7); g.fill();
    g.fillStyle = '#1d3a8a'; g.font = 'bold 34px sans-serif'; g.textAlign = 'center'; g.fillText('CORPO HUMANO', w / 2, h - 18); })));
  body.position.set(0.3, 1.9, -3.48); G.add(body);
  // cartaz Novembro Azul (laço)
  const nov = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 0.9), M(canvasTex('novazul', 480, 360, (g, w, h) => { g.fillStyle = '#1d4fa8'; g.fillRect(0, 0, w, h); g.strokeStyle = '#7fc0ff'; g.lineWidth = 26; g.lineCap = 'round';
    g.beginPath(); g.moveTo(170, 300); g.bezierCurveTo(200, 120, 300, 60, 240, 50); g.bezierCurveTo(180, 60, 280, 120, 310, 300); g.stroke();
    g.fillStyle = '#ffffff'; g.font = 'bold 44px sans-serif'; g.textAlign = 'center'; g.fillText('NOVEMBRO', w / 2, 300 + 0); g.fillText('AZUL', w / 2, 345); })));
  nov.position.set(-2.4, 2.1, -3.48); G.add(nov);
  // porta com placa
  box(G, 1.1, 2.2, 0.08, M('#b07a48'), 3.6, 0, -3.48); sph(G, 0.05, M('#ffd23f'), 3.25, 1.05, -3.42, 10);
  const pl2 = new THREE.Mesh(new THREE.PlaneGeometry(1.4, 0.32), M(signTex(o.door || 'CONSULTÓRIO', '#3a8dde', '#ffffff', 1024, 230))); pl2.position.set(3.6, 2.5, -3.47); G.add(pl2);
  // pia e armário na parede esquerda
  box(G, 0.6, 0.9, 1.4, M('#ffffff'), -4.2, 0, -0.6); box(G, 0.5, 0.06, 0.5, M('#c9d3dc'), -4.15, 0.9, -0.6);
  // cadeiras de espera
  for (const cz of [1.0, 1.7]) { box(G, 0.55, 0.06, 0.5, M('#3a8dde'), -4.0, 0.45, cz); box(G, 0.06, 0.55, 0.5, M('#3a8dde'), -4.3, 0.45, cz); for (const dz of [-0.2, 0.2]) box(G, 0.04, 0.45, 0.04, M('#5a5a6a'), -3.8, 0, cz + dz); }
  for (const lx of [-2, 1.5]) box(G, 1.6, 0.05, 0.3, M('#ffffff', { emissive: '#f4fbff', emissiveIntensity: 0.9 }), lx, 3.15, -1.0);
  const pl = new THREE.PointLight('#f4fbff', 6, 14, 1.3); pl.position.set(0, 2.3, 0.5); G.add(pl);
  return G;
};
