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
RITMO = float(os.environ.get('VOZ_RITMO', '1.15'))  # atempo com tom preservado: os trechos curtos saem lentos (~2,3 palavras/s); 1,15 leva a ~2,6


def frases(texto):
    """Lista de (trecho, pausa_depois). Parágrafos separados por linha em branco."""
    import re
    paras = [' '.join(p.split()) for p in texto.split('\n\n') if p.strip()]
    out = []
    for pi, p in enumerate(paras):
        sents = [x for x in re.split(r'(?<=[.!?…])\s+', p) if x.strip()]
        trechos, buf = [], []
        for x in sents:
            if buf and len(' '.join(buf + [x]).split()) > MAX_PALAVRAS:
                trechos.append(' '.join(buf)); buf = []
            buf.append(x)
        if buf: trechos.append(' '.join(buf))
        for ti, t in enumerate(trechos):
            ultimo = ti == len(trechos) - 1
            pausa = (PAUSA_PARAGRAFO if pi < len(paras) - 1 else 0.0) if ultimo else PAUSA_TRECHO
            out.append((t, pausa))
    return out


def aparar(w, sr=48000, lim=0.012):
    import numpy as np
    a = np.abs(w); idx = np.where(a > lim)[0]
    if not len(idx): return w
    i0 = max(0, idx[0] - int(0.03 * sr)); i1 = min(len(w), idx[-1] + int(0.12 * sr))
    return w[i0:i1]


def gerar(proj, segs):
    import torch, soundfile as sf, numpy as np
    from voxcpm import VoxCPM
    swap(); torch.set_num_threads(os.cpu_count() or 2); dev = device(); print('voz: dispositivo', dev, flush=True)
    m = VoxCPM.from_pretrained('openbmb/VoxCPM2', load_denoiser=False, optimize=False, device=dev)
    os.makedirs(os.path.join(proj, 'audio'), exist_ok=True)
    for seg in segs:
        out = os.path.join(proj, 'audio', seg + '.wav')
        if os.path.exists(out): print('pula', seg); continue
        t0 = time.time(); partes = []
        lista = frases(open(os.path.join(proj, 'script', seg + '.txt')).read())
        for k, (txt, pausa) in enumerate(lista):
            torch.manual_seed(SEMENTE)
            fala = txt.replace('"', '').replace('“', '').replace('”', '')
            w = m.generate(text=f'({DESCRICAO}){fala}', cfg_value=2.0, inference_timesteps=10, max_len=min(4096, max(256, len(txt) * 6)))
            w = aparar(np.asarray(w, dtype=np.float32))
            partes += [w, np.zeros(int(pausa * 48000), np.float32)]
            print(f'  frase {k + 1}/{len(lista)}: {len(w) / 48000:.1f} s  {txt[:60]}', flush=True)
        w = np.concatenate(partes)
        tmp = out + '.48k.wav'; sf.write(tmp, w, 48000)
        af = ['-af', f'atempo={RITMO}'] if abs(RITMO - 1) > 0.001 else []
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp] + af + ['-ar', '48000', '-ac', '1', out], check=True); os.remove(tmp)
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out], capture_output=True, text=True).stdout)
        npal = sum(len(t.split()) for t, _ in lista)
        print(seg, f'{dur:.1f} s de áudio ({npal / dur:.2f} palavras/s) em {time.time() - t0:.0f} s', flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'setup': setup()
    else: gerar(sys.argv[1], sys.argv[2:])
