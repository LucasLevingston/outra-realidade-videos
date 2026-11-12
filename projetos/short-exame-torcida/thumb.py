import sys, math; sys.path.insert(0, '/home/claude/outra-realidade-videos/engine/py')
from PIL import Image, ImageDraw, ImageFont
import chars as CH, ui2d as UI
D = '/home/claude/outra-realidade-videos/projetos/short-exame-torcida'
W, H = 1080, 1920
bg = Image.open(D + '/plates/cl_wide_interior_day_00b656_color.png').convert('RGB')
s = max(W / bg.width, H / bg.height); bg = bg.resize((int(bg.width * s), int(bg.height * s)))
bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
im = bg.convert('RGBA')
sb = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sb); cx, cy = W // 2, 760
for i in range(0, 36, 2):
    a0, a1 = math.radians(i * 10), math.radians(i * 10 + 10); R = 2500
    d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=(58, 141, 222, 70))
im.alpha_composite(sb)
F = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
d = ImageDraw.Draw(im)
def t(y, s, sz, col):
    f = ImageFont.truetype(F, sz)
    while f.getbbox(s)[2] > W - 80: sz -= 4; f = ImageFont.truetype(F, sz)
    d.text((W // 2, y), s, font=f, fill=col, anchor='mm', stroke_width=max(8, sz // 10), stroke_fill=(20, 16, 28))
t(380, 'E SE O EXAME TIVESSE', 110, (255, 255, 255))
t(530, 'TORCIDA?', 170, (255, 210, 63))
p = UI.pill('NOVEMBRO AZUL', '#3a8dde', '#ffffff', 56); im.alpha_composite(p, (W // 2 - p.width // 2, 660))
def put(name, arms, face, ex, h, x, base):
    c = CH.card(name, arms, face, (0, 0), ex); c = c.resize((int(c.width * h / c.height), h), Image.LANCZOS)
    sh = Image.new('RGBA', (int(h * 0.36), 50), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([0, 0, sh.width - 1, 49], fill=(20, 10, 30, 110))
    im.alpha_composite(sh, (x - sh.width // 2, base - 25)); im.alpha_composite(c, (x - c.width // 2, base - c.height))
put('beto', 'both_up', 'laugh', (), 640, 230, 1560)
put('ze', 'hold', 'laugh', ('drum', 'sticks'), 640, 860, 1560)
put('dito', 'up', 'hot', ('flag', 'sweat'), 900, 560, 1640)
p = UI.pill('OUTRA REALIDADE', '#ffd23f', '#1d1d2b', 50); im.alpha_composite(p, (W // 2 - p.width // 2, 1780))
im.convert('RGB').save(D + '/thumb.jpg', quality=92)
