"""Short: E se o Brasil fosse o país mais capitalista do mundo? — modo 2D flat (engine/py/flat2d.py)."""
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
    """início da n-ésima ocorrência da palavra (aceita alternativas separadas por |)"""
    opts = word.lower().split('|')
    k = 0
    for w, a, b in WORDS:
        if a < after: continue
        ww = norm(w)
        if any((ww == o) if exact else ww.startswith(o) for o in opts):
            k += 1
            if k == n: return a
    raise KeyError(word)

# ---------- legenda (números em algarismos)
PATS = [(['r', '', '2'], 'R$ 2'), (['r', '', '12', 'mil'], 'R$ 12 MIL'), (['dois', 'reais'], 'R$ 2'), (['2', 'reais'], 'R$ 2'), (['cinquenta', 'centavos'], 'R$ 0,50'), (['50', 'centavos'], 'R$ 0,50'),
        (['um', 'real'], 'R$ 1'), (['1', 'real'], 'R$ 1'), (['doze', 'mil', 'reais'], 'R$ 12 MIL'), (['12', 'mil', 'reais'], 'R$ 12 MIL'),
        (['12000', 'reais'], 'R$ 12 MIL'), (['três'], '3'), (['seis'], '6')]
cap = []; i = 0
while i < len(WORDS):
    for pat, rep in PATS:
        seg = [norm(w) for w, _, _ in WORDS[i:i + len(pat)]]
        if seg == pat:
            cap.append((rep, WORDS[i][1], WORDS[i + len(pat) - 1][2])); i += len(pat); break
    else:
        cap.append((WORDS[i][0].strip(',.'), WORDS[i][1], WORDS[i][2])); i += 1
if cap: cap[-1] = ('PRIMEIRO?', cap[-1][1], cap[-1][2])
KEYS = ['BRASIL', 'CAPITALISTA', 'CAIO', 'DESPERTADOR', 'R$ 2', 'PEDÁGIO', 'R$ 0,50', 'QUARTEIRÃO', 'R$ 1', 'CHEIRINHO', 'REUNIÃO', 'PATROCÍNIO',
        'CAFÉ', 'EMPRESA', '3', 'AÇÕES', 'MARMITA', 'BOLSA', 'ASSINATURA', 'R$ 12 MIL', 'SOMBRA', 'ÁRVORE', 'VOCÊ', 'VENDER', 'PRIMEIRO?']

def phone(inner, scale=0.7, header=None, sub=None, hcol='#2fbf71'):
    hd = f'<div class="hd" style="background:{hcol}">{esc(header)}<small>{esc(sub)}</small></div>' if header else ''
    return (f'<div style="width:{620 * scale:.0f}px;height:{1000 * scale:.0f}px"><div class="ph" style="transform:scale({scale});transform-origin:0 0">'
            f'<div class="scr">{hd}{inner}</div></div></div>')

def pillv(label, value, size=96, col=None):
    c = f';color:{col}' if col else ''
    return f'<div class="pillv" style="position:relative;left:auto;translate:none;font-size:{size}px{c}"><span class="l">{esc(label)}</span>{esc(value)}</div>'

def centered(): C.els[-1] = C.els[-1].replace('style="', 'style="left:540px;translate:-50% 0;', 1)

def tilt(text, size=74, col='#ffd23f'):
    return f'<div class="tilt" style="font-size:{size}px;color:{col}">{esc(text)}</div>'

def card(icon, title, sub=''):
    return f'<div class="card">{F.ICONS[icon]}<div>{esc(title)}</div><div class="s">{esc(sub)}</div></div>'

def pos(svg, x, y):
    return f'<div style="position:absolute;left:{x}px;top:{y}px">{svg}</div>'

def bigclock(t, size=150):
    return f'<div style="background:#22213a;color:#fff;border:8px solid #f4f0e8;border-radius:36px;font-size:{size}px;line-height:1.25;padding:0 50px;box-shadow:0 10px 0 rgba(20,16,28,.3)">{t}</div>'

TAG = ('<div style="position:relative;background:#ffd23f;border:9px solid #24203a;border-radius:24px 70px 70px 24px;padding:18px 70px 22px 110px;'
       'font-size:110px;color:#24203a;white-space:nowrap;box-shadow:0 12px 0 rgba(20,16,28,.35)">'
       '<div style="position:absolute;left:34px;top:50%;margin-top:-24px;width:48px;height:48px;border-radius:50%;background:#f4f0e8;border:8px solid #24203a"></div>R$ ???</div>')

def gancho(t0, t1, first=True):
    cid = 'c1' if first else 'c99'
    sid = C.scene(t0, t1, F.bg_sunburst(), [char(cid, 'caio', 540, 1900, 1.15, 'up', 'surprise')], cam='push', amount=0.06, whoosh=not first)
    C.life(cid, t0, t1)
    tg = C.add(TAG, 0.0 if first else t0, t1, x=None, y=180, rot=-6, anim='pop' if first else 'none', sound='cash' if first else None); centered()
    C.tween(f'#{tg}', {'rotation': -6}, {'rotation': 4, 'duration': 0.5, 'repeat': max(1, int((t1 - t0) / 0.5)), 'yoyo': True, 'ease': 'sine.inOut'}, t0 + 0.35)
    return sid

# ===== 1 GANCHO
t_caio = T('caio') - 0.12
gancho(0, t_caio)
C.add(tilt('TUDO À VENDA?', 96), T('capitalista', exact=False), t_caio, x=None, y=560, rot=-6, sound='pop'); centered()
C.flash(T('capitalista', exact=False) - 0.03); C.sfx(0.0, 'riser', 0.5); C.sfx(T('capitalista', exact=False), 'coin', 0.6)

# ===== 2 ACONTECIMENTOS
# despertador
t0, t1 = t_caio, T('rua') - 0.3
C.scene(t0, t1, F.bg_room('bedroom', 'dawn'), [char('c2', 'caio', 540, 1700, 1.0, 'hang', 'sleepy')], cam='push', amount=0.08, amb='room')
C.life('c2', t0, t1, blink=False, bob=4)
C.add(tilt('BELO HORIZONTE', 60, '#fff'), T('belo') if 'belo' in [norm(w) for w, _, _ in WORDS] else t0 + 0.1, t1, x=90, y=120, rot=-5, sound='pop', vol=0.5)
al = C.add(F.alarm_svg(1.0, 'R$ 2,00'), T('despertador'), t1, x=560, y=200, anim='up', sound='notif')
C.tween(f'#{al}', {'rotation': -5}, {'rotation': 5, 'duration': 0.07, 'repeat': 20, 'yoyo': True, 'ease': 'none'}, T('despertador') + 0.3)
C.add(pillv('SONECA', 'R$ 2', 90), T('pediu') + 0.25, t1, x=None, y=600, sound='coin'); centered()
C.add(tilt('MÚSICA DE NOVO?', 62, '#fff'), T('música'), t1, x=150, y=1480, rot=-6, sound='pop', vol=0.5)
C.sfx(T('música') + 0.1, 'buzz', 0.35)

# calçada com pedágio
t0, t1 = T('rua') - 0.3, T('padaria') - 0.15
C.scene(t0, t1, F.bg_city('day', seed=7) + pos(F.tollgate_svg(1.2, 'gate1'), 160, 1050),
        [char('c3', 'caio', 260, 1860, 0.9, 'shrug', 'worried')], cam='panR', amb='street')
C.life('c3', t0, t1)
C.tween('#gate1', {'rotation': -70}, {'rotation': 0, 'duration': 0.45, 'ease': 'back.out(1.8)'}, T('pedágio') - 0.05)
C.sfx(T('pedágio'), 'buzz', 0.4)
C.add(pillv('PEDÁGIO DA CALÇADA', 'R$ 0,50', 104), T('cinquenta|50'), t1, x=None, y=230, sound='coin'); centered()
C.add(tilt('POR QUARTEIRÃO', 70), T('quarteirão'), t1, x=200, y=520, rot=-6, sound='pop', vol=0.6)

# padaria + cheirinho
t0, t1 = T('padaria') - 0.15, T('trabalho') - 0.3
C.scene(t0, t1, F.bg_city('day', seed=11) + pos(F.bakery_svg(1.0), 0, 620),
        [char('c4', 'caio', 560, 1880, 1.0, 'hang', 'happy')], cam='push', amount=0.07, amb='street')
C.life('c4', t0, t1)
smell = ''.join(f'<path d="M{x},300 Q{x - 30},240 {x},180 Q{x + 30},120 {x},60" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" opacity=".85"/>' for x in (60, 140, 220))
sm = C.add(f'<svg viewBox="0 0 280 320" width="280" height="320">{smell}</svg>', T('cheirinho') - 0.2, t1, x=640, y=880, anim='up', sound=None)
C.tween(f'#{sm}', {'y': 0, 'opacity': 1}, {'y': -40, 'opacity': 0.6, 'duration': 0.5, 'repeat': 6, 'yoyo': True, 'ease': 'sine.inOut'}, T('cheirinho') + 0.1)
C.add(card('check', 'PÃO', 'R$ 1'), T('pão'), t1, x=90, y=160, rot=-6, sound='pop')
C.add(card('x', 'CHEIRINHO', '+R$ 1'), T('cheirinho'), t1, x=700, y=200, rot=6, sound='cash')
C.add('<div class="ring" style="width:330px;height:360px"></div>', T('porta') if 'porta' in [norm(w) for w, _, _ in WORDS] else T('cheirinho') + 0.6, t1, x=670, y=170, anim='pop', sound='ting', vol=0.6)

# reunião patrocinada
t0, t1 = T('trabalho') - 0.3, T('almoço') - 0.3
C.scene(t0, t1, F.bg_room('office', 'day'), [char('ch5', 'pai', 800, 1660, 0.9, 'point', 'talk', flip=True),
                                            char('c5', 'caio', 300, 1760, 0.95, 'hang', 'surprise')], cam='push', amount=0.07, amb='room')
C.life('ch5', t0, t1, bob=5); C.life('c5', t0, t1)
C.add(tilt('REUNIÃO', 70, '#fff'), T('reunião'), t1, x=90, y=110, rot=-5, sound='pop', vol=0.5)
C.add(pillv('PATROCÍNIO', '✓ APROVADO', 70, '#ffd23f'), T('patrocínio'), t1, x=None, y=230, sound='cash'); centered()
C.add('<div class="bubble" style="position:relative;left:0;translate:none;font-size:52px"><div class="tag" style="background:#3a8dde">CHEFE</div>'
      'ESTE BOM DIA É OFERECIDO POR ☕ CAFÉ DO ZÉ<div class="tail"></div></div>', T('bom'), t1, x=100, y=560, anim='up', sound='pop')
C.sfx(T('café'), 'ting', 0.6)

# empresa em 3 minutos
t0, t1 = T('almoço') - 0.3, T('seis|6') - 0.4
C.scene(t0, t1, F.bg_navy(), [], cam='push', amount=0.1)
C.add(tilt('HORA DO ALMOÇO', 70), t0 + 0.05, t1, x=90, y=110, rot=-6, sound='pop', vol=0.5)
inner = (f'<div style="position:absolute;left:0;right:0;top:230px;text-align:center;color:#24203a">'
         f'<div style="display:inline-block">{F.ICONS["check"].replace("width=\"90\" height=\"90\"", "width=\"200\" height=\"200\"")}</div>'
         f'<div style="font-size:64px;line-height:1.05;margin-top:20px">EMPRESA<br>ABERTA!</div><div style="font-size:30px;color:#6b6890;margin-top:16px">CAIO LTDA</div></div>')
ph = C.add(phone(inner, 0.72, 'ABRA SUA EMPRESA', 'em 1 toque', '#2fbf71'), T('empresa'), t1, x=317, y=330, anim='up', sound='click')
C.sfx(T('empresa') + 0.25, 'typing', 0.4); C.sfx(T('empresa') + 0.9, 'ting', 0.6)
C.add(bigclock('3 MIN', 120), T('minutos', exact=False), t1, x=None, y=1120, sound='tick'); centered()
for k in range(1, 4): C.sfx(T('minutos', exact=False) + 0.4 * k, 'tick', 0.3)

# marmita na bolsa
t0, t1 = T('seis|6') - 0.4, T('fim') - 0.3
C.scene(t0, t1, F.bg_room('office', 'sunset'), [char('c6', 'caio', 330, 1820, 1.0, 'cheer', 'happy')], cam='panL', amb='room')
C.life('c6', t0, t1)
C.add(bigclock('18:00', 110), T('seis|6'), t1, x=90, y=120, rot=-4, sound='tick')
mar = ('<svg viewBox="0 0 360 240" width="360" height="240"><rect x="20" y="70" width="320" height="150" rx="26" fill="#c9c9d6" stroke="#24203a" stroke-width="8"/>'
       '<rect x="10" y="40" width="340" height="50" rx="20" fill="#e8483a" stroke="#24203a" stroke-width="8"/>'
       '<text x="180" y="168" font-family="Pop" font-size="46" text-anchor="middle" fill="#24203a">MARMITA</text></svg>')
C.add(mar, T('marmita'), t1, x=600, y=1380, anim='up', rot=5, sound='pop')
chart = ('<svg viewBox="0 0 520 300" width="520" height="300" style="position:absolute;left:30px;top:330px">'
         '<polyline points="0,280 70,250 140,262 210,200 280,215 350,140 420,120 500,30" fill="none" stroke="#2fa86a" stroke-width="12" stroke-linejoin="round" stroke-linecap="round"/></svg>')
cot = ('<div style="position:absolute;left:0;right:0;top:170px;text-align:center"><div style="font-size:44px;color:#24203a">MARMITA3</div>'
       '<div style="font-size:90px;color:#2fa86a;line-height:1.05">▲ +18%</div></div>')
C.add(phone(cot + chart, 0.62, 'BOLSA DE VALORES', 'ao vivo', '#7b5aa6'), T('ações|acões'), t1, x=520, y=380, anim='right', rot=4, sound='click')
C.sfx(T('bolsa') if 'bolsa' in [norm(w) for w, _, _ in WORDS] else T('marmita') + 0.5, 'cash', 0.7)
for k in range(3):
    C.add('<div class="money">+R$ 9,80</div>', T('marmita') + 0.3 + 0.25 * k, t1, x=480 + 170 * k, y=1300 - 60 * k, anim='float', sound='coin' if k == 0 else None, vol=0.5)

# FATO MAIS FORTE — praça: ventilador por assinatura e sombra alugada
t0, t1 = T('fim') - 0.3, T('você', n=1) - 0.25
C.scene(t0, t1, F.bg_city('sunset', seed=5) + pos(F.tree_svg(1.15), -30, 840) + pos(F.fan_svg(1.0, 'fan8'), 760, 1030),
        [char('p8a', 'p2', 130, 1780, 0.62, 'hang', 'happy'), char('p8b', 'p3', 330, 1760, 0.62, 'hang', 'happy'),
         char('c8', 'caio', 640, 1900, 0.95, 'cheer', 'laugh')], cam='drama', rot=3, amount=0.06, shake=(T('faturou'),), amb='street')
for c, b in (('p8a', 4), ('p8b', 4), ('c8', 8)): C.life(c, t0, t1, bob=b)
C.tween('#fan8', {'rotation': 0}, {'rotation': 360 * 12, 'duration': t1 - t0, 'ease': 'none'}, t0)
C.add(tilt('FIM DO MÊS', 66, '#fff'), t0 + 0.05, t1, x=90, y=110, rot=-5, sound='pop', vol=0.5)
C.add(tilt('VENTO POR ASSINATURA', 58), T('assinatura'), t1, x=330, y=1010, rot=5, sound='click')
C.add('<div style="background:#fff;border:7px solid #24203a;border-radius:18px;padding:8px 26px;font-size:46px;color:#24203a;box-shadow:0 8px 0 rgba(20,16,28,.3)">ALUGA-SE SOMBRA</div>',
      T('sombra'), t1, x=60, y=1150, rot=-4, sound='pop')
C.add(pillv('FATUROU', 'R$ 12 MIL', 120), T('faturou'), t1, x=None, y=250, sound='cash'); centered()
C.add('<div class="ring" style="width:640px;height:260px"></div>', T('faturou') + 0.35, t1, x=220, y=240, anim='pop', sound='ting', vol=0.7)
C.sfx(T('faturou') - 1.2, 'riser', 0.5)

# ===== 3 PERGUNTA FINAL
t0, t1 = T('você', n=1) - 0.25, END + 0.08
C.scene(t0, t1, F.bg_sunburst(), [char('c9', 'caio', 540, 2330, 1.75, 'point', 'neutral')], cam='push', amount=0.05)
C.life('c9', t0, t1, talk=[(T('você', n=1), END)])
C.add(tilt('E VOCÊ?', 120), T('você', n=1), t1, x=280, y=150, rot=-7, sound='sparkle')
C.add('<div class="bubble" style="position:relative;left:0;translate:none;font-size:56px"><div class="tag" style="background:#4a9be8">CAIO</div>IA VENDER O QUÊ PRIMEIRO?<div class="tail"></div></div>',
      T('vender'), t1, x=100, y=380, anim='up', sound='pop')
gancho(t1, TOTAL, first=False)   # loop

C.caption(cap, KEYS, y=830)
MUSIC = [(0, T('fim') - 0.3, 'comedy'), (T('fim') - 0.3, T('você', n=1) - 0.25, 'tension'), (T('você', n=1) - 0.25, TOTAL, 'comedy')]
F.main(C, MUSIC)
