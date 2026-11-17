"""Short v2: E se o Brasil virasse o país mais capitalista do mundo? (ref: youtube 9eKPD8sUjYk) — 2D flat + 6C/6D/14A."""
import os, sys, json, re
PROJ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PROJ, '..', '..', 'engine', 'py'))
import flat2d as F
from flat2d import char, esc

WORDS = json.load(open(os.path.join(PROJ, 'audio', 'words.json')))['short']
END = WORDS[-1][2]
TOTAL = round(END + 0.62, 2)
C = F.Comp(PROJ, TOTAL)
norm = lambda w: re.sub(r'[^\wà-ú-]', '', w.lower())
NW = [norm(w) for w, _, _ in WORDS]

def T(word, n=1, exact=True, after=0.0):
    opts = word.lower().split('|'); k = 0
    for w, a, b in WORDS:
        if a < after: continue
        ww = norm(w)
        if any((ww == o) if exact else ww.startswith(o) for o in opts):
            k += 1
            if k == n: return a
    raise KeyError(word)

# ---------- legenda (números em algarismos)
PATS = [(['em', 'presa'], 'EMPRESA'), (['às', 'capitais'], 'AS CAPITAIS'), (['dez'], '10'), (['seis'], '6'), (['cinco'], '5'), (['três'], '3')]
cap = []; i = 0
while i < len(WORDS):
    for pat, rep in PATS:
        if NW[i:i + len(pat)] == pat:
            cap.append((rep, WORDS[i][1], WORDS[i + len(pat) - 1][2])); i += len(pat); break
    else:
        cap.append((WORDS[i][0].strip(',.'), WORDS[i][1], WORDS[i][2])); i += 1
cap[-1] = ('BRASIL?', cap[-1][1], cap[-1][2])
KEYS = ['BRASIL', 'CAPITALISTA', 'LEILÃO', 'IMPOSTO', 'CAIO', 'CELULAR', 'METADE', 'EMPRESA', '10', 'SALÁRIO', 'MÍNIMO', 'SAÚDE', 'CARTÃO',
        'RUA', 'PRAIA', 'CATRACA', '6', 'DINHEIRO', 'BILIONÁRIO', 'ÔNIBUS', 'LUCRO', '5', '3', 'EMPREGOS', 'PEDÁGIO', 'ECONOMIAS', 'TREM-BALA',
        'RICOS', 'MURO', 'GRADE', 'VOCÊ', 'VIVERIA', 'BRASIL?']

def pillv(label, value, size=96, col=None):
    c = f';color:{col}' if col else ''
    return f'<div class="pillv" style="position:relative;left:auto;translate:none;font-size:{size}px{c}"><span class="l">{esc(label)}</span>{esc(value)}</div>'
def centered(): C.els[-1] = C.els[-1].replace('style="', 'style="left:540px;translate:-50% 0;', 1)
def tilt(text, size=74, col='#ffd23f'): return f'<div class="tilt" style="font-size:{size}px;color:{col}">{esc(text)}</div>'
def card(icon, title, sub=''): return f'<div class="card">{F.ICONS[icon]}<div>{esc(title)}</div><div class="s">{esc(sub)}</div></div>'
def pos(svg, x, y): return f'<div style="position:absolute;left:{x}px;top:{y}px">{svg}</div>'
def tchip(t): return tilt(t, 92)   # marcador de tempo que abre cada salto

TAG = ('<div style="position:relative;background:#ffd23f;border:9px solid #24203a;border-radius:24px 70px 70px 24px;padding:18px 70px 22px 110px;'
       'font-size:110px;color:#24203a;white-space:nowrap;box-shadow:0 12px 0 rgba(20,16,28,.35)">'
       '<div style="position:absolute;left:34px;top:50%;margin-top:-24px;width:48px;height:48px;border-radius:50%;background:#f4f0e8;border:8px solid #24203a"></div>R$ ???</div>')

def gancho(t0, t1, first=True):
    cid = 'c1' if first else 'c99'
    C.scene(t0, t1, F.bg_sunburst(), [char(cid, 'caio', 540, 1900, 1.15, 'up', 'surprise')], cam='push', amount=0.06, whoosh=not first,
            trans='cut' if first else 'dissolve', dust=10, dust_col='#fff8d0', vig=0.35)
    C.life(cid, t0, t1)
    tg = C.add(TAG, 0.0 if first else t0, t1, x=None, y=180, rot=-6, anim='pop' if first else 'none', sound='cash' if first else None); centered()
    C.tween(f'#{tg}', {'rotation': -6}, {'rotation': 4, 'duration': 0.5, 'repeat': max(1, int((t1 - t0) / 0.5)), 'yoyo': True, 'ease': 'sine.inOut'}, t0 + 0.35)

# ===== 1 GANCHO
t_dia = T('primeiro') - 0.25
gancho(0, t_dia)
C.add(tilt('BRASIL À VENDA?', 92), T('capitalista', exact=False), t_dia, x=None, y=560, rot=-6, sound='pop'); centered()
C.flash(T('capitalista', exact=False) - 0.03); C.sfx(0.0, 'riser', 0.5); C.sfx(T('capitalista', exact=False), 'coin', 0.6)

# ===== 2 ACONTECIMENTOS
# Dia 1 — leilão e fim do imposto
t0, t1 = t_dia, T('primeira') - 0.25
C.scene(t0, t1, F.bg_room('auction', 'day'), [char('lo2', 'prof', 790, 1600, 0.82, 'point', 'happy', flip=True),
                                             char('c2', 'caio', 290, 1880, 0.98, 'hang', 'surprise')],
        cam='push', amount=0.07, amb='room', beams=F.beams_svg(540, -100, 3, '#fff2c0', 0, 0.28, 230, 2000, 120), dust=16)
C.life('lo2', t0, t1, bob=5); C.life('c2', t0, t1)
C.add(tchip('DIA 1'), t0 + 0.1, t1, x=70, y=400, rot=-6, sound='pop', vol=0.5)
gv = C.add(F.gavel_svg(1.0), T('venda'), t1, x=720, y=420, anim='pop', rot=-20, sound=None)
C.tween(f'#{gv}', {'rotation': -40}, {'rotation': 10, 'duration': 0.18, 'ease': 'power3.in', 'repeat': 1, 'yoyo': True}, T('leilão'))
C.sfx(T('leilão') + 0.16, 'slam', 0.7)
C.add('<div class="stamp" style="font-size:110px">VENDIDO!</div>', T('leilão') + 0.2, T('imposto') - 0.1, x=None, y=600, anim='stamp', rot=-8, sound='thud', vol=0.5); centered()
C.add(card('x', 'IMPOSTO DE RENDA', 'ACABOU'), T('imposto'), t1, x=405, y=440, rot=4, sound='ting')

# Semana 1 — celular, empresa, salário mínimo
t0, t1 = T('primeira') - 0.25, T('depois') - 0.25
C.scene(t0, t1, F.bg_room('bedroom', 'day'), [char('c3', 'caio', 400, 1900, 1.05, 'phone', 'happy', props=('phone',))], cam='push', amount=0.08, amb='room',
        beams=F.beams_svg(780, 330, 2, '#fff6c8', 28, 0.3, 140, 1800, 120), dust=14, fg=F.fg_plants('right'))
C.life('c3', t0, t1)
C.add(tchip('SEMANA 1'), t0 + 0.25, t1, x=70, y=120, rot=-6, sound='pop', vol=0.5)
C.add(pillv('CELULAR IMPORTADO', '−50%', 104), T('metade'), t1, x=None, y=260, sound='cash'); centered()
C.add(card('check', 'EMPRESA', 'ABERTA EM 10 MIN'), T('empresa'), t1, x=80, y=520, rot=-6, sound='ting')
C.sfx(T('empresa') + 0.3, 'typing', 0.35)
C.add(card('x', 'SALÁRIO MÍNIMO', 'DEIXOU DE EXISTIR'), T('salário'), t1, x=720, y=1000, rot=6, sound='buzz', vol=0.45)

# Mês 1 — saúde no cartão
t0, t1 = T('depois') - 0.25, T('rua') - 0.3
C.scene(t0, t1, F.bg_navy(), [char('c4', 'caio', 540, 2200, 1.6, 'hang', 'worried', headonly=True)], cam='push', amount=0.08, dust=8, dust_col='#9fb8ff', vig=0.45)
C.life('c4', t0, t1)
C.add(tchip('MÊS 1'), t0 + 0.25, t1, x=70, y=110, rot=-6, sound='pop', vol=0.5)
C.add(card('x', 'POSTO DE SAÚDE', 'VIROU EMPRESA'), T('posto'), t1, x=90, y=300, rot=-5, sound='pop')
C.add(F.card_svg(1.0, declined=False), T('cartão'), t1, x=600, y=330, anim='right', rot=8, sound='click')
C.add(pillv('CONSULTA', 'SÓ NO CRÉDITO', 84), T('cartão') + 0.15, t1, x=None, y=640, sound='coin'); centered()

# Mês 1 — rua comprada e praia com catraca
t0, t1 = T('rua') - 0.3, T('seis|6') - 0.5
C.scene(t0, t1, F.bg_city('day', seed=9) + F.haze_svg('#ffffff', 0.22, 800) + pos(F.tollgate_svg(1.2, 'gate5'), 160, 1050),
        [char('c5', 'caio', 270, 1880, 0.95, 'shrug', 'worried')], cam='panR', amb='street', dust=6)
C.life('c5', t0, t1)
C.tween('#gate5', {'rotation': -70}, {'rotation': 0, 'duration': 0.45, 'ease': 'back.out(1.8)'}, T('comprada') - 0.05)
C.add(pillv('RUA DO BAIRRO', 'COMPRADA', 96, '#ffd23f'), T('comprada'), t1, x=None, y=230, sound='cash'); centered()
C.add(card('x', 'PRAIA', 'COM CATRACA'), T('praia'), t1, x=700, y=520, rot=6, sound='buzz', vol=0.4)
C.sfx(T('catraca'), 'click', 0.6)

# 6 meses — dinheiro do mundo, prédios de vidro, ônibus parado
t0, t1 = T('seis|6') - 0.5, T('cinco|5') - 0.45
C.scene(t0, t1, F.bg_city('sunset', seed=4) + F.glass_towers_svg() + F.haze_svg('#ffd0a0', 0.25, 900),
        [char('p6', 'p1', 820, 1760, 0.7, 'hang', 'worried', flip=True), char('c6', 'caio', 290, 1900, 1.0, 'hip', 'worried')],
        cam='panL', amb='street', beams=F.beams_svg(300, 700, 2, '#ffe0a0', -50, 0.22, 200, 1700, 160), dust=10)
C.life('c6', t0, t1); C.life('p6', t0, t1, bob=4)
C.add(tchip('6 MESES'), t0 + 0.4, t1, x=70, y=110, rot=-6, sound='pop', vol=0.5)
for k in range(7):
    b = C.add('<div style="width:150px;height:76px;background:#7fd6a0;border:6px solid #24203a;border-radius:10px;font-size:34px;color:#24203a;display:flex;align-items:center;justify-content:center">$$</div>',
              T('dinheiro') + 0.12 * k, t1, x=60 + 140 * k, y=-120, anim='none', sound='cash' if k == 0 else None, vol=0.6)
    C.tween(f'#{b}', {'y': 0, 'rotation': -20 + 7 * k}, {'y': 1500, 'rotation': 25 - 5 * k, 'duration': 2.4, 'ease': 'power1.in'}, T('dinheiro') + 0.12 * k)
C.add(pillv('+1 BILIONÁRIO', 'POR SEMANA', 90, '#3ee08a'), T('bilionário'), t1, x=None, y=300, sound='coin'); centered()
C.add(F.busstop_svg(0.7), T('ônibus'), t1, x=540, y=1180, anim='up', sound='buzz', vol=0.45)
C.add(tilt('SEM LUCRO, SEM ÔNIBUS', 58, '#fff'), T('lucro'), t1, x=100, y=1000, rot=-5, sound='wrong', vol=0.4)

# 5 anos — três empregos
t0, t1 = T('cinco|5') - 0.45, T('anos', 2) - 0.5
C.scene(t0, t1, F.bg_room('office', 'night'), [char('c7', 'caio', 540, 1900, 1.1, 'temple', 'sleepy')],
        cam='push', amount=0.07, amb='room', beams=F.beams_svg(780, 260, 2, '#9fd0ff', 20, 0.22, 160, 1700, 120), dust=10, dust_col='#cfe4ff', vig=0.6)
C.life('c7', t0, t1, blink=False, bob=3)
C.add(tchip('5 ANOS'), t0 + 0.4, t1, x=70, y=110, rot=-6, sound='pop', vol=0.5)
for k in range(3):
    C.add(f'<div style="background:#fff;border:6px solid #24203a;border-radius:18px;padding:10px 26px;font-size:46px;color:#24203a;box-shadow:0 8px 0 rgba(20,16,28,.3)">EMPREGO {k + 1}</div>',
          T('três|3') + 0.18 * k, t1, x=60 + 330 * k, y=262 + 30 * (k % 2), rot=-6 + 6 * k, sound='pop' if k == 0 else 'click', vol=0.5)
for k, (w, lab) in enumerate((('hospital', 'HOSPITAL'), ('escola', 'ESCOLA'), ('pedágio', 'PEDÁGIO DA RUA'))):
    C.add(f'<div class="lp" style="position:relative;left:auto;width:760px"><span class="n">{lab}</span>−R$</div>', T(w), t1, x=160, y=430 + 115 * k, anim='left', sound='coin', vol=0.5)

# FATO MAIS FORTE — 10 anos: economia, trem-bala, cidade particular atrás do muro
t10 = T('anos', 2) - 0.5
C.silence(t10, 0.7)
t0, t1 = t10, T('você') - 0.25
C.scene(t0, t1, F.bg_city('night', seed=12) + F.glass_towers_svg(5) + F.wall_svg(''),
        [char('c8', 'caio', 550, 2200, 1.3, 'hang', 'worried')], cam='drama', rot=3, amount=0.07, shake=(T('muro'),), amb='street',
        trans='cut', fg=F.fg_bars('#2a2840', xs=(40, 210, 860, 1030), rails=(300,)), dust=12, dust_col='#ffe9a0', vig=0.6)
C.sfx(t0, 'thunder', 0.5)
C.life('c8', t0, t1, bob=3)
C.add(tchip('10 ANOS'), t0 + 0.05, t1, x=70, y=110, rot=-6, sound='pop', vol=0.5)
C.add(pillv('ECONOMIA', 'ENTRE AS MAIORES', 84, '#3ee08a'), T('economias'), t1, x=None, y=260, sound='ting'); centered()
tr = C.add(F.train_svg(0.9), T('trem', exact=False) - 0.1, t1, x=1100, y=560, anim='none', sound='whoosh', vol=0.7)
C.tween(f'#{tr}', {'x': 0}, {'x': -2600, 'duration': 2.2, 'ease': 'power1.inOut'}, T('trem', exact=False) - 0.1)
C.add(pillv('OS MAIS RICOS', 'CIDADE PARTICULAR', 74, '#ffd23f'), T('ricos'), t1, x=None, y=450, sound='pop', vol=0.6); centered()
C.add(tilt('O RESTO, PELA GRADE', 66, '#fff'), T('grade'), t1, x=200, y=1110, rot=4, sound='thud', vol=0.5)
C.sfx(T('muro') - 1.2, 'riser', 0.45)

# ===== 3 PERGUNTA FINAL — boca sincronizada palavra por palavra
t0, t1 = T('você') - 0.25, END + 0.08
C.scene(t0, t1, F.bg_sunburst(), [char('c9', 'caio', 540, 2330, 1.75, 'point', 'neutral')], cam='push', amount=0.05, dust=10, dust_col='#fff8d0', vig=0.35)
C.life('c9', t0, t1)
C.mouth('c9', [w for w in WORDS if w[1] >= T('você') - 0.05])
C.add(tilt('E VOCÊ?', 120), T('você'), t1, x=280, y=150, rot=-7, sound='sparkle')
C.add('<div class="bubble" style="position:relative;left:0;translate:none;font-size:56px"><div class="tag" style="background:#4a9be8">CAIO</div>VIVERIA NESSE BRASIL?<div class="tail"></div></div>',
      T('viveria'), t1, x=100, y=380, anim='up', sound='pop')
gancho(t1, TOTAL, first=False)   # loop

C.caption(cap, KEYS, y=830)
MUSIC = [(0, T('cinco|5') - 0.45, 'epic'), (T('cinco|5') - 0.45, TOTAL, 'tension')]
F.main(C, MUSIC)
