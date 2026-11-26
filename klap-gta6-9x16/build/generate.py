"""Klap brand reel v2, "GTA 6 clippers" (9:16): writes index.html, plan/sfx_events.json, plan/edit.json and
plan/music_plan.json (read by build/music.py).

v2 (owner: no AI.NXTLVL logo, better fonts, smoother and more creative motion, alignment, a real voice): Klap's own
palette (ink #020617, violet-500 #8b5cf6, Poppins for UI) with Clash Display for the headlines, every scene rebuilt as
motion design on one grid (headline band 300-540, stage 600-1400, live caption 1470; everything centred or symmetric),
per-word headlines with a violet pill on the key phrase, zoom-through / whip transitions, speed-ramped GTA 6 cuts on the
beat, a 3D feed wall with reel UI, a payout stack with a rolling counter, a 3D filmstrip scrub for the "3-hour stream",
the logo built letter by letter on the music drop, Klap's app rebuilt in HTML with Klap's own wording, virality rings,
a 16:9 -> 9:16 reframe into the Gaming layout, word-pop captions, a split payoff and the CTA.

Footage: Rockstar Games' official GTA 6 promo clips (owner's standing exception: muted footage), Pexels 6878208 facecam.
MrBeast and IShowSpeed appear by name only (owner's call). Facts: klap.app and klap.app/for/clippers (2026-11-25).
One paused GSAP timeline; counters are pure functions of time (hf-seek).
python3 build/generate.py
"""
import json
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = []
for w in json.load(open(os.path.join(ROOT, "plan", "words.json"))):
    if W and w["w"][:1] in ".,-?" and W[-1]["line"] == w["line"]:
        W[-1]["w"] += w["w"]; W[-1]["t1"] = w["t1"]
    else:
        W.append(dict(w))
JS, SFX, HTML = [], [], []
INK, VIOLET, VIOLET2, GREEN, RED = "#020617", "#8b5cf6", "#6d3df0", "#22c55e", "#ff3b5c"


def js(s):
    JS.append(s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(max(0, t), 3)})


def ft(sel, t, d, frm, to_, ease="expo.out"):
    js(f'tl.fromTo("{sel}", {frm}, {{...{to_}, duration: {d}, ease: "{ease}", immediateRender: false}}, {max(0, t):.3f});')


def to(sel, t, d, props, ease="power2.out"):
    js(f'tl.to("{sel}", {{...{props}, duration: {d}, ease: "{ease}"}}, {max(0, t):.3f});')


def st(sel, t, props):
    js(f'tl.set("{sel}", {props}, {max(0, t):.3f});')


def key(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def wt(words, n=0, after=0.0, end=False):
    words = words if isinstance(words, (list, tuple)) else [words]
    hits = [w for w in W if w["t0"] >= after and any(key(w["w"]).startswith(x) for x in words)]
    if not hits:
        raise SystemExit(f"none of {words} after {after}")
    h = hits[min(n, len(hits) - 1)]
    return h["t1"] if end else h["t0"]


TRK = [0]


def vid(i, src, t0, t1, media=0.0, cls="fill", extra=""):
    TRK[0] += 1
    return (f'<video id="{i}" class="{cls}" src="assets/video/{src}.mp4" data-start="{t0:.3f}" data-duration="{max(.1, t1 - t0):.3f}" '
            f'data-media-start="{media:.3f}" data-track-index="{TRK[0]}" muted playsinline {extra}></video>')


END = max(w["t1"] for w in W)
DUR = round(END + 1.6, 2)
T = {}
T["clips"] = wt("clips"); T["feed"] = wt("feed"); T["clippers"] = wt("clippers"); T["paid"] = wt("paid"); T["views1"] = wt("views")
T["beast"] = wt(["mrbeast", "mr"]); T["speed"] = wt(["ishowspeed", "ishow", "i"], after=T["beast"] + .2); T["dollar"] = wt("dollar")
T["thousand"] = wt("thousand"); T["hard"] = wt("hard"); T["moment"] = wt("moment"); T["three"] = wt(["three", "3"], after=T["hard"])
T["crazy"] = wt("crazy"); T["chase"] = wt("chase"); T["tool"] = wt("tool"); T["klap"] = wt(["klap", "clap"])
T["klaphit"] = wt(["klap", "clap"], end=True) - .03
T["paste"] = wt("paste"); T["link"] = wt("link"); T["picks"] = wt("picks"); T["scores"] = wt("scores"); T["viral"] = wt("viral")
T["cuts"] = wt("cuts"); T["vertical"] = wt("vertical"); T["gameplay"] = wt("gameplay"); T["streamer"] = wt("streamer")
T["captions"] = wt("captions"); T["pop"] = wt("pop", after=T["captions"]); T["so"] = wt("so", after=T["pop"])
T["scrub"] = wt("scrubbing"); T["your"] = wt("your", after=T["scrub"]); T["up"] = wt("up", after=T["your"])
T["cta"] = wt("comment"); T["kw"] = wt(["klap", "clap"], after=T["cta"]); T["bio"] = wt("bio"); T["end"] = DUR

# ---- music plan: "Miami" by Lyvo. Full energy under the hook, its breakdown from "the hard part", the kick slams back
# (track 120.024 s) right after the name "Klap". Two segments on one beat grid (offsets differ by whole beats).
BEATS = json.load(open(os.path.join(ROOT, "sfx", "music", "beats_miami.json")))
BI = BEATS["beat_interval_s"]
DROP = 120.024
o2 = DROP - T["klaphit"]
b_break = min(BEATS["beats_s"], key=lambda b: abs(b - 60.0))
n = round((o2 - (b_break - T["hard"] + .05)) / BI)
o1 = o2 - n * BI
CUT = T["klaphit"] - 4 * BI
grid = [b - o1 for b in BEATS["beats_s"] if 0 <= b - o1 < CUT] + [b - o2 for b in BEATS["beats_s"] if CUT <= b - o2 < DUR]
GAP = [T["klap"] - .08, T["klaphit"] - .01]
json.dump({"track": "sfx/music/m3_miami.mp3", "o1": round(o1, 4), "o2": round(o2, 4), "cut": round(CUT, 4), "dur": DUR, "gap": [round(g, 3) for g in GAP]},
          open(os.path.join(ROOT, "plan", "music_plan.json"), "w"), indent=1)

# ---- scenes
S = {}
S["A"] = (0, T["feed"] - .35)
S["B"] = (S["A"][1], T["beast"] - .3)          # the feed wall, with the payouts stacked on it from T.clippers
S["D"] = (S["B"][1], T["hard"] - .25)
S["E"] = (S["D"][1], T["klaphit"])
S["G"] = (S["E"][1], T["paste"] - .3)
S["H"] = (S["G"][1], T["picks"] - .25)
S["I"] = (S["H"][1], T["cuts"] - .25)
S["J"] = (S["I"][1], T["so"] - .25)             # reframe, then the captions
S["J"] = (S["J"][0], T["so"] - .1); S["L"] = (T["so"] - .1, T["cta"] + .35)
S["M"] = (S["L"][1], DUR)   # the CTA scene lands as "Comment" finishes; its headline rides in with it
for k, (a, b) in S.items():
    if k != "A":
        st(f"#s{k}", a - .18, "{opacity: 1}")
    if b < DUR:
        st(f"#s{k}", b + .12, "{opacity: 0}")


def zoom_in(k, d=.6):
    a = S[k][0] - .18
    ft(f"#s{k}", a, d, "{scale: .84, opacity: 0, filter: 'blur(10px)'}", "{scale: 1, opacity: 1, filter: 'blur(0px)'}", "expo.out")
    sfx("whoosh", a)


def zoom_out(k):
    b = S[k][1]
    to(f"#s{k}", b - .3, .34, "{scale: 1.24, opacity: 0, filter: 'blur(10px)'}", "power2.in")


def whip_in(k, d=1):
    a = S[k][0] - .18
    ft(f"#s{k}", a, .55, f"{{x: {1100 * d}, opacity: 1, filter: 'blur(12px)'}}", "{x: 0, opacity: 1, filter: 'blur(0px)'}", "expo.out")
    sfx("whoosh_big", a)


def whip_out(k, d=1):
    b = S[k][1]
    to(f"#s{k}", b - .28, .3, f"{{x: {-1100 * d}, filter: 'blur(12px)'}}", "power3.in")


def flash(t, op=.5, d=.4):
    st("#flash", t - .01, f"{{opacity: {op}}}"); to("#flash", t, d, "{opacity: 0}", "power2.out")


def shake(t, amp=9):
    for i, (dx, dy) in enumerate(((1, -.8), (-.8, .6), (.6, -.4), (-.3, .2), (0, 0))):
        st("#shake", t + i * .034, f"{{x: {dx * amp:.1f}, y: {dy * amp:.1f}}}")


# ---- headlines: per-word reveal, a violet pill on the key phrase ([...])
def head_html(k, lines, big=False):
    out = []
    for ln in lines:
        ln = re.sub(r"\]([.,?!:]+)", lambda m: m.group(1) + "]", ln)
        parts = re.split(r"(\[[^\]]+\])", ln)
        spans = []
        for p in parts:
            if not p.strip():
                continue
            if p.startswith("["):
                spans.append(f'<span class="w pw"><i></i><b>{p[1:-1]}</b></span>')
            else:
                spans.extend(f'<span class="w">{x}</span>' for x in p.split())
        out.append(f'<div class="ln">{"".join(spans)}</div>')
    HTML.append(f'<div class="hd{" big" if big else ""}{" on" if k == 0 else ""}" id="hd{k}">{"".join(out)}</div>')


HEADS = [(0.0, ["GTA 6 is out."], True),
         (T["clips"] - .05, ["GTA clips are", "taking over [every feed]."], False),
         (T["clippers"] - .1, ["Clippers get [paid]", "for views."], False),
         (T["beast"] - .15, ["Big campaigns pay", "[per 1,000 views]."], False),
         (T["hard"] - .1, ["The hard part:", "finding [the moment]."], False),
         (T["three"] - .08, ["3-hour stream.", "[One crazy chase]."], False),
         (T["tool"] - .08, ["This tool", "[finds it] for you."], False),
         (T["klaphit"] - .2, None, False),
         (T["paste"] - .1, ["Paste the", "[stream link]."], False),
         (T["picks"] - .1, ["It picks the moments", "and [scores each one]."], False),
         (T["cuts"] - .1, ["Cut [vertical],", "streamer in frame."], False),
         (T["captions"] - .1, ["Captions", "that [pop]."], False),
         (T["so"] - .05, ["Still on hour two?", "[Your clip] is up."], False),
         (T["cta"] + .2, ["Comment", "[KLAP]."], False)]
for k, (t0, lines, big) in enumerate(HEADS):
    t1 = HEADS[k + 1][0] if k + 1 < len(HEADS) else DUR + 1
    if lines is None:
        continue
    head_html(k, lines, big)
    if k == 0:
        ft("#hd0", 0, .7, "{scale: 1.1}", "{scale: 1}", "expo.out")
    else:
        st(f"#hd{k}", t0, "{opacity: 1}")
        ft(f"#hd{k} .w", t0, .62, "{y: 48, opacity: 0, rotateX: -35}", "{y: 0, opacity: 1, rotateX: 0, stagger: .055}", "expo.out")
        ft(f"#hd{k} .pw i", t0 + .3, .5, "{scaleX: 0}", "{scaleX: 1}", "expo.out")
        if k == 12:   # "Your clip is up." lands on "your"
            st("#hd12 .ln:nth-child(2) .w", t0 + .05, "{opacity: 0}")
            ft("#hd12 .ln:nth-child(2) .w", T["your"] - .08, .62, "{y: 48, opacity: 0, rotateX: -35}", "{y: 0, opacity: 1, rotateX: 0, stagger: .055}", "expo.out")
            ft("#hd12 .pw i", T["your"] + .2, .5, "{scaleX: 0}", "{scaleX: 1}", "expo.out")
    if t1 < DUR:
        to(f"#hd{k}", t1 - .16, .16, "{opacity: 0, y: -26, filter: 'blur(6px)'}", "power2.in")
    sfx("swish", t0 - .05)

# ---- live caption, three words at a time
CAPFIX = {"PAID": "paid", "AND": "and"}


def capword(w):
    core = w.strip(".,?!")
    if core.isupper() and len(core) > 3 and core in CAPFIX:
        return w.replace(core, CAPFIX[core])
    return w


k = 0
for i in range(0, len(W), 3):
    chunk = W[i:i + 3]
    nxt = W[i + 3]["t0"] if i + 3 < len(W) else chunk[-1]["t1"] + .25
    if nxt - chunk[-1]["t1"] > .6:
        nxt = chunk[-1]["t1"] + .35
    spans = " ".join(f'<span id="cw{k}_{j}">{capword(w["w"])}</span>' for j, w in enumerate(chunk))
    HTML.append(f'<div class="cap" id="cp{k}">{spans}</div>')
    ft(f"#cp{k}", chunk[0]["t0"] - .06, .14, "{opacity: 0, y: 10}", "{opacity: 1, y: 0}", "power2.out")
    for j, w in enumerate(chunk):
        ft(f"#cw{k}_{j}", w["t0"] - .04, .12, "{color: 'rgba(255,255,255,.4)'}", "{color: '#ffffff'}", "none")
    to(f"#cp{k}", nxt - .06, .06, "{opacity: 0}", "none")
    k += 1

# ================= A: the hook, speed-ramped GTA 6 cuts on the beat (each clip's whip lands on the cut)
a0, a1 = S["A"]
CLIPS = {"h_flip": 1.6, "h_heli": 2.0, "h_cops": 1.9, "h_truck": 2.3, "h_shoot": 1.2}
SEQ = ["h_flip", "h_heli", "h_cops", "h_truck", "h_shoot"]
beats_a = [b for b in grid if .45 < b < a1 - .3]
cuts = [0.0] + beats_a[1::2]
A_HTML = []
for j, c in enumerate(cuts):
    c1 = cuts[j + 1] if j + 1 < len(cuts) else a1 + .4
    src = SEQ[j % len(SEQ)]
    seg = c1 - c
    media = max(0.0, CLIPS[src] - seg - .02)
    A_HTML.append(f'<div class="clipw" id="aw{j}">{vid(f"av{j}", src, c, c1 + .02, media)}</div>')
    if j:
        st(f"#aw{j}", c, "{opacity: 1}")
        ft(f"#aw{j}", c, .7, "{scale: 1.16}", "{scale: 1.0}", "expo.out")
        flash(c, .35, .3); shake(c, 6)
        sfx("thump", c); sfx("swish", c - .08)
        st(f"#aw{j - 1}", c + .03, "{opacity: 0}")
ft("#aw0", 0, .9, "{scale: 1.22}", "{scale: 1.0}", "expo.out")
to("#sA", a1 - .3, .36, "{scale: .42, opacity: 0, borderRadius: '70px'}", "power3.in")
sfx("whoosh_big", a1 - .3)

# ================= B: every feed (3D wall with reel UI), then the payouts stack on it
b0, b1 = S["B"]
TILES = ["t_cops", "t_flip", "t_heli", "t_boat", "t_scoot", "t_truck", "t_ball", "t_dive"]
HANDLES = [("gta6.moments", "2.4M"), ("vicecityclips", "891K"), ("leonidaplays", "1.2M"), ("gtaclipz", "640K"),
           ("jason.and.lucia", "3.1M"), ("chase.cam", "415K"), ("gta6daily", "1.8M"), ("clipgodvi", "720K")]
ICONS = ('<svg viewBox="0 0 24 24"><path d="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 3 4.5 6.8 4.5c2.1 0 3.5 1.1 5.2 3 1.7-1.9 3.1-3 5.2-3 3.8 0 5.9 3.9 4.4 7.3C19.5 16.4 12 21 12 21z"/></svg>'
         '<svg viewBox="0 0 24 24"><path d="M12 3C6.5 3 2 6.8 2 11.4c0 2.4 1.2 4.6 3.2 6.1L4 21l4.3-2.1c1.2.3 2.4.5 3.7.5 5.5 0 10-3.8 10-8.4S17.5 3 12 3z"/></svg>'
         '<svg viewBox="0 0 24 24"><path d="M3 11.5 21 3l-6.5 18-3-7.5z"/></svg>')
B_COLS = []
for c in range(3):
    tiles = ""
    for r in range(4):
        n_ = c * 4 + r
        h, v = HANDLES[n_ % 8]
        tiles += (f'<div class="tile">{vid(f"tv{n_}", TILES[(c * 3 + r) % 8], b0 - .2, b1 + .3 + n_ * .013, (c * 1.3 + r * .7) % 4)}'
                  f'<div class="tgrad"></div><div class="tic">{ICONS}</div><div class="tmeta"><b>@{h}</b><span>{v} views</span></div></div>')
    B_COLS.append(f'<div class="col" id="col{c}">{tiles}</div>')
    ft(f"#col{c}", b0 - .2, b1 - b0 + .6, f"{{y: {-260 if c % 2 else -640}}}", f"{{y: {-640 if c % 2 else -260}}}", "none")
st("#sB", b0 - .2, "{opacity: 1}")
ft("#wall", b0 - .2, 1.1, "{scale: 2.4, rotateX: 40, rotateZ: -4, opacity: 0}", "{scale: 1, rotateX: 24, rotateZ: -10, opacity: 1}", "expo.out")
ft("#wall", b0 + .9, b1 - b0, "{rotateZ: -10, scale: 1}", "{rotateZ: -7, scale: 1.06}", "sine.inOut")
sfx("whoosh", b0 - .1)
tp = T["clippers"] - .05
to("#bdim", tp, .5, "{opacity: 1}")
ft("#earn", tp, .6, "{opacity: 0, y: 40, scale: .9}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.6)")
sfx("pop", tp)
for i in range(3):
    ft(f"#pay{i}", T["paid"] - .05 + i * .2, .6, "{opacity: 0, x: 260, rotateZ: 5}", "{opacity: 1, x: 0, rotateZ: 0}", "back.out(1.5)")
    sfx("cash", T["paid"] + i * .2); sfx("notify", T["paid"] + .08 + i * .2)
for i in range(9):
    sfx("tick", T["paid"] + .1 + i * .11)
whip_out("B")

# ================= D: the campaigns (names only), the rate
whip_in("D")
ft("#cardA", T["beast"] - .1, .6, "{opacity: 0, x: -200, rotateY: 30}", "{opacity: 1, x: 0, rotateY: 0}", "back.out(1.4)")
ft("#cardB", T["speed"] - .1, .6, "{opacity: 0, x: 200, rotateY: -30}", "{opacity: 1, x: 0, rotateY: 0}", "back.out(1.4)")
sfx("swish", T["beast"] - .1); sfx("swish", T["speed"] - .1)
ft("#rate", T["dollar"] - .05, .55, "{opacity: 0, scale: .55, y: 30}", "{opacity: 1, scale: 1, y: 0}", "back.out(1.9)")
flash(T["dollar"], .3); sfx("stamp", T["dollar"]); sfx("cash", T["dollar"] + .12)
ft("#rate .per", T["thousand"] - .05, .4, "{opacity: 0, x: -24}", "{opacity: 1, x: 0}", "expo.out")
ft("#vbar, #vwN", T["thousand"] - .05, .35, "{opacity: 0}", "{opacity: 1}", "none")
ft("#vfill", T["thousand"], .9, "{scaleX: 0}", "{scaleX: 1}", "power2.inOut")
ft("#veq", T["thousand"] + .85, .35, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}", "back.out(2.2)")
sfx("success", T["thousand"] + .9)
for c_ in ("#cardA .chip", "#cardB .chip"):
    ft(c_, T["thousand"] + .1, .35, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}", "back.out(2)")
ft("#dbgv", S["D"][0] - .2, S["D"][1] - S["D"][0] + .4, "{scale: 1.15}", "{scale: 1.28}", "none")
zoom_out("D")

# ================= E: the 3-hour stream (filmstrip scrub), the chase, the find, the drop
zoom_in("E")
e0, e1 = S["E"]
N_FR, FRW, FRG, CH = 16, 360, 16, 11
tx0, tx1 = -(FRW / 2), -(CH * (FRW + FRG) + FRW / 2)
st("#strip", 0, "{rotateX: 14, transformPerspective: 1400}")
ft("#strip", e0 - .1, T["chase"] - .1 - (e0 - .1), f"{{x: {tx0 + 160}}}", f"{{x: {tx1}}}", "power3.inOut")
ft("#stripw", e0 - .18, .9, "{scale: 1.25, opacity: 0}", "{scale: 1, opacity: 1}", "expo.out")
for i in range(10):
    sfx("tick", e0 + .3 + i * (T["chase"] - e0 - .6) / 10)
sfx("riser_short", T["chase"] - 1.3)
ft("#tl3", T["three"] - .05, .45, "{scale: .6, color: '#ffffff'}", f"{{scale: 1, color: '{RED}'}}", "back.out(2.4)")
sfx("stamp", T["three"])
tc = T["chase"] - .1
st("#fr11", tc, "{zIndex: 5}")
ft("#fr11", tc, .55, "{scale: 1, filter: 'grayscale(1) brightness(.55)'}", "{scale: 1.42, filter: 'grayscale(0) brightness(1)'}", "back.out(1.5)")
to(".fr:not(#fr11)", tc, .5, "{opacity: .22}")
ft("#spike", tc, .4, "{opacity: 0, scaleY: 0}", "{opacity: 1, scaleY: 1}", "back.out(2)")
ft("#pin", tc + .05, .45, "{opacity: 0, y: 26, scale: .8}", "{opacity: 1, y: 0, scale: 1}", "back.out(2)")
flash(tc, .45, .4); shake(tc, 10)
sfx("impact", tc); sfx("screech", T["crazy"] - .1)
tf = T["tool"] - .05
ft("#scan", tf, .75, "{x: -620, opacity: 0}", "{x: 620, opacity: 1}", "power2.inOut")
to("#scan", tf + .7, .15, "{opacity: 0}")
sfx("riser_short", tf)
st("#selbox", tf + .34, "{opacity: 1}")
ft("#selbox", tf + .35, .6, "{attr: {'stroke-dashoffset': 2600}}", "{attr: {'stroke-dashoffset': 0}}", "power2.inOut")
to("#pin", tf + .4, .25, "{opacity: 0, y: -14}", "power2.in")
ft("#foundTag", tf + .8, .4, "{opacity: 0, y: 16}", "{opacity: 1, y: 0}", "back.out(2)")
sfx("g_pickup", tf + .85)
ft("#fr11", tf + .8, .6, "{scale: 1.42}", "{scale: 1.6}", "expo.out")
to("#stripw", tf + .8, .6, "{y: -40}", "expo.out")
tk = T["klaphit"]
sfx("riser_short", tk - .7)
to("#sE", tk - .12, .14, "{scale: 1.3, opacity: 0, filter: 'blur(12px)'}", "power2.in")

# ================= G: the reveal (logo built on the kick)
st("#sG", tk - .02, "{opacity: 1}")
flash(tk, .85, .55); shake(tk, 12)
for i, (sc, d_) in enumerate(((.2, .9), (.2, 1.3))):
    st(f"#kring{i}", tk - .01 + i * .1, f"{{opacity: .9, scale: {sc}}}")
    to(f"#kring{i}", tk + i * .1, d_, "{opacity: 0, scale: 3.2}", "power2.out")
ft("#kicon", tk, .7, "{opacity: 0, scale: .1, rotateZ: -40}", "{opacity: 1, scale: 1, rotateZ: 0}", "back.out(2.0)")
for i, L in enumerate("Klap"):
    ft(f"#kl_{L}", tk + .18 + i * .07, .6, "{opacity: 0, y: 90, rotateX: 50}", "{opacity: 1, y: 0, rotateX: 0}", "back.out(1.6)")
    sfx("g_pop", tk + .18 + i * .07)
for i in range(24):
    ang = i * 15 + (i % 2) * 7
    dx, dy = math.cos(math.radians(ang)) * (420 + (i % 3) * 90), math.sin(math.radians(ang)) * (420 + (i % 3) * 90)
    ft(f"#pt{i}", tk, .9 + (i % 4) * .15, "{opacity: 1, x: 0, y: 0, scale: 1}", f"{{opacity: 0, x: {dx:.0f}, y: {dy:.0f}, scale: .2}}", "power3.out")
ft("#ktag", tk + .55, .5, "{opacity: 0, y: 24}", "{opacity: 1, y: 0}", "expo.out")
st("#kglow", tk - .01, "{opacity: 1, scale: .6}"); to("#kglow", tk, 1.4, "{opacity: .55, scale: 1.1}", "power2.out")
sfx("impact", tk); sfx("whoosh_big", tk + .02); sfx("sparkle", tk + .25)
zoom_out("G")

# ================= H: paste the stream link, Generate
zoom_in("H")
h0 = S["H"][0]
ft(".app", h0 - .18, .9, "{y: 60, rotateX: 8}", "{y: 0, rotateX: 0}", "expo.out")
ft("#cursor", h0, .7, "{x: 420, y: 260, opacity: 0}", "{x: 0, y: 0, opacity: 1}", "power3.inOut")
tpa = T["paste"]
ft("#kv", tpa - .05, .3, "{opacity: 0, scale: .6, y: 10}", "{opacity: 1, scale: 1, y: 0}", "back.out(2.4)")
to("#kv", T["link"] + .5, .2, "{opacity: 0}")
st("#ph", tpa + .04, "{opacity: 0}")
URL = "twitch.tv/videos/2290158741"
for i, ch in enumerate(URL):
    st(f"#u{i}", tpa + .04 + i * .018, "{opacity: 1}")
sfx("click", tpa); sfx("typing", tpa + .05)
tg = T["link"] + .45
ft("#cursor", tg - .35, .35, "{x: 0, y: 0}", "{x: 300, y: 0}", "power2.inOut")
ft("#gen", tg, .1, "{scale: 1}", "{scale: .92}", "power2.out"); to("#gen", tg + .1, .35, "{scale: 1}", "back.out(3)")
st("#ripple", tg, "{opacity: .5, scale: .3}"); to("#ripple", tg + .02, .6, "{opacity: 0, scale: 2.2}", "power2.out")
sfx("click", tg); sfx("pop", tg + .05)
ft("#prog", tg + .2, .4, "{opacity: 0, y: 16}", "{opacity: 1, y: 0}", "expo.out")
ft("#progbar", tg + .25, max(.6, S["H"][1] - tg - .2), "{scaleX: 0}", "{scaleX: 1}", "power1.inOut")
ft("#shim", tg + .25, 1.2, "{x: -400}", "{x: 1000}", "none")
zoom_out("H")

# ================= I: best moments, virality rings
zoom_in("I")
CIRC = round(2 * math.pi * 40, 1)
SCORES = (94, 99, 87)
for i, (dx, rot, dl) in enumerate(((-300, 16, .14), (0, 0, 0), (300, -16, .26))):
    ft(f"#mc{i}", T["picks"] - .1 + dl, .7, f"{{opacity: 0, y: 220, rotateY: {rot * 2.5}, scale: .8}}", f"{{opacity: 1, y: 0, rotateY: {rot}, scale: 1}}", "back.out(1.3)")
    sfx("g_pop", T["picks"] - .1 + dl)
for i in range(3):
    ts = T["scores"] + i * .14
    ft(f"#vb{i}", ts, .35, "{opacity: 0, scale: .5}", "{opacity: 1, scale: 1}", "back.out(2.4)")
    ft(f"#ring{i}", ts + .05, .9, f"{{attr: {{'stroke-dashoffset': {CIRC}}}}}", f"{{attr: {{'stroke-dashoffset': {CIRC * (1 - SCORES[i] / 100):.1f}}}}}", "power2.out")
    for q in range(6):
        sfx("tick", ts + q * .08)
ft("#top", T["viral"] - .1, .5, "{opacity: 0, y: 20, scale: .7}", "{opacity: 1, y: 0, scale: 1}", "back.out(2.2)")
ft("#mc1 .glow", T["viral"] - .1, .6, "{opacity: 0}", "{opacity: 1}")
ft("#mc1", T["viral"] - .1, .6, "{scale: 1}", "{scale: 1.06}", "back.out(2)")
ft("#rankpill", T["viral"] + .1, .5, "{opacity: 0, y: 24}", "{opacity: 1, y: 0}", "expo.out")
sfx("g_levelup", T["viral"])
zoom_out("I")

# ================= J: reframe 16:9 -> 9:16 (Gaming layout), then captions that pop
zoom_in("J")
j0 = S["J"][0]
st("#trk", j0 + .09, "{opacity: 1}")
ft("#trk", j0 + .1, .5, "{attr: {'stroke-dashoffset': 1000}}", "{attr: {'stroke-dashoffset': 0}}", "power2.inOut")
ft("#trkl", j0 + .5, .35, "{opacity: 0, y: 10}", "{opacity: 1, y: 0}", "expo.out")
sfx("g_tick", j0 + .15); sfx("g_tick", j0 + .55)
tv = T["vertical"] - .08
to("#land", tv, .6, "{scale: .47, y: 262, opacity: 0}", "power3.inOut")
ft("#fc1", tv, .6, "{x: 0, y: 0, scale: 1}", "{x: -270, y: -340, scale: 1.5}", "power3.inOut")
to("#fc1", tv + .55, .08, "{opacity: 0}")
to("#trk, #trkl", tv, .2, "{opacity: 0}")
ft("#phone", tv + .05, .7, "{opacity: 0, scale: .6, y: 60}", "{opacity: 1, scale: 1, y: 0}", "expo.out")
ft("#fc2", tv + .55, .2, "{opacity: 0}", "{opacity: 1}", "none")
sfx("whoosh", tv); sfx("shutter", tv + .55)
ft("#lyt", tv + .6, .4, "{opacity: 0, scale: .7}", "{opacity: 1, scale: 1}", "back.out(2)")
ft("#lg", T["gameplay"] - .05, .4, "{opacity: 0, x: -30}", "{opacity: 1, x: 0}", "back.out(2)")
ft("#ls", T["streamer"] - .05, .4, "{opacity: 0, x: -30}", "{opacity: 1, x: 0}", "back.out(2)")
sfx("pop", T["gameplay"]); sfx("pop", T["streamer"])
to("#lg, #ls, #lyt", T["captions"] - .25, .2, "{opacity: 0}")
CAPW = ["NO", "WAY", "HE", "MADE", "THAT"]
tcap = T["captions"]
for i, w in enumerate(CAPW):
    tw = tcap + i * .17
    ft(f"#kc{i}", tw, .25, "{opacity: 0, scale: 1.9, rotateZ: -6}", "{opacity: 1, scale: 1, rotateZ: 0}", "back.out(2.6)")
    st(f"#kc{i}", tw, f"{{color: '{VIOLET}'}}"); st(f"#kc{i}", tw + .17, "{color: '#ffffff'}")
    sfx("g_pop", tw)
ft("#styles", T["pop"], .5, "{opacity: 0, y: 24}", "{opacity: 1, y: 0}", "expo.out")
for i in range(3):
    ft(f"#sty{i}", T["pop"] + .05 + i * .08, .4, "{opacity: 0, scale: .7}", "{opacity: 1, scale: 1}", "back.out(2)")
whip_out("J")

# ================= L: they scrub, you post
whip_in("L")
l0 = S["L"][0]
ft("#jl", l0 - .1, .6, "{opacity: 0, x: -90}", "{opacity: 1, x: 0}", "expo.out")
ft("#jr", l0 + .55, .6, "{opacity: 0, x: 90, scale: .92}", "{opacity: 1, x: 0, scale: 1}", "back.out(1.4)")
ft("#upl", l0 + .9, .35, "{opacity: 0, y: 10}", "{opacity: 1, y: 0}", "expo.out")
ft("#uplbar", l0 + .95, max(.5, T["up"] - l0 - 1.0), "{scaleX: .2}", "{scaleX: 1}", "power1.inOut")
to("#upl", T["up"] - .08, .15, "{opacity: 0, scale: .8}", "power2.in")
ft("#jr", T["your"] - .1, .5, "{scale: 1}", "{scale: 1.04}", "back.out(2)")
ft("#jl", T["your"] - .15, .5, "{filter: 'brightness(1)'}", "{filter: 'brightness(.55)'}", "power2.out")
ft("#posted", T["up"] - .05, .4, "{opacity: 0, scale: .4}", "{opacity: 1, scale: 1}", "back.out(2.4)")
flash(T["up"], .25); sfx("success", T["up"]); sfx("g_complete", T["up"] + .1)
for i in range(8):
    ft(f"#ht{i}", T["up"] + .05 + i * .09, 1.2, "{opacity: 1, y: 0, x: 0, scale: .5}",
       f"{{opacity: 0, y: -360, x: {(-1) ** i * (16 + i * 10)}, scale: 1.25}}", "power1.out")
ft("#live", T["up"] + .45, .45, "{opacity: 0, y: 22}", "{opacity: 1, y: 0}", "expo.out")
zoom_out("L")

# ================= M: CTA
zoom_in("M")
m0 = S["M"][0]
ft("#klogo2", m0 - .1, .7, "{opacity: 0, scale: .7, y: 20}", "{opacity: 1, scale: 1, y: 0}", "back.out(1.8)")
sfx("sparkle", m0)
ft("#cbox", T["kw"] - .35, .5, "{opacity: 0, y: 50, scale: .92}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.8)")
for i, ch in enumerate("KLAP"):
    ft(f"#ck{i}", T["kw"] - .08 + i * .075, .05, "{opacity: 0}", "{opacity: 1}", "none")
    sfx("click", T["kw"] - .08 + i * .075)
st("#caret", T["cta"], "{opacity: 1}")
for i in range(9):
    st("#caret", T["cta"] + .3 + i * .5, "{opacity: 0}"); st("#caret", T["cta"] + .55 + i * .5, "{opacity: 1}")
ft("#cpost", T["kw"] + .3, .3, "{color: '#8a8f9c', scale: 1}", f"{{color: '{VIOLET}', scale: 1.08}}", "back.out(2)")
sfx("pop", T["kw"] + .35)
ft("#bio", T["bio"] - .25, .45, "{opacity: 0, y: 26}", "{opacity: 1, y: 0}", "expo.out")
sfx("ding", T["bio"])
ft("#free", T["bio"] + .5, .5, "{opacity: 0}", "{opacity: 1}", "none")
ft("#brand", T["paste"] - .1, .5, "{opacity: 0, y: -10}", "{opacity: .85, y: 0}", "expo.out")
to("#brand", m0, .3, "{opacity: 0}")

# ---- counters (pure functions of time)
CNT = {"pay0": T["paid"] - .1, "pay1": T["paid"] + 1.1, "vw0": T["thousand"], "vw1": T["thousand"] + .9, "tl0": e0 - .1, "tl1": T["chase"] - .1,
       "sc0": T["scores"], "l0": l0, "l1": S["L"][1], "up": T["up"], "end": DUR}

COUNTERS = """
const C = %s;
const clamp = (x) => Math.max(0, Math.min(1, x));
const eio = (x) => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const eo = (x) => 1 - Math.pow(1 - x, 3);
const fmt = (n) => Math.round(n).toLocaleString("en-US");
const hms = (s) => { s = Math.max(0, Math.floor(s)); const h = Math.floor(s / 3600), m = Math.floor(s / 60) %% 60, x = s %% 60; return h + ":" + String(m).padStart(2, "0") + ":" + String(x).padStart(2, "0"); };
const $ = (id) => document.getElementById(id);
function counters(t) {
  const p = eio(clamp((t - C.pay0) / (C.pay1 - C.pay0)));
  $("earnN").textContent = "$" + (p * 1566.7).toFixed(2).replace(/\\B(?=(\\d{3})+(?!\\d))/g, ",");
  const v = eo(clamp((t - C.vw0) / (C.vw1 - C.vw0)));
  $("vwN").textContent = fmt(v * 1000) + " views";
  const q = clamp((t - C.tl0) / (C.tl1 - C.tl0)), pos = 1 - Math.pow(1 - q, 2.2);
  $("tcode").textContent = hms(pos * 6534);
  $("scrubf").style.transform = "scaleX(" + (pos * .605) + ")";
  $("scrubh").style.transform = "translateX(" + (pos * .605 * 960) + "px)";
  for (const [i, s] of [[0, 94], [1, 99], [2, 87]]) { const r = eo(clamp((t - C.sc0 - i * .14) / .9)); $("vs" + i).textContent = Math.round(r * s); }
  const jit = Math.sin(t * 7.1) * 18 + Math.sin(t * 13.7) * 7;
  $("jtc").textContent = hms(8088 + Math.floor((t - C.l0) * .6) + Math.round(jit));
  $("jhead").style.transform = "translateX(" + (168 + jit * 1.6) + "px)";
  $("jspin").style.transform = "rotate(" + (t * 400) + "deg)";
  const rp = clamp((t - C.l0) / (C.l1 - C.l0)); $("jren").style.transform = "scaleX(" + (.31 + rp * .08) + ")"; $("jrenN").textContent = Math.round(31 + rp * 8) + "%%";
  const u = eo(clamp((t - C.up) / 1.6)); const views = 12400 + u * 171600;
  $("pv").style.opacity = t >= C.up - .05 ? 1 : 0;
  $("pv").textContent = (views >= 1000 ? (views / 1000).toFixed(views < 100000 ? 1 : 0) + "K" : fmt(views)) + " views";
}
counters(0);
window.addEventListener("hf-seek", (e) => counters(e.detail.time));
tl.to({}, {duration: %.2f, onUpdate: () => counters(tl.time())}, 0);
""" % (json.dumps({k: round(v, 3) for k, v in CNT.items()}), DUR)

CSS = """
@font-face { font-family: Clash; font-weight: 600; src: url("assets/fonts/ClashDisplay-600.woff2"); }
@font-face { font-family: Clash; font-weight: 700; src: url("assets/fonts/ClashDisplay-700.woff2"); }
@font-face { font-family: Pop; font-weight: 500; src: url("assets/fonts/poppins-500.woff2"); }
@font-face { font-family: Pop; font-weight: 600; src: url("assets/fonts/poppins-600.woff2"); }
@font-face { font-family: Pop; font-weight: 700; src: url("assets/fonts/poppins-700.woff2"); }
@font-face { font-family: Pop; font-weight: 800; src: url("assets/fonts/poppins-800.woff2"); }
@font-face { font-family: Mono; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: $INK; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Pop; font-weight: 600; color: #fff; background: $INK; }
#bgglow { position: absolute; inset: 0; background: radial-gradient(60% 36% at 20% 12%, rgba(139,92,246,.28), rgba(0,0,0,0) 70%), radial-gradient(60% 36% at 85% 90%, rgba(109,61,240,.22), rgba(0,0,0,0) 70%); }
#shake { position: absolute; inset: 0; }
.scn { position: absolute; inset: 0; opacity: 0; transform-origin: 50% 50%; }
#sA { opacity: 1; transform-origin: 50% 48%; overflow: hidden; }
.fill { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.clipw { position: absolute; inset: 0; opacity: 0; } #aw0 { opacity: 1; }
.shadeT { position: absolute; left: 0; right: 0; top: 0; height: 820px; background: linear-gradient(rgba(2,6,23,.94), rgba(2,6,23,.6) 50%, rgba(2,6,23,0)); }
.shadeB { position: absolute; left: 0; right: 0; bottom: 0; height: 700px; background: linear-gradient(rgba(2,6,23,0), rgba(2,6,23,.82) 55%, rgba(2,6,23,.97)); }
#vig { position: absolute; inset: 0; pointer-events: none; background: radial-gradient(100% 64% at 50% 50%, rgba(0,0,0,0) 60%, rgba(2,6,23,.62) 100%); }
#grain { position: absolute; inset: 0; pointer-events: none; opacity: .06; background-image: url("assets/img/grain.png"); }
#flash { position: absolute; inset: 0; background: #fff; mix-blend-mode: overlay; opacity: 0; pointer-events: none; }
#brand { position: absolute; right: 60px; top: 262px; height: 36px; opacity: 0; }
/* headlines */
.hd { position: absolute; left: 40px; right: 40px; top: 300px; text-align: center; opacity: 0; font-family: Clash; font-weight: 700; font-size: 88px; line-height: 1.0; letter-spacing: -.02em; perspective: 900px; }
.hd.on { opacity: 1; }
.hd.big { top: 330px; font-size: 124px; letter-spacing: -.025em; }
.ln { display: flex; justify-content: center; gap: .22em; white-space: nowrap; margin: 6px 0; }
.w { display: inline-block; opacity: 0; transform-origin: 50% 100%; text-shadow: 0 8px 36px rgba(0,0,0,.75); }
.hd.on .w { opacity: 1; }
.pw { position: relative; padding: 0 .16em; margin: 0 -.02em; text-shadow: none; }
.pw i { position: absolute; inset: .04em 0 -.02em 0; background: $VIOLET; border-radius: 22px; transform: scaleX(0); transform-origin: 0 50%; box-shadow: 0 12px 40px rgba(139,92,246,.4); }
.pw b { position: relative; font-weight: 700; }
.cap { position: absolute; left: 60px; right: 60px; top: 1470px; text-align: center; font-family: Pop; font-weight: 700; font-size: 46px; opacity: 0;
  color: rgba(255,255,255,.4); text-shadow: 0 3px 16px rgba(0,0,0,.9); }
/* B: the wall */
#wallw { position: absolute; inset: 0; perspective: 1500px; overflow: hidden; }
#wall { position: absolute; left: 50%; top: 50%; width: 1200px; height: 2800px; margin: -1400px 0 0 -600px; display: flex; gap: 26px; justify-content: center;
  transform-style: preserve-3d; transform: rotateX(24deg) rotateZ(-10deg); }
.col { display: flex; flex-direction: column; gap: 26px; }
.tile { position: relative; width: 372px; height: 661px; border-radius: 30px; overflow: hidden; background: #111; box-shadow: 0 24px 60px rgba(0,0,0,.6), 0 0 0 2px rgba(255,255,255,.08); }
.tgrad { position: absolute; left: 0; right: 0; bottom: 0; height: 200px; background: linear-gradient(rgba(0,0,0,0), rgba(0,0,0,.7)); }
.tic { position: absolute; right: 14px; bottom: 90px; display: flex; flex-direction: column; gap: 16px; }
.tic svg { width: 34px; height: 34px; fill: #fff; filter: drop-shadow(0 2px 6px rgba(0,0,0,.6)); }
.tmeta { position: absolute; left: 16px; bottom: 18px; font-family: Pop; font-size: 18px; line-height: 1.3; } .tmeta b { display: block; font-weight: 700; } .tmeta span { color: rgba(255,255,255,.75); font-weight: 500; }
#bdim { position: absolute; inset: 0; opacity: 0; background: linear-gradient(rgba(2,6,23,.9), rgba(2,6,23,.55) 40%, rgba(2,6,23,.62) 60%, rgba(2,6,23,.96)); }
#bdim0 { position: absolute; inset: 0; background: linear-gradient(rgba(2,6,23,.86), rgba(2,6,23,.2) 36%, rgba(2,6,23,.25) 62%, rgba(2,6,23,.95)); }
#earn { position: absolute; left: 140px; right: 140px; top: 620px; height: 190px; border-radius: 36px; opacity: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px;
  background: rgba(10,14,32,.72); border: 2px solid rgba(255,255,255,.12); box-shadow: 0 30px 80px rgba(0,0,0,.6); backdrop-filter: blur(14px); }
#earn .k { font-family: Mono; font-size: 22px; letter-spacing: .18em; color: rgba(255,255,255,.6); }
#earnN { font-family: Clash; font-weight: 700; font-size: 104px; line-height: 1; color: $GREEN; text-shadow: 0 0 40px rgba(34,197,94,.45); font-variant-numeric: tabular-nums; }
.pay { position: absolute; left: 140px; right: 140px; height: 132px; border-radius: 30px; opacity: 0; display: flex; align-items: center; gap: 22px; padding: 0 30px;
  background: rgba(255,255,255,.96); color: $INK; box-shadow: 0 26px 60px rgba(0,0,0,.55); }
#pay0 { top: 850px; } #pay1 { top: 1004px; } #pay2 { top: 1158px; }
.pay .ok { width: 62px; height: 62px; border-radius: 50%; background: $GREEN; display: grid; place-items: center; flex: none; }
.pay .ok svg { width: 32px; height: 32px; }
.pay .tt { flex: 1; font-size: 28px; font-weight: 700; line-height: 1.2; } .pay .tt span { display: block; font-size: 20px; font-weight: 500; color: #64748b; }
.pay .amt { font-family: Clash; font-weight: 700; font-size: 54px; letter-spacing: -.01em; }
/* D: campaigns */
#dbgv { transform: scale(1.15); }
#cards { position: absolute; left: 90px; right: 90px; top: 610px; perspective: 1400px; display: flex; flex-direction: column; gap: 26px; }
.card { position: relative; height: 150px; border-radius: 34px; display: flex; align-items: center; gap: 28px; padding: 0 34px; opacity: 0;
  background: linear-gradient(135deg, rgba(255,255,255,.14), rgba(255,255,255,.05)); border: 2px solid rgba(255,255,255,.2); box-shadow: 0 30px 70px rgba(0,0,0,.5); backdrop-filter: blur(16px); }
.mono { width: 96px; height: 96px; border-radius: 28px; flex: none; display: grid; place-items: center; font-family: Clash; font-weight: 700; font-size: 44px; color: $INK; background: linear-gradient(135deg, #ff5fa2, #ffa24c); }
#cardB .mono { background: linear-gradient(135deg, #47e5ff, $VIOLET); }
.card .kk { font-family: Mono; font-size: 20px; letter-spacing: .16em; color: rgba(255,255,255,.6); }
.card .nm { font-family: Clash; font-weight: 700; font-size: 54px; letter-spacing: -.01em; line-height: 1.05; }
.card .chip { margin-left: auto; font-size: 24px; font-weight: 700; padding: 10px 18px; border-radius: 999px; color: #0f2d1a; background: $GREEN; opacity: 0; white-space: nowrap; }
#rate { position: absolute; left: 0; right: 0; top: 980px; text-align: center; opacity: 0; }
#rate b { font-family: Clash; font-weight: 700; font-size: 250px; line-height: .9; letter-spacing: -.02em; text-shadow: 0 0 70px rgba(139,92,246,.35); }
#rate .per { display: inline-block; font-family: Clash; font-weight: 700; font-size: 86px; color: $VIOLET; margin-left: 18px; opacity: 0; vertical-align: baseline; }
#vbar { position: absolute; left: 190px; right: 190px; top: 1290px; height: 20px; border-radius: 10px; background: rgba(255,255,255,.14); opacity: 0; }
#vfill { position: absolute; inset: 0; border-radius: 10px; background: linear-gradient(90deg, $VIOLET2, $VIOLET); transform-origin: 0 50%; transform: scaleX(0); }
#vwN { position: absolute; left: 190px; top: 1326px; font-family: Mono; font-size: 24px; color: rgba(255,255,255,.75); letter-spacing: .06em; opacity: 0; }
#veq { position: absolute; right: 190px; top: 1318px; font-size: 26px; font-weight: 700; padding: 6px 16px; border-radius: 999px; background: $GREEN; color: #0f2d1a; opacity: 0; }
/* E: filmstrip */
#tcode { position: absolute; left: 0; right: 0; top: 612px; text-align: center; font-family: Clash; font-weight: 700; font-size: 96px; line-height: 1; letter-spacing: .01em; font-variant-numeric: tabular-nums; }
#stripw { position: absolute; left: 0; right: 0; top: 760px; height: 420px; perspective: 1500px; overflow: visible; }
#strip { position: absolute; left: 540px; top: 90px; height: 203px; display: flex; gap: 16px; transform-origin: 50% 50%; }
.fr { position: relative; width: 360px; height: 203px; border-radius: 16px; overflow: hidden; flex: none; filter: grayscale(1) brightness(.55); background: #111; box-shadow: 0 18px 40px rgba(0,0,0,.6), 0 0 0 2px rgba(255,255,255,.1); }
.fr img, .fr video { width: 100%; height: 100%; object-fit: cover; display: block; }
#fr11 { transform-origin: 50% 50%; }
#spike { position: absolute; left: 50%; width: 10px; height: 60px; margin-left: -5px; border-radius: 5px; background: $RED; box-shadow: 0 0 24px $RED; transform-origin: 50% 0; opacity: 0; }
#pin { position: absolute; left: 50%; top: 1178px; transform: translateX(-50%); white-space: nowrap; opacity: 0; font-size: 28px; font-weight: 700; padding: 10px 22px; border-radius: 14px; background: $RED; box-shadow: 0 10px 30px rgba(255,59,92,.5); }
#scrub { position: absolute; left: 60px; width: 960px; top: 1256px; height: 14px; border-radius: 7px; background: rgba(255,255,255,.14); }
#scrubf { position: absolute; inset: 0; border-radius: 7px; background: linear-gradient(90deg, $VIOLET2, $VIOLET); transform-origin: 0 50%; transform: scaleX(0); }
#scrubh { position: absolute; left: -16px; top: -9px; width: 32px; height: 32px; border-radius: 50%; background: #fff; box-shadow: 0 0 0 6px rgba(255,255,255,.18); }
.tl0, #tl3 { position: absolute; top: 1290px; font-family: Mono; font-size: 26px; color: rgba(255,255,255,.7); } .tl0 { left: 60px; } #tl3 { right: 60px; transform-origin: 100% 50%; }
#scan { position: absolute; left: 50%; top: 620px; width: 12px; height: 720px; margin-left: -6px; opacity: 0; background: linear-gradient(rgba(139,92,246,0), $VIOLET 30%, #fff 50%, $VIOLET 70%, rgba(139,92,246,0)); box-shadow: 0 0 40px $VIOLET; }
#selsvg { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; pointer-events: none; }
#selbox { fill: none; stroke: $VIOLET; stroke-width: 6; stroke-dasharray: 2600; stroke-dashoffset: 2600; opacity: 0; filter: drop-shadow(0 0 16px rgba(139,92,246,.8)); }
#foundTag { position: absolute; left: 50%; top: 1178px; transform: translateX(-50%); opacity: 0; white-space: nowrap; font-size: 26px; font-weight: 700; padding: 10px 22px; border-radius: 999px; background: $VIOLET; }
/* G: reveal */
#kglow { position: absolute; left: 50%; top: 50%; width: 900px; height: 900px; margin: -450px 0 0 -450px; border-radius: 50%; opacity: 0; background: radial-gradient(circle, rgba(139,92,246,.5), rgba(139,92,246,0) 65%); }
.kring { position: absolute; left: 50%; top: 925px; width: 500px; height: 500px; margin: -250px 0 0 -250px; border-radius: 50%; border: 8px solid #fff; opacity: 0; }
#klogo { position: absolute; left: 50%; top: 925px; width: 760px; height: 300px; margin: -150px 0 0 -380px; perspective: 900px; }
#kicon { position: absolute; left: 0; top: 0; height: 300px; opacity: 0; filter: drop-shadow(0 0 40px rgba(255,255,255,.3)); }
.kl { position: absolute; left: 330px; top: 46px; width: 430px; height: 198px; opacity: 0; transform-origin: 50% 100%; }
#ktag { position: absolute; left: 0; right: 0; top: 1130px; text-align: center; font-family: Pop; font-weight: 500; font-size: 44px; color: rgba(255,255,255,.8); opacity: 0; letter-spacing: -.01em; }
.pt { position: absolute; left: 536px; top: 921px; width: 10px; height: 10px; border-radius: 50%; background: #fff; opacity: 0; }
.pt:nth-child(3n) { background: $VIOLET; width: 14px; height: 14px; }
/* H: the app */
.app { position: absolute; left: 50px; right: 50px; top: 600px; border-radius: 44px; background: #fff; color: $INK; font-family: Pop; font-weight: 500; box-shadow: 0 50px 110px rgba(0,0,0,.65); padding: 36px 46px 46px; transform-origin: 50% 0; }
.nav { display: flex; align-items: center; gap: 26px; font-size: 25px; color: #475569; } .nav img { height: 48px; } .nav .sp { flex: 1; }
.app h3 { font-family: Pop; font-weight: 700; font-size: 62px; margin: 36px 0 24px; letter-spacing: -.01em; }
.inp { position: relative; height: 122px; border-radius: 30px; border: 2px solid #e2e8f0; display: flex; align-items: center; padding: 0 16px 0 30px; box-shadow: 0 16px 44px rgba(15,23,42,.08); font-size: 29px; color: #94a3b8; }
.inp .ico { width: 40px; height: 40px; flex: none; margin-right: 22px; }
#ph, #url { position: absolute; left: 92px; top: 50%; transform: translateY(-50%); white-space: nowrap; } #url { color: $INK; font-weight: 600; } #url span { opacity: 0; }
#gen { position: relative; margin-left: auto; height: 88px; padding: 0 30px; border-radius: 22px; background: $INK; color: #fff; display: flex; align-items: center; gap: 12px; font-size: 30px; font-weight: 600; overflow: visible; }
#ripple { position: absolute; left: 50%; top: 50%; width: 160px; height: 160px; margin: -80px 0 0 -80px; border-radius: 50%; border: 4px solid $VIOLET; opacity: 0; }
#kv { position: absolute; right: 250px; top: -70px; font-family: Pop; font-weight: 700; font-size: 26px; padding: 8px 16px; border-radius: 12px; background: $INK; color: #fff; opacity: 0; }
#cursor { position: absolute; right: 86px; top: 72px; width: 58px; filter: drop-shadow(0 4px 8px rgba(0,0,0,.4)); opacity: 0; }
.tmpl { display: flex; gap: 18px; margin-top: 30px; }
.tmpl div { flex: 1; height: 96px; border-radius: 18px; background: linear-gradient(135deg, #1e293b, #312e81); display: flex; align-items: center; justify-content: center; gap: 8px; font-family: Pop; font-weight: 800; font-size: 22px; color: #fff; white-space: nowrap; }
.tmpl div.sel { box-shadow: 0 0 0 4px $VIOLET; } .tmpl b { color: #fde047; }
#prog { margin-top: 30px; opacity: 0; } #prog .t { font-size: 27px; color: #475569; margin-bottom: 14px; display: flex; justify-content: space-between; }
#prog .bar { position: relative; height: 16px; border-radius: 8px; background: #eef2f7; overflow: hidden; }
#progbar { height: 100%; background: linear-gradient(90deg, $VIOLET2, $VIOLET); transform-origin: 0 50%; }
#shim { position: absolute; top: 0; bottom: 0; width: 240px; background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.55), rgba(255,255,255,0)); }
/* I: moments */
#moments { position: absolute; left: 0; right: 0; top: 640px; height: 640px; perspective: 1600px; }
.mc { position: absolute; left: 50%; top: 40px; width: 300px; height: 533px; margin-left: -150px; border-radius: 30px; opacity: 0; transform-style: preserve-3d; }
.mc .in { position: absolute; inset: 0; border-radius: 30px; overflow: hidden; box-shadow: 0 30px 70px rgba(0,0,0,.6), 0 0 0 3px rgba(255,255,255,.12); }
#mc0 { margin-left: -480px; } #mc2 { margin-left: 180px; } #mc1 { top: -14px; width: 330px; height: 587px; margin-left: -165px; z-index: 2; }
.mc .glow { position: absolute; inset: -8px; border-radius: 38px; border: 5px solid $VIOLET; box-shadow: 0 0 50px rgba(139,92,246,.8); opacity: 0; }
.vb { position: absolute; left: 16px; top: 16px; display: flex; align-items: center; gap: 10px; padding: 8px 18px 8px 10px; border-radius: 999px; background: rgba(255,255,255,.96); color: $INK; opacity: 0; box-shadow: 0 8px 24px rgba(0,0,0,.4); }
.vb svg { width: 60px; height: 60px; transform: rotate(-90deg); } .vb circle { fill: none; stroke-width: 7; } .vb .bg { stroke: #e2e8f0; } .vb .fg { stroke: $VIOLET; stroke-linecap: round; stroke-dasharray: 251.3; stroke-dashoffset: 251.3; }
.vb b { font-family: Clash; font-weight: 700; font-size: 38px; line-height: 1; } .vb small { font-size: 18px; color: #64748b; font-weight: 600; }
#top { position: absolute; left: 50%; top: -74px; transform: translateX(-50%); opacity: 0; font-size: 24px; font-weight: 800; letter-spacing: .1em; padding: 8px 18px; border-radius: 999px; background: $VIOLET; }
.rk { position: absolute; left: 0; right: 0; bottom: -58px; text-align: center; font-family: Mono; font-size: 28px; color: rgba(255,255,255,.75); }
#rankpill { position: absolute; left: 0; right: 0; top: 1330px; text-align: center; opacity: 0; }
#rankpill span { font-size: 30px; font-weight: 700; padding: 12px 26px; border-radius: 999px; background: rgba(139,92,246,.16); border: 2px solid $VIOLET; color: #e9d5ff; }
/* J: reframe + captions */
#land { position: absolute; left: 60px; width: 960px; top: 715px; height: 540px; border-radius: 30px; overflow: visible; transform-origin: 50% 50%; }
#land .in { position: absolute; inset: 0; border-radius: 30px; overflow: hidden; box-shadow: 0 40px 90px rgba(0,0,0,.6), 0 0 0 3px rgba(255,255,255,.1); }
#fc1 { position: absolute; right: 24px; bottom: 24px; width: 300px; height: 188px; border-radius: 18px; overflow: hidden; box-shadow: 0 0 0 4px #fff; transform-origin: 100% 100%; }
#trksvg { position: absolute; left: -20px; top: -20px; width: 1000px; height: 580px; pointer-events: none; }
#trk { fill: none; stroke: $VIOLET; stroke-width: 5; stroke-dasharray: 1000; stroke-dashoffset: 1000; opacity: 0; }
#trkl { position: absolute; right: 24px; top: 300px; opacity: 0; font-family: Mono; font-size: 22px; letter-spacing: .12em; color: #fff; padding: 6px 12px; border-radius: 8px; background: $VIOLET; }
#phone { position: absolute; left: 315px; top: 600px; width: 450px; height: 800px; border-radius: 44px; overflow: hidden; opacity: 0; background: #000; box-shadow: 0 40px 100px rgba(0,0,0,.7), 0 0 0 10px #0f172a, 0 0 0 12px rgba(255,255,255,.16); }
#fc2 { position: absolute; left: 0; top: 0; width: 450px; height: 285px; overflow: hidden; opacity: 0; }
#game2 { position: absolute; left: 0; top: 285px; width: 450px; height: 515px; overflow: hidden; }
#lyt { position: absolute; left: 50%; top: 262px; transform: translateX(-50%); opacity: 0; white-space: nowrap; font-family: Mono; font-size: 20px; letter-spacing: .14em; padding: 8px 16px; border-radius: 999px; background: $VIOLET; }
.lbl2 { position: absolute; font-size: 24px; font-weight: 700; padding: 6px 14px; border-radius: 10px; opacity: 0; white-space: nowrap; }
#ls { left: 16px; top: 16px; background: #fff; color: $INK; } #lg { left: 16px; bottom: 16px; background: #fff; color: $INK; }
#kcap { position: absolute; left: 10px; right: 10px; top: 470px; text-align: center; font-family: Pop; font-weight: 800; font-size: 50px; line-height: 1.1; -webkit-text-stroke: 3px #000; paint-order: stroke fill; text-shadow: 0 6px 0 #000; }
#kcap span { display: inline-block; opacity: 0; margin: 0 7px; }
#styles { position: absolute; left: 0; right: 0; top: 1330px; display: flex; justify-content: center; gap: 14px; opacity: 0; }
#styles div { padding: 10px 18px; border-radius: 12px; background: rgba(255,255,255,.1); border: 2px solid rgba(255,255,255,.18); font-family: Pop; font-weight: 800; font-size: 20px; white-space: nowrap; opacity: 0; } #styles b { color: #fde047; }
/* L: split */
.half { position: absolute; top: 610px; width: 470px; height: 780px; border-radius: 36px; overflow: hidden; opacity: 0; }
#jl { left: 50px; background: rgba(255,255,255,.05); border: 2px solid rgba(255,255,255,.12); }
#jr { left: 560px; background: linear-gradient(160deg, rgba(139,92,246,.3), rgba(109,61,240,.1)); border: 2px solid rgba(139,92,246,.55); }
.half .lab { position: absolute; left: 0; right: 0; top: 28px; text-align: center; font-family: Mono; font-size: 24px; letter-spacing: .16em; color: rgba(255,255,255,.7); }
#jmon { position: absolute; left: 30px; right: 30px; top: 86px; height: 230px; border-radius: 20px; overflow: hidden; filter: grayscale(1) brightness(.55); }
#jtl { position: absolute; left: 30px; right: 30px; top: 340px; height: 56px; border-radius: 10px; background: rgba(255,255,255,.07); overflow: hidden; display: flex; gap: 4px; padding: 8px; }
#jtl i { display: block; height: 40px; border-radius: 6px; background: rgba(255,255,255,.18); flex: none; }
#jhead { position: absolute; left: 30px; top: 330px; width: 4px; height: 76px; background: #fff; box-shadow: 0 0 10px #fff; }
#jtc { position: absolute; left: 0; right: 0; top: 424px; text-align: center; font-family: Clash; font-weight: 700; font-size: 72px; color: rgba(255,255,255,.55); font-variant-numeric: tabular-nums; }
#jrenw { position: absolute; left: 40px; right: 40px; top: 540px; }
#jrenw .t { display: flex; justify-content: space-between; font-size: 22px; color: rgba(255,255,255,.6); margin-bottom: 10px; }
#jrenb { height: 12px; border-radius: 6px; background: rgba(255,255,255,.1); overflow: hidden; } #jren { height: 100%; background: #94a3b8; transform-origin: 0 50%; }
#jspin { position: absolute; left: 50%; top: 640px; width: 66px; height: 66px; margin-left: -33px; border-radius: 50%; border: 8px solid rgba(255,255,255,.12); border-top-color: rgba(255,255,255,.6); }
#jphone { position: absolute; left: 50%; top: 86px; width: 290px; height: 516px; margin-left: -145px; border-radius: 34px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,.6), 0 0 0 6px #0f172a; }
#upl { position: absolute; left: 60px; right: 60px; top: 626px; opacity: 0; font-size: 24px; color: rgba(255,255,255,.75); text-align: center; }
#upl .b { height: 10px; border-radius: 5px; background: rgba(255,255,255,.12); margin-top: 10px; overflow: hidden; } #uplbar { height: 100%; background: $VIOLET; transform-origin: 0 50%; }
#posted { position: absolute; left: 50%; top: 622px; transform: translateX(-50%); display: flex; align-items: center; gap: 10px; white-space: nowrap; opacity: 0; font-size: 30px; font-weight: 700; padding: 10px 22px; border-radius: 999px; background: $GREEN; color: #04210f; box-shadow: 0 10px 30px rgba(34,197,94,.5); }
#pv { position: absolute; left: 0; right: 0; top: 690px; text-align: center; font-family: Clash; font-weight: 700; font-size: 44px; color: #fff; font-variant-numeric: tabular-nums; }
.ht { position: absolute; left: 336px; top: 560px; width: 44px; height: 44px; opacity: 0; fill: #ff4d79; }
#live { position: absolute; left: 0; right: 0; top: 1412px; text-align: center; opacity: 0; }
#live span { font-size: 26px; font-weight: 600; padding: 10px 22px; border-radius: 999px; background: rgba(139,92,246,.14); border: 2px solid $VIOLET; color: #e9d5ff; }
/* M: CTA */
#kbgv, #kbgv2 { transform: scale(1.1); }
#klogo2 { position: absolute; left: 50%; top: 690px; width: 620px; margin-left: -310px; opacity: 0; filter: drop-shadow(0 0 40px rgba(255,255,255,.22)); }
#cbox { position: absolute; left: 110px; right: 110px; top: 1010px; height: 132px; border-radius: 66px; opacity: 0; display: flex; align-items: center; gap: 24px; padding: 0 38px 0 26px; background: rgba(250,250,252,.98); color: $INK; box-shadow: 0 30px 80px rgba(0,0,0,.6), 0 0 0 3px rgba(139,92,246,.85); }
#cbox .av { width: 80px; height: 80px; border-radius: 50%; background: conic-gradient($VIOLET, #ff5fa2, #ffa24c, #47e5ff, $VIOLET); flex: none; }
#cbox .tx { flex: 1; font-family: Clash; font-weight: 700; font-size: 58px; letter-spacing: .04em; display: flex; align-items: center; } #cbox .tx span { opacity: 0; }
#caret { display: inline-block; width: 4px; height: 58px; background: $INK; margin-left: 6px; opacity: 0; }
#cpost { font-size: 34px; font-weight: 700; color: #8a8f9c; }
#bio { position: absolute; left: 0; right: 0; top: 1196px; text-align: center; opacity: 0; }
#bio span { font-size: 32px; font-weight: 600; padding: 12px 28px; border-radius: 999px; background: rgba(255,255,255,.1); border: 2px solid rgba(255,255,255,.4); }
#free { position: absolute; left: 0; right: 0; top: 1300px; text-align: center; opacity: 0; font-size: 26px; color: rgba(255,255,255,.6); }
"""
for a, b in (("$INK", INK), ("$VIOLET2", VIOLET2), ("$VIOLET", VIOLET), ("$GREEN", GREEN), ("$RED", RED)):
    CSS = CSS.replace(a, b)

UP = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 15V4"/><path d="M7 9l5-5 5 5"/><path d="M4 15v4a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-4"/></svg>'
SPARK = '<svg width="30" height="30" viewBox="0 0 24 24" fill="#fff"><path d="M12 2l1.8 5.6L19 9.5l-5.2 1.9L12 17l-1.8-5.6L5 9.5l5.2-1.9z"/><path d="M19 14l.9 2.6 2.6.9-2.6.9L19 21l-.9-2.6-2.6-.9 2.6-.9z"/></svg>'
CURSOR = '<svg id="cursor" viewBox="0 0 24 24"><path d="M4 2l15 9-6.5 1.6L9.5 19z" fill="#020617" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="#04210f" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5 5L20 6.5"/></svg>'
HEART = '<svg class="ht" id="ht{i}" viewBox="0 0 24 24"><path d="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 3 4.5 6.8 4.5c2.1 0 3.5 1.1 5.2 3 1.7-1.9 3.1-3 5.2-3 3.8 0 5.9 3.9 4.4 7.3C19.5 16.4 12 21 12 21z"/></svg>'
d0, d1 = S["D"]
i0, i1 = S["I"]
jj0, jj1 = S["J"]
mm0 = S["M"][0]
strip_html = "".join(
    f'<div class="fr" id="fr{i}">' + (vid("chasev", "stream_chase_l", T["chase"] - .3, e1 + .2, .2, "") if i == CH else f'<img src="assets/img/strip/f{i:02d}.jpg" alt="">') + "</div>"
    for i in range(N_FR))
SC = f"""
  <div class="scn" id="sA">{''.join(A_HTML)}<div class="shadeT"></div><div class="shadeB"></div></div>
  <div class="scn" id="sB"><div id="wallw" data-layout-allow-overflow data-layout-allow-overlap><div id="wall">{''.join(B_COLS)}</div></div><div id="bdim0"></div><div id="bdim"></div>
    <div id="earn"><div class="k">PAYOUTS</div><div id="earnN">$0.00</div></div>
    {''.join(f'<div class="pay" id="pay{i}"><div class="ok">{CHECK}</div><div class="tt">Payout approved<span>Clipping campaign · {v} views</span></div><div class="amt">${a}</div></div>' for i, (v, a) in enumerate((("134,200", "134.20"), ("412,500", "412.50"), ("1,020,000", "1,020.00"))))}
  </div>
  <div class="scn" id="sD">{vid("dbgv", "r_sky_blur", d0 - .2, d1 + .3, .5, "fill")}
    <div id="cards">
      <div class="card" id="cardA"><div class="mono">MB</div><div><div class="kk">CLIPPING CAMPAIGN</div><div class="nm">MrBeast</div></div><div class="chip">~$1 / 1K views</div></div>
      <div class="card" id="cardB"><div class="mono">IS</div><div><div class="kk">CLIPPING CAMPAIGN</div><div class="nm">IShowSpeed</div></div><div class="chip">~$1 / 1K views</div></div>
    </div>
    <div id="rate"><b>$1</b><span class="per">/ 1K views</span></div>
    <div id="vbar"><div id="vfill"></div></div><div id="vwN">0 views</div><div id="veq">= $1.00</div></div>
  <div class="scn" id="sE">
    <div id="tcode">0:00:00</div>
    <div id="stripw" data-layout-allow-overflow><div id="strip" data-layout-allow-overflow>{strip_html}</div></div>
    <div id="scrub"><div id="scrubf"></div><div id="scrubh"></div></div><div class="tl0">0:00:00</div><div id="tl3">3:00:00</div>
    <div id="spike" style="top: 1236px"></div><div id="pin">1 crazy chase</div>
    <svg id="selsvg"><rect id="selbox" x="268" y="794" width="544" height="312" rx="22" ry="22"/></svg>
    <div id="foundTag">Moment found · 0:14</div><div id="scan"></div></div>
  <div class="scn" id="sG"><div id="kglow"></div><div class="kring" id="kring0"></div><div class="kring" id="kring1"></div>
    {''.join(f'<div class="pt" id="pt{i}"></div>' for i in range(24))}
    <div id="klogo"><img id="kicon" src="assets/img/klap_icon_white.svg" alt="">{''.join(f'<img class="kl" id="kl_{L}" src="assets/img/kl_{L}.svg" alt="">' for L in "Klap")}</div>
    <div id="ktag">Turn videos into viral shorts</div></div>
  <div class="scn" id="sH"><div class="app">
    <div class="nav"><img src="assets/img/klap_logo_ink.svg" alt=""><span class="sp"></span><span>Videos</span><span>Calendar</span><span>Analytics</span></div>
    <h3>Videos</h3>
    <div class="inp">{UP}<span id="ph">Drop a file or paste a link</span><span id="url">{''.join(f'<span id="u{i}">{c}</span>' for i, c in enumerate(URL))}</span>
      <div id="gen"><div id="ripple"></div>{SPARK}Generate</div><div id="kv">Ctrl + V</div>{CURSOR}</div>
    <div class="tmpl"><div class="sel">NO WAY <b>HE</b> DID</div><div>NO <b>WAY</b> HE DID</div><div>No way he did</div></div>
    <div id="prog"><div class="t"><span>Finding the best moments</span><span>virality score</span></div><div class="bar"><div id="progbar"></div><div id="shim"></div></div></div></div></div>
  <div class="scn" id="sI"><div id="moments">
    {''.join(f'<div class="mc" id="mc{i}"><div class="glow"></div><div class="in">{vid(f"hv{i}", s, i0 - .2, i1 + .3, m)}</div><div class="vb" id="vb{i}"><svg viewBox="0 0 90 90"><circle class="bg" cx="45" cy="45" r="40"/><circle class="fg" id="ring{i}" cx="45" cy="45" r="40"/></svg><div><b id="vs{i}">0</b><small>/100</small></div></div><div class="rk">#{r}</div></div>' for i, (s, m, r) in enumerate((("t_cops", .3, 2), ("t_flip", .75, 1), ("t_heli", .6, 3))))}
    <div id="top">TOP PICK</div></div><div id="rankpill"><span>Ranked by virality score</span></div></div>
  <div class="scn" id="sJ">
    <div id="land"><div class="in">{vid("iv0", "stream_cops_l", jj0 - .2, T["vertical"] + .7, .3)}</div><div id="fc1">{vid("iv1", "facecam", jj0 - .2, T["vertical"] + .7, .0)}</div>
      <svg id="trksvg"><rect id="trk" x="656" y="348" width="316" height="204" rx="20"/></svg><div id="trkl">ACTIVE SPEAKER</div></div>
    <div id="phone"><div id="game2">{vid("iv2", "game_l", T["vertical"] - .2, jj1 + .3, .0)}</div><div id="fc2">{vid("iv4", "facecam", T["vertical"] - .2, jj1 + .3, 1.0)}</div>
      <div id="lyt">GAMING LAYOUT</div><div class="lbl2" id="ls">streamer</div><div class="lbl2" id="lg">gameplay</div>
      <div id="kcap">{''.join(f'<span id="kc{i}">{w}</span>' for i, w in enumerate(CAPW))}</div></div>
    <div id="styles"><div id="sty0">NO WAY <b>HE</b></div><div id="sty1"><b>NO</b> WAY HE</div><div id="sty2">No way he</div></div></div>
  <div class="scn" id="sL">
    <div class="half" id="jl"><div class="lab">OTHER CLIPPERS</div><div id="jmon">{vid("jv0", "stream", l0 - .2, S["L"][1] + .3, 2.0)}</div>
      <div id="jtl">{''.join(f'<i style="width:{w}px"></i>' for w in (38, 62, 24, 80, 44, 30, 70, 26, 52, 40, 66, 28, 48, 36, 58, 44))}</div><div id="jhead"></div>
      <div id="jtc">2:14:48</div><div id="jrenw"><div class="t"><span>Rendering</span><span id="jrenN">31%</span></div><div id="jrenb"><div id="jren"></div></div></div><div id="jspin"></div></div>
    <div class="half" id="jr"><div class="lab">YOU</div><div id="jphone">{vid("jv1", "t_flip", l0 - .2, S["L"][1] + .3, .4)}</div>
      <div id="posted"><svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#04210f" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5 5L20 6.5"/></svg>Posted</div>
      <div id="upl"><span>Uploading</span><div class="b"><div id="uplbar"></div></div></div>
      <div id="pv">12.4K views</div>{''.join(HEART.format(i=i) for i in range(8))}</div>
    <div id="live"><span>Live streams too: first clips in about 15 minutes</span></div></div>
  <div class="scn" id="sM">{vid("kbgv", "c_boat_blur", mm0 - .2, min(DUR, mm0 + 2.7), .0, "fill")}{vid("kbgv2", "r_sky_blur2", min(DUR, mm0 + 2.7), DUR, 1.5, "fill")}
    <div class="shadeT"></div><div class="shadeB"></div>
    <img id="klogo2" src="assets/img/klap_logo_white.svg" alt="">
    <div id="cbox"><div class="av"></div><div class="tx">{"".join(f'<span id="ck{i}">{c}</span>' for i, c in enumerate("KLAP"))}<i id="caret"></i></div><b id="cpost">Post</b></div>
    <div id="bio"><span>or tap the link in bio</span></div><div id="free">Try Klap free on 1 video. No credit card required.</div></div>
"""

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Klap x GTA 6 clippers 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div id="bgglow"></div>
      <div id="shake" data-layout-allow-overflow>
      {SC}
      </div>
      <div id="grain" data-layout-allow-overlap></div>
      <img id="brand" src="assets/img/klap_logo_white_sm.svg" alt="">
      {chr(10).join(HTML)}
      <div id="flash"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      {chr(10).join("      " + j for j in JS).strip()}
      {COUNTERS}
      tl.set({{}}, {{}}, {DUR:.2f});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(html)
SFX.sort(key=lambda e: e["t"])
json.dump(SFX, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
json.dump({k: round(v, 3) for k, v in T.items()}, open(os.path.join(ROOT, "plan", "times.json"), "w"), indent=0)
json.dump({"dur": DUR, "scenes": {k: [round(a, 3), round(b, 3)] for k, (a, b) in S.items()}}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx, {TRK[0]} videos")
print({k: round(v, 2) for k, v in T.items()})
print({k: (round(a, 2), round(b, 2)) for k, (a, b) in S.items()})
