"""AI.NXTLVL: GTA 6 clipping part 2, "chat already found your clips" (1080x1920, 30 fps).

Owner: "recreate this reel and make it better" (a creator's reel: a mascot explains a chat-spike clip finder). Our
version, owner's picks: AI.NXTLVL, our own mascot story, a real tool + PDF guide behind the CTA (CHAT).
  * Nyx, our mascot: a small violet robot whose antenna is the AI.NXTLVL four-point star; visor-face expressions.
  * Set: a Vice City night desk (sunset window, palms, neon), one big monitor whose content changes per beat:
    the live stream (Rockstar's official GTA 6 promo footage, muted: the owner's standing exception) with chat
    exploding, the chat graph spike, Claude building the tool, the pipeline, the 20-second trick, the real terminal
    output of our tool (tool/chat_clips.py) and a folder of vertical GTA clips, the Thursday calendar, the CTA.
  * Better than the reference: real game footage instead of placeholders, the tool and guide actually exist, the
    numbers on screen are the tool's own output format, no other creator's character.
Clock: the VO (build/vo_assemble.py -> plan/words.json, plan/lines.json).
python3 build/generate.py  ->  index.html, plan/edit.json, plan/sfx_events.json
"""
import html as H
import json
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FW, FH, FPS = 1080, 1920, 30
WORDS = json.load(open(os.path.join(ROOT, "plan", "words.json")))
LINES = {l["id"]: l for l in json.load(open(os.path.join(ROOT, "plan", "lines.json")))}
DUR = round(LINES["g09"]["e"] + 1.6, 1)
NIGHT, DEEP, VIOLET, STAR, LAV, PINK, CYAN, ORANGE = "#07050f", "#10022c", "#7f1bf8", "#7a2ffb", "#b687f9", "#ff4fa3", "#3ef0ff", "#ffb36b"
A, SFX, BODY, CAPS = [], [], [], []
R = random.Random(9)


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


def ease(d=.4):
    return "back.out(1.7)"


def show(sel, t, d=.35, y=40, sc=.9, e="back.out(1.7)"):
    js(f'tl.fromTo("{sel}", {{opacity: 0, y: {y}, scale: {sc}}}, {{opacity: 1, y: 0, scale: 1, duration: {d}, ease: "{e}", immediateRender: false}}, {t:.3f});')


def hide(sel, t, d=.18):
    js(f'tl.to("{sel}", {{opacity: 0, duration: {d}}}, {t - d:.3f});')


def star_svg(color=STAR, glow=True):
    f = 'filter="url(#sg)"' if glow else ""
    return f'<path {f} d="M12 0c.8 6.6 4.8 10.8 12 12-7.2 1.2-11.2 5.4-12 12-.8-6.6-4.8-10.8-12-12 7.2-1.2 11.2-5.4 12-12z" fill="{color}"/>'


def nyx(nid):
    """Nyx (viewBox 300x360): ids n_e_n (normal eyes), n_e_w (wide), n_e_h (happy), n_e_s (star eyes), n_e_z (sleepy),
    n_shades, n_armR (right arm, pivot 238 248), n_star (antenna star)"""
    return f"""<svg class="nyx" id="{nid}" viewBox="0 0 300 360">
<defs><filter id="sg" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="hd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a1680"/><stop offset="1" stop-color="#1c0846"/></linearGradient>
<linearGradient id="bd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2e0f6a"/><stop offset="1" stop-color="#170638"/></linearGradient></defs>
<ellipse cx="150" cy="346" rx="96" ry="10" fill="rgba(0,0,0,.35)"/>
<rect x="146" y="20" width="8" height="42" rx="4" fill="{LAV}"/>
<g class="n_star" transform="translate(132 0) scale(1.5)">{star_svg()}</g>
<g class="n_armL"><rect x="44" y="236" width="34" height="78" rx="17" fill="url(#bd)" stroke="{LAV}" stroke-width="3"/></g>
<g class="n_armR"><rect x="222" y="236" width="34" height="78" rx="17" fill="url(#bd)" stroke="{LAV}" stroke-width="3"/></g>
<rect x="84" y="222" width="132" height="112" rx="34" fill="url(#bd)" stroke="{LAV}" stroke-width="3.5"/>
<g transform="translate(138 262) scale(1)">{star_svg(PINK)}</g>
<rect x="34" y="58" width="232" height="170" rx="46" fill="url(#hd)" stroke="{LAV}" stroke-width="4"/>
<rect x="56" y="80" width="188" height="124" rx="32" fill="{NIGHT}"/>
<rect x="64" y="86" width="90" height="16" rx="8" fill="rgba(255,255,255,.08)"/>
<g class="n_e_n" fill="{CYAN}" filter="url(#sg)"><rect x="98" y="118" width="26" height="40" rx="12"/><rect x="176" y="118" width="26" height="40" rx="12"/></g>
<g class="n_e_w" fill="{CYAN}" filter="url(#sg)" opacity="0"><circle cx="111" cy="138" r="24" fill="none" stroke="{CYAN}" stroke-width="9"/><circle cx="189" cy="138" r="24" fill="none" stroke="{CYAN}" stroke-width="9"/><circle cx="111" cy="138" r="7"/><circle cx="189" cy="138" r="7"/></g>
<g class="n_e_h" opacity="0" fill="none" stroke="{CYAN}" stroke-width="10" stroke-linecap="round" filter="url(#sg)"><path d="M92 148 Q111 118 130 148"/><path d="M170 148 Q189 118 208 148"/></g>
<g class="n_e_s" opacity="0"><g transform="translate(93 120) scale(1.5)">{star_svg(PINK)}</g><g transform="translate(171 120) scale(1.5)">{star_svg(PINK)}</g></g>
<g class="n_e_z" opacity="0" stroke="{CYAN}" stroke-width="9" stroke-linecap="round" filter="url(#sg)"><path d="M94 142 h34"/><path d="M172 142 h34"/></g>
<path class="n_m" d="M136 176 Q150 186 164 176" stroke="{LAV}" stroke-width="6" fill="none" stroke-linecap="round"/>
<g class="n_shades" opacity="0"><rect x="70" y="112" width="70" height="44" rx="14" fill="{NIGHT}" stroke="{PINK}" stroke-width="5"/><rect x="160" y="112" width="70" height="44" rx="14" fill="{NIGHT}" stroke="{PINK}" stroke-width="5"/><path d="M140 130 h20" stroke="{PINK}" stroke-width="5"/></g>
</svg>"""


EYES = ["n_e_n", "n_e_w", "n_e_h", "n_e_s", "n_e_z"]


def face(nid, eyes, t):
    for e in EYES:
        js(f'tl.set("#{nid} .{e}", {{opacity: {1 if e == eyes else 0}}}, {t:.3f});')


# ---------------------------------------------------------------- monitor screens (each a layer in #scr)
SCREENS = []


def screen(sid, inner, t0, t1):
    SCREENS.append(f'<div class="sc" id="{sid}">{inner}</div>')
    js(f'tl.fromTo("#{sid}", {{opacity: 0, scale: 1.06}}, {{opacity: 1, scale: 1, duration: .22, ease: "power2.out", immediateRender: false}}, {t0:.3f});')
    js(f'tl.set("#{sid}", {{opacity: 0}}, {t1:.3f});')
    sfx("swish", t0, -10)


CHAT_N = ["hi chat", "what car is that", "lol", "this map is huge", "gg", "first time here", "the graphics omg", "w stream",
          "is this rp?", "drop the build", "nice", "who is driving lol"]
CHAT_X = ["LMAO", "KEKW", "CLIP IT", "NO WAY", "???", "LMAOOO", "W", "BRO", "OMEGALUL", "CLIP THAT", "WHAT", "HAHAHA"]
NAMES = ["nightowl", "vc_runner", "lil_tony", "palmtree", "ghost_77", "mia.b", "turbo", "neonfox", "ricky_r", "sol", "kai", "dex"]
COLS = [CYAN, PINK, ORANGE, LAV, "#7dff9a", "#ffd84a"]


def chat_rows(n, hype, seed):
    r = random.Random(seed)
    out = ""
    for i in range(n):
        msg = r.choice(CHAT_X if hype else CHAT_N)
        out += f'<div class="cm"><b style="color:{r.choice(COLS)}">{r.choice(NAMES)}</b> {H.escape(msg)}</div>'
    return out


def build():
    t_cta = L(9) - .1
    # ---------- the stream (hook + g01 + g02)
    t1 = L(3) - .1
    stream = (f'<video id="sv" src="assets/video/stream.mp4" data-start="0" data-duration="{t1:.3f}" data-media-start="0" data-track-index="0" muted playsinline></video>'
              f'<div class="live"><i></i>LIVE</div><div class="viewers" id="viewers">12.4K watching</div>'
              f'<div class="chat" id="chat"><div class="chh">STREAM CHAT</div><div class="cmw"><div class="cms" id="cmslow">{chat_rows(14, False, 1)}</div>'
              f'<div class="cms" id="cmfast">{chat_rows(40, True, 2)}</div></div></div>'
              f'<div class="ring" id="ring"><b id="ringn">0</b><span>msgs / 10 s</span></div>'
              f'<div class="graph" id="graph"><svg viewBox="0 0 980 150" preserveAspectRatio="none"><path id="gline" d="M0 130 L80 128 L160 126 L240 129 L320 124 L400 127 L480 125 L560 122 L620 118 L660 20 L700 112 L760 124 L840 126 L980 125" '
              f'fill="none" stroke="{CYAN}" stroke-width="6" stroke-linejoin="round"/></svg><div class="flag" id="flag">THAT\'S YOUR CLIP</div><div class="spk" id="spk"></div></div>'
              f'<div class="cards" id="cards"><div class="cardA" id="cardA"><svg viewBox="0 0 24 24" class="ic">{star_svg(LAV, False)}</svg>AI CLIP FINDER<i class="xx" id="xx"></i></div>'
              f'<div class="cardB" id="cardB">CHAT</div></div>')
    screen("s_stream", stream, 0, t1)
    js(f'tl.set("#s_stream", {{opacity: 1}}, 0);')
    # hook cards (frame 0 already shows the AI card; it gets crossed out on "don't need"; CHAT stamps in)
    t_x = T("need") - .05
    js(f'tl.fromTo("#xx", {{scaleX: 0}}, {{scaleX: 1, duration: .2, ease: "power2.out", immediateRender: false}}, {t_x:.3f});')
    js(f'tl.to("#cardA", {{opacity: .45, duration: .2}}, {t_x + .1:.3f});')
    t_chat = T("chat", L(0) + .5) - .05
    js(f'tl.fromTo("#cardB", {{opacity: 0, scale: 2.4, rotation: -14}}, {{opacity: 1, scale: 1, rotation: -6, duration: .3, ease: "back.out(2)", immediateRender: false}}, {t_chat:.3f});')
    sfx("buzz", t_x, -8)
    sfx("stamp", t_chat, -2)
    js(f'tl.to("#cards", {{opacity: 0, duration: .2}}, {L(1) - .2:.3f});')
    # chat: slow scroll, then explosion on "explodes"
    js(f'tl.fromTo("#cmslow", {{y: 0}}, {{y: -260, duration: {T("explodes"):.3f}, ease: "none", immediateRender: false}}, 0);')
    t_ex = T("explodes") - .1
    js(f'tl.set("#cmslow", {{opacity: 0}}, {t_ex:.3f}); tl.set("#cmfast", {{opacity: 1}}, {t_ex:.3f});')
    js(f'tl.fromTo("#cmfast", {{y: 0}}, {{y: -1500, duration: {L(2) - t_ex + .6:.3f}, ease: "power1.in", immediateRender: false}}, {t_ex:.3f});')
    js(f'tl.fromTo("#chat", {{boxShadow: "0 0 0px rgba(255,79,163,0)"}}, {{boxShadow: "0 0 60px rgba(255,79,163,.9)", duration: .3, yoyo: true, repeat: 5, immediateRender: false}}, {t_ex:.3f});')
    js(f'tl.fromTo("#mon", {{x: 0}}, {{x: 9, duration: .05, yoyo: true, repeat: 7, ease: "steps(1)", immediateRender: false}}, {t_ex:.3f});')
    sfx("whoosh", t_ex, -4)
    t_h = T("hundreds") - .1
    js(f'tl.fromTo("#ring", {{opacity: 0, scale: .4}}, {{opacity: 1, scale: 1, duration: .3, ease: "back.out(2)", immediateRender: false}}, {t_h:.3f});')
    js(f'tl.fromTo("#ringn", {{innerText: 0}}, {{innerText: 312, duration: .9, snap: {{innerText: 1}}, ease: "power2.out", immediateRender: false}}, {t_h:.3f});')
    js(f'tl.to("#ring", {{opacity: 0, duration: .2}}, {L(2) - .1:.3f});')
    js(f'tl.fromTo("#viewers", {{color: "#ffffff"}}, {{color: "{PINK}", duration: .2, immediateRender: false}}, {t_ex:.3f});')
    # g02: the graph and the flag
    t2 = L(2) - .1
    js(f'tl.fromTo("#graph", {{opacity: 0, y: 40}}, {{opacity: 1, y: 0, duration: .3, ease: "power2.out", immediateRender: false}}, {t2:.3f});')
    js(f'tl.fromTo("#gline", {{strokeDasharray: 1400, strokeDashoffset: 1400}}, {{strokeDashoffset: 0, duration: .6, ease: "power1.out", immediateRender: false}}, {t2:.3f});')
    show("#flag", T("clip.", L(2)) - .25, y=20)
    js(f'tl.fromTo("#spk", {{opacity: 0, scale: .3}}, {{opacity: 1, scale: 1, duration: .3, ease: "back.out(2.5)", immediateRender: false}}, {t2 + .45:.3f});')
    sfx("ding", T("clip.", L(2)) - .25, -4)
    # ---------- g03: Claude builds the tool
    t3, t4 = L(3) - .1, L(4) - .1
    code = ["# chat_clips.py", "for t, msg in chat:", "    counts[t // 10] += weight(msg)", "spikes = find_spikes(counts)", "for s in spikes:",
            "    cut(video, s.start - 20, vertical=True)"]
    codeh = "".join(f'<div class="cl">{H.escape(c)}</div>' for c in code)
    claude = (f'<div class="aiw"><div class="aih"><i></i><b>Claude</b></div><div class="ub" id="ub">Build me a tool that finds chat spikes and cuts vertical clips.</div>'
              f'<div class="file" id="file"><div class="fh">chat_clips.py</div>{codeh}</div><div class="pill" id="pill">1 FILE · FREE</div></div>')
    screen("s_claude", claude, t3, t4)
    show("#ub", t3 + .1, y=20)
    js(f'tl.fromTo("#file .cl", {{opacity: 0, x: -20}}, {{opacity: 1, x: 0, duration: .12, stagger: .12, immediateRender: false}}, {T("tiny") - .1:.3f});')
    js(f'tl.set("#file", {{opacity: 1}}, {T("tiny") - .15:.3f});')
    show("#pill", T("one", L(3)) - .05, y=20)
    sfx("pop", T("one", L(3)) - .05, -4)
    for k in range(6):
        sfx("key", T("tiny") - .1 + k * .12, -10)
    # ---------- g04/g05: pipeline (chat.json -> bars every 10 s -> spikes -> scissors -> vertical clip)
    t5, t6 = L(5) - .1, L(6) - .1
    bars = "".join(f'<i class="bar{" hot" if k in (7, 15, 22) else ""}" style="height:{R.randint(16, 48) if k not in (7, 15, 22) else R.randint(150, 190)}px"></i>' for k in range(28))
    pipe = (f'<div class="pipe"><div class="app" id="app"><b>FREE APP</b><span>downloads the chat</span></div><div class="arrow">→</div>'
            f'<div class="json" id="json">chat.json</div></div><div class="bars" id="bars">{bars}<div class="blab">COUNT EVERY 10 S</div></div>'
            f'<div class="scis" id="scis">✂</div><div class="vclip" id="vclip"><video id="vcv" src="assets/video/v_flip.mp4" data-start="{t5:.3f}" data-duration="{t6 - t5:.3f}" '
            f'data-media-start="0" data-track-index="1" muted playsinline></video></div><div class="vlab" id="vlab">VERTICAL CLIP</div>')
    screen("s_pipe", pipe, t4, t6)
    show("#app", t4 + .05, y=20)
    show("#json", T("chat", L(4)) - .1, y=20)
    t_cnt = T("counts") - .1
    js(f'tl.fromTo("#bars .bar", {{scaleY: 0}}, {{scaleY: 1, duration: .1, stagger: .05, ease: "power2.out", immediateRender: false}}, {t_cnt:.3f});')
    js(f'tl.set("#bars", {{opacity: 1}}, {t_cnt:.3f});')
    t_sp = T("spikes") - .1
    js(f'tl.fromTo("#bars .hot", {{backgroundColor: "{CYAN}"}}, {{backgroundColor: "{PINK}", duration: .2, stagger: .1, immediateRender: false}}, {t_sp:.3f});')
    js(f'tl.fromTo("#scis", {{opacity: 0, x: -200, rotation: 0}}, {{opacity: 1, x: 0, rotation: -20, duration: .3, ease: "power2.out", immediateRender: false}}, {T("cuts") - .1:.3f});')
    js(f'tl.fromTo("#vclip", {{opacity: 0, scale: .3, rotation: 90}}, {{opacity: 1, scale: 1, rotation: 0, duration: .4, ease: "back.out(1.6)", immediateRender: false}}, {T("vertical") - .15:.3f});')
    show("#vlab", T("vertical") + .1, y=20)
    sfx("snip", T("cuts") - .05, -2)
    sfx("whoosh", T("vertical") - .15, -6)
    # ---------- g06: the trick (chat reacts late -> start 20 s early)
    t7 = L(7) - .1
    trick = (f'<div class="tl" id="tlbar"><i class="axis"></i><div class="mom" id="mom"><b>★</b><span>THE MOMENT</span></div>'
             f'<div class="cht" id="cht"><b></b><span>CHAT REACTS</span></div><div class="win" id="win"><span id="winlab">YOUR CLIP</span></div>'
             f'<div class="minus" id="minus">−20 S</div></div><div class="trickh" id="trickh">THE TRICK</div>')
    screen("s_trick", trick, t6, t7)
    show("#trickh", t6 + .05, y=20)
    show("#mom", t6 + .25, y=-20)
    show("#cht", T("late") - .1, y=-20)
    js(f'tl.fromTo("#win", {{opacity: 0, x: 300}}, {{opacity: 1, x: 300, duration: .2, immediateRender: false}}, {T("late"):.3f});')
    js(f'tl.to("#win", {{x: 0, duration: .5, ease: "power3.inOut"}}, {T("twenty") - .1:.3f});')
    show("#minus", T("twenty") - .1, y=20)
    sfx("rewind", T("twenty") - .1, -4)
    # ---------- g07: one command, a folder of clips (the tool's real output format)
    t8 = L(8) - .1
    out = ["$ python chat_clips.py chat.json stream.mp4", "18,240 chat messages, 6h02m11s of stream", "Top 10 moments (clip starts 20 s before the spike):",
           "  #1  0h41m10s   287 messages  18.4x normal", "  #2  1h27m40s   264 messages  15.9x normal", "  #3  2h03m20s   301 messages  21.2x normal",
           "Done: 10 vertical clips in clips/"]
    term = "".join(f'<div class="tln{" cmd" if i == 0 else ""}{" ok" if i == len(out) - 1 else ""}">{H.escape(o)}</div>' for i, o in enumerate(out))
    thumbs = "".join(f'<div class="th" id="th{k}"><video id="thv{k}" src="assets/video/v_{c}.mp4" data-start="{t7:.3f}" data-duration="{t8 - t7:.3f}" data-media-start="0" '
                     f'data-track-index="{2 + k % 3}" muted playsinline></video></div>' for k, c in enumerate(["cops", "heli", "boat", "scoot", "truck", "dive"]))
    folder = (f'<div class="term" id="term">{term}</div><div class="folder" id="folder"><div class="ftab">clips/</div><div class="fgrid">{thumbs}</div></div>')
    screen("s_term", folder, t7, t8)
    js(f'tl.fromTo("#term .tln", {{opacity: 0}}, {{opacity: 1, duration: .01, stagger: .16, immediateRender: false}}, {t7 + .05:.3f});')
    for k in range(7):
        sfx("key", t7 + .05 + k * .16, -12)
    t_f = T("folder") - .25
    show("#folder", t_f, y=60)
    js(f'tl.fromTo("#folder .th", {{opacity: 0, scale: .4, y: 40}}, {{opacity: 1, scale: 1, y: 0, duration: .25, stagger: .08, ease: "back.out(2)", immediateRender: false}}, {t_f + .15:.3f});')
    for k in range(6):
        sfx("pop", t_f + .15 + k * .08, -12)
    # ---------- g08: Thursday, six-hour streams, you don't watch them
    cal = (f'<div class="cal" id="cal"><div class="calh">THURSDAY</div><div class="cald">19</div><div class="calm">NOV · GTA 6</div></div>'
           f'<div class="streams" id="streams">' + "".join(
               f'<div class="sr"><i class="dot"></i><span>{n}</span><div class="sb"><i id="sbf{k}"></i></div><b>6:00:00</b></div>' for k, n in enumerate(["vice_streamer", "nightowl_rp", "turbo_tv", "mia.plays"]))
           + '</div><div class="nope" id="nope">YOU WATCH: 0 HOURS</div>')
    screen("s_cal", cal, t8, t_cta)
    show("#cal", t8 + .05)
    t_six = T("six-hour") - .1
    js(f'tl.fromTo("#streams .sr", {{opacity: 0, x: -60}}, {{opacity: 1, x: 0, duration: .25, stagger: .08, immediateRender: false}}, {t_six:.3f});')
    for k in range(4):
        js(f'tl.fromTo("#sbf{k}", {{scaleX: 0}}, {{scaleX: 1, duration: 1.4, ease: "power1.inOut", immediateRender: false}}, {t_six + .1 + k * .08:.3f});')
    show("#nope", T("single") - .2, y=20)
    sfx("stamp", T("single") - .2, -4)
    # ---------- g09: CTA
    cta = (f'<div class="cbox" id="cbox"><i class="cav"></i><span class="ct" id="ct">{"".join(f"<b>{c}</b>" for c in "CHAT")}</span><span class="snd"></span></div>'
           f'<div class="gifts"><div class="gift" id="g1"><div class="fh">chat_clips.py</div><div class="cl"># find the spikes</div><div class="cl"># cut vertical clips</div>'
           f'<div class="cl">for t, msg in chat:</div><div class="cl">  counts[t // 10] += 1</div><div class="cl">spikes = top(counts)</div><div class="cl">cut(s - 20, vertical)</div>'
           f'<div class="gtag">THE TOOL</div></div><div class="gift pdf" id="g2"><img src="assets/img/guide_cover.jpg"><div class="gtag">THE GUIDE</div></div></div>')
    screen("s_cta", cta, t_cta, DUR + .1)
    show("#cbox", t_cta + .05, y=30)
    tc = T("chat", L(9)) - .1
    js(f'tl.fromTo("#ct b", {{opacity: 0, y: -20}}, {{opacity: 1, y: 0, duration: .08, stagger: .08, immediateRender: false}}, {tc:.3f});')
    for k in range(4):
        sfx("key", tc + k * .08, -4)
    show("#g1", T("tool", L(9)) - .1, y=80)
    show("#g2", T("guide", L(9)) - .15, y=80)
    sfx("pop", T("tool", L(9)) - .1, -4)
    sfx("pop", T("guide", L(9)) - .15, -4)
    # ---------- headlines (top), per beat
    heads = [("h0", ['YOU DON\'T NEED <span class="acc">AI</span>', 'TO FIND GTA 6 CLIPS'], 0.0, L(1) - .1),
             ("h1", ['CHAT <span class="acc">EXPLODES</span>'], L(1) + .9, L(3) - .1),
             ("h3", ['CLAUDE BUILT', 'A <span class="acc">TINY TOOL</span>'], L(3) - .05, L(4) - .1),
             ("h4", ['IT COUNTS', 'THE <span class="acc">CHAT</span>'], L(4) - .05, L(6) - .1),
             ("h6", ['STARTS <span class="acc">20 S EARLY</span>'], T("twenty") - .1, L(7) - .1),
             ("h7", ['ONE COMMAND.', 'A <span class="acc">FOLDER OF CLIPS</span>'], L(7) - .05, L(8) - .1),
             ("h8", ['GTA 6 DROPS', '<span class="acc">THURSDAY</span>'], L(8) - .05, t_cta - .1),
             ("h9", ['COMMENT <span class="acc">"CHAT"</span>'], t_cta, DUR + .1)]
    for hid, lines, a, b in heads:
        BODY.append(f'<div class="hl" id="{hid}">' + "".join(f'<span class="ln"><span class="in">{l}</span></span>' for l in lines) + '</div>')
        if a <= 0:
            js(f'tl.set("#{hid}", {{opacity: 1}}, 0); tl.fromTo("#{hid}", {{scale: 1.08}}, {{scale: 1, duration: .6, ease: "expo.out"}}, 0);')
        else:
            js(f'tl.set("#{hid}", {{opacity: 1}}, {a:.3f});')
            js(f'tl.fromTo("#{hid} .in", {{yPercent: 110}}, {{yPercent: 0, duration: .4, ease: "expo.out", stagger: .07, immediateRender: false}}, {a:.3f});')
        js(f'tl.set("#{hid}", {{opacity: 0}}, {b:.3f});')
    # ---------- Nyx's acting
    face("nyx1", "n_e_n", 0)
    js(f'tl.fromTo("#nyx1", {{rotation: 0}}, {{rotation: -6, duration: .15, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {t_x:.3f});')   # shakes head
    face("nyx1", "n_e_w", t_ex)
    js(f'tl.fromTo("#nyx1", {{y: 0}}, {{y: -40, duration: .15, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false}}, {t_ex:.3f});')
    face("nyx1", "n_e_s", T("clip.", L(2)) - .25)
    face("nyx1", "n_e_n", t3)
    js(f'tl.fromTo("#nyx1 .n_armR", {{rotation: 0, svgOrigin: "239 246"}}, {{rotation: -25, svgOrigin: "239 246", duration: .12, yoyo: true, repeat: 9, ease: "steps(2)", immediateRender: false}}, {T("tiny") - .1:.3f});')
    face("nyx1", "n_e_h", T("one", L(3)))
    face("nyx1", "n_e_n", t4)
    face("nyx1", "n_e_w", T("twenty") - .1)
    face("nyx1", "n_e_h", t7 + .4)
    face("nyx1", "n_e_n", t8)
    js(f'tl.set("#nyx1 .n_shades", {{opacity: 0}}, 0);')
    js(f'tl.fromTo("#nyx1 .n_shades", {{opacity: 0, y: -120}}, {{opacity: 1, y: 0, duration: .3, ease: "bounce.out", immediateRender: false}}, {T("single") - .25:.3f});')
    sfx("pop", T("single") - .1, -6)
    js(f'tl.set("#nyx1 .n_shades", {{opacity: 0}}, {t_cta:.3f});')
    face("nyx1", "n_e_h", t_cta)
    js(f'tl.fromTo("#nyx1 .n_armR", {{rotation: 0, svgOrigin: "239 246"}}, {{rotation: -150, svgOrigin: "239 246", duration: .3, ease: "back.out(2)", immediateRender: false}}, {t_cta + .2:.3f});')
    js(f'tl.fromTo("#nyx1 .n_armR", {{rotation: -150, svgOrigin: "239 246"}}, {{rotation: -120, svgOrigin: "239 246", duration: .25, yoyo: true, repeat: 7, ease: "sine.inOut", immediateRender: false}}, {t_cta + .5:.3f});')
    # idle: bob + antenna star twinkle all along; blinks
    js(f'tl.fromTo("#nyxw", {{y: 0}}, {{y: -10, duration: .9, yoyo: true, repeat: {int(DUR / .9)}, ease: "sine.inOut", immediateRender: false}}, 0);')
    js(f'tl.fromTo("#nyx1 .n_star", {{scale: 1.5, opacity: 1}}, {{scale: 1.7, opacity: .7, duration: .45, yoyo: true, repeat: {int(DUR / .45)}, ease: "sine.inOut", svgOrigin: "150 18", immediateRender: false}}, 0);')
    for tb in (2.2, 6.0, 12.5, 18.0, 25.5, 31.0):
        if tb < DUR - .5:
            js(f'tl.fromTo("#nyx1 .n_e_n", {{scaleY: 1, svgOrigin: "150 138"}}, {{scaleY: .1, svgOrigin: "150 138", duration: .07, yoyo: true, repeat: 1, ease: "steps(1)", immediateRender: false}}, {tb:.3f});')
    # the room: neon sign flicker, sun drift
    js(f'tl.fromTo("#neon", {{opacity: 1}}, {{opacity: .55, duration: .06, yoyo: true, repeat: 5, ease: "steps(1)", immediateRender: false}}, 3.0);')
    js(f'tl.fromTo("#sun", {{y: 0}}, {{y: 30, duration: {DUR:.2f}, ease: "none", immediateRender: false}}, 0);')
    js(f'tl.fromTo("#steam", {{y: 0, opacity: .8}}, {{y: -30, opacity: 0, duration: 1.4, repeat: {int(DUR / 1.4)}, ease: "power1.out", immediateRender: false}}, 0);')
    js(f'tl.fromTo("#mon", {{scale: 1}}, {{scale: 1.025, duration: {DUR:.2f}, ease: "none", immediateRender: false}}, 0);')
    return t_cta


def caps():
    KEY = {"ai", "chat", "explodes", "spike", "clip.", "claude", "free.", "spikes,", "vertical", "late,", "twenty", "folder", "thursday.", "single", "chat,"}
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
        CAPS.append(f'<div class="cap" id="c{k}"><b>{txt}</b></div>')
        js(f'tl.fromTo("#c{k}", {{opacity: 0, scale: .85}}, {{opacity: 1, scale: 1, duration: .1, ease: "back.out(2)", immediateRender: false}}, {max(0, a):.3f});')
        js(f'tl.set("#c{k}", {{opacity: 0}}, {b:.3f});')
    return len(chunks)


def room():
    palms = "".join(f'<svg class="palm" style="left:{x}px;top:{y}px;width:{w}px;transform:scaleX({s})" viewBox="0 0 120 220"><path d="M60 220 C58 160 62 110 58 70" stroke="{NIGHT}" stroke-width="8" fill="none"/>'
                    f'<path d="M58 70 C30 50 10 60 0 80 C25 62 42 64 58 72 C40 40 20 36 6 40 C30 42 46 52 58 70 C70 36 90 30 110 36 C92 40 74 52 60 70 C86 58 104 64 118 80 C100 64 80 62 60 72Z" fill="{NIGHT}"/></svg>'
                    for x, y, w, s in [(-70, 600, 200, 1), (930, 560, 220, -1), (-20, 360, 150, -1)])
    return (f'<div class="room"><div class="sky"></div><div class="sun" id="sun"></div><div class="sea"></div>{palms}'
            f'<div class="winframe"></div><div class="desk"></div><div class="kbd"></div><div class="mug" id="mug"><i></i></div><div class="steam" id="steam"></div>'
            f'<div class="neon" id="neon">ai.nxtlvl</div></div>')


CSS = f"""
@font-face {{ font-family: "Montserrat"; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }}
@font-face {{ font-family: "Manrope"; font-weight: 200 800; src: url("assets/fonts/manrope.ttf"); }}
@font-face {{ font-family: "J"; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
@font-face {{ font-family: "IS"; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: {NIGHT}; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; font-family: "Manrope", sans-serif; color: #fff; background: {NIGHT}; }}
.acc {{ font-family: "IS", serif; font-weight: 400; color: {LAV}; letter-spacing: 0; text-transform: none; font-size: 1.12em; }}
/* room */
.room {{ position: absolute; inset: 0; }}
.sky {{ position: absolute; left: 0; top: 0; width: {FW}px; height: 1040px; background: linear-gradient(180deg, #0b0320 0%, #2a0a55 22%, #7a1f7a 36%, #ff6f8f 52%, #ffb36b 70%, #ff8f6b 100%); }}
.sun {{ position: absolute; left: 600px; top: 300px; width: 300px; height: 300px; border-radius: 50%; background: linear-gradient(180deg, #ffd86b 0%, #ff4fa3 70%);
  -webkit-mask: repeating-linear-gradient(180deg, #000 0 26px, transparent 26px 34px); }}
.sea {{ position: absolute; left: 0; top: 860px; width: {FW}px; height: 160px; background: linear-gradient(180deg, #3b0f5e, #12042a); }}
.palm {{ position: absolute; height: auto; opacity: .95; }}
.winframe {{ position: absolute; inset: 0 0 auto 0; height: 1040px; box-shadow: inset 0 0 0 26px #160632, inset 0 0 120px rgba(0,0,0,.6); }}
.neon {{ position: absolute; right: 60px; top: 1560px; font-family: "IS", serif; font-size: 70px; color: {PINK}; text-shadow: 0 0 12px {PINK}, 0 0 34px {PINK}; transform: rotate(-4deg); opacity: .9; }}
.kbd {{ position: absolute; left: 390px; top: 1490px; width: 560px; height: 60px; border-radius: 14px; background: linear-gradient(180deg, #2a0d5a, #170638); box-shadow: 0 0 0 3px rgba(182,135,249,.45), 0 0 30px rgba(127,27,248,.4);
  background-image: repeating-linear-gradient(90deg, rgba(182,135,249,.25) 0 34px, transparent 34px 40px); }}
.mug {{ position: absolute; left: 870px; top: 1390px; width: 90px; height: 100px; border-radius: 10px 10px 22px 22px; background: {PINK}; box-shadow: 0 0 24px rgba(255,79,163,.6); }}
.mug i {{ position: absolute; right: -30px; top: 22px; width: 36px; height: 46px; border: 9px solid {PINK}; border-left: 0; border-radius: 0 22px 22px 0; }}
.steam {{ position: absolute; left: 892px; top: 1320px; width: 46px; height: 60px; border-left: 5px solid rgba(255,255,255,.35); border-right: 5px solid rgba(255,255,255,.2); border-radius: 50%; }}
.desk {{ position: absolute; left: 0; top: 1040px; width: {FW}px; height: 880px; background: linear-gradient(180deg, #2a0d5a 0%, #160632 22%, #0b031c 100%);
  box-shadow: inset 0 6px 0 rgba(182,135,249,.5), inset 0 40px 80px rgba(127,27,248,.25); }}
/* monitor */
#mon {{ position: absolute; left: 70px; top: 420px; width: 940px; height: 600px; border-radius: 30px; background: #0d0420; border: 10px solid #1e0a44;
  box-shadow: 0 0 0 3px rgba(182,135,249,.5), 0 30px 80px rgba(0,0,0,.6), 0 0 90px rgba(127,27,248,.4); z-index: 3; transform-origin: 50% 100%; }}
.stand {{ position: absolute; left: 480px; top: 1020px; width: 120px; height: 60px; background: linear-gradient(180deg, #1e0a44, #12052c); border-radius: 0 0 18px 18px; z-index: 2; }}
#scr {{ position: absolute; inset: 0; border-radius: 20px; overflow: hidden; }}
.sc {{ position: absolute; inset: 0; opacity: 0; background: radial-gradient(120% 90% at 50% 0%, #1c0844 0%, {NIGHT} 70%); }}
#sv {{ position: absolute; left: 0; top: 0; width: 700px; height: 600px; object-fit: cover; }}
.live {{ position: absolute; left: 20px; top: 18px; padding: 6px 14px; border-radius: 10px; background: #e5243b; font-family: J; font-size: 24px; display: flex; align-items: center; gap: 8px; }}
.live i {{ width: 12px; height: 12px; border-radius: 50%; background: #fff; }}
.viewers {{ position: absolute; left: 130px; top: 20px; padding: 6px 12px; border-radius: 10px; background: rgba(0,0,0,.55); font-family: J; font-size: 22px; }}
.chat {{ position: absolute; right: 0; top: 0; width: 280px; height: 600px; background: #0c0420; border-left: 3px solid #2a0d5a; overflow: hidden; }}
.chh {{ padding: 14px 16px; font-family: J; font-size: 18px; letter-spacing: .1em; color: {LAV}; border-bottom: 2px solid #2a0d5a; background: #12052c; position: relative; z-index: 2; }}
.cmw {{ position: absolute; left: 0; right: 0; top: 52px; bottom: 0; overflow: hidden; }}
.cms {{ position: absolute; left: 0; right: 0; top: 0; padding: 10px 14px; }}
#cmfast {{ opacity: 0; }}
.cm {{ font-size: 21px; line-height: 1.25; margin-bottom: 9px; font-weight: 600; color: #e9ddff; }}
#cmfast .cm {{ font-weight: 800; font-size: 25px; color: #fff; }}
.ring {{ position: absolute; left: 470px; top: 330px; width: 200px; height: 200px; border-radius: 50%; border: 10px solid {PINK}; background: rgba(7,5,15,.85);
  display: flex; flex-direction: column; align-items: center; justify-content: center; opacity: 0; box-shadow: 0 0 40px {PINK}; }}
.ring b {{ font-family: Montserrat; font-weight: 900; font-size: 64px; line-height: 1; }}
.ring span {{ font-family: J; font-size: 17px; color: {LAV}; }}
.graph {{ position: absolute; left: 0; bottom: 0; width: 700px; height: 170px; background: linear-gradient(180deg, rgba(7,5,15,.2), rgba(7,5,15,.92) 40%); opacity: 0; }}
.graph svg {{ position: absolute; left: 10px; bottom: 10px; width: 680px; height: 130px; }}
.flag {{ position: absolute; left: 330px; top: -40px; padding: 10px 18px; border-radius: 12px; background: {PINK}; font-family: Montserrat; font-weight: 900; font-size: 30px; opacity: 0;
  box-shadow: 0 10px 30px rgba(255,79,163,.6); }}
.spk {{ position: absolute; left: 448px; top: 20px; width: 26px; height: 26px; border-radius: 50%; background: {PINK}; box-shadow: 0 0 0 10px rgba(255,79,163,.3), 0 0 30px {PINK}; opacity: 0; }}
.cards {{ position: absolute; inset: 0; background: rgba(7,5,15,.55); display: flex; align-items: center; justify-content: center; gap: 40px; }}
.cardA, .cardB {{ position: relative; padding: 30px 34px; border-radius: 24px; font-family: Montserrat; font-weight: 900; font-size: 44px; }}
.cardA {{ background: #1e0a44; border: 4px solid {LAV}; display: flex; align-items: center; gap: 14px; }}
.cardA .ic {{ width: 44px; height: 44px; }}
.xx {{ position: absolute; left: -10px; right: -10px; top: 50%; height: 12px; margin-top: -6px; background: {PINK}; border-radius: 6px; transform: rotate(-10deg) scaleX(0); transform-origin: 0 50%; }}
.cardB {{ background: {CYAN}; color: {NIGHT}; font-size: 74px; padding: 24px 44px; border: 6px solid #fff; opacity: 0; box-shadow: 0 0 50px rgba(62,240,255,.7); }}
/* claude */
.aiw {{ position: absolute; inset: 22px; border-radius: 22px; background: #f6f1ea; color: #1d1a17; padding: 22px 26px; }}
.aih {{ display: flex; align-items: center; gap: 12px; font-size: 30px; font-weight: 800; padding-bottom: 14px; border-bottom: 2px solid #e6ddd2; }}
.aih i {{ width: 28px; height: 28px; border-radius: 8px; background: #d97757; }}
.ub {{ margin: 18px 0 0 auto; width: 74%; padding: 16px 22px; border-radius: 22px 22px 6px 22px; background: #1d1a17; color: #fff; font-size: 27px; font-weight: 700; opacity: 0; }}
.file {{ margin-top: 18px; width: 82%; border-radius: 16px; background: #1b1530; color: #e9ddff; padding: 0 0 14px; overflow: hidden; opacity: 0; font-family: J; font-size: 21px; }}
.fh {{ padding: 10px 18px; background: #2a1f4a; color: {LAV}; font-family: J; font-size: 20px; }}
.cl {{ padding: 4px 18px; white-space: pre; }}
.pill {{ position: absolute; right: 30px; bottom: 30px; padding: 12px 22px; border-radius: 999px; background: {CYAN}; color: {NIGHT}; font-family: Montserrat; font-weight: 900; font-size: 30px; opacity: 0; }}
/* pipeline */
.pipe {{ position: absolute; left: 40px; top: 40px; display: flex; align-items: center; gap: 22px; }}
.app {{ padding: 16px 22px; border-radius: 18px; background: #1e0a44; border: 3px solid {LAV}; opacity: 0; }}
.app b {{ display: block; font-family: Montserrat; font-weight: 900; font-size: 30px; }} .app span {{ font-size: 20px; color: {LAV}; }}
.arrow {{ font-size: 50px; color: {LAV}; }}
.json {{ padding: 20px 24px; border-radius: 14px; background: #fff; color: {NIGHT}; font-family: J; font-size: 28px; opacity: 0; box-shadow: 8px 8px 0 {STAR}; }}
.bars {{ position: absolute; left: 40px; bottom: 50px; width: 600px; height: 230px; display: flex; align-items: flex-end; gap: 6px; opacity: 0; border-bottom: 3px solid {LAV}; }}
.bar {{ flex: 1; border-radius: 4px 4px 0 0; background: {CYAN}; transform-origin: 50% 100%; }}
.blab {{ position: absolute; left: 0; bottom: -40px; font-family: J; font-size: 20px; color: {LAV}; }}
.scis {{ position: absolute; left: 620px; top: 300px; font-size: 90px; color: {PINK}; opacity: 0; }}
.vclip {{ position: absolute; right: 60px; top: 70px; width: 230px; height: 409px; border-radius: 20px; overflow: hidden; border: 5px solid #fff; opacity: 0; box-shadow: 0 0 40px rgba(62,240,255,.6); }}
.vclip video {{ width: 100%; height: 100%; object-fit: cover; }}
.vlab {{ position: absolute; right: 52px; top: 500px; font-family: J; font-size: 22px; color: {CYAN}; opacity: 0; }}
/* trick */
.trickh {{ position: absolute; left: 0; right: 0; top: 50px; text-align: center; font-family: Montserrat; font-weight: 900; font-size: 60px; color: {ORANGE}; opacity: 0; }}
.tl {{ position: absolute; left: 60px; right: 60px; top: 190px; height: 300px; }}
.axis {{ position: absolute; left: 0; right: 0; top: 100px; height: 6px; border-radius: 3px; background: {LAV}; }}
.mom {{ position: absolute; left: 230px; top: 20px; text-align: center; opacity: 0; }}
.mom b {{ display: block; font-size: 60px; line-height: 70px; color: {ORANGE}; }} .mom span {{ display: block; margin-top: 30px; font-family: J; font-size: 20px; }}
.cht {{ position: absolute; left: 560px; top: 4px; text-align: center; opacity: 0; }}
.cht b {{ display: block; width: 26px; height: 100px; margin: 0 auto; border-radius: 6px; background: {PINK}; box-shadow: 0 0 30px {PINK}; }}
.cht span {{ display: block; margin-top: 8px; font-family: J; font-size: 20px; }}
.win {{ position: absolute; left: 160px; top: 190px; width: 420px; height: 66px; border-radius: 14px; border: 5px solid {CYAN}; background: rgba(62,240,255,.15); display: flex; align-items: center;
  justify-content: center; opacity: 0; }}
.win span {{ font-family: Montserrat; font-weight: 900; font-size: 26px; color: {CYAN}; }}
.minus {{ position: absolute; left: 170px; top: 270px; font-family: Montserrat; font-weight: 900; font-size: 64px; color: {CYAN}; opacity: 0; }}
/* terminal + folder */
.term {{ position: absolute; left: 24px; top: 24px; width: 600px; height: 560px; border-radius: 18px; background: #05030c; border: 2px solid #2a0d5a; padding: 20px; font-family: J; font-size: 19px; }}
.tln {{ color: #cfc2ee; margin-bottom: 12px; white-space: pre; opacity: 0; }}
.tln.cmd {{ color: {CYAN}; }} .tln.ok {{ color: #7dff9a; }}
.folder {{ position: absolute; right: 22px; top: 60px; width: 330px; height: 500px; border-radius: 18px; background: #f0c24a; padding: 50px 16px 16px; opacity: 0; box-shadow: 0 20px 40px rgba(0,0,0,.4); }}
.ftab {{ position: absolute; left: 0; top: -26px; padding: 8px 22px; border-radius: 14px 14px 0 0; background: #f0c24a; font-family: J; font-size: 22px; color: {NIGHT}; }}
.fgrid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }}
.th {{ height: 200px; border-radius: 10px; overflow: hidden; border: 3px solid #fff; opacity: 0; }}
.th video {{ width: 100%; height: 100%; object-fit: cover; }}
/* calendar */
.cal {{ position: absolute; left: 50px; top: 60px; width: 300px; border-radius: 24px; background: #fff; color: {NIGHT}; text-align: center; overflow: hidden; opacity: 0; box-shadow: 10px 10px 0 {PINK}; }}
.calh {{ background: {PINK}; color: #fff; font-family: Montserrat; font-weight: 900; font-size: 34px; padding: 12px 0; }}
.cald {{ font-family: Montserrat; font-weight: 900; font-size: 170px; line-height: 1.1; }}
.calm {{ font-family: J; font-size: 24px; padding-bottom: 18px; }}
.streams {{ position: absolute; left: 400px; top: 80px; width: 560px; display: flex; flex-direction: column; gap: 22px; }}
.sr {{ display: grid; grid-template-columns: 22px 170px 1fr 110px; align-items: center; gap: 12px; opacity: 0; }}
.sr .dot {{ width: 16px; height: 16px; border-radius: 50%; background: #e5243b; }}
.sr span {{ font-family: J; font-size: 20px; }} .sr b {{ font-family: J; font-size: 22px; color: {ORANGE}; }}
.sb {{ height: 20px; border-radius: 10px; background: #2a0d5a; overflow: hidden; }}
.sb i {{ display: block; height: 100%; background: linear-gradient(90deg, {STAR}, {PINK}); transform-origin: 0 50%; }}
.nope {{ position: absolute; left: 400px; top: 420px; padding: 14px 26px; border-radius: 14px; background: {CYAN}; color: {NIGHT}; font-family: Montserrat; font-weight: 900; font-size: 38px; opacity: 0; }}
/* CTA */
.cbox {{ position: absolute; left: 40px; right: 40px; top: 40px; height: 110px; border-radius: 999px; background: #fff; display: flex; align-items: center; padding: 0 24px; gap: 20px; opacity: 0; }}
.cav {{ width: 66px; height: 66px; border-radius: 50%; background: linear-gradient(135deg, {STAR}, {PINK}); }}
.ct {{ font-family: Montserrat; font-weight: 900; font-size: 56px; color: {NIGHT}; letter-spacing: .06em; }}
.ct b {{ display: inline-block; }}
.snd {{ margin-left: auto; width: 70px; height: 70px; border-radius: 50%; background: {PINK}; }}
.gifts {{ position: absolute; left: 40px; right: 40px; top: 190px; display: flex; gap: 40px; justify-content: center; }}
.gift {{ position: relative; width: 380px; height: 380px; border-radius: 20px; background: #1b1530; border: 4px solid {LAV}; overflow: visible; font-family: J; font-size: 22px; color: #e9ddff; opacity: 0; }}
.gift .fh {{ border-radius: 16px 16px 0 0; }}
.gift.pdf {{ background: none; border: 0; width: 300px; }}
.gift.pdf img {{ width: 300px; height: 375px; border-radius: 16px; border: 4px solid #fff; display: block; }}
.gtag {{ position: absolute; left: 50%; bottom: -24px; transform: translateX(-50%); padding: 8px 18px; border-radius: 999px; background: {CYAN}; color: {NIGHT}; font-family: Montserrat; font-weight: 900; font-size: 24px; white-space: nowrap; }}
/* Nyx */
#nyxw {{ position: absolute; left: 20px; top: 1120px; width: 380px; z-index: 4; }}
.nyx {{ display: block; width: 100%; overflow: visible; transform-origin: 50% 90%; }}
/* headlines */
.hl {{ position: absolute; left: 50px; right: 50px; top: 160px; z-index: 6; opacity: 0; text-align: center; font-family: Montserrat; font-weight: 900; font-size: 74px; line-height: 1.04;
  letter-spacing: -.02em; text-shadow: 0 6px 30px rgba(0,0,0,.6); }}
.hl .ln {{ display: block; overflow: hidden; padding: .03em 0 .08em; }}
.hl .in {{ display: inline-block; }}
/* captions, on the desk to the right of Nyx */
.cap {{ position: absolute; left: 390px; right: 30px; top: 1250px; text-align: center; z-index: 7; opacity: 0; }}
.cap b {{ display: inline-block; padding: 12px 26px 16px; border-radius: 20px; background: rgba(16,2,44,.9); border: 3px solid {STAR}; font-family: Montserrat; font-weight: 800; font-size: 52px;
  letter-spacing: -.01em; box-shadow: 0 0 30px rgba(127,27,248,.5); }}
.cap em {{ font-style: normal; color: {CYAN}; }}
.brand {{ position: absolute; left: 0; right: 0; top: 1760px; text-align: center; z-index: 5; }}
.brand img {{ width: 200px; opacity: .8; }}
#grain {{ position: absolute; inset: 0; opacity: .05; background: url(assets/img/grain.png); mix-blend-mode: overlay; z-index: 9; pointer-events: none; }}
"""


def main():
    t_cta = build()
    n = caps()
    page = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>AI.NXTLVL: GTA 6 chat already found your clips 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      {room()}
      <i class="stand"></i>
      <div id="mon"><div id="scr">{"".join(SCREENS)}</div></div>
      <div id="nyxw">{nyx("nyx1")}</div>
      {"".join(BODY)}
      <div class="brand"><img src="assets/img/logo-wordmark.png"></div>
      {"".join(CAPS)}
      <div id="grain"></div>
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
    json.dump({"dur": DUR, "cta": round(t_cta, 3)}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
    print(f"wrote index.html: {len(A)} timeline lines, {n} captions, {len(SFX)} sfx, {DUR} s")


if __name__ == "__main__":
    main()
