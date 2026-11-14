import sys; sys.path.insert(0, 'REPO/engine/py')
from presets import *
FORMAT = 'short'; GAP = 0; TAIL = 0.6; MOOD = 'day'; STING = None
OVERLAYS = False   # textos ficam na camada HyperFrames
PILL_TOP = 360     # contador ocupa o canto superior direito
KEYWORDS = ['milhao', 'conta', 'sempre', 'dezembro', 'sete', 'beto', 'banco', 'caiu', 'dividas', 'novecentos', 'predio', 'todo',
            'sindico', 'bairro', 'primo', 'irmao', 'doze', 'milhoes', 'varzea', 'estadio', 'domingo', 'primeiro']
BUBBLES = [('E você, ia fazer o que com o primeiro milhão?', 'BETO', '#5cb85c', '>você', '>milhão')]
CARDS = {}
ORDER = ['short']
FANS = ['p1@7,3.4:wave/happy^-1,0', 'p2@9,2.4:both_up/happy^-1,0', 'p3@11,1.4:point/laugh^-1,0', 'p4@13,0.4:wave/laugh^-1,0', 'p5@15,-0.6:both_up/happy^-1,0', 'p6@17,-1.6:wave/happy^-1,0']
SEG = {'short': [
 # 1 GANCHO
 [('b_room', 'I', 'drama', ['beto@a:phone/surprise+phone^0.3,-0.4'], {'flash': 'milhão', 'lab': [('milhão', 'R$ 1 MILHÃO?', 'yellow')]}),
  ('tw_up', 'N', 'push', [], {'opts': {'lit': 0.6}, 'fx': ['twinkle'], 'at': 'mês', 'lab': [('mês', 'TODO MÊS · PRA SEMPRE', 'orange')]})],
 # 2 ACONTECIMENTOS
 [('b_room', 'ID', 'push', ['beto@a:phone/sleepy+phone^0.3,-0.4'], {'lab': [('sete', '1º DEZ · 07:00', 'white'), ('Beto', 'BETO', 'teal', '28 ANOS')]}),
  ('b_room', 'ID', 'drama', ['beto@a:both_up/surprise+phone'], {'at': 'lá', 'shake': 'milhão', 'lab': [('Sem', 'SEM PRÊMIO · SEM HERANÇA', 'white')]})],
 [('k_tv', 'G', 'push', ['cida!@3.3,-0.7:both_up/laugh^-1,0'], {'opts': {'tv': 'DÍVIDAS: R$ 0'}, 'lab': [('quitou', 'DÍVIDAS QUITADAS', 'green')]}),
  ('k_sink', 'G', 'push', ['beto@1.3,-2.2:hip/proud', 'p6!@2.2,-2.6:cheek/surprise^-1,0'], {'at': 'ainda'})],
 [('tw_up', 'D', 'pull', [], {'opts': {'lit': 0.2}, 'lab': [('terceiro', 'MÊS 3', 'yellow'), ('todo', 'O PRÉDIO TODO', 'orange')]}),
  ('lr_door', 'ID', 'push', ['beto@h:hip/proud^-1,0'], {'at': 'Agora'})],
 [('st_wide', 'D', 'push', FANS, {'lab': [('sexto', 'MÊS 6', 'yellow'), ('Fila', 'FILA DE PRIMOS', 'orange')]}),
  ('st_stall', 'D', 'orbit', ['beto@a:temple/worried^1,0', 'p4!@b:wave/laugh^-1,0'], {'at': 'gente', 'lab': [('irmão', 'IRMÃO!', 'red')]})],
 [('f_mid', 'D', 'pull', ['beto@p:both_up/proud', 'p1@d1:wave/happy', 'p3@d3:both_up/laugh'], {'lab': [('ano', '1 ANO DEPOIS', 'yellow'), ('várzea', 'TIME DE VÁRZEA', 'teal')]}),
  ('f_high', 'D', 'drama', [], {'at': 'estádio', 'shake': 'estádio', 'flash': 'estádio', 'lab': [('estádio', 'ESTÁDIO PARTICULAR', 'orange')]})],
 # 3 PERGUNTA FINAL (volta ao quarto do gancho = loop)
 [('b_room', 'I', 'push', ['beto@a:point/talk+phone^0,0'], {'speaker': 'beto'})],
]}

HF = [
 dict(kind='phone', at='app', until='caiu', title='BANCO 🏦', sub='notificações', low=True,
      msgs=[('PIX RECEBIDO', 'R$ 1.000.000,00', 'lá'), ('DE', '???', 'prêmio'), ('SALDO', 'R$ 1.000.003,12', 'caiu')]),
 dict(kind='counter', at='quitou', label='SALDO', value='R$ 1.000.000'),
 dict(kind='counter', at='novecentos', label='SALDO', value='R$ 900.000'),
 dict(kind='counter', at='terceiro', label='PATRIMÔNIO', value='1 PRÉDIO'),
 dict(kind='stamp', at='síndico', until='sexto', text='SÍNDICO'),
 dict(kind='counter', at='Fila', label='PRIMOS NOVOS', value='+47'),
 dict(kind='counter', at='doze', until='>domingo', label='SALDO', value='R$ 12.000.000'),
]
