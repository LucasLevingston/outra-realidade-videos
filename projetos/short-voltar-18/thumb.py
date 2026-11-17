"""Thumb 1080x1920 do Short (mesmo estilo 2D flat)."""
import os, sys, asyncio
PROJ = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(PROJ, '..', '..', 'engine', 'py'))
import flat2d as F
from playwright.async_api import async_playwright
bg = F.bg_sunburst()
caio = F.char('ct', 'beto', 540, 1760, 1.05, 'up', 'surprise', props=('pimple',))
font = os.path.abspath(os.path.join(PROJ, '..', '..', 'engine', 'fonts', 'Poppins-Bold.ttf'))
html = f'''<html><head><style>@font-face{{font-family:Pop;src:url(file://{font})}}
body{{margin:0}}#r{{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:Pop}}
.ch{{position:absolute;overflow:visible}} .bg{{position:absolute;left:0;top:0}}
.t{{position:absolute;left:0;width:1080px;text-align:center;font-size:112px;line-height:1.02;white-space:nowrap;-webkit-text-stroke:18px #14101c;paint-order:stroke fill;text-shadow:0 10px 0 rgba(20,16,28,.45)}}
.pill{{position:absolute;left:50%;translate:-50% 0;background:#22213a;border:8px solid #f4f0e8;border-radius:70px;padding:8px 46px 14px;color:#3ee08a;font-size:96px;white-space:nowrap;box-shadow:0 10px 0 rgba(20,16,28,.35)}}
.pill span{{display:block;color:#f4f0e8;font-size:28px;letter-spacing:3px;text-align:center}}
.ft{{position:absolute;left:50%;translate:-50% 0;bottom:120px;background:#14101c;color:#fff;font-size:40px;letter-spacing:4px;padding:10px 34px;border-radius:16px}}
</style></head><body><div id="r">{bg}
<div class="t" style="top:290px;color:#fff">E SE VOCÊ</div>
<div class="t" style="top:405px;color:#fff">VOLTASSE</div>
<div class="t" style="top:520px;color:#ffd23f">AOS 18 ANOS?</div>
<div class="pill" style="top:700px;rotate:-4deg"><span>IDADE</span><s style="color:#c9c9e6;text-decoration-color:#e8483a;text-decoration-thickness:10px">35</s> → 18</div>
{caio}<div class="ft">OUTRA REALIDADE</div></div></body></html>'''
open('/tmp/claude-0/t/thumb.html', 'w').write(html)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width': 1080, 'height': 1920}); await pg.goto('file:///tmp/claude-0/t/thumb.html'); await pg.wait_for_timeout(500)
        await pg.screenshot(path='/tmp/claude-0/t/thumb.png'); await b.close()
asyncio.run(main())
os.system(f'ffmpeg -v error -y -i /tmp/claude-0/t/thumb.png -q:v 2 {PROJ}/thumb.jpg')
print('thumb ok')
