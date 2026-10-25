"""Fight Night: the /court skill (by @nocodealex) as a voxel boxing match. 1080x1920, 36 s.

python3 -I build/generate.py      (run from the project root)

The 3D world lives in assets/js/fight.js (Three.js, rendered on hf-seek). This file writes index.html: the canvas, the
cut times and punch times that fight.js reads, and the HTML overlay layer on a GSAP timeline (headlines, fighter
cards, the fight HUD, judge tags, scorecards, K.O., the rematch checklist, CTA and one-word captions).
Every on-screen claim about the candles case comes from the repo's examples/candles/VERDICT.md (a 3-juror run).
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 36.0
VO_LEN = 35.66

# speech runs of the commentator take (sped up 1.18x), from silence detection + local transcription
PHRASES = [
    (0.00, 1.27, "Ladies and gentlemen"), (1.69, 2.49, "Two Claudes"), (2.69, 3.46, "One idea."),
    (3.76, 5.14, "Only one leaves the ring."), (5.52, 6.94, "See, Claude on its own"),
    (7.15, 8.52, "agrees with everything you say."), (8.79, 10.37, "So tonight in the red corner"),
    (10.58, 12.74, "a Claude arguing your idea FAILS!"), (12.97, 13.96, "And in the blue corner"),
    (14.16, 15.67, "one arguing it WORKS!"), (15.88, 17.09, "Openings! Rebuttals!"),
    (17.22, 18.65, "Every point lands a punch!"), (18.87, 21.40, "Ringside, twelve Claude judges score it blind"),
    (21.54, 23.54, "an accountant, a customer, a competitor"), (23.78, 24.67, "Tonight's challenger:"),
    (24.82, 26.43, "quit nursing to sell candles."), (26.72, 28.33, "OHHH, it's a KNOCKOUT!"),
    (28.58, 30.88, "And the referee hands you exactly what to fix"), (31.12, 32.07, "before the rematch."),
    (32.27, 32.91, "It's free!"), (33.15, 35.54, "Comment FIGHT and I'll DM you the skill!"),
]

# cut and cue times shared with fight.js
T = {"redOn": 1.69, "blueOn": 2.05, "idea": 2.69, "ring": 3.6, "touch": 4.45, "yes": 5.4, "red": 8.65, "blue": 12.85,
     "fight": 15.8, "judges": 18.8, "named": [21.62, 22.3, 22.95], "screen": 23.7, "verdict": 25.75, "ko": 26.65,
     "knock": 27.6, "ref": 28.5, "raise": 29.0, "belt": 32.2, "end": DUR}
# punches in the exchange: (time, who lands it, power)
HITS = [(16.0, "r", .8), (16.55, "b", .8), (17.3, "r", .6), (17.6, "b", .6), (17.9, "r", .7), (18.35, "r", 1.0)]
# what each punch says (from the candles verdict)
PUNCH_TXT = ["$8K saved = ~5 months of rent", "40 sales at $28 already", "~13 sales a month. Rent needs ~57",
             "People really paid", "No stopping point", "No insurance. No plan B."]

KEYW = {"Claudes", "idea.", "ring.", "everything", "red", "FAILS!", "blue", "WORKS!", "Openings!", "Rebuttals!",
        "punch!", "twelve", "blind", "candles.", "KNOCKOUT!", "fix", "rematch.", "free!", "FIGHT", "skill!"}

A = []


def add(js):
    A.append("      " + js)


def words():
    out = []
    for a, z, text in PHRASES:
        ws = text.split()
        wt = [len(w.strip(".,:!?")) + 2 for w in ws]
        t, tot = a, sum(wt)
        for w, k in zip(ws, wt):
            d = (z - a) * k / tot
            out.append((round(t, 3), round(t + d, 3), w))
            t += d
    return out


def pop(sel, t, frm="scale:.5,opacity:0,y:40", d=.4, ease="back.out(2.2)"):
    add(f'tl.fromTo("{sel}",{{{frm}}},{{scale:1,opacity:1,x:0,y:0,rotation:0,rotationY:0,duration:{d},ease:"{ease}"}},{t:.2f});')


def out(sel, t, d=.2):
    add(f'tl.to("{sel}",{{opacity:0,y:-30,duration:{d},ease:"power2.in"}},{t:.2f});')


def head(cls, l1, acc, y=150):
    w = "".join(f'<span class="hw">{x}</span> ' for x in l1.split())
    return f'<div class="hd {cls}" style="top:{y}px"><div class="h1">{w}</div><div class="h2"><span class="acc">{acc}</span></div></div>'


def head_in(cls, t, t_out):
    add(f'tl.fromTo(".{cls} .hw",{{y:60,opacity:0,rotation:5}},{{y:0,opacity:1,rotation:0,duration:.35,stagger:.06,ease:"back.out(2.4)"}},{t:.2f});')
    add(f'tl.fromTo(".{cls} .acc",{{scale:.3,opacity:0,rotation:-8}},{{scale:1,opacity:1,rotation:0,duration:.45,ease:"back.out(2.8)"}},{t + .15:.2f});')
    out(f".{cls}", t_out)


def overlays():
    h = []
    h.append('<div class="lg mono">LADIES &amp; GENTLEMEN</div>')
    h.append(head("hA", "Two Claudes.", "One idea.", 700))
    h.append(head("hB", "Only one", "leaves the ring."))
    h.append(head("hC", "Claude agrees with", "everything."))
    for i, (w, x, y, r) in enumerate([("Genius!", 120, 520, -8), ("Love it!", 640, 470, 6), ("YES!", 170, 900, 5),
                                      ("Perfect!", 660, 860, -6), ("10/10!", 400, 400, -3)]):
        h.append(f'<div class="yb yb{i}" style="left:{x}px;top:{y}px;transform:rotate({r}deg)">{w}</div>')
    for side, name, tag, cls in (("RED CORNER", "THE PROSECUTOR", "IT'LL FAIL ✗", "red"), ("BLUE CORNER", "THE DEFENSE", "IT'LL WORK ✓", "blue")):
        h.append(f'<div class="fc fc-{cls}"><div class="mono fs">{side}</div><div class="fn">{name}</div>'
                 f'<div class="ft">{tag}</div><div class="fbar"></div></div>')
    # fight HUD
    h.append('<div class="hud"><div class="hb hb-r"><div class="hn">PROSECUTOR</div><div class="ht"><div class="hf hf-r"></div></div></div>'
             '<div class="vs">VS</div><div class="hb hb-b"><div class="hn">DEFENSE</div><div class="ht"><div class="hf hf-b"></div></div></div></div>')
    h.append('<div class="rnd rnd1"><div class="mono">ROUND 1</div><b>OPENINGS</b></div>')
    h.append('<div class="rnd rnd2"><div class="mono">ROUND 2</div><b>REBUTTALS</b></div>')
    for i, ((ht, who, p), txt) in enumerate(zip(HITS, PUNCH_TXT)):
        x = 90 if who == "r" else 470
        h.append(f'<div class="pt pt{i} pt-{who}" style="left:{x}px;top:{700 + (i % 3) * 120}px">'
                 f'<span class="bang">POW!</span>{txt}</div>')
    h.append('<div class="combo">COMBO <b>x3</b></div>')
    h.append(head("hG", "12 judges.", "Scoring blind."))
    h.append('<div class="blind">🙈 Nobody sees another card</div>')
    for i, (ic, nm) in enumerate([("🧮", "THE ACCOUNTANT"), ("🛍️", "THE CUSTOMER"), ("🏆", "THE COMPETITOR")]):
        h.append(f'<div class="jt jt{i}"><span>{ic}</span>{nm}</div>')
    h.append(head("hH", "Tonight's", "challenger."))
    h.append('<div class="tr mono">TEST RUN · 3 JUDGES</div>')
    for i, nm in enumerate(["STATISTICIAN", "PARENT", "LAWYER"]):
        h.append(f'<div class="sc sc{i}"><div class="mono">{nm}</div><b>GUILTY</b></div>')
    h.append('<div class="ohh">OHHH...</div><div class="ko">K.O.!</div><div class="ko2 mono">GUILTY · 3–0</div>')
    h.append(head("hJ", "What to fix", "before the rematch."))
    items = ["Reach ~57 sales a month first", "Get your rehire in writing", "Landlord OK + liability insurance"]
    h.append('<div class="ck"><div class="mono ckh">🥊 REMATCH CHECKLIST</div>' + "".join(
        f'<div class="ci ci{i}"><span class="tk">✓</span>{t}</div>' for i, t in enumerate(items)) +
        '<div class="cs">Sentence: <b>don\'t resign yet.</b></div></div>')
    h.append(head("hK", "It's", "free."))
    h.append('<div class="cbox"><div class="mono">ADD A COMMENT</div><div class="cin"><span class="typed"></span><span class="caret"></span>'
             '</div><div class="send">➤</div></div>')
    h.append('<div class="credit">/court skill by <b>@nocodealex</b> · free · MIT<br>A second opinion, not legal or financial advice</div>')
    return "".join(h)


def overlay_tl():
    add('tl.set(".rnd, .pt, .combo, .ko, .ko2, .ohh, .yb, .sc, .tr, .jt, .blind",{opacity:0},0);')
    pop(".lg", .1, "opacity:0,scale:1.4", .5, "power3.out")
    out(".lg", 1.6)
    head_in("hA", 1.7, 3.5)
    add('tl.fromTo(".hA .acc",{scale:.3,opacity:0},{scale:1,opacity:1,duration:.45,ease:"back.out(2.8)",immediateRender:false},2.69);')
    head_in("hB", 3.75, 5.35)
    head_in("hC", 5.55, 8.55)
    for i, t in enumerate((5.75, 6.3, 7.2, 7.75, 8.1)):
        pop(f".yb{i}", t, "scale:0,opacity:0,rotation:-20", .3, "back.out(3)")
        out(f".yb{i}", 8.55)
    # fighter cards
    for cls, a, z in (("red", 8.8, 12.8), ("blue", 13.0, 15.75)):
        pop(f".fc-{cls}", a, "x:-500,opacity:0", .45, "power4.out")
        add(f'tl.fromTo(".fc-{cls} .fbar",{{scaleX:0}},{{scaleX:1,duration:.5,ease:"power3.out"}},{a + .3:.2f});')
        pop(f".fc-{cls} .ft", a + 1.8 if cls == "red" else a + 1.2, "scale:2.2,opacity:0,rotation:-8", .35, "back.out(2)")
        out(f".fc-{cls}", z)
    # fight HUD
    pop(".hud", 15.82, "y:-160,opacity:0", .35, "power3.out")
    out(".hud", 18.75)
    for sel, a in ((".rnd1", 15.88), (".rnd2", 16.5)):
        pop(sel, a, "scale:2.5,opacity:0", .25, "power4.out")
        out(sel, a + .55)
    hp = {"r": 100, "b": 100}
    for i, (ht, who, p) in enumerate(HITS):
        target = "b" if who == "r" else "r"
        hp[target] -= int(p * 18)
        add(f'tl.to(".hf-{target}",{{scaleX:{hp[target] / 100:.2f},duration:.25,ease:"power2.out"}},{ht:.2f});')
        add(f'tl.fromTo(".hb-{target}",{{x:0}},{{x:12,duration:.04,yoyo:true,repeat:5,immediateRender:false}},{ht:.2f});')
        pop(f".pt{i}", ht, "scale:.2,opacity:0,rotation:-14", .25, "back.out(3)")
        out(f".pt{i}", ht + .55, .15)
    pop(".combo", 17.95, "scale:3,opacity:0,rotation:10", .25, "power4.out")
    out(".combo", 18.6)
    # judges
    head_in("hG", 19.0, 23.6)
    pop(".blind", 20.6, "y:40,opacity:0", .35)
    out(".blind", 23.6)
    for i, t in enumerate(T["named"]):
        pop(f".jt{i}", t, "x:-300,opacity:0", .3, "power4.out")
        out(f".jt{i}", 23.6)
    # challenger and the test-run votes
    head_in("hH", 23.8, 26.6)
    pop(".tr", 25.75, "y:30,opacity:0", .3)
    for i in range(3):
        pop(f".sc{i}", T["verdict"] + .15 + i * .25, "rotationY:90,opacity:0", .3, "power3.out")
    out(".tr, .sc", 26.6)
    # knockout
    pop(".ohh", 26.75, "scale:.4,opacity:0", .5, "power2.out")
    add('tl.to(".ohh",{scale:1.25,duration:.8,ease:"none"},27.0);')
    out(".ohh", 27.55, .1)
    pop(".ko", T["knock"], "scale:4,opacity:0,rotation:-12", .28, "power4.out")
    add(f'tl.fromTo(".ko",{{x:-14}},{{x:14,duration:.04,yoyo:true,repeat:7,immediateRender:false}},{T["knock"] + .28:.2f});')
    pop(".ko2", T["knock"] + .35, "y:40,opacity:0", .3)
    out(".ko, .ko2", 28.45)
    add(f'tl.set("#flash",{{opacity:.9}},{T["knock"]:.2f});tl.to("#flash",{{opacity:0,duration:.4}},{T["knock"] + .02:.2f});')
    for t in [h[0] for h in HITS]:
        add(f'tl.set("#flash",{{opacity:.35}},{t:.2f});tl.to("#flash",{{opacity:0,duration:.18}},{t + .01:.2f});')
    # rematch checklist
    head_in("hJ", 28.6, 32.1)
    pop(".ck", 28.95, "y:-200,opacity:0", .45, "power3.out")
    for i, t in enumerate((29.4, 30.0, 30.6)):
        pop(f".ci{i}", t, "x:-60,opacity:0", .3)
    pop(".cs", 31.2, "opacity:0,y:20", .3)
    out(".ck", 32.1)
    # CTA
    head_in("hK", 32.27, DUR + 1)
    pop(".cbox", 32.9, "y:200,opacity:0", .4, "power3.out")
    add('(()=>{const o={v:0};tl.to(o,{v:5,duration:.5,ease:"none",onUpdate:()=>{document.querySelector(".typed").textContent='
        '"FIGHT".slice(0,Math.floor(o.v+.001));}},33.55);})();')
    add(f'tl.to(".caret",{{opacity:0,duration:.01,yoyo:true,repeat:{int((DUR - 33) / .5) * 2 - 1},repeatDelay:.49}},33.0);')
    add('tl.to(".send",{scale:1.25,duration:.15,yoyo:true,repeat:3},34.2);')
    pop(".credit", 33.2, "opacity:0,y:20", .4, "power2.out")
    # whip flashes on every cut
    for t in (T["ring"], T["yes"], T["red"], T["blue"], T["fight"], T["judges"], T["screen"], T["verdict"], T["ko"], T["ref"], T["belt"]):
        add(f'tl.set("#whip",{{opacity:.85,x:260}},{t - .06:.2f});tl.to("#whip",{{opacity:0,x:-260,duration:.24,ease:"power2.out"}},{t - .05:.2f});')


def captions():
    ws = words()
    html = "".join(f'<div class="cw cw{i}{" key" if w in KEYW else ""}">{w.strip(".,:")}</div>' for i, (_, _, w) in enumerate(ws))
    for i, (s, e, w) in enumerate(ws):
        nxt = ws[i + 1][0] if i + 1 < len(ws) else DUR
        end = min(nxt, e + .25)
        add(f'tl.fromTo(".cw{i}",{{opacity:0,scale:.6,y:20}},{{opacity:1,scale:1,y:0,duration:.12,ease:"back.out(3)",immediateRender:false}},{s:.3f});')
        add(f'tl.set(".cw{i}",{{opacity:0}},{end:.3f});')
    add('tl.set(".cw",{opacity:0},0);')
    return html


CSS = """
@font-face { font-family: "Manrope"; font-weight: 200 800; src: url("assets/fonts/manrope.ttf"); }
@font-face { font-family: "Fraunces"; font-style: italic; font-weight: 100 900; src: url("assets/fonts/fraunces-italic.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 100 800; src: url("assets/fonts/jbmono.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #0b0814; }
body { font-family: "Manrope", sans-serif; color: #fff; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #0b0814; }
.clip { position: absolute; inset: 0; }
#gl { width: 1080px; height: 1920px; display: block; }
.mono { font: 700 26px "JBMono"; letter-spacing: 6px; }
#ov { z-index: 5; }
.hd { position: absolute; left: 0; width: 1080px; text-align: center; text-shadow: 0 6px 24px rgba(0,0,0,.55); }
.h1 { font: 800 82px/1.05 "Manrope"; letter-spacing: -2px; }
.h2 { font: italic 600 104px/1.08 "Fraunces"; color: #ffb347; letter-spacing: -2px; }
.hw, .acc { display: inline-block; }
.fc, .hud, .rnd, .pt, .combo, .ck, .cbox, .credit, .lg, .blind, .jt, .tr, .sc, .ko, .ko2, .ohh, .yb { opacity: 0; }
.lg { position: absolute; left: 0; width: 1080px; top: 220px; text-align: center; color: #ffd84a; font-size: 34px; letter-spacing: 12px;
  text-shadow: 0 0 30px rgba(255,216,74,.6); }
.yb { position: absolute; background: #fff; color: #111; font: 800 54px "Manrope"; padding: 18px 34px; border-radius: 30px;
  box-shadow: 0 16px 40px rgba(0,0,0,.25); }
.yb::after { content: ""; position: absolute; left: 50px; bottom: -18px; border: 14px solid transparent; border-top-color: #fff; }
.fc { position: absolute; left: 60px; top: 1060px; width: 700px; padding: 26px 36px 30px; border-radius: 26px; background: rgba(10,8,18,.82);
  border: 3px solid rgba(255,255,255,.15); }
.fc-red { border-color: #e03140; box-shadow: 0 0 60px rgba(224,49,64,.45); }
.fc-blue { left: 320px; border-color: #2f6bff; box-shadow: 0 0 60px rgba(47,107,255,.45); }
.fs { color: #ff8a92; font-size: 24px; }
.fc-blue .fs { color: #8fb0ff; }
.fn { font: 800 70px "Manrope"; letter-spacing: -1px; margin-top: 4px; }
.ft { display: inline-block; margin-top: 10px; font: 800 44px "Manrope"; padding: 6px 22px; border-radius: 14px; background: #e03140; }
.fc-blue .ft { background: #2f6bff; }
.fbar { position: absolute; left: 0; bottom: 0; height: 8px; width: 100%; background: #e03140; transform-origin: 0 50%; border-radius: 0 0 26px 26px; }
.fc-blue .fbar { background: #2f6bff; }
.hud { position: absolute; left: 40px; right: 40px; top: 120px; display: flex; align-items: center; gap: 18px; }
.hb { flex: 1; }
.hn { font: 800 30px "Manrope"; margin-bottom: 8px; }
.hb-b .hn { text-align: right; }
.ht { height: 34px; border-radius: 10px; background: rgba(255,255,255,.18); border: 3px solid #fff; overflow: hidden; }
.hf { height: 100%; width: 100%; }
.hf-r { background: linear-gradient(90deg, #ff6b6b, #e03140); transform-origin: 0 50%; }
.hf-b { background: linear-gradient(270deg, #7aa2ff, #2f6bff); transform-origin: 100% 50%; }
.vs { font: italic 900 64px "Fraunces"; color: #ffd84a; text-shadow: 0 0 20px rgba(255,216,74,.7); }
.rnd { position: absolute; left: 0; width: 1080px; top: 330px; text-align: center; }
.rnd .mono { color: #ffd84a; font-size: 34px; }
.rnd b { display: block; font: 900 120px "Manrope"; letter-spacing: -3px; text-shadow: 0 8px 30px rgba(0,0,0,.6); }
.pt { position: absolute; width: 520px; padding: 20px 26px; border-radius: 22px; font: 800 40px/1.15 "Manrope"; background: #fff; color: #111;
  box-shadow: 0 18px 40px rgba(0,0,0,.35); }
.pt-r { border: 5px solid #e03140; }
.pt-b { border: 5px solid #2f6bff; }
.bang { display: block; font: italic 900 30px "Fraunces"; color: #e03140; }
.pt-b .bang { color: #2f6bff; }
.combo { position: absolute; right: 70px; top: 560px; font: 900 64px "Manrope"; color: #ffd84a; transform: rotate(-6deg);
  text-shadow: 0 6px 24px rgba(0,0,0,.6); }
.combo b { font-size: 90px; }
.blind { position: absolute; left: 0; width: 1080px; top: 470px; text-align: center; font: 700 40px "Manrope";
  text-shadow: 0 4px 18px rgba(0,0,0,.6); }
.jt { position: absolute; left: 70px; display: flex; align-items: center; gap: 16px; font: 800 44px "Manrope"; padding: 14px 30px;
  border-radius: 40px; background: #fff; color: #111; box-shadow: 0 14px 34px rgba(0,0,0,.35); }
.jt span { font-size: 54px; }
.jt0 { top: 1000px; } .jt1 { top: 1110px; left: 160px; } .jt2 { top: 1220px; left: 250px; }
.tr { position: absolute; left: 0; width: 1080px; top: 470px; text-align: center; color: #ffd84a; }
.sc { position: absolute; top: 1030px; width: 300px; padding: 20px 0; border-radius: 22px; text-align: center; background: #e03140;
  box-shadow: 0 18px 40px rgba(0,0,0,.35); }
.sc .mono { font-size: 22px; letter-spacing: 3px; }
.sc b { display: block; font: 900 54px "Manrope"; }
.sc0 { left: 40px; } .sc1 { left: 390px; } .sc2 { left: 740px; }
.ohh { position: absolute; left: 0; width: 1080px; top: 330px; text-align: center; font: italic 900 130px "Fraunces"; color: #ffd84a; }
.ko { position: absolute; left: 0; width: 1080px; top: 520px; text-align: center; font: 900 330px/1 "Manrope"; color: #ffd84a; letter-spacing: -10px;
  -webkit-text-stroke: 10px #111; text-shadow: 0 16px 0 #e03140, 0 30px 60px rgba(0,0,0,.6); }
.ko2 { position: absolute; left: 0; width: 1080px; top: 900px; text-align: center; font-size: 46px; color: #fff; text-shadow: 0 4px 18px rgba(0,0,0,.7); }
.ck { position: absolute; left: 70px; top: 400px; width: 940px; padding: 36px 40px; border-radius: 30px; background: #fffaf0; color: #111;
  box-shadow: 0 30px 70px rgba(0,0,0,.45); border: 5px solid #f4c542; }
.ckh { color: #b5222e; font-size: 26px; letter-spacing: 4px; margin-bottom: 10px; }
.ci { display: flex; align-items: center; gap: 18px; font: 700 42px/1.2 "Manrope"; padding: 12px 0; }
.tk { flex: none; width: 54px; height: 54px; border-radius: 50%; background: #3e8e62; color: #fff; display: flex; align-items: center; justify-content: center;
  font-size: 34px; }
.cs { margin-top: 14px; font: 600 36px "Manrope"; color: #444; }
.cs b { color: #b5222e; }
.cbox { position: absolute; left: 90px; top: 1130px; width: 900px; padding: 30px 36px; border-radius: 30px; background: #fff; color: #111;
  box-shadow: 0 30px 70px rgba(0,0,0,.4); }
.cbox .mono { color: #777; font-size: 24px; }
.cin { margin-top: 16px; width: 700px; height: 110px; border-radius: 22px; border: 5px solid #e03140; display: flex; align-items: center; padding: 0 30px;
  font: 800 72px "Manrope"; letter-spacing: 4px; }
.caret { width: 6px; height: 70px; background: #111; margin-left: 6px; }
.send { position: absolute; right: 36px; top: 76px; width: 120px; height: 110px; border-radius: 22px; background: #111; color: #fff; font-size: 52px;
  display: flex; align-items: center; justify-content: center; }
.credit { position: absolute; left: 0; width: 1080px; top: 1345px; text-align: center; font: 600 30px/1.4 "Manrope"; color: rgba(255,255,255,.9);
  text-shadow: 0 3px 12px rgba(0,0,0,.6); }
.credit b { color: #ffd84a; }
#caps { z-index: 6; }
.cw { position: absolute; left: 0; width: 1080px; top: 1455px; text-align: center; font: 900 92px "Manrope"; letter-spacing: -2px;
  color: #fff; text-shadow: 0 0 2px #000, 0 4px 0 rgba(0,0,0,.55), 0 10px 30px rgba(0,0,0,.75); opacity: 0; }
.cw.key { color: #ffb347; }
#fx { z-index: 7; }
#flash { position: absolute; inset: 0; background: #fff; opacity: 0; }
#whip { position: absolute; inset: 0; opacity: 0; background: repeating-linear-gradient(0deg, rgba(255,255,255,0) 0 20px,
  rgba(255,255,255,.6) 20px 24px, rgba(255,255,255,0) 24px 64px); }
#vig { position: absolute; inset: 0; background: radial-gradient(120% 80% at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.45) 100%),
  linear-gradient(180deg, rgba(0,0,0,.45) 0%, rgba(0,0,0,0) 22%, rgba(0,0,0,0) 62%, rgba(0,0,0,.6) 100%); }
"""


def main():
    ov_html = overlays()
    overlay_tl()
    cap_html = captions()
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Fight Night 9x16</title>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js"}}}}</script>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0"></canvas>
      <div id="vigl" class="clip" data-start="0" data-duration="{DUR}" data-track-index="1" data-layout-ignore><div id="vig"></div></div>
      <div id="ov" class="clip" data-start="0" data-duration="{DUR}" data-track-index="2" data-layout-allow-overflow>{ov_html}</div>
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3">{cap_html}</div>
      <div id="fx" class="clip" data-start="0" data-duration="{DUR}" data-track-index="4" data-layout-ignore><div id="whip"></div><div id="flash"></div></div>
      <audio id="vo" src="assets/audio/vo.wav" data-start="0" data-duration="{VO_LEN}" data-track-index="10" data-volume="1"></audio>
      <audio id="music" src="assets/audio/music.wav" data-start="0" data-duration="{DUR}" data-track-index="11" data-volume="1"></audio>
    </div>
    <script>
      window.FIGHT_T = {json.dumps(T)};
      window.FIGHT_HITS = {json.dumps(HITS)};
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      tl.set("#flash, #whip", {{opacity:0}}, 0);
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
    <script type="module" src="assets/js/fight.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    print("wrote index.html", len(html) // 1024, "KB")


if __name__ == "__main__":
    main()
