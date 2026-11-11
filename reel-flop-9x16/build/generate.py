"""Reel-flop explainer, 9:16 (1080x1920, 30 fps), v4: black-and-white PAPERCRAFT.

Owner: v3 "still feels dull" (music too slow/flat, look too flat/grey, too still between cuts) and sent a reference reel
(reference/ref.mp4, kept out of git): a papercraft / stop-motion explainer. Owner picked: black/white papercraft (the red
accent stays), no character, props built in code. Its grammar, rebuilt here in our own black/white world:
  * every section is its own crumpled-paper world (light / mid / dark paper, build/paper.py) standing on a cardboard
    floor; sections whip-pan into each other;
  * props are paper cut-outs: rough edges that "boil" like stop-motion (one SVG turbulence filter whose seed changes 12
    times a second) and hard drop shadows; they pop in with a squash;
  * a taped paper headline strip at the top of each section;
  * the spoken words land one by one as ransom-note paper scraps on the floor (Fraunces), key words on red paper;
  * the camera never sits still: a slow push-in in every section, punches on key words, a paper sunburst on peaks.
Script, voice, word timings and the hook (cold-open slams + paper tear, the fake swipe, the "algorithm" scrap tearing
into a giant 3, the countdown) are unchanged in content. v3 is kept in cache/generate_v3_backup.py.

/root/tts/.venv/bin/python build/generate.py  ->  index.html, plan/sfx_events.json
"""
import json
import math
import os
import random

from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FW, FH, FPS = 1080, 1920, 30
WORDS = json.load(open(os.path.join(ROOT, "plan", "words.json")))
DUR = round(WORDS[-1]["t1"] + 1.7, 2)
INK, PAPER, RED = "#141414", "#f1efea", "#e8262a"
FLOOR_Y = 1300
A, SFX = [], []
R = random.Random(42)


def js(s):
    A.append("      " + s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(max(0, t), 3)})


def words_of(line):
    return [w for w in WORDS if w["line"] == line]


def L(line, i, key="t0"):
    return words_of(line)[i][key]


# ---------------------------------------------------------------- text measuring
_F = {}
FONT_FILE = {"inter": "inter-latin-{w}-normal.woff2", "fraunces": "fraunces-latin-{w}-normal.woff2"}


def font(family, weight):
    key = (family, weight)
    if key not in _F:
        _F[key] = TTFont(os.path.join(ROOT, "assets", "fonts", FONT_FILE[family].format(w=weight)))
    return _F[key]


def text_w(s, size, family="inter", weight=800, ls=0.0):
    f = font(family, weight)
    cmap, hm, upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    return sum(hm[cmap.get(ord(c), cmap[ord("n")])][0] for c in s) / upm * size + ls * size * max(0, len(s) - 1)


def ttf(family, weight):
    path = os.path.join(ROOT, "cache", f"{family}-{weight}.ttf")
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        f = TTFont(os.path.join(ROOT, "assets", "fonts", FONT_FILE[family].format(w=weight)))
        f.flavor = None
        f.save(path)
    return path


# ---------------------------------------------------------------- sections (paper worlds) and the camera
def section(sid, tone, t0, t1, inner, floor=True, strip=None, push=.05, alt=None):
    """A paper world: ground + floor + the scene inside a moving camera + a taped headline strip. `alt`: a second
    ground/floor tone, hidden, that hard cuts can switch on (#sid_g2 / #sid_f2)."""
    fl = f'<div class="floor {tone}"></div>' if floor else ""
    if alt:
        fl += f'<div class="floor {alt}" id="{sid}_f2" style="opacity:0"></div>'
    g2 = f'<div class="gnd {alt}" id="{sid}_g2" style="opacity:0"></div>' if alt else ""
    st = ""
    if strip:
        w = text_w(strip, 46, "inter", 800, .02) + 72
        st = (f'<div class="strip" id="{sid}_st" style="width:{w:.0f}px;margin-left:{-w / 2:.0f}px">{strip}'
              f'<i class="tape tl"></i><i class="tape tr"></i></div>')
        js(f'tl.fromTo("#{sid}_st", {{opacity: 0, y: -60, rotation: -9}}, {{opacity: 1, y: 0, rotation: -1.5, duration: .4, ease: "back.out(2.2)", immediateRender: false}}, {t0 + .12:.3f});')
        sfx("paper", t0 + .14)
    js(f'tl.fromTo("#{sid}_cam", {{scale: 1}}, {{scale: {1 + push}, duration: {max(.5, t1 - t0 + .4):.2f}, ease: "none", immediateRender: false}}, {t0:.3f});')
    return (f'<div class="sec" id="{sid}"><div class="gnd {tone}" id="{sid}_g"></div>{g2}<div class="cam" id="{sid}_cam">{fl}'
            f'<div class="punch" id="{sid}_p">{inner}</div></div>{st}</div>')


def show_sec(sid, t):
    js(f'tl.set("#{sid}", {{visibility: "visible"}}, {t:.3f});')


def hide_sec(sid, t):
    js(f'tl.set("#{sid}", {{visibility: "hidden"}}, {t:.3f});')


def whip(a, b, t, d=1):
    """Whip pan from section a to section b at time t (the new world slides in, the old out, both blurred)."""
    show_sec(b, t)
    js(f'tl.fromTo("#{b}", {{x: {FW * d}, filter: "blur(16px)"}}, {{x: 0, filter: "blur(0px)", duration: .34, ease: "expo.inOut", immediateRender: false}}, {t:.3f});')
    js(f'tl.fromTo("#{a}", {{x: 0, filter: "blur(0px)"}}, {{x: {-FW * d}, filter: "blur(16px)", duration: .34, ease: "expo.inOut", immediateRender: false}}, {t:.3f});')
    hide_sec(a, t + .36)
    sfx("whoosh", t)


def punch(sid, t, amt=.06):
    """A zoom punch on a key word: a quick extra scale on the section's punch layer that settles back."""
    js(f'tl.fromTo("#{sid}_p", {{scale: 1}}, {{keyframes: {{scale: [1, {1 + amt}, 1]}}, duration: .4, ease: "power2.out", immediateRender: false}}, {t - .02:.3f});')


def pop(sel, t, d=.32, rot=0, y=40, sc=.6):
    """A cut-out pops in with a squash (stop-motion feel: overshoot and settle)."""
    js(f'tl.fromTo("{sel}", {{opacity: 0, scale: {sc}, y: {y}, rotation: {rot - 8}}}, {{opacity: 1, scale: 1, y: 0, rotation: {rot}, duration: {d}, ease: "back.out(2.6)", immediateRender: false}}, {t:.3f});')


def stamp(sel, t, rot=-8):
    """A rubber stamp slams on (red ink)."""
    js(f'tl.fromTo("{sel}", {{opacity: 0, scale: 2.2, rotation: {rot - 10}}}, {{opacity: 1, scale: 1, rotation: {rot}, duration: .2, ease: "power4.in", immediateRender: false}}, {t:.3f});')
    sfx("stamp", t + .18)


def sunburst(sid, n=22):
    rays = []
    for i in range(n):
        a0, a1 = i * 2 * math.pi / n, (i + .5) * 2 * math.pi / n
        p = f"0,0 {1600 * math.cos(a0):.0f},{1600 * math.sin(a0):.0f} {1600 * math.cos(a1):.0f},{1600 * math.sin(a1):.0f}"
        rays.append(f'<polygon points="{p}"/>')
    return f'<svg class="sun" id="{sid}" viewBox="-1600 -1600 3200 3200">{"".join(rays)}</svg>'


# ---------------------------------------------------------------- ransom-note captions (global layer, on the floor)
CAP = []
KEY = {"algorithm.", "three", "\"Hey", "guys.\"", "still.", "show.", "result", "\"HOOK\"", "flopped", "nothing", "first,", "Fix", "Save"}
CAP_TOP, CAP_MAXW, CAP_SIZE = 1350, 940, 56
SCRAP_POS = {}


def cap_layout(ws):
    """Rows of scraps for a chunk of words, centred, wrapping at CAP_MAXW. Returns ([(word, x, y, w)], rows)."""
    rows, row, rw = [], [], 0
    for w in ws:
        wd = text_w(w["w"], CAP_SIZE, "fraunces", 700) + 30
        if row and rw + wd + 12 > CAP_MAXW:
            rows.append((row, rw))
            row, rw = [], 0
        rw += wd + (12 if row else 0)
        row.append((w, wd))
    if row:
        rows.append((row, rw))
    out = []
    for ri, (row, rw) in enumerate(rows):
        x = (FW - rw) / 2
        for w, wd in row:
            out.append((w, x, CAP_TOP + ri * 92, wd))
            x += wd + 12
    return out, len(rows)


def chunks(line):
    """Split a spoken line into chunks of at most two rows of scraps, breaking after commas where possible."""
    out, cur = [], []
    for w in words_of(line):
        cur.append(w)
        if cap_layout(cur)[1] > 2:
            cur.pop()
            cut = max((i for i, x in enumerate(cur) if x["w"].endswith(",")), default=None)
            if cut is not None and cut < len(cur) - 1:
                out.append(cur[:cut + 1])
                cur = cur[cut + 1:]
            else:
                out.append(cur)
                cur = []
            cur.append(w)
    if cur:
        out.append(cur)
    return out


def captions(lines):
    groups = []
    for line in lines:
        groups += chunks(line)
    k = 0
    for gi, g in enumerate(groups):
        lay, _ = cap_layout(g)
        t_end = groups[gi + 1][0]["t0"] - .06 if gi + 1 < len(groups) else None
        for w, x, y, wd in lay:
            sid = f"cp{k}"
            k += 1
            red = w["w"] in KEY
            rot = R.uniform(-4, 4)
            dy = R.uniform(-6, 6)
            mark = '<i class="mk"></i>' if (w["line"], w["w"]) == ("l01", "algorithm.") else ""
            CAP.append(f'<div class="scrap{" red" if red else ""}" id="{sid}" style="left:{x:.0f}px;top:{y + dy:.0f}px;width:{wd:.0f}px">'
                       f'{w["w"].replace(chr(34), "&quot;")}{mark}</div>')
            SCRAP_POS[(w["line"], w["w"])] = (x, y + dy, wd, sid)
            js(f'tl.fromTo("#{sid}", {{opacity: 0, scale: 1.45, rotation: {rot + R.choice([-10, 10]):.1f}, y: -14}}, {{opacity: 1, scale: 1, rotation: {rot:.1f}, y: 0, duration: .2, ease: "back.out(3)", immediateRender: false}}, {w["t0"] - .03:.3f});')
            if t_end:
                js(f'tl.to("#{sid}", {{opacity: 0, y: 60, rotation: {rot + R.uniform(-25, 25):.0f}, duration: .16, ease: "power2.in"}}, {t_end:.3f});')
        sfx("paper", g[0]["t0"] - .03)


# ---------------------------------------------------------------- props
def phone(pid, screens, x=305, y=520, w=470, h=760):
    return (f'<div class="phone pp" id="{pid}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
            f'<div class="scr" id="{pid}_scr">{screens}</div><i class="notch"></i></div>')


def person(cls=""):
    return f'<div class="person {cls}"><i class="hd"></i><i class="bd"></i></div>'


def pbar(bid, mk=True):
    return f'<div class="pbar"><i class="pfill" id="{bid}"></i>{"<i class=mk></i>" if mk else ""}</div>'


def lines3():
    return '<i class="ln1"></i><i class="ln2"></i><i class="ln3"></i>'


# ---------------------------------------------------------------- cold open: slams, a rip, the paper tears away
IMPACT = (560, 980)
GLASS = []


def tear_grid():
    r = random.Random(4)
    radii = [0, 110, 300, 600, 1000, 2400]
    n = 13
    base = [i * 2 * math.pi / n + r.uniform(-.18, .18) for i in range(n)]
    P = []
    for ri, rad in enumerate(radii):
        ring = []
        for a in base:
            if ri == 0:
                ring.append(IMPACT)
                continue
            rr = rad * r.uniform(.78, 1.22)
            aa = a + r.uniform(-.1, .1)
            ring.append((IMPACT[0] + rr * math.cos(aa), IMPACT[1] + rr * math.sin(aa)))
        P.append(ring)
    return P


def slam_card(cid, tone, col, rows, shown=False):
    h = "".join(f'<div class="sw" id="{cid}w{j}" style="font-size:{min(sz, int(940 / max(1, text_w(t, 1, "inter", 800, -.04))))}px">{t}</div>'
                for j, (t, sz) in enumerate(rows))
    return f'<div class="scard {tone}" id="{cid}" style="color:{col};{"opacity:1" if shown else ""}">{h}</div>'


def cold_open():
    cards = (slam_card("sc0", "light", INK, [("THIS", 360)], shown=True) + slam_card("sc1", "dark", PAPER, [("REEL", 360)])
             + slam_card("sc2", "light", INK, [("IS", 250), ("ABOUT", 250), ("TO", 250)]) + slam_card("sc3", "redp", PAPER, [("LOSE", 380)])
             + slam_card("sc4", "light", INK, [("YOU.", 380)]))
    P = tear_grid()
    lines = []
    for a in range(len(P[0])):
        pts = " ".join(f"{P[ri][a][0]:.0f},{P[ri][a][1]:.0f}" for ri in range(len(P)))
        lines.append(f'<polyline class="crk" pathLength="1000" points="{pts}"/>')
    for ri in (1, 2, 3, 4):
        for a in range(len(P[0])):
            if (ri + a) % 3 == 0 and ri > 2:
                continue
            b = (a + 1) % len(P[0])
            lines.append(f'<polyline class="crk" pathLength="1000" points="{P[ri][a][0]:.0f},{P[ri][a][1]:.0f} {P[ri][b][0]:.0f},{P[ri][b][1]:.0f}"/>')
    cracks = f'<svg id="cracks" viewBox="0 0 {FW} {FH}"><g class="under">{"".join(lines)}</g><g class="over">{"".join(lines)}</g></svg>'
    you = slam_card("x", "light", INK, [("YOU.", 380)], shown=True).replace('id="x"', "").replace('id="xw0"', "")
    pieces = []
    for ri in range(len(P) - 1):
        for a in range(len(P[0])):
            b = (a + 1) % len(P[0])
            poly = [P[ri][a], P[ri][b], P[ri + 1][b], P[ri + 1][a]] if ri else [IMPACT, P[1][b], P[1][a]]
            cx = sum(p[0] for p in poly) / len(poly)
            cy = sum(p[1] for p in poly) / len(poly)
            k = len(GLASS)
            GLASS.append((cx, cy))
            cp = ", ".join(f"{x:.0f}px {y:.0f}px" for x, y in poly)
            edge = " ".join(f"{x:.0f},{y:.0f}" for x, y in poly)
            pieces.append(f'<div class="gp" id="gp{k}" style="clip-path:polygon({cp});transform-origin:{cx:.0f}px {cy:.0f}px">{you}'
                          f'<svg class="ge" viewBox="0 0 {FW} {FH}"><polygon points="{edge}"/></svg></div>')
    return f'<div id="slam">{cards}{cracks}</div><div id="glass">{"".join(pieces)}</div>'


# ---------------------------------------------------------------- the giant numerals and the shards that build the 3
NUM_SIZE = 1000
NUM_BASE = FLOOR_Y - 10          # the giant numerals stand on the floor


def num_top():
    f = font("inter", 800)
    hh, upm = f["hhea"], f["head"].unitsPerEm
    asc, desc = hh.ascent / upm, -hh.descent / upm
    return round(NUM_BASE - ((1 - (asc + desc)) / 2 + asc) * NUM_SIZE)


def sample_mask(draw_fn, n, seed):
    from PIL import Image, ImageDraw
    im = Image.new("L", (FW, FH), 0)
    draw_fn(ImageDraw.Draw(im))
    data = im.get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata()
    px = [(i % FW, i // FW) for i, v in enumerate(data) if v > 128]
    return random.Random(seed).sample(px, n)


def shards(t_x, t_g, t_3):
    """The struck "algorithm." scrap tears into 150 shards that burst up and rush into the outline of the giant 3."""
    from PIL import ImageFont
    x, y, wd, sid = SCRAP_POS[("l01", "algorithm.")]
    starts = sample_mask(lambda d: d.rectangle([x, y, x + wd, y + 78], fill=255), 150, 3)
    f = font("inter", 800)
    adv = f["hmtx"][f.getBestCmap()[ord("3")]][0] / f["head"].unitsPerEm * NUM_SIZE
    fi = ImageFont.truetype(ttf("inter", 800), NUM_SIZE)
    targets = sample_mask(lambda d: d.text((540 - adv / 2, NUM_BASE), "3", font=fi, fill=255, anchor="ls"), 150, 5)
    key = lambda p: p[0] + .35 * p[1]    # noqa: E731
    starts, targets = sorted(starts, key=key), sorted(targets, key=key)
    rnd = random.Random(7)
    cx = sum(p[0] for p in starts) / len(starts)
    cy = sum(p[1] for p in starts) / len(starts)
    out = []
    for k, ((sx, sy), (tx, ty)) in enumerate(zip(starts, targets)):
        size = rnd.randint(18, 34)
        pts = [(rnd.randint(0, 40), rnd.randint(0, 30)), (rnd.randint(60, 100), rnd.randint(0, 45)), (rnd.randint(20, 80), rnd.randint(70, 100))]
        poly = ", ".join(f"{a}% {b}%" for a, b in pts)
        col = RED if rnd.random() < .45 else PAPER
        out.append(f'<i class="shd" id="sh{k}" style="left:{sx - size / 2:.0f}px;top:{sy - size / 2:.0f}px;width:{size}px;height:{size}px;'
                   f'clip-path:polygon({poly});background:{col}"></i>')
        ang = math.atan2(sy - cy, sx - cx) + rnd.uniform(-.7, .7)
        dist = rnd.uniform(160, 520)
        ex, ey = math.cos(ang) * dist, math.sin(ang) * dist - rnd.uniform(120, 360)
        js(f'tl.fromTo("#sh{k}", {{opacity: 1, x: 0, y: 0, rotation: 0}}, {{opacity: 1, x: {ex:.0f}, y: {ey:.0f}, rotation: {rnd.uniform(-260, 260):.0f}, duration: .4, ease: "expo.out", immediateRender: false}}, {t_x:.3f});')
        d = rnd.uniform(0, .1)
        js(f'tl.to("#sh{k}", {{x: {tx - sx:.0f}, y: {ty - sy:.0f}, rotation: {rnd.uniform(-30, 30):.0f}, backgroundColor: "{INK}", duration: {.46 - d:.2f}, ease: "expo.inOut"}}, {t_g + d:.3f});')
    js(f'tl.to(".shd", {{opacity: 0, duration: .16}}, {t_3:.3f});')
    js(f'tl.fromTo("#{sid} .mk", {{scaleX: 0}}, {{scaleX: 1, duration: .2, ease: "power3.inOut", immediateRender: false}}, {t_x - .3:.3f});')
    js(f'tl.set("#{sid}", {{visibility: "hidden"}}, {t_x:.3f});')
    sfx("scratch", t_x - .3)
    sfx("rip", t_x)
    sfx("rise", t_g)
    return f'<div id="shards">{"".join(out)}</div>'


# ================================================================= the scenes
def scenes():
    H, S = [], []

    # ---- S0 cold open: THIS / REEL / IS ABOUT TO / LOSE (red paper rips) / YOU. (the paper tears away)
    H.append(cold_open())
    sfx("hit", 0.0)
    js('tl.fromTo("#sc0 .sw", {scale: 1.18}, {scale: 1, duration: .22, ease: "expo.out", immediateRender: false}, 0);')
    prev = "sc0"
    for cid, t in [("sc1", L("l00", 1)), ("sc2", L("l00", 2)), ("sc3", L("l00", 5)), ("sc4", L("l00", 6))]:
        js(f'tl.set("#{prev}", {{opacity: 0}}, {t - .03:.3f}); tl.set("#{cid}", {{opacity: 1}}, {t - .03:.3f});')
        js(f'tl.fromTo("#{cid} .sw", {{scale: 1.22, rotation: {R.uniform(-4, 4):.1f}}}, {{scale: 1, rotation: 0, duration: .24, ease: "expo.out", immediateRender: false}}, {t - .03:.3f});')
        sfx("stamp", t - .02)
        prev = cid
    for j, i in enumerate((3, 4)):
        js(f'tl.fromTo("#sc2w{j + 1}", {{opacity: 0, scale: 1.25}}, {{opacity: 1, scale: 1, duration: .2, ease: "expo.out", immediateRender: false}}, {L("l00", i) - .03:.3f});')
    t_lose = L("l00", 5) - .03
    js(f'tl.fromTo(".crk", {{strokeDashoffset: 1000}}, {{strokeDashoffset: 0, duration: .14, ease: "power2.out", immediateRender: false}}, {t_lose + .02:.3f});')
    js(f'tl.set("#cracks", {{opacity: 1}}, {t_lose:.3f});')
    sfx("rip", t_lose)
    sfx("hit", t_lose)
    t_br = L("l00", 6, "t1") + .02
    js(f'tl.set("#slam", {{opacity: 0}}, {t_br:.3f}); tl.set("#glass", {{opacity: 1}}, {t_br:.3f});')
    rnd = random.Random(11)
    for k, (cx, cy) in enumerate(GLASS):
        dx, dy = cx - IMPACT[0], cy - IMPACT[1]
        dist = math.hypot(dx, dy)
        push = 40 + 260 * max(0, 1 - dist / 1400) + rnd.uniform(0, 60)
        bx, by = dx / max(dist, 1) * push, dy / max(dist, 1) * push - rnd.uniform(20, 90)
        rot = rnd.uniform(-35, 35)
        js(f'tl.to("#gp{k}", {{x: {bx:.0f}, y: {by:.0f}, rotation: {rot:.0f}, scale: {rnd.uniform(1.02, 1.12):.2f}, duration: .14, ease: "expo.out"}}, {t_br:.3f});')
        js(f'tl.to("#gp{k}", {{x: {bx * 1.6:.0f}, y: {by + 1700 + rnd.uniform(0, 700):.0f}, rotation: {rot * 3:.0f}, duration: {rnd.uniform(.5, .72):.2f}, ease: "power2.in"}}, {t_br + .14 + rnd.uniform(0, .05):.3f});')
    js(f'tl.set("#glass", {{opacity: 0}}, {t_br + 1.0:.3f});')
    sfx("rip", t_br - .02)
    sfx("whoosh_big", t_br + .08)

    # ---- S1 (light paper): the fake swipe on a paper phone. "Your reel didn't flop because of the algorithm."
    a_end = L("l01", 7, "t1")
    t_x = a_end + .14                       # the algorithm scrap tears
    t_g, t_3 = t_x + .4, t_x + .9           # the shards gather; the solid 3
    t1a, t2a = t_br, t_x + .4
    show_sec("s1", t1a)
    reel = (f'<div class="reel" id="r1">{person()}<div class="vtag"><i class="play"></i>312 views <b>&#8595; 97%</b></div>{pbar("r1pb", False)}</div>'
            f'<div class="reel nxt" id="r1n">{person("p2")}{lines3()}</div>')
    inner = (phone("ph1", reel) + '<div class="thumb" id="th1"></div>'
             '<div class="rtag" id="almost">YOU ALMOST SCROLLED.<i class="tape tl"></i></div>')
    S.append(section("s1", "light", t1a, t2a, inner, strip="WHY YOUR REEL FLOPPED"))
    js(f'tl.fromTo("#ph1", {{rotation: -2}}, {{rotation: 1.5, duration: {t2a - t1a:.2f}, ease: "sine.inOut", immediateRender: false}}, {t1a:.3f});')
    js(f'tl.fromTo("#r1pb", {{scaleX: 0}}, {{scaleX: .3, duration: {t2a - t1a:.2f}, ease: "none", immediateRender: false}}, {t1a:.3f});')
    t_sw = L("l01", 2) + .05
    pop("#th1", t_sw - .22, d=.18, y=60)
    js(f'tl.to("#th1", {{y: -420, duration: .38, ease: "power2.inOut"}}, {t_sw:.3f});')
    js(f'tl.to("#r1, #r1n", {{yPercent: -62, duration: .38, ease: "power2.inOut"}}, {t_sw:.3f});')
    js(f'tl.to("#th1", {{opacity: 0, duration: .12}}, {t_sw + .4:.3f});')
    js(f'tl.to("#r1, #r1n", {{yPercent: 0, duration: .7, ease: "elastic.out(1, .55)"}}, {t_sw + .44:.3f});')
    sfx("swish", t_sw)
    sfx("swish", t_sw + .44)
    stamp("#almost", t_sw + .56, rot=-6)
    punch("s1", t_sw + .6)
    punch("s1", L("l01", 7), .05)

    # ---- S2: "It flopped in the first three seconds." Giant paper-cut 3, 2, 1, 0 standing on the floor; the world
    # flips with every number (light + sunburst, dark, light, dark with a red 0)
    t_s3 = L("l03", 0) - .14
    flip_t = L("l02", 6, "t1") + .06
    c2 = L("l02", 5) - .02
    c1 = (c2 + flip_t) / 2
    inner = sunburst("sun2") + f'<div class="bign pp" id="bign" style="top:{num_top()}px">&#8203;3</div>'
    S.append(section("s2", "light", t_x, t_s3, inner, strip="THE FIRST 3 SECONDS", push=.04, alt="dark"))
    show_sec("s2", t_x)
    js(f'tl.to("#s1", {{opacity: 0, scale: .96, duration: .35, ease: "power2.in"}}, {t_x:.3f});')
    hide_sec("s1", t_x + .4)
    js(f'tl.fromTo("#s2", {{opacity: 0}}, {{opacity: 1, duration: .3, immediateRender: false}}, {t_x:.3f});')
    js(f'tl.fromTo("#sun2", {{rotation: 0, opacity: 0}}, {{rotation: 40, opacity: 1, duration: {t_s3 - t_x:.2f}, ease: "none", immediateRender: false}}, {t_x:.3f});')
    js(f'tl.fromTo("#bign", {{opacity: 0}}, {{opacity: 1, duration: .14, immediateRender: false}}, {t_3 - .05:.3f});')
    js(f'tl.fromTo("#bign", {{scale: 1.08, rotation: -4}}, {{scale: 1, rotation: 0, duration: .45, ease: "back.out(3)", immediateRender: false}}, {t_3 - .05:.3f});')
    sfx("hit", t_3 - .04)
    for t, n, tone, col in [(c2, 2, "dark", PAPER), (c1, 1, "light", INK), (flip_t, 0, "dark", RED)]:
        o = 1 if tone == "dark" else 0
        js(f'tl.set("#s2_g2, #s2_f2", {{opacity: {o}}}, {t:.3f});')
        js(f'tl.set("#sun2", {{visibility: "{"hidden" if tone == "dark" else "visible"}"}}, {t:.3f});')
        js(f'tl.set("#bign", {{textContent: "\\u200b{n}", color: "{col}"}}, {t:.3f});')
        js(f'tl.fromTo("#bign", {{scale: 1.14, rotation: {R.choice([-5, 5])}}}, {{scale: 1, rotation: 0, duration: .3, ease: "back.out(3)", immediateRender: false}}, {t:.3f});')
        sfx("count" if n else "glitch", t)
    punch("s2", flip_t, .08)

    # ---- S3 (dark paper): "Here are three mistakes killing your views." Three taped paper cards drop in
    t_s4 = L("l04", 0) - .14
    cards = "".join(f'<div class="card3 pp" id="c3_{k}" style="left:{90 + k * 310}px"><span>{k + 1}</span><i class="tape tc"></i></div>' for k in range(3))
    inner = cards + '<div class="arrow pp" id="arr3"><svg viewBox="0 0 100 160"><path d="M50 0v120M15 90l35 50 35-50"/></svg></div>'
    S.append(section("s3", "dark", t_s3, t_s4, inner, strip="3 MISTAKES"))
    whip("s2", "s3", t_s3)
    for k in range(3):
        tt = L("l03", 2) + k * .14
        pop(f"#c3_{k}", tt, rot=R.uniform(-6, 6), y=-200)
        sfx("paper", tt + .1)
    pop("#arr3", L("l03", 6) - .05, y=-80)
    sfx("drop", L("l03", 6))
    punch("s3", L("l03", 3))

    # ---- S4 (light): mistake 1. "One: your hook is a greeting. Nobody stays for 'Hey guys.'"
    t_f1 = L("l06", 0) - .12
    reel = (f'<div class="reel" id="r4">{person()}<div class="bubble pp" id="bub4"><span id="bub4t"></span></div>{pbar("r4pb")}</div>'
            f'<div class="reel nxt" id="r4n">{person("p2")}{lines3()}</div>')
    inner = phone("ph4", reel) + '<div class="thumb" id="th4"></div><div class="rstamp" id="st4">SKIPPED AT 0:01</div>'
    S.append(section("s4", "light", t_s4, t_f1, inner, strip="MISTAKE 1: THE GREETING"))
    whip("s3", "s4", t_s4, -1)
    js(f'tl.fromTo("#ph4", {{rotation: 2}}, {{rotation: -1.5, duration: {t_f1 - t_s4:.2f}, ease: "sine.inOut", immediateRender: false}}, {t_s4:.3f});')
    t_cap = L("l04", 4) - .1
    pop("#bub4", t_cap - .1, y=20)
    cap = "Hey guys, so today..."
    for i in range(1, len(cap) + 1):
        js(f'tl.set("#bub4t", {{textContent: {json.dumps(cap[:i])}}}, {t_cap + i * .035:.3f});')
        if i % 4 == 1:
            sfx("type", t_cap + i * .035)
    js(f'tl.fromTo("#r4pb", {{scaleX: 0}}, {{scaleX: .035, duration: 2.6, ease: "none", immediateRender: false}}, {L("l04", 1):.3f});')
    t_sw = L("l05", 3)
    pop("#th4", t_sw - .3, d=.2, y=60)
    js(f'tl.to("#th4", {{y: -420, opacity: 0, duration: .34, ease: "power3.in"}}, {t_sw:.3f});')
    js(f'tl.to("#r4, #r4n", {{yPercent: -100, duration: .38, ease: "power3.in"}}, {t_sw + .04:.3f});')
    sfx("whoosh", t_sw)
    stamp("#st4", t_sw + .3, rot=-9)
    punch("s4", t_sw + .6)

    # ---- S4b (dark): fix 1. "Start with the result." The next reel opens on the result; a sunburst behind
    t_m2 = L("l07", 0) - .12
    reel = f'<div class="reel" id="r4b">{person("p3")}<div class="res"><div id="res1">1M VIEWS</div><div id="res2">in 3 days. Here\'s how.</div></div>{pbar("r4bpb")}</div>'
    inner = sunburst("sun4b") + phone("ph4b", reel) + '<div class="rstamp white" id="st4b">STILL WATCHING</div>'
    S.append(section("s4b", "dark", t_f1, t_m2, inner, strip="FIX: START WITH THE RESULT"))
    whip("s4", "s4b", t_f1)
    js(f'tl.fromTo("#sun4b", {{rotation: 0, opacity: 0}}, {{rotation: 30, opacity: 1, duration: {t_m2 - t_f1:.2f}, ease: "none", immediateRender: false}}, {t_f1:.3f});')
    t_res = L("l06", 3) - .05
    pop("#res1", t_res, sc=.4, y=0)
    pop("#res2", t_res + .12, y=10)
    sfx("hit", t_res)
    punch("s4b", t_res)
    js(f'tl.fromTo("#r4bpb", {{scaleX: 0}}, {{scaleX: .24, duration: 1.4, ease: "none", immediateRender: false}}, {t_f1 + .1:.3f});')
    stamp("#st4b", t_res + .2, rot=7)

    # ---- S5 (mid paper): mistake 2. "Two: your first frame is still. If nothing moves, thumbs keep scrolling."
    t_m3 = L("l09", 0) - .14
    still = (f'<div class="fi"><div class="photo"><i class="sunc"></i><i class="hill1"></i><i class="hill2"></i></div>'
             f'<div class="paused" id="pz5"><i></i><i></i></div>{pbar("r5pb")}</div>')
    other = lambda c: f'<div class="fi {c}">{person(c)}{lines3()}</div>'   # noqa: E731
    reel = f'<div class="reel" id="feed5"><div class="strip5" id="strip5">{still}{other("p2")}{other("p3")}</div></div>'
    inner = (phone("ph5", reel) + '<div class="thumb" id="th5"></div><div class="rtag" id="nm5">NOTHING MOVES<i class="tape tl"></i></div>'
             '<div class="rstamp" id="st5">SCROLLED PAST</div>')
    S.append(section("s5", "mid", t_m2, t_m3, inner, strip="MISTAKE 2: A STILL FIRST FRAME"))
    whip("s4b", "s5", t_m2, -1)
    pop("#pz5", L("l07", 5), sc=.3, y=0)
    sfx("click", L("l07", 5))
    punch("s5", L("l07", 5))
    stamp("#nm5", L("l08", 1), rot=-5)
    t_sc = L("l08", 3)
    pop("#th5", t_sc - .28, d=.2, y=60)
    js(f'tl.to("#th5", {{y: -420, opacity: 0, duration: .3, ease: "power3.in"}}, {t_sc:.3f});')
    js(f'tl.to("#nm5", {{opacity: 0, duration: .12}}, {t_sc:.3f});')
    js(f'tl.to("#strip5", {{yPercent: -66.667, duration: .85, ease: "expo.inOut"}}, {t_sc:.3f});')
    js(f'tl.fromTo("#strip5", {{filter: "blur(0px)"}}, {{filter: "blur(9px)", duration: .3, ease: "power2.in", immediateRender: false}}, {t_sc + .1:.3f});')
    js(f'tl.to("#strip5", {{filter: "blur(0px)", duration: .3, ease: "power2.out"}}, {t_sc + .5:.3f});')
    sfx("whoosh", t_sc + .05)
    sfx("swish", t_sc + .35)
    stamp("#st5", t_sc + .7, rot=8)

    # ---- S6 (light): mistake 3. "Three: you explain before you show." Two taped cards, wrong order
    t_f3 = L("l10", 0) - .12
    inner = ('<div class="card2 pp" id="cEx"><span class="cn">1</span><div><b>EXPLAIN</b><i>how you did it</i></div><i class="tape tl"></i></div>'
             '<div class="card2 pp" id="cSh"><span class="cn">2</span><div><b>SHOW</b><i>the result</i></div><i class="tape tr"></i></div>'
             '<div class="rstamp" id="st6">TOO LATE</div>')
    S.append(section("s6", "light", t_m3, t_f3, inner, strip="MISTAKE 3: EXPLAIN BEFORE SHOW"))
    whip("s5", "s6", t_m3)
    pop("#cEx", L("l09", 2) - .05, rot=-2, y=-160)
    sfx("paper", L("l09", 2))
    pop("#cSh", L("l09", 3) - .2, rot=2, y=-160)
    sfx("paper", L("l09", 3) - .15)
    stamp("#st6", L("l09", 3) + .05, rot=-10)
    punch("s6", L("l09", 3) + .15)

    # ---- S6b (dark): fix 3. "Show the result first, then explain how you got it." The cards swap
    t_s7 = L("l11", 0) - .14
    inner = ('<div class="card2 pp" id="cSh2"><span class="cn">1</span><div><b>SHOW</b><i>the result</i></div><i class="tape tr"></i></div>'
             '<div class="card2 pp" id="cEx2"><span class="cn">2</span><div><b>EXPLAIN</b><i>how you got it</i></div><i class="tape tl"></i></div>'
             '<div class="chk pp" id="chk6"><svg viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7"/></svg></div>')
    S.append(section("s6b", "dark", t_f3, t_s7, inner, strip="FIX: SHOW FIRST"))
    whip("s6", "s6b", t_f3, -1)
    t_swap = t_f3 + .3
    js(f'tl.set("#cSh2, #cEx2", {{opacity: 1}}, {t_f3:.3f});')
    js(f'tl.fromTo("#cSh2", {{y: 250}}, {{y: 0, duration: .6, ease: "expo.inOut", immediateRender: false}}, {t_swap:.3f});')
    js(f'tl.fromTo("#cSh2", {{x: 0}}, {{keyframes: {{x: [0, 90, 0]}}, duration: .6, ease: "sine.inOut", immediateRender: false}}, {t_swap:.3f});')
    js(f'tl.fromTo("#cEx2", {{y: -250}}, {{y: 0, duration: .6, ease: "expo.inOut", immediateRender: false}}, {t_swap:.3f});')
    js(f'tl.fromTo("#cEx2", {{x: 0}}, {{keyframes: {{x: [0, -90, 0]}}, duration: .6, ease: "sine.inOut", immediateRender: false}}, {t_swap:.3f});')
    sfx("swish", t_swap)
    pop("#chk6", t_swap + .62, sc=.3, y=0)
    sfx("success", t_swap + .62)
    punch("s6b", t_swap + .62)

    # ---- S7 (light): "Fix these three and watch your next reel." A taped notebook checklist, red ticks, a counter
    t_s8 = L("l12", 0) - .14
    fixes = ["Start with the result", "Move in frame one", "Show, then explain"]
    rows = "".join(f'<div class="nrow" id="nr{k}"><b>{k + 1}.</b> {t}<svg class="tick" viewBox="0 0 60 50"><path id="tk{k}" pathLength="100" d="M5 28 L22 44 L55 6"/></svg></div>'
                   for k, t in enumerate(fixes))
    inner = (f'<div class="note pp" id="note7">{rows}<i class="tape tc"></i></div>'
             '<div class="ctr pp" id="ctr7"><div id="ctrn">312</div><div class="ctrl">views on your next reel</div></div>')
    S.append(section("s7", "light", t_s7, t_s8, inner, strip="THE FIX"))
    whip("s6b", "s7", t_s7)
    pop("#note7", t_s7 + .2, rot=-1.5, y=-120)
    for k in range(3):
        tt = L("l11", k) + .05
        js(f'tl.fromTo("#nr{k}", {{opacity: 0, x: -30}}, {{opacity: 1, x: 0, duration: .2, ease: "power3.out", immediateRender: false}}, {tt - .1:.3f});')
        js(f'tl.fromTo("#tk{k}", {{strokeDashoffset: 100}}, {{strokeDashoffset: 0, duration: .22, ease: "power2.out", immediateRender: false}}, {tt + .15:.3f});')
        sfx("type", tt + .15)
    t_c = L("l11", 4) - .05
    pop("#ctr7", t_c, rot=1.5, y=60)
    vals = [312, 900, 2400, 5200, 9800, 15400, 22100, 29300, 36100, 41800, 45600, 47600, 48200]
    for i, v in enumerate(vals):
        js(f'tl.set("#ctrn", {{textContent: "{v:,}"}}, {t_c + .1 + i * .075:.3f});')
    sfx("rise", t_c)
    sfx("ding", t_c + .1 + (len(vals) - 1) * .075)
    punch("s7", t_c + .1 + (len(vals) - 1) * .075)

    # ---- S8 (dark): CTA. "Save this so you don't forget, and comment HOOK for my list of twenty hooks that work."
    letters = "".join(f'<div class="hl pp hl{k}" id="hl{k}">{c}</div>' for k, c in enumerate("HOOK"))
    inner = (sunburst("sun8") + '<div class="bkm pp" id="bkm8"><svg viewBox="0 0 24 24"><path d="M6 3.5h12v17l-6-4.2-6 4.2z"/></svg></div>'
             '<div class="cbox pp" id="cbox8"><span id="cbph">Add a comment...</span><span id="cbk"></span><i id="caret"></i></div>'
             f'<div id="hook8">{letters}</div>')
    S.append(section("s8", "dark", t_s8, DUR + .5, inner, strip="COMMENT “HOOK”", push=.03))
    whip("s7", "s8", t_s8, -1)
    pop("#bkm8", L("l12", 0), sc=.3, y=0)
    sfx("pop", L("l12", 0))
    t_in = L("l12", 7) - .1
    pop("#cbox8", t_in, y=40)
    t_k = L("l12", 8) - .06
    js(f'tl.set("#cbph", {{display: "none"}}, {t_k:.3f});')
    for i, s_ in enumerate(["H", "HO", "HOO", "HOOK"]):
        js(f'tl.set("#cbk", {{textContent: "{s_}"}}, {t_k + i * .09:.3f});')
        sfx("type", t_k + i * .09)
    t_h = t_k + .45
    js(f'tl.fromTo("#sun8", {{rotation: 0, opacity: 0}}, {{rotation: 25, opacity: 1, duration: {DUR - t_h:.2f}, ease: "none", immediateRender: false}}, {t_h:.3f});')
    for k, rot in enumerate([-7, 5, -4, 8]):
        pop(f"#hl{k}", t_h + k * .1, d=.3, rot=rot, sc=1.8, y=-30)
        sfx("stamp" if k % 2 == 0 else "paper", t_h + k * .1 + .12)
    punch("s8", t_h + .35, .07)
    return "".join(H), "".join(S), (t_x, t_g, t_3)


CSS = f"""
@font-face {{ font-family: "Inter"; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
@font-face {{ font-family: "Fraunces"; font-weight: 700; src: url("assets/fonts/fraunces-latin-700-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: #222; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; font-family: "Inter"; color: {INK}; background: #222; }}
.fx {{ position: absolute; width: 0; height: 0; }}
/* paper worlds */
.sec {{ position: absolute; inset: 0; overflow: hidden; visibility: hidden; }}
.gnd {{ position: absolute; inset: 0; background-size: cover; }}
.gnd.light {{ background-image: url(assets/img/paper_light.jpg); }}
.gnd.mid {{ background-image: url(assets/img/paper_mid.jpg); }}
.gnd.dark {{ background-image: url(assets/img/paper_dark.jpg); }}
.cam {{ position: absolute; inset: 0; transform-origin: 50% 62%; }}
.punch {{ position: absolute; inset: 0; transform-origin: 50% 50%; }}
.floor {{ position: absolute; left: -60px; right: -60px; top: {FLOOR_Y}px; bottom: -80px; background-size: 1200px 1920px; background-position: 0 -400px;
  box-shadow: 0 -10px 24px rgba(0,0,0,.3); filter: url(#rough); }}
.floor.light {{ background-image: url(assets/img/paper_mid.jpg); }}
.floor.mid {{ background-image: url(assets/img/paper_dark.jpg); }}
.floor.dark {{ background-image: url(assets/img/paper_dark.jpg); filter: url(#rough) brightness(.5); }}
.sun {{ position: absolute; left: -1060px; top: -700px; width: 3200px; height: 3200px; opacity: 0; }}
.sun polygon {{ fill: rgba(255,255,255,.3); }}
#sun4b polygon, #sun8 polygon {{ fill: rgba(255,255,255,.07); }}
/* paper cut-outs: rough boiling edges + hard shadow */
.pp {{ filter: url(#rough) drop-shadow(7px 10px 0 rgba(0,0,0,.3)); }}
.tape {{ position: absolute; width: 110px; height: 38px; background: rgba(236,232,222,.75); box-shadow: 0 1px 2px rgba(0,0,0,.15); }}
.tape.tl {{ left: -34px; top: -10px; transform: rotate(-24deg); }}
.tape.tr {{ right: -34px; top: -10px; transform: rotate(22deg); }}
.tape.tc {{ left: 50%; margin-left: -55px; top: -20px; transform: rotate(-3deg); }}
.strip {{ position: absolute; left: 50%; top: 268px; height: 76px; display: flex; align-items: center; justify-content: center; white-space: nowrap;
  background: url(assets/img/paper_tile.jpg); font-weight: 800; font-size: 46px; letter-spacing: .02em; color: {INK};
  filter: url(#rough) drop-shadow(5px 8px 0 rgba(0,0,0,.3)); opacity: 0; z-index: 5; }}
/* ransom-note captions */
#caps {{ position: absolute; inset: 0; z-index: 9; pointer-events: none; }}
.scrap {{ position: absolute; height: 78px; display: flex; align-items: center; justify-content: center; white-space: nowrap;
  font-family: "Fraunces"; font-weight: 700; font-size: {CAP_SIZE}px; color: {INK}; background: url(assets/img/paper_tile.jpg);
  filter: url(#rough) drop-shadow(4px 6px 0 rgba(0,0,0,.35)); opacity: 0; }}
.scrap.red {{ background: {RED}; color: #fff; }}
.scrap .mk {{ position: absolute; left: -6px; right: -6px; top: 44%; height: 12px; background: {INK}; border-radius: 6px; transform: scaleX(0); transform-origin: left center; }}
/* cold open */
#slam {{ position: absolute; inset: 0; z-index: 8; }}
.scard {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; opacity: 0; background-size: cover; }}
.scard.light {{ background-image: url(assets/img/paper_light.jpg); }}
.scard.dark {{ background-image: url(assets/img/paper_dark.jpg); }}
.scard.redp {{ background-color: {RED}; background-image: url(assets/img/paper_light.jpg); background-blend-mode: multiply; }}
.sw {{ font-weight: 800; letter-spacing: -.04em; line-height: .9; white-space: nowrap; filter: url(#rough) drop-shadow(8px 12px 0 rgba(0,0,0,.28)); }}
#sc2w1, #sc2w2 {{ opacity: 0; }}
#cracks {{ position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; filter: url(#rough); }}
.crk {{ fill: none; stroke-dasharray: 1000; stroke-linejoin: round; stroke-linecap: round; }}
#cracks .under .crk {{ stroke: rgba(0,0,0,.8); stroke-width: 7; }}
#cracks .over .crk {{ stroke: rgba(255,255,255,.95); stroke-width: 3; }}
#glass {{ position: absolute; inset: 0; z-index: 8; opacity: 0; pointer-events: none; }}
.gp {{ position: absolute; inset: 0; filter: drop-shadow(6px 10px 0 rgba(0,0,0,.35)); }}
.ge {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
.ge polygon {{ fill: none; stroke: #fff; stroke-width: 6; }}
/* the phone */
.phone {{ position: absolute; border-radius: 64px; background: #1b1b1b; padding: 16px; }}
.scr {{ position: relative; width: 100%; height: 100%; border-radius: 50px; overflow: hidden; background: #2b2b2b; }}
.notch {{ position: absolute; left: 50%; top: 30px; width: 120px; height: 34px; margin-left: -60px; border-radius: 20px; background: #0d0d0d; z-index: 6; }}
.reel {{ position: absolute; inset: 0; background: linear-gradient(180deg, #8f8f8c, #5f5f5c 60%, #4a4a48); }}
.reel.nxt {{ top: 100%; background: linear-gradient(180deg, #b9b9b5, #7d7d7a); }}
#r4b {{ background: linear-gradient(180deg, #4a4a48, #232322 70%); }}
.person .hd {{ position: absolute; left: 165px; top: 250px; width: 108px; height: 128px; border-radius: 50%; background: #d7d5cf; }}
.person .bd {{ position: absolute; left: 92px; top: 390px; width: 254px; height: 420px; border-radius: 127px 127px 0 0; background: #c3c1bb; }}
.person.p2 .hd {{ background: #ecebe6; left: 120px; }} .person.p2 .bd {{ background: #dedcd6; left: 50px; }}
.person.p3 .hd {{ top: 330px; }} .person.p3 .bd {{ top: 470px; }}
.ln1, .ln2, .ln3 {{ position: absolute; left: 40px; height: 22px; border-radius: 11px; background: rgba(255,255,255,.5); }}
.ln1 {{ top: 520px; width: 300px; }} .ln2 {{ top: 560px; width: 220px; }} .ln3 {{ top: 600px; width: 260px; }}
.vtag {{ position: absolute; left: 24px; top: 90px; display: flex; align-items: center; gap: 10px; padding: 8px 16px; border-radius: 999px; background: rgba(255,255,255,.92);
  font-weight: 700; font-size: 28px; color: {INK}; }}
.vtag b {{ color: {RED}; }}
.play {{ width: 0; height: 0; border-left: 18px solid {INK}; border-top: 11px solid transparent; border-bottom: 11px solid transparent; }}
.pbar {{ position: absolute; left: 26px; right: 26px; bottom: 34px; height: 9px; border-radius: 5px; background: rgba(255,255,255,.35); }}
.pfill {{ position: absolute; left: 0; top: 0; bottom: 0; width: 100%; border-radius: 5px; background: #fff; transform-origin: left center; transform: scaleX(0); }}
#r4pb, #r5pb {{ background: {RED}; }}
.pbar .mk {{ position: absolute; left: 10%; top: -8px; width: 5px; height: 25px; border-radius: 2px; background: {RED}; }}
.thumb {{ position: absolute; left: 600px; top: 1150px; width: 120px; height: 120px; border-radius: 50%; background: url(assets/img/paper_tile.jpg);
  filter: url(#rough) drop-shadow(6px 10px 0 rgba(0,0,0,.35)); opacity: 0; z-index: 7; }}
.rtag {{ position: absolute; left: 150px; top: 430px; padding: 18px 30px; background: {RED}; color: #fff; font-weight: 800; font-size: 50px; white-space: nowrap;
  filter: url(#rough) drop-shadow(6px 10px 0 rgba(0,0,0,.35)); opacity: 0; z-index: 7; }}
.rstamp {{ position: absolute; left: 220px; top: 860px; width: 640px; padding: 14px 0; text-align: center; border: 9px solid {RED}; border-radius: 18px;
  color: {RED}; font-weight: 800; font-size: 62px; letter-spacing: .04em; white-space: nowrap; opacity: 0; z-index: 7; filter: url(#rough);
  background: rgba(255,255,255,.55); }}
.rstamp.white {{ color: #fff; border-color: #fff; background: rgba(0,0,0,.45); top: 1120px; }}
.bubble {{ position: absolute; left: 30px; right: 30px; top: 150px; padding: 18px 22px; border-radius: 26px; background: #fff; text-align: center; opacity: 0; }}
.bubble span {{ font-family: "Fraunces"; font-weight: 700; font-size: 40px; color: {INK}; }}
.res {{ position: absolute; left: 10px; right: 10px; top: 120px; text-align: center; }}
#res1 {{ font-weight: 800; font-size: 96px; letter-spacing: -.04em; color: #fff; opacity: 0; }}
#res2 {{ font-family: "Fraunces"; font-weight: 700; font-size: 36px; color: #e9e7e1; margin-top: 4px; opacity: 0; }}
.strip5 {{ position: absolute; left: 0; right: 0; top: 0; height: 300%; }}
.fi {{ position: relative; height: 33.3334%; overflow: hidden; background: linear-gradient(180deg, #a5a5a1, #6f6f6c); }}
.fi.p3 {{ background: linear-gradient(180deg, #828280, #4f4f4d); }}
.photo {{ position: absolute; inset: 40px 30px 120px; border: 14px solid #fff; overflow: hidden; background: linear-gradient(180deg, #cfcdc7, #9d9b96); }}
.sunc {{ position: absolute; left: 230px; top: 70px; width: 90px; height: 90px; border-radius: 50%; background: #f5f4f0; }}
.hill1 {{ position: absolute; left: -80px; top: 330px; width: 460px; height: 460px; border-radius: 50%; background: #5d5c59; }}
.hill2 {{ position: absolute; left: 140px; top: 390px; width: 420px; height: 420px; border-radius: 50%; background: #3f3e3c; }}
.paused {{ position: absolute; left: 50%; top: 42%; width: 130px; height: 130px; margin: -65px 0 0 -65px; border-radius: 50%; background: rgba(20,20,20,.75);
  display: flex; align-items: center; justify-content: center; gap: 18px; opacity: 0; }}
.paused i {{ width: 16px; height: 52px; border-radius: 4px; background: #fff; }}
/* cards */
.card3 {{ position: absolute; top: 760px; width: 270px; height: 360px; background: url(assets/img/paper_tile.jpg); display: grid; place-items: center; opacity: 0; }}
.card3 span {{ font-weight: 800; font-size: 210px; letter-spacing: -.05em; color: {INK}; }}
.arrow {{ position: absolute; left: 470px; top: 470px; width: 140px; height: 230px; opacity: 0; }}
.arrow svg {{ width: 100%; height: 100%; overflow: visible; }}
.arrow path {{ fill: none; stroke: {RED}; stroke-width: 18; stroke-linecap: round; stroke-linejoin: round; }}
.card2 {{ position: absolute; left: 130px; width: 820px; height: 210px; display: flex; align-items: center; gap: 34px; padding: 0 44px;
  background: url(assets/img/paper_tile.jpg); opacity: 0; }}
#cEx, #cSh2 {{ top: 600px; }} #cSh, #cEx2 {{ top: 850px; }}
.cn {{ width: 104px; height: 104px; border-radius: 50%; display: grid; place-items: center; font-weight: 800; font-size: 58px; background: {INK}; color: #fff; flex: none; }}
.card2 b {{ display: block; font-weight: 800; font-size: 76px; letter-spacing: -.02em; line-height: 1; }}
.card2 div i {{ display: block; font-family: "Fraunces"; font-style: normal; font-weight: 700; font-size: 34px; opacity: .65; margin-top: 8px; }}
#cSh2 {{ background: {RED}; color: #fff; }} #cSh2 .cn {{ background: #fff; color: {RED}; }}
.chk {{ position: absolute; left: 840px; top: 540px; width: 140px; height: 140px; border-radius: 50%; background: #fff; display: grid; place-items: center; opacity: 0; }}
.chk svg {{ width: 90px; height: 90px; fill: none; stroke: {RED}; stroke-width: 3.4; stroke-linecap: round; stroke-linejoin: round; }}
/* notebook + counter */
.note {{ position: absolute; left: 110px; top: 450px; width: 860px; padding: 40px 50px 34px 110px; background-color: #f7f6f1;
  background-image: repeating-linear-gradient(180deg, transparent 0 86px, rgba(60,60,60,.22) 86px 89px), linear-gradient(90deg, transparent 0 84px, rgba(232,38,42,.55) 84px 87px, transparent 87px);
  opacity: 0; }}
.nrow {{ position: relative; height: 89px; display: flex; align-items: center; font-family: "Fraunces"; font-weight: 700; font-size: 50px; color: {INK}; white-space: nowrap; opacity: 0; }}
.nrow b {{ margin-right: 18px; }}
.tick {{ position: absolute; right: -10px; top: 12px; width: 70px; height: 60px; overflow: visible; }}
.tick path {{ fill: none; stroke: {RED}; stroke-width: 9; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 100; stroke-dashoffset: 100; }}
.ctr {{ position: absolute; left: 190px; top: 900px; width: 700px; padding: 26px 0 30px; text-align: center; background: {INK}; color: #fff; opacity: 0; }}
#ctrn {{ font-weight: 800; font-size: 170px; letter-spacing: -.05em; line-height: 1; font-variant-numeric: tabular-nums; }}
.ctrl {{ font-family: "Fraunces"; font-weight: 700; font-size: 40px; color: #d9d7d1; margin-top: 4px; }}
/* CTA */
.bkm {{ position: absolute; left: 470px; top: 410px; width: 140px; height: 170px; opacity: 0; }}
.bkm svg {{ width: 100%; height: 100%; overflow: visible; }}
.bkm path {{ fill: #f1efea; stroke: none; }}
.cbox {{ position: absolute; left: 110px; top: 640px; width: 860px; height: 132px; border-radius: 999px; display: flex; align-items: center; padding: 0 46px;
  background: url(assets/img/paper_tile.jpg); font-size: 50px; font-weight: 800; color: {INK}; opacity: 0; }}
#cbph {{ font-family: "Fraunces"; font-weight: 700; color: rgba(0,0,0,.45); }}
#caret {{ width: 5px; height: 56px; margin-left: 6px; background: {INK}; border-radius: 2px; }}
#hook8 {{ position: absolute; left: 0; right: 0; top: 880px; display: flex; justify-content: center; gap: 14px; }}
.hl {{ width: 210px; height: 270px; display: grid; place-items: center; font-weight: 800; font-size: 230px; line-height: 1; opacity: 0; }}
.hl0 {{ background: {RED}; color: #fff; }} .hl1 {{ background: url(assets/img/paper_tile.jpg); color: {INK}; }}
.hl2 {{ background: #0e0e0e; color: #fff; outline: 4px solid #f1efea; }} .hl3 {{ background: url(assets/img/paper_tile.jpg); color: {RED}; font-family: "Fraunces"; }}
/* numerals + shards */
.bign {{ position: absolute; left: 0; right: 0; text-align: center; font-weight: 800; font-size: {NUM_SIZE}px; line-height: 1; color: {INK}; opacity: 0; }}
#shards {{ position: absolute; inset: 0; z-index: 10; pointer-events: none; }}
.shd {{ position: absolute; opacity: 0; }}
"""


def main():
    H, S, (t_x, t_g, t_3) = scenes()
    captions([f"l{i:02d}" for i in range(1, 13)])
    sh = shards(t_x, t_g, t_3)
    # stop-motion boil: the edge filter's noise changes 12 times a second
    for i in range(int(DUR * 12)):
        js(f'tl.set("#roughT", {{attr: {{seed: {i % 9 + 1}}}}}, {i / 12:.3f});')
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>Reel flop explainer 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      <svg class="fx"><defs><filter id="rough" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence id="roughT" type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="1"/>
        <feDisplacementMap in="SourceGraphic" scale="7" xChannelSelector="R" yChannelSelector="G"/></filter></defs></svg>
      {S}
      {H}
      <div id="caps">{"".join(CAP)}</div>
      {sh}
      <audio id="vo" src="assets/audio/vo.wav" data-start="0" data-duration="{DUR}" data-track-index="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(sorted(SFX, key=lambda e: e["t"]), open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
    print(f"wrote index.html, {len(A)} timeline lines, {len(SFX)} sfx cues, {DUR} s")


if __name__ == "__main__":
    main()
