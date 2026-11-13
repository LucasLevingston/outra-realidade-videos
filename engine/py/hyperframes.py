"""Camada HyperFrames do Short: o motor renderiza o mundo 3D + personagens + câmera (OVERLAYS = False no scenes.py)
e o HyperFrames compõe por cima, em HTML + GSAP, a legenda karaokê, os rótulos em pílula, os balões de fala e os flashes,
com o áudio final (mix do longaudio.py). Renderiza o MP4 final com `npx hyperframes render`.

uso:
  python3 hyperframes.py setup                 # npm install hyperframes@0.9.39 gsap@3 em HF_DIR (uma vez por sessão)
  python3 hyperframes.py PROJ build            # monta PROJ/hf/ (index.html + assets) a partir de plan.json e scenes.py
  python3 hyperframes.py PROJ render OUT.mp4    # npx hyperframes render (precisa de PROJ/render_bg.mp4 e PROJ/mix/mix.wav)

Requisitos: Node 22+, ffmpeg e Chrome/Chromium; `setup` instala hyperframes e gsap em HF_DIR (padrão ~/.cache/outra-realidade-hf). Fonte em engine/fonts.
"""
import sys, os, json, shutil, subprocess, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import longform as LF

HF_DIR = os.environ.get('HF_DIR', os.path.expanduser('~/.cache/outra-realidade-hf'))
FONT_DIR = os.environ.get('FONT_DIR', '/usr/share/fonts/truetype/google-fonts')
FONT_LOCAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fonts')
STYLES = {'white': ('#ffffff', '#1d1d2b'), 'yellow': ('#ffd23f', '#1d1d2b'), 'red': ('#e04848', '#ffffff'), 'blue': ('#3a8dde', '#ffffff'),
          'teal': ('#2f9e95', '#ffffff'), 'orange': ('#ff9f1c', '#ffffff'), 'purple': ('#7b5aa6', '#ffffff'), 'green': ('#2f9e4a', '#ffffff')}


def esc(s):
    return html.escape(str(s), quote=True)


def build(proj):
    S, P, scenes = LF.build_scenes(proj)
    out = os.path.join(proj, 'hf'); os.makedirs(os.path.join(out, 'assets'), exist_ok=True)
    total = round(P['total'], 3)
    for f in ('Poppins-Bold.ttf',):
        src = os.path.join(FONT_LOCAL, f) if os.path.exists(os.path.join(FONT_LOCAL, f)) else os.path.join(FONT_DIR, f)
        shutil.copy(src, os.path.join(out, 'assets', f))
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
    # elementos extras do HyperFrames (HF no scenes.py): relógio, contador, etiqueta, carimbo, nome, celular, escolha A/B…
    x_els, x_tl, low = extras(S, words, total)
    els += x_els; tl += x_tl
    # legenda karaokê: uma palavra por vez, centro (~45% da altura); palavras-chave em amarelo
    KEY = set(getattr(S, 'KEYWORDS', []))
    for j, (w, a, b) in enumerate(words):
        nxt = words[j + 1][1] if j + 1 < len(words) else b + 0.4
        end = nxt if nxt - b < 0.5 else b + 0.25
        end = min(end, nxt - 0.02) if j + 1 < len(words) else end   # uma palavra por vez: nunca sobrepor a seguinte
        disp = w.strip(',.;:').upper().replace('"', '').replace('“', '').replace('”', '')
        a0 = max(0, a - 0.02); i = f'w{j}'; key = ' key' if LF.norm(w) in KEY else ''
        if any(x0 <= a0 < x1 for x0, x1 in low): key += ' low'   # card no meio da tela: legenda desce
        if not disp or end - a0 < 0.06: continue   # palavra colada na seguinte (mesmo instante): pula
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
.pill {{ left: 50%; top: {getattr(S, 'PILL_TOP', 255)}px; transform-origin: 50% 50%; translate: -50% 0; padding: 14px 40px; border-radius: 60px; font-size: 64px; line-height: 1.05;
        white-space: nowrap; border: 6px solid #1d1d2b; box-shadow: 0 8px 0 rgba(20,16,28,.35); text-align: center; }}
.pill .small {{ font-size: 28px; opacity: .85; letter-spacing: 1px; }}
.bubble {{ left: 50%; top: 450px; translate: -50% 0; width: 820px; box-sizing: border-box; background: #fff; color: #1d1d2b; border: 6px solid #1d1d2b;
          border-radius: 46px; padding: 46px 40px 34px; font-size: 56px; line-height: 1.12; text-align: center; box-shadow: 0 10px 0 rgba(20,16,28,.3); }}
.bubble .tag {{ position: absolute; left: 34px; top: -30px; color: #fff; font-size: 30px; padding: 6px 22px; border-radius: 30px; border: 5px solid #1d1d2b; }}
.bubble .tail {{ position: absolute; left: 50%; bottom: -34px; width: 50px; height: 50px; background: #fff; border-right: 6px solid #1d1d2b;
                border-bottom: 6px solid #1d1d2b; transform: translateX(-50%) rotate(45deg); }}
.word {{ left: 0; width: 1080px; top: 800px; text-align: center; font-size: 104px; color: #fff; letter-spacing: 1px;
        -webkit-text-stroke: 14px #14101c; paint-order: stroke fill; text-shadow: 0 8px 0 rgba(20,16,28,.45); }}
.word.key {{ color: #ffd23f; }}
.word.low {{ top: 1290px; }}
{EXTRA_CSS}
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


EXTRA_CSS = '''
.hud { left: 50px; top: 150px; background: rgba(18,16,28,.92); border-left: 10px solid #e04848; border-radius: 18px; padding: 12px 26px 14px; color: #fff; }
.hud .d { font-size: 24px; opacity: .7; letter-spacing: 2px; }
.hud .t { font-size: 76px; line-height: 1; }
.hud .s { display: inline-block; margin-top: 8px; background: #ffd23f; color: #1d1d2b; font-size: 22px; padding: 3px 12px; border-radius: 8px; }
.counter { right: 50px; top: 150px; background: rgba(18,16,28,.92); border-radius: 18px; padding: 12px 26px; color: #fff; text-align: center; min-width: 200px; }
.counter .l { font-size: 22px; opacity: .75; letter-spacing: 1px; }
.counter .v { font-size: 92px; line-height: 1; color: #ff5a5a; }
.tag { left: 50%; top: 0; width: 660px; margin-left: -330px; transform-origin: 50% 0; }
.tag .str { position: absolute; left: 50%; top: 0; width: 6px; height: 470px; margin-left: -3px; background: #f4ede0; }
.tag .card { position: absolute; left: 0; top: 460px; width: 660px; box-sizing: border-box; background: #ffd23f; border: 7px solid #1d1d2b; border-radius: 26px;
             padding: 26px 30px; text-align: center; box-shadow: 0 12px 0 rgba(20,16,28,.35); }
.tag .card .h { font-size: 64px; color: #d42a2a; line-height: 1.05; }
.tag .card .b { font-size: 40px; color: #1d1d2b; line-height: 1.1; margin-top: 6px; }
.tag .card .hole { position: absolute; left: 50%; top: -14px; width: 26px; height: 26px; margin-left: -13px; border-radius: 50%; background: #1d1d2b; }
.stamp { left: 50%; top: 620px; translate: -50% 0; border: 12px solid #e04848; color: #e04848; border-radius: 22px; padding: 10px 40px; font-size: 96px;
         letter-spacing: 3px; white-space: nowrap; background: rgba(255,255,255,.88); }
.stamp.sm { top: 720px; font-size: 54px; border-width: 8px; padding: 6px 24px; }
.name { left: 50px; top: 1400px; background: rgba(18,16,28,.92); border-left: 10px solid #e04848; border-radius: 16px; padding: 12px 26px; color: #fff; }
.name .n { font-size: 50px; line-height: 1.05; }
.name .s { font-size: 24px; opacity: .8; letter-spacing: 1px; }
.badge { right: 50px; top: 360px; background: #1d1d2b; color: #fff; font-size: 34px; padding: 10px 24px; border-radius: 12px; letter-spacing: 2px; }
.tone { left: 0; top: 0; width: 1080px; height: 1920px; background: #b08850; mix-blend-mode: color; opacity: .75; }
.phone { left: 50%; top: 420px; width: 600px; height: 760px; margin-left: -300px; background: #1d1d2b; border-radius: 60px; padding: 22px; box-sizing: border-box; }
.phone .scr { width: 100%; height: 100%; background: #efe7da; border-radius: 42px; overflow: hidden; }
.phone .hd { background: #2f9e74; color: #fff; padding: 30px 30px 18px; font-size: 38px; }
.phone .hd small { display: block; font-size: 22px; opacity: .85; }
.phone .m { position: absolute; left: 60px; width: 470px; box-sizing: border-box; background: #fff; border-radius: 20px; padding: 12px 20px; font-size: 32px; color: #1d1d2b; }
.phone .m small { display: block; font-size: 20px; color: #2f9e74; }
.bigclock { left: 50%; top: 560px; margin-left: -300px; width: 600px; background: #1d1d2b; color: #fff; border-radius: 40px; text-align: center; font-size: 200px; line-height: 1.3; border: 8px solid #f4ede0; }
.choice { left: 0; top: 0; width: 1080px; height: 1920px; background: rgba(10,8,22,.62); }
.choice .ti { position: absolute; left: 0; width: 1080px; top: 330px; text-align: center; font-size: 104px; color: #fff; -webkit-text-stroke: 12px #14101c; paint-order: stroke fill; }
.choice .op { position: absolute; left: 110px; width: 860px; box-sizing: border-box; border-radius: 34px; text-align: center; color: #fff; padding: 22px 30px 30px; border: 8px solid transparent; }
.choice .op .k { font-size: 120px; line-height: 1; }
.choice .op .t { font-size: 48px; }
.choice .cta { position: absolute; left: 0; width: 1080px; top: 1300px; text-align: center; font-size: 60px; color: #ffd23f; -webkit-text-stroke: 10px #14101c; paint-order: stroke fill; }
'''


def extras(S, words, total):
    """Elementos extras declarados em HF (lista de dicts) no scenes.py. Âncoras são palavras da narração:
    'palavra' = 1ª ocorrência, 'palavra#2' = 2ª, '>palavra' = última; 'at' liga, 'until' desliga (padrão: próximo item do mesmo grupo).
    kinds: hud(day,time,date) · counter(label,value) · tag(title,sub,stamp,stamp_at) · stamp(text) · name(name,sub) · badge(text)
           tone(color) · phone(title,sub,msgs=[(quem,texto,âncora)]) · bigclock(text) · choice(title,a,b,hl=[(âncora,'a'|'b'|'ab')],cta,cta_at)
    'low': True desce a legenda karaokê enquanto o item estiver na tela."""
    items = getattr(S, 'HF', [])
    if not items: return [], [], []
    def find(anchor, default=None):
        if anchor is None: return default
        if isinstance(anchor, (int, float)): return float(anchor)
        last = anchor.startswith('>'); a = anchor.lstrip('>'); n = 1
        if '#' in a: a, n = a.split('#'); n = int(n)
        hits = [w[1] for w in words if LF.norm(w[0]).startswith(LF.norm(a))]
        if not hits: raise SystemExit(f'HF: âncora "{anchor}" não está na narração')
        return hits[-1] if last else hits[n - 1]
    # início de cada item e fim padrão = início do próximo do mesmo grupo
    for it in items: it['_t0'] = max(0, find(it['at']) - 0.05)
    for k, it in enumerate(items):
        nxt = [o['_t0'] for o in items[k + 1:] if o.get('group', o['kind']) == it.get('group', it['kind'])]
        it['_t1'] = min(total, find(it.get('until'), nxt[0] if nxt else total) + (0.3 if it.get('until') else 0))
    els, tl, low = [], [], []
    for k, it in enumerate(items):
        a, b, kind, i = it['_t0'], it['_t1'], it['kind'], f'x{k}'
        if b - a < 0.15: continue
        if it.get('low'): low.append((a, b))
        clip = lambda cls, inner, style='': f'<div id="{i}" class="clip {cls}" data-start="{a:.3f}" data-duration="{b - a:.3f}" style="{style}">{inner}</div>'
        pop = f'tl.fromTo("#{i}",{{scale:0.6,opacity:0}},{{scale:1,opacity:1,duration:0.25,ease:"back.out(2)"}},{a:.3f});'
        out = f'tl.to("#{i}",{{opacity:0,duration:0.15}},{b - 0.15:.3f});'
        if kind == 'hud':
            els.append(clip('hud', f'<div class="d">{esc(it["day"])}</div><div class="t">{esc(it["time"])}</div><div class="s">{esc(it["date"])}</div>'))
            tl.append(f'tl.fromTo("#{i} .t",{{y:-14,opacity:0.3}},{{y:0,opacity:1,duration:0.2}},{a:.3f});')
        elif kind == 'counter':
            els.append(clip('counter', f'<div class="l">{esc(it["label"])}</div><div class="v">{esc(it["value"])}</div>'))
            tl.append(f'tl.fromTo("#{i} .v",{{scale:1.5}},{{scale:1,duration:0.25,ease:"back.out(2)"}},{a:.3f});')
        elif kind == 'tag':
            st = ''
            if it.get('stamp'):
                st = f'<div class="stamp sm" id="{i}s" style="top:690px;left:62%;transform:rotate(-12deg)">{esc(it["stamp"])}</div>'
            els.append(clip('tag', f'<div class="str"></div><div class="card"><div class="hole"></div><div class="h">{esc(it["title"])}</div><div class="b">{esc(it.get("sub", ""))}</div></div>{st}'))
            tl.append(f'tl.fromTo("#{i}",{{y:-900,rotation:-14}},{{y:0,rotation:0,duration:1.1,ease:"elastic.out(1,0.45)"}},{a:.3f});')
            tl.append(f'tl.to("#{i}",{{rotation:2.5,duration:1.4,ease:"sine.inOut",yoyo:true,repeat:{max(0, int((b - a - 1.1) / 1.4))}}},{a + 1.1:.3f});')
            if it.get('stamp'):
                ts = find(it.get('stamp_at'), a + 1.2)
                tl.append(f'tl.fromTo("#{i}s",{{scale:2.6,opacity:0}},{{scale:1,opacity:1,duration:0.22,ease:"power3.in"}},{ts:.3f});')
            tl.append(out)
        elif kind == 'stamp':
            els.append(clip('stamp', esc(it['text']), 'transform:rotate(-10deg)'))
            tl.append(f'tl.fromTo("#{i}",{{scale:2.6,opacity:0}},{{scale:1,opacity:1,duration:0.22,ease:"power3.in"}},{a:.3f});'); tl.append(out)
        elif kind == 'name':
            els.append(clip('name', f'<div class="n">{esc(it["name"])}</div><div class="s">{esc(it.get("sub", ""))}</div>'))
            tl.append(f'tl.fromTo("#{i}",{{x:-420,opacity:0}},{{x:0,opacity:1,duration:0.3,ease:"power3.out"}},{a:.3f});'); tl.append(out)
        elif kind == 'badge':
            els.append(clip('badge', esc(it['text']))); tl.append(pop); tl.append(out)
        elif kind == 'tone':
            els.append(clip('tone', '', f'background:{it.get("color", "#b08850")}'))
            tl.append(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:0.75,duration:0.3}},{a:.3f});'); tl.append(out)
        elif kind == 'phone':
            ms = ''
            for j, (who, txt, an) in enumerate(it.get('msgs', [])):
                ms += f'<div class="m" id="{i}m{j}" style="top:{200 + j * 118}px"><small>{esc(who)}</small>{esc(txt)}</div>'
                tl.append(f'tl.fromTo("#{i}m{j}",{{x:-60,opacity:0}},{{x:0,opacity:1,duration:0.22,ease:"back.out(2)"}},{find(an):.3f});')
            els.append(clip('phone', f'<div class="scr"><div class="hd">{esc(it["title"])}<small>{esc(it.get("sub", ""))}</small></div>{ms}</div>'))
            tl.append(f'tl.fromTo("#{i}",{{y:900}},{{y:0,duration:0.4,ease:"power3.out"}},{a:.3f});'); tl.append(out)
        elif kind == 'bigclock':
            els.append(clip('bigclock', esc(it['text']))); tl.append(pop); tl.append(out)
        elif kind == 'choice':
            ops = ''
            for j, (key, col, top) in enumerate((('a', '#2f9e74', 640), ('b', '#7b4fc4', 920))):
                ops += f'<div class="op" id="{i}{key}" style="top:{top}px;background:{col}"><div class="k">{key.upper()}</div><div class="t">{esc(it[key])}</div></div>'
                tl.append(f'tl.fromTo("#{i}{key}",{{y:120,opacity:0}},{{y:0,opacity:1,duration:0.3,ease:"back.out(1.6)"}},{a + 0.15 + j * 0.15:.3f});')
            cta = f'<div class="cta" id="{i}c">{esc(it.get("cta", ""))}</div>' if it.get('cta') else ''
            els.append(clip('choice', f'<div class="ti">{esc(it.get("title", "VOCÊ DECIDE"))}</div>{ops}{cta}'))
            tl.append(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:1,duration:0.25}},{a:.3f});')
            for (an, which) in it.get('hl', []):
                t = find(an)
                for key in 'ab':
                    on = key in which
                    tl.append(f'tl.to("#{i}{key}",{{scale:{1.06 if on and which != "ab" else 1},opacity:{1 if on else 0.4},borderColor:"{"#ffd23f" if on and which != "ab" else "transparent"}",duration:0.2}},{t:.3f});')
            if cta: tl.append(f'tl.fromTo("#{i}c",{{scale:0.4,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2)"}},{find(it.get("cta_at"), a + 1):.3f});')
    return els, tl, low


def render(proj, out_mp4):
    hf = os.path.join(proj, 'hf')
    shutil.copy(os.path.join(proj, 'render_bg.mp4'), os.path.join(hf, 'assets', 'bg.mp4'))
    shutil.copy(os.path.join(proj, 'mix', 'mix.wav'), os.path.join(hf, 'assets', 'mix.wav'))
    env = dict(os.environ, HYPERFRAMES_TELEMETRY='0')
    if not env.get('HYPERFRAMES_BROWSER_PATH'):  # usa o Chromium já instalado (o download do headless-shell é bloqueado aqui)
        import glob
        c = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux64/chrome'))  # só existe na nuvem; no computador o HyperFrames acha o Chrome sozinho
        c = c or [x for x in ('/usr/bin/google-chrome', '/usr/bin/chromium') if os.path.exists(x)]
        if c: env['HYPERFRAMES_BROWSER_PATH'] = c[-1]
    cmd = ['npx', '--prefix', HF_DIR, 'hyperframes', 'render', os.path.abspath(hf), '-o', os.path.abspath(out_mp4), '-q', 'delivery', '-w', '2', '--no-browser-gpu']
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
