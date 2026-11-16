"""Áudio do vídeo longo: narração montada nos tempos do plano + trilha sintetizada + efeitos + mix com níveis fixos.
uso: python3 longaudio.py PROJ_DIR   -> PROJ_DIR/mix/{narr,music,sfx,mix}.wav e imprime os níveis."""
import sys, os, json, re, subprocess
import numpy as np, scipy.io.wavfile as wf
from scipy.signal import butter, sosfilt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
SR = 48000
rng = np.random.default_rng(3)

def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
def tt(d): return np.arange(int(SR * d)) / SR
def mid(n): return 440 * 2 ** ((n - 69) / 12)
def add(buf, x, t0, g=1.0):
    i = int(t0 * SR)
    if i < 0: x = x[-i:]; i = 0
    if i >= len(buf) or not len(x): return
    j = min(len(buf), i + len(x)); buf[i:j] += x[:j - i] * g

MOODS = {
    'night':   dict(ch=[[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]], bpm=84, bright=0.6),
    'day':     dict(ch=[[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62]], bpm=96, bright=1.0),
    'tension': dict(ch=[[50, 53, 57], [50, 53, 58], [48, 52, 55], [49, 52, 57]], bpm=100, bright=0.7),
    'tender':  dict(ch=[[53, 57, 60], [48, 52, 55], [50, 53, 57], [46, 50, 53]], bpm=72, bright=0.8),
    # humor/cotidiano: pizzicato + baixo saltitante, staccato, tom maior
    'comedy':  dict(ch=[[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62]], bpm=112, bright=1.0, style='comedy'),
    # mistério/espaço/sumiço: pads longos, notas graves, sino distante, tom menor
    'mystery': dict(ch=[[57, 60, 64], [53, 57, 60], [50, 53, 57], [52, 56, 59]], bpm=70, bright=0.6, style='mystery'),
    # futebol/esporte/torcida: bateria de estádio (surdo + caixa), palmas, metais curtos, ~125 bpm, tom maior
    'sport':   dict(ch=[[60, 64, 67], [65, 69, 72], [67, 71, 74], [60, 64, 67]], bpm=125, bright=1.0, style='sport'),
}
SEGMOOD = {'c0': 'night', 'c1': 'night', 'c2': 'day', 'c3': 'tension', 'i1': 'day', 'c4': 'day', 'c5': 'night', 'i2': 'tension', 'c6': 'tender', 'c7': 'tender', 'c8': 'night'}

def comedy_block(M, dur):
    beat = 60 / M['bpm']; bar = beat * 4
    out = np.zeros(int(SR * (dur + 2))); nb = int(dur / bar) + 1
    def pizz(f, d=0.22, a=0.16):
        y = tt(d); return (np.sin(2 * np.pi * f * y) + 0.45 * np.sin(4 * np.pi * f * y) + 0.2 * np.sin(6 * np.pi * f * y)) * np.exp(-y * 22) * a
    for b in range(nb):
        t0 = b * bar; ch = M['ch'][b % 4]
        # baixo saltitante: raiz / quinta / raiz-oitava / quinta
        for k, n in enumerate([ch[0] - 24, ch[2] - 24, ch[0] - 12, ch[2] - 24]):
            y = tt(0.24); add(out, (np.sin(2 * np.pi * mid(n) * y) + 0.3 * np.sin(4 * np.pi * mid(n) * y)) * np.exp(-y * 9) * 0.32, t0 + k * beat)
        # pizzicato staccato nos contratempos + melodia simples
        mel = [ch[2], ch[1] + 12, ch[2], ch[0] + 12, ch[1], ch[2], ch[1] + 12, ch[2] + 12] if b % 2 == 0 else [ch[0] + 12, ch[2], ch[1], ch[2], ch[0] + 12, ch[1] + 12, ch[2], ch[0]]
        for k, n in enumerate(mel):
            if (b + k) % 5 == 3: continue
            add(out, pizz(mid(n + 12)), t0 + k * beat / 2)
        for k in (1, 3):
            y = tt(0.12); add(out, bp(rng.standard_normal(len(y)), 1500, 6000) * np.exp(-y * 40) * 0.09, t0 + k * beat)  # estalo de palma leve
        for k in range(8):
            add(out, hp(rng.standard_normal(int(SR * 0.03)), 7000) * np.exp(-tt(0.03) * 120) * 0.03, t0 + k * beat / 2 + beat / 4)
        y = tt(0.2); add(out, np.sin(2 * np.pi * (60 + 70 * np.exp(-y * 35)) * y) * np.exp(-y * 16) * 0.22, t0)
    return out[:int(SR * dur)]

def mystery_block(M, dur):
    beat = 60 / M['bpm']; bar = beat * 4
    out = np.zeros(int(SR * (dur + 4))); nb = int(dur / bar) + 1
    for b in range(nb):
        t0 = b * bar; ch = M['ch'][b % 4]; x = tt(bar + 1.2)
        # pad longo com leve vibrato, entrando e saindo devagar
        pad = sum(np.sin(2 * np.pi * mid(n - 12) * x * (1 + 0.002 * np.sin(2 * np.pi * 0.3 * x))) + 0.3 * np.sin(2 * np.pi * mid(n) * 1.004 * x) for n in ch)
        env = np.minimum(1, x / 1.2) * np.minimum(1, (bar + 1.2 - x) / 1.2)
        add(out, lp(pad * env, 1500) * 0.085, t0)
        # nota grave sustentada
        add(out, np.sin(2 * np.pi * mid(ch[0] - 24) * x) * env * 0.26, t0)
        # sino distante (1 por compasso, no tempo 3) + eco
        y = tt(2.4); f = mid(ch[2] + 24)
        bell = (np.sin(2 * np.pi * f * y) + 0.4 * np.sin(2 * np.pi * f * 2.76 * y) + 0.2 * np.sin(2 * np.pi * f * 5.4 * y)) * np.exp(-y * 2.2) * 0.07
        add(out, bell, t0 + 2 * beat); add(out, bell * 0.4, t0 + 2 * beat + 0.42)
        # pulso grave suave
        for k in (0, 2):
            y = tt(0.5); add(out, np.sin(2 * np.pi * (42 + 30 * np.exp(-y * 20)) * y) * np.exp(-y * 7) * 0.16, t0 + k * beat)
        # brilho agudo (estrelas) bem baixo
        for k in range(4):
            y = tt(0.5); f2 = mid(ch[(k + b) % 3] + 36)
            add(out, np.sin(2 * np.pi * f2 * y) * np.exp(-y * 5) * 0.025, t0 + k * beat + beat / 2)
    return out[:int(SR * dur)]

def sport_block(M, dur):
    beat = 60 / M['bpm']; bar = beat * 4
    out = np.zeros(int(SR * (dur + 2))); nb = int(dur / bar) + 1
    for b in range(nb):
        t0 = b * bar; ch = M['ch'][b % 4]
        # surdo (tempos 1 e 3 fortes, 2 e 4 abafados)
        for k in range(4):
            y = tt(0.35); add(out, np.sin(2 * np.pi * (58 + 40 * np.exp(-y * 25)) * y) * np.exp(-y * (8 if k % 2 == 0 else 16)) * (0.34 if k % 2 == 0 else 0.18), t0 + k * beat)
        # caixa/repique em semicolcheias com acento
        for k in range(16):
            if k % 4 == 3 and b % 2: continue
            y = tt(0.06); add(out, bp(rng.standard_normal(len(y)), 1800, 7000) * np.exp(-y * 70) * (0.11 if k % 4 == 2 else 0.045), t0 + k * beat / 4)
        # palmas nos tempos 2 e 4
        for k in (1, 3):
            y = tt(0.12); cl = bp(rng.standard_normal(len(y)), 1000, 4500) * np.exp(-y * 35) * 0.12
            add(out, cl, t0 + k * beat); add(out, cl * 0.6, t0 + k * beat + 0.012)
        # metais curtos (acorde staccato) no 1 e no "e" do 2
        for off in (0, beat * 1.5):
            y = tt(0.22)
            br = sum(np.sign(np.sin(2 * np.pi * mid(n) * y)) * 0.3 + np.sin(2 * np.pi * mid(n) * y) for n in ch)
            add(out, lp(br, 2600) * np.exp(-y * 9) * 0.05, t0 + off)
        # baixo
        y = tt(beat * 2); add(out, np.sin(2 * np.pi * mid(ch[0] - 24) * y) * np.exp(-y * 2.5) * 0.25, t0)
        y = tt(beat * 2); add(out, np.sin(2 * np.pi * mid(ch[2] - 24) * y) * np.exp(-y * 2.5) * 0.22, t0 + 2 * beat)
    return out[:int(SR * dur)]

def music_block(mood, dur):
    M = MOODS[mood]; beat = 60 / M['bpm']; bar = beat * 4
    if M.get('style') == 'comedy': return comedy_block(M, dur)
    if M.get('style') == 'mystery': return mystery_block(M, dur)
    if M.get('style') == 'sport': return sport_block(M, dur)
    out = np.zeros(int(SR * (dur + 2)))
    nb = int(dur / bar) + 1
    for b in range(nb):
        t0 = b * bar; ch = M['ch'][b % 4]; x = tt(bar + 0.3)
        pad = sum(np.sin(2 * np.pi * mid(n - 12) * x) + 0.25 * np.sin(2 * np.pi * mid(n) * 2.003 * x) for n in ch)
        env = np.minimum(1, x / 0.4) * np.minimum(1, (bar + 0.3 - x) / 0.4)
        add(out, lp(pad * env, 2200) * 0.08, t0)
        add(out, np.sin(2 * np.pi * mid(ch[0] - 24) * x) * np.exp(-x * 1.1) * 0.30, t0)
        arp = [ch[0], ch[1], ch[2], ch[1] + 12, ch[2] + 12, ch[1] + 12, ch[2], ch[1]]
        for k, n in enumerate(arp):
            y = tt(0.6); f = mid(n + 12)
            add(out, (np.sin(2 * np.pi * f * y) + 0.3 * np.sin(4 * np.pi * f * y)) * np.exp(-y * 6) * 0.11 * M['bright'], t0 + k * beat / 2)
        for k in (0, 2):
            y = tt(0.25); add(out, np.sin(2 * np.pi * (48 + 80 * np.exp(-y * 30)) * y) * np.exp(-y * 14) * 0.28, t0 + k * beat)
        for k in range(8):
            add(out, hp(rng.standard_normal(int(SR * 0.04)), 6000) * np.exp(-tt(0.04) * 90) * 0.035, t0 + k * beat / 2 + beat / 4)
    return out[:int(SR * dur)]

def sfx_lib():
    L = {}
    x = tt(0.5); L['whoosh'] = bp(rng.standard_normal(len(x)), 300, 2500) * np.sin(np.pi * x / 0.5) ** 2
    x = tt(0.09); L['pop'] = np.sin(2 * np.pi * (300 + 1300 * x / 0.09) * x) * np.sin(np.pi * x / 0.09)
    x = tt(0.7); L['ting'] = (np.sin(2 * np.pi * 1760 * x) + 0.5 * np.sin(2 * np.pi * 2640 * x)) * np.exp(-x * 8)
    x = tt(0.5); L['thud'] = np.sin(2 * np.pi * (55 + 60 * np.exp(-x * 25)) * x) * np.exp(-x * 9) + lp(rng.standard_normal(len(x)), 800) * np.exp(-x * 16) * 0.5
    x = tt(2.5); L['thunder'] = lp(rng.standard_normal(len(x)), 300) * np.exp(-x * 1.4) * (1 + 0.5 * np.sin(2 * np.pi * 7 * x)) + np.sin(2 * np.pi * (40 + 30 * np.exp(-x * 3)) * x) * np.exp(-x * 2)
    x = tt(1.6); L['chime'] = sum(np.sin(2 * np.pi * mid(n) * x) * np.exp(-x * 2.2) for n in (72, 76, 79, 84)) * 0.5
    x = tt(0.45); L['boing'] = np.sin(2 * np.pi * np.cumsum(180 + 220 * np.sin(2 * np.pi * 9 * x) * np.exp(-x * 4)) / SR) * np.exp(-x * 6)
    x = tt(0.35); L['notif'] = np.concatenate([np.sin(2 * np.pi * 988 * tt(0.12)) * np.exp(-tt(0.12) * 20), np.sin(2 * np.pi * 1319 * tt(0.23)) * np.exp(-tt(0.23) * 12)])
    x = tt(0.04); L['click'] = hp(rng.standard_normal(len(x)), 2000) * np.exp(-x * 150)
    L['typing'] = np.zeros(int(SR * 0.9))
    for k in range(9): add(L['typing'], L['click'] * (0.6 + 0.4 * rng.random()), k * 0.09 + rng.random() * 0.03)
    x = tt(0.08); L['tick'] = np.sin(2 * np.pi * 2200 * x) * np.exp(-x * 80)
    x = tt(0.6); L['cash'] = (np.sin(2 * np.pi * 2093 * x) + np.sin(2 * np.pi * 2637 * x)) * np.exp(-x * 7) * 0.5
    x = tt(0.4); L['buzz'] = np.sign(np.sin(2 * np.pi * 110 * x)) * np.minimum(1, (0.4 - x) / 0.05) * 0.5
    x = tt(0.35); L['glitch'] = np.sign(np.sin(2 * np.pi * np.cumsum(400 + 900 * rng.random(len(x))) / SR)) * (np.floor(x * 40) % 2) * 0.35
    x = tt(0.5); L['slam'] = lp(rng.standard_normal(len(x)), 900) * np.exp(-x * 14) + np.sin(2 * np.pi * 70 * x) * np.exp(-x * 10)
    x = tt(0.28); L['cough'] = bp(rng.standard_normal(len(x)), 300, 1800) * (np.exp(-x * 18) + 0.6 * np.exp(-np.maximum(0, x - 0.12) * 22) * (x > 0.12))
    x = tt(1.2); L['riser'] = bp(rng.standard_normal(len(x)), 500, 5000) * (x / 1.2) ** 2 + np.sin(2 * np.pi * np.cumsum(200 + 600 * x / 1.2) / SR) * (x / 1.2) * 0.3
    x = tt(0.5); L['sparkle'] = sum(np.sin(2 * np.pi * f * x) * np.exp(-np.maximum(0, x - d) * 12) * (x > d) for f, d in ((2349, 0), (2794, 0.06), (3136, 0.12))) * 0.5
    x = tt(0.25); L['wrong'] = np.sin(2 * np.pi * 220 * x) * np.sign(np.sin(2 * np.pi * 5 * x + 0.3)) * np.exp(-x * 4) * 0.6
    x = tt(1.8); L['crowd'] = bp(rng.standard_normal(len(x)), 300, 3000) * np.sin(np.pi * x / 1.8) ** 1.5 * (1 + 0.25 * np.sin(2 * np.pi * 3 * x)) * 0.7
    x = tt(2.2); L['cheer'] = (bp(rng.standard_normal(len(x)), 400, 4000) * np.minimum(1, x / 0.15) * np.exp(-x * 1.1) * (1 + 0.3 * np.sin(2 * np.pi * 5 * x))
                               + sum(np.sin(2 * np.pi * np.cumsum(f + 40 * np.sin(2 * np.pi * (3 + i) * x)) / SR) for i, f in enumerate((520, 640, 760))) * np.exp(-x * 1.6) * 0.06)
    return L

def ambience(kind, dur):
    x = tt(dur); n = rng.standard_normal(len(x))
    if kind == 'waves': a = lp(n, 500) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.12 * x) ** 2)
    elif kind == 'rain': a = hp(n, 2500) * 0.6 + lp(n, 400) * 0.4
    elif kind == 'room': a = lp(n, 200) * 0.25
    elif kind == 'street': a = bp(n, 200, 1200) * 0.4
    elif kind == 'stadium': a = bp(n, 250, 2500) * 0.5 * (0.8 + 0.2 * np.sin(2 * np.pi * 0.4 * x))
    else: a = lp(n, 120) * 0.2
    fade = np.minimum(1, np.minimum(x / 0.3, (dur - x) / 0.3))
    return a * fade

def build(proj):
    P = json.load(open(os.path.join(proj, 'plan.json')))
    import longform
    S, _, scenes = longform.build_scenes(proj)
    N = int(P['total'] * SR) + SR
    narr = np.zeros(N); mus = np.zeros(N); sfx = np.zeros(N); amb = np.zeros(N)
    for sg in P['segs']:
        sr, a = wf.read(os.path.join(proj, 'audio', sg['seg'] + '.wav')); a = a.astype(np.float64) / 32768
        add(narr, a, sg['start'])
    # trilha por segmento com crossfade nos cartões
    for k, sg in enumerate(P['segs']):
        st = sg['start'] - (longform.GAP if k else 0); en = sg['start'] + sg['dur'] + (longform.GAP if k + 1 < len(P['segs']) else longform.TAIL)
        blk = music_block(getattr(S, 'MOOD', None) or getattr(S, 'SEGMOOD', {}).get(sg['seg']) or SEGMOOD.get(sg['seg'], 'night'), en - st + 1.5)
        x = np.arange(len(blk)) / SR; fade = np.minimum(1, np.minimum(x / 1.2, (len(blk) / SR - x) / 1.5))
        add(mus, blk * fade, st)
    L = sfx_lib()
    prev = None
    for sc in scenes:
        set_ = sc['spec']['set']
        if prev is not None and (set_ != prev['spec']['set'] or sc['spec']['cam'] != prev['spec']['cam']):
            add(sfx, L['whoosh'], sc['t0'] - 0.25, 0.5)
        for lb in sc['labels']: add(sfx, L['pop'], sc['t0'] + lb['t'], 0.5)
        for (t, a) in sc.get('shake', []): add(sfx, L['thud'], t, 1.0)
        for t in sc.get('flash_abs', []): add(sfx, L['thunder'], t, 1.0)
        dur = sc['t1'] - sc['t0']
        kind = 'rain' if 'rain' in sc['fx'] else ('waves' if set_ in ('beach', 'harbor') else ('street' if set_ == 'street' else ('stadium' if set_ == 'stadium' else ('room' if set_ not in ('space',) else 'space'))))
        add(amb, ambience(kind, dur + 0.3), sc['t0'], 1.0 if kind != 'rain' else 1.6)
        prev = sc
    for sg in P['segs'][1:]:
        add(sfx, L['chime'], sg['start'] - longform.GAP + 0.1, 0.8)
    # efeitos ligados a palavras da fala: SFX = [('palavra' ou 'palavra#n', 'efeito'[, ganho]), ...]
    seen = {}
    for item in getattr(S, 'SFX', []):
        w, ef = item[0], item[1]; g = item[2] if len(item) > 2 else 0.8
        base, n = (w.split('#') + ['1'])[:2]; n = int(n)
        hits = [x[1] for x in P['words'] if longform.norm(x[0]).startswith(longform.norm(base))]
        if len(hits) >= n and ef in L: add(sfx, L[ef], hits[n - 1] - 0.08, g)
        else: print('SFX sem âncora:', w, ef)
    sting = getattr(S, 'STING', None)
    if sting:
        ts = next((w[1] for w in P['words'] if longform.norm(w[0]).startswith(longform.norm(sting))), None)
        if ts is not None:
            i = int((ts - 0.05) * SR); mus[i:] = 0; mus[max(0, i - 600):i] *= np.linspace(1, 0, min(600, i))
            x = tt(1.6); boom = np.sin(2 * np.pi * (38 + 70 * np.exp(-x * 6)) * x) * np.exp(-x * 2.2) + lp(rng.standard_normal(len(x)), 200) * np.exp(-x * 5) * 0.6
            add(sfx, boom, ts - 0.03, 1.2)
            x = tt(P['total'] - ts); dr = (np.sin(2 * np.pi * 55 * x) + 0.5 * np.sin(2 * np.pi * 82.4 * x)) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.25 * x)) * np.minimum(1, x / 1.0)
            add(mus, dr * 0.3, ts + 0.15)
    sfx = sfx + amb * 0.35
    os.makedirs(os.path.join(proj, 'mix'), exist_ok=True)
    # ---- mix (níveis fixos)
    W = int(0.05 * SR); nw = N // W
    def wr(x): return np.sqrt(np.mean(x[:nw * W].reshape(nw, W) ** 2, axis=1) + 1e-12)
    vr = wr(narr); gate = vr > vr.max() * 10 ** (-30 / 20)
    def grms(x, g): return np.sqrt(np.mean(x[:nw * W].reshape(nw, W)[g] ** 2) + 1e-12)
    V = grms(narr, gate)
    mus *= V * 0.5 / grms(mus, gate)
    sr_ = wr(sfx); sg_ = sr_ > sr_.max() * 10 ** (-40 / 20)
    sfx *= min(V * 0.5 / grms(sfx, sg_), 0.7 * np.max(np.abs(narr)) / np.max(np.abs(sfx)))
    db = lambda a, b: 20 * np.log10(a / b)
    print(f'música vs voz: {db(grms(mus, gate), V):+.2f} dB | efeitos vs voz: {db(grms(sfx, sg_), V):+.2f} dB | pico efeitos/voz: {np.max(np.abs(sfx)) / np.max(np.abs(narr)):.2f}')
    mix = narr + mus + sfx
    pre = os.path.join(proj, 'mix', 'pre.wav'); wf.write(pre, SR, mix.astype(np.float32))
    out = subprocess.run(['ffmpeg', '-hide_banner', '-i', pre, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', out)[-1]); g = -14 - I
    print(f'LUFS antes {I:.2f}, ganho {g:+.2f} dB')
    wf.write(os.path.join(proj, 'mix', 'lin.wav'), SR, (mix * 10 ** (g / 20)).astype(np.float32))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(proj, 'mix', 'lin.wav'), '-af', 'alimiter=limit=0.891:level=false:attack=2:release=60', '-t', str(P['total']),
                    '-c:a', 'pcm_s16le', os.path.join(proj, 'mix', 'mix.wav')])

if __name__ == '__main__':
    build(sys.argv[1])
