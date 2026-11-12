# Motor 3D + 2D — Outra Realidade

Estilo do canal: **cenários 3D toon** (three.js, texturas pintadas, contorno de tinta, desfoque de fundo) com **personagens 2D cabeça-de-feijão** (contorno ameixa, membros finos) compostos por cima, câmera 2.5D viva (push, pan, orbit com parallax pela profundidade).
O mesmo motor faz o **Short 9:16** e o **vídeo longo 16:9**.

## Instalação (sessão nova)
```bash
pip install --break-system-packages -q opencv-python-headless faster-whisper   # playwright + chrome já vêm no ambiente
```
three.js r160 já está em `engine/web/three.module.js` (sem rede).

## Projeto
```
PROJ/
  script/<seg>.txt     # roteiro; parágrafos separados por linha em branco (Short: seg = "short", 1 parágrafo por bloco: gancho, fato, reviravolta, pergunta)
  audio/<seg>.wav      # narração ElevenLabs convertida: ffmpeg -i x.mp3 -ar 48000 -ac 1 <seg>.wav
  scenes.py            # plano de cenas (ver modelo em engine/templates/)
```

## Passo a passo
```bash
E=REPO/engine/py
python3 $E/words.py PROJ short            # tempos das palavras (whisper local)
python3 $E/longform.py PROJ plan          # alinha roteiro↔áudio e monta a linha do tempo
python3 $E/longform.py PROJ plates        # renderiza as placas 3D (≈3 s cada, retomável)
python3 $E/longform.py PROJ sheet /tmp/sheet.jpg   # folha de conferência (OLHAR antes do render)
WORKERS=2 python3 $E/longform.py PROJ render       # quadros em blocos de 45 s, retomável (rodar com nohup + acompanhar o log)
python3 $E/longaudio.py PROJ              # trilha + efeitos + mix (música −6 dB da voz, efeitos ≤ −6 dB, −14 LUFS)
python3 $E/longform.py PROJ final OUT.mp4 # Short: CRF 18 · Longo: 2 passes < 95 MB
```
Tempo: Short ≈ 5–8 min no total; longo de 28 min ≈ 1 h de render com 2 processos.

## scenes.py
```python
import sys; sys.path.insert(0, 'REPO/engine/py')
from presets import *          # PRE (câmeras/slots), LT (luzes), MOON, LOW, SNOW, STORM
FORMAT = 'short'               # ou 'long'
GAP = 0; TAIL = 0.6            # Short: sem cartões. Longo: GAP 2.5 / TAIL 5 + CARDS
MOOD = 'night'                 # trilha: night | day | tension | tender
STING = 'Só'                   # 1ª palavra da reviravolta: a trilha para, entra impacto grave
KEYWORDS = ['lua', 'mar']      # palavras da legenda em amarelo (sem acento)
BUBBLES = [('Agora dá pra ir a pé!', 'BETO', '#e04848', 'Agora', 'pé')]  # balão: texto, nome, cor, 1ª e última palavra
CARDS = {}; ORDER = ['short']
SEG = {'short': [   # um item por parágrafo; cada item = lista de planos dividindo o parágrafo
  [('b_sea', 'N', 'push', [], {'opts': MOON, 'lab': [('Santos', 'SANTOS · SP', 'white')]})],
  [('b_dito', 'N', 'orbit', ['dito@d:temple/surprise^0.3,-1', 'beto!@b:point/laugh+lantern'], {'speaker': 'beto', 'shake': 'deitado'})],
]}
```
- **Plano**: `(preset, luz, movimento, personagens, extras)`.
- **Luz**: N noite · D dia · G fim de tarde · W amanhecer · O nublado · S tempestade · I interior noite · ID interior dia · X espaço.
- **Movimentos**: push, pull, panR, panL, tiltU, tiltD, orbit, hold, drama (push + giro), whip.
- **Extras**: `opts` (opções do cenário), `lab` (rótulos: palavra que dispara, texto, cor, subtítulo), `fx` (rain, snow, twinkle, birds, dust, crabs, turtles, dark), `speaker` (boca mexe nas frases com aspas), `shake` (palavra), `flash` (palavra).
- **Personagem**: `nome[!]@slot:braços/rosto^olharX,olharY+extra+extra` (`!` = espelhado; slot do preset ou `"x,z"` em metros).
  - Elenco (`chars.py`): dito, cida, caio, caio20, lia, beto, ze, filho, anchor, astro, prof, menina, locutor, lobo, p1–p6 (figurantes). Novos personagens: acrescentar em `CAST`.
  - Braços: hang, point, pointL, up, both_up, wave, hip, belly, temple, cross, hold, phone, oar, thumb, cheek, reach.
  - Rostos: neutral, happy, talk, surprise, worried, sad, laugh, angry, squint, cold, hot, shout, sleepy, proud.
  - Extras: phone, lantern, mug, tablet, paper, notebook, photo, icecream, sign, sunglasses, sweat, tears, wet, scarf, snowhat, shiver.
- **Cenários** (`web/sets.js`): beach (praia de Santos: orla, prédios, ilha, canoas; opts moon, receded, snow, storm, sun, snowman, canoeTilt), kitchen, lab (observatório), street (opts stall, shop), space (Terra; opts tilt, moon, axisGlow, farMoon, mars, probe), harbor (colônia; opts lowtide, ships, storm), radio, studio, classroom, bedroom. Cenário novo = nova função em `SETS` + presets em `presets.py`.

## Regras do estilo
- Cada frase ilustrada; algo novo a cada plano; nenhum plano parado (todos os movimentos têm deriva).
- Personagens sempre vivos (respiração, piscada, balanço) e com sombra de contato; tingidos pela luz da cena.
- Rótulos em pílula no topo; legenda: Short = karaokê (1 palavra, 45% da altura); longo = frase inteira embaixo.
- Nunca editar a narração; a imagem segue o áudio.
