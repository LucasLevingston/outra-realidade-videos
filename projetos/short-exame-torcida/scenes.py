import sys; sys.path.insert(0, 'REPO/engine/py')
from presets import *
FORMAT = 'short'; GAP = 0; TAIL = 0.6; MOOD = 'day'; STING = 'Só'
OVERLAYS = False
KEYWORDS = ['torcida', 'prostata', 'dito', 'bandeira', 'tambor', 'regra', 'novembro', 'fila', 'quarteirao', 'coro', 'silencio', 'quinze', 'vermelho', 'proximo', 'campo', 'chefe', 'torcer']
BUBBLES = [('Uh, é exame!', 'TORCIDA', '#3a8dde', 'Uh', 'exame'),
           ('E você, levava quem pra torcer?', 'SEU DITO', '#2f9e95', 'você', 'torcer')]
CARDS = {}
ORDER = ['short']
FANS = ['beto@t1:both_up/laugh', 'ze@t2:hold/laugh+drum+sticks', 'caio20@t3:wave/happy']
QUEUE = {'shop': 'POSTO DE SAÚDE · NOVEMBRO AZUL', 'shopX': 20, 'carX': -40}
SEG = {'short': [
 # 1 GANCHO
 [('cl_wide', 'ID', 'push', ['dito@a:up/proud+flag', 'lia@d:cross/surprise^-1,0'] + FANS, {'flash': 'torcida', 'lab': [('torcida', 'TORCIDA ORGANIZADA?', 'yellow')]}),
  ('cl_fans', 'ID', 'orbit', ['beto@t1:both_up/shout', 'ze@t2:hold/laugh+drum+sticks', 'caio20@t3:up/happy+flag'], {'lab': [('bandeira', 'BANDEIRA + TAMBOR', 'white', '3 AMIGOS')]})],
 # 2 ACONTECIMENTO
 [('cl_door', 'ID', 'push', ['lia@b:point/talk^1,0', 'dito@a:up/happy+flag'], {'opts': {'door': 'CONSULTÓRIO'}, 'lab': [('regra', 'REGRA DE NOVEMBRO', 'blue', 'EXAME = TORCIDA')]}),
  ('st_wide', 'D', 'panR', ['p1@15.0,-7.0:hang/neutral', 'p3@16.4,-7.0:wave/happy', 'p5@17.8,-7.0:hang/talk', 'p2@19.2,-7.0:hip/neutral', 'p4@20.6,-7.0:phone/neutral+phone', 'p6@22.0,-7.0:hang/happy', 'dito@23.4,-7.0:up/proud+flag'], {'opts': QUEUE, 'lab': [('Segunda', 'SEG · 08:00', 'white'), ('quarteirão', 'FILA NO QUARTEIRÃO', 'orange')]})],
 # 3 REVIRAVOLTA (escalada)
 [('cl_fans', 'ID', 'orbit', ['beto@t1:both_up/shout', 'ze@t2:hold/shout+drum+sticks', 'caio20@t3:wave/laugh'], {'lab': [('coro', 'CORO NO CONSULTÓRIO', 'yellow')]}),
  ('cl_wide', 'ID', 'push', ['lia@d:point/angry', 'dito@a:temple/worried'] + ['beto@t1:both_up/shout', 'ze@t2:hold/shout+drum+sticks', 'caio20@t3:up/laugh'], {'speaker': 'beto', 'shake': 'exame'}),
  ('cl_maca', 'ID', 'push', ['dito@a:cheek/hot+sweat', 'lia@d:hold/neutral+tablet'], {'lab': [('quinze', '15 ANOS FUGINDO', 'red'), ('vermelho', 'VERMELHO TOMATE', 'red')]})],
 # 3 REVIRAVOLTA (virada)
 [('cl_doc', 'ID', 'drama', ['lia@d:pointL/talk^-1,0', 'dito@a:hang/surprise'], {'shake': 'Só', 'lab': [('próximo', 'QUEM É O PRÓXIMO?', 'red')]}),
  ('cl_fans', 'ID', 'push', ['beto@t1:hang/worried+sweat', 'ze@t2:hold/worried+drum', 'caio20@t3:cheek/worried'], {'flash': 'campo', 'lab': [('campo', 'A TORCIDA ENTROU EM CAMPO', 'yellow'), ('chefe', 'SEU DITO', 'teal', 'CHEFE DA TORCIDA')]})],
 # 4 FINAL COM PERGUNTA
 [('cl_wide', 'ID', 'push', ['dito@a:point/talk', 'lia@d:thumb/happy'] + FANS, {'speaker': 'dito'})],
]}
