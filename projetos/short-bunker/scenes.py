import sys; sys.path.insert(0, 'REPO/engine/py')
from presets import *
FORMAT = 'short'; GAP = 0; TAIL = 0.6; MOOD = 'tension'; STING = None
OVERLAYS = False   # textos ficam na camada HyperFrames
PILL_TOP = 360     # contador ocupa o canto superior direito
KEYWORDS = ['bunker', 'cem', 'porta', 'fechou', 'quatrocentas', 'latas', 'feijao', 'radio', 'bicicleta', 'luz',
            'internet', 'manual', 'onze', 'cor', 'nome', 'rosinha', 'pedalar', 'duas', 'horas', 'dobro', 'tamanho',
            'uma', 'so', 'noite', 'inteira', 'aguentava']
BUBBLES = [('E você, aguentava os cem dias?', 'BETO', '#e04848', '>você', '>dias')]
CARDS = {}
ORDER = ['short']
D1 = {'day': 1, 'cans': 'full'}
SEG = {'short': [
 # 1 GANCHO
 [('bk_wide', 'I', 'push', ['beto@b:temple/worried^-1,-0.2'], {'opts': dict(D1, hatch='open'), 'flash': 'bunker', 'lab': [('bunker', '100 DIAS NUM BUNKER?', 'yellow')]}),
  ('bk_door', 'I', 'drama', ['beto@a:hang/surprise^-1,-0.2'], {'at': 'porta', 'opts': D1, 'shake': 'fechou', 'lab': [('abre', 'ABRE NO DIA 100', 'orange')]})],
 # 2 ACONTECIMENTOS
 [('bk_cal', 'I', 'push', [], {'opts': D1, 'lab': [('um', 'DIA 1', 'white')]}),
  ('bk_shelf', 'I', 'pull', ['beto@a:point/happy^1,0'], {'at': 'Beto', 'opts': D1, 'lab': [('Beto', 'BETO', 'teal', '32 ANOS'), ('quatrocentas', '400 LATAS', 'yellow')]}),
  ('bk_bike', 'I', 'orbit', ['beto@a:thumb/proud^1,0'], {'at': 'bicicleta', 'opts': D1, 'lab': [('luz', 'GERA LUZ', 'green')]})],
 [('bk_wide', 'I', 'push', ['beto@a:hold/sad^0,0+paper'], {'opts': {'day': 10, 'cans': 'full'}, 'lab': [('dez', 'DIA 10', 'white'), ('internet', 'SEM INTERNET', 'red')]}),
  ('bk_close', 'I', 'drama', ['beto@a:hold/squint^0,0+paper'], {'at': 'Ele', 'opts': {'day': 10, 'cans': 'full'}, 'lab': [('onze', 'MANUAL ×11', 'orange')]})],
 [('bk_cal', 'I', 'push', [], {'opts': {'day': 30, 'cans': 'many'}, 'lab': [('trinta', 'DIA 30', 'white')]}),
  ('bk_shelf', 'I', 'orbit', ['beto@a:hold/laugh^1,0+can'], {'at': 'Aí', 'opts': {'day': 30, 'cans': 'many'}, 'lab': [('nome', 'LATAS COM NOME', 'yellow'), ('Rosinha', 'ROSINHA ♥', 'purple')]})],
 [('bk_bike', 'I', 'push', ['beto@a:hip/hot^1,0+sweat'], {'opts': {'day': 60, 'cans': 'few'}, 'lab': [('sessenta', 'DIA 60', 'white'), ('duas', '2 h POR DIA', 'orange')]}),
  ('bk_bike', 'I', 'drama', ['beto@a:both_up/proud^0,0+sweat'], {'at': 'perna', 'opts': {'day': 60, 'cans': 'few'}, 'shake': 'dobro', 'lab': [('dobro', 'PERNA 2×', 'yellow')]})],
 [('bk_shelf', 'I', 'pull', ['beto@a:temple/sad^1,0'], {'opts': {'day': 99, 'cans': 'one', 'dim': True}, 'lab': [('noventa', 'DIA 99', 'white'), ('uma', 'ÚLTIMA LATA', 'red')]}),
  ('bk_close', 'I', 'drama', ['beto@a:hold/talk^0,0+can+tears'], {'at': 'Beto', 'opts': {'day': 99, 'cans': 'one', 'dim': True}, 'shake': 'noite', 'lab': [('noite', 'A NOITE INTEIRA', 'yellow')]})],
 # 3 PERGUNTA FINAL (volta ao plano aberto do gancho = loop)
 [('bk_wide', 'I', 'push', ['beto@a:point/talk^0,0+can'], {'opts': {'day': 99, 'cans': 'one', 'dim': True}, 'speaker': 'beto'})],
]}
HF = [dict(kind='counter', at='quatrocentas', until='internet', label='LATAS', value='400'),
      dict(kind='counter', at='Sobrou', until='>você', label='LATAS', value='1')]
