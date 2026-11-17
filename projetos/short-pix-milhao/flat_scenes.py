"""Short: E se caísse um Pix de 1 milhão na sua conta hoje? — modo 2D flat (engine/py/flat2d.py)."""
import os, sys, json
PROJ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PROJ, '..', '..', 'engine', 'py'))
import flat2d as F
from flat2d import char, esc

WORDS = json.load(open(os.path.join(PROJ, 'audio', 'words.json')))['short']
END = WORDS[-1][2]
TOTAL = round(END + 0.62, 2)
C = F.Comp(PROJ, TOTAL)

# ---------- legenda (texto do roteiro com os tempos medidos; números em algarismos)
FIX = {6: ('R$ 1', 1.12, 1.3), 7: None, 13: ('ÀS', 3.18, 3.34), 14: ('7:04', 3.34, 4.0), 17: None, 28: ('R$ 32', 6.78, 7.32), 29: None,
       31: ('1 MILHÃO', 8.32, 8.82), 32: None, 33: None, 35: ('32', 8.92, 9.64), 36: None, 37: None, 94: ('À', 25.9, 26.14),
       112: ('CIDA', 29.98, 30.26), 121: ('SOBRINHO', 32.76, 33.16)}
cap = []
for i, (w, a, b) in enumerate(WORDS):
    if i in FIX:
        if FIX[i]: cap.append(FIX[i])
        continue
    cap.append((w.strip(',.'), a, b))
KEYS = ['PIX', 'MILHÃO', '1 MILHÃO', 'SALDO', 'VIROU', 'BANCO', '3', 'GERENTE', 'CARTÃO', 'PRETO', 'RESTAURANTE', 'MÃE', 'MOTO', '900', '47',
        'PARENTES', 'CIDA', '50', 'VOCÊ', 'QUIETO?', 'R$ 32', '32']

def T(word, n=1):
    """início da n-ésima ocorrência da palavra na narração"""
    k = 0
    for w, a, b in WORDS:
        if w.lower().strip(',.?').startswith(word.lower()):
            k += 1
            if k == n: return a
    raise KeyError(word)

def phone(inner, scale=0.7, header=None, sub=None, hcol='#2fbf71'):
    hd = f'<div class="hd" style="background:{hcol}">{esc(header)}<small>{esc(sub)}</small></div>' if header else ''
    return (f'<div style="width:{620 * scale:.0f}px;height:{1000 * scale:.0f}px"><div class="ph" style="transform:scale({scale});transform-origin:0 0">'
            f'<div class="scr">{hd}{inner}</div></div></div>')

def pillv(label, value, size=96):
    return f'<div class="pillv" style="position:relative;left:auto;translate:none;font-size:{size}px"><span class="l">{esc(label)}</span>{esc(value)}</div>'

def tilt(text, size=74, col='#ffd23f'):
    return f'<div class="tilt" style="font-size:{size}px;color:{col}">{esc(text)}</div>'

def card(icon, title, sub=''):
    return f'<div class="card">{F.ICONS[icon]}<div>{esc(title)}</div><div class="s">{esc(sub)}</div></div>'

def bigclock(t):
    return f'<div style="background:#22213a;color:#fff;border:8px solid #f4f0e8;border-radius:36px;font-size:150px;line-height:1.25;padding:0 50px;box-shadow:0 10px 0 rgba(20,16,28,.3)">{t}</div>'

def notif(title, value, app='BANCO · AGORA'):
    return f'<div class="notif"><div class="a">{esc(app)}</div><div class="t">{esc(title)}</div><div class="v">{esc(value)}</div></div>'

PIXNOTIF = (notif('Pix recebido', 'R$ 1.000.000,00') +
            '<div style="position:absolute;left:0;right:0;top:370px;text-align:center;color:#24203a">'
            '<div style="display:inline-block;width:190px;height:190px">' + F.ICONS['check'].replace('width="90" height="90"', 'width="190" height="190"') + '</div>'
            '<div style="font-size:44px;color:#6b6890;margin-top:16px">SALDO DISPONÍVEL</div>'
            '<div style="font-size:78px;color:#2fa86a;line-height:1.05">R$ 1.000.032</div></div>')

def gancho(t0, t1, first=True):
    sid = C.scene(t0, t1, F.bg_sunburst(), [char('c1' if first else 'c99', 'caio', 540, 1900, 1.15, 'up', 'surprise')], cam='push', amount=0.06, whoosh=not first)
    C.life('c1' if first else 'c99', t0, t1)
    C.add(phone(PIXNOTIF, 0.62),
          t0, t1, x=348, y=95, anim='pop' if first else 'none', sound='notif' if first else None)
    return sid

# 1 GANCHO
gancho(0, T('a'))
C.add(tilt('1 MILHÃO?', 92), T('milhão'), T('a'), x=70, y=600, rot=-8, sound='pop')
C.flash(T('milhão') - 0.03); C.sfx(0.0, 'riser', 0.5)

# 2 ACONTECIMENTOS — manhã
t0, t1 = T('a'), T('o') - 0.02  # "o celular"
C.scene(t0, t1, F.bg_room('bedroom', 'dawn'), [char('c2', 'caio', 360, 1700, 1.05, 'up', 'sleepy')], cam='push', amb='room')
C.life('c2', t0, t1)
C.add(bigclock('07:04'), T('7h04'), t1, x=300, y=180, sound='tick')

t0, t1 = t1, T('saldo')
C.scene(t0, t1, F.bg_room('bedroom', 'dawn'), [char('c3', 'caio', 540, 2430, 1.6, 'hang', 'surprise', headonly=True)], cam='push', amount=0.1, amb='room')
C.life('c3', t0, t1)
ph = C.add(phone(PIXNOTIF, 0.7), t0, t1, x=323, y=90, anim='up', sound=None)
C.tween(f'#{ph}', {'rotation': 0}, {'keyframes': [{'rotation': -4, 'duration': .05}, {'rotation': 4, 'duration': .05}] * 4 + [{'rotation': 0, 'duration': .05}]}, T('vibrou'))
C.sfx(T('vibrou'), 'notif', 0.9); C.sfx(T('vibrou') + 0.05, 'buzz', 0.25)

t0, t1 = T('saldo'), T('em')
C.scene(t0, t1, F.bg_navy(), [], cam='push', amount=0.12)
steps = ['R$ 32', 'R$ 1.032', 'R$ 18.032', 'R$ 96.032', 'R$ 247.032', 'R$ 512.032', 'R$ 788.032', 'R$ 963.032', 'R$ 1.000.032']
ts = [T('saldo') + 0.05] + [T('virou') + 0.13 * k for k in range(1, len(steps))]
for k, v in enumerate(steps):
    e = ts[k + 1] if k + 1 < len(steps) else t1
    i = C.add(pillv('SALDO', v), ts[k], e, x=None, y=300, anim='pop' if k == 0 else 'none', sound='pop' if k == 0 else 'tick', vol=0.5, cls='', origin='50% 50%')
    C.els[-1] = C.els[-1].replace('class="clip ov "', 'class="clip ov" ').replace('style="', 'style="left:540px;translate:-50% 0;', 1)
    if k == 0:
        C.tween(f'#{i}', {'scale': 1, 'rotation': 0}, {'scale': 1.08, 'rotation': 2, 'duration': 0.42, 'repeat': 3, 'yoyo': True, 'ease': 'sine.inOut'}, ts[0] + 0.35)
    if k == len(steps) - 1:
        C.tween(f'#{i}', {'scale': 1}, {'scale': 1.1, 'duration': 0.35, 'ease': 'back.out(2)'}, 9.06)
C.add('<div class="ring" style="width:940px;height:300px"></div>', 9.06, t1, x=70, y=262, anim='pop', sound='ting', vol=0.8)
C.add('<div class="money">+R$ 1.000.000</div>', T('virou'), t1, x=300, y=1180, anim='float', sound='cash', vol=0.8)

# banco ligando
t0, t1 = T('em'), 11.98
C.scene(t0, t1, F.bg_room('kitchen', 'day'), [char('c5', 'caio', 760, 1880, 1.05, 'phone', 'worried', props=('phone',))], cam='panL', amb='room')
C.life('c5', t0, t1)
C.add(tilt('10 MIN', 80), T('10'), t1, x=80, y=200, rot=-8)
for k, (w, x) in enumerate((('banco', 40), ('3', 400), ('vezes', 760))):
    C.add(card('phone', 'BANCO', f'{k + 1}ª LIGAÇÃO'), T(w), t1, x=x - 10 if k else x, y=330, rot=(-6, 3, -3)[k], sound='notif', vol=0.6)

# gerente
t0, t1 = 11.98, T('cartão')
C.scene(t0, t1, F.bg_room('kitchen', 'day'), [char('c6', 'caio', 540, 1900, 1.0, 'phone', 'happy', props=('phone',))], cam='push', amb='room')
C.life('c6', t0, t1)
C.add(phone('', 0.7, 'Rodrigo · Gerente', 'online agora'), t0, t1, x=323, y=70, anim='up', sound='click')
C.add('<div class="msg" style="white-space:nowrap"><small>RODRIGO</small>Bom dia, Caio!</div>', T('bom'), t1, x=355, y=270, sound='pop')
C.add(f'<div style="width:150px;height:150px">{F.ICONS["smile"]}</div>', T('carinha'), t1, x=580, y=380, sound='boing', vol=0.6)
C.add('<div class="msg" style="width:330px"><small>RODRIGO</small>Cartão preto pra você, sem anuidade!</div>', T('ofereceu'), t1, x=345, y=560, sound='pop')
C.sfx(12.3, 'typing', 0.4)

t0, t1 = T('cartão'), T('no')
C.scene(t0, t1, F.bg_sunburst('#ffd84d', '#ff9f2e'), [char('c7', 'caio', 540, 1900, 1.1, 'cheer', 'laugh')], cam='push', amb=None)
C.life('c7', t0, t1)
cardhtml = ('<div style="width:600px;height:370px;border-radius:34px;background:linear-gradient(135deg,#2a2840,#0f0e1a);border:8px solid #f4f0e8;box-shadow:0 14px 0 rgba(20,16,28,.35);position:relative;color:#f4f0e8">'
            '<div style="position:absolute;left:50px;top:110px;width:100px;height:76px;border-radius:14px;background:#e9c46a;border:5px solid #24203a"></div>'
            '<div style="position:absolute;left:50px;bottom:40px;font-size:40px;letter-spacing:6px">•••• 1032</div>'
            '<div style="position:absolute;right:46px;top:40px;font-size:34px;letter-spacing:3px">CAIO</div></div>')
cid = C.add(cardhtml, t0, t1, x=240, y=160, anim='none', sound='whoosh')
C.tween(f'#{cid}', {'rotationY': 180, 'scale': 0.3, 'rotation': -20}, {'rotationY': 0, 'scale': 1, 'rotation': -6, 'duration': 0.6, 'ease': 'back.out(1.4)'}, t0)
C.add(f'<div style="display:flex;align-items:center;gap:14px;background:#fff;border:6px solid #24203a;border-radius:60px;padding:8px 34px 8px 12px;font-size:46px;color:#24203a">{F.ICONS["check"]}SEM ANUIDADE</div>',
      T('sem'), t1, x=250, y=570, rot=3, sound='ting')

# almoço
t0, t1 = T('no'), T('quitou')
C.scene(t0, t1, F.bg_room('restaurant', 'day'), [char('f1', 'p1', 200, 1600, 0.82, 'cheer', 'happy'), char('f2', 'p3', 880, 1600, 0.82, 'up', 'laugh', flip=True),
                                                 char('c8', 'caio', 540, 1900, 1.05, 'up', 'laugh')], cam='panR', amb='street')
for c in ('f1', 'f2', 'c8'): C.life(c, t0, t1)
C.add(pillv('CONTA PAGA', 'R$ 1.840', 90), T('restaurante'), t1, x=None, y=250, sound='cash')
C.els[-1] = C.els[-1].replace('style="', 'style="left:540px;translate:-50% 0;', 1)
C.sfx(T('pagou'), 'cheer', 0.6)

t0, t1 = T('quitou'), T('comprou')
C.scene(t0, t1, F.bg_room('living', 'sunset'), [char('m9', 'mae', 380, 1880, 1.0, 'hug', 'happy'), char('c9', 'caio', 720, 1880, 1.05, 'hug', 'happy', flip=True)], cam='push', amb='room')
C.life('m9', t0, t1); C.life('c9', t0, t1)
C.add('<div class="stamp">QUITADO</div>', T('financiamento'), t1, x=200, y=330, anim='stamp', rot=-10, sound='thud', vol=0.7)
C.add(tilt('FINANCIAMENTO DA MÃE', 46, '#fff'), T('quitou'), t1, x=200, y=210, rot=-4, sound=None)

t0, t1 = T('comprou'), 23.32
C.scene(t0, t1, F.bg_city('day', 5), [char('c10', 'caio', 470, 1640, 1.0, 'phone2', 'happy', props=('helmet',)), F.moto_svg(540, 1860, 1.25, 'moto10')], cam='panR', amb='street')
C.life('c10', t0, t1, blink=False)
C.tween('#moto10', {'x': -900}, {'x': 0, 'duration': 0.45, 'ease': 'power3.out'}, t0)
C.tween('#c10', {'x': -900}, {'x': 0, 'duration': 0.45, 'ease': 'power3.out'}, t0)
C.add(tilt('À VISTA!', 110), T('vista'), t1, x=330, y=330, rot=-7, sound='cash')

# conta do dia
t0, t1 = 23.32, 25.9
C.scene(t0, t1, F.bg_navy(), [], cam='push', amount=0.03)
for k, (w, v, n) in enumerate((('e', '−R$ 1.840', 'RESTAURANTE'), ('mesmo', '−R$ 64 mil', 'FINANCIAMENTO'), ('assim', '−R$ 24 mil', 'MOTO'))):
    tt_ = (23.34, T('mesmo'), T('assim'))[k]
    C.add(f'<div class="lp" style="position:relative;left:0">{esc(v)}<span class="n">{esc(n)}</span></div>', tt_, t1, x=120, y=200 + 135 * k, anim='left', sound='pop', vol=0.6)
C.add(pillv('SOBROU', 'R$ 910 MIL', 110), T('900'), t1, x=None, y=1080, sound='cash')
C.els[-1] = C.els[-1].replace('style="', 'style="left:540px;translate:-50% 0;', 1)
C.add('<div class="note">valores da história · saldo era R$ 1.000.032</div>', T('900'), t1, x=0, y=1330, anim='none', sound=None)

# 3 FATO MAIS FORTE — grupo da família (noite)
t0, t1 = 25.9, 29.66
C.scene(t0, t1, F.bg_city('night', 8), [], cam='drama', rot=3, amount=0.06, shake=(T('visto'),), amb='street')
grp = C.add(phone('', 0.7, 'FAMÍLIA', '', '#7b5aa6'), t0, t1, x=323, y=100, anim='up', sound='whoosh')
counts = [3, 9, 17, 26, 34, 41, 47]
tc = [t0 + 0.05] + [T('47') + 0.1 * k for k in range(1, len(counts))]
for k, n in enumerate(counts):
    e = tc[k + 1] if k + 1 < len(counts) else t1
    C.add(f'<div style="color:#fff;font-size:30px;width:400px;background:#7b5aa6">{n} participantes</div>', tc[k], e, x=350, y=190, anim='none', sound='tick' if k else None, vol=0.4, z=5)
msgs = [('PRIMO JÚLIO', 'Oi primo, lembra de mim?', '#3a8dde'), ('TIO NENÊ', 'Que saudade, sobrinho!', '#e8483a'), ('VÓ DA PRIMA', 'Bom diaaa', '#2fbf71'), ('MADRINHA?', 'Te vi pequenininho!', '#ff9f1c')]
mt = [26.5, 27.2, T('47'), T('parentes')]
for k, (n, m, c) in enumerate(msgs):
    C.add(f'<div class="msg" style="position:relative;left:0;font-size:30px;max-width:420px"><small style="color:{c}">{esc(n)}</small>{esc(m)}</div>', mt[k], t1, x=330, y=300 + 120 * k, anim='pop', sound='notif', vol=0.55, z=5)
C.add(tilt('+44 PARENTES', 84, '#ffd23f'), T('parentes'), t1, x=250, y=1120, rot=-8, sound='pop')
C.sfx(T('visto') - 1.2, 'riser', 0.5)

# tia Cida
t0, t1 = 29.66, 33.36
C.scene(t0, t1, F.bg_room('kitchen', 'night'), [char('t13', 'tia', 540, 1890, 1.1, 'phone', 'neutral', props=('phone',))], cam='push', amb='room')
C.life('t13', t0, t1, talk=[(T('só'), 33.16)])
C.add(f'<div style="display:flex;align-items:center;gap:18px;background:#2fbf71;border:6px solid #24203a;border-radius:60px;padding:10px 40px 10px 20px;color:#fff;font-size:44px">{F.ICONS["mic"]}<span style="display:flex;gap:7px;align-items:center">' + ''.join(f'<i style="display:block;width:9px;height:{h}px;background:#fff;border-radius:5px"></i>' for h in (20,44,30,56,24,48,36,18,40,28)) + '</span><span>0:07</span></div>',
      T('áudio'), t1, x=280, y=470, rot=-3, sound='notif')
C.add('<div class="bubble" style="position:relative;left:0;translate:none"><div class="tag" style="background:#ef6fa2">TIA CIDA</div>SÓ UNS 50 MIL, SOBRINHO!<div class="tail"></div></div>',
      T('só'), t1, x=100, y=110, anim='up', sound='pop')

# 4 PERGUNTA FINAL
t0, t1 = 33.36, END + 0.08
C.scene(t0, t1, F.bg_sunburst(), [char('c14', 'caio', 540, 2330, 1.75, 'point', 'neutral')], cam='push', amount=0.05)
C.life('c14', t0, t1, talk=[(T('você'), END)])
C.add(tilt('E VOCÊ?', 120), T('você'), t1, x=280, y=150, rot=-7, sound='sparkle')
C.add('<div class="bubble" style="position:relative;left:0;translate:none;font-size:50px"><div class="tag" style="background:#4a9be8">CAIO</div>CONTAVA PRA ALGUÉM OU FICAVA QUIETO?<div class="tail"></div></div>',
      T('contava'), t1, x=100, y=380, anim='up', sound='pop')
# loop: volta ao enquadramento do gancho
gancho(t1, TOTAL, first=False)

C.caption(cap, KEYS, y=830)
MUSIC = [(0, 25.9, 'epic'), (25.9, 33.36, 'tension'), (33.36, TOTAL, 'epic')]
F.main(C, MUSIC)
