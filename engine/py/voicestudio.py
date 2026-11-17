"""Narração do canal com o VoiceStudio (motor OmniVoice, k2-fsa/OmniVoice) clonando a voz fixa "Lucas" (engine/vozes/lucas.wav, CC BY 4.0, iluucasz).
Roda local, sem créditos. Na nuvem (CPU) leva ~13 min por ~50 s de áudio.

uso:
  python3 voicestudio.py setup                 # instala torch + OmniVoice (sem as dependências opcionais que não instalam no Python 3.13)
  python3 voicestudio.py PROJ seg1 [seg2 ...]   # lê PROJ/script/<seg>.txt, grava PROJ/audio/<seg>.wav (48 kHz mono) e imprime duração e palavras/s
"""
import sys, os, re, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, '..', 'vozes', 'lucas.wav')
REF_TXT = open(os.path.join(HERE, '..', 'vozes', 'lucas.txt')).read().strip()
SRC = os.path.expanduser('~/.cache/voicestudio-src')
PARAMS = ['--num_step', '32', '--guidance_scale', '2.0', '--speed', '1.0']   # fixo: não mudar (2,6 palavras/s medido em 16/11/2026)

def setup():
    pip = [sys.executable, '-m', 'pip', 'install', '--break-system-packages', '-q']
    subprocess.run(pip + ['torch', 'torchaudio'], check=True)
    subprocess.run(pip + ['transformers>=5.10.0', 'accelerate', 'pydub', 'audioop-lts', 'soundfile', 'numpy', 'huggingface_hub>=1.7', 'hf-xet', 'num2words'], check=True)
    if not os.path.exists(SRC):
        subprocess.run(['git', 'clone', '-q', '--depth', '1', 'https://github.com/debpalash/VoiceStudio.git', SRC], check=True)
    subprocess.run(pip + ['--no-deps', SRC], check=True)
    subprocess.run([sys.executable, '-c', 'from omnivoice.models.omnivoice import OmniVoice; print("voicestudio: pronto")'], check=True)

def clean(txt):
    paras = [p.strip() for p in txt.split('\n\n') if p.strip()]
    t = ' '.join(paras).replace('\n', ' ')
    t = re.sub(r'\{[^}]*\}', '', t).replace('"', '').replace('“', '').replace('”', '')
    return re.sub(r'\s+', ' ', t).strip()

def gen(proj, seg):
    txt = clean(open(os.path.join(proj, 'script', seg + '.txt')).read())
    os.makedirs(os.path.join(proj, 'audio'), exist_ok=True)
    raw = os.path.join(proj, 'audio', seg + '_raw.wav'); out = os.path.join(proj, 'audio', seg + '.wav')
    t0 = time.time()
    subprocess.run(['omnivoice-infer', '--model', 'k2-fsa/OmniVoice', '--text', txt, '--language', 'pt', '--ref_audio', os.path.abspath(REF),
                    '--ref_text', REF_TXT, '--device', os.environ.get('VOZ_DEVICE', 'cpu'), '--output', raw] + PARAMS, check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-ar', '48000', '-ac', '1', '-c:a', 'pcm_s16le', out], check=True); os.remove(raw)
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out], capture_output=True, text=True).stdout)
    n = len(txt.split())
    print(f'{seg}: {d:.1f}s, {n} palavras, {n / d:.2f} palavras/s, gerado em {(time.time() - t0) / 60:.1f} min -> {out}', flush=True)

if __name__ == '__main__':
    if sys.argv[1] == 'setup': setup()
    else:
        for s in sys.argv[2:]: gen(sys.argv[1], s)
