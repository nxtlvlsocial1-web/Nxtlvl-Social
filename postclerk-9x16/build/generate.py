"""Postclerk promo reel ("Stop paying for Metricool."): writes index.html and build/ev.json. 1080x1920, 30 fps, about 42 s.

python3 build/generate.py      (from the project root, after build/voice.py; build/audio.py after this)

A dark, premium SaaS promo in Postclerk's own look (postclerk.io): near-black with indigo glows, Outfit headlines, Inter UI,
JetBrains Mono for the terminal, the leaf mark. Twelve beats follow the owner's script, one scene per line, every one built
around a visual event on a word: the Metricool card stamped STOP PAYING, FREE and the open-source repo, the Postclerk
reveal, platform chips popping on their names into the real Accounts and Calendar screens (the owner's recording, token
blurred by build/safe_clip.py), the composer switching captions per platform, the feed preview filling in, the turn (a
glitch and Metricool crossed out), the real AI assistants screen, the three agents, the one-sentence terminal prompt filling
a week, the Cloudflare deploy clock, and the comment CTA. Word-by-word captions sit between the visuals and the bottom
safe zone. Every sound event is logged to build/ev.json for build/audio.py.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
W = json.load(open(os.path.join(B, "words.json")))
CU = json.load(open(os.path.join(B, "cues.json")))
ICON = json.load(open(os.path.join(B, "icons.json")))
LN = CU["lines"]
DUR = round(LN[-1][1] + 2.2, 2)

BG, PANEL, PANEL2, LINE = "#09090C", "#141419", "#1C1C23", "rgba(255,255,255,.09)"
IND, IND_D, IND_L = "#7C86FF", "#4F39F6", "#B4BAFF"
MINT, RED, AMBER, TXT, MUTED = "#34D399", "#FF5A6E", "#F5B544", "#F4F4F6", "#9A9AA6"
PCOL = {"instagram": "#E1306C", "tiktok": "#25F4EE", "linkedin": "#0A66C2", "youtube": "#FF0033", "facebook": "#1877F2", "threads": "#FFFFFF", "google": "#4285F4"}
PNAME = {"instagram": "Instagram", "tiktok": "TikTok", "linkedin": "LinkedIn", "youtube": "YouTube", "facebook": "Facebook", "threads": "Threads", "google": "Google Business"}
LEAF = "M16 2.5H26.5a3 3 0 0 1 3 3V16A13.5 13.5 0 0 1 16 29.5H5.5a3 3 0 0 1-3-3V16A13.5 13.5 0 0 1 16 2.5Z"


def ws(li, text, nth=1, end=False):
    hits = [w for w in W if w["line"] == li + 1 and re.sub(r"[^a-z0-9]", "", w["w"].lower()).startswith(text.lower())]
    if len(hits) < nth:
        raise SystemExit(f"cue word {text!r} not in line {li + 1}")
    return hits[nth - 1]["e" if end else "s"]


L = [a for a, _ in LN]
E = [b for _, b in LN]
SC = []
for k in range(len(LN)):
    a = 0 if k == 0 else round(L[k] - .14, 3)
    z = DUR if k == len(LN) - 1 else round(L[k + 1] - .14, 3)
    SC.append((a, z))

A, EV, HIDE = [], [], []


def add(js):
    A.append("      " + js)


def ev(t, kind, g=1.0):
    EV.append([round(t, 3), kind, g])


def glyph(name, size, color="#fff"):
    if name == "linkedin":
        return f'<svg viewBox="0 0 24 24" width="{size}" height="{size}"><path fill="{color}" d="{ICON[name]}"/></svg>'
    return f'<svg viewBox="0 0 24 24" width="{size}" height="{size}"><path fill="{color}" d="{ICON[name]}"/></svg>'


def leaf(size, color="#fff", cls=""):
    return f'<svg class="{cls}" viewBox="0 0 32 32" width="{size}" height="{size}"><path fill="{color}" d="{LEAF}"/></svg>'


def chip(name, cls="chip"):
    return f'<div class="{cls}" data-p="{name}"><span class="gi" style="background:{PCOL[name]}">{glyph(name, 34, "#0B0B0F" if name in ("tiktok", "threads") else "#fff")}</span><b>{PNAME[name]}</b></div>'


def window(wid, vids, url="postclerk.io"):
    inner = "".join(vids)
    return (f'<div class="win" id="{wid}"><div class="bar"><i></i><i></i><i></i><span>{url}</span></div>'
            f'<div class="view"><div class="cam" id="{wid}cam">{inner}</div></div></div>')


def video(vid, start, dur, mstart):
    return (f'<video id="{vid}" class="vid" src="assets/video/showcase.mp4" muted playsinline data-start="{round(start, 3)}" '
            f'data-duration="{round(dur, 3)}" data-media-start="{round(mstart, 3)}" data-track-index="3"></video>')


# ---------------------------------------------------------------- scene markup
S = {}
# 1. hook: the Metricool card, stamped
S[1] = f'''<div class="center col" style="top:420px">
  <div class="kick" id="s1k">YOUR SOCIAL MEDIA TOOL</div>
  <div class="mcard" id="mcard"><img src="assets/img/metricool.png" alt="Metricool"/><div class="strike" id="s1strike"></div></div>
  <div class="bill" id="s1bill"><span>monthly bill</span><b id="s1amt">$$$</b></div>
  <div class="stamp" id="s1stamp">STOP<br/>PAYING</div>
</div>'''
# 2. free + open source
S[2] = f'''<div class="center col" style="top:330px">
  <div class="free" id="s2free">FREE</div>
  <div class="zero" id="s2zero"><b>$0</b><span>/ month · open source</span></div>
  <div class="row" id="s2chips"><div class="pill mint">OPEN SOURCE</div><div class="pill">MIT LICENSE</div><div class="pill">SELF-HOST</div></div>
  <div class="repo" id="s2repo"><img src="assets/img/github_repo.png" alt="Postclerk on GitHub"/></div>
</div>'''
# 3. the reveal
S[3] = f'''<div class="center col" style="top:520px">
  <div class="ring" id="s3ring"></div><div class="ring r2" id="s3ring2"></div>
  <div class="mark" id="s3mark">{leaf(220)}</div>
  <div class="word" id="s3word">{"".join(f"<span>{c}</span>" for c in "Postclerk")}</div>
  <div class="tag" id="s3tag">the agentic social media manager</div>
  <div class="sweep" id="s3sweep"></div>
</div>'''
# 4. platforms into the real screens
names = ["instagram", "tiktok", "linkedin", "youtube"]
more = ["facebook", "threads", "google"]
S[4] = f'''<div class="kick k4" id="s4k">7 PLATFORMS · 1 CALENDAR</div><div class="chips4" id="s4chips">{"".join(chip(n, "chip c4") for n in names)}<div class="chip c4 plus" id="s4plus"><b>+3 more</b></div>{"".join(chip(n, "chip c4 m") for n in more)}</div>
  <div class="stagew" id="s4w">{window("w4", [video("v4a", L[3] + .9, ws(3, "all") - .1 - (L[3] + .9), 0.25), video("v4b", ws(3, "all") - .1, SC[3][1] - ws(3, "all") + .1, 4.95)])}</div>
  <div class="label" id="s4lab"><i></i>ONE CALENDAR</div>'''
# 5. composer
COMP = [("instagram", "New menu drop this weekend. Come hungry. #coffee #newmenu", 2200),
        ("linkedin", "We rebuilt our menu from 1,200 customer votes. Here is what we learned.", 3000),
        ("tiktok", "POV: you finally try the new menu", 2200)]
S[5] = f'''<div class="center col" style="top:300px">
  <div class="card comp" id="s5card">
    <div class="ch"><b>New post</b><span>Scheduled · Fri 9:00 AM</span></div>
    <div class="media"><div class="blob b1"></div><div class="blob b2"></div><div class="cup"></div></div>
    <div class="tabs">{"".join(f'<div class="tab" id="s5t{i}"><span class="gi sm" style="background:{PCOL[n]}">{glyph(n, 22, "#0B0B0F" if n == "tiktok" else "#fff")}</span>{PNAME[n]}</div>' for i, (n, _, _) in enumerate(COMP))}<i class="ul" id="s5ul"></i></div>
    <div class="cap">{"".join(f'<p id="s5c{i}">' + "".join(f"<s>{ch}</s>" for ch in c) + '</p>' for i, (_, c, _) in enumerate(COMP))}</div>
    <div class="cnt">{"".join(f'<span id="s5n{i}">{len(c)} / {mx}</span>' for i, (_, c, mx) in enumerate(COMP))}</div>
  </div>
</div>'''
# 6. feed preview
TILE = ["linear-gradient(135deg,#FF9A8B,#FF6A88)", "linear-gradient(135deg,#7C86FF,#4F39F6)", "linear-gradient(135deg,#34D399,#0EA5E9)",
        "linear-gradient(135deg,#F5B544,#F97316)", "linear-gradient(135deg,#A78BFA,#EC4899)", "linear-gradient(135deg,#22D3EE,#6366F1)",
        "linear-gradient(135deg,#FDE68A,#F59E0B)", "linear-gradient(135deg,#F472B6,#8B5CF6)", "linear-gradient(135deg,#86EFAC,#16A34A)"]
S[6] = f'''<div class="center col" style="top:285px">
  <div class="phone" id="s6phone"><div class="notch"></div>
    <div class="ph"><div class="av">{leaf(40)}</div><div class="st"><b>48</b><span>posts</span></div><div class="st"><b>12.4k</b><span>followers</span></div><div class="st"><b>310</b><span>following</span></div></div>
    <div class="pn"><b>your.brand</b><span>Feed preview</span></div>
    <div class="grid">{"".join(f'<div class="tile{" new" if i < 3 else ""}" id="s6g{i}" style="background:{TILE[i]}">{"<em>SCHEDULED</em>" if i < 3 else ""}</div>' for i in range(9))}</div>
  </div>
  <div class="badge" id="s6badge"><i></i>NOT LIVE YET</div>
</div>'''
# 7. the turn
S[7] = f'''<div class="center col" style="top:430px">
  <div class="vs">
    <div class="side" id="s7l"><div class="mcard sm"><img src="assets/img/metricool.png" alt="Metricool"/></div><div class="x" id="s7x">&#10005;</div></div>
    <div class="vsb" id="s7vs">VS</div>
    <div class="side" id="s7r"><div class="pcard">{leaf(64)}<b>Postclerk</b></div></div>
  </div>
  <div class="q" id="s7q">What it doesn't give you</div>
</div>'''
# 8. it connects to your AI (the real screen)
S[8] = f'''<div class="ainode" id="s8node"><span>YOUR AI</span></div><svg class="cable" id="s8cable" viewBox="0 0 1080 400" width="1080" height="400"><path id="s8path" d="M540 20 C 540 140, 540 200, 540 330" stroke="url(#cg)" stroke-width="6" fill="none" stroke-linecap="round"/><defs><linearGradient id="cg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{IND_L}"/><stop offset="1" stop-color="{IND_D}"/></linearGradient></defs></svg>
  <div class="stagew" id="s8w" style="top:610px">{window("w8", [video("v8", L[7] - .14, SC[7][1] - SC[7][0] + .2, 8.4)])}</div>'''
# 9. three agents
S[9] = f'''<div class="center col" style="top:330px">
  <div class="hub" id="s9hub">{leaf(110)}</div>
  <div class="agent" id="s9a0" style="left:-330px;top:-40px"><i></i>Claude Code</div>
  <div class="agent" id="s9a1" style="left:120px;top:-170px"><i></i>Cursor</div>
  <div class="agent" id="s9a2" style="left:170px;top:120px"><i></i>Codex</div>
  <svg class="links" viewBox="-540 -300 1080 700" width="1080" height="700" style="left:-540px;top:-300px"><path id="s9l0" d="M-160 -10 L -40 30"/><path id="s9l1" d="M200 -120 L 50 -10"/><path id="s9l2" d="M230 150 L 60 80"/></svg>
  <div class="mini" id="s9m">{"".join(f'<div class="mpost" id="s9p{i}"><span class="gi sm" style="background:{PCOL[n]}">{glyph(n, 20, "#0B0B0F" if n in ("tiktok", "threads") else "#fff")}</span><b>Draft</b><em>&#10003;</em></div>' for i, n in enumerate(["instagram", "linkedin", "tiktok"]))}</div>
</div>'''
# 10. one sentence fills a week
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
WEEKP = ["instagram", "linkedin", "tiktok", "youtube", "instagram", "threads", "facebook"]
PROMPT = "plan my posts for next week"
S[10] = f'''<div class="center col" style="top:285px">
  <div class="term" id="s10term"><div class="bar"><i></i><i></i><i></i><span>claude</span></div>
    <div class="tl"><b>&gt;</b> <span id="s10txt">{"".join(f"<s>{c}</s>" for c in PROMPT)}</span><u id="s10cur"></u></div>
    <div class="tl dim" id="s10r1">postclerk · creating 7 posts...</div>
  </div>
  <div class="week" id="s10week">{"".join(f'<div class="day"><span>{d}</span><div class="wp" id="s10p{i}"><span class="gi sm" style="background:{PCOL[WEEKP[i]]}">{glyph(WEEKP[i], 18, "#0B0B0F" if WEEKP[i] in ("tiktok", "threads") else "#fff")}</span><em>9:00</em></div></div>' for i, d in enumerate(DAYS))}</div>
  <div class="done" id="s10done">Done.</div>
</div>'''
# 11. deploy
S[11] = f'''<div class="center col" style="top:330px">
  <div class="card dep" id="s11card">
    <div class="ch"><b>Deploy your own copy</b><span>Cloudflare Workers</span></div>
    <div class="clock" id="s11clock"><b id="s11t">0:00</b><span>about two minutes</span></div>
    <div class="pb"><i id="s11bar"></i></div>
    <div class="log">{"".join(f'<p id="s11l{i}"><em>&#10003;</em>{t}</p>' for i, t in enumerate(["Fork the repo", "Connect Cloudflare", "Build and deploy", "Live on your own URL"]))}</div>
  </div>
  <div class="row" id="s11chips"><div class="pill mint">CLOUDFLARE FREE TIER</div><div class="pill">YOUR DATA</div></div>
</div>'''
# 12. CTA
S[12] = f'''<div class="center col" style="top:330px">
  <div class="ctamark" id="s12mark">{leaf(120)}<b>Postclerk</b></div>
  <div class="cbox" id="s12box"><div class="av2"></div><span id="s12typed">{"".join(f"<s>{c}</s>" for c in "POST")}</span><u id="s12cur"></u><i class="send" id="s12send">Post</i></div>
  <div class="ctabig" id="s12big">Comment <b>POST</b></div>
  <div class="ctasub" id="s12sub">and I'll send you the link</div>
</div>'''

# ---------------------------------------------------------------- timeline
for k in range(2, 13):
    HIDE.append(f"#s{k}")


def scene_tl(k):
    a, z = SC[k - 1]
    sid = f"#s{k}"
    if k > 1:
        add(f'tl.set("{sid}",{{autoAlpha:1}},{a});')
    if k > 1:
        add(f'tl.fromTo("{sid}",{{scale:1.12,filter:"blur(18px)"}},{{scale:1,filter:"blur(0px)",duration:.38,ease:"power3.out"}},{a});')
    if k < 12:
        add(f'tl.to("{sid}",{{scale:.94,filter:"blur(14px)",autoAlpha:0,duration:.22,ease:"power2.in"}},{z - .2});')
        add(f'tl.set("{sid}",{{autoAlpha:0}},{z});')


def s1():
    t0, stop, met = 0.0, ws(0, "stop"), ws(0, "metricool")
    HIDE.extend(["#s1stamp", "#s1strike"])
    add(f'tl.fromTo("#mcard",{{scale:1.08}},{{scale:1,duration:.6,ease:"power2.out"}},{t0});')
    add(f'tl.fromTo("#s1bill",{{y:0}},{{y:-6,duration:.6,ease:"sine.inOut"}},{t0});')
    add(f'tl.fromTo("#s1stamp",{{opacity:0,scale:2.6,rotation:-18}},{{opacity:1,scale:1,rotation:-9,duration:.22,ease:"power4.in"}},{stop});')
    add(f'tl.to("#stage",{{keyframes:[{{x:-14,y:8}},{{x:12,y:-6}},{{x:-8,y:4}},{{x:0,y:0}}],duration:.28}},{stop + .22});')
    add(f'tl.fromTo("#s1strike",{{opacity:1,scaleX:0}},{{opacity:1,scaleX:1,duration:.3,ease:"power2.out"}},{met});')
    add(f'tl.to("#mcard",{{filter:"grayscale(1) brightness(.75)",duration:.3}},{met});')
    add(f'tl.to("#s1amt",{{color:"{RED}",duration:.2}},{stop});')
    ev(stop + .2, "stamp"); ev(met, "swipe", .6); ev(0.02, "pop", .6)


def s2():
    a, _ = SC[1]
    free, op = ws(1, "free"), ws(1, "open")
    HIDE.extend(["#s2free", "#s2zero", "#s2chips", "#s2repo"])
    add(f'tl.fromTo("#s2free",{{opacity:0,scale:.4,y:40}},{{opacity:1,scale:1,y:0,duration:.42,ease:"back.out(2.2)"}},{free - .08});')
    add(f'tl.fromTo("#s2zero",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.35,ease:"power3.out"}},{free + .12});')
    add(f'tl.fromTo("#s2chips .pill",{{opacity:0,y:24,scale:.8}},{{opacity:1,y:0,scale:1,duration:.3,stagger:.09,ease:"back.out(2)"}},{op - .05});')
    add(f'tl.fromTo("#s2repo",{{opacity:0,y:160,rotationX:38}},{{opacity:1,y:0,rotationX:14,duration:.55,ease:"power3.out"}},{a + .05});')
    add(f'tl.to("#s2repo",{{rotationX:6,y:-10,duration:{round(SC[1][1] - a - .7, 2)},ease:"sine.inOut"}},{a + .6});')
    add(f'tl.to("#bgtint",{{background:"radial-gradient(60% 40% at 50% 30%, rgba(52,211,153,.22), transparent 70%)",duration:.5}},{free});')
    add(f'tl.to("#bgtint",{{background:"radial-gradient(60% 40% at 50% 30%, rgba(124,134,255,.0), transparent 70%)",duration:.4}},{SC[1][1]});')
    ev(free - .05, "boom"); ev(op, "pops", .6); ev(a, "whoosh", .5)


def s3():
    a, _ = SC[2]
    pc = ws(2, "postclerk")
    HIDE.extend(["#s3mark", "#s3word span", "#s3tag", "#s3ring", "#s3ring2", "#s3sweep"])
    add(f'tl.fromTo("#s3mark",{{opacity:0,scale:0,rotation:-90}},{{opacity:1,scale:1,rotation:0,duration:.5,ease:"back.out(1.8)"}},{pc - .25});')
    add(f'tl.fromTo("#s3ring",{{opacity:.9,scale:.3}},{{opacity:0,scale:2.4,duration:.7,ease:"power2.out"}},{pc - .1});')
    add(f'tl.fromTo("#s3ring2",{{opacity:.6,scale:.3}},{{opacity:0,scale:3.2,duration:.9,ease:"power2.out"}},{pc});')
    add(f'tl.fromTo("#s3word span",{{opacity:0,y:60,rotationX:-80}},{{opacity:1,y:0,rotationX:0,duration:.4,stagger:.035,ease:"power3.out"}},{pc + .05});')
    add(f'tl.fromTo("#s3tag",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.35}},{pc + .45});')
    add(f'tl.fromTo("#s3sweep",{{opacity:1,x:-700}},{{opacity:1,x:700,duration:.6,ease:"power2.inOut"}},{pc + .45});')
    add(f'tl.to("#s3mark",{{y:-12,duration:.8,yoyo:true,repeat:1,ease:"sine.inOut"}},{pc + .5});')
    ev(pc - .2, "rise"); ev(pc, "reveal")


def s4():
    a, z = SC[3]
    HIDE.extend(["#s4chips .chip", "#s4w", "#s4lab"])
    add(f'tl.fromTo("#s4k",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.3,ease:"power3.out"}},{a + .05});')
    ts = [ws(3, "instagram"), ws(3, "tiktok"), ws(3, "linkedin"), ws(3, "youtube")]
    three, allw, cal = ws(3, "three"), ws(3, "all"), ws(3, "calendar")
    pos = [(-250, 0), (250, 0), (-250, 120), (250, 120)]
    for i, t in enumerate(ts):
        add(f'tl.fromTo("#s4chips .c4:nth-child({i + 1})",{{opacity:0,scale:.3,x:{pos[i][0]},y:{pos[i][1] + 60}}},{{opacity:1,scale:1,x:{pos[i][0]},y:{pos[i][1]},duration:.3,ease:"back.out(2.4)"}},{t - .06});')
        ev(t - .04, "pop", .7)
    add(f'tl.fromTo("#s4plus",{{opacity:0,scale:.3,x:0,y:250}},{{opacity:1,scale:1,x:0,y:210,duration:.3,ease:"back.out(2.4)"}},{three - .06});')
    mp = [(-330, 210), (0, 210), (330, 210)]
    for i in range(3):
        add(f'tl.fromTo("#s4chips .m:nth-of-type({i + 6})",{{opacity:0,scale:.3,x:0,y:210}},{{opacity:1,scale:.82,x:{mp[i][0]},y:{mp[i][1]},duration:.32,ease:"back.out(2)"}},{three + .25 + i * .08});')
    add(f'tl.to("#s4plus",{{opacity:0,scale:.5,duration:.2}},{three + .3});')
    ev(three, "pops", .7)
    # chips fly into the window; the window rises with the real Accounts screen, then the calendar
    add(f'tl.fromTo("#s4w",{{opacity:0,y:200,rotationX:30,scale:.85}},{{opacity:1,y:0,rotationX:10,scale:1,duration:.55,ease:"power3.out"}},{L[3] + .9});')
    add(f'tl.to("#s4chips",{{y:-150,scale:.78,duration:.5,ease:"power3.inOut"}},{L[3] + .9});')
    add(f'tl.to("#s4k",{{opacity:0,duration:.25}},{L[3] + .9});')
    add(f'tl.fromTo("#w4cam",{{scale:1.9,xPercent:12,yPercent:30}},{{scale:2.25,xPercent:8,yPercent:28,duration:1.9,ease:"sine.inOut"}},{L[3] + .9});')
    add(f'tl.to("#s4chips",{{opacity:0,scale:.3,y:-120,duration:.35,ease:"power3.in"}},{allw - .15});')
    add(f'tl.set("#w4cam",{{scale:1.15,xPercent:-2,yPercent:2}},{allw - .1});')
    add(f'tl.to("#w4cam",{{scale:1.42,xPercent:-6,yPercent:6,duration:{round(z - allw, 2)},ease:"sine.inOut"}},{allw - .1});')
    add(f'tl.to("#s4w",{{rotationX:0,y:-40,duration:.6,ease:"power2.out"}},{allw - .1});')
    add(f'tl.fromTo("#s4lab",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.3,ease:"back.out(2)"}},{cal - .1});')
    add(f'tl.fromTo("#flash",{{opacity:.55}},{{opacity:0,duration:.35}},{allw - .1});')
    ev(L[3] + .9, "whoosh", .6); ev(allw - .1, "swipe", .7); ev(cal, "ping", .6)


def s5():
    a, z = SC[4]
    HIDE.extend(["#s5card", "#s5c1", "#s5c2", "#s5n1", "#s5n2", "#s5card .cap s"])
    sw = [ws(4, "one"), ws(4, "different"), ws(4, "platform")]
    add(f'tl.fromTo("#s5card",{{opacity:0,y:120,rotationX:24,scale:.9}},{{opacity:1,y:0,rotationX:0,scale:1,duration:.5,ease:"power3.out"}},{a + .02});')
    for i, t in enumerate(sw):
        if i:
            add(f'tl.set(["#s5c{i - 1}","#s5n{i - 1}"],{{opacity:0}},{t});')
            add(f'tl.set(["#s5c{i}","#s5n{i}"],{{opacity:1}},{t});')
            ev(t, "tab", .7)
        add(f'tl.to("#s5ul",{{x:{i * 266},duration:.25,ease:"power3.out"}},{t});')
        add(f'tl.to("#s5t{i}",{{color:"#fff",duration:.15}},{t});')
        if i:
            add(f'tl.to("#s5t{i - 1}",{{color:"{MUTED}",duration:.15}},{t});')
        nxt = sw[i + 1] if i + 1 < len(sw) else z
        st = round(min(.022, (nxt - t - .25) / len(COMP[i][1])), 4)
        add(f'tl.to("#s5c{i} s",{{opacity:1,duration:.01,stagger:{st}}},{t + .02});')
        ev(t + .05, "type", .45)
    add(f'tl.to("#s5card",{{y:-14,duration:{round(z - a - .75, 2)},ease:"sine.inOut"}},{a + .5});')


def s6():
    a, z = SC[5]
    HIDE.extend(["#s6phone", "#s6badge"])
    prev, live = ws(5, "preview"), ws(5, "live")
    add(f'tl.fromTo("#s6phone",{{opacity:0,y:180,rotationY:-25,scale:.9}},{{opacity:1,y:0,rotationY:-8,scale:1,duration:.55,ease:"power3.out"}},{a + .02});')
    add(f'tl.to("#s6phone",{{rotationY:6,duration:{round(z - a - .8, 2)},ease:"sine.inOut"}},{a + .55});')
    for i in range(3, 9):
        add(f'tl.fromTo("#s6g{i}",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.25,ease:"back.out(2)"}},{a + .15 + (i - 3) * .03});')
    for i in range(3):
        add(f'tl.fromTo("#s6g{i}",{{opacity:0,y:-80,scale:1.2}},{{opacity:1,y:0,scale:1,duration:.35,ease:"bounce.out"}},{prev + .1 + i * .16});')
        ev(prev + .12 + i * .16, "drop", .55)
    add(f'tl.fromTo("#s6badge",{{opacity:0,scale:.5}},{{opacity:1,scale:1,duration:.3,ease:"back.out(2.5)"}},{live - .2});')
    ev(live - .2, "ping", .6)


def s7():
    a, z = SC[6]
    HIDE.extend(["#s7l", "#s7r", "#s7vs", "#s7x", "#s7q"])
    but, doesnt = L[6], ws(6, "doesn")
    add(f'tl.fromTo("#glitch",{{opacity:1}},{{opacity:0,duration:.32,ease:"steps(4)"}},{a});')
    add(f'tl.fromTo("#stage",{{x:-30,skewX:8}},{{x:0,skewX:0,duration:.3,ease:"steps(5)"}},{a});')
    add(f'tl.fromTo("#s7l",{{opacity:0,x:-200}},{{opacity:1,x:0,duration:.4,ease:"power3.out"}},{a + .05});')
    add(f'tl.fromTo("#s7r",{{opacity:0,x:200}},{{opacity:1,x:0,duration:.4,ease:"power3.out"}},{a + .12});')
    add(f'tl.fromTo("#s7vs",{{opacity:0,scale:3}},{{opacity:1,scale:1,duration:.3,ease:"power4.in"}},{a + .3});')
    add(f'tl.fromTo("#s7q",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.3}},{a + .4});')
    add(f'tl.fromTo("#s7x",{{opacity:0,scale:2.4}},{{opacity:1,scale:1,duration:.22,ease:"power4.in"}},{doesnt});')
    add(f'tl.to("#s7l .mcard",{{filter:"grayscale(1) brightness(.6)",duration:.25}},{doesnt});')
    add(f'tl.to("#s7r .pcard",{{boxShadow:"0 0 80px rgba(124,134,255,.65)",scale:1.06,duration:.4}},{doesnt + .1});')
    add(f'tl.to("#bgtint",{{background:"radial-gradient(60% 40% at 50% 30%, rgba(255,90,110,.18), transparent 70%)",duration:.3}},{a});')
    add(f'tl.to("#bgtint",{{background:"radial-gradient(60% 40% at 50% 30%, rgba(124,134,255,.0), transparent 70%)",duration:.3}},{z});')
    ev(a, "glitch"); ev(doesnt, "stamp", .8)


def s8():
    a, z = SC[7]
    HIDE.extend(["#s8node", "#s8w", "#s8cable"])
    ai = ws(7, "ai")
    add(f'tl.fromTo("#s8w",{{opacity:0,y:220,rotationX:30,scale:.85}},{{opacity:1,y:0,rotationX:8,scale:1,duration:.5,ease:"power3.out"}},{a + .02});')
    add(f'tl.fromTo("#w8cam",{{scale:1.05,xPercent:-6,yPercent:4}},{{scale:1.6,xPercent:-14,yPercent:14,duration:{round(z - a, 2)},ease:"sine.inOut"}},{a + .02});')
    add(f'tl.fromTo("#s8node",{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:.35,ease:"back.out(2.5)"}},{ai - .25});')
    add(f'tl.set("#s8cable",{{opacity:1}},{ai - .1});')
    add(f'tl.fromTo("#s8path",{{strokeDasharray:400,strokeDashoffset:400}},{{strokeDashoffset:0,duration:.4,ease:"power2.out"}},{ai - .1});')
    add(f'tl.to("#s8node",{{boxShadow:"0 0 0 18px rgba(124,134,255,.0), 0 0 90px rgba(124,134,255,.8)",duration:.5,repeat:1,yoyo:true}},{ai + .2});')
    ev(a + .02, "whoosh", .5); ev(ai - .1, "zap", .8)


def s9():
    a, z = SC[8]
    HIDE.extend(["#s9hub", "#s9a0", "#s9a1", "#s9a2", "#s9l0", "#s9l1", "#s9l2", "#s9m .mpost"])
    ts = [ws(8, "claude"), ws(8, "cursor"), ws(8, "codex")]
    draft, sched = ws(8, "draft"), ws(8, "schedule")
    add(f'tl.fromTo("#s9hub",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2)"}},{a + .02});')
    for i, t in enumerate(ts):
        add(f'tl.fromTo("#s9a{i}",{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:.3,ease:"back.out(2.6)"}},{t - .05});')
        add(f'tl.fromTo("#s9l{i}",{{opacity:1,strokeDasharray:300,strokeDashoffset:300}},{{opacity:1,strokeDashoffset:0,duration:.3}},{t + .1});')
        ev(t - .03, "pop", .7)
    for i in range(3):
        add(f'tl.fromTo("#s9p{i}",{{opacity:0,y:-160,x:{(i - 1) * 140},scale:.5}},{{opacity:1,y:0,x:0,scale:1,duration:.4,ease:"power3.out"}},{draft + i * .12});')
        add(f'tl.fromTo("#s9p{i} em",{{scale:0}},{{scale:1,duration:.25,ease:"back.out(3)"}},{sched + i * .1});')
        add(f'tl.to("#s9p{i} b",{{color:"{MINT}",duration:.1}},{sched + i * .1});')
        ev(sched + i * .1, "tick", .5)
    add(f'tl.set(".mpost b",{{innerHTML:"Scheduled"}},{sched});')
    ev(draft, "whoosh", .4)


def s10():
    a, z = SC[9]
    HIDE.extend(["#s10term", "#s10txt s", "#s10r1", "#s10week", "#s10week .wp", "#s10done"])
    plan, week, done = ws(9, "plan"), ws(9, "week", end=True), ws(9, "done")
    add(f'tl.fromTo("#s10term",{{opacity:0,y:60,scale:.92}},{{opacity:1,y:0,scale:1,duration:.4,ease:"power3.out"}},{a + .02});')
    n = len(PROMPT); step = max(.025, (week - plan) / n)
    add(f'tl.to("#s10txt s",{{opacity:1,duration:.01,stagger:{round(step, 3)}}},{plan - .05});')
    add(f'tl.to("#s10cur",{{opacity:0,duration:.01,repeat:{int((z - a) / .5)},yoyo:true,repeatDelay:.25}},{a});')
    add(f'tl.fromTo("#s10r1",{{opacity:0}},{{opacity:1,duration:.2}},{week + .05});')
    add(f'tl.fromTo("#s10week",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.3}},{week + .05});')
    for i in range(7):
        add(f'tl.fromTo("#s10p{i}",{{opacity:0,y:-60,scale:.6}},{{opacity:1,y:0,scale:1,duration:.22,ease:"back.out(2.5)"}},{week + .12 + i * .07});')
        ev(week + .12 + i * .07, "tick", .45)
    add(f'tl.fromTo("#s10done",{{opacity:0,scale:2.6,rotation:-8}},{{opacity:1,scale:1,rotation:-4,duration:.22,ease:"power4.in"}},{done - .05});')
    add(f'tl.to("#stage",{{keyframes:[{{x:-10,y:6}},{{x:9,y:-5}},{{x:0,y:0}}],duration:.22}},{done + .17});')
    ev(plan - .05, "typing", .5); ev(done + .15, "stamp", .9)


def s11():
    a, z = SC[10]
    HIDE.extend(["#s11card", "#s11chips .pill", "#s11card .log p"])
    free, two = ws(10, "free"), ws(10, "minutes")
    add(f'tl.fromTo("#s11card",{{opacity:0,y:120,rotationX:24}},{{opacity:1,y:0,rotationX:0,duration:.5,ease:"power3.out"}},{a + .02});')
    add(f'tl.fromTo("#s11bar",{{scaleX:0}},{{scaleX:1,duration:{round(two - a, 2)},ease:"power1.inOut"}},{a + .2});')
    add(f'tl.fromTo(CLK,{{v:0}},{{v:118,duration:{round(two - a, 2)},ease:"power1.inOut",onUpdate:()=>{{const s=Math.round(CLK.v);document.getElementById("s11t").textContent=Math.floor(s/60)+":"+String(s%60).padStart(2,"0");}}}},{a + .2});')
    for i in range(4):
        t = a + .35 + (two - a - .2) * (i + 1) / 4.4
        add(f'tl.fromTo("#s11l{i}",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.25,ease:"power3.out"}},{t});')
        ev(t, "tick", .5)
    add(f'tl.fromTo("#s11chips .pill",{{opacity:0,y:20,scale:.8}},{{opacity:1,y:0,scale:1,duration:.3,stagger:.1,ease:"back.out(2)"}},{free - .05});')
    add(f'tl.to("#s11clock b",{{color:"{MINT}",duration:.2}},{two + .2});')
    ev(free, "pops", .6); ev(two + .2, "chime", .7)


def s12():
    a, z = SC[11]
    HIDE.extend(["#s12mark", "#s12box", "#s12typed s", "#s12big", "#s12sub"])
    com, post = ws(11, "comment"), ws(11, "post")
    add(f'tl.fromTo("#s12mark",{{opacity:0,y:-40,scale:.8}},{{opacity:1,y:0,scale:1,duration:.45,ease:"back.out(2)"}},{a + .02});')
    add(f'tl.fromTo("#s12box",{{opacity:0,y:60}},{{opacity:1,y:0,duration:.4,ease:"power3.out"}},{a + .15});')
    add(f'tl.to("#s12typed s",{{opacity:1,duration:.01,stagger:.09}},{post - .1});')
    add(f'tl.to("#s12cur",{{opacity:0,duration:.01,repeat:{int((z - a) / .5)},yoyo:true,repeatDelay:.25}},{a});')
    add(f'tl.to("#s12send",{{background:"{IND_D}",color:"#fff",scale:1.08,duration:.2}},{post + .35});')
    add(f'tl.fromTo("#s12big",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2.2)"}},{com});')
    add(f'tl.fromTo("#s12sub",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.35}},{post + .4});')
    add(f'tl.to("#s12mark svg",{{rotation:360,duration:1.2,ease:"power2.inOut"}},{E[11] + .2});')
    ev(com, "pop", .7); ev(post - .1, "typing", .5); ev(post + .35, "click", .8); ev(E[11] + .3, "chime", .6)


def captions():
    groups, cur = [], []
    for w in W:
        cur.append(w)
        if len(cur) >= 4 or re.search(r"[.,?!:]$", w["w"]):
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    out = []
    for gi, g in enumerate(groups):
        a, z = g[0]["s"] - .05, g[-1]["e"] + .12
        if gi + 1 < len(groups): z = min(z, groups[gi + 1][0]["s"] - .14)
        spans = "".join(f'<span id="w{gi}_{j}">{w["w"]}</span> ' for j, w in enumerate(g))
        out.append(f'<div class="cg" id="cg{gi}">{spans}</div>')
        HIDE.append(f"#cg{gi}")
        add(f'tl.fromTo("#cg{gi}",{{opacity:0,y:24,scale:.92}},{{opacity:1,y:0,scale:1,duration:.16,ease:"power3.out"}},{round(a, 3)});')
        add(f'tl.to("#cg{gi}",{{opacity:0,duration:.06}},{round(z, 3)});')
        for j, w in enumerate(g):
            hot = re.sub(r"[^a-z]", "", w["w"].lower()) in ("metricool", "free", "postclerk", "calendar", "composer", "preview", "ai", "sentence", "done", "cloudflare", "post", "open", "source")
            add(f'tl.to("#w{gi}_{j}",{{color:"{IND_L if not hot else MINT}",scale:1.08,duration:.08}},{round(w["s"], 3)});')
            add(f'tl.to("#w{gi}_{j}",{{color:"#fff",scale:1,duration:.12}},{round(w["e"], 3)});')
    return "".join(out)


CSS = f"""
@font-face {{ font-family: "Inter"; font-weight: 100 900; src: url("assets/fonts/inter.woff2") format("woff2"); }}
@font-face {{ font-family: "Outfit"; font-weight: 100 900; src: url("assets/fonts/outfit.woff2") format("woff2"); }}
@font-face {{ font-family: "JBM"; font-weight: 100 800; src: url("assets/fonts/jbmono.woff2") format("woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {BG}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: {BG}; font-family: "Inter", sans-serif; color: {TXT}; }}
#bg {{ position: absolute; inset: 0; background: radial-gradient(70% 45% at 50% 22%, rgba(79,57,246,.28), transparent 70%), radial-gradient(60% 40% at 80% 80%, rgba(124,134,255,.14), transparent 70%), {BG}; }}
#bg .grid {{ position: absolute; inset: -40px; background-image: radial-gradient(rgba(255,255,255,.07) 1.4px, transparent 1.6px); background-size: 44px 44px; }}
#bg .blob {{ position: absolute; width: 900px; height: 900px; border-radius: 50%; filter: blur(140px); opacity: .45; }}
#bgtint {{ position: absolute; inset: 0; }}
#stagewrap {{ position: absolute; inset: 0; }}
#stage {{ position: absolute; inset: 0; transform-origin: 50% 45%; }}
.scene {{ position: absolute; inset: 0; perspective: 1400px; transform-origin: 50% 40%; }}
.center {{ position: absolute; left: 540px; width: 0; }}
.col {{ display: flex; flex-direction: column; align-items: center; }}
.col > * {{ flex: none; }}
.kick {{ font: 700 30px/1 "Inter"; letter-spacing: 6px; color: {MUTED}; white-space: nowrap; margin-bottom: 36px; }}
.mcard {{ position: relative; background: #fff; border-radius: 34px; padding: 54px 70px; box-shadow: 0 30px 80px rgba(0,0,0,.55); }}
.mcard img {{ display: block; width: 520px; height: auto; image-rendering: auto; }}
.mcard.sm {{ padding: 30px 38px; border-radius: 26px; }} .mcard.sm img {{ width: 250px; }}
.strike {{ position: absolute; left: 30px; right: 30px; top: 50%; height: 12px; margin-top: -6px; background: {RED}; border-radius: 8px; transform-origin: 0 50%; transform: rotate(-6deg); }}
.bill {{ margin-top: 40px; display: flex; gap: 22px; align-items: baseline; white-space: nowrap; }}
.bill span {{ font: 500 34px/1 "Inter"; color: {MUTED}; }} .bill b {{ font: 800 64px/1 "Outfit"; color: #fff; }}
.stamp {{ position: absolute; top: 470px; left: -250px; width: 520px; text-align: center; font: 900 116px/.92 "Outfit"; color: {RED}; border: 12px solid {RED}; border-radius: 28px; padding: 26px 10px; background: rgba(20,6,10,.55); letter-spacing: 2px; text-shadow: 0 0 40px rgba(255,90,110,.5); }}
.free {{ font: 900 290px/.9 "Outfit"; letter-spacing: -6px; background: linear-gradient(180deg, #A7F3D0, {MINT} 60%, #059669); -webkit-background-clip: text; background-clip: text; color: transparent; filter: drop-shadow(0 0 60px rgba(52,211,153,.45)); white-space: nowrap; }}
.zero {{ display: flex; gap: 18px; align-items: baseline; white-space: nowrap; margin-top: 6px; }}
.zero b {{ font: 800 76px/1 "Outfit"; }} .zero span {{ font: 500 36px/1 "Inter"; color: {MUTED}; }}
.row {{ display: flex; gap: 18px; margin-top: 40px; white-space: nowrap; }}
.pill {{ font: 700 28px/1 "Inter"; letter-spacing: 3px; padding: 18px 26px; border-radius: 999px; border: 2px solid {LINE}; background: rgba(255,255,255,.04); color: #fff; }}
.pill.mint {{ border-color: rgba(52,211,153,.6); color: {MINT}; background: rgba(52,211,153,.08); }}
.repo {{ margin-top: 54px; transform-origin: 50% 0; }}
.repo img {{ display: block; width: 820px; border-radius: 22px; box-shadow: 0 40px 100px rgba(0,0,0,.6), 0 0 0 2px rgba(255,255,255,.08); }}
.ring {{ position: absolute; top: 0; width: 300px; height: 300px; margin-left: -150px; left: 0; border-radius: 50%; border: 6px solid {IND}; }}
.ring.r2 {{ border-color: {IND_L}; border-width: 3px; }}
.mark {{ width: 300px; height: 300px; display: grid; place-items: center; filter: drop-shadow(0 0 50px rgba(124,134,255,.7)); }}
.word {{ margin-top: 40px; font: 700 150px/1 "Outfit"; letter-spacing: -3px; white-space: nowrap; perspective: 800px; }}
.word span {{ display: inline-block; }}
.tag {{ margin-top: 26px; font: 500 38px/1 "Inter"; color: {MUTED}; white-space: nowrap; }}
.sweep {{ position: absolute; top: 290px; width: 260px; height: 220px; left: -130px; background: linear-gradient(90deg, transparent, rgba(255,255,255,.35), transparent); transform: skewX(-20deg); mix-blend-mode: overlay; }}
.chips4 {{ position: absolute; left: 540px; top: 470px; width: 0; height: 0; }}
.k4 {{ position: absolute; left: 540px; top: 300px; transform: translateX(-50%); font-size: 34px; color: {IND_L}; }}
.chip {{ position: absolute; left: 0; top: 0; transform: translate(-50%,-50%); display: flex; align-items: center; gap: 16px; padding: 16px 28px 16px 16px; border-radius: 999px; background: {PANEL2}; border: 2px solid {LINE}; white-space: nowrap; box-shadow: 0 16px 40px rgba(0,0,0,.45); }}
.chip b {{ font: 700 38px/1 "Inter"; }}
.chip.plus {{ padding: 18px 30px; background: {IND_D}; border-color: {IND}; }}
.gi {{ display: grid; place-items: center; width: 58px; height: 58px; border-radius: 16px; }}
.gi.sm {{ width: 40px; height: 40px; border-radius: 12px; }}
.stagew {{ position: absolute; left: 60px; top: 560px; width: 960px; perspective: 1600px; }}
.win {{ width: 960px; border-radius: 26px; overflow: hidden; background: #0d0d10; box-shadow: 0 40px 120px rgba(0,0,0,.7), 0 0 0 2px rgba(255,255,255,.1), 0 0 80px rgba(79,57,246,.25); transform-style: preserve-3d; }}
.win .bar {{ height: 52px; display: flex; align-items: center; gap: 10px; padding: 0 20px; background: #17171c; border-bottom: 1px solid {LINE}; }}
.win .bar i {{ width: 14px; height: 14px; border-radius: 50%; background: #3a3a44; }} .win .bar i:nth-child(1) {{ background: #FF5F57; }} .win .bar i:nth-child(2) {{ background: #FEBC2E; }} .win .bar i:nth-child(3) {{ background: #28C840; }}
.win .bar span {{ margin-left: 18px; font: 500 22px/1 "Inter"; color: {MUTED}; background: #0f0f13; padding: 8px 18px; border-radius: 10px; }}
.win .view {{ position: relative; width: 960px; height: 469px; overflow: hidden; }}
.win .cam {{ position: absolute; inset: 0; transform-origin: 50% 50%; }}
.vid {{ position: absolute; left: 0; top: 0; width: 960px; height: 469px; object-fit: cover; }}
.label {{ position: absolute; left: 540px; top: 1130px; transform: translateX(-50%); display: flex; align-items: center; gap: 14px; font: 800 34px/1 "Inter"; letter-spacing: 5px; padding: 18px 30px; border-radius: 999px; background: {IND_D}; white-space: nowrap; box-shadow: 0 0 50px rgba(79,57,246,.6); }}
.label i {{ width: 14px; height: 14px; border-radius: 50%; background: #fff; }}
.card {{ background: {PANEL}; border: 2px solid {LINE}; border-radius: 34px; box-shadow: 0 40px 100px rgba(0,0,0,.6); }}
.card .ch {{ display: flex; justify-content: space-between; align-items: baseline; padding: 30px 36px 18px; white-space: nowrap; }}
.card .ch b {{ font: 700 40px/1 "Outfit"; }} .card .ch span {{ font: 500 26px/1 "Inter"; color: {MUTED}; }}
.comp {{ width: 900px; transform-origin: 50% 0; }}
.comp .media {{ position: relative; margin: 0 36px; height: 330px; border-radius: 22px; overflow: hidden; background: linear-gradient(135deg, #2b1d14, #6b3b1f 60%, #c47a3a); }}
.comp .blob {{ position: absolute; border-radius: 50%; filter: blur(20px); }}
.comp .b1 {{ width: 300px; height: 300px; left: -60px; top: -80px; background: rgba(255,214,170,.35); }}
.comp .b2 {{ width: 260px; height: 260px; right: -40px; bottom: -90px; background: rgba(255,140,80,.4); }}
.comp .cup {{ position: absolute; left: 50%; top: 50%; width: 170px; height: 150px; margin: -80px 0 0 -85px; border-radius: 0 0 70px 70px; background: #f6efe6; box-shadow: 40px 0 0 -18px transparent, inset 0 -18px 0 rgba(0,0,0,.08); }}
.comp .cup::after {{ content: ""; position: absolute; right: -58px; top: 26px; width: 60px; height: 70px; border: 16px solid #f6efe6; border-left: none; border-radius: 0 40px 40px 0; }}
.tabs {{ position: relative; display: flex; margin: 26px 36px 0; border-bottom: 2px solid {LINE}; }}
.tab {{ width: 266px; display: flex; align-items: center; gap: 12px; padding: 18px 6px 22px; font: 700 30px/1 "Inter"; color: {MUTED}; white-space: nowrap; }}
.tabs .ul {{ position: absolute; left: 0; bottom: -2px; width: 266px; height: 5px; border-radius: 4px; background: {IND}; }}
.cap {{ position: relative; height: 210px; margin: 26px 36px 0; }}
.cap p {{ position: absolute; inset: 0; font: 500 38px/1.38 "Inter"; color: #E8E8EE; }}
.cap s {{ text-decoration: none; }}
.cnt {{ position: relative; height: 60px; margin: 0 36px; }}
.cnt span {{ position: absolute; right: 0; top: 4px; font: 600 24px/1 "JBM"; color: {MUTED}; }}
.phone {{ position: relative; width: 600px; height: 1010px; border-radius: 76px; background: #0c0c10; border: 14px solid #232329; box-shadow: 0 50px 120px rgba(0,0,0,.7), 0 0 0 2px rgba(255,255,255,.08); overflow: hidden; transform-style: preserve-3d; }}
.notch {{ position: absolute; top: 18px; left: 50%; width: 170px; height: 40px; margin-left: -85px; border-radius: 30px; background: #000; }}
.ph {{ display: flex; align-items: center; gap: 22px; padding: 96px 34px 0; }}
.av {{ width: 120px; height: 120px; border-radius: 50%; display: grid; place-items: center; background: linear-gradient(135deg,{IND},{IND_D}); flex: none; }}
.st {{ display: flex; flex-direction: column; align-items: center; flex: 1; }} .st b {{ font: 700 34px/1.1 "Inter"; }} .st span {{ font: 500 22px/1.2 "Inter"; color: {MUTED}; }}
.pn {{ padding: 22px 34px 26px; display: flex; flex-direction: column; gap: 8px; }} .pn b {{ font: 700 28px/1 "Inter"; }} .pn span {{ font: 600 22px/1 "Inter"; color: {IND}; }}
.grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px; padding: 0 4px; }}
.tile {{ position: relative; aspect-ratio: 1 / 1.25; }}
.tile.new {{ outline: 4px dashed rgba(255,255,255,.85); outline-offset: -10px; }}
.tile em {{ position: absolute; left: 50%; bottom: 16px; transform: translateX(-50%); font: 800 16px/1 "Inter"; letter-spacing: 2px; font-style: normal; background: rgba(0,0,0,.6); padding: 8px 10px; border-radius: 8px; white-space: nowrap; }}
.badge {{ position: absolute; top: 880px; display: flex; align-items: center; gap: 12px; font: 800 30px/1 "Inter"; letter-spacing: 4px; padding: 18px 28px; border-radius: 999px; background: {AMBER}; color: #1a1205; white-space: nowrap; box-shadow: 0 0 50px rgba(245,181,68,.5); }}
.badge i {{ width: 14px; height: 14px; border-radius: 50%; background: #1a1205; }}
.vs {{ display: flex; align-items: center; gap: 40px; }}
.side {{ position: relative; }}
.x {{ position: absolute; inset: -10px; display: grid; place-items: center; font: 900 170px/1 "Inter"; color: {RED}; text-shadow: 0 0 40px rgba(255,90,110,.6); }}
.vsb {{ font: 900 64px/1 "Outfit"; color: {MUTED}; }}
.pcard {{ display: flex; align-items: center; gap: 18px; padding: 30px 38px; border-radius: 26px; background: {PANEL2}; border: 2px solid {IND}; white-space: nowrap; }}
.pcard b {{ font: 700 54px/1 "Outfit"; }}
.q {{ margin-top: 150px; font: 800 64px/1.1 "Outfit"; text-align: center; white-space: nowrap; }}
.ainode {{ position: absolute; left: 540px; top: 330px; transform: translateX(-50%); padding: 30px 46px; border-radius: 999px; background: linear-gradient(135deg,{IND},{IND_D}); box-shadow: 0 0 60px rgba(124,134,255,.6); }}
.ainode span {{ font: 900 54px/1 "Outfit"; letter-spacing: 4px; white-space: nowrap; }}
.cable {{ position: absolute; left: 0; top: 380px; }}
.hub {{ width: 240px; height: 240px; border-radius: 60px; display: grid; place-items: center; background: linear-gradient(135deg, {PANEL2}, #101014); border: 2px solid {IND}; box-shadow: 0 0 80px rgba(79,57,246,.5); }}
.agent {{ position: absolute; display: flex; align-items: center; gap: 14px; padding: 22px 30px; border-radius: 999px; background: {PANEL2}; border: 2px solid {LINE}; font: 700 40px/1 "Inter"; white-space: nowrap; box-shadow: 0 16px 40px rgba(0,0,0,.45); }}
.agent i {{ width: 16px; height: 16px; border-radius: 50%; background: {MINT}; box-shadow: 0 0 14px {MINT}; }}
.links {{ position: absolute; overflow: visible; }} .links path {{ stroke: {IND}; stroke-width: 4; fill: none; stroke-dasharray: 6 10; }}
.mini {{ margin-top: 330px; display: flex; flex-direction: column; gap: 16px; }}
.mpost {{ width: 640px; display: flex; align-items: center; gap: 18px; padding: 20px 26px; border-radius: 22px; background: {PANEL}; border: 2px solid {LINE}; }}
.mpost b {{ font: 700 32px/1 "Inter"; flex: 1; }} .mpost em {{ font-style: normal; font: 900 32px/1 "Inter"; color: {MINT}; transform: scale(0); }}
.term {{ width: 940px; border-radius: 26px; overflow: hidden; background: #0d0d10; border: 2px solid {LINE}; box-shadow: 0 40px 100px rgba(0,0,0,.6); }}
.term .bar {{ height: 52px; display: flex; align-items: center; gap: 10px; padding: 0 20px; background: #17171c; }}
.term .bar i {{ width: 14px; height: 14px; border-radius: 50%; background: #3a3a44; }} .term .bar span {{ margin-left: 14px; font: 600 22px/1 "JBM"; color: {MUTED}; }}
.tl {{ padding: 26px 30px 0; font: 600 40px/1.3 "JBM"; color: #fff; white-space: nowrap; }}
.tl:last-child {{ padding-bottom: 30px; }}
.tl b {{ color: {MINT}; }} .tl s {{ text-decoration: none; opacity: 0; }} .tl u {{ display: inline-block; width: 22px; height: 44px; vertical-align: -8px; background: {IND}; margin-left: 4px; }}
.tl.dim {{ font-size: 30px; color: {MUTED}; }}
.week {{ margin-top: 40px; display: grid; grid-template-columns: repeat(7, 126px); gap: 10px; }}
.day {{ height: 270px; border-radius: 20px; background: {PANEL}; border: 2px solid {LINE}; display: flex; flex-direction: column; align-items: center; padding-top: 18px; gap: 18px; }}
.day > span {{ font: 700 26px/1 "Inter"; color: {MUTED}; }}
.wp {{ width: 104px; padding: 14px 0; border-radius: 16px; background: {PANEL2}; border: 2px solid rgba(124,134,255,.45); display: flex; flex-direction: column; align-items: center; gap: 10px; }}
.wp em {{ font: 700 20px/1 "JBM"; font-style: normal; color: {IND_L}; }}
.done {{ position: absolute; top: 640px; font: 900 190px/1 "Outfit"; color: {MINT}; text-shadow: 0 0 60px rgba(52,211,153,.55); white-space: nowrap; }}
.dep {{ width: 900px; padding-bottom: 30px; }}
.clock {{ display: flex; align-items: baseline; gap: 22px; padding: 10px 36px 0; white-space: nowrap; }}
.clock b {{ font: 800 150px/1 "Outfit"; letter-spacing: -2px; font-variant-numeric: tabular-nums; }} .clock span {{ font: 500 32px/1 "Inter"; color: {MUTED}; }}
.pb {{ margin: 26px 36px 10px; height: 18px; border-radius: 10px; background: #26262e; overflow: hidden; }}
.pb i {{ display: block; height: 100%; background: linear-gradient(90deg,{IND_D},{IND},{MINT}); transform-origin: 0 50%; }}
.log {{ padding: 10px 36px 0; }} .log p {{ display: flex; gap: 18px; align-items: center; font: 600 34px/1.75 "Inter"; color: #E8E8EE; white-space: nowrap; }}
.log em {{ font-style: normal; color: {MINT}; font-weight: 900; }}
.ctamark {{ display: flex; align-items: center; gap: 26px; white-space: nowrap; filter: drop-shadow(0 0 40px rgba(124,134,255,.6)); }}
.ctamark b {{ font: 700 104px/1 "Outfit"; letter-spacing: -2px; }}
.cbox {{ margin-top: 70px; width: 900px; display: flex; align-items: center; gap: 22px; padding: 22px 22px 22px 26px; border-radius: 999px; background: {PANEL2}; border: 2px solid {LINE}; }}
.cbox .av2 {{ width: 70px; height: 70px; border-radius: 50%; background: linear-gradient(135deg,#F59E0B,#EC4899); flex: none; }}
.cbox span {{ font: 700 48px/1 "Inter"; letter-spacing: 2px; }} .cbox s {{ text-decoration: none; opacity: 0; }}
.cbox u {{ width: 6px; height: 54px; background: {IND}; margin-left: -14px; }}
.cbox .send {{ margin-left: auto; font: 800 32px/1 "Inter"; font-style: normal; padding: 20px 34px; border-radius: 999px; color: {MUTED}; background: #26262e; }}
.ctabig {{ margin-top: 70px; font: 900 110px/1 "Outfit"; letter-spacing: -2px; white-space: nowrap; }}
.ctabig b {{ color: {IND_L}; text-shadow: 0 0 50px rgba(124,134,255,.6); }}
.ctasub {{ margin-top: 22px; font: 500 44px/1 "Inter"; color: {MUTED}; white-space: nowrap; }}
#capband {{ position: absolute; left: 0; right: 0; top: 1250px; height: 340px; pointer-events: none; background: linear-gradient(180deg, transparent, rgba(9,9,12,.82) 28%, rgba(9,9,12,.82) 72%, transparent); }}
#caps {{ position: absolute; left: 60px; right: 60px; top: 1330px; height: 190px; }}
.cg {{ position: absolute; left: 0; right: 0; top: 0; text-align: center; font: 800 70px/1.2 "Outfit"; color: #fff; text-shadow: 0 4px 24px rgba(0,0,0,.85), 0 0 2px rgba(0,0,0,.9); }}
.cg span {{ display: inline-block; }}
#flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; pointer-events: none; }}
#glitch {{ position: absolute; inset: 0; opacity: 0; pointer-events: none; background: repeating-linear-gradient(0deg, rgba(255,90,110,.18) 0 6px, transparent 6px 22px), repeating-linear-gradient(90deg, rgba(124,134,255,.12) 0 3px, transparent 3px 40px); mix-blend-mode: screen; }}
#vign {{ position: absolute; inset: 0; pointer-events: none; background: radial-gradient(120% 80% at 50% 45%, transparent 55%, rgba(0,0,0,.55)); }}
#grain {{ position: absolute; inset: -100px; pointer-events: none; opacity: .07; background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>"); }}
"""


def main():
    s1(); s2(); s3(); s4(); s5(); s6(); s7(); s8(); s9(); s10(); s11(); s12()
    for k in range(1, 13):
        scene_tl(k)
    caps = captions()
    # background life: the glows drift, the grain shifts every frame-ish (stepped, seek-safe)
    add(f'tl.to("#b1",{{x:180,y:120,duration:{DUR},ease:"sine.inOut"}},0);')
    add(f'tl.to("#b2",{{x:-160,y:-200,duration:{DUR},ease:"sine.inOut"}},0);')
    add(f'tl.to("#bg .grid",{{y:44,duration:{DUR},ease:"none"}},0);')
    add(f'tl.to("#grain",{{x:60,y:-40,duration:{DUR},ease:"steps({int(DUR * 12)})"}},0);')
    A.insert(0, "      gsap.set(" + json.dumps(list(dict.fromkeys(HIDE))) + ",{opacity:0});")
    scenes = "".join(f'<div class="scene" id="s{k}">{S[k]}</div>' for k in range(1, 13))
    has_mix = os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav"))
    audio = (f'<audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>' if has_mix else
             f'<audio id="vo" src="assets/audio/voice.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>')
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Postclerk reel 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <div id="bg" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0" data-layout-ignore><div class="grid"></div><div class="blob" id="b1" style="left:-300px;top:-200px;background:#4F39F6"></div><div class="blob" id="b2" style="right:-320px;bottom:-100px;background:#7C86FF"></div><div id="bgtint"></div></div>
      <div id="stagewrap" data-layout-allow-overflow><div id="stage">{scenes}</div></div>
      <div id="capband"></div>
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="7">{caps}</div>
      <div id="fx" class="clip" data-start="0" data-duration="{DUR}" data-track-index="8" data-layout-ignore><div id="glitch"></div><div id="flash"></div><div id="vign"></div><div id="grain"></div></div>
      {audio}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const CLK = {{ v: 0 }};
      const tl = gsap.timeline({{ paused: true, defaults: {{ immediateRender: false }} }});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump({"ev": sorted(EV), "end": DUR, "lines": LN, "scenes": SC}, open(os.path.join(B, "ev.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, {len(EV)} sound events, audio: {'mix' if has_mix else 'voice'}")


if __name__ == "__main__":
    main()
