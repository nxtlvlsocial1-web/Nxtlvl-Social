"""Creedom "I Wish..." reel: writes index.html. 1080x1920, 30 fps, about 52 s. Account: @nxtlvlsocial.ai.

The 3D film (assets/js/cree.js) plays full frame: a stressed creator in his bedroom studio at night, three wishes, and
Cree, Creedom's mascot, answering them: half revealed twice, then a full hero entrance, then three fixes, a hug and the
end card. This file adds the HTML layer: the creator's captions, Cree's speech clouds (he only chirps gibberish, so the
clouds are how viewers hear him), the "42 views" counter, the wish chips, the glass tags, and the end card (Creedom
wordmark, a comment box typing CREEDOM). It also writes build/chirps.json, the times Cree "talks", for build/audio.py.

python3 build/generate.py      (from the project root, after build/voice.py; build/audio.py writes the mix)
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
CU = json.load(open(os.path.join(B, "cues.json")))
WORDS = json.load(open(os.path.join(B, "words.json")))
LN, BT, DUR = CU["lines"], CU["beats"], round(CU["end"], 2)
Ls = lambda k: LN[k][0]  # noqa: E731
Le = lambda k: LN[k][1]  # noqa: E731
Bs = lambda k: BT[k][0]  # noqa: E731
Be = lambda k: BT[k][1]  # noqa: E731
A = []


def add(js):
    A.append("      " + js)


def show(sel, t, d=.3, frm="opacity:0,y:16", to="opacity:1,y:0", ease="power3.out"):
    add(f'tl.fromTo("{sel}",{{{frm}}},{{{to},duration:{d},ease:"{ease}",immediateRender:false}},{t:.3f});')


def hide(sel, t, d=.2, props="opacity:0"):
    add(f'tl.to("{sel}",{{{props},duration:{d},ease:"power2.in"}},{t:.3f});')


# Cree's speech clouds: (id, text, appears, gone, chirp start, chirp end, left px, top px, tail side)
CLOUDS = [
    ("k1", "Say no more.", Bs("say") + .05, Be("say") + .05, Bs("say") + .1, Bs("say") + .95, 110, 600, "right"),
    ("k2", "Second three. That's where they swipe.", Bs("fix1") + .3, Ls("08") + .35, Bs("fix1") + .35, Bs("fix1") + 1.9, 470, 650, "down"),
    ("k3", "Your people saved these. Make more.", Bs("fix2") + .25, Ls("09") + .25, Bs("fix2") + .3, Bs("fix2") + 1.7, 470, 650, "down"),
    ("k4", "Comment comes in. DM goes out.", Bs("fix3") + .2, Ls("10") - .2, Bs("fix3") + .25, Bs("fix3") + 1.6, 460, 650, "down"),
    ("k5", "Waiting for you to ask.", Bs("ask") + .02, Be("ask") + .05, Bs("ask") + .08, Bs("ask") + 1.05, 470, 700, "down"),
]
CHIRPS = [[round(c[4], 3), round(c[5], 3)] for c in CLOUDS] + [[round(Bs("tail") + .25, 3), round(Bs("tail") + .8, 3)]]


def story():
    H = []
    # 1. the "42 views" counter by his phone
    H.append('<div class="pill views" id="vw"><svg viewBox="0 0 24 24"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z" fill="none" stroke="#fff" stroke-width="2.2"/><circle cx="12" cy="12" r="3.2" fill="#fff"/></svg><b>42</b><span>views</span></div>')
    show("#vw", .45, .35, "opacity:0,scale:.6,y:20", "opacity:1,scale:1,y:0", "back.out(2.2)")
    add(f'tl.fromTo("#vw",{{rotation:0}},{{rotation:-4,duration:.08,yoyo:true,repeat:5,immediateRender:false}},{Ls("01") + 1.9:.3f});')
    hide("#vw", Le("01") + .05, .2, "opacity:0,y:30")
    # 2. step cards (the guide's "step cards"): the three wishes, then the three fixes
    CARDS = [("w0", "WISH 1", "Review my reel before I post", Ls("04") - .05, Le("04") + .3),
             ("w1", "WISH 2", "Learn from my old reels", Ls("05") - .05, Le("05") + .3),
             ("w2", "WISH 3", "Set up my DM automation", Ls("06") - .05, Le("06") + .3),
             ("f0", "FIX 1", "Reel review, second by second", Bs("fix1") + .15, Bs("fix2") - .1),
             ("f1", "FIX 2", "What your past reels say", Bs("fix2") + .15, Bs("fix3") - .1),
             ("f2", "FIX 3", "Comments to DM, on autopilot", Bs("fix3") + .15, Ls("10") - .2)]
    for cid, lab, txt, a, z in CARDS:
        H.append(f'<div class="card" id="{cid}"><i>{lab}</i><b>{txt}</b></div>')
        show(f"#{cid}", a, .35, "opacity:0,x:-40", "opacity:1,x:0")
        hide(f"#{cid}", z, .2, "opacity:0,x:-30")
    # 3. glass tags on the fixes
    H.append('<div class="tag" id="tg1"><b>0:03</b><span>Slow start</span></div>')
    show("#tg1", Bs("fix1") + 1.85, .3, "opacity:0,scale:.6", "opacity:1,scale:1", "back.out(2.4)"); hide("#tg1", Bs("fix2") - .1, .15)
    H.append('<div class="tag gold" id="tg2"><b>&#9733;</b><span>Most saved</span></div>')
    show("#tg2", Bs("fix2") + 1.55, .3, "opacity:0,scale:.6", "opacity:1,scale:1", "back.out(2.4)"); hide("#tg2", Bs("fix3") - .1, .15)
    H.append('<div class="tag rule" id="tg3"><span>Comments</span><b>&rarr;</b><span>DM</span><i id="sw"><em></em></i></div>')
    show("#tg3", Bs("fix3") + .5, .3, "opacity:0,scale:.6", "opacity:1,scale:1", "back.out(2.4)")
    add(f'tl.to("#sw",{{backgroundColor:"#22C55E",duration:.15,immediateRender:false}},{Bs("fix3") + .9:.3f});')
    add(f'tl.to("#sw em",{{x:30,duration:.15,ease:"power2.out",immediateRender:false}},{Bs("fix3") + .9:.3f});')
    hide("#tg3", Ls("10") - .2, .15)
    # 4. Cree's speech clouds
    for cid, txt, a, z, *_ , x, y, tail in CLOUDS:
        H.append(f'<div class="cloud t-{tail}" id="{cid}" style="left:{x}px;top:{y}px"><p>{txt}</p><i class="b1"></i><i class="b2"></i></div>')
        show(f"#{cid}", a, .32, "opacity:0,scale:.4", "opacity:1,scale:1", "back.out(2.6)")
        add(f'tl.fromTo("#{cid} p",{{y:0}},{{y:-5,duration:.18,yoyo:true,repeat:3,ease:"sine.inOut",immediateRender:false}},{a + .3:.3f});')
        hide(f"#{cid}", z - .18, .18, "opacity:0,scale:.85")
    # 5. the end card: wordmark, a comment box typing CREEDOM, the promise
    H.append('<div id="endc"><img class="logo" src="assets/img/creedom_logo.png" alt="Creedom"/>'
             '<div class="cbox"><span class="av"></span><span class="ty"><b id="kw">CREEDOM</b><i class="cur"></i></span><span class="post">Post</span></div>'
             '<div class="sub">I&rsquo;ll DM you the link</div></div>')
    EIN = Bs("endin") + .1
    show("#endc .logo", EIN, .5, "opacity:0,y:-30,scale:.9", "opacity:1,y:0,scale:1", "back.out(1.8)")
    show("#endc .cbox", EIN + .4, .4, "opacity:0,y:30", "opacity:1,y:0")
    add(f'tl.fromTo("#kw",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:.9,ease:"steps(7)",immediateRender:false}},{EIN + .75:.3f});')
    add(f'tl.fromTo("#endc .post",{{scale:1}},{{scale:.9,duration:.1,yoyo:true,repeat:1,immediateRender:false}},{EIN + 1.85:.3f});')
    show("#endc .sub", EIN + 1.1, .4, "opacity:0,y:16")
    return "".join(H)


CAP_TOP = {"01": 470, "02": 300, "03": 1330, "04": 425, "05": 1360, "06": 425, "07": 420, "08": 1430, "09": 1430, "10": 1430}   # per line, never over his face


def captions():
    html = []
    for k, (a, z) in LN.items():
        if k == "11":          # the end card's comment box says it
            continue
        ws = [w for w in WORDS if w["take"] == k]
        chunks, cur = [], []
        for w in ws:
            cur.append(w)
            if len(" ".join(x["w"] for x in cur)) > 16 or re.search(r"[.!?,]$", w["w"]) and len(cur) > 1:
                chunks.append(cur); cur = []
        if cur:
            chunks.append(cur)
        for j, ch in enumerate(chunks):
            t1 = chunks[j + 1][0]["s"] - .04 if j + 1 < len(chunks) else z + .25
            pid = f"c{k}_{j}"
            spans = "".join(f'<span id="{pid}w{i}">{x["w"].replace("CREEDOM", "<b>CREEDOM</b>")} </span>' for i, x in enumerate(ch))
            html.append(f'<div class="cap" id="{pid}" style="top:{CAP_TOP.get(k, 470)}px">{spans}</div>')
            add(f'tl.set("#{pid}",{{opacity:1}},{ch[0]["s"] - .05:.3f});')
            for i, x in enumerate(ch):
                add(f'tl.fromTo("#{pid}w{i}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:.12,ease:"power2.out",immediateRender:false}},{x["s"] - .03:.3f});')
            add(f'tl.to("#{pid}",{{opacity:0,duration:.08}},{t1:.3f});')
    return "".join(html)


CSS = """
@font-face { font-family: "GSans"; font-weight: 400 800; src: url("assets/fonts/googlesans.ttf"); }
@font-face { font-family: "Fraunces"; font-style: italic; font-weight: 400 800; src: url("assets/fonts/fraunces-italic.ttf"); }
@font-face { font-family: "Manrope"; font-weight: 200 800; src: url("assets/fonts/manrope.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #1A1224; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #1A1224; font-family: "GSans"; }
.clip { position: absolute; inset: 0; }
#gl { width: 1080px; height: 1920px; display: block; }
.pill, .wish, .tag, .cloud, #endc > * { opacity: 0; }
.views { position: absolute; left: 610px; top: 980px; display: flex; align-items: center; gap: 12px; padding: 14px 26px; border-radius: 999px; background: rgba(20,14,24,.78); border: 2px solid rgba(255,255,255,.18); color: #fff; }
.views svg { width: 38px; height: 38px; } .views b { font: 800 52px/1 "GSans"; } .views span { font: 600 34px/1 "GSans"; color: #D9CCE6; }
.wish { position: absolute; left: 50%; top: 300px; width: 330px; margin-left: -165px; text-align: center; padding: 14px 0; border-radius: 999px; background: rgba(243,67,162,.92); color: #fff; font: 800 34px/1 "GSans"; letter-spacing: 1px; box-shadow: 0 10px 30px rgba(243,67,162,.45); }
.wish i { font-style: normal; margin-right: 10px; color: #FFE7A8; }
.tag { position: absolute; display: flex; align-items: center; gap: 14px; padding: 14px 24px; border-radius: 20px; background: rgba(255,240,248,.82); border: 2px solid rgba(255,255,255,.9); box-shadow: 0 12px 34px rgba(60,10,40,.35); color: #2A1024; }
.tag b { font: 800 40px/1 "GSans"; color: #E8395A; } .tag span { font: 700 36px/1 "GSans"; }
#tg1 { left: 190px; top: 760px; } #tg2 { left: 70px; top: 1240px; } #tg2 b { color: #E0A11A; } #tg2 { background: rgba(255,246,220,.9); }
#tg3 { left: 70px; top: 1240px; } #tg3 b { color: #2A1024; }
#tg3 i { position: relative; width: 66px; height: 36px; border-radius: 18px; background: #B9AFC2; margin-left: 6px; } #tg3 em { position: absolute; left: 4px; top: 4px; width: 28px; height: 28px; border-radius: 50%; background: #fff; }
.cloud { position: absolute; max-width: 520px; padding: 26px 34px; border-radius: 48px; background: #FFFFFF; box-shadow: 0 14px 40px rgba(40,0,30,.35), inset 0 -6px 0 rgba(243,67,162,.12); transform-origin: 50% 100%; }
.cloud p { font: 800 46px/1.15 "GSans"; color: #2A1024; text-align: center; }
.cloud i { position: absolute; border-radius: 50%; background: #fff; box-shadow: 0 6px 16px rgba(40,0,30,.25); }
.cloud.t-down .b1 { width: 38px; height: 38px; left: 50%; bottom: -46px; margin-left: 10px; } .cloud.t-down .b2 { width: 22px; height: 22px; left: 50%; bottom: -80px; margin-left: 40px; }
.cloud.t-right .b1 { width: 38px; height: 38px; right: -40px; bottom: 6px; } .cloud.t-right .b2 { width: 22px; height: 22px; right: -74px; bottom: -14px; }
.cap { position: absolute; left: 70px; right: 90px; top: 470px; text-align: left; opacity: 0; font: 800 62px/1.15 "GSans"; color: #fff; text-shadow: 0 2px 14px rgba(10,4,24,.55), 0 1px 3px rgba(10,4,24,.6); }
.cap span { opacity: 0; display: inline-block; white-space: pre; } .cap b { color: #FF8CC6; font-weight: 800; }
.card { position: absolute; left: 70px; top: 290px; padding: 18px 26px 20px; border-radius: 22px; background: rgba(18,10,30,.72); border: 1px solid rgba(255,255,255,.14); opacity: 0; }
.card i { display: block; font: 800 24px/1 "GSans"; font-style: normal; letter-spacing: 3px; color: #FF8CC6; } .card b { display: block; margin-top: 10px; font: 800 38px/1.15 "GSans"; color: #fff; }
#endc { position: absolute; inset: 0; }
#endc .logo { position: absolute; left: 50%; top: 430px; width: 640px; margin-left: -320px; filter: drop-shadow(0 8px 30px rgba(243,67,162,.45)); }
#endc .cbox { position: absolute; left: 110px; right: 110px; top: 640px; display: flex; align-items: center; gap: 18px; padding: 18px 22px; border-radius: 26px; background: rgba(255,255,255,.95); box-shadow: 0 16px 40px rgba(40,0,30,.4); }
#endc .av { width: 58px; height: 58px; border-radius: 50%; background: linear-gradient(135deg, #F343A2, #FF9A6A); flex: none; }
#endc .ty { flex: 1; display: flex; align-items: center; } #endc .ty b { font: 800 50px/1 "GSans"; color: #2A1024; letter-spacing: 2px; } #endc .cur { display: inline-block; width: 4px; height: 50px; background: #F343A2; margin-left: 6px; }
#endc .post { font: 800 36px/1 "GSans"; color: #fff; background: #F343A2; padding: 14px 24px; border-radius: 16px; }
#endc .sub { position: absolute; left: 0; right: 0; top: 790px; text-align: center; font: italic 600 50px/1.2 "Fraunces"; color: #FFE3F1; text-shadow: 0 4px 18px rgba(0,0,0,.5); }
"""


def main():
    ui = story()
    caps = captions()
    mix = "mix.wav" if os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav")) else "voice.wav"
    env = json.load(open(os.path.join(B, "env.json"))) if os.path.exists(os.path.join(B, "env.json")) else {}
    ct = {"lines": LN, "beats": BT, "end": DUR, "words": WORDS, "chirps": CHIRPS, "voiceEnv": env.get("voice", []), "creeEnv": env.get("cree", [])}
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom I Wish 9x16</title>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" class="clip" data-hold data-start="0" data-duration="{DUR}" data-track-index="0"></canvas>
      <div id="ui" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3" data-layout-allow-overflow>{ui}</div>
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="4">{caps}</div>
      <audio id="mix" src="assets/audio/{mix}" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.CT = {json.dumps(ct)};
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
    <script type="module" src="assets/js/cree.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump({"chirps": CHIRPS}, open(os.path.join(B, "chirps.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, audio {mix}")


if __name__ == "__main__":
    main()
