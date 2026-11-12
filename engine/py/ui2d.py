import math, random, json
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OL = (29, 29, 43, 255)
SS = 3
FONT = (__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'fonts', 'Poppins-Bold.ttf'))

@lru_cache(None)
def font(sz):
    return ImageFont.truetype(FONT, sz)

def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x

def sstep(x):
    x = clamp(x); return x * x * x * (x * (x * 6 - 15) + 10)

def eout(x):
    x = clamp(x); return 1 - (1 - x) ** 3

def back(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

def spring(x):
    if x <= 0: return 0.0
    return 1 - math.exp(-6 * x) * math.cos(11 * x)

def lerp(a, b, t):
    return a + (b - a) * t

def hexc(h, a=255):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


class D:
    """Drawing on a supersampled image with unscaled coordinates."""
    def __init__(s, im, k=SS):
        s.im = im; s.d = ImageDraw.Draw(im); s.k = k

    def _p(s, pts):
        return [(x * s.k, y * s.k) for x, y in pts]

    def ell(s, cx, cy, rx, ry, fill, ol=OL, w=5):
        k = s.k
        s.d.ellipse([(cx - rx) * k, (cy - ry) * k, (cx + rx) * k, (cy + ry) * k], fill=fill,
                    outline=ol if w else None, width=int(w * k) if w else 0)

    def rr(s, x0, y0, x1, y1, r, fill, ol=OL, w=5):
        k = s.k
        s.d.rounded_rectangle([x0 * k, y0 * k, x1 * k, y1 * k], radius=r * k, fill=fill,
                              outline=ol if w else None, width=int(w * k) if w else 0)

    def poly(s, pts, fill, ol=OL, w=5):
        s.d.polygon(s._p(pts), fill=fill, outline=ol if w else None, width=int(w * s.k) if w else 0)

    def line(s, pts, col, w, cap=True):
        s.d.line(s._p(pts), fill=col, width=int(w * s.k), joint="curve")
        if cap:
            for x, y in (pts[0], pts[-1]):
                s.d.ellipse([(x - w / 2) * s.k, (y - w / 2) * s.k, (x + w / 2) * s.k, (y + w / 2) * s.k], fill=col)

    def limb(s, pts, col, w):
        s.line(pts, OL, w + 10); s.line(pts, col, w)

    def arc(s, cx, cy, rx, ry, a0, a1, col, w):
        k = s.k
        s.d.arc([(cx - rx) * k, (cy - ry) * k, (cx + rx) * k, (cy + ry) * k], a0, a1, fill=col, width=int(w * k))

    def chord(s, cx, cy, rx, ry, a0, a1, fill, ol=OL, w=5):
        k = s.k
        s.d.chord([(cx - rx) * k, (cy - ry) * k, (cx + rx) * k, (cy + ry) * k], a0, a1, fill=fill,
                  outline=ol, width=int(w * k))

    def text(s, x, y, txt, sz, fill, anchor="mm", stroke=0, sfill=OL):
        s.d.text((x * s.k, y * s.k), txt, font=font(int(sz * s.k)), fill=fill, anchor=anchor,
                 stroke_width=int(stroke * s.k), stroke_fill=sfill)


def sprite(w, h, fn, k=SS):
    im = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0))
    fn(D(im, k))
    return im.resize((w, h), Image.LANCZOS) if k != 1 else im


# ---------------------------------------------------------------- characters
CW, CH = 440, 820
FEET = (220, 800)

DITO = dict(skin="#b97a4e", shirt="#2f9e95", shirt2="#257f78", pants="#5b6378", hat="#f2c230", hair=None,
            must=True, kind="human", shoes="#7a4a2a")
VIZ = dict(skin="#f0c09a", shirt="#5cb85c", shirt2="#4a9a4a", pants="#3d6fb6", hat="cap", hair="#3a2618",
           must=False, kind="human", shoes="#e04848")
LOBO = dict(skin="#8e8f9e", shirt="#7b5aa6", shirt2="#674b8c", pants="#4a4a5a", hat=None, hair=None,
            must=False, kind="wolf", shoes="#5c5c6c")

ARMS = {
    "down": ([(150, 432), (128, 520), (130, 592)], [(290, 432), (312, 520), (310, 592)]),
    "point_up": ([(150, 432), (128, 520), (130, 592)], [(290, 432), (350, 365), (378, 282)]),
    "point_left": ([(150, 432), (80, 420), (12, 392)], [(290, 432), (312, 520), (310, 592)]),
    "point_cam": ([(150, 432), (128, 520), (130, 592)], [(290, 432), (322, 510), (262, 478)]),
    "wrap": ([(150, 432), (196, 512), (272, 486)], [(290, 432), (246, 524), (168, 500)]),
    "belly": ([(150, 432), (134, 512), (192, 552)], [(290, 432), (306, 512), (248, 552)]),
    "scratch": ([(150, 432), (128, 520), (130, 592)], [(290, 432), (360, 380), (330, 232)]),
    "sign": ([(150, 432), (160, 520), (196, 556)], [(290, 432), (280, 520), (244, 556)]),
    "fan": ([(150, 432), (128, 520), (130, 592)], [(290, 432), (356, 400), (330, 318)]),
}


def draw_char(d, P, st):
    skin = hexc(P["skin"]); shirt = hexc(P["shirt"]); pants = hexc(P["pants"])
    wolf = P["kind"] == "wolf"
    eyes = st.get("eyes", "open"); mouth = st.get("mouth", "smile"); arms = st.get("arms", "down")
    look = st.get("look", (0, 0)); brow = st.get("brow", None); ex = st.get("extras", ())
    # legs
    for lx in (190, 250):
        d.rr(lx - 22, 590, lx + 22, 770, 14, pants)
        d.ell(lx + (-8 if lx < 220 else 8), 782, 34, 16, hexc(P["shoes"]))
    # body
    d.rr(138, 400, 302, 628, 46, shirt)
    if not wolf:
        for yy in (470, 530):
            d.line([(150, yy), (290, yy)], hexc(P["shirt2"]), 10, cap=False)
    else:
        d.poly([(150, 610), (175, 640), (200, 612), (225, 640), (250, 612), (275, 640), (295, 610)], shirt)
    # arms
    la, ra = ARMS[arms]
    sk = skin
    for a in (la, ra):
        d.limb(a, shirt if arms not in ("wrap",) else shirt, 30)
        d.limb([a[-2], a[-1]], skin, 26)
        hx, hy = a[-1]
        d.ell(hx, hy, 22, 22, skin)
        if arms in ("point_up", "point_left", "point_cam", "scratch") and a is ra or (arms == "point_left" and a is la):
            pass
    if arms == "point_cam":
        d.limb([(262, 470), (262, 418)], skin, 16)
        d.ell(262, 482, 32, 30, skin)
    if arms == "point_up":
        d.limb([(378, 282), (386, 248)], skin, 12)
    if arms == "point_left":
        d.limb([(12, 392), (-8 + 20, 380)], skin, 12)
    if "sign" in ex or arms == "sign":
        pass
    # neck + head
    d.rr(198, 360, 242, 420, 12, skin)
    hx, hy = 220, 282
    if wolf:
        for sx in (-1, 1):
            d.poly([(hx + sx * 70, hy - 90), (hx + sx * 122, hy - 196), (hx + sx * 128, hy - 70)], skin)
            d.poly([(hx + sx * 84, hy - 100), (hx + sx * 116, hy - 165), (hx + sx * 116, hy - 92)], hexc("#d69aa6"), w=0)
        for sx in (-1, 1):
            d.poly([(hx + sx * 100, hy + 20), (hx + sx * 150, hy + 50), (hx + sx * 108, hy + 70)], skin)
    d.ell(hx - 118, hy + 6, 22, 30, skin) if not wolf else None
    d.ell(hx + 118, hy + 6, 22, 30, skin) if not wolf else None
    d.ell(hx, hy, 122, 116, skin)
    if wolf:
        d.ell(hx, hy + 52, 66, 46, hexc("#c9cad4"))
        d.ell(hx, hy + 22, 22, 15, OL, w=0)
        d.poly([(hx - 40, hy - 112), (hx - 20, hy - 140), (hx, hy - 112), (hx + 20, hy - 142), (hx + 40, hy - 112)], skin)
    # hair / hats
    if P.get("hair") and not wolf:
        d.chord(hx, hy - 8, 124, 112, 180, 360, hexc(P["hair"]))
    if P["hat"] == "cap":
        d.chord(hx, hy - 30, 124, 104, 180, 360, hexc("#e04848"))
        d.rr(hx - 10, hy - 52, hx + 170, hy - 28, 12, hexc("#c43a3a"))
        d.ell(hx, hy - 132, 14, 10, hexc("#c43a3a"))
    elif P["hat"]:
        d.rr(hx - 92, hy - 160, hx + 92, hy - 70, 40, hexc(P["hat"]))
        d.ell(hx, hy - 72, 150, 30, hexc(P["hat"]))
        d.rr(hx - 92, hy - 98, hx + 92, hy - 80, 6, hexc("#c99a18"), w=0)
        if "snowhat" in ex:
            d.ell(hx, hy - 150, 96, 30, (255, 255, 255, 255))
    # cheeks
    d.ell(hx - 66, hy + 36, 22, 13, hexc("#ef8a8a", 200), w=0)
    d.ell(hx + 66, hy + 36, 22, 13, hexc("#ef8a8a", 200), w=0)
    # eyes
    ex_, ey_ = look
    for sx in (-1, 1):
        cx = hx + sx * 40; cy = hy - 6
        if eyes == "closed":
            d.arc(cx, cy, 22, 14, 10, 170, OL, 6)
        elif eyes == "happy":
            d.arc(cx, cy + 8, 22, 18, 200, 340, OL, 7)
        else:
            d.ell(cx, cy, 26, 28, (255, 255, 255, 255), w=4)
            d.ell(cx + ex_ * 9, cy + ey_ * 10, 13, 14, OL, w=0)
            d.ell(cx + ex_ * 9 + 4, cy + ey_ * 10 - 5, 4, 4, (255, 255, 255, 255), w=0)
        if brow == "worried":
            d.line([(cx - sx * 24, cy - 40), (cx + sx * 20, cy - 52)], OL, 7)
        elif brow == "up":
            d.arc(cx, cy - 34, 22, 12, 200, 340, OL, 7)
        elif brow == "sad":
            d.line([(cx - sx * 22, cy - 50), (cx + sx * 22, cy - 40)], OL, 7)
    if "sunglasses" in ex:
        d.rr(hx - 76, hy - 32, hx - 8, hy + 16, 16, OL, w=0)
        d.rr(hx + 8, hy - 32, hx + 76, hy + 16, 16, OL, w=0)
        d.line([(hx - 10, hy - 14), (hx + 10, hy - 14)], OL, 8)
        d.line([(hx - 60, hy - 22), (hx - 40, hy - 22)], (255, 255, 255, 160), 5)
    # mouth
    my = hy + 60 if not wolf else hy + 78
    if mouth == "smile":
        d.arc(hx, my - 16, 30, 22, 20, 160, OL, 7)
    elif mouth == "open":
        d.chord(hx, my - 6, 30, 26, 0, 180, hexc("#8a2a35"))
        d.ell(hx, my + 10, 14, 7, hexc("#e66a7a"), w=0)
    elif mouth == "o":
        d.ell(hx, my + 2, 13, 16, hexc("#8a2a35"), w=5)
    elif mouth == "laugh":
        d.chord(hx, my - 14, 42, 40, 0, 180, hexc("#8a2a35"))
        d.chord(hx, my - 14, 34, 12, 0, 180, (255, 255, 255, 255), w=0)
        d.ell(hx, my + 14, 16, 8, hexc("#e66a7a"), w=0)
    elif mouth == "sad":
        d.arc(hx, my + 10, 26, 18, 200, 340, OL, 7)
    elif mouth == "grit":
        d.rr(hx - 30, my - 12, hx + 30, my + 12, 8, (255, 255, 255, 255), w=5)
        d.line([(hx - 30, my), (hx + 30, my)], OL, 4, cap=False)
        for xx in (-15, 0, 15):
            d.line([(hx + xx, my - 12), (hx + xx, my + 12)], OL, 3, cap=False)
    elif mouth == "flat":
        d.line([(hx - 20, my), (hx + 20, my)], OL, 7)
    if P["must"]:
        d.ell(hx - 28, my - 26, 34, 16, (245, 245, 245, 255), w=4)
        d.ell(hx + 28, my - 26, 34, 16, (245, 245, 245, 255), w=4)
    if "sweat" in ex:
        for (x0, y0) in ((hx + 96, hy - 60), (hx - 104, hy - 30)):
            d.poly([(x0, y0 - 26), (x0 - 12, y0), (x0 + 12, y0)], hexc("#6ec6ff"), w=3)
            d.ell(x0, y0 + 2, 12, 12, hexc("#6ec6ff"), w=3)
    if "scarf" in ex:
        d.rr(160, 372, 280, 418, 20, hexc("#e04848"))
        d.rr(236, 400, 270, 500, 12, hexc("#e04848"))
        for yy in (430, 460):
            d.line([(240, yy), (266, yy)], hexc("#ffd23f"), 6, cap=False)


@lru_cache(maxsize=256)
def char_sprite(name, eyes="open", mouth="smile", arms="down", look=(0, 0), brow=None, extras=()):
    P = {"dito": DITO, "viz": VIZ, "lobo": LOBO}[name]
    st = dict(eyes=eyes, mouth=mouth, arms=arms, look=look, brow=brow, extras=extras)
    return sprite(CW, CH, lambda d: draw_char(d, P, st), k=2)


def place_char(canvas, spr, fx, fy, scale, rot=0.0, breath=0.0, ox=0, oy=0):
    """Paste character with feet at world (fx,fy) onto canvas (already offset by ox,oy)."""
    w, h = spr.size
    sw = max(1, int(w * scale)); sh = max(1, int(h * scale * (1 + breath)))
    im = spr.resize((sw, sh), Image.BICUBIC)
    fxs, fys = FEET[0] * scale, FEET[1] * scale * (1 + breath)
    if abs(rot) > 0.01:
        # rotate around feet
        pad = int(max(sw, sh) * 0.3)
        big = Image.new("RGBA", (sw + 2 * pad, sh + 2 * pad), (0, 0, 0, 0))
        big.paste(im, (pad, pad))
        im = big.rotate(rot, resample=Image.BICUBIC, center=(fxs + pad, fys + pad))
        fxs += pad; fys += pad
    paste(canvas, im, fx - fxs - ox, fy - fys - oy)


def paste(canvas, im, x, y):
    x = int(round(x)); y = int(round(y))
    W, H = canvas.size; w, h = im.size
    sx0 = max(0, -x); sy0 = max(0, -y)
    sx1 = min(w, W - x); sy1 = min(h, H - y)
    if sx1 <= sx0 or sy1 <= sy0: return
    src = im if (sx0, sy0, sx1, sy1) == (0, 0, w, h) else im.crop((sx0, sy0, sx1, sy1))
    canvas.alpha_composite(src, dest=(x + sx0, y + sy0))


def with_alpha(im, a):
    if a >= 0.999: return im
    im = im.copy(); al = im.getchannel("A").point(lambda v: int(v * a)); im.putalpha(al); return im


def scaled(im, s):
    if abs(s - 1) < 0.005: return im
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BICUBIC)


# ---------------------------------------------------------------- UI elements
@lru_cache(None)
def pill(text, bg="#ffffff", fg="#1d1d2b", sz=54, small=None, icon=None):
    f = font(sz)
    tw = f.getbbox(text)[2] - f.getbbox(text)[0]
    iw = int(sz * 1.1) if icon else 0
    padx = int(sz * 0.6)
    w = tw + 2 * padx + iw + 10; h = int(sz * 1.75) + (int(sz * 0.55) if small else 0)
    def fn(d):
        d.rr(5, 5, w - 5, h - 5, (h - 10) / 2 if not small else 34, hexc(bg), w=6)
        y = h / 2 + (sz * 0.22 if small else 0)
        if small:
            d.text(w / 2 + iw / 2, sz * 0.62, small, int(sz * 0.42), hexc(fg))
        if icon:
            draw_icon(d, icon, padx + iw / 2 - 4, y, sz * 0.5)
        d.text(w / 2 + iw / 2, y + 2, text, sz, hexc(fg))
    return sprite(w, h, fn, k=2)


def draw_icon(d, icon, cx, cy, r):
    if icon == "sun":
        for i in range(8):
            a = i * math.pi / 4
            d.line([(cx + math.cos(a) * r * 0.8, cy + math.sin(a) * r * 0.8), (cx + math.cos(a) * r * 1.15, cy + math.sin(a) * r * 1.15)], hexc("#ff9f1c"), 6)
        d.ell(cx, cy, r * 0.6, r * 0.6, hexc("#ffd23f"), w=4)
    elif icon == "snow":
        for i in range(3):
            a = i * math.pi / 3
            d.line([(cx - math.cos(a) * r, cy - math.sin(a) * r), (cx + math.cos(a) * r, cy + math.sin(a) * r)], hexc("#3a8dde"), 7)
        d.ell(cx, cy, r * 0.25, r * 0.25, hexc("#ffffff"), w=3)
    elif icon == "clock":
        d.ell(cx, cy, r, r, hexc("#ffffff"), w=5)
        d.line([(cx, cy), (cx, cy - r * 0.6)], OL, 6); d.line([(cx, cy), (cx + r * 0.45, cy)], OL, 6)
    elif icon == "pin":
        d.ell(cx, cy - r * 0.3, r * 0.6, r * 0.6, hexc("#e04848"), w=4)
        d.poly([(cx - r * 0.45, cy - r * 0.05), (cx + r * 0.45, cy - r * 0.05), (cx, cy + r)], hexc("#e04848"), w=0)
        d.ell(cx, cy - r * 0.3, r * 0.22, r * 0.22, hexc("#ffffff"), w=0)
    elif icon == "cal":
        d.rr(cx - r, cy - r * 0.85, cx + r, cy + r, 8, hexc("#ffffff"), w=4)
        d.rr(cx - r, cy - r * 0.85, cx + r, cy - r * 0.3, 8, hexc("#e04848"), w=4)


@lru_cache(None)
def bubble(text, name, tag="#ff8c42", width=820, sz=62, tail="down", tailx=0.3):
    f = font(sz)
    words = text.split(); lines = []; cur = ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if f.getlength(t) > width - 110 and cur:
            lines.append(cur); cur = w_
        else:
            cur = t
    lines.append(cur)
    lh = int(sz * 1.25)
    bh = len(lines) * lh + 90
    W = width; H = bh + 110
    def fn(d):
        top = 50
        tx = W * tailx
        if tail == "down":
            d.poly([(tx - 40, top + bh - 12), (tx + 40, top + bh - 12), (tx - 10, top + bh + 52)], (255, 255, 255, 255), w=6)
        d.rr(6, top, W - 6, top + bh, 48, (255, 255, 255, 255), w=6)
        if tail == "down":
            d.poly([(tx - 34, top + bh - 16), (tx + 34, top + bh - 16), (tx - 8, top + bh + 40)], (255, 255, 255, 255), w=0)
        for i, ln in enumerate(lines):
            d.text(W / 2, top + 50 + lh * i + lh / 2, ln, sz, OL)
        fn2 = font(38); nw = fn2.getlength(name) + 60
        d.rr(40, 12, 40 + nw, 84, 36, hexc(tag), w=5)
        d.text(40 + nw / 2, 49, name, 38, (255, 255, 255, 255))
    return sprite(W, H, fn, k=2)


@lru_cache(maxsize=512)
def word_img(word, yellow, sz=118):
    f = font(sz)
    bb = f.getbbox(word, stroke_width=14)
    w = bb[2] - bb[0] + 20; h = bb[3] - bb[1] + 20
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((10 - bb[0], 10 - bb[1]), word, font=f, fill=(255, 210, 63, 255) if yellow else (255, 255, 255, 255),
           stroke_width=14, stroke_fill=(16, 16, 24, 255))
    return im
