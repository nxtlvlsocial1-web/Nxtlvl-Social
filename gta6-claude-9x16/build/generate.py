"""GTA 6 x Claude reel, 9:16 (1080x1920, 30 fps), from the client's production brief (cache/brief.pdf).

"GTA 6 drops next week. I made Claude build my own." The visuals are the REAL game Claude built with the open-source
Claude Code Game Studios repo (game/neon-drift-district/, footage/ captured from it, plan/build_log.json with the real
steps and the real 46 min). No GTA or Rockstar assets (the brief's ground rule; the key art the owner shared is not used).
The terminal and folder shots are faithful recreations of that real session: the exact /prototype prompt, the card's
real questions and answers, the files and checks from the log.

The brief's rules, applied: captions 2-4 words at a time, white with orange (#E8603C) on key words, inside 250 px of
safe area top and bottom; a hard cut or punch-in every 1.5-2 s, no slow fades; the on-screen text cards exactly as the
brief writes them; whoosh on cuts, engine / drift sound under gameplay, a bass hit on the ramp jump (build/sfx_mix.py);
the last frame cuts cleanly back into the first so it loops. House style on top: words that pop, glass panels, bursts
on the hits, motion blur on fast moves, a vignette and grain.

python3 build/generate.py  ->  index.html, plan/sfx_events.json
"""
import json
import math
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FW, FH, FPS = 1080, 1920, 30
WORDS = json.load(open(os.path.join(ROOT, "plan", "words.json")))
LOG = json.load(open(os.path.join(ROOT, "plan", "build_log.json")))
DUR = round(WORDS[-1]["t1"] + 2.4, 2)
OR, INK = "#E8603C", "#0b0d12"
A, SFX, H = [], [], []
R = random.Random(19)


def js(s):
    A.append("      " + s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(max(0, t), 3)})


def L(line, i=0, key="t0"):
    return [w for w in WORDS if w["line"] == line][i][key]


# ---------------------------------------------------------------- shots
SHOTS = []          # (t0, t1, kind, payload)


def shot(t0, t1, kind, **kw):
    SHOTS.append((round(t0, 3), round(t1, 3), kind, kw))


def build_timeline():
    g = {k: L(k) for k in ("g01", "g02", "g03", "g04", "g05", "g06", "g07", "g08", "g09", "g10", "g11")}
    step2, step3 = L("g09", 8), L("g09", 13)
    # A: the hook on the real game (drift, combo), then the game's own title card
    shot(0, 1.75, "clip", clip="drive", at=5.2, push=(1.0, 1.08))
    shot(1.75, g["g01"], "clip", clip="drift", at=4.4, push=(1.12, 1.0))
    shot(g["g01"], g["g02"], "clip", clip="title", at=0.0, push=(1.0, 1.1))
    # B / C: the repo, the questions, the brief, the build (recreated from the real log)
    shot(g["g02"], 7.9, "term", scene="clone")
    shot(7.9, g["g03"], "repo")
    shot(g["g03"], 12.4, "term", scene="questions")
    shot(12.4, 14.0, "term", scene="brief")
    shot(14.0, g["g04"], "term", scene="build")
    shot(g["g04"], 17.9, "term", scene="prompt")
    shot(17.9, g["g05"], "term", scene="prompt2")
    # D: double-click the file, the game opens on the drop
    shot(g["g05"], 21.0, "folder")
    shot(21.0, g["g06"], "clip", clip="title", at=0.4, push=(1.15, 1.0))
    # E / F: drifts, combos, the rooftop ramp in slow motion
    shot(g["g06"], 23.8, "clip", clip="drift", at=2.9, push=(1.0, 1.1))     # the game pops DRIFT x2 under the card
    shot(23.8, g["g07"], "clip", clip="ramp", at=1.9, push=(1.08, 1.0))
    shot(g["g07"], 26.7, "clip", clip="ramp", at=3.55, push=(1.0, 1.12))
    shot(26.7, g["g08"], "clip", clip="ramp", at=4.25, push=(1.18, 1.0))
    # G: the whole city from above, the real build time
    shot(g["g08"], g["g09"], "clip", clip="wide", at=0.0, push=(1.0, 1.1))
    # the three steps: paste the repo, describe it, play it
    shot(g["g09"], 32.8, "term", scene="step1")
    shot(32.8, step2, "term", scene="welcome")
    shot(step2, step3, "term", scene="describe")
    shot(step3, g["g10"], "folder", quick=True)
    # A again: the CTA over gameplay, and the loop back into the first frame
    shot(g["g10"], 40.6, "clip", clip="drive", at=8.4, push=(1.0, 1.08))
    shot(40.6, 42.5, "clip", clip="drift", at=6.4, push=(1.1, 1.0))
    shot(42.5, 44.3, "clip", clip="drive", at=0.6, push=(1.0, 1.1))
    shot(44.3, 45.8, "clip", clip="drift", at=1.2, push=(1.08, 1.0))
    shot(45.8, DUR, "clip", clip="drive", at=5.2 - (DUR - 45.8), push=(1.0, 1.0))     # ends exactly where frame 0 starts


# ---------------------------------------------------------------- the on-screen cards (exactly as the brief writes them)
CARDS = [(0, "g01", "GTA 6: <o>NOV 19</o>"), ("g01", "g02", "MINE: <o>TONIGHT</o>"), ("g02", "g03", "<o>FREE</o> ON GITHUB"),
         ("g03", "g04", "DESCRIBE IT <o>-&gt;</o> IT BUILDS IT"), ("g04", "g05", "<o>1</o> PROMPT"), ("g06", "g07", "DRIFT <o>x2</o>"),
         (("g07", 4), "g08", "<o>0</o> LINES OF CODE"), ("g08", "g09", "<o>46</o> MINUTES"), ("g09", ("g09", 8), "STEP <o>1</o>/3"),
         (("g09", 8), ("g09", 13), "STEP <o>2</o>/3"), (("g09", 13), "g10", "STEP <o>3</o>/3"), ("g10", "g11", 'COMMENT <o>"GAME"</o>'),
         ("g11", None, "TAG <o>THEM</o>")]


def tref(x):
    if x == 0:
        return 0.0
    if x is None:
        return DUR
    if isinstance(x, tuple):
        return L(x[0], x[1])
    return L(x)


def cards_html():
    out = []
    for k, (a, b, txt) in enumerate(CARDS):
        t0, t1 = tref(a), tref(b)
        cid = f"cd{k}"
        txt = txt.replace("<o>", '<span class="o">').replace("</o>", "</span>")
        mid = (t0 + t1) / 2
        sh = next((x for x in SHOTS if x[0] <= mid < x[1]), SHOTS[0])
        on_screen = sh[2] != "clip" or sh[3].get("clip") == "title"     # above a terminal / folder, or above the game's own title card
        plain = txt.replace('<span class="o">', "").replace("</span>", "").replace("&gt;", ">")
        st = f"top:{290 if on_screen else 520}px;" + ("opacity:1;" if t0 == 0 else "")
        fs = 92 if len(plain) <= 15 else 66
        out.append(f'<div class="card" id="{cid}" style="{st}"><div class="ci" style="font-size:{fs}px">{txt}</div><i class="cbar" id="{cid}b"></i></div>')
        if t0 > 0:
            js(f'tl.fromTo("#{cid}", {{opacity: 0, scale: 1.5, rotation: {R.choice([-4, 4])}, y: -20}}, {{opacity: 1, scale: 1, rotation: {R.choice([-1.5, 1.5])}, y: 0, duration: .26, ease: "back.out(2.2)", immediateRender: false}}, {t0 - .02:.3f});')
            js(f'tl.fromTo("#{cid}b", {{scaleX: 0}}, {{scaleX: 1, duration: .3, ease: "expo.out", immediateRender: false}}, {t0 + .1:.3f});')
            sfx("stamp", t0)
        else:
            js(f'tl.fromTo("#{cid}", {{scale: 1.06}}, {{scale: 1, duration: .5, ease: "expo.out", immediateRender: false}}, 0);')
        js(f'tl.fromTo("#{cid} .ci", {{scale: 1}}, {{scale: 1.05, duration: {max(.3, t1 - t0):.2f}, ease: "none", immediateRender: false}}, {t0:.3f});')
        if t1 < DUR - .01:
            js(f'tl.set("#{cid}", {{opacity: 0}}, {t1 - .02:.3f});')
    return "".join(out)


# ---------------------------------------------------------------- captions: 2-4 words at a time, key words orange
KEY = {"GTA", "six", "Claude", "free", "GitHub", "Claude", "Game", "Studios.", "prompt,", "neon", "made.", "Drifts.", "Combos.", "rooftop",
       "ramp.", "single", "line", "forty-six", "minutes.", "one:", "two:", "three:", "play", "GAME,", "November", "nineteenth"}


def caption_groups():
    groups, cur = [], []
    for w in WORDS:
        if cur and (w["line"] != cur[-1]["line"] or len(cur) >= 4 or (len(cur) >= 2 and cur[-1]["w"][-1] in ",.:" )):
            groups.append(cur)
            cur = []
        cur.append(w)
    if cur:
        groups.append(cur)
    return groups


def captions_html():
    out = []
    groups = caption_groups()
    for k, gr in enumerate(groups):
        t0 = gr[0]["t0"] - .04
        t1 = groups[k + 1][0]["t0"] - .04 if k + 1 < len(groups) else DUR
        spans = []
        for j, w in enumerate(gr):
            word = w["w"].replace("six", "6") if w["w"].startswith("six") else w["w"]
            word = word.replace("forty-six", "46").replace("nineteenth", "19th")
            cls = "o" if w["w"] in KEY else ""
            spans.append(f'<span class="cw {cls}" id="cp{k}_{j}">{word}</span>')
            js(f'tl.fromTo("#cp{k}_{j}", {{opacity: 0, scale: 1.6, y: 16}}, {{opacity: 1, scale: 1, y: 0, duration: .16, ease: "back.out(3)", immediateRender: false}}, {w["t0"] - .03:.3f});')
        n = sum(len(w["w"]) for w in gr) + len(gr) - 1
        out.append(f'<div class="cap" id="cp{k}"><span class="cbg" style="font-size:{86 if n <= 16 else 72}px">{" ".join(spans)}</span></div>')
        js(f'tl.set("#cp{k}", {{opacity: 1}}, {t0:.3f}); tl.set("#cp{k}", {{opacity: 0}}, {t1:.3f});')
    return "".join(out)


# ---------------------------------------------------------------- terminal scenes (recreated from the real session)
PROMPT = LOG["prompt"]
Q = LOG["questions"]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def chunk_html(h, lid, n=3):
    """Wrap the text (not the tags) of a line in spans of n characters (an entity counts as one) for typing."""
    import re
    out, k = [], 0
    for part in re.split(r"(<[^>]+>)", h):
        if part.startswith("<"):
            out.append(part)
            continue
        chars = re.findall(r"&[#a-z0-9]+;|.", part)
        for i in range(0, len(chars), n):
            out.append(f'<span class="k" id="{lid}k{k}">{"".join(chars[i:i + n])}</span>')
            k += 1
    return "".join(out), k


def term_html(sid, scene, t0, t1):
    head = '<div class="tchrome"><i></i><i></i><i></i><span>~/Claude-Code-Game-Studios</span></div>'
    lines = []          # (html, delay, typed)
    if scene in ("clone", "step1"):
        lines = [(f'<span class="pr">$</span> git clone https://github.com/Donchitos/<b class="o">Claude-Code-Game-Studios</b>', .1, True),
                 ("Cloning into 'Claude-Code-Game-Studios'... <span class=ok>done.</span>", .9, False),
                 ('<span class="pr">$</span> cd Claude-Code-Game-Studios &amp;&amp; <b>claude</b>', 1.2, True)]
    elif scene == "welcome":
        lines = [('<div class="wbox"><b class="o">&#10043;</b> Welcome to <b>Claude Code</b><br><span class="dim">cwd: ~/Claude-Code-Game-Studios</span></div>', .05, False),
                 ('<span class="pr o">&gt;</span> <i class="caret"></i>', .5, False)]
    elif scene == "questions":
        lines = [(f'<span class="pr o">&gt;</span> /prototype {esc(PROMPT[:62])}...', .05, False)]
        for k, q in enumerate(Q[:3]):
            lines.append((f'<span class="q">? {esc(q["asked"].split(":")[0])}?</span>', .35 + k * .55, False))
            lines.append((f'<span class="a">&#8627; {esc(q["answer"])}</span>', .55 + k * .55, False))
    elif scene == "brief":
        lines = [('<span class="ok">&#10003;</span> Wrote <b>design/game-brief.md</b>', .05, False),
                 ('<div class="doc"><b># Game Brief: Neon Drift District</b><br>## In your words<br><span class="dim">a top-down open-world city driving game at night. Neon streets, rain reflections...</span></div>', .35, False),
                 ('<span class="q">? Build it, or change something first?</span>', .9, False), ('<span class="a">&#8627; Build it.</span>', 1.15, False)]
    elif scene == "build":
        files = LOG.get("files", {})
        il = next((v for k, v in (files.items() if isinstance(files, dict) else []) if "index" in k), 1266)
        lines = [('<span class="o">&#9679;</span> Building <b>prototypes/neon-drift-district/</b>', .05, False),
                 (f'  index.html <span class="dim">{il if isinstance(il, int) else 1266} lines</span>  config.js  vendor/three.js', .35, False),
                 ('<span class="o">&#9679;</span> Playing it in a headless browser...', .7, False),
                 ('  <span class="ok">&#10003; boots</span>  <span class="ok">&#10003; 0 errors</span>  <span class="ok">&#10003; keys respond</span>', 1.05, False),
                 ('<span class="ok">&#10003;</span> <b>Neon Drift District</b> is ready. Double-click index.html', 1.45, False)]
    elif scene in ("prompt", "prompt2", "describe"):
        txt = PROMPT[:PROMPT.index("jump.") + 5] + " ..." if scene != "describe" else "a neon open-world city I can drive around"
        typed = scene != "prompt2"
        lines = [(f'<div class="pbox"><span class="pr o">&gt;</span> /prototype <span class="ptxt">{esc(txt)}</span></div>', .05, typed)]
    out = [f'<div class="term" id="{sid}">{head}<div class="tbody">']
    for k, (h, d, typed) in enumerate(lines):
        lid = f"{sid}l{k}"
        if typed:
            h, nk = chunk_html(h, lid)
        out.append(f'<div class="tl" id="{lid}"{" style=opacity:1" if typed else ""}>{h}</div>')
        t = t0 + d
        if typed:
            # typing: reveal with a clip-path sweep, line by line, with key clicks
            dur = min(1.4, max(.5, len(h) / 160)) if scene not in ("prompt", "describe") else min(t1 - t - .2, 1.7)
            for i in range(nk):
                js(f'tl.set("#{lid}k{i}", {{opacity: 1}}, {t + dur * i / max(1, nk - 1):.3f});')
            for i in range(int(dur / .07)):
                sfx("type", t + i * .07)
        else:
            js(f'tl.fromTo("#{lid}", {{opacity: 0, y: 14}}, {{opacity: 1, y: 0, duration: .18, ease: "power3.out", immediateRender: false}}, {t:.3f});')
            sfx("tick", t)
    out.append('</div></div>')
    return "".join(out)


def repo_html(sid):
    return (f'<div class="repo" id="{sid}"><div class="rhead"><span class="dim">Donchitos /</span> <b>Claude-Code-Game-Studios</b> <i class="pub">Public</i></div>'
            '<div class="rbig">Claude Code<br><span class="o">Game Studios</span></div>'
            '<div class="rdesc">Describe a game. Claude Code asks a few questions, writes a one-page brief, and builds a playable browser game from it.</div>'
            '<div class="rtags"><i>MIT license</i><i>free</i><i>/prototype</i></div></div>')


def folder_html(sid):
    icons = [("html", "index.html"), ("js", "config.js"), ("dir", "vendor"), ("dir", "assets")]
    ic = "".join(f'<div class="fi" id="{sid}_{k}"><i class="ico {t}">{"&lt;/&gt;" if t == "html" else ("JS" if t == "js" else "")}</i><span>{n}</span></div>' for k, (t, n) in enumerate(icons))
    return (f'<div class="fold" id="{sid}"><div class="fchrome"><i></i><i></i><i></i><span>neon-drift-district</span></div><div class="fgrid">{ic}</div>'
            f'<svg class="cursor" id="{sid}_cur" viewBox="0 0 24 24"><path d="M4 2l16 11-7 1.5L9.5 22z"/></svg></div>')


# ---------------------------------------------------------------- FX: bursts, flash
FXH = []


def burst(x, y, t, color=OR, n=14, r0=60, r1=240):
    bid = f"bu{len(FXH)}"
    lines = "".join(f'<line x1="{math.cos(a) * r0:.0f}" y1="{math.sin(a) * r0:.0f}" x2="{math.cos(a) * r1:.0f}" y2="{math.sin(a) * r1:.0f}" pathLength="100"/>'
                    for a in [i * 2 * math.pi / n + .15 for i in range(n)])
    FXH.append(f'<svg class="bur" id="{bid}" style="left:{x - 300}px;top:{y - 300}px;stroke:{color}" viewBox="-300 -300 600 600">{lines}<circle class="shw" id="{bid}r" r="70"/></svg>')
    js(f'tl.set("#{bid}", {{opacity: 1}}, {t:.3f}); tl.to("#{bid}", {{opacity: 0, duration: .45, ease: "power2.in"}}, {t + .15:.3f});')
    js(f'tl.fromTo("#{bid} line", {{strokeDashoffset: 100, scale: .6, transformOrigin: "0px 0px"}}, {{strokeDashoffset: -100, scale: 1.25, transformOrigin: "0px 0px", duration: .55, ease: "expo.out", immediateRender: false}}, {t:.3f});')
    js(f'tl.fromTo("#{bid}r", {{scale: .2, opacity: .9, transformOrigin: "0px 0px"}}, {{scale: 3.2, opacity: 0, transformOrigin: "0px 0px", duration: .6, ease: "expo.out", immediateRender: false}}, {t:.3f});')


def flash(t, op=.55):
    js(f'tl.fromTo("#flash", {{opacity: {op}}}, {{opacity: 0, duration: .12, ease: "power2.out", immediateRender: false}}, {t:.3f});')


# ---------------------------------------------------------------- build the shots
STILLS = ["still_city", "still_drift", "still_combo", "still_ramp", "still_speedo"]


def tbg(sid):
    k = int(sid[1:])
    t0, t1 = SHOTS[k][0], SHOTS[k][1]
    js(f'tl.fromTo("#{sid}bg", {{scale: 1.15}}, {{scale: 1.25, duration: {t1 - t0:.3f}, ease: "none", immediateRender: false}}, {t0:.3f});')
    return f'<div class="tbg" id="{sid}bg" style="background-image:url(footage/{STILLS[k % len(STILLS)]}.png)"></div><div class="tdim"></div>'


def shots_html():
    out = []
    for k, (t0, t1, kind, kw) in enumerate(SHOTS):
        sid = f"s{k}"
        d = t1 - t0
        vis = "visibility:visible;" if t0 == 0 else ""
        if kind == "clip":
            out.append(f'<div class="shot" id="{sid}" style="{vis}"><video class="vid" id="{sid}v" src="footage/clip_{kw["clip"]}.mp4" data-start="{t0}" data-duration="{d:.3f}" '
                       f'data-media-start="{kw["at"]:.3f}" data-track-index="{k % 2}" muted playsinline></video></div>')
            a, b = kw["push"]
            js(f'tl.fromTo("#{sid}v", {{scale: {a}}}, {{scale: {b}, duration: {d:.3f}, ease: "power1.inOut", immediateRender: false}}, {t0:.3f});')
        elif kind == "term":
            out.append(f'<div class="shot tshot" id="{sid}" style="{vis}">{tbg(sid)}{term_html(sid + "t", kw["scene"], t0, t1)}</div>')
            js(f'tl.fromTo("#{sid}t", {{scale: 1.0}}, {{scale: 1.07, duration: {d:.3f}, ease: "none", immediateRender: false}}, {t0:.3f});')
        elif kind == "repo":
            out.append(f'<div class="shot tshot" id="{sid}" style="{vis}">{tbg(sid)}{repo_html(sid + "r")}</div>')
            js(f'tl.fromTo("#{sid}r", {{scale: 1.12, rotation: -1}}, {{scale: 1.0, rotation: 0, duration: {d:.3f}, ease: "power2.out", immediateRender: false}}, {t0:.3f});')
        elif kind == "folder":
            fid = sid + "f"
            out.append(f'<div class="shot tshot" id="{sid}" style="{vis}">{tbg(sid)}{folder_html(fid)}</div>')
            tc = t0 + (.25 if kw.get("quick") else .35)
            js(f'tl.fromTo("#{fid}_cur", {{x: 520, y: 520}}, {{x: 0, y: 0, duration: {tc - t0:.2f}, ease: "power3.out", immediateRender: false}}, {t0:.3f});')
            for i in (0, 1):
                js(f'tl.fromTo("#{fid}_0", {{scale: 1}}, {{keyframes: {{scale: [1, .92, 1]}}, duration: .1, immediateRender: false}}, {tc + i * .13:.3f});')
                sfx("click", tc + i * .13)
            js(f'tl.to("#{fid}_0", {{scale: 9, opacity: 0, duration: {t1 - tc - .2:.2f}, ease: "expo.in"}}, {tc + .3:.3f});')
            js(f'tl.to("#{fid}", {{scale: 1.3, duration: {t1 - tc - .2:.2f}, ease: "expo.in"}}, {tc + .3:.3f});')
            sfx("whoosh_big", t1 - .3)
        # the cut: shots swap hard, each cut gets a whoosh and a frame of flash
        js(f'tl.set("#{sid}", {{visibility: "visible"}}, {t0:.3f}); tl.set("#{sid}", {{visibility: "hidden"}}, {t1:.3f});')
        if t0 > 0:
            sfx("whoosh" if k % 2 else "swish", t0 - .05)
            flash(t0, .35 if kind == "clip" else .2)
    return "".join(out)


CSS = f"""
@font-face {{ font-family: "Inter"; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
@font-face {{ font-family: "Mono"; font-weight: 400; src: url("assets/fonts/jetbrains-mono-latin-400-normal.woff2"); }}
@font-face {{ font-family: "Mono"; font-weight: 700; src: url("assets/fonts/jetbrains-mono-latin-700-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: #000; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; background: #05060a; font-family: Inter; color: #fff; }}
.shot {{ position: absolute; inset: 0; visibility: hidden; overflow: hidden; }}
.vid {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
.tshot {{ background: #05060a; }}
.tbg {{ position: absolute; inset: -40px; background-size: cover; background-position: center; filter: blur(22px) saturate(1.3) brightness(.55); }}
.tdim {{ position: absolute; inset: 0; background: radial-gradient(100% 70% at 50% 45%, rgba(5,6,10,.35) 0%, rgba(5,6,10,.8) 100%); }}
.k {{ opacity: 0; }}
.o {{ color: {OR}; }}
.dim {{ color: #8a90a6; }}
.ok {{ color: #4ade80; }}
/* the terminal */
.term {{ position: absolute; left: 50px; right: 50px; top: 470px; min-height: 560px; max-height: 760px; border-radius: 30px; background: rgba(13,15,22,.96); border: 2px solid rgba(255,255,255,.08);
  box-shadow: 0 50px 120px rgba(0,0,0,.6), 0 0 0 1px rgba(232,96,60,.15), 0 0 80px rgba(232,96,60,.12); font-family: Mono; overflow: hidden; }}
.tchrome {{ height: 70px; display: flex; align-items: center; gap: 14px; padding: 0 28px; background: rgba(255,255,255,.04); border-bottom: 1px solid rgba(255,255,255,.06); }}
.tchrome i {{ width: 20px; height: 20px; border-radius: 50%; background: #ff5f57; }} .tchrome i:nth-child(2) {{ background: #febc2e; }} .tchrome i:nth-child(3) {{ background: #28c840; }}
.tchrome span {{ margin-left: 18px; font-size: 28px; color: #8a90a6; }}
.tbody {{ padding: 34px 38px; display: flex; flex-direction: column; gap: 20px; font-size: 34px; line-height: 1.35; color: #e8eaf2; }}
.tl {{ opacity: 0; word-break: break-word; }}
.pr {{ color: #4ade80; font-weight: 700; }}
.q {{ color: #f5f6fa; font-weight: 700; }}
.a {{ color: {OR}; padding-left: 30px; }}
.wbox {{ border: 2px solid {OR}; border-radius: 18px; padding: 28px 30px; font-size: 42px; }}
.doc {{ border-left: 6px solid {OR}; padding: 8px 0 8px 24px; font-size: 31px; color: #cfd3e3; }}
.pbox {{ border: 2px solid rgba(255,255,255,.25); border-radius: 18px; padding: 28px; font-size: 40px; line-height: 1.38; }}
.ptxt {{ color: #fff; }}
.caret {{ display: inline-block; width: 22px; height: 44px; background: {OR}; vertical-align: middle; }}
/* the repo card */
.repo {{ position: absolute; left: 60px; right: 60px; top: 470px; padding: 60px 54px; border-radius: 34px; background: rgba(22,26,36,.95); border: 2px solid rgba(255,255,255,.1);
  box-shadow: 0 50px 120px rgba(0,0,0,.6); }}
.rhead {{ font-family: Mono; font-size: 34px; color: #e8eaf2; display: flex; align-items: center; gap: 14px; flex-wrap: wrap; }}
.pub {{ font-style: normal; font-size: 28px; border: 2px solid rgba(255,255,255,.3); border-radius: 999px; padding: 4px 16px; color: #aab; }}
.rbig {{ margin-top: 44px; font-size: 118px; font-weight: 800; letter-spacing: -.04em; line-height: .98; }}
.rdesc {{ margin-top: 36px; font-size: 40px; font-weight: 600; line-height: 1.35; color: #cfd3e3; }}
.rtags {{ margin-top: 40px; display: flex; gap: 16px; }}
.rtags i {{ font-style: normal; font-family: Mono; font-size: 28px; padding: 10px 22px; border-radius: 999px; background: rgba(232,96,60,.14); color: {OR}; }}
/* the folder */
.fold {{ position: absolute; left: 90px; right: 90px; top: 480px; height: 720px; border-radius: 30px; background: rgba(28,31,42,.97); border: 2px solid rgba(255,255,255,.1);
  box-shadow: 0 50px 120px rgba(0,0,0,.6); transform-origin: 30% 40%; }}
.fchrome {{ height: 70px; display: flex; align-items: center; gap: 14px; padding: 0 28px; border-bottom: 1px solid rgba(255,255,255,.08); }}
.fchrome i {{ width: 20px; height: 20px; border-radius: 50%; background: #ff5f57; }} .fchrome i:nth-child(2) {{ background: #febc2e; }} .fchrome i:nth-child(3) {{ background: #28c840; }}
.fchrome span {{ margin-left: 18px; font-size: 30px; font-weight: 700; color: #cfd3e3; }}
.fgrid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 40px; padding: 50px; }}
.fi {{ display: flex; flex-direction: column; align-items: center; gap: 18px; font-size: 34px; font-weight: 600; color: #e8eaf2; transform-origin: 50% 40%; }}
.fi:first-child span {{ background: #3b82f6; padding: 2px 14px; border-radius: 8px; }}
.ico {{ width: 150px; height: 170px; border-radius: 18px; background: linear-gradient(160deg, #f5f6fa, #c9cddb); display: grid; place-items: center;
  font-style: normal; font-family: Mono; font-weight: 700; font-size: 46px; color: {OR}; }}
.ico.js {{ color: #c79a00; }}
.ico.dir {{ background: linear-gradient(160deg, #7cb2ff, #3b82f6); border-radius: 18px 18px 18px 18px; height: 130px; margin-top: 40px; }}
.cursor {{ position: absolute; left: 300px; top: 330px; width: 70px; height: 70px; fill: #fff; stroke: #000; stroke-width: 1.5; filter: drop-shadow(0 6px 10px rgba(0,0,0,.5)); }}
/* cards (the brief's on-screen text) */
.card {{ position: absolute; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; opacity: 0; z-index: 6; }}
.ci {{ padding: 18px 40px 22px; border-radius: 22px; background: rgba(5,6,10,.82); font-weight: 800; font-size: 92px; letter-spacing: -.03em; line-height: 1;
  white-space: nowrap; box-shadow: 0 20px 60px rgba(0,0,0,.45); }}
.cbar {{ display: block; width: 62%; height: 12px; margin-top: 14px; border-radius: 6px; background: {OR}; transform-origin: left center; transform: scaleX(0); }}
/* captions */
.cap {{ position: absolute; left: 40px; right: 40px; top: 1262px; text-align: center; opacity: 0; z-index: 7; }}
.cbg {{ display: inline-block; min-width: 980px; padding: 8px 26px 14px; border-radius: 24px; background: rgba(5,6,10,.8); box-shadow: 0 16px 50px rgba(0,0,0,.45); }}
.cw {{ display: inline-block; margin: 0 .12em; opacity: 0; font-weight: 800; font-size: 1em; letter-spacing: -.02em; line-height: 1.12; text-transform: uppercase;
  color: #fff; text-shadow: 0 0 2px #000, 0 6px 0 rgba(0,0,0,.85), 0 0 30px rgba(0,0,0,.6); -webkit-text-stroke: 4px #000; paint-order: stroke fill; }}
.cw.o {{ color: {OR}; }}
/* fx */
#fx {{ position: absolute; inset: 0; z-index: 8; pointer-events: none; }}
.bur {{ position: absolute; width: 600px; height: 600px; overflow: visible; opacity: 0; fill: none; stroke-width: 12; stroke-linecap: round; }}
.bur line {{ stroke-dasharray: 100; }} .bur .shw {{ fill: none; stroke-width: 8; }}
#flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 9; mix-blend-mode: screen; }}
#vig {{ position: absolute; inset: 0; z-index: 5; pointer-events: none; background: radial-gradient(120% 85% at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.5) 100%); }}
#grain {{ position: absolute; inset: 0; z-index: 10; pointer-events: none; opacity: .06; background: url(assets/img/grain.png); mix-blend-mode: overlay; }}
"""


def main():
    build_timeline()
    sh = shots_html()
    cards = cards_html()
    caps = captions_html()
    # hits: the combo pops, the ramp launch (bass hit), the landing, the reveal on the drop
    burst(540, 400, L("g06") + .9, color="#ff3df0")
    burst(540, 900, L("g07") + .35, color=OR)
    sfx("bass", L("g07") + .3)
    burst(540, 1050, L("g08") - .25, color="#22d3ee")
    sfx("hit", L("g08") - .25)
    burst(540, 960, L("g05") + 1.06, color=OR, n=18, r0=200, r1=520)
    sfx("hit", L("g05"))
    sfx("rise", L("g05") - 1.2)
    sfx("boost", 0.0)
    sfx("success", 15.05)
    sfx("siren", L("g08") + .1)
    # engine under the gameplay, tyres under the drifts
    for t0, t1, kind, kw in SHOTS:
        if kind == "clip":
            SFX.append({"type": "engine", "t": t0, "len": round(t1 - t0, 3)})
            if kw["clip"] == "drift":
                SFX.append({"type": "squeal", "t": t0 + .2, "len": round(t1 - t0 - .2, 3)})
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>GTA 6 x Claude reel 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      {sh}
      <div id="vig"></div>
      {cards}
      {caps}
      <div id="fx">{"".join(FXH)}</div>
      <div id="flash"></div>
      <div id="grain"></div>
      <audio id="vo" src="assets/audio/vo.wav" data-start="0" data-duration="45.38" data-track-index="2"></audio>
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
    print(f"wrote index.html: {len(SHOTS)} shots, {len(A)} timeline lines, {len(SFX)} sfx cues, {DUR} s")


if __name__ == "__main__":
    main()
