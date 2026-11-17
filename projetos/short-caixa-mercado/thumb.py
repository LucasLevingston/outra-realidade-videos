"""Thumb 1080x1920 do Short (mesmo estilo 2D flat)."""
import os, sys, asyncio
PROJ = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(PROJ, '..', '..', 'engine', 'py'))
import flat2d as F
from playwright.async_api import async_playwright
TMP = '/tmp/thumb-caixa'; os.makedirs(TMP, exist_ok=True)
bg = F.bg_sunburst()
caixa = F.char('ct', 'caixa', 380, 1700, 1.0, 'up', 'surprise')
fish = F.fish_svg(0.9, flip=True)
font = os.path.abspath(os.path.join(PROJ, '..', '..', 'engine', 'fonts', 'Poppins-Bold.ttf'))
html = f'''<html><head><style>@font-face{{font-family:Pop;src:url(file://{font})}}
body{{margin:0}}#r{{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:Pop}}
.ch{{position:absolute;overflow:visible}} .bg{{position:absolute;left:0;top:0}}
.t{{position:absolute;left:0;width:1080px;text-align:center;font-size:104px;line-height:1.02;white-space:nowrap;-webkit-text-stroke:18px #14101c;paint-order:stroke fill;text-shadow:0 10px 0 rgba(20,16,28,.45)}}
.stamp{{position:absolute;border:12px solid #e8483a;color:#e8483a;border-radius:24px;padding:4px 36px;font-size:100px;background:rgba(255,255,255,.92)}}
.ft{{position:absolute;left:50%;translate:-50% 0;bottom:120px;background:#14101c;color:#fff;font-size:40px;letter-spacing:4px;padding:10px 34px;border-radius:16px}}
.fish{{position:absolute;left:470px;top:1180px;rotate:-12deg}}
</style></head><body><div id="r">{bg}
<div class="t" style="top:290px;color:#fff">4 COISAS PRA</div>
<div class="stamp" style="top:420px;left:290px;rotate:-6deg">NUNCA</div>
<div class="t" style="top:600px;color:#ffd23f">FAZER NO CAIXA</div>
{caixa}<div class="fish">{fish}</div><div class="ft">OUTRA REALIDADE</div></div></body></html>'''
open(f'{TMP}/thumb.html', 'w').write(html)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files', '--no-sandbox'])
        pg = await b.new_page(viewport={'width': 1080, 'height': 1920}); await pg.goto(f'file://{TMP}/thumb.html'); await pg.wait_for_timeout(500)
        await pg.screenshot(path=f'{TMP}/thumb.png'); await b.close()
asyncio.run(main())
os.system(f'ffmpeg -v error -y -i {TMP}/thumb.png -q:v 2 {PROJ}/thumb.jpg')
print('thumb ok')
