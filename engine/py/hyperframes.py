"""Camada HyperFrames do Short: o motor renderiza o mundo 3D + personagens + câmera (OVERLAYS = False no scenes.py)
e o HyperFrames compõe por cima, em HTML + GSAP, a legenda karaokê, os rótulos em pílula, os balões de fala e os flashes,
com o áudio final (mix do longaudio.py). Renderiza o MP4 final com `npx hyperframes render`.

uso:
  python3 hyperframes.py setup                 # npm install hyperframes@0.9.39 gsap@3 em HF_DIR (uma vez por sessão)
  python3 hyperframes.py PROJ build            # monta PROJ/hf/ (index.html + assets) a partir de plan.json e scenes.py
  python3 hyperframes.py PROJ render OUT.mp4    # npx hyperframes render (precisa de PROJ/render_bg.mp4 e PROJ/mix/mix.wav)

Requisitos: `npm install hyperframes gsap` em HF_DIR (padrão /home/claude/hf); fontes Poppins locais.
"""
import sys, os, json, shutil, subprocess, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import longform as LF

HF_DIR = os.environ.get('HF_DIR', '/home/claude/hf')
FONT_DIR = '/usr/share/fonts/truetype/google-fonts'
STYLES = {'white': ('#ffffff', '#1d1d2b'), 'yellow': ('#ffd23f', '#1d1d2b'), 'red': ('#e04848', '#ffffff'), 'blue': ('#3a8dde', '#ffffff'),
          'teal': ('#2f9e95', '#ffffff'), 'orange': ('#ff9f1c', '#ffffff'), 'purple': ('#7b5aa6', '#ffffff'), 'green': ('#2f9e4a', '#ffffff')}


def esc(s):
    return html.escape(str(s), quote=True)


def build(proj):
    S, P, scenes = LF.build_scenes(proj)
    out = os.path.join(proj, 'hf'); os.makedirs(os.path.join(out, 'assets'), exist_ok=True)
    total = round(P['total'], 3)
    for f in ('Poppins-Bold.ttf',):
        shutil.copy(os.path.join(FONT_DIR, f), os.path.join(out, 'assets', f))
    shutil.copy(os.path.join(HF_DIR, 'node_modules/gsap/dist/gsap.min.js'), os.path.join(out, 'assets', 'gsap.min.js'))
    els, tl = [], []
    # rótulos (pílulas no topo), um por vez por cena
    n = 0
    for sc in scenes:
        for lb in sc.get('labels', []):
            ts = sc['t0'] + lb['t']; te = min(sc['t1'], sc['t0'] + lb.get('t_end', 999))
            if te - ts < 0.15: continue
            bg, fg = STYLES.get(lb.get('style', 'white'), STYLES['white']); n += 1; i = f'lb{n}'
            small = f'<div class="small">{esc(lb["small"])}</div>' if lb.get('small') else ''
            els.append(f'<div id="{i}" class="clip pill" data-start="{ts:.3f}" data-duration="{te - ts:.3f}" style="background:{bg};color:{fg}">{small}{esc(lb["text"])}</div>')
            tl.append(f'tl.fromTo("#{i}",{{scale:0.2,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2.2)"}},{ts:.3f});')
            if te - ts > 0.5:  # saída só depois que a entrada terminou (sem tweens sobrepostos)
                tl.append(f'tl.to("#{i}",{{opacity:0,scale:0.9,duration:0.18}},{te - 0.18:.3f});')
    # balões de fala
    words = P.get('words', [])
    for k, (txt, name, col, w0, w1) in enumerate(getattr(S, 'BUBBLES', [])):
        seq = list(reversed(words)) if w0.startswith('>') else words
        a = next((w[1] for w in seq if LF.norm(w[0]).startswith(LF.norm(w0))), None)
        b = next((w[2] for w in words if a is not None and w[1] >= a and LF.norm(w[0]).startswith(LF.norm(w1))), None)
        if a is None or b is None: continue
        a -= 0.05; b = min(total, b + 0.5); i = f'bb{k}'
        els.append(f'<div id="{i}" class="clip bubble" data-start="{a:.3f}" data-duration="{b - a:.3f}"><div class="tag" style="background:{col}">{esc(name)}</div>{esc(txt)}<div class="tail"></div></div>')
        tl.append(f'tl.fromTo("#{i}",{{scale:0.3,opacity:0,y:30}},{{scale:1,opacity:1,y:0,duration:0.32,ease:"back.out(1.8)"}},{a:.3f});')
        tl.append(f'tl.to("#{i}",{{opacity:0,duration:0.2}},{b - 0.2:.3f});')
    # legenda karaokê: uma palavra por vez, centro (~45% da altura); palavras-chave em amarelo
    KEY = set(getattr(S, 'KEYWORDS', []))
    for j, (w, a, b) in enumerate(words):
        nxt = words[j + 1][1] if j + 1 < len(words) else b + 0.4
        end = nxt if nxt - b < 0.5 else b + 0.25
        disp = w.strip(',.;:').upper().replace('"', '').replace('“', '').replace('”', '')
        if not disp: continue
        a0 = max(0, a - 0.02); i = f'w{j}'; key = ' key' if LF.norm(w) in KEY else ''
        els.append(f'<div id="{i}" class="clip word{key}" data-start="{a0:.3f}" data-duration="{max(0.08, end - a0):.3f}">{esc(disp)}</div>')
        tl.append(f'tl.fromTo("#{i}",{{scale:1.18}},{{scale:1,duration:0.14,ease:"power2.out"}},{a0:.3f});')
    # flashes brancos (troca de lugar / impacto)
    for k, sc in enumerate(scenes):
        for ft in sc.get('flash_abs', []):
            i = f'fl{k}'
            els.append(f'<div id="{i}" class="clip flash" data-start="{ft:.3f}" data-duration="0.22"></div>')
            tl.append(f'tl.fromTo("#{i}",{{opacity:1}},{{opacity:0,duration:0.2,ease:"none"}},{ft:.3f});')
    doc = f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face {{ font-family: Pop; src: url(assets/Poppins-Bold.ttf); font-weight: 700; }}
html, body {{ margin: 0; background: #000; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Pop, sans-serif; font-weight: 700; }}
.clip {{ position: absolute; }}
#bg {{ left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
.pill {{ left: 50%; top: 255px; transform-origin: 50% 50%; translate: -50% 0; padding: 14px 40px; border-radius: 60px; font-size: 64px; line-height: 1.05;
        white-space: nowrap; border: 6px solid #1d1d2b; box-shadow: 0 8px 0 rgba(20,16,28,.35); text-align: center; }}
.pill .small {{ font-size: 28px; opacity: .85; letter-spacing: 1px; }}
.bubble {{ left: 50%; top: 380px; translate: -50% 0; width: 820px; box-sizing: border-box; background: #fff; color: #1d1d2b; border: 6px solid #1d1d2b;
          border-radius: 46px; padding: 46px 40px 34px; font-size: 56px; line-height: 1.12; text-align: center; box-shadow: 0 10px 0 rgba(20,16,28,.3); }}
.bubble .tag {{ position: absolute; left: 34px; top: -30px; color: #fff; font-size: 30px; padding: 6px 22px; border-radius: 30px; border: 5px solid #1d1d2b; }}
.bubble .tail {{ position: absolute; left: 50%; bottom: -34px; width: 50px; height: 50px; background: #fff; border-right: 6px solid #1d1d2b;
                border-bottom: 6px solid #1d1d2b; transform: translateX(-50%) rotate(45deg); }}
.word {{ left: 0; width: 1080px; top: 800px; text-align: center; font-size: 104px; color: #fff; letter-spacing: 1px;
        -webkit-text-stroke: 14px #14101c; paint-order: stroke fill; text-shadow: 0 8px 0 rgba(20,16,28,.45); }}
.word.key {{ color: #ffd23f; }}
.flash {{ left: 0; top: 0; width: 1080px; height: 1920px; background: #fff; }}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-fps="30" data-duration="{total}">
<video id="bg" class="clip" src="assets/bg.mp4" data-start="0" data-duration="{total}" muted playsinline></video>
<audio id="mix" class="clip" src="assets/mix.wav" data-start="0" data-duration="{total}" data-volume="1"></audio>
{chr(10).join(els)}
<script src="assets/gsap.min.js"></script>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tl)}
tl.set({{}}, {{}}, {total});
window.__timelines = window.__timelines || {{}};
window.__timelines["root"] = tl;
</script>
</div></body></html>
'''
    open(os.path.join(out, 'index.html'), 'w').write(doc)
    json.dump({'name': os.path.basename(proj.rstrip('/'))}, open(os.path.join(out, 'hyperframes.json'), 'w'))
    print(f'hf: {len(els)} elementos, {total:.1f}s -> {out}/index.html')


def render(proj, out_mp4):
    hf = os.path.join(proj, 'hf')
    shutil.copy(os.path.join(proj, 'render_bg.mp4'), os.path.join(hf, 'assets', 'bg.mp4'))
    shutil.copy(os.path.join(proj, 'mix', 'mix.wav'), os.path.join(hf, 'assets', 'mix.wav'))
    env = dict(os.environ, HYPERFRAMES_TELEMETRY='0')
    if not env.get('HYPERFRAMES_BROWSER_PATH'):  # usa o Chromium já instalado (o download do headless-shell é bloqueado aqui)
        import glob
        c = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux64/chrome'))
        if c: env['HYPERFRAMES_BROWSER_PATH'] = c[-1]
    cmd = ['npx', '--prefix', HF_DIR, 'hyperframes', 'render', hf, '-o', os.path.abspath(out_mp4), '-q', 'delivery', '-w', '2', '--no-browser-gpu']
    print(' '.join(cmd), flush=True)
    subprocess.run(cmd, check=True, env=env, cwd=HF_DIR)
    # o render do HyperFrames remixa/normaliza o áudio (saiu ~3 dB acima): troca pelo mix original do longaudio.py,
    # mantendo os níveis fixos da skill (música −6 dB, ~−14 LUFS). O vídeo é copiado sem recodificar.
    tmp = out_mp4 + '.tmp.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out_mp4, '-i', os.path.join(proj, 'mix', 'mix.wav'), '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', '-shortest', tmp], check=True)
    os.replace(tmp, out_mp4)
    print(out_mp4, round(os.path.getsize(out_mp4) / 1e6, 1), 'MB')


def setup():
    os.makedirs(HF_DIR, exist_ok=True)
    if not os.path.exists(os.path.join(HF_DIR, 'package.json')):
        subprocess.run(['npm', 'init', '-y'], cwd=HF_DIR, check=True, capture_output=True)
    subprocess.run(['npm', 'install', '-s', 'hyperframes@0.9.39', 'gsap@3'], cwd=HF_DIR, check=True)
    subprocess.run(['npx', 'hyperframes', 'telemetry', 'disable'], cwd=HF_DIR, capture_output=True)
    print('hyperframes: pronto em', HF_DIR)


if __name__ == '__main__':
    if sys.argv[1] == 'setup': setup(); sys.exit()
    proj, cmd = sys.argv[1], sys.argv[2]
    if cmd == 'build': build(proj)
    elif cmd == 'render': render(proj, sys.argv[3])
