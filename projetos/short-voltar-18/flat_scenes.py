"""Short: E se você pudesse voltar aos 18 anos com tudo que sabe hoje? — modo 2D flat (engine/py/flat2d.py)."""
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

def T(word, n=1, exact=True, after=0.0):
    """início da n-ésima ocorrência da palavra (depois de `after` s)"""
    k = 0
    for w, a, b in WORDS:
        if a < after: continue
        ww = norm(w)
        if (ww == word.lower()) if exact else ww.startswith(word.lower()):
            k += 1
            if k == n: return a
    raise KeyError(word)

# ---------- legenda (números em algarismos)
PATS = [(['trinta', 'e', 'cinco'], '35'), (['cinquenta', 'reais'], 'R$ 50'), (['dez', 'centavos'], 'R$ 0,10'), (['50', 'reais'], 'R$ 50'), (['10', 'centavos'], 'R$ 0,10'),
        (['dezoito'], '18'), (['dez'], '10'), (['cinco'], '5')]
cap = []; i = 0
while i < len(WORDS):
    for pat, rep in PATS:
        seg = [norm(w) for w, _, _ in WORDS[i:i + len(pat)]]
        if seg == pat:
            cap.append((rep, WORDS[i][1], WORDS[i + len(pat) - 1][2])); i += len(pat); break
    else:
        cap.append((WORDS[i][0].strip(',.'), WORDS[i][1], WORDS[i][2])); i += 1
KEYS = ['18', '35', 'BETO', 'ESPINHA', 'TAMPINHA', 'PROVA', '10', 'PROFESSOR', '5', 'DESCULPA', 'IRMÃO', 'BRIGA', 'MESADA', 'R$ 50', 'LATA',
        'MOEDA', 'R$ 0,10', 'FAMÍLIA', 'RIU', 'AVÓ', 'VOCÊ', 'PRIMEIRO?', 'MUDAR']

def phone(inner, scale=0.7, header=None, sub=None, hcol='#2fbf71'):
    hd = f'<div class="hd" style="background:{hcol}">{esc(header)}<small>{esc(sub)}</small></div>' if header else ''
    return (f'<div style="width:{620 * scale:.0f}px;height:{1000 * scale:.0f}px"><div class="ph" style="transform:scale({scale});transform-origin:0 0">'
            f'<div class="scr">{hd}{inner}</div></div></div>')

def pillv(label, value, size=96):
    return f'<div class="pillv" style="position:relative;left:auto;translate:none;font-size:{size}px"><span class="l">{esc(label)}</span>{esc(value)}</div>'

def centered(): C.els[-1] = C.els[-1].replace('style="', 'style="left:540px;translate:-50% 0;', 1)

def tilt(text, size=74, col='#ffd23f'):
    return f'<div class="tilt" style="font-size:{size}px;color:{col}">{esc(text)}</div>'

def card(icon, title, sub=''):
    return f'<div class="card">{F.ICONS[icon]}<div>{esc(title)}</div><div class="s">{esc(sub)}</div></div>'

def bigclock(t):
    return f'<div style="background:#22213a;color:#fff;border:8px solid #f4f0e8;border-radius:36px;font-size:150px;line-height:1.25;padding:0 50px;box-shadow:0 10px 0 rgba(20,16,28,.3)">{t}</div>'

AGE = ('<div class="pillv" style="position:relative;left:auto;translate:none;font-size:120px"><span class="l">IDADE</span>'
       '<span style="color:#c9c9e6;text-decoration:line-through;text-decoration-thickness:10px;text-decoration-color:#e8483a">35</span> → 18</div>')

def gancho(t0, t1, first=True):
    cid = 'b1' if first else 'b99'
    sid = C.scene(t0, t1, F.bg_sunburst(), [char(cid, 'beto', 540, 1900, 1.15, 'up', 'surprise', props=('pimple',))], cam='push', amount=0.06, whoosh=not first)
    C.life(cid, t0, t1)
    C.add(AGE, t0 if not first else 0.0, t1, x=None, y=200, anim='pop' if first else 'none', sound='pop' if first else None); centered()
    return sid

# 1 GANCHO
t_beto = T('beto') - 0.12
gancho(0, t_beto)
C.add(tilt('18 DE NOVO?', 96), T('18'), t_beto, x=150, y=560, rot=-8, sound='pop')
C.flash(T('18') - 0.03); C.sfx(0.0, 'riser', 0.5); C.sfx(T('18'), 'glitch', 0.4)

# 2 ACONTECIMENTOS — volta no tempo
t0, t1 = t_beto, T('acordou') - 0.05
C.scene(t0, t1, F.bg_room('living', 'night'), [char('b2', 'beto', 540, 1560, 1.0, 'hang', 'sleepy')], cam='push', amb='room')
C.life('b2', t0, t1, blink=False, bob=4)
C.add(tilt('Zzz', 90, '#fff'), t0 + 0.1, t1, x=700, y=560, rot=-6, sound=None)
C.add(pillv('IDADE', '35', 110), T('35'), t1, x=None, y=230, sound='pop'); centered()

t0, t1 = T('acordou') - 0.05, T('espinha') - 0.4
C.scene(t0, t1, F.bg_room('bedroom', 'dawn'), [char('b3', 'beto', 540, 1880, 1.05, 'up', 'surprise', props=('pimple',))], cam='push', amount=0.08, amb='room')
C.life('b3', t0, t1)
C.flash(t0 + 0.02); C.sfx(t0 + 0.02, 'glitch', 0.5)
C.add(pillv('IDADE', '18', 110), T('18', 2), t1, x=None, y=200, sound='ting'); centered()
C.add(tilt('QUARTO DE ADOLESCENTE', 56, '#fff'), T('adolescente', exact=False), t1, x=110, y=480, rot=-5, sound='pop', vol=0.5)

t0, t1 = t1, T('segunda', exact=False) - 0.05
C.scene(t0, t1, F.bg_room('bedroom', 'dawn'), [char('b4', 'beto', 540, 2200, 1.6, 'hang', 'worried', props=('pimple',), headonly=True)], cam='push', amount=0.03, amb='room')
C.life('b4', t0, t1)
C.add('<div class="ring" style="width:170px;height:170px"></div>', T('espinha'), t1, x=518, y=1082, anim='pop', sound='ting', vol=0.7)
C.add(tilt('ESPINHA!', 70), T('espinha'), t1, x=640, y=980, rot=-8, sound=None)
C.add(F.flipphone(0.85, '#7fe0c0', '12:00'), T('celular'), t1, x=60, y=180, anim='left', rot=-8, sound='click')
C.add(tilt('TAMPINHA', 66, '#fff'), T('tampinha'), t1, x=330, y=420, rot=6, sound='pop', vol=0.5)

# segunda-feira: prova
t0, t1 = T('segunda', exact=False) - 0.05, T('professor') - 0.05
C.scene(t0, t1, F.bg_room('classroom', 'day'), [char('pr5', 'prof', 840, 1560, 0.78, 'point', 'neutral', flip=True),
                                               char('b5', 'beto', 330, 1760, 0.95, 'up', 'happy', props=('pimple',))], cam='panR', amb='room')
C.life('b5', t0, t1); C.life('pr5', t0, t1)
C.add(tilt('SEGUNDA-FEIRA', 66, '#fff'), t0 + 0.05, t1, x=90, y=120, rot=-5, sound='pop', vol=0.5)
sheet = ('<div style="width:420px;height:520px;background:#fff;border:7px solid #24203a;border-radius:18px;box-shadow:0 10px 0 rgba(20,16,28,.3);position:relative;color:#24203a">'
         '<div style="padding:26px 30px 0;font-size:34px">PROVA · MATEMÁTICA</div>'
         + ''.join(f'<div style="margin:18px 30px 0;display:flex;align-items:center;gap:14px;font-size:30px"><div style="width:44px;height:44px">{F.ICONS["check"].replace("width=\"90\" height=\"90\"", "width=\"44\" height=\"44\"")}</div>QUESTÃO {k}</div>' for k in range(1, 6))
         + '</div>')
C.add(sheet, T('respostas'), t1, x=600, y=110, rot=4, anim='up', sound='click')
C.sfx(T('respostas') + 0.3, 'typing', 0.4)
C.add('<div class="stamp" style="font-size:150px">10</div>', T('10'), t1, x=700, y=330, anim='stamp', rot=-12, sound='thud', vol=0.7)
C.sfx(T('10') + 0.18, 'ting', 0.6)

t0, t1 = T('professor') - 0.05, T('primeira') - 0.3
C.scene(t0, t1, F.bg_room('classroom', 'day'), [char('pr6', 'prof', 540, 2300, 1.6, 'hang', 'surprise', headonly=True)], cam='push', amount=0.1, amb='room')
C.life('pr6', t0, t1, blink=False)
C.add(bigclock('5 MIN'), T('cinco', after=T('professor')), t1, x=None, y=160, sound='tick'); centered()
for k in range(1, 8): C.sfx(T('cinco', after=T('professor')) + 0.45 * k, 'tick', 0.35)
C.add(tilt('...', 140, '#fff'), T('nada'), t1, x=700, y=560, rot=0, sound='pop', vol=0.4)

# primeira semana: irmão
t0, t1 = T('primeira') - 0.3, T('começou', exact=False) - 0.05
C.scene(t0, t1, F.bg_room('living', 'day'), [char('i7', 'irmao', 780, 1820, 0.95, 'hip', 'surprise', flip=True),
                                            char('b7', 'beto', 330, 1880, 1.0, 'shrug', 'worried', props=('pimple',))], cam='push', amb='room')
C.life('b7', t0, t1); C.life('i7', t0, t1)
C.add(tilt('SEMANA 1', 80), t0 + 0.05, t1, x=90, y=140, rot=-6, sound='pop', vol=0.5)
C.add(f'<div style="display:flex;align-items:center;gap:14px;background:#fff;border:6px solid #24203a;border-radius:60px;padding:8px 34px 8px 12px;font-size:46px;color:#24203a">{F.ICONS["check"]}DESCULPA, IRMÃO</div>',
      T('desculpa'), t1, x=170, y=330, rot=-3, sound='ting')
C.add(card('x', 'BRIGA', 'AINDA NÃO ACONTECEU'), T('briga'), t1, x=640, y=520, rot=6, sound='buzz', vol=0.4)

# mesada na lata
t0, t1 = T('começou', exact=False) - 0.05, T('fim') - 0.3
C.scene(t0, t1, F.bg_room('bedroom', 'day'), [char('b8', 'beto', 330, 1880, 1.0, 'cheer', 'happy', props=('pimple',))], cam='panL', amb='room')
C.life('b8', t0, t1)
C.add(pillv('MESADA', 'R$ 50', 100), T('mesada'), t1, x=None, y=200, sound='coin'); centered()
lid = C.add(F.can_svg(1.0, 'MESADA'), T('lata'), t1, x=620, y=1250, anim='up', sound='coin')
for k in range(3):
    C.add('<div class="money">+R$ 50</div>', T('50') + 0.15 * k, t1, x=250 + 260 * k, y=1150 - 60 * (k % 2), anim='float', sound='coin' if k == 0 else None, vol=0.6)

# moeda digital
t0, t1 = T('fim') - 0.3, T('família', exact=False) - 0.1
C.scene(t0, t1, F.bg_navy(), [], cam='push', amount=0.1)
fm = C.add(tilt('FIM DO MÊS', 76), t0 + 0.05, t1, x=90, y=120, rot=-6, sound='pop', vol=0.5)
C.tween(f'#{fm}', {'scale': 1}, {'scale': 1.08, 'duration': 0.45, 'repeat': int((t1 - t0) / 0.45), 'yoyo': True, 'ease': 'sine.inOut'}, t0 + 0.4)
chart = ('<svg viewBox="0 0 520 300" width="520" height="300" style="position:absolute;left:30px;top:420px">'
         '<polyline points="0,280 70,270 140,275 210,262 280,268 350,250 420,255 500,240" fill="none" stroke="#2fa86a" stroke-width="10" stroke-linejoin="round" stroke-linecap="round"/></svg>')
cot = ('<div style="position:absolute;left:0;right:0;top:170px;text-align:center;color:#24203a"><div style="font-size:40px;color:#6b6890">COTAÇÃO</div>'
       '<div style="font-size:110px;color:#24203a;line-height:1.05">R$ 0,10</div></div>')
mph = C.add(phone(cot + chart, 0.72, 'MOEDA DIGITAL', 'comprar', '#7b5aa6'), T('moeda'), t1, x=317, y=330, anim='up', sound='click')
C.tween(f'#{mph}', {'y': 0, 'rotation': 0}, {'y': -18, 'rotation': 2, 'duration': 0.5, 'repeat': int((t1 - T('moeda')) / 0.5), 'yoyo': True, 'ease': 'sine.inOut'}, T('moeda') + 0.32)
C.add('<div class="ring" style="width:420px;height:200px"></div>', T('centavos'), t1, x=330, y=520, anim='pop', sound='ting', vol=0.8)
C.add(pillv('COLOCOU TUDO', 'R$ 50', 80), T('colocou'), t1, x=None, y=1170, sound='cash'); centered()

# 3 FATO MAIS FORTE — jantar de domingo
t0, t1 = T('família', exact=False) - 0.1, T('menos') - 0.05
C.scene(t0, t1, F.bg_room('kitchen', 'night'), [char('pa9', 'pai', 230, 1640, 0.85, 'shrug', 'laugh'), char('ma9', 'mae', 850, 1640, 0.85, 'hip', 'laugh', flip=True),
                                               char('i9', 'irmao', 540, 1560, 0.75, 'cheer', 'laugh'),
                                               char('b9', 'beto', 540, 2000, 1.05, 'hang', 'worried', props=('pimple',))], cam='drama', rot=3, amount=0.06, shake=(T('riu'),), amb='room')
for c in ('pa9', 'ma9', 'i9', 'b9'): C.life(c, t0, t1, bob=9 if c != 'b9' else 4)
C.add(tilt('JANTAR DE DOMINGO', 60, '#fff'), t0 + 0.05, t1, x=90, y=120, rot=-5, sound='pop', vol=0.5)
C.add(tilt('HAHAHA', 130), T('riu'), t1, x=200, y=330, rot=-8, sound='crowd', vol=0.7)
C.add(tilt('HAHA', 90, '#fff'), T('riu') + 0.3, t1, x=640, y=560, rot=8, sound=None)
C.sfx(T('riu') - 1.2, 'riser', 0.5)

# avó
t0, t1 = T('menos') - 0.05, T('você', n=2) - 0.25
C.scene(t0, t1, F.bg_room('kitchen', 'night'), [char('v10', 'vo', 540, 1900, 1.1, 'phone2', 'happy')], cam='push', amb='room')
C.life('v10', t0, t1)
bill = ('<div style="width:420px;height:200px;background:#7fd6a0;border:7px solid #24203a;border-radius:18px;display:flex;align-items:center;justify-content:center;'
        'font-size:84px;color:#24203a;box-shadow:0 10px 0 rgba(20,16,28,.3)">R$ 50</div>')
C.add(bill, T('entrou'), t1, x=330, y=1380, anim='up', rot=-6, sound='cash')
C.add(pillv('+R$ 50', 'DA VÓ', 100), T('mais'), t1, x=None, y=200, sound='coin'); centered()
C.add(tilt('MENOS A AVÓ', 66, '#fff'), T('menos'), t1, x=150, y=560, rot=-6, sound='pop', vol=0.5)

# 4 PERGUNTA FINAL
t0, t1 = T('você', n=2) - 0.25, END + 0.08
C.scene(t0, t1, F.bg_sunburst(), [char('b11', 'beto', 540, 2330, 1.75, 'point', 'neutral', props=('pimple',))], cam='push', amount=0.05)
C.life('b11', t0, t1, talk=[(T('você', n=2), END)])
C.add(tilt('E VOCÊ?', 120), T('você', n=2), t1, x=280, y=150, rot=-7, sound='sparkle')
C.add('<div class="bubble" style="position:relative;left:0;translate:none;font-size:56px"><div class="tag" style="background:#2fbf71">BETO</div>IA MUDAR O QUÊ PRIMEIRO?<div class="tail"></div></div>',
      T('mudar'), t1, x=100, y=380, anim='up', sound='pop')
# loop: volta ao enquadramento do gancho
gancho(t1, TOTAL, first=False)

C.caption(cap, KEYS, y=830)
MUSIC = [(0, T('família', exact=False) - 0.1, 'retro'), (T('família', exact=False) - 0.1, T('você', n=2) - 0.25, 'tension'), (T('você', n=2) - 0.25, TOTAL, 'retro')]
F.main(C, MUSIC)
