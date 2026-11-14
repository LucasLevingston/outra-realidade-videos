import sys, math; sys.path.insert(0, '/home/claude/outra-realidade-videos/engine/py')
from PIL import Image, ImageDraw, ImageFont
import chars as CH, ui2d as UI
W, H = 1080, 1920
PL = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/outra-realidade-videos/projetos/short-milhao-mes/plates/tw_up_night_a2ab63_color.png'
bg = Image.open(PL).convert('RGB')
bw, bh = bg.size; s = max(W / bw, H / bh); bg = bg.resize((int(bw * s), int(bh * s)))
bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
im = bg.convert('RGBA')
sb = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sb); cx, cy = W // 2, 640
for i in range(0, 36, 2):
    a0 = math.radians(i * 10); a1 = math.radians(i * 10 + 10); R = 2500
    d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=(255, 210, 63, 60))
im.alpha_composite(sb)
F = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
d = ImageDraw.Draw(im)
def t(y, txt, sz, col):
    f = ImageFont.truetype(F, sz)
    while f.getbbox(txt)[2] > W - 80: sz -= 4; f = ImageFont.truetype(F, sz)
    d.text((W // 2, y), txt, font=f, fill=col, anchor='mm', stroke_width=max(8, sz // 10), stroke_fill=(20, 16, 28))
# Beto surpreso com o celular, chuva de notas
import random; random.seed(7)
for _ in range(26):
    x, y, r = random.randint(40, W - 160), random.randint(700, 1500), random.randint(-35, 35)
    n = Image.new('RGBA', (150, 72), (0, 0, 0, 0)); dn = ImageDraw.Draw(n)
    dn.rounded_rectangle([2, 2, 147, 69], 10, fill=(92, 184, 92), outline=(30, 70, 40), width=5)
    dn.ellipse([55, 16, 95, 56], outline=(30, 70, 40), width=4)
    im.alpha_composite(n.rotate(r, expand=True), (x, y))
c = CH.card('beto', 'both_up', 'surprise', (0.2, -0.5), ('phone',))
c = c.resize((int(c.width * 1000 / c.height), 1000), Image.LANCZOS)
sh = Image.new('RGBA', (420, 70), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([0, 0, 419, 69], fill=(20, 10, 30, 110))
im.alpha_composite(sh, (W // 2 - 210, 1600))
im.alpha_composite(c, (W // 2 - c.width // 2, 1650 - c.height))
t(345, 'E SE CAÍSSE R$ 1 MILHÃO', 104, (255, 255, 255))
t(490, 'TODO MÊS?', 170, (255, 210, 63))
pl = UI.pill('PRA SEMPRE', '#e04848', '#ffffff', 52); im.alpha_composite(pl, (W // 2 - pl.width // 2, 600))
pl = UI.pill('OUTRA REALIDADE', '#ffd23f', '#1d1d2b', 50); im.alpha_composite(pl, (W // 2 - pl.width // 2, 1760))
im.convert('RGB').save('/home/claude/outra-realidade-videos/projetos/short-milhao-mes/thumb.jpg', quality=92)
print('ok')
