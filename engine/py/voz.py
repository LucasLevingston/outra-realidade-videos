"""Narração oficial do canal: VoiceStudio / VoxCPM2 (openbmb/VoxCPM2, Apache-2.0). UMA voz só, sempre a mesma.

uso:
  python3 voz.py setup                 # instala voxcpm + faster-whisper, liga swap de 8 GB e baixa o modelo
  python3 voz.py referencia            # (só se engine/vozes/narrador.wav não existir) cria a referência do narrador
  python3 voz.py PROJ seg1 [seg2 ...]  # lê PROJ/script/<seg>.txt -> PROJ/audio/<seg>.wav (48 kHz mono)

Como fica fluido, com uma voz só e sem cortes:
- VOZ ÚNICA: todo o texto (inclusive as falas `{personagem} "..."`) é lido pelo narrador. A marcação {nome} só serve
  para o motor saber quem mexe a boca; aqui ela é ignorada. Nunca existe outra voz.
- TIMBRE TRAVADO: todo trecho clona a mesma referência fixa (engine/vozes/narrador.wav, ~12 s, criada uma vez por
  descrição + semente 1011105763) em modo continuação (prompt_wav + prompt_text) + reference_wav.
- TEXTO LIMPO: reticências viram vírgula (o modelo lia "..." como "ponto"), aspas e símbolos saem.
- TRECHOS MAIORES: até MAX_PALAVRAS (22) palavras, sempre cortados em fim de frase -> menos emendas, entonação contínua.
- SEM CORTES: max_len folgado; o recorte do silêncio é relativo ao pico (-42 dB) com folga de 90 ms antes e 200 ms depois
  e fade curto, então o começo e o fim das palavras nunca são comidos.
- CHECAGEM POR TRECHO: cada trecho é transcrito (whisper local). Se faltar/sobrar palavra (erro > 20 %), se o idioma
  não sair português ou se a duração for absurda, gera de novo (até 4 tentativas) e fica com a melhor.
- VOLUME IGUAL: cada trecho é nivelado no mesmo RMS antes de juntar, para não parecer que a voz mudou.
Retomável: um segmento cujo .wav já existe é pulado.
"""
import sys, os, re, time, subprocess, unicodedata

SEMENTE = 1011105763
DESCRICAO = ("Jovem brasileiro de uns 25 anos, voz masculina agradável e leve, fala espontânea e descontraída, "
             "contando uma história surpreendente para um amigo, curioso e animado de forma natural, "
             "português do Brasil com sotaque paulistano suave e natural, dicção clara, nada de locutor")
VOZES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'vozes')
REF_WAV = os.path.join(VOZES_DIR, 'narrador.wav')
REF_TXT = os.path.join(VOZES_DIR, 'narrador.txt')
REF_TEXTO = ("Cara, deixa eu te contar uma coisa que aconteceu essa semana. Você não vai acreditar, sério. "
             "Eu tava voltando pra casa, tipo umas nove da noite, e aí do nada a rua inteira apagou. "
             "E sabe o que é mais estranho? Ninguém parecia ligar.")
SWAP = os.path.expanduser('~/swapfile')
SR = 48000

MAX_PALAVRAS = int(os.environ.get('VOZ_MAX_PALAVRAS', '22'))
PAUSA_TRECHO = 0.30      # s entre trechos do mesmo parágrafo
PAUSA_PARAGRAFO = 0.55   # s entre parágrafos (troca de ideia/bloco)
RITMO = float(os.environ.get('VOZ_RITMO', '0.90'))  # atempo com tom preservado: o clone sai a ~3,3 palavras/s; 0,90 + respiros leva a ~2,8
RESPIRO = 0.30           # s mínimos de silêncio entre frases dentro do mesmo trecho
TENTATIVAS = 4
ERRO_MAX = 0.12          # erro de palavras aceito por trecho (20 palavras: até 2; menos de 9: nenhuma)
ALVO_RMS = 0.075         # nível de cada trecho antes de juntar


# ---------------------------------------------------------------- ambiente
def setup():
    for pkg in ('voxcpm>=2.0.3', 'faster-whisper', 'num2words'):
        r = subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', pkg])
        if r.returncode: subprocess.run([sys.executable, '-m', 'pip', 'install', '--break-system-packages', '-q', pkg], check=True)
    swap()
    from huggingface_hub import snapshot_download
    snapshot_download('openbmb/VoxCPM2')
    print('voz: pronto')


def device():
    import torch
    if os.environ.get('VOZ_DEVICE'): return os.environ['VOZ_DEVICE']
    if torch.cuda.is_available(): return 'cuda'
    if getattr(torch.backends, 'mps', None) and torch.backends.mps.is_available(): return 'mps'
    return 'cpu'


def swap():
    """Só no Linux com pouca memória (< 12 GB): liga um swap de 8 GB. Em outro sistema, ou sem permissão, não faz nada."""
    try:
        if not sys.platform.startswith('linux'): return
        mem = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / 1e9
        if mem >= 12: return
        on = subprocess.run(['swapon', '--show'], capture_output=True, text=True).stdout
    except Exception:
        return
    if SWAP in on or len(on.strip().splitlines()) > 1: return
    try:
        free = __import__('shutil').disk_usage(os.path.dirname(SWAP)).free / 1e9
        if not os.path.exists(SWAP) and free < 20:
            print('swap não ligado: pouco disco livre', round(free, 1), 'GB'); return
        if not os.path.exists(SWAP):
            subprocess.run(['fallocate', '-l', '8G', SWAP], check=True); os.chmod(SWAP, 0o600)
            subprocess.run(['mkswap', SWAP], check=True, capture_output=True)
        subprocess.run(['swapon', SWAP], check=True)
    except Exception as e:
        print('swap não ligado:', e)


def modelo():
    import torch
    from voxcpm import VoxCPM
    swap(); torch.set_num_threads(os.cpu_count() or 2); dev = device(); print('voz: dispositivo', dev, flush=True)
    return VoxCPM.from_pretrained('openbmb/VoxCPM2', load_denoiser=False, optimize=False, device=dev)


_W = None
def ouvido():
    global _W
    if _W is None:
        from faster_whisper import WhisperModel
        _W = WhisperModel('small', device='cpu', compute_type='int8')
    return _W


# ---------------------------------------------------------------- texto
def limpar(t):
    """Texto que vai pro modelo: sem marcação de personagem, sem aspas, reticências -> vírgula."""
    t = re.sub(r'\{\w+\}\s*', '', t)
    t = re.sub(r'["“”«»]', '', t)
    t = t.replace('…', '...')
    t = re.sub(r'\s*\.\.\.+\s*(?=[a-záéíóúâêôãõç])', ', ', t)   # "fechou... e só" -> "fechou, e só"
    t = re.sub(r'\.\.\.+', '.', t)                              # "a Rosinha..." no fim -> ponto
    t = re.sub(r'[*_#\[\]()<>]', '', t)
    return ' '.join(t.split())


def frases(texto):
    """[(trecho, pausa_depois)]. Parágrafos separados por linha em branco; tudo na voz do narrador."""
    paras = [limpar(p) for p in texto.split('\n\n') if p.strip()]
    paras = [p for p in paras if p]
    out = []
    for pi, p in enumerate(paras):
        sents = [x for x in re.split(r'(?<=[.!?])\s+', p) if x.strip()]
        trechos, buf = [], []
        for x in sents:
            if buf and len(' '.join(buf + [x]).split()) > MAX_PALAVRAS:
                trechos.append(' '.join(buf)); buf = []
            buf.append(x)
        if buf: trechos.append(' '.join(buf))
        for ti, t in enumerate(trechos):
            ultimo = ti == len(trechos) - 1
            out.append((t, (PAUSA_PARAGRAFO if pi < len(paras) - 1 else 0.0) if ultimo else PAUSA_TRECHO))
    return out


def _norm(t):
    from num2words import num2words
    t = re.sub(r'\d+', lambda m: ' ' + num2words(int(m.group()), lang='pt_BR') + ' ', t.lower())
    t = unicodedata.normalize('NFKD', t)
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return re.sub(r'[^a-z ]', ' ', t).split()


def erro(ref, hip):
    """Erro de palavras (WER) entre o texto e o que o whisper ouviu."""
    r, h = _norm(ref), _norm(hip)
    if not r: return 0.0
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            cur = min(d[j] + 1, d[j - 1] + 1, prev + (r[i - 1] != h[j - 1]))
            prev, d[j] = d[j], cur
    return d[len(h)] / len(r)


def escutar(w, palavras=False):
    """(texto ouvido, prob. de ser português[, [(palavra, início, fim)]]) do áudio 48 kHz."""
    import numpy as np
    from scipy.signal import resample_poly
    a = resample_poly(w, 1, 3).astype(np.float32)
    segs, info = ouvido().transcribe(a, beam_size=5, condition_on_previous_text=False, word_timestamps=palavras)
    segs = list(segs); pt = info.language_probability if info.language == 'pt' else 0.0
    txt = ' '.join(s.text.strip() for s in segs)
    if not palavras: return txt, pt
    return txt, pt, [(x.word, x.start, x.end) for s in segs for x in (s.words or [])]


def sobras(w, txt, ws):
    """Corta som a mais antes da 1ª palavra ou depois da última (ex.: "É, e se…" quando o texto é "E se…")."""
    r = _norm(txt)
    h = [(_norm(p) or [''])[0] for p, _, _ in ws]
    if len(r) < 2 or len(h) < 2: return w
    i0 = next((j for j in range(min(3, len(h) - 1)) if h[j] == r[0] and h[j + 1] == r[1]), 0)
    i1 = next((j for j in range(len(h) - 1, max(len(h) - 4, 0), -1) if h[j] == r[-1] and h[j - 1] == r[-2]), len(h) - 1)
    a = int(max(0, ws[i0][1] - 0.06) * SR) if i0 > 0 else 0
    b = int(min(len(w) / SR, ws[i1][2] + 0.20) * SR) if i1 < len(h) - 1 else len(w)
    if a or b < len(w):
        print(f'    cortado som a mais: {" ".join(p for p, _, _ in ws[:i0])} | {" ".join(p for p, _, _ in ws[i1 + 1:])}', flush=True)
        w = aparar(w[a:b])
    return w


# ---------------------------------------------------------------- áudio
def aparar(w, sr=SR):
    """Tira só o silêncio das pontas, relativo ao pico (-42 dB), com folga larga pra não comer consoante nem final."""
    import numpy as np
    if not len(w): return w
    f = int(0.01 * sr); n = len(w) // f
    if n < 3: return w
    rms = np.sqrt(np.mean(w[:n * f].reshape(n, f) ** 2, axis=1) + 1e-12)
    on = np.where(rms > rms.max() * 10 ** (-42 / 20))[0]
    if not len(on): return w
    i0 = max(0, on[0] * f - int(0.09 * sr)); i1 = min(len(w), (on[-1] + 1) * f + int(0.20 * sr))
    w = w[i0:i1].copy()
    fi, fo = int(0.006 * sr), int(0.03 * sr)
    w[:fi] *= np.linspace(0, 1, fi); w[-fo:] *= np.linspace(1, 0, fo)
    return w


def respirar(w, n):
    """Garante um respiro de RESPIRO s nas n pausas mais longas dentro do trecho (os fins de frase), sem tocar na fala."""
    import numpy as np
    if n <= 0: return w
    f = int(0.01 * SR); k = len(w) // f
    rms = np.sqrt(np.mean(w[:k * f].reshape(k, f) ** 2, axis=1) + 1e-12)
    mudo = rms < rms.max() * 10 ** (-35 / 20)
    runs, i = [], 0
    while i < k:
        if mudo[i]:
            j = i
            while j < k and mudo[j]: j += 1
            if i > 0 and j < k and j - i >= 5: runs.append((j - i, i, j))
            i = j
        else: i += 1
    alvo = sorted(sorted(runs, reverse=True)[:n], key=lambda r: r[1])
    out, pos = [], 0
    for ln, i, j in alvo:
        falta = int(RESPIRO * SR) - ln * f
        meio = (i + j) // 2 * f
        out.append(w[pos:meio])
        if falta > 0: out.append(np.zeros(falta, np.float32))
        pos = meio
    out.append(w[pos:])
    return np.concatenate(out)


def nivelar(w):
    import numpy as np
    f = int(0.02 * SR); n = len(w) // f
    if n < 2: return w
    rms = np.sqrt(np.mean(w[:n * f].reshape(n, f) ** 2, axis=1))
    fala = rms[rms > rms.max() * 0.1]
    g = ALVO_RMS / (np.sqrt(np.mean(fala ** 2)) + 1e-9)
    return np.clip(w * g, -0.98, 0.98)


def referencia(m=None):
    """Cria UMA vez a referência do narrador. Se já existe, nunca refaz (é o que trava a voz do canal)."""
    import torch, soundfile as sf, numpy as np
    if os.path.exists(REF_WAV): return m
    m = m or modelo(); os.makedirs(VOZES_DIR, exist_ok=True)
    melhor = None
    for k in range(TENTATIVAS):
        torch.manual_seed(SEMENTE + k)
        w = aparar(np.asarray(m.generate(text=f'({DESCRICAO}){REF_TEXTO}', cfg_value=2.0, inference_timesteps=10,
                                          max_len=2048), dtype=np.float32))
        ouv, pt = escutar(w); e = erro(REF_TEXTO, ouv)
        print(f'referência {k}: erro {e:.2f}  pt {pt:.2f}  {len(w) / SR:.1f} s', flush=True)
        if melhor is None or (e, -pt) < (melhor[0], -melhor[1]): melhor = (e, pt, w)
        if e <= 0.05 and pt > 0.95: break
    sf.write(REF_WAV, nivelar(melhor[2]), SR); open(REF_TXT, 'w').write(REF_TEXTO)
    print('referência do narrador criada', flush=True)
    return m


def falar(m, txt, i):
    """Gera um trecho clonando a referência; confere com o whisper e regera se sair errado."""
    import torch, numpy as np
    reft = open(REF_TXT).read().strip()
    npal = len(txt.split()); melhor = None
    for k in range(TENTATIVAS):
        torch.manual_seed(SEMENTE + 1000 * k + i)
        w = m.generate(text=txt, prompt_wav_path=REF_WAV, prompt_text=reft, reference_wav_path=REF_WAV,
                       cfg_value=2.0, inference_timesteps=10, max_len=min(4096, max(400, len(txt) * 10)))
        w = aparar(np.asarray(w, dtype=np.float32))
        ouv, pt, ws = escutar(w, True)
        w = sobras(w, txt, ws)
        ouv, pt = escutar(w); e = erro(txt, ouv); dur = len(w) / SR
        fora = not (npal / 4.4 <= dur <= npal / 1.5 + 0.8)
        ruim = e * npal > int(ERRO_MAX * npal) or pt < 0.6 or fora   # trecho curto: nenhuma palavra pode faltar
        nota = e + (0 if pt >= 0.6 else 1) + (0.5 if fora else 0)
        if melhor is None or nota < melhor[0]: melhor = (nota, w, e, ouv)
        if not ruim: break
        print(f'    regerando (erro {e:.2f}, pt {pt:.2f}, {dur:.1f} s): ouviu "{ouv[:70]}"', flush=True)
    return melhor


def gerar(proj, segs):
    import soundfile as sf, numpy as np
    m = referencia(); m = m or modelo()
    os.makedirs(os.path.join(proj, 'audio'), exist_ok=True)
    for seg in segs:
        out = os.path.join(proj, 'audio', seg + '.wav')
        if os.path.exists(out): print('pula', seg); continue
        t0 = time.time(); partes = []; avisos = []
        lista = frases(open(os.path.join(proj, 'script', seg + '.txt')).read())
        for k, (txt, pausa) in enumerate(lista):
            _, w, e, ouv = falar(m, txt, k)
            if e * len(txt.split()) > int(ERRO_MAX * len(txt.split())): avisos.append(f'trecho {k + 1}: "{txt}" -> ouviu "{ouv}"')
            w = respirar(w, len(re.findall(r'[.!?](?=\s)', txt)))
            partes += [nivelar(w), np.zeros(int(pausa * SR), np.float32)]
            print(f'  trecho {k + 1}/{len(lista)}: {len(w) / SR:.1f} s  erro {e:.2f}  {txt[:60]}', flush=True)
        w = np.concatenate(partes)
        tmp = out + '.tmp.wav'; sf.write(tmp, w, SR)
        af = ['-af', f'atempo={RITMO}'] if abs(RITMO - 1) > 0.001 else []
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp] + af + ['-ar', str(SR), '-ac', '1', out], check=True); os.remove(tmp)
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out],
                                   capture_output=True, text=True).stdout)
        npal = sum(len(t.split()) for t, _ in lista)
        print(seg, f'{dur:.1f} s de áudio ({npal / dur:.2f} palavras/s) em {time.time() - t0:.0f} s', flush=True)
        for a in avisos: print('  ATENÇÃO, conferir:', a, flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'setup': setup()
    elif sys.argv[1] in ('referencia', 'vozes'): referencia()
    else: gerar(sys.argv[1], sys.argv[2:])
