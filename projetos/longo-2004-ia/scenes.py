# Plano de cenas — L19 "E se você voltasse pra 2004 com uma IA no celular?" (vídeo longo 16:9)
# Cada parágrafo do roteiro -> lista de planos: (preset, luz, movimento, [personagens], extras)
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'engine', 'py'))
from presets import *

FORMAT = 'long'
GAP = 2.5; TAIL = 5.0
MOOD = None   # trilha por segmento (SEGMOOD do longaudio)

# cenário novo pc2004 (quarto / sala / lan house de 2004)
PRE.update({
 'pc_room':   ('pc2004', [0.2, 1.6, 3.2], [0.6, 1.0, -2.6], 50, {'a': (1.6, -1.8), 'b': (-0.4, -1.2), 'c': (0.4, -0.6)}),
 'pc_desk':   ('pc2004', [-0.6, 1.45, 0.9], [1.2, 1.0, -2.8], 42, {'a': (0.5, -1.7), 'b': (1.9, -1.6)}),
 'pc_screen': ('pc2004', [1.15, 1.12, -1.35], [1.2, 1.05, -2.7], 36, {}),
 'pc_lan':    ('pc2004', [0, 1.7, 3.4], [0, 1.1, -2.6], 55, {'a': (-1.4, -1.4), 'b': (0.6, -1.2), 'c': (2.2, -0.8), 'd': (-2.6, -1.6)}),
 'st_crowd':  ('street', [1, 1.6, -1], [10, 1.4, -6], 44, {'a': (6, -6.5), 'b': (6.6, -5.4), 'c': (7.2, -4.3), 'd': (7.6, -7.2), 'e': (5.4, -3.6)}),
 'c_close':   ('classroom', [0.4, 1.5, 2.4], [-0.2, 1.0, -2.5], 46, {'a': (0.2, -1.0), 'k1': (-1.0, -1.5), 'k2': (0.0, -1.1), 'k3': (1.1, -1.4)}),
 'pc_lan2':   ('pc2004', [2.6, 1.5, 1.8], [-1.0, 1.1, -2.4], 45, {'a': (0.0, -1.3), 'b': (1.3, -0.7)}),
})

C = 'caio20'
ROOM = {'bed': True}                                   # quarto do Caio em 2004
SALA = {'wall': '#9fc7a8', 'cal': 'MARÇO\n2004'}      # computador da sala
LAN = {'lan': True, 'cal': 'ABRIL\n2004'}

SEG = {}
SEG['c0'] = [
 [('st_wide', 'D', 'push', [f'{C}@a:phone/happy+phone', 'p1@b:hang/neutral', 'p4@c:hip/neutral', 'p6@d:cross/neutral'], {'opts': {'shop': 'FILA AQUI', 'shopX': 9}, 'lab': [('dois', '2004', 'yellow'), ('inteligência', 'IA NO BOLSO', 'teal')]})],
 [('st_down', 'D', 'panR', [], {'opts': {'shop': 'CASA DO MURO AZUL', 'shopX': 6}, 'lab': [('terça', 'TERÇA · 8H', 'white')]}),
  ('st_wide', 'D', 'push', ['p1@a:hang/neutral', 'p2@b:hip/neutral', 'p3@c:cross/neutral', 'p4@d:hang/neutral', 'p5@e:hang/neutral'], {'lab': [('maior', 'A MAIOR FILA DA CIDADE', 'yellow')]})],
 [('st_stall', 'D', 'push', ['p6@a:cross/neutral', 'p4!@b:hip/neutral'], {'opts': {'stall': [2, -8], 'stallText': 'PADARIA\nPÃO R$ 0,10'}, 'lab': [('padaria', 'PADARIA', 'orange'), ('borracharia', 'BORRACHARIA', 'blue'), ('vereador', 'ATÉ VEREADOR', 'red')]})],
 [('pc_room', 'ID', 'push', [f'{C}@a:phone/neutral+phone'], {'opts': ROOM, 'lab': [('Caio', 'CAIO', 'teal', '17 ANOS'), ('programar', 'NÃO SABE PROGRAMAR', 'red')]})],
 [('pc_desk', 'ID', 'push', [f'{C}@a:phone/happy+phone^0.5,0'], {'opts': ROOM, 'lab': [('vinte', 'CELULAR DE 2026', 'yellow'), ('qualquer', 'FAZ QUALQUER COISA QUE ELE PEDE', 'teal')]})],
 [('pc_room', 'I', 'pull', [f'{C}@a:hang/sleepy'], {'opts': ROOM, 'flash': 'começo', 'lab': [('vinte', '22 ANOS ATRÁS', 'white')]})],
]
SEG['c1'] = [
 [('pc_room', 'I', 'push', [f'{C}@c:hang/sleepy+phone'], {'opts': dict(ROOM, cal='MARÇO\n2026'), 'lab': [('segunda', 'SEGUNDA · 2026', 'white')]})],
 [('pc_room', 'ID', 'orbit', [f'{C}@c:temple/surprise^0.4,-0.3'], {'opts': ROOM, 'lab': [('tubo', 'COMPUTADOR DE TUBO', 'yellow'), ('CD', 'CD GRAVADO', 'white')]}),
  ('pc_desk', 'ID', 'push', [f'{C}@a:reach/surprise^0.6,0'], {'opts': ROOM, 'lab': [('pôster', 'PÔSTER ???', 'purple')]})],
 [('k_wide', 'ID', 'push', ['cida@st:hold/happy+mug', f'{C}!@fl:hang/surprise'], {'lab': [('café', 'CAFÉ NO COADOR', 'orange'), ('novinha', 'MÃE: 20 ANOS MAIS NOVA', 'yellow')]})],
 [('k_wide', 'ID', 'hold', [f'{C}@fl:temple/worried', 'cida!@st:hold/talk+mug'], {'speaker': 'cida', 'lab': [('febre', '"TÁ COM FEBRE?"', 'red')]}),
  ('k_window', 'ID', 'drama', [f'{C}@b:hang/surprise^-0.6,-0.3'], {'at': 'olhou', 'shake': 'Março', 'lab': [('Março', 'MARÇO DE 2004', 'yellow')]})],
 [('c_desks', 'ID', 'push', [f'{C}@k2:phone/talk+phone', 'p2!@k3:belly/laugh'], {'speaker': 'p2', 'lab': [('Duda', 'DUDA', 'purple', 'AMIGA DA ESCOLA'), ('ligar', '"CELULAR É PRA LIGAR"', 'purple')]})],
 [('c_desks', 'ID', 'push', ['p2@k3:phone/neutral+phone'], {'lab': [('flip', 'FLIP + ANTENA', 'white'), ('mapa', 'SEM MAPA · SEM APP', 'red'), ('discada', 'INTERNET DISCADA', 'yellow')]}),
  ('pc_screen', 'I', 'push', [], {'opts': {'scr': 'dial', 'screen': 'CONECTANDO... 56K'}, 'lab': [('meia-noite', 'SÓ DEPOIS DA MEIA-NOITE', 'blue')]})],
 [('lr_wide', 'ID', 'push', ['cida@b:phone/talk+phone'], {'opts': {'clock': 14.0, 'screen': 'NOVELA'}, 'lab': [('fixo', 'TELEFONE FIXO', 'white'), ('filme', 'FOTO: 3 DIAS NA FARMÁCIA', 'orange')]})],
 [('c_desks', 'ID', 'push', [f'{C}@a:phone/worried+phone^0,0.6'], {'lab': [('tela', 'A TELA ACENDEU', 'yellow')]}),
  ('c_desks', 'ID', 'drama', [f'{C}@a:phone/happy+phone^0,0.6'], {'flash': 'IA', 'lab': [('jeitinho', 'A IA VEIO JUNTO', 'teal')]})],
 [('c_board', 'ID', 'push', ['prof@b:point/talk', f'{C}@k2:phone/neutral+phone', 'p2@k3:hang/neutral'], {'opts': {'board': 'TRABALHO:\nREGIÕES DO BRASIL'}, 'lab': [('geografia', 'GEOGRAFIA', 'white')]}),
  ('c_desks', 'ID', 'push', [f'{C}@a:phone/talk+phone^0,0.6'], {'lab': [('mapa', 'MAPA + GRÁFICO + FONTES', 'yellow')]})],
 [('c_board', 'ID', 'push', [f'{C}@a:point/proud', 'prof!@b:hang/surprise', 'p2@k3:hang/surprise', 'p3@k1:hang/surprise'], {'opts': {'board': 'REGIÕES\nDO BRASIL'}, 'lab': [('dois', '2 MINUTOS', 'yellow'), ('silêncio', 'SILÊNCIO', 'white')]})],
 [('c_desks', 'ID', 'panR', ['p3@k1:temple/squint', 'p5@k2:point/talk', 'p1@k3:hang/surprise'], {'lab': [('revista', '"COPIOU DE REVISTA IMPORTADA?"', 'white')]})],
 [('c_board', 'ID', 'push', ['prof@b:hang/surprise', f'{C}!@a:thumb/proud'], {'opts': {'board': 'REGIÕES\nDO BRASIL'}, 'speaker': 'prof', 'lab': [('Quem', '"QUEM FEZ ISSO?"', 'purple'), ('pediu', 'ELE NÃO FEZ. ELE PEDIU.', 'yellow')]})],
 [('pc_room', 'W', 'push', [f'{C}@c:phone/happy+phone'], {'opts': ROOM, 'lab': [('seis', '06:00 · RESUMO DO DIA', 'teal'), ('provas', 'PROVAS · RECADOS · CIDADE', 'white')]})],
 [('pc_desk', 'ID', 'push', [f'{C}@a:phone/neutral+phone^0.5,0'], {'opts': ROOM, 'lab': [('dentista', 'OK: DENTISTA', 'teal'), ('luz', 'OK: CONTA DE LUZ', 'teal'), ('avó', 'OK: ANIVERSÁRIO DA AVÓ', 'teal')]})],
 [('pc_room', 'ID', 'hold', [f'{C}@b:hang/sleepy'], {'opts': ROOM, 'lab': [('três', '+3 HORAS POR DIA', 'yellow'), ('dormir', 'PRA DORMIR', 'purple')]})],
 [('k_wide', 'I', 'push', ['cida@t1:temple/worried+notebook', f'{C}!@fl:hang/neutral^-1,0'], {'lab': [('caderno', 'CADERNO DE PEDIDOS', 'orange'), ('pensou', 'E SE FOSSE PRA ELA?', 'yellow')]})],
]
SEG['c2'] = [
 [('k_wide', 'ID', 'push', ['cida@st:hold/happy+notebook'], {'lab': [('Cida', 'DONA CIDA', 'red', 'BOLO PRA FORA'), ('cem', '+100 PEDIDOS A LÁPIS', 'white')]})],
 [('k_sink', 'ID', 'push', ['cida@a:temple/worried+notebook'], {'lab': [('levou', 'PEDIU 2, LEVOU 3', 'orange'), ('Marlene', 'DONA MARLENE: DEVENDO', 'red'), ('chocolate', 'CHOCOLATE: DE QUEM?', 'purple')]})],
 [('k_wide', 'ID', 'hold', [f'{C}@fl:point/talk', 'cida!@t1:hold/neutral+notebook'], {'speaker': 'cida', 'lab': [('site', '"E SE TIVESSE UM SITE?"', 'teal'), ('banco', '"SITE É COISA DE BANCO"', 'red')]})],
 [('pc_desk', 'I', 'push', [f'{C}@a:phone/talk+phone^0.6,0'], {'opts': SALA, 'lab': [('queria', 'O QUE QUER', 'yellow'), ('quem', 'PRA QUEM É', 'yellow'), ('cobrar', 'COMO COBRA', 'yellow')]})],
 [('pc_screen', 'I', 'push', [], {'opts': dict(SALA, scr='site'), 'lab': [('cardápio', 'CARDÁPIO COM FOTO', 'white'), ('Carrinho', 'CARRINHO · ENTREGA · CARTÃO', 'teal'), ('lembrete', 'LEMBRETE PRA QUEM DEVE', 'red')]})],
 [('pc_desk', 'I', 'push', [f'{C}@a:hold/neutral^0.6,0'], {'opts': dict(SALA, scr='site'), 'lab': [('testar', 'TESTE: PEDIR · PAGAR · CANCELAR', 'white'), ('erros', '2 ERROS ARRUMADOS', 'teal')]})],
 [('pc_screen', 'I', 'pull', [], {'opts': dict(SALA, scr='site'), 'flash': 'Vinte', 'lab': [('Vinte', '20 MINUTOS', 'yellow'), ('Bolos', 'NO AR', 'red')]})],
 [('pc_desk', 'ID', 'push', ['cida@b:temple/surprise^-0.6,0', f'{C}@a:thumb/proud'], {'opts': dict(SALA, scr='site'), 'lab': [('pago', '1º PEDIDO PAGO', 'teal'), ('coco', '2 BOLOS DE COCO · SÁBADO', 'white'), ('milagre', 'MILAGRE?', 'yellow')]})],
 [('k_wide', 'ID', 'panR', ['cida@st:both_up/laugh'], {'lab': [('trinta', '32 PEDIDOS', 'yellow'), ('lápis', 'NENHUM A LÁPIS', 'white')]})],
 [('st_wide', 'D', 'push', ['p6@a:phone/surprise+phone'], {'lab': [('Marlene', 'LEMBRETE PRA DONA MARLENE', 'white'), ('dez', 'PAGOU EM 10 MIN', 'teal')]})],
 [('k_wide', 'ID', 'push', ['cida@st:belly/laugh', f'{C}!@fl:belly/laugh'], {'speaker': 'cida', 'lab': [('educação', '"COBRA COM MAIS EDUCAÇÃO QUE EU!"', 'red')]})],
 [('pc_room', 'I', 'push', [f'{C}@c:phone/talk+phone'], {'opts': ROOM, 'lab': [('aniversário', 'NIVER DA MÃE · SÁBADO', 'orange'), ('música', 'MÚSICA AO VIVO · 6 PESSOAS', 'white')]})],
 [('pc_desk', 'I', 'push', [f'{C}@a:thumb/happy+phone'], {'opts': ROOM, 'lab': [('reservada', 'OK: MESA RESERVADA', 'teal'), ('surpresa', 'OK: BOLO SURPRESA', 'teal'), ('ninguém', 'SEGREDO', 'purple')]})],
 [('pc_room', 'I', 'push', ['cida@b:hang/sleepy'], {'opts': dict(SALA, screen='RESERVANDO...'), 'fx': ['night'], 'lab': [('duas', '02:00', 'white')]}),
  ('pc_screen', 'I', 'push', [], {'opts': dict(SALA, screen='RESERVANDO...'), 'lab': [('setinha', 'O MOUSE ANDANDO SOZINHO', 'red')]})],
 [('pc_room', 'I', 'drama', ['cida@b:cheek/shout+phone'], {'opts': dict(SALA, screen='RESERVANDO...'), 'speaker': 'cida', 'shake': 'vírus', 'lab': [('vírus', '"É VÍRUS!"', 'red'), ('Beto', 'LIGOU PRO BETO', 'white'), ('formatar', 'AMANHÃ: FORMATAR TUDO', 'red')]})],
 [('pc_room', 'I', 'drama', [f'{C}@a:temple/worried'], {'opts': ROOM, 'lab': [('sumisse', 'SE A IA SUMIR...', 'red'), ('nunca', 'SEM VOLTA PRA 2026', 'yellow')]})],
]
SEG['c3'] = [
 [('lr_door', 'ID', 'push', ['beto@h:hold/neutral', f'{C}!@b:hang/worried'], {'opts': {'door': 'lit', 'clock': 7.0}, 'lab': [('Sete', '07:00', 'white'), ('maleta', 'BONÉ + MALETA', 'red')]})],
 [('pc_lan', 'ID', 'push', ['beto@b:cross/neutral'], {'opts': LAN, 'lab': [('lan', 'LAN HOUSE DO BETO', 'yellow'), ('tarde', '"O MENINO DO SITE"', 'white')]})],
 [('pc_room', 'ID', 'drama', ['beto@b:point/angry', f'{C}!@a:hang/worried'], {'opts': SALA, 'speaker': 'beto', 'lab': [('três', '"EU LEVO 3 MESES"', 'red'), ('apagar', '"VOU APAGAR TUDO"', 'red')]})],
 [('pc_room', 'ID', 'push', [f'{C}@a:point/talk', 'beto!@b:temple/neutral'], {'opts': SALA, 'speaker': C, 'lab': [('quantos', '"QUANTOS CLIENTES?"', 'teal')]}),
  ('pc_room', 'ID', 'hold', ['beto@b:temple/talk', f'{C}!@a:hang/neutral'], {'opts': SALA, 'at': 'coçou', 'speaker': 'beto', 'lab': [('trinta', '"UNS 30"', 'white'), ('lan', '+ FILA DA LAN HOUSE', 'white')]})],
 [('pc_lan2', 'ID', 'push', ['beto@a:hold/worried+notebook'], {'opts': LAN, 'lab': [('caderno', 'TUDO NUM CADERNO', 'orange'), ('seta', 'SETA PRA TODO LADO', 'red')]})],
 [('pc_desk', 'ID', 'push', [f'{C}@a:phone/talk+phone^0.6,0', 'beto@b:cross/squint'], {'opts': SALA, 'speaker': C, 'lab': [('dez', '"ME DÁ 10 MINUTOS"', 'teal'), ('Consertos', 'APP: CONSERTOS DO BETO', 'yellow')]})],
 [('pc_screen', 'ID', 'push', [], {'opts': dict(SALA, scr='app'), 'lab': [('trinta', '30 CLIENTES', 'white'), ('Verde', 'VERDE: PRONTO', 'teal'), ('amarelo', 'AMARELO: ESPERANDO PEÇA', 'yellow'), ('vermelho', 'VERMELHO: ATRASADO', 'red')]})],
 [('pc_desk', 'ID', 'push', ['beto@b:hold/surprise^-0.6,0'], {'opts': dict(SALA, scr='app'), 'lab': [('recado', 'RECADO: "SEU PC TÁ PRONTO"', 'teal')]})],
 [('pc_desk', 'ID', 'hold', ['beto@b:hold/surprise^-0.6,0', f'{C}@a:hang/neutral'], {'opts': dict(SALA, scr='app')}),
  ('pc_room', 'ID', 'push', ['beto@b:thumb/happy', f'{C}!@a:hang/surprise'], {'opts': dict(SALA, scr='app'), 'at': 'Não', 'speaker': 'beto', 'lab': [('vírus', '"NÃO É VÍRUS"', 'teal'), ('tomada', '"PRECISA DE UMA TOMADA BOA"', 'yellow')]})],
 [('lr_door', 'ID', 'push', ['beto@h:point/happy', f'{C}!@b:hang/surprise'], {'opts': {'door': 'lit'}, 'speaker': 'beto', 'lab': [('sei', '"EU SEI QUE NÃO FOI VOCÊ"', 'white'), ('piscou', '*PISCADINHA*', 'yellow')]})],
 [('st_wide', 'N', 'push', ['cida@a:belly/laugh', f'{C}@b:both_up/happy', 'p2@c:hang/happy', 'p4@d:wave/happy'], {'opts': {'shop': 'RESTAURANTE · MÚSICA AO VIVO', 'shopX': 9}, 'lab': [('sábado', 'SÁBADO', 'white'), ('surpresa', 'PARABÉNS, DONA CIDA!', 'yellow')]})],
 [('st_stall', 'N', 'push', ['beto@a:hold/happy', 'p6!@b:belly/laugh'], {'opts': {'stall': [2, -8], 'stallText': 'BOLO\nSURPRESA'}, 'lab': [('terceiro', '3º PEDAÇO', 'orange')]})],
 [('st_wide', 'N', 'push', ['cida@a:hold/talk', f'{C}!@b:hang/neutral'], {'opts': {'shop': 'RESTAURANTE · MÚSICA AO VIVO', 'shopX': 9}, 'speaker': 'cida', 'lab': [('descobriu', '"COMO DESCOBRIU?"', 'red'), ('pesquisei', '"EU PESQUISEI."', 'teal'), ('formatou', 'QUASE FORMATOU A FESTA', 'yellow')]})],
 [('st_wide', 'D', 'push', ['p1@a:hang/neutral', 'p4@b:hip/neutral', 'p6@c:cross/neutral', 'p5@d:hang/neutral'], {'opts': {'shop': 'BOLOS DA DONA CIDA', 'shopX': 9}, 'lab': [('padaria', 'PADARIA', 'orange'), ('borracharia', 'BORRACHARIA', 'blue'), ('costura', 'COSTURA', 'purple')]})],
 [('st_stall', 'D', 'push', ['p3@a:hold/happy', 'p5!@b:hang/sleepy'], {'opts': {'stall': [2, -8], 'stallText': 'FILA\nDO CAIO'}, 'lab': [('bolo', 'TROUXE BOLO', 'yellow'), ('cadeira', 'CADEIRA DE PRAIA', 'blue')]})],
 [('st_wide', 'D', 'push', ['p3@a:temple/angry', 'p1@b:hang/surprise'], {'lab': [('dois', 'R$ 2.000', 'red'), ('abria', 'SITE QUE NEM ABRE', 'red')]})],
 [('st_down', 'D', 'pull', [], {'opts': {'shop': 'FILA', 'shopX': 6}, 'lab': [('quarenta', '40 COMERCIANTES', 'yellow'), ('cinco', '1 POR VEZ = SÓ EM 2005', 'red'), ('faria', 'E VOCÊ?', 'yellow')]})],
]
SEG['c4'] = [
 [('s_wide', 'ID', 'push', [], {'opts': {'screen': 'FEIRA DE\nTECNOLOGIA'}, 'lab': [('prefeitura', 'A PREFEITURA CHAMOU', 'blue'), ('gênio', '"O MENINO GÊNIO"', 'yellow')]})],
 [('s_wide', 'ID', 'panR', ['anchor@l:hold/neutral', 'tecnico@r:cross/neutral'], {'opts': {'screen': 'FEIRA DE\nTECNOLOGIA'}, 'lab': [('câmera', 'TV LOCAL', 'red'), ('prefeito', 'O PREFEITO', 'white'), ('Beto', 'BETO, DE BRAÇO CRUZADO', 'orange')]})],
 [('c_board', 'ID', 'push', ['p3@k1:hold/proud+paper', 'p2@k3:hold/neutral+paper', f'{C}@k2:phone/neutral+phone'], {'opts': {'board': 'FEIRA DE\nTECNOLOGIA'}, 'lab': [('cartolina', 'CARTOLINA + ISOPOR', 'white'), ('celular', 'SÓ O CELULAR', 'yellow')]})],
 [('s_wide', 'ID', 'push', [f'{C}@l:phone/talk+phone', 'tecnico!@r:hang/surprise'], {'opts': {'screen': 'AO VIVO'}, 'lab': [('trezentas', '300 PESSOAS', 'white'), ('plataforma', 'O COMÉRCIO DA CIDADE INTEIRA', 'yellow')]})],
 [('s_screen', 'ID', 'push', [], {'opts': {'screen': 'LOJA + PAINEL\nPRA CADA UM'}, 'lab': [('Login', 'LOGIN · CARRINHO · CARTÃO', 'teal'), ('vendas', 'PAINEL DA PREFEITURA', 'blue'), ('testado', 'TESTADO + LANÇAMENTO', 'yellow')]})],
 [('s_screen', 'ID', 'hold', [], {'opts': {'screen': 'LOJA ✓\nPAGAMENTO ✓\nPAINEL ✓'}, 'lab': [('Loja', 'OK: LOJA', 'teal'), ('Pagamento', 'OK: PAGAMENTO', 'teal'), ('Painel', 'OK: PAINEL', 'teal')]})],
 [('s_wide', 'ID', 'drama', [f'{C}@l:both_up/happy', 'beto!@r:hold/surprise'], {'opts': {'screen': 'PRONTO!'}, 'flash': 'Quarenta', 'lab': [('Quarenta', '40 MINUTOS · 1 CONVERSA', 'yellow'), ('consertos', 'OS CONSERTOS DO BETO TAMBÉM', 'orange')]})],
 [('st_stall', 'N', 'push', ['p6@a:phone/laugh+phone'], {'opts': {'stall': [2, -8], 'stallText': 'PADARIA\n80 PEDIDOS'}, 'lab': [('oitenta', '80 PEDIDOS NUMA NOITE', 'yellow')]})],
 [('s_wide', 'ID', 'push', ['tecnico@r:point/talk', f'{C}!@l:hang/neutral'], {'opts': {'screen': 'PRONTO!'}, 'lab': [('Quem', '"QUEM FEZ ISSO?"', 'white')]}),
  ('s_wide', 'ID', 'push', [f'{C}@l:hold/proud', 'tecnico!@r:hang/surprise'], {'opts': {'screen': 'EU PEDI.'}, 'at': 'Eu', 'speaker': C, 'lab': [('pedi', '"EU NÃO FIZ. EU PEDI."', 'yellow')]})],
 [('s_wide', 'ID', 'panL', [f'{C}@l:point/talk', 'beto!@r:both_up/laugh'], {'opts': {'screen': 'O QUE · PRA QUEM\nCOMO FUNCIONA'}, 'lab': [('qualquer', 'QUALQUER UM PODIA PEDIR', 'teal'), ('aplaudiram', 'APLAUSOS', 'yellow')]})],
 [('pc_room', 'I', 'push', [f'{C}@c:hold/neutral+paper'], {'opts': ROOM, 'lab': [('troféu', 'TROFÉU DE ISOPOR', 'orange')]})],
 [('pc_desk', 'I', 'push', [f'{C}@a:phone/sad+phone^0.5,0'], {'opts': ROOM, 'lab': [('precisava', 'NÃO PRECISAVA DE 2004', 'yellow'), ('mãe', 'A MÃE, EM 2026', 'red'), ('respondido', '1 MENSAGEM SEM RESPOSTA', 'white')]})],
 [('pc_lan', 'ID', 'push', [f'{C}@a:hang/sad', 'beto!@b:cross/neutral'], {'opts': LAN, 'lab': [('gênio', '"EU NÃO SOU GÊNIO"', 'teal')]}),
  ('pc_lan2', 'ID', 'push', ['beto@a:belly/laugh', f'{C}@b:hang/happy'], {'opts': LAN, 'at': 'sei', 'speaker': 'beto', 'lab': [('moleque', '"EU SEI, MOLEQUE."', 'orange')]})],
 [('pc_screen', 'ID', 'push', [], {'opts': dict(LAN, lan=False, scr='chat', screen='Tá na tomada boa?'), 'lab': [('assistente', 'ASSISTENTE DO BETO', 'yellow'), ('tomada', '"TÁ NA TOMADA BOA?"', 'white')]})],
 [('pc_lan2', 'ID', 'push', [f'{C}@b:point/happy', 'beto!@a:thumb/laugh'], {'opts': LAN, 'speaker': 'beto', 'lab': [('pede', '"AGORA QUEM PEDE É O SENHOR"', 'teal'), ('formatar', '"SÓ NÃO DEIXA FORMATAR"', 'orange')]})],
 [('c_desks', 'G', 'push', [f'{C}@a:hang/neutral', 'p2!@k1:hang/surprise'], {'lab': [('vinte', '"UNS 20 ANOS"', 'teal')]}),
  ('c_desks', 'G', 'push', ['p2@k1:cheek/happy', f'{C}!@a:hang/happy'], {'at': 'Sabe', 'speaker': 'p2', 'lab': [('pediu', '"QUANDO VOCÊ FALOU QUE PEDIU"', 'purple'), ('mesmo', '"PARECEU VOCÊ MESMO"', 'purple')]})],
 [('pc_room', 'N', 'push', [f'{C}@c:phone/neutral+phone'], {'opts': ROOM, 'fx': ['night'], 'lab': [('casa', '"ME LEVA PRA CASA"', 'teal')]}),
  ('pc_screen', 'N', 'drama', [], {'opts': dict(ROOM, scr='chat'), 'flash': 'casa'})],
 [('pc_room', 'W', 'pull', [f'{C}@b:temple/surprise'], {'opts': dict(ROOM, cal='MARÇO\n2026', poster='2026'), 'lab': [('acordou', '2026', 'yellow'), ('Dezoito', '18 DIAS EM 2004', 'white'), ('zero', 'AQUI: 0 MINUTOS', 'teal')]})],
]
SEG['c5'] = [
 [('k_wide', 'W', 'push', ['cida@t1:phone/worried+phone'], {'opts': {'tv': 'BOLO DE COCO: DE QUEM?'}, 'lab': [('coco', 'BOLO DE COCO: DE QUEM?', 'orange'), ('dois', '2 SEM DONO', 'red')]})],
 [('k_wide', 'W', 'push', ['cida@t1:hold/neutral', f'{C}@t2:phone/talk+phone'], {'lab': [('loja', 'A LOJA DE BOLO, EM 2026', 'yellow'), ('resumo', 'RESUMO TODA MANHÃ', 'teal')]})],
 [('k_wide', 'ID', 'push', ['cida@t1:hold/happy', f'{C}!@t2:hang/happy'], {'speaker': 'cida', 'lab': [('fez', '"FOI VOCÊ QUE FEZ?"', 'red'), ('pedi', '"EU PEDI."', 'teal')]})],
 [('pc_desk', 'ID', 'push', [f'{C}@a:point/happy^0,0'], {'opts': ROOM, 'lab': [('automático', 'O QUE VOCÊ COLOCARIA NO AUTOMÁTICO?', 'yellow'), ('Comenta', 'COMENTA AQUI', 'yellow'), ('Shorts', 'UMA REALIDADE NOVA TODO DIA', 'teal')]})],
]

# padrões por cenário: TV da cozinha, lousa da sala de aula e TV da sala sem nada do vídeo da Lua
DEF = {'k_': {'tv': 'NOVELA DAS 8'}, 'c_': {'board': 'GEOGRAFIA\nREGIÕES DO BRASIL'}, 'lr_': {'screen': 'NOVELA'}}
for _seg in SEG.values():
    for _para in _seg:
        for _i, _sh in enumerate(_para):
            for _pfx, _d in DEF.items():
                if _sh[0].startswith(_pfx):
                    _ex = dict(_sh[4]); _ex['opts'] = dict(_d, **(_ex.get('opts') or {})); _para[_i] = (_sh[0], _sh[1], _sh[2], _sh[3], _ex)

# planos com gente na rua/sala de aula: câmera mais perto
for _seg in SEG.values():
    for _para in _seg:
        for _i, _sh in enumerate(_para):
            if _sh[3] and _sh[0] in ('st_wide', 'c_desks'):
                _para[_i] = ({'st_wide': 'st_crowd', 'c_desks': 'c_close'}[_sh[0]],) + tuple(_sh[1:])

ORDER = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5']
CARDS = {'c1': ('CAPÍTULO 1', 'O DIA EM QUE VOLTOU'), 'c2': ('CAPÍTULO 2', 'A LOJA DE BOLO DA DONA CIDA'),
         'c3': ('CAPÍTULO 3', 'O TÉCNICO DO BAIRRO'), 'c4': ('CAPÍTULO 4', 'A CIDADE INTEIRA')}
