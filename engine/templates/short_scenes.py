import sys; sys.path.insert(0, 'REPO/engine/py')
from presets import *
FORMAT = 'short'; GAP = 0; TAIL = 0.6; MOOD = 'night'; STING = 'Só'
KEYWORDS = ['lua', 'santos', 'mar', 'embora', 'quarenta', 'metros', 'ilha', 'lobisomens', 'desempregados', 'eixo', 'terra', 'piao', 'verao', 'inverno', 'falta']
BUBBLES = [('Agora dá pra ir a pé pra ilha!', 'BETO', '#e04848', 'Agora', 'ilha'), ('E você, ia sentir falta da Lua?', 'SEU DITO', '#2f9e95', 'você', 'Lua')]
CARDS = {}
ORDER = ['short']
SEG = {'short': [
 [('b_sea', 'N', 'push', [], {'opts': MOON, 'flash': 'sumisse', 'lab': [('Santos', 'SANTOS · SP', 'white')]}), ('b_sea', 'N', 'pull', [], {'lab': [('embora', 'O MAR FOI EMBORA', 'yellow')]})],
 [('b_dito', 'N', 'push', ['dito@d:hang/neutral^0.3,-1'], {'lab': [('Onze', '23:40', 'white'), ('Dito', 'SEU DITO', 'teal', 'PESCADOR')]}), ('b_sky', 'N', 'tiltU', [], {'fx': ['twinkle']}), ('b_sea', 'N', 'pull', [], {'opts': LOW, 'lab': [('quarenta', '-40 m', 'red')]})],
 [('b_canoe', 'N', 'push', ['dito@d:temple/surprise'], {'opts': dict(LOW, canoeTilt=0.45), 'shake': 'deitado'}), ('b_dito', 'N', 'orbit', ['dito@d:hang/worried', 'beto!@b:pointL/laugh'], {'opts': LOW, 'speaker': 'beto'}), ('b_mureta', 'N', 'push', ['lobo@a:hold/sad+sign'], {})],
 [('sp_close', 'X', 'drama', [], {'opts': {'axisGlow': True}, 'lab': [('eixo', 'EIXO DA TERRA', 'yellow')]}), ('sp_earth', 'X', 'orbit', [], {'opts': {'tilt': 34}, 'shake': 'bambear', 'lab': [('bambear', 'BAMBEANDO!', 'red')]}), ('b_sea', 'D', 'push', ['dito@s1:hang/hot+sunglasses+sweat'], {'lab': [('verão', 'MANHÃ 35°C', 'orange')]}), ('b_sea', 'O', 'push', ['dito@s1:cross/cold+scarf+shiver'], {'opts': SNOW, 'fx': ['snow'], 'lab': [('inverno', 'TARDE -5°C', 'blue')]})],
 [('b_dito', 'N', 'push', ['dito@d:point/talk'], {'speaker': 'dito'})],
]}
