"""The Secret Free Store reel (@ai.nxtlvl): writes index.html. 1080x1920, 30 fps.

python3 build/generate.py      (from the project root, after build/voice.py)

Nxtlvl Bot sneaks through a mall of paid apps, finds a hidden door marked GitHub and opens six loot chests, each a free
repo that replaces a paid app, rarer and rarer: Typeform -> Formbricks and Mailchimp -> Listmonk (rare), DocuSign ->
Documenso and Google Analytics -> Umami (epic), Otter -> Whisper (legendary), Zapier -> n8n (mythic). Three more chests
stay locked: they open in the DMs. Keyword CTA: comment REPO (the auto-DM sends all nine links).

The 3D (assets/js/store.js) plays the shot list. This file writes the HTML layer: the hook title, the game HUD (loot
counter and money saved), the area toast, a rarity banner and a swap card for every chest, FREE stamps, the mythic and
secret banners, word-by-word captions and the end card (an inventory with three locked slots). Prices: the cheapest paid
plan, billed monthly, checked 2026-11-10 (see build/PRICES.md).
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
VL = json.load(open(os.path.join(ROOT, "voice", "lines.json")))
LINES = VL["lines"]
WORDS = json.load(open(os.path.join(B, "words.json")))
DUR = round(VL["duration"], 2)
r3 = lambda x: round(x, 3)  # noqa: E731

L = [None] + [ln["start"] for ln in LINES]
E = [None] + [ln["end"] for ln in LINES]
PS = [None] + [[None] + [p["start"] for p in ln["phrases"]] for ln in LINES]
PE = [None] + [[None] + [p["end"] for p in ln["phrases"]] for ln in LINES]
DOOR = E[2] + .05
K = {
    "cB": PS[1][3] - .12, "cC": L[2] - .12, "door": DOOR, "cD": DOOR + .12, "cE": DOOR + .85,
    "cF": L[3] - .06, "shakeR1": L[3], "openR1": PS[3][3],
    "cG": L[4] - .1, "shakeR2": L[4], "openR2": PS[4][2],
    "cH1": L[5] - .1, "shakeE": L[5], "openE1": PS[5][3], "cH2": PS[5][4] - .1, "openE2": PS[5][5],
    "cI1": L[6] - .1, "shakeG": L[6], "openG": PS[6][3], "cI2": PS[6][4] - .1,
    "cJ1": L[7] - .15, "lev": PS[7][2], "cJ2": E[7] - .05,
    "myth": PS[8][2], "cK": PS[8][2], "cL": PS[8][3] - .05,
    "cM": L[9] - .1, "rattle": L[9] + .9, "cN": PS[9][2] - .1, "wink": PE[9][2] - .55,
    "cO": L[10] - .1, "endc": L[10] - .1,
}
K = {k: r3(v) for k, v in K.items()}
FREE = [PS[3][4], PS[4][3], PS[6][5], PS[8][4]]

# the six chests: [id, rarity, paid name, paid logo (img or None), paid price, price note, free name, free tag, shake, show paid, open, hide]
CH = [
    ("r1", "rare", "Typeform", "typeform", "$39", "/mo", "Formbricks", "FREE · OPEN SOURCE", K["shakeR1"], PS[3][2], K["openR1"], K["cG"]),
    ("r2", "rare", "Mailchimp", "mailchimp", "$13", "/mo", "Listmonk", "FREE · OPEN SOURCE", K["shakeR2"], PS[4][1], K["openR2"], K["cH1"]),
    ("e1", "epic", "DocuSign", None, "$15", "/mo", "Documenso", "FREE · OPEN SOURCE", K["shakeE"], PS[5][2], K["openE1"], K["cH2"]),
    ("e2", "epic", "Google Analytics", None, "$0*", "you pay with your data", "Umami", "FREE · OPEN SOURCE · YOUR DATA", K["cH2"], PS[5][4], K["openE2"], K["cI1"]),
    ("g1", "legendary", "Otter.ai", "otter", "$16.99", "/mo", "Whisper", "FREE · RUNS OFFLINE", K["shakeG"], PS[6][2], K["openG"], K["cJ1"]),
    ("m1", "mythic", "Zapier", "zapier", "$29.99", "/mo", "n8n", "FREE TO SELF-HOST · FAIR-CODE", PS[8][1] - .06, PS[8][1], K["myth"], K["cM"]),
]
SAVE = [39, 13, 15, 0, 16.99, 29.99]
RCOL = {"rare": "#3D8BFF", "epic": "#B45CFF", "legendary": "#FFC233", "mythic": "#FF2E4D", "secret": "#8F7BFF"}
LOGO = {"typeform": "assets/img/typeform.webp", "mailchimp": "assets/img/mailchimp.png", "otter": "assets/img/otter.png", "zapier": "assets/img/zapier.png"}
A = []


def add(js):
    A.append("      " + js)


def show(sel, t, d=.3, frm="opacity:0,y:14", to="opacity:1,y:0", ease="power2.out"):
    add(f'tl.fromTo("{sel}",{{{frm}}},{{{to},duration:{d},ease:"{ease}",immediateRender:false}},{t:.3f});')


def hide(sel, t, d=.22, props="opacity:0"):
    add(f'tl.to("{sel}",{{{props},duration:{d},ease:"power2.in"}},{t:.3f});')


def slam(sel, t, s0=1.8, d=.32):
    add(f'tl.fromTo("{sel}",{{opacity:0,scale:{s0}}},{{opacity:1,scale:1,duration:{d},ease:"back.out(2.2)",immediateRender:false}},{t:.3f});')


def setText(sel, txt, t):
    add(f'tl.set("{sel}",{{textContent:{json.dumps(txt)}}},{t:.3f});')


def story():
    html = []
    # the hook title is on screen from the very first frame
    show("#title", 0.0, .01, "opacity:1", "opacity:1")
    add('tl.fromTo("#title .t2",{scale:1.12},{scale:1,duration:.5,ease:"back.out(2)",immediateRender:false},0);')
    add('tl.fromTo("#title .t3",{opacity:0,y:10},{opacity:1,y:0,duration:.3,ease:"power2.out",immediateRender:false},%.3f);' % (PS[1][3] - .05))
    hide("#title", K["cC"] - .05, .25, "opacity:0,y:-24")
    # the door
    # the vault: area toast and the HUD
    slam("#area", K["cE"] + .05, 1.25, .3)
    hide("#area", K["cF"] - .02, .18, "opacity:0,y:-20")
    show("#hud", K["cE"] + .1, .35, "opacity:0,y:-16")
    hide("#hud", K["endc"] - .05, .3, "opacity:0,y:-16")
    saved, loot = 0.0, 0
    for k, c in enumerate(CH):
        cid, rar, pname, logo, price, note, fname, ftag, t_shake, t_paid, t_open, t_hide = c
        sid = f"#{cid}"
        show(sid, t_shake - .02, .01, "opacity:0", "opacity:1")
        slam(f"{sid} .rar", t_shake, 1.9, .3)
        show(f"{sid} .card", t_paid - .08, .2, "opacity:0,scale:.9", "opacity:1,scale:1")
        show(f"{sid} .paid", t_paid - .05, .25, "opacity:0,x:-30", "opacity:1,x:0")
        add(f'tl.fromTo("{sid} .strike",{{scaleX:0}},{{scaleX:1,duration:.2,ease:"power2.out",immediateRender:false}},{t_open - .05:.3f});')
        add(f'tl.to("{sid} .paid",{{opacity:.55,duration:.2}},{t_open + .1:.3f});')
        slam(f"{sid} .free", t_open + .02, 1.5, .32)
        hide(sid, t_hide - .02, .15)
        # the HUD: loot and money saved
        loot += 1
        setText("#hud .lt-n", f"{loot}/9", t_open + .1)
        add(f'tl.fromTo("#hud .lt",{{scale:1.25}},{{scale:1,duration:.4,ease:"back.out(2)",immediateRender:false}},{t_open + .1:.3f});')
        new = round(saved + SAVE[k], 2)
        if SAVE[k]:
            for j in range(1, 9):
                setText("#hud .sv-n", f"${saved + (new - saved) * j / 8:,.2f}", t_open + .1 + j * .04)
            add(f'tl.fromTo("#hud .sv",{{scale:1.25}},{{scale:1,duration:.4,ease:"back.out(2)",immediateRender:false}},{t_open + .45:.3f});')
        saved = new
        html.append(card(c))
    # FREE stamps
    for k, t0 in enumerate(FREE):
        slam(f"#free{k}", t0 - .03, 1.6, .24)
        hide(f"#free{k}", t0 + .75, .2)
    # the mythic: the banner on "MYTHIC"
    slam("#mythic", K["lev"] - .02, 2.2, .35)
    add(f'tl.fromTo("#mythic",{{x:-6}},{{x:6,duration:.05,repeat:15,yoyo:true,ease:"none",immediateRender:false}},{K["lev"] + .35:.3f});')
    hide("#mythic", PS[8][1] - .1, .1)
    # the year: the saved pill flips to per year
    setText("#hud .sv-u", "/yr", K["cM"] + .2)
    setText("#hud .sv-n", f"${saved * 12:,.0f}", K["cM"] + .2)
    add(f'tl.fromTo("#hud .sv",{{scale:1.3}},{{scale:1,duration:.45,ease:"back.out(2)",immediateRender:false}},{K["cM"] + .2:.3f});')
    # the secret chests
    slam("#secret", K["cM"] + .1, 1.6, .3)
    slam("#secret .dm", PS[9][2] + .05, 1.5, .28)
    hide("#secret", K["endc"] - .05, .2)
    # the end card
    show("#endc", K["endc"], .01, "opacity:0", "opacity:1")
    show("#endc .e0", K["endc"] + .02, .25, "opacity:0,y:-12")
    slam("#endc .e1", K["endc"] + .22, 1.7, .36)
    show("#endc .e2", K["endc"] + .55, .3)
    for j in range(9):
        show(f"#endc .slot{j}", K["endc"] + .75 + j * .07, .22, "opacity:0,scale:.6", "opacity:1,scale:1")
    add(f'tl.fromTo("#endc .lock",{{rotation:-10}},{{rotation:10,duration:.08,repeat:7,yoyo:true,ease:"none",immediateRender:false}},{K["endc"] + 1.6:.3f});')
    show("#endc .e3", K["endc"] + 1.45, .3)
    add(f'tl.fromTo("#endc .e1",{{scale:1}},{{scale:1.05,duration:.45,repeat:7,yoyo:true,ease:"sine.inOut",immediateRender:false}},{K["endc"] + .6:.3f});')
    return "".join(html)


def card(c):
    cid, rar, pname, logo, price, note, fname, ftag, *_ = c
    if logo == "typeform":
        badge = f'<span class="lg wide"><img src="{LOGO[logo]}" style="object-position:50% 50%;transform:scale(2.1)"></span>'
    elif logo == "zapier":
        badge = f'<span class="lg wide"><img src="{LOGO[logo]}" style="object-fit:contain;transform:scale(1.05)"></span>'
    elif logo:
        badge = f'<span class="lg sq"><img src="{LOGO[logo]}"></span><span class="nm">{pname}</span>'
    else:
        badge = f'<span class="nm">{pname}</span>'
    pr = f'<span class="pr">{price}<small>{note}</small></span>'
    return (f'<div class="loot {rar}" id="{cid}"><div class="rar">{rar.upper()}</div><div class="card">'
            f'<div class="paid">{badge}{pr}<i class="strike"></i></div>'
            f'<div class="free"><span class="fn">{fname}</span><span class="ft">{ftag}</span></div></div></div>')


def captions():
    """Word-by-word captions, one phrase at a time, on a dark pill; the word being said is lit."""
    html, k = [], 0
    for li, ln in enumerate(LINES):
        if li == len(LINES) - 1:
            continue                                   # the end card says the last line
        ws = [w for w in WORDS if w["line"] == li + 1]
        for p in ln["phrases"]:
            pw = [w for w in ws if p["start"] - .06 <= w["s"] + .02 < p["end"] + .02]
            if not pw:
                continue
            cid = f"c{k}"; k += 1
            spans = "".join(f'<span class="w" id="{cid}w{j}">{w["w"]}</span> ' for j, w in enumerate(pw))
            html.append(f'<div class="cap" id="{cid}"><span class="tx">{spans.strip()}</span></div>')
            a, b = pw[0]["s"] - .05, pw[-1]["e"] + .12
            add(f'tl.fromTo("#{cid}",{{opacity:0,scale:.92}},{{opacity:1,scale:1,duration:.1,ease:"power2.out",immediateRender:false}},{a:.3f});')
            for j, w in enumerate(pw):
                add(f'tl.fromTo("#{cid}w{j}",{{opacity:.35}},{{opacity:1,duration:.06,immediateRender:false}},{w["s"] - .03:.3f});')
                add(f'tl.set("#{cid}w{j}",{{color:"#6FF7FF"}},{w["s"] - .03:.3f});')
                add(f'tl.set("#{cid}w{j}",{{color:"#FFFFFF"}},{w["e"]:.3f});')
            add(f'tl.to("#{cid}",{{opacity:0,duration:.08}},{b:.3f});')
    return "".join(html)


CSS = """
@font-face { font-family: "Manrope"; font-weight: 200 800; src: url("assets/fonts/manrope.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/jbmono-bold.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #0B0A12; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #0B0A12; }
.clip { position: absolute; inset: 0; }
#gl { width: 1080px; height: 1920px; display: block; }
#title, #quest, #area, #hud, .loot, .stamp, #mythic, #secret, #secret .dm, #endc, #endc .e0, #endc .e1, #endc .e2, #endc .e3, #endc .slot, .cap { opacity: 0; }
.sh { text-shadow: 0 4px 0 rgba(14,18,32,.55), 0 8px 26px rgba(0,0,0,.45); }
#title { position: absolute; left: 60px; right: 60px; top: 268px; text-align: center; color: #FFFFFF; }
#title .t0 { display: inline-block; padding: 9px 22px; border-radius: 30px; background: #0E1220; color: #6FF7FF; font: 800 30px/1 "JBMono"; letter-spacing: 5px; border: 3px solid #45F3FF; }
#title .t1 { display: block; margin-top: 18px; font: 800 74px/1 "Manrope"; letter-spacing: 1px; }
#title .t2 { display: block; font: 800 128px/1.02 "Manrope"; letter-spacing: -2px; color: #FFB08F; -webkit-text-stroke: 4px #0E1220; paint-order: stroke fill; }
#title .t3 { display: inline-block; margin-top: 14px; padding: 10px 24px; border-radius: 18px; background: rgba(14,18,32,.86); font: 800 44px/1.1 "Manrope"; }
#title .t3 b { color: #6FF7FF; }
#quest { position: absolute; left: 50%; top: 300px; width: 520px; margin-left: -260px; padding: 16px 0; border-radius: 22px; background: rgba(14,18,32,.88); border: 3px solid #45F3FF; text-align: center; }
#quest .q0 { display: block; font: 700 24px/1 "JBMono"; letter-spacing: 5px; color: #6FF7FF; }
#quest .q1 { display: block; margin-top: 8px; font: 800 46px/1 "Manrope"; color: #FFFFFF; }
#area { position: absolute; left: 70px; right: 70px; top: 390px; text-align: center; }
#area .a0 { display: inline-block; padding: 8px 20px; border-radius: 12px; background: #FFC233; color: #2A1A00; font: 700 28px/1 "JBMono"; letter-spacing: 5px; }
#area .a1 { display: block; margin-top: 12px; font: 800 82px/1 "Manrope"; color: #FFFFFF; letter-spacing: -1px; }
#area .a1 b { color: #FFD36B; }
#hud { position: absolute; left: 56px; right: 56px; top: 262px; display: flex; justify-content: space-between; }
#hud .pill { display: flex; align-items: center; gap: 14px; height: 92px; padding: 0 24px 0 14px; border-radius: 40px; background: rgba(14,18,32,.86); border: 3px solid rgba(255,255,255,.18); color: #FFFFFF; }
#hud .lt, #hud .sv { transform-origin: 50% 50%; }
#hud .ic { width: 52px; height: 52px; border-radius: 14px; display: flex; align-items: center; justify-content: center; }
#hud .chest { background: #7A5233; border: 4px solid #FFC233; border-radius: 10px; position: relative; }
#hud .chest::after { content: ""; position: absolute; left: 0; right: 0; top: 14px; height: 5px; background: #FFC233; }
#hud .coin { border-radius: 50%; background: radial-gradient(circle at 35% 35%, #FFE08A, #F2B533 60%, #B9801A); border: 3px solid #FFE9A8; font: 800 28px/1 "Manrope"; color: #7A4E00; }
#hud .lab { display: block; font: 700 28px/1 "JBMono"; letter-spacing: 3px; color: rgba(255,255,255,.75); }
#hud .val { display: block; margin-top: 4px; font: 800 38px/1 "Manrope"; }
#hud .sv .val { color: #7CF5A0; }
#hud .sv-u { font-size: 28px; color: rgba(255,255,255,.7); margin-left: 2px; }
.loot { position: absolute; left: 70px; right: 70px; top: 372px; text-align: center; }
.loot .rar { display: inline-block; padding: 10px 34px; border-radius: 16px; font: 800 52px/1 "Manrope"; letter-spacing: 8px; color: #FFFFFF; transform-origin: 50% 50%; }
.loot.rare .rar { background: linear-gradient(180deg, #5AA0FF, #2A6BE0); box-shadow: 0 0 40px rgba(61,139,255,.75), inset 0 -6px 0 rgba(0,0,0,.2); }
.loot.epic .rar { background: linear-gradient(180deg, #C77CFF, #8A2FE0); box-shadow: 0 0 40px rgba(180,92,255,.75), inset 0 -6px 0 rgba(0,0,0,.2); }
.loot.legendary .rar { background: linear-gradient(180deg, #FFD966, #F0A400); color: #3A2400; box-shadow: 0 0 50px rgba(255,194,51,.85), inset 0 -6px 0 rgba(0,0,0,.15); }
.loot.mythic .rar { background: linear-gradient(180deg, #FF5A72, #C8102E); box-shadow: 0 0 60px rgba(255,46,77,.95), inset 0 -6px 0 rgba(0,0,0,.25); }
.loot .card { margin-top: 18px; padding: 20px 26px 22px; border-radius: 28px; background: rgba(14,18,32,.9); border: 3px solid rgba(255,255,255,.14); }
.loot.rare .card { border-color: rgba(61,139,255,.7); } .loot.epic .card { border-color: rgba(180,92,255,.7); }
.loot.legendary .card { border-color: rgba(255,194,51,.85); } .loot.mythic .card { border-color: rgba(255,46,77,.9); }
.loot .paid { position: relative; display: inline-flex; align-items: center; gap: 16px; height: 76px; padding: 0 6px; }
.loot .paid .lg { display: inline-flex; align-items: center; justify-content: center; overflow: hidden; background: #FFFFFF; flex: none; }
.loot .paid .lg.sq { width: 64px; height: 64px; border-radius: 16px; }
.loot .paid .lg.wide { width: 250px; height: 64px; border-radius: 14px; }
.loot .paid .lg img { width: 100%; height: 100%; object-fit: cover; }
.loot .paid .lg.sq img { object-fit: contain; }
.loot .paid .nm { font: 800 44px/1 "Manrope"; color: #FFFFFF; white-space: nowrap; }
.loot .paid .pr { font: 800 44px/1 "Manrope"; color: #FF8A80; white-space: nowrap; }
.loot .paid .pr small { font-size: 28px; margin-left: 4px; color: rgba(255,138,128,.85); }
.loot .strike { position: absolute; left: -10px; right: -10px; top: 50%; height: 7px; margin-top: -3px; border-radius: 4px; background: #FF3B30; transform-origin: 0 50%; transform: scaleX(0); }
.loot .paid, .loot .card { opacity: 0; }
.loot .free { margin-top: 12px; opacity: 0; transform-origin: 50% 50%; }
.loot .free .fn { display: block; font: 800 96px/1 "Manrope"; letter-spacing: -2px; color: #FFFFFF; }
.loot.rare .free .fn { color: #8FC0FF; } .loot.epic .free .fn { color: #D9A8FF; } .loot.legendary .free .fn { color: #FFD966; } .loot.mythic .free .fn { color: #FF8A9A; }
.loot .free .ft { display: inline-block; margin-top: 12px; padding: 8px 18px; border-radius: 12px; background: #7CF5A0; color: #062A12; font: 700 28px/1 "JBMono"; letter-spacing: 1px; }
.stamp { position: absolute; left: 90px; top: 1030px; width: 440px; padding: 14px 0; text-align: center; border: 10px solid #7CF5A0; border-radius: 26px; color: #7CF5A0;
  font: 800 130px/1 "Manrope"; letter-spacing: 10px; transform: rotate(-9deg); text-shadow: 0 0 30px rgba(124,245,160,.6); box-shadow: 0 0 40px rgba(124,245,160,.35), inset 0 0 30px rgba(124,245,160,.25); background: #06200F; }
#mythic { position: absolute; left: 0; right: 0; top: 420px; text-align: center; }
#mythic span { display: inline-block; padding: 14px 44px; border-radius: 20px; background: linear-gradient(180deg, #FF5A72, #B00C28); color: #FFFFFF; font: 800 112px/1 "Manrope"; letter-spacing: 12px; box-shadow: 0 0 80px rgba(255,46,77,.95); }
#mythic small { display: block; margin-top: 18px; font: 700 30px/1 "JBMono"; letter-spacing: 6px; color: #FF8A9A; }
#secret { position: absolute; left: 70px; right: 70px; top: 372px; text-align: center; }
#secret .s0 { display: inline-block; padding: 12px 30px; border-radius: 18px; background: linear-gradient(180deg, #A795FF, #6A4FE0); color: #FFFFFF; font: 800 56px/1 "Manrope"; letter-spacing: 3px; box-shadow: 0 0 50px rgba(143,123,255,.8); }
#secret .s1 { display: block; margin-top: 14px; font: 700 30px/1 "JBMono"; letter-spacing: 5px; color: #D6CCFF; }
#secret .dm { display: inline-block; margin-top: 22px; padding: 16px 30px; border-radius: 22px; background: rgba(14,18,32,.9); border: 3px solid #A795FF; color: #FFFFFF; font: 800 44px/1 "Manrope"; }
#secret .dm b { color: #6FF7FF; }
#endc { position: absolute; left: 0; right: 0; top: 0; bottom: 0; }
#endc .e0 { position: absolute; left: 0; right: 0; top: 270px; text-align: center; font: 800 64px/1 "Manrope"; letter-spacing: 6px; color: #FFFFFF; }
#endc .e1 { position: absolute; left: 0; right: 0; top: 350px; text-align: center; transform-origin: 50% 50%; }
#endc .e1 span { display: inline-block; padding: 6px 46px 14px; border-radius: 34px; background: linear-gradient(180deg, #FFE08A, #F2A93B); color: #2A1500; font: 800 200px/1 "Manrope"; letter-spacing: 10px;
  box-shadow: 0 0 70px rgba(255,194,51,.85), inset 0 -10px 0 rgba(0,0,0,.18); border: 6px solid #FFF3C4; }
#endc .e2 { position: absolute; left: 0; right: 0; top: 600px; text-align: center; font: 800 52px/1.1 "Manrope"; color: #FFFFFF; }
#endc .e2 b { color: #6FF7FF; }
#endc .grid { position: absolute; left: 130px; right: 130px; top: 690px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
#endc .slot { height: 88px; border-radius: 18px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: rgba(14,18,32,.9); border: 3px solid; }
#endc .slot b { font: 800 32px/1 "Manrope"; color: #FFFFFF; }
#endc .slot i { font: 700 17px/1 "JBMono"; font-style: normal; letter-spacing: 2px; margin-top: 7px; }
#endc .slot.locked { background: rgba(40,30,70,.92); border-color: #A795FF; }
#endc .lock { position: relative; width: 34px; height: 26px; border-radius: 6px; background: #FFC233; margin-top: 12px; }
#endc .lock::before { content: ""; position: absolute; left: 6px; top: -16px; width: 14px; height: 16px; border: 5px solid #E6E1F5; border-bottom: 0; border-radius: 12px 12px 0 0; }
#endc .e3 { position: absolute; left: 0; right: 0; top: 1018px; text-align: center; }
#endc .e3 span { display: inline-block; padding: 12px 26px; border-radius: 20px; background: rgba(14,18,32,.88); font: 800 34px/1.1 "Manrope"; color: #FFFFFF; }
#endc .e3 span b { color: #FFB08F; }
.cap { position: absolute; left: 60px; right: 60px; top: 1330px; text-align: center; }
.cap .tx { display: inline-block; padding: 12px 26px; border-radius: 22px; background: rgba(10,12,22,.82); font: 800 58px/1.2 "Manrope"; color: #FFFFFF; letter-spacing: .5px; }
"""


def main():
    loot = story()
    caps = captions()
    mix = "mix.wav" if os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav")) else "voice.wav"
    slots = [("Formbricks", "rare"), ("Listmonk", "rare"), ("Documenso", "epic"), ("Umami", "epic"), ("Whisper", "legendary"), ("n8n", "mythic")]
    grid = "".join(f'<div class="slot slot{j}" style="border-color:{RCOL[r]};box-shadow:0 0 18px {RCOL[r]}66"><b>{n}</b></div>' for j, (n, r) in enumerate(slots))
    grid += "".join(f'<div class="slot slot{6 + j} locked"><b>?</b><span class="lock"></span></div>' for j in range(3))
    stamps = "".join(f'<div class="stamp" id="free{k}"{' style="left:560px;top:1150px;transform:rotate(8deg)"' if k == 3 else ''}>FREE</div>' for k in range(len(FREE)))
    ui = ('<div id="title" class="sh"><span class="t0">PART 2</span><span class="t1">THE SECRET</span><span class="t2">FREE STORE</span>'
          '<span class="t3">every paid app is <b>free</b> in here</span></div>'
          '<div id="area" class="sh"><span class="a0">AREA UNLOCKED</span><span class="a1">THE <b>GITHUB</b> VAULT</span></div>'
          '<div id="hud"><div class="pill lt"><span class="ic chest"></span><span><span class="lab">LOOT</span><span class="val lt-n">0/9</span></span></div>'
          '<div class="pill sv"><span class="ic coin">$</span><span><span class="lab">SAVED</span><span class="val"><span class="sv-n">$0.00</span><span class="sv-u">/mo</span></span></span></div></div>'
          + loot + stamps +
          '<div id="mythic"><span>MYTHIC</span><small>THE ONE EVERYONE PAYS FOR</small></div>'
          '<div id="secret"><span class="s0">+3 SECRET CHESTS</span><span class="s1">LOCKED · CHESTS 7, 8, 9</span><br><span class="dm">they only open in <b>DMs</b></span></div>'
          '<div id="endc"><div class="e0 sh">COMMENT</div><div class="e1"><span>REPO</span></div>'
          '<div class="e2 sh">and I\'ll DM you <b>all 9</b> free repos</div>'
          f'<div class="grid">{grid}</div>'
          '<div class="e3"><span>Send this to a friend still paying for <b>Zapier</b></span></div></div>')
    ct = {"l": L[1:], "e": E[1:], "ph": [ps[1:] for ps in PS[1:]], "pe": [pe[1:] for pe in PE[1:]], "k": K, "end": DUR}
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Secret Free Store 9x16</title>
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
    <script type="module" src="assets/js/store.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(ct, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, audio {mix}, saved ${sum(SAVE):.2f}/mo")


if __name__ == "__main__":
    main()
