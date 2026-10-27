"""Generate index.html, assets/audio/music.wav and assets/audio/sfx.wav.

Run from the project root:  python3 build/generate.py
"""
import html
import json
import os
import sys
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from timing import chunks, find, words  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 62.6
W = words()
T = lambda word, after=0.0: find(W, word, after)  # noqa: E731

# ---------------------------------------------------------------- scene times
t_best = T("best")
t_stream, t_degree, t_job, t_limit = T("stream,"), T("degree"), T("job"), T("limit")
t_kitne = T("kitne")
t_first = T("first.")
t_success1 = T("success")
t_pers, t_int, t_apt, t_skills = T("personality,"), T("interests,"), T("aptitude,"), T("skills")
t_work = T("work")
t_prior = T("priorities")
t_nahi_list = T("nahi", 46.0)
t_roadmap = T("roadmap")
t_two = T("2-minute")
t_options_end = T("options", 59)

P_DEG = t_degree - 0.12
P_JOB = t_job - 0.12
MAP_IN = t_kitne - 0.1
FACTORS_IN = 32.36

SCENES = [  # id, start, end
    ("s01", 0.0, 2.61), ("s02", 2.61, 7.25),
    ("s03", 7.25, P_DEG), ("s04", P_DEG, P_JOB), ("s05", P_JOB, 12.34),
    ("s06", 12.34, MAP_IN), ("s07", MAP_IN, 19.38),
    ("s08", 19.38, 24.30), ("s09", 24.30, 28.75),
    ("s10", 28.75, FACTORS_IN), ("s11", FACTORS_IN, 39.87),
    ("s12", 39.87, 44.44), ("s13", 44.44, 47.11), ("s14", 47.11, 51.97),
    ("s15", 51.97, 53.99), ("s16", 53.99, 56.99), ("s17", 56.99, DUR),
]
S = {sid: (a, b) for sid, a, b in SCENES}
MATRIX = open(os.path.join(ROOT, "build", "phone-matrix.txt")).read().strip()

# ---------------------------------------------------------------- html pieces
ICONS = {
    "personality": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/><path d="M19 3l.8 1.7L21.5 5.5l-1.7.8L19 8l-.8-1.7L16.5 5.5l1.7-.8z"/>',
    "interests": '<path d="M12 21s-7.5-4.6-9.3-9.2C1.4 8.4 3.6 5 7 5c2 0 3.4 1.1 5 3 1.6-1.9 3-3 5-3 3.4 0 5.6 3.4 4.3 6.8C19.5 16.4 12 21 12 21z"/>',
    "aptitude": '<path d="M9.5 3A3 3 0 0 0 6.5 6 3 3 0 0 0 4 9.2a3.2 3.2 0 0 0 .6 5.3A3 3 0 0 0 8 19a2.5 2.5 0 0 0 4 1V5a2.5 2.5 0 0 0-2.5-2z"/><path d="M14.5 3A3 3 0 0 1 17.5 6 3 3 0 0 1 20 9.2a3.2 3.2 0 0 1-.6 5.3A3 3 0 0 1 16 19a2.5 2.5 0 0 1-4 1"/>',
    "skills": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "values": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
}
FACTORS = [
    ("personality", "Personality", t_pers),
    ("interests", "Interests", t_int),
    ("aptitude", "Aptitude", t_apt),
    ("skills", "Skills confidence", t_skills),
    ("values", "Work values", t_work),
]
BRANCHES = ["Doctor", "Surgeon", "Psychologist", "Researcher",
            "Public Health", "Biotech", "Pharmacist", "Nutritionist"]


def clip(sid, inner, track=1, cls=""):
    a, b = S[sid]
    return (f'<section id="{sid}" class="clip scene {cls}" data-start="{a:.3f}" '
            f'data-duration="{b - a:.3f}" data-track-index="{track}">{inner}</section>')


def photo(sid, src, extra=""):
    return f'<div id="{sid}-kb" class="kb"><img src="assets/img/{src}" alt="" />{extra}</div>'


def headline(hid, text_html, style=""):
    return (f'<div class="hl-wrap" style="{style}"><div id="{hid}" class="hl">'
            f'<span class="hl-text">{text_html}</span></div></div>')


def panel(sid, name, label):
    return clip(sid, (
        f'<img class="bgfill" src="assets/img/panel-{name}-blur.jpg" alt="" />'
        f'<div class="shade"></div>'
        f'<div class="panel-stage"><div id="{sid}-card" class="panel-card">'
        f'<img src="assets/img/panel-{name}.jpg" alt="" /></div></div>'
        f'<div class="panel-label-wrap"><div id="{sid}-lab" class="panel-label">{label}</div></div>'
    ))


parts = []

# 1-2  hook on the study desk
parts.append(clip("s01", photo("s01", "study-desk.jpg") + '<div class="vignette"></div>' +
                  headline("s01-hl", "Tumhe pata hai <b>kya banna</b> hai…")))
qmarks = "".join(f'<div class="qm-wrap" style="left:{x}px;top:{y}px"><div id="s02-q{i}" class="qm">?</div></div>'
                 for i, (x, y) in enumerate([(700, 520), (860, 700), (640, 860)]))
parts.append(clip("s02", photo("s02", "study-desk.jpg") + '<div class="vignette"></div>' + qmarks +
                  headline("s02-hl", 'But <b class="hot">BEST</b> options kaun-se hain?')))

# 3-5  stream -> degree -> job title
crumbs = ('<div class="crumbs-wrap"><div id="crumbs" class="crumbs">'
          '<span id="cr1" class="crumb">STREAM</span><span id="ca1" class="arrow">→</span>'
          '<span id="cr2" class="crumb">DEGREE</span><span id="ca2" class="arrow">→</span>'
          '<span id="cr3" class="crumb">JOB TITLE</span><div id="crumb-box" class="crumb-box"></div></div></div>')
parts.append(panel("s03", "form", "STREAM"))
parts.append(panel("s04", "prospectus", "DEGREE"))
parts.append(panel("s05", "laptop", "JOB TITLE"))
crumb_layer = (f'<div id="crumb-layer" class="clip" data-start="7.250" data-duration="{12.34 - 7.25:.3f}" '
               f'data-track-index="2">{crumbs}</div>')

# 6-7  one direction, many possibilities
parts.append(clip("s06", photo("s06", "whiteboard.jpg") + '<div class="vignette"></div>' +
                  headline("s06-hl", "But <b>ek direction</b> ke andar…")))
cx, cy = 540, 770
nodes, lines = [], []
for i, name in enumerate(BRANCHES):
    ang = -np.pi / 2 + i * 2 * np.pi / len(BRANCHES)
    x, y = cx + 340 * np.cos(ang), cy + 300 * np.sin(ang)
    lines.append(f'<line id="mm-l{i}" class="mm-line" x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" pathLength="1" />')
    nodes.append(f'<div class="mm-node-wrap" style="left:{x - 150:.0f}px;top:{y - 40:.0f}px">'
                 f'<div id="mm-n{i}" class="mm-node">{name}</div></div>')
mindmap = (f'<svg class="mm-svg" width="1080" height="1920" viewBox="0 0 1080 1920">{"".join(lines)}</svg>'
           f'<div class="mm-center-wrap" style="left:{cx - 140}px;top:{cy - 140}px"><div id="mm-c" class="mm-center">'
           f'<span class="mm-small">1 direction</span><span>Healthcare</span></div></div>' + "".join(nodes))
parts.append(clip("s07", '<img class="bgfill" src="assets/img/whiteboard-blur.jpg" alt="" /><div class="shade deep"></div>' +
                  mindmap + headline("s07-hl", '1 direction = <b class="hot">many possibilities</b>')))

# 8-9  the real question
parts.append(clip("s08", photo("s08", "parent-talk.jpg") + '<div class="vignette"></div>' +
                  headline("s08-hl", "Sirf <b>“kya banna hai”</b> nahi…")))
parts.append(clip("s09", photo("s09", "parent-talk.jpg") + '<div class="vignette"></div>' +
                  headline("s09-hl", 'Which paths deserve your attention <span class="mark-wrap"><span id="s09-mark" class="mark"></span><b>FIRST?</b></span>')))

# 10  phone with the stand-in screen
screen = (f'<div class="screen" style="transform:{MATRIX}"><div class="screen-in">'
          '<div id="scr-logo" class="scr-logo">Success<br />Mappers</div>'
          '<div id="scr-sub" class="scr-sub">Career Scan</div>'
          '<div id="scr-bar" class="scr-bar"><div id="scr-fill" class="scr-fill"></div></div></div></div>')
parts.append(clip("s10", f'<div id="s10-kb" class="kb">{screen}<img class="keyed" src="assets/img/phone-keyed.png" alt="" /></div>' +
                  '<div class="vignette"></div>' +
                  '<div class="brand-chip-wrap"><div id="s10-chip" class="brand-chip">Success Mappers</div></div>'))

# 11  the five factors
pills = "".join(
    f'<div class="pill-wrap"><div id="f-{k}" class="pill"><span class="pill-ic"><svg viewBox="0 0 24 24">{ICONS[k]}</svg></span>'
    f'<span class="pill-tx">{label}</span></div></div>' for k, label, _ in FACTORS)
parts.append(clip("s11", '<img class="bgfill" src="assets/img/phone-blur.jpg" alt="" /><div class="shade indigo"></div>'
                  '<div class="stack"><div id="s11-title" class="stack-title">Kya-kya consider karta hai?</div>' + pills + '</div>'))

# 12  directions + priorities
cards = "".join(
    f'<div id="pc{i}" class="pcard" style="top:{y}px"><span class="pbadge">{n}</span>'
    f'<span class="pcol"><span class="ptitle">{tt}</span><span class="pbar" style="width:{bw}px"></span>'
    f'<span class="pbar thin" style="width:{bw - 120}px"></span></span></div>'
    for i, (n, tt, y, bw) in enumerate([("1", "Explore first", 0, 420), ("2", "Explore next", 170, 380), ("3", "Keep in view", 340, 340)]))
parts.append(clip("s12", '<div class="cream"></div><div class="stack-title dark top">Career directions + <b class="hot">priorities</b></div>'
                  f'<div class="pcards">{cards}</div>'))

# 13  list (crossed out)
rows = "".join(f'<div class="lrow"><span class="ldot"></span><span class="lbar" style="width:{w}px"></span></div>'
               for w in (520, 440, 560, 380, 480))
parts.append(clip("s13", '<div class="cream"></div><div class="list-stage"><div id="lcard" class="lcard">'
                  '<div class="ltitle">Options ki list</div>' + rows +
                  '<div id="lstrike" class="lstrike"></div><div id="lx" class="lx">✕</div></div></div>'))

# 14  roadmap
road = ("M 170 1080 C 170 900, 520 960, 560 820 S 280 640, 420 540 S 860 520, 880 380")
miles = [("Explore", 0.18), ("Shortlist", 0.5), ("Next steps", 0.78)]


def road_points(n=2000):
    segs = [((170, 1080), (170, 900), (520, 960), (560, 820))]
    p0, c2 = (560, 820), (520, 960)
    for c2n, e in (((280, 640), (420, 540)), ((860, 520), (880, 380))):
        c1 = (2 * p0[0] - c2[0], 2 * p0[1] - c2[1])
        segs.append((p0, c1, c2n, e)); p0, c2 = e, c2n
    pts = []
    for a, b, c, d in segs:
        for t in np.linspace(0, 1, n):
            pts.append(tuple((1 - t) ** 3 * np.array(a) + 3 * (1 - t) ** 2 * t * np.array(b)
                             + 3 * (1 - t) * t ** 2 * np.array(c) + t ** 3 * np.array(d)))
    pts = np.array(pts); L = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    return pts, L / L[-1]


RP, RL = road_points()
mile_xy = [RP[np.searchsorted(RL, f)] for _, f in miles]
parts.append(clip("s14", '<div class="indigo-bg"></div>'
                  f'<svg class="road-svg" width="1080" height="1920" viewBox="0 0 1080 1920">'
                  f'<path id="road" class="road" d="{road}" pathLength="1" />'
                  f'<path id="road-dash" class="road-dash" d="{road}" pathLength="1" /></svg>'
                  + "".join(f'<div class="mile-wrap" style="left:{mile_xy[i][0] - 22:.0f}px;top:{mile_xy[i][1] - 22:.0f}px">'
                            f'<div id="mile{i}" class="mile"><span class="mdot"></span><span class="mlabel">{m}</span></div></div>'
                            for i, (m, _) in enumerate(miles))
                  + '<div id="flag" class="flag">⚑</div>'
                  '<div class="road-title-wrap"><div id="road-title" class="road-title">Roadmap <span id="road-tick" class="tick">✓</span></div></div>'))

# 15  student or parent
parts.append(clip("s15", photo("s15", "parent-talk.jpg") + '<div class="vignette"></div>' +
                  headline("s15-hl", 'Student ho <b>ya parent?</b>')))

# 16  2-minute timer CTA
parts.append(clip("s16", '<div class="indigo-bg"></div>'
                  '<div class="cta-stage"><div id="cta-brand" class="cta-brand">Success Mappers</div>'
                  '<div class="timer"><svg viewBox="0 0 200 200" width="360" height="360"><circle class="ring-bg" cx="100" cy="100" r="86"/>'
                  '<circle id="ring" class="ring" cx="100" cy="100" r="86" pathLength="1"/></svg>'
                  '<div class="timer-tx"><span class="big">2:00</span><span class="min">minutes</span></div></div>'
                  '<div id="cta-free" class="cta-free"><b class="hot">FREE</b> 2-min Career Scan</div></div>'))

# 17  end card
parts.append(clip("s17", '<div class="cream"></div><div class="end-stage">'
                  '<div id="end1" class="end-line">Choosing a career is <b>important.</b></div>'
                  '<div id="end2" class="end-line">Understanding your <b class="hot">options</b> matters too.</div>'
                  '<div id="end-brand" class="end-brand">Success Mappers</div>'
                  '<div id="end-btn" class="end-btn">Take the FREE 2-min scan</div>'
                  '<div id="end-tap" class="end-tap">Tap Learn More</div></div>'))

# ---------------------------------------------------------------- captions
cap_parts, cap_tl = [], []
groups = [g for g in chunks(W) if g[0]["start"] < 56.9]
for gi, g in enumerate(groups):
    a = g[0]["start"]
    nxt = groups[gi + 1][0]["start"] if gi + 1 < len(groups) else 99
    b = min(nxt, g[-1]["end"] + 0.35) if nxt - g[-1]["end"] > 0.6 else nxt
    b = min(b, 56.99)
    spans = []
    for wi, w in enumerate(g):
        txt = w["w"].replace("SUCSESS", "Success")
        spans.append(f'<span id="w{gi}_{wi}" class="cw">{html.escape(txt)}</span>')
        cap_tl.append((w["start"], f"#w{gi}_{wi}", w["end"]))
    cap_parts.append(f'<div id="cap{gi}" class="clip cap" data-start="{a:.3f}" data-duration="{b - a:.3f}" '
                     f'data-track-index="4"><div id="capi{gi}" class="cap-in">{" ".join(spans)}</div></div>')
    cap_tl.append((a, f"POP#capi{gi}", None))

# ---------------------------------------------------------------- timeline js
js = []
A = js.append


def kb(sel, sid, s0, s1, ox, oy, x0=0, x1=0, y0=0, y1=0):
    a, b = S[sid]
    A(f'tl.fromTo("{sel}",{{scale:{s0},x:{x0},y:{y0},transformOrigin:"{ox}px {oy}px"}},'
      f'{{scale:{s1},x:{x1},y:{y1},duration:{b - a:.3f},ease:"none"}},{a:.3f});')


def pop(sel, t, dur=0.45, frm="scale:0.6,opacity:0,y:30", ease="back.out(2)"):
    A(f'tl.fromTo("{sel}",{{{frm}}},{{scale:1,opacity:1,y:0,x:0,duration:{dur},ease:"{ease}"}},{t:.3f});')


def cut_in(sel, t):  # quick settle on scene start
    A(f'tl.fromTo("{sel}",{{opacity:0.0}},{{opacity:1,duration:0.18,ease:"power1.out"}},{t:.3f});')


kb("#s01-kb", "s01", 1.0, 1.1, 600, 700)
pop("#s01-hl", 0.12)
kb("#s02-kb", "s02", 1.32, 1.42, 600, 720, 20, -10)
pop("#s02-hl", 3.39)
A(f'tl.fromTo("#s02-hl .hot",{{color:"#1f2937"}},{{color:"#d9480f",duration:0.2}},{t_best:.3f});')
for i, t in enumerate((4.3, 4.9, 5.5)):
    pop(f"#s02-q{i}", t, 0.4, "scale:0,opacity:0,y:20,rotation:-25")
for sid, t in (("s03", 7.25), ("s04", P_DEG), ("s05", P_JOB)):
    a, b = S[sid]
    A(f'tl.fromTo("#{sid}-card",{{scale:0.9,opacity:0,y:40}},{{scale:1,opacity:1,y:0,duration:0.35,ease:"power3.out"}},{a:.3f});')
    A(f'tl.to("#{sid}-card",{{scale:1.06,duration:{b - a - 0.35:.3f},ease:"none"}},{a + 0.35:.3f});')
    pop(f"#{sid}-lab", a + 0.12)
pop("#cr1", 7.3, 0.35); pop("#ca1", P_DEG + 0.05, 0.3); pop("#cr2", P_DEG + 0.1, 0.35)
pop("#ca2", P_JOB + 0.05, 0.3); pop("#cr3", P_JOB + 0.1, 0.35)
A(f'tl.fromTo("#crumb-box",{{opacity:0,scale:1.15}},{{opacity:1,scale:1,duration:0.35,ease:"power2.out"}},{t_limit:.3f});')
kb("#s06-kb", "s06", 1.0, 1.14, 800, 820)
pop("#s06-hl", 12.85)
pop("#s07-hl", MAP_IN + 0.1)
pop("#mm-c", MAP_IN + 0.15, 0.45, "scale:0,opacity:0,y:0")
for i in range(len(BRANCHES)):
    t = MAP_IN + 0.55 + i * 0.42
    A(f'tl.fromTo("#mm-l{i}",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.3,ease:"power2.out"}},{t:.3f});')
    pop(f"#mm-n{i}", t + 0.18, 0.4, "scale:0.3,opacity:0,y:0")
A('tl.fromTo("#s08-kb",{scale:1.04,transformOrigin:"540px 760px"},{scale:1.1,duration:2.52,ease:"none"},19.38);')
A('tl.to("#s08-kb",{scale:1.3,duration:0.25,ease:"power2.out"},21.9);')
A('tl.to("#s08-kb",{scale:1.36,duration:2.15,ease:"none"},22.15);')
pop("#s08-hl", 19.5)
kb("#s09-kb", "s09", 1.5, 1.6, 700, 640)
pop("#s09-hl", 24.42)
A(f'tl.fromTo("#s09-mark",{{scaleX:0}},{{scaleX:1,duration:0.3,ease:"power2.out"}},{t_first - 0.05:.3f});')
kb("#s10-kb", "s10", 1.0, 1.28, 780, 930)
A('tl.fromTo("#scr-logo",{opacity:0,y:20},{opacity:1,y:0,duration:0.4},28.95);')
A('tl.fromTo("#scr-sub",{opacity:0},{opacity:1,duration:0.4},29.3);')
A('tl.fromTo("#scr-fill",{scaleX:0},{scaleX:1,duration:2.6,ease:"power1.inOut"},29.5);')
pop("#s10-chip", t_success1)
pop("#s11-title", FACTORS_IN + 0.05, 0.4)
for k, _, t in FACTORS:
    pop(f"#f-{k}", t - 0.05, 0.4, "scale:0.7,opacity:0,x:-80")
A(f'tl.to(".pill",{{scale:1.04,duration:0.18,yoyo:true,repeat:1,stagger:0.08}},{38.2:.3f});')
for i, d in enumerate((340, -170, -170)):
    A(f'tl.fromTo("#pc{i}",{{opacity:0,x:-60,y:{d}}},{{opacity:1,x:0,y:{d},duration:0.35,ease:"power2.out"}},{39.95 + i * 0.25:.3f});')
    A(f'tl.to("#pc{i}",{{y:0,duration:0.5,ease:"power3.inOut"}},{t_prior:.3f});')
pop("#lcard", 44.5, 0.4, "scale:0.85,opacity:0,y:40")
A(f'tl.fromTo("#lstrike",{{scaleX:0}},{{scaleX:1,duration:0.3,ease:"power2.in"}},{t_nahi_list - 0.05:.3f});')
pop("#lx", t_nahi_list + 0.25, 0.35, "scale:2,opacity:0,y:0", "power3.out")
A('tl.fromTo("#road",{strokeDashoffset:1},{strokeDashoffset:0,duration:3.2,ease:"power1.inOut"},47.25);')
A('tl.fromTo("#road-dash",{opacity:0},{opacity:1,duration:0.6},47.6);')
for i, (_, f) in enumerate(miles):
    pop(f"#mile{i}", 47.25 + 3.2 * f, 0.35, "scale:0,opacity:0,y:0")
pop("#flag", 50.4, 0.4, "scale:0,opacity:0,y:30")
pop("#road-title", t_roadmap - 0.25)
pop("#road-tick", t_roadmap + 0.15, 0.35, "scale:0,opacity:0,y:0")
kb("#s15-kb", "s15", 1.0, 1.08, 540, 760)
pop("#s15-hl", 52.05)
pop("#cta-brand", 54.05, 0.4)
A('tl.fromTo("#ring",{strokeDashoffset:1},{strokeDashoffset:0,duration:2.6,ease:"none"},54.2);')
pop("#cta-free", t_two, 0.45)
pop("#end1", 57.05); pop("#end2", 59.4)
pop("#end-brand", 60.2, 0.45); pop("#end-btn", 60.6, 0.45); pop("#end-tap", 61.0, 0.4)
A('tl.to("#end-btn",{scale:1.06,duration:0.35,yoyo:true,repeat:1,ease:"sine.inOut"},61.5);')
for sid, a, _ in SCENES[1:]:
    cut_in(f"#{sid} > *:first-child", a)
for t, sel, end in cap_tl:
    if sel.startswith("POP"):
        A(f'tl.fromTo("{sel[3:]}",{{opacity:0,y:18,scale:0.94}},{{opacity:1,y:0,scale:1,duration:0.16,ease:"power2.out"}},{t:.3f});')
    else:
        A(f'tl.fromTo("{sel}",{{color:"#ffffff",scale:1}},{{color:"#FFB020",scale:1.08,duration:0.08}},{t:.3f});')
        A(f'tl.to("{sel}",{{color:"#ffffff",scale:1,duration:0.08}},{end:.3f});')

# ---------------------------------------------------------------- write html
CSS = open(os.path.join(ROOT, "build", "style.css")).read()
doc = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Success Mappers UGC ad 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{CSS}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
      {"".join(parts)}
      {crumb_layer}
      {"".join(cap_parts)}
      <audio id="vo" src="voiceover.mp3" data-start="0" data-duration="61.65" data-track-index="5" data-volume="1"></audio>
      <audio id="music" src="assets/audio/music.wav" data-start="0" data-duration="{DUR}" data-track-index="6" data-volume="0.6"></audio>
      <audio id="sfx" src="assets/audio/sfx.wav" data-start="0" data-duration="{DUR}" data-track-index="7" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join("      " + l for l in js).strip()}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(doc)

# ---------------------------------------------------------------- audio
SR = 44100
rng = np.random.default_rng(7)


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    st = np.stack([x, x], 1) if x.ndim == 1 else x
    with wave.open(path, "wb") as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((st * 32767).astype("<i2").tobytes())


def lp(x, fc):  # one-pole low-pass
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc; y[i] = acc
    return y


def env(n, att, dec):
    t = np.arange(n) / SR
    return np.minimum(t / max(att, 1e-4), 1) * np.exp(-t / dec)


N = int(DUR * SR)
# --- lo-fi bed: 80 bpm, Fmaj7 - Em7 - Dm7 - Cmaj7, two bars each
bpm, beat = 80, 60 / 80
music = np.zeros(N)
chords = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]
hz = lambda m: 440 * 2 ** ((m - 69) / 12)  # noqa: E731
bar = 4 * beat
t0 = 0.0; ci = 0
while t0 < DUR:
    for note in chords[ci % 4]:
        for hit in (0, 2 * bar - 2 * beat):
            s = int((t0 + hit) * SR); n = int(2.8 * SR)
            if s >= N: continue
            n = min(n, N - s); t = np.arange(n) / SR; f = hz(note)
            tone = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.4)
                    + 0.08 * np.sin(2 * np.pi * 3.01 * f * t) * np.exp(-t / 0.2))
            music[s:s + n] += 0.11 * tone * env(n, 0.01, 1.3) * (1 + 0.15 * np.sin(2 * np.pi * 4.5 * t))
    bass = chords[ci % 4][0] - 12
    for k in range(8):
        s = int((t0 + k * beat) * SR); n = min(int(0.7 * SR), N - s)
        if n <= 0 or k % 2: continue
        t = np.arange(n) / SR
        music[s:s + n] += 0.16 * np.sin(2 * np.pi * hz(bass) * t) * env(n, 0.005, 0.35)
    t0 += 2 * bar; ci += 1
drums = np.zeros(N)
nb = int(DUR / beat)
for k in range(nb):
    s = int(k * beat * SR)
    if k % 4 in (0, 2):  # kick
        n = min(int(0.3 * SR), N - s); t = np.arange(n) / SR
        drums[s:s + n] += 0.5 * np.sin(2 * np.pi * (45 + 70 * np.exp(-t / 0.03)) * t) * np.exp(-t / 0.12)
    if k % 4 in (1, 3):  # soft snare
        n = min(int(0.2 * SR), N - s)
        drums[s:s + n] += 0.12 * rng.standard_normal(n) * np.exp(-np.arange(n) / SR / 0.06)
    for h in (0, 0.5):  # hats
        hs = int((k + h) * beat * SR); n = min(int(0.05 * SR), N - hs)
        if n > 0:
            drums[hs:hs + n] += 0.035 * rng.standard_normal(n) * np.exp(-np.arange(n) / SR / 0.012)
music = lp(music, 2200) + lp(drums, 3500)
crackle = np.zeros(N); idx = rng.integers(0, N, 900); crackle[idx] = rng.uniform(-0.2, 0.2, 900)
music += lp(crackle, 3000) + 0.004 * lp(rng.standard_normal(N), 1200)
fade = np.ones(N); fi = int(0.4 * SR); fo = int(2.5 * SR)
fade[:fi] = np.linspace(0, 1, fi); fade[-fo:] = np.linspace(1, 0, fo)
music *= fade
music *= 10 ** (-27 / 20) / np.sqrt(np.mean(music ** 2))  # quiet bed under the VO
write_wav(os.path.join(ROOT, "assets/audio/music.wav"), music)

# --- sound effects
sfx = np.zeros(N)


def add(t, x, g=1.0):
    s = int(t * SR); n = min(len(x), N - s)
    if n > 0 and s >= 0: sfx[s:s + n] += g * x[:n]


def whoosh(d=0.38):
    n = int(d * SR); t = np.arange(n) / SR; x = rng.standard_normal(n)
    sweep = np.sin(np.pi * t / d) ** 2
    return lp(x, 1800) * sweep * 0.5 + lp(x, 600) * sweep * 0.4


def pop_s(f0=880):
    n = int(0.09 * SR); t = np.arange(n) / SR
    f = f0 * (1 - 0.45 * t / 0.09)
    return 0.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.03)


def tick():
    n = int(0.03 * SR); t = np.arange(n) / SR
    return 0.35 * np.sin(2 * np.pi * 2400 * t) * np.exp(-t / 0.006)


def ding():
    n = int(0.9 * SR); t = np.arange(n) / SR
    return 0.28 * (np.sin(2 * np.pi * 1318 * t) + 0.5 * np.sin(2 * np.pi * 1976 * t)) * np.exp(-t / 0.35)


def scratch():
    n = int(0.3 * SR); x = rng.standard_normal(n)
    return 0.35 * (x - lp(x, 2500)) * np.exp(-np.arange(n) / SR / 0.12)


for sid, a, _ in SCENES[1:]:
    add(a - 0.12, whoosh(), 0.55)
for t in (0.12, 3.39, 12.85, MAP_IN + 0.1, 19.5, 24.42, t_success1, 52.05):
    add(t, pop_s(760), 0.8)
for t in (4.3, 4.9, 5.5):
    add(t, pop_s(1100), 0.5)
for t in (7.3, P_DEG + 0.1, P_JOB + 0.1):
    add(t, pop_s(940), 0.7)
add(t_limit, scratch(), 0.8)
for i in range(len(BRANCHES)):
    add(MAP_IN + 0.73 + i * 0.42, pop_s(700 + 60 * i), 0.55)
for _, _, t in FACTORS:
    add(t - 0.05, pop_s(820), 0.75)
add(t_prior, whoosh(0.3), 0.35)
add(t_nahi_list - 0.05, scratch(), 0.9)
for i, (_, f) in enumerate(miles):
    add(47.25 + 3.2 * f, pop_s(900), 0.5)
add(t_roadmap + 0.15, ding(), 0.9)
for k in range(10):
    add(54.25 + k * 0.26, tick(), 0.45)
add(t_two, pop_s(980), 0.7)
for t in (57.05, 59.4, 60.6):
    add(t, pop_s(800), 0.6)
add(60.6, ding(), 0.6)
write_wav(os.path.join(ROOT, "assets/audio/sfx.wav"), sfx * 0.5)

json.dump({"words": W, "scenes": SCENES}, open(os.path.join(ROOT, "build", "timing.json"), "w"), indent=1)
print("scenes", len(SCENES), "captions", len(groups), "tweens", len(js))
