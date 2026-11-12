import sys; sys.path.insert(0, 'REPO/engine/py')
from presets import *
FORMAT = 'short'; GAP = 0; TAIL = 0.6; MOOD = 'night'; STING = 'Só'
OVERLAYS = False
KEYWORDS = ['simulacao', 'caio', 'cafe', 'ar', 'congelou', 'grito', 'erro', '404', 'realidade', 'observatorio', 'lia', 'unico', 'sabia', 'saber']
BUBBLES = [('ERRO 404: realidade não encontrada', 'SISTEMA', '#e04848', 'Erro', 'encontrada'),
           ('Calma. Você é o único que ainda não sabia.', 'DOUTORA LIA', '#7b5aa6', 'calma', 'sabia'),
           ('E você, ia querer saber?', 'CAIO', '#3a8dde', '>você', 'saber')]
CARDS = {}
ORDER = ['short']
TOM = {'stall': [2.6, -7.4], 'stallText': 'TOMATE\nR$ 4,99'}
SEG = {'short': [
 [('b_room', 'ID', 'push', ['caio20@a:temple/surprise^0.4,-0.4'], {'flash': 'simulação', 'lab': [('simulação', 'SIMULAÇÃO?', 'yellow')]})],
 [('k_wide', 'ID', 'push', ['caio20@t1:hold/surprise+mug'], {'lab': [('Segunda', 'SEG · 07:00', 'white'), ('parou', 'O CAFÉ PAROU NO AR', 'orange')]})],
 [('st_stall', 'D', 'orbit', ['caio20@a:both_up/surprise', 'p4@5.0,-8.5:hang/neutral'], {'opts': TOM, 'lab': [('congelou', 'TUDO PAUSADO', 'blue')]})],
 [('st_stall', 'D', 'drama', ['caio20@a:temple/worried'], {'opts': TOM, 'flash': 'Erro', 'shake': 'Erro'})],
 [('l_desk', 'N', 'push', ['lia@4.0,-1.0:cross/neutral', 'caio20@5.0,0.0:hang/worried'], {'lab': [('observatório', 'OBSERVATÓRIO', 'white')]}),
  ('l_desk', 'N', 'drama', ['lia@4.0,-1.0:point/talk'], {'speaker': 'lia', 'lab': [('único', 'O ÚNICO', 'red', 'QUE NÃO SABIA')]})],
 [('b_room', 'ID', 'push', ['caio20@a:point/talk'], {'speaker': 'caio20'})],
]}
