"""Creators 100X x Creedom "365 Days in One Room" (9:16, cosy 2.5D diorama): writes index.html, plan/sfx_events.json and
plan/edit.json from plan/words.json.

Script approved by the owner on 2026-11-20, voiced with ElevenLabs (Jessica, Eleven v3; build/vo_el.py take 1, pauses trimmed
by build/vo_tight.py, a 1 s breath after the reel-check line by build/vo_insert.py, word times by build/vo_words.py).

One cutaway miniature bedroom-studio, one camera angle that keeps coming back:
  0 hook: night, snow outside, the ring light clicks on, "Day 1";
  1 a year in fast-forward: day and night flicker, the window runs through the seasons (snow, blossom, sun, falling leaves), her
    outfit changes, she jumps between the ring light, the desk and the bed, coffee cups pile up, the plant grows, the calendar
    races to Day 365;
  2 the views counter on the wall: 47, it twitches and never moves;
  3 3 a.m., she's asleep at the desk, phone still glowing;
  4 the turn: pink light bursts from the phone, Cree pops out, her whole year of reels fans out across the wall, red marks pin
    the second each one lost people ("left at 0:02");
  5 the reel check (example score 4.7 / 5) folds into the phone;
  6 the same angle as the opening, now warm: string lights, the counter spinning, hearts floating up, chibi fans cheering in the
    window, Cree dancing on the desk;
  7 CTA: the counter turns into COMMENT GROW.
Claims stay within what Creedom does (reads the account, shows where viewers dropped off, scores a reel before posting). The 47,
the drop-off marks and the score are examples; the counter at the end spins too fast to read, so no number is promised.
python3 build/generate.py
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fx import T, js, sfx, ft, to, st, LINES, L0, L1, JS, SFX, ROOT, punch  # noqa: E402
from fx import cree_html, cree_to, pose, cree_hop, sparkle, P  # noqa: E402
from chibi import DEFS as CHIBI_DEFS, seated  # noqa: E402

random.seed(365)
DUR = round(L1["g7"] + 1.7, 2)
T0 = {k: (L0[k], L1[k]) for k in LINES}

# ---- headlines (screen space) ---------------------------------------------------------------------------------------------
HTMLS, OPEN, WID = [], [None], [0]


def head(hid, rows, top, line, size=96, after=0.0):
    spoken, k, out, rws = [w for w in LINES[line] if w["t0"] >= after - 1e-3], 0, [], []
    for row in rows:
        ws = []
        for word, cls in row:
            WID[0] += 1
            wid = f"h{WID[0]}"
            key, t = word.lower().strip(".,:!?…"), None
            while k < len(spoken):
                sw = spoken[k]["w"].lower().strip(".,:!?")
                k += 1
                if sw.startswith(key[:4]) or key.startswith(sw[:4]):
                    t = spoken[k - 1]["t0"]
                    break
            if t is None:
                t = spoken[-1]["t0"]
            ws.append(f'<span class="hw {cls}" id="{wid}">{word}</span>')
            out.append((wid, t))
        rws.append(f'<div class="hl">{" ".join(ws)}</div>')
    HTMLS.append(f'<div class="head" id="{hid}" style="top:{top}px;font-size:{size}px">{"".join(rws)}</div>')
    for wid, t in out:
        ft(f"#{wid}", t - .05, .34, "{opacity: 0, filter: 'blur(12px)', y: 22}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
    first = min(t for _, t in out)
    if OPEN[0]:
        to(f"#{OPEN[0]}", first - .3, .2, "{opacity: 0, filter: 'blur(14px)', y: -36}", "power2.in")
    OPEN[0] = hid


# ---- camera (three parallax rigs) --------------------------------------------------------------------------------------------
RIGS = (("#rbg", .5), ("#rw", 1.0), ("#rfg", 1.5))


def cam(t, cx, cy, z, d=1.0, ease="power2.inOut", setonly=False):
    for sel, f in RIGS:
        zf = 1 + (z - 1) * f
        cxf, cyf = 540 + (cx - 540) * f, 960 + (cy - 960) * f
        props = f"x: {540 - cxf * zf:.1f}, y: {960 - cyf * zf:.1f}, scale: {zf:.4f}"
        js(f'gsap.set("{sel}", {{{props}}});' if setonly else f'tl.to("{sel}", {{{props}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


def counter(t0, t1, v0, v1, sel_js):
    """a number that counts from v0 to v1 between t0 and t1 (sel_js writes the value v into the page)"""
    js(f'(() => {{ const o = {{v: {v0}}}; tl.to(o, {{v: {v1}, duration: {t1 - t0:.3f}, ease: "none", onUpdate: () => {{ const v = o.v; {sel_js} }}}}, {t0:.3f}); }})();')


TICK = ('<svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="22" fill="#2fbf71"/><path d="M13 25 L21 33 L36 16" fill="none" stroke="#fff" stroke-width="5" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>')
HEART = '<svg viewBox="0 0 40 36" width="{w}" height="{h}"><path d="M20 34 C4 22 0 14 4 8 C8 1 17 2 20 9 C23 2 32 1 36 8 C40 14 36 22 20 34 Z" fill="{c}"/></svg>'
BUBBLE = ('<svg viewBox="0 0 44 40" width="{w}" height="{h}"><path d="M6 4 H38 Q42 4 42 8 V26 Q42 30 38 30 H18 L9 38 L11 30 H6 Q2 30 2 26 V8 Q2 4 6 4 Z" fill="#fff"/>'
          '<circle cx="14" cy="17" r="3" fill="#F343A2"/><circle cx="22" cy="17" r="3" fill="#F343A2"/><circle cx="30" cy="17" r="3" fill="#F343A2"/></svg>')

# =======================================================================================================================
# THE ROOM: back wall 150..930 x 580..1200, floor out to 40..1040 at y 1480
PLANKS = "".join(f'<line x1="{150 + i * 97.5:.1f}" y1="1200" x2="{40 + i * 125:.1f}" y2="1480" stroke="#7a4c30" stroke-width="2" opacity=".45"/>' for i in range(1, 8))
STRIPES = "".join(f'<rect x="{150 + i * 39}" y="580" width="16" height="620" fill="#fff" opacity=".07"/>' for i in range(20))
SHELL = f'''<svg class="shell" viewBox="0 0 1080 1920"><defs>
<linearGradient id="gbw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6dcc7"/><stop offset="1" stop-color="#e8c2a8"/></linearGradient>
<linearGradient id="gsl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d4a88e"/><stop offset="1" stop-color="#e2b99f"/></linearGradient>
<linearGradient id="gsr" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#d9ad93"/><stop offset="1" stop-color="#e6bea4"/></linearGradient>
<linearGradient id="gfl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a8714b"/><stop offset="1" stop-color="#c38a5f"/></linearGradient>
<linearGradient id="gdk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2e6d8"/><stop offset="1" stop-color="#dccbb7"/></linearGradient>
<linearGradient id="gbed" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fb7ff"/><stop offset="1" stop-color="#7b93e0"/></linearGradient>
</defs>
<polygon points="150,580 930,580 930,1200 150,1200" fill="url(#gbw)"/>{STRIPES}
<polygon points="40,470 150,580 150,1200 40,1480" fill="url(#gsl)"/>
<polygon points="930,580 1040,470 1040,1480 930,1200" fill="url(#gsr)"/>
<polygon points="150,1200 930,1200 1040,1480 40,1480" fill="url(#gfl)"/>{PLANKS}
<rect x="150" y="1184" width="780" height="16" fill="#fff8ef" opacity=".7"/>
<polygon points="40,1480 1040,1480 1040,1524 40,1524" fill="#5c3b28"/>
<polyline points="40,470 150,580 930,580 1040,470" fill="none" stroke="#fbf3ea" stroke-width="12" stroke-linejoin="round"/>
<line x1="40" y1="470" x2="40" y2="1524" stroke="#fbf3ea" stroke-width="12"/><line x1="1040" y1="470" x2="1040" y2="1524" stroke="#fbf3ea" stroke-width="12"/>
<ellipse cx="560" cy="1372" rx="300" ry="58" fill="#e9a6c2" opacity=".75"/><ellipse cx="560" cy="1372" rx="250" ry="44" fill="none" stroke="#fff" stroke-width="4" opacity=".5"/>
<polygon points="190,1050 510,1050 532,1100 168,1100" fill="url(#gdk)"/><rect x="168" y="1100" width="364" height="24" fill="#cdb9a2"/>
<rect x="180" y="1124" width="14" height="140" fill="#b9a38b"/><rect x="506" y="1124" width="14" height="140" fill="#b9a38b"/>
<polygon points="820,1268 1012,1268 1032,1330 800,1330" fill="#fff6ee"/><polygon points="800,1330 1032,1330 1032,1440 800,1440" fill="url(#gbed)"/>
<rect x="800" y="1430" width="232" height="16" fill="#6b4a36"/><ellipse cx="870" cy="1290" rx="46" ry="16" fill="#fff"/>
<path d="M800 1336 Q900 1318 1032 1340 L1032 1440 L800 1440 Z" fill="#8ea6f2" opacity=".6"/>
<line x1="760" y1="1035" x2="760" y2="1330" stroke="#2a2430" stroke-width="7"/>
<path d="M760 1330 L716 1372 M760 1330 L804 1372 M760 1330 L760 1378" stroke="#2a2430" stroke-width="6" stroke-linecap="round"/>
<circle cx="760" cy="960" r="74" fill="none" stroke="#3a3440" stroke-width="16"/><circle cx="760" cy="960" r="74" fill="none" stroke="#fffaf0" stroke-width="9" id="ringtube" opacity=".35"/>
</svg>'''

# the window: one group per season, a night layer over them, fans for the happy ending
def flakes(n, cls, col, w, h, rnd=True):
    return "".join(f'<i class="ptc {cls}" id="{cls}{i}" style="width:{w}px;height:{h}px;background:{col};left:{random.randint(0, 250)}px;'
                   f'{"border-radius:50%;" if rnd else "border-radius:2px;"}"></i>' for i in range(n))


TREE = ('<i class="trunk"></i><i class="br" style="left:58px;bottom:96px;transform:rotate(-38deg)"></i>'
        '<i class="br" style="left:74px;bottom:100px;transform:rotate(34deg)"></i>')


def canopy(col, col2):
    return "".join(f'<i class="canopy" style="left:{x}px;bottom:{y}px;width:{r}px;height:{r}px;background:{c}"></i>'
                   for x, y, r, c in ((20, 96, 70, col), (58, 110, 66, col2), (34, 128, 60, col), (8, 118, 48, col2), (76, 92, 50, col)))


SEASONS = {
    "sW": ("linear-gradient(180deg,#bcd7f2,#e8f1fb)", "#ffffff", "#f2f6ff", "", flakes(18, "sn", "#fff", 7, 7)),
    "sSp": ("linear-gradient(180deg,#9fd3ff,#d9f0ff)", "#9ee08a", "#7fcf72", canopy("#ffc0dd", "#ff9ccb"), flakes(12, "pe", "#ffb3d6", 8, 6, False)),
    "sSu": ("linear-gradient(180deg,#5fb6ff,#bfe6ff)", "#6fcf5e", "#58b84a", canopy("#4fb44a", "#3e9c3c") + '<i class="sun"></i>', ""),
    "sAu": ("linear-gradient(180deg,#f7c58a,#fde2bf)", "#e0a050", "#c98536", canopy("#f08a3c", "#d9622b"), flakes(12, "lf", "#e8742f", 10, 7, False)),
}
WIN = ""
for sid, (sky, h1, h2, can, parts) in SEASONS.items():
    WIN += (f'<div class="ssn" id="{sid}"><div class="sky" style="background:{sky}"></div><div class="hill2" style="background:{h2}"></div>'
            f'<div class="hill" style="background:{h1}"></div>{TREE}{can}{parts}</div>')
STARS = "".join(f'<i id="stx{i}" style="left:{random.randint(6, 250)}px;top:{random.randint(6, 110)}px"></i>' for i in range(14))
WIN += (f'<div class="ssn" id="sN" style="opacity:.82"><div class="sky" style="background:linear-gradient(180deg,rgba(8,12,40,.92),rgba(24,34,80,.72))"></div>'
        f'<i class="moon"></i><div class="stars">{STARS}</div></div>')
FANS = ""
for i, x in enumerate((-8, 52, 112, 172)):
    FANS += seated(f"fan{i}", x, 116 + (i % 2) * 8, 78, turn=True, phone=(i % 2 == 0), style="--ph:1")
WIN += f'<div id="fans">{FANS}</div>'

# counter, calendar, corkboard, wall clock, string lights
CTR = ('<div class="ctr"><div class="lab" id="clab">VIEWS</div><div class="lab" id="clab2">COMMENT</div>'
       '<div class="num" id="c47">47</div><div class="num" id="c48">48</div><div class="num" id="cspin">47</div><div class="num" id="cgrow">GROW</div></div>')
CAL = '<div class="cal"><div class="mon" id="cmon">JAN</div><div class="dl">DAY</div><div class="dn" id="cday">1</div></div>'
NOTES = (('#fff3a6', 12, 14, -6, "post<br>daily!"), ('#ffc6dd', 128, 10, 5, "hook??"), ('#bfe3ff', 70, 82, -3, "why do<br>they leave"))
CORK = '<div class="cork">' + "".join(f'<div class="note" data-layout-ignore style="left:{x}px;top:{y}px;background:{c};transform:rotate({r}deg)">{t}</div>'
                                      for c, x, y, r, t in NOTES) + '</div>'
CLOCK = ('<div class="clock" id="clk" style="left:455px;top:840px;opacity:1"><span id="ck1">9:00 PM</span></div>'
         '<div class="clock" id="clk3" style="left:455px;top:840px">3:07 AM</div>')
SLX = [(160 + i * 49, 598 + (14 if i % 2 else 0) + (6 if i % 4 == 1 else 0)) for i in range(16)]
SLS = ('<svg class="shell" viewBox="0 0 1080 1920" style="pointer-events:none"><path d="M150 590 ' +
       " ".join(f"Q{x - 24} {y + 10} {x} {y}" for x, y in SLX) + ' L930 590" fill="none" stroke="#5a4a40" stroke-width="2.5"/></svg>' +
       "".join(f'<i class="sl" id="sl{i}" style="left:{x - 7}px;top:{y}px"></i>' for i, (x, y) in enumerate(SLX)))
SLG = "".join(f'<i class="slglow" id="slg{i}" style="left:{x}px;top:{y + 9}px"></i>' for i, (x, y) in enumerate(SLX))

# desk things: coffee cups that pile up, the phone, the lamp, steam
CUPC = ("#e86f8e", "#6fa8e8", "#f2b84b", "#7ccf9a", "#b48cff", "#ff8a5c", "#5fd0d6")
CUPS = "".join(f'<i class="cup" id="cup{i}" style="left:{196 + i * 26}px;top:{1022 - (i % 2) * 4}px"><b style="background:{CUPC[i]}"></b></i>' for i in range(7))
STEAM = "".join(f'<i class="steam" id="stm{i}" style="left:{200 + 26 * 6 + i * 8}px;top:{990 - i * 6}px"></i>' for i in range(2))
LAMP = ('<svg class="lamp" viewBox="0 0 56 100"><path d="M10 6 H46 L54 40 H2 Z" fill="#ffd27a"/><rect x="25" y="40" width="6" height="50" fill="#5a4a40"/>'
        '<ellipse cx="28" cy="94" rx="20" ry="6" fill="#5a4a40"/></svg>')
PLANT = ('<svg class="plant" id="plant" viewBox="0 0 120 190"><path d="M60 150 C58 110 40 90 22 70 M60 150 C62 106 82 80 100 56 M60 150 C60 100 60 70 58 30" '
         'stroke="#3f8f4a" stroke-width="6" fill="none" stroke-linecap="round"/>'
         + "".join(f'<ellipse cx="{x}" cy="{y}" rx="16" ry="9" fill="{c}" transform="rotate({r} {x} {y})" id="lv{i}"/>' for i, (x, y, r, c) in enumerate(
             ((24, 72, -30, "#5fbf6a"), (98, 58, 30, "#4fae5a"), (58, 32, -80, "#6fcf7a"), (36, 104, 20, "#4fae5a"), (86, 96, -20, "#5fbf6a"), (62, 70, 70, "#6fcf7a"))))
         + '<path d="M34 150 H86 L80 188 H40 Z" fill="#d97a4a"/><rect x="30" y="146" width="60" height="10" rx="4" fill="#e88a5a"/></svg>')

# her: standing (outfits through CSS variables) and asleep at the desk (from behind)
STAR = ('<div id="star"><svg viewBox="0 0 190 340"><defs>'
        '<radialGradient id="ssk" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ffe0cc"/><stop offset="1" stop-color="#e8a98c"/></radialGradient>'
        '<radialGradient id="shr" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#6b3b3f"/><stop offset="1" stop-color="#2e1517"/></radialGradient></defs>'
        '<rect x="70" y="250" width="20" height="86" rx="10" fill="#3a2430"/><rect x="100" y="250" width="20" height="86" rx="10" fill="#3a2430"/>'
        '<g id="shood" opacity="0"><ellipse cx="95" cy="118" rx="62" ry="64" style="fill:var(--dress2)"/></g>'
        '<path d="M42 268 C42 180 64 140 95 140 C126 140 148 180 148 268 Z" style="fill:var(--dress)"/>'
        '<path d="M120 150 C140 170 148 220 148 268 L118 268 C126 220 126 180 120 150 Z" style="fill:var(--dress2)" opacity=".55"/>'
        '<g id="shead"><circle cx="95" cy="88" r="52" fill="url(#shr)"/><circle cx="95" cy="32" r="24" fill="url(#shr)"/>'
        '<ellipse cx="99" cy="98" rx="42" ry="46" fill="url(#ssk)"/>'
        '<path d="M56 90 C58 56 86 42 108 44 C132 46 146 64 145 88 C126 72 104 68 84 74 C72 78 62 84 56 90 Z" fill="url(#shr)"/>'
        '<circle cx="78" cy="118" r="8" fill="#f59bb1" opacity=".6"/><circle cx="124" cy="116" r="8" fill="#f59bb1" opacity=".6"/>'
        '<ellipse cx="88" cy="102" rx="4.5" ry="6" fill="#2a1220"/><ellipse cx="114" cy="101" rx="4.5" ry="6" fill="#2a1220"/>'
        '<path id="sm_open" d="M92 124 Q101 134 110 124 Z" fill="#9a3b4e"/>'
        '<path id="sm_sad" d="M92 130 Q101 122 110 130" fill="none" stroke="#9a3b4e" stroke-width="3.5" stroke-linecap="round" opacity="0"/>'
        '<ellipse id="sm_wow" cx="101" cy="127" rx="6" ry="7.5" fill="#9a3b4e" opacity="0"/>'
        '<path id="sm_smile" d="M88 122 Q101 140 114 122 Z" fill="#9a3b4e" opacity="0"/></g>'
        '<g id="sscarf" opacity="1"><path d="M58 142 Q95 168 132 142 L136 158 Q95 184 54 158 Z" fill="#e5484d"/>'
        '<path d="M110 156 L126 214 L108 216 L100 162 Z" fill="#c93a40"/><path d="M64 150 L128 150" stroke="#fff" stroke-width="3" opacity=".6"/></g>'
        '<g id="sarm"><path d="M136 176 C160 168 164 140 146 118" fill="none" style="stroke:var(--dress)" stroke-width="24" stroke-linecap="round"/>'
        '<circle cx="144" cy="114" r="11" fill="url(#ssk)"/><rect x="128" y="76" width="26" height="44" rx="6" fill="#1a1016"/>'
        '<rect id="sscr" x="131" y="79" width="20" height="38" rx="4" fill="#ffd9ea"/></g>'
        '<path id="slarm" d="M50 180 C34 210 40 240 52 250" fill="none" style="stroke:var(--dress)" stroke-width="22" stroke-linecap="round"/></svg></div>')
SLEEP = ('<div id="sleep" style="--dress:#e8763c;--dress2:#b9542a"><svg viewBox="0 0 240 330">'
         '<path d="M70 262 L60 330 M170 262 L180 330 M120 268 L120 330" stroke="#6b4a36" stroke-width="9" stroke-linecap="round"/>'
         '<ellipse cx="120" cy="258" rx="74" ry="16" fill="#8a5a36"/>'
         '<path d="M58 258 C52 200 70 158 120 156 C170 158 188 200 182 258 Z" style="fill:var(--dress)"/>'
         '<path d="M150 170 C176 196 184 230 182 258 L158 258 C160 222 158 196 150 170 Z" style="fill:var(--dress2)" opacity=".55"/>'
         '<ellipse cx="66" cy="146" rx="30" ry="18" style="fill:var(--dress)" transform="rotate(-18 66 146)"/>'
         '<ellipse cx="174" cy="146" rx="30" ry="18" style="fill:var(--dress)" transform="rotate(18 174 146)"/>'
         '<g transform="rotate(-14 120 128)"><circle cx="120" cy="124" r="46" fill="#3a1d20"/><circle cx="120" cy="72" r="22" fill="#3a1d20"/>'
         '<path d="M88 108 Q100 92 118 96" stroke="#6b3b3f" stroke-width="5" fill="none" opacity=".6"/></g>'
         '<ellipse cx="120" cy="170" rx="54" ry="10" style="fill:var(--dress2)" opacity=".35"/></svg></div>')
ZZ = "".join(f'<b class="zz" id="zz{i}" style="left:{430 + i * 22}px;top:{950 - i * 26}px;font-size:{28 + i * 8}px">z</b>' for i in range(3))

# her year of reels: 14 cards across the back wall, each with a red drop-off mark
CARDC = ("#ff9ec7,#f343a2", "#9ad0ff,#4a7de8", "#ffe08a,#f59e3d", "#a8f0c6,#3fb37f", "#d6b8ff,#8a5cf0", "#ffb59e,#ef5d4a", "#9ff0f0,#2fb5c9")
CARD_POS = [(200 + c * 113, 690 + r * 182) for r in range(2) for c in range(7)]
CARDS = ""
for i, (x, y) in enumerate(CARD_POS):
    g = CARDC[i % len(CARDC)]
    CARDS += (f'<div class="card" id="cd{i}" style="left:{x}px;top:{y}px;background:linear-gradient(160deg,{g})"><i></i><u></u><em id="cde{i}"></em></div>'
              f'<i class="pin" id="pn{i}" style="left:{x}px;top:{y}px"></i>')
HEARTS = ""
for i in range(16):
    w = random.randint(26, 46)
    HEARTS += (f'<i class="hrt" id="hr{i}">' + (BUBBLE.format(w=w + 8, h=w) if i % 4 == 3 else HEART.format(w=w, h=int(w * .9), c=random.choice(("#ff4f8b", "#ff7ab0", "#ff2d55", "#ffd27a"))))
               + '</i>')

WORLD = (f'{CHIBI_DEFS}{SHELL}<div class="win">{WIN}</div><i class="sill"></i>{CTR}{CAL}{CORK}{CLOCK}{SLS}'
         f'{CUPS}{STEAM}<div class="dphone"><i id="dps"></i></div>{LAMP}{PLANT}{CARDS}{STAR}{SLEEP}'
         f'<div id="night"></div><i class="glow" id="ringwash"></i><i class="glow" id="ringglow"></i><i class="glow" id="lampglow"></i>'
         f'<i class="glow" id="phglow"></i><div id="daylight"></div><div class="wglow" id="wglow"></div>{SLG}<i class="glow" id="burst"></i>{ZZ}'
         f'<i class="flare" id="flare1" style="top:1040px"></i>{HEARTS}')
BG = '<div class="backdrop"></div><div class="table"></div><div class="dshadow"></div>'
BOKEH = "".join(f'<i style="position:absolute;left:{x}px;top:{y}px;width:{r}px;height:{r}px;border-radius:50%;background:{c};opacity:.55"></i>'
                for x, y, r, c in ((-60, 1640, 160, "#ff9ec7"), (930, 1600, 190, "#ffd27a"), (120, 1760, 120, "#ffd27a"), (820, 1790, 140, "#ff7ab0")))
FG = f'<div id="bokeh" style="position:absolute;inset:0;filter:blur(18px);opacity:.25">{BOKEH}</div>'

# =======================================================================================================================
# TIMELINE
OPEN_CAM = (540, 1010, 1.1)
cam(0, *OPEN_CAM, setonly=True)


def her(t, cx, feet, s=1.0):
    st("#star", t, f"{{x: {cx - 95:.0f}, y: {feet - 340:.0f}, scale: {s}}}")


def mouth(t, m):
    for k in ("open", "sad", "wow", "smile"):
        st(f"#sm_{k}", t, f"{{opacity: {1 if k == m else 0}}}")


def arm(t, a, d=0.0):
    if d:
        js(f'tl.to("#sarm", {{rotation: {a}, svgOrigin: "136 176", duration: {d}, ease: "power2.inOut"}}, {t:.3f});')
    else:
        js(f'tl.set("#sarm", {{rotation: {a}, svgOrigin: "136 176"}}, {t:.3f});')


OUTFIT = {"W": ("#6f9cf0", "#3f68c8", 1, 0), "Sp": ("#ff8ec4", "#e2559c", 0, 0), "Su": ("#ffd25a", "#e8a530", 0, 0), "Au": ("#e8763c", "#b9542a", 0, 1)}


def season(t, k):
    for sid in ("sW", "sSp", "sSu", "sAu"):
        st(f"#{sid}", t, f"{{opacity: {1 if sid == 's' + k else 0}}}")
    d, d2, scarf, hood = OUTFIT[k]
    st("#star", t, f'{{"--dress": "{d}", "--dress2": "{d2}"}}')
    st("#sscarf", t, f"{{opacity: {scarf}}}")
    st("#shood", t, f"{{opacity: {hood}}}")


def nightlight(t, on, d=0.0):
    """on: night (dark room, ring light lit, night sky in the window); off: day (window light pours in)"""
    v = (".72", "1", ".82", "0", "0") if on else (".1", "0", "0", ".9", ".8")
    for sel, val in zip(("#night", "#ringglow", "#sN", "#daylight", "#wglow"), v):
        (to(sel, t, d, f"{{opacity: {val}}}", "power1.inOut") if d else st(sel, t, f"{{opacity: {val}}}"))
    (to("#ringwash", t, d, f"{{opacity: {'.9' if on else '0'}}}") if d else st("#ringwash", t, f"{{opacity: {'.9' if on else '0'}}}"))
    st("#ringtube", t, f"{{opacity: {1 if on else .35}}}")


# ambience that runs the whole film: falling snow, petals, leaves; stars twinkle; steam
for cls, n, fall, sway, dmin, dmax in (("sn", 18, 260, 20, 2.4, 4.0), ("pe", 12, 260, 60, 2.6, 3.6), ("lf", 12, 260, 70, 2.2, 3.2)):
    for i in range(n):
        d = random.uniform(dmin, dmax)
        js(f'tl.fromTo("#{cls}{i}", {{y: {-20 - random.uniform(0, 240):.0f}, x: 0, rotation: 0}}, {{y: {fall}, x: {random.randint(-sway, sway)}, rotation: {random.randint(-300, 300)}, duration: {d:.2f}, '
           f'repeat: {int(DUR / d) + 1}, ease: "none"}}, 0);')
for i in range(14):
    js(f'tl.fromTo("#stx{i}", {{opacity: 1}}, {{opacity: .2, duration: {random.uniform(.5, 1.2):.2f}, yoyo: true, repeat: {int(DUR)}, ease: "sine.inOut", immediateRender: false}}, {random.uniform(0, 1):.2f});')

# ---- 0 hook: night, snow, Day 1, the ring light clicks on ----------------------------------------------------------------------
season(0, "W")
nightlight(0, True)
st("#ringglow", 0, "{opacity: 0}")
st("#ringwash", 0, "{opacity: 0}")
st("#ringtube", 0, "{opacity: .35}")
her(0, 600, 1360)
mouth(0, "open")
arm(0, 0)
t_ring = .25
ft("#ringglow", t_ring, .12, "{opacity: 0}", "{opacity: 1}", "power4.in")
ft("#ringwash", t_ring, .12, "{opacity: 0}", "{opacity: .9}", "power4.in")
st("#ringtube", t_ring, "{opacity: 1}")
sfx("click", t_ring)
cam(.3, 540, 1000, 1.18, 3.0, "sine.inOut")
head("h0", [[("365", "it"), ("days.", "")], [("One", ""), ("room.", "")]], 250, "g0", size=128)

# ---- 1 a year in fast-forward -------------------------------------------------------------------------------------------------
t_y0, t_y1 = T0["g1"][0] - .05, T0["g1"][1] - .1
cam(t_y0 - .15, 540, 1010, 1.0, .5, "power3.out")
sfx("whoosh_big", t_y0 - .15)
head("h1a", [[("She", ""), ("posted", "")], [("through", ""), ("the", ""), ("snow,", "")]], 250, "g1", size=96)
head("h1b", [[("the", ""), ("spring,", ""), ("the", ""), ("summer…", "")], [("every", ""), ("single", ""), ("night.", "au")]], 250, "g1", size=88, after=T("g1", "spring") - .1)
SEAS_T = [(t_y0, "W"), (T("g1", "spring") - .1, "Sp"), (T("g1", "summer") - .1, "Su"), (T("g1", "every") - .05, "Au"), (t_y1 - .45, "W")]
for t, k in SEAS_T[1:]:
    season(t, k)
    sfx("swish", t)
SPOTS = [(600, 1360, 1.0, 0), (340, 1300, .92, 58), (905, 1395, 1.02, 30)]
STEP = .36
n = int((t_y1 - t_y0) / STEP)
order = [0, 1, 0, 2, 1, 0, 1, 2, 0, 1, 0, 2, 1, 0, 2, 1, 0]
for k in range(n):
    t = t_y0 + k * STEP
    cx, feet, s, a = SPOTS[order[k % len(order)]]
    her(t, cx, feet, s)
    arm(t, a)
    nightlight(t, k % 2 == 1)
    sfx("tick", t)
nightlight(t_y1, True)
her(t_y1, 340, 1300, .92)
arm(t_y1, 58)
# the calendar races Jan 1 to Dec 31, season by season
MONTHS = '["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]'
DAYS = [(SEAS_T[0][0], 1), (SEAS_T[1][0], 60), (SEAS_T[2][0], 152), (SEAS_T[3][0], 244), (SEAS_T[4][0], 335), (t_y1, 365)]
for (a, va), (b, vb) in zip(DAYS, DAYS[1:]):
    counter(a, b, va, vb, f'const d = Math.round(v); document.getElementById("cday").textContent = d; '
                          f'document.getElementById("cmon").textContent = {MONTHS}[Math.min(11, Math.floor((d - 1) / 30.42))];')
for i in range(7):
    ft(f"#cup{i}", t_y0 + .3 + i * (t_y1 - t_y0 - .6) / 7, .2, "{opacity: 0, y: -16}", "{opacity: 1, y: 0}", "back.out(2.5)")
for i in range(2):
    js(f'tl.fromTo("#stm{i}", {{opacity: 0, y: 0, scaleY: .6}}, {{keyframes: [{{opacity: .6, y: -14, scaleY: 1, duration: .6}}, {{opacity: 0, y: -30, duration: .6}}], '
       f'repeat: {int(DUR / 1.2)}, ease: "sine.inOut", immediateRender: false}}, {t_y1 + .3 * i:.2f});')
ft("#plant", t_y0, t_y1 - t_y0, "{scaleY: .45, scaleX: .7}", "{scaleY: 1.08, scaleX: 1}", "none")
for i in range(6):
    ft(f"#lv{i}", t_y0 + .5 + i * .8, .3, "{opacity: 0, scale: 0, transformOrigin: '50% 50%'}", "{opacity: 1, scale: 1}", "back.out(2)")
js(f'tl.set("#ck1", {{textContent: "9:00 PM"}}, 0);')

# ---- 2 the number on the wall never moved -------------------------------------------------------------------------------------
t_nm = T("g2", "number")
head("h2", [[("And", ""), ("the", ""), ("number", ""), ("on", "")], [("her", ""), ("wall", ""), ("never", ""), ("moved.", "dim")]], 250, "g2", size=92)
cam(T0["g2"][0] - .2, 330, 760, 1.9, 1.5, "power2.inOut")
mouth(T0["g2"][0], "sad")
for k, tt in enumerate((T("g2", "never") - .1, T("g2", "never") + .35, T("g2", "moved") + .1)):
    st("#c48", tt, "{opacity: 1}")
    st("#c47", tt, "{opacity: 0}")
    st("#c48", tt + .1, "{opacity: 0}")
    st("#c47", tt + .1, "{opacity: 1}")
    sfx("tick", tt)
sfx("error", T("g2", "moved"))

# ---- 3 3 a.m., asleep at the desk -----------------------------------------------------------------------------------------------
t_3 = T0["g3"][0]
head("h3a", [[("She", ""), ("didn't", ""), ("need", ""), ("another", "")], [("year", ""), ("of", ""), ("trying.", "dim")]], 250, "g3", size=92)
cam(t_3 - .3, 360, 1030, 1.55, 1.1)
cam(t_3 + .9, 370, 1030, 1.68, T0["g4"][0] - t_3 - 1.2, "none")
st("#star", t_3 - .3, "{opacity: 0}")
st("#sleep", t_3 - .3, "{opacity: 1}")
st("#clk", t_3 - .3, "{opacity: 0}")
st("#clk3", t_3 - .3, "{opacity: 1}")
ft("#phglow", t_3 - .3, .6, "{opacity: 0}", "{opacity: .55}", "power1.out")
to("#ringglow", t_3 - .3, .6, "{opacity: 0}")
to("#ringwash", t_3 - .3, .6, "{opacity: 0}")
st("#ringtube", t_3 - .3, "{opacity: .35}")
to("#night", t_3 - .3, .6, "{opacity: .82}")
js(f'tl.fromTo("#sleep svg", {{scaleY: 1}}, {{scaleY: 1.02, duration: 1.1, yoyo: true, repeat: 3, ease: "sine.inOut", transformOrigin: "50% 100%", immediateRender: false}}, {t_3:.3f});')
for i in range(3):
    js(f'tl.fromTo("#zz{i}", {{opacity: 0, y: 10, x: 0}}, {{keyframes: [{{opacity: 1, y: -10, x: 6, duration: .7}}, {{opacity: 0, y: -40, x: 14, duration: .7}}], '
       f'repeat: 1, immediateRender: false}}, {t_3 + .3 + i * .45:.3f});')
t_ne = T("g3", "needed")
head("h3b", [[("She", ""), ("needed", ""), ("to", "")], [("know", ""), ("why.", "it")]], 250, "g3", size=124, after=t_ne - .2)
js(f'tl.fromTo("#dps", {{opacity: .25}}, {{opacity: .9, duration: .2, yoyo: true, repeat: 3, immediateRender: false}}, {T("g3", "why") - .1:.3f});')

# ---- 4 the turn: the phone bursts pink, Cree pops out, her year fans out across the wall ---------------------------------------
t_cr = T("g4", "Creedom")
head("h4a", [[("Creedom", "it"), ("read", ""), ("her", "")], [("whole", ""), ("year", ""), ("of", ""), ("posts,", "")]], 250, "g4", size=96)
sfx("riser", t_cr - 1.0)
ft("#burst", t_cr - .08, .2, "{opacity: 0, scale: .2}", "{opacity: 1, scale: 1.2}", "power3.out")
to("#burst", t_cr + .25, .7, "{opacity: 0, scale: 1.6}", "power2.in")
ft("#flare1", t_cr - .05, .3, "{opacity: 0, scaleX: .1}", "{opacity: 1, scaleX: 1}", "power3.out")
to("#flare1", t_cr + .45, .9, "{opacity: 0, scaleX: 1.4}", "power2.in")
punch(t_cr, 1.04)
sfx("sparkle", t_cr - .05)
cam(t_cr - .05, 540, 1000, 1.02, .7, "power3.out")
st("#sleep", t_cr, "{opacity: 0}")
st("#star", t_cr, "{opacity: 1}")
her(t_cr, 600, 1335, .97)
season(t_cr, "Au")
st("#sscarf", t_cr, "{opacity: 0}")
mouth(t_cr, "wow")
arm(t_cr, 58)
js(f'tl.fromTo("#star", {{y: "+=0"}}, {{keyframes: [{{y: "-=30", duration: .14, ease: "power2.out"}}, {{y: "+=30", duration: .2, ease: "bounce.out"}}], immediateRender: false}}, {t_cr:.3f});')
to("#night", t_cr, 1.0, "{opacity: .38}", "power1.inOut")
ft("#lampglow", t_cr + .1, .4, "{opacity: 0}", "{opacity: .8}", "power2.out")
to("#phglow", t_cr, .4, "{opacity: .9}")
st("#clk3", t_cr, "{opacity: 0}")
CF = (475, 1080, .2)                                     # Cree on the desk, right of the phone
cree_to(t_cr - .1, *P(433, 1060, .04), d=.01)
st("#cree", t_cr - .05, "{opacity: 1}")
pose(t_cr - .05, "cheer", flip=False, squash=False)
cree_to(t_cr, *P(*CF), d=.45, ease="back.out(1.8)")
js(f'tl.fromTo("#creeb", {{y: 0}}, {{keyframes: [{{y: -90, duration: .22, ease: "power2.out"}}, {{y: 0, duration: .25, ease: "bounce.out"}}], immediateRender: false}}, {t_cr:.3f});')
sparkle(t_cr + .1, .8)
t_rd = T("g4", "read")
pose(t_rd, "point", flip=True)
for i, (x, y) in enumerate(CARD_POS):
    tk = t_rd + .05 + i * .1
    ft(f"#cd{i}", tk, .45, f"{{opacity: 0, x: {433 - x}, y: {1040 - y}, scale: .15, rotation: {random.randint(-90, 90)}}}",
       f"{{opacity: 1, x: 0, y: 0, scale: 1, rotation: {random.uniform(-6, 6):.1f}}}", "back.out(1.4)")
    if i % 2 == 0:
        sfx("flip", tk)
st("#sm_wow", t_rd + .6, "{opacity: 0}")
st("#sm_open", t_rd + .6, "{opacity: 1}")
js(f'tl.to("#shead", {{rotation: -6, svgOrigin: "95 140", duration: .5, ease: "sine.inOut"}}, {t_rd + .3:.3f});')
t_sh = T("g4", "showed")
t_ex = T("g4", "exact")
head("h4b", [[("and", ""), ("showed", ""), ("her", ""), ("the", "")], [("exact", ""), ("second", ""), ("people", ""), ("left.", "rd")]], 250, "g4", size=88, after=T("g4", "and"))
for i in range(len(CARD_POS)):
    tk = t_ex - .1 + i * .045
    ft(f"#cde{i}", tk, .2, "{opacity: 0, scaleX: .2}", "{opacity: 1, scaleX: 1}", "back.out(3)")
    ft(f"#pn{i}", tk, .25, "{opacity: 0, y: -30, scale: 1.6}", "{opacity: 1, y: 0, scale: 1}", "bounce.out")
    if i % 3 == 0:
        sfx("tick", tk)
ZC = CARD_POS[9]
t_zm = T("g4", "second") - .15
cam(t_zm, ZC[0], ZC[1] + 40, 2.3, .7, "power3.inOut")
ft("#callout", t_zm + .45, .3, "{opacity: 0, scale: .6, y: 20}", "{opacity: 1, scale: 1, y: 0}", "back.out(2.4)")
sfx("error", t_zm + .5)
js(f'tl.to("#shead", {{rotation: 0, svgOrigin: "95 140", duration: .4}}, {t_zm:.3f});')
to("#callout", T0["g4"][1] + .15, .2, "{opacity: 0}")

# ---- 5 the reel check, folded into the phone ---------------------------------------------------------------------------------------
t_sc = T("g5", "scored")
t_nx = T0["g6"][0]
head("h5", [[("It", ""), ("scored", "it"), ("her", ""), ("next", ""), ("reel", "")], [("before", ""), ("she", ""), ("hit", ""), ("post.", "")]], 250, "g5", size=88)
cam(T0["g5"][0] - .3, 540, 1010, 1.0, .7)
for i, (x, y) in enumerate(CARD_POS):
    to(f"#cd{i}", T0["g5"][0] - .3 + i * .02, .35, f"{{opacity: 0, x: {433 - x}, y: {1040 - y}, scale: .15}}", "power2.in")
    to(f"#pn{i}", T0["g5"][0] - .3 + i * .02, .2, "{opacity: 0}")
sfx("whoosh", T0["g5"][0] - .3)
pose(T0["g5"][0], "mag", flip=True)
ft("#ana", t_sc, .5, "{opacity: 0, scale: .25, y: 300}", "{opacity: 1, scale: 1, y: 0}", "back.out(1.5)")
sfx("whoosh", t_sc)
for k in range(2):
    ft("#scan", t_sc + .35 + .5 * k, .5, "{y: 0, opacity: 1}", "{y: 400, opacity: 1}", "sine.inOut")
    sfx("glitch", t_sc + .4 + .5 * k)
st("#scan", t_sc + 1.35, "{opacity: 0}")
js(f'tl.fromTo("#adots", {{opacity: 1}}, {{opacity: .2, duration: .25, yoyo: true, repeat: 3, ease: "none", immediateRender: false}}, {t_sc + .2:.3f});')
T_SC = t_sc + .8
js(f'(() => {{ const sc = {{v: 0}}; tl.to(sc, {{v: 4.7, duration: 1.1, ease: "power2.out", onUpdate: () => {{ document.getElementById("scn").textContent = sc.v.toFixed(1); }}}}, {T_SC:.3f}); }})();')
for i in range(6):
    tk = T_SC + .1 + .16 * i
    ft(f"#ch{i}", tk, .28, "{opacity: 0, scale: .6, y: 16}", "{opacity: 1, scale: 1, y: 0}", "back.out(2.6)")
    sfx("tick", tk)
t_vg = T_SC + 1.15
ft("#avg", t_vg, .3, "{opacity: 0, x: -20}", "{opacity: 1, x: 0}", "power3.out")
js(f'tl.fromTo("#abar", {{width: "0%"}}, {{width: "94%", duration: .5, ease: "power3.out", immediateRender: false}}, {t_vg:.3f});')
to("#ahd1", t_vg, .2, "{opacity: 0}")
ft("#ahd2", t_vg + .05, .25, "{opacity: 0}", "{opacity: 1}", "power2.out")
ft("#atk", t_vg + .05, .3, "{opacity: 0, scale: .4}", "{opacity: 1, scale: 1}", "back.out(3)")
js(f'tl.fromTo("#ascore", {{scale: 1}}, {{scale: 1.12, duration: .16, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false}}, {t_vg:.3f});')
sfx("ding2", t_vg)
mouth(t_vg, "smile")
pose(t_vg, "cheer")
sparkle(t_vg, .6)
t_fd = t_nx - .6
to("#ana", t_fd, .4, "{opacity: 0, scale: .2, y: 360}", "power3.in")
sfx("whoosh", t_fd)
js(f'tl.fromTo("#dps", {{opacity: .25}}, {{opacity: 1, duration: .12, yoyo: true, repeat: 1, immediateRender: false}}, {t_fd + .38:.3f});')
sfx("ding", t_fd + .4)

# ---- 6 same room, same girl, completely different night ----------------------------------------------------------------------------
t_sr = T("g6", "Same")
t_sg = T("g6", "girl") - .2
t_cd = T("g6", "Completely")
head("h6a", [[("Same", ""), ("room.", "")], [("Same", ""), ("girl.", "")]], 250, "g6", size=124)
head("h6b", [[("Completely", "au")], [("different", ""), ("night.", "")]], 250, "g6", size=120, after=t_cd)
cam(t_sr - .3, *OPEN_CAM, .8, "power3.inOut")
cam(t_sr + .55, 540, 1000, 1.18, t_cd - t_sr - .7, "sine.inOut")
sfx("whoosh_big", t_sr - .3)
her(t_sr - .3, 600, 1360)
arm(t_sr - .3, 0)
season(t_sr - .3, "W")
st("#sscarf", t_sr - .3, "{opacity: 0}")
st("#star", t_sr - .3, '{"--dress": "#ff8ec4", "--dress2": "#e2559c"}')
mouth(t_sr - .3, "smile")
st("#ringtube", t_sr - .3, "{opacity: 1}")
ft("#ringglow", t_sr - .2, .12, "{opacity: 0}", "{opacity: 1}", "power4.in")
ft("#ringwash", t_sr - .2, .12, "{opacity: 0}", "{opacity: .9}", "power4.in")
sfx("click", t_sr - .2)
st("#clk", t_sr - .3, "{opacity: 1}")
cree_to(t_sr - .3, *P(470, 1080, .2), d=.01)
pose(t_sr - .3, "wave", flip=False)
# warm night: string lights, lamp, the room glows; the counter starts spinning
js(f'tl.to("#night", {{opacity: .3, backgroundColor: "#ff9a6a", duration: .8, ease: "power1.inOut"}}, {t_sr - .3:.3f});')
for i in range(len(SLX)):
    tk = t_sr + i * .04
    st(f"#sl{i}", tk, '{backgroundColor: "#ffe7a8"}')
    st(f"#slg{i}", tk, "{opacity: 1}")
js(f'tl.to(".slglow", {{opacity: .45, duration: .3, yoyo: true, repeat: 9, stagger: {{each: .05, from: "random"}}, ease: "sine.inOut"}}, {t_sr + 1.0:.3f});')
st("#c47", t_sg, "{opacity: 0}")
st("#cspin", t_sg, "{opacity: 1}")
counter(t_sg, T0["g7"][0] - .1, 0, 1, 'document.getElementById("cspin").textContent = String(10000 + Math.floor(v * 977777 * 7919) % 89999);')
js(f'tl.fromTo("#cspin", {{filter: "blur(0px)"}}, {{filter: "blur(3.5px)", duration: .4, immediateRender: false}}, {t_sg:.3f});')
sfx("coin", t_sg)
pose(t_sg, "cheer")
cree_hop(t_sg + .1, 50, 3)
js(f'tl.to("#slarm", {{rotation: -120, svgOrigin: "50 180", duration: .3, ease: "back.out(2)"}}, {t_sg:.3f});')
# hearts and comments float up from her phone
for i in range(16):
    tk = t_sg + .1 + i * .32
    x0, y0 = 650 + random.randint(-20, 20), 1080
    js(f'tl.fromTo("#hr{i}", {{x: {x0}, y: {y0}, opacity: 0, scale: .4}}, {{keyframes: [{{opacity: 1, scale: 1, y: {y0 - 120}, x: {x0 + random.randint(-60, 60)}, duration: .5}}, '
       f'{{opacity: 0, y: {y0 - 420}, x: {x0 + random.randint(-160, 160)}, duration: 1.4, ease: "power1.in"}}], immediateRender: false}}, {tk:.3f});')
    if i % 3 == 0:
        sfx("ping", tk)
# completely different night: fans cheer in the window, the window glows
ft("#fans", t_cd - .1, .4, "{opacity: 0, y: 40}", "{opacity: 1, y: 0}", "back.out(1.6)")
js(f'tl.fromTo("#fans .cbs", {{y: 0}}, {{y: -6, duration: .22, yoyo: true, repeat: 15, ease: "sine.inOut", stagger: .07, immediateRender: false}}, {t_cd + .2:.3f});')
to("#wglow", t_cd, .6, "{opacity: .9}")
sfx("applause", t_cd - .1)
sfx("bell", t_cd)
punch(t_cd, 1.03)
js(f'tl.fromTo("#bokeh", {{opacity: .25}}, {{opacity: .7, duration: 1.2, immediateRender: false}}, {t_cd:.3f});')

# ---- 7 CTA: the counter turns into COMMENT GROW ----------------------------------------------------------------------------------
t_cm = T("g7", "Comment")
t_gw = T("g7", "GROW")
head("h7", [[("and", ""), ("I'll", ""), ("send", ""), ("you", "")], [("the", ""), ("secret.", "it")]], 250, "g7", size=96, after=T("g7", "and"))
cam(t_cm - .3, 390, 820, 1.6, .9, "power3.inOut")
to("#cspin", t_cm - .1, .15, "{opacity: 0}")
to("#clab", t_cm - .1, .15, "{opacity: 0}")
ft("#clab2", t_cm, .25, "{opacity: 0, y: -10}", "{opacity: 1, y: 0}", "power3.out")
ft("#cgrow", t_gw - .05, .35, "{opacity: 0, scale: 1.6}", "{opacity: 1, scale: 1}", "back.out(2)")
js(f'tl.fromTo("#cgrow", {{scale: 1}}, {{scale: 1.06, duration: .4, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {t_gw + .5:.3f});')
sfx("click", t_cm)
sfx("ding", t_gw)
punch(t_gw, 1.04)

# ---- cinema pass: letterbox and cold grade in the lonely year; both lift at "Creedom" ------------------------------------------------
st("#lbT", 0, "{scaleY: 1}")
st("#lbB", 0, "{scaleY: 1}")
to("#lbT", t_cr - .1, .9, "{scaleY: 0}", "power3.inOut")
to("#lbB", t_cr - .1, .9, "{scaleY: 0}", "power3.inOut")
to("#cold", t_cr, 1.2, "{opacity: .3}", "power1.inOut")
to("#warmg", t_cr, 1.2, "{opacity: .45}", "power1.inOut")
to("#cold", t_sr - .3, .8, "{opacity: 0}", "power1.inOut")
to("#warmg", t_sr - .3, .8, "{opacity: .9}", "power1.inOut")
js(f'tl.fromTo("#creep", {{y: 0}}, {{y: -6, duration: .7, ease: "sine.inOut", yoyo: true, repeat: {int(DUR / .7)}, immediateRender: false}}, 0);')
js(f'tl.fromTo("#hand", {{x: -4, y: 3}}, {{x: 4, y: -3, duration: 3.7, yoyo: true, repeat: {int(DUR / 3.7)}, ease: "sine.inOut", immediateRender: false}}, 0);')

CHIPS = [("Hook", 5), ("Pacing", 4), ("Ending", 5), ("Visuals", 5), ("Audio", 4), ("CTA", 5)]
ANAH = ('<div class="ahd"><img src="assets/img/poses/mag.png" alt=""><span id="ahd1">CREE · CHECKING YOUR REEL<b id="adots">…</b></span>'
        f'<span id="ahd2">CREE · REEL CHECKED</span><i class="atick" id="atk">{TICK}</i></div>'
        '<div class="athumb"><i class="asil"></i><b data-layout-ignore>Your best<br>moment,<br>first.</b><i id="scan"></i>'
        '<i class="abr tl"></i><i class="abr tr"></i><i class="abr bl"></i><i class="abr br"></i></div>'
        '<div class="aright"><div class="alab">REEL SCORE</div><div id="ascore"><span id="scn">0.0</span><small>/ 5</small></div>'
        '<div id="avg">Very good</div><div class="atrack"><i id="abar"></i></div><div class="achips">'
        + "".join(f'<span class="chip" id="ch{i}">{n} <b>{v}</b></span>' for i, (n, v) in enumerate(CHIPS))
        + '</div><div class="aex">Example score</div></div>')
CALLOUT = f'<div id="callout" style="left:{540 - 190}px;top:1190px">LEFT AT 0:02</div>'

WORLD += cree_html()
CSS = open(os.path.join(ROOT, "build", "style.css")).read()
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom: 365 Days in One Room 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div id="punch"><div id="hand">
        <div class="rig" id="rbg" data-layout-allow-overflow>{BG}</div>
        <div class="rig" id="rw" data-layout-allow-overflow data-layout-allow-overlap>{WORLD}</div>
        <div class="rig" id="rfg" data-layout-allow-overflow>{FG}</div>
      </div></div>
      <div id="cold"></div><div id="warmg"></div><div id="vig"></div><div id="black"></div>
      <div id="scrim"></div>
      <div id="ana" data-layout-allow-overlap>{ANAH}</div>{CALLOUT}
      <div id="lbT"></div><div id="lbB"></div>
      {chr(10).join(HTMLS)}
      <div id="grain"></div><div id="flash"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      {chr(10).join("      " + j for j in JS).strip()}
      tl.set({{}}, {{}}, {DUR:.2f});
      tl.progress(1, true).progress(0, true);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(html)
SFX.sort(key=lambda e: e["t"])
json.dump(SFX, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
json.dump({"dur": DUR, "music_switch": round(t_cr, 3), "lines": T0}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx")
