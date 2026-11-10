"""The STACK lead magnet: "The Zero Stack", the 8 open-source tools from the reel (plus 8 more), as a branded PDF.

python3 zero-stack-9x16/lead-magnet/build_pdf.py      (needs node + the preinstalled Playwright)

Brand: brands/nxtlvl (NXTLVLSOCIAL.AI, the comet-star mark, night + violet glows, Montserrat / Instrument Serif /
JetBrains Mono). Prices are 2026 US list prices on monthly billing; licences were read from each project's own LICENSE
file. Writes zero-stack.html and nxtlvl_zero-stack.pdf next to this file (the PDF is a deliverable, not committed).
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

# app, monthly price, replacement, licence, what it is, how to start (free), link, honest note
SWAPS = [
    ("Adobe Creative Cloud", 69.99, "GIMP · Inkscape · Kdenlive", "GPL", "Photo editing (GIMP), vector design (Inkscape) and video editing (Kdenlive): three mature desktop apps that cover Photoshop, Illustrator and Premiere.",
     "Download all three for Mac, Windows or Linux. No account, no server.", "gimp.org · inkscape.org · kdenlive.org", "No Adobe file round-trips for teams that live in .psd and .ai; fine for a solo creator."),
    ("Canva Pro", 18.00, "Penpot", "MPL-2.0", "A browser design tool for social posts, decks and brand kits, with components and real-time collaboration.",
     "Use the free cloud plan at penpot.app, or self-host it with Docker.", "penpot.app · github.com/penpot/penpot", "No Canva-style template library: build your own templates once and reuse them."),
    ("CapCut Pro", 19.99, "Shotcut", "GPL-3.0", "A full video editor: multi-track timeline, captions, colour, transitions and 4K export, with no watermark.",
     "Download for Mac, Windows or Linux.", "shotcut.org · github.com/mltframework/shotcut", "No one-tap AI effects or trend templates; editing is manual."),
    ("Mailchimp (10,000 contacts)", 108.88, "Listmonk", "AGPL-3.0", "Newsletter and mailing-list manager: lists, campaigns, templates, analytics, double opt-in.",
     "Self-host the single binary or Docker image; send through any SMTP service (Amazon SES costs about $1 per 10,000 emails).", "listmonk.app · github.com/knadh/listmonk", "You run the server and the sending service yourself."),
    ("Hootsuite", 99.00, "Postiz", "AGPL-3.0", "Schedule and publish posts to Instagram, TikTok, LinkedIn, X, YouTube and more from one calendar, with team workflows.",
     "Self-host with Docker for free (they also sell a hosted plan).", "postiz.com · github.com/gitroomhq/postiz-app", "Each network needs its own developer app keys when you self-host."),
    ("Linktree Pro", 15.00, "LinkStack", "AGPL-3.0", "Your own link-in-bio page with themes, click stats and a custom domain.",
     "Self-host on any PHP host or with Docker.", "linkstack.org · github.com/LinkStackOrg/LinkStack", "No built-in shop or tipping; link to your store instead."),
    ("Notion (Business)", 24.00, "AppFlowy", "AGPL-3.0", "Docs, wikis, kanban boards and databases, local-first, with an AI assistant you can point at your own models.",
     "Download the desktop or mobile app; sync is optional (self-host or their cloud).", "appflowy.com · github.com/AppFlowy-IO/AppFlowy", "Fewer integrations than Notion."),
    ("ChatGPT Plus", 20.00, "Ollama + an open model", "MIT", "Runs AI models on your own laptop, offline. Pair it with an open-licence model such as Mistral 7B or Qwen (Apache-2.0).",
     "Install Ollama, then run: ollama run mistral", "ollama.com · github.com/ollama/ollama", "Needs a decent laptop (16 GB of memory is comfortable); local models are smaller than the frontier ones."),
]
BONUS = [
    ("Calendly", "Cal.com", "MIT", "Booking pages and scheduling."),
    ("Zoom", "Jitsi Meet", "Apache-2.0", "Video calls in the browser, no account needed."),
    ("Slack", "Mattermost", "Open source", "Team chat with channels and threads."),
    ("Google Drive / Dropbox", "Nextcloud", "AGPL-3.0", "Files, sharing, calendar and docs on your server."),
    ("Typeform", "Formbricks", "AGPL-3.0", "Forms and surveys."),
    ("Zapier", "Activepieces", "MIT", "No-code automations between your apps."),
    ("Google Analytics", "Plausible / Umami", "AGPL-3.0 / MIT", "Privacy-friendly website analytics."),
    ("Bitly", "Dub", "AGPL-3.0", "Short links with click analytics."),
]
BILL = sum(s[1] for s in SWAPS)
e = html.escape


def page(n, body, cls=""):
    head = "" if n == 1 else (f'<div class="head"><div class="brand">{LOGO}</div><div class="pg">THE ZERO STACK · {n:02d} / {TOTAL:02d}</div></div>')
    return f'<section class="page {cls}">{head}{body}</section>'


COVER = f"""
<div class="cover-brand">{LOGO}</div>
<div class="cover-body">
  <div class="kicker">FROM THE "EVERY APP VANISHED" REEL</div>
  <h1>The Zero<br><em>Stack.</em></h1>
  <p class="cover-sub">Every paid app in Maya's business vanished overnight, a month before her launch. These are the
  eight free, open-source tools that replaced them, and eight more for whatever you pay for next.</p>
  <div class="chips"><span>8 SWAPS</span><span>${BILL:,.2f}/MO &#8594; $0 IN LICENCES</span><span>+ 8 BONUS TOOLS</span></div>
</div>
<div class="cover-mark">{MARK}</div>
<div class="cover-foot"><span>Free means free to use: no licence fee, no subscription. Some need a small server, and we tell you which.</span></div>
"""

rows = "".join(f'<tr><td class="n">{k + 1:02d}</td><td><b>{e(s[0])}</b></td><td class="pr">${s[1]:,.2f}</td><td class="new">{e(s[2])}</td><td class="lic">{e(s[3])}</td></tr>' for k, s in enumerate(SWAPS))
P2 = f"""
<div class="kicker">THE SWAP SHEET</div>
<h2>Eight bills, <em>eight</em> free tools</h2>
<p class="lede">The apps from the reel, what they cost a solo creator each month (2026 US list prices, monthly billing),
and the open-source tool that does the job.</p>
<table class="swaps"><thead><tr><th></th><th>Paid app</th><th>Per month</th><th>Replace with</th><th>Licence</th></tr></thead>
<tbody>{rows}</tbody>
<tfoot><tr><td></td><td><b>Total</b></td><td class="pr">${BILL:,.2f}</td><td class="new" colspan="2">$0 in licences · about ${BILL * 12:,.0f} a year back</td></tr></tfoot></table>
<div class="note"><h3>The honest version of "$0"</h3>
<p>Desktop apps (GIMP, Inkscape, Kdenlive, Shotcut, AppFlowy, Ollama) cost nothing at all. The web tools you self-host
(Listmonk, Postiz, LinkStack) need a small server: one $10 to $20 a month VPS runs all three. Several projects also sell
a hosted plan if you'd rather not run anything yourself.</p></div>
"""


def card(k, s):
    return (f'<div class="card"><div class="ct"><span class="cn">{k + 1:02d}</span><div><div class="old">{e(s[0])} · ${s[1]:,.2f}/mo</div>'
            f'<h3>&#8594; {e(s[2])} <span class="lic">{e(s[3])}</span></h3></div></div>'
            f'<p>{e(s[4])}</p><p class="start"><b>Start:</b> {e(s[5])}</p><p class="link">{e(s[6])}</p><p class="trade"><b>Trade-off:</b> {e(s[7])}</p></div>')


P3 = '<div class="kicker">THE TOOLS · 1 TO 4</div><h2>Design, video, <em>email</em>, social</h2><div class="cards">' + "".join(card(k, SWAPS[k]) for k in range(4)) + "</div>"
P4 = '<div class="kicker">THE TOOLS · 5 TO 8</div><h2>Links, plans and your <em>own</em> AI</h2><div class="cards">' + "".join(card(k, SWAPS[k]) for k in range(4, 8)) + "</div>"
P5 = ('<div class="kicker">BONUS</div><h2>Eight more you can <em>cancel</em></h2><p class="lede">Not in the reel, same idea: the paid app on the left, the open-source tool that replaces it.</p><div class="bonus">'
      + "".join(f'<div class="bx"><div class="old">{e(a)}</div><h3>&#8594; {e(b)}</h3><span class="lic">{e(c)}</span><p>{e(d)}</p></div>' for a, b, c, d in BONUS) + "</div>")
P6 = """
<div class="kicker">THIS WEEKEND</div>
<h2>Switch in <em>one</em> weekend</h2>
<ul class="check">
  <li><b>Saturday morning:</b> install the desktop four (GIMP, Kdenlive or Shotcut, AppFlowy, Ollama). Open one real project in each.</li>
  <li><b>Saturday afternoon:</b> rebuild your three most-used Canva templates in Penpot.</li>
  <li><b>Sunday morning:</b> rent one small VPS and install Listmonk, Postiz and LinkStack with Docker. Import your email list as a CSV.</li>
  <li><b>Sunday afternoon:</b> schedule next week's posts in Postiz, point your bio link at LinkStack, then cancel one subscription.</li>
  <li><b>Next month:</b> cancel the rest only once each replacement has done a full week of real work.</li>
</ul>
<div class="note"><h3>Read before you cancel</h3>
<p>Prices are 2026 US list prices on monthly billing and change often; check each provider's pricing page. Licences were read
from each project's LICENSE file; some projects keep extra paid "enterprise" features in a separate folder, and the free
core covers everything in this guide. The reel's story and its numbers are a what-if; the tools are real.</p></div>
<div class="outro"><div class="outro-mark">""" + MARK + """</div><div><h3>Want more setups like this?</h3>
<p>Follow @nxtlvlsocial.ai for AI and creator tools that save you real money.</p></div></div>
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
    doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>The Zero Stack</title><style>{CSS}</style></head><body>{body}</body></html>'
    src = os.path.join(HERE, "zero-stack.html")
    open(src, "w", encoding="utf-8").write(doc)
    out = os.path.join(ROOT, "zero-stack-9x16", "renders", "nxtlvl_zero-stack.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    prev = os.environ.get("PREVIEW_DIR", os.path.join(HERE, "preview"))
    os.makedirs(prev, exist_ok=True)
    subprocess.run(["node", "-e", SHOT, src, out, prev], check=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
