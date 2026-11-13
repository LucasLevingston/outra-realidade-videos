import sys; sys.path.insert(0, 'REPO/engine/py')
from presets import *
FORMAT = 'short'; GAP = 0; TAIL = 0.6; MOOD = 'day'; STING = None
OVERLAYS = False   # textos ficam na camada HyperFrames
KEYWORDS = ['nanico', 'gui', 'cinquenta', 'centimetro', 'pequeno', 'pilula', 'vermelha', 'gigante', 'baixinho', 'tres', 'dobro', 'seis',
            'campeonatos', 'cesta', 'doze', 'proibiu', 'oito', 'quatro', 'vinte', 'predio', 'terremoto', 'escuro', 'cristo', 'estatua',
            'piramide', 'eiffel', 'cem', 'espaco', 'planeta', 'terra', 'melhor', 'tomaria']
BUBBLES = [('E aí, nanico?', 'TURMA', '#e04848', 'E', 'nanico'),
           ('Eu odeio ser baixinho.', 'GUI', '#3a8dde', 'Eu', 'baixinho'),
           ('Gui, cuidado onde pisa!', 'VIZINHA', '#e86a8a', 'cuidado', 'pisa'),
           ('E você, tomaria a pílula?', 'GUI', '#3a8dde', '>você', 'pílula')]
CARDS = {}
ORDER = ['short']
BULLY = ['p3@-1.7,-1.6:pointL/laugh', 'p5@1.5,-2.2:belly/laugh']
BOARD = {'board': 'MEDIDAS\nGUI: 1,50 m'}
SEG = {'short': [
 # 1 GANCHO
 [('c_board', 'ID', 'push', ['gui@0.2,-0.3:hang/sad^0.6,0'] + BULLY, {'opts': BOARD, 'speaker': 'p3', 'flash': 'nanico', 'lab': [('nanico', 'NANICO?', 'yellow')]})],
 [('c_board', 'ID', 'push', ['gui@0.2,0.2:hang/neutral^0,0'], {'opts': BOARD, 'lab': [('Gui', 'GUI', 'teal', '17 ANOS'), ('cinquenta', '1,50 m', 'yellow')]}),
  ('c_desks', 'ID', 'push', ['gui@-0.2,-2.2:cross/worried'], {'opts': BOARD, 'lab': [('centímetro', '+0 cm', 'red')]})],
 [('c_desks', 'ID', 'orbit', ['gui@-0.2,-2.2:hang/sad', 'p3@k1:pointL/laugh', 'p5@2.6,-0.4:belly/laugh'], {'opts': BOARD, 'speaker': 'p3', 'lab': [('Pequenininho', 'PEQUENININHO!', 'orange'), ('Miniatura', 'MINIATURA!', 'orange')]}),
  ('c_board', 'ID', 'push', ['gui@0.2,0.2:cheek/happy'], {'opts': BOARD, 'lab': [('pequeno', 'MUITO PEQUENO', 'white')]})],
 # 2 ACONTECIMENTOS
 [('b_room', 'I', 'push', ['gui@a:hang/sleepy^0.4,-0.6'], {'fx': ['twinkle'], 'lab': [('noite', 'O SONHO', 'purple')]}),
  ('b_room', 'I', 'drama', ['gui@a:hold/surprise+pill'], {'flash': 'gigante', 'lab': [('pílula', 'PÍLULA VERMELHA', 'red'), ('gigante', 'VIRA GIGANTE', 'yellow')]}),
  ('b_room', 'I', 'push', ['gui@a:hold/sad+pill'], {'speaker': 'gui'})],
 [('c_desks', 'ID', 'drama', ['gui@a:hip/proud*2', 'p3@k1:hang/surprise^0,-1'], {'opts': BOARD, 'shake': 'Três', 'lab': [('Três', '3 m', 'yellow'), ('dobro', 'O DOBRO', 'orange')]}),
  ('c_board', 'ID', 'push', ['p3@1.4,0.4:hang/surprise^-1,-1', 'gui@-0.6,-1.5:cross/proud*1.9'], {'opts': BOARD, 'speaker': 'p3', 'lab': [('nanico', 'NANICO?!', 'red')]})],
 [('f_mid', 'D', 'push', ['gui@p:hold/happy+ball*3.2'], {'lab': [('bola', 'NUNCA JOGOU', 'white'), ('dois', 'DIA 2 · 6 m', 'yellow')]}),
  ('f_mid', 'D', 'orbit', ['gui@p:both_up/proud*3.2', 'p1@d1:hang/surprise^0,-1', 'p4@d3:temple/surprise^0,-1'], {'lab': [('campeonatos', 'CAMPEÃO DE TUDO', 'orange'), ('cesta', 'SÓ LARGAR NA CESTA', 'white')]})],
 [('f_wide', 'D', 'pull', ['gui@p:hang/surprise*14', 'p1@d1:hang/surprise', 'p4@d2:up/worried', 'p2@-6,22:hang/surprise'], {'shake': 'doze', 'lab': [('três', 'DIA 3 · 12 m', 'yellow')]}),
  ('f_wide', 'D', 'push', ['gui@p:hang/sad*14', 'p1@d1:hang/worried', 'p4@d2:cross/angry', 'tecnico@-6,22:pointL/angry'], {'lab': [('proibiu', 'PROIBIDO DE JOGAR', 'red')]})],
 [('st_wide', 'D', 'push', ['gui@24,-8:temple/worried*7'], {'lab': [('oito', 'PESO ×8', 'red'), ('quatro', 'OSSOS ×4', 'blue')]}),
  ('st_wide', 'D', 'panR', ['gui@24,-8:thumb/happy*7'], {'lab': [('fingir', 'FINGE QUE TÁ TUDO BEM', 'yellow')]})],
 [('st_down', 'D', 'push', ['gui@40,0:hang/surprise*16'], {'fx': ['dust'], 'lab': [('quatro', 'DIA 4 · 24 m', 'yellow'), ('prédio', '= PRÉDIO DE 8 ANDARES', 'white')]}),
  ('st_down', 'O', 'drama', ['gui@40,0:temple/worried*16'], {'fx': ['dust'], 'shake': 'terremoto', 'lab': [('terremoto', 'TERREMOTO!', 'red'), ('escuro', 'BAIRRO NO ESCURO', 'purple')]}),
  ('st_stall', 'O', 'push', ['p6@a:up/shout^0,-1'], {'speaker': 'p6', 'fx': ['dark']})],
 [('b_high', 'G', 'push', ['gui@-4,-40:hang/happy*25'], {'lab': [('cinco', 'DIA 5 > CRISTO REDENTOR', 'yellow'), ('seis', 'DIA 6 > ESTÁTUA DA LIBERDADE', 'orange')]}),
  ('b_high', 'G', 'pull', ['gui@-25,-160:both_up/proud*70'], {'shake': 'Eiffel', 'lab': [('sete', 'DIA 7 > PIRÂMIDE', 'yellow'), ('oito', 'DIA 8 > TORRE EIFFEL', 'red')]})],
 [('sp_close', 'X', 'drama', ['gui@0,14:hang/surprise*2.5'], {'fx': ['twinkle'], 'lab': [('dezesseis', 'DIA 16 · ~100 km', 'yellow'), ('espaço', 'CABEÇA NO ESPAÇO', 'white')]}),
  ('sp_earth', 'X', 'push', ['gui@6,16:wave/happy*3'], {'fx': ['twinkle'], 'lab': [('planeta', 'SAIU DO PLANETA', 'purple')]})],
 [('sp_earth', 'X', 'drama', ['gui@-12,-20:both_up/proud*11'], {'fx': ['twinkle'], 'shake': 'Terra', 'flash': 'Terra', 'lab': [('vinte', 'DIA 23', 'yellow'), ('Terra', 'DO TAMANHO DA TERRA', 'orange')]})],
 # 3 PERGUNTA FINAL
 [('c_board', 'ID', 'push', ['gui@0.2,0.5:hold/talk+pill^0,-0.3'], {'opts': BOARD, 'speaker': 'gui', 'lab': [('melhor', 'BAIXINHO ERA MELHOR', 'teal')]})],
]}
