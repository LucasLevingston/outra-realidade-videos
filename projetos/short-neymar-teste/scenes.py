import sys; sys.path.insert(0, 'REPO/engine/py')
from presets import *
FORMAT = 'short'; GAP = 0; TAIL = 0.6; MOOD = 'day'; STING = 'Só'
OVERLAYS = False   # rótulos, balões, legenda e flashes vêm da camada HyperFrames (hyperframes.py)
KEYWORDS = ['neymar', 'santos', 'copa', 'mundo', 'vila', 'belmiro', 'franca', '90', '10', 'cinco', 'franceses', 'chao', 'goal', 'gol', 'brasil', 'padaria', 'graca', 'faliu', 'microfone', 'aceitou']
BUBBLES = [('Agora eu quero jogar no gol.', 'CAMISA 10', '#2f9e4a', 'Agora', 'gol'), ('E você, colocava ele no gol?', 'CAMISA 10', '#2f9e4a', '>você', 'gol')]
CARDS = {}
ORDER = ['short']
BRA = {'crowd': ['#ffd23f', '#2f9e4a', '#ffffff', '#3a8dde', '#ffd23f', '#2f9e4a']}
SAN = {'crowd': ['#ffffff', '#1d1d2b', '#ffffff', '#1d1d2b', '#ffd23f']}
PAD = {'stall': [2.6, -7.4], 'stallText': 'PÃO\nDE GRAÇA', 'shop': 'PADARIA DO ZÉ', 'shopX': 3}
SEG = {'short': [
 [('f_mid', 'N', 'push', ['craque@p:both_up/laugh'], {'opts': BRA, 'lab': [('Santos', 'CAMISA 10', 'yellow', 'DE VOLTA AO SANTOS')]})],
 [('f_crowd', 'N', 'pull', [], {'opts': SAN, 'lab': [('Vila', 'VILA BELMIRO', 'white', 'NINGUÉM DORME')]})],
 [('f_high', 'N', 'push', [], {'opts': dict(BRA, score='BRA 0 × 0 FRA'), 'lab': [('Final', 'FINAL DA COPA', 'yellow'), ('noventa', "90'", 'red')]}),
  ('f_mid', 'N', 'orbit', ['craque@p:point/proud', 'frances@d1:hang/surprise', 'frances!@d2:temple/worried', 'frances@d3:hang/surprise'], {'opts': dict(BRA, ball=[4.5, 4.3]), 'shake': 'chão', 'lab': [('cinco', '5 FRANCESES NO CHÃO', 'orange')]})],
 [('f_goal', 'N', 'drama', ['craque@p:both_up/laugh', 'goleiro@gk:hang/sad'], {'opts': dict(BRA, ball=[0.4, 53.2]), 'flash': 'Gol', 'shake': 'Gol', 'lab': [('Gol', 'GOOOL!', 'yellow'), ('Brasil', 'BRA 1 × 0 FRA', 'green')]})],
 [('st_stall', 'D', 'push', ['ze@a:hold/happy'], {'opts': PAD, 'lab': [('semana', '7 DIAS DE PÃO GRÁTIS', 'orange'), ('faliu', 'CAIXA: R$ 0', 'red')]})],
 [('lk_wide', 'ID', 'push', ['craque@a:up/talk'], {'opts': {'banner': ' '}, 'speaker': 'craque', 'flash': 'vestiário', 'lab': [('vestiário', 'VESTIÁRIO', 'white')]})],
 [('lk_wide', 'ID', 'drama', ['tecnico@b:thumb/proud', 'craque@c:both_up/laugh'], {'opts': {'banner': ' '}, 'shake': 'aceitou', 'lab': [('aceitou', 'NOVO GOLEIRO', 'yellow')]})],
 [('f_mid', 'N', 'push', ['craque@p:point/talk'], {'opts': BRA, 'speaker': 'craque'})],
]}
