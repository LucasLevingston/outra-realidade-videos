"""Modo 2D flat do motor (padrão "Rafa, CLT × iFood"): cenários vetoriais em SVG, personagens cabeça-de-feijão em SVG,
câmera 2D (push/pull/pan/drama + tremor), rótulos, cards, celulares, balões e legenda karaokê, tudo numa composição
HyperFrames (HTML + GSAP) renderizada em MP4 1080x1920. Sem 3D, sem desfoque, cores chapadas e contorno fino.

uso (num projeto):  python3 PROJ/flat_scenes.py build | mix | render OUT.mp4
O flat_scenes.py do projeto cria `C = flat2d.Comp(PROJ, total)`, monta as cenas com C.scene(...) / C.add(...) /
C.caption(...) / C.sfx(...) e chama `flat2d.main(C)`. Modelo: projetos/short-pix-milhao/flat_scenes.py.
"""
import os, sys, json, html, shutil, subprocess, re, glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
HF_DIR = os.environ.get('HF_DIR', os.path.expanduser('~/.cache/outra-realidade-hf'))
OL = '#24203a'          # contorno ameixa/grafite
W, H = 1080, 1920

def esc(s): return html.escape(str(s), quote=True)

# ------------------------------------------------------------------ cenários (SVG 1080x1920, desenhados maiores que a tela para a câmera)
def svg(body, w=W, h=H):
    return f'<svg class="bg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">{body}</svg>'

def grad(id_, c1, c2, vertical=True):
    a = 'x1="0" y1="0" x2="0" y2="1"' if vertical else 'x1="0" y1="0" x2="1" y2="0"'
    return f'<linearGradient id="{id_}" {a}><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'

_gid = [0]
def gid(p='g'):
    _gid[0] += 1; return f'{p}{_gid[0]}'

def bg_sunburst(c1='#ffd84d', c2='#ffab2e', cx=540, cy=900, n=22):
    rays = []
    import math
    for k in range(n):
        a0 = 2 * math.pi * k / n; a1 = a0 + math.pi / n
        p = [(cx, cy), (cx + 3000 * math.cos(a0), cy + 3000 * math.sin(a0)), (cx + 3000 * math.cos(a1), cy + 3000 * math.sin(a1))]
        rays.append('<polygon points="' + ' '.join(f'{x:.0f},{y:.0f}' for x, y in p) + f'" fill="{c1}"/>')
    g = gid('rg')
    return svg(f'<defs><radialGradient id="{g}" cx=".5" cy=".47" r=".6"><stop offset="0" stop-color="#fff6c8" stop-opacity=".9"/>'
               f'<stop offset="1" stop-color="{c2}" stop-opacity="0"/></radialGradient></defs>'
               f'<rect width="{W}" height="{H}" fill="{c2}"/>{"".join(rays)}<rect width="{W}" height="{H}" fill="url(#{g})"/>')

def bg_navy(c='#232657'):
    g = gid('nv')
    return svg(f'<defs><radialGradient id="{g}" cx=".5" cy=".4" r=".8"><stop offset="0" stop-color="#2e3270"/><stop offset="1" stop-color="{c}"/></radialGradient></defs>'
               f'<rect width="{W}" height="{H}" fill="url(#{g})"/>')

def _windows(x0, y0, x1, y1, col, step=(58, 70), size=(26, 34), seed=1, lit=1.0, off='#3a3566'):
    rng = np.random.default_rng(seed); out = []
    y = y0
    while y + size[1] < y1:
        x = x0
        while x + size[0] < x1:
            c = col if rng.random() < lit else off
            out.append(f'<rect x="{x}" y="{y}" width="{size[0]}" height="{size[1]}" rx="3" fill="{c}"/>')
            x += step[0]
        y += step[1]
    return ''.join(out)

def _building(x, w, top, base, fill, win, seed, lit=1.0, off=None):
    off = off or fill
    return (f'<rect x="{x}" y="{top}" width="{w}" height="{base - top}" fill="{fill}" stroke="{OL}" stroke-width="5"/>'
            + _windows(x + 22, top + 30, x + w - 10, base - 20, win, seed=seed, lit=lit, off=off))

def bg_city(mode='day', seed=3):
    """mode: day | night | sunset"""
    if mode == 'night':
        sky = grad('skyN', '#1b1840', '#43317a'); bcols = ['#2c2a5e', '#35306b', '#29265a', '#3b3473', '#312d66']; win = '#ffd54a'; lit = 0.55; off = '#24224d'
    elif mode == 'sunset':
        sky = grad('skyS', '#f07a6a', '#ffc58a'); bcols = ['#6b4a8a', '#7d5590', '#5d4280', '#865e94', '#6f4c86']; win = '#ffd98a'; lit = 0.6; off = '#553a73'
    else:
        sky = grad('skyD', '#7fd0f5', '#c5ecfb'); bcols = ['#ff8a7a', '#5fc3a8', '#ffcf5a', '#7aa8ff', '#f59ac0']; win = '#ffffff'; lit = 0.9; off = '#e9f3ff'
    sid = re.search(r'id="(\w+)"', sky).group(1)
    rng = np.random.default_rng(seed); b = []
    # fundo: prédios distantes (sem janelas)
    x = -40
    while x < W + 40:
        w = int(rng.integers(120, 200)); top = int(rng.integers(820, 1050))
        fc = '#9fb8e6' if mode == 'day' else ('#4a3f86' if mode == 'night' else '#a0688c')
        b.append(f'<rect x="{x}" y="{top}" width="{w}" height="{1500 - top}" fill="{fc}"/>'); x += w - 10
    x = -30; k = 0
    while x < W + 30:
        w = int(rng.integers(170, 260)); top = int(rng.integers(900, 1180))
        b.append(_building(x, w, top, 1520, bcols[k % len(bcols)], win, seed + k, lit, off)); x += w + int(rng.integers(-5, 12)); k += 1
    extra = ''
    if mode == 'night':
        stars = ''.join(f'<circle class="tw" cx="{int(rng.integers(0, W))}" cy="{int(rng.integers(40, 760))}" r="{rng.uniform(2, 4.5):.1f}" fill="#fff"/>' for _ in range(40))
        extra = stars + f'<circle cx="820" cy="300" r="78" fill="#fff3c4" stroke="{OL}" stroke-width="5"/>'
    elif mode == 'sunset':
        extra = f'<circle cx="300" cy="760" r="120" fill="#fff0b0"/>'
    else:
        extra = (f'<circle cx="190" cy="250" r="90" fill="#ffe36a"/>'
                 + ''.join(f'<g class="cloud" transform="translate({cx},{cy})"><ellipse cx="0" cy="0" rx="90" ry="46" fill="#fff"/><ellipse cx="70" cy="-20" rx="70" ry="50" fill="#fff"/><ellipse cx="-70" cy="10" rx="60" ry="36" fill="#fff"/></g>'
                           for cx, cy in ((560, 300), (900, 520), (300, 620))))
    road = (f'<rect x="0" y="1520" width="{W}" height="400" fill="{"#3b3a52" if mode != "day" else "#5d5f73"}"/>'
            f'<rect x="0" y="1510" width="{W}" height="26" fill="{"#57557a" if mode != "day" else "#c9c9d6"}" stroke="{OL}" stroke-width="4"/>'
            + ''.join(f'<rect x="{x}" y="1740" width="110" height="16" rx="6" fill="#f2efe6"/>' for x in range(20, W, 220)))
    return svg(f'<defs>{sky}</defs><rect width="{W}" height="{H}" fill="url(#{sid})"/>{extra}{"".join(b)}{road}')

def _window_frame(x, y, w, h, sky1, sky2, sun=None):
    g = gid('win')
    s = f'<circle cx="{x + w * .62}" cy="{y + h * .62}" r="{w * .16}" fill="{sun}"/>' if sun else ''
    return (f'<defs>{grad(g, sky1, sky2)}</defs><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="url(#{g})" stroke="{OL}" stroke-width="7"/>{s}'
            f'<line x1="{x + w / 2}" y1="{y}" x2="{x + w / 2}" y2="{y + h}" stroke="{OL}" stroke-width="7"/>'
            f'<line x1="{x}" y1="{y + h / 2}" x2="{x + w}" y2="{y + h / 2}" stroke="{OL}" stroke-width="7"/>')

def bg_room(kind='bedroom', light='day'):
    """kind: bedroom | kitchen | living | restaurant ; light: day | dawn | sunset | night"""
    walls = {'day': '#f6e3b8', 'dawn': '#f3d2b3', 'sunset': '#f2b98f', 'night': '#3b3a6a'}
    floor = {'day': '#c98f5e', 'dawn': '#b98563', 'sunset': '#b07357', 'night': '#2a2850'}
    skies = {'day': ('#79cdf3', '#c6eefc', '#ffe36a'), 'dawn': ('#f7a07c', '#ffe0a6', '#fff2b0'),
             'sunset': ('#e9707a', '#ffbe7d', '#fff0b0'), 'night': ('#14123a', '#2c2565', '#fff3c4')}
    wall = walls[light]; fl = floor[light]; s1, s2, sun = skies[light]
    body = [f'<rect width="{W}" height="{H}" fill="{wall}"/>',
            f'<rect x="0" y="1380" width="{W}" height="540" fill="{fl}"/><rect x="0" y="1370" width="{W}" height="22" fill="#fff" opacity=".55"/>']
    if kind == 'bedroom':
        body += [_window_frame(600, 330, 360, 420, s1, s2, sun),
                 f'<rect x="120" y="360" width="250" height="320" rx="8" fill="#7ec8a0" stroke="{OL}" stroke-width="6"/><circle cx="245" cy="490" r="70" fill="#ffd36a" stroke="{OL}" stroke-width="6"/>',
                 f'<rect x="40" y="1180" width="640" height="230" rx="30" fill="#5b7fd6" stroke="{OL}" stroke-width="7"/>'
                 f'<rect x="60" y="1140" width="200" height="90" rx="30" fill="#fff" stroke="{OL}" stroke-width="6"/>'
                 f'<rect x="20" y="1060" width="40" height="360" rx="12" fill="#8a5a3c" stroke="{OL}" stroke-width="6"/>',
                 f'<rect x="780" y="1180" width="200" height="220" rx="10" fill="#a26b45" stroke="{OL}" stroke-width="6"/><rect x="840" y="1080" width="70" height="100" rx="8" fill="#ffd36a" stroke="{OL}" stroke-width="6"/>']
    elif kind == 'kitchen':
        body += [_window_frame(380, 300, 330, 380, s1, s2, sun),
                 f'<rect x="0" y="880" width="{W}" height="500" fill="#e9e2d4" stroke="{OL}" stroke-width="6"/>'
                 + ''.join(f'<rect x="{x}" y="900" width="250" height="230" rx="12" fill="#6fbf9f" stroke="{OL}" stroke-width="6"/><circle cx="{x + 220}" cy="1015" r="9" fill="{OL}"/>' for x in (20, 290, 560, 830))
                 + f'<rect x="0" y="860" width="{W}" height="36" fill="#d2c4a8" stroke="{OL}" stroke-width="6"/>',
                 ''.join(f'<rect x="{x}" y="130" width="230" height="150" rx="10" fill="#6fbf9f" stroke="{OL}" stroke-width="6"/>' for x in (40, 790))]
    elif kind == 'living':
        body += [_window_frame(560, 300, 420, 470, s1, s2, sun),
                 f'<rect x="90" y="360" width="300" height="220" rx="8" fill="#ffffff" stroke="{OL}" stroke-width="6"/><path d="M110 560 L190 450 L250 520 L300 470 L370 560Z" fill="#7ec8a0"/>',
                 f'<rect x="60" y="1110" width="960" height="300" rx="50" fill="#c0586a" stroke="{OL}" stroke-width="7"/>'
                 f'<rect x="100" y="1030" width="880" height="160" rx="40" fill="#d06878" stroke="{OL}" stroke-width="7"/>']
    elif kind == 'classroom':
        body += [f'<rect x="70" y="250" width="940" height="470" rx="14" fill="#2f6b4f" stroke="{OL}" stroke-width="10"/>'
                 f'<rect x="60" y="720" width="960" height="26" rx="8" fill="#a26b45" stroke="{OL}" stroke-width="6"/>'
                 f'<text x="140" y="420" font-family="Pop" font-size="86" fill="#f4f0e8" opacity=".9">2x + 3 = 11</text>'
                 f'<text x="140" y="560" font-family="Pop" font-size="86" fill="#f4f0e8" opacity=".9">x = ?</text>'
                 f'<circle cx="880" cy="140" r="70" fill="#fff" stroke="{OL}" stroke-width="7"/><line x1="880" y1="140" x2="880" y2="95" stroke="{OL}" stroke-width="7"/><line x1="880" y1="140" x2="915" y2="150" stroke="{OL}" stroke-width="7"/>',
                 ''.join(f'<rect x="{x}" y="1430" width="300" height="40" rx="10" fill="#c98f5e" stroke="{OL}" stroke-width="6"/><rect x="{x + 30}" y="1470" width="24" height="180" fill="{OL}"/><rect x="{x + 246}" y="1470" width="24" height="180" fill="{OL}"/>' for x in (60, 720))]
    elif kind == 'restaurant':
        body += [''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="300" stroke="{OL}" stroke-width="5"/><path d="M{x - 70} 360 Q{x} 250 {x + 70} 360Z" fill="#ffcf5a" stroke="{OL}" stroke-width="6"/>' for x in (200, 540, 880)),
                 f'<rect x="0" y="560" width="{W}" height="20" fill="#c06a4a"/>'
                 + ''.join(f'<rect x="{x}" y="640" width="150" height="190" rx="10" fill="#fff8e6" stroke="{OL}" stroke-width="5"/>' for x in (90, 465, 840)),
                 f'<rect x="40" y="1330" width="1000" height="70" rx="16" fill="#e85d4a" stroke="{OL}" stroke-width="7"/>'
                 + ''.join(f'<ellipse cx="{x}" cy="1330" rx="80" ry="22" fill="#fff" stroke="{OL}" stroke-width="5"/>' for x in (180, 540, 900))]
    return svg(''.join(body))

# ------------------------------------------------------------------ personagens cabeça-de-feijão
SKIN = {'a': '#c98a5e', 'b': '#e0a878', 'c': '#8d5a3b', 'd': '#f2c49b'}
CAST = {
    'caio': dict(skin='a', hair='curly', hc='#1d1a26', shirt='#4a9be8', pants='#2f3a66', shoe='#1d1a26'),
    'mae':  dict(skin='b', hair='bun', hc='#b9b4c4', shirt='#8f6cc9', pants='#5a4688', shoe='#3a2a4a', glasses=True),
    'tia':  dict(skin='c', hair='bigcurly', hc='#8a3a2e', shirt='#ef6fa2', pants='#6a3a5a', shoe='#3a2a4a', glasses=True, earrings=True),
    'beto': dict(skin='b', hair='short', hc='#3a2616', shirt='#2fbf71', pants='#2f3a66', shoe='#1d1a26'),
    'irmao': dict(skin='b', hair='curly', hc='#3a2616', shirt='#ffb347', pants='#3c3c5a', shoe='#1d1a26'),
    'pai':  dict(skin='b', hair='short', hc='#6b6878', shirt='#3a8dde', pants='#3c3c5a', shoe='#1d1a26', glasses=True),
    'vo':   dict(skin='d', hair='bun', hc='#eceaf2', shirt='#6fbf9f', pants='#4a6a5a', shoe='#3a2a4a', glasses=True, earrings=True),
    'prof': dict(skin='c', hair='short', hc='#9a96a8', shirt='#a26b45', pants='#3c3c5a', shoe='#1d1a26', glasses=True),
    'p1':   dict(skin='d', hair='short', hc='#5a3a22', shirt='#ffb347', pants='#3c3c5a', shoe='#1d1a26'),
    'p2':   dict(skin='c', hair='short', hc='#1d1a26', shirt='#5fc3a8', pants='#3c3c5a', shoe='#1d1a26'),
    'p3':   dict(skin='b', hair='bob', hc='#e0b040', shirt='#e85d4a', pants='#3c3c5a', shoe='#1d1a26'),
}

def _arm(x0, y0, pts, col, skin):
    d = f'M{x0},{y0} ' + ' '.join(f'L{x},{y}' for x, y in pts)
    hx, hy = pts[-1]
    return (f'<path d="{d}" fill="none" stroke="{OL}" stroke-width="40" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="27" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="{hx}" cy="{hy}" r="25" fill="{skin}" stroke="{OL}" stroke-width="7"/>')

ARMS = {  # (esquerdo, direito) — pontos a partir dos ombros (-92,-395) e (92,-395)
    'hang':    ([(-120, -300), (-125, -215)], [(120, -300), (125, -215)]),
    'up':      ([(-160, -500), (-175, -640)], [(160, -500), (175, -640)]),
    'phone':   ([(-120, -300), (-125, -215)], [(130, -330), (55, -440)]),
    'phone2':  ([(-115, -320), (-45, -430)], [(115, -320), (45, -430)]),
    'point':   ([(-120, -300), (-125, -215)], [(150, -420), (210, -520)]),
    'wave':    ([(-120, -300), (-125, -215)], [(165, -470), (190, -600)]),
    'hip':     ([(-150, -320), (-100, -250)], [(150, -320), (100, -250)]),
    'shrug':   ([(-160, -340), (-215, -420)], [(160, -340), (215, -420)]),
    'hug':     ([(-140, -330), (-30, -320)], [(140, -330), (30, -320)]),
    'cheer':   ([(-150, -480), (-140, -620)], [(120, -300), (125, -215)]),
}

def _hair(kind, hc, cy):
    if kind == 'curly':
        pts = [(-130, -40), (-100, -95), (-50, -125), (0, -135), (50, -125), (100, -95), (130, -40), (150, 10), (-150, 10)]
        return ''.join(f'<circle cx="{x}" cy="{cy + y}" r="{58 if abs(x) < 140 else 40}" fill="{hc}" stroke="{OL}" stroke-width="6"/>' for x, y in pts) + \
               ''.join(f'<circle cx="{x}" cy="{cy + y}" r="56" fill="{hc}"/>' for x, y in pts[:7])
    if kind == 'bigcurly':
        pts = [(-170, 40), (-160, -40), (-120, -105), (-55, -140), (0, -150), (55, -140), (120, -105), (160, -40), (170, 40), (-175, 110), (175, 110)]
        return ''.join(f'<circle cx="{x}" cy="{cy + y}" r="66" fill="{hc}" stroke="{OL}" stroke-width="6"/>' for x, y in pts) + \
               ''.join(f'<circle cx="{x}" cy="{cy + y}" r="62" fill="{hc}"/>' for x, y in pts)
    if kind == 'bun':
        return (f'<circle cx="0" cy="{cy - 165}" r="55" fill="{hc}" stroke="{OL}" stroke-width="6"/>'
                f'<path d="M-150,{cy + 10} Q-150,{cy - 150} 0,{cy - 150} Q150,{cy - 150} 150,{cy + 10} Q100,{cy - 80} 0,{cy - 85} Q-100,{cy - 80} -150,{cy + 10}Z" fill="{hc}" stroke="{OL}" stroke-width="6"/>')
    if kind == 'bob':
        return f'<path d="M-165,{cy + 70} Q-170,{cy - 160} 0,{cy - 150} Q170,{cy - 160} 165,{cy + 70} L120,{cy + 70} Q110,{cy - 70} 0,{cy - 80} Q-110,{cy - 70} -120,{cy + 70}Z" fill="{hc}" stroke="{OL}" stroke-width="6"/>'
    return f'<path d="M-148,{cy - 5} Q-150,{cy - 150} 0,{cy - 145} Q150,{cy - 150} 148,{cy - 5} Q90,{cy - 85} 0,{cy - 88} Q-90,{cy - 85} -148,{cy - 5}Z" fill="{hc}" stroke="{OL}" stroke-width="6"/>'

def _face(cid, face, cy, glasses):
    ey = cy + 5
    brows = {'surprise': (-28, -28, 0), 'worried': (-18, -18, 12), 'angry': (-14, -14, -14)}.get(face, (-22, -22, 0))
    b = (f'<path d="M-78,{ey + brows[0] - 10 + brows[2]} Q-50,{ey + brows[0] - 28} -22,{ey + brows[0] - 12}" fill="none" stroke="{OL}" stroke-width="8" stroke-linecap="round"/>'
         f'<path d="M22,{ey + brows[1] - 12} Q50,{ey + brows[1] - 28} 78,{ey + brows[1] - 10 + brows[2]}" fill="none" stroke="{OL}" stroke-width="8" stroke-linecap="round"/>')
    if face in ('happy', 'laugh'):
        eyes = (f'<path d="M-68,{ey + 4} Q-50,{ey - 16} -32,{ey + 4}" fill="none" stroke="{OL}" stroke-width="9" stroke-linecap="round"/>'
                f'<path d="M32,{ey + 4} Q50,{ey - 16} 68,{ey + 4}" fill="none" stroke="{OL}" stroke-width="9" stroke-linecap="round"/>')
    else:
        r = 17 if face == 'surprise' else 14
        eyes = (f'<circle cx="-50" cy="{ey}" r="{r}" fill="{OL}"/><circle cx="50" cy="{ey}" r="{r}" fill="{OL}"/>'
                f'<circle cx="-45" cy="{ey - 5}" r="5" fill="#fff"/><circle cx="55" cy="{ey - 5}" r="5" fill="#fff"/>')
    my = cy + 78
    closed = {'happy': f'<path d="M-40,{my - 8} Q0,{my + 30} 40,{my - 8}" fill="#7a2a3a" stroke="{OL}" stroke-width="7" stroke-linejoin="round"/>',
              'laugh': f'<path d="M-52,{my - 14} Q0,{my + 52} 52,{my - 14}Z" fill="#7a2a3a" stroke="{OL}" stroke-width="7"/><path d="M-26,{my + 14} Q0,{my + 32} 26,{my + 14}" fill="#e86a7a"/>',
              'surprise': f'<ellipse cx="0" cy="{my + 4}" rx="24" ry="30" fill="#7a2a3a" stroke="{OL}" stroke-width="7"/>',
              'worried': f'<path d="M-32,{my + 8} Q-16,{my - 6} 0,{my + 6} Q16,{my + 16} 32,{my + 2}" fill="none" stroke="{OL}" stroke-width="8" stroke-linecap="round"/>',
              'sleepy': f'<path d="M-22,{my + 4} L22,{my + 4}" stroke="{OL}" stroke-width="8" stroke-linecap="round"/>',
              }.get(face, f'<path d="M-34,{my - 2} Q0,{my + 22} 34,{my - 2}" fill="none" stroke="{OL}" stroke-width="8" stroke-linecap="round"/>')
    opn = f'<ellipse cx="0" cy="{my + 6}" rx="34" ry="26" fill="#7a2a3a" stroke="{OL}" stroke-width="7"/><ellipse cx="0" cy="{my + 18}" rx="18" ry="9" fill="#e86a7a"/>'
    if face == 'sleepy':
        eyes = (f'<path d="M-70,{ey} L-30,{ey}" stroke="{OL}" stroke-width="9" stroke-linecap="round"/><path d="M30,{ey} L70,{ey}" stroke="{OL}" stroke-width="9" stroke-linecap="round"/>')
    gl = ''
    if glasses:
        gl = (f'<circle cx="-50" cy="{ey}" r="36" fill="#ffffff" fill-opacity=".18" stroke="{OL}" stroke-width="7"/><circle cx="50" cy="{ey}" r="36" fill="#ffffff" fill-opacity=".18" stroke="{OL}" stroke-width="7"/>'
              f'<line x1="-14" y1="{ey}" x2="14" y2="{ey}" stroke="{OL}" stroke-width="7"/>')
    return (f'<g id="{cid}-eyes" style="transform-box:fill-box;transform-origin:50% 50%">{eyes}</g>{b}{gl}'
            f'<ellipse cx="-92" cy="{cy + 48}" rx="26" ry="15" fill="#ff7a8a" opacity=".45"/><ellipse cx="92" cy="{cy + 48}" rx="26" ry="15" fill="#ff7a8a" opacity=".45"/>'
            f'<g id="{cid}-mc">{closed}</g><g id="{cid}-mo" style="opacity:0">{opn}</g>')

def char(cid, who, x, y, scale=1.0, pose='hang', face='neutral', flip=False, props=(), headonly=False):
    """Personagem em pé com os pés em (x, y) na tela. props: phone, helmet, sunglasses, card, jacket."""
    c = CAST[who]; sk = SKIN[c['skin']]; cy = -575
    st = c['shirt']
    if 'jacket' in props: st = '#e8483a'
    al, ar = ARMS[pose]
    arms = _arm(-92, -395, al, st, sk) + _arm(92, -395, ar, st, sk)
    phone = ''
    if 'phone' in props:
        hx, hy = ar[-1]
        phone = f'<rect x="{hx - 30}" y="{hy - 70}" width="62" height="105" rx="12" fill="#2a2840" stroke="{OL}" stroke-width="6"/><rect x="{hx - 21}" y="{hy - 60}" width="44" height="78" rx="6" fill="#7fe0c0"/>'
        arms = _arm(-92, -395, al, st, sk) + _arm(92, -395, ar, st, sk) + phone
    legs = (f'<rect x="-66" y="-210" width="48" height="200" rx="20" fill="{c["pants"]}" stroke="{OL}" stroke-width="7"/>'
            f'<rect x="18" y="-210" width="48" height="200" rx="20" fill="{c["pants"]}" stroke="{OL}" stroke-width="7"/>'
            f'<ellipse cx="-48" cy="-6" rx="40" ry="20" fill="{c["shoe"]}" stroke="{OL}" stroke-width="6"/><ellipse cx="48" cy="-6" rx="40" ry="20" fill="{c["shoe"]}" stroke="{OL}" stroke-width="6"/>')
    torso = f'<path d="M-112,-200 L-112,-360 Q-112,-430 -40,-432 L40,-432 Q112,-430 112,-360 L112,-200 Z" fill="{st}" stroke="{OL}" stroke-width="8"/>'
    if 'jacket' in props:
        torso += f'<rect x="-112" y="-330" width="224" height="26" fill="#f4f0e8"/>'
    head = (f'<circle cx="-150" cy="{cy + 20}" r="26" fill="{sk}" stroke="{OL}" stroke-width="6"/><circle cx="150" cy="{cy + 20}" r="26" fill="{sk}" stroke="{OL}" stroke-width="6"/>'
            f'<path d="M0,{cy - 140} C110,{cy - 140} 158,{cy - 70} 156,{cy + 10} C154,{cy + 100} 95,{cy + 140} 0,{cy + 142} C-95,{cy + 140} -154,{cy + 100} -156,{cy + 10} C-158,{cy - 70} -110,{cy - 140} 0,{cy - 140}Z" fill="{sk}" stroke="{OL}" stroke-width="8"/>')
    if c.get('earrings'):
        head += f'<circle cx="-152" cy="{cy + 60}" r="12" fill="#ffd23f" stroke="{OL}" stroke-width="4"/><circle cx="152" cy="{cy + 60}" r="12" fill="#ffd23f" stroke="{OL}" stroke-width="4"/>'
    hair = _hair(c['hair'], c['hc'], cy)
    back_hair = hair if c['hair'] == 'bigcurly' else ''
    front_hair = '' if c['hair'] == 'bigcurly' else hair
    if c['hair'] == 'bigcurly':
        front_hair = f'<path d="M-150,{cy - 20} Q-120,{cy - 140} 0,{cy - 140} Q120,{cy - 140} 150,{cy - 20} Q60,{cy - 95} 0,{cy - 92} Q-60,{cy - 95} -150,{cy - 20}Z" fill="{c["hc"]}" stroke="{OL}" stroke-width="6"/>'
    extras = ''
    if 'sunglasses' in props:
        extras += f'<rect x="-100" y="{cy - 22}" width="200" height="54" rx="22" fill="{OL}"/><rect x="-80" y="{cy - 14}" width="60" height="8" rx="4" fill="#fff" opacity=".5"/>'
    if 'pimple' in props:
        extras += f'<circle cx="38" cy="{cy - 70}" r="17" fill="#e8483a" stroke="{OL}" stroke-width="5"/><circle cx="33" cy="{cy - 75}" r="5" fill="#fff" opacity=".7"/>'
    if 'helmet' in props:
        front_hair = f'<path d="M-170,{cy + 40} Q-175,{cy - 175} 0,{cy - 172} Q175,{cy - 175} 170,{cy + 40}Z" fill="#e8483a" stroke="{OL}" stroke-width="8"/><rect x="-120" y="{cy - 35}" width="240" height="60" rx="26" fill="#3a3a5a" stroke="{OL}" stroke-width="6"/>'
        back_hair = ''
    face_g = _face(cid, face, cy, c.get('glasses'))
    shadow = '<ellipse cx="0" cy="0" rx="135" ry="20" fill="#000" opacity=".16"/>'
    body = '' if headonly else f'{shadow}{legs}{torso}{arms}'
    fl = ' scale(-1,1)' if flip else ''
    inner = (f'<g id="{cid}-b">{body}<g id="{cid}-h" style="transform-box:fill-box;transform-origin:50% 90%">{back_hair}{head}{face_g}{front_hair}{extras}</g></g>')
    vb_top = -800
    w = 560 * scale; h = 830 * scale
    return (f'<svg id="{cid}" class="ch" viewBox="-280 {vb_top} 560 830" width="{w:.0f}" height="{h:.0f}" '
            f'style="left:{x - w / 2:.0f}px;top:{y - h + 30 * scale:.0f}px;transform:{"scaleX(-1)" if flip else "none"}"><g>{inner}</g></svg>')

# ------------------------------------------------------------------ objetos
def moto_svg(x, y, scale=1.0, mid='moto'):
    w = 620 * scale; h = 380 * scale
    return (f'<svg id="{mid}" class="ch" viewBox="-310 -360 620 380" width="{w:.0f}" height="{h:.0f}" style="left:{x - w / 2:.0f}px;top:{y - h:.0f}px">'
            f'<ellipse cx="0" cy="8" rx="270" ry="20" fill="#000" opacity=".15"/>'
            f'<circle cx="-190" cy="-80" r="84" fill="#2a2840" stroke="{OL}" stroke-width="8"/><circle cx="-190" cy="-80" r="34" fill="#c9c9d6" stroke="{OL}" stroke-width="6"/>'
            f'<circle cx="190" cy="-80" r="84" fill="#2a2840" stroke="{OL}" stroke-width="8"/><circle cx="190" cy="-80" r="34" fill="#c9c9d6" stroke="{OL}" stroke-width="6"/>'
            f'<path d="M-200,-90 L-60,-150 L120,-150 L200,-90 L150,-110 L-150,-110Z" fill="#3a3a5a" stroke="{OL}" stroke-width="7"/>'
            f'<path d="M-160,-170 Q-80,-250 40,-230 L170,-200 L150,-140 L-170,-140Z" fill="#3b82f6" stroke="{OL}" stroke-width="8"/>'
            f'<path d="M-150,-190 Q-80,-215 -10,-205 L-20,-170 L-150,-170Z" fill="#2a2840" stroke="{OL}" stroke-width="6"/>'
            f'<line x1="150" y1="-200" x2="205" y2="-300" stroke="{OL}" stroke-width="14" stroke-linecap="round"/><line x1="180" y1="-300" x2="240" y2="-300" stroke="{OL}" stroke-width="14" stroke-linecap="round"/>'
            f'<circle cx="230" cy="-215" r="22" fill="#ffe36a" stroke="{OL}" stroke-width="6"/></svg>')

def flipphone(scale=1.0, screen='#7fe0c0', text=''):
    """Celular antigo de tampinha (aberto)."""
    w = 260 * scale; h = 520 * scale
    return (f'<svg viewBox="0 0 260 520" width="{w:.0f}" height="{h:.0f}">'
            f'<rect x="20" y="10" width="220" height="230" rx="34" fill="#9aa3b8" stroke="{OL}" stroke-width="8"/>'
            f'<rect x="45" y="40" width="170" height="170" rx="10" fill="{screen}" stroke="{OL}" stroke-width="6"/>'
            f'<text x="130" y="140" font-family="Pop" font-size="44" text-anchor="middle" fill="{OL}">{esc(text)}</text>'
            f'<rect x="100" y="236" width="60" height="24" fill="#7a8298" stroke="{OL}" stroke-width="6"/>'
            f'<rect x="20" y="256" width="220" height="254" rx="34" fill="#b5bccd" stroke="{OL}" stroke-width="8"/>'
            + ''.join(f'<rect x="{50 + 60 * (k % 3)}" y="{300 + 50 * (k // 3)}" width="44" height="32" rx="8" fill="#eef0f6" stroke="{OL}" stroke-width="4"/>' for k in range(12))
            + '</svg>')

def can_svg(scale=1.0, label='MESADA'):
    w = 300 * scale; h = 360 * scale
    return (f'<svg viewBox="0 0 300 360" width="{w:.0f}" height="{h:.0f}">'
            f'<ellipse cx="150" cy="320" rx="120" ry="28" fill="#000" opacity=".15"/>'
            f'<path d="M40,60 L40,300 Q150,340 260,300 L260,60Z" fill="#c9ced9" stroke="{OL}" stroke-width="8"/>'
            f'<ellipse cx="150" cy="60" rx="110" ry="30" fill="#e6e9f0" stroke="{OL}" stroke-width="8"/>'
            f'<rect x="100" y="52" width="100" height="14" rx="6" fill="{OL}"/>'
            f'<rect x="40" y="140" width="220" height="90" fill="#ffd23f" stroke="{OL}" stroke-width="6"/>'
            f'<text x="150" y="203" font-family="Pop" font-size="44" text-anchor="middle" fill="{OL}">{esc(label)}</text></svg>')

ICONS = {
    'phone': f'<svg viewBox="0 0 100 100" width="110" height="110"><rect x="28" y="8" width="44" height="84" rx="10" fill="#2a2840" stroke="{OL}" stroke-width="5"/><rect x="34" y="18" width="32" height="58" rx="4" fill="#7fe0c0"/><path d="M8,30 Q2,50 8,70" fill="none" stroke="#e8483a" stroke-width="6" stroke-linecap="round"/><path d="M92,30 Q98,50 92,70" fill="none" stroke="#e8483a" stroke-width="6" stroke-linecap="round"/></svg>',
    'x': f'<svg viewBox="0 0 100 100" width="90" height="90"><circle cx="50" cy="50" r="44" fill="#e8483a" stroke="{OL}" stroke-width="6"/><path d="M33,33 L67,67 M67,33 L33,67" fill="none" stroke="#fff" stroke-width="11" stroke-linecap="round"/></svg>',
    'check': f'<svg viewBox="0 0 100 100" width="90" height="90"><circle cx="50" cy="50" r="44" fill="#2fbf71" stroke="{OL}" stroke-width="6"/><path d="M28,52 L44,67 L73,36" fill="none" stroke="#fff" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    'mic': f'<svg viewBox="0 0 100 100" width="80" height="80"><rect x="35" y="10" width="30" height="52" rx="15" fill="#fff" stroke="{OL}" stroke-width="5"/><path d="M22,48 Q22,78 50,78 Q78,78 78,48" fill="none" stroke="#fff" stroke-width="7"/><line x1="50" y1="78" x2="50" y2="92" stroke="#fff" stroke-width="7"/></svg>',
    'smile': f'<svg viewBox="0 0 100 100" width="100%" height="100%"><circle cx="50" cy="50" r="45" fill="#ffd23f" stroke="{OL}" stroke-width="5"/><circle cx="35" cy="40" r="6" fill="{OL}"/><circle cx="65" cy="40" r="6" fill="{OL}"/><path d="M28,58 Q50,82 72,58" fill="none" stroke="{OL}" stroke-width="7" stroke-linecap="round"/></svg>',
}

# ------------------------------------------------------------------ composição
CSS = '''
@font-face { font-family: Pop; src: url(assets/Poppins-Bold.ttf); font-weight: 700; }
html, body { margin: 0; background: #000; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Pop, sans-serif; font-weight: 700; }
.clip { position: absolute; }
.scene { left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }
.shk, .cam { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 50% 50%; }
.bg { position: absolute; left: 0; top: 0; }
.ch { position: absolute; overflow: visible; }
.ov { position: absolute; }
.pillv { left: 50%; translate: -50% 0; background: #22213a; border: 7px solid #f4f0e8; border-radius: 70px; padding: 10px 46px 14px; text-align: center; color: #3ee08a;
         font-size: 96px; line-height: 1; white-space: nowrap; box-shadow: 0 10px 0 rgba(20,16,28,.35); }
.pillv .l { display: block; color: #f4f0e8; font-size: 26px; letter-spacing: 3px; margin-bottom: 6px; }
.pillv:after { content: ""; position: absolute; left: 50%; bottom: -26px; margin-left: -20px; border: 20px solid transparent; border-top-color: #f4f0e8; border-bottom: 0; }
.money { color: #3ee08a; font-size: 56px; -webkit-text-stroke: 9px #14101c; paint-order: stroke fill; white-space: nowrap; }
.tilt { font-size: 74px; color: #ffd23f; -webkit-text-stroke: 12px #14101c; paint-order: stroke fill; white-space: nowrap; }
.card { width: 270px; height: 300px; background: #fff; border: 7px solid #24203a; border-radius: 26px; box-shadow: 0 10px 0 rgba(20,16,28,.3);
        display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; color: #24203a; font-size: 34px; line-height: 1.05; }
.card .s { font-size: 22px; color: #e8483a; margin-top: 6px; }
.stamp { border: 12px solid #e8483a; color: #e8483a; border-radius: 24px; padding: 6px 40px; font-size: 110px; letter-spacing: 4px; background: rgba(255,255,255,.9); white-space: nowrap; }
.lp { left: 120px; width: 840px; height: 104px; box-sizing: border-box; background: #fff; border: 6px solid #24203a; border-radius: 60px; display: flex; align-items: center;
      justify-content: space-between; padding: 0 44px; font-size: 54px; color: #e8483a; box-shadow: 0 8px 0 rgba(20,16,28,.3); }
.lp .n { color: #24203a; font-size: 34px; letter-spacing: 1px; }
.lp.tot { background: #2fbf71; color: #fff; }
.lp.tot .n { color: #fff; }
.note { left: 0; width: 1080px; text-align: center; color: #c9c9e6; font-size: 24px; }
.ph { width: 620px; height: 1000px; background: #22213a; border: 8px solid #14101c; border-radius: 74px; box-sizing: border-box; padding: 22px; box-shadow: 0 16px 0 rgba(20,16,28,.3); }
.ph .scr { position: relative; width: 100%; height: 100%; background: #f4f0e8; border-radius: 54px; overflow: hidden; }
.ph .hd { background: #2fbf71; color: #fff; padding: 46px 34px 22px; font-size: 40px; line-height: 1.05; }
.ph .hd small { display: block; font-size: 24px; opacity: .9; }
.msg { position: absolute; left: 30px; max-width: 470px; min-width: 260px; background: #fff; border: 5px solid #24203a; border-radius: 26px; padding: 16px 24px; font-size: 36px; color: #24203a; line-height: 1.1; }
.msg small { display: block; font-size: 20px; color: #2fa86a; }
.notif { position: absolute; left: 24px; right: 24px; top: 70px; background: #fff; border: 5px solid #24203a; border-radius: 30px; padding: 20px 26px; color: #24203a; }
.notif .a { font-size: 30px; color: #6b6890; letter-spacing: 1px; }
.notif .t { font-size: 52px; line-height: 1.05; }
.notif .v { font-size: 52px; white-space: nowrap; color: #2fa86a; line-height: 1.05; }
.bubble { left: 50%; translate: -50% 0; width: 880px; box-sizing: border-box; background: #fff; color: #24203a; border: 7px solid #24203a; border-radius: 40px;
          padding: 44px 40px 34px; font-size: 58px; line-height: 1.1; text-align: center; box-shadow: 0 10px 0 rgba(20,16,28,.3); }
.bubble .tag { position: absolute; left: 34px; top: -28px; color: #fff; font-size: 30px; padding: 4px 22px; border-radius: 30px; border: 5px solid #24203a; }
.bubble .tail { position: absolute; left: 50%; bottom: -34px; width: 50px; height: 50px; background: #fff; border-right: 7px solid #24203a; border-bottom: 7px solid #24203a; transform: translateX(-50%) rotate(45deg); }
.word { left: 0; width: 1080px; text-align: center; font-size: 106px; color: #fff; letter-spacing: 1px; -webkit-text-stroke: 15px #14101c; paint-order: stroke fill; text-shadow: 0 8px 0 rgba(20,16,28,.45); }
.word.key { color: #ffd23f; }
.flash { left: 0; top: 0; width: 1080px; height: 1920px; background: #fff; }
.ring { border: 12px solid #e8483a; border-radius: 50%; }
'''


class Comp:
    def __init__(s, proj, total):
        s.proj = proj; s.total = round(total, 3); s.els = []; s.tl = []; s.n = 0; s.sfx_list = []; s.amb = []; s.music = []; s.scenes = []

    def nid(s, p='e'):
        s.n += 1; return f'{p}{s.n}'

    # --- cena: fundo + personagens dentro da câmera
    def scene(s, t0, t1, bg, chars=(), cam='push', amount=0.07, shake=(), rot=0.0, origin='50% 50%', x0=0, x1=0, mood=None, amb=None, whoosh=True):
        i = s.nid('s'); dur = t1 - t0
        s.els.append(f'<div id="{i}" class="clip scene" data-start="{t0:.3f}" data-duration="{dur:.3f}"><div id="{i}k" class="shk"><div id="{i}c" class="cam" style="transform-origin:{origin}">{bg}{"".join(chars)}</div></div></div>')
        a, b = {'push': (1.0, 1.0 + amount), 'pull': (1.0 + amount, 1.0), 'hold': (1.0, 1.0 + amount * 0.4), 'drama': (1.0, 1.0 + amount * 1.8)}.get(cam, (1.03, 1.03 + amount * 0.3))
        r1 = rot if cam == 'drama' else 0
        if cam in ('panR', 'panL'):
            x0, x1 = (30, -30) if cam == 'panR' else (-30, 30)
        s.tl.append(f'tl.fromTo("#{i}c",{{scale:{a},x:{x0},rotation:0}},{{scale:{b},x:{x1},rotation:{r1},duration:{dur:.3f},ease:"sine.inOut"}},{t0:.3f});')
        for ts in shake:
            s.tl.append(f'tl.fromTo("#{i}k",{{x:0,y:0}},{{keyframes:[{{x:-22,y:10,duration:.035}},{{x:18,y:-12,duration:.035}},{{x:-12,y:6,duration:.035}},{{x:8,y:-4,duration:.035}},{{x:0,y:0,duration:.08}}]}},{ts:.3f});')
            s.sfx(ts, 'thud', 0.9)
        if whoosh and t0 > 0.05: s.sfx(t0 - 0.08, 'whoosh', 0.6)
        if amb: s.amb.append((t0, t1, amb))
        s.scenes.append((t0, t1, i))
        return i

    def life(s, cid, t0, t1, talk=(), blink=True, bob=6):
        """Respiração (balanço), piscadas a cada ~2,6 s e boca mexendo nas falas."""
        n = max(1, int((t1 - t0) / 0.9))
        s.tl.append(f'tl.fromTo("#{cid}-b",{{y:0}},{{y:-{bob},duration:0.9,repeat:{n},yoyo:true,ease:"sine.inOut"}},{t0:.3f});')
        s.tl.append(f'tl.fromTo("#{cid}-h",{{rotation:-1.2}},{{rotation:1.2,duration:1.3,repeat:{max(1, int((t1 - t0) / 1.3))},yoyo:true,ease:"sine.inOut"}},{t0:.3f});')
        if blink:
            t = t0 + 0.9
            while t < t1 - 0.2:
                s.tl.append(f'tl.to("#{cid}-eyes",{{scaleY:0.08,duration:0.06,yoyo:true,repeat:1}},{t:.3f});'); t += 2.6
        for a, b in talk:
            t = a; k = 0
            while t < b:
                op = 1 if k % 2 == 0 else 0
                s.tl.append(f'tl.set("#{cid}-mo",{{opacity:{op}}},{t:.3f});tl.set("#{cid}-mc",{{opacity:{1 - op}}},{t:.3f});'); t += 0.11; k += 1
            s.tl.append(f'tl.set("#{cid}-mo",{{opacity:0}},{b:.3f});tl.set("#{cid}-mc",{{opacity:1}},{b:.3f});')

    def tween(s, sel, frm, to, t):
        s.tl.append(f'tl.fromTo("{sel}",{json.dumps(frm)},{json.dumps(to)},{t:.3f});')

    # --- elementos de tela (por cima da câmera)
    def add(s, html_, t0, t1, x=None, y=None, anim='pop', rot=0, sound='pop', vol=0.7, z=None, cls='', origin='50% 50%'):
        i = s.nid('o'); st = []
        if x is not None: st.append(f'left:{x}px')
        if y is not None: st.append(f'top:{y}px')
        if z is not None: st.append(f'z-index:{z}')
        st.append(f'transform-origin:{origin}')
        s.els.append(f'<div id="{i}" class="clip ov {cls}" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" style="{";".join(st)}">{html_}</div>')
        if anim == 'pop':
            s.tl.append(f'tl.fromTo("#{i}",{{scale:0.2,opacity:0,rotation:{rot - 8}}},{{scale:1,opacity:1,rotation:{rot},duration:0.32,ease:"back.out(2.2)"}},{t0:.3f});')
        elif anim == 'up':
            s.tl.append(f'tl.fromTo("#{i}",{{y:120,opacity:0,rotation:{rot}}},{{y:0,opacity:1,rotation:{rot},duration:0.3,ease:"back.out(1.6)"}},{t0:.3f});')
        elif anim == 'left':
            s.tl.append(f'tl.fromTo("#{i}",{{x:-700,rotation:{rot}}},{{x:0,rotation:{rot},duration:0.35,ease:"power3.out"}},{t0:.3f});')
        elif anim == 'right':
            s.tl.append(f'tl.fromTo("#{i}",{{x:700,rotation:{rot}}},{{x:0,rotation:{rot},duration:0.35,ease:"power3.out"}},{t0:.3f});')
        elif anim == 'float':
            s.tl.append(f'tl.fromTo("#{i}",{{y:40,opacity:0}},{{y:-220,opacity:1,duration:{t1 - t0:.3f},ease:"power1.out"}},{t0:.3f});')
            s.tl.append(f'tl.to("#{i}",{{opacity:0,duration:0.25}},{t1 - 0.25:.3f});')
        elif anim == 'stamp':
            s.tl.append(f'tl.fromTo("#{i}",{{scale:2.6,opacity:0,rotation:{rot}}},{{scale:1,opacity:1,rotation:{rot},duration:0.22,ease:"power3.in"}},{t0:.3f});')
        else:
            s.tl.append(f'tl.set("#{i}",{{rotation:{rot}}},{t0:.3f});')
        if sound: s.sfx(t0, sound, vol)
        return i

    def caption(s, words, keys=(), y=830):
        """words: [(texto, t0, t1)] — uma palavra por vez, karaokê; keys em amarelo."""
        K = set(k.upper() for k in keys)
        for j, (w, a, b) in enumerate(words):
            nxt = words[j + 1][1] if j + 1 < len(words) else b + 0.35
            end = min(nxt - 0.01, b + 0.35) if j + 1 < len(words) else b + 0.35
            if end - a < 0.06: continue
            i = s.nid('w'); key = ' key' if w.upper().strip('?!.,') in K else ''
            s.els.append(f'<div id="{i}" class="clip word{key}" style="top:{y}px" data-start="{a:.3f}" data-duration="{end - a:.3f}">{esc(w.upper())}</div>')
            s.tl.append(f'tl.fromTo("#{i}",{{scale:1.2}},{{scale:1,duration:0.13,ease:"power2.out"}},{a:.3f});')

    def flash(s, t):
        i = s.nid('f')
        s.els.append(f'<div id="{i}" class="clip flash" data-start="{t:.3f}" data-duration="0.22"></div>')
        s.tl.append(f'tl.fromTo("#{i}",{{opacity:1}},{{opacity:0,duration:0.2,ease:"none"}},{t:.3f});')

    def sfx(s, t, name, vol=0.8):
        s.sfx_list.append((max(0.0, t), name, vol))

    # --- saída
    def build(s):
        out = os.path.join(s.proj, 'hf'); os.makedirs(os.path.join(out, 'assets'), exist_ok=True)
        shutil.copy(os.path.join(HERE, '..', 'fonts', 'Poppins-Bold.ttf'), os.path.join(out, 'assets'))
        shutil.copy(os.path.join(HF_DIR, 'node_modules/gsap/dist/gsap.min.js'), os.path.join(out, 'assets', 'gsap.min.js'))
        doc = ('<!doctype html><html><head><meta charset="utf-8"><style>' + CSS + '</style></head><body>'
               f'<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-fps="30" data-duration="{s.total}">'
               + '\n'.join(s.els) +
               '<script src="assets/gsap.min.js"></script><script>const tl = gsap.timeline({ paused: true });\n' + '\n'.join(s.tl) +
               f'\ntl.set({{}}, {{}}, {s.total});window.__timelines = window.__timelines || {{}};window.__timelines["root"] = tl;</script></div></body></html>')
        open(os.path.join(out, 'index.html'), 'w').write(doc)
        json.dump({'name': os.path.basename(s.proj.rstrip('/'))}, open(os.path.join(out, 'hyperframes.json'), 'w'))
        print(f'flat2d: {len(s.els)} elementos, {len(s.scenes)} cenas, {s.total:.2f}s -> {out}/index.html')

    def mix(s, music):
        """music: [(t0, t1, mood)] com crossfade de 1 s. Níveis fixos: música −6 dB da voz, efeitos ≤ −6 dB e pico ≤ 0,7× voz, −14 LUFS."""
        import longaudio as LA
        import scipy.io.wavfile as wf
        SR = LA.SR; N = int(SR * s.total)
        sr, v = wf.read(os.path.join(s.proj, 'audio', 'short.wav')); v = v.astype(np.float32) / (32768 if v.dtype == np.int16 else 1)
        narr = np.zeros(N); narr[:min(N, len(v))] = v[:N]
        mus = np.zeros(N)
        for k, (a, b, mood) in enumerate(music):
            a0 = max(0, a - 0.5); b0 = min(s.total, b + 0.5); blk = LA.music_block(mood, b0 - a0 + 0.1)
            n = min(len(blk), N - int(a0 * SR)); env = np.ones(n)
            f = int(SR * 1.0)
            if k > 0: env[:f] = np.linspace(0, 1, f)
            if k < len(music) - 1: env[-f:] = np.minimum(env[-f:], np.linspace(1, 0, f))
            mus[int(a0 * SR):int(a0 * SR) + n] += blk[:n] * env
        L = LA.sfx_lib(); fx = np.zeros(N + SR * 3)
        for t, name, vol in sorted(s.sfx_list):
            if name in L: LA.add(fx, L[name] / (np.max(np.abs(L[name])) + 1e-9) * vol, t)
        amb = np.zeros(N + SR)
        for a, b, kind in s.amb:
            LA.add(amb, LA.ambience(kind, b - a) * 0.5, a)
        fx = fx[:N] + amb[:N] * 0.35
        Wn = int(0.05 * SR); nw = N // Wn
        wr = lambda x: np.sqrt(np.mean(x[:nw * Wn].reshape(nw, Wn) ** 2, axis=1) + 1e-12)
        vr = wr(narr); gate = vr > vr.max() * 10 ** (-30 / 20)
        grms = lambda x, g: np.sqrt(np.mean(x[:nw * Wn].reshape(nw, Wn)[g] ** 2) + 1e-12)
        V = grms(narr, gate); mus *= V * 0.5 / grms(mus, gate)
        sr_ = wr(fx); sg = sr_ > sr_.max() * 10 ** (-40 / 20)
        fx *= min(V * 0.5 / grms(fx, sg), 0.7 * np.max(np.abs(narr)) / np.max(np.abs(fx)))
        db = lambda a, b: 20 * np.log10(a / b)
        print(f'música vs voz: {db(grms(mus, gate), V):+.2f} dB | efeitos vs voz: {db(grms(fx, sg), V):+.2f} dB | pico efeitos/voz: {np.max(np.abs(fx)) / np.max(np.abs(narr)):.2f}')
        mx = narr + mus + fx; d = os.path.join(s.proj, 'mix'); os.makedirs(d, exist_ok=True)
        for nm, x in (('narr', narr), ('music', mus), ('sfx', fx)): wf.write(os.path.join(d, nm + '.wav'), SR, x.astype(np.float32))
        pre = os.path.join(d, 'pre.wav'); wf.write(pre, SR, mx.astype(np.float32))
        o = subprocess.run(['ffmpeg', '-hide_banner', '-i', pre, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
        I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', o)[-1]); g = -14 - I
        print(f'LUFS antes {I:.2f}, ganho {g:+.2f} dB')
        wf.write(os.path.join(d, 'lin.wav'), SR, (mx * 10 ** (g / 20)).astype(np.float32))
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(d, 'lin.wav'), '-af', 'alimiter=limit=0.891:level=false:attack=2:release=60',
                        '-t', str(s.total), '-c:a', 'pcm_s16le', os.path.join(d, 'mix.wav')], check=True)
        print('sfx:', len(s.sfx_list), 'efeitos; 1 a cada', round(s.total / max(1, len(s.sfx_list)), 2), 's')

    def render(s, out_mp4, workers=2):
        hf = os.path.join(s.proj, 'hf')
        env = dict(os.environ, HYPERFRAMES_TELEMETRY='0')
        if not env.get('HYPERFRAMES_BROWSER_PATH'):
            c = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux64/chrome')) or [x for x in ('/usr/bin/google-chrome', '/usr/bin/chromium') if os.path.exists(x)]
            if c: env['HYPERFRAMES_BROWSER_PATH'] = c[-1]
        raw = out_mp4 + '.video.mp4'
        cmd = ['npx', '--prefix', HF_DIR, 'hyperframes', 'render', os.path.abspath(hf), '-o', os.path.abspath(raw), '-q', 'delivery', '-w', str(workers), '--no-browser-gpu']
        print(' '.join(cmd), flush=True); subprocess.run(cmd, check=True, env=env, cwd=HF_DIR)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-i', os.path.join(s.proj, 'mix', 'mix.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                        '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', '-shortest', out_mp4], check=True)
        print(out_mp4, round(os.path.getsize(out_mp4) / 1e6, 1), 'MB')


def main(C, music):
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'build'
    if cmd in ('build', 'all'): C.build()
    if cmd in ('mix', 'all'): C.mix(music)
    if cmd == 'render': C.render(sys.argv[2])
