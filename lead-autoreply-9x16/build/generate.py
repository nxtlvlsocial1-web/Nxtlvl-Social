"""samarpit.ai "Wed · System Build: lead auto-reply" (9:16): writes index.html, plan/sfx_events.json and plan/edit.json.

The 3D scene (assets/js/scene.js) is a pure function of time; this file times it to the voice (plan/words.json from
build/vo_pick.py) through window.LR_T, and lays the type over it on one paused GSAP timeline: the spoken line as a
word-on-speech headline (one sentence group at a time), the four steps as cards whose words light on speech, labels glued
to the 3D boxes (positioned by scene.js), the LIVE TEST badge and the closing comment box.
python3 build/generate.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = []
for w in json.load(open(os.path.join(ROOT, "plan", "words.json"))):
    if W and w["w"].startswith(".") and W[-1]["line"] == w["line"]:      # Whisper splits "p.m." into "p" + ".m.": one word again
        W[-1]["w"] += w["w"]; W[-1]["t1"] = w["t1"]
    else:
        W.append(dict(w))
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
    js(f'tl.fromTo("{sel}", {frm}, {{...{to_}, duration: {d}, ease: "{ease}", immediateRender: false}}, {max(0, t):.3f});')


def to(sel, t, d, props, ease="power2.out"):
    js(f'tl.to("{sel}", {{...{props}, duration: {d}, ease: "{ease}"}}, {max(0, t):.3f});')


def key(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def wt(line, words, n=0):
    words = words if isinstance(words, (list, tuple)) else [words]
    hits = [w for w in LW[line] if any(key(w["w"]).startswith(x) for x in words)]
    if not hits:
        raise SystemExit(f"{line}: none of {words} in {[w['w'] for w in LW[line]]}")
    return hits[min(n, len(hits) - 1)]["t0"]


start = {k: v[0]["t0"] for k, v in LW.items()}
END = max(w["t1"] for w in W)
DUR = round(END + 1.6, 2)
T = {
    "l00": start["l00"], "eleven": wt("l00", ["eleven", "11"]), "ten": wt("l00", ["ten", "10"]), "booked": wt("l00", "booked"),
    "l01": start["l01"], "seconds": wt("l01", "seconds"), "sleep": wt("l01", "sleep"), "code": wt("l01", "code"),
    "l02": start["l02"], "boxes": wt("l02", "boxes"),
    "s1": start["l03"], "form": wt("l03", "form"), "s2": start["l04"], "sheet": wt("l04", "sheet"),
    "s3": start["l05"], "instant": wt("l05", "instant"), "name": wt("l05", "name"), "thank": wt("l05", "thank"),
    "price": wt("l05", "price"), "booking": wt("l05", "booking"), "s4": start["l06"], "buzz": wt("l06", "buzz"),
    "live": start["l07"], "formIn": wt("l07", "form"), "already": wt("l07", "already"),
    "l08": start["l08"], "night": wt("l08", "night"), "tag": wt("l08", "tag"), "cta": start["l09"], "flow": wt("l09", "flow"),
    "end": DUR,
}

# ---- headlines: line id -> groups; a group is [(display word, class)] and replaces the one before it.
# One display word per spoken word. class: "" plain, "st" steel, "am" amber, "co" coral, "it" serif italic, "br" line break
SPEC = {
    "l00": [[("A", ""), ("customer", ""), ("messaged", ""), ("you", ""), ("at", "br"), ("11", "st"), ("PM.", "st")],
            [("You", ""), ("replied", ""), ("at", ""), ("10", "co"), ("AM.", "co")],
            [("They'd", ""), ("already", ""), ("booked", "br co it"), ("someone", "co it"), ("else.", "co it")]],
    "l01": [[("This", ""), ("replies", ""), ("in", "br am it"), ("seconds.", "am it")],
            [("While", ""), ("you", ""), ("sleep.", "am"), ("And", "br"), ("there's", ""), ("no", "am it"), ("code.", "am it")]],
    "l02": [[("It's", ""), ("just", ""), ("4", "br am big"), ("boxes.", "am big it")]],
    "l07": [[("Live", "co"), ("test.", "co")],
            [("Form", ""), ("in...", ""), ("and", ""), ("the", "br"), ("reply", "am"), ("is", "am"), ("already", "am it"), ("there.", "am it")]],
    "l08": [[("4", "am big"), ("boxes.", "am big it")],
            [("It", ""), ("runs", ""), ("all", "br am it"), ("night.", "am it")],
            [("Tag", ""), ("someone", ""), ("who", ""), ("still", "br"), ("replies", ""), ("at", ""), ("10", "co"), ("AM.", "co")]],
    "l09": [[("Comment", ""), ("FLOW,", "am"), ("and", ""), ("I'll", "br"), ("send", ""), ("you", ""), ("the", ""), ("template.", "am it")]],
}
# step cards: line id -> (number, card words, how many spoken words they cover after the spoken number)
STEPS = {"l03": ("1", ["A", "new", "form", "entry", "starts", "the", "flow."]),
         "l04": ("2", ["The", "lead", "saves", "to", "a", "sheet."]),
         "l05": ("3", ["They", "get", "an", "instant", "reply."]),
         "l06": ("4", ["Your", "phone", "buzzes", "with", "the", "lead."])}
ORDER = ["l00", "l01", "l02", "l03", "l04", "l05", "l06", "l07", "l08", "l09"]
GID = []                                       # (element id, show time) for every headline group / card, in order


def headline(lid):
    groups, ws = SPEC[lid], LW[lid]
    n_disp = sum(len(g) for g in groups)
    if n_disp != len(ws):
        raise SystemExit(f"{lid}: {n_disp} display words but {len(ws)} spoken: {[w['w'] for w in ws]}")
    i = 0
    for gi, g in enumerate(groups):
        parts = []
        gid = f"hl-{lid}-{gi}"
        for txt, cls in g:
            w = ws[i]
            if "br" in cls.split():
                parts.append("<br>")
            c = " ".join(x for x in cls.split() if x != "br")
            wid = f"{lid}w{i}"
            if lid == "l00" and gi == 0:
                c += " on"
            else:
                ft(f"#{wid}", w["t0"] - .05, .22, "{opacity: 0, y: 26, scale: .9}", "{opacity: 1, y: 0, scale: 1}", "back.out(2)")
            parts.append(f'<span class="w {c}" id="{wid}">{txt}</span>')
            i += 1
        HTML.append(f'<div class="hl" id="{gid}">' + " ".join(parts) + "</div>")
        GID.append((gid, ws[i - len(g)]["t0"]))


def step(lid):
    num, words = STEPS[lid]
    ws = LW[lid]
    gid = f"tip-{lid}"
    body = " ".join(f'<span class="tw" id="{lid}t{k}">{x}</span>' for k, x in enumerate(words))
    HTML.append(f'<div class="tip" id="{gid}"><div class="num">{num}</div><div class="tb">{body}</div></div>')
    t0 = ws[0]["t0"]
    ft(f"#{gid}", t0 - .14, .42, "{opacity: 0, y: 60, rotationX: -40}", "{opacity: 1, y: 0, rotationX: 0}", "back.out(1.6)")
    for k, w in enumerate(ws[1:len(words) + 1]):
        ft(f"#{lid}t{k}", w["t0"] - .04, .18, "{opacity: .25}", "{opacity: 1}", "power2.out")
    GID.append((gid, t0))
    sfx("g_pickup", t0 + .02)


for lid in ORDER:
    (step if lid in STEPS else headline)(lid)
# each group leaves as the next one arrives (the last one stays to the end)
for (a, ta), (b, tb) in zip(GID, GID[1:]):
    to(f"#{a}", tb - .13, .13, "{opacity: 0, y: -30, filter: 'blur(8px)'}", "power2.in")

# ---- LIVE TEST badge, comment box, handle, flashes
ft("#live", T["live"] - .1, .3, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}", "back.out(2.4)")
to("#live", T["already"] - .35, .2, "{opacity: 0, scale: .8}", "power2.in")
tc = T["cta"]
ft("#cbox", tc - .05, .45, "{opacity: 0, y: 50, scale: .9}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.8)")
for k, ch in enumerate("FLOW"):
    ft(f"#ck{k}", T["flow"] - .3 + k * .07, .05, "{opacity: 0}", "{opacity: 1}", "none")
    sfx("click", T["flow"] - .3 + k * .07)
ft("#cpost", T["flow"] + .05, .25, "{color: '#5a6274'}", "{color: '#ffb020'}", "power2.out")
ft("#handle", T["flow"] + .3, .5, "{opacity: 0, y: 20}", "{opacity: 1, y: 0}")
js(f'tl.set("#flash", {{opacity: .5, backgroundColor: "{AMBER}"}}, {T["seconds"] - .02:.3f});')
to("#flash", T["seconds"], .45, "{opacity: 0}", "power2.out")
js(f'tl.set("#flash", {{opacity: .45, backgroundColor: "{AMBER}"}}, {T["already"] - .02:.3f});')
to("#flash", T["already"], .45, "{opacity: 0}", "power2.out")
js(f'tl.set("#flash", {{opacity: .4, backgroundColor: "{AMBER}"}}, {T["flow"] + .08:.3f});')
to("#flash", T["flow"] + .1, .5, "{opacity: 0}", "power2.out")
ft("#dim", tc - .2, .5, "{opacity: 0}", "{opacity: 1}", "power2.out")

# ---- sound design on the beats
sfx("notify", T["eleven"] - .05)
for k in range(9):
    sfx("tick", T["ten"] - .85 + k * .13)
sfx("riser_short", T["ten"] - .9)
sfx("whoosh", T["ten"] + .3)
sfx("g_wrong", T["booked"] + .02)
sfx("thump", T["booked"] + .02)
sfx("whoosh_big", T["l01"] - .15)
for k in range(5):
    sfx("tick", T["l01"] + k * .1)
sfx("notify", T["seconds"] - .12)
sfx("sparkle", T["seconds"] - .02)
sfx("pop", T["code"])
sfx("whoosh_big", T["l02"] - .3)
for k in range(4):
    sfx("g_drop", T["boxes"] - .12 + k * .13)
sfx("impact", T["boxes"] + .3)
stepT = [T["s1"], T["s2"], T["s3"], T["s4"]]
for k in range(4):
    sfx("whoosh", stepT[k] - .55)
for k in range(3):
    sfx("g_swish", stepT[k + 1] - .7)
sfx("swish", T["form"] - .5)
sfx("g_pop", T["form"])
sfx("typing", T["sheet"] - .1)
sfx("g_pop", T["sheet"] + .05)
sfx("msg", T["instant"])
for k in ("name", "thank", "price", "booking"):
    sfx("pop", T[k] - .05)
sfx("buzzer", T["buzz"] + .05)
sfx("riser_short", T["live"] - .8)
sfx("whoosh_big", T["live"] - .35)
sfx("g_swish", T["formIn"])
hit = (T["already"] - .25 - T["formIn"] - .1) / 3
for k in range(4):
    sfx("g_tick", T["formIn"] + .1 + k * hit)
sfx("whoosh", T["already"] - .3)
sfx("g_correct", T["already"])
sfx("sparkle", T["already"] + .1)
sfx("whoosh_big", T["l08"])
sfx("sparkle", T["night"])
sfx("pop", T["tag"])
sfx("whoosh", tc - .1)
sfx("impact", T["flow"] + .1)
sfx("g_complete", T["flow"] + .2)

CSS = f"""
@font-face {{ font-family: Mont; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }}
@font-face {{ font-family: Serif; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }}
@font-face {{ font-family: Mono; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #05070d; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Mont; font-weight: 800; color: #f4f1ea; background: #05070d; }}
#gl {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
#dawn {{ position: absolute; inset: 0; pointer-events: none; opacity: 0;
  background: radial-gradient(120% 60% at 50% 100%, rgba(255,150,60,.55), rgba(255,120,60,.12) 55%, rgba(0,0,0,0) 80%); mix-blend-mode: screen; }}
#lost {{ position: absolute; inset: 0; pointer-events: none; opacity: 0; box-shadow: inset 0 0 260px 40px {CORAL}; }}
#vig {{ position: absolute; inset: 0; pointer-events: none; background: radial-gradient(95% 62% at 50% 55%, rgba(0,0,0,0) 55%, rgba(0,0,0,.6) 100%); }}
#dim {{ position: absolute; inset: 0; pointer-events: none; opacity: 0; background: linear-gradient(180deg, rgba(5,7,13,.35) 30%, rgba(5,7,13,.0) 55%); }}
#flash {{ position: absolute; inset: 0; background: {AMBER}; mix-blend-mode: screen; opacity: 0; pointer-events: none; }}
#bar {{ position: absolute; left: 70px; right: 70px; top: 262px; display: flex; justify-content: space-between; align-items: center;
  font-family: Mono; font-weight: 700; font-size: 24px; letter-spacing: .14em; color: #8a93a6; }}
#bar b {{ color: {AMBER}; font-weight: 700; }}
.hl {{ position: absolute; left: 60px; right: 60px; top: 330px; text-align: center; font-weight: 800; font-size: 82px; line-height: 1.05;
  letter-spacing: -.035em; text-shadow: 0 6px 30px rgba(0,0,0,.7); }}
.hl .w {{ display: inline-block; opacity: 0; }}
.hl .w.on {{ opacity: 1; }}
.st {{ color: {STEEL}; }} .am {{ color: {AMBER}; }} .co {{ color: {CORAL}; }}
.it {{ font-family: Serif; font-style: italic; font-weight: 400; letter-spacing: -.01em; font-size: 1.16em; }}
.big {{ font-size: 1.35em; }}
.tip {{ position: absolute; left: 70px; right: 70px; top: 330px; padding: 32px 36px 34px; border-radius: 34px; opacity: 0; transform-origin: 50% 100%;
  background: linear-gradient(160deg, rgba(28,34,46,.9), rgba(14,18,26,.9)); border: 2px solid rgba(255,176,32,.35);
  box-shadow: 0 30px 70px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.08); }}
.tip .num {{ position: absolute; left: -16px; top: -26px; width: 84px; height: 84px; border-radius: 50%; background: {AMBER}; color: #1a1206;
  display: grid; place-items: center; font-size: 50px; font-weight: 800; box-shadow: 0 0 34px rgba(255,176,32,.6); }}
.tb {{ padding-left: 54px; font-weight: 800; font-size: 60px; line-height: 1.08; letter-spacing: -.03em; }}
.tw {{ opacity: .25; }}
.lab {{ position: absolute; left: 0; top: 0; opacity: 0; padding: 10px 22px 9px; border-radius: 999px; font-family: Mono; font-weight: 700; font-size: 26px;
  letter-spacing: .1em; white-space: nowrap; color: #dfe7ff; background: rgba(14,20,34,.78); border: 2px solid rgba(91,140,255,.8); }}
.lab b {{ color: {AMBER}; }}
.rc {{ position: absolute; left: 0; top: 0; opacity: 0; padding: 14px 26px; border-radius: 22px 22px 22px 6px; font-weight: 800; font-size: 32px;
  white-space: nowrap; color: #1a1206; background: {AMBER}; box-shadow: 0 10px 30px rgba(255,176,32,.35); }}
#live {{ position: absolute; left: 50%; top: 1530px; margin-left: -150px; width: 300px; opacity: 0; padding: 14px 0; border-radius: 999px; text-align: center;
  font-family: Mono; font-weight: 700; font-size: 30px; letter-spacing: .16em; color: #fff; background: rgba(255,90,54,.16); border: 2px solid {CORAL}; }}
#live i {{ display: inline-block; width: 18px; height: 18px; border-radius: 50%; background: {CORAL}; margin-right: 14px; box-shadow: 0 0 16px {CORAL}; }}
#cbox {{ position: absolute; left: 90px; right: 90px; top: 690px; height: 132px; border-radius: 66px; opacity: 0; display: flex; align-items: center; gap: 24px;
  padding: 0 36px 0 26px; background: rgba(244,241,234,.97); color: #07090d; box-shadow: 0 30px 80px rgba(0,0,0,.6), 0 0 0 3px rgba(255,176,32,.6); }}
#cbox .av {{ width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(140deg, {AMBER}, {CORAL}); flex: none; }}
#cbox .tx {{ flex: 1; font-size: 54px; letter-spacing: .02em; }}
#cbox .tx span {{ opacity: 0; }}
#cpost {{ font-size: 36px; color: #5a6274; }}
#handle {{ position: absolute; left: 0; right: 0; top: 860px; text-align: center; font-family: Mono; font-weight: 700; font-size: 40px; letter-spacing: .08em; opacity: 0; }}
#handle span {{ color: {AMBER}; }}
"""
labs = "".join(f'<div class="lab" id="lab{k}"><b>{k + 1}</b> {n}</div>' for k, n in enumerate(["FORM", "SHEET", "REPLY", "ALERT"]))
rcs = "".join(f'<div class="rc" id="rc{k}">{n}</div>' for k, n in enumerate(["Hi Priya", "Thank you!", "Price list.pdf", "Book a slot"]))
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>samarpit.ai Lead auto-reply 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" width="1080" height="1920"></canvas>
      <div id="dawn"></div>
      <div id="lost"></div>
      <div id="vig"></div>
      <div id="dim"></div>
      {labs}
      {rcs}
      <div id="bar"><span><b>WED</b> &#183; SYSTEM BUILD</span><span>NO-CODE AUTOMATION</span></div>
      {chr(10).join(HTML)}
      <div id="live"><i></i>LIVE TEST</div>
      <div id="cbox"><div class="av"></div><div class="tx">{"".join(f'<span id="ck{k}">{c}</span>' for k, c in enumerate("FLOW"))}</div><b id="cpost">Post</b></div>
      <div id="handle"><span>@</span>samarpit.ai</div>
      <div id="flash"></div>
    </div>
    <script>window.LR_T = {json.dumps({k: round(v, 3) for k, v in T.items()})};</script>
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
