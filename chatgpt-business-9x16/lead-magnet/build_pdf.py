"""The CHATGPT lead magnet: "Get Your Business into ChatGPT", a setup checklist for claiming a free business profile in
Businesses in ChatGPT (OpenAI, beta, launched 10 November 2026), as a branded PDF.

python3 chatgpt-business-9x16/lead-magnet/build_pdf.py      (needs node + the preinstalled Playwright)

Facts from VentureBeat and The Next Web (both 10 Nov 2026); the claim steps follow VentureBeat's walkthrough.
Writes chatgpt.html here and renders/nxtlvl_chatgpt-business.pdf (a deliverable, not committed).
"""
import html
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
MARK = open(os.path.join(ROOT, "brands", "nxtlvl", "logo-mark.svg")).read()
MARK = MARK[MARK.index("<svg"):]
TOTAL = 4
LOGO = f'<span class="mk">{MARK}</span><span class="wmtxt">NXTLVLSOCIAL.AI</span>'
e = html.escape

STEPS = [
    ("Open Business Hub", "chatgpt.com/business-hub", ["Log into ChatGPT with the account you use for work.", "Go to chatgpt.com/business-hub.", "No ChatGPT Enterprise plan or ads account is needed."]),
    ("Find your business", "search and claim", ["Type your business name in the search bar and pick it from the list.", "Not listed? Type it in yourself.", "Click Get Started, then log in with the account that should be the admin."]),
    ("Prove it's yours", "verification", ["OpenAI verifies with one of: a business phone number, a business email, your website domain or your Shopify account.", "Which one you're offered depends on your business.", "Use contact details that match your public listing and website."]),
    ("Pass the ID check", "the blue check", ["After the claim is approved, the person managing the profile completes an identity check with Persona.", "You need it before you can publish changes, add products, see analytics or create an agent.", "Approved profiles get the blue check."]),
]


def page(n, body, cls=""):
    head = "" if n == 1 else (f'<div class="head"><div class="brand">{LOGO}</div><div class="pg">GET YOUR BUSINESS INTO CHATGPT · {n:02d} / {TOTAL:02d}</div></div>')
    return f'<section class="page {cls}">{head}{body}</section>'


COVER = f"""
<div class="cover-brand">{LOGO}</div>
<div class="cover-body">
  <div class="kicker">NEW · BUSINESSES IN CHATGPT · BETA</div>
  <h1>Get your business<br><em>into ChatGPT.</em></h1>
  <p class="cover-sub">Since 10 November 2026, a business can claim a free, verified profile in ChatGPT. Here is
  what to prepare, the four steps, and what to do once you have the blue check.</p>
  <div class="chips"><span>FREE AT LAUNCH</span><span>4 STEPS</span><span>ABOUT 10 MINUTES</span></div>
</div>
<div class="cover-mark">{MARK}</div>
<div class="cover-foot"><span>A beta from OpenAI: the details below were correct at launch and may change.</span></div>
"""
P2 = """
<div class="kicker">BEFORE YOU START</div>
<h2>Have these <em>ready</em></h2>
<ul class="check">
  <li><b>A ChatGPT account for work.</b> Whoever logs in becomes the admin of the profile.</li>
  <li><b>A business phone number or email</b> that matches your public listing, ideally an email on your own domain.</li>
  <li><b>Access to your website</b> (to verify the domain) or <b>your Shopify admin</b>, if you sell on Shopify.</li>
  <li><b>A photo ID</b> for the person managing the profile: the Persona identity check comes after the claim.</li>
  <li><b>Your up-to-date details:</b> what you sell, prices and what is in stock.</li>
</ul>
<div class="note"><h3>Who can claim today</h3>
<p>Online businesses can apply in the markets where ChatGPT operates and OpenAI supports the verification. Local stores
and restaurants can currently claim only an existing US listing. Business Agents (a chat agent for your business) are
for eligible US ecommerce and online-service companies with a website.</p></div>
"""


def stepcard(k, s):
    lis = "".join(f"<li>{e(x)}</li>" for x in s[2])
    return f'<div class="card"><div class="ct"><span class="cn">{k + 1:02d}</span><div><div class="tools">{e(s[1])}</div><h3>{e(s[0])}</h3></div></div><ol class="steps">{lis}</ol></div>'


P3 = '<div class="kicker">THE FOUR STEPS</div><h2>Claim it <em>today</em></h2><div class="cards">' + "".join(stepcard(k, s) for k, s in enumerate(STEPS)) + "</div>"
P4 = """
<div class="kicker">ONCE YOU'RE VERIFIED</div>
<h2>Make it <em>work</em> for you</h2>
<ul class="check">
  <li><b>Add your products.</b> Upload a product feed with prices and stock, or connect your Shopify store.</li>
  <li><b>Keep it accurate.</b> Update prices and stock whenever they change; ChatGPT uses what you give it.</li>
  <li><b>Check your analytics.</b> Business Hub shows the last 28 days: mentions, website clicks and the topics people ask about. Numbers appear once you pass a minimum, so a blank one may just mean data is still coming in.</li>
  <li><b>US online shop?</b> You can publish one Business Agent that answers from your product details. It must say it is AI, keep prices accurate and avoid pressure tactics.</li>
</ul>
<div class="note"><h3>Read before you claim</h3>
<p>Claiming and managing a profile is free at launch; OpenAI has said it may charge in future. A profile does not buy a
better ranking: ChatGPT keeps making its own recommendations, and paid ads are a separate product. OpenAI says it does
not share people's conversations with businesses. Sources: VentureBeat and The Next Web, 10 November 2026.</p></div>
<div class="outro"><div class="outro-mark">""" + MARK + """</div><div><h3>Want more like this?</h3>
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
    body = "".join([page(1, COVER, "cover"), page(2, P2), page(3, P3), page(4, P4)])
    doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Get Your Business into ChatGPT</title><style>{CSS}</style></head><body>{body}</body></html>'
    src = os.path.join(HERE, "chatgpt.html")
    open(src, "w", encoding="utf-8").write(doc)
    out = os.path.join(ROOT, "chatgpt-business-9x16", "renders", "nxtlvl_chatgpt-business.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    prev = os.environ.get("PREVIEW_DIR", os.path.join(HERE, "preview"))
    os.makedirs(prev, exist_ok=True)
    subprocess.run(["node", "-e", SHOT, src, out, prev], check=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
