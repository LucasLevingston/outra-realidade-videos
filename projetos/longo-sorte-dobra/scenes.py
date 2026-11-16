# Plano de cenas — L26 "E se sua sorte DOBRASSE a cada dia?" (vídeo longo 16:9)
# Cada parágrafo do roteiro -> lista de planos: (preset, luz, movimento, [personagens], extras)
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'engine', 'py'))
from presets import *

FORMAT = 'long'
GAP = 2.5; TAIL = 5.0
MOOD = None
# trilha por capítulo (clima do que acontece nele)
SEGMOOD = {'c0': 'mystery', 'c1': 'comedy', 'c2': 'day', 'c3': 'comedy', 'c4': 'day', 'c5': 'tender'}

PRE.update({
 'br_wide': ('bedroom', [0.8, 1.6, 2.4], [-1.4, 0.9, -2.8], 52, {'a': (-0.6, -1.6), 'b': (0.9, -2.0)}),
 'br_bed':  ('bedroom', [0.3, 1.35, 1.0], [-1.8, 0.85, -2.6], 42, {'a': (-1.2, -1.7)}),
 'st_crowd':  ('street', [1, 1.6, -1], [10, 1.4, -6], 44, {'a': (6, -6.5), 'b': (6.6, -5.4), 'c': (7.2, -4.3), 'd': (7.6, -7.2), 'e': (5.4, -3.6)}),
 'st_rain': ('street', [2, 1.6, 0], [9, 1.5, -7], 46, {'a': (6.5, -6.4), 'b': (8.2, -6.0)}),
})

C = 'caio20'
BANCA = {'stall': [2, -8], 'stallText': 'BANCA DO\nSEU DITO'}

SEG = {}
SEG['c0'] = [
 [('st_rain', 'D', 'push', [f'{C}@a:both_up/surprise^0,-0.6'], {'lab': [('sorte', 'SORTE x2 POR DIA', 'yellow'), ('chuva', 'A CHUVA DESVIA', 'teal')]})],
 [('st_wide', 'O', 'panR', [f'{C}@a:hang/sad', 'p1@c:hold/neutral', 'p6@d:cross/neutral'], {'fx': ['rain'], 'lab': [('Caio', 'CAIO', 'teal', '19 ANOS · SANTOS'), ('azarado', 'O MAIS AZARADO DA CIDADE', 'red')]})],
 [('st_rain', 'S', 'drama', [f'{C}@a:hang/surprise+wet'], {'fx': ['rain'], 'flash': 'raio', 'shake': 'raio', 'lab': [('raio', 'RAIO NO GUARDA-CHUVA', 'yellow'), ('nem', 'SEM GUARDA-CHUVA', 'red')]})],
 [('br_wide', 'W', 'push', [f'{C}@a:temple/sleepy'], {'lab': [('comum', 'PESSOA COMUM: 50', 'white'), ('acordou', 'SORTE DO CAIO: 1', 'red')]})],
 [('br_bed', 'W', 'pull', [f'{C}@a:hang/neutral^0,-0.5'], {'lab': [('dobra', 'DOBRA TODO DIA', 'yellow'), ('zero', 'DIA 0', 'white')]})],
]
SEG['c1'] = [
 [('br_wide', 'W', 'push', [f'{C}@a:hang/sleepy', 'cida@b:point/talk'], {'lab': [('Segunda', 'SEGUNDA · 06:00', 'white'), ('pilha', 'A PILHA TAVA NO CONTROLE', 'orange'), ('Dona', 'SORTE: 1', 'red')]})],
 [('br_bed', 'W', 'drama', [f'{C}@a:temple/shout'], {'shake': 'chão', 'lab': [('celular', 'CELULAR NO CHÃO', 'red'), ('mapa', 'TELA = MAPA DE METRÔ', 'white')]})],
 [('k_wide', 'ID', 'push', [f'{C}@fl:hang/sad', 'cida@st:hold/talk+mug'], {'speaker': 'cida', 'lab': [('manteiga', 'MANTEIGA PRA BAIXO', 'red'), ('guarda', '"LEVA GUARDA-CHUVA"', 'purple'), ('sol', 'SOL DE RACHAR', 'yellow')]})],
 [('st_wide', 'D', 'panR', [f'{C}@e:reach/shout', 'p3@b:wave/happy'], {'lab': [('ônibus', 'O ÔNIBUS FOI EMBORA', 'red'), ('dois', '2 QUARTEIRÕES CORRENDO', 'white'), ('acenou', 'O MOTORISTA ACENOU', 'orange')]})],
 [('st_rain', 'O', 'drama', [f'{C}@a:hang/sad+wet', 'p5@b:hip/laugh'], {'fx': ['rain'], 'lab': [('seca', 'A RUA INTEIRA SECA', 'yellow'), ('nuvem', 'UMA NUVEM SÓ PRA ELE', 'blue')]})],
 [('of_wide', 'ID', 'push', [f'{C}@b:hang/worried+wet'], {'opts': {'screen': 'ENTREVISTAS'}, 'lab': [('oito', '1ª EM 8 MESES', 'white'), ('dez', '10 MIN ATRASADO', 'red'), ('chiclete', 'CHICLETE NO TÊNIS', 'purple')]})],
 [('of_desk', 'ID', 'push', ['p2@v:hold/neutral+paper', f'{C}!@b:hang/worried+wet'], {'opts': {'screen': 'ERRO'}, 'lab': [('travou', 'O PC TRAVOU', 'red')]}),
  ('of_desk', 'ID', 'hold', ['p2@v:hold/talk+paper', f'{C}!@b:hang/sad'], {'opts': {'screen': 'ERRO'}, 'at': 'gente', 'speaker': 'p2', 'lab': [('liga', '"A GENTE TE LIGA"', 'purple'), ('ninguém', 'NINGUÉM LIGA', 'white')]})],
 [('st_stall', 'D', 'push', ['dito@a:hold/neutral+paper', f'{C}!@b:hang/worried'], {'opts': BANCA, 'lab': [('Dito', 'SEU DITO', 'teal', 'DONO DA BANCA'), ('trigésima', '30ª SEMANA', 'white'), ('vizinho', 'ERROU POR 1', 'red')]})],
 [('st_stall', 'D', 'push', ['dito@a:hold/sad', f'{C}!@b:hold/neutral'], {'opts': BANCA, 'speaker': 'dito', 'lab': [('pirulito', 'PIRULITO DE CONSOLO', 'orange'), ('vencido', 'VENCIDO', 'red')]})],
 [('st_wide', 'G', 'panL', [f'{C}@a:hold/sad', 'p4@c:cross/neutral'], {'opts': {'shop': 'PADARIA', 'shopX': 9}, 'lab': [('chinelo', 'CHINELO ARREBENTOU', 'red'), ('pé', 'NUM PÉ SÓ', 'white'), ('sacola', 'SACOLA RASGANDO', 'orange')]})],
 [('br_wide', 'N', 'push', [f'{C}@a:phone/sad+phone'], {'fx': ['night'], 'lab': [('Lara', 'LARA', 'purple', 'AMIGA DESDE OS 7'), ('normal', '"NORMAL"', 'white'), ('errado', '= DEU TUDO ERRADO', 'red')]})],
 [('br_bed', 'N', 'push', [f'{C}@a:hang/sad^0,-0.8'], {'fx': ['night'], 'lab': [('meia', 'MEIA MOLHADA', 'blue'), ('pediu', '"SÓ UM DIA"', 'yellow')]})],
 [('br_bed', 'N', 'drama', [f'{C}@a:hang/sleepy'], {'fx': ['night'], 'flash': 'piscou', 'lab': [('piscou', 'SORTE: 1 VIROU 2', 'yellow'), ('amanhã', 'E AMANHÃ?', 'teal')]})],
]
SEG['c2'] = [
 [('k_wide', 'W', 'push', [f'{C}@fl:hold/happy', 'cida@st:hold/neutral+mug'], {'lab': [('Terça', 'DIA 1 · SORTE: 2', 'yellow'), ('gaveta', 'A PILHA NA GAVETA', 'white'), ('lado', 'PÃO DE LADO = VITÓRIA', 'teal')]})],
 [('st_wide', 'D', 'push', [f'{C}@e:reach/neutral'], {'lab': [('minuto', 'PERDEU POR 1 MIN', 'orange'), ('três', '(NÃO POR 3)', 'white')]})],
 [('st_wide', 'D', 'push', [f'{C}@a:hold/surprise^0,0.4', 'p3!@b:hang/happy'], {'lab': [('Quarta', 'DIA 2 · SORTE: 4', 'yellow'), ('moeda', 'R$ 1 NA CALÇADA', 'teal'), ('sapato', 'O ÔNIBUS ESPEROU', 'white')]})],
 [('k_wide', 'ID', 'push', ['cida@st:belly/laugh', f'{C}!@fl:hold/proud'], {'lab': [('troféu', 'MOEDA = TROFÉU', 'yellow'), ('feijão', 'QUASE CAI O FEIJÃO', 'orange')]})],
 [('st_stall', 'D', 'push', ['dito@a:hold/happy+paper', f'{C}!@b:thumb/happy'], {'opts': BANCA, 'lab': [('Quinta', 'DIA 3 · SORTE: 8', 'yellow'), ('verde', 'SINAL VERDE', 'teal'), ('troco', 'TROCO CERTO', 'white')]})],
 [('st_wide', 'D', 'push', [f'{C}@a:hold/neutral', 'p6@b:hold/surprise'], {'opts': {'shop': 'PADARIA', 'shopX': 9}, 'lab': [('caixa', 'TROCO A MAIS', 'orange'), ('devolveu', 'ELE DEVOLVEU', 'teal')]})],
 [('br_wide', 'ID', 'push', [f'{C}@a:phone/surprise+phone'], {'lab': [('Sexta', 'DIA 4 · SORTE: 16', 'yellow'), ('nove', '09:00 · RH LIGANDO', 'white'), ('ficha', 'A FICHA DELE', 'teal')]})],
 [('br_wide', 'ID', 'drama', [f'{C}@a:both_up/shout+phone'], {'shake': 'gritou', 'lab': [('segunda', '"COMEÇA SEGUNDA"', 'purple'), ('vizinho', 'O VIZINHO BATEU NA PAREDE', 'red')]})],
 [('k_wide', 'G', 'push', ['cida@t1:hold/squint+mug', f'{C}!@t2:hang/happy'], {'lab': [('diferente', '"VOCÊ TÁ DIFERENTE"', 'red'), ('cabelo', 'ATÉ O CABELO', 'yellow')]})],
 [('st_stall', 'D', 'drama', ['dito@a:both_up/happy', f'{C}!@b:both_up/laugh'], {'opts': dict(BANCA, stallText='GANHADOR:\nCAIO!'), 'flash': 'ganhou', 'lab': [('Sábado', 'DIA 5 · SORTE: 32', 'yellow'), ('cesta', 'CESTA DE CAFÉ', 'orange'), ('primeira', '1º PRÊMIO DA VIDA', 'teal')]})],
 [('k_wide', 'ID', 'push', [f'{C}@fl:hold/laugh', 'cida!@st:temple/surprise'], {'lab': [('igreja', 'RIFA DA IGREJA', 'white'), ('bingo', 'BINGO DO PRÉDIO', 'white'), ('loja', 'LOJA DE LIQUIDIFICADOR', 'yellow')]})],
 [('k_wide', 'ID', 'push', ['lu@t1:hold/talk', f'{C}!@t2:hang/happy'], {'speaker': 'lu', 'lab': [('dinheiro', '"CARA DE QUEM ACHOU DINHEIRO"', 'purple')]}),
  ('k_wide', 'ID', 'push', [f'{C}@t2:thumb/proud', 'lu!@t1:hold/laugh'], {'at': 'Eu', 'lab': [('três', '"3 VEZES"', 'teal')]})],
 [('br_wide', 'G', 'push', [f'{C}@a:hang/happy'], {'lab': [('menos', '32 < 50', 'red'), ('melhor', 'A MELHOR SEMANA', 'yellow')]})],
 [('br_bed', 'N', 'drama', [f'{C}@a:hang/surprise^0,-0.6'], {'fx': ['night'], 'flash': 'cem', 'lab': [('cem', 'E ACIMA DE 100?', 'yellow')]})],
]
SEG['c3'] = [
 [('br_wide', 'W', 'push', [f'{C}@a:both_up/happy'], {'lab': [('Domingo', 'DIA 6 · SORTE: 64', 'yellow'), ('normal', 'ACIMA DO NORMAL', 'teal'), ('cinco', 'ACORDOU ANTES DO DESPERTADOR', 'white')]})],
 [('of_cool', 'ID', 'push', [f'{C}@a:hold/surprise+mug', 'p1!@b:hang/surprise'], {'lab': [('emprego', '1º DIA NO EMPREGO', 'white'), ('máquina', 'MÁQUINA DE CAFÉ VOLTOU', 'teal'), ('dois', 'QUEBRADA HÁ 2 ANOS', 'red')]})],
 [('of_desk', 'ID', 'push', [f'{C}@v:point/happy', 'beto!@b:temple/surprise'], {'opts': {'screen': 'SENHA: ****'}, 'lab': [('Beto', 'BETO', 'orange', 'O CHEFE'), ('primeira', 'SENHA CERTA DE PRIMEIRA', 'teal')]}),
  ('of_desk', 'ID', 'hold', ['beto@b:point/shout', f'{C}!@v:hang/surprise'], {'opts': {'screen': 'ACESSO OK'}, 'at': 'Moleque', 'speaker': 'beto', 'lab': [('hacker', '"VOCÊ É HACKER?"', 'orange')]})],
 [('st_wide', 'D', 'push', [f'{C}@e:hang/proud', 'p1@a:hang/surprise'], {'lab': [('sete', 'DIA 7 · SORTE: 128', 'yellow'), ('exato', 'O ÔNIBUS NO SEGUNDO EXATO', 'teal')]})],
 [('st_wide', 'S', 'push', [f'{C}@e:hang/happy', 'p2@a:hold/happy', 'p4@b:hold/happy', 'p6@c:hold/happy', 'p5@d:hold/happy'], {'fx': ['rain'], 'lab': [('corredor', 'CORREDOR SECO', 'yellow'), ('formiga', 'FILA DE FORMIGA', 'white')]})],
 [('st_stall', 'D', 'push', [f'{C}@a:hold/neutral+paper', 'p1!@b:both_up/happy'], {'lab': [('carteira', 'CARTEIRA + R$ 500', 'white'), ('gerente', 'ERA O GERENTE DO BANCO', 'orange'), ('dívida', 'DÍVIDA PERDOADA', 'teal')]})],
 [('f_crowd', 'D', 'panR', [], {'opts': {'score': 'BAIRRO 0 × 0'}, 'lab': [('Quarta', 'DIA 8 · SORTE: 256', 'yellow'), ('meio', '1 ANO E MEIO SEM VENCER', 'red')]})],
 [('f_goal', 'D', 'push', ['craque@p:point/happy', 'goleiro@gk:both_up/surprise'], {'opts': {'score': 'BAIRRO 6 × 0', 'ball': True}, 'lab': [('gol', 'GOL', 'yellow'), ('contra', 'ATÉ GOL CONTRA', 'orange')]}),
  ('f_wide', 'D', 'drama', [], {'opts': {'score': 'BAIRRO 6 × 0'}, 'at': 'terminou', 'shake': 'seis', 'lab': [('seis', '6 A 0', 'yellow'), ('nome', '"CAIO! CAIO!"', 'teal')]})],
 [('k_wide', 'ID', 'drama', ['cida@st:both_up/laugh+tears', f'{C}!@fl:hang/surprise'], {'opts': {'tv': 'RECEITA DE BOLO'}, 'shake': 'levantou', 'lab': [('solava', 'O BOLO QUE SEMPRE SOLAVA', 'white'), ('forno', 'LEVANTOU A PORTA DO FORNO', 'yellow')]})],
 [('k_wide', 'ID', 'push', ['lu@t1:hold/happy', f'{C}!@t2:hold/happy'], {'lab': [('bicicleta', 'PNEU FURADO', 'red'), ('cheio', 'ENCHEU SOZINHO', 'teal')]})],
 [('s_wide', 'ID', 'push', ['anchor@l:hold/talk', f'{C}!@r:hang/surprise'], {'opts': {'screen': 'O RAPAZ MAIS\nSORTUDO DO BRASIL'}, 'lab': [('nove', 'DIA 9 · SORTE: 512', 'yellow'), ('TV', 'TV DE SANTOS', 'red')]})],
 [('st_stall', 'D', 'push', ['dito@a:point/happy', f'{C}!@b:hang/neutral'], {'opts': dict(BANCA, stallText='SENTAR DO LADO\nDO CAIO: R$ 5/MIN'), 'lab': [('fila', 'FILA PRA ENCOSTAR', 'white'), ('cinco', 'R$ 5 O MINUTO', 'yellow')]})],
 [('st_wide', 'D', 'push', ['p3@a:both_up/laugh', 'p6@b:phone/happy+phone', 'p5@c:hold/surprise'], {'lab': [('dinheiro', 'DINHEIRO NO BOLSO', 'teal'), ('crush', 'MENSAGEM DO CRUSH', 'purple'), ('adiada', 'PROVA ADIADA', 'yellow')]})],
 [('l_desk', 'I', 'push', ['lia@a:hold/squint', f'{C}!@b:hang/neutral'], {'opts': {'screen': 'CARA: 100/100'}, 'lab': [('Lia', 'DOUTORA LIA', 'purple', 'OBSERVATÓRIO'), ('cem', '100 CARAS SEGUIDAS', 'yellow')]})],
 [('l_desk', 'I', 'drama', ['lia@a:temple/surprise+notebook'], {'opts': {'screen': 'CARA: 100/100'}, 'speaker': 'lia', 'lab': [('existe', '"ISSO NÃO EXISTE"', 'purple'), ('vazando', 'A SORTE TÁ VAZANDO', 'teal'), ('onde', 'ATÉ ONDE VAI?', 'yellow')]})],
]
SEG['c4'] = [
 [('l_scope', 'I', 'push', ['lia@a:hold/neutral+notebook'], {'opts': {'screen': 'SORTE: 1024'}, 'lab': [('dez', 'DIA 10 · SORTE: 1.024', 'yellow'), ('métrica', 'FITA · PRANCHETA · MOEDAS', 'white')]})],
 [('l_desk', 'I', 'push', ['lia@a:point/talk', f'{C}!@b:hang/surprise'], {'opts': {'screen': '10 m: DIA BOM\n20 m: ÓTIMO'}, 'lab': [('dez', '10 m = DIA BOM', 'teal'), ('vinte', '20 m = DIA ÓTIMO', 'teal'), ('raio', 'O RAIO DOBRA', 'yellow')]})],
 [('st_stall', 'D', 'drama', ['dito@a:both_up/surprise', f'{C}!@b:hold/surprise+paper'], {'opts': dict(BANCA, stallText='LOTERIA\n6 ACERTOS!'), 'flash': 'acertou', 'lab': [('onze', 'DIA 11 · SORTE: 2.048', 'yellow'), ('seis', '6 NÚMEROS', 'teal'), ('ninguém', 'SÓ ELE', 'white')]})],
 [('k_wide', 'D', 'push', ['cida@st:both_up/laugh+tears', f'{C}!@fl:thumb/happy'], {'lab': [('casa', 'CASA PRA DONA CIDA', 'yellow'), ('forno', 'FORNO NOVO', 'white')]}),
  ('st_stall', 'N', 'push', ['dito@a:both_up/happy'], {'opts': dict(BANCA, stallText='BANCA DO\nSEU DITO ★'), 'at': 'segunda', 'lab': [('letreiro', 'LETREIRO ACESO', 'orange')]})],
 [('st_down', 'D', 'push', [], {'lab': [('doze', 'DIA 12 · SORTE: 4.096', 'yellow'), ('semáforo', 'SEMÁFORO SEMPRE VERDE', 'teal')]}),
  ('b_sea', 'D', 'pull', [], {'at': 'praia', 'lab': [('limpinha', 'PRAIA LIMPINHA', 'blue')]})],
 [('h_boats', 'D', 'push', ['p1@a:both_up/happy', 'p5@b:hold/laugh'], {'lab': [('cheio', 'BARCO CHEIO', 'yellow'), ('banana', 'PEIXE A PREÇO DE BANANA', 'orange')]})],
 [('of_wide', 'ID', 'push', ['beto@b:temple/worried', f'{C}!@v:hang/neutral'], {'opts': {'screen': 'VENDAS +5.000%', 'live': True}, 'lab': [('casa', 'TRABALHA DE CASA', 'white'), ('semana', '1 SEMANA = 1 ANO', 'yellow'), ('sistema', 'O SISTEMA CAIU', 'red')]})],
 [('of_desk', 'ID', 'push', ['beto@b:both_up/shout', f'{C}!@v:hang/surprise'], {'opts': {'screen': 'VENDAS +5.000%', 'live': True}, 'speaker': 'beto', 'lab': [('Fica', '"FICA EM CASA, MOLEQUE!"', 'orange'), ('aumento', '+ AUMENTO', 'teal')]})],
 [('lr_wide', 'ID', 'push', [f'{C}@v:phone/surprise+phone'], {'opts': {'screen': 'PROPOSTAS'}, 'lab': [('treze', 'DIA 13 · SORTE: 8.192', 'yellow'), ('voo', 'VOO GRÁTIS PRA VIDA', 'blue'), ('atrasava', 'AVIÃO NUNCA ATRASA', 'white')]})],
 [('s_wide', 'ID', 'push', ['anchor@l:hold/talk'], {'opts': {'screen': 'ESPECIAL:\nOS LIQUIDIFICADORES'}, 'lab': [('contrato', 'CONTRATO: SÓ SENTAR NO BANCO', 'teal'), ('meia', 'REPORTAGEM DE 30 MIN', 'red')]})],
 [('st_wide', 'D', 'pull', ['p1@a:hold/happy+paper', 'p2@b:hold/neutral+photo', 'p3@c:hold/neutral+paper', 'p4@d:hang/neutral', 'p6@e:hold/happy'], {'lab': [('volta', 'FILA DÁ A VOLTA NO QUARTEIRÃO', 'yellow'), ('cachorro', 'FOTO DO CACHORRO', 'white'), ('currículo', 'CURRÍCULO', 'white')]})],
 [('st_wide', 'D', 'push', ['lia@e:hold/squint+notebook'], {'lab': [('binóculo', 'BINÓCULO + PRANCHETA', 'purple'), ('plantas', 'AS PLANTAS CRESCEM', 'teal')]})],
 [('b_canoe', 'G', 'push', [f'{C}@d:hang/happy', 'lu!@b:hang/happy'], {'opts': {'noUmbrella': True}, 'lab': [('quatorze', 'DIA 14 · SORTE: 16.384', 'yellow'), ('Lara', 'SÓ OS DOIS', 'purple')]})],
 [('b_sky', 'N', 'push', [], {'opts': {'night': True}, 'fx': ['twinkle'], 'lab': [('estrela', 'UMA ESTRELA CADENTE', 'white'), ('chuva', 'UMA CHUVA DELAS', 'yellow')]}),
  ('b_orla', 'N', 'pull', ['p2@m:phone/surprise+phone', 'p5@m2:hang/surprise', 'p3@k:hang/surprise'], {'opts': {'night': True}, 'fx': ['twinkle'], 'at': 'orla', 'lab': [('orla', 'A ORLA INTEIRA PAROU', 'teal')]})],
 [('b_canoe', 'N', 'push', ['lu@b:hold/laugh', f'{C}!@d:hang/happy'], {'opts': {'night': True}, 'fx': ['twinkle'], 'speaker': 'lu', 'lab': [('pedido', '"FAZ UM PEDIDO"', 'purple')]}),
  ('b_canoe', 'N', 'drama', [f'{C}@d:hang/sleepy^0,-0.4'], {'opts': {'night': True}, 'fx': ['twinkle'], 'at': 'você', 'lab': [('pedir', 'E VOCÊ?', 'yellow')]})],
]
SEG['c5'] = [
 [('lr_door', 'W', 'push', ['cida@h:hold/happy', f'{C}!@b:hang/happy'], {'opts': {'door': 'lit'}, 'lab': [('quinze', 'DIA 15 · NÃO CABE MAIS', 'yellow'), ('fila', 'A BANCA TEM FILA', 'orange'), ('guarda', 'GUARDA-CHUVA NA PORTA', 'blue')]})],
 [('br_wide', 'D', 'push', [f'{C}@a:point/happy^0,0'], {'lab': [('arriscar', 'O QUE VOCÊ IA ARRISCAR?', 'yellow'), ('Comenta', 'COMENTA AQUI', 'yellow'), ('Shorts', 'UMA REALIDADE NOVA TODO DIA', 'teal')]})],
]

# efeitos ligados à fala
SFX = [('despertador', 'tick'), ('chão', 'thud'), ('manteiga', 'wrong'), ('acenou', 'boing'), ('chover', 'thunder'),
       ('chiclete', 'boing'), ('travou', 'buzz'), ('vizinho', 'wrong'), ('pirulito', 'pop'), ('arrebentou', 'boing'),
       ('mensagem', 'notif'), ('piscou', 'sparkle'), ('moeda#2', 'ting'), ('troco', 'cash'), ('tocou#3', 'notif'),
       ('gritou', 'cheer', 0.6), ('cesta', 'sparkle'), ('liquidificador', 'ting'), ('liquidificador#2', 'ting'),
       ('máquina', 'ting'), ('senha', 'typing'), ('hacker', 'boing'), ('carteira', 'cash'), ('gol', 'cheer'),
       ('torcida', 'crowd'), ('forno', 'slam'), ('pneu', 'pop'), ('câmera', 'click'), ('crush', 'notif'),
       ('moeda#4', 'ting'), ('existe', 'riser'), ('loteria', 'riser'), ('acertou#2', 'cash'), ('letreiro', 'sparkle'),
       ('semáforo', 'ting'), ('peixe', 'cheer', 0.5), ('aumento', 'cash'), ('telefone', 'notif'), ('liquidificadores', 'ting'),
       ('binóculo', 'click'), ('estrela', 'sparkle'), ('outra', 'sparkle'), ('pedido', 'chime'), ('Comenta', 'pop')]

# TV da cozinha e da sala sem nada de outros vídeos
DEF = {'k_': {'tv': 'NOVELA DAS 8'}, 'lr_': {'screen': 'BOM DIA, SANTOS'}}
for _seg in SEG.values():
    for _para in _seg:
        for _i, _sh in enumerate(_para):
            for _pfx, _d in DEF.items():
                if _sh[0].startswith(_pfx):
                    _ex = dict(_sh[4]); _ex['opts'] = dict(_d, **(_ex.get('opts') or {})); _para[_i] = (_sh[0], _sh[1], _sh[2], _sh[3], _ex)
# planos com gente na rua: câmera mais perto
for _seg in SEG.values():
    for _para in _seg:
        for _i, _sh in enumerate(_para):
            if _sh[3] and _sh[0] == 'st_wide':
                _para[_i] = ('st_crowd',) + tuple(_sh[1:])

ORDER = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5']
CARDS = {'c1': ('CAPÍTULO 1', 'DIA 0 · O CARA MAIS AZARADO DE SANTOS'), 'c2': ('CAPÍTULO 2', 'DIAS 1 A 5 · A SORTE ACORDA'),
         'c3': ('CAPÍTULO 3', 'DIAS 6 A 9 · ACIMA DE 100'), 'c4': ('CAPÍTULO 4', 'DIAS 10 A 14 · A SORTE TRANSBORDA')}
