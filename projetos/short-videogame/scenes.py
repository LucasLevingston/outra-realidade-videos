import sys; sys.path.insert(0, 'REPO/engine/py')
from presets import *
FORMAT = 'short'; GAP = 0; TAIL = 0.6; MOOD = 'tension'; STING = None
OVERLAYS = False   # textos ficam na camada HyperFrames
PILL_TOP = 360     # contador ocupa o canto superior direito
KEYWORDS = ['videogame', 'unico', 'humano', 'segunda', 'sete', 'caio', 'vida', 'cem', 'mesma', 'frase', 'igualzinho',
            'padaria', 'dez', 'moedas', 'lixeira', 'moeda', 'mil', 'terceiro', 'viaduto', 'novinho', 'checkpoint',
            'setimo', 'missao', 'ceu', 'chefao', 'chefe', 'trinta', 'metros', 'jogo']
BUBBLES = [('Bom dia, aventureiro!', 'MORADOR', '#3a8dde', 'Bom', 'aventureiro'),
           ('E aí, você saía do jogo ou ficava?', 'CAIO', '#e04848', '>aí', '>ficava')]
CARDS = {}
ORDER = ['short']
NPC = ['p1@8.3,-1.5:hang/neutral^-1,0', 'p2@11.4,1.7:hang/neutral^-1,0', 'p3@12.3,-2.6:hang/neutral^-1,0', 'p5@14.3,-1.2:hang/neutral^-1,0']
SEG = {'short': [
 # 1 GANCHO
 [('b_room', 'I', 'drama', ['caio20@a:temple/surprise^0.3,-0.4'], {'flash': 'videogame', 'lab': [('videogame', 'DENTRO DO GAME?', 'yellow')]}),
  ('st_wide', 'D', 'push', NPC + ['caio20@5.1,2.9:hang/worried^1,0'], {'at': 'fosse', 'lab': [('único', 'ÚNICO HUMANO', 'orange')]})],
 # 2 ACONTECIMENTOS
 [('b_room', 'ID', 'push', ['caio20@a:hang/sleepy^0.3,-0.4'], {'lab': [('sete', 'SEG · 07:00', 'white'), ('Caio', 'CAIO', 'teal', '26 ANOS')]}),
  ('b_room', 'ID', 'drama', ['caio20@a:both_up/surprise^0,-1'], {'at': 'barra', 'shake': 'flutuando', 'lab': [('barra', 'BARRA DE VIDA', 'green')]})],
 [('st_wide', 'D', 'push', ['p1@8.3,-1.5:wave/happy^-1,0', 'p2@11.4,1.7:wave/happy^-1,0', 'p3@12.3,-2.6:wave/happy^-1,0', 'caio20@5.1,2.9:hang/surprise^1,0'], {'speaker': 'p1', 'lab': [('mesma', 'A MESMA FRASE', 'orange')]}),
  ('st_stall', 'D', 'orbit', ['caio20@a:temple/worried^1,0', 'p4!@b:wave/happy^-1,0'], {'at': 'Toda', 'lab': [('Toda', 'TODA VEZ!', 'red')]})],
 [('st_stall', 'D', 'push', ['caio20@a:point/happy^1,0', 'p6!@b:hold/happy^-1,0'], {'lab': [('padaria', 'PADARIA', 'white'), ('dez', 'PÃO = 10 MOEDAS', 'yellow')]}),
  ('st_wide', 'D', 'orbit', ['caio20@7,2.6:both_up/laugh'], {'at': 'chutar', 'shake': 'lixeira', 'lab': [('lixeira', '+1 MOEDA', 'yellow')]})],
 [('tw_up', 'D', 'tiltD', [], {'shake': 'viaduto', 'lab': [('terceiro', 'DIA 3', 'yellow')]}),
  ('lr_door', 'ID', 'push', ['caio20@h:hip/proud^-1,0'], {'at': 'acorda', 'flash': 'acorda', 'lab': [('checkpoint', 'CHECKPOINT', 'green')]})],
 [('st_wide', 'S', 'pull', ['caio20@5.1,2.9:hang/worried^1,-1'], {'fx': ['rain'], 'lab': [('sétimo', 'DIA 7', 'yellow'), ('Derrotar', 'MISSÃO: DERROTAR O CHEFÃO', 'orange')]}),
  ('st_wide', 'S', 'drama', ['tecnico@24,-8.6:cross/angry^-1,0*12', 'caio20@5.1,2.9:temple/surprise^1,-1'], {'at': 'chefe', 'fx': ['rain'], 'shake': 'trinta', 'flash': 'trinta', 'lab': [('trinta', '30 m', 'red')]})],
 # 3 PERGUNTA FINAL (volta ao quarto do gancho = loop)
 [('b_room', 'I', 'push', ['caio20@a:point/talk^0,0'], {'speaker': 'caio20'})],
]}

HF = [
 dict(kind='counter', at='Cem', until='sai', label='VIDA', value='100%'),
 dict(kind='counter', at='mil', until='terceiro', label='MOEDAS', value='1.000'),
 dict(kind='stamp', at='chefe', until='>altura', text='CHEFÃO FINAL'),
]
