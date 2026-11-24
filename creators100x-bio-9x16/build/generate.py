"""Creators 100X "Your bio is losing you followers" (9:16, 2D marker doodles on notebook paper): writes index.html,
plan/sfx_events.json and plan/edit.json from plan/words.json.
Blueprint: relatable -> conflict -> realisation -> action. A doodled visitor lands on a profile, reads one line of bio and
leaves; the bio is rewritten in four lines (who you help, what they get, proof, what to do next) and the visitor follows.
Everything is SVG drawn on with stroke-dashoffset; the ink "boils" (three displacement filters swapped at 12 fps) like a
hand-drawn stop-motion. The example profile is made up and labelled EXAMPLE.
python3 build/generate.py"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fx import ROOT, LINES, L0, L1, T, JS, SFX, js, sfx, ft, to, st  # noqa: E402
import fx  # noqa: E402

FIRST = {}          # selector -> (t, from-vars) of its earliest entrance, re-applied after the timeline reset


def ft(sel, t, d, frm, to_, ease="power3.out"):
    fx.ft(sel, t, d, frm, to_, ease)
    if "opacity: 1" in frm.replace(" ", " ") and "opacity: 0" not in frm:
        return
    if sel not in FIRST or t < FIRST[sel][0]:
        FIRST[sel] = (t, frm)

random.seed(7)
DUR = round(L1["b5"] + 1.5, 2)
HTML, SVG = [], []
INK, PINK, LIME, RED = "#101111", "#fd0b68", "#ccfb79", "#fd0b68"


# ---------------------------------------------------------------- hand-drawn geometry
def _smooth(pts, closed):
    """Catmull-Rom through the points -> cubic path"""
    n = len(pts)
    if closed:
        P = [pts[-1]] + pts + [pts[0], pts[1]]
    else:
        P = [pts[0]] + pts + [pts[-1]]
    d = f"M{P[1][0]:.1f},{P[1][1]:.1f}"
    rng = range(1, n + (1 if closed else 0)) if closed else range(1, n)
    for i in rng:
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d + (" Z" if closed else "")


def wobble(pts, closed=False, amp=2.0, step=34):
    dense = []
    segs = list(zip(pts, pts[1:] + ([pts[0]] if closed else [])))
    for (x0, y0), (x1, y1) in segs:
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(L / step))
        for k in range(n):
            dense.append((x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n))
    if not closed:
        dense.append(pts[-1])
    dense = [(x + random.uniform(-amp, amp), y + random.uniform(-amp, amp)) for x, y in dense]
    return _smooth(dense, closed)


def rrect_pts(x, y, w, h, r):
    pts = []
    for cx, cy, a0 in ((x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)):
        for k in range(5):
            a = math.radians(a0 + k * 22.5)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def rrect(x, y, w, h, r, amp=1.6):
    return wobble(rrect_pts(x, y, w, h, r), True, amp)


def loop(cx, cy, rx, ry, turns=1.12, amp=2.5, a0=-100):
    n = int(28 * turns)
    pts = [(cx + rx * (1 + random.uniform(-.03, .03)) * math.cos(math.radians(a0 + 360 * turns * k / n)),
            cy + ry * (1 + random.uniform(-.04, .04)) * math.sin(math.radians(a0 + 360 * turns * k / n))) for k in range(n + 1)]
    return _smooth(pts, False)


def line(x0, y0, x1, y1, amp=1.5):
    return wobble([(x0, y0), (x1, y1)], False, amp)


def P(pid, d, w=6, col=INK, fill="none", extra=""):
    """an ink stroke that can be drawn on (pathLength 1)"""
    return f'<path id="{pid}" d="{d}" pathLength="1" stroke="{col}" stroke-width="{w}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def draw(sel, t, d=.35, ease="power2.inOut"):
    ft(sel, t, d, "{strokeDasharray: 1, strokeDashoffset: 1}", "{strokeDasharray: 1, strokeDashoffset: 0}", ease)


def hide_until(sel, t):
    js(f'gsap.set("{sel}", {{opacity: 0}});')
    st(sel, t, "{opacity: 1}")


def pop(sel, t, d=.32, frm="{opacity: 0, scale: .3}", ease="back.out(2.6)"):
    ft(sel, t, d, frm, "{opacity: 1, scale: 1, rotation: 0}", ease)


def wipe(cid, t, w, d=.35):
    """reveal clipped handwriting left to right"""
    ft(f"#{cid} rect", t, d, "{attr: {width: 0}}", f"{{attr: {{width: {w}}}}}", "power1.inOut")


TXT = lambda x, y, s, size=44, font="Kalam", col=INK, extra="": (f'<text x="{x}" y="{y}" font-family="{font}" font-weight="700" font-size="{size}" '
                                                              f'fill="{col}" {extra}>{s}</text>')
CLIP = []


def clipped(cid, x, y, w, h, inner):
    CLIP.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="0" height="{h}"/></clipPath>')
    return f'<g clip-path="url(#{cid})">{inner}</g>'


# ---------------------------------------------------------------- word times
t_visit, t_read, t_leave, t_that, t_bio = T("b0", "visit"), T("b0", "read"), T("b0", "leave"), T("b0", "That"), T("b0", "bio")
t_living, t_dm, t_tells, t_nothing = L0["b1"], T("b1", "DM"), T("b1", "Tells"), T("b1", "nothing")
t_they, t_you2, t_they2, t_get = L0["b2"], LINES["b2"][5]["t0"], LINES["b2"][6]["t0"], T("b2", "get")   # the 2nd "you." and the 2nd "They"
t_so, t_four = L0["b3"], T("b3", "four")
ITEMS = [T("b3", "Who"), T("b3", "What"), T("b3", "Proof"), T("b3", "And")]
t_same, t_now, t_follow = L0["b4"], T("b4", "Now"), T("b4", "follow")
t_comment, t_bioW, t_send, t_formula, t_fifteen = L0["b5"], T("b5", "BIO"), T("b5", "send"), T("b5", "formula"), T("b5", "fifteen")

# ---------------------------------------------------------------- the paper
SVG.append(f'<rect x="0" y="0" width="1080" height="1920" fill="#fdf8f4"/>')
for k in range(28):
    y = 120 + k * 64
    SVG.append(f'<path d="{line(0, y, 1080, y, .8)}" stroke="#b9c7dd" stroke-width="2" opacity=".45" fill="none"/>')
SVG.append(f'<path d="{line(92, 0, 92, 1920, .8)}" stroke="#f59ab8" stroke-width="3" opacity=".7" fill="none"/>')

INKS = []          # everything that boils
# ---------------------------------------------------------------- the profile card
CX0, CY0, CW, CH = 110, 560, 860, 900
INKS.append(f'<path id="cardfill" d="{rrect(CX0, CY0, CW, CH, 54)}" fill="#ffffff" stroke="none"/>')
INKS.append(P("card", rrect(CX0, CY0, CW, CH, 54), 7))
INKS.append(f'<circle id="avfill" cx="250" cy="700" r="76" fill="{LIME}"/>')
INKS.append(P("av", loop(250, 700, 78, 78), 6))
INKS.append(P("pan", loop(240, 708, 30, 30, 1.0, 1.2) + " " + line(266, 690, 300, 662, 1), 5))
INKS.append(f'<g id="handle">{TXT(355, 688, "@maya.cooks", 50)}</g>')
INKS.append(f'<g id="stats">{TXT(357, 752, "84 posts", 32, col="#555")}{TXT(527, 752, "<tspan id=fol>1,204</tspan> followers", 32, col="#555")}</g>')
INKS.append(f'<g id="ex"><rect x="790" y="590" width="150" height="44" rx="22" fill="{INK}"/>{TXT(812, 622, "EXAMPLE", 28, "Caveat", LIME)}</g>')
# old bio
INKS.append(f'<g id="oldbio">{TXT(160, 870, "Living my best life", 56)}{TXT(160, 942, "DM for collabs", 56)}</g>')
INKS.append(P("oldscrib", wobble([(150, 870), (640, 850), (160, 900), (650, 880), (170, 930), (560, 910), (160, 955), (520, 940)], False, 3, 60), 10, INK))
INKS.append(P("redloop", loop(415, 895, 320, 95, 1.15, 3), 8, RED))
INKS.append(f'<g id="qmark">{TXT(800, 1000, "?", 170, "Caveat", RED)}</g>')
# new bio: four lines with number tags and highlighter
NEW = ["Cheap meals for busy students", "15-minute, one-pan recipes", "40K students cook with me", "New recipe every Tuesday"]
for i, s in enumerate(NEW):
    y = 842 + i * 58
    hl = {0: (546, 264, LIME), 2: (214, 82, "#ffb3d1")}.get(i)
    inner = ""
    if hl:
        inner += f'<rect id="hl{i}" x="{hl[0]}" y="{y - 34}" width="{hl[1]}" height="42" rx="8" fill="{hl[2]}" opacity=".95"/>'
    inner += TXT(214, y, s, 42)
    INKS.append(clipped(f"nb{i}", 200, y - 50, 760, 70, inner))
    INKS.append(f'<g id="tag{i}"><circle cx="172" cy="{y - 14}" r="22" fill="{INK}"/>{TXT(163, y - 2, str(i + 1), 34, "Caveat", LIME)}</g>')
INKS.append(P("arrow4", wobble([(735, 1002), (770, 1030), (760, 1060)], False, 1) + " " + line(744, 1050, 760, 1062, .5) + " " + line(776, 1046, 760, 1062, .5), 5))
# follow button
INKS.append(f'<path id="fbfill" d="{rrect(170, 1080, 740, 92, 46)}" fill="{PINK}" opacity="0"/>')
INKS.append(P("fb", rrect(170, 1080, 740, 92, 46), 6))
INKS.append(f'<g id="fbt0">{TXT(470, 1142, "Follow", 50)}</g><g id="fbt1" opacity="0">{TXT(430, 1142, "Following", 50, col="#fff")}</g>')
# post grid
ICON = [lambda x, y: loop(x, y, 26, 26, 1.0, 1) + " " + line(x + 20, y - 18, x + 50, y - 44, 1),
        lambda x, y: wobble([(x - 40, y - 8), (x + 40, y - 8)], False, 1) + " " + wobble([(x - 40, y - 8), (x - 26, y + 22), (x + 26, y + 22), (x + 40, y - 8)], False, 1),
        lambda x, y: loop(x, y, 30, 30, 1.0, 1) + " " + line(x, y, x, y - 20, .5) + " " + line(x, y, x + 15, y + 6, .5),
        lambda x, y: loop(x, y + 4, 22, 30, 1.0, 1) + " " + loop(x, y + 10, 10, 10, 1.0, .5),
        lambda x, y: wobble([(x - 8, y - 30), (x + 8, y - 30), (x + 14, y + 28), (x - 14, y + 28)], True, 1),
        lambda x, y: wobble([(x - 28, y - 20), (x + 20, y - 20), (x + 16, y + 26), (x - 24, y + 26)], True, 1) + " " + loop(x + 30, y, 10, 12, 1.0, .5)]
for k in range(6):
    gx, gy = 150 + (k % 3) * 265, 1206 + (k // 3) * 126
    col = ("#eaffc9", "#ffe0ec", "#fff1d6")[k % 3]
    INKS.append(f'<path id="gf{k}" d="{rrect(gx, gy, 250, 112, 18, 1)}" fill="{col}"/>')
    INKS.append(P(f"g{k}", rrect(gx, gy, 250, 112, 18, 1), 5))
    INKS.append(P(f"gi{k}", ICON[k](gx + 125, gy + 58), 4.5))

# sticky "YOUR BIO" + arrow to the bio
INKS.append(f'<g transform="rotate(-6 790 1250)"><g id="sticky1"><rect x="660" y="1180" width="270" height="150" fill="#fff27a"/>'
            f'{TXT(688, 1270, "YOUR BIO", 62, "Caveat")}</g></g>')
INKS.append(P("arr1", wobble([(700, 1180), (640, 1080), (600, 990)], False, 2), 7) + P("arr1h", wobble([(574, 1012), (600, 985), (618, 1018)], False, 1), 7))
# sticky "about YOU" -> X
INKS.append(f'<g transform="rotate(5 800 900)"><g id="sticky2"><rect x="690" y="830" width="230" height="130" fill="#ffd6e7"/>'
            f'{TXT(712, 890, "all about", 40, "Caveat")}{TXT(712, 940, "YOU", 58, "Caveat", PINK)}</g></g>')
INKS.append(P("xx", line(690, 830, 920, 960, 3) + " " + line(920, 830, 690, 960, 3), 9, RED))

# ---------------------------------------------------------------- the visitor (bottom left) and the bolt (bottom right)
VX, VY = 250, 1850
VIS = f'''<g transform="translate({VX} {VY})"><g id="vis"><g id="visb">
  <path id="legL" d="{line(-22, -120, -34, 0, 1)}" stroke="{INK}" stroke-width="9" stroke-linecap="round" fill="none"/>
  <path id="legR" d="{line(22, -120, 34, 0, 1)}" stroke="{INK}" stroke-width="9" stroke-linecap="round" fill="none"/>
  <path d="{rrect(-62, -250, 124, 145, 40)}" fill="#ff8ac0" stroke="{INK}" stroke-width="7"/>
  <g id="armsN"><path d="{wobble([(-58, -220), (-92, -160), (-80, -110)], False, 1)}" stroke="{INK}" stroke-width="9" stroke-linecap="round" fill="none"/>
    <path id="armR" d="{wobble([(58, -220), (92, -160), (80, -110)], False, 1)}" stroke="{INK}" stroke-width="9" stroke-linecap="round" fill="none"/></g>
  <g id="armsS" opacity="0"><path d="{wobble([(-58, -220), (-110, -230), (-120, -290)], False, 1)}" stroke="{INK}" stroke-width="9" stroke-linecap="round" fill="none"/>
    <path d="{wobble([(58, -220), (110, -230), (120, -290)], False, 1)}" stroke="{INK}" stroke-width="9" stroke-linecap="round" fill="none"/></g>
  <circle cx="0" cy="-322" r="78" fill="#fff4ea" stroke="{INK}" stroke-width="7"/>
  <g id="eyes"><ellipse cx="-28" cy="-332" rx="20" ry="24" fill="#fff" stroke="{INK}" stroke-width="5"/><ellipse cx="28" cy="-332" rx="20" ry="24" fill="#fff" stroke="{INK}" stroke-width="5"/>
    <g id="pup"><circle cx="-24" cy="-328" r="9" fill="{INK}"/><circle cx="32" cy="-328" r="9" fill="{INK}"/></g>
    <path id="lids" d="M-50,-356 L-6,-350 M6,-350 L50,-356" stroke="{INK}" stroke-width="7" stroke-linecap="round" opacity="0"/></g>
  <path id="mN" d="{line(-18, -288, 18, -288, 1)}" stroke="{INK}" stroke-width="6" stroke-linecap="round" fill="none"/>
  <path id="mF" d="M-20,-282 Q0,-298 20,-282" stroke="{INK}" stroke-width="6" stroke-linecap="round" fill="none" opacity="0"/>
  <path id="mH" d="M-26,-294 Q0,-262 26,-294" stroke="{INK}" stroke-width="6" stroke-linecap="round" fill="#fff" opacity="0"/>
</g>
  <g id="vq" opacity="0">{TXT(-20, -430, "?", 110, "Caveat", RED)}</g>
  <g id="vheart" opacity="0"><path d="M0,-410 C-40,-450 -80,-410 0,-360 C80,-410 40,-450 0,-410 Z" fill="{PINK}" stroke="{INK}" stroke-width="5"/></g>
  <g id="vbub" opacity="0"><path d="{rrect(70, -560, 420, 120, 40)}" fill="#fff" stroke="{INK}" stroke-width="6"/>
    <path d="M120,-442 L90,-400 L170,-444" fill="#fff" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>
    {TXT(100, -485, "What do I get?", 54, "Caveat")}</g>
  <g transform="translate(215 -330) scale(1.25)"><g id="watch" opacity="0"><circle r="58" fill="#fff" stroke="{INK}" stroke-width="7"/>
    <rect x="-12" y="-82" width="24" height="18" rx="5" fill="{INK}"/><path id="hand" d="M0,0 L0,-40" stroke="{RED}" stroke-width="7" stroke-linecap="round"/>
    <g id="w1" opacity="0">{TXT(-14, 20, "1", 64, "Caveat")}</g><g id="w2" opacity="0">{TXT(-16, 20, "2", 64, "Caveat")}</g><g id="w3" opacity="0">{TXT(-16, 20, "3", 64, "Caveat", RED)}</g></g></g>
  <g id="puffs" opacity="0"><path d="{line(110, -200, 190, -200, 2)} {line(120, -150, 220, -150, 2)} {line(110, -100, 180, -100, 2)}" stroke="{INK}" stroke-width="6" stroke-linecap="round" fill="none"/></g>
</g></g>'''
BOLT = f'''<g transform="translate(900 1760)"><g id="bolt"><g id="boltb">
  <path d="{rrect(-80, -80, 160, 160, 40, 1.4)}" fill="{INK}" stroke="{INK}" stroke-width="6"/>
  <path d="M10,-56 L-34,4 L-6,4 L-16,58 L32,-8 L4,-8 Z" fill="#fff" stroke="{INK}" stroke-width="3"/>
  <path d="M-34,4 L-6,4 L-16,58 L12,18 Z" fill="{LIME}"/>
  <g id="bsweat" opacity="0"><path d="M92,-60 Q104,-40 92,-30 Q80,-40 92,-60 Z" fill="#7cc8ff" stroke="{INK}" stroke-width="3"/></g>
  <g id="bbang" opacity="0">{TXT(70, -90, "!", 100, "Caveat", RED)}</g>
</g></g></g>'''
HAND = f'''<g id="tapper" opacity="0"><path d="{wobble([(0, 0), (0, -56), (14, -60), (16, -20), (30, -26), (44, -18), (58, -10), (60, 40), (40, 70), (0, 70), (-20, 30)], True, 1)}"
  fill="#fff4ea" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/></g>'''

# ---------------------------------------------------------------- CTA: comment bubble + the PDF
CTA = f'''<g id="cta">
  <g id="cbub"><path d="{rrect(140, 760, 800, 170, 60)}" fill="#fff" stroke="{INK}" stroke-width="7"/>
    <path d="M230,928 L200,990 L300,930" fill="#fff" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>
    <circle cx="225" cy="845" r="38" fill="{LIME}" stroke="{INK}" stroke-width="5"/>
    {"".join(f'<g id="ck{i}" opacity="0">{TXT(290 + i * 70, 878, c, 88)}</g>' for i, c in enumerate("BIO"))}
    <g id="cpost">{TXT(780, 870, "Post", 48, col=PINK)}</g></g>
  <g transform="rotate(-4 540 1290)"><g id="pdf"><path d="{rrect(300, 990, 480, 600, 26)}" fill="#fdf4f4" stroke="{INK}" stroke-width="7"/>
    <g clip-path="url(#pdfclip)"><circle cx="330" cy="1020" r="120" fill="{LIME}" opacity=".7"/><circle cx="760" cy="1570" r="140" fill="#ffb3d1" opacity=".75"/></g>
    <rect x="340" y="1040" width="180" height="44" rx="22" fill="{INK}"/>{TXT(362, 1072, "FREE PDF", 30, "Caveat", LIME)}
    {TXT(340, 1170, "The 4-line", 74)}{TXT(340, 1250, "<tspan fill='" + PINK + "'>bio</tspan> formula", 74)}
    {TXT(342, 1320, "who you help, what they get,", 30, col="#555")}{TXT(342, 1360, "proof, what to do next", 30, col="#555")}
    <path d="{wobble([(345, 1410), (735, 1410)], False, 1)}" stroke="{INK}" stroke-width="4" fill="none"/>
    {TXT(342, 1470, "Creators 100X", 40)}</g></g>
  <g transform="rotate(8 760 1060)"><g id="sticky3"><rect x="640" y="980" width="250" height="150" fill="#fff27a"/>{TXT(664, 1046, "15", 70, "Caveat", PINK)}{TXT(664, 1104, "examples", 50, "Caveat")}</g></g>
</g>'''

CLIP.append('<clipPath id="pdfclip"><rect x="304" y="994" width="472" height="592" rx="24"/></clipPath>')
SVG_BODY = "".join(SVG) + f'<g id="stage"><g id="ink" filter="url(#boil0)">{"".join(INKS)}{CTA}{VIS}{BOLT}{HAND}</g></g>'

# ---------------------------------------------------------------- choreography
# boil: swap the displacement seed at 12 fps
for k in range(int(DUR * 12) + 1):
    js(f'tl.set("#ink", {{attr: {{filter: "url(#boil{k % 3})"}}}}, {k / 12:.3f});')
js('gsap.set("#ink path[pathLength]", {strokeDasharray: 1, strokeDashoffset: 0});')
js('gsap.set("#stage", {transformOrigin: "540px 1000px"});')

# b0 -- the card draws itself, the visitor walks in, reads, leaves
draw("#card", 0, .45)
pop("#cardfill", .05, .3, "{opacity: 0, scale: 1}")
draw("#av", .15, .3); pop("#avfill", .2); draw("#pan", .3, .25)
for sel, t in (("#handle", .3), ("#stats", .42), ("#ex", .5), ("#oldbio", .55)):
    ft(sel, t, .3, "{opacity: 0, x: -20}", "{opacity: 1, x: 0}", "power3.out")
draw("#fb", .45, .35); pop("#fbt0", .6)
for k in range(6):
    draw(f"#g{k}", .5 + k * .05, .3); pop(f"#gf{k}", .55 + k * .05, .25, "{opacity: 0, scale: 1}"); draw(f"#gi{k}", .65 + k * .05, .3)
js(f'gsap.set("#vis", {{x: -420}});')
to("#vis", t_visit - .4, .7, "{x: 0}", "power2.out")
js(f'tl.fromTo("#legL", {{rotation: 0}}, {{rotation: 14, duration: .15, yoyo: true, repeat: 4, transformOrigin: "50% 0%", immediateRender: false}}, {t_visit - .4:.3f});')
js(f'tl.fromTo("#legR", {{rotation: 0}}, {{rotation: -14, duration: .15, yoyo: true, repeat: 4, transformOrigin: "50% 0%", immediateRender: false}}, {t_visit - .4:.3f});')
to("#pup", t_visit + .25, .25, "{x: 6, y: -8}")
to("#lids", t_read, .15, "{opacity: 1}")
for i, t in enumerate((t_read + .05, t_read + .38, t_leave - .1)):
    if i == 0:
        pop("#watch", t - .1, .25)
    js(f'tl.set("#w{i + 1}", {{opacity: 1}}, {t:.3f}); tl.set("#w{i}", {{opacity: 0}}, {t:.3f});' if i else f'tl.set("#w1", {{opacity: 1}}, {t:.3f});')
    sfx("tick", t)
js(f'tl.fromTo("#hand", {{rotation: 0}}, {{rotation: 270, duration: {t_leave - t_read:.2f}, ease: "none", transformOrigin: "50% 100%", immediateRender: false}}, {t_read:.3f});')
to("#watch", t_leave + .25, .2, "{opacity: 0, scale: .5}")
to("#lids", t_leave, .1, "{opacity: 0}")
st("#mN", t_leave, "{opacity: 0}"); st("#mF", t_leave, "{opacity: 1}")
ft("#puffs", t_leave, .15, "{opacity: 0}", "{opacity: 1}")
to("#vis", t_leave + .05, .55, "{x: -460}", "power2.in")
to("#puffs", t_leave + .3, .2, "{opacity: 0}")
sfx("whoosh", t_leave)
pop("#sticky1", t_that, .3, "{opacity: 0, scale: 1.6, rotation: 10}", "back.out(2)")
sfx("paper", t_that)
draw("#arr1", t_that + .2, .35); draw("#arr1h", t_bio, .15)
sfx("swish", t_that + .2)
# b1 -- the bio is read out; circled; "?"
to("#sticky1", t_living - .3, .25, "{opacity: 0, y: 40}", "power2.in")
to("#arr1, #arr1h", t_living - .3, .2, "{opacity: 0}")
for sel, t in (("#oldbio text:nth-of-type(1)", t_living), ("#oldbio text:nth-of-type(2)", t_dm)):
    js(f'tl.fromTo("{sel}", {{scale: 1}}, {{scale: 1.08, duration: .18, yoyo: true, repeat: 1, transformOrigin: "0% 50%", immediateRender: false}}, {t:.3f});')
draw("#redloop", t_tells, .45, "power1.inOut")
sfx("swish", t_tells)
pop("#qmark", t_nothing, .35, "{opacity: 0, scale: 2.2, rotation: -20}")
sfx("error", t_nothing)
# the visitor peeks back, shrugs
st("#mF", t_tells - .1, "{opacity: 0}"); st("#mN", t_tells - .1, "{opacity: 1}")
to("#vis", t_tells - .1, .5, "{x: -40}", "power2.out")
st("#armsN", t_nothing, "{opacity: 0}"); st("#armsS", t_nothing, "{opacity: 1}")
pop("#vq", t_nothing + .1)
js(f'tl.fromTo("#visb", {{y: 0}}, {{y: -16, duration: .14, yoyo: true, repeat: 1, immediateRender: false}}, {t_nothing:.3f});')
# b2 -- "all about YOU" -> X; "What do I get?"
to("#qmark, #redloop", t_they - .25, .25, "{opacity: 0}")
to("#vq", t_they - .25, .2, "{opacity: 0}")
st("#armsN", t_they, "{opacity: 1}"); st("#armsS", t_they, "{opacity: 0}")
pop("#sticky2", t_they, .3, "{opacity: 0, scale: 1.6, rotation: -12}", "back.out(2)")
sfx("paper", t_they)
draw("#xx", t_you2, .3)
sfx("scratch", t_you2)
pop("#vbub", t_they2, .35, "{opacity: 0, scale: .3, transformOrigin: '10% 100%'}")
sfx("pop", t_they2)
to("#pup", t_they2, .2, "{x: 10, y: -4}")
# b3 -- scribble the old bio out, write four lines
to("#vbub", t_so - .2, .2, "{opacity: 0}")
to("#sticky2, #xx", t_so - .2, .2, "{opacity: 0, x: 60}", "power2.in")
draw("#oldscrib", t_so, .4, "power1.inOut")
sfx("swish", t_so)
to("#oldbio, #oldscrib", t_four + .25, .25, "{opacity: 0}")
to("#pup", t_so, .3, "{x: 4, y: -12}")
for i, t in enumerate(ITEMS):
    pop(f"#tag{i}", t - .12, .3)
    wipe(f"nb{i}", t - .05, 760, .45)
    sfx("pop", t - .1)
    sfx("swish", t)
draw("#arrow4", ITEMS[3] + .55, .25)
# the visitor leaves during b3 -- no: watches, then steps out for the "same profile" re-entry
# b4 -- same profile: the visitor comes back, reads, follows
# "Same profile": a double take -- eyes pop, a little jump
js(f'tl.fromTo("#eyes", {{scale: 1}}, {{scale: 1.3, duration: .12, yoyo: true, repeat: 1, transformOrigin: "50% 50%", immediateRender: false}}, {t_same:.3f});')
js(f'tl.fromTo("#visb", {{y: 0}}, {{y: -30, duration: .14, yoyo: true, repeat: 1, immediateRender: false}}, {t_same + .05:.3f});')
js(f'tl.fromTo("#pup", {{x: -6, y: -10}}, {{x: 10, y: -10, duration: .3, yoyo: true, repeat: 1, immediateRender: false}}, {t_same + .5:.3f});')
st("#mN", t_now, "{opacity: 0}"); st("#mH", t_now, "{opacity: 1}")
js(f'gsap.set("#tapper", {{x: 360, y: 1560}});')
ft("#tapper", t_now, .45, "{opacity: 0, x: 360, y: 1560}", "{opacity: 1, x: 560, y: 1150}", "power2.out")
js(f'tl.to("#tapper", {{scale: .85, duration: .08, yoyo: true, repeat: 1, transformOrigin: "30% 0%"}}, {t_follow - .05:.3f});')
to("#tapper", t_follow + .5, .25, "{opacity: 0}")
ft("#fbfill", t_follow, .2, "{opacity: 0}", "{opacity: 1}")
st("#fbt0", t_follow, "{opacity: 0}"); st("#fbt1", t_follow, "{opacity: 1}")
st("#fol", t_follow + .1, '{textContent: "1,205"}')
pop("#vheart", t_follow + .1, .35, "{opacity: 0, scale: .2, transformOrigin: '50% 100%'}")
sfx("click", t_follow); sfx("ding", t_follow + .05)
CONF = []
for k in range(16):
    a = random.uniform(0, 2 * math.pi)
    col = random.choice((PINK, LIME, "#fff27a", INK))
    CONF.append(f'<path id="cf{k}" d="{line(0, 0, random.randint(14, 26), random.randint(-8, 8), 1)}" stroke="{col}" stroke-width="7" stroke-linecap="round" fill="none" opacity="0" transform="translate(540 1126)"/>')
    js(f'tl.fromTo("#cf{k}", {{opacity: 1, x: 540, y: 1126, rotation: 0}}, {{keyframes: [{{x: {540 + math.cos(a) * random.randint(200, 420):.0f}, y: {1126 + math.sin(a) * random.randint(120, 260):.0f}, '
       f'rotation: {random.randint(-200, 200)}, duration: .45, ease: "power3.out"}}, {{opacity: 0, duration: .3}}], immediateRender: false}}, {t_follow + .02:.3f});')
# b5 -- the card makes way; the comment bubble and the PDF
CARD_SEL = "#card, #cardfill, #av, #avfill, #pan, #handle, #stats, #ex, #fb, #fbfill, #fbt0, #fbt1, " + ", ".join(
    [f"#g{k}, #gf{k}, #gi{k}" for k in range(6)] + [f"#tag{i}" for i in range(4)] + ["#arrow4"] + [f"[clip-path='url(#nb{i})']" for i in range(4)])
to(CARD_SEL, t_comment - .3, .22, "{opacity: 0, y: -60}", "power2.in")
js('gsap.set("#cta", {opacity: 0}); gsap.set("#pdf, #sticky3", {opacity: 0});')
st("#cta", t_comment - .05, "{opacity: 1}")
ft("#cbub", t_comment - .02, .35, "{opacity: 0, scale: .4, transformOrigin: '50% 50%'}", "{opacity: 1, scale: 1}", "back.out(2.2)")
for i in range(3):
    st(f"#ck{i}", t_bioW + i * .09, "{opacity: 1}")
    sfx("typing", t_bioW + i * .09)
js(f'tl.to("#cpost", {{scale: .85, duration: .08, yoyo: true, repeat: 1, transformOrigin: "50% 50%"}}, {t_bioW + .5:.3f});')
sfx("click", t_bioW + .5)
ft("#pdf", t_send - .15, .5, "{opacity: 0, y: 500, rotation: 8}", "{opacity: 1, y: 0, rotation: 0}", "back.out(1.6)")
sfx("whoosh", t_send - .15)
pop("#sticky3", t_fifteen - .05, .3, "{opacity: 0, scale: 1.8, rotation: -14}", "back.out(2)")
sfx("paper", t_fifteen)
st("#mH", t_send, "{opacity: 1}")
js(f'tl.fromTo("#visb", {{y: 0}}, {{y: -26, duration: .16, yoyo: true, repeat: 3, immediateRender: false}}, {t_fifteen:.3f});')

# the bolt: idle bob + reactions
js(f'tl.fromTo("#boltb", {{y: 0, rotation: -3}}, {{y: -10, rotation: 3, duration: .7, yoyo: true, repeat: {int(DUR / .7)}, ease: "sine.inOut", transformOrigin: "50% 50%", immediateRender: false}}, 0);')
for t in (t_bio, *ITEMS, t_follow, t_bioW):
    js(f'tl.to("#bolt", {{y: "-=46", duration: .14, yoyo: true, repeat: 1, ease: "power2.out"}}, {t:.3f});')
pop("#bsweat", t_leave, .2); to("#bsweat", t_leave + .9, .2, "{opacity: 0}")
pop("#bbang", t_nothing, .2); to("#bbang", t_nothing + .8, .2, "{opacity: 0}")
js(f'tl.to("#bolt", {{rotation: 360, duration: .6, ease: "back.out(1.4)", transformOrigin: "50% 50%"}}, {t_follow + .05:.3f});')

# more sound: the card drawing itself, footsteps, marker strokes, the exits
sfx("swish", 0.02); sfx("pop", .2); sfx("swish", .45)
for k in range(6):
    sfx("tick", .55 + k * .05) if k % 2 == 0 else None
sfx("steps", t_visit - .4); sfx("steps", t_tells - .1); sfx("pop", t_same)
sfx("pop", t_leave + .02)
for i, t in enumerate(ITEMS):
    for k in range(3):
        sfx("typing", t + .05 + k * .12)
sfx("swish", ITEMS[3] + .55)
sfx("sparkle", t_follow + .1)
sfx("whoosh", t_comment - .25)
sfx("pop", t_comment - .05)
sfx("chime", t_fifteen + .25)
sfx("ding2", t_bio)
sfx("pop", t_dm)

# punch-ins on the hits
for t, s in ((t_leave, 1.04), (t_nothing, 1.05), (t_so, 1.04), (t_follow, 1.05), (t_comment, 1.03)):
    js(f'tl.fromTo("#stage", {{scale: 1}}, {{scale: {s}, duration: .12, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false}}, {t:.3f});')


# ---------------------------------------------------------------- captions + pills (clean type over the doodles)
def head(hid, rows, line_id, size=78, after=0.0, until=None):
    spoken = [w for w in LINES[line_id] if w["t0"] >= after - 1e-6]
    k, out, rws = 0, [], []
    for row in rows:
        ws = []
        for word in row:
            pk = word.startswith("*")
            word = word.lstrip("*")
            key = word.lower().strip('.,:!?"')
            t = None
            while k < len(spoken):
                sw = spoken[k]["w"].lower().strip('.,:!?"')
                k += 1
                if sw[:4] == key[:4]:
                    t = spoken[k - 1]["t0"]
                    break
            t = spoken[-1]["t0"] if t is None else t
            wid = f"{hid}w{len(out)}"
            ws.append(f'<span class="hw{" pk" if pk else ""}" id="{wid}">{word}</span>')
            out.append((wid, t))
        rws.append(f'<div class="hl">{" ".join(ws)}</div>')
    HTML.append(f'<div class="head" id="{hid}" style="font-size:{size}px">{"".join(rws)}</div>')
    for wid, t in out:
        ft(f"#{wid}", t - .05, .3, "{opacity: 0, y: 26, scale: .9, filter: 'blur(8px)'}", "{opacity: 1, y: 0, scale: 1, filter: 'blur(0px)'}", "back.out(2)")
    if until is not None:
        to(f"#{hid}", until - .18, .18, "{opacity: 0, y: -24, filter: 'blur(8px)'}", "power2.in")


head("h0a", [["People", "visit", "your", "profile,"], ["read", "one", "line,", "and", "*leave."]], "b0", 76, until=t_that)
head("h0b", [["That", "line", "is", "your", "*bio."]], "b0", 92, after=t_that, until=L0["b1"])
head("h1", [['"Living', "my", "best", "life."], ['DM', 'for', 'collabs."'], ["Tells", "them", "*nothing."]], "b1", 76, until=L0["b2"])
head("h2a", [["They", "don't", "follow"], ["you", "for", "*you."]], "b2", 88, until=t_they2)
head("h2b", [["They", "follow", "for"], ["*what", "*they", "*get."]], "b2", 88, after=t_they2, until=L0["b3"])
head("h3", [["So", "write", "it", "in", "*four", "*lines."], ["Who", "you", "help.", "What", "they", "get."], ["Proof.", "And", "what", "to", "do", "next."]], "b3", 64, until=L0["b4"])
head("h4", [["Same", "profile."], ["Now", "they", "*follow."]], "b4", 92, until=L0["b5"])
head("h5", [["Comment", "*BIO"], ["and", "I'll", "send", "you", "the", "formula"], ["with", "*fifteen", "examples."]], "b5", 72)
PILLS = [(0, "3 SECONDS ON YOUR PROFILE"), (L0["b1"], "THE BIO MOST CREATORS HAVE"), (L0["b2"], "WHAT VISITORS WANT"), (L0["b3"], "THE 4-LINE BIO"),
         (L0["b4"], "SAME PROFILE, NEW BIO"), (L0["b5"], "FREE PDF IN YOUR DMS")]
for i, (t, txt) in enumerate(PILLS):
    HTML.append(f'<div class="stat" id="st{i}"><span>{txt}</span></div>')
    end = PILLS[i + 1][0] if i + 1 < len(PILLS) else DUR + 1
    if t <= 0:
        js(f'gsap.set("#st{i}", {{opacity: 1}});')
    else:
        ft(f"#st{i}", t, .3, "{opacity: 0, scale: .6, rotation: -4}", "{opacity: 1, scale: 1, rotation: 0}", "back.out(3)")
    if end < DUR:
        to(f"#st{i}", end - .12, .12, "{opacity: 0, scale: .9}", "power2.in")

POST = " ".join(f'gsap.set("{sel}", {frm});' for sel, (t, frm) in sorted(FIRST.items(), key=lambda kv: kv[1][0]) if t > 0.0)
POST += ' gsap.set("#vis", {x: -420});'
FILTERS = "".join(f'<filter id="boil{k}" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".022" numOctaves="2" seed="{k * 7 + 3}"/>'
                  f'<feDisplacementMap in="SourceGraphic" scale="4.5"/></filter>' for k in range(3))
CSS = open(os.path.join(ROOT, "build", "style.css")).read()
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creators 100X: Your bio is losing you followers 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <svg id="dd" viewBox="0 0 1080 1920" width="1080" height="1920"><defs>{FILTERS}{"".join(CLIP)}</defs>{SVG_BODY}{"".join(CONF)}</svg>
      {chr(10).join(HTML)}
      <div id="grain"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      {chr(10).join("      " + j for j in JS).strip()}
      tl.set({{}}, {{}}, {DUR:.2f});
      tl.progress(1, true).progress(0, true);
      {POST}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(html)
SFX.sort(key=lambda e: e["t"])
json.dump(SFX, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
json.dump({"dur": DUR, "music_in": 0, "lines": L0}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx")
