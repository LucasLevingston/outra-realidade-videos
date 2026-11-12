import sys, math; sys.path.insert(0, '/home/claude/outra-realidade-videos/engine/py')
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import chars as CH, ui2d as UI
W, H = 1080, 1920
bg = Image.open('/home/claude/p3/plates/b_room_interior_day_039231_color.png').convert('RGB').resize((W, H))
im = bg.convert('RGBA')
# sunburst suave no topo
sb = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sb); cx, cy = W // 2, 700
for i in range(36):
    if i % 2: continue
    a0 = math.radians(i * 10); a1 = math.radians(i * 10 + 10); R = 2500
    d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=(255, 210, 63, 55))
im.alpha_composite(sb)
F = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
d = ImageDraw.Draw(im)
def t(y, s, sz, col):
    f = ImageFont.truetype(F, sz)
    while f.getbbox(s)[2] > W - 80: sz -= 4; f = ImageFont.truetype(F, sz)
    d.text((W // 2, y), s, font=f, fill=col, anchor='mm', stroke_width=max(8, sz // 10), stroke_fill=(20, 16, 28))
t(380, 'E SE A SUA VIDA FOSSE', 120, (255, 255, 255))
t(540, 'UMA SIMULAÇÃO?', 150, (255, 210, 63))
p = UI.pill('ERRO 404', '#e04848', '#ffffff', 56); im.alpha_composite(p, (W // 2 - p.width // 2, 672))
c = CH.card('caio20', 'temple', 'surprise', (0.4, -0.4), ())
c = c.resize((int(c.width * 1000 / c.height), 1000), Image.LANCZOS)
sh = Image.new('RGBA', (360, 60), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([0, 0, 359, 59], fill=(20, 10, 30, 110))
im.alpha_composite(sh, (W // 2 - 180, 1600))
im.alpha_composite(c, (W // 2 - c.width // 2, 1630 - c.height))
p = UI.pill('OUTRA REALIDADE', '#ffd23f', '#1d1d2b', 50); im.alpha_composite(p, (W // 2 - p.width // 2, 1780))
im.convert('RGB').save('/home/claude/p3/thumb.jpg', quality=92)
print(c.size)
