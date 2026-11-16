import sys; sys.path.insert(0, 'REPO/engine/py')
from presets import *
FORMAT = 'short'; GAP = 0; TAIL = 0.6; MOOD = 'mystery'; STING = None
OVERLAYS = False   # textos ficam na camada HyperFrames
KEYWORDS = ['sol', 'apagasse', 'santos', 'tres', 'escura', 'meia', 'noite', 'milho', 'lanterna', 'eclipse', 'dez', 'graus',
            'negativos', 'frio', 'boneco', 'neve', 'lenha', 'fila', 'quarteirao', 'telescopio', 'nenhum', 'gelo', 'cinquenta', 'aguentar']
BUBBLES = [('E você, ia aguentar o frio?', 'SEU DITO', '#2f9e95', '>você', '>frio')]
SFX = [('lanterna', 'click'), ('eclipse', 'ting'), ('neve', 'sparkle'), ('lenha', 'cash'), ('telescópio', 'click'), ('nenhum', 'wrong'), ('gelo', 'thud')]
CARDS = {}
ORDER = ['short']
SN = {'snow': True, 'snowman': [40, 40]}
SNB = {'snow': True, 'snowman': [2.8, -8]}
SEG = {'short': [
 # 1 GANCHO
 [('b_sea', 'N', 'push', ['dito@s1:temple/surprise^-0.5,-1'], {'flash': 'apagasse', 'lab': [('Sol', 'SEM SOL?', 'yellow')]}),
  ('b_dito', 'N', 'drama', ['dito@d:temple/surprise^0.3,-1', 'p2!@e:up/worried^0,-1'], {'at': 'Em', 'lab': [('três', '15:00', 'white'), ('escura', 'NOITE FECHADA', 'orange')]})],
 # 2 ACONTECIMENTOS
 [('st_stall', 'N', 'push', ['dito@a:hold/happy^1,0'], {'opts': {'stall': [2, -8], 'stallText': 'MILHO\nR$ 8'}, 'lab': [('primeiro', 'DIA 1', 'white'), ('Dito', 'SEU DITO', 'teal', 'VENDE MILHO')]}),
  ('b_orla', 'N', 'orbit', ['p1@m:up/happy+phone', 'p3!@m2:up/laugh+phone', 'p4@k:phone/surprise+phone', 'p5!@k2:up/happy+phone'], {'at': 'pessoal', 'fx': ['twinkle'], 'lab': [('eclipse', 'ECLIPSE?', 'orange')]})],
 [('b_dito', 'N', 'push', ['dito@d:cross/cold^0,-0.3+scarf+shiver'], {'opts': SN, 'fx': ['snow'], 'lab': [('terceiro', 'DIA 3', 'white'), ('negativos', '−10 °C', 'blue')]}),
  ('b_low', 'N', 'orbit', ['p1@d:both_up/laugh+scarf', 'p6!@b:point/happy+snowhat'], {'at': 'boneco', 'opts': SNB, 'fx': ['snow'], 'lab': [('boneco', 'BONECO DE NEVE', 'teal')]})],
 [('st_stall', 'N', 'pull', ['dito@a:thumb/proud^1,0+scarf+snowhat'], {'opts': {'snow': True, 'stall': [2, -8], 'stallText': 'LENHA\nR$ 50'}, 'fx': ['snow'], 'lab': [('semana', 'SEMANA 1', 'white'), ('lenha', 'LENHA', 'orange')]}),
  ('st_wide', 'N', 'push', ['p1@5.9,0.4:cross/cold+scarf+shiver', 'p2!@8.1,0.0:hang/cold+snowhat', 'p3@10.3,-0.4:cross/cold+scarf', 'p4!@12.5,-0.8:hang/cold+shiver', 'p5@14.8,-1.2:cross/sad+scarf'], {'at': 'fila', 'opts': {'snow': True, 'carX': 60}, 'fx': ['snow'], 'lab': [('quarteirão', 'FILA GIGANTE', 'yellow')]})],
 [('l_scope', 'N', 'push', ['lia@a:temple/worried^-1,-0.5'], {'opts': {'screen': 'SOL: ---', 'screen2': 'SINAL: 0'}, 'lab': [('trinta', 'DIA 30', 'white'), ('nenhum', 'SOL NÃO ENCONTRADO', 'red')]}),
  ('sp_close', 'XD', 'drama', [], {'at': 'Terra', 'opts': {'frozen': True}, 'shake': 'gelo', 'lab': [('cinquenta', '−50 °C', 'blue')]})],
 # 3 PERGUNTA FINAL (volta ao plano do gancho = loop)
 [('b_dito', 'N', 'push', ['dito@d:point/talk^0,0+scarf+snowhat+shiver'], {'opts': SN, 'fx': ['snow'], 'speaker': 'dito'})],
]}
