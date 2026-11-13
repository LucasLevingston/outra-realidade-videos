"""Montagem do vídeo longo (16:9): alinhamento roteiro↔áudio, linha do tempo, placas, render em blocos retomável.
uso: python3 longform.py PROJ_DIR plan|plates|sheet|render|audio|final
PROJ_DIR contém: script/*.txt, audio/*.wav + words.json, scenes.py (PRE, SEG, ORDER, CARDS, LT)."""
import sys, os, re, json, math, unicodedata, difflib, subprocess, importlib.util, hashlib
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

FPS = 30
GAP = 2.5        # silêncio do cartão de capítulo antes de cada segmento (exceto o primeiro)
TAIL = 5.0       # cartão final

def norm(w):
    w = unicodedata.normalize('NFD', w.lower()); w = ''.join(c for c in w if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]', '', w)

def load_scenes(proj):
    spec = importlib.util.spec_from_file_location('scenes', os.path.join(proj, 'scenes.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

NUMS = {'11': 'onze', '40': 'quarenta', '62': 'sessenta e dois', '12': 'doze'}
def tokens_from_text(t):
    out = []
    for w in t.split():
        out.append(w)
    return out

def fmt(S):
    return getattr(S, 'FORMAT', 'long')

def plan(proj):
    S = load_scenes(proj)
    global GAP, TAIL
    GAP = getattr(S, 'GAP', GAP); TAIL = getattr(S, 'TAIL', TAIL)
    words = json.load(open(os.path.join(proj, 'audio', 'words.json')))
    timeline = []; t = 0.0; segs = []
    for si, seg in enumerate(S.ORDER):
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(proj, 'audio', seg + '.wav')], capture_output=True, text=True).stdout)
        if si > 0: t += GAP
        segs.append(dict(seg=seg, start=t, dur=dur)); t += dur
    total = t + TAIL
    shots = []; subs = []; talk = []; allwords = []
    for sg in segs:
        seg = sg['seg']; T0 = sg['start']
        paras = [p.strip() for p in open(os.path.join(proj, 'script', seg + '.txt')).read().split('\n\n') if p.strip()]
        assert len(paras) == len(S.SEG[seg]), (seg, len(paras), len(S.SEG[seg]))
        # tokens do roteiro com (parágrafo, frase)
        stoks = []
        for pi, p in enumerate(paras):
            sents = re.split(r'(?<=[.!?])\s+(?=[A-ZÀ-Ú"“])', p)
            for si_, s in enumerate(sents):
                for w in s.split():
                    n = norm(w)
                    if n: stoks.append((n, pi, si_, w))
        W = words[seg]; wn = [norm(w[0]) for w in W]
        sm = difflib.SequenceMatcher(None, [x[0] for x in stoks], wn, autojunk=False)
        tmap = [None] * len(stoks)
        for a, b, n in sm.get_matching_blocks():
            for k in range(n): tmap[a + k] = (W[b + k][1], W[b + k][2])
        # interpola faltantes
        known = [i for i, v in enumerate(tmap) if v]
        for i in range(len(tmap)):
            if tmap[i] is None:
                prv = max([k for k in known if k < i], default=None); nxt = min([k for k in known if k > i], default=None)
                if prv is None: tmap[i] = (0.0, 0.2)
                elif nxt is None: tmap[i] = (tmap[prv][1], tmap[prv][1] + 0.2)
                else:
                    f = (i - prv) / (nxt - prv); a = tmap[prv][1] + (tmap[nxt][0] - tmap[prv][1]) * f; tmap[i] = (a, a + 0.15)
        # frases
        sentences = {}
        for i, (n, pi, si_, w) in enumerate(stoks):
            k = (pi, si_)
            sentences.setdefault(k, {'words': [], 't0': tmap[i][0], 't1': tmap[i][1]})
            sentences[k]['words'].append((w, tmap[i][0], tmap[i][1])); sentences[k]['t1'] = tmap[i][1]
        keys = sorted(sentences)
        for k in keys:
            for (w, a, b) in sentences[k]['words']: allwords.append((w, T0 + a, T0 + b))
        # legendas: pedaços de até ~11 palavras
        for k in keys:
            ws = sentences[k]['words']
            chunks = [ws[i:i + 11] for i in range(0, len(ws), 11)]
            if len(chunks) > 1 and len(chunks[-1]) < 4: chunks[-2] += chunks[-1]; chunks.pop()
            for c in chunks:
                subs.append(dict(text=' '.join(w for w, _, _ in c), t0=T0 + c[0][1], t1=T0 + c[-1][2]))
            txt = ' '.join(w for w, _, _ in ws)
            if '"' in txt or '“' in txt:
                talk.append((T0 + sentences[k]['t0'], T0 + sentences[k]['t1']))
        # parágrafos -> tempos contíguos
        pstart = [min(sentences[k]['t0'] for k in keys if k[0] == pi) for pi in range(len(paras))]
        for pi in range(len(paras)):
            p0 = T0 + (pstart[pi] if pi > 0 else -(GAP if sg['start'] > 0 else 0))
            p1 = T0 + (pstart[pi + 1] if pi + 1 < len(paras) else sg['dur'] + (GAP if seg != S.ORDER[-1] else TAIL))
            if pi == 0 and sg['start'] == 0: p0 = 0
            shots_p = S.SEG[seg][pi]
            # divide em frases mais próximas da divisão igual
            sent_starts = sorted(T0 + sentences[k]['t0'] for k in keys if k[0] == pi)
            n = len(shots_p)
            # se o parágrafo for longo (>16 s) e só tiver 1 plano, repete com outro movimento
            if n == 1 and p1 - p0 > 16:
                a = shots_p[0]; alt = {'push': 'panR', 'pull': 'panL', 'hold': 'orbit', 'panR': 'push', 'panL': 'pull', 'orbit': 'push', 'drama': 'hold', 'tiltU': 'pull', 'tiltD': 'push'}
                shots_p = [a, (a[0], a[1], alt.get(a[2], 'hold'), a[3], dict(a[4], lab=[]))]; n = 2
            cuts = [p0]
            for j in range(1, n):
                ideal = p0 + (p1 - p0) * j / n
                cands = [s for s in sent_starts if cuts[-1] + 2.5 < s < p1 - 2.5]
                cuts.append(min(cands, key=lambda s: abs(s - ideal)) if cands else max(ideal, cuts[-1] + (p1 - cuts[-1]) / (n - j + 1)))  # nunca volta no tempo
            cuts.append(p1)
            # palavras do parágrafo pra rótulos
            pw = [(norm(w), T0 + a) for k in keys if k[0] == pi for (w, a, b) in sentences[k]['words']]
            for j, shot in enumerate(shots_p):
                preset, lt, move, chars, ex = shot
                st0, st1 = cuts[j], cuts[j + 1]
                shots.append(dict(seg=seg, para=pi, preset=preset, light=S.LT[lt], move=move, chars=chars, ex=ex, t0=st0, t1=st1, pw=pw))
    json.dump(dict(segs=segs, total=total, shots=shots, subs=subs, talk=talk, words=allwords, gap=GAP, tail=TAIL), open(os.path.join(proj, 'plan.json'), 'w'), ensure_ascii=False)
    print(f'total {total:.1f}s ({total/60:.2f} min), {len(shots)} planos, {len(subs)} legendas')

def plate_spec(S, preset, light, opts):
    set_, pos, look, fov, slots = S.PRE[preset]
    W, H = (1440, 2560) if fmt(S) == 'short' else (2560, 1440)
    if fmt(S) == 'short':
        fov = min(72, fov * 1.4)
        dist = math.dist(pos, look); look = [look[0], look[1] + 0.16 * dist, look[2]]  # sobe a câmera: personagens descem no quadro vertical
    spec = {'set': set_, 'light': light, 'w': W, 'h': H, 'cam': {'pos': pos, 'look': look, 'fov': fov}, 'opts': opts or {}}
    spec['id'] = preset + '_' + light + '_' + hashlib.md5(json.dumps(spec, sort_keys=True).encode()).hexdigest()[:6]
    return spec

def parse_char(s, slots):
    m = re.match(r'(\w+)(!?)@([\w.,\-]+):(\w+)/(\w+)(\^[-\d.]+,[-\d.]+)?((?:\+\w+)*)(\*[\d.]+)?', s)
    name, flip, slot, arms, face, look, extra, scl = m.groups()
    if slot in slots: x, z = slots[slot]
    else: x, z = map(float, slot.split(','))
    lk = tuple(map(float, look[1:].split(','))) if look else (0, 0)
    ex = tuple(e for e in extra.split('+') if e)
    d = dict(name=name, flip=bool(flip), x=x, z=z, arms=arms, face=face, look=lk, extra=ex)
    if scl: d['scale'] = float(scl[1:])
    return d

def build_scenes(proj):
    S = load_scenes(proj); P = json.load(open(os.path.join(proj, 'plan.json')))
    scenes = []
    for sh in P['shots']:
        ex = sh['ex']; spec = plate_spec(S, sh['preset'], sh['light'], ex.get('opts'))
        slots = S.PRE[sh['preset']][4]
        chars = [parse_char(c, slots) for c in sh['chars']]
        def wt(word, after=None):
            n = norm(word)
            for w, t in sh['pw']:
                if w.startswith(n) and sh['t0'] - 0.5 <= t < sh['t1']: return t
            return None
        labels = []
        for i, lb in enumerate(ex.get('lab', [])):
            t = wt(lb[0])
            if t is None: t = sh['t0'] + 0.6 + i * 2.0
            labels.append(dict(t=t - sh['t0'] - 0.05, text=lb[1], style=lb[2], small=lb[3] if len(lb) > 3 else None))
        # rótulos simultâneos: empilha
        for i in range(1, len(labels)):
            labels[i - 1]['t_end'] = labels[i]['t']
        sc = dict(plate={'id': spec['id']}, spec=spec, t0=sh['t0'], t1=sh['t1'], move=sh['move'], chars=chars, labels=labels, fx=ex.get('fx', []),
                  speaker=ex.get('speaker'), seg=sh['seg'], para=sh['para'])
        if ex.get('shake'):
            t = wt(ex['shake']); sc['shake'] = [(t if t else sh['t0'] + 1, 22)]
        if ex.get('flash'):
            t = wt(ex['flash']); sc['flashes'] = [(t if t else sh['t0'] + 1) - sh['t0']]; sc['flash_abs'] = [(t if t else sh['t0'] + 1)]
            if 'lightning' not in sc['fx']: sc['fx'] = sc['fx'] + ['lightning']
        scenes.append(sc)
    return S, P, scenes

if __name__ == '__main__':
    proj, cmd = sys.argv[1], sys.argv[2]
    if cmd == 'plan': plan(proj)
    elif cmd == 'plates':
        S, P, scenes = build_scenes(proj)
        specs = {sc['spec']['id']: sc['spec'] for sc in scenes}
        json.dump(list(specs.values()), open(os.path.join(proj, 'plates.json'), 'w'))
        print(len(specs), 'placas')
        import plates; plates.render_all(list(specs.values()), os.path.join(proj, 'plates'))

# ---------------------------------------------------------------- render
from PIL import Image, ImageDraw, ImageFont
import bisect
FONTB = (__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'fonts', 'Poppins-Bold.ttf'))
_card_cache = {}
def card_img(a, b):
    k = (a, b)
    if k in _card_cache: return _card_cache[k]
    im = Image.new('RGBA', (1920, 1080), (14, 12, 48, 215)); d = ImageDraw.Draw(im)
    for i in range(36):
        ang = i * 10
        d.pieslice([960 - 1600, 540 - 1600, 960 + 1600, 540 + 1600], ang, ang + 5, fill=(255, 210, 63, 18))
    d.ellipse([960 - 90, 300 - 90, 960 + 90, 300 + 90], outline=(255, 255, 255, 200), width=8)
    for i in range(24):
        d.arc([960 - 90, 300 - 90, 960 + 90, 300 + 90], i * 15, i * 15 + 7, fill=(14, 12, 48, 255), width=10)
    f1 = ImageFont.truetype(FONTB, 64); f2 = ImageFont.truetype(FONTB, 104)
    d.text((960, 470), a, font=f1, fill=(255, 210, 63, 255), anchor='mm', stroke_width=6, stroke_fill=(16, 12, 24, 255))
    d.text((960, 600), b, font=f2, fill=(255, 255, 255, 255), anchor='mm', stroke_width=8, stroke_fill=(16, 12, 24, 255))
    d.rounded_rectangle([960 - 200, 990, 960 + 200, 1050], 30, fill=(255, 210, 63, 255), outline=(16, 12, 24, 255), width=5)
    d.text((960, 1021), 'OUTRA REALIDADE', font=ImageFont.truetype(FONTB, 34), fill=(16, 12, 24, 255), anchor='mm')
    _card_cache[k] = im; return im

class Renderer:
    def __init__(s, proj):
        import comp
        s.comp = comp; s.proj = proj
        s.S, s.P, s.scenes = build_scenes(proj)
        s.t0s = [sc['t0'] for sc in s.scenes]
        s.subs = s.P['subs']; s.sub_t0 = [x['t0'] for x in s.subs]
        s.talk = s.P['talk']
        import scipy.io.wavfile as wf
        env = []
        for sg in s.P['segs']:
            sr, a = wf.read(os.path.join(proj, 'audio', sg['seg'] + '.wav')); a = a.astype(np.float32) / 32768
            env.append((sg['start'], sr, a))
        s.env_src = env
        s.cards = []
        for sg in s.P['segs']:
            if sg['seg'] in s.S.CARDS:
                ends = [sh['t1'] for sh in s.P['shots'] if sh['seg'] == sg['seg'] and sh['para'] == 0]
                s.cards.append((sg['start'] - GAP, max(ends), s.S.CARDS[sg['seg']]))
        s.flashes = [t for sc in s.scenes for t in sc.get('flash_abs', [])]
        s.short = fmt(s.S) == 'short'
        s.out = (1080, 1920) if s.short else (1920, 1080)
        s.ctx = {'pdir': os.path.join(proj, 'plates'), 'talking': s.talking, 'env': s.env, 'out': s.out}
        s.words = s.P.get('words', []); s.word_t0 = [w[1] for w in s.words]
        s.KEY = set(getattr(s.S, 'KEYWORDS', []))
        s.TAIL = s.P.get('tail', TAIL); s.GAP = s.P.get('gap', GAP)
        s.bubbles = getattr(s.S, 'BUBBLES', [])
        # OVERLAYS = False no scenes.py: o motor renderiza só o mundo 3D + personagens + câmera;
        # rótulos, balões e legendas ficam para a camada HyperFrames (hyperframes.py)
        s.overlays = getattr(s.S, 'OVERLAYS', True); s.ctx['overlays'] = s.overlays
    def talking(s, t):
        return any(a <= t <= b for a, b in s.talk)
    def env(s, t):
        for st, sr, a in s.env_src:
            i = int((t - st) * sr)
            if 0 <= i < len(a) - 800: return float(np.sqrt(np.mean(a[i:i + 800] ** 2)) * 12)
        return 0.0
    def frame(s, t):
        i = max(0, bisect.bisect_right(s.t0s, t) - 1); sc = s.scenes[i]
        o = s.comp.render_frame(sc, t, s.ctx)
        # transição: flash curto nas trocas de cenário (não em mesmo preset)
        if s.short:
            return s.frame_short(o, t)
        # legenda
        j = bisect.bisect_right(s.sub_t0, t) - 1
        if j >= 0 and s.subs[j]['t0'] <= t <= s.subs[j]['t1'] + 0.35:
            im = s.comp.subtitle_img(s.subs[j]['text'])
            o.alpha_composite(im, (960 - im.width // 2, 1050 - im.height))
        for (a, b, (l1, l2)) in s.cards:
            if a <= t < b:
                al = min(1.0, (t - a) / 0.35, (b - t) / 0.45)
                c = card_img(l1, l2)
                if al < 1: c = s.comp.UI.with_alpha(c, max(0, al))
                o.alpha_composite(c)
        if not s.short and t >= s.P['total'] - s.TAIL:
            u = t - (s.P['total'] - TAIL)
            c = card_img('OBRIGADO POR ASSISTIR', 'INSCREVA-SE')
            o.alpha_composite(s.comp.UI.with_alpha(c, min(1, u / 0.5)))
        for ft in s.flashes:
            if 0 <= t - ft < 0.2:
                o.alpha_composite(Image.new('RGBA', o.size, (255, 255, 255, int(255 * (1 - (t - ft) / 0.2)))))
        # fade de entrada/saída
        T = s.P['total']
        if not s.short and t > T - 0.6: o.alpha_composite(Image.new('RGBA', o.size, (0, 0, 0, int(255 * min(1, (t - (T - 0.6)) / 0.6)))))
        return o.convert('RGB')

def _frame_short(s, o, t):
    if not s.overlays:
        return o.convert('RGB')
    # bolhas de fala (texto, nome, cor, palavra inicial, palavra final)
    for (txt, name, col, w0, w1) in s.bubbles:
        # w0 com prefixo '>' = última ocorrência da palavra (ex.: '>você' na pergunta final)
        a = next((w[1] for w in (reversed(s.words) if w0.startswith('>') else s.words) if norm(w[0]).startswith(norm(w0))), None)
        b = next((w[2] for w in s.words if a is not None and w[1] >= a and norm(w[0]).startswith(norm(w1))), None)
        if a is not None and b is not None and a - 0.05 <= t <= b + 0.5:
            k = s.comp.back((t - a + 0.05) / 0.3); al = min(1, (b + 0.5 - t) / 0.2)
            bb = s.comp.UI.bubble(txt, name, col, 860, 62, tailx=0.5)
            bb = s.comp.UI.with_alpha(s.comp.UI.scaled(bb, k), al)
            s.comp.UI.paste(o, bb, 540 - bb.width / 2, 470 - bb.height / 2)
    # legenda karaokê: uma palavra por vez, centro (~45% da altura)
    j = bisect.bisect_right(s.word_t0, t + 0.02) - 1
    if j >= 0:
        w, a, b = s.words[j]
        nxt = s.words[j + 1][1] if j + 1 < len(s.words) else b + 0.4
        end = nxt if nxt - b < 0.5 else b + 0.25
        if t <= end:
            disp = w.strip(',.;:').upper().replace('"', '').replace('“', '').replace('”', '')
            key = norm(w) in s.KEY
            k = 1 + 0.18 * (1 - s.comp.eout((t - a + 0.02) / 0.14))
            im = s.comp.UI.scaled(s.comp.UI.word_img(disp, key), k)
            s.comp.UI.paste(o, im, 540 - im.width / 2, 864 - im.height / 2)
    for ft in s.flashes:
        if 0 <= t - ft < 0.2:
            o.alpha_composite(Image.new('RGBA', o.size, (255, 255, 255, int(255 * (1 - (t - ft) / 0.2)))))
    return o.convert('RGB')
Renderer.frame_short = _frame_short

_R = None
def _chunk(args):
    proj, f0, f1, path = args
    global _R
    if _R is None: _R = Renderer(proj)
    tmp = path + '.tmp.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % _R.out, '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for f in range(f0, f1):
        p.stdin.write(_R.frame(f / FPS).tobytes())
    p.stdin.close(); p.wait(); os.replace(tmp, path)
    return path

def render(proj, workers=2, chunk_s=45):
    P = json.load(open(os.path.join(proj, 'plan.json')))
    N = int(round(P['total'] * FPS)); step = int(chunk_s * FPS)
    os.makedirs(os.path.join(proj, 'chunks'), exist_ok=True)
    jobs = [(proj, f, min(N, f + step), os.path.join(proj, 'chunks', f'part_{f // step:03d}.mp4')) for f in range(0, N, step)]
    todo = [j for j in jobs if not os.path.exists(j[3])]
    print(f'{len(jobs)} blocos, faltam {len(todo)}', flush=True)
    from multiprocessing import Pool
    import time
    t0 = time.time()
    with Pool(workers) as pool:
        for k, path in enumerate(pool.imap_unordered(_chunk, todo)):
            print(f'ok {os.path.basename(path)} ({k + 1}/{len(todo)}) {time.time() - t0:.0f}s', flush=True)
    open(os.path.join(proj, 'chunks', 'list.txt'), 'w').write(''.join(f"file '{os.path.abspath(j[3])}'\n" for j in jobs))

def sheet(proj, out, n=24):
    R = Renderer(proj)
    ts = [float(x) for x in sys.argv[4].split(',')] if len(sys.argv) > 4 else [sc['t0'] + (sc['t1'] - sc['t0']) * 0.6 for sc in R.scenes[::max(1, len(R.scenes) // n)]]
    tw, th = (270, 480) if R.short else (480, 270)
    ims = [R.frame(t).resize((tw, th)) for t in ts]
    for im, t in zip(ims, ts): ImageDraw.Draw(im).text((6, 4), f'{t:.1f}', fill=(255, 0, 0), font=ImageFont.truetype(FONTB, 18))
    cols = 8 if R.short else 4; rows = (len(ims) + cols - 1) // cols
    sh = Image.new('RGB', (cols * tw, rows * th))
    for i, im in enumerate(ims): sh.paste(im, ((i % cols) * tw, (i // cols) * th))
    sh.save(out)

if __name__ == '__main__' and sys.argv[2] in ('render', 'sheet'):
    if sys.argv[2] == 'render': render(sys.argv[1], int(os.environ.get('WORKERS', 2)))
    else: sheet(sys.argv[1], sys.argv[3])

def final(proj, out_path):
    """Junta os blocos + mix. Short: CRF 18 (12–20 Mbps). Longo: 2 passes com bitrate calculado pra ficar < 95 MB."""
    P = json.load(open(os.path.join(proj, 'plan.json'))); S = load_scenes(proj)
    lst = os.path.join(proj, 'chunks', 'list.txt'); mix = os.path.join(proj, 'mix', 'mix.wav')
    cat = os.path.join(proj, 'chunks', 'all.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', cat], check=True)
    if fmt(S) == 'short':
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', cat, '-i', mix, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                        '-maxrate', '16M', '-bufsize', '32M', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', '-shortest', out_path], check=True)
    else:
        dur = P['total']; kbps = int(94 * 8 * 1000 / dur) - 80 - 8
        common = ['-c:v', 'libx264', '-preset', 'slow', '-tune', 'animation', '-b:v', f'{kbps}k', '-maxrate', f'{kbps * 3}k', '-bufsize', f'{kbps * 6}k', '-pix_fmt', 'yuv420p']
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', cat] + common + ['-pass', '1', '-passlogfile', '/tmp/p2', '-an', '-f', 'null', '/dev/null'], check=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', cat, '-i', mix, '-map', '0:v', '-map', '1:a'] + common + ['-pass', '2', '-passlogfile', '/tmp/p2',
                        '-c:a', 'aac', '-b:a', '80k', '-ar', '48000', '-movflags', '+faststart', '-shortest', out_path], check=True)
    print(out_path, os.path.getsize(out_path) / 1e6, 'MB')

if __name__ == '__main__' and sys.argv[2] == 'final':
    final(sys.argv[1], sys.argv[3])
