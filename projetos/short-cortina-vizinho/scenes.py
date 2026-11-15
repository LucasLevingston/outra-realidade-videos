import sys; sys.path.insert(0, 'REPO/engine/py')
from presets import *
FORMAT = 'short'; GAP = 0; TAIL = 0.6; MOOD = 'day'; STING = None
OVERLAYS = False
KEYWORDS = ['banho', 'vizinho', 'curioso', 'espiar', 'panos', 'luz', 'argolinhas', 'cano', 'ventinho', 'vao', 'enorme',
            'largos', 'melhor', 'noite', 'silhueta', 'forro', 'grosso', 'raio', 'cortina', 'blecaute', 'invencao']
BUBBLES = [('Qual invenção a gente explica agora?', 'VOCÊ', '#2f9e95', 'Comenta', '>agora')]
CARDS = {}
ORDER = ['short']
VIZ = 'ze@v:hold/happy^0,0'
SEG = {'short': [
 # 1 GANCHO
 [('bt_wide', 'ID', 'push', ['voce@a:cheek/surprise^-1,0+wet', 'ze@v:hold/happy^0,0'], {'opts': {'curtain': 'none'}, 'lab': [('banho', 'NO BANHO...', 'white')]}),
  ('bt_win', 'ID', 'drama', ['ze@v:point/laugh^0,0'], {'at': 'vizinho', 'opts': {'curtain': 'none'}, 'flash': 'espiar', 'lab': [('vizinho', 'VIZINHO CURIOSO', 'yellow')]})],
 # 2 ACONTECIMENTOS
 [('bt_win', 'ID', 'push', ['voce@a:hold/proud^-1,0'], {'opts': {'curtain': 'nailed'}, 'lab': [('prega', 'PANO PREGADO', 'green')]}),
  ('bt_wide', 'ID', 'orbit', ['voce@a:temple/sad^-1,0'], {'at': 'Só', 'opts': {'curtain': 'nailed'}, 'lab': [('luz', 'SEM LUZ', 'red')]})],
 [('bt_win', 'ID', 'panR', ['voce@a:point/happy^-1,0'], {'opts': {'curtain': 'rings'}, 'lab': [('argolinhas', 'ARGOLAS + CANO', 'orange')]})],
 [('bt_win', 'ID', 'push', ['voce@a:cheek/worried^-1,0+wet', 'ze@v:wave/laugh^0,0'], {'opts': {'curtain': 'gap'}, 'shake': 'enorme', 'lab': [('vão', 'VÃO ENORME', 'red')]}),
  ('bt_caio', 'ID', 'drama', ['voce@a:temple/worried^-1,0+wet'], {'at': 'lá', 'opts': {'curtain': 'gap'}, 'lab': [('espiando', 'DE NOVO?!', 'yellow')]})],
 [('bt_wide', 'ID', 'pull', ['voce@a:thumb/happy^0,0+wet'], {'opts': {'curtain': 'wide'}, 'lab': [('largos', 'PANOS SOBREPOSTOS', 'green')]})],
 [('bt_out', 'N', 'push', ['ze@z:point/laugh^-1,-0.3'], {'opts': {'curtain': 'silhouette'}, 'lab': [('noite', 'À NOITE', 'white'), ('silhueta', 'SILHUETA!', 'red')]})],
 [('bt_win', 'I', 'push', ['voce@a:hold/proud^-1,0'], {'opts': {'curtain': 'blackout'}, 'lab': [('forro', 'FORRO GROSSO', 'orange')]}),
  ('bt_wide', 'I', 'pull', ['voce@a:cross/proud^0,0'], {'at': 'nem', 'opts': {'curtain': 'blackout'}, 'lab': [('raio', 'ZERO LUZ', 'white')]})],
 [('bt_out', 'N', 'orbit', ['ze@z:temple/sad^-1,-0.3'], {'opts': {'curtain': 'blackout'}, 'lab': [('Agora', 'NÃO VÊ MAIS NADA', 'green')]}),
  ('bt_caio', 'I', 'drama', ['voce@a:both_up/laugh^0,0'], {'at': 'Você', 'opts': {'curtain': 'blackout'}, 'shake': 'blecaute', 'flash': 'blecaute', 'lab': [('cortina', 'CORTINA BLECAUTE', 'yellow')]})],
 # 3 PERGUNTA FINAL (volta ao enquadramento do gancho = loop)
 [('bt_wide', 'ID', 'push', ['voce@a:point/talk^0,0'], {'opts': {'curtain': 'blackout'}, 'speaker': 'voce'})],
]}
HF = [dict(kind='stamp', at='blecaute', until='>blecaute', text='INVENTADO!')]
