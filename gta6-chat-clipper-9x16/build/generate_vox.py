"""AI.NXTLVL: GTA 6 clipping part 2, v2 "Vox" cut (1080x1920, 30 fps, 30 s).

Owner (v2): "it looks like a reskin of the reference; go with a Vox style animation, use the GTA 6 Miami background I
uploaded earlier, mascot-based concepts for every frame, visual elements so no frame is dull, 30 seconds, and check that
no video or concept is out of proportion".
  * Look (vox-explainer skill): torn cream paper cards with small shadows, halftone dots, paper + film grain, colour
    fringing at the frame edges only, a soft vignette, bold condensed type as blocks, a red marker that circles and
    strikes, yellow highlighter. Motion is STEPPED on twos (12 drawings a second); no smooth easing, no typewriter.
  * Backdrop: the owner's GTA 6 Miami art (Rockstar's "GTA VI: The Album" reel, assets/video/vc_full.mp4, native
    1080x1920), a different stretch of it behind each shot, slow stepped push.
  * Nyx (our AI.NXTLVL mascot) as a paper sticker, in every shot, with a prop: magnifier, buried in chat, pointer,
    wrench, scissors, rewind dial, beach chair + shades, waving with the files.
  * Proportions: every video sits in a box of its own aspect (stream 16:9, clips 9:16, background 9:16), every image in
    a box of its own aspect (guide cover 4:5); object-fit cover only where the aspects already match.
Clock: the VO (build/vo_assemble.py -> plan/words.json, plan/lines.json).
python3 build/generate_vox.py  ->  index.html, plan/edit.json, plan/sfx_events.json
"""
import html as H
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nyx import nyx, star_svg, EYES  # noqa: E402  (the mascot drawing is shared with v1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FW, FH, FPS = 1080, 1920, 30
WORDS = json.load(open(os.path.join(ROOT, "plan", "words.json")))
LINES = {l["id"]: l for l in json.load(open(os.path.join(ROOT, "plan", "lines.json")))}
DUR = 30.0
CREAM, PAPER, NAVY, RED, YEL, PINK, VIO, CYAN = "#F1E6D0", "#FBF7EE", "#14213D", "#B8312A", "#F2C230", "#ff4fa3", "#7a2ffb", "#3ef0ff"
A, SFX, BODY, CAPS = [], [], [], []
R = random.Random(5)


def js(s):
    A.append("      " + s)


def sfx(kind, t, gain=0.0):
    SFX.append({"type": kind, "t": round(max(0.0, t), 3), "gain": gain})


def norm(w):
    return w.lower().strip(".,?!:'\"")


def T(word, after=0.0, key="s"):
    for w in WORDS:
        if w["s"] >= after - .05 and norm(w["w"]) == norm(word):
            return w[key]
    raise KeyError(word)


def L(i, key="s"):
    return LINES[f"g{i:02d}"][key]


def st(d):
    return f"steps({max(1, round(d * 12))})"


def drop(sel, t, d=.34, y=-80, rot=0):
    """a paper piece drops in, stepped"""
    js(f'tl.fromTo("{sel}", {{opacity: 0, y: {y}, rotation: {rot - 6}}}, {{opacity: 1, y: 0, rotation: {rot}, duration: {d}, ease: "{st(d)}", immediateRender: false}}, {t:.3f});')


def slap(sel, t, d=.25, rot=-6):
    js(f'tl.fromTo("{sel}", {{opacity: 0, scale: 2.2, rotation: {rot - 10}}}, {{opacity: 1, scale: 1, rotation: {rot}, duration: {d}, ease: "{st(d)}", immediateRender: false}}, {t:.3f});')


def draw(sel, t, d=.4, length=1600):
    js(f'tl.fromTo("{sel}", {{strokeDasharray: {length}, strokeDashoffset: {length}}}, {{strokeDashoffset: 0, duration: {d}, ease: "{st(d)}", immediateRender: false}}, {t:.3f});')


TORN = ("polygon(0% 7%, 5% 0%, 11% 6%, 18% 1%, 26% 7%, 34% 0%, 43% 6%, 52% 1%, 61% 7%, 69% 0%, 77% 6%, 85% 1%, 93% 7%, 100% 2%, 99% 50%, 100% 96%, "
        "93% 100%, 85% 94%, 77% 99%, 69% 93%, 61% 100%, 52% 94%, 43% 99%, 34% 93%, 26% 100%, 18% 94%, 11% 99%, 5% 93%, 0% 98%, 1% 50%)")


def strip(sid, html, top, size=88, rot=-2, cls=""):
    BODY.append(f'<div class="strip {cls}" id="{sid}" style="top:{top}px;transform:rotate({rot}deg)"><b style="font-size:{size}px">{html}</b></div>')


def card(sid, inner, style, cls=""):
    BODY.append(f'<div class="card {cls}" id="{sid}" style="{style}"><div class="cin">{inner}</div></div>')


def group(gid, t0, t1):
    """every element whose id starts with the shot prefix is hidden outside its shot"""
    js(f'tl.set("[id^={gid}_]", {{opacity: 0}}, {t1:.3f});')


def face(eyes, t):
    for e in EYES:
        js(f'tl.set("#nyx1 .{e}", {{opacity: {1 if e == eyes else 0}}}, {t:.3f});')


def nyx_to(t, x, y, s=1.0, rot=0, d=.34):
    js(f'tl.to("#nyxw", {{x: {x}, y: {y}, scale: {s}, rotation: {rot}, duration: {d}, ease: "{st(d)}"}}, {t:.3f});')


def plate(t0, t1, at, push=(1.0, 1.08)):
    """the Miami art behind a shot: one stretch of the album reel, stepped push"""
    vid = f"bg{sum(1 for b in BODY if 'class="bgv"' in b)}"
    BODY.append(f'<div class="bgw" id="{vid}w"><video class="bgv" id="{vid}" src="assets/video/vc_full.mp4" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" '
                f'data-media-start="{at:.3f}" data-track-index="{len(BODY) % 4}" muted playsinline></video></div>')
    js(f'tl.set("#{vid}w", {{opacity: 1}}, {t0:.3f}); tl.set("#{vid}w", {{opacity: 0}}, {t1:.3f});')
    js(f'tl.fromTo("#{vid}", {{scale: {push[0]}}}, {{scale: {push[1]}, duration: {t1 - t0:.3f}, ease: "{st(t1 - t0)}", immediateRender: false}}, {t0:.3f});')


def prop(pid, svg, style):
    BODY.append(f'<div class="prop" id="{pid}" style="{style}">{svg}</div>')


MAG = f'<svg viewBox="0 0 120 120"><circle cx="48" cy="48" r="34" fill="rgba(255,255,255,.35)" stroke="{NAVY}" stroke-width="10"/><path d="M74 74 L110 110" stroke="{NAVY}" stroke-width="16" stroke-linecap="round"/></svg>'
SCIS = (f'<svg viewBox="0 0 140 140"><circle cx="34" cy="104" r="22" fill="none" stroke="{RED}" stroke-width="10"/><circle cx="104" cy="104" r="22" fill="none" stroke="{RED}" stroke-width="10"/>'
        f'<path d="M48 88 L112 10 M92 88 L28 10" stroke="{NAVY}" stroke-width="10" stroke-linecap="round"/></svg>')
WRENCH = f'<svg viewBox="0 0 120 120"><path d="M30 100 L80 50" stroke="{NAVY}" stroke-width="16" stroke-linecap="round"/><circle cx="88" cy="36" r="24" fill="none" stroke="{NAVY}" stroke-width="12"/></svg>'
POINTER = f'<svg viewBox="0 0 200 40"><path d="M6 20 L180 20" stroke="{NAVY}" stroke-width="10" stroke-linecap="round"/><circle cx="186" cy="20" r="12" fill="{RED}"/></svg>'
DIAL = (f'<svg viewBox="0 0 140 140"><circle cx="70" cy="70" r="60" fill="{PAPER}" stroke="{NAVY}" stroke-width="8"/><path id="dialh" d="M70 70 L70 22" stroke="{RED}" stroke-width="10" stroke-linecap="round"/>'
        f'<path d="M30 40 A50 50 0 0 0 30 100" fill="none" stroke="{NAVY}" stroke-width="6"/><path d="M22 92 L30 104 L42 96" fill="none" stroke="{NAVY}" stroke-width="6"/></svg>')
CHAIR = (f'<svg viewBox="0 0 300 200"><path d="M40 60 L240 150" stroke="{PINK}" stroke-width="40" stroke-linecap="round"/><path d="M60 170 L120 90 M220 180 L180 120" stroke="{NAVY}" stroke-width="10" stroke-linecap="round"/>'
         f'<path d="M30 70 L250 160" stroke="{PAPER}" stroke-width="10" stroke-dasharray="20 18"/></svg>')

BUBS = ["LMAO", "KEKW", "CLIP IT", "NO WAY", "???", "W", "BRO", "LMAOOO", "CLIP THAT", "WHAT", "OMEGALUL", "HAHA"]


def build():
    ts = [0.0] + [L(i) - .08 for i in range(1, 8)] + [DUR]
    # ---------- S1 hook: "You don't need AI to find the best GTA 6 clips. Chat already found them."
    s0, s1 = ts[0], ts[1]
    plate(s0, s1, 14.0)
    strip("a_t1", 'YOU DON\'T NEED <span class="st" id="a_st">AI</span>', 230, 82, -2)
    strip("a_t2", 'TO FIND <span class="hl">GTA 6 CLIPS</span>', 360, 84, 1.5)
    card("a_ai", '<div class="aic">AI CLIP<br>FINDER</div>', "left:110px;top:700px;width:380px;height:300px;transform:rotate(-5deg)")
    card("a_chat", '<div class="bub big">CHAT</div><div class="cap2">already found them</div>', "left:560px;top:760px;width:420px;height:330px;transform:rotate(4deg)")
    BODY.append(f'<svg class="mk" id="a_x" viewBox="0 0 380 300" style="left:110px;top:700px;width:380px;height:300px"><path d="M30 40 L350 260 M350 40 L30 260" stroke="{RED}" stroke-width="18" stroke-linecap="round" fill="none"/></svg>')
    BODY.append(f'<svg class="mk" id="a_ring" viewBox="0 0 460 380" style="left:540px;top:735px;width:460px;height:380px"><path d="M230 20 C380 18 450 110 440 200 C430 300 330 360 220 360 C100 360 18 290 20 190 C22 90 110 24 250 30" stroke="{RED}" stroke-width="10" fill="none" stroke-linecap="round"/></svg>')
    js(f'tl.set("[id^=a_]", {{opacity: 1}}, 0); tl.set("#a_x, #a_ring, #a_chat", {{opacity: 0}}, 0);')
    js(f'tl.fromTo("#a_t1", {{scale: 1.15}}, {{scale: 1, duration: .5, ease: "{st(.5)}"}}, 0);')
    t_need = T("need") - .05
    js(f'tl.fromTo("#a_st", {{"--s": 0}}, {{"--s": 1, duration: .25, ease: "{st(.25)}", immediateRender: false}}, {t_need:.3f});')
    js(f'tl.set("#a_x", {{opacity: 1}}, {t_need + .3:.3f});')
    draw("#a_x path", t_need + .3, .3, 900)
    t_chat = T("chat", L(0) + .5) - .05
    slap("#a_chat", t_chat, rot=4)
    js(f'tl.set("#a_ring", {{opacity: 1}}, {t_chat + .25:.3f});')
    draw("#a_ring path", t_chat + .25, .45, 1500)
    sfx("buzz", t_need + .3, -8)
    sfx("stamp", t_chat, -2)
    prop("a_mag", MAG, "left:470px;top:1040px;width:170px;height:170px")
    js(f'tl.set("#a_mag", {{opacity: 1}}, 0); tl.fromTo("#a_mag", {{x: -160, y: 60, rotation: -20}}, {{x: 40, y: -60, rotation: 0, duration: {t_chat:.3f}, ease: "{st(t_chat)}", immediateRender: false}}, 0);')
    group("a", s0, s1)
    # ---------- S2: "When something crazy happens, chat explodes."
    s2 = ts[2]
    plate(s1, s2, 2.0)
    card("b_stream", f'<div class="vbox169"><video id="b_sv" src="assets/video/stream.mp4" data-start="{s1:.3f}" data-duration="{s2 - s1 + .1:.3f}" data-media-start="0" '
                     f'data-track-index="1" muted playsinline></video><div class="live">LIVE</div></div><div class="cap2">GTA 6 stream · hour 4 of 6</div>',
         "left:90px;top:300px;width:900px;transform:rotate(-1.5deg)")
    bubs = ""
    for k in range(18):
        x, y, r = R.randint(40, 820), R.randint(820, 1380), R.randint(-14, 14)
        bubs += f'<div class="bub" id="b_b{k}" style="left:{x}px;top:{y}px;transform:rotate({r}deg)">{BUBS[k % len(BUBS)]}</div>'
    BODY.append(bubs)
    strip("b_t", 'CHAT <span class="hl">EXPLODES</span>', 1180, 96, -3)
    card("b_cnt", '<div class="cnt"><b id="b_n">0</b><span>messages in 10 s</span></div>', "left:640px;top:1430px;width:340px;transform:rotate(3deg)")
    js(f'tl.set("#b_stream", {{opacity: 1}}, {s1:.3f});')
    drop("#b_stream", s1, rot=-1.5)
    t_ex = T("explodes") - .12
    js(f'tl.fromTo("[id^=b_b]", {{opacity: 0, scale: .2}}, {{opacity: 1, scale: 1, duration: .1, ease: "steps(1)", stagger: .045, immediateRender: false}}, {t_ex - .3:.3f});')
    slap("#b_t", t_ex, rot=-3)
    drop("#b_cnt", t_ex + .25, rot=3)
    js(f'tl.fromTo("#b_n", {{innerText: 0}}, {{innerText: 312, duration: .6, snap: {{innerText: 1}}, ease: "{st(.6)}", immediateRender: false}}, {t_ex + .25:.3f});')
    js(f'tl.fromTo("#b_stream", {{x: 0}}, {{x: 10, duration: .08, yoyo: true, repeat: 5, ease: "steps(1)", immediateRender: false}}, {t_ex:.3f});')
    for k in range(5):
        sfx("pop", t_ex - .3 + k * .16, -10)
    sfx("whoosh", t_ex, -4)
    group("b", s1, s2)
    # ---------- S3: "That spike is your clip."
    s3 = ts[3]
    plate(s2, s3, 9.0)
    card("c_graph", f'<svg viewBox="0 0 860 380" class="gsvg"><path d="M20 340 H840" stroke="{NAVY}" stroke-width="5"/><path id="c_line" d="M20 320 L90 316 L160 322 L230 312 L300 318 L370 310 L440 314 L500 300 L540 60 L580 296 L650 312 L720 316 L840 314" '
                    f'fill="none" stroke="{NAVY}" stroke-width="9" stroke-linejoin="round"/><text x="24" y="372" font-family="J" font-size="22" fill="{NAVY}">CHAT / 10 S</text></svg>',
         "left:110px;top:520px;width:860px;transform:rotate(-1deg)")
    BODY.append(f'<svg class="mk" id="c_ring" viewBox="0 0 240 300" style="left:540px;top:500px;width:240px;height:300px"><path d="M120 16 C200 16 226 100 222 160 C216 250 170 286 116 284 C50 282 16 220 18 150 C20 70 60 14 140 20" stroke="{RED}" stroke-width="10" fill="none" stroke-linecap="round"/></svg>')
    strip("c_t", 'THAT SPIKE = <span class="hl">YOUR CLIP</span>', 270, 70, 2)
    js(f'tl.set("#c_graph, #c_t", {{opacity: 1}}, {s2:.3f}); tl.set("#c_ring", {{opacity: 0}}, {s2:.3f});')
    drop("#c_graph", s2, rot=-1)
    draw("#c_line", s2 + .1, .6, 1800)
    t_sp = T("spike") - .05
    js(f'tl.set("#c_ring", {{opacity: 1}}, {t_sp:.3f});')
    draw("#c_ring path", t_sp, .35, 1100)
    slap("#c_t", T("clip.", L(2)) - .3, rot=2)
    prop("c_ptr", POINTER, "left:300px;top:1000px;width:380px;height:76px")
    js(f'tl.set("#c_ptr", {{opacity: 1}}, {s2:.3f}); tl.fromTo("#c_ptr", {{rotation: 30, x: -60}}, {{rotation: -36, x: 0, duration: .4, ease: "{st(.4)}", immediateRender: false, transformOrigin: "0% 50%"}}, {t_sp - .1:.3f});')
    sfx("ding", t_sp, -4)
    group("c", s2, s3)
    # ---------- S4: "So I had Claude build a tiny free tool."
    s4 = ts[4]
    plate(s3, s4, 5.0)
    code = ["# chat_clips.py", "for t, msg in chat:", "  counts[t // 10] += 1", "spikes = top(counts)", "cut(spike - 20, vertical)"]
    card("d_note", '<div class="note">"Claude, build me a tool that finds chat spikes."</div>', "left:90px;top:330px;width:560px;transform:rotate(-3deg)")
    card("d_code", '<div class="fh">chat_clips.py</div>' + "".join(f'<div class="cl" id="d_l{k}">{H.escape(c)}</div>' for k, c in enumerate(code)),
         "left:260px;top:640px;width:720px;transform:rotate(2deg)", "dark")
    strip("d_t", '<span class="hl">1 FILE</span> · FREE', 1150, 86, -2)
    js(f'tl.set("#d_note, #d_code, #d_t", {{opacity: 1}}, {s3:.3f});')
    drop("#d_note", s3, rot=-3)
    drop("#d_code", s3 + .25, rot=2)
    js(f'tl.fromTo("[id^=d_l]", {{opacity: 0}}, {{opacity: 1, duration: .1, ease: "steps(1)", stagger: .17, immediateRender: false}}, {s3 + .5:.3f});')
    slap("#d_t", T("tiny") - .05, rot=-2)
    prop("d_wr", WRENCH, "left:340px;top:1260px;width:150px;height:150px")
    js(f'tl.set("#d_wr", {{opacity: 1}}, {s3:.3f}); tl.fromTo("#d_wr", {{rotation: 0}}, {{rotation: -40, duration: .17, yoyo: true, repeat: 7, ease: "steps(2)", immediateRender: false}}, {s3 + .3:.3f});')
    for k in range(5):
        sfx("key", s3 + .5 + k * .17, -10)
    group("d", s3, s4)
    # ---------- S5: "It counts the chat every ten seconds and cuts each spike into a vertical clip."
    s5 = ts[5]
    plate(s4, s5, 11.0)
    hot = (6, 13, 19)
    bars = "".join(f'<i class="bar{" hot" if k in hot else ""}" id="e_bar{k}" style="height:{(R.randint(150, 200) if k in hot else R.randint(26, 70))}px"></i>' for k in range(24))
    card("e_bars", f'<div class="bars">{bars}</div><div class="cap2">one bar = 10 seconds of chat</div>', "left:70px;top:320px;width:940px;transform:rotate(-1deg)")
    BODY.append(f'<svg class="mk" id="e_cut" viewBox="0 0 40 360" style="left:452px;top:300px;width:40px;height:360px"><path d="M20 0 V360" stroke="{RED}" stroke-width="6" stroke-dasharray="18 14"/></svg>')
    card("e_h", f'<div class="vbox169"><video id="e_hv" src="assets/video/stream.mp4" data-start="{s4:.3f}" data-duration="{s5 - s4:.3f}" data-media-start="6" data-track-index="2" muted playsinline></video></div>',
         "left:80px;top:860px;width:520px;transform:rotate(-3deg)")
    card("e_v", f'<div class="vbox916"><video id="e_vv" src="assets/video/v_flip.mp4" data-start="{s4:.3f}" data-duration="{s5 - s4:.3f}" data-media-start="0" data-track-index="3" muted playsinline></video></div>'
                '<div class="cap2">vertical clip</div>', "left:660px;top:760px;width:300px;transform:rotate(4deg)")
    js(f'tl.set("#e_bars", {{opacity: 1}}, {s4:.3f}); tl.set("#e_cut, #e_h, #e_v", {{opacity: 0}}, {s4:.3f});')
    drop("#e_bars", s4, rot=-1)
    js(f'tl.fromTo("[id^=e_bar]", {{scaleY: 0}}, {{scaleY: 1, duration: .1, ease: "steps(1)", stagger: .06, immediateRender: false, transformOrigin: "50% 100%"}}, {s4 + .2:.3f});')
    t_cuts = T("cuts") - .1
    js(f'tl.fromTo(".bar.hot", {{backgroundColor: "{NAVY}"}}, {{backgroundColor: "{RED}", duration: .15, ease: "steps(1)", stagger: .12, immediateRender: false}}, {t_cuts - .3:.3f});')
    js(f'tl.set("#e_cut", {{opacity: 1}}, {t_cuts:.3f});')
    draw("#e_cut path", t_cuts, .25, 400)
    drop("#e_h", t_cuts + .15, rot=-3)
    t_v = T("vertical") - .15
    js(f'tl.fromTo("#e_v", {{opacity: 0, rotation: -86, scale: .5}}, {{opacity: 1, rotation: 4, scale: 1, duration: .4, ease: "{st(.4)}", immediateRender: false}}, {t_v:.3f});')
    prop("e_sc", SCIS, "left:420px;top:1240px;width:200px;height:200px")
    js(f'tl.set("#e_sc", {{opacity: 1}}, {s4:.3f}); tl.fromTo("#e_sc", {{rotation: 0}}, {{rotation: -18, duration: .12, yoyo: true, repeat: 5, ease: "steps(1)", immediateRender: false}}, {t_cuts:.3f});')
    sfx("snip", t_cuts, -2)
    sfx("whoosh", t_v, -6)
    group("e", s4, s5)
    # ---------- S6: "Chat reacts late, so each clip starts twenty seconds early."
    s6 = ts[6]
    plate(s5, s6, 30.5)
    card("f_tl", f'<svg viewBox="0 0 900 300" class="tlsvg"><path d="M20 160 H880" stroke="{NAVY}" stroke-width="8"/>'
                 f'<g id="f_star"><path transform="translate(300 70) scale(2.6)" d="M12 0c.8 6.6 4.8 10.8 12 12-7.2 1.2-11.2 5.4-12 12-.8-6.6-4.8-10.8-12-12 7.2-1.2 11.2-5.4 12-12z" fill="{YEL}" stroke="{NAVY}" stroke-width="1.2"/>'
                 f'<text x="262" y="220" font-family="J" font-size="26" fill="{NAVY}">THE MOMENT</text></g>'
                 f'<g id="f_react"><rect x="640" y="50" width="34" height="110" fill="{RED}"/><text x="580" y="220" font-family="J" font-size="26" fill="{NAVY}">CHAT REACTS</text></g>'
                 f'<rect id="f_win" x="560" y="240" width="300" height="46" rx="8" fill="{YEL}" stroke="{NAVY}" stroke-width="4"/>'
                 f'<text id="f_wt" x="648" y="272" font-family="J" font-size="24" fill="{NAVY}">YOUR CLIP</text></svg>',
         "left:70px;top:520px;width:940px;transform:rotate(1deg)")
    strip("f_t", 'STARTS <span class="hl">20 S EARLY</span>', 280, 86, -2)
    BODY.append(f'<div class="sticker" id="f_m">−20 S</div>')
    js(f'tl.set("#f_tl", {{opacity: 1}}, {s5:.3f}); tl.set("#f_t, #f_m", {{opacity: 0}}, {s5:.3f});')
    drop("#f_tl", s5, rot=1)
    js(f'tl.fromTo("#f_star", {{opacity: 0}}, {{opacity: 1, duration: .1, ease: "steps(1)", immediateRender: false}}, {s5 + .25:.3f});')
    js(f'tl.fromTo("#f_react", {{opacity: 0}}, {{opacity: 1, duration: .1, ease: "steps(1)", immediateRender: false}}, {T("late") - .05:.3f});')
    t20 = T("twenty") - .1
    js(f'tl.fromTo("#f_win, #f_wt", {{x: 0}}, {{x: -330, duration: .5, ease: "{st(.5)}", immediateRender: false}}, {t20:.3f});')
    slap("#f_t", t20, rot=-2)
    slap("#f_m", t20 + .2, rot=8)
    prop("f_dial", DIAL, "left:430px;top:1250px;width:170px;height:170px")
    js(f'tl.set("#f_dial", {{opacity: 1}}, {s5:.3f}); tl.fromTo("#f_dial", {{rotation: 0}}, {{rotation: -300, duration: .6, ease: "{st(.6)}", immediateRender: false}}, {t20:.3f});')
    sfx("rewind", t20, -4)
    group("f", s5, s6)
    # ---------- S7: "GTA 6 drops Thursday. Let chat watch the streams for you."
    s7 = ts[7]
    plate(s6, s7, 16.5, push=(1.0, 1.12))
    card("g_cal", '<div class="calh">THURSDAY</div><div class="cald">19</div><div class="calm">NOV · GTA 6</div>', "left:80px;top:300px;width:300px;transform:rotate(-4deg)", "cal")
    vhs = "".join(f'<div class="vhs" id="g_v{k}" style="top:{k * 112}px"><b>6-HOUR STREAM</b><span>{n}</span></div>' for k, n in enumerate(["vice_streamer", "nightowl_rp", "turbo_tv"]))
    BODY.append(f'<div class="vstack" id="g_stack">{vhs}</div>')
    BODY.append("".join(f'<div class="bub sm" id="g_b{k}" style="left:{x}px;top:{y}px">{w}</div>' for k, (x, y, w) in enumerate([(640, 690, "watching"), (820, 760, "LMAO"), (700, 830, "CLIP IT")])))
    strip("g_t", 'GTA 6 DROPS <span class="hl">THURSDAY</span>', 1000, 66, 2)
    js(f'tl.set("#g_cal, #g_stack, #g_t", {{opacity: 1}}, {s6:.3f});')
    drop("#g_cal", s6, rot=-4)
    js(f'tl.fromTo("[id^=g_v]", {{opacity: 0, x: 200}}, {{opacity: 1, x: 0, duration: .2, ease: "steps(2)", stagger: .1, immediateRender: false}}, {s6 + .3:.3f});')
    slap("#g_t", s6 + .1, rot=2)
    t_let = T("let") - .05
    js(f'tl.fromTo("[id^=g_b]", {{opacity: 0, scale: .3}}, {{opacity: 1, scale: 1, duration: .1, ease: "steps(1)", stagger: .12, immediateRender: false}}, {t_let:.3f});')
    prop("g_chair", CHAIR, "left:150px;top:1300px;width:420px;height:280px")
    js(f'tl.set("#g_chair", {{opacity: 1}}, {s6:.3f});')
    sfx("pop", t_let, -8)
    group("g", s6, s7)
    # ---------- S8: CTA "Comment CHAT for the tool and the setup guide."
    plate(s7, DUR, 29.0, push=(1.0, 1.05))
    strip("h_t", 'COMMENT <span class="hl">"CHAT"</span>', 250, 96, -2)
    card("h_box", '<div class="cbox"><i></i><span id="h_ct">' + "".join(f"<b>{c}</b>" for c in "CHAT") + '</span></div>', "left:90px;top:430px;width:900px;transform:rotate(1deg)")
    card("h_tool", '<div class="fh">chat_clips.py</div><div class="cl"># find the spikes</div><div class="cl"># cut vertical clips</div><div class="cl"># starts 20 s early</div><div class="tag">THE TOOL</div>',
         "left:110px;top:700px;width:420px;transform:rotate(-4deg)", "dark")
    card("h_pdf", '<div class="pbox"><img src="assets/img/guide_cover.jpg"></div><div class="tag">THE GUIDE</div>', "left:600px;top:660px;width:380px;transform:rotate(5deg)")
    js(f'tl.set("#h_t, #h_box", {{opacity: 1}}, {s7:.3f}); tl.set("#h_tool, #h_pdf", {{opacity: 0}}, {s7:.3f});')
    slap("#h_t", s7, rot=-2)
    drop("#h_box", s7 + .15, rot=1)
    tc = T("chat", L(7)) - .1
    js(f'tl.fromTo("#h_ct b", {{opacity: 0}}, {{opacity: 1, duration: .08, ease: "steps(1)", stagger: .08, immediateRender: false}}, {tc:.3f});')
    drop("#h_tool", T("tool", L(7)) - .15, rot=-4, y=200)
    drop("#h_pdf", T("guide", L(7)) - .2, rot=5, y=200)
    for k in range(4):
        sfx("key", tc + k * .08, -4)
    sfx("pop", T("tool", L(7)) - .15, -4)
    sfx("pop", T("guide", L(7)) - .2, -4)
    # ---------- Nyx through the film: one paper sticker, moved shot to shot (stepped), a new pose each time
    poses = [  # (time, x, y, scale, rot, eyes)
        (0.0, 640, 1100, 1.0, 4, "n_e_n"), (s1, 640, 1250, 1.0, -8, "n_e_w"), (s2, 60, 1010, 1.0, 0, "n_e_s"), (s3, 60, 1180, 1.0, -3, "n_e_n"),
        (s4, 60, 1200, 1.0, 3, "n_e_n"), (s5, 60, 1180, 1.0, -4, "n_e_w"), (s6, 380, 1150, .9, -18, "n_e_h"), (s7, 60, 1170, 1.05, 3, "n_e_h")]
    for t, x, y, s, r, e in poses:
        js(f'tl.set("#nyxw", {{x: {x}, y: {y}, scale: {s}, rotation: {r}}}, {t:.3f});')
        face(e, t)
    js(f'tl.fromTo("#nyxw", {{y: 1100 - 40}}, {{y: 1100, duration: .3, ease: "{st(.3)}"}}, 0);')
    js(f'tl.fromTo("#nyx1", {{rotation: 0}}, {{rotation: -8, duration: .17, yoyo: true, repeat: 3, ease: "steps(2)", immediateRender: false}}, {t_need:.3f});')
    face("n_e_h", T("found") - .05)
    face("n_e_s", t_ex)
    js(f'tl.fromTo("#nyxw", {{rotation: -8}}, {{rotation: 8, duration: .17, yoyo: true, repeat: 5, ease: "steps(1)", immediateRender: false}}, {t_ex:.3f});')
    face("n_e_h", T("tiny"))
    face("n_e_h", t_v)
    face("n_e_h", t20 + .4)
    js(f'tl.set("#nyx1 .n_shades", {{opacity: 0}}, 0); tl.set("#nyx1 .n_shades", {{opacity: 1}}, {s6 + .2:.3f}); tl.set("#nyx1 .n_shades", {{opacity: 0}}, {s7:.3f});')
    js(f'tl.fromTo("#nyx1 .n_armR", {{rotation: 0, svgOrigin: "239 246"}}, {{rotation: -150, svgOrigin: "239 246", duration: .25, ease: "{st(.25)}", immediateRender: false}}, {s7 + .2:.3f});')
    js(f'tl.fromTo("#nyx1 .n_armR", {{rotation: -150, svgOrigin: "239 246"}}, {{rotation: -115, svgOrigin: "239 246", duration: .25, yoyo: true, repeat: 7, ease: "steps(2)", immediateRender: false}}, {s7 + .45:.3f});')
    # boil: the sticker wobbles a degree every other drawing
    t = 0.0
    while t < DUR - .1:
        js(f'tl.set("#nyx1", {{x: {R.uniform(-2, 2):.1f}, y: {R.uniform(-2, 2):.1f}}}, {t:.3f});')
        t += 2 / 12
    for tb in (2.0, 6.3, 12.0, 17.6, 24.5, 28.6):
        js(f'tl.fromTo("#nyx1 .n_e_n", {{scaleY: 1, svgOrigin: "150 138"}}, {{scaleY: .1, svgOrigin: "150 138", duration: .08, yoyo: true, repeat: 1, ease: "steps(1)", immediateRender: false}}, {tb:.3f});')
    # a stepped whip of paper between shots
    for t in ts[1:-1]:
        js(f'tl.fromTo("#wipe", {{x: -1300}}, {{x: 1300, duration: .25, ease: "steps(3)", immediateRender: false}}, {t - .12:.3f});')
        sfx("swish", t - .12, -12)
    return ts


def caps():
    KEY = {"ai", "chat", "explodes.", "spike", "clip.", "claude", "free", "spike", "vertical", "late,", "twenty", "thursday.", "chat,"}
    chunks, cur = [], []
    for i, w in enumerate(WORDS):
        cur.append(w)
        nxt = WORDS[i + 1] if i + 1 < len(WORDS) else None
        txt = " ".join(x["w"] for x in cur)
        if nxt is None or nxt["line"] != w["line"] or w["w"][-1] in ".,?!:" or len(txt + " " + (nxt["w"] if nxt else "")) > 20:
            chunks.append(cur)
            cur = []
    for k, ch in enumerate(chunks):
        a = ch[0]["s"] - .04
        b = chunks[k + 1][0]["s"] - .04 if k + 1 < len(chunks) else DUR - .2
        if b - ch[-1]["e"] > .6:
            b = ch[-1]["e"] + .45
        txt = " ".join((f'<em>{H.escape(w["w"])}</em>' if norm(w["w"]) in {norm(x) for x in KEY} else H.escape(w["w"])) for w in ch)
        CAPS.append(f'<div class="cap" id="cp{k}"><b>{txt}</b></div>')
        js(f'tl.fromTo("#cp{k}", {{opacity: 0}}, {{opacity: 1, duration: .08, ease: "steps(1)", immediateRender: false}}, {max(0, a):.3f});')
        js(f'tl.set("#cp{k}", {{opacity: 0}}, {b:.3f});')
    return len(chunks)


CSS = f"""
@font-face {{ font-family: "Montserrat"; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }}
@font-face {{ font-family: "J"; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: {NAVY}; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; font-family: "Montserrat", sans-serif; color: {NAVY}; background: {NAVY}; }}
/* backdrop: the Miami art, native 9:16 so cover never distorts */
.bgw {{ position: absolute; inset: 0; opacity: 0; overflow: hidden; }}
.bgv {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
#tint {{ position: absolute; inset: 0; z-index: 1; background: linear-gradient(180deg, rgba(20,33,61,.25), rgba(20,33,61,.05) 40%, rgba(20,33,61,.45)); }}
#halftone {{ position: absolute; inset: 0; z-index: 1; opacity: .16; background-image: radial-gradient(rgba(20,33,61,.9) 1.6px, transparent 2.2px); background-size: 12px 12px; mix-blend-mode: multiply; }}
/* paper pieces */
.strip {{ position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; max-width: 1000px; z-index: 5; opacity: 0; filter: drop-shadow(8px 10px 0 rgba(20,33,61,.45)); }}
.strip b {{ display: block; padding: 16px 38px 22px; background: {PAPER}; color: {NAVY}; font-weight: 900; line-height: 1; letter-spacing: -.02em; text-transform: uppercase;
  clip-path: {TORN}; transform: scaleX(.92); white-space: nowrap; }}
.hl {{ background: linear-gradient(transparent 52%, {YEL} 52%, {YEL} 92%, transparent 92%); }}
.st {{ position: relative; --s: 0; }}
.st::after {{ content: ""; position: absolute; left: -6%; right: -6%; top: 48%; height: 12px; background: {RED}; transform: scaleX(var(--s)) rotate(-6deg); transform-origin: 0 50%; }}
.card {{ position: absolute; z-index: 4; opacity: 0; filter: drop-shadow(9px 11px 0 rgba(20,33,61,.45)); }}
.cin {{ position: relative; background: {CREAM}; padding: 22px; clip-path: {TORN}; height: 100%; }}
.card.dark .cin {{ background: #182544; color: {CREAM}; }}
.card.cal .cin {{ background: {PAPER}; padding: 0; text-align: center; overflow: hidden; }}
.mk {{ position: absolute; z-index: 6; opacity: 0; overflow: visible; }}
.prop {{ position: absolute; z-index: 6; opacity: 0; filter: drop-shadow(5px 6px 0 rgba(20,33,61,.4)); }}
.prop svg {{ width: 100%; height: 100%; overflow: visible; }}
.cap2 {{ font-family: J; font-size: 22px; margin-top: 10px; text-align: center; }}
.aic {{ display: flex; height: 100%; align-items: center; justify-content: center; text-align: center; font-weight: 900; font-size: 58px; line-height: 1.02; }}
.bub {{ position: absolute; z-index: 5; padding: 12px 24px 14px; background: {PAPER}; border: 5px solid {NAVY}; border-radius: 26px 26px 26px 6px; font-weight: 900; font-size: 46px; opacity: 0;
  box-shadow: 6px 7px 0 rgba(20,33,61,.45); }}
.bub.big {{ position: relative; display: inline-block; opacity: 1; font-size: 120px; left: 50%; transform: translateX(-50%); margin-top: 30px; background: {YEL}; }}
.bub.sm {{ font-size: 34px; }}
/* boxes that keep each source's aspect */
.vbox169 {{ position: relative; width: 100%; aspect-ratio: 16 / 9; overflow: hidden; background: #000; }}
.vbox916 {{ position: relative; width: 100%; aspect-ratio: 9 / 16; overflow: hidden; background: #000; }}
.pbox {{ position: relative; width: 100%; aspect-ratio: 4 / 5; overflow: hidden; }}
.vbox169 video, .vbox916 video, .pbox img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; }}
.live {{ position: absolute; left: 16px; top: 14px; padding: 4px 12px; background: {RED}; color: #fff; font-family: J; font-size: 22px; }}
.cnt {{ text-align: center; }} .cnt b {{ display: block; font-weight: 900; font-size: 110px; line-height: 1; color: {RED}; }} .cnt span {{ font-family: J; font-size: 22px; }}
.gsvg, .tlsvg {{ width: 100%; height: auto; display: block; }}
.note {{ font-weight: 800; font-size: 40px; line-height: 1.15; }}
.fh {{ font-family: J; font-size: 24px; color: {YEL}; padding-bottom: 10px; border-bottom: 2px dashed rgba(241,230,208,.4); margin-bottom: 10px; }}
.cl {{ font-family: J; font-size: 28px; line-height: 1.55; white-space: pre; }}
.bars {{ display: flex; align-items: flex-end; gap: 8px; height: 230px; border-bottom: 5px solid {NAVY}; }}
.bar {{ flex: 1; background: {NAVY}; }}
.sticker {{ position: absolute; left: 640px; top: 900px; z-index: 6; padding: 18px 30px; background: {YEL}; border: 6px solid {NAVY}; font-weight: 900; font-size: 92px; opacity: 0;
  box-shadow: 9px 11px 0 rgba(20,33,61,.45); }}
.calh {{ background: {RED}; color: {PAPER}; font-weight: 900; font-size: 36px; padding: 12px 0; }}
.cald {{ font-weight: 900; font-size: 170px; line-height: 1.08; }}
.calm {{ font-family: J; font-size: 24px; padding-bottom: 18px; }}
.vstack {{ position: absolute; left: 440px; top: 330px; width: 560px; height: 340px; z-index: 4; opacity: 0; }}
.vhs {{ position: absolute; left: 0; width: 540px; height: 96px; background: #182544; color: {CREAM}; padding: 14px 22px; box-shadow: 7px 8px 0 rgba(20,33,61,.45); border-left: 18px solid {RED}; opacity: 0; }}
.vhs b {{ display: block; font-weight: 900; font-size: 32px; }} .vhs span {{ font-family: J; font-size: 20px; color: {YEL}; }}
.cbox {{ display: flex; align-items: center; gap: 22px; padding: 8px 10px; }}
.cbox i {{ width: 70px; height: 70px; border-radius: 50%; background: {VIO}; }}
#h_ct {{ font-weight: 900; font-size: 74px; letter-spacing: .06em; }} #h_ct b {{ display: inline-block; }}
.tag {{ margin-top: 14px; display: inline-block; padding: 8px 18px; background: {YEL}; color: {NAVY}; font-weight: 900; font-size: 28px; }}
/* Nyx as a paper sticker */
#nyxw {{ position: absolute; left: 0; top: 0; width: 360px; z-index: 7; transform-origin: 50% 90%; }}
#nyxw .nyx {{ filter: drop-shadow(0 0 0 #fff) drop-shadow(5px 0 0 {PAPER}) drop-shadow(-5px 0 0 {PAPER}) drop-shadow(0 5px 0 {PAPER}) drop-shadow(0 -5px 0 {PAPER}) drop-shadow(9px 11px 0 rgba(20,33,61,.45)); }}
/* wipe, captions, finish */
#wipe {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; z-index: 8; background: {PAPER}; clip-path: polygon(0 0, 30% 0, 22% 100%, 0 100%); transform: translateX(-1300px); }}
.cap {{ position: absolute; left: 0; right: 0; top: 1610px; text-align: center; z-index: 9; opacity: 0; }}
.cap b {{ display: inline-block; padding: 10px 26px 14px; background: {NAVY}; color: {PAPER}; font-weight: 900; font-size: 54px; letter-spacing: -.01em; box-shadow: 6px 7px 0 rgba(0,0,0,.35); }}
.cap em {{ font-style: normal; color: {YEL}; }}
#fringe {{ position: absolute; inset: 0; z-index: 10; pointer-events: none; box-shadow: inset 6px 0 0 rgba(255,0,80,.18), inset -6px 0 0 rgba(0,200,255,.18), inset 0 0 160px rgba(0,0,0,.45); }}
#grain {{ position: absolute; inset: 0; z-index: 10; opacity: .09; background: url(assets/img/grain.png); mix-blend-mode: overlay; pointer-events: none; }}
.brand {{ position: absolute; right: 40px; top: 120px; z-index: 9; width: 170px; opacity: .9; }}
"""


def main():
    ts = build()
    n = caps()
    js(f'tl.fromTo("#grain", {{x: 0}}, {{x: 6, duration: .083, yoyo: true, repeat: {int(DUR / .083)}, ease: "steps(1)"}}, 0);')
    page = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>AI.NXTLVL: GTA 6 chat already found your clips, Vox cut 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      {"".join(b for b in BODY if 'class="bgw"' in b)}
      <div id="tint"></div><div id="halftone"></div>
      {"".join(b for b in BODY if 'class="bgw"' not in b)}
      <div id="nyxw">{nyx("nyx1")}</div>
      <img class="brand" src="assets/img/logo-wordmark.png">
      {"".join(CAPS)}
      <div id="wipe"></div>
      <div id="fringe"></div><div id="grain"></div>
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
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page)
    json.dump(sorted(SFX, key=lambda e: e["t"]), open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
    json.dump({"dur": DUR, "shots": [round(x, 3) for x in ts]}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
    print(f"wrote index.html: {len(A)} timeline lines, {n} captions, {len(SFX)} sfx, {DUR} s")


if __name__ == "__main__":
    main()
