import sys; sys.path.insert(0, 'REPO/engine/py')
from presets import *
FORMAT = 'short'; GAP = 0; TAIL = 0.6; MOOD = 'sport'; STING = None
OVERLAYS = False   # textos ficam na camada HyperFrames
KEYWORDS = ['brasil', 'todas', 'copas', 'vinte', 'duas', 'estrelas', 'nenhuma', 'final', 'caio', 'gol', 'titulo', 'rotina',
            'manga', 'novecentos', 'vigesima', 'terceira', 'bandeira', 'feriado', 'mes', 'regra', 'direto', 'taca', 'casa', 'comemorar']
BUBBLES = [('E você, ainda ia comemorar?', 'CAIO', '#3a8dde', '>você', '>comemorar')]
SFX = [('Copas', 'cheer'), ('estrelas', 'sparkle'), ('gol', 'crowd'), ('rotina', 'wrong'), ('novecentos', 'cash'), ('vigésima', 'ting'),
       ('bandeira', 'boing'), ('feriado', 'tick'), ('jornal', 'notif'), ('taça', 'thud')]
CARDS = {}
ORDER = ['short']
BRA = {'crowd': ['#ffd23f', '#2f9e4a', '#ffffff', '#3a8dde', '#ffd23f', '#2f9e4a']}
CAM = {'stall': [2.6, -7.4], 'stallText': 'CAMISA NOVA\nR$ 900', 'shop': 'ESPORTES', 'shopX': 3}
PAD = {'shop': 'PADARIA DO ZÉ', 'shopX': 3}
SEG = {'short': [
 # 1 GANCHO
 [('f_mid', 'N', 'push', ['caio20@p:both_up/surprise^-0.3,-0.5'], {'opts': BRA, 'flash': 'todas', 'lab': [('todas', 'TODAS AS COPAS?', 'yellow')]}),
  ('lk_wide', 'ID', 'drama', ['craque@a:temple/worried^0,-0.5'], {'at': 'Cara', 'opts': {'banner': '22 ESTRELAS'}, 'lab': [('vinte', '22 ★', 'yellow'), ('nenhuma', 'SEM ESPAÇO', 'red')]})],
 # 2 ACONTECIMENTOS
 [('lr_wide', 'I', 'push', ['caio20@-0.2,-2.0:hang/neutral^0.6,0', 'cida@-1.2,-2.1:hang/sleepy', 'dito!@0.8,-1.9:cross/neutral'], {'opts': {'screen': 'FINAL 2026', 'prog': 0.95}, 'lab': [('final', 'FINAL 2026', 'white'), ('Caio', 'CAIO', 'blue', 'TORCEDOR')]}),
  ('lr_sofa', 'I', 'orbit', ['caio20@v:cross/sleepy^0.6,0', 'cida@k:hang/sleepy'], {'at': 'quando', 'lab': [('gol', 'GOL DO TÍTULO', 'green'), ('rotina', 'ZZZ… ROTINA', 'orange')]})],
 [('st_stall', 'D', 'push', ['caio20@a:hold/happy^1,0+paper'], {'opts': CAM, 'lab': [('manga', 'MANGA SÓ DE ESTRELAS', 'yellow'), ('novecentos', 'R$ 900', 'red')]}),
  ('st_stall', 'D', 'drama', ['caio20@a:thumb/proud^0,0+paper'], {'at': 'só', 'opts': CAM, 'lab': [('vigésima', '23ª ★', 'yellow')]})],
 [('st_wide', 'D', 'panR', ['ze@5.9,0.4:hip/neutral', 'p1!@8.1,0.0:hang/sleepy', 'p3@10.3,-0.4:phone/neutral+phone'], {'opts': PAD, 'lab': [('bandeira', 'SEM BANDEIRA', 'white')]}),
  ('st_down', 'D', 'push', [], {'at': 'feriado', 'opts': PAD, 'lab': [('mês', 'FERIADO: 30 DIAS', 'orange'), ('ano', 'TODO ANO', 'white')]})],
 [('s_wide', 'ID', 'push', ['anchor@0.0,-1.7:point/talk'], {'opts': {'screen': 'NOVA REGRA:\nBRASIL DIRETO\nNA FINAL'}, 'lab': [('regra', 'NOVA REGRA', 'red')]}),
  ('f_wide', 'N', 'drama', ['craque@p:both_up/laugh'], {'at': 'agora', 'opts': BRA, 'shake': 'taça', 'lab': [('direto', 'DIRETO NA FINAL', 'yellow'), ('taça', 'TAÇA JÁ EM CASA', 'green')]})],
 # 3 PERGUNTA FINAL (volta ao plano do gancho = loop)
 [('f_mid', 'N', 'push', ['caio20@p:point/talk^0,0'], {'opts': BRA, 'speaker': 'caio20'})],
]}
