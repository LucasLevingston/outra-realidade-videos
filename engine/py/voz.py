"""Narração oficial do canal: VoiceStudio / VoxCPM2 (openbmb/VoxCPM2, Apache-2.0), voz criada por descrição + semente fixa.
Roda local, no processador, sem créditos. Mesmos parâmetros do motor VoxCPM2 do VoiceStudio (debpalash/VoiceStudio):
texto no formato '(descrição)texto', cfg 2.0, 10 passos, max_len = 6 × caracteres, torch.manual_seed(SEMENTE) antes de gerar.

uso:
  python3 voz.py setup                         # instala voxcpm, liga swap de 8 GB (o modelo precisa de ~9 GB de memória) e baixa o modelo
  python3 voz.py PROJ seg1 [seg2 ...]          # lê PROJ/script/<seg>.txt, gera por trechos (parágrafo, até 14 palavras) e junta com pausas de respiração -> PROJ/audio/<seg>.wav (48 kHz mono)

Usa a placa de vídeo quando houver (CUDA ou Apple MPS). Na nuvem (2 CPUs, sem placa): ~6,5 s de processamento por segundo de áudio (Short de 30 s ≈ 3–4 min).
Retomável: um segmento cujo .wav já existe é pulado.
"""
import sys, os, time, subprocess

SEMENTE = 1011105763
DESCRICAO = ("Jovem brasileiro de uns 25 anos, voz masculina agradável e leve, fala espontânea e descontraída, "
             "contando uma história surpreendente para um amigo, curioso e animado de forma natural, "
             "sotaque brasileiro de São Paulo, nada de locutor")
SWAP = os.path.expanduser('~/swapfile')

# Vozes fixas do canal. Cada voz tem UMA referência gravada em engine/vozes/<voz>.wav (+ .txt), criada uma única vez
# por descrição + semente (`voz.py vozes`). Todos os trechos de todos os vídeos clonam essa referência
# (reference_wav + prompt_wav), então o timbre não muda de um trecho pro outro. Nunca regerar uma referência já existente.
VOZES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'vozes')
REF_TEXTO = 'Cara, deixa eu te contar uma coisa que aconteceu essa semana. Você não vai acreditar, sério.'
VOZES = {
    'narrador': (DESCRICAO, SEMENTE),
    'homem':    ('Homem brasileiro de uns 30 anos, voz masculina mais grave e calma, fala do dia a dia, sotaque do Rio de Janeiro, nada de locutor', 2024110301),
    'mulher':   ('Mulher brasileira de uns 30 anos, voz feminina clara e firme, fala natural e um pouco irônica, sotaque de São Paulo, nada de locutora', 2024110302),
    'mulher2':  ('Mulher brasileira de uns 28 anos, voz feminina doce e aguda, fala rápida e preocupada, sotaque nordestino leve, nada de locutora', 2024110303),
    'senhora':  ('Senhora brasileira de uns 60 anos, voz feminina calorosa e animada, fala de avó, sotaque do interior de Minas, nada de locutora', 2024110304),
    'idoso':    ('Senhor brasileiro de uns 65 anos, voz masculina rouca e tranquila, fala de avô, sotaque caipira leve, nada de locutor', 2024110305),
    'crianca':  ('Menino brasileiro de uns 10 anos, voz infantil animada e curiosa, fala natural de criança', 2024110306),
}
# personagem do elenco (chars.py) -> voz. Personagem sem entrada usa 'homem' ou 'mulher'.
ELENCO = {'voce': 'homem', 'rafa': 'homem', 'beto': 'homem', 'ze': 'idoso', 'dito': 'idoso', 'caio': 'crianca', 'gui': 'crianca', 'filho': 'crianca',
          'bia': 'mulher', 'lia': 'mulher', 'prof': 'mulher', 'lu': 'mulher2', 'menina': 'crianca', 'cida': 'senhora', 'p6': 'mulher2'}


def voz_de(nome):
    nome = (nome or 'narrador').lower()
    return nome if nome in VOZES else ELENCO.get(nome, 'homem')


def referencias(m=None):
    """Cria (uma vez) a referência de cada voz em engine/vozes/. As existentes nunca são refeitas."""
    import torch, soundfile as sf, numpy as np
    os.makedirs(VOZES_DIR, exist_ok=True)
    for v, (desc, seed) in VOZES.items():
        wav = os.path.join(VOZES_DIR, v + '.wav')
        if os.path.exists(wav): continue
        if m is None: m = modelo()
        torch.manual_seed(seed)
        w = m.generate(text=f'({desc}){REF_TEXTO}', cfg_value=2.0, inference_timesteps=10, max_len=1024)
        sf.write(wav, aparar(np.asarray(w, dtype=np.float32)), 48000); open(os.path.join(VOZES_DIR, v + '.txt'), 'w').write(REF_TEXTO)
        print('voz de referência criada:', v, flush=True)
    return m


def modelo():
    import torch
    from voxcpm import VoxCPM
    swap(); torch.set_num_threads(os.cpu_count() or 2); dev = device(); print('voz: dispositivo', dev, flush=True)
    return VoxCPM.from_pretrained('openbmb/VoxCPM2', load_denoiser=False, optimize=False, device=dev)


def setup():
    r = subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'voxcpm>=2.0.3'])
    if r.returncode: subprocess.run([sys.executable, '-m', 'pip', 'install', '--break-system-packages', '-q', 'voxcpm>=2.0.3'], check=True)
    swap()
    from huggingface_hub import snapshot_download
    snapshot_download('openbmb/VoxCPM2')
    print('voz: pronto')


def device():
    import torch
    if os.environ.get('VOZ_DEVICE'): return os.environ['VOZ_DEVICE']  # ex.: VOZ_DEVICE=cpu
    if torch.cuda.is_available(): return 'cuda'
    if getattr(torch.backends, 'mps', None) and torch.backends.mps.is_available(): return 'mps'
    return 'cpu'


def swap():
    """Só no Linux da nuvem com pouca memória (< 12 GB): liga um swap de 8 GB. Em outro sistema, ou sem permissão, não faz nada."""
    try:
        if not sys.platform.startswith('linux'): return
        mem = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / 1e9
        if mem >= 12: return
        on = subprocess.run(['swapon', '--show'], capture_output=True, text=True).stdout
    except Exception:
        return
    if SWAP in on or len(on.strip().splitlines()) > 1: return  # já existe swap ligado
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


# Cadência humana: o roteiro NÃO é gerado de uma vez (sai corrido, sem respiro e "robotizado") nem frase a frase
# isolada (sai lento e arrastado, ~2,5 palavras/s). Cada parágrafo vira trechos de até ~MAX_PALAVRAS palavras
# (cortados em fim de frase), gerados com a mesma semente e unidos com pausas de respiração.
MAX_PALAVRAS = 14        # tamanho máximo de um trecho gerado de uma vez
PAUSA_TRECHO = 0.34      # s entre trechos do mesmo parágrafo
PAUSA_PARAGRAFO = 0.62   # s entre parágrafos (troca de ideia/bloco)
RITMO = float(os.environ.get('VOZ_RITMO', '0.95'))  # atempo com tom preservado: clonando a referência os trechos saem a ~2,9 palavras/s; 0,95 leva a ~2,7


def falas(p):
    """Divide um parágrafo em [(voz, texto)]: `{bia} "fala"` vai pra voz da Bia; o resto é do narrador."""
    import re
    out = []; pos = 0
    for mt in re.finditer(r'\{(\w+)\}\s*["“]([^"”]+)["”]', p):
        if p[pos:mt.start()].strip(): out.append(('narrador', p[pos:mt.start()].strip()))
        out.append((voz_de(mt.group(1)), mt.group(2).strip())); pos = mt.end()
    if p[pos:].strip(): out.append(('narrador', p[pos:].strip()))
    return out


def frases(texto):
    """Lista de (voz, trecho, pausa_depois). Parágrafos separados por linha em branco; falas marcadas com {personagem}."""
    import re
    paras = [' '.join(p.split()) for p in texto.split('\n\n') if p.strip()]
    out = []
    for pi, p in enumerate(paras):
      blocos = falas(p)
      for bi, (voz, bt) in enumerate(blocos):
        sents = [x for x in re.split(r'(?<=[.!?…])\s+', bt) if x.strip()]
        trechos, buf = [], []
        for x in sents:
            if buf and len(' '.join(buf + [x]).split()) > MAX_PALAVRAS:
                trechos.append(' '.join(buf)); buf = []
            buf.append(x)
        if buf: trechos.append(' '.join(buf))
        for ti, t in enumerate(trechos):
            ultimo = ti == len(trechos) - 1 and bi == len(blocos) - 1
            pausa = (PAUSA_PARAGRAFO if pi < len(paras) - 1 else 0.0) if ultimo else PAUSA_TRECHO
            out.append((voz, t, pausa))
    return out


def aparar(w, sr=48000, lim=0.012):
    import numpy as np
    a = np.abs(w); idx = np.where(a > lim)[0]
    if not len(idx): return w
    i0 = max(0, idx[0] - int(0.03 * sr)); i1 = min(len(w), idx[-1] + int(0.12 * sr))
    return w[i0:i1]


def gerar(proj, segs):
    import torch, soundfile as sf, numpy as np
    m = referencias()
    m = m or modelo()
    os.makedirs(os.path.join(proj, 'audio'), exist_ok=True)
    for seg in segs:
        out = os.path.join(proj, 'audio', seg + '.wav')
        if os.path.exists(out): print('pula', seg); continue
        t0 = time.time(); partes = []
        lista = frases(open(os.path.join(proj, 'script', seg + '.txt')).read())
        for k, (voz, txt, pausa) in enumerate(lista):
            torch.manual_seed(VOZES[voz][1])
            ref = os.path.join(VOZES_DIR, voz + '.wav'); reft = open(os.path.join(VOZES_DIR, voz + '.txt')).read().strip()
            fala = txt.replace('"', '').replace('“', '').replace('”', '')
            # clona a referência fixa da voz (timbre idêntico em todos os trechos e vídeos)
            w = m.generate(text=fala, reference_wav_path=ref, prompt_wav_path=ref, prompt_text=reft,
                           cfg_value=2.0, inference_timesteps=10, max_len=min(4096, max(256, len(txt) * 6)))
            w = aparar(np.asarray(w, dtype=np.float32))
            partes += [w, np.zeros(int(pausa * 48000), np.float32)]
            print(f'  frase {k + 1}/{len(lista)} [{voz}]: {len(w) / 48000:.1f} s  {txt[:60]}', flush=True)
        w = np.concatenate(partes)
        tmp = out + '.48k.wav'; sf.write(tmp, w, 48000)
        af = ['-af', f'atempo={RITMO}'] if abs(RITMO - 1) > 0.001 else []
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp] + af + ['-ar', '48000', '-ac', '1', out], check=True); os.remove(tmp)
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out], capture_output=True, text=True).stdout)
        npal = sum(len(t.split()) for _, t, _ in lista)
        print(seg, f'{dur:.1f} s de áudio ({npal / dur:.2f} palavras/s) em {time.time() - t0:.0f} s', flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'setup': setup()
    elif sys.argv[1] == 'vozes': referencias()
    else: gerar(sys.argv[1], sys.argv[2:])
