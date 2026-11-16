import sys, math; sys.path.insert(0, '/home/claude/outra-realidade-videos/engine/py')
from PIL import Image, ImageDraw, ImageFont
import chars as CH, ui2d as UI
W, H = 1080, 1920
PL = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/outra-realidade-videos/projetos/short-brasil-todas-copas/plates/PLACA.png'
bg = Image.open(PL).convert('RGB')
bw, bh = bg.size; s = max(W / bw, H / bh); bg = bg.resize((int(bw * s), int(bh * s)))
bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
im = bg.convert('RGBA')
sb = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sb); cx, cy = W // 2, 640
for i in range(0, 36, 2):
    a0 = math.radians(i * 10); a1 = math.radians(i * 10 + 10); R = 2500
    d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=(255, 210, 63, 55))
im.alpha_composite(sb)
F = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
d = ImageDraw.Draw(im)
def t(y, txt, sz, col):
    f = ImageFont.truetype(F, sz)
    while f.getbbox(txt)[2] > W - 80: sz -= 4; f = ImageFont.truetype(F, sz)
    d.text((W // 2, y), txt, font=f, fill=col, anchor='mm', stroke_width=max(8, sz // 10), stroke_fill=(20, 16, 28))
# Caio comemorando
c = CH.card('caio20', 'both_up', 'surprise', (0.0, -0.4), ())
c = c.resize((int(c.width * 860 / c.height), 860), Image.LANCZOS)
sh = Image.new('RGBA', (420, 70), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([0, 0, 419, 69], fill=(20, 10, 30, 110))
im.alpha_composite(sh, (W // 2 - 210, 1590))
im.alpha_composite(c, (W // 2 - c.width // 2, 1640 - c.height))
t(345, 'E SE O BRASIL GANHASSE', 92, (255, 255, 255))
t(490, 'TODAS AS COPAS?', 150, (255, 210, 63))
pl = UI.pill('22 ESTRELAS NA CAMISA', '#e04848', '#ffffff', 52); im.alpha_composite(pl, (W // 2 - pl.width // 2, 600))
pl = UI.pill('OUTRA REALIDADE', '#ffd23f', '#1d1d2b', 50); im.alpha_composite(pl, (W // 2 - pl.width // 2, 1760))
im.convert('RGB').save('/home/claude/outra-realidade-videos/projetos/short-brasil-todas-copas/thumb.jpg', quality=92)
print('ok')
