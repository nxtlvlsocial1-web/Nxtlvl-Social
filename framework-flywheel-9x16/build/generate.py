"""samarpit.ai "Framework in 30: Funnel vs flywheel" (9:16): writes index.html, plan/sfx_events.json and plan/edit.json.

The 3D scene (assets/js/scene.js) is a pure function of time; this file times it to the voice (plan/words.json from
build/vo_pick.py) through window.FF_T, and lays the type over it on one paused GSAP timeline: the spoken line as a
word-on-speech headline, the stage words as chips glued to the 3D funnel and wheel, the three tips as cards with a small
UI moment each (a day-3 message, five stars filling, a +1 friend), and the closing two lines.
python3 build/generate.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = json.load(open(os.path.join(ROOT, "plan", "words.json")))
LW = {}
for w in W:
    LW.setdefault(w["line"], []).append(w)
JS, SFX, HTML = [], [], []
STEEL, AMBER, CORAL = "#5b8cff", "#ffb020", "#ff5a36"


def js(s):
    JS.append(s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(max(0, t), 3)})


def ft(sel, t, d, frm, to_, ease="power3.out"):
    js(f'tl.fromTo("{sel}", {frm}, {{...{to_}, duration: {d}, ease: "{ease}", immediateRender: false}}, {t:.3f});')


def to(sel, t, d, props, ease="power2.out"):
    js(f'tl.to("{sel}", {{...{props}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


def st(sel, t, props):
    js(f'tl.set("{sel}", {props}, {t:.3f});')


def wt(line, word, n=0):
    hits = [w for w in LW[line] if re.sub(r"[^a-z0-9]", "", w["w"].lower()).startswith(word.lower())]
    return hits[min(n, len(hits) - 1)]["t0"]


start = {k: v[0]["t0"] for k, v in LW.items()}
END = max(w["t1"] for w in W)
DUR = round(END + 1.8, 2)
T = {
    "vanish": wt("f00", "vanish"), "funnel": start["f01"], "ads": wt("f01", "ads"), "visit": wt("f01", "visit"), "buy": wt("f01", "buy"),
    "nothing": wt("f01", "nothing"), "wheel": start["f02"], "attract": wt("f02", "attract"), "sell": wt("f02", "sell"),
    "delight": wt("f02", "delight"), "refer": wt("f02", "refer"), "tip1": start["f03"], "tip2": start["f04"], "tip3": start["f05"],
    "friend": wt("f05", "friend"), "cta": start["f06"], "funnelWord": wt("f06", "funnel"), "spin": wt("f06", "spin"), "end": DUR,
}

# ---- headline lines: (line id, [(display word, class)], row breaks before these display indexes, chips)
# class: "" plain, "st" steel, "am" amber, "co" coral, "it" serif italic (adds to colour), chip:<id> -> a 3D chip, not the headline
SPEC = {
    "f00": [("Why", ""), ("do", ""), ("customers", ""), ("buy", ""), ("once,", ""), ("and", ""), ("vanish?", "co it")],
    "f01": [("Because", ""), ("you", ""), ("built", ""), ("a", ""), ("funnel.", "st"), ("Ads.", "chip:lab-ads"), ("Visit.", "chip:lab-visit"),
            ("Buy.", "chip:lab-buy"), ("Then...", "br"), ("nothing.", "co it")],
    "f02": [("A", ""), ("flywheel", "am"), ("puts", ""), ("them", ""), ("back", "am it"), ("in.", "am it"), ("Attract.", "chip:lab-attract"),
            ("Sell.", "chip:lab-sell"), ("Delight.", "chip:lab-delight"), ("Refer.", "chip:lab-refer")],
    "f06": [("Stop", ""), ("refilling", ""), ("the", ""), ("funnel.", "st"), ("Spin", "br am big"), ("the", "am big"), ("wheel.", "am big it")],
}
TIPS = {"f03": ("1", ["Message", "every", "buyer", "on", "day", "3."], "msg"),
        "f04": ("2", ["Ask", "the", "happy", "ones", "for", "a", "review."], "stars"),
        "f05": ("3", ["Give", "them", "a", "reason", "to", "bring", "a", "friend."], "friend")}


def headline(lid):
    spec, ws = SPEC[lid], LW[lid]
    if len(spec) != len(ws):
        raise SystemExit(f"{lid}: {len(spec)} display words but {len(ws)} spoken words: check the take")
    parts, n = [], 0
    for k, ((txt, cls), w) in enumerate(zip(spec, ws)):
        if cls.startswith("chip:"):
            cid = cls[5:]
            ft(f"#{cid}", w["t0"] - .04, .32, "{opacity: 0, scale: .4}", "{opacity: 1, scale: 1}", "back.out(2.6)")
            sfx("pop", w["t0"] - .02)
            continue
        if "br" in cls.split():
            parts.append("<br>")
        c = " ".join(x for x in cls.split() if x not in ("br",))
        parts.append(f'<span class="w {c}" id="{lid}w{n}">{txt}</span>')
        ft(f"#{lid}w{n}", w["t0"] - .05, .22, "{opacity: 0, y: 26, scale: .9}", "{opacity: 1, y: 0, scale: 1}", "back.out(2)")
        n += 1
    HTML.append(f'<div class="hl{" hl-end" if lid == "f06" else ""}" id="hl-{lid}">' + " ".join(parts) + "</div>")


for lid in ("f00", "f01", "f02", "f06"):
    headline(lid)
# line exits (the next line takes the spot)
order = ["f00", "f01", "f02", "f03", "f04", "f05", "f06"]
for a, b in zip(order, order[1:]):
    if a in SPEC:
        to(f"#hl-{a}", start[b] - .14, .14, "{opacity: 0, y: -30, filter: 'blur(8px)'}", "power2.in")
    else:
        to(f"#tip-{a}", start[b] - .16, .16, "{opacity: 0, y: -40, filter: 'blur(8px)'}", "power2.in")
# funnel chips leave with the funnel; wheel chips stay on the wheel
to(".fchip", T["wheel"] - .2, .2, "{opacity: 0, scale: .5}", "power2.in")

# ---- tip cards
for lid, (num, words, kind) in TIPS.items():
    ws = LW[lid]
    body = " ".join(f'<span class="tw" id="{lid}t{k}">{x}</span>' for k, x in enumerate(words))
    extra = {"msg": '<div class="ui msg" id="ui-msg"><div class="cal"><b>DAY</b><i>3</i></div><div class="bub" id="bub">Hey! How are you finding it so far?</div></div>',
             "stars": '<div class="ui stars" id="ui-stars">' + "".join(f'<span class="star" id="star{k}">&#9733;</span>' for k in range(5)) + "</div>",
             "friend": '<div class="ui friend" id="ui-friend"><span class="av a1"></span><span class="av a2" id="av2"></span><b id="plus1">+1</b></div>'}[kind]
    HTML.append(f'<div class="tip" id="tip-{lid}"><div class="num">{num}</div><div class="tb">{body}</div>{extra}</div>')
    t0 = start[lid]
    ft(f"#tip-{lid}", t0 - .12, .4, "{opacity: 0, y: 60, rotationX: -35}", "{opacity: 1, y: 0, rotationX: 0}", "back.out(1.6)")
    sfx("whoosh", t0 - .14)
    sfx("g_pickup", t0 + .02)
    # words light on speech (skip the spoken number, the card shows it)
    for k, w in enumerate(ws[1:len(words) + 1]):
        ft(f"#{lid}t{k}", w["t0"] - .04, .18, "{opacity: .25}", "{opacity: 1}", "power2.out")
    if kind == "msg":
        tm = wt(lid, "day")
        ft("#ui-msg", t0 + .2, .35, "{opacity: 0, x: -30}", "{opacity: 1, x: 0}")
        ft("#bub", tm - .1, .3, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}", "back.out(2.4)")
        sfx("msg", tm - .05)
    elif kind == "stars":
        tr = wt(lid, "review")
        ft("#ui-stars", t0 + .2, .3, "{opacity: 0}", "{opacity: 1}")
        for k in range(5):
            ft(f"#star{k}", tr - .25 + k * .09, .25, "{color: '#3a4252', scale: .6}", "{color: '#ffb020', scale: 1}", "back.out(3)")
        sfx("sparkle", tr - .2)
    else:
        tf = T["friend"]
        ft("#ui-friend", t0 + .2, .3, "{opacity: 0}", "{opacity: 1}")
        ft("#av2", tf - .05, .4, "{opacity: 0, x: -44, scale: .4}", "{opacity: 1, x: 0, scale: 1}", "back.out(2.2)")
        ft("#plus1", tf + .1, .3, "{opacity: 0, scale: .4}", "{opacity: 1, scale: 1}", "back.out(3)")
        sfx("g_levelup", tf)

# ---- top bar, end handle
ft("#bar", 0, .4, "{opacity: 0, y: -20}", "{opacity: 1, y: 0}")
ft("#handle", T["spin"] + .2, .5, "{opacity: 0, y: 20}", "{opacity: 1, y: 0}")
st("#flash", T["spin"] - .02, "{opacity: .55}")
to("#flash", T["spin"], .5, "{opacity: 0}", "power2.out")

# ---- sound design on the 3D beats
for k in range(5):
    sfx("g_drop", .5 + k * .1)
sfx("g_wrong", T["vanish"] + .05)
sfx("whoosh_big", T["funnel"] - .25)
for k in range(5):
    sfx("tick", T["funnel"] + .4 + k * .5)
sfx("impact", T["nothing"] + .05)
sfx("riser", T["wheel"] - 1.0)
sfx("whoosh_big", T["wheel"] - .1)
sfx("g_complete", T["refer"] + .3)
sfx("whoosh", T["cta"] - .1)
sfx("swish", T["funnelWord"] + .25)
sfx("riser_short", T["spin"] - .8)
sfx("impact", T["spin"])
sfx("sparkle", T["spin"] + .15)

CSS = f"""
@font-face {{ font-family: Mont; font-weight: 800; src: url("assets/fonts/montserrat.ttf"); }}
@font-face {{ font-family: Serif; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }}
@font-face {{ font-family: Mono; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #07090d; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Mont; color: #f4f1ea; background: #07090d; }}
#gl {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
#vig {{ position: absolute; inset: 0; pointer-events: none; background: radial-gradient(90% 60% at 50% 55%, rgba(0,0,0,0) 55%, rgba(0,0,0,.55) 100%); }}
#flash {{ position: absolute; inset: 0; background: {AMBER}; mix-blend-mode: screen; opacity: 0; pointer-events: none; }}
#bar {{ position: absolute; left: 70px; right: 70px; top: 262px; display: flex; justify-content: space-between; align-items: center; opacity: 0;
  font-family: Mono; font-weight: 700; font-size: 24px; letter-spacing: .14em; color: #8a93a6; }}
#bar b {{ color: {AMBER}; font-weight: 700; }}
.hl {{ position: absolute; left: 70px; right: 70px; top: 330px; text-align: center; font-weight: 800; font-size: 84px; line-height: 1.04;
  letter-spacing: -.035em; text-shadow: 0 6px 30px rgba(0,0,0,.6); }}
.hl .w {{ display: inline-block; opacity: 0; }}
.st {{ color: {STEEL}; }} .am {{ color: {AMBER}; }} .co {{ color: {CORAL}; }}
.it {{ font-family: Serif; font-style: italic; font-weight: 400; letter-spacing: -.01em; font-size: 1.15em; }}
.hl-end {{ top: 320px; font-size: 80px; }}
.big {{ font-size: 1.3em; }}
.chip {{ position: absolute; left: 0; top: 0; opacity: 0; padding: 12px 24px 11px; border-radius: 999px; font-family: Mono; font-weight: 700; font-size: 30px;
  letter-spacing: .1em; white-space: nowrap; backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); }}
.fchip {{ color: #dfe7ff; background: rgba(20,32,60,.72); border: 2px solid {STEEL}; box-shadow: 0 0 24px rgba(91,140,255,.45); }}
.wchip {{ color: #1a1206; background: {AMBER}; box-shadow: 0 0 30px rgba(255,176,32,.6); }}
.tip {{ position: absolute; left: 70px; right: 70px; top: 330px; padding: 34px 38px 36px; border-radius: 34px; opacity: 0; transform-origin: 50% 100%;
  background: linear-gradient(160deg, rgba(28,34,46,.92), rgba(16,20,28,.92)); border: 2px solid rgba(255,176,32,.35);
  box-shadow: 0 30px 70px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.08); }}
.tip .num {{ position: absolute; left: -16px; top: -26px; width: 84px; height: 84px; border-radius: 50%; background: {AMBER}; color: #1a1206;
  display: grid; place-items: center; font-size: 50px; font-weight: 800; box-shadow: 0 0 34px rgba(255,176,32,.6); }}
.tb {{ padding-left: 54px; font-weight: 800; font-size: 60px; line-height: 1.08; letter-spacing: -.03em; }}
.tw {{ opacity: .25; }}
.ui {{ margin: 26px 0 0 54px; opacity: 0; display: flex; align-items: center; gap: 18px; }}
.cal {{ width: 96px; height: 96px; border-radius: 18px; background: #f4f1ea; color: #111; display: flex; flex-direction: column; align-items: center; overflow: hidden; flex: none; }}
.cal b {{ width: 100%; text-align: center; background: {CORAL}; color: #fff; font-family: Mono; font-size: 20px; padding: 4px 0; }}
.cal i {{ font-style: normal; font-size: 50px; font-weight: 800; line-height: 1.25; }}
.bub {{ padding: 18px 24px; border-radius: 26px 26px 26px 6px; background: #2b6bff; color: #fff; font-family: Mont; font-weight: 800; font-size: 30px; letter-spacing: -.01em; opacity: 0; }}
.stars {{ gap: 10px; }}
.star {{ font-size: 76px; color: #3a4252; display: inline-block; text-shadow: 0 0 20px rgba(255,176,32,.35); }}
.friend .av {{ width: 92px; height: 92px; border-radius: 50%; display: inline-block; border: 4px solid #141922; }}
.a1 {{ background: radial-gradient(circle at 50% 36%, #ffd9a0 0 22%, transparent 23%), radial-gradient(circle at 50% 105%, #ffb020 0 45%, transparent 46%), #2a3342; }}
.a2 {{ margin-left: -30px; opacity: 0; background: radial-gradient(circle at 50% 36%, #c9d8ff 0 22%, transparent 23%), radial-gradient(circle at 50% 105%, #5b8cff 0 45%, transparent 46%), #2a3342; }}
#plus1 {{ font-size: 64px; font-weight: 800; color: {AMBER}; opacity: 0; }}
#handle {{ position: absolute; left: 0; right: 0; top: 1440px; text-align: center; font-family: Mono; font-weight: 700; font-size: 40px; letter-spacing: .08em; opacity: 0; color: #f4f1ea; }}
#handle span {{ color: {AMBER}; }}
"""
chips = "".join(f'<div class="chip fchip" id="lab-{k}">{k.upper()}</div>' for k in ("ads", "visit", "buy")) + \
        "".join(f'<div class="chip wchip" id="lab-{k}">{k.upper()}</div>' for k in ("attract", "sell", "delight", "refer"))
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>samarpit.ai Funnel vs flywheel 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" width="1080" height="1920"></canvas>
      <div id="vig"></div>
      {chips}
      <div id="bar"><span><b>TUE</b> &#183; FRAMEWORK IN 30</span><span>FUNNEL VS FLYWHEEL</span></div>
      {chr(10).join(HTML)}
      <div id="handle"><span>@</span>samarpit.ai</div>
      <div id="flash"></div>
    </div>
    <script>window.FF_T = {json.dumps({k: round(v, 3) for k, v in T.items()})};</script>
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
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx; T = {T}")
