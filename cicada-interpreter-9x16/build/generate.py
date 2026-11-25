"""AI.NXTLVL "Cicada: a live interpreter for any call" (9:16): writes index.html, plan/sfx_events.json, plan/edit.json.

The 3D scene (assets/js/scene.js) is a pure function of time; this file times it to the voice (plan/words.json from
build/vo_kok.py) through window.CI_T and lays the type over it on one paused GSAP timeline: the spoken line as a
word-on-speech headline (sentence groups, one boxed key word each, like a selection box), labels glued to 3D objects
(positioned by scene.js), the name card, the GitHub card and the comment box. Facts: plan/facts.md.
python3 build/generate.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def key(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


W = []
for w in json.load(open(os.path.join(ROOT, "plan", "words.json"))):
    if W and w["w"][:1] in ".,-" and W[-1]["line"] == w["line"]:       # Whisper splits "3,000" / "to-do": one word again
        W[-1]["w"] += w["w"]; W[-1]["t1"] = w["t1"]
    elif W and key(w["w"]) == "thousand" and key(W[-1]["w"]) == "three":   # captions show the number
        W[-1]["w"] = "3,000"; W[-1]["t1"] = w["t1"]
    else:
        W.append(dict(w))
LW = {}
for w in W:
    LW.setdefault(w["line"], []).append(w)
JS, SFX, HTML = [], [], []
VIOLET, LAV, CYAN, NIGHT = "#7a2ffb", "#b687f9", "#6fe3ff", "#07050f"


def js(s):
    JS.append(s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(max(0, t), 3)})


def ft(sel, t, d, frm, to_, ease="power3.out"):
    js(f'tl.fromTo("{sel}", {frm}, {{...{to_}, duration: {d}, ease: "{ease}", immediateRender: false}}, {max(0, t):.3f});')


def to(sel, t, d, props, ease="power2.out"):
    js(f'tl.to("{sel}", {{...{props}, duration: {d}, ease: "{ease}"}}, {max(0, t):.3f});')


def key(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def wt(line, words, n=0, end=False):
    words = words if isinstance(words, (list, tuple)) else [words]
    hits = [w for w in LW[line] if any(key(w["w"]).startswith(x) for x in words)]
    if not hits:
        raise SystemExit(f"{line}: none of {words} in {[w['w'] for w in LW[line]]}")
    h = hits[min(n, len(hits) - 1)]
    return h["t1"] if end else h["t0"]


start = {k: v[0]["t0"] for k, v in LW.items()}
endl = {k: v[-1]["t1"] for k, v in LW.items()}
END = max(w["t1"] for w in W)
DUR = round(END + 1.5, 2)
T = {
    "l00": start["l00"], "jp2": wt("l00", "japanese", 1), "l01": start["l01"], "call": wt("l01", "call"), "bot": wt("l02", "bot"), "l03": start["l03"],
    "cicada": wt("l03", "cicada"), "l04": start["l04"], "tokyo": wt("l04", "tokyo"), "asks": wt("l04", "asks"),
    "can": wt("l04", "can"), "friday": wt("l04", "friday"), "l05": start["l05"], "l06": start["l06"], "hold": wt("l06", "hold"),
    "yes": wt("l06", "yes"), "thursday": wt("l06", "thursday"), "l07": start["l07"], "let": wt("l07", "let"), "l07end": endl["l07"],
    "l08": start["l08"], "summary": wt("l09", "summary"), "todo": wt("l09", ["todo", "to"], 0), "l10": start["l10"],
    "click": wt("l10", "click"), "jumps": wt("l10", "jump"), "exact": wt("l10", "exact"), "l11": start["l11"],
    "stars": wt("l11", "stars"), "l12": start["l12"], "l13": start["l13"], "callkw": wt("l13", "call"), "end": DUR,
}

# ---- headline style: per line, word key -> class ("hb" boxed key word, "it" serif italic lavender, "cy" cyan, "big")
STYLE = {
    "l00": {"japanese": "hb"}, "l01": {"opensourced": "hb", "open": "hb", "sourced": "hb", "any": "it", "call": "it"},
    "l02": {"no": "hb", "bot": "hb"}, "l03": {"cicada": "hb big"}, "l04": {"tokyo": "hb", "price": "it", "list": "it", "friday": "it"},
    "l05": {"english": "hb", "live": "it"}, "l06": {"one": "hb", "key": "hb", "thursday": "it"}, "l07": {"japanese": "hb", "right": "it", "in": "", "call": "it"},
    "l08": {"already": "hb it", "written": "hb it"}, "l09": {"todo": "hb", "to": "hb", "do": "hb", "thursday": "it"},
    "l10": {"exact": "hb", "moment": "hb"}, "l11": {"3000": "hb", "3": "hb", "000": "hb", "stars": "hb", "github": "it"},
    "l12": {"clients": "it", "abroad": "it"}, "l13": {"call": "hb", "link": "it"},
}
ORDER = [f"l{k:02d}" for k in range(14)]
GID = []


def groups(ws):
    out, cur = [], []
    for w in ws:
        cur.append(w)
        if re.search(r"[.?!:]$", w["w"]) or len(cur) >= 11:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


for lid in ORDER:
    if lid == "l03":                                       # the name card says it
        continue
    st = STYLE.get(lid, {})
    for gi, g in enumerate(groups(LW[lid])):
        gid = f"hl-{lid}-{gi}"
        parts = []
        # merge neighbouring boxed words into one box
        k = 0
        while k < len(g):
            cls = st.get(key(g[k]["w"]), "")
            if "hb" in cls:
                j = k
                while j + 1 < len(g) and "hb" in st.get(key(g[j + 1]["w"]), ""):
                    j += 1
                first = lid == "l00" and gi == 0
                inner = " ".join(f'<span class="w{" on" if first else ""}" id="{gid}w{m}">{g[m]["w"]}</span>' for m in range(k, j + 1))
                extra = " ".join(x for x in cls.split() if x != "hb")
                parts.append(f'<span class="hb {extra}{" on0" if first else ""}" id="{gid}b{k}"><i class="c1"></i><i class="c2"></i><i class="c3"></i><i class="c4"></i>{inner}</span>')
                ft(f"#{gid}b{k}", max(.001, g[k]["t0"] - .02), .3, "{'--bx': 0}", "{'--bx': 1}", "power2.out")
                for m in range(k, j + 1 if not first else k):
                    ft(f"#{gid}w{m}", g[m]["t0"] - .05, .22, "{opacity: 0, y: 24}", "{opacity: 1, y: 0}", "back.out(2)")
                k = j + 1
                continue
            first = lid == "l00" and gi == 0
            parts.append(f'<span class="w {cls}{" on" if first else ""}" id="{gid}w{k}">{g[k]["w"]}</span>')
            if not first:
                ft(f"#{gid}w{k}", g[k]["t0"] - .05, .22, "{opacity: 0, y: 24}", "{opacity: 1, y: 0}", "back.out(2)")
            k += 1
        HTML.append(f'<div class="hl" id="{gid}">' + " ".join(parts) + "</div>")
        GID.append((gid, g[0]["t0"]))
for (a, ta), (b, tb) in zip(GID, GID[1:]):
    to(f"#{a}", tb - .12, .12, "{opacity: 0, y: -24, filter: 'blur(8px)'}", "power2.in")

# ---- name card (l03), GitHub card (l11), comment box (l13)
ft("#nobot", T["bot"] - .1, .35, "{opacity: 0, y: 30}", "{opacity: 1, y: 0}", "back.out(2)")
to("#nobot", T["l03"] - .25, .2, "{opacity: 0}")
ft("#name", T["cicada"] - .08, .45, "{opacity: 0, scale: .85, y: 30}", "{opacity: 1, scale: 1, y: 0}", "back.out(1.8)")
to("#name", T["l04"] - .25, .2, "{opacity: 0, scale: .95}", "power2.in")
ft("#namebg", T["cicada"] - .15, .3, "{opacity: 0}", "{opacity: 1}")
to("#namebg", T["l04"] - .25, .2, "{opacity: 0}")
ft("#gh", T["l11"] - .1, .45, "{opacity: 0, y: 40, rotationX: -30}", "{opacity: 1, y: 0, rotationX: 0}", "back.out(1.6)")
js(f'tl.fromTo("#ghn", {{innerText: 0}}, {{innerText: 3200, duration: 1.0, ease: "power2.out", snap: {{innerText: 50}}, immediateRender: false,'
   f' onUpdate: function () {{ const el = document.getElementById("ghn"); const v = +el.innerText; el.innerText = v >= 3200 ? "3.2k" : v.toLocaleString("en-US"); }}}}, {T["stars"] - .55:.3f});')
to("#gh", T["l12"] - .25, .2, "{opacity: 0, y: -20}", "power2.in")
tc = T["l13"]
ft("#cbox", tc - .05, .45, "{opacity: 0, y: 50, scale: .92}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.8)")
for k, ch in enumerate("CALL"):
    ft(f"#ck{k}", T["callkw"] - .2 + k * .07, .05, "{opacity: 0}", "{opacity: 1}", "none")
    sfx("click", T["callkw"] - .2 + k * .07)
ft("#cpost", T["callkw"] + .15, .25, "{color: '#6b6585'}", "{color: '#7a2ffb'}", "power2.out")
for at, op in ((T["cicada"], .35), (T["let"] + .2, .3), (T["callkw"] + .3, .3)):
    js(f'tl.set("#flash", {{opacity: {op}}}, {at - .02:.3f});')
    to("#flash", at, .45, "{opacity: 0}", "power2.out")

# ---- whip streaks on the shot changes (the camera moves are in scene.js)
for k, at in enumerate([T["jp2"] - .2, T["l01"] - .2, T["bot"] - .4, T["l03"] - .25, T["l04"] - .15, T["can"] - .3, T["l05"] - .15, T["l06"] - .25,
                        T["let"] - .05, T["l08"] - .25, T["summary"] - .2, T["l10"] - .25, T["l11"] - .25, T["l12"] - .25]):
    d = 1 if k % 2 else -1
    js(f'tl.fromTo("#whip", {{opacity: 0, x: {-900 * d}}}, {{opacity: .55, x: 0, duration: .12, ease: "power2.in", immediateRender: false}}, {at:.3f});')
    js(f'tl.to("#whip", {{opacity: 0, x: {900 * d}, duration: .14, ease: "power2.out"}}, {at + .12:.3f});')

# ---- sound design
sfx("whoosh", .0)
sfx("ja_reply_soft", .05)                                   # frame 1: the Japanese out, under the hook
sfx("whoosh_big", T["l01"] - .25)
for i in range(5):
    sfx("pop", T["call"] - .2 + i * .07)
sfx("whoosh", T["bot"] - .45)
sfx("g_correct", T["bot"] + .1)
sfx("whoosh", T["l03"] - .3)
sfx("impact", T["cicada"])
sfx("sparkle", T["cicada"] + .05)
sfx("whoosh_big", T["l04"] - .25)
sfx("riser_short", T["tokyo"] - .6)
sfx("ding", T["tokyo"] + .25)
sfx("whoosh", T["asks"] - .3)
sfx("ja_client", T["asks"] + .05)
sfx("msg", T["can"])
sfx("whoosh", T["l05"] - .2)
sfx("whoosh", T["l06"] - .3)
sfx("click", T["hold"])
sfx("thump", T["hold"] + .02)
sfx("g_pickup", T["yes"])
sfx("pop", T["let"])
sfx("whoosh_big", T["let"] + .05)
sfx("ja_reply", T["l07end"] + .2)
sfx("g_complete", T["l07end"] + .1)
sfx("whoosh", T["l08"] - .3)
sfx("g_pop", T["summary"])
sfx("g_pickup", T["todo"])
sfx("click", T["click"])
sfx("g_swish", T["jumps"])
sfx("ding", T["exact"] + .1)
sfx("whoosh", T["l11"] - .3)
sfx("pop", T["l11"])
sfx("sparkle", T["stars"])
sfx("whoosh_big", T["l12"] - .3)
for i in range(5):
    sfx("g_tick", T["l12"] + .25 + i * .16)
sfx("whoosh", tc - .1)
sfx("impact", T["callkw"] + .3)
sfx("g_complete", T["callkw"] + .4)

CSS = f"""
@font-face {{ font-family: Mont; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }}
@font-face {{ font-family: Serif; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }}
@font-face {{ font-family: Mono; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
@font-face {{ font-family: NotoJP; font-weight: 100 900; src: url("assets/fonts/NotoSansJP-sub.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {NIGHT}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Mont; font-weight: 800; color: #fff; background: {NIGHT}; }}
#gl {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
#vig {{ position: absolute; inset: 0; pointer-events: none; background: radial-gradient(100% 64% at 50% 56%, rgba(0,0,0,0) 52%, rgba(3,2,8,.62) 100%); }}
#topfade {{ position: absolute; left: 0; right: 0; top: 0; height: 720px; pointer-events: none; background: linear-gradient(180deg, rgba(7,5,15,.78) 0%, rgba(7,5,15,.45) 45%, rgba(7,5,15,0) 100%); }}
#grain {{ position: absolute; inset: -50%; pointer-events: none; opacity: .07; background-image: repeating-radial-gradient(circle at 17% 32%, rgba(255,255,255,.5) 0 1px, transparent 1px 3px); mix-blend-mode: overlay; }}
#whip {{ position: absolute; left: -10%; right: -10%; top: 0; bottom: 0; opacity: 0; pointer-events: none; mix-blend-mode: screen;
  background: linear-gradient(90deg, rgba(122,47,251,0) 0%, rgba(182,135,249,.35) 38%, rgba(255,255,255,.55) 50%, rgba(182,135,249,.35) 62%, rgba(122,47,251,0) 100%); filter: blur(30px); }}
.gr {{ position: absolute; left: 0; top: 0; opacity: 0; white-space: nowrap; font-weight: 800; font-size: 40px; color: #efe9ff;
  text-shadow: 0 0 18px rgba(122,47,251,.9), 0 0 4px rgba(182,135,249,.8); }}
.gr.ja {{ font-family: NotoJP; font-weight: 700; }}
#flash {{ position: absolute; inset: 0; background: {VIOLET}; mix-blend-mode: screen; opacity: 0; pointer-events: none; }}
#bar {{ position: absolute; left: 70px; right: 70px; top: 258px; display: flex; justify-content: space-between; align-items: center;
  font-family: Mono; font-weight: 700; font-size: 24px; letter-spacing: .16em; color: rgba(255,255,255,.62); }}
#bar img {{ height: 40px; }}
#bar b {{ color: {LAV}; font-weight: 700; }}
.hl {{ position: absolute; left: 60px; right: 60px; top: 330px; text-align: center; font-weight: 800; font-size: 76px; line-height: 1.12;
  letter-spacing: -.03em; text-shadow: 0 6px 30px rgba(0,0,0,.7); }}
.hl .w {{ display: inline-block; opacity: 0; }}
.hl .w.on {{ opacity: 1; }}
.hb.on0 {{ --bx: 1; }}
.it {{ font-family: Serif; font-style: italic; font-weight: 400; letter-spacing: -.01em; font-size: 1.14em; color: {LAV}; }}
.big {{ font-size: 1.3em; }}
.hb {{ --bx: 0; position: relative; display: inline-block; padding: 0 14px 4px; margin: 0 2px; }}
.hb::before {{ content: ""; position: absolute; inset: 2px -2px -2px; border: 3px solid {VIOLET}; border-radius: 6px; background: rgba(122,47,251,.14);
  clip-path: inset(0 calc(100% - var(--bx) * 100%) 0 0); box-shadow: 0 0 26px rgba(122,47,251,.45); }}
.hb i {{ position: absolute; width: 14px; height: 14px; background: #fff; border: 3px solid {VIOLET}; border-radius: 3px; opacity: var(--bx); }}
.hb .c1 {{ left: -9px; top: -5px; }} .hb .c2 {{ right: -9px; top: -5px; }} .hb .c3 {{ left: -9px; bottom: -9px; }} .hb .c4 {{ right: -9px; bottom: -9px; }}
.hb.it {{ color: #fff; }}
.chip {{ position: absolute; left: 0; top: 0; opacity: 0; padding: 14px 26px 13px; border-radius: 999px; font-weight: 800; font-size: 32px; white-space: nowrap;
  color: #fff; background: rgba(20,12,40,.72); border: 2px solid rgba(182,135,249,.7); box-shadow: 0 14px 40px rgba(0,0,0,.45), 0 0 30px rgba(122,47,251,.35);
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); }}
#nobot {{ font-size: 34px; left: 50%; top: 1470px; transform: translateX(-50%); }}
#nobot s {{ color: #ff8aa0; text-decoration-thickness: 4px; }}
.pin {{ font-family: Mono; font-weight: 700; font-size: 30px; letter-spacing: .08em; }}
#pinTokyo {{ border-color: {CYAN}; color: {CYAN}; }}
#keyTip {{ font-size: 30px; }}
#keyTip b {{ display: inline-block; min-width: 46px; padding: 2px 10px; margin-right: 10px; border-radius: 10px; background: {VIOLET}; text-align: center; }}
#jaOut {{ font-family: NotoJP; font-weight: 700; font-size: 44px; padding: 20px 30px; border-radius: 28px 28px 28px 8px; border-color: {CYAN};
  box-shadow: 0 0 40px rgba(111,227,255,.35); }}
#jaOut small {{ display: block; font-family: Mono; font-size: 20px; letter-spacing: .12em; color: {CYAN}; margin-bottom: 8px; }}
#name {{ position: absolute; left: 0; right: 0; top: 520px; text-align: center; opacity: 0; }}
#namebg {{ position: absolute; inset: 0; opacity: 0; pointer-events: none; background: radial-gradient(70% 40% at 50% 36%, rgba(7,5,15,.85), rgba(7,5,15,.35) 70%, rgba(7,5,15,0)); }}
#name .nm {{ font-size: 170px; letter-spacing: -.05em; line-height: 1; text-shadow: 0 0 60px rgba(122,47,251,.6); }}
#name .jp {{ font-family: NotoJP; font-weight: 700; font-size: 64px; color: {LAV}; margin-top: 6px; }}
#name .tags {{ margin-top: 26px; display: flex; gap: 16px; justify-content: center; }}
#name .tags span {{ font-family: Mono; font-weight: 700; font-size: 26px; letter-spacing: .08em; padding: 10px 20px; border-radius: 999px; border: 2px solid rgba(182,135,249,.6); background: rgba(20,12,40,.6); }}
#gh {{ position: absolute; left: 110px; right: 110px; top: 560px; opacity: 0; padding: 30px 36px; border-radius: 28px; background: rgba(13,10,24,.86);
  border: 2px solid rgba(182,135,249,.45); box-shadow: 0 30px 80px rgba(0,0,0,.6); transform-origin: 50% 100%; }}
#gh .rp {{ font-family: Mono; font-size: 34px; color: #e9e4ff; }}
#gh .rp b {{ color: #fff; }}
#gh .ds {{ font-weight: 700; font-size: 28px; color: rgba(255,255,255,.72); margin: 14px 0 22px; line-height: 1.3; }}
#gh .mt {{ display: flex; gap: 26px; align-items: center; font-family: Mono; font-size: 28px; color: rgba(255,255,255,.8); }}
#gh .st {{ padding: 10px 20px; border-radius: 14px; background: {VIOLET}; color: #fff; font-size: 34px; }}
#cbox {{ position: absolute; left: 90px; right: 90px; top: 640px; height: 132px; border-radius: 66px; opacity: 0; display: flex; align-items: center; gap: 24px;
  padding: 0 38px 0 26px; background: rgba(248,246,255,.97); color: {NIGHT}; box-shadow: 0 30px 80px rgba(0,0,0,.6), 0 0 0 3px rgba(122,47,251,.7); }}
#cbox .av {{ width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(140deg, {VIOLET}, {CYAN}); flex: none; }}
#cbox .tx {{ flex: 1; font-size: 56px; letter-spacing: .03em; }}
#cbox .tx span {{ opacity: 0; }}
#cpost {{ font-size: 36px; color: #6b6585; }}
#wm {{ position: absolute; left: 0; right: 0; top: 820px; text-align: center; opacity: 0; }}
#wm img {{ height: 70px; }}
"""
apps = ["Zoom", "Teams", "Google Meet", "Discord", "Telegram"]
chips = "".join(f'<div class="chip" id="app{i}">{a}</div>' for i, a in enumerate(apps))
greet = ["Good morning", "おはようございます", "Buenos días", "Bonjour", "こんにちは", "Guten Morgen", "Buongiorno", "Bom dia", "Hola", "Ciao"]
chips += "".join(f'<div class="gr{" ja" if ord(g[0]) > 0x3000 else ""}" id="gr{i}">{g}</div>' for i, g in enumerate(greet))
chips += '<div class="chip" id="nobot"><s>Meeting bot</s> &nbsp;not needed</div>'
chips += '<div class="chip pin" id="pinYou">YOU</div><div class="chip pin" id="pinTokyo">TOKYO</div>'
chips += '<div class="chip" id="keyTip"><b>&#8997;</b>hold to talk</div>'
chips += '<div class="chip" id="jaOut"><small>THE CLIENT HEARS</small>&#12399;&#12356;&#12289;&#26408;&#26332;&#26085;&#12395;&#36865;&#12426;&#12414;&#12377;&#12290;</div>'
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>AI.NXTLVL Cicada live interpreter 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" width="1080" height="1920"></canvas>
      <div id="vig"></div>
      <div id="topfade"></div>
      {chips}
      <div id="bar"><img src="assets/img/logo-wordmark.png" alt=""><span><b>AI</b> TOOLS</span></div>
      {chr(10).join(HTML)}
      <div id="namebg"></div>
      <div id="name"><div class="nm">Cicada</div><div class="jp">&#30693;&#20102;</div><div class="tags"><span>OPEN SOURCE</span><span>APACHE-2.0</span></div></div>
      <div id="gh"><div class="rp">wquguru / <b>cicada</b></div><div class="ds">Live subtitles, interpreting and meeting notes for any call. Mac, Windows, Linux, Android.</div>
        <div class="mt"><span class="st">&#9733; <span id="ghn">0</span></span><span>Apache-2.0</span><span>open source</span></div></div>
      <div id="cbox"><div class="av"></div><div class="tx">{"".join(f'<span id="ck{k}">{c}</span>' for k, c in enumerate("CALL"))}</div><b id="cpost">Post</b></div>
      <div id="whip"></div>
      <div id="grain"></div>
      <div id="flash"></div>
    </div>
    <script>window.CI_T = {json.dumps({k: round(v, 3) for k, v in T.items()})};</script>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      {chr(10).join("      " + j for j in JS).strip()}
      tl.set({{}}, {{}}, {DUR:.2f});
      window.__timelines["main"] = tl;
    </script>
    <script type="module" src="assets/js/scene.js"></script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(html)
SFX.sort(key=lambda e: e["t"])
json.dump(SFX, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
json.dump({"dur": DUR, "scenes": {}}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx")
print({k: round(v, 2) for k, v in T.items()})
