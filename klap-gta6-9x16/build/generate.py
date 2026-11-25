"""AI.NXTLVL x Klap brand reel, "GTA 6 clippers" (9:16): writes index.html, plan/sfx_events.json, plan/edit.json and
plan/music_plan.json (read by build/music.py).

Footage: Rockstar Games' official GTA 6 promo clips (owner's standing exception: footage only, muted), a Pexels facecam
(6878208, Pexels licence). Klap's screens are rebuilt in HTML with Klap's own wording (klap.app and klap.app/for/clippers,
checked 2026-11-25): "Drop a file or paste a link from any video URL", Generate, virality score, Gaming layout, animated
captions, live streams (first clips in about 15 minutes). MrBeast and IShowSpeed appear by name only (owner's call: no
faces in a paid ad). One paused GSAP timeline; counters are pure functions of time (hf-seek). Layout grid as the other
AI.NXTLVL reels: top bar 258, headline band 330, stage 590-1420, live caption 1470.
python3 build/generate.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = []
for w in json.load(open(os.path.join(ROOT, "plan", "words.json"))):
    if W and w["w"][:1] in ".,-" and W[-1]["line"] == w["line"]:
        W[-1]["w"] += w["w"]; W[-1]["t1"] = w["t1"]
    else:
        W.append(dict(w))
JS, SFX, HTML = [], [], []
NIGHT, PINK, ORANGE, CYAN, GOLD, INK = "#07060d", "#ff5fa2", "#ffa24c", "#47e5ff", "#ffc23d", "#0b0f1a"


def js(s):
    JS.append(s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(max(0, t), 3)})


def ft(sel, t, d, frm, to_, ease="power3.out"):
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


def vid(i, src, t0, t1, media=0.0, cls="fill", style=""):
    TRK[0] += 1
    return (f'<video id="{i}" class="{cls}" src="assets/video/{src}.mp4" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" '
            f'data-media-start="{media:.3f}" data-track-index="{TRK[0]}" muted playsinline style="{style}"></video>')


END = max(w["t1"] for w in W)
DUR = round(END + 1.5, 2)
T = {}
T["clips"] = wt("clips"); T["feed"] = wt("feed"); T["clippers"] = wt("clippers"); T["paid"] = wt("paid"); T["views1"] = wt("views")
T["beast"] = wt(["mrbeast", "mr"]); T["speed"] = wt(["ishowspeed", "ishow", "i"], after=T["beast"] + .2); T["dollar"] = wt("dollar")
T["thousand"] = wt("thousand"); T["hard"] = wt("hard"); T["moment"] = wt("moment"); T["three"] = wt(["three", "3"], after=T["hard"])
T["crazy"] = wt("crazy"); T["chase"] = wt("chase"); T["tool"] = wt("tool"); T["klap"] = wt(["klap", "clap"])
T["paste"] = wt("paste"); T["link"] = wt("link"); T["picks"] = wt("picks"); T["scores"] = wt("scores"); T["viral"] = wt("viral")
T["cuts"] = wt("cuts"); T["vertical"] = wt("vertical"); T["gameplay"] = wt("gameplay"); T["streamer"] = wt("streamer")
T["captions"] = wt("captions"); T["pop"] = wt("pop", after=T["captions"]); T["so"] = wt("so", after=T["pop"])
T["scrub"] = wt("scrubbing"); T["your"] = wt("your", after=T["scrub"]); T["up"] = wt("up", after=T["your"])
T["cta"] = wt("comment"); T["kw"] = wt(["klap", "clap"], after=T["cta"]); T["grab"] = wt("grab"); T["bio"] = wt("bio")
T["end"] = DUR

# ---- music plan: "Miami" by Lyvo. Full energy under the hook, its breakdown from "The hard part", the kick slams back
# (track 120.024 s) exactly on "Klap". Two segments on one continuous beat grid (offsets differ by whole beats).
BEATS = json.load(open(os.path.join(ROOT, "sfx", "music", "beats_miami.json")))
BI = BEATS["beat_interval_s"]
DROP = 120.024
o2 = DROP - T["klap"]
b_break = min(BEATS["beats_s"], key=lambda b: abs(b - 60.0))      # first beat of the breakdown
n = round((o2 - (b_break - T["hard"] + .05)) / BI)
o1 = o2 - n * BI
CUT = T["klap"] - 4 * BI
grid = [b - o1 for b in BEATS["beats_s"] if 0 <= b - o1 < CUT] + [b - o2 for b in BEATS["beats_s"] if CUT <= b - o2 < DUR]
json.dump({"track": "sfx/music/m3_miami.mp3", "o1": round(o1, 4), "o2": round(o2, 4), "cut": round(CUT, 4), "dur": DUR},
          open(os.path.join(ROOT, "plan", "music_plan.json"), "w"), indent=1)


def beat_after(t):
    return min((b for b in grid if b >= t - .01), default=t)


# ---- scenes
S = {}
S["A"] = (0, T["feed"] - .3)
S["B"] = (S["A"][1], T["beast"] - .3)
S["D"] = (S["B"][1], T["hard"] - .25)
S["E"] = (S["D"][1], T["klap"] - .1)
S["F"] = (S["E"][1], T["paste"] - .3)
S["G"] = (S["F"][1], T["picks"] - .25)
S["H"] = (S["G"][1], T["cuts"] - .25)
S["I"] = (S["H"][1], T["so"] - .25)
S["J"] = (S["I"][1], T["cta"] - .3)
S["K"] = (S["J"][1], DUR)
for k, (a, b) in S.items():
    if k != "A":
        st(f"#s{k}", a, "{opacity: 1}")
    if b < DUR:
        st(f"#s{k}", b + .2, "{opacity: 0}")


def whip_in(k, frm="{scale: 1.18, filter: 'blur(14px)', opacity: 0}", to_="{scale: 1, filter: 'blur(0px)', opacity: 1}"):
    a = S[k][0]
    ft(f"#s{k}", a, .32, frm, to_, "power3.out")
    sfx("whoosh", a - .08)


def whip_out(k):
    b = S[k][1]
    to(f"#s{k}", b - .02, .22, "{scale: .9, filter: 'blur(10px)', opacity: 0}", "power2.in")


# ---- headlines (two lines: white Montserrat + Vice City gradient serif)
HEADS = [("GTA 6 is out.", "Clips are everywhere.", 0.0),
         ("Clippers get paid", "for views.", T["clippers"] - .15),
         ("Big campaigns pay", "by the view.", T["beast"] - .2),
         ("The hard part:", "finding the moment.", T["hard"] - .1),
         ("3-hour stream.", "One crazy chase.", T["three"] - .1),
         ("This tool", "finds it for you.", T["tool"] - .1),
         (None, None, T["klap"] - .25),
         ("Paste the", "stream link.", T["paste"] - .15),
         ("It picks the moments", "and scores each one.", T["picks"] - .15),
         ("Cut vertical,", "streamer in frame.", T["cuts"] - .15),
         ("Plus captions", "that pop.", T["captions"] - .15),
         ("Still on hour two?", "Your clip is up.", T["so"] - .1),
         ("Comment", "KLAP.", T["cta"] - .1)]
for k, (a, b, t0) in enumerate(HEADS):
    t1 = HEADS[k + 1][2] if k + 1 < len(HEADS) else DUR + 1
    if a is None:
        continue
    HTML.append(f'<div class="hd{" on" if k == 0 else ""}" id="hd{k}"><div class="h1">{a}</div><div class="h2"><span>{b}</span></div></div>')
    if k:
        st(f"#hd{k}", t0, "{opacity: 1}")
        ft(f"#hd{k} .h1", t0, .34, "{opacity: 0, y: 30, scale: .96}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.9)")
        h2t = T["your"] - .1 if k == 11 else t0 + .12
        ft(f"#hd{k} .h2", h2t, .4, "{opacity: 0, y: 30, scale: .96}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.9)")
    if t1 < DUR:
        to(f"#hd{k}", t1 - .14, .14, "{opacity: 0, y: -22, filter: 'blur(6px)'}", "power2.in")
# frame 1 shows "GTA 6 is out."; the second line lands on "clips"
st("#hd0 .h2", 0, "{opacity: 0}")
ft("#hd0 .h2", T["clips"] - .05, .4, "{opacity: 0, y: 30, scale: .96}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.9)")
ft("#hd0 .h1", 0, .5, "{scale: 1.12}", "{scale: 1}", "power3.out")

# ---- live caption, three words at a time
k = 0
for i in range(0, len(W), 3):
    chunk = W[i:i + 3]
    nxt = W[i + 3]["t0"] if i + 3 < len(W) else chunk[-1]["t1"] + .25
    if nxt - chunk[-1]["t1"] > .6:
        nxt = chunk[-1]["t1"] + .35
    spans = " ".join(f'<span id="cw{k}_{j}">{w["w"]}</span>' for j, w in enumerate(chunk))
    HTML.append(f'<div class="cap" id="cp{k}">{spans}</div>')
    ft(f"#cp{k}", chunk[0]["t0"] - .06, .12, "{opacity: 0}", "{opacity: 1}", "none")
    for j, w in enumerate(chunk):
        ft(f"#cw{k}_{j}", w["t0"] - .04, .12, "{color: 'rgba(255,255,255,.45)'}", "{color: '#ffffff'}", "none")
    to(f"#cp{k}", nxt - .06, .06, "{opacity: 0}", "none")
    k += 1

# ================= scene A: the hook, full-bleed GTA 6 cuts on the beat
a0, a1 = S["A"]
SEQ = [("c_flip", .7), ("c_heli", .25), ("c_cops", .05), ("c_truck", .3), ("c_shoot", .0)]
BASE = {"c_heli": 1.3}   # crops the rating badge off the left edge
cuts = [0.0] + [b for b in grid if .5 < b < a1 - .3][1::2]
cuts = [c for c in cuts if c < a1 - .25]
A_HTML = []
for j, c in enumerate(cuts):
    c1 = cuts[j + 1] if j + 1 < len(cuts) else a1 + .35
    src, m = SEQ[j % len(SEQ)]
    A_HTML.append(f'<div class="clipw" id="aw{j}">{vid(f"av{j}", src, c, c1, m)}</div>')
    if j:
        st(f"#aw{j}", c, "{opacity: 1}")
        b = BASE.get(src, 1.0)
        ft(f"#aw{j}", c, .45, f"{{scale: {b + .14}}}", f"{{scale: {b}}}", "power3.out")
        js(f'tl.set("#flash", {{opacity: .35}}, {c - .01:.3f});'); to("#flash", c, .3, "{opacity: 0}", "power2.out")
        sfx("whoosh" if j % 2 else "swish", c - .06); sfx("thump", c)
    st(f"#aw{j}", c1 + .01, "{opacity: 0}") if j + 1 < len(cuts) else None
ft("#aw0", 0, .6, "{scale: 1.2}", "{scale: 1.0}", "power3.out")
# out: the full-bleed clip shrinks into the feed wall
to("#sA", a1 - .05, .42, "{scale: .3, borderRadius: '60px', opacity: 0}", "power3.in")
sfx("whoosh_big", a1 - .1)

# ================= scene B: every feed (3D wall of GTA clips) + clippers get paid
b0, b1 = S["B"]
TILES = ["t_cops", "t_flip", "t_heli", "t_boat", "t_scoot", "t_truck", "t_ball", "t_dive"]
B_COLS = []
for c in range(4):
    tiles = "".join(f'<div class="tile">{vid(f"tv{c}_{r}", TILES[(c * 3 + r) % len(TILES)], b0, b1 + .25 + (c * 4 + r) * .011, (c * 1.3 + r * .7) % 4)}'
                    f'<div class="tic"><i></i><i></i><i></i></div></div>' for r in range(4))
    B_COLS.append(f'<div class="col" id="col{c}">{tiles}</div>')
    ft(f"#col{c}", b0, b1 - b0 + .25, f"{{y: {-220 if c % 2 else -520}}}", f"{{y: {-520 if c % 2 else -220}}}", "none")
ft("#wall", b0, .6, "{scale: 2.2, opacity: 0}", "{scale: 1.0, opacity: 1}", "power3.out")
# payout HUD: views and earnings at ~$1 per 1,000 views
ft("#hud", T["clippers"] - .1, .45, "{opacity: 0, y: 60, scale: .9}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.7)")
sfx("pop", T["clippers"])
for i in range(7):
    sfx("cash" if i % 3 == 0 else "tick", T["paid"] + i * .22)
whip_out("B")

# ================= scene D: the campaigns (names only), ~$1 per 1,000 views
whip_in("D", "{opacity: 0, scale: 1.15, filter: 'blur(14px)'}", "{opacity: 1, scale: 1, filter: 'blur(0px)'}")
ft("#cardA", T["beast"] - .1, .5, "{opacity: 0, x: -260, rotationY: 35}", "{opacity: 1, x: 0, rotationY: 0}", "back.out(1.5)")
ft("#cardB", T["speed"] - .1, .5, "{opacity: 0, x: 260, rotationY: -35}", "{opacity: 1, x: 0, rotationY: 0}", "back.out(1.5)")
sfx("swish", T["beast"] - .1); sfx("swish", T["speed"] - .1)
ft("#rate", T["dollar"] - .05, .5, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}", "back.out(2.2)")
sfx("impact", T["dollar"]); sfx("cash", T["dollar"] + .1)
ft("#rate .per", T["thousand"] - .05, .35, "{opacity: 0, y: 20}", "{opacity: 1, y: 0}", "power3.out")
for c in ("#cardA .pill", "#cardB .pill"):
    ft(c, T["thousand"] + .1, .3, "{opacity: 0, scale: .7}", "{opacity: 1, scale: 1}", "back.out(2)")
whip_out("D")

# ================= scene E: a 3-hour stream, one crazy chase
whip_in("E", "{y: 120, opacity: 0, filter: 'blur(10px)'}", "{y: 0, opacity: 1, filter: 'blur(0px)'}")
ft("#tl3", T["three"] - .05, .4, "{scale: .6, color: '#ffffff'}", f"{{scale: 1, color: '{PINK}'}}", "back.out(2.5)")
sfx("stamp", T["three"])
ft("#seg", T["chase"] - .15, .3, "{opacity: 0, scaleX: .2}", "{opacity: 1, scaleX: 1}", "back.out(2)")
ft("#pin", T["chase"] - .1, .4, "{opacity: 0, y: 30}", "{opacity: 1, y: 0}", "back.out(2)")
st("#ev1", T["chase"] - .1, "{opacity: 1}")
js(f'tl.set("#flash", {{opacity: .4}}, {T["chase"] - .11:.3f});'); to("#flash", T["chase"] - .1, .35, "{opacity: 0}")
sfx("impact", T["chase"] - .1); sfx("screech", T["crazy"])

# ================= scene F: the tool finds it, then Klap
f0 = S["F"][0]
ft("#scan", T["tool"] - .1, .7, "{x: -560, opacity: 0}", "{x: 560, opacity: 1}", "power2.inOut")
to("#scan", T["tool"] + .6, .15, "{opacity: 0}")
sfx("riser_short", T["tool"] - .2)
ft("#lift", T["tool"] + .45, .6, "{opacity: 0, y: 330, scale: .3}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.4)")
sfx("whoosh", T["tool"] + .4)
to("#player2, #tline2", T["tool"] + .4, .4, "{opacity: .18, filter: 'blur(6px)'}")
# the reveal on the drop
tk = T["klap"]
to("#fstage", tk - .3, .25, "{opacity: 0, scale: .85, filter: 'blur(12px)'}", "power2.in")
st("#kring", tk - .03, "{opacity: .9, scale: .2}"); to("#kring", tk - .02, .9, "{opacity: 0, scale: 2.6}", "power2.out")
ft("#kicon", tk - .05, .6, "{opacity: 0, scale: .2, rotation: -25}", "{opacity: 1, scale: 1, rotation: 0}", "back.out(2.2)")
ft("#kword", tk + .2, .5, "{opacity: 0, x: -80, clipPath: 'inset(0 100% 0 0)'}", "{opacity: 1, x: 0, clipPath: 'inset(0 0% 0 0)'}", "power3.out")
ft("#ktag", tk + .5, .45, "{opacity: 0, y: 24}", "{opacity: 1, y: 0}", "power3.out")
js(f'tl.set("#flash", {{opacity: .55}}, {tk - .03:.3f});'); to("#flash", tk - .02, .5, "{opacity: 0}")
for i, (dx, dy) in enumerate(((10, -8), (-8, 6), (6, -4), (-3, 2), (0, 0))):
    st("#shake", tk + i * .035, f"{{x: {dx}, y: {dy}}}")
sfx("impact", tk); sfx("whoosh_big", tk - .25); sfx("sparkle", tk + .3)
whip_out("F")

# ================= scene G: paste the stream link, Generate
whip_in("G", "{y: 140, opacity: 0, scale: .94}", "{y: 0, opacity: 1, scale: 1}")
st("#ph", T["paste"] + .05, "{opacity: 0}")
ft("#kv", T["paste"] - .05, .25, "{opacity: 0, scale: .7}", "{opacity: 1, scale: 1}", "back.out(2.5)")
to("#kv", T["link"] + .35, .2, "{opacity: 0}")
ft("#url", T["paste"] + .05, .2, "{opacity: 0, x: -20}", "{opacity: 1, x: 0}", "power3.out")
sfx("click", T["paste"]); sfx("pop", T["paste"] + .07)
ft("#cursor", T["paste"] + .1, .6, "{x: -380, y: 160}", "{x: 0, y: 0}", "power3.inOut")
tg = T["link"] + .3
ft("#gen", tg, .12, "{scale: 1}", "{scale: .9}", "power2.out"); to("#gen", tg + .12, .2, "{scale: 1}", "back.out(3)")
sfx("click", tg)
ft("#prog", tg + .15, .25, "{opacity: 0, y: 20}", "{opacity: 1, y: 0}", "power3.out")
ft("#progbar", tg + .2, S["G"][1] - tg - .2, "{scaleX: 0}", "{scaleX: 1}", "power1.inOut")
whip_out("G")

# ================= scene H: best moments, each with a virality score
whip_in("H", "{opacity: 0, scale: 1.1}", "{opacity: 1, scale: 1}")
for i, (dx, rot) in enumerate(((-300, 14), (0, 0), (300, -14))):
    ft(f"#mc{i}", T["picks"] + [0.12, 0, .24][i], .55, f"{{opacity: 0, y: 260, rotationY: {rot * 2}}}", f"{{opacity: 1, y: 0, rotationY: {rot}}}", "back.out(1.4)")
    sfx("g_pop", T["picks"] + [0.12, 0, .24][i])
for i in range(3):
    ft(f"#vb{i}", T["scores"] + i * .15, .3, "{opacity: 0, scale: .5}", "{opacity: 1, scale: 1}", "back.out(2.5)")
    for q in range(5):
        sfx("tick", T["scores"] + i * .15 + q * .07)
ft("#rankpill", T["viral"] - .1, .4, "{opacity: 0, y: 30}", "{opacity: 1, y: 0}", "back.out(2)")
ft("#mc1 .glow", T["viral"], .5, "{opacity: 0}", "{opacity: 1}")
sfx("g_levelup", T["viral"])
whip_out("H")

# ================= scene I: reframe 16:9 -> 9:16 (Gaming layout), captions that pop
whip_in("I", "{opacity: 0, y: 100}", "{opacity: 1, y: 0}")
tv = T["vertical"] - .05
to("#land", tv, .5, "{scale: .62, opacity: 0}", "power3.inOut")
ft("#phone", tv, .55, "{opacity: 0, scaleX: 1.9, scaleY: .55}", "{opacity: 1, scaleX: 1, scaleY: 1}", "power3.inOut")
ft("#fcam2", tv + .1, .5, "{opacity: 0, x: 200, y: 220, scale: .5}", "{opacity: 1, x: 0, y: 0, scale: 1}", "power3.out")
sfx("whoosh", tv); sfx("shutter", tv + .45)
ft("#lyt", tv + .4, .35, "{opacity: 0, y: -16}", "{opacity: 1, y: 0}", "back.out(2)")
ft("#lg", T["gameplay"] - .05, .3, "{opacity: 0, x: -30}", "{opacity: 1, x: 0}", "back.out(2)")
ft("#ls", T["streamer"] - .05, .3, "{opacity: 0, x: 30}", "{opacity: 1, x: 0}", "back.out(2)")
sfx("pop", T["gameplay"]); sfx("pop", T["streamer"])
to("#lg, #ls", T["captions"] - .2, .2, "{opacity: 0}")
CAPW = ["NO", "WAY", "HE", "MADE", "THAT", "JUMP"]
tc0 = T["captions"]
for i, w in enumerate(CAPW):
    tw = tc0 + i * .17
    ft(f"#kc{i}", tw, .22, "{opacity: 0, scale: 1.8}", "{opacity: 1, scale: 1}", "back.out(3)")
    js(f'tl.set("#kc{i}", {{color: "#ffd400"}}, {tw:.3f}); tl.set("#kc{i}", {{color: "#ffffff"}}, {tw + .17:.3f});')
    sfx("g_pop", tw)
whip_out("I")

# ================= scene J: they scrub, you post
whip_in("J", "{opacity: 0, scale: 1.08}", "{opacity: 1, scale: 1}")
ft("#jl", S["J"][0] + .1, .45, "{opacity: 0, x: -120}", "{opacity: 1, x: 0}", "power3.out")
ft("#jr", T["your"] - .15, .5, "{opacity: 0, x: 120}", "{opacity: 1, x: 0}", "back.out(1.5)")
ft("#posted", T["up"] - .05, .35, "{opacity: 0, scale: .5}", "{opacity: 1, scale: 1}", "back.out(2.5)")
sfx("notify", T["up"]); sfx("g_complete", T["up"] + .1)
for i in range(7):
    ft(f"#ht{i}", T["up"] + .1 + i * .09, 1.1, "{opacity: 1, y: 0, x: 0, scale: .6}",
       f"{{opacity: 0, y: -330, x: {(-1) ** i * (20 + i * 9)}, scale: 1.2}}", "power1.out")
ft("#live", T["up"] + .4, .4, "{opacity: 0, y: 24}", "{opacity: 1, y: 0}", "power3.out")
whip_out("J")

# ================= scene K: CTA
whip_in("K", "{opacity: 0, scale: 1.12}", "{opacity: 1, scale: 1}")
ft("#klogo2", S["K"][0] + .05, .5, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}", "back.out(2)")
ft("#cbox", T["cta"] - .05, .45, "{opacity: 0, y: 50, scale: .92}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.8)")
for i, ch in enumerate("KLAP"):
    ft(f"#ck{i}", T["kw"] - .1 + i * .07, .04, "{opacity: 0}", "{opacity: 1}", "none")
    sfx("click", T["kw"] - .1 + i * .07)
ft("#cpost", T["kw"] + .3, .25, "{color: '#8a8f9c'}", f"{{color: '{PINK}'}}", "power2.out")
sfx("pop", T["kw"] + .35)
ft("#bio", T["grab"] - .05, .4, "{opacity: 0, y: 30}", "{opacity: 1, y: 0}", "back.out(2)")
sfx("ding", T["bio"])

# ---- counters (pure functions of time)
CNT = {"paid0": T["paid"] - .2, "paid1": S["B"][1], "tl0": S["E"][0] + .2, "tl1": T["chase"] - .2, "sc0": T["scores"],
       "hr0": S["J"][0], "hr1": S["J"][1]}

CSS = f"""
@font-face {{ font-family: Mont; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }}
@font-face {{ font-family: Serif; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }}
@font-face {{ font-family: Mono; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
@font-face {{ font-family: Inter; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
@font-face {{ font-family: Pop; font-weight: 600; src: url("assets/fonts/poppins-600.woff2"); }}
@font-face {{ font-family: Pop; font-weight: 700; src: url("assets/fonts/poppins-700.woff2"); }}
@font-face {{ font-family: Pop; font-weight: 800; src: url("assets/fonts/poppins-800.woff2"); }}
@font-face {{ font-family: Anton; src: url("assets/fonts/Anton.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {NIGHT}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Mont; font-weight: 800; color: #fff;
  background: radial-gradient(70% 40% at 12% 10%, rgba(255,95,162,.22), rgba(0,0,0,0) 70%), radial-gradient(70% 40% at 90% 92%, rgba(71,229,255,.16), rgba(0,0,0,0) 70%), {NIGHT}; }}
#shake {{ position: absolute; inset: 0; }}
.scn {{ position: absolute; inset: 0; opacity: 0; }}
#sA {{ opacity: 1; transform-origin: 50% 46%; overflow: hidden; }}
.fill {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
.clipw {{ position: absolute; inset: 0; opacity: 0; }} #aw0 {{ opacity: 1; }}
.shadeT {{ position: absolute; left: 0; right: 0; top: 0; height: 760px; background: linear-gradient(rgba(7,6,13,.92), rgba(7,6,13,.55) 55%, rgba(7,6,13,0)); }}
.shadeB {{ position: absolute; left: 0; right: 0; bottom: 0; height: 640px; background: linear-gradient(rgba(7,6,13,0), rgba(7,6,13,.8) 55%, rgba(7,6,13,.95)); }}
#vig {{ position: absolute; inset: 0; pointer-events: none; background: radial-gradient(100% 62% at 50% 52%, rgba(0,0,0,0) 58%, rgba(3,2,8,.6) 100%); }}
#grain {{ position: absolute; inset: 0; pointer-events: none; opacity: .07; background-image: url("assets/img/grain.png"); }}
#flash {{ position: absolute; inset: 0; background: #fff; mix-blend-mode: overlay; opacity: 0; pointer-events: none; }}
#bar {{ position: absolute; left: 70px; right: 70px; top: 258px; display: flex; justify-content: space-between; align-items: center;
  font-family: Mono; font-size: 24px; letter-spacing: .16em; color: rgba(255,255,255,.7); }}
#bar img {{ height: 40px; }} #bar b {{ color: {PINK}; }}
.hd {{ position: absolute; left: 30px; right: 30px; top: 330px; text-align: center; opacity: 0; }}
.hd.on {{ opacity: 1; }}
.hd .h1, .hd .h2 {{ opacity: 0; }} .hd.on .h1, .hd.on .h2 {{ opacity: 1; }}
.h1 {{ font-size: 82px; line-height: 1.0; letter-spacing: -.035em; text-shadow: 0 6px 30px rgba(0,0,0,.8); white-space: nowrap; }}
.h2 {{ font-family: Serif; font-style: italic; font-weight: 400; font-size: 98px; line-height: 1.04; white-space: nowrap; filter: drop-shadow(0 4px 22px rgba(0,0,0,.65)); }}
.h2 span {{ background: linear-gradient(90deg, #ff7ac6, #ffb36b); -webkit-background-clip: text; background-clip: text; color: transparent; padding: 0 .08em; }}
.cap {{ position: absolute; left: 60px; right: 60px; top: 1470px; text-align: center; font-family: Inter; font-weight: 700; font-size: 46px; opacity: 0;
  color: rgba(255,255,255,.45); text-shadow: 0 3px 14px rgba(0,0,0,.9); }}
/* B: the wall */
#wallw {{ position: absolute; inset: 0; perspective: 1500px; overflow: hidden; }}
#wall {{ position: absolute; left: 50%; top: 50%; width: 1360px; height: 2600px; margin: -1300px 0 0 -680px; display: flex; gap: 28px; justify-content: center;
  transform-style: preserve-3d; transform: rotateX(26deg) rotateZ(-12deg); }}
.col {{ display: flex; flex-direction: column; gap: 28px; }}
.tile {{ position: relative; width: 310px; height: 551px; border-radius: 30px; overflow: hidden; background: #111; box-shadow: 0 20px 50px rgba(0,0,0,.6), 0 0 0 2px rgba(255,255,255,.08); }}
.tic {{ position: absolute; right: 16px; bottom: 26px; display: flex; flex-direction: column; gap: 18px; }}
.tic i {{ display: block; width: 34px; height: 34px; border-radius: 50%; background: rgba(255,255,255,.85); box-shadow: 0 2px 8px rgba(0,0,0,.5); }}
#bdim {{ position: absolute; inset: 0; background: linear-gradient(rgba(7,6,13,.85), rgba(7,6,13,.25) 40%, rgba(7,6,13,.3) 62%, rgba(7,6,13,.92)); }}
#hud {{ position: absolute; left: 130px; right: 130px; top: 1100px; height: 250px; border-radius: 40px; opacity: 0; display: flex; align-items: center; justify-content: space-around;
  background: rgba(14,10,24,.78); border: 2px solid rgba(255,255,255,.14); box-shadow: 0 30px 80px rgba(0,0,0,.6); backdrop-filter: blur(14px); }}
#hud .k {{ font-family: Mono; font-size: 24px; letter-spacing: .16em; color: rgba(255,255,255,.6); }}
#hud .v {{ font-family: Anton; font-size: 104px; line-height: 1.05; letter-spacing: .01em; }}
#hud .money {{ color: {GOLD}; text-shadow: 0 0 34px rgba(255,194,61,.45); }}
#hud .sep {{ width: 2px; height: 150px; background: rgba(255,255,255,.14); }}
/* D: campaigns */
#dbg {{ filter: blur(16px) brightness(.42) saturate(1.2); transform: scale(1.15); }}
#cards {{ position: absolute; left: 90px; right: 90px; top: 610px; perspective: 1400px; display: flex; flex-direction: column; gap: 34px; }}
.card {{ position: relative; height: 210px; border-radius: 40px; display: flex; align-items: center; gap: 34px; padding: 0 40px; opacity: 0;
  background: linear-gradient(135deg, rgba(255,255,255,.16), rgba(255,255,255,.05)); border: 2px solid rgba(255,255,255,.22); box-shadow: 0 30px 70px rgba(0,0,0,.5); backdrop-filter: blur(16px); }}
.mono {{ width: 130px; height: 130px; border-radius: 34px; flex: none; display: grid; place-items: center; font-family: Anton; font-size: 62px; color: #fff;
  background: linear-gradient(135deg, {PINK}, {ORANGE}); box-shadow: 0 10px 30px rgba(255,95,162,.45); }}
#cardB .mono {{ background: linear-gradient(135deg, {CYAN}, #7a5cff); box-shadow: 0 10px 30px rgba(71,229,255,.35); }}
.card .kk {{ font-family: Mono; font-size: 22px; letter-spacing: .16em; color: rgba(255,255,255,.62); }}
.card .nm {{ font-size: 66px; letter-spacing: -.03em; line-height: 1.05; }}
.card .pill {{ position: absolute; right: 34px; top: 30px; font-family: Inter; font-weight: 700; font-size: 26px; padding: 8px 18px; border-radius: 999px;
  color: {GOLD}; background: rgba(255,194,61,.14); border: 2px solid rgba(255,194,61,.7); opacity: 0; }}
#rate {{ position: absolute; left: 0; right: 0; top: 1110px; text-align: center; opacity: 0; }}
#rate b {{ font-family: Anton; font-size: 230px; line-height: .95; color: {GOLD}; text-shadow: 0 0 60px rgba(255,194,61,.5); letter-spacing: .01em; }}
#rate b small {{ font-size: 120px; vertical-align: top; color: rgba(255,194,61,.8); }}
#rate .per {{ display: block; font-family: Inter; font-weight: 700; font-size: 44px; color: rgba(255,255,255,.88); opacity: 0; }}
/* E: stream + timeline */
#player {{ position: absolute; left: 60px; width: 960px; top: 640px; height: 540px; border-radius: 34px; overflow: hidden; background: #000;
  box-shadow: 0 40px 90px rgba(0,0,0,.65), 0 0 0 3px rgba(255,255,255,.1); }}
.live {{ position: absolute; left: 24px; top: 22px; font-family: Inter; font-weight: 700; font-size: 26px; padding: 6px 16px 6px 36px; border-radius: 10px; background: #e5283d; letter-spacing: .05em; }}
.live:before {{ content: ""; position: absolute; left: 14px; top: 50%; width: 12px; height: 12px; margin-top: -6px; border-radius: 50%; background: #fff; }}
#ev1 {{ opacity: 0; }}
#tline {{ position: absolute; left: 60px; width: 960px; top: 1225px; height: 150px; }}
#track {{ position: absolute; left: 0; right: 0; top: 54px; height: 16px; border-radius: 8px; background: rgba(255,255,255,.16); overflow: hidden; }}
#trackf {{ position: absolute; left: 0; top: 0; bottom: 0; width: 100%; background: linear-gradient(90deg, {PINK}, {ORANGE}); transform-origin: 0 50%; transform: scaleX(0); }}
#head {{ position: absolute; left: 0; top: 44px; width: 36px; height: 36px; margin-left: -18px; border-radius: 50%; background: #fff; box-shadow: 0 0 0 6px rgba(255,255,255,.2); }}
#tc {{ position: absolute; left: 0; top: -6px; width: 200px; margin-left: -100px; text-align: center; font-family: Mono; font-size: 30px; }}
.tl0, #tl3 {{ position: absolute; top: 92px; font-family: Mono; font-size: 30px; color: rgba(255,255,255,.7); }}
.tl0 {{ left: 0; }} #tl3 {{ right: 0; transform-origin: 100% 50%; }}
#seg {{ position: absolute; left: 58%; width: 5%; top: 46px; height: 32px; border-radius: 8px; background: #ff3b5c; box-shadow: 0 0 24px #ff3b5c; opacity: 0; }}
#pin {{ position: absolute; left: 60.5%; top: -64px; transform: translateX(-50%); font-family: Inter; font-weight: 700; font-size: 30px; white-space: nowrap; opacity: 0;
  padding: 8px 18px; border-radius: 14px; background: #ff3b5c; }}
#scan {{ position: absolute; left: 50%; top: 600px; width: 14px; height: 820px; margin-left: -7px; opacity: 0;
  background: linear-gradient(rgba(71,229,255,0), {CYAN} 30%, #fff 50%, {CYAN} 70%, rgba(71,229,255,0)); box-shadow: 0 0 40px {CYAN}; }}
#lift {{ position: absolute; left: 50%; top: 600px; width: 420px; height: 746px; margin-left: -210px; border-radius: 34px; overflow: hidden; opacity: 0;
  box-shadow: 0 40px 90px rgba(0,0,0,.7), 0 0 0 4px #ff3b5c, 0 0 60px rgba(255,59,92,.6); }}
/* F: Klap reveal */
#kwrap {{ position: absolute; left: 0; right: 0; top: 700px; display: flex; flex-direction: column; align-items: center; }}
#kring {{ position: absolute; left: 50%; top: 860px; width: 420px; height: 420px; margin: -210px 0 0 -210px; border-radius: 50%; border: 10px solid #fff; opacity: 0; }}
#klogo {{ display: flex; align-items: center; gap: 46px; height: 300px; }}
#kicon {{ height: 300px; opacity: 0; filter: drop-shadow(0 0 50px rgba(255,255,255,.35)); }}
#kword {{ height: 214px; margin-top: 30px; opacity: 0; }}
#ktag {{ margin-top: 70px; font-family: Pop; font-weight: 600; font-size: 46px; color: rgba(255,255,255,.78); opacity: 0; }}
/* G: Klap app */
.app {{ position: absolute; left: 50px; right: 50px; top: 610px; border-radius: 44px; background: #fff; color: {INK}; font-family: Pop; font-weight: 600;
  box-shadow: 0 40px 100px rgba(0,0,0,.6); padding: 34px 44px 46px; }}
.nav {{ display: flex; align-items: center; gap: 22px; font-size: 26px; color: #4b5563; }}
.nav img {{ height: 50px; }} .nav .sp {{ flex: 1; }}
.app h3 {{ font-family: Pop; font-weight: 700; font-size: 64px; margin: 38px 0 26px; letter-spacing: -.01em; }}
.inp {{ position: relative; height: 120px; border-radius: 28px; border: 2px solid #e5e7eb; display: flex; align-items: center; gap: 22px; padding: 0 16px 0 30px;
  box-shadow: 0 14px 40px rgba(15,23,42,.08); font-size: 29px; color: #9ca3af; font-weight: 600; }}
.inp svg {{ flex: none; }}
#ph, #url {{ position: absolute; left: 92px; top: 50%; transform: translateY(-50%); white-space: nowrap; }}
#url {{ color: {INK}; opacity: 0; font-weight: 600; }}
#gen {{ margin-left: auto; height: 88px; padding: 0 30px; border-radius: 22px; background: {INK}; color: #fff; display: flex; align-items: center; gap: 12px; font-size: 30px; font-weight: 600; }}
#kv {{ position: absolute; right: 240px; top: -64px; font-family: Inter; font-weight: 700; font-size: 26px; padding: 8px 16px; border-radius: 12px; background: {INK}; color: #fff; opacity: 0; }}
#cursor {{ position: absolute; right: 70px; top: 70px; width: 58px; filter: drop-shadow(0 4px 8px rgba(0,0,0,.4)); }}
#prog {{ margin-top: 30px; opacity: 0; }}
#prog .t {{ font-size: 28px; color: #4b5563; margin-bottom: 14px; }}
#prog .bar {{ height: 16px; border-radius: 8px; background: #eef0f4; overflow: hidden; }}
#progbar {{ height: 100%; background: linear-gradient(90deg, #7c3aed, {PINK}); transform-origin: 0 50%; }}
.tmpl {{ display: flex; gap: 18px; margin-top: 30px; }}
.tmpl div {{ flex: 1; height: 96px; border-radius: 18px; background: linear-gradient(135deg, #1f2433, #2b2140); display: flex; align-items: center; justify-content: center; gap: 7px; font-family: Mont; font-weight: 900;
  font-size: 21px; color: #fff; letter-spacing: .02em; white-space: nowrap; }}
.tmpl div.sel {{ box-shadow: 0 0 0 4px #3b82f6; }} .tmpl b {{ color: #ffd400; }}
/* H: moments */
#moments {{ position: absolute; left: 0; right: 0; top: 640px; height: 620px; perspective: 1600px; }}
.mc {{ position: absolute; left: 50%; top: 40px; width: 300px; height: 533px; margin-left: -150px; border-radius: 30px; overflow: visible; opacity: 0; transform-style: preserve-3d; }}
.mc .in {{ position: absolute; inset: 0; border-radius: 30px; overflow: hidden; box-shadow: 0 30px 70px rgba(0,0,0,.6), 0 0 0 3px rgba(255,255,255,.14); }}
#mc0 {{ margin-left: -480px; }} #mc2 {{ margin-left: 180px; }}
#mc1 {{ top: 0; width: 330px; height: 587px; margin-left: -165px; z-index: 2; }}
.mc .glow {{ position: absolute; inset: -10px; border-radius: 38px; border: 5px solid {PINK}; box-shadow: 0 0 50px {PINK}; opacity: 0; }}
.vb {{ position: absolute; left: 18px; top: 18px; display: flex; align-items: center; gap: 8px; padding: 8px 16px 8px 12px; border-radius: 999px; background: #fff; color: {INK};
  font-family: Pop; font-weight: 800; font-size: 34px; opacity: 0; box-shadow: 0 6px 20px rgba(0,0,0,.4); }}
.vb small {{ font-size: 20px; color: #6b7280; font-weight: 600; }}
.rk {{ position: absolute; left: 0; right: 0; bottom: -64px; text-align: center; font-family: Mono; font-size: 30px; color: rgba(255,255,255,.75); }}
#rankpill {{ position: absolute; left: 0; right: 0; top: 1330px; text-align: center; opacity: 0; }}
#rankpill span {{ font-family: Inter; font-weight: 700; font-size: 32px; padding: 12px 26px; border-radius: 999px; background: rgba(255,95,162,.16); border: 2px solid {PINK}; color: #ffd0e6; }}
/* I: reframe */
#land {{ position: absolute; left: 60px; width: 960px; top: 700px; height: 540px; border-radius: 30px; overflow: hidden; box-shadow: 0 40px 90px rgba(0,0,0,.6); }}
#fcam1 {{ position: absolute; right: 22px; bottom: 22px; width: 300px; height: 188px; border-radius: 18px; overflow: hidden; box-shadow: 0 0 0 4px #fff; }}
#phone {{ position: absolute; left: 50%; top: 590px; width: 474px; height: 842px; margin-left: -237px; border-radius: 46px; overflow: hidden; opacity: 0; background: #000;
  box-shadow: 0 40px 100px rgba(0,0,0,.7), 0 0 0 10px #15131c, 0 0 0 12px rgba(255,255,255,.18); }}
#fcam2 {{ position: absolute; left: 0; top: 0; width: 474px; height: 300px; overflow: hidden; opacity: 0; }}
#game2 {{ position: absolute; left: 0; top: 300px; width: 474px; height: 542px; overflow: hidden; }}
#kcap {{ position: absolute; left: 10px; right: 10px; top: 318px; text-align: center; font-family: Mont; font-weight: 900; font-size: 50px; line-height: 1.1; letter-spacing: -.01em;
  -webkit-text-stroke: 3px #000; paint-order: stroke fill; text-shadow: 0 5px 0 #000; }}
#kcap span {{ display: inline-block; opacity: 0; margin: 0 6px; }}
#lyt {{ position: absolute; left: 0; right: 0; top: 548px; text-align: center; opacity: 0; font-family: Mono; font-size: 26px; letter-spacing: .14em; color: {CYAN}; }}
.lbl2 {{ position: absolute; font-family: Inter; font-weight: 700; font-size: 30px; padding: 8px 18px; border-radius: 12px; opacity: 0; white-space: nowrap; }}
#ls {{ left: 790px; top: 720px; background: {CYAN}; color: {INK}; }}
#lg {{ left: 80px; top: 1180px; background: {ORANGE}; color: {INK}; }}
/* J: split */
.half {{ position: absolute; top: 620px; width: 470px; height: 700px; border-radius: 36px; overflow: hidden; opacity: 0; }}
#jl {{ left: 50px; background: rgba(255,255,255,.05); border: 2px solid rgba(255,255,255,.12); }}
#jr {{ left: 560px; background: linear-gradient(160deg, rgba(255,95,162,.25), rgba(71,229,255,.14)); border: 2px solid rgba(255,95,162,.5); }}
.half .lab {{ position: absolute; left: 0; right: 0; top: 30px; text-align: center; font-family: Mono; font-size: 26px; letter-spacing: .16em; color: rgba(255,255,255,.7); }}
#jmon {{ position: absolute; left: 30px; right: 30px; top: 100px; height: 230px; border-radius: 20px; overflow: hidden; filter: grayscale(1) brightness(.6); }}
#jtrack {{ position: absolute; left: 40px; right: 40px; top: 380px; height: 12px; border-radius: 6px; background: rgba(255,255,255,.18); }}
#jhead {{ position: absolute; left: 0; top: -12px; width: 36px; height: 36px; margin-left: -18px; border-radius: 50%; background: #9aa0aa; }}
#jtc {{ position: absolute; left: 0; right: 0; top: 440px; text-align: center; font-family: Mono; font-size: 64px; color: rgba(255,255,255,.55); }}
#jspin {{ position: absolute; left: 50%; top: 560px; width: 70px; height: 70px; margin-left: -35px; border-radius: 50%; border: 8px solid rgba(255,255,255,.15); border-top-color: rgba(255,255,255,.6); }}
#jphone {{ position: absolute; left: 50%; top: 90px; width: 290px; height: 516px; margin-left: -145px; border-radius: 34px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,.6), 0 0 0 6px #15131c; }}
#posted {{ position: absolute; left: 50%; top: 520px; transform: translateX(-50%); display: flex; align-items: center; gap: 10px; white-space: nowrap; opacity: 0;
  font-family: Inter; font-weight: 700; font-size: 32px; padding: 10px 22px; border-radius: 999px; background: #22c55e; color: #04210f; box-shadow: 0 10px 30px rgba(34,197,94,.5); }}
.ht {{ position: absolute; left: 330px; top: 470px; width: 46px; height: 46px; opacity: 0; }}
#live {{ position: absolute; left: 0; right: 0; top: 1350px; text-align: center; opacity: 0; }}
#live span {{ font-family: Inter; font-weight: 700; font-size: 30px; padding: 12px 24px; border-radius: 999px; background: rgba(71,229,255,.12); border: 2px solid {CYAN}; color: #c9f6ff; }}
/* K: CTA */
#kbg {{ filter: blur(8px) brightness(.38) saturate(1.2); transform: scale(1.1); }}
#klogo2 {{ position: absolute; left: 50%; top: 700px; width: 600px; margin-left: -300px; opacity: 0; filter: drop-shadow(0 0 40px rgba(255,255,255,.25)); }}
#cbox {{ position: absolute; left: 110px; right: 110px; top: 1010px; height: 132px; border-radius: 66px; opacity: 0; display: flex; align-items: center; gap: 24px;
  padding: 0 38px 0 26px; background: rgba(250,250,252,.97); color: {INK}; box-shadow: 0 30px 80px rgba(0,0,0,.6), 0 0 0 3px rgba(255,95,162,.8); }}
#cbox .av {{ width: 80px; height: 80px; border-radius: 50%; background: conic-gradient({PINK}, {ORANGE}, {GOLD}, {CYAN}, #7a5cff, {PINK}); flex: none; }}
#cbox .tx {{ flex: 1; font-size: 56px; letter-spacing: .05em; }} #cbox .tx span {{ opacity: 0; }}
#cpost {{ font-size: 36px; color: #8a8f9c; }}
#bio {{ position: absolute; left: 0; right: 0; top: 1200px; text-align: center; opacity: 0; }}
#bio span {{ font-family: Inter; font-weight: 700; font-size: 34px; padding: 12px 28px; border-radius: 999px; background: rgba(255,255,255,.1); border: 2px solid rgba(255,255,255,.4); }}
"""

UP = '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#6b7280" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 15V4"/><path d="M7 9l5-5 5 5"/><path d="M4 15v4a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-4"/></svg>'
SPARK = '<svg width="30" height="30" viewBox="0 0 24 24" fill="#fff"><path d="M12 2l1.8 5.6L19 9.5l-5.2 1.9L12 17l-1.8-5.6L5 9.5l5.2-1.9z"/><path d="M19 14l.9 2.6 2.6.9-2.6.9L19 21l-.9-2.6-2.6-.9 2.6-.9z"/></svg>'
CURSOR = '<svg id="cursor" viewBox="0 0 24 24"><path d="M4 2l15 9-6.5 1.6L9.5 19z" fill="#0b0f1a" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>'
FLAME = '<svg width="30" height="30" viewBox="0 0 24 24" fill="#ff5a1f"><path d="M12 2c1 4 5 5.5 5 11a5 5 0 0 1-10 0c0-2.5 1.2-4 2.5-5 .2 2 1 3 2 3.5C11 9 11 5 12 2z"/></svg>'
HEART = '<svg class="ht" id="ht{i}" viewBox="0 0 24 24" fill="#ff4d79"><path d="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 3 4.5 6.8 4.5c2.1 0 3.5 1.1 5.2 3 1.7-1.9 3.1-3 5.2-3 3.8 0 5.9 3.9 4.4 7.3C19.5 16.4 12 21 12 21z"/></svg>'
CHECK = '<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#04210f" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5 5L20 6.5"/></svg>'

e0, e1 = S["E"]
SC = f"""
  <div class="scn" id="sA">{''.join(A_HTML)}<div class="shadeT"></div><div class="shadeB"></div></div>
  <div class="scn" id="sB"><div id="wallw"><div id="wall">{''.join(B_COLS)}</div></div><div id="bdim"></div>
    <div id="hud"><div><div class="k">VIEWS</div><div class="v" id="nv">0</div></div><div class="sep"></div><div><div class="k">EARNED</div><div class="v money" id="nm">$0</div></div></div></div>
  <div class="scn" id="sD">{vid("dbgv", "r_sky", S["D"][0], S["D"][1] + .25, .5, "fill", "")}<div class="fill" id="dbg"></div>
    <div id="cards">
      <div class="card" id="cardA"><div class="mono">MB</div><div><div class="kk">CLIPPING CAMPAIGNS</div><div class="nm">MrBeast</div></div><div class="pill">~$1 / 1K views</div></div>
      <div class="card" id="cardB"><div class="mono">IS</div><div><div class="kk">CLIPPING CAMPAIGNS</div><div class="nm">IShowSpeed</div></div><div class="pill">~$1 / 1K views</div></div>
    </div>
    <div id="rate"><b><small>~</small>$1</b><span class="per">for every 1,000 views</span></div></div>
  <div class="scn" id="sE"><div id="fstage">
    <div id="player"><div id="player2" class="fill">{vid("ev0", "stream", e0, T["chase"] - .1 + .01, 0, "fill")}{vid("ev1", "stream_chase_l", T["chase"] - .1, e1 + .25, .2, "fill")}</div><div class="live">LIVE</div></div>
    <div id="tline"><div id="tline2"><div id="tc">0:00:00</div><div id="track"><div id="trackf"></div></div><div id="seg"></div><div id="head"></div>
      <div class="tl0">0:00:00</div><div id="tl3">3:00:00</div><div id="pin">1 crazy chase</div></div></div>
    <div id="scan"></div>
    <div id="lift">{vid("liftv", "c_truck", T["tool"] + .4, e1 + .25, .1, "fill")}</div></div></div>
  <div class="scn" id="sF"><div id="kring"></div><div id="kwrap"><div id="klogo"><img id="kicon" src="assets/img/klap_icon_white.svg" alt=""><img id="kword" src="assets/img/klap_word_white.svg" alt=""></div>
    <div id="ktag">Turn videos into viral shorts</div></div></div>
  <div class="scn" id="sG"><div class="app">
    <div class="nav"><img src="assets/img/klap_logo_ink.svg" alt=""><span class="sp"></span><span>Videos</span><span>Calendar</span><span>Analytics</span></div>
    <h3>Videos</h3>
    <div class="inp">{UP}<span id="ph">Drop a file or paste a link</span><span id="url">twitch.tv/videos/2290158741</span>
      <div id="gen">{SPARK}Generate</div><div id="kv">Ctrl + V</div>{CURSOR}</div>
    <div class="tmpl"><div class="sel">NO WAY <b>HE</b> DID</div><div>NO <b>WAY</b> HE DID</div><div>No way he did</div></div>
    <div id="prog"><div class="t">Finding the best moments...</div><div class="bar"><div id="progbar"></div></div></div></div></div>
  <div class="scn" id="sH"><div id="moments">
    {''.join(f'<div class="mc" id="mc{i}"><div class="glow"></div><div class="in">{vid(f"hv{i}", s, S["H"][0], S["H"][1] + .25, m)}</div><div class="vb" id="vb{i}">{FLAME}<span id="vs{i}">0</span><small>/100</small></div><div class="rk">#{r}</div></div>' for i, (s, m, r) in enumerate((("t_cops", .3, 2), ("t_flip", .1, 1), ("t_heli", .6, 3))))}
    </div><div id="rankpill"><span>Ranked by virality score</span></div></div>
  <div class="scn" id="sI">
    <div id="land">{vid("iv0", "stream_cops_l", S["I"][0], T["vertical"] + .6, .3, "fill")}<div id="fcam1">{vid("iv1", "facecam", S["I"][0], T["vertical"] + .6, .0, "fill")}</div></div>
    <div id="phone"><div id="game2">{vid("iv2", "game_l", T["vertical"] - .1, S["I"][1] + .25, .0, "fill")}</div>
      <div id="fcam2">{vid("iv4", "facecam", T["vertical"] - .1, S["I"][1] + .25, 1.0, "fill")}</div>
      <div id="kcap">{''.join(f'<span id="kc{i}">{w}</span>' for i, w in enumerate(CAPW))}</div></div>
    <div id="lyt">KLAP · GAMING LAYOUT</div><div class="lbl2" id="ls">streamer</div><div class="lbl2" id="lg">gameplay</div></div>
  <div class="scn" id="sJ">
    <div class="half" id="jl"><div class="lab">OTHER CLIPPERS</div><div id="jmon">{vid("jv0", "stream", S["J"][0], S["J"][1] + .25, 2.0, "fill")}</div>
      <div id="jtrack"><div id="jhead"></div></div><div id="jtc">2:14:07</div><div id="jspin"></div></div>
    <div class="half" id="jr"><div class="lab">YOU</div><div id="jphone">{vid("jv1", "t_flip", S["J"][0], S["J"][1] + .25, .4, "fill")}</div>
      <div id="posted">{CHECK}Posted</div>{''.join(HEART.format(i=i) for i in range(7))}</div>
    <div id="live"><span>Works on live streams: first clips in ~15 min</span></div></div>
  <div class="scn" id="sK">{vid("kbgv", "c_boat", S["K"][0], min(DUR, S["K"][0] + 2.85), .0, "fill")}{vid("kbgv2", "r_sky", min(DUR, S["K"][0] + 2.85), DUR, 1.5, "fill")}<div class="fill" id="kbg"></div>
    <div class="shadeT"></div><div class="shadeB"></div>
    <img id="klogo2" src="assets/img/klap_logo_white.svg" alt="">
    <div id="cbox"><div class="av"></div><div class="tx">{"".join(f'<span id="ck{i}">{c}</span>' for i, c in enumerate("KLAP"))}</div><b id="cpost">Post</b></div>
    <div id="bio"><span>or tap the link in bio</span></div></div>
"""
# the blurred backdrops are CSS-filtered copies of the videos: apply the filter to the video elements themselves
SC = SC.replace('<div class="fill" id="dbg"></div>', "").replace('<div class="fill" id="kbg"></div>', "")
SC = SC.replace('id="dbgv" class="fill"', 'id="dbgv" class="fill" data-blur="d"').replace('id="kbgv" class="fill"', 'id="kbgv" class="fill" data-blur="k"').replace('id="kbgv2" class="fill"', 'id="kbgv2" class="fill" data-blur="k"')
CSS += """
video[data-blur="d"] { filter: blur(16px) brightness(.55) saturate(1.2); transform: scale(1.15); }
video[data-blur="k"] { filter: blur(8px) brightness(.36) saturate(1.2); transform: scale(1.1); }
"""

COUNTERS = f"""
const C = {json.dumps({k: round(v, 3) for k, v in CNT.items()})};
const clamp = (x) => Math.max(0, Math.min(1, x));
const eio = (x) => x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2;
const fmt = (n) => Math.round(n).toLocaleString("en-US");
const hms = (s) => {{ s = Math.floor(s); const h = Math.floor(s / 3600), m = Math.floor(s / 60) % 60, x = s % 60; return h + ":" + String(m).padStart(2, "0") + ":" + String(x).padStart(2, "0"); }};
const $ = (id) => document.getElementById(id);
function counters(t) {{
  const p = eio(clamp((t - C.paid0) / (C.paid1 - C.paid0)));
  $("nv").textContent = fmt(p * 480000); $("nm").textContent = "$" + fmt(p * 480);
  const q = clamp((t - C.tl0) / (C.tl1 - C.tl0)), pos = .605 * (1 - Math.pow(1 - q, 1.6)) + Math.sin(q * 9) * .03 * (1 - q);
  $("head").style.transform = "translateX(" + (pos * 960) + "px)"; $("tc").style.transform = "translateX(" + (pos * 960) + "px)";
  $("trackf").style.transform = "scaleX(" + pos + ")"; $("tc").textContent = hms(pos * 10800);
  for (const [i, v] of [[0, 94], [1, 99], [2, 87]]) {{ const r = clamp((t - C.sc0 - i * .15) / .5); $("vs" + i).textContent = Math.round(eio(r) * v); }}
  const h = clamp((t - C.hr0) / (C.hr1 - C.hr0)), sw = .48 + .1 * Math.sin(t * 5.3) + .05 * Math.sin(t * 11.7);
  $("jhead").style.left = (sw * 100) + "%"; $("jtc").textContent = hms(8047 + h * 9 + Math.sin(t * 5.3) * 40);
  $("jspin").style.transform = "rotate(" + (t * 420) + "deg)";
}}
counters(0);
window.addEventListener("hf-seek", (e) => counters(e.detail.time));
tl.to({{}}, {{duration: {DUR:.2f}, onUpdate: () => counters(tl.time())}}, 0);
"""

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>AI.NXTLVL x Klap GTA 6 clippers 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div id="shake" data-layout-allow-overflow>
      {SC}
      </div>
      <div id="vig"></div><div id="grain"></div>
      <div id="bar"><img src="assets/img/logo-wordmark.png" alt=""><span><b>GTA 6</b> · CLIPPING</span></div>
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
json.dump({"dur": DUR, "scenes": {k: [round(a, 3), round(b, 3)] for k, (a, b) in S.items()}}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx, {TRK[0]} videos")
print({k: round(v, 2) for k, v in T.items()})
print({k: (round(a, 2), round(b, 2)) for k, (a, b) in S.items()})
