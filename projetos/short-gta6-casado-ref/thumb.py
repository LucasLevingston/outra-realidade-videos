import sys, math; sys.path.insert(0, '/home/claude/outra-realidade-videos/engine/py')
from PIL import Image, ImageDraw, ImageFont
import chars as CH, ui2d as UI
W, H = 1080, 1920
bg = Image.open(sys.argv[1]).convert('RGB'); out = sys.argv[2]
bw, bh = bg.size; s = max(W / bw, H / bh); bg = bg.resize((int(bw * s), int(bh * s)))
bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
im = bg.convert('RGBA')
im.alpha_composite(Image.new('RGBA', (W, H), (10, 8, 30, 70)))
sb = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sb); cx, cy = W // 2, 620
for i in range(0, 36, 2):
    a0 = math.radians(i * 10); a1 = math.radians(i * 10 + 10); R = 2500
    d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=(255, 210, 63, 45))
im.alpha_composite(sb)
F = '/home/claude/outra-realidade-videos/engine/fonts/Poppins-Bold.ttf'
d = ImageDraw.Draw(im)
def t(y, txt, sz, col):
    f = ImageFont.truetype(F, sz)
    while f.getbbox(txt)[2] > W - 80: sz -= 4; f = ImageFont.truetype(F, sz)
    d.text((W // 2, y), txt, font=f, fill=col, anchor='mm', stroke_width=max(8, sz // 10), stroke_fill=(20, 16, 28))
b = CH.card('bia', 'cross', 'angry', (0.6, 0), ()); b = b.resize((int(b.width * 820 / b.height), 820), Image.LANCZOS)
im.alpha_composite(b, (640, 1560 - b.height))
c = CH.card('voce', 'hold', 'surprise', (-0.4, -0.3), ('controller', 'sweat')); c = c.resize((int(c.width * 1000 / c.height), 1000), Image.LANCZOS)
sh = Image.new('RGBA', (380, 64), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([0, 0, 379, 63], fill=(20, 10, 30, 120)); im.alpha_composite(sh, (190, 1600))
im.alpha_composite(c, (380 - c.width // 2, 1640 - c.height))
t(350, 'E SE O GTA 6 LANÇAR', 104, (255, 255, 255))
t(495, 'E VOCÊ FOR CASADO?', 120, (255, 210, 63))
pl = UI.pill('A OU B?', '#e04848', '#ffffff', 70); im.alpha_composite(pl, (W // 2 - pl.width // 2, 610))
pl = UI.pill('OUTRA REALIDADE', '#ffd23f', '#1d1d2b', 50); im.alpha_composite(pl, (W // 2 - pl.width // 2, 1740))
im.convert('RGB').save(out, quality=92); print('ok')
