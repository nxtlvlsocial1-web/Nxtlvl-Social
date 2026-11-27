"""SST v4 (9:16, ~50 s): writes index.html, plan/sfx_events.json and plan/edit.json.

Owner on v3: "highlight the issues faced ... only about the problems ... no need to mention the vision ... go through
the article and mention the problems faced honestly" (areporterlive.com, "Hacking tracking and stalking just to stop the
progress of sports science technology", updated 2026-09-17). Every on-screen fact is the article's: both iPhones hacked,
the hard disk hacked twice with data and source code stolen, Instagram / Facebook / Gmail / WhatsApp / Proton Mail /
domain / internet provider / bank accounts hacked and used to track and message, Google OTPs 5 times from numbers
registered to other people, 4 fake profiles made with AI, people watching the neighbourhood, 7 attempts to start a fight,
the vehicle punctured or damaged 15-20 times, accidents caused deliberately, the police informed, no action
yet. Attributed throughout ("as described in a published account"); the people the article accuses are not shown (no
proven finding). Kept from v3: the navy grade, the footage band, Montserrat / Inter type, the restrained glitch, subtitles,
the exact SST logo on its white card.
python3 build/plan_v4.py && python3 build/prep_shots.py && python3 build/generate.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = json.load(open(os.path.join(ROOT, "plan", "words.json")))
EDL = json.load(open(os.path.join(ROOT, "plan", "edl.json")))
SCRIPT = json.load(open(os.path.join(ROOT, "plan", "sentences.json")))
LW = {}
for w in W:
    LW.setdefault(w["line"], []).append(w)
JS, SFX, HTML = [], [], []
NAVY, INK, BLUE, BLUE2, RED = "#0b1526", "#05080f", "#2f6bdc", "#6f9bff", "#e5484d"
BY, BH = 380, 1160


def js(s):
    JS.append(s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(max(0, t), 3)})


def ft(sel, t, d, frm, to_, ease="power2.out"):
    js(f'tl.fromTo("{sel}", {frm}, {{...{to_}, duration: {d}, ease: "{ease}", immediateRender: false}}, {max(0, t):.3f});')


def to(sel, t, d, props, ease="power2.out"):
    js(f'tl.to("{sel}", {{...{props}, duration: {d}, ease: "{ease}"}}, {max(0, t):.3f});')


def st(sel, t, props):
    js(f'tl.set("{sel}", {props}, {max(0, t):.3f});')


start = {k: v[0]["t0"] for k, v in LW.items()}
endl = {k: v[-1]["t1"] for k, v in LW.items()}
LAST = sorted(LW)[-1]


def wt(lid, word, n=0):
    hits = [w for w in LW[lid] if w["w"].lower().strip(",.'").startswith(word)]
    return hits[min(n, len(hits) - 1)]["t0"]


DUR = round(endl[LAST] + 2.2, 2)   # v6: 2.2 s end card keeps the reel under 60 s

# ---- footage: one video per shot, alternating tracks so dissolves can overlap
clips = []
for k, s in enumerate(EDL["shots"]):
    t, d = s["t"], s["d"]
    nxt_cut = k + 1 < len(EDL["shots"]) and EDL["shots"][k + 1].get("cut")
    vis = d + (.08 if nxt_cut else EDL["handle"] if k < len(EDL["shots"]) - 1 else .0)
    clips.append(f'<div class="shot" id="w{s["id"]}"><video id="{s["id"]}" class="clip" src="assets/video/{s["id"]}.mp4" muted playsinline '
                 f'data-start="{t:.3f}" data-duration="{vis:.3f}" data-track-index="{1 + k % 2}"></video></div>')
    fade = .01 if k == 0 else (.05 if s.get("cut") else .5)
    ft(f"#w{s['id']}", t, fade, "{opacity: 0}", "{opacity: 1}", "sine.inOut")
    ft(f"#w{s['id']}", t, vis, "{scale: 1.0}", "{scale: 1.06}", "none")
    to(f"#w{s['id']}", t + vis - .02, .01, "{opacity: 0}")
to("#band", start[LAST] - .5, .9, "{opacity: 0}", "sine.inOut")


# ---- headlines (top): white, royal-blue second line, a small note under
def head(k, a, b, note, t0, t1, tb=None):
    inner = f'<div class="h1">{a}</div>' + (f'<div class="h2" id="hd{k}b">{b}</div>' if b else "") + (f'<div class="note" id="hd{k}n">{note}</div>' if note else "")
    HTML.append(f'<div class="head" id="hd{k}">{inner}</div>')
    if k:
        ft(f"#hd{k}", t0, .45, "{opacity: 0, y: 14}", "{opacity: 1, y: 0}", "power2.out")
    if b:
        ft(f"#hd{k}b", tb if tb else t0 + .5, .45, "{opacity: 0, y: 10}", "{opacity: 1, y: 0}", "power2.out")
    if note:
        ft(f"#hd{k}n", t0 + .3, .5, "{opacity: 0}", "{opacity: 1}", "power1.out")
    to(f"#hd{k}", t1 - .3, .3, "{opacity: 0}", "power1.in")


HEADS = [("TWO IPHONES. HACKED.", "HARD DISK HACKED TWICE.", "", 0.0, start["j02"], start["j01"]),
         ("FOR MONTHS.", "AND YEARS.", "", start["j02"], start["j03"], wt("j02", "and")),
         ("WHAT THE FOUNDER HAS FACED", "", "AS DESCRIBED IN A PUBLISHED ACCOUNT", start["j03"], start["j04"], None),
         ("ACCOUNTS BROKEN INTO.", "USED TO TRACK AND MESSAGE.", "", start["j04"], start["j10"], wt("j09", "used")),
         ("LOGIN CODES. 5 TIMES.", "", "FROM NUMBERS IN OTHER PEOPLE'S NAMES", start["j10"], start["j11"], None),
         ("4 FAKE PROFILES.", "", "MADE WITH AI, IN THE FOUNDER'S NAME", start["j11"], start["j12"], None),
         ("THEN IT MOVED OFFLINE.", "", "", start["j12"], start["j13"], None),
         ("WATCHED.", "", "PEOPLE AROUND THE NEIGHBOURHOOD", start["j13"], start["j14"], None),
         ("7 ATTEMPTS", "TO START A FIGHT.", "", start["j14"], start["j15"], wt("j14", "strangers")),
         ("15-20 TIMES", "THE VEHICLE DAMAGED.", "", start["j15"], start["j16"], wt("j15", "the")),
         ("ACCIDENTS.", "CAUSED DELIBERATELY.", "", start["j16"], start["j17"], wt("j16", "were")),
         ("THE POLICE WERE TOLD.", "NO ACTION YET.", "", start["j17"], start["j19"], start["j18"]),
         ("THE ASK IS SIMPLE.", "LET IT REACH PEOPLE.", "", start["j19"], start[LAST] - .3, start["j20"])]
for k, (a, b, note, t0, t1, tb) in enumerate(HEADS):
    head(k, a, b, note, t0, t1, tb)

# ---- the attribution, always on screen once the account is named
ft("#attr", start["j03"] + .4, .6, "{opacity: 0}", "{opacity: 1}", "power1.out")
to("#attr", start[LAST] - .6, .4, "{opacity: 0}")

# ---- graphics over the band (each on a dimmed band)
def dim(t0, t1, op=.62):
    js(f'tl.to("#dim", {{opacity: {op}, duration: .4, ease: "power1.out"}}, {t0:.3f});')
    js(f'tl.to("#dim", {{opacity: 0, duration: .4, ease: "power1.in"}}, {t1 - .4:.3f});')


# accounts: rows appear on their words, each stamped BREACHED; the rest of the list on "all broken into"
ACC = [("INSTAGRAM", wt("j04", "instagram")), ("FACEBOOK", wt("j05", "facebook")), ("GMAIL", wt("j06", "gmail")),
       ("WHATSAPP", wt("j07", "whatsapp")), ("BANK ACCOUNT", wt("j08", "bank")),
       ("PROTON MAIL", wt("j09", "all") + .05), ("DOMAIN ACCOUNT", wt("j09", "all") + .2), ("INTERNET PROVIDER", wt("j09", "all") + .35)]
rows = "".join(f'<div class="row" id="ac{k}"><span>{n}</span><b>BREACHED</b></div>' for k, (n, _) in enumerate(ACC))
HTML.append(f'<div class="panel" id="acc">{rows}</div>')
dim(start["j04"] - .1, start["j10"])
ft("#acc", start["j04"] - .1, .4, "{opacity: 0}", "{opacity: 1}")
for k, (n, at) in enumerate(ACC):
    ft(f"#ac{k}", at - .05, .35, "{opacity: 0, x: -40}", "{opacity: 1, x: 0}", "power3.out")
    ft(f"#ac{k} b", at + .15, .25, "{opacity: 0, scale: 1.6}", "{opacity: 1, scale: 1}", "back.out(2)")
    sfx("tick" if k < 5 else "click", at + .15)
to("#acc", start["j10"] - .35, .3, "{opacity: 0}")
# tracking rings on "used to track"
ft("#track", wt("j09", "track") - .1, .2, "{opacity: 0}", "{opacity: 1}", "none")
js(f'tl.fromTo("#track circle", {{attr: {{r: 10}}, opacity: .9}}, {{attr: {{r: 300}}, opacity: 0, duration: 1.1, stagger: .22, ease: "power1.out", immediateRender: false}}, {wt("j09", "track") - .1:.3f});')
to("#track", start["j10"] - .3, .2, "{opacity: 0}")

# login codes: five notifications stack, the counter climbs to 5
otp = "".join(f'<div class="ntf" id="ot{k}"><i>G</i><div><b>Google</b><span>Your verification code is &#8226;&#8226;&#8226;&#8226;&#8226;&#8226;</span></div><em>+91 &#8226;&#8226;&#8226;&#8226;&#8226; &#8226;&#8226;&#8226;&#8226;&#8226;</em></div>' for k in range(5))
HTML.append(f'<div class="panel" id="otp">{otp}<div class="cnt">{"".join(f'<span id="oc{k}">{k + 1}x</span>' for k in range(5))}</div></div>')
dim(start["j10"] - .1, start["j11"])
ft("#otp", start["j10"] - .1, .3, "{opacity: 0}", "{opacity: 1}")
t_o = wt("j10", "codes")
for k in range(5):
    ft(f"#ot{k}", t_o + k * .32, .35, "{opacity: 0, y: -30}", "{opacity: 1, y: 0}", "power3.out")
    st(f"#oc{k}", t_o + k * .32, "{opacity: 1}")
    if k:
        st(f"#oc{k - 1}", t_o + k * .32, "{opacity: 0}")
    sfx("notify_soft", t_o + k * .32)
to("#otp", start["j11"] - .3, .3, "{opacity: 0}")

# fake profiles: four identical cards, each stamped FAKE
prof = "".join(f'<div class="pf" id="pf{k}"><div class="av"></div><b>@founder.official</b><span>ID 4471 0923</span><em>FAKE</em></div>' for k in range(4))
HTML.append(f'<div class="panel" id="prof"><div class="pgrid">{prof}</div><div class="pnote">SAME USERNAME. SAME USER ID.</div></div>')
dim(start["j11"] - .1, start["j12"], .7)
ft("#prof", start["j11"] - .1, .3, "{opacity: 0}", "{opacity: 1}")
t_p = wt("j11", "four")
for k in range(4):
    ft(f"#pf{k}", t_p + k * .2, .4, "{opacity: 0, scale: .85}", "{opacity: 1, scale: 1}", "back.out(1.6)")
    ft(f"#pf{k} em", t_p + 1.1 + k * .12, .25, "{opacity: 0, scale: 1.8}", "{opacity: 1, scale: 1}", "back.out(2)")
    sfx("thump", t_p + 1.1 + k * .12)
ft("#prof .pnote", t_p + 1.6, .4, "{opacity: 0}", "{opacity: 1}")
to("#prof", start["j12"] - .3, .25, "{opacity: 0}")

# counters: 7, then 15-20
for cid, lid, word in (("c7", "j14", "seven"), ("c15", "j15", "fifteen")):
    ft(f"#{cid}", wt(lid, word) - .05, .45, "{opacity: 0, scale: .7}", "{opacity: 1, scale: 1}", "back.out(1.8)")
    sfx("thump", wt(lid, word))
    nxt = start["j15"] if lid == "j14" else start["j16"]
    to(f"#{cid}", nxt - .3, .25, "{opacity: 0}")
HTML.append('<div class="big" id="c7"><b>7</b><span>TIMES</span></div><div class="big" id="c15"><b class="mid">15-20</b><span>TIMES</span></div>')

# v6 (owner: "remove letters written to prime minister, add intentional accidents"): accidents get their own beat on the
# wrecked-car shot (an impact on the word); the police beat keeps only the NO ACTION YET stamp, no letters
sfx("impact", wt("j16", "accidents") - .05)
HTML.append('<div class="panel" id="lets"><div class="stamp" id="noact">NO ACTION YET</div></div>')
dim(start["j17"] - .1, start["j19"], .5)
ft("#lets", start["j17"] - .1, .3, "{opacity: 0}", "{opacity: 1}")
ft("#noact", start["j18"] - .05, .35, "{opacity: 0, scale: 1.8, rotation: -8}", "{opacity: 1, scale: 1, rotation: -8}", "back.out(1.6)")
sfx("stamp_soft", start["j18"])
to("#lets", start["j19"] - .35, .3, "{opacity: 0}")

# ---- subtitles: the script's words, max two lines
subs = []
for lid in sorted(LW):
    if lid == LAST:
        continue
    ws = LW[lid]
    words = SCRIPT[lid].split()
    if len(words) != len(ws):
        words = [w["w"] for w in ws]
    if len(words) > 10:
        h = len(words) // 2
        parts = [(words[:h], ws[:h]), (words[h:], ws[h:])]
    else:
        parts = [(words, ws)]
    for txt, tw in parts:
        subs.append((" ".join(txt), tw[0]["t0"], tw[-1]["t1"]))
for k, (txt, t0, t1) in enumerate(subs):
    nxt = subs[k + 1][1] if k + 1 < len(subs) else DUR
    off = min(t1 + .4, nxt - .22)
    HTML.append(f'<div class="sub" id="sb{k}">{txt}</div>')
    ft(f"#sb{k}", t0 - .08, .2, "{opacity: 0}", "{opacity: 1}", "power1.out")
    to(f"#sb{k}", off, .16, "{opacity: 0}", "power1.in")

# ---- the online part: a restrained glitch on each hit; it stops when it "moves offline"
gl0, gl1 = 0.0, start["j12"] - .2
ft("#scan", .1, .8, "{opacity: 0}", "{opacity: 1}", "sine.inOut")
to("#scan", gl1, .4, "{opacity: 0}")
ft("#cool", 0, 1.0, "{opacity: 0}", "{opacity: 1}")
HITS = [wt("j00", "hacked"), wt("j01", "hacked"), wt("j01", "stolen"), wt("j09", "broken"), wt("j10", "google"), wt("j11", "fake")]
for k, at in enumerate(HITS):
    js(f'tl.set("#band", {{filter: "drop-shadow(5px 0 0 rgba(255,40,70,.55)) drop-shadow(-5px 0 0 rgba(60,170,255,.55))", x: {6 if k % 2 else -6}}}, {at:.3f});')
    js(f'tl.set("#slice", {{opacity: .9, y: {[160, 520, 860, 300, 700, 980][k % 6]}}}, {at:.3f});')
    js(f'tl.set("#band", {{filter: "none", x: 0}}, {at + .09:.3f});')
    js(f'tl.set("#slice", {{opacity: 0}}, {at + .09:.3f});')
    sfx("glitch", at)
# the offline turn: a beat of black
st("#blk", start["j12"] - .2, "{opacity: 1}")
to("#blk", start["j12"] + .15, .5, "{opacity: 0}", "power1.out")
sfx("thump", start["j12"] - .15)
ft("#warm", start["j19"], 3.0, "{opacity: 0}", "{opacity: 1}", "sine.inOut")
to("#warm", start[LAST] - .5, .9, "{opacity: 0}")

# ---- end card: the exact SST logo, the ask, the article's disclaimer
te = start[LAST]
ft("#endbg", te - .5, .9, "{opacity: 0}", "{opacity: 1}", "sine.inOut")
ft("#sweep", te - .3, 1.6, "{x: -1400, opacity: 0}", "{x: 1400, opacity: 1}", "power2.inOut")
ft("#logo", te - .05, .9, "{opacity: 0, scale: .96}", "{opacity: 1, scale: 1}", "power2.out")
ft("#tag1", te + .7, .8, "{opacity: 0, y: 12}", "{opacity: 1, y: 0}", "power2.out")
ft("#tagrule", te + .9, .9, "{scaleX: 0}", "{scaleX: 1}", "power2.inOut")
ft("#disc", te + 1.0, .8, "{opacity: 0}", "{opacity: 1}", "power1.out")

# ---- sound
sfx("whoosh_soft", start["j03"] - .3)
sfx("whoosh_soft", start["j13"] - .3)
sfx("whoosh_soft", start["j19"] - .4)
sfx("riser_low", max(te - 1.1, endl["j20"] + .4))   # never under "interference"
sfx("impact", te - .02)

CSS = f"""
@font-face {{ font-family: Mont; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }}
@font-face {{ font-family: Inter; font-weight: 500; src: url("assets/fonts/inter-latin-500-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {INK}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: linear-gradient(180deg, {NAVY} 0%, #08101d 45%, {INK} 100%); font-family: Mont; color: #fff; }}
#band {{ position: absolute; left: 0; top: {BY}px; width: 1080px; height: {BH}px; overflow: hidden;
  -webkit-mask-image: linear-gradient(180deg, transparent 0, #000 110px, #000 calc(100% - 140px), transparent 100%);
  mask-image: linear-gradient(180deg, transparent 0, #000 110px, #000 calc(100% - 140px), transparent 100%); }}
.shot {{ position: absolute; inset: 0; opacity: 0; transform-origin: 50% 45%; }}
.clip {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
#dim {{ position: absolute; inset: 0; background: {INK}; opacity: 0; }}
#cool {{ position: absolute; inset: 0; opacity: 0; background: radial-gradient(90% 70% at 50% 50%, rgba(10,25,60,0) 30%, rgba(4,10,28,.55) 100%); mix-blend-mode: multiply; }}
#warm {{ position: absolute; inset: 0; opacity: 0; background: radial-gradient(80% 60% at 70% 20%, rgba(255,196,140,.18), rgba(255,196,140,0) 70%); mix-blend-mode: soft-light; }}
#scan {{ position: absolute; inset: 0; opacity: 0; background: repeating-linear-gradient(0deg, rgba(120,160,255,.05) 0 2px, rgba(0,0,0,0) 2px 5px); mix-blend-mode: screen; }}
#slice {{ position: absolute; left: 0; right: 0; height: 26px; opacity: 0; background: linear-gradient(90deg, rgba(60,150,255,0), rgba(120,190,255,.35), rgba(255,60,90,.25), rgba(60,150,255,0)); mix-blend-mode: screen; }}
#track {{ position: absolute; inset: 0; opacity: 0; }}
#track circle {{ fill: none; stroke: rgba(130,180,255,.8); stroke-width: 3; }}
#blk {{ position: absolute; inset: 0; background: #000; opacity: 0; }}
#vig {{ position: absolute; inset: 0; pointer-events: none; background: radial-gradient(110% 70% at 50% 52%, rgba(0,0,0,0) 55%, rgba(0,0,0,.55) 100%); }}
.head {{ position: absolute; left: 40px; right: 40px; top: 222px; text-align: center; opacity: 0; }}
#hd0 {{ opacity: 1; }}
.h1 {{ font-weight: 800; font-size: 46px; letter-spacing: .05em; white-space: nowrap; line-height: 1.15; }}
.h2 {{ font-weight: 800; font-size: 46px; letter-spacing: .05em; white-space: nowrap; line-height: 1.15; color: {BLUE2}; opacity: 0; }}
.note {{ margin-top: 12px; font-family: Inter; font-weight: 600; font-size: 24px; letter-spacing: .12em; color: rgba(255,255,255,.78); opacity: 0; }}
.panel {{ position: absolute; left: 0; right: 0; top: {BY}px; height: {BH}px; opacity: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
.row {{ width: 720px; height: 92px; margin: 7px 0; padding: 0 28px; border-radius: 18px; display: flex; align-items: center; justify-content: space-between; opacity: 0;
  background: rgba(15,28,52,.85); border: 2px solid rgba(111,155,255,.25); font-family: Inter; font-weight: 700; font-size: 34px; letter-spacing: .06em; }}
.row b {{ font-size: 22px; letter-spacing: .14em; padding: 8px 14px; border-radius: 10px; color: #fff; background: {RED}; opacity: 0; }}
.ntf {{ width: 800px; margin: 8px 0; padding: 20px 24px; border-radius: 26px; display: flex; align-items: center; gap: 18px; opacity: 0;
  background: rgba(235,240,250,.94); color: #0b1526; font-family: Inter; }}
.ntf i {{ width: 56px; height: 56px; border-radius: 14px; background: #fff; border: 2px solid #d7deea; display: grid; place-items: center; font-style: normal; font-weight: 800; font-size: 30px; color: {BLUE}; flex: none; }}
.ntf b {{ display: block; font-weight: 700; font-size: 26px; }} .ntf span {{ font-weight: 500; font-size: 24px; color: #334; }}
.ntf em {{ margin-left: auto; font-style: normal; font-weight: 600; font-size: 20px; color: #667; white-space: nowrap; }}
.cnt {{ position: relative; width: 300px; height: 110px; margin-top: 18px; font-weight: 800; font-size: 96px; color: {RED}; text-align: center; }}
.cnt span {{ position: absolute; left: 0; right: 0; top: 0; opacity: 0; }}
.pgrid {{ display: grid; grid-template-columns: 400px 400px; gap: 22px; }}
.pf {{ position: relative; height: 230px; border-radius: 24px; padding: 26px; opacity: 0; background: rgba(15,28,52,.9); border: 2px solid rgba(111,155,255,.25);
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; font-family: Inter; }}
.pf .av {{ width: 80px; height: 80px; border-radius: 50%; background: radial-gradient(circle at 50% 38%, #8aa0c8 0 22%, transparent 23%), radial-gradient(ellipse at 50% 100%, #8aa0c8 0 45%, transparent 46%), #1d2c4a; }}
.pf b {{ font-weight: 700; font-size: 26px; }} .pf span {{ font-weight: 500; font-size: 20px; color: rgba(255,255,255,.65); }}
.pf em {{ position: absolute; right: 16px; top: 16px; font-style: normal; font-weight: 800; font-size: 22px; letter-spacing: .14em; padding: 6px 12px; border-radius: 8px; background: {RED}; opacity: 0; }}
.pnote {{ margin-top: 26px; font-family: Inter; font-weight: 700; font-size: 28px; letter-spacing: .12em; color: rgba(255,255,255,.85); opacity: 0; }}
.big {{ position: absolute; left: 0; right: 0; top: 760px; text-align: center; opacity: 0; }}
.big b {{ display: block; font-weight: 800; font-size: 220px; line-height: 1; color: #fff; text-shadow: 0 8px 40px rgba(0,0,0,.8); }}
.big b.mid {{ font-size: 170px; }}
.big span {{ display: block; margin-top: 18px; font-family: Inter; font-weight: 700; font-size: 34px; letter-spacing: .3em; color: {BLUE2}; }}
.chip {{ font-family: Inter; font-weight: 700; font-size: 28px; letter-spacing: .14em; padding: 12px 24px; border-radius: 999px; border: 2px solid {BLUE2}; color: #dbe6ff; opacity: 0; margin-bottom: 30px; }}
.lt {{ position: relative; width: 640px; height: 150px; margin: -20px 0 0; padding: 24px 30px; border-radius: 12px; background: #eef2f8; color: #0b1526; opacity: 0;
  box-shadow: 0 20px 50px rgba(0,0,0,.5); font-family: Inter; }}
.lt b {{ display: block; font-weight: 800; font-size: 26px; letter-spacing: .1em; }} .lt span {{ display: block; font-weight: 600; font-size: 22px; color: #445; margin-bottom: 10px; }}
.lt i {{ display: block; height: 8px; border-radius: 4px; background: #cbd3e1; margin-top: 8px; width: 90%; }} .lt i.s {{ width: 55%; }}
.stamp {{ margin-top: 34px; font-weight: 800; font-size: 54px; letter-spacing: .08em; padding: 10px 26px; border: 6px solid {RED}; border-radius: 12px; color: {RED}; background: rgba(5,8,15,.6); opacity: 0; }}
#attr {{ position: absolute; left: 0; right: 0; top: 1556px; text-align: center; font-family: Inter; font-weight: 600; font-size: 22px; letter-spacing: .12em; color: rgba(255,255,255,.62); opacity: 0; }}
.sub {{ position: absolute; left: 90px; right: 90px; top: 1418px; text-align: center; font-family: Inter; font-weight: 600; font-size: 40px; line-height: 1.28;
  color: #fff; opacity: 0; text-shadow: 0 2px 4px rgba(0,0,0,.9), 0 0 24px rgba(0,0,0,.8); }}
#endbg {{ position: absolute; inset: 0; opacity: 0; background: radial-gradient(70% 45% at 50% 46%, #13254a 0%, {NAVY} 55%, {INK} 100%); }}
#sweep {{ position: absolute; top: 0; bottom: 0; left: 0; width: 900px; opacity: 0; transform: skewX(-18deg);
  background: linear-gradient(90deg, rgba(47,107,220,0), rgba(80,140,255,.28), rgba(47,107,220,0)); filter: blur(20px); }}
#logo {{ position: absolute; left: 190px; width: 700px; top: 660px; padding: 34px 40px; border-radius: 28px; background: #fff; opacity: 0;
  box-shadow: 0 40px 100px rgba(0,0,0,.55); }}
#logo img {{ display: block; width: 100%; }}
#tag {{ position: absolute; left: 60px; right: 60px; top: 1110px; text-align: center; }}
#tag1 {{ font-weight: 800; font-size: 42px; letter-spacing: .08em; color: #fff; opacity: 0; }}
#tagrule {{ width: 220px; height: 4px; margin: 26px auto 0; background: {BLUE}; transform: scaleX(0); }}
#disc {{ position: absolute; left: 110px; right: 110px; top: 1300px; text-align: center; font-family: Inter; font-weight: 500; font-size: 24px; line-height: 1.45; color: rgba(255,255,255,.62); opacity: 0; }}
"""
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>SST The Journey Continues v4 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div id="band" data-layout-allow-overlap>
        {chr(10).join("        " + c for c in clips).strip()}
        <div id="cool"></div>
        <div id="warm"></div>
        <div id="dim"></div>
        <svg id="track" viewBox="0 0 1080 1160"><circle cx="540" cy="580" r="10"/><circle cx="540" cy="580" r="10"/><circle cx="540" cy="580" r="10"/></svg>
        <div id="scan"></div>
        <div id="slice"></div>
        <div id="blk"></div>
      </div>
      <div id="endbg"><div id="sweep"></div></div>
      <div id="logo"><img src="assets/img/sst_logo.jpg" alt="SST"></div>
      <div id="tag"><div id="tag1">WITHOUT INTERFERENCE.</div><div id="tagrule"></div></div>
      <div id="disc">Allegations as described in a published account (A Reporter Live).<br>The founder is not against any nation or profession.</div>
      {chr(10).join(HTML)}
      <div id="attr">AS DESCRIBED IN A PUBLISHED ACCOUNT</div>
      <div id="vig"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      {chr(10).join("      " + j for j in JS).strip()}
      tl.set({{}}, {{}}, {DUR:.2f});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(html)
SFX.sort(key=lambda e: e["t"])
json.dump(SFX, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
json.dump({"dur": DUR, "scenes": {}}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx, {len(subs)} subtitles")
