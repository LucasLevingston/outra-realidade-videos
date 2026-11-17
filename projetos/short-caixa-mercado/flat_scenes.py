"""Short: 4 coisas pra nunca fazer no caixa do supermercado — modo 2D flat (engine/py/flat2d.py)."""
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

def T(word, n=1, exact=False, after=0.0):
    """início da n-ésima palavra que começa com `word` (depois de `after` s)"""
    k = 0
    for w, a, b in WORDS:
        if a < after: continue
        ww = norm(w)
        if (ww == word.lower()) if exact else ww.startswith(word.lower()):
            k += 1
            if k == n: return a
    raise KeyError(word)

# ---------- legenda (números em algarismos)
PATS = [(['quatro'], '4'), (['um', 'metro'], '1 METRO'), (['o', 'é'], 'UÉ'), (['tucunareaço'], 'TUCUNARÉ-AÇU'), (['tucunare'], 'TUCUNARÉ')]
cap = []; i = 0
while i < len(WORDS):
    for pat, rep in PATS:
        seg = [norm(w) for w, _, _ in WORDS[i:i + len(pat)]]
        if seg == pat:
            cap.append((rep, WORDS[i][1], WORDS[i + len(pat) - 1][2])); i += len(pat); break
    else:
        cap.append((WORDS[i][0].strip(',.:'), WORDS[i][1], WORDS[i][2])); i += 1
KEYS = ['CAIXA', 'SUPERMERCADO', '4', 'NUNCA', 'PRIMEIRO', 'CARTÃO', 'RECUSADO', 'TRIBUNAL', 'MARTELINHO', 'RÉU', 'DÍVIDA', 'SEGUNDO', 'TUCUNARÉ-AÇU', 'TUCUNARÉ',
        'VIVO', 'ESTEIRA', 'BRIGUENTOS', 'AMAZÔNIA', '1 METRO', 'LEITOR', 'FILA', 'TERCEIRO', 'CASAL', 'OUTRA', 'PESSOA', 'PRIMA', 'DISCUSSÃO', 'BALAS',
        'QUARTO', 'MINHOCA', 'ENTERRAR', 'PISO', 'SEGUINTE', 'ATENDE', 'DESSAS?', 'COMENTA']

def pillv(label, value, size=96):
    return f'<div class="pillv" style="position:relative;left:auto;translate:none;font-size:{size}px"><span class="l">{esc(label)}</span>{esc(value)}</div>'

def centered(): C.els[-1] = C.els[-1].replace('style="', 'style="left:540px;translate:-50% 0;', 1)

def tilt(text, size=74, col='#ffd23f'):
    return f'<div class="tilt" style="font-size:{size}px;color:{col}">{esc(text)}</div>'

def card(icon, title, sub=''):
    return f'<div class="card">{F.ICONS[icon]}<div>{esc(title)}</div><div class="s">{esc(sub)}</div></div>'

def bubble(who, text, col='#e8483a', size=54):
    return (f'<div class="bubble" style="position:relative;left:0;translate:none;font-size:{size}px"><div class="tag" style="background:{col}">{esc(who)}</div>'
            f'{esc(text)}<div class="tail"></div></div>')

def num(n):
    return (f'<div style="width:170px;height:170px;border-radius:50%;background:#ffd23f;border:9px solid #24203a;display:flex;align-items:center;justify-content:center;'
            f'font-size:120px;color:#24203a;box-shadow:0 10px 0 rgba(20,16,28,.3)">{n}</div>')

def gancho(t0, t1, first=True):
    cid = 'c1' if first else 'c99'
    sid = C.scene(t0, t1, F.bg_room('market', 'day'), [char(cid, 'caixa', 540, 1260, 1.0, 'wave', 'happy')], cam='push', amount=0.07, whoosh=not first, amb='room')
    C.life(cid, t0, t1)
    C.add(tilt('VAI SER CAIXA?', 96), 0.0 if first else t0, t1, x=120, y=230, rot=-7, anim='pop' if first else 'none', sound='pop' if first else None)
    return sid

# 1 GANCHO
t_entao = T('então') - 0.1
gancho(0, t_entao)
C.sfx(0.0, 'riser', 0.45); C.sfx(T('supermercado') - 0.02, 'ting', 0.5)

t0, t1 = t_entao, T('primeiro') - 0.1
C.scene(t0, t1, F.bg_sunburst(), [char('c2', 'caixa', 540, 1900, 1.15, 'point', 'neutral')], cam='push', amount=0.08)
C.life('c2', t0, t1, talk=[(t0 + 0.1, t1 - 0.2)])
C.add(pillv('NO CAIXA', '4 COISAS', 110), T('quatro'), t1, x=None, y=180, sound='pop'); centered()
C.add('<div class="stamp" style="font-size:120px">NUNCA</div>', T('nunca'), t1, x=290, y=470, anim='stamp', rot=-10, sound='thud', vol=0.7)
C.flash(T('nunca') - 0.03)

# 2 ACONTECIMENTOS — 1) cartão recusado
t0, t1 = T('primeiro') - 0.1, T('passar') - 0.1
C.scene(t0, t1, F.bg_room('market', 'day'), [char('p1a', 'p1', 800, 1700, 0.9, 'phone2', 'worried', flip=True),
                                             char('c3', 'caixa', 300, 1260, 0.85, 'hip', 'neutral')], cam='panR', amb='room')
C.life('p1a', t0, t1); C.life('c3', t0, t1)
C.add(num(1), t0 + 0.05, t1, x=70, y=150, sound='pop', vol=0.5)
C.add(F.card_svg(1.0, declined=False), T('cartão'), T('recusado'), x=560, y=380, anim='up', rot=6, sound='click')
C.add(F.card_svg(1.0, declined=True), T('recusado'), t1, x=560, y=380, anim='none', rot=6, sound='wrong', vol=0.6)
C.add(tilt('RECUSADO', 70, '#ff6b5a'), T('recusado') + 0.05, t1, x=560, y=660, rot=-6, sound=None)
C.add('<div class="stamp" style="font-size:96px">TRIBUNAL?</div>', T('tribunal'), t1, x=60, y=1480, anim='stamp', rot=-8, sound='thud', vol=0.6)

t0, t1 = T('passar') - 0.1, T('costuma') - 0.1
C.scene(t0, t1, F.bg_room('market', 'day'), [char('c4', 'caixa', 540, 2250, 1.55, 'hang', 'angry', headonly=True)], cam='push', amount=0.1, shake=(T('martelinho') + 0.1,), amb='room')
C.life('c4', t0, t1, talk=[(T('como', after=T('passar')), T('costuma') - 0.2)])
C.add(tilt('PASSAR DE NOVO = NORMAL', 54, '#fff'), t0 + 0.05, t1, x=90, y=470, rot=-4, sound='pop', vol=0.4)
C.add(F.gavel_svg(1.1), T('martelinho'), t1, x=600, y=1180, anim='up', rot=-10, sound=None)
C.add(bubble('CAIXA', 'COMO O RÉU PRETENDE QUITAR ESSA DÍVIDA?'), T('como', after=T('passar')), t1, x=100, y=110, anim='up', sound='pop')

t0, t1 = T('costuma') - 0.1, T('segundo') - 0.1
C.scene(t0, t1, F.bg_room('market', 'day'), [char('p1b', 'p1', 540, 2250, 1.55, 'hang', 'worried', headonly=True)], cam='push', amount=0.06, amb='room')
C.life('p1b', t0, t1)
C.add(tilt('SEM GRAÇA...', 100), T('sem'), t1, x=180, y=300, rot=-6, sound='boing', vol=0.5)

# 2) tucunaré na esteira
t0, t1 = T('segundo') - 0.1, T('ele') - 0.1
C.scene(t0, t1, F.bg_room('market', 'day'), [char('c5', 'caixa', 760, 1260, 0.85, 'shrug', 'surprise', flip=True)], cam='panL', amb='room')
C.life('c5', t0, t1)
C.add(num(2), t0 + 0.05, t1, x=70, y=150, sound='pop', vol=0.5)
fid = C.add(F.fish_svg(0.85), T('tucunar'), t1, x=60, y=1000, anim='left', sound='boing')
C.tween(f'#{fid}', {'rotation': -6}, {'rotation': 6, 'duration': 0.18, 'repeat': int((t1 - T('tucunar')) / 0.18), 'yoyo': True, 'ease': 'sine.inOut'}, T('tucunar') + 0.35)
C.add(pillv('NA ESTEIRA', 'VIVO', 100), T('vivo'), t1, x=None, y=380, sound='ting'); centered()

t0, t1 = T('ele') - 0.1, T('ou', exact=True) - 0.1
C.scene(t0, t1, F.bg_navy(), [], cam='push', amount=0.1)
f2 = C.add(F.fish_svg(1.4, flip=True), t0 + 0.05, t1, x=106, y=960, anim='pop', sound='whoosh', vol=0.5)
C.tween(f'#{f2}', {'y': 0}, {'y': -20, 'duration': 0.4, 'repeat': int((t1 - t0) / 0.4), 'yoyo': True, 'ease': 'sine.inOut'}, t0 + 0.4)
C.add(card('x', 'BRIGUENTO', 'NÍVEL MÁXIMO'), T('briguentos'), t1, x=90, y=200, rot=-5, sound='buzz', vol=0.45)
C.add(card('check', 'AMAZÔNIA', 'ORIGEM'), T('amazônia'), t1, x=720, y=200, rot=5, sound='pop')
ruler = ('<div style="width:880px;height:70px;background:#ffd23f;border:7px solid #24203a;border-radius:14px;position:relative;'
         'background-image:repeating-linear-gradient(90deg,#24203a 0 5px,transparent 5px 88px);font-size:52px;color:#24203a;text-align:center;line-height:70px">QUASE 1 METRO</div>')
C.add(ruler, T('metro'), t1, x=100, y=1470, anim='up', sound='tick')
C.add('<div class="ring" style="width:960px;height:520px"></div>', T('metro') + 0.1, t1, x=60, y=900, anim='pop', sound=None)

t0, t1 = T('ou', exact=True) - 0.1, T('terceiro') - 0.1
C.scene(t0, t1, F.bg_room('market', 'day'), [char('q1', 'mae', 640, 1720, 0.62, 'hip', 'worried'), char('q2', 'irmao', 820, 1760, 0.66, 'hip', 'surprise'),
                                             char('q3', 'p2', 1000, 1800, 0.7, 'shrug', 'angry'),
                                             char('c6', 'caixa', 240, 1260, 0.85, 'phone2', 'worried')], cam='drama', rot=2, amount=0.05, shake=(T('fila'),), amb='room')
for c in ('q1', 'q2', 'q3', 'c6'): C.life(c, t0, t1)
f3 = C.add(F.fish_svg(0.7), t0 + 0.05, t1, x=380, y=1010, anim='none', sound=None)
C.tween(f'#{f3}', {'rotation': -8}, {'rotation': 8, 'duration': 0.14, 'repeat': int((t1 - t0) / 0.14), 'yoyo': True, 'ease': 'sine.inOut'}, t0 + 0.05)
C.add(card('x', 'LEITOR', 'NÃO PASSA'), T('leitor'), t1, x=690, y=640, rot=6, sound='wrong', vol=0.6)
C.add(tilt('FILA PARADA', 100), T('fila'), t1, x=150, y=260, rot=-6, sound='crowd', vol=0.5)

# 3) o casal
t0, t1 = T('terceiro') - 0.1, T('mesmo') - 0.1
C.scene(t0, t1, F.bg_room('market', 'day'), [char('m7', 'p2', 700, 1720, 0.8, 'hug', 'happy', flip=True), char('w7', 'p3', 900, 1740, 0.8, 'hug', 'happy', flip=True),
                                             char('c7', 'caixa', 270, 1260, 0.85, 'point', 'surprise')], cam='push', amb='room')
for c in ('m7', 'w7', 'c7'): C.life(c, t0, t1)
C.life('c7', t0, t1, talk=[((T('semana') - 0.55), T('mesmo') - 0.2)])
C.add(num(3), t0 + 0.05, t1, x=70, y=150, sound='pop', vol=0.5)
C.add(tilt('CASAL', 90, '#ff8ab0'), T('casal'), (T('semana') - 0.55), x=640, y=520, rot=6, sound='sparkle', vol=0.5)
C.add(bubble('CAIXA', 'UÉ, SEMANA PASSADA VOCÊ VEIO COM OUTRA PESSOA'), (T('semana') - 0.55), t1, x=100, y=110, anim='up', sound='pop')

t0, t1 = T('mesmo') - 0.1, T('quarto') - 0.1
C.scene(t0, t1, F.bg_room('market', 'day'), [char('m8', 'p2', 360, 1760, 0.95, 'shrug', 'worried'), char('w8', 'p3', 760, 1760, 0.95, 'hip', 'angry', flip=True)],
        cam='drama', rot=-3, amount=0.06, shake=(T('discussão'),), amb='room')
C.life('m8', t0, t1, talk=[(T('mesmo'), T('discussão') - 0.1)]); C.life('w8', t0, t1, talk=[(T('discussão'), t1 - 0.2)], bob=10)
C.add(card('check', 'ERA A PRIMA', 'MESMO ASSIM...'), T('prima'), t1, x=90, y=200, rot=-5, sound='ting', vol=0.5)
C.add(tilt('DISCUSSÃO!', 110, '#ff6b5a'), T('discussão'), t1, x=330, y=560, rot=5, sound=None)
C.add(tilt('BALAS', 70, '#fff'), T('balas'), t1, x=730, y=300, rot=8, sound='pop', vol=0.4)

# 4) a minhoca
t0, t1 = T('quarto') - 0.1, T('disser') - 0.35
C.scene(t0, t1, F.bg_room('market', 'day'), [char('c9', 'caixa', 420, 1260, 0.9, 'phone2', 'happy'), char('p9', 'p1', 860, 1720, 0.85, 'hang', 'surprise', flip=True)], cam='push', amount=0.08, amb='room')
C.life('c9', t0, t1, talk=[(T('se', exact=True, after=T('quarto')), t1 - 0.2)]); C.life('p9', t0, t1)
C.add(num(4), t0 + 0.05, t1, x=70, y=150, sound='pop', vol=0.5)
C.add(bubble('CAIXA', 'SE EU FOSSE UMA MINHOCA, VOCÊ AINDA PASSARIA NO MEU CAIXA?', size=50), T('se', exact=True, after=T('quarto')), t1, x=100, y=380, anim='up', sound='pop')
w9 = C.add(F.worm_svg(1.0), T('minhoca'), t1, x=80, y=1300, anim='up', sound='boing')
C.tween(f'#{w9}', {'scaleX': 1}, {'scaleX': 1.12, 'duration': 0.3, 'repeat': int((t1 - T('minhoca')) / 0.3), 'yoyo': True, 'ease': 'sine.inOut'}, T('minhoca') + 0.3)

t0, t1 = T('disser') - 0.35, (T('dia', exact=True)) - 0.35
C.scene(t0, t1, F.bg_room('market', 'day'), [char('p10', 'p1', 760, 1720, 0.85, 'hip', 'angry', flip=True)], cam='push', amount=0.06, shake=(T('enterrar'),), amb='room')
C.life('p10', t0, t1, talk=[(T('não', after=T('disser')), T('não', after=T('disser')) + 0.5)])
C.add('<div class="stamp" style="font-size:130px">NÃO</div>', T('não', after=T('disser')), t1, x=520, y=330, anim='stamp', rot=8, sound='thud', vol=0.6)
C.add(tilt('EVITE VIRAR MINHOCA', 70), T('evite'), t1, x=70, y=150, rot=-5, sound='pop', vol=0.5)
w10 = C.add(F.worm_svg(0.9), T('enterrar'), t1, x=120, y=1300, anim='none', sound='thud', vol=0.5)
C.tween(f'#{w10}', {'y': 0, 'opacity': 1}, {'y': 260, 'opacity': 0.0, 'duration': max(0.4, t1 - T('enterrar') - 0.1), 'ease': 'power1.in'}, T('enterrar'))
C.add('<div style="width:520px;height:40px;background:#c98f5e;border:6px solid #24203a;border-radius:20px"></div>', T('piso'), t1, x=80, y=1500, anim='pop', sound=None)

# FATO MAIS FORTE — o tucunaré virou caixa
t0, t1 = (T('dia', exact=True)) - 0.35, T('você', after=T('tucunar', n=2)) - 0.2
C.scene(t0, t1, F.bg_room('market', 'day'), [char('q11', 'p3', 840, 1760, 0.8, 'phone2', 'surprise', flip=True)], cam='drama', rot=3, amount=0.06, shake=(T('tucunar', n=2),), amb='room')
C.life('q11', t0, t1)
C.flash(t0 + 0.03); C.sfx(t0 + 0.03, 'chime', 0.5)
C.add(tilt('NO DIA SEGUINTE', 70, '#fff'), t0 + 0.05, t1, x=90, y=140, rot=-5, sound='pop', vol=0.4)
t_cx = T('caixa', after=T('seguinte'))
f11 = C.add(F.fish_svg(1.0, flip=True), t_cx, t1, x=120, y=990, anim='up', sound='boing')
C.tween(f'#{f11}', {'y': 0}, {'y': -16, 'duration': 0.35, 'repeat': int((t1 - t_cx) / 0.35), 'yoyo': True, 'ease': 'sine.inOut'}, t_cx + 0.3)
C.add(tilt('CAIXA ABERTO', 66, '#fff'), T('voltou'), t1, x=520, y=560, rot=6, sound='ting', vol=0.4)
C.add(pillv('QUEM ATENDE', 'O TUCUNARÉ', 92), T('tucunar', n=2), t1, x=None, y=360, sound='ting'); centered()
C.sfx(T('tucunar', n=2) - 1.1, 'riser', 0.45)

# 3 PERGUNTA FINAL
t0, t1 = T('você', after=T('tucunar', n=2)) - 0.2, END + 0.08
C.scene(t0, t1, F.bg_sunburst(), [char('c12', 'caixa', 540, 2330, 1.75, 'point', 'neutral')], cam='push', amount=0.05)
C.life('c12', t0, t1, talk=[(t0 + 0.2, END)])
C.add(tilt('E VOCÊ?', 120), t0 + 0.2, t1, x=280, y=150, rot=-7, sound='sparkle')
C.add(bubble('CAIXA', 'JÁ FEZ ALGUMA DESSAS?', size=60), T('já'), t1, x=100, y=380, anim='up', sound='pop')
gancho(t1, TOTAL, first=False)

C.caption(cap, KEYS, y=830)
MUSIC = [(0, (T('dia', exact=True)) - 0.35, 'comedy'),
         ((T('dia', exact=True)) - 0.35, T('você', after=T('tucunar', n=2)) - 0.2, 'tension'),
         (T('você', after=T('tucunar', n=2)) - 0.2, TOTAL, 'comedy')]
F.main(C, MUSIC)
