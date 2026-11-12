"""Personagens 2D (cartões) no estilo cabeça-de-feijão: contorno ameixa, cores chapadas, membros finos.
card(name, pose) -> RGBA 600x1000, sola dos pés em y=975 (centro x=300)."""
import math
from functools import lru_cache
from PIL import Image, ImageDraw

OL = (52, 26, 52, 255)
K = 2  # supersample

def hx(h, a=255):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)

CAST = {
    'dito':  dict(skin='#e9c29b', shirt='#2f9e95', stripe='#257f78', pants='#59607a', shoes='#7a4a2a', hair='#f2f2f2', hat='bucket', hatc='#f2c230', must=True, h=1.0),
    'cida':  dict(skin='#f2d2b4', shirt='#e86a8a', stripe='#ffffff', pants='#e86a8a', shoes='#7a4a2a', hair='#c9c9d4', bun=True, glasses=True, dress=True, h=0.94),
    'caio':  dict(skin='#f4d8bc', shirt='#e04848', stripe='#ffd23f', pants='#3d6fb6', shoes='#ffffff', hair='#5a3a22', spiky=True, h=0.72),
    'caio20': dict(skin='#f4d8bc', shirt='#3a8dde', stripe='#ffffff', pants='#3d4a6a', shoes='#ffffff', hair='#5a3a22', spiky=True, h=1.0),
    'lia':   dict(skin='#f7e0c8', shirt='#7b5aa6', stripe='#7b5aa6', pants='#3a3a5a', shoes='#3a3a5a', hair='#1e1a2a', pony=True, glasses=True, coat=True, h=0.97),
    'beto':  dict(skin='#f0c09a', shirt='#5cb85c', stripe='#4a9a4a', pants='#3d6fb6', shoes='#e04848', hair='#3a2618', hat='cap', hatc='#e04848', shorts=True, h=0.98),
    'ze':    dict(skin='#d9a77c', shirt='#f08a3c', stripe='#d0702a', pants='#4a4a5a', shoes='#5a3a2a', hair='#3a2a1a', hat='cap', hatc='#3a8dde', beard=True, h=1.0),
    'filho': dict(skin='#d9a77c', shirt='#ffd23f', stripe='#e0b020', pants='#3d6fb6', shoes='#ffffff', hair='#2a1a10', spiky=True, h=0.9),
    'anchor': dict(skin='#f2d2b4', shirt='#2a3a6a', stripe='#2a3a6a', pants='#2a3a6a', shoes='#1a1a1a', hair='#3a2a1a', tie='#d42a2a', h=1.0),
    'astro': dict(skin='#f2d2b4', shirt='#eef0f4', stripe='#d9483b', pants='#eef0f4', shoes='#9a9aa8', hair='#c9c9d4', bun=True, h=0.96),
    'prof':  dict(skin='#e8b48a', shirt='#ffd23f', stripe='#ffd23f', pants='#9d7ad6', shoes='#5a3a2a', hair='#2a1a10', bun=True, glasses=True, dress=True, h=0.96),
    'menina': dict(skin='#f2d2b4', shirt='#9d7ad6', stripe='#ffffff', pants='#9d7ad6', shoes='#ffffff', hair='#c87a3a', pony=True, dress=True, h=0.7),
    'locutor': dict(skin='#e8b48a', shirt='#ffffff', stripe='#d9483b', pants='#3a3a5a', shoes='#1a1a1a', hair='#1a1a1a', headset=True, h=1.0),
    'lobo': dict(skin='#9a9bab', shirt='#7b5aa6', stripe='#674b8c', pants='#4a4a5a', shoes='#5c5c6c', hair='#7a7b8b', wolf=True, h=1.0),
    'p1': dict(skin='#f2d2b4', shirt='#3a8dde', stripe='#2a6aae', pants='#4a4a5a', shoes='#1a1a1a', hair='#3a2a1a', h=0.98),
    'p2': dict(skin='#c99068', shirt='#ffd23f', stripe='#e0b020', pants='#5a6aa0', shoes='#e04848', hair='#1a1a1a', pony=True, h=0.95),
    'p3': dict(skin='#f4d8bc', shirt='#9d7ad6', stripe='#7b5aa6', pants='#3a3a3a', shoes='#ffffff', hair='#d8b060', spiky=True, h=0.97),
    'p4': dict(skin='#e0b088', shirt='#5cbf9a', stripe='#4aa080', pants='#6a4a3a', shoes='#5a3a2a', hair='#8a8a8a', hat='cap', hatc='#ffd23f', h=0.99),
    'p5': dict(skin='#8a5a3e', shirt='#f08a5d', stripe='#d0703a', pants='#3a4a6a', shoes='#ffffff', hair='#1a1a1a', h=0.98),
    'p6': dict(skin='#f2d2b4', shirt='#e86a8a', stripe='#ffffff', pants='#e86a8a', shoes='#7a4a2a', hair='#5a3a22', bun=True, dress=True, h=0.94),
}
# poses de braço: lista de pontos (ombro, cotovelo, mão) no canvas 600x1000
ARMS = {
    'hang':  ([(236, 560), (222, 650), (226, 735)], [(364, 560), (378, 650), (374, 735)]),
    'point': ([(236, 560), (222, 650), (226, 735)], [(364, 560), (450, 520), (530, 480)]),
    'pointL': ([(236, 560), (150, 520), (70, 480)], [(364, 560), (378, 650), (374, 735)]),
    'up':    ([(236, 560), (222, 650), (226, 735)], [(364, 560), (420, 470), (440, 370)]),
    'both_up': ([(236, 560), (180, 470), (160, 370)], [(364, 560), (420, 470), (440, 370)]),
    'wave':  ([(236, 560), (222, 650), (226, 735)], [(364, 560), (440, 500), (460, 400)]),
    'hip':   ([(236, 560), (176, 630), (240, 690)], [(364, 560), (424, 630), (360, 690)]),
    'belly': ([(236, 560), (220, 660), (276, 690)], [(364, 560), (380, 660), (324, 690)]),
    'temple': ([(236, 560), (222, 650), (226, 735)], [(364, 560), (440, 480), (392, 372)]),
    'cross': ([(236, 560), (266, 650), (352, 630)], [(364, 560), (334, 660), (248, 640)]),
    'hold':  ([(236, 560), (240, 650), (290, 640)], [(364, 560), (360, 650), (310, 640)]),
    'phone': ([(236, 560), (222, 650), (226, 735)], [(364, 560), (360, 650), (318, 600)]),
    'oar':   ([(236, 560), (200, 620), (180, 690)], [(364, 560), (330, 620), (290, 680)]),
    'thumb': ([(236, 560), (222, 650), (226, 735)], [(364, 560), (420, 610), (420, 540)]),
    'cheek': ([(236, 560), (196, 520), (236, 420)], [(364, 560), (404, 520), (364, 420)]),
    'reach': ([(236, 560), (200, 600), (130, 610)], [(364, 560), (400, 600), (470, 610)]),
}
FACE = {  # olhos, sobrancelha, boca
    'neutral': ('dot', 'flat', 'smile'), 'happy': ('happy', 'up', 'grin'), 'talk': ('dot', 'flat', 'open'),
    'surprise': ('wide', 'up', 'o'), 'worried': ('dot', 'worried', 'wobble'), 'sad': ('down', 'sad', 'frown'),
    'laugh': ('happy', 'up', 'laugh'), 'angry': ('dot', 'angry', 'flat'), 'squint': ('squint', 'flat', 'flat'),
    'blink': ('closed', 'flat', 'smile'), 'cold': ('squint', 'worried', 'teeth'), 'hot': ('dot', 'worried', 'open'),
    'shout': ('wide', 'angry', 'open'), 'sleepy': ('closed', 'flat', 'flat'), 'proud': ('happy', 'up', 'smile'),
}

class Dr:
    def __init__(s, im): s.d = ImageDraw.Draw(im)
    def P(s, pts): return [(x * K, y * K) for x, y in pts]
    def ell(s, cx, cy, rx, ry, fill, ol=OL, w=8):
        s.d.ellipse([(cx - rx) * K, (cy - ry) * K, (cx + rx) * K, (cy + ry) * K], fill=fill, outline=ol if w else None, width=w * K if w else 0)
    def poly(s, pts, fill, ol=OL, w=8): s.d.polygon(s.P(pts), fill=fill, outline=ol if w else None, width=w * K if w else 0)
    def rr(s, x0, y0, x1, y1, r, fill, ol=OL, w=8): s.d.rounded_rectangle([x0 * K, y0 * K, x1 * K, y1 * K], radius=r * K, fill=fill, outline=ol if w else None, width=w * K if w else 0)
    def line(s, pts, col, w):
        s.d.line(s.P(pts), fill=col, width=int(w * K), joint='curve')
        for x, y in (pts[0], pts[-1]): s.d.ellipse([(x - w / 2) * K, (y - w / 2) * K, (x + w / 2) * K, (y + w / 2) * K], fill=col)
    def limb(s, pts, col, w): s.line(pts, OL, w + 12); s.line(pts, col, w)
    def arc(s, cx, cy, rx, ry, a0, a1, col, w): s.d.arc([(cx - rx) * K, (cy - ry) * K, (cx + rx) * K, (cy + ry) * K], a0, a1, fill=col, width=int(w * K))
    def chord(s, cx, cy, rx, ry, a0, a1, fill, ol=OL, w=8): s.d.chord([(cx - rx) * K, (cy - ry) * K, (cx + rx) * K, (cy + ry) * K], a0, a1, fill=fill, outline=ol, width=w * K)

def bean(cx, cy, rx, ry, n=48):
    pts = []
    for i in range(n):
        a = i / n * 2 * math.pi
        w = rx * (1.0 + 0.10 * math.sin(a))  # mais largo em cima
        pts.append((cx + math.cos(a) * w, cy - math.sin(a) * ry))
    return pts

def draw(d, C, arms, face, look, extra):
    skin = hx(C['skin']); shirt = hx(C['shirt']); pants = hx(C['pants'])
    eyes, brow, mouth = FACE.get(face, FACE['neutral'])
    hx_, hy = 300, 330
    # pernas finas
    leg = pants if not C.get('shorts') else skin
    for lx in (272, 328):
        if C.get('shorts'): d.limb([(lx, 760), (lx, 800)], pants, 34)
        d.limb([(lx, 770), (lx + (lx - 300) * 0.15, 950)], leg if not C.get('dress') else skin, 16)
        d.ell(lx + (lx - 300) * 0.5, 960, 34, 16, hx(C['shoes']), w=7)
    # corpo
    if C.get('dress'):
        d.poly([(244, 520), (356, 520), (400, 800), (200, 800)], shirt)
        d.line([(214, 760), (386, 760)], hx(C['stripe']), 8)
    else:
        d.rr(240, 520, 360, 790, 40, shirt)
        if C['stripe'] != C['shirt']:
            for yy in (600, 680): d.line([(248, yy), (352, yy)], hx(C['stripe']), 10)
    if C.get('coat'):
        d.poly([(232, 520), (300, 520), (290, 820), (222, 820)], (250, 250, 252, 255)); d.poly([(300, 520), (368, 520), (378, 820), (310, 820)], (250, 250, 252, 255))
    if C.get('tie'): d.poly([(292, 530), (308, 530), (316, 640), (300, 665), (284, 640)], hx(C['tie']), w=5)
    if 'scarf' in extra:
        d.rr(250, 500, 350, 548, 22, hx('#e04848')); d.rr(316, 530, 348, 640, 14, hx('#e04848'))
    if 'notebook' in extra and arms in ('hold',):
        d.rr(250, 600, 352, 690, 8, hx('#7a5a3a'))
    # braços finos
    la, ra = ARMS[arms]
    for a in (la, ra):
        d.limb(a, shirt if not C.get('coat') else (250, 250, 252, 255), 16)
        hxp, hyp = a[-1]; d.ell(hxp, hyp, 20, 20, skin, w=7)
    if 'phone' in extra: d.rr(300, 560, 336, 624, 8, hx('#22222e'), w=5)
    if 'lantern' in extra: d.rr(512, 470, 560, 500, 8, hx('#ffd23f'), w=5)
    if 'mug' in extra: d.rr(372, 700, 410, 750, 8, hx('#ffffff'), w=6)
    if 'tablet' in extra: d.rr(256, 600, 344, 680, 10, hx('#22222e'), w=6)
    if 'paper' in extra: d.rr(270, 600, 340, 690, 4, hx('#fffdf2'), w=5)
    if 'icecream' in extra: d.poly([(512, 480), (548, 480), (530, 540)], hx('#e8b060'), w=5); d.ell(530, 466, 22, 20, hx('#ff9ac0'), w=5)
    if 'sign' in extra:
        from PIL import ImageFont
        d.rr(170, 560, 430, 680, 12, hx('#fff4d6'), w=7)
        f = ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf', 30 * K)
        d.d.text((300 * K, 620 * K), 'DESEMPREGADO', font=f, fill=hx('#d63a3a'), anchor='mm')
    if 'photo' in extra: d.rr(254, 590, 346, 660, 4, hx('#ffffff'), w=5); d.ell(300, 622, 18, 18, hx('#fff3b0'), w=3)
    # pescoço
    d.rr(286, 470, 314, 530, 10, skin, w=7)
    # cabelo de trás
    if C.get('pony'): d.ell(hx_ + 120, hy - 10, 40, 70, hx(C['hair']))
    if C.get('bun'): d.ell(hx_, hy - 150, 46, 40, hx(C['hair']))
    if C.get('wolf'):
        for sx in (-1, 1): d.poly([(hx_ + sx * 60, hy - 120), (hx_ + sx * 120, hy - 230), (hx_ + sx * 130, hy - 90)], skin, w=8)
    # cabeça de feijão
    d.poly(bean(hx_, hy, 128, 140), skin, w=8)
    # cabelo da frente
    hc = hx(C['hair'])
    if C.get('spiky'):
        pts = [(hx_ - 128, hy - 30)]
        for i in range(7): pts += [(hx_ - 110 + i * 37, hy - 150 - (i % 2) * 34), (hx_ - 92 + i * 37, hy - 120)]
        pts += [(hx_ + 128, hy - 30), (hx_ + 100, hy - 110), (hx_ - 100, hy - 110)]
        d.poly(pts, hc, w=7)
    elif C.get('hat') is None and not C.get('bun') and not C.get('wolf'):
        d.chord(hx_, hy - 40, 140, 112, 180, 360, hc, w=7)
    elif C.get('bun') or C.get('pony'):
        d.chord(hx_, hy - 40, 140, 112, 180, 360, hc, w=7)
    if C.get('must') and C.get('hair'):  # cabelo branco nas laterais
        d.ell(hx_ - 126, hy + 5, 22, 40, hx(C['hair']), w=6); d.ell(hx_ + 126, hy + 5, 22, 40, hx(C['hair']), w=6)
    # olhos
    ex, ey = look
    for sx in (-1, 1):
        cx = hx_ + sx * 46 + ex * 8; cy = hy - 6 + ey * 8
        if eyes in ('dot', 'down'):
            d.ell(cx, cy + (6 if eyes == 'down' else 0), 13, 16, OL, w=0); d.ell(cx + 4, cy - 6, 4, 4, (255, 255, 255, 255), w=0)
        elif eyes == 'wide':
            d.ell(cx, cy, 22, 24, (255, 255, 255, 255), w=6); d.ell(cx + ex * 5, cy + ey * 5, 10, 11, OL, w=0)
        elif eyes == 'happy': d.arc(cx, cy + 8, 18, 14, 200, 340, OL, 8)
        elif eyes == 'closed': d.arc(cx, cy, 18, 10, 20, 160, OL, 7)
        elif eyes == 'squint': d.line([(cx - 16, cy), (cx + 16, cy)], OL, 8)
        bx0, by0 = cx - 20, cy - 40
        if brow == 'up': d.arc(cx, cy - 38, 20, 10, 200, 340, OL, 7)
        elif brow == 'worried': d.line([(cx - sx * 22, cy - 34), (cx + sx * 18, cy - 46)], OL, 7)
        elif brow == 'angry': d.line([(cx - sx * 22, cy - 46), (cx + sx * 18, cy - 34)], OL, 7)
        elif brow == 'sad': d.line([(cx - sx * 20, cy - 46), (cx + sx * 20, cy - 38)], OL, 7)
        else: d.line([(cx - 16, cy - 40), (cx + 16, cy - 40)], OL, 7)
    if C.get('glasses'):
        for sx in (-1, 1): d.ell(hx_ + sx * 46, hy - 6, 30, 28, None, w=6)
        d.line([(hx_ - 16, hy - 8), (hx_ + 16, hy - 8)], OL, 6)
    if 'sunglasses' in extra:
        for sx in (-1, 1): d.rr(hx_ + sx * 46 - 32, hy - 26, hx_ + sx * 46 + 32, hy + 14, 14, OL, w=0)
        d.line([(hx_ - 16, hy - 12), (hx_ + 16, hy - 12)], OL, 7)
    # bochechas
    for sx in (-1, 1): d.ell(hx_ + sx * 74, hy + 34, 20, 11, hx('#ef9a9a', 170), w=0)
    # boca
    my = hy + 64
    if mouth == 'smile': d.arc(hx_, my - 18, 26, 20, 25, 155, OL, 7)
    elif mouth == 'grin': d.chord(hx_, my - 10, 30, 24, 0, 180, (255, 255, 255, 255), w=7)
    elif mouth == 'open': d.ell(hx_, my, 18, 15, hx('#7a2a3a'), w=6)
    elif mouth == 'o': d.ell(hx_, my + 2, 11, 14, hx('#7a2a3a'), w=6)
    elif mouth == 'laugh': d.chord(hx_, my - 12, 38, 36, 0, 180, hx('#7a2a3a'), w=7); d.ell(hx_, my + 10, 14, 7, hx('#e66a7a'), w=0)
    elif mouth == 'frown': d.arc(hx_, my + 10, 22, 14, 205, 335, OL, 7)
    elif mouth == 'wobble': d.line([(hx_ - 20, my), (hx_ - 7, my - 5), (hx_ + 7, my + 3), (hx_ + 20, my - 2)], OL, 6)
    elif mouth == 'teeth': d.rr(hx_ - 24, my - 10, hx_ + 24, my + 10, 6, (255, 255, 255, 255), w=6); d.line([(hx_ - 24, my), (hx_ + 24, my)], OL, 4)
    else: d.line([(hx_ - 16, my), (hx_ + 16, my)], OL, 7)
    if C.get('wolf'):
        d.ell(hx_, hy + 50, 60, 40, hx('#d0d0dc'), w=7); d.ell(hx_, hy + 30, 18, 12, OL, w=0)
    if C.get('must'):
        d.ell(hx_ - 22, my - 24, 28, 13, (245, 245, 245, 255), w=6); d.ell(hx_ + 22, my - 24, 28, 13, (245, 245, 245, 255), w=6)
    if C.get('beard'): d.chord(hx_, hy + 60, 104, 90, 0, 180, hx(C['hair']), w=7); d.ell(hx_, my, 16, 10, hx('#7a2a3a'), w=5)
    # chapéus
    if C.get('hat') == 'bucket':
        d.rr(hx_ - 96, hy - 176, hx_ + 96, hy - 92, 40, hx(C['hatc'])); d.ell(hx_, hy - 96, 158, 30, hx(C['hatc']))
        d.rr(hx_ - 96, hy - 124, hx_ + 96, hy - 104, 6, hx('#c99a18'), w=0)
        if 'snowhat' in extra: d.ell(hx_, hy - 172, 98, 28, (255, 255, 255, 255))
    elif C.get('hat') == 'cap':
        d.chord(hx_, hy - 50, 134, 110, 180, 360, hx(C['hatc'])); d.rr(hx_ - 20, hy - 72, hx_ + 180, hy - 48, 12, hx(C['hatc']))
    if C.get('headset'):
        d.arc(hx_, hy - 40, 140, 130, 180, 360, OL, 14); d.rr(hx_ - 152, hy - 30, hx_ - 118, hy + 30, 10, hx('#3a3a4e')); d.rr(hx_ + 118, hy - 30, hx_ + 152, hy + 30, 10, hx('#3a3a4e'))
    if 'sweat' in extra:
        for (x0, y0) in ((hx_ + 120, hy - 70), (hx_ - 126, hy - 40)):
            d.poly([(x0, y0 - 26), (x0 - 12, y0), (x0 + 12, y0)], hx('#6ec6ff'), w=4); d.ell(x0, y0 + 2, 12, 12, hx('#6ec6ff'), w=4)
    if 'tears' in extra:
        for sx in (-1, 1): d.ell(hx_ + sx * 52, hy + 30, 8, 14, hx('#6ec6ff'), w=4)
    if 'wet' in extra:
        for i in range(5): d.ell(hx_ - 120 + i * 60, hy - 120 + (i % 2) * 50, 7, 11, hx('#6ec6ff'), w=3)

@lru_cache(maxsize=4096)
def card(name, arms='hang', face='neutral', look=(0, 0), extra=()):
    C = CAST[name]
    im = Image.new('RGBA', (600 * K, 1000 * K), (0, 0, 0, 0))
    draw(Dr(im), C, arms, face, look, extra)
    return im.resize((600, 1000), Image.LANCZOS)
