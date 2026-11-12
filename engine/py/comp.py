"""Compositor 2.5D: placa 3D (cor+profundidade) + cartões 2D + câmera viva + overlays.
Cada cena: dict com plate (spec), t0/t1 (s, timeline global), move, chars, fx, labels, focus, speaker."""
import math, json, os, random
import numpy as np, cv2
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont
import chars as CH
import ui2d as UI

OUT_W, OUT_H = 1920, 1080
TINT = {'night': (0.74, 0.78, 1.0), 'interior': (1.0, 0.95, 0.86), 'interior_day': (1.0, 0.98, 0.94), 'day': (1, 1, 1), 'golden': (1.06, 0.9, 0.74),
        'overcast': (0.9, 0.92, 0.97), 'storm': (0.72, 0.76, 0.88), 'space': (1, 1, 1), 'dawn': (1.0, 0.9, 0.84)}

def sstep(x):
    x = min(1, max(0, x)); return x * x * x * (x * (x * 6 - 15) + 10)
def eout(x):
    x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def back(x):
    x = min(1, max(0, x)); c1 = 1.70158; c3 = c1 + 1; return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

class Plate:
    def __init__(s, d, pid):
        s.col = cv2.cvtColor(cv2.imread(os.path.join(d, pid + '_color.png')), cv2.COLOR_BGR2RGB)
        dep = cv2.imread(os.path.join(d, pid + '_depth.png'))[:, :, ::-1].astype(np.float32)
        meta = json.load(open(os.path.join(d, pid + '.json')))
        s.depth = (dep[:, :, 0] / 255.0 + dep[:, :, 1] / 255.0 / 255.0 + dep[:, :, 2] / 255.0 / 65025.0) * meta['far']
        s.depth[s.depth <= 0.01] = meta['far']
        s.P = np.array(meta['P'], np.float64).reshape(4, 4).T  # three.js é column-major
        s.h, s.w = s.col.shape[:2]; s.spec = meta['spec']
        s.blur = None
    def project(s, x, y, z):
        v = s.P @ np.array([x, y, z, 1.0])
        return ((v[0] / v[3]) * 0.5 + 0.5) * s.w, (1 - ((v[1] / v[3]) * 0.5 + 0.5)) * s.h, v[3]

_plates = {}
def get_plate(d, pid):
    if pid not in _plates:
        if len(_plates) > 6: _plates.pop(next(iter(_plates)))
        _plates[pid] = Plate(d, pid)
    return _plates[pid]

# ---------------------------------------------------------------- movimentos de câmera
MOVES = {  # (zoom0, zoom1, dx0, dx1, dy0, dy1, par0, par1, roll0, roll1)
    'push':   (1.12, 1.26, 0, 0, 0, 0, -6, 10, 0, 0),
    'pull':   (1.30, 1.12, 0, 0, 0, 0, 10, -6, 0, 0),
    'panR':   (1.18, 1.22, -110, 110, 0, 0, -16, 16, 0, 0),
    'panL':   (1.18, 1.22, 110, -110, 0, 0, 16, -16, 0, 0),
    'tiltU':  (1.20, 1.24, 0, 0, 90, -90, 0, 6, 0, 0),
    'tiltD':  (1.20, 1.24, 0, 0, -90, 90, 0, -6, 0, 0),
    'orbit':  (1.18, 1.24, -60, 60, 0, 0, -26, 26, -1.2, 1.2),
    'hold':   (1.16, 1.22, -20, 20, 0, 0, -5, 5, 0, 0),
    'drama':  (1.14, 1.34, 0, 0, 0, 0, -4, 12, 0, 3.5),
    'whip':   (1.24, 1.20, 260, 0, 0, 0, 30, 0, 0, 0),
}

def cam_state(sc, t):
    D = max(0.01, sc['t1'] - sc['t0']); u = (t - sc['t0']) / D
    m = list(MOVES[sc.get('move', 'hold')])
    if 'zoom' in sc: m[0], m[1] = sc['zoom']
    e = eout(u * 1.6) if sc.get('move') == 'whip' else sstep(u)
    z = m[0] + (m[1] - m[0]) * e; dx = m[2] + (m[3] - m[2]) * e; dy = m[4] + (m[5] - m[4]) * e
    par = m[6] + (m[7] - m[6]) * e; roll = m[8] + (m[9] - m[8]) * e
    off = sc.get('offset', (0, 0))
    return z, dx + off[0], dy + off[1], par, roll

# ---------------------------------------------------------------- cache de cena
class SceneCache:
    def __init__(s, sc, pdir):
        s.sc = sc; s.pl = get_plate(pdir, sc['plate']['id'])
        H, W = s.pl.h, s.pl.w
        s.X, s.Y = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
        f = sc.get('focus')
        if f is None:
            cz = [s.pl.project(c['x'], 0, c['z'])[2] for c in sc.get('chars', [])]
            f = min(cz) if cz else 30.0
        s.zf = f
        s.inv = np.clip(s.zf / s.pl.depth - 1.0, -1.0, 2.5).astype(np.float32)
        col = s.pl.col
        if sc.get('dof', True) and cz_ok(sc):
            bl = cv2.GaussianBlur(col, (0, 0), sc.get('blur', 5.0))
            m = np.clip((s.pl.depth - s.zf * 1.6) / (s.zf * 2.0), 0, 1)[:, :, None]
            col = (col * (1 - m) + bl * m).astype(np.uint8)
        s.col = col
        tint = TINT.get(s.pl.spec.get('light', 'day'), (1, 1, 1))
        s.tint = np.array(tint, np.float32)
        s.chars = []
        for c in sc.get('chars', []):
            fx, fy, w = s.pl.project(c['x'], 0, c['z'])
            hh = 2.2 * CH.CAST[c['name']]['h'] * c.get('scale', 1.0)
            _, hy, _ = s.pl.project(c['x'], hh, c['z'])
            s.chars.append(dict(c, fx=fx, fy=fy, depth=w, px_h=max(8, fy - hy)))
        s.chars.sort(key=lambda c: -c['depth'])

def cz_ok(sc): return bool(sc.get('chars')) or sc.get('focus') is not None

_cache = {}
def scene_cache(sc, pdir):
    k = id(sc)
    if k not in _cache:
        if len(_cache) > 3: _cache.pop(next(iter(_cache)))
        _cache[k] = SceneCache(sc, pdir)
    return _cache[k]

def tinted(img, tint):
    a = np.array(img).astype(np.float32)
    a[:, :, :3] *= tint; return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')

@lru_cache(maxsize=2048)
def char_img(name, arms, face, look, extra, h, flip, tint):
    im = CH.card(name, arms, face, look, extra)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    s = h / 1000.0
    im = im.resize((max(4, int(600 * s)), max(4, int(1000 * s))), Image.LANCZOS)
    return tinted(im, np.array(tint, np.float32))

def blink(t, seed):
    return ((t + seed * 1.37) % 3.4) < 0.12

# ---------------------------------------------------------------- render de um quadro
def render_frame(sc, t, ctx):
    cache = scene_cache(sc, ctx['pdir'])
    pl = cache.pl
    z, dx, dy, par, roll = cam_state(sc, t)
    # tremor
    for (ts, amp) in sc.get('shake', []):
        u = t - ts
        if 0 <= u < 0.5:
            k = math.exp(-u * 9); dx += amp * k * math.sin(u * 70); dy += amp * k * math.cos(u * 55)
    # parallax por profundidade
    disp = cache.inv * (par * pl.w / 2560)
    img = cv2.remap(cache.col, cache.X - disp, cache.Y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    canvas = Image.fromarray(img).convert('RGBA')
    # personagens
    tint = tuple(float(v) for v in cache.tint)
    for c in cache.chars:
        cpar = par * pl.w / 2560 * float(np.clip(cache.zf / c['depth'] - 1.0, -1, 2.5))
        face = c.get('face', 'neutral')
        if c.get('faces'):
            for (tt, ff) in c['faces']:
                if t >= sc['t0'] + tt: face = ff
        arms = c.get('arms', 'hang')
        if c.get('arms_at'):
            for (tt, aa) in c['arms_at']:
                if t >= sc['t0'] + tt: arms = aa
        if sc.get('speaker') == c['name'] and ctx['talking'](t):
            face = 'talk' if ctx['env'](t) > 0.35 else ('neutral' if face in ('neutral', 'talk') else face)
        elif blink(t, hash(c['name']) % 7) and face in ('neutral', 'worried', 'sad', 'proud'):
            face = 'blink' if face == 'neutral' else face
        h = c['px_h']; breath = 1 + 0.012 * math.sin(t * 2.4 + hash(c['name']) % 5)
        im = char_img(c['name'], arms, face, tuple(c.get('look', (0, 0))), tuple(c.get('extra', ())), int(h * breath), bool(c.get('flip')), tint)
        x = c['fx'] + cpar; y = c['fy']
        # entrada andando
        if c.get('walk'):
            w0, w1, wx = c['walk']
            u = (t - sc['t0'] - w0) / max(0.01, w1 - w0)
            if u < 1: x += (1 - sstep(u)) * wx; y -= abs(math.sin(t * 9)) * h * 0.03 if u > 0 else 0
        if c.get('jump'):
            for jt in c['jump']:
                u = t - sc['t0'] - jt
                if 0 <= u < 0.4: y -= math.sin(u / 0.4 * math.pi) * h * 0.08
        sway = c.get('sway', 1.0) * 1.2 * math.sin(t * 2.0 + hash(c['name']) % 3)
        if face == 'laugh': sway += 4 * math.sin(t * 16)
        if 'shiver' in c.get('extra', ()): x += 3 * math.sin(t * 60)
        # sombra de contato
        sh = Image.new('RGBA', (int(h * 0.42), max(4, int(h * 0.07))), (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse([0, 0, sh.width - 1, sh.height - 1], fill=(20, 10, 30, 90))
        UI.paste(canvas, sh, x - sh.width / 2, y - sh.height / 2)
        if abs(sway) > 0.1:
            im2 = im.rotate(sway, resample=Image.BICUBIC, center=(im.width / 2, im.height * 0.975))
        else:
            im2 = im
        UI.paste(canvas, im2, x - im.width / 2, y - im.height * 0.975)
    # efeitos no espaço da placa
    for fx in sc.get('fx', []):
        FX[fx](canvas, t, sc)
    # câmera: zoom/pan/roll -> 1920x1080
    arr = np.array(canvas.convert('RGB'))
    OW, OH = ctx.get('out', (OUT_W, OUT_H))
    s = (OW / pl.w) * z
    cx, cy = pl.w / 2 + dx * pl.w / 2560, pl.h / 2 + dy * pl.w / 2560
    M = cv2.getRotationMatrix2D((cx, cy), roll, s)
    M[0, 2] += OW / 2 - cx; M[1, 2] += OH / 2 - cy
    out = cv2.warpAffine(arr, M, (OW, OH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    o = Image.fromarray(out).convert('RGBA')
    # rótulos (espaço da tela)
    for lb in (sc.get('labels', []) if ctx.get('overlays', True) else []):
        ts = sc['t0'] + lb['t']; te = sc['t0'] + lb.get('t_end', 999)
        if ts <= t < min(sc['t1'], te):
            k = back((t - ts) / 0.3); a = min(1, (min(sc['t1'], te) - t) / 0.2)
            im = label_img(lb['text'], lb.get('style', 'white'), lb.get('small'), 50 if OW > OH else 74)
            im = UI.with_alpha(UI.scaled(im, k), a)
            px, py = lb.get('pos', (OW // 2, 150 if OW > OH else 300))
            UI.paste(o, im, px - im.width / 2, py - im.height / 2)
    return o

@lru_cache(maxsize=256)
def label_img(text, style, small, sz=50):
    styles = {'white': ('#ffffff', '#1d1d2b'), 'yellow': ('#ffd23f', '#1d1d2b'), 'red': ('#e04848', '#ffffff'), 'blue': ('#3a8dde', '#ffffff'),
              'teal': ('#2f9e95', '#ffffff'), 'orange': ('#ff9f1c', '#ffffff'), 'purple': ('#7b5aa6', '#ffffff')}
    bg, fg = styles[style]
    return UI.pill(text, bg, fg, sz, small=small)

# ---------------------------------------------------------------- efeitos
def fx_rain(c, t, sc):
    d = ImageDraw.Draw(c); W, H = c.size; rs = random.Random(1)
    for i in range(260):
        x = (rs.random() * W + t * 300) % W; y = (rs.random() * H + t * 1600 * (0.7 + rs.random() * 0.6)) % H
        d.line([(x, y), (x - 8, y + 34)], fill=(190, 210, 255, 150), width=3)
def fx_snow(c, t, sc):
    d = ImageDraw.Draw(c); W, H = c.size; rs = random.Random(2)
    for i in range(220):
        r = 3 + rs.random() * 6; x = (rs.random() * W + 40 * math.sin(t + i)) % W; y = (rs.random() * H + t * (90 + rs.random() * 120)) % H
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 220))
def fx_twinkle(c, t, sc):
    d = ImageDraw.Draw(c); W, H = c.size; rs = random.Random(3)
    for i in range(40):
        x = rs.random() * W; y = rs.random() * H * 0.45; a = 0.5 + 0.5 * math.sin(t * 3 + i)
        r = 2 + 3 * a; d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 250, 220, int(200 * a)))
def fx_birds(c, t, sc):
    d = ImageDraw.Draw(c); W, H = c.size; rs = random.Random(4)
    for i in range(9):
        x = (rs.random() * W + t * 120 * (0.8 + rs.random() * 0.4)) % (W + 200) - 100; y = H * (0.12 + rs.random() * 0.2) + 10 * math.sin(t * 3 + i)
        f = 14 * math.sin(t * 10 + i)
        d.line([(x - 22, y - f), (x, y), (x + 22, y - f)], fill=(40, 30, 50, 230), width=5)
def fx_dust(c, t, sc):
    d = ImageDraw.Draw(c); W, H = c.size; rs = random.Random(5)
    for i in range(50):
        x = (rs.random() * W + t * 25) % W; y = (rs.random() * H - t * 12) % H; r = 2 + rs.random() * 3
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 240, 200, 70))
def fx_crabs(c, t, sc):
    W, H = c.size; rs = random.Random(6)
    for i in range(7):
        x = (rs.random() * W + t * 60 * (1 if i % 2 else -1)) % W; y = H * (0.78 + rs.random() * 0.15)
        im = crab_img(); UI.paste(c, im, x, y - abs(math.sin(t * 12 + i)) * 6)
def fx_turtles(c, t, sc):
    W, H = c.size; rs = random.Random(7)
    for i in range(14):
        x = (rs.random() * W * 0.8 + W * 0.1 + t * 18 * (rs.random() - 0.3)) % W; y = H * (0.7 + rs.random() * 0.25) - t * 6
        UI.paste(c, turtle_img(), x, y + 4 * math.sin(t * 8 + i))
def fx_lightning(c, t, sc):
    for ts in sc.get('flashes', []):
        u = t - (sc['t0'] + ts)
        if 0 <= u < 0.15:
            c.alpha_composite(Image.new('RGBA', c.size, (230, 240, 255, int(160 * (1 - u / 0.15)))))
def fx_waves(c, t, sc):
    pass
def fx_dark(c, t, sc):
    c.alpha_composite(Image.new('RGBA', c.size, (5, 5, 25, 70)))
FX = {'rain': fx_rain, 'snow': fx_snow, 'twinkle': fx_twinkle, 'birds': fx_birds, 'dust': fx_dust, 'crabs': fx_crabs, 'turtles': fx_turtles,
      'lightning': fx_lightning, 'dark': fx_dark}

@lru_cache(None)
def crab_img():
    def fn(d):
        d.ell(40, 34, 30, 18, UI.hexc('#e8603a'), w=4)
        for sx in (-1, 1):
            d.ell(40 + sx * 34, 18, 10, 9, UI.hexc('#e8603a'), w=4)
            for k in range(3): d.line([(40 + sx * 20, 40 + k * 4), (40 + sx * 40, 52 + k * 5)], UI.OL, 4)
        d.ell(32, 22, 4, 4, UI.OL, w=0); d.ell(48, 22, 4, 4, UI.OL, w=0)
    return UI.sprite(80, 64, fn, k=2)
@lru_cache(None)
def turtle_img():
    def fn(d):
        for (x, y) in ((14, 18), (50, 18), (14, 42), (50, 42)): d.ell(x, y, 8, 6, UI.hexc('#6ab06a'), w=3)
        d.ell(32, 30, 20, 16, UI.hexc('#3f8a5a'), w=4); d.ell(32, 8, 8, 7, UI.hexc('#6ab06a'), w=3)
    return UI.sprite(64, 56, fn, k=2)

# ---------------------------------------------------------------- legenda (frase inteira, embaixo)
FONT = (__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'fonts', 'Poppins-Bold.ttf'))
@lru_cache(maxsize=512)
def subtitle_img(text):
    f = ImageFont.truetype(FONT, 46)
    words = text.split(); lines = []; cur = ''
    for w in words:
        tt = (cur + ' ' + w).strip()
        if f.getlength(tt) > 1450 and cur: lines.append(cur); cur = w
        else: cur = tt
    lines.append(cur)
    lh = 60; H = lh * len(lines) + 20; W = 1600
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        d.text((W / 2, 10 + lh * i + lh / 2), ln, font=f, fill=(255, 255, 255, 255), anchor='mm', stroke_width=7, stroke_fill=(16, 12, 24, 255))
    return im
