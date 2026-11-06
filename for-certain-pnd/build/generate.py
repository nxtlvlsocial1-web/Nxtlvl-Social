"""For Certain (PARTYNEXTDOOR): the first minute as a storybook-collage lyric edit, 3:4 (1080x1440). Writes index.html.

Modelled on the owner's reference (reference/ref_edit.mp4, see plan/PLAN.md):
- One object per line that acts the line out, on painterly night-blue and amber worlds (the owner's ChatGPT
  illustrations in assets/img/gen, not in git).
- Small white caps set up each line; one big rose-red keyword lands on its beat.
- Smooth 30 fps motion. The camera always pushes in slowly.
- Portal zooms: the camera dives through a circle in the current world (the moon, a record label, a phone, a pupil,
  a ring, the sun, a lens, a glass rim) into the next.
- Whips, flashes and blur dissolves for the other cuts.
- The drop at 20.63 s bursts in on the first 808.
- Ends on the nxtlvl logo (dark violet) with the song fading across it.
Line timings are estimates from the vocal band (plan/PLAN.md section 5).

python3 build/generate.py
"""
import json
import math
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FW, FH, FPS = 1080, 1440, 30
SONG_END = 61.91
DUR = 63.6
BOX = json.load(open(os.path.join(ROOT, "plan", "bboxes.json")))
G = "assets/img/gen/"
A, HIDE, SCN, CUES = [], [], [], []      # CUES: (time, kind) for build/sfx_sheet.py
NID = [0]
R = random.Random(7)
BG_S = 1080 / 1024                     # background images cover the frame: 1024x1536 -> 1080x1620, 90 px cropped top and bottom


def js(s):
    A.append("      " + s)


def nid(p):
    NID[0] += 1
    return f"{p}{NID[0]}"


def bgpt(x, y):
    """A point in a 1024x1536 background image -> frame coordinates."""
    return x * BG_S, y * BG_S - 90


# ------------------------------------------------------------------------------------------------ scene timeline
# (name, start, end, background, transition into the NEXT scene, portal point in frame px or None)
SC = [
    ("party", 0.00, 3.25, "b1_party", "whipup", None),
    ("moon", 3.25, 5.20, "b2_moon", "portal", bgpt(571, 657)),
    ("vinyl", 5.20, 7.45, "b5_dancefloor", "portal", (540, 735)),
    ("phone", 7.45, 10.85, "b6_rain", "portal", (540, 760)),
    ("eye", 10.85, 14.00, "f1_eye", "portal", bgpt(524, 746)),
    ("heart", 14.00, 20.63, "b3_swirl", "drop", (540, 760)),
    ("ring", 20.63, 23.21, "b7_stage", "portal", (540, 880)),
    ("globe", 23.21, 25.79, "b4_sunset", "portal", bgpt(505, 723)),
    ("badman", 25.79, 28.37, "b5_dancefloor", "whipl", None),
    ("birkin", 28.37, 30.95, "b7_stage", "whipr", None),
    ("certain", 30.95, 33.00, "b2_moon", "dissolve", None),
    ("search", 33.00, 34.75, "b1_party", "portal", (470, 560)),
    ("woah", 34.75, 36.40, "b3_swirl", "flash", None),
    ("want", 36.40, 41.27, "b9_wall", "vhs", None),
    ("tried", 41.27, 42.85, "b1_party", "whipl", None),
    ("pride", 42.85, 45.40, "b2_moon", "flash", None),
    ("fortytwo", 45.40, 47.65, "b8_bar", "portal", (540, 760)),
    ("neon", 47.65, 50.40, "b9_wall", "whipr", None),
    ("dance", 50.40, 53.70, "b5_dancefloor", "dissolve", None),
    ("know", 53.70, 55.45, "c6_couple_laugh", "dissolve", None),
    ("need", 55.45, 58.90, "b6_rain", "whipdown", None),
    ("pressure", 58.90, SONG_END, "b7_stage", "logo", (540, 720)),
]
IDX = {s[0]: k for k, s in enumerate(SC)}
EL = {s[0]: [] for s in SC}            # html inside each scene's camera


def put(scene, html):
    EL[scene].append(html)


def obj(scene, name, cx, cy, h, t0, z=4, rot=0, cls="obj", enter="rise", d=.7, extra="", idle=True):
    """Place a cut-out so its visible bounding box is centred on (cx, cy) and h px tall; it rises out of a blur."""
    x0, y0, x1, y1 = BOX[name]
    s = h / (y1 - y0)
    w = 1024 * s
    left = cx - ((x0 + x1) / 2) * s
    top = cy - ((y0 + y1) / 2) * s
    i = nid("o")
    put(scene, f'<div class="{cls}" id="{i}" style="left:{left:.0f}px;top:{top:.0f}px;width:{w:.0f}px;height:{1536 * s:.0f}px;'
               f'z-index:{z};transform:rotate({rot}deg)"><img src="{G}{name}.png" alt="">{extra}</div>')
    if enter == "rise":
        js(f'tl.fromTo("#{i}", {{opacity: 0, y: 120, scale: .86, filter: "blur(18px)"}}, {{opacity: 1, y: 0, scale: 1, filter: "blur(0px)", '
           f'duration: {d}, ease: "expo.out", immediateRender: false}}, {t0:.3f});')
    elif enter == "pop":
        js(f'tl.fromTo("#{i}", {{opacity: 0, scale: .2, rotation: {rot - 25}}}, {{opacity: 1, scale: 1, rotation: {rot}, '
           f'duration: {d}, ease: "back.out(1.9)", immediateRender: false}}, {t0:.3f});')
    elif enter == "none":
        js(f'tl.set("#{i}", {{opacity: 1}}, {t0:.3f});')
    HIDE.append(f"#{i}")
    if idle:
        js(f'tl.to("#{i} > img", {{y: -14, duration: 1.6, ease: "sine.inOut", yoyo: true, repeat: 7}}, {t0 + d:.3f});')
    return i, left, top, s


def text(scene, small, big, ts, tb, y, size=170, red=True, align="center", x=None, script=False, t1=None):
    """Small white caps that stream in, then the big keyword that slams on its beat."""
    i = nid("t")
    xs = f"left:{x}px;" if x is not None else "left:0;width:1080px;"
    letters = "".join(f'<span>{c if c != " " else "&nbsp;"}</span>' for c in small)
    put(scene, f'<div class="txt" id="{i}" style="top:{y}px;{xs}text-align:{align}">'
               + (f'<div class="sm">{letters}</div>' if small else "")
               + (f'<div class="bg{" red" if red else ""}{" scr" if script else ""}" style="font-size:{size}px">{big}</div>' if big else "")
               + "</div>")
    HIDE.append(f"#{i}")
    js(f'tl.set("#{i}", {{opacity: 1}}, {min(ts, tb) - .01:.3f});')
    if small:
        js(f'tl.fromTo("#{i} .sm span", {{opacity: 0, y: 26, filter: "blur(10px)"}}, {{opacity: 1, y: 0, filter: "blur(0px)", duration: .35, '
           f'ease: "power3.out", stagger: {min(.025, .45 / max(1, len(small))):.3f}, immediateRender: false}}, {ts:.3f});')
    if big:
        js(f'tl.set("#{i} .bg", {{opacity: 0}}, {min(ts, tb) - .01:.3f});')
        js(f'tl.fromTo("#{i} .bg", {{opacity: 0, scale: 1.45, filter: "blur(16px)"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", '
           f'duration: .32, ease: "expo.out", immediateRender: false}}, {tb:.3f});')
        js(f'tl.fromTo("#c{IDX[scene]}", {{x: 0, y: 0}}, {{keyframes: [{{x: -9, y: 5, duration: .04}}, {{x: 7, y: -4, duration: .04}}, '
           f'{{x: -3, y: 2, duration: .04}}, {{x: 0, y: 0, duration: .05}}], immediateRender: false}}, {tb:.3f});')
    if t1:                                     # leaves before the next line arrives
        js(f'tl.to("#{i}", {{opacity: 0, filter: "blur(12px)", y: -30, duration: .22, ease: "power2.in"}}, {t1 - .22:.3f});')
    return i


def glow(scene, x, y, r, color, t0, t1=None, op=.8, z=3):
    i = nid("gl")
    put(scene, f'<i class="glow" id="{i}" style="left:{x - r}px;top:{y - r}px;width:{2 * r}px;height:{2 * r}px;z-index:{z};'
               f'background:radial-gradient(circle, {color} 0%, rgba(0,0,0,0) 68%)"></i>')
    HIDE.append(f"#{i}")
    js(f'tl.fromTo("#{i}", {{opacity: 0, scale: .4}}, {{opacity: {op}, scale: 1, duration: .5, ease: "power2.out", immediateRender: false}}, {t0:.3f});')
    return i


def char(scene, name, cx, base, h, t0, z=5, flip=False, d=.8, idle=True):
    i, *_ = obj(scene, name, cx, base - h / 2, h, t0, z=z, d=d, idle=idle)
    if flip:
        js(f'tl.set("#{i} > img", {{scaleX: -1}}, 0);')
    return i


# ------------------------------------------------------------------------------------------------ the scenes
def scenes():
    # 1. We didn't vibe on the first night: the party seen from the doorway, her looking back
    char("party", "c3_her_turn", 820, 1430, 900, .35, z=5, flip=True)
    text("party", "WE DIDN'T VIBE ON THE", "FIRST NIGHT", .9, 2.55, 150, 150)
    # 2. But you're so enticin': the perfume over the moon, mist on the word
    i, l, t, s = obj("moon", "o1_perfume", 540, 1040, 560, 3.3)
    mist = "".join(f'<i class="mist" style="left:{460 + R.uniform(-30, 30):.0f}px;top:{720 + R.uniform(-20, 20):.0f}px"></i>' for _ in range(14))
    put("moon", f'<div class="mistw" id="mist">{mist}</div>')
    HIDE.append("#mist")
    js('tl.set("#mist", {opacity: 1}, 4.35);')
    CUES.append((4.35, "spray"))
    js('tl.fromTo("#mist .mist", {opacity: .9, x: 0, y: 0, scale: .3}, {opacity: 0, x: (k) => -260 + (k % 7) * 80, y: (k) => -320 + (k % 5) * 50, '
       'scale: 2.6, duration: 1.1, ease: "power2.out", stagger: .025, immediateRender: false}, 4.35);')
    text("moon", "BUT YOU'RE SO", "ENTICIN'", 3.45, 4.35, 150, 180)
    # 3. We didn't vibe then: the record spins and scratches to a stop on THEN
    i, *_ = obj("vinyl", "o2_vinyl", 540, 735, 640, 5.22, idle=False, d=.55)
    js(f'tl.fromTo("#{i} > img", {{rotation: 0}}, {{rotation: 300, duration: 1.66, ease: "none", immediateRender: false}}, 5.22);')
    js(f'tl.to("#{i} > img", {{rotation: 262, duration: .14, ease: "power2.out"}}, 6.88);')        # the scratch: back, then dead
    CUES.append((6.88, "scratch"))
    js(f'tl.to("#{i} > img", {{rotation: 268, duration: .3, ease: "power3.out"}}, 7.02);')
    text("vinyl", "WE DIDN'T VIBE", "THEN", 5.3, 6.88, 1120, 200)
    # 4. But now I want you: her name lights the phone
    i, l, t, s = obj("phone", "o3_phone", 540, 760, 1080, 7.48, d=.6, idle=False)
    scr = (f'<div class="pscr" style="left:{172 * s:.0f}px;top:{86 * s:.0f}px;width:{(852 - 172) * s:.0f}px;height:{(1456 - 86) * s:.0f}px">'
           '<div class="ring1"></div><div class="ring2"></div><div class="who">her</div><div class="call">calling...</div></div>')
    put("phone", f'<div id="pwrap" style="position:absolute;left:{l:.0f}px;top:{t:.0f}px;width:{1024 * s:.0f}px;height:{1536 * s:.0f}px;z-index:5">{scr}</div>')
    HIDE.append("#pwrap")
    js('tl.fromTo("#pwrap", {opacity: 0}, {opacity: 1, duration: .25, immediateRender: false}, 8.1);')
    js('tl.fromTo("#pwrap .ring1, #pwrap .ring2", {scale: .4, opacity: .9}, {scale: 2.2, opacity: 0, duration: 1.1, ease: "power2.out", '
       'stagger: .35, repeat: 2, immediateRender: false}, 8.2);')
    text("phone", "BUT", "NOW", 7.5, 8.15, 140, 230)
    text("phone", "", "I WANT YOU", 8.75, 8.75, 1180, 150, red=False)
    # 5. So, I-I-I, pure desire: the eye, the I stutters with his voice, flames in the iris
    px, py = bgpt(524, 746)
    glow("eye", px, py, 260, "rgba(255,90,40,.75)", 13.3, op=.85, z=2)
    i = nid("t")
    segs = "".join(f'<span class="iseg">{w}</span>' for w in ["I-", "I-", "I,"])
    put("eye", f'<div class="txt" id="{i}" style="top:230px;left:0;width:1080px;text-align:center"><div class="bg red" style="font-size:230px">{segs}</div></div>')
    HIDE.append(f"#{i}")
    js(f'tl.set("#{i}", {{opacity: 1}}, 11.9);')
    for k, tk in enumerate([11.95, 12.3, 12.62]):
        js(f'tl.fromTo("#{i} .iseg:nth-child({k + 1})", {{opacity: 0, scale: 1.7, filter: "blur(12px)"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", '
           f'duration: .2, ease: "expo.out", immediateRender: false}}, {tk:.3f});')
    js(f'tl.to("#{i}", {{opacity: 0, filter: "blur(12px)", duration: .22}}, 12.88);')
    text("eye", "SO,", "", 11.75, 11.75, 150, 0)
    text("eye", "PURE", "DESIRE", 12.95, 13.35, 1110, 210)
    # 6. Heart racin': the heart beats on the syllables, an ECG races, AH-OOH-AH echoes, then the long push
    i, *_ = obj("heart", "o4_heart", 540, 760, 700, 14.05, idle=False, d=.6)
    t, beat = 14.55, .42
    while t < 20.4:
        js(f'tl.fromTo("#{i} > img", {{scale: 1}}, {{keyframes: [{{scale: 1.09, duration: .06}}, {{scale: 1, duration: .16}}], ease: "power2.out", immediateRender: false}}, {t:.3f});')
        beat = max(.2, beat * .965)
        t += beat
    put("heart", '<svg id="ecg" class="ecg" viewBox="0 0 1080 200" width="1080" height="200"><path pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" '
                 'd="M0 120 H260 L290 120 L310 60 L330 180 L350 20 L372 150 L392 120 H560 L590 120 L610 60 L630 180 L650 20 L672 150 L692 120 H1080"/></svg>')
    HIDE.append("#ecg")
    js('tl.set("#ecg", {opacity: 1}, 15.0);')
    js('tl.fromTo("#ecg path", {strokeDashoffset: 1}, {strokeDashoffset: 0, duration: 1.4, ease: "none", repeat: 3, immediateRender: false}, 15.0);')
    text("heart", "SO HEART", "RACIN'", 14.1, 14.65, 120, 190, t1=16.75)
    text("heart", "ENTIRE BODY", "SAYIN'", 15.45, 16.2, 1150, 150, red=False, t1=18.35)
    for k, (tk, sz, y) in enumerate([(16.8, 120, 230), (17.6, 150, 440), (18.4, 190, 1120)]):
        i = nid("t")
        put("heart", f'<div class="txt" id="{i}" style="top:{y}px;left:0;width:1080px;text-align:center"><div class="bg red scr" style="font-size:{sz}px">ah-ooh-ah</div></div>')
        HIDE.append(f"#{i}")
        js(f'tl.fromTo("#{i}", {{opacity: 0, scale: .6, filter: "blur(10px)"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", duration: .4, ease: "expo.out", immediateRender: false}}, {tk:.3f});')
        js(f'tl.to("#{i}", {{opacity: .25, scale: 1.25, duration: 1.6, ease: "power1.out"}}, {tk + .4:.3f});')
    js('tl.to("#c5", {scale: 1.6, duration: 2.2, ease: "power2.in", transformOrigin: "540px 760px"}, 18.4);')                       # accelerating into the heart
    # 7. The drop: GIRLFRIEND, the ring box
    i, *_ = obj("ring", "o5_ringbox", 540, 880, 860, 20.63, enter="pop", d=.5)
    x0, y0, x1, y1 = BOX["o5_ringbox"]
    s_ = 860 / (y1 - y0)
    dx, dy = 540 + (520 - (x0 + x1) / 2) * s_, 880 + (585 - (y0 + y1) / 2) * s_
    put("ring", f'<svg id="spk" class="spark" viewBox="-50 -50 100 100" style="left:{dx - 70:.0f}px;top:{dy - 70:.0f}px;width:140px;height:140px">'
                '<path d="M0 -48 C6 -8 8 -6 48 0 C8 6 6 8 0 48 C-6 8 -8 6 -48 0 C-8 -6 -6 -8 0 -48 Z" fill="#fff"/></svg>')
    HIDE.append("#spk")
    js('tl.fromTo("#spk", {opacity: 0, scale: 0, rotation: -60}, {opacity: 1, scale: 1.2, rotation: 0, duration: .35, ease: "back.out(2.4)", immediateRender: false}, 21.65);')
    js('tl.to("#spk", {scale: .5, opacity: 0, duration: .5, ease: "power2.in"}, 22.2);')
    CUES.append((21.65, "sparkle"))
    text("ring", "I WANT YOU TO MAKE YOU MY", "GIRLFRIEND", 20.63, 21.65, 90, 150)
    # 8. Wait 'til the world ends: the globe over the sunset, the sun flares
    obj("globe", "o6_globe", 540, 560, 520, 23.25)
    sx, sy = bgpt(505, 723)
    glow("globe", sx, sy, 320, "rgba(255,190,90,.9)", 24.85, op=.95, z=6)
    text("globe", "WAIT 'TIL THE", "WORLD ENDS", 23.75, 24.85, 1110, 170)
    # 9. Badman deserves ya: him, a crown draws on
    i = char("badman", "c1_him_profile", 540, 1430, 1180, 25.8, z=5, idle=False)
    x0, y0, x1, y1 = BOX["c1_him_profile"]
    s = 1180 / (y1 - y0)
    hx = 540 + (480 - (x0 + x1) / 2) * s
    hy = 1430 - 1180 + (75 - y0) * s
    put("badman", f'<svg id="crown" class="crown" viewBox="0 0 200 120" style="left:{hx - 115:.0f}px;top:{hy - 120:.0f}px">'
                  '<path pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" d="M15 105 L28 30 L68 70 L100 12 L132 70 L172 30 L185 105 Z"/></svg>')
    HIDE.append("#crown")
    js('tl.set("#crown", {opacity: 1}, 25.9);')
    js('tl.fromTo("#crown path", {strokeDashoffset: 1}, {strokeDashoffset: 0, duration: .7, ease: "power2.inOut", immediateRender: false}, 25.9);')
    js('tl.fromTo("#crown", {scale: 1.3, rotation: -10}, {scale: 1, rotation: -6, duration: .5, ease: "back.out(2)", immediateRender: false}, 25.9);')
    text("badman", "", "BADMAN", 25.85, 25.85, 1110, 220, t1=26.6)
    text("badman", "DESERVES", "YA", 26.6, 27.05, 1110, 170, red=False)
    # 10. Badman buy Birkins: the bags drop on the 808s and bounce
    for k, (cx, h, td, rot) in enumerate([(300, 430, 28.4, -8), (790, 470, 29.05, 7), (545, 560, 29.7, 0)]):
        j, *_ = obj("birkin", "o7_handbag", cx, 860 + 40 * (k == 2), h, td, enter="none", idle=False)
        js(f'tl.fromTo("#{j}", {{y: -1300, rotation: {rot - 20}}}, {{y: 0, rotation: {rot}, duration: .55, ease: "bounce.out", immediateRender: false}}, {td:.3f});')
        CUES.append((td + .2, "thud"))
    text("birkin", "BADMAN BUY", "BIRKINS", 28.45, 29.75, 110, 200)
    # 11. For you, for certain: the cover as a print, CERTAIN stamped
    i = nid("o")
    put("certain", f'<div class="print" id="{i}" style="left:250px;top:330px;width:580px;height:580px;transform:rotate(-4deg)"><img src="assets/img/cover.jpg" alt=""></div>')
    HIDE.append(f"#{i}")
    js(f'tl.fromTo("#{i}", {{opacity: 0, y: 160, rotation: 10, filter: "blur(16px)"}}, {{opacity: 1, y: 0, rotation: -4, filter: "blur(0px)", duration: .7, ease: "expo.out", immediateRender: false}}, 31.0);')
    j = nid("t")
    put("certain", f'<div class="stamp" id="{j}">CERTAIN</div>')
    HIDE.append(f"#{j}")
    js(f'tl.fromTo("#{j}", {{opacity: 0, scale: 2.2}}, {{opacity: 1, scale: 1, duration: .28, ease: "back.out(2)", immediateRender: false}}, 32.35);')
    CUES.append((32.4, "stamp"))
    text("certain", "FOR YOU, FOR", "", 31.25, 31.25, 190, 0)
    # 12. Search, I been searchin': the lens sweeps the party
    i, *_ = obj("search", "o8_magnifier", 470, 700, 900, 33.02, d=.45, idle=False)
    js(f'tl.fromTo("#{i}", {{x: 360, y: 120, rotation: 18}}, {{x: 0, y: 0, rotation: 0, duration: 1.2, ease: "power2.inOut", immediateRender: false}}, 33.02);')
    text("search", "", "SEARCH", 33.05, 33.05, 1130, 200)
    text("search", "I BEEN SEARCHIN'", "", 33.75, 33.75, 1340, 0)
    # 13. Woah, woah, ah: the swirl turns; the roll at 35.5 is a three-step stutter push
    js('tl.fromTo("#bg12", {rotation: 0, scale: 1.25}, {rotation: 40, scale: 1.25, duration: 1.7, ease: "none", immediateRender: false}, 34.75);')
    for k, tk in enumerate([35.5, 35.7, 35.9]):
        js(f'tl.to("#c12", {{scale: {1.12 + .14 * k:.2f}, duration: .08, ease: "power4.out", transformOrigin: "540px 760px"}}, {tk:.3f});')
    text("woah", "", "WOAH", 34.85, 34.85, 300, 230, script=False)
    text("woah", "", "woah, ah", 35.5, 35.5, 620, 170, red=False, script=True)
    # 14. And I want you x5: the phrase stamps five times, bigger each time, the couple photos pile up
    for k, (tk, sz, y) in enumerate([(36.55, 70, 140), (37.45, 90, 250), (38.35, 115, 380), (39.25, 140, 540), (40.15, 175, 730)]):
        i = nid("t")
        put("want", f'<div class="txt" id="{i}" style="top:{y}px;left:0;width:1080px;text-align:center;z-index:8"><div class="bg{" red" if k == 4 else ""}" style="font-size:{sz}px">AND I WANT YOU</div></div>')
        HIDE.append(f"#{i}")
        js(f'tl.fromTo("#{i}", {{opacity: 0, scale: 1.5, filter: "blur(14px)"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", duration: .25, ease: "expo.out", immediateRender: false}}, {tk:.3f});')
    for k, (name, x, y, rot, tk) in enumerate([("c5_couple_slowdance", 120, 470, -8, 36.6), ("c6_couple_laugh", 560, 520, 6, 37.5),
                                              ("c7_couple_walk", 330, 640, -2, 38.4)]):
        i = nid("o")
        put("want", f'<div class="print pol" id="{i}" style="left:{x}px;top:{y}px;width:400px;height:520px;transform:rotate({rot}deg)"><img src="{G}{name}.png" alt=""></div>')
        HIDE.append(f"#{i}")
        js(f'tl.fromTo("#{i}", {{opacity: 0, y: 700, rotation: {rot + 25}}}, {{opacity: 1, y: 0, rotation: {rot}, duration: .55, ease: "expo.out", immediateRender: false}}, {tk:.3f});')
    # 15. Tried on the first night: the tape rewinds to the party
    i, *_ = obj("tried", "o9_vhs", 540, 760, 560, 41.3, enter="pop", d=.45)
    js(f'tl.to("#{i}", {{opacity: 0, scale: 1.6, filter: "blur(14px)", duration: .3, ease: "power2.in"}}, 41.95);')
    put("tried", '<div id="rew" class="rew">&#9664;&#9664; REW</div><div id="scan" class="scan"></div>')
    HIDE.extend(["#rew", "#scan"])
    js('tl.set("#rew", {opacity: 1}, 41.6); tl.set("#scan", {opacity: .55}, 41.6);')
    for k in range(8):
        js(f'tl.set("#bg14", {{x: {R.choice([-14, 10, -6, 16, 0])}, filter: "hue-rotate({R.choice([0, 25, -20])}deg) saturate(1.4)"}}, {41.6 + k * .1:.3f});')
    text("tried", "TRIED ON THE", "FIRST NIGHT", 41.4, 42.3, 1120, 150)
    # 16. Extended my hand and let go of my pride: the hand, PRIDE shatters
    obj("pride", "o10_hand", 470, 760, 470, 42.9, d=.7)
    text("pride", "EXTENDED MY", "HAND", 42.95, 43.55, 150, 200, red=False)
    i = nid("t")
    pieces = "".join(f'<div class="shard" style="clip-path:polygon({p})">PRIDE</div>' for p in
                     ["0 0,40% 0,30% 55%,0 40%", "40% 0,75% 0,60% 50%,30% 55%", "75% 0,100% 0,100% 45%,60% 50%",
                      "0 40%,30% 55%,25% 100%,0 100%", "30% 55%,60% 50%,70% 100%,25% 100%", "60% 50%,100% 45%,100% 100%,70% 100%"])
    put("pride", f'<div class="txt" id="{i}" style="top:1080px;left:0;width:1080px;text-align:center"><div class="sm">LET GO OF MY</div><div class="shards">{pieces}</div></div>')
    HIDE.append(f"#{i}")
    js(f'tl.fromTo("#{i}", {{opacity: 0}}, {{opacity: 1, duration: .25, immediateRender: false}}, 44.2);')
    js(f'tl.to("#{i} .shard", {{x: (k) => [-260, 0, 260, -320, 40, 340][k], y: (k) => [-220, -320, -200, 260, 340, 240][k], '
       f'rotation: (k) => [-40, 25, 50, -60, 30, 70][k], opacity: 0, duration: .55, ease: "power3.out"}}, 44.9);')
    CUES.append((44.9, "shatter"))
    # 17. A bottle of '42: the bottle pours, the glass from above, the dive through its rim
    i, l, t, s = obj("fortytwo", "o11_bottle", 400, 700, 900, 45.45, d=.6, extra='<div class="lbl42">\'42</div>', idle=False)
    js(f'tl.to("#{i}", {{rotation: -38, x: 140, y: -60, duration: .6, ease: "power2.inOut"}}, 46.75);')
    CUES.append((47.05, "pour"))
    j, *_ = obj("fortytwo", "o12_glass_top", 540, 760, 560, 47.0, enter="pop", d=.5, z=6)
    text("fortytwo", "I GOT A BOTTLE OF", "'42", 45.5, 46.35, 110, 230)
    text("fortytwo", "I COULD", "POUR FOR YOU", 46.8, 47.05, 1140, 130, red=False)
    # 18. I'm not sayin' no tonight: neon NO flickers off, TONIGHT lights
    put("neon", '<div id="nno" class="neon">NO</div><div id="nto" class="neon pink">TONIGHT</div>')
    HIDE.extend(["#nno", "#nto"])
    for k, (o, dt) in enumerate([(1, 0), (.2, .05), (1, .1), (.4, .17), (1, .22)]):
        js(f'tl.set("#nno", {{opacity: {o}}}, {48.45 + dt:.3f});')
    for k, (o, dt) in enumerate([(.3, 0), (0, .06), (.15, .1), (0, .14)]):
        js(f'tl.set("#nno", {{opacity: {o}}}, {49.05 + dt:.3f});')
    for k, (o, dt) in enumerate([(1, 0), (.2, .05), (1, .1), (.5, .16), (1, .2)]):
        js(f'tl.set("#nto", {{opacity: {o}}}, {49.3 + dt:.3f});')
    CUES.extend([(48.45, "neon"), (49.3, "neon")])
    text("neon", "I'M NOT SAYIN'", "", 47.75, 47.75, 160, 0)
    text("neon", "", "yeah", 49.95, 49.95, 1180, 120, red=False, script=True)
    # 19. While you dance, I'ma hold you tight: her dancing under the ball, then the slow dance
    char("dance", "c4_her_dance", 540, 1440, 1150, 50.45)
    put("dance", '<div id="slow" class="full"><img src="' + G + 'c5_couple_slowdance.png" alt=""></div>')
    HIDE.append("#slow")
    js('tl.fromTo("#slow", {opacity: 0, scale: 1.12, filter: "blur(16px)"}, {opacity: 1, scale: 1, filter: "blur(0px)", duration: .45, ease: "power2.out", immediateRender: false}, 52.2);')
    text("dance", "WHILE YOU", "DANCE", 50.5, 51.2, 120, 200)
    text("dance", "I'MA", "HOLD YOU TIGHT", 52.25, 52.65, 1130, 140)
    # 20. You know how I want you: the laughing couple
    text("know", "YOU KNOW HOW", "I WANT YOU", 53.8, 54.75, 1120, 160)
    # 21. And sometimes, I feel like I need you: rain, the candle
    cx, cy = bgpt(512, 1150)
    glow("need", cx, cy - 40, 230, "rgba(255,170,80,.75)", 55.5, op=.8, z=2)
    text("need", "AND SOMETIMES, I FEEL LIKE", "I NEED YOU", 55.6, 57.7, 140, 170)
    # 22. The pressure of love: the gauge, the needle climbs into the red, then the logo
    i, l, t, s = obj("pressure", "o13_gauge", 540, 720, 760, 58.95, d=.6, idle=False)
    nx, ny = 505 * s, 686 * s
    put("pressure", f'<div id="needle" style="position:absolute;left:{l + nx - 9:.0f}px;top:{t + ny - 250 * s:.0f}px;width:18px;height:{250 * s:.0f}px;'
                    f'transform-origin:50% 100%;z-index:6"><i class="ndl"></i></div>')
    HIDE.append("#needle")
    js('tl.set("#needle", {opacity: 1}, 59.0);')
    js('tl.fromTo("#needle", {rotation: -125}, {rotation: 60, duration: 1.4, ease: "power3.inOut", immediateRender: false}, 59.3);')
    js('tl.to("#needle", {keyframes: [{rotation: 108, duration: .5, ease: "power2.inOut"}, {rotation: 98, duration: .12}, {rotation: 112, duration: .12}, {rotation: 102, duration: .12}, {rotation: 110, duration: .12}]}, 60.7);')
    text("pressure", "THE", "PRESSURE", 59.25, 59.6, 120, 210)
    text("pressure", "OF", "LOVE", 60.1, 60.3, 1140, 190, red=False)


# ------------------------------------------------------------------------------------------------ transitions
def transitions():
    for k, (name, a, b, bg, kind, pt) in enumerate(SC):
        prev = SC[k - 1][4] if k else None
        if prev != "dissolve":                  # a dissolve fades its scene in itself
            js(f'tl.set("#s{k}", {{opacity: 1}}, {max(0, a - (.6 if prev == "portal" else .02)):.3f});')
        js(f'tl.fromTo("#p{k}", {{scale: 1}}, {{scale: 1.09, duration: {b - a + .6:.2f}, ease: "none", immediateRender: false}}, {a:.3f});')
        if pt:
            js(f'tl.set("#p{k}", {{transformOrigin: "{pt[0]:.0f}px {pt[1]:.0f}px"}}, 0);')
        if k + 1 >= len(SC):
            continue
        n = k + 1
        CUES.append((b - (.6 if kind == "portal" else .3), {"portal": "portal", "dissolve": "air", "flash": "hit", "drop": "drop",
                                                             "vhs": "glitch"}.get(kind, "whip")))
        if kind == "portal":
            D = .6
            x, y = pt
            js(f'tl.fromTo("#c{k}", {{scale: 1, filter: "blur(0px)"}}, {{scale: 9, filter: "blur(10px)", duration: {D}, ease: "power3.in", immediateRender: false, '
               f'transformOrigin: "{x:.0f}px {y:.0f}px"}}, {b - D:.3f});')
            js(f'tl.fromTo("#s{n}", {{clipPath: "circle(30px at {x:.0f}px {y:.0f}px)"}}, {{clipPath: "circle(1900px at {x:.0f}px {y:.0f}px)", '
               f'duration: {D + .15}, ease: "power3.in", immediateRender: false}}, {b - D:.3f});')
            js(f'tl.fromTo("#c{n}", {{scale: .35, filter: "blur(6px)"}}, {{scale: 1, filter: "blur(0px)", duration: {D + .25}, ease: "power3.out", '
               f'immediateRender: false, transformOrigin: "{x:.0f}px {y:.0f}px"}}, {b - D:.3f});')
            js(f'tl.set("#s{k}", {{opacity: 0}}, {b + .2:.3f});')
            js(f'tl.set("#s{n}", {{clipPath: "none"}}, {b + .2:.3f});')
        elif kind in ("whipup", "whipdown", "whipl", "whipr"):
            dx, dy = {"whipup": (0, 1), "whipdown": (0, -1), "whipl": (-1, 0), "whipr": (1, 0)}[kind]
            js(f'tl.to("#c{k}", {{x: {-dx * 1300}, y: {dy * 1700}, filter: "blur(24px)", duration: .32, ease: "power3.in"}}, {b - .32:.3f});')
            js(f'tl.fromTo("#c{n}", {{x: {dx * 1300}, y: {-dy * 1700}, filter: "blur(24px)"}}, {{x: 0, y: 0, filter: "blur(0px)", duration: .42, '
               f'ease: "power3.out", immediateRender: false}}, {b - .04:.3f});')
            js(f'tl.set("#s{k}", {{opacity: 0}}, {b + .02:.3f});')
        elif kind == "dissolve":
            js(f'tl.fromTo("#s{n}", {{opacity: 0}}, {{opacity: 1, duration: .45, ease: "power1.inOut", immediateRender: false}}, {b - .3:.3f});')
            js(f'tl.fromTo("#c{n}", {{filter: "blur(18px)", scale: 1.06}}, {{filter: "blur(0px)", scale: 1, duration: .6, ease: "power2.out", immediateRender: false}}, {b - .3:.3f});')
            js(f'tl.to("#c{k}", {{filter: "blur(16px)", duration: .45, ease: "power1.in"}}, {b - .3:.3f});')
            js(f'tl.set("#s{k}", {{opacity: 0}}, {b + .2:.3f});')
        elif kind in ("flash", "drop", "vhs"):
            if kind == "vhs":
                for j in range(5):
                    js(f'tl.set("#c{k}", {{x: {R.choice([-30, 24, -12, 36])}, filter: "hue-rotate({R.choice([40, -40, 90])}deg) contrast(1.6)"}}, {b - .25 + j * .05:.3f});')
            js(f'tl.fromTo("#flash", {{opacity: 0}}, {{opacity: {.95 if kind == "drop" else .8}, duration: .07, immediateRender: false}}, {b - .07:.3f});')
            js(f'tl.to("#flash", {{opacity: 0, duration: {.45 if kind == "drop" else .3}, ease: "power2.out"}}, {b:.3f});')
            js(f'tl.fromTo("#c{n}", {{scale: {1.35 if kind == "drop" else 1.18}, filter: "blur(10px)"}}, {{scale: 1, filter: "blur(0px)", duration: .5, '
               f'ease: "expo.out", immediateRender: false}}, {b:.3f});')
            js(f'tl.set("#s{k}", {{opacity: 0}}, {b:.3f});')
    # the logo: a push into the gauge, then the logo on its dark violet while the song fades
    k = len(SC) - 1
    js(f'tl.to("#c{k}", {{scale: 5, filter: "blur(12px)", duration: .55, ease: "power3.in", transformOrigin: "540px 720px"}}, {SONG_END - .45:.3f});')
    CUES.append((SONG_END + .05, "logo"))
    js(f'tl.fromTo("#logo", {{opacity: 0}}, {{opacity: 1, duration: .45, ease: "sine.inOut", immediateRender: false}}, {SONG_END - .2:.3f});')
    js(f'tl.fromTo("#logo img", {{opacity: 0, scale: 1.1, filter: "blur(18px)"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", duration: .6, ease: "power3.out", immediateRender: false}}, {SONG_END:.3f});')
    js(f'tl.fromTo("#logo .lsweep i", {{x: -700}}, {{x: 700, duration: .75, ease: "power2.inOut", immediateRender: false}}, {SONG_END + .45:.3f});')
    js(f'tl.fromTo("#logo .lstar", {{scale: 0, rotation: -45, opacity: 0}}, {{scale: 1, rotation: 0, opacity: 1, duration: .35, ease: "back.out(2.2)", immediateRender: false}}, {SONG_END + .9:.3f});')
    js(f'tl.to("#logo .lstar", {{scale: .55, opacity: 0, duration: .4, ease: "power2.in"}}, {SONG_END + 1.25:.3f});')
    js(f'tl.to("#logo img", {{scale: .97, duration: 1.2, ease: "none"}}, {SONG_END + .6:.3f});')
    HIDE.append("#logo")


CSS = f"""
@font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton.ttf"); }}
@font-face {{ font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 500; src: url("assets/fonts/inter-latin-500-normal.woff2"); }}
@font-face {{ font-family: "Play"; font-style: italic; font-weight: 700; src: url("assets/fonts/PlayfairDisplay-700Italic.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: #07070f; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; background: #07070f; }}
.scene {{ position: absolute; inset: 0; opacity: 0; overflow: hidden; }}
.push, .cam {{ position: absolute; inset: 0; }}
.bgi {{ position: absolute; left: 0; top: -90px; width: 1080px; height: 1620px; object-fit: cover; }}
.obj {{ position: absolute; opacity: 0; }}
.obj > img {{ width: 100%; height: 100%; display: block; filter: drop-shadow(0 30px 40px rgba(0,0,0,.55)); }}
.glow {{ position: absolute; opacity: 0; mix-blend-mode: screen; border-radius: 50%; }}
.txt {{ position: absolute; opacity: 0; z-index: 9; pointer-events: none; }}
.sm {{ font: 800 40px/1.2 "Inter"; color: #fff; letter-spacing: .1em; text-shadow: 0 3px 14px rgba(0,0,0,.7); }}
.sm span {{ display: inline-block; }}
.bg {{ font-family: "Anton"; line-height: .98; color: #fff; letter-spacing: .01em; text-shadow: 0 8px 30px rgba(0,0,0,.6); transform-origin: 50% 60%; }}
.bg.red {{ color: #ff3d57; text-shadow: 0 0 26px rgba(255,61,87,.55), 0 8px 30px rgba(0,0,0,.6); }}
.bg.scr {{ font-family: "Play"; font-style: italic; font-weight: 700; text-transform: none; }}
.iseg {{ display: inline-block; opacity: 0; margin: 0 .05em; }}
.spark {{ position: absolute; opacity: 0; z-index: 7; filter: drop-shadow(0 0 16px #fff) drop-shadow(0 0 36px #ffd9a0); }}
.mistw {{ position: absolute; inset: 0; opacity: 0; z-index: 6; }}
.mist {{ position: absolute; width: 140px; height: 140px; border-radius: 50%; background: radial-gradient(circle, rgba(255,235,220,.75), rgba(255,200,170,0) 70%); filter: blur(6px); }}
.pscr {{ position: absolute; border-radius: 60px; overflow: hidden; background: radial-gradient(ellipse at 50% 35%, rgba(255,120,90,.55), rgba(40,10,40,.2) 70%); }}
.pscr .who {{ position: absolute; left: 0; right: 0; top: 30%; text-align: center; font: italic 700 120px/1 "Play"; color: #fff; text-shadow: 0 0 30px rgba(255,140,120,.9); }}
.pscr .call {{ position: absolute; left: 0; right: 0; top: 47%; text-align: center; font: 500 40px/1 "Inter"; color: rgba(255,255,255,.85); letter-spacing: .08em; }}
.ring1, .ring2 {{ position: absolute; left: 50%; top: 34%; width: 260px; height: 260px; margin: -130px; border-radius: 50%; border: 4px solid rgba(255,190,170,.8); }}
.ecg {{ position: absolute; left: 0; top: 1180px; opacity: 0; z-index: 7; }}
.ecg path {{ fill: none; stroke: #ff3d57; stroke-width: 6; stroke-linejoin: round; filter: drop-shadow(0 0 10px #ff3d57); }}
.crown {{ position: absolute; width: 230px; height: 138px; opacity: 0; z-index: 7; transform-origin: 50% 100%; overflow: visible; }}
.crown path {{ fill: rgba(255,200,90,.15); stroke: #ffc65a; stroke-width: 7; stroke-linejoin: round; filter: drop-shadow(0 0 12px #ffb040); }}
.print {{ position: absolute; opacity: 0; background: #f4ecdf; padding: 18px; box-shadow: 0 30px 60px rgba(0,0,0,.6); z-index: 5; }}
.print img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.print.pol {{ padding: 16px 16px 70px; }}
.stamp {{ position: absolute; left: 140px; top: 820px; width: 800px; text-align: center; opacity: 0; z-index: 8; font: 400 190px/1 "Anton"; color: #ff3d57;
  border: 12px solid #ff3d57; border-radius: 18px; transform: rotate(-8deg); text-shadow: 0 0 20px rgba(255,61,87,.5); box-shadow: 0 0 30px rgba(255,61,87,.35); }}
.rew {{ position: absolute; right: 70px; top: 70px; font: 800 64px/1 "Inter"; color: #fff; opacity: 0; z-index: 9; letter-spacing: .06em; text-shadow: 3px 0 #f0f, -3px 0 #0ff; }}
.scan {{ position: absolute; inset: 0; opacity: 0; z-index: 8; background: repeating-linear-gradient(0deg, rgba(0,0,0,.35) 0 3px, rgba(0,0,0,0) 3px 7px); }}
.shards {{ position: relative; height: 230px; }}
.shard {{ position: absolute; left: 0; right: 0; top: 0; font: 400 230px/1 "Anton"; color: #ff3d57; text-shadow: 0 0 26px rgba(255,61,87,.55); }}
.lbl42 {{ position: absolute; left: 0; right: 0; top: 50%; text-align: center; font: italic 700 120px/1 "Play"; color: #6a2a12; opacity: .85; }}
.neon {{ position: absolute; left: 0; width: 1080px; text-align: center; opacity: 0; z-index: 8; font: 400 300px/1 "Anton"; color: #fff1e8;
  text-shadow: 0 0 10px #fff, 0 0 30px #ff7a3d, 0 0 70px #ff5a1f, 0 0 120px #ff3d1f; }}
#nno {{ top: 380px; }}
#nto {{ top: 700px; font-size: 220px; text-shadow: 0 0 10px #fff, 0 0 30px #ff4f9a, 0 0 70px #ff2d78, 0 0 120px #ff2d78; }}
.full {{ position: absolute; inset: 0; opacity: 0; z-index: 6; }}
.full img {{ position: absolute; left: 0; top: -90px; width: 1080px; height: 1620px; object-fit: cover; }}
#needle .ndl {{ display: block; width: 18px; height: 100%; background: linear-gradient(#c8281f, #7a1410); border-radius: 9px 9px 4px 4px; box-shadow: 0 0 12px rgba(255,60,40,.6); }}
#needle {{ opacity: 0; }}
#flash {{ position: absolute; inset: 0; z-index: 40; background: #fff4e6; opacity: 0; }}
#vig {{ position: absolute; inset: 0; z-index: 41; pointer-events: none; background: radial-gradient(ellipse 85% 75% at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,.5) 100%); }}
#grain {{ position: absolute; left: -40px; top: -40px; width: 1160px; height: 1520px; z-index: 42; pointer-events: none; opacity: .09; background: url(assets/img/grain.png); mix-blend-mode: overlay; }}
#logo {{ position: absolute; inset: 0; z-index: 50; background: #05030d; opacity: 0; overflow: hidden; }}
.lin {{ position: absolute; left: 0; top: {FH / 2 - 540:.0f}px; width: 1080px; height: 1080px; transform: scale(.6); }}
#logo img {{ position: absolute; inset: 0; width: 100%; height: 100%; display: block;
  -webkit-mask-image: radial-gradient(circle closest-side, #000 74%, transparent 100%); mask-image: radial-gradient(circle closest-side, #000 74%, transparent 100%); }}
.lsweep {{ position: absolute; left: 228px; top: 228px; width: 624px; height: 624px; border-radius: 50%; overflow: hidden; mix-blend-mode: screen;
  -webkit-mask-image: radial-gradient(circle, #000 70%, transparent 71%); mask-image: radial-gradient(circle, #000 70%, transparent 71%); }}
.lsweep i {{ position: absolute; left: -50%; top: 0; width: 200%; height: 100%;
  background: linear-gradient(115deg, rgba(255,255,255,0) 40%, rgba(255,255,255,.7) 50%, rgba(255,255,255,0) 60%); }}
.lstar {{ position: absolute; left: 651px; top: 285px; width: 80px; height: 80px; opacity: 0; filter: drop-shadow(0 0 14px #fff) drop-shadow(0 0 30px #c9a8ff); }}
"""


def main():
    scenes()
    transitions()
    g = random.Random(3)
    for f in range(int(DUR * 12)):
        js(f'tl.set("#grain", {{x: {g.randint(0, 40)}, y: {g.randint(0, 40)}}}, {f / 12:.3f});')
    html_sc = []
    for k, (name, a, b, bg, kind, pt) in enumerate(SC):
        src = f"{G}{bg}.png"
        html_sc.append(f'<div class="scene" id="s{k}" style="z-index:{k + 1}"><div class="push" id="p{k}"><div class="cam" id="c{k}">'
                       f'<img class="bgi" id="bg{k}" src="{src}" alt="">{"".join(EL[name])}</div></div></div>')
        HIDE.append(f"#s{k}")
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>For Certain lyric edit 3x4</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      {"".join(html_sc)}
      <div id="flash"></div><div id="vig"></div><div id="grain"></div>
      <div id="logo"><div class="lin"><img src="assets/img/brand/nxtlvl_logo.png" alt="Nxtlvl"><div class="lsweep"><i></i></div>
        <svg class="lstar" viewBox="-50 -50 100 100"><path d="M0 -48 C6 -8 8 -6 48 0 C8 6 6 8 0 48 C-6 8 -8 6 -48 0 C-8 -6 -6 -8 0 -48 Z" fill="#fff"/></svg></div></div>
      <audio id="song" src="assets/audio/section.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      gsap.set({json.dumps(list(dict.fromkeys(HIDE)))}, {{opacity: 0}});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump([{"t": round(t, 3), "type": k} for t, k in sorted(CUES)], open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
    print(f"wrote index.html {len(html) // 1024} KB, {len(A)} timeline lines, {len(SC)} scenes")


if __name__ == "__main__":
    main()
