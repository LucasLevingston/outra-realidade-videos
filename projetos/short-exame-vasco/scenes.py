import sys; sys.path.insert(0, 'REPO/engine/py')
from presets import *
FORMAT = 'short'; GAP = 0; TAIL = 0.6; MOOD = 'day'; STING = 'Tudo'
OVERLAYS = False
KEYWORDS = ['prostata', 'cinco', 'nunca', 'torcida', 'vasco', 'vascao', 'silencio', 'tambor', 'baixinho', 'trena', 'dedo', 'centimetro',
            'maos', 'lobo', 'mau', 'comer', 'aberto', 'confuso', 'intencoes', 'usou', 'vazio', 'dez', 'segundos', 'novembro', 'azul', 'tres', 'dias', 'comentarios']
BUBBLES = [('Vai pra cima, Vascão!', 'TORCIDA', '#1d1d22', 'gritando', 'Vascão'),
           ('Nossa, que mãos grandes você tem!', 'SEU DITO', '#2f9e95', 'Nossa', 'tem'),
           ('Pode entrar, tá aberto!', 'SEU DITO', '#2f9e95', 'Pode', 'aberto'),
           ('Conhece alguém que faria isso? 👇', 'SEU DITO', '#2f9e95', 'Conhece', 'comentários')]
CARDS = {}
ORDER = ['short']
FANS = ['v1@t1:up/laugh+vflag', 'v2@t2:hold/laugh+vdrum+sticks', 'v3@t3:both_up/happy']
SHOUT = ['v1@t1:up/shout+vflag', 'v2@t2:hold/shout+vdrum+sticks', 'v3@t3:both_up/shout']
QUIET = ['v1@t1:up/worried+vflag', 'v2@t2:hold/squint+vdrum+sticks', 'v3@t3:cheek/worried']
PARTY = {'shop': 'FESTA DA TORCIDA · NOVEMBRO AZUL', 'shopX': 16, 'carX': -40}
SEG = {'short': [
 # 1 GANCHO
 [('cl_wide', 'ID', 'push', ['dito@a:temple/worried^1,0', 'medico@d:cross/neutral^-1,0'], {'flash': 'próstata', 'lab': [('próstata', 'EXAME DE PRÓSTATA', 'blue'), ('cinco', '5 COISAS PRA NUNCA FAZER', 'yellow')]})],
 # 2 ACONTECIMENTO (a lista)
 [('cl_wide', 'ID', 'push', ['dito@a:hang/surprise', 'medico@d:cross/surprise^-1,0'] + FANS, {'flash': 'Vasco', 'lab': [('Primeiro', '1 · A TORCIDA', 'yellow')]}),
  ('cl_fans', 'ID', 'orbit', SHOUT, {'speaker': 'v1', 'shake': 'Vascão', 'lab': [('centenas', 'CENTENAS DE TORCEDORES', 'white')]})],
 [('cl_doc', 'ID', 'push', ['medico@d:pointL/angry^-1,0', 'dito@a:hang/worried'], {'lab': [('silêncio', 'SILÊNCIO!', 'red')]}),
  ('cl_fans', 'ID', 'push', QUIET, {'lab': [('baixinho', 'TAMBOR NO MODO SILENCIOSO', 'white')]})],
 [('cl_doc', 'ID', 'push', ['dito@a:hold/happy+tape', 'medico@d:up/surprise^-1,0'], {'lab': [('Segundo', '2 · A TRENA', 'yellow'), ('dedo', 'MEDINDO O DEDO', 'white')]}),
  ('cl_fans', 'ID', 'drama', SHOUT, {'shake': 'alto', 'lab': [('centímetro', '+1 cm', 'orange')]})],
 [('cl_maca', 'ID', 'push', ['dito@a:cheek/surprise', 'medico@d:both_up/neutral^-1,0'], {'speaker': 'dito', 'lab': [('Terceiro', '3 · A FRASE', 'yellow')]}),
  ('cl_doc', 'ID', 'orbit', ['lobomed@d:both_up/laugh', 'dito@a:hang/surprise'], {'flash': 'lobo', 'lab': [('lobo', 'LOBO MAU?', 'red')]}),
  ('cl_doc', 'ID', 'push', ['medico@d:cross/squint^-1,0', 'dito@a:hang/worried+sweat'], {'lab': [('comer', 'NÃO VAI TE COMER', 'white')]})],
 [('cl_maca', 'ID', 'push', ['dito@m:thumb/happy', 'medico@d:hold/neutral+tablet'], {'speaker': 'dito', 'lab': [('Quarto', '4 · A POSIÇÃO', 'yellow')]}),
  ('cl_doc', 'ID', 'drama', ['medico@d:temple/worried^-1,0', 'dito@a:thumb/happy'], {'lab': [('confuso', 'MÉDICO CONFUSO', 'orange')]})],
 [('cl_maca', 'ID', 'push', ['dito@a:cheek/worried', 'medico@d:hold/surprise+tablet'], {'lab': [('Quinto', '5 · A PERGUNTA', 'yellow')]}),
  ('cl_wide', 'ID', 'orbit', ['dito@a:hang/sad+tears', 'medico@d:pointL/talk^-1,0'], {'lab': [('usou', 'ELA TAMBÉM TE USOU', 'red')]}),
  ('cl_doc', 'ID', 'push', ['medico@d:point/talk^-1,0', 'dito@a:hold/sad+tears'], {'lab': [('vazio', 'ELE EXPLICA O VAZIO', 'blue')]})],
 # 3 REVIRAVOLTA
 [('cl_wide', 'ID', 'drama', ['dito@a:hang/surprise', 'medico@d:thumb/happy^-1,0'], {'shake': 'Tudo', 'lab': [('segundos', 'SÓ 10 SEGUNDOS', 'red')]}),
  ('cl_maca', 'ID', 'push', ['dito@a:point/happy^-1,-1'], {'flash': 'Azul', 'lab': [('Azul', 'NOVEMBRO AZUL', 'blue', 'TODO NOVEMBRO')]})],
 [('cl_door', 'ID', 'push', ['dito@c:up/proud+vflag', 'v1@a:both_up/laugh', 'v3@b:up/happy'], {'opts': {'door': 'SAÍDA'}, 'lab': [('dez', 'EXAME: 10 s', 'white')]}),
  ('st_wide', 'G', 'panR', ['v1@9.84,-3.53:both_up/laugh', 'p1@10.66,-3.14:wave/happy', 'v2@10.61,-2.24:hold/laugh+vdrum+sticks', 'v4@11.39,-0.96:both_up/happy', 'p3@12.2,-0.57:up/laugh', 'v3@12.16,0.33:both_up/shout', 'dito@10.91,-1.55:up/proud+vflag'], {'opts': PARTY, 'shake': 'três', 'lab': [('três', 'FESTA: 3 DIAS', 'orange')]})],
 # 4 FINAL COM PERGUNTA
 [('cl_wide', 'ID', 'push', ['dito@a:point/talk', 'medico@d:thumb/happy^-1,0'] + FANS, {'speaker': 'dito'})],
]}
