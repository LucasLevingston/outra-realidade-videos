import sys, math, glob; sys.path.insert(0, '/home/claude/outra-realidade-videos/engine/py')
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import chars as CH, ui2d as UI
P = '/home/claude/outra-realidade-videos/projetos/longo-sorte-dobra'
W, H = 1280, 720
bg = Image.open(glob.glob(P + '/plates/st_crowd_day_*_color.png')[0]).convert('RGB')
bw, bh = bg.size; s = max(W / bw, H / bh); bg = bg.resize((int(bw * s), int(bh * s)))
bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H)).filter(ImageFilter.GaussianBlur(3))
im = bg.convert('RGBA')
sb = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sb); cx, cy = 330, 420
for i in range(0, 36, 2):
    a0 = math.radians(i * 10); a1 = math.radians(i * 10 + 10); R = 2500
    d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=(255, 210, 63, 70))
im.alpha_composite(sb)
# moedas voando
d = ImageDraw.Draw(im)
for (x, y, r) in [(120, 140, 34), (520, 110, 28), (90, 520, 26), (560, 470, 38), (430, 200, 22), (200, 330, 20)]:
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 196, 40), outline=(120, 70, 10), width=5)
    d.ellipse([x - r * 0.6, y - r * 0.6, x + r * 0.6, y + r * 0.6], outline=(200, 130, 20), width=3)
c = CH.card('caio20', 'both_up', 'laugh', (0.3, -0.4), ())
c = c.resize((int(c.width * 640 / c.height), 640), Image.LANCZOS)
sh = Image.new('RGBA', (300, 50), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([0, 0, 299, 49], fill=(20, 10, 30, 110))
im.alpha_composite(sh, (330 - 150, 680)); im.alpha_composite(c, (330 - c.width // 2, 705 - c.height))
F = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
d = ImageDraw.Draw(im)
def t(x, y, txt, sz, col, maxw=600):
    f = ImageFont.truetype(F, sz)
    while f.getbbox(txt)[2] > maxw: sz -= 4; f = ImageFont.truetype(F, sz)
    d.text((x, y), txt, font=f, fill=col, anchor='mm', stroke_width=max(8, sz // 9), stroke_fill=(20, 16, 28))
t(930, 150, 'E SE SUA SORTE', 86, (255, 255, 255))
t(930, 280, 'DOBRASSE', 150, (255, 210, 63))
t(930, 400, 'TODO DIA?', 96, (255, 255, 255))
pl = UI.pill('SORTE: 1 ATÉ 16.384', '#e04848', '#ffffff', 46); im.alpha_composite(pl, (930 - pl.width // 2, 490))
pl = UI.pill('OUTRA REALIDADE', '#ffd23f', '#1d1d2b', 40); im.alpha_composite(pl, (930 - pl.width // 2, 620))
im.convert('RGB').save(P + '/thumb.jpg', quality=92); print('ok')
