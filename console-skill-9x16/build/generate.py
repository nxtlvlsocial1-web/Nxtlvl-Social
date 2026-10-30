"""Writes index.html: the console-skill Reel for AI.NXTLVL as one HyperFrames composition.

python3 build/generate.py      (from the project root, after build/voice.py and build/prep.py)

Style follows the EarnEdits reference (Video-15505): warm dark pixel-art scenes, one object in a spotlight, a headline
built word by word at the top (heavy lowercase sans for connector words, a cream pixel display face, white pixel text on
slanted red labels), yellow spark marks, glitch cuts every 1-2 s, motion stepped on twos (15 fps), grain and vignette.
The script follows the modern story arc (nxtlvl-social-video 3a). Every spoken word appears on screen as it is said.
Writes build/cues.json (cuts and sound events) for build/audio.py.
"""
import json
import os
import random

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
W = json.load(open(os.path.join(B, "words.json")))
DUR = 39.0
FPS = 15
F = 1 / 30
R = random.Random(11)
CREAM, RED, YEL, INK = "#EFE4CC", "#D12A1F", "#F4C531", "#140E0A"

A = []        # timeline lines
HIDE = []     # selectors hidden at load
SHOTS = []    # shot html
EV = []       # (t, kind) sound events
CUTS = []


def t_(i):
    return W[i]["s"]


def js(s):
    A.append("      " + s)


def steps(d):
    return f'"steps({max(1, round(d * FPS))})"'


def ev(t, kind):
    EV.append((round(t, 3), kind))


# ---------------------------------------------------------------- geometry

def homography(w, h, quad):
    src = [(0, 0), (w, 0), (w, h), (0, h)]
    M, v = [], []
    for (x, y), (u, vv) in zip(src, quad):
        M.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); v.append(u)
        M.append([0, 0, 0, x, y, 1, -vv * x, -vv * y]); v.append(vv)
    a, b, c, d, e, f, g, hh = np.linalg.solve(np.array(M, float), np.array(v, float))
    return f"matrix3d({a:.6f},{d:.6f},0,{g:.8f},{b:.6f},{e:.6f},0,{hh:.8f},0,0,1,0,{c:.3f},{f:.3f},0,1)"


QUAD = {
    "monitor": [(463, 343), (1191, 263), (1193, 707), (457, 675)],
    "laptop": [(603, 206), (1272, 218), (1221, 654), (517, 601)],
    "phone": [(433, 318), (1196, 400), (1162, 752), (368, 600)],
    "handheld": [(453, 306), (1184, 229), (1240, 594), (471, 683)],
    "crt": [(468, 566), (797, 541), (802, 826), (466, 833)],
}
SIZE = {"boy-at-pc": (1536, 1024), "bg-ps2-desk": (1254, 1254), "pc-monitor-desk": (1536, 1024), "disc-bell-jar": (1145, 1374),
        "disc-case": (1536, 1024), "laptop-desk": (1536, 1024), "bg-spotlight-room": (1024, 1536), "bg-desk-wide": (1536, 1024),
        "phone-desk": (1536, 1024), "hands-controller": (1536, 1024), "bg-crt-tv": (1312, 1199), "hand-magnifier": (1536, 1024),
        "handheld-hands": (1672, 941), "hourglass": (1312, 1199), "boy-trophy": (1024, 1536), "calendar-pages": (1536, 1024)}


# ---------------------------------------------------------------- shots

class Shot:
    def __init__(self, sid, t0, t1, img=None, cam0=None, cam1=None, video=None, head_top=290, cut="glitch"):
        self.id, self.t0, self.t1, self.img = sid, t0, t1, img
        self.inner, self.cam_inner, self.head = [], [], []
        self.head_top = head_top
        CUTS.append(t0)
        if t0 > 0:
            if cut == "glitch":
                glitch(t0)
            ev(t0, "cut")
        if img:
            iw, ih = SIZE[img]
            self.inner.append(f'<img class="bgi" src="assets/img/{img}-bg.jpg" alt="">')
            (s0, fx0, fy0, cx0, cy0), (s1, fx1, fy1, cx1, cy1) = cam0, cam1
            p0 = dict(x=round(cx0 - fx0 * s0, 1), y=round(cy0 - fy0 * s0, 1), scale=s0)
            p1 = dict(x=round(cx1 - fx1 * s1, 1), y=round(cy1 - fy1 * s1, 1), scale=s1)
            js(f'tl.set("#{sid}-cam", {json.dumps(p0)}, {t0:.3f});')
            js(f'tl.to("#{sid}-cam", {{...{json.dumps(p1)}, duration: {t1 - t0:.3f}, ease: {steps(t1 - t0)}}}, {t0:.3f});')
            self.iw, self.ih = iw, ih
        if video:
            src, mstart = video
            VIDEOS.append(f'<div class="vwrap" id="{sid}-vw"><video id="{sid}-v" class="clip" src="assets/video/{src}" data-start="{t0:.3f}" '
                          f'data-duration="{t1 - t0:.3f}" data-media-start="{mstart}" data-track-index="0" muted playsinline></video></div>')
            js(f'tl.fromTo("#{sid}-vw", {{scale: 1.0}}, {{scale: 1.07, duration: {t1 - t0:.3f}, ease: {steps(t1 - t0)}}}, {t0:.3f});')
        SHOTS.append(self)

    def html(self):
        cam = ""
        if self.img:
            cam = (f'<div class="cam" id="{self.id}-cam" style="width:{self.iw}px;height:{self.ih}px">'
                   f'<img class="art" src="assets/img/{self.img}.jpg" alt="">{"".join(self.cam_inner)}</div>')
        bg = "" if self.img else ' style="background:transparent"'
        return (f'<div id="{self.id}" class="clip shot" data-start="{self.t0:.3f}" data-duration="{self.t1 - self.t0:.3f}" data-track-index="2"{bg}>'
                f'<div class="rig" id="{self.id}-rig">{"".join(self.inner[:1])}{cam}{"".join(self.inner[1:])}</div>'
                f'<div class="head" id="{self.id}-head" style="top:{self.head_top}px">{"".join(self.head)}</div></div>')

    # -- screen inserted into the art (perspective-mapped)
    def screen(self, kind, inner, t_on, w=800, h=480, sid=None):
        sid = sid or f"{self.id}-scr"
        self.cam_inner.append(f'<div class="scr" id="{sid}" style="width:{w}px;height:{h}px;transform:{homography(w, h, QUAD[kind])}">{inner}</div>')
        HIDE.append("#" + sid)
        for k, o in enumerate([.7, .25, 1]):
            js(f'tl.set("#{sid}", {{opacity: {o}}}, {t_on + k * F:.3f});')
        ev(t_on, "on")
        return sid

    def add(self, html_, cam=False):
        (self.cam_inner if cam else self.inner).append(html_)


VIDEOS = []


# ---------------------------------------------------------------- headline

def line(shot, kind, words, size=None, gap=0, color=None):
    """One headline line. words: [(text, t)]. kind: sm | big | lab | red."""
    n = len(shot.head)
    lid = f"{shot.id}-l{n}"
    st = []
    if size:
        st.append(f"font-size:{size}px")
    if gap:
        st.append(f"margin-top:{gap}px")
    if color:
        st.append(f"color:{color}")
    style = f' style="{";".join(st)}"' if st else ""
    if kind == "lab":
        inner = " ".join(f'<span class="w" id="{lid}-w{i}">{w}</span>' for i, (w, _) in enumerate(words))
        shot.head.append(f'<div class="ln lab" id="{lid}"{style}><span class="lb"><span class="lt">{inner}</span></span></div>')
        t0 = words[0][1]
        HIDE.append(f"#{lid}")
        js(f'tl.set("#{lid}", {{opacity: 1, scale: 1.45, rotation: -4}}, {t0:.3f});')
        js(f'tl.set("#{lid}", {{scale: 1.12, rotation: 2}}, {t0 + 1 / 15:.3f});')
        js(f'tl.set("#{lid}", {{scale: 1, rotation: 0}}, {t0 + 2 / 15:.3f});')
        ev(t0, "slam")
        for i, (w, t) in enumerate(words):
            if i:
                HIDE.append(f"#{lid}-w{i}")
                js(f'tl.set("#{lid}-w{i}", {{opacity: 1}}, {t:.3f});')
                ev(t, "tick")
        shake(f"#{lid}", t0 + 2 / 15, 4, 7)
        return lid
    if kind == "sm":
        inner = " ".join(f'<span class="w" id="{lid}-w{i}">{w}</span>' for i, (w, _) in enumerate(words))
        shot.head.append(f'<div class="ln sm" id="{lid}"{style}>{inner}</div>')
        for i, (w, t) in enumerate(words):
            HIDE.append(f"#{lid}-w{i}")
            js(f'tl.set("#{lid}-w{i}", {{opacity: 1, y: 14}}, {t:.3f});')
            js(f'tl.set("#{lid}-w{i}", {{y: 0}}, {t + 1 / 15:.3f});')
        return lid
    # big / red: pixel display face, letters scramble in
    parts = []
    for i, (w, t) in enumerate(words):
        chars = "".join(f'<span class="ch" id="{lid}-w{i}c{j}">{c}</span>' for j, c in enumerate(w))
        parts.append(f'<span class="w">{chars}</span>')
    shot.head.append(f'<div class="ln {kind}" id="{lid}"{style}>{" ".join(parts)}</div>')
    for i, (w, t) in enumerate(words):
        order = list(range(len(w)))
        R.shuffle(order)
        for k, j in enumerate(order):
            c = f"#{lid}-w{i}c{j}"
            HIDE.append(c)
            o = t + (k % 3) * F
            js(f'tl.set("{c}", {{opacity: 1, y: {R.choice([-16, 12, -8])}, x: {R.choice([-10, 8, 0])}}}, {o:.3f});')
            js(f'tl.set("{c}", {{y: 0, x: 0}}, {o + 2 * F:.3f});')
        ev(t, "pop")
    return lid


def shake(sel, t, n=6, amp=14):
    for k in range(n):
        a = amp * (1 - k / n)
        js(f'tl.set("{sel}", {{x: {R.uniform(-a, a):.1f}, y: {R.uniform(-a, a):.1f}}}, {t + k / 15:.3f});')
    js(f'tl.set("{sel}", {{x: 0, y: 0}}, {t + n / 15:.3f});')


def punch(shot, t, s=1.07):
    js(f'tl.set("#{shot.id}-rig", {{scale: {s}}}, {t:.3f});')
    js(f'tl.set("#{shot.id}-rig", {{scale: {1 + (s - 1) / 3:.3f}}}, {t + 1 / 15:.3f});')
    js(f'tl.set("#{shot.id}-rig", {{scale: 1}}, {t + 2 / 15:.3f});')
    ev(t, "thump")


SPARK = ('<svg viewBox="0 0 120 120" width="{w}" height="{w}"><g fill="{c}">'
         '<rect x="10" y="44" width="34" height="12" transform="rotate(-35 27 50)"/>'
         '<rect x="44" y="12" width="12" height="34" transform="rotate(10 50 29)"/>'
         '<rect x="70" y="30" width="34" height="12" transform="rotate(35 87 36)"/></g></svg>')


def spark(shot, x, y, t, t_end, rot=0, w=130, c=YEL):
    sid = f"{shot.id}-sp{len(shot.inner)}"
    shot.add(f'<div class="spark" id="{sid}" style="left:{x}px;top:{y}px">{SPARK.format(w=w, c=c)}</div>')
    HIDE.append("#" + sid)
    js(f'tl.set("#{sid}", {{opacity: 1, scale: .4, rotation: {rot}}}, {t:.3f});')
    js(f'tl.set("#{sid}", {{scale: 1.15}}, {t + 1 / 15:.3f});')
    k, tt = 0, t + 2 / 15
    while tt < t_end:
        js(f'tl.set("#{sid}", {{scale: {1 if k % 2 else 1.08}, rotation: {rot + (5 if k % 2 else -5)}}}, {tt:.3f});')
        tt += 2 / 15
        k += 1


def pop_in(sel, t, frm=1.4):
    HIDE.append(sel)
    js(f'tl.set("{sel}", {{opacity: 1, scale: {frm}}}, {t:.3f});')
    js(f'tl.set("{sel}", {{scale: {1 + (frm - 1) / 3:.3f}}}, {t + 1 / 15:.3f});')
    js(f'tl.set("{sel}", {{scale: 1}}, {t + 2 / 15:.3f});')


def flicker_in(sel, t):
    HIDE.append(sel)
    for k, o in enumerate([1, .2, .8, 1]):
        js(f'tl.set("{sel}", {{opacity: {o}}}, {t + k * F:.3f});')


def wiggle(sel, t0, t1, amp=4):
    k, tt = 0, t0
    while tt < t1:
        js(f'tl.set("{sel}", {{rotation: {amp if k % 2 else -amp}, y: {-6 if k % 2 else 0}}}, {tt:.3f});')
        tt += 2 / 15
        k += 1


GL = []


def glitch(t):
    """Two frames of torn horizontal bars and a jolt over a cut."""
    for f_ in range(2):
        bars = []
        for i in range(6):
            bars.append(dict(top=R.randint(0, 1880), h=R.choice([8, 16, 24, 40, 70]), x=R.randint(-80, 80),
                             c=R.choice([RED, CREAM, "#000", "#000", RED])))
        GL.append((t + f_ * F, bars))


# ---------------------------------------------------------------- shot list

def build():
    c = lambda i: round(t_(i) - .04, 3)

    # 1. HOOK at 70: dropped into a PS2 game on a CRT
    s = Shot("s1", 0, c(3), video=("gta-crt.mp4", 0.2), head_top=760, cut="none")
    line(s, "sm", [(W[i]["w"], t_(i)) for i in (0, 1, 2)], size=74)

    # 2. CLAUDE
    s = Shot("s2", c(3), c(6), "boy-at-pc", (1.42, 640, 380, 540, 1120), (1.58, 700, 360, 540, 1120))
    line(s, "big", [("CLAUDE", t_(3))], size=170)
    line(s, "sm", [(W[i]["w"], t_(i)) for i in (4, 5)], gap=6)
    spark(s, 770, 250, t_(3) + .1, c(6), rot=10)
    spark(s, 150, 300, t_(3) + .17, c(6), rot=-80)

    # 3. PS2 GAMES, the covers fanning in
    s = Shot("s3", c(6), c(8), "bg-ps2-desk", (1.3, 760, 640, 540, 1060), (1.42, 760, 640, 540, 1060))
    line(s, "big", [("PS2", t_(6)), ("GAMES", t_(7))], size=150)
    for k, (n, x, r) in enumerate([("god-hand", 130, -12), ("gta-vcs", 335, -4), ("resident-evil-4", 540, 4), ("god-of-war-2", 745, 12)]):
        sel = f"s3-cv{k}"
        s.add(f'<img class="cover" id="{sel}" src="assets/img/cover-{n}.png" style="left:{x - 100}px;top:1170px;transform:rotate({r}deg)" alt="">')
        t = t_(7) + k * 2 / 15
        HIDE.append("#" + sel)
        js(f'tl.set("#{sel}", {{opacity: 1, y: -120, rotation: {r}}}, {t:.3f});')
        js(f'tl.set("#{sel}", {{y: 14}}, {t + 1 / 15:.3f});')
        js(f'tl.set("#{sel}", {{y: 0}}, {t + 2 / 15:.3f});')
        ev(t, "tick")

    # 4. into PC GAMES: the monitor wakes with a game window
    s = Shot("s4", c(8), c(11), "pc-monitor-desk", (1.26, 825, 490, 540, 1130), (1.36, 825, 490, 540, 1130))
    line(s, "sm", [("into", t_(8))])
    line(s, "big", [("PC", t_(9)), ("GAMES", t_(10))], size=150)
    s.screen("monitor", '<div class="desk"></div><div class="win" id="s4-win" style="left:170px;top:50px;width:460px;height:380px">'
             '<div class="tb">GAME.EXE<i></i></div><img src="assets/img/cover-gta-vcs.png" style="width:100%;height:calc(100% - 44px);object-fit:cover" alt=""></div>',
             t_(9))
    pop_in("#s4-win", t_(10), 1.3)
    ev(t_(10), "tick")

    # 5. PEAK 1 (contrast): NOT AN EMULATOR
    s = Shot("s5", c(11), c(16), "disc-bell-jar", (1.5, 615, 820, 540, 1150), (1.68, 615, 840, 540, 1150))
    line(s, "sm", [(W[i]["w"], t_(i)) for i in (11, 12)])
    line(s, "lab", [("NOT", t_(13)), ("AN", t_(14)), ("EMULATOR", t_(15))], size=78, gap=18)
    s.add('<div class="xmark" id="s5-x"><i></i><i></i></div>')
    HIDE.append("#s5-x")
    js(f'tl.set("#s5-x", {{opacity: 1, scale: 1.8}}, {t_(15) + .1:.3f});')
    js(f'tl.set("#s5-x", {{scale: 1.15}}, {t_(15) + .1 + 1 / 15:.3f});')
    js(f'tl.set("#s5-x", {{scale: 1}}, {t_(15) + .1 + 2 / 15:.3f});')
    shake(f"#s5-rig", t_(15) + .1, 6, 22)
    punch(s, t_(15) + .1, 1.09)
    spark(s, 820, 520, t_(15) + .15, c(16), rot=20, c=YEL)
    spark(s, 120, 560, t_(15) + .2, c(16), rot=-70, c=YEL)

    # 6. it REBUILDS the actual game: MIPS to C++, code streaming out of the disc
    s = Shot("s6", c(16), c(21), "disc-case", (1.25, 950, 560, 540, 1060), (1.42, 960, 560, 540, 1060))
    line(s, "big", [("REBUILDS", t_(17))], size=150)
    line(s, "sm", [(W[i]["w"], t_(i)) for i in (18, 19, 20)])
    code = ["// MIPS R5900  ->  C++", "void func_001A2F80(R5900Context* ctx) {", "  ctx->r[4] = READ32(ctx->r[29] + 0x10);",
            "  sub_00124C10(ctx);", "  if (ctx->r[2] != 0) goto L_001A2FB4;", "  gs_draw_sprite(ctx, 0x3F);", "}", "// game.exe  BUILD OK"]
    rows = "".join(f'<div class="cl" id="s6-c{i}">{ln}</div>' for i, ln in enumerate(code))
    s.add(f'<div class="code" id="s6-code"><div class="ch2">PS2 CODE &gt; PC CODE</div>{rows}</div>')
    flicker_in("#s6-code", t_(17) + .05)
    for i in range(len(code)):
        t = t_(17) + .12 + i * .2
        HIDE.append(f"#s6-c{i}")
        js(f'tl.set("#s6-c{i}", {{opacity: 1}}, {t:.3f});')
        ev(t, "type")

    # 7. as a REAL PC PROGRAM: the laptop runs it
    s = Shot("s7", c(21), c(26), "laptop-desk", (1.22, 890, 430, 540, 1110), (1.34, 890, 430, 540, 1110))
    line(s, "sm", [(W[i]["w"], t_(i)) for i in (21, 22)])
    line(s, "lab", [("REAL", t_(23)), ("PC", t_(24)), ("PROGRAM", t_(25))], size=72, gap=10)
    s.screen("laptop", '<div class="desk"></div><div class="icon" id="s7-ico"><img src="assets/img/cover-god-hand.png" alt=""><b>GAME.EXE</b></div>'
             '<div class="win" id="s7-win" style="left:200px;top:40px;width:540px;height:400px"><div class="tb">GAME.EXE<i></i></div>'
             '<img src="assets/img/cover-god-hand.png" style="width:100%;height:calc(100% - 44px);object-fit:cover" alt=""></div>', t_(21) + .05)
    js(f'tl.set("#s7-ico", {{scale: 1.2}}, {t_(24):.3f});')
    js(f'tl.set("#s7-ico", {{scale: 1}}, {t_(24) + 2 / 15:.3f});')
    pop_in("#s7-win", t_(25), 1.35)
    spark(s, 850, 1270, t_(25) + .1, c(26), rot=30, w=110)

    # 8. it's called CONSOLE SKILL: the repo card drops into the spotlight
    s = Shot("s8", c(26), c(30), "bg-spotlight-room", (1.25, 512, 760, 540, 950), (1.3, 512, 760, 540, 950))
    line(s, "sm", [(W[i]["w"], t_(i)) for i in (26, 27)])
    line(s, "big", [("CONSOLE", t_(28))], size=160)
    line(s, "big", [("SKILL", t_(29))], size=160, color=RED)
    s.add('<div class="repo" id="s8-repo"><div class="rh"><span class="dot"></span>Jakeschincariol / <b>console-skill</b></div>'
          '<div class="rd">11 Claude skills that port PS2 games you own to PC</div><div class="rf"><span>MIT</span><span>PS2Recomp</span><span>github.com</span></div></div>')
    pop_in("#s8-repo", t_(28) + .1, 1.3)
    shake("#s8-repo", t_(29), 4, 8)
    spark(s, 860, 420, t_(29) + .05, c(30), rot=15)
    spark(s, 90, 470, t_(29) + .1, c(30), rot=-75)
    ev(t_(28) + .1, "slam")

    # 9. ELEVEN FREE Claude skills on GitHub: the skill list stacks up
    s = Shot("s9", c(30), c(36), "bg-desk-wide", (1.9, 768, 560, 540, 1000), (2.0, 768, 560, 540, 1000))
    nums = "".join(f'<span class="n" id="s9-n{k}">{k}</span>' for k in range(1, 12))
    s.add(f'<div class="count">{nums}</div>')
    for k in range(1, 12):
        t = t_(30) + (k - 1) * F * 1.5
        HIDE.append(f"#s9-n{k}")
        js(f'tl.set("#s9-n{k}", {{opacity: 1}}, {t:.3f});')
        if k < 11:
            js(f'tl.set("#s9-n{k}", {{opacity: 0}}, {t + F * 1.5:.3f});')
        ev(t, "blip") if k % 3 == 0 else None
    js(f'tl.set(".count", {{scale: 1.25}}, {t_(30) + 10 * F * 1.5:.3f});')
    js(f'tl.set(".count", {{scale: 1}}, {t_(30) + 10 * F * 1.5 + 2 / 15:.3f});')
    s.head_top = 640
    line(s, "lab", [("FREE", t_(31))], size=84)
    line(s, "sm", [(W[i]["w"], t_(i)) for i in (32, 33, 34, 35)], gap=8)
    skills = ["reverse", "backend", "graphics", "controller", "mod", "levels", "sound", "physics", "saves", "anywhere", "tester"]
    tags = "".join(f'<span class="tag" id="s9-t{i}">/console-{n}</span>' for i, n in enumerate(skills))
    s.add(f'<div class="tags">{tags}</div>')
    for i in range(len(skills)):
        t = t_(32) + i * .1
        pop_in(f"#s9-t{i}", t, 1.5)
        ev(t, "blip")

    # 10. for PS2 games YOU OWN: real hands on a real DualShock
    s = Shot("s10", c(36), c(41), video=("re4-monitor.mp4", 1.0), head_top=660)
    line(s, "sm", [("for", t_(36))])
    line(s, "lab", [("PS2", t_(37)), ("GAMES", t_(38)), ("YOU", t_(39)), ("OWN", t_(40))], size=60, gap=10)
    s.add('<div class="check" id="s10-ok"><svg viewBox="0 0 10 8" width="120" height="96"><path d="M0 4h2v1h1v1h1V5h1V4h1V3h1V2h1V1h1V0h1v2h-1v1H8v1H7v1H6v1H5v1H4v1H3V7H2V6H1V5H0z" fill="#140E0A"/></svg></div>')
    pop_in("#s10-ok", t_(40) + .05, 1.6)
    ev(t_(40) + .05, "check")

    # 11. PEAK 2: MOD IT just by asking, a chat on the phone
    s = Shot("s11", c(41), c(49), "phone-desk", (1.28, 790, 540, 540, 1150), (1.42, 790, 540, 540, 1150))
    line(s, "sm", [(W[i]["w"], t_(i)) for i in (41, 42, 43)])
    line(s, "big", [("MOD", t_(44)), ("IT", t_(45))], size=170, color=RED)
    line(s, "sm", [(W[i]["w"], t_(i)) for i in (46, 47, 48)])
    s.screen("phone", '<div class="chat"><div class="bub me" id="s11-b0">make the graphics sharper</div>'
             '<div class="bub me" id="s11-b1">and add a new level</div><div class="dots" id="s11-d"><i></i><i></i><i></i></div>'
             '<div class="bub ai" id="s11-b2">on it.</div></div>', t_(41) + .05, w=840, h=420)
    pop_in("#s11-b0", t_(44) + .05, 1.3); ev(t_(44) + .05, "msg")
    pop_in("#s11-b1", t_(46), 1.3); ev(t_(46), "msg")
    flicker_in("#s11-d", t_(47))
    js(f'tl.set("#s11-d", {{opacity: 0}}, {t_(48):.3f});')
    pop_in("#s11-b2", t_(48), 1.3); ev(t_(48), "msg")
    punch(s, t_(44))
    spark(s, 860, 440, t_(44) + .05, c(49), rot=20)

    # 12. SHARPER GRAPHICS: a cover un-pixelates
    s = Shot("s12", c(49), c(51), "bg-spotlight-room", (1.25, 512, 900, 540, 1100), (1.3, 512, 900, 540, 1100))
    line(s, "big", [("SHARPER", t_(49))], size=150)
    line(s, "lab", [("GRAPHICS", t_(50))], size=74, gap=8)
    imgs = "".join(f'<img id="s12-p{k}" src="assets/img/cover-gow2-{k}.png" alt="">' for k in range(4))
    s.add(f'<div class="bigcover">{imgs}</div>')
    for k, t in enumerate([c(49), t_(49) + .2, t_(50) - .02, t_(50) + .25]):
        HIDE.append(f"#s12-p{k}")
        js(f'tl.set("#s12-p{k}", {{opacity: 1}}, {t:.3f});')
        if k:
            js(f'tl.set("#s12-p{k - 1}", {{opacity: 0}}, {t:.3f});')
            ev(t, "blip")
    spark(s, 830, 900, t_(50) + .25, c(51), rot=25)

    # 13. NEW LEVELS: platforms build up step by step
    s = Shot("s13", c(51), c(53), "bg-spotlight-room", (1.25, 512, 760, 540, 900), (1.25, 512, 760, 540, 900))
    line(s, "big", [("NEW", t_(51))], size=150)
    line(s, "big", [("LEVELS", t_(52))], size=150, color=RED)
    for k, hgt in enumerate([1, 2, 3, 2, 4, 5]):
        sel = f"s13-b{k}"
        s.add(f'<div class="blk" id="{sel}" style="left:{90 + k * 150}px;top:{1480 - hgt * 90}px;height:{hgt * 90}px"></div>')
        pop_in("#" + sel, t_(51) + .08 + k * 2 / 15, 1.25)
        ev(t_(51) + .08 + k * 2 / 15, "blip")
    s.add('<div class="flag" id="s13-f"></div>')
    pop_in("#s13-f", t_(52) + .45, 1.5)

    # 14. your own CONTROLLER
    s = Shot("s14", c(53), c(56), "hands-controller", (1.5, 730, 470, 540, 1150), (1.68, 730, 450, 540, 1150))
    line(s, "sm", [(W[i]["w"], t_(i)) for i in (53, 54)])
    line(s, "big", [("CONTROLLER", t_(55))], size=136)
    punch(s, t_(55))
    spark(s, 820, 840, t_(55) + .05, c(56), rot=20)
    spark(s, 120, 880, t_(55) + .1, c(56), rot=-70)
    for k in range(4):
        js(f'tl.set("#s14-rig", {{y: {-10 if k % 2 else 6}}}, {t_(55) + .3 + k * .2:.3f});')

    # 15. GAME CRASHES? error windows on the CRT
    s = Shot("s15", c(56), c(58), "bg-crt-tv", (1.6, 640, 700, 540, 1130), (1.78, 640, 700, 540, 1130))
    line(s, "lab", [("GAME", t_(56)), ("CRASHES?", t_(57))], size=84)
    errs = "".join(f'<div class="err" data-layout-allow-overlap id="s15-e{k}" style="left:{30 + k * 70}px;top:{30 + k * 60}px"><div class="tb">ERROR<i></i></div>'
                   f'<div class="eb"><span class="ex">x</span>{m}</div></div>' for k, m in enumerate(["CRASH", "FATAL", "HALT"]))
    s.screen("crt", f'<div class="crtbg"></div>{errs}', c(56) + .02, w=520, h=440)
    for k in range(3):
        pop_in(f"#s15-e{k}", t_(57) + k * .1, 1.3)
        ev(t_(57) + k * .1, "err")
    shake("#s15-rig", t_(57) + .3, 6, 16)
    glitch(t_(57) + .35)

    # 16. the TESTER SKILL finds out WHY
    s = Shot("s16", c(58), c(64), "hand-magnifier", (1.3, 900, 420, 540, 1150), (1.45, 1040, 360, 540, 1150))
    line(s, "sm", [(W[i]["w"], t_(i)) for i in (58, 59, 60)])
    line(s, "big", [("FINDS", t_(61)), ("OUT", t_(62)), ("WHY", t_(63))], size=128)
    s.add('<div class="bug" id="s16-bug"></div>')
    pop_in("#s16-bug", t_(61), 1.6)
    wiggle("#s16-bug", t_(61) + .14, c(64), 8)
    ev(t_(61), "blip")
    s.add('<div class="solved" id="s16-ok"><svg viewBox="0 0 10 8" width="80" height="64"><path d="M0 4h2v1h1v1h1V5h1V4h1V3h1V2h1V1h1V0h1v2h-1v1H8v1H7v1H6v1H5v1H4v1H3V7H2V6H1V5H0z" fill="#140E0A"/></svg><b>SOLVED</b></div>')
    pop_in("#s16-ok", t_(63) + .1, 1.6)
    ev(t_(63) + .1, "check")
    spark(s, 830, 1290, t_(63) + .15, c(64), rot=25, w=110)

    # 17. then play it on WINDOWS, MAC, LINUX: three hard cuts
    s = Shot("s17a", c(64), c(69), "pc-monitor-desk", (1.3, 825, 490, 540, 1130), (1.4, 825, 490, 540, 1130))
    line(s, "sm", [(W[i]["w"], t_(i)) for i in (64, 65, 66, 67)])
    line(s, "big", [("WINDOWS", t_(68))], size=150)
    s.screen("monitor", '<div class="desk blue"></div><div class="win" style="left:150px;top:46px;width:500px;height:390px"><div class="tb">GAME.EXE<i></i></div>'
             '<img src="assets/img/cover-resident-evil-4.png" style="width:100%;height:calc(100% - 44px);object-fit:cover" alt=""></div>', t_(68) - .02)
    s = Shot("s17b", c(69), c(70), "laptop-desk", (1.45, 900, 430, 540, 1100), (1.55, 900, 430, 540, 1100), cut="hard")
    line(s, "big", [("MAC", t_(69))], size=170)
    s.screen("laptop", '<div class="desk black"></div><img src="assets/img/apple-white.png" style="position:absolute;left:330px;top:110px;width:220px" alt="">', c(69))
    s = Shot("s17c", c(70), c(71), "pc-monitor-desk", (1.42, 790, 480, 540, 1100), (1.5, 790, 480, 540, 1100), cut="hard")
    line(s, "big", [("LINUX", t_(70))], size=170)
    s.screen("monitor", '<div class="term"><div>$ ./game</div><div>loading assets...</div><div>ok<span class="cur" id="s17c-cur"></span></div></div>', c(70))
    for k in range(5):
        js(f'tl.set("#s17c-cur", {{opacity: {k % 2}}}, {c(70) + k * .16:.3f});')

    # 18. PEAK 3: even a STEAM DECK
    s = Shot("s18", c(71), c(75), "handheld-hands", (1.18, 850, 460, 540, 1150), (1.3, 850, 460, 540, 1150))
    line(s, "sm", [(W[i]["w"], t_(i)) for i in (71, 72)])
    line(s, "big", [("STEAM", t_(73)), ("DECK", t_(74))], size=136, color=RED)
    s.screen("handheld", '<div class="desk black"></div><img src="assets/img/deck-logo.png" id="s18-logo" style="position:absolute;left:300px;top:130px;width:220px" alt="">'
             '<img src="assets/img/cover-god-of-war-2.png" id="s18-game" style="position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover" alt="">', c(71) + .05)
    flicker_in("#s18-game", t_(74) + .05)
    punch(s, t_(74), 1.1)
    shake("#s18-rig", t_(74) + .14, 5, 14)
    spark(s, 860, 470, t_(74) + .05, c(75), rot=15)
    spark(s, 90, 470, t_(74) + .1, c(75), rot=-75)

    # 19. release: it's still EARLY
    s = Shot("s19", c(75), c(78), "hourglass", (1.55, 660, 640, 540, 1170), (1.7, 660, 640, 540, 1170))
    line(s, "sm", [(W[i]["w"], t_(i)) for i in (75, 76)])
    line(s, "lab", [("EARLY", t_(77))], size=84, gap=10)

    # 20. so not every game BOOTS YET: a progress bar stuck at 99%
    s = Shot("s20", c(78), c(84), "calendar-pages", (1.45, 820, 430, 540, 1060), (1.58, 860, 420, 540, 1060))
    line(s, "sm", [(W[i]["w"], t_(i)) for i in (78, 79, 80, 81)])
    line(s, "big", [("BOOTS", t_(82)), ("YET", t_(83))], size=150)
    segs = "".join(f'<i id="s20-g{k}"></i>' for k in range(20))
    s.add(f'<div class="bar"><div class="bt" id="s20-pct">0%</div><div class="bs">{segs}</div></div>')
    for k in range(19):
        t = c(78) + .15 + k * .07
        HIDE.append(f"#s20-g{k}")
        js(f'tl.set("#s20-g{k}", {{opacity: 1}}, {t:.3f});')
        if k % 3 == 0:
            ev(t, "blip")
    js(f'tl.set("#s20-pct", {{opacity: 1}}, {c(78):.3f});')
    pct = "".join(f'<span class="pv" id="s20-v{k}">{v}%</span>' for k, v in enumerate([12, 37, 64, 88, 99]))
    s.inner[-1] = s.inner[-1].replace('<div class="bt" id="s20-pct">0%</div>', f'<div class="bt" id="s20-pct">{pct}</div>')
    for k in range(5):
        t = c(78) + .15 + k * .27
        HIDE.append(f"#s20-v{k}")
        js(f'tl.set("#s20-v{k}", {{opacity: 1}}, {t:.3f});')
        if k < 4:
            js(f'tl.set("#s20-v{k}", {{opacity: 0}}, {t + .27:.3f});')
    tt, k = c(78) + 1.5, 0
    while tt < c(84):
        js(f'tl.set("#s20-v4", {{opacity: {1 if k % 2 else .25}}}, {tt:.3f});')
        tt += 2 / 15
        k += 1
    shake("#s20-rig", t_(83), 4, 10)

    # 21. CTA: Comment "CONSOLE"
    s = Shot("s21", c(84), DUR, "boy-trophy", (1.22, 512, 700, 540, 1110), (1.3, 512, 700, 540, 1110), head_top=980)
    line(s, "big", [("COMMENT", t_(84))], size=128)
    line(s, "red", [('"CONSOLE"', t_(85))], size=150)
    line(s, "sm", [(W[i]["w"], t_(i)) for i in (86, 87, 88, 89, 90, 91, 92, 93, 94)], size=46, gap=12)
    s.add('<img class="wm" id="s21-wm" src="assets/img/wordmark.png" alt="AI.NXTLVL">')
    flicker_in("#s21-wm", t_(84) + .2)
    for k, (x, y, r, sc) in enumerate([(-40, 1330, -25, .3), (60, 1530, -10, .26), (830, 1330, 25, .3), (740, 1530, 10, .26), (330, 1610, -4, .22), (560, 1615, 6, .22)]):
        sel = f"s21-c{k}"
        flip = " scaleX(-1)" if x > 500 else ""
        s.add(f'<div class="clapw" id="{sel}" style="left:{x}px;top:{y}px;width:{733 * sc:.0f}px"><img src="assets/img/clap.png" style="width:100%;transform:rotate({r}deg){flip}" alt=""></div>')
        pop_in("#" + sel, t_(85) + k * 2 / 15, 1.4)
        wiggle("#" + sel, t_(85) + k * 2 / 15 + .14, DUR, 7)
    rng = random.Random(4)
    for k in range(34):
        sel = f"s21-cf{k}"
        x, y0, sz = rng.randint(40, 1040), rng.randint(-300, 200), rng.choice([14, 18, 22])
        col = rng.choice([RED, YEL, CREAM, RED])
        s.add(f'<div class="cf" id="{sel}" style="left:{x}px;top:{y0}px;width:{sz}px;height:{sz}px;background:{col}"></div>')
        t0 = t_(84) + rng.uniform(0, .6)
        HIDE.append("#" + sel)
        js(f'tl.set("#{sel}", {{opacity: 1}}, {t0:.3f});')
        js(f'tl.to("#{sel}", {{y: {rng.randint(1300, 1900)}, x: {rng.randint(-120, 120)}, rotation: {rng.choice([-180, 180, 360])}, '
           f'duration: {DUR - t0:.3f}, ease: {steps(DUR - t0)}}}, {t0:.3f});')
    ev(t_(85), "clap")


CSS = f"""
@font-face {{ font-family: "Pixelify"; font-weight: 700; src: url("assets/fonts/PixelifySans-Bold.ttf"); }}
@font-face {{ font-family: "Silk"; font-weight: 700; src: url("assets/fonts/Silkscreen-Bold.ttf"); }}
@font-face {{ font-family: "Silk"; font-weight: 400; src: url("assets/fonts/Silkscreen-Regular.ttf"); }}
@font-face {{ font-family: "Rubik"; font-weight: 900; src: url("assets/fonts/Rubik-Black.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {INK}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: {INK}; }}
.vwrap {{ position: absolute; inset: 0; overflow: hidden; }}
.vwrap video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; filter: contrast(1.1) saturate(.82) sepia(.22) brightness(.92); }}
.shot {{ position: absolute; inset: 0; overflow: hidden; }}
.rig {{ position: absolute; inset: 0; transform-origin: 540px 1000px; }}
.bgi {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
.cam {{ position: absolute; left: 0; top: 0; transform-origin: 0 0;
  -webkit-mask-image: linear-gradient(180deg, transparent 0, #000 9%, #000 91%, transparent 100%);
          mask-image: linear-gradient(180deg, transparent 0, #000 9%, #000 91%, transparent 100%); }}
.art {{ position: absolute; left: 0; top: 0; image-rendering: pixelated; }}
.scr {{ position: absolute; left: 0; top: 0; transform-origin: 0 0; overflow: hidden; background: #0b0c14; }}
.head {{ position: absolute; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center; z-index: 8; }}
.ln {{ line-height: 1; }}
.sm {{ font: 900 62px/1.05 "Rubik"; color: {CREAM}; letter-spacing: -1px; text-transform: lowercase; text-shadow: 0 6px 0 #000, 0 0 24px rgba(0,0,0,.75); }}
.big, .red {{ font: 700 140px/0.95 "Pixelify"; color: {CREAM}; text-transform: uppercase; white-space: nowrap;
  text-shadow: 7px 7px 0 #000, 0 0 30px rgba(0,0,0,.7); }}
.red {{ color: {RED}; }}
.ch {{ display: inline-block; }}
.w {{ display: inline-block; }}
.lab {{ font: 700 70px/1 "Silk"; color: #fff; text-transform: uppercase; }}
.lab .lb {{ display: inline-block; background: {RED}; padding: 12px 30px 16px; transform: skewX(-9deg); box-shadow: 8px 8px 0 #000; }}
.lab .lt {{ display: inline-block; transform: skewX(9deg); white-space: nowrap; }}
.spark {{ position: absolute; z-index: 6; }}
.cover {{ position: absolute; width: 200px; height: 282px; border: 5px solid {CREAM}; box-shadow: 8px 10px 0 #000; image-rendering: pixelated; }}
.desk {{ position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 40%, #2b3a6e 0, #141a33 60%, #0a0c18 100%); }}
.desk.blue {{ background: linear-gradient(160deg, #1f5fbf 0, #0e2f78 60%, #08174a 100%); }}
.desk.black {{ background: #050507; }}
.win {{ position: absolute; background: #111; border: 4px solid {CREAM}; box-shadow: 10px 10px 0 rgba(0,0,0,.6); overflow: hidden; }}
.win .tb, .err .tb {{ height: 44px; background: {CREAM}; color: {INK}; font: 700 26px/44px "Silk"; padding-left: 14px; position: relative; }}
.win .tb i, .err .tb i {{ position: absolute; right: 10px; top: 10px; width: 24px; height: 24px; background: {RED}; }}
.icon {{ position: absolute; left: 60px; top: 60px; width: 150px; text-align: center; color: #fff; font: 700 22px "Silk"; }}
.icon img {{ width: 110px; height: 150px; object-fit: cover; border: 3px solid #fff; display: block; margin: 0 auto 8px; }}
.code {{ position: absolute; left: 60px; right: 60px; top: 1170px; padding: 22px 26px; background: rgba(10,7,5,.88); border: 4px solid {CREAM};
  box-shadow: 10px 10px 0 #000; font: 400 25px/1.55 "Silk"; color: {CREAM}; white-space: nowrap; overflow: hidden; }}
.code .ch2 {{ display: inline-block; background: {RED}; color: #fff; font: 700 26px/1 "Silk"; padding: 8px 14px; margin-bottom: 10px; }}
.code .cl:first-of-type {{ color: {YEL}; }}
.code .cl:last-child {{ color: {YEL}; }}
.repo {{ position: absolute; left: 70px; right: 70px; top: 1060px; padding: 30px 34px; background: #0f1217; border: 4px solid {CREAM}; box-shadow: 12px 12px 0 #000; color: {CREAM}; }}
.repo .rh {{ font: 400 34px/1.2 "Silk"; color: #c9d1d9; }}
.repo .rh b {{ font-weight: 700; color: #fff; }}
.repo .dot {{ display: inline-block; width: 26px; height: 26px; background: {RED}; margin-right: 14px; vertical-align: -3px; }}
.repo .rd {{ margin-top: 18px; font: 900 40px/1.15 "Rubik"; color: {CREAM}; }}
.repo .rf {{ margin-top: 20px; display: flex; gap: 14px; }}
.repo .rf span {{ font: 700 24px/1 "Silk"; padding: 8px 12px; border: 3px solid {YEL}; color: {YEL}; }}
.count {{ position: absolute; left: 0; right: 0; top: 250px; height: 380px; text-align: center; }}
.count .n {{ position: absolute; left: 0; right: 0; font: 700 380px/1 "Pixelify"; color: {CREAM}; text-shadow: 12px 12px 0 #000; }}
.tags {{ position: absolute; left: 60px; right: 60px; top: 1010px; display: flex; flex-wrap: wrap; justify-content: center; gap: 14px; }}
.tag {{ font: 700 31px/1 "Silk"; color: {INK}; background: {CREAM}; padding: 12px 16px; box-shadow: 6px 6px 0 #000; }}
.tag:nth-child(3n+2) {{ background: {RED}; color: #fff; }}
.check {{ position: absolute; left: 470px; top: 1060px; width: 160px; height: 160px; background: {YEL}; display: flex; align-items: center; justify-content: center; box-shadow: 8px 8px 0 #000; transform-origin: 50% 50%; }}
.chat {{ position: absolute; inset: 0; background: #101114; padding: 30px 40px; display: flex; flex-direction: column; gap: 18px; }}
.bub {{ font: 900 38px/1.1 "Rubik"; padding: 16px 24px; max-width: 75%; box-shadow: 6px 6px 0 #000; }}
.bub.me {{ align-self: flex-end; background: {YEL}; color: {INK}; }}
.bub.ai {{ align-self: flex-start; background: {CREAM}; color: {INK}; }}
.dots {{ align-self: flex-start; display: flex; gap: 10px; padding: 16px 22px; background: #2a2b30; }}
.dots i {{ width: 16px; height: 16px; background: {CREAM}; display: block; }}
.bigcover {{ position: absolute; left: 290px; top: 1000px; width: 500px; height: 687px; border: 6px solid {CREAM}; box-shadow: 14px 14px 0 #000; }}
.bigcover img {{ position: absolute; inset: 0; width: 100%; height: 100%; image-rendering: pixelated; }}
#s12-p3 {{ image-rendering: auto; }}
.blk {{ position: absolute; width: 150px; background: repeating-linear-gradient(180deg, {RED} 0 16px, #8f1a12 16px 18px, {RED} 18px 90px),
  linear-gradient(90deg, rgba(0,0,0,0) 0 92%, rgba(0,0,0,.35) 92%); border: 4px solid #000; border-top: 16px solid {CREAM}; }}
.flag {{ position: absolute; left: 870px; top: 900px; width: 12px; height: 140px; background: {CREAM}; }}
.flag::after {{ content: ""; position: absolute; left: 12px; top: 0; width: 70px; height: 46px; background: {YEL}; }}
.xmark {{ position: absolute; left: 340px; top: 950px; width: 400px; height: 400px; transform-origin: 50% 50%; }}
.xmark i {{ position: absolute; left: -20px; top: 168px; width: 440px; height: 64px; background: {RED}; box-shadow: 8px 8px 0 #000; transform: rotate(45deg); }}
.xmark i + i {{ transform: rotate(-45deg); }}
.crtbg {{ position: absolute; inset: 0; background: #1d2a8c; }}
.err {{ position: absolute; width: 300px; background: #c9c4b4; border: 4px solid #000; box-shadow: 8px 8px 0 #000; }}
.err .eb {{ padding: 18px 14px; font: 700 34px/1 "Silk"; color: {INK}; display: flex; align-items: center; gap: 14px; }}
.err .ex {{ display: inline-block; width: 44px; height: 44px; background: {RED}; color: #fff; font: 700 34px/40px "Silk"; text-align: center; }}
.bug {{ position: absolute; left: 500px; top: 1040px; width: 120px; height: 100px; transform-origin: 50% 50%;
  background: conic-gradient(from 0deg, {RED} 0 100%); clip-path: polygon(30% 0,70% 0,70% 15%,85% 15%,85% 35%,100% 35%,100% 50%,85% 50%,85% 70%,100% 70%,100% 85%,85% 85%,85% 100%,15% 100%,15% 85%,0 85%,0 70%,15% 70%,15% 50%,0 50%,0 35%,15% 35%,15% 15%,30% 15%); }}
.solved {{ position: absolute; left: 300px; top: 1290px; width: 480px; height: 210px; background: {YEL}; border: 6px solid #000; box-shadow: 12px 12px 0 #000;
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px; transform-origin: 50% 50%; }}
.solved b {{ font: 700 64px/1 "Silk"; color: {INK}; }}
.term {{ position: absolute; inset: 0; background: #050806; padding: 40px 46px; font: 400 44px/1.5 "Silk"; color: #4BE36B; }}
.cur {{ display: inline-block; width: 26px; height: 44px; background: #4BE36B; vertical-align: -6px; margin-left: 10px; }}
.bar {{ position: absolute; left: 140px; right: 140px; top: 1230px; }}
.bar .bt {{ position: relative; height: 80px; font: 700 80px/1 "Pixelify"; color: {CREAM}; text-align: center; text-shadow: 6px 6px 0 #000; }}
.bar .pv {{ position: absolute; left: 0; right: 0; }}
.bar .bs {{ margin-top: 14px; height: 70px; border: 6px solid {CREAM}; background: rgba(0,0,0,.7); padding: 6px; display: flex; gap: 5px; box-shadow: 8px 8px 0 #000; }}
.bar .bs i {{ flex: 1; background: {RED}; }}
.wm {{ position: absolute; left: 740px; top: 268px; width: 260px; filter: drop-shadow(0 4px 0 #000); }}
.clapw {{ position: absolute; z-index: 6; }}
.clapw img {{ display: block; image-rendering: pixelated; }}
.cf {{ position: absolute; z-index: 4; box-shadow: 3px 3px 0 rgba(0,0,0,.5); }}
#glitch {{ position: absolute; inset: 0; z-index: 30; pointer-events: none; }}
#glitch b {{ position: absolute; left: 0; width: 1080px; display: block; }}
#grain {{ position: absolute; left: -60px; top: -60px; width: 1200px; height: 2133px; z-index: 20; image-rendering: pixelated; mix-blend-mode: overlay; }}
#vig {{ position: absolute; inset: 0; z-index: 19; }}
"""


def main():
    build()
    # grain: one pixel-noise layer jumped to a new offset on every step (15 fps); swapping its src overflows the runtime
    gid = 0
    t = 0.0
    k = 0
    while t < DUR:
        js(f'tl.set("#grain", {{x: {R.randint(-28, 28) * 2}, y: {R.randint(-28, 28) * 2}}}, {t:.3f});')
        t += 1 / FPS
        k += 1
    # glitch bars
    nb = 6
    bars = "".join(f'<b id="gb{i}"></b>' for i in range(nb))
    for t, bs in sorted(GL):
        for i, b in enumerate(bs):
            js(f'tl.set("#gb{i}", {{opacity: 1, y: {b["top"]}, x: {b["x"]}, height: {b["h"]}, backgroundColor: "{b["c"]}"}}, {t:.3f});')
        js(f'tl.set("#glitch b", {{opacity: 0}}, {t + F:.3f});')
    HIDE.append("#glitch b")
    A.insert(0, "      gsap.set(" + json.dumps(list(dict.fromkeys(HIDE))) + ", {opacity: 0});")
    has_mix = os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav"))
    audio = f'<audio id="mix" src="assets/audio/{"mix" if has_mix else "voice"}.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>'
    shots = "\n      ".join(s.html() for s in SHOTS)
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Console skill 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      {chr(10).join("      " + v for v in VIDEOS).strip()}
      {shots}
      <div id="fx" class="clip" data-start="0" data-duration="{DUR}" data-track-index="8"><img id="vig" src="assets/img/vignette.png" alt=""><img id="grain" src="assets/img/grain-0.png" alt=""><div id="glitch">{bars}</div></div>
      {audio}
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
    json.dump({"dur": DUR, "cuts": CUTS, "ev": sorted(EV)}, open(os.path.join(B, "cues.json"), "w"), indent=0)
    print(f"wrote index.html {len(html) // 1024} KB, {len(SHOTS)} shots, {len(A)} timeline lines, {len(EV)} sound events, audio: {'mix' if has_mix else 'voice'}")


if __name__ == "__main__":
    main()
