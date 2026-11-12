"""Narração oficial do canal: VoiceStudio / VoxCPM2 (openbmb/VoxCPM2, Apache-2.0), voz criada por descrição + semente fixa.
Roda local, no processador, sem créditos. Mesmos parâmetros do motor VoxCPM2 do VoiceStudio (debpalash/VoiceStudio):
texto no formato '(descrição)texto', cfg 2.0, 10 passos, max_len = 6 × caracteres, torch.manual_seed(SEMENTE) antes de gerar.

uso:
  python3 voz.py setup                         # instala voxcpm, liga swap de 8 GB (o modelo precisa de ~9 GB de memória) e baixa o modelo
  python3 voz.py PROJ seg1 [seg2 ...]          # lê PROJ/script/<seg>.txt (parágrafos viram uma fala só) e grava PROJ/audio/<seg>.wav (48 kHz mono)

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


def gerar(proj, segs):
    import torch, soundfile as sf
    from voxcpm import VoxCPM
    swap(); torch.set_num_threads(os.cpu_count() or 2); dev = device(); print('voz: dispositivo', dev, flush=True)
    m = VoxCPM.from_pretrained('openbmb/VoxCPM2', load_denoiser=False, optimize=False, device=dev)
    os.makedirs(os.path.join(proj, 'audio'), exist_ok=True)
    for seg in segs:
        out = os.path.join(proj, 'audio', seg + '.wav')
        if os.path.exists(out): print('pula', seg); continue
        txt = ' '.join(open(os.path.join(proj, 'script', seg + '.txt')).read().split())
        torch.manual_seed(SEMENTE)
        t0 = time.time()
        w = m.generate(text=f'({DESCRICAO}){txt}', cfg_value=2.0, inference_timesteps=10, max_len=min(4096, max(256, len(txt) * 6)))
        tmp = out + '.48k.wav'; sf.write(tmp, w, 48000)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-ar', '48000', '-ac', '1', out], check=True); os.remove(tmp)
        print(seg, f'{len(w) / 48000:.1f} s de áudio em {time.time() - t0:.0f} s', flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'setup': setup()
    else: gerar(sys.argv[1], sys.argv[2:])
