import sys; sys.path.insert(0, 'REPO/engine/py')
from presets import *
# Ref: https://www.youtube.com/shorts/56c8c2nRsF4 (regras em regras_edicao.md): HUD de relógio, contador, etiqueta ERRO FATAL, final A/B
FORMAT = 'short'; GAP = 0; TAIL = 0.6; MOOD = 'tension'; STING = None
OVERLAYS = False   # textos ficam na camada HyperFrames
PILL_TOP = 420     # o HUD do relógio ocupa o topo esquerdo
KEYWORDS = ['gta', 'casado', 'feriadao', 'trinta', 'trigesimo', 'bia', 'amanha', 'some', 'rafa', 'catorze', 'testada', 'diferente',
            'louca', 'churrasco', 'liberadas', 'tocar', 'horinha', 'roteador', 'salvado', 'corredor', 'dez', 'missao', 'escolhe']
BUBBLES = [('Cê viu o Rafa? Ele não sai do quarto desde a meia-noite.', 'LU', '#9d7ad6', 'viu', 'meia'),
           ('Amor, amanhã a gente sai às dez, né?', 'BIA', '#ff9f1c', '>Amor', 'né'),
           ('Comenta aí: A ou B?', 'VOCÊ', '#2f9e95', '>Comenta', '>B')]
CARDS = {}
ORDER = ['short']
NIGHT_ROOM = {'clock': 23.9, 'screen': 'MISSÃO 12', 'prog': 0.85}
DAY_ROOM = {'clock': 15.0, 'screen': 'MISSÃO 3', 'prog': 0.2}
RAFA_ROOM = {'clock': 3.0, 'screen': 'MISSÃO 9', 'prog': 0.6}
SEG = {'short': [
 # 1 GANCHO
 [('tw_up', 'N', 'push', [], {'opts': {'lit': 0.35}, 'flash': 'casado', 'lab': [('casado', 'GTA 6 + CASADO?', 'yellow')]}),
  ('tw_win', 'N', 'push', [], {'opts': {'lit': 0.95}, 'fx': ['twinkle']}),
  ('lr_sofa', 'I', 'drama', ['voce@v:hold/surprise+controller+sweat'], {'opts': NIGHT_ROOM})],
 # 2 ACONTECIMENTOS
 [('lr_wide', 'I', 'push', ['voce@v:hold/happy+controller'], {'opts': NIGHT_ROOM}),
  ('lr_door', 'I', 'push', ['bia@h:cross/proud^-1,0'], {'opts': NIGHT_ROOM})],
 [('tw_win', 'N', 'pull', [], {'opts': {'lit': 0.95}, 'flash': 'Meia'}),
  ('tw_up', 'N', 'push', [], {'opts': {'lit': 0.95}})],
 [('lr_sofa', 'I', 'push', ['rafa@v:hold/sleepy+controller'], {'opts': RAFA_ROOM, 'fx': ['night']})],
 [('lr_sofa', 'I', 'drama', ['rafa@v:hold/talk+controller+sweat'], {'opts': RAFA_ROOM, 'fx': ['night'], 'speaker': 'rafa'}),
  ('lr_tv', 'I', 'push', [], {'opts': RAFA_ROOM, 'fx': ['night'], 'at': 'Ninguém'})],
 [('k_sink', 'G', 'push', ['voce@1.3,-2.2:hip/proud', 'bia!@2.2,-2.6:cross/happy^-1,0'], {'flash': 'semana'}),
  ('k_sink', 'G', 'push', ['voce@1.3,-2.2:hold/happy', 'bia!@2.2,-2.6:cheek/surprise^-1,0'], {}),
  ('k_tv', 'G', 'orbit', ['voce@a:thumb/happy', 'cida!@3.3,-0.7:both_up/laugh^-1,0'], {'opts': {'tv': 'CHURRASCO SÁBADO'}})],
 [('lr_wide', 'ID', 'push', ['voce@v:hold/happy+controller+sunglasses'], {'opts': DAY_ROOM, 'flash': 'Quinta'}),
  ('lr_sofa', 'ID', 'drama', ['voce@v:phone/surprise+phone'], {'opts': DAY_ROOM, 'shake': 'tocar', 'at': 'Até'}),
  ('k_window', 'ID', 'push', ['lu@a:phone/worried+phone^0.5,0'], {'speaker': 'lu', 'at': 'Era'})],
 [('lr_sofa', 'I', 'push', ['rafa@v:hold/happy+controller'], {'opts': RAFA_ROOM, 'fx': ['night']}),
  ('lr_tv', 'I', 'drama', [], {'opts': dict(RAFA_ROOM, screen='SEM CONEXÃO', prog=0.0), 'fx': ['night'], 'shake': 'salvado'})],
 [('lr_wide', 'I', 'push', ['voce@v:hold/neutral+controller'], {'opts': NIGHT_ROOM}),
  ('lr_door', 'I', 'push', ['bia@h:hip/talk^-1,0'], {'opts': NIGHT_ROOM, 'speaker': 'bia', 'at': 'Uma'})],
 [('lr_clock', 'I', 'drama', [], {'opts': NIGHT_ROOM}),
  ('lr_tv', 'I', 'push', [], {'opts': NIGHT_ROOM})],
 # 3 PERGUNTA FINAL
 [('lr_sofa', 'I', 'push', ['voce@v:point/talk+controller^0,0'], {'opts': NIGHT_ROOM, 'speaker': 'voce'})],
]}

# camada HyperFrames: gramática da referência (relógio no topo, contador, etiquetas, carimbos, celular, A/B)
Q = 'QUINTA · 19 DE NOVEMBRO'
HF = [
 dict(kind='hud', at='Se', day='VÉSPERA', time='23:40', date='QUARTA · 18 DE NOVEMBRO'),
 dict(kind='hud', at='Eu', day='VÉSPERA', time='23:46', date='QUARTA · 18 DE NOVEMBRO'),
 dict(kind='hud', at='trigésimo', day='VÉSPERA', time='23:51', date='QUARTA · 18 DE NOVEMBRO'),
 dict(kind='name', at='trinta#2', until='Essa', name='VOCÊ', sub='31 ANOS · CASADO HÁ 5'),
 dict(kind='name', at='Bia', until='amanhã', name='BIA', sub='30 ANOS · NUNCA PERDEU UMA DISCUSSÃO'),
 dict(kind='hud', at='Bia', day='VÉSPERA', time='23:58', date='QUARTA · 18 DE NOVEMBRO'),
 dict(kind='hud', at='Meia', day='DIA 1', time='00:00', date=Q),
 dict(kind='bigclock', at='Meia', until='grupo#2', text='00:00', low=True),
 dict(kind='phone', at='grupo#2', until='responde', title='FUTEBOL DE QUINTA ⚽', sub='31 participantes', low=True,
      msgs=[('JÚNIOR', 'BAIXOU 100% 🔥', 'grupo#2'), ('DIEGO', 'tô dentro', 'enlouquece'), ('RAFA', 'alguém online?', 'galera'), ('JÚNIOR', 'não me liguem', 'some')]),
 dict(kind='counter', at='galera', label='AMIGOS SUMIDOS', value='0'),
 dict(kind='counter', at='some', label='AMIGOS SUMIDOS', value='6'),
 dict(kind='counter', at='responde', until='Rafa', label='AMIGOS SUMIDOS', value='22'),
 dict(kind='hud', at='Rafa', day='DIA 1', time='14:00', date=Q),
 dict(kind='name', at='Rafa', until='vacilou', name='RAFA', sub='31 ANOS · VISTO POR ÚLTIMO HÁ 14H'),
 dict(kind='counter', at='catorze', until='Você#4', label='AMIGOS SUMIDOS', value='29'),
 dict(kind='tag', at='vacilou', until='Você#4', title='ERRO FATAL Nº 1', sub='AVISAR SÓ NO DIA', stamp='NÃO FAÇA', stamp_at='Ninguém#2', low=True),
 dict(kind='hud', at='Você#4', day='7 DIAS ANTES', time='20:10', date='QUINTA · 12 DE NOVEMBRO'),
 dict(kind='tone', at='Você#4', until='liberadas', color='#b08850'),
 dict(kind='badge', at='semana', until='liberadas', text='UMA SEMANA ANTES'),
 dict(kind='name', at='troca', until='Quinta#2', name='DONA CIDA', sub='SOGRA · CHURRASCO DE SÁBADO'),
 dict(kind='counter', at='liberadas', until='Quinta#2', label='HORAS LIBERADAS', value='48'),
 dict(kind='hud', at='Quinta#2', day='DIA 1', time='15:00', date=Q),
 dict(kind='name', at='Lu', until='Ele', name='LU', sub='MULHER DO RAFA'),
 dict(kind='hud', at='Rafa#3', day='CASA DO RAFA', time='03:00', date='MADRUGADA'),
 dict(kind='tag', at='Rafa#3', until='três#2', title='ERRO FATAL Nº 2', sub='PROMETER "SÓ UMA HORINHA"', stamp='NÃO FAÇA', stamp_at='horinha', low=True),
 dict(kind='stamp', at='salvado', until='Quinta#3', text='NÃO SALVO'),
 dict(kind='hud', at='Quinta#3', day='DIA 1', time='23:58', date=Q),
 dict(kind='choice', at='Agora', until='>Comenta', title='VOCÊ DECIDE', a='SALVA O JOGO E VAI DORMIR', b='SÓ MAIS UMA MISSÃO',
      hl=[('Salva', 'a'), ('Ou', 'b')], low=True),
]
