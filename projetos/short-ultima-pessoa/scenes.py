import sys; sys.path.insert(0, 'REPO/engine/py')
from presets import *
FORMAT = 'short'; GAP = 0; TAIL = 0.6; MOOD = 'day'; STING = 'Só'
KEYWORDS = ['ultima', 'terra', 'despertador', 'unico', 'barulho', 'vazia', 'bilhoes', 'sumiram', 'padaria', 'quentinho', 'sorvete', 'ninguem', 'presidente', 'brasil', 'contra', 'radio', 'astronauta', 'espacial', 'primeiro']
BUBBLES = [('Tem alguém aí embaixo?', 'ASTRONAUTA', '#7b5aa6', 'Tem', 'embaixo'), ('E você, o que ia fazer primeiro?', 'CAIO', '#3a8dde', '>você', 'primeiro')]
CARDS = {}
ORDER = ['short']
STALL = {'stall': [2.6, -7.4], 'stallText': 'PÃO\nQUENTINHO', 'shop': 'PADARIA', 'shopX': 3}
SEG = {'short': [
 [('b_room', 'W', 'push', ['caio20@a:temple/sleepy^0.4,-0.6'], {'lab': [('última', 'ÚLTIMA PESSOA DA TERRA', 'yellow')]}),
  ('st_down', 'W', 'pull', [], {'fx': ['dust'], 'lab': [('único', 'NENHUM BARULHO', 'white')]})],
 [('st_wide', 'D', 'push', ['caio20@5,2.5:hang/surprise^0.6,0'], {'lab': [('Seis', '06:15', 'white'), ('Caio', 'CAIO', 'teal', 'SÃO PAULO')]}),
  ('st_wide', 'D', 'panR', [], {'shake': 'sumiram', 'lab': [('bilhões', '8 BILHÕES SUMIRAM', 'red')]}),
  ('st_stall', 'D', 'push', ['caio20@a:hang/happy^0.5,0'], {'opts': STALL, 'lab': [('quentinho', 'AINDA QUENTE', 'orange')]})],
 [('st_stall', 'D', 'orbit', ['caio20@a:point/laugh+icecream'], {'opts': STALL, 'lab': [('primeiro', 'DIA 1', 'white'), ('Sorvete', 'CAFÉ DA MANHÃ', 'orange')]}),
  ('s_wide', 'ID', 'push', ['caio20@0,-0.2:point/talk'], {'speaker': 'caio20x', 'opts': {'screen': 'JORNAL\nDO CAIO'}, 'lab': [('ninguém', 'AUDIÊNCIA: 0', 'red'), ('presidente', 'PRESIDENTE DO BRASIL', 'yellow'), ('contra', 'VOTOS CONTRA: 0', 'teal')]}),
  ('r_desk', 'N', 'drama', ['caio20@0,0.4:hang/surprise^0.5,0'], {'shake': 'chiou', 'lab': [('terceira', 'NOITE 3', 'purple')]}),
  ('sp_close', 'X', 'push', ['astro@-0.8,26.5:wave/happy'], {'opts': {'probe': [3, 10, 15]}, 'fx': ['twinkle'], 'lab': [('estação', 'ESTAÇÃO ESPACIAL', 'white', 'A 400 KM')]}),
  ('sp_close', 'X', 'drama', ['astro@-0.8,26.5:both_up/proud'], {'opts': {'probe': [3, 10, 15]}, 'fx': ['twinkle'], 'lab': [('presidente', 'PRESIDENTE DA TERRA', 'yellow')]})],
 [('b_room', 'W', 'push', ['caio20@a:point/talk'], {'speaker': 'caio20'})],
]}
