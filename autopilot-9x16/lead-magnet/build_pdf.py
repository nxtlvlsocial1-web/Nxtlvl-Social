"""The AUTOPILOT lead magnet: "The Autopilot Stack", the six open-source tools from the reel and six ready-made
automation recipes for a small business, as a branded PDF.

python3 autopilot-9x16/lead-magnet/build_pdf.py      (needs node + the preinstalled Playwright)

Brand: brands/nxtlvl (NXTLVLSOCIAL.AI, the comet-star mark). Licences were read from each project's LICENSE file.
Writes autopilot.html here and renders/nxtlvl_autopilot.pdf (a deliverable, not committed).
"""
import html
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
MARK = open(os.path.join(ROOT, "brands", "nxtlvl", "logo-mark.svg")).read()
MARK = MARK[MARK.index("<svg"):]
TOTAL = 6
LOGO = f'<span class="mk">{MARK}</span><span class="wmtxt">NXTLVLSOCIAL.AI</span>'
e = html.escape

TOOLS = [
    ("Activepieces", "Zapier", "MIT", "The glue: when something happens in one app, do something in another.", "Self-host with Docker (free) or use their cloud.", "activepieces.com · github.com/activepieces/activepieces"),
    ("Chatwoot", "Intercom", "MIT", "One inbox for Instagram DMs, WhatsApp, Facebook, email and your website chat, with auto-replies.", "Self-host with Docker, or their cloud plan.", "chatwoot.com · github.com/chatwoot/chatwoot"),
    ("Cal.com", "Calendly", "MIT", "Booking pages for tables, classes and calls, with reminders.", "Free cloud plan for one person, or self-host.", "cal.com · github.com/calcom/cal.com"),
    ("Mautic", "HubSpot email", "GPL", "Email journeys: welcome series, follow-ups, segments, newsletters.", "Self-host on any PHP host or with Docker.", "mautic.org · github.com/mautic/mautic"),
    ("Formbricks", "Typeform", "AGPL-3.0", "Forms and surveys: pre-orders, feedback after a visit, waitlists.", "Free cloud plan, or self-host.", "formbricks.com · github.com/formbricks/formbricks"),
    ("Flowise", "paid AI chatbot builders", "Apache-2.0", "Build an AI agent on your own menu, prices and FAQs, and plug it into your inbox.", "Self-host with Docker; point it at a local model (Ollama) or an AI API key.", "flowiseai.com · github.com/FlowiseAI/Flowise"),
]
RECIPES = [
    ("New lead, handled", "Activepieces + Twenty CRM + Mautic", ["A form or DM comes in with a name and email.", "Activepieces adds them to your CRM (Twenty is open source too).", "Mautic sends the welcome email within a minute."]),
    ("Every DM in one inbox", "Chatwoot", ["Connect Instagram, WhatsApp and your website chat.", "Turn on auto-replies for opening hours, menu and directions.", "Anything else is waiting for you in one list in the morning."]),
    ("Bookings without back-and-forth", "Cal.com + Chatwoot", ["Make one event type per thing people book (a table, a workshop).", "Save the booking link as a canned reply in Chatwoot.", "Cal.com sends the reminder the day before."]),
    ("Follow-ups that send themselves", "Mautic", ["Day 0: welcome and this week's menu.", "Day 2: the most popular item, with a photo.", "Day 7: ask for a review, with the link."]),
    ("Pre-orders and feedback", "Formbricks + Activepieces", ["A pre-order form for the weekend bakes.", "Activepieces sends each order to a sheet and pings your phone.", "A two-question survey goes out after every visit."]),
    ("An AI that answers at 3 AM", "Flowise + Chatwoot", ["Give Flowise your menu, prices, hours and FAQs.", "Connect it to Chatwoot as an agent bot.", "It answers the easy questions and hands the rest to you."]),
]


def page(n, body, cls=""):
    head = "" if n == 1 else (f'<div class="head"><div class="brand">{LOGO}</div><div class="pg">THE AUTOPILOT STACK · {n:02d} / {TOTAL:02d}</div></div>')
    return f'<section class="page {cls}">{head}{body}</section>'


COVER = f"""
<div class="cover-brand">{LOGO}</div>
<div class="cover-body">
  <div class="kicker">FROM THE "WHILE YOU SLEPT" REEL</div>
  <h1>The Autopilot<br><em>Stack.</em></h1>
  <p class="cover-sub">Six free, open-source tools that answer your messages, take bookings and follow up while you
  sleep, and six recipes to set them up for a small business like Rosa's café.</p>
  <div class="chips"><span>6 TOOLS</span><span>6 RECIPES</span><span>$0 IN LICENCES</span></div>
</div>
<div class="cover-mark">{MARK}</div>
<div class="cover-foot"><span>Free to use: no licence fee, no subscription. The web tools need a small server, and we say which.</span></div>
"""
rows = "".join(f'<tr><td class="n">{k + 1:02d}</td><td class="new">{e(t[0])}</td><td><b>{e(t[1])}</b></td><td class="lic">{e(t[2])}</td></tr>' for k, t in enumerate(TOOLS))
P2 = f"""
<div class="kicker">THE STACK</div>
<h2>Six tools, <em>one</em> night shift</h2>
<p class="lede">The neon signs from the reel: each tool, the paid app it replaces and its licence.</p>
<table class="swaps"><thead><tr><th></th><th>Open-source tool</th><th>Replaces</th><th>Licence</th></tr></thead><tbody>{rows}</tbody></table>
<div class="note"><h3>What "free" means here</h3>
<p>No licence fee and no subscription. Chatwoot, Activepieces, Mautic and Flowise run on your own server: one small VPS
($10 to $20 a month) runs them all. Cal.com and Formbricks also have free cloud plans. Some projects keep extra paid
"enterprise" features in a separate folder; the free core covers everything in this guide.</p></div>
"""


def card(k, t):
    return (f'<div class="card"><div class="ct"><span class="cn">{k + 1:02d}</span><div><div class="old">replaces {e(t[1])}</div>'
            f'<h3>{e(t[0])} <span class="lic">{e(t[2])}</span></h3></div></div><p>{e(t[3])}</p><p class="start"><b>Start:</b> {e(t[4])}</p><p class="link">{e(t[5])}</p></div>')


P3 = '<div class="kicker">THE TOOLS</div><h2>What each one <em>does</em></h2><div class="cards">' + "".join(card(k, t) for k, t in enumerate(TOOLS)) + "</div>"


def recipe(k, r):
    steps = "".join(f"<li>{e(s)}</li>" for s in r[2])
    return f'<div class="card"><div class="ct"><span class="cn">{k + 1:02d}</span><div><div class="tools">{e(r[1])}</div><h3>{e(r[0])}</h3></div></div><ol class="steps">{steps}</ol></div>'


P4 = '<div class="kicker">RECIPES · 1 TO 3</div><h2>Copy these <em>tonight</em></h2><div class="cards">' + "".join(recipe(k, RECIPES[k]) for k in range(3)) + "</div>"
P5 = '<div class="kicker">RECIPES · 4 TO 6</div><h2>And these <em>tomorrow</em></h2><div class="cards">' + "".join(recipe(k, RECIPES[k]) for k in range(3, 6)) + "</div>"
P6 = """
<div class="kicker">THIS WEEKEND</div>
<h2>Go to sleep <em>on</em> Sunday</h2>
<ul class="check">
  <li><b>Saturday morning:</b> rent one small VPS and install Chatwoot and Activepieces with Docker.</li>
  <li><b>Saturday afternoon:</b> connect Instagram and WhatsApp to Chatwoot; write five auto-replies.</li>
  <li><b>Sunday morning:</b> make your Cal.com booking page and a Formbricks pre-order form.</li>
  <li><b>Sunday afternoon:</b> set up the Mautic welcome series and the Activepieces "new lead" flow.</li>
  <li><b>Next week:</b> add the Flowise agent once the rest has run for a few days.</li>
</ul>
<div class="note"><h3>Read before you switch</h3>
<p>Licences were read from each project's LICENSE file. Flowise needs an AI model to talk to: run one on your own
computer with Ollama, or add an API key from an AI provider (that part may cost money). We left out n8n on purpose: its
licence limits commercial use, so it is not open source. The reel's café and its numbers are a what-if; the tools are real.</p></div>
<div class="outro"><div class="outro-mark">""" + MARK + """</div><div><h3>Want more setups like this?</h3>
<p>Follow @nxtlvlsocial.ai for AI and creator tools that save you real time and money.</p></div></div>
"""

CSS = """
@font-face { font-family: "Montserrat"; font-weight: 100 900; src: url("fonts/montserrat.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 400; src: url("fonts/JetBrainsMono-Regular.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 700; src: url("fonts/JetBrainsMono-Bold.ttf"); }
@font-face { font-family: "ISerif"; font-style: italic; src: url("fonts/InstrumentSerif-Italic.ttf"); }
@page { size: A4; margin: 0; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { background: #07050f; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: "Montserrat", sans-serif; color: #cfc8dd; }
.page { position: relative; width: 210mm; height: 297mm; overflow: hidden; padding: 44px 52px 40px; page-break-after: always;
  background: radial-gradient(ellipse 60% 45% at 0% 0%, rgba(101,22,199,.5), transparent 70%),
              radial-gradient(ellipse 55% 40% at 100% 100%, rgba(75,6,193,.45), transparent 70%), #07050f; }
.page:last-child { page-break-after: auto; }
svg { display: block; }
.head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 26px; }
.brand, .cover-brand { display: flex; align-items: center; gap: 10px; }
.mk { width: 26px; height: 26px; display: block; } .mk svg { width: 100%; height: 100%; }
.wmtxt { font: 700 11px "JBMono"; letter-spacing: 4px; color: #fff; }
.cover-brand .mk { width: 44px; height: 44px; } .cover-brand .wmtxt { font-size: 15px; }
.pg, .kicker { font: 700 10px "JBMono"; letter-spacing: 3px; color: #b687f9; }
.pg { color: rgba(207,200,221,.55); }
b { color: #fff; font-weight: 700; }
.kicker { margin-bottom: 10px; }
h1 { font: 800 72px/1.0 "Montserrat"; letter-spacing: -2.5px; color: #fff; }
h1 em, h2 em { font-family: "ISerif"; font-style: italic; font-weight: 400; color: #b687f9; letter-spacing: 0; }
h1 em { font-size: 88px; }
h2 { font: 800 28px/1.1 "Montserrat"; letter-spacing: -.8px; color: #fff; }
h2 em { font-size: 33px; }
h3 { font: 700 14px/1.3 "Montserrat"; color: #fff; }
p { font-size: 12px; line-height: 1.6; }
.lede { margin: 10px 0 18px; font-size: 12.5px; color: #ddd5ea; }
.cover-body { position: absolute; left: 52px; right: 52px; top: 240px; z-index: 2; }
.cover-sub { margin-top: 26px; max-width: 470px; font-size: 16px; line-height: 1.55; color: #ddd5ea; }
.chips { margin-top: 30px; display: flex; gap: 10px; flex-wrap: wrap; max-width: 520px; }
.chips span { font: 700 10.5px "JBMono"; letter-spacing: 1.5px; color: #fff; padding: 8px 14px; border-radius: 30px; border: 1px solid rgba(182,135,249,.5); background: rgba(101,22,199,.25); }
.cover-mark { position: absolute; right: 30px; bottom: 120px; width: 330px; height: 330px; z-index: 1; filter: drop-shadow(0 0 40px rgba(122,47,251,.7)); }
.cover-mark svg { width: 100%; height: 100%; }
.cover-foot { position: absolute; left: 52px; right: 52px; bottom: 44px; z-index: 2; padding-top: 16px; border-top: 1px solid rgba(182,135,249,.25); }
.cover-foot span { font: 400 italic 19px "ISerif"; color: #cfc8dd; }
table.swaps { width: 100%; border-collapse: separate; border-spacing: 0 6px; }
.swaps th { text-align: left; font: 700 9.5px "JBMono"; letter-spacing: 2px; color: #b687f9; padding: 0 10px 4px; }
.swaps td { padding: 11px 10px; font-size: 12px; background: rgba(20,10,46,.78); }
.swaps td:first-child { border-radius: 10px 0 0 10px; } .swaps td:last-child { border-radius: 0 10px 10px 0; }
.swaps .n { font: 400 italic 20px "ISerif"; color: #a75bfc; width: 34px; }
.swaps .pr { color: #ff9a8f; font-weight: 700; white-space: nowrap; }
.swaps .new { color: #7ef0a8; font-weight: 700; }
.swaps .lic { font: 700 9.5px "JBMono"; color: #cfc8dd; }
.swaps tfoot td { background: rgba(101,22,199,.35); font-size: 12.5px; }
.note { margin-top: 18px; padding: 16px 20px; border-radius: 14px; background: rgba(20,10,46,.75); border: 1px solid rgba(167,91,252,.28); }
.note h3 { margin-bottom: 6px; }
.cards { margin-top: 16px; display: grid; gap: 12px; }
.card { padding: 15px 18px; border-radius: 14px; background: rgba(20,10,46,.78); border: 1px solid rgba(167,91,252,.22); }
.ct { display: flex; gap: 14px; align-items: center; margin-bottom: 6px; }
.cn { font: 400 italic 38px/0.9 "ISerif"; color: #a75bfc; }
.old { font: 700 10px "JBMono"; letter-spacing: 1px; color: #ff9a8f; text-decoration: line-through; }
.card h3, .bx h3 { font-size: 15.5px; color: #7ef0a8; }
.lic { display: inline-block; margin-left: 6px; font: 700 9px "JBMono"; letter-spacing: 1px; color: #cfc8dd; padding: 2px 7px; border-radius: 10px; border: 1px solid rgba(182,135,249,.4); vertical-align: middle; }
.card p { font-size: 11.3px; line-height: 1.5; margin-top: 4px; }
.card .link { font: 400 10.5px "JBMono"; color: #b687f9; }
.card .trade { color: #b9b1c9; }
.bonus { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.bx { padding: 15px 16px; border-radius: 14px; background: rgba(20,10,46,.78); border: 1px solid rgba(167,91,252,.22); }
.bx .lic { margin: 6px 0 0; }
.bx p { margin-top: 6px; font-size: 11.3px; }
.check { list-style: none; margin: 18px 0 6px; }
.check li { position: relative; padding: 0 0 12px 28px; font-size: 12.5px; line-height: 1.5; }
.check li::before { content: ""; position: absolute; left: 0; top: 2px; width: 15px; height: 15px; border-radius: 4px; border: 1.5px solid #a75bfc; }
.outro { position: absolute; left: 52px; right: 52px; bottom: 40px; display: flex; gap: 18px; align-items: center; padding: 18px 22px;
  border-radius: 16px; background: linear-gradient(120deg, rgba(101,22,199,.45), rgba(20,10,46,.85)); border: 1px solid rgba(182,135,249,.35); }
.outro-mark { width: 64px; height: 64px; flex: none; } .outro-mark svg { width: 100%; height: 100%; }
.outro h3 { font-size: 17px; margin-bottom: 4px; }
.outro p { font-size: 11.5px; color: #e2daf0; }

.card .tools { font: 700 10px "JBMono"; letter-spacing: 1px; color: #b687f9; }
.steps { margin: 6px 0 0 18px; } .steps li { font-size: 12px; line-height: 1.55; padding: 2px 0; }
.swaps td.lic, .swaps .lic { font: 700 10px "JBMono"; }
"""

SHOT = """
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + process.argv[1], { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: process.argv[2], preferCSSPageSize: true, printBackground: true });
  await p.setViewportSize({ width: 794, height: 1123 });
  const pages = await p.$$('.page');
  for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: process.argv[3] + '/page-' + (i + 1) + '.png' });
  await b.close();
})().catch((e) => { console.error(e); process.exit(1); });
"""

def main():
    body = "".join([page(1, COVER, "cover"), page(2, P2), page(3, P3), page(4, P4), page(5, P5), page(6, P6)])
    doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>The Autopilot Stack</title><style>{CSS}</style></head><body>{body}</body></html>'
    src = os.path.join(HERE, "autopilot.html")
    open(src, "w", encoding="utf-8").write(doc)
    out = os.path.join(ROOT, "autopilot-9x16", "renders", "nxtlvl_autopilot.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    prev = os.environ.get("PREVIEW_DIR", os.path.join(HERE, "preview"))
    os.makedirs(prev, exist_ok=True)
    subprocess.run(["node", "-e", SHOT, src, out, prev], check=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
