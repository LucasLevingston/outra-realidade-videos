import sys; sys.path.insert(0, 'REPO/engine/py')
from presets import *
# Ref: https://www.instagram.com/p/DfkU3yVsDmC/ (regras em regras_edicao.md): "nunca faça X" -> a cena mostra X; rótulo novo a cada ~2 s; listas que crescem
FORMAT = 'short'; GAP = 0; TAIL = 0.6; MOOD = 'comedy'; STING = None
OVERLAYS = False   # textos ficam na camada HyperFrames
KEYWORDS = ['falte', 'gta', 'cinco', 'chefe', 'profissional', 'vice', 'gripado', 'tossezinha', 'pigarro', 'ridiculo', 'offline',
            'profissionalismo', 'noite', 'instale', 'console', 'controle', 'nada', 'internet', 'computador', 'imprevisto', 'criatividade',
            'empresa', 'lu', 'nega', 'negue', 'crianca', 'produtivo', 'trailer', 'gameplay', 'live', 'banheiro', 'quarenta', 'expediente',
            'camisa', 'trabalhar', 'jogar']
BUBBLES = [('Vai jogar no lançamento?', 'LU', '#9d7ad6', 'perguntar', 'lançamento'),
           ('Eu? Joguinho é coisa de criança.', 'VOCÊ', '#2f9e95', 'joguinho', 'produtivo'),
           ('E você, ia trabalhar ou ia jogar?', 'VOCÊ', '#2f9e95', '>você', '>jogar')]
CARDS = {}
ORDER = ['short']
SFX = [('mensagem', 'typing'), ('bem', 'notif'), ('profissional', 'sparkle'), ('Vice', 'boing'),
       ('tossezinha', 'cough', 1.0), ('pigarro', 'cough', 1.0), ('últimas', 'cough', 0.9), ('ridículo', 'ting'),
       ('Steam', 'click'), ('PlayStation', 'click'), ('Xbox', 'click'), ('profissionalismo', 'wrong'),
       ('instale', 'ting'), ('atualize', 'ting'), ('carregando', 'ting'), ('planejando', 'boing'),
       ('internet', 'typing'), ('computador', 'typing'), ('imprevisto', 'typing'), ('criatividade', 'sparkle'),
       ('negue', 'buzz'), ('criança', 'boing'), ('trailer', 'notif'), ('live', 'click'), ('Já', 'riser'),
       ('quarenta', 'tick'), ('Ainda', 'sparkle'), ('camisa', 'whoosh')]

DESK = {'cert': True, 'screen': 'PLANILHA'}
NIGHT_TV = {'clock': 23.97, 'screen': 'BAIXANDO', 'prog': 1.0}
DAY_TV = {'clock': 9.5, 'screen': 'MISSÃO 1', 'prog': 0.15}
SEG = {'short': [
 # 1 GANCHO
 [('of_wide', 'ID', 'push', ['voce@v:hip/happy^0,0', 'lu@c:hold/neutral^1,0'], {'opts': DESK, 'flash': 'falte', 'lab': [('falte', 'NÃO FALTE!', 'yellow')]}),
  ('of_desk', 'ID', 'drama', ['voce@v:thumb/proud^0,0'], {'at': 'GTA', 'opts': DESK, 'lab': [('GTA', 'NO DIA DO GTA 6', 'white')]})],
 # 2 ACONTECIMENTOS
 [('b_room', 'N', 'push', ['voce@a:phone/sleepy^0.3,0+phone'], {'lab': [('cinco', '05:00', 'white')]}),
  ('b_room', 'N', 'drama', ['voce@a:phone/cold^0.3,0+phone+sweat'], {'at': 'dizendo'}),
  ('of_cert', 'ID', 'push', [], {'at': 'Você', 'opts': DESK}),
  ('of_desk', 'ID', 'push', ['voce@0.6,-2.4:hip/proud^-1,0', 'tecnico@-0.15,-2.6:point/happy^1,0'], {'at': 'empresa', 'opts': DESK, 'lab': [('conta', 'A EMPRESA CONTA COM VOCÊ', 'yellow')]}),
  ('lr_tv', 'ID', 'push', [], {'at': 'Vice', 'opts': dict(DAY_TV, screen='VICE CITY', prog=0.0), 'lab': [('esperar', 'PODE ESPERAR', 'orange')]})],
 [('lr_wide', 'ID', 'push', ['voce@v:temple/cold^0,0+scarf'], {'opts': DAY_TV, 'lab': [('ensaiar', 'ENSAIO GERAL', 'yellow')]}),
  ('lr_sofa', 'ID', 'drama', ['voce@v:belly/sleepy^0,0+scarf+sweat'], {'at': 'tossezinha', 'opts': DAY_TV, 'lab': [('tossezinha', 'COF COF ✓', 'white'), ('pigarro', 'HÃ-HÃM ✓', 'white'), ('últimas', 'VOZ DE ÚLTIMAS ✓', 'white')]}),
  ('lr_sofa', 'ID', 'push', ['voce@v:thumb/proud^0,0+scarf'], {'at': 'Isso', 'opts': DAY_TV})],
 [('lr_sofa', 'ID', 'push', ['voce@v:hold/happy^0.5,0+controller'], {'opts': DAY_TV}),
  ('lr_wide', 'ID', 'orbit', ['voce@v:hold/laugh^0.5,0+controller'], {'at': 'Isso', 'opts': dict(DAY_TV, prog=0.6), 'shake': 'falta'})],
 [('lr_tv', 'N', 'push', [], {'opts': NIGHT_TV, 'lab': [('instale', 'JOGO INSTALADO ✓', 'green'), ('atualize', 'CONSOLE ATUALIZADO ✓', 'green')]}),
  ('lr_sofa', 'N', 'push', ['voce@v:hold/happy^0.5,0+controller'], {'at': 'controle', 'opts': NIGHT_TV, 'lab': [('carregando', 'CONTROLE 100%', 'green')]}),
  ('lr_wide', 'N', 'pull', ['voce@v:cross/proud^0,0'], {'at': 'afinal', 'opts': NIGHT_TV, 'lab': [('planejando', 'ZERO PLANOS', 'yellow')]})],
 [('of_desk', 'ID', 'push', ['voce@v:temple/squint^0.5,0'], {'opts': dict(DESK, screen='DESCULPAS.TXT')}),
  ('of_mon', 'ID', 'push', [], {'at': 'imprevisto', 'opts': dict(DESK, screen='DESCULPAS.TXT')}),
  ('of_desk', 'ID', 'push', ['voce@v:both_up/laugh^0,0'], {'at': 'criatividade', 'opts': DESK, 'lab': [('criatividade', 'CRIATIVIDADE PRA EMPRESA', 'yellow')]})],
 [('of_cool', 'ID', 'push', ['voce@a:hold/neutral^1,0+mug', 'lu!@b:hip/talk^-1,0'], {'opts': DESK}),
  ('of_cool', 'ID', 'drama', ['voce@a:cross/proud^1,0+mug', 'lu!@b:cheek/surprise^-1,0'], {'at': 'negue', 'opts': DESK, 'lab': [('negue', 'NEGA TUDO', 'red')]}),
  ('of_cool', 'ID', 'push', ['voce@a:thumb/proud^0,0+mug', 'lu!@b:cross/squint^-1,0'], {'at': 'joguinho', 'opts': DESK, 'lab': [('produtivo', 'SUPER PRODUTIVO', 'green')]})],
 [('of_wc', 'ID', 'push', ['voce@a:phone/happy^0,0+phone'], {'opts': {'stall': 'open'}, 'lab': [('trailer', 'TRAILER · 31ª VEZ', 'white'), ('live', 'AO VIVO', 'red')]}),
  ('of_mon', 'ID', 'push', [], {'at': 'banheiro', 'opts': dict(DESK, screen='GAMEPLAY', live=True)}),
  ('of_wc', 'ID', 'drama', ['voce@-4.85,-3.2:phone/surprise^0.5,0+phone+sweat', 'tecnico!@-4.05,-1.9:cross/angry^-1,0'], {'at': 'Já', 'opts': {'stall': 'open'}, 'shake': 'expediente', 'flash': 'expediente'}),
  ('of_wc', 'ID', 'pull', ['voce@a:thumb/happy^0,0+phone'], {'at': 'Ainda', 'opts': {'stall': 'open'}, 'lab': [('Ainda', 'AINDA BEM...', 'yellow')]})],
 # 3 PERGUNTA FINAL (volta ao enquadramento do gancho = loop)
 [('of_wide', 'ID', 'push', ['voce@v:hip/happy^0,0', 'lu@c:hold/neutral^1,0'], {'opts': DESK, 'lab': [('camisa', 'VISTA A CAMISA', 'yellow')]}),
  ('of_desk', 'ID', 'push', ['voce@v:point/talk^0,0'], {'at': 'conta', 'opts': DESK, 'speaker': 'voce'})],
]}

# camada HyperFrames: telas de interface e listas que crescem (gramática da referência)
HF = [
 dict(kind='phone', at='mensagem', until='Você', title='CHEFE', sub='online', low=True,
      msgs=[('VOCÊ', 'Chefe, não tô me sentindo bem…', 'mensagem'), ('VOCÊ', 'acho que é virose 🤒', 'sentindo'), ('CHEFE', 'Melhoras! A empresa conta com você', 'bem')]),
 dict(kind='badge', at='profissional', until='empresa', text='FUNCIONÁRIO RESPONSÁVEL'),
 dict(kind='name', at='empresa', until='Vice', name='CHEFE', sub='GERENTE · 20 ANOS DE CASA'),
 dict(kind='stamp', at='ridículo', until='também', text='NOTA 10'),
 dict(kind='phone', at='perfil', until='falta', title='MEU PERFIL', sub='status', low=True,
      msgs=[('STEAM', '⚫ OFFLINE', 'Steam'), ('PLAYSTATION', '⚫ OFFLINE', 'PlayStation'), ('XBOX', '⚫ OFFLINE', 'Xbox')]),
 dict(kind='stamp', at='falta', until='Nunca#3', text='FALTA GRAVE'),
 dict(kind='badge', at='noite', until='instale', text='NOITE ANTERIOR · 23:58'),
 dict(kind='phone', at='internet', until='criatividade', title='DESCULPAS.TXT', sub='3 itens', low=True,
      msgs=[('1', 'A internet caiu', 'internet'), ('2', 'O computador pifou', 'computador'), ('3', 'Imprevisto em casa', 'imprevisto')]),
 dict(kind='name', at='Lu', until='negue', name='LU', sub='COLEGA DO FINANCEIRO'),
 dict(kind='counter', at='quarenta', until='Ainda', label='GAMEPLAY NO EXPEDIENTE', value='40 MIN'),
 dict(kind='stamp', at='nunca#5', until='Então', text='INOCENTE'),
]
