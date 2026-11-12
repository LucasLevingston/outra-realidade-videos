"""Tempos de cada palavra da narração (faster-whisper local, sem créditos do ElevenLabs).
uso: python3 words.py PROJ_DIR seg1 seg2 ...   (lê PROJ/audio/<seg>.wav, grava PROJ/audio/words.json)"""
import sys, os, json, subprocess
import numpy as np, scipy.io.wavfile as wf
from faster_whisper import WhisperModel
proj, segs = sys.argv[1], sys.argv[2:]
m = WhisperModel('small', device='cpu', compute_type='int8')
out = {}
for f in segs:
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(proj, 'audio', f + '.wav'), '-ar', '16000', '-ac', '1', '/tmp/_w16.wav'])
    sr, a = wf.read('/tmp/_w16.wav'); a = a.astype(np.float32) / 32768
    segs_, _ = m.transcribe(a, language='pt', word_timestamps=True)
    out[f] = [[w.word.strip(), round(float(w.start), 3), round(float(w.end), 3)] for s in segs_ for w in s.words]
    json.dump(out, open(os.path.join(proj, 'audio', 'words.json'), 'w'), ensure_ascii=False); print(f, len(out[f]), flush=True)
