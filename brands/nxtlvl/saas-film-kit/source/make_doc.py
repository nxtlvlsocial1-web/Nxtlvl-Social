"""Combined PDF: Nxtlvl Social logo + SaaS film elements + every prompt, in one document."""
import html
K = '/home/user/Nxtlvl-Social/brands/nxtlvl/saas-film-kit/'
F = 'file:///home/user/Nxtlvl-Social/website/fonts/'
e = html.escape

STYLE = ('Premium SaaS product motion graphic. Very light lavender background (#F4F0FE) with a soft violet (#7D18FC) to lilac (#B46CFF) '
         'gradient glow, frosted white glass UI cards with rounded corners and soft shadows, glossy 3D elements, smooth ease-in-out motion, '
         'gentle parallax, Apple and Linear style product animation, bright, clean, minimal. Colours only white, lavender, violet, lilac, '
         'a little pink, and green for success. No text, no letters, no numbers, no logos, no people.')
NEG = 'text, letters, numbers, watermark, logo, brand names, distorted UI, clutter, dark background, neon overload, glitch, shaky camera, deformed character, flicker, low quality'
LOGO_PROMPT = ('The app-icon logo from the image comes alive: the violet gradient tile glows softly, the white four-point star shimmers and emits a brief '
               'sparkle, the three trailing streaks shoot forward with a light trail and settle back into place, a soft violet light sweep passes across '
               'the tile. Gentle float up and back down. Background stays very light lavender (#F4F0FE), camera locked, no other objects. The logo '
               'shape, colours and proportions stay exactly the same as the reference; it ends perfectly still, identical to the first frame. '
               'No text, no letters, no new shapes.')
SCENES = [
 ('01-hello', '1. Hello', '0-4 s', 'Meet your AI growth team',
  'The glossy violet jelly blob mascot in the image floats gently, waves hello twice, blinks and smiles; its sparkle twinkles; the glass chips around it drift slowly and the orbit ring turns. Camera slowly pushes in. Keep the mascot exactly as in the image.'),
 ('02-dashboard', '2. Dashboard', '4-9 s', '6 AI agents, working daily',
  'The blob mascot points at the glass cards; chat bubbles in the chat window appear one by one, the line chart draws itself upward to the dot, calendar squares light up violet one after another, and the small card with the green tick slides in. Gentle parallax, camera glides right.'),
 ('03-whatsapp-flow', '3. WhatsApp flow', '9-14 s', 'Every enquiry answered in seconds',
  'Light pulses travel along the dotted violet line from the green chat card into the glossy glass orb, which glows and pulses, then the pulses split along the three paths: the reply bubble pops, the calendar card shows its green tick, the contact card settles. Isometric feel, slow orbit.'),
 ('04-lead-capture', '4. Lead capture', '14-19 s', 'Every lead captured',
  'The form card lifts off the phone, flies along the dotted arc and drops into the glass inbox, where the cards stack and the green tick badge pops; the small phone on the right lights its violet dot. Smooth dolly from left to right.'),
 ('05-content-website', '5. Content and websites', '19-24 s', 'Reels, ads and websites',
  'The play button on the phone pulses, the thumbnail tiles slide in one by one like a timeline, hearts float upward, the browser window blocks settle into place and the round gauge sweeps to full with a green glow. Gentle 3D rotation.'),
 ('06-growth', '6. Growth', '24-30 s', 'Grow on one monthly plan',
  'The bars grow one by one from left to right, the line arcs up to the peak dot, sparkles burst at the top, the green stat card pops in, and the blob mascot bounces with joy, arms up. Camera slowly pulls back.'),
 ('07-end-card', '7. End card', 'last 2 s', 'Logo + Book a free call',
  'Use this frame as is, or as the last frame of the logo animation. Nothing needs generating here; it already holds the real logo and the call to action.'),
]
COMBINED = (STYLE.replace('Premium SaaS product motion graphic.', 'Premium SaaS product launch film, 30 seconds, 16:9, one continuous smooth camera move linking every shot.') +
 ' The mascot is the glossy violet jelly blob from the reference image, with big friendly eyes and a small sparkle above its head, identical in every shot.\n\n'
 'Shot 1 (0-4s): The blob mascot floats in the centre, waves hello and smiles; its sparkle twinkles. Camera slowly pushes in.\n'
 'Shot 2 (4-9s): The blob turns and points; frosted glass dashboard cards fly in around it: a chat window with message bubbles appearing one by one, a line chart drawing upward, a calendar tile lighting up violet squares.\n'
 'Shot 3 (9-14s): Camera glides into the chat window. A green-tinted chat bubble travels along a glowing violet line into a pulsing glass AI orb, which splits into three paths: a reply bubble, a calendar card flipping to a green tick, and a contact card sliding into a stacked list.\n'
 'Shot 4 (14-19s): A glossy phone shows an ad card; a form card flies out, unfolds and drops into a glowing inbox tray where cards stack and a green badge pulses.\n'
 'Shot 5 (19-24s): A vertical phone frame; video thumbnails slide in like a timeline, a violet play button pulses, hearts and comment bubbles float upward. Beside it a glass browser window assembles itself and a speed gauge sweeps to full with a green glow.\n'
 'Shot 6 (24-30s): A large glass bar chart grows bar by bar in a violet gradient, a line arcs upward, sparkles burst at the peak; the blob mascot pops up beside the chart and does a happy bounce with both arms raised. Camera slowly pulls back, leaving clean empty space on the left for a headline and logo.\n\n'
 'No text, no letters, no numbers, no logos, no people, no dark backgrounds, no glitch, no flicker.')

def pre(t): return f'<div class="prompt">{e(t)}</div>'
scene_pages = ''
for i in range(0, len(SCENES), 2):
    block = ''
    for slug, title, time, text, prompt in SCENES[i:i + 2]:
        block += (f'<div class="scene"><img src="{K}frames/{slug}.png"><div class="meta"><h3>{title}</h3><p class="tag">{time} · overlay text: <b>{e(text)}</b> · '
                  f'start frame: <code>frames/{slug}.png</code></p>{pre(prompt if slug == "07-end-card" else "[STYLE BLOCK] " + prompt)}</div></div>')
    scene_pages += f'<section>{"<h2>3. Scenes: start frames and prompts</h2>" if i == 0 else ""}{block}</section>'

logo_files = [('nxtlvl-social-logo-lockup.png', 'Logo lockup: rocket tile + wordmark, transparent, 2400 px'), ('nxtlvl-social-rocket-tile.png', 'App icon / profile: rocket on gradient tile, 1024 px'),
              ('nxtlvl-social-rocket-mark.png', 'Rocket mark, white, for dark backgrounds'), ('nxtlvl-social-rocket-mark-dark.png', 'Rocket mark, ink, for light backgrounds'),
              ('logo-frame-1x1.png', 'Kling first + last frame, 1:1'), ('logo-frame-16x9.png', 'Kling first + last frame, 16:9')]
lf = ''.join(f'<figure class="{"dark" if "mark.png" in f else ""}"><img src="{K}logo/{f}"><figcaption><b>{f}</b><br>{d}</figcaption></figure>' for f, d in logo_files)

doc = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:B;src:url({F}bricolage-variable.woff2);font-weight:200 800}}
@font-face{{font-family:S;src:url({F}satoshi-400.woff2);font-weight:400}}@font-face{{font-family:S;src:url({F}satoshi-700.woff2);font-weight:700}}
@page{{size:A4;margin:14mm 13mm}} *{{box-sizing:border-box}} body{{font:400 9.6pt/1.5 S,sans-serif;color:#140B2E;margin:0}}
h1,h2,h3{{font-family:B;font-weight:800;letter-spacing:-.02em;margin:0}} h2{{font-size:18pt;margin:0 0 10px}} h3{{font-size:12pt}}
section{{page-break-before:always}} p{{margin:0 0 8px}} .lead{{color:#4D4570;max-width:170mm}} code{{font-size:8.5pt;background:#F1ECFB;padding:1px 5px;border-radius:5px}}
.cover{{height:265mm;border-radius:20px;padding:20mm 16mm;background:radial-gradient(45% 40% at 85% 15%,rgba(180,108,255,.35),transparent 70%),radial-gradient(40% 40% at 10% 90%,rgba(255,79,163,.14),transparent 70%),#F4F0FE;position:relative;overflow:hidden}}
.cover .lock{{width:120mm}} .cover h1{{font-size:38pt;line-height:1.02;margin-top:30mm;max-width:150mm}} .cover p{{font-size:12.5pt;color:#4D4570;max-width:140mm;margin-top:8mm}}
.cover .shot{{position:absolute;right:-20mm;bottom:22mm;width:150mm;border-radius:16px;box-shadow:0 30px 60px -30px rgba(94,6,242,.5)}} .cover small{{position:absolute;left:16mm;bottom:12mm;color:#7B7499}}
.files{{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-top:10px}} figure{{margin:0;border:1px solid #E6DEFA;border-radius:12px;padding:9px;background:#fff}}
figure img{{width:100%;height:34mm;object-fit:contain;background:repeating-conic-gradient(#F4F0FE 0 25%,#fff 0 50%) 0 0/14px 14px;border-radius:8px}} figure.dark img{{background:#140B2E}}
figcaption{{font-size:8.2pt;color:#4D4570;margin-top:5px;line-height:1.35}} figcaption b{{color:#140B2E;font-size:8pt}}
.prompt{{background:#F4F0FE;border:1px solid #E6DEFA;border-radius:10px;padding:9px 11px;font:400 8.6pt/1.5 ui-monospace,Menlo,monospace;white-space:pre-wrap;color:#2A2148}}
.scene{{display:grid;grid-template-columns:86mm 1fr;gap:9mm;align-items:start;margin-bottom:9mm}} .scene img{{width:100%;border-radius:10px;border:1px solid #E6DEFA}}
.scene .tag{{color:#4D4570;font-size:8.6pt;margin:3px 0 7px}} .two{{display:grid;grid-template-columns:1fr 1fr;gap:8mm}}
table{{width:100%;border-collapse:collapse;font-size:9pt}} th{{text-align:left;font-size:7.8pt;text-transform:uppercase;letter-spacing:.06em;color:#7B7499;padding:6px;border-bottom:1px solid #E6DEFA}} td{{padding:7px 6px;border-bottom:1px solid #F0EAFD;vertical-align:top}}
.note{{background:#fff;border:1px solid #E6DEFA;border-left:4px solid #7D18FC;border-radius:8px;padding:8px 11px;margin:10px 0;color:#4D4570}}
</style></head><body>
<div class="cover"><img class="lock" src="{K}logo/nxtlvl-social-logo-lockup.png">
<h1>SaaS motion film kit</h1><p>The Nxtlvl Social logo, every element of the 30-second SaaS film as a ready start frame, and every prompt: one document to make the film in Kling, Seedance, Veo or Higgsfield.</p>
<img class="shot" src="{K}frames/02-dashboard.png"><small>21 November 2026 · All elements made in code from the real logo and the Nextyy mascot · connect@nxtlvlsocial.ai</small></div>

<section><h2>1. The Nxtlvl Social logo</h2><p class="lead">The real logo is the rocket: a white four-point star with three trailing streaks, on the violet gradient tile, next to the "nxtlvl social" wordmark. Every file below is drawn from that exact mark. Never let an AI tool redraw the logo; animate the real file instead.</p>
<div class="files">{lf}</div>
<div class="note">The older squiggly "N" mark in <code>brands/nxtlvl/png/icon-*.png</code> and <code>logo.svg</code> is not the Nxtlvl Social logo. Use the files in <code>brands/nxtlvl/saas-film-kit/logo/</code>.</div>
<h3 style="margin-top:12px">Colours and type</h3>
<table><tr><th>Use</th><th>Value</th></tr><tr><td>Logo gradient</td><td>#5E06F2 → #7D18FC → #B46CFF</td></tr><tr><td>Tile base</td><td>#0A0620 with violet light</td></tr><tr><td>Background</td><td>Mist #F4F0FE</td></tr><tr><td>Ink text</td><td>#140B2E · wordmark "social" #6B6391</td></tr><tr><td>Success</td><td>#0B9B68</td></tr><tr><td>Fonts</td><td>Bricolage Grotesque ExtraBold (headlines), Satoshi (text)</td></tr></table></section>

<section><h2>2. Logo animation</h2><p class="lead">Kling 3.0 Pro, image to video, 5 s, no audio. Put the same frame in as the <b>first and last frame</b>, so the clip always lands back on the exact logo.</p>
<div class="two"><figure><img src="{K}logo/logo-frame-1x1.png" style="height:60mm"><figcaption><b>logo/logo-frame-1x1.png</b> · square intro or outro</figcaption></figure>
<figure><img src="{K}logo/logo-frame-16x9.png" style="height:60mm"><figcaption><b>logo/logo-frame-16x9.png</b> · tile left of centre, space for the wordmark</figcaption></figure></div>
<h3 style="margin:12px 0 6px">Prompt</h3>{pre(LOGO_PROMPT)}
<p style="margin-top:8px">For the 16:9 version add: <i>"The tile sits slightly left of centre, leaving clean space on the right for the wordmark, which is added later."</i> Add the wordmark afterwards in HyperFrames or any editor; never let the AI write it.</p>
<h3 style="margin:12px 0 6px">Style block (start every scene prompt with this)</h3>{pre(STYLE)}
<h3 style="margin:12px 0 6px">Negative prompt</h3>{pre(NEG)}</section>
{scene_pages}
<section><h2>4. Combined prompt: the whole film in one go</h2><p class="lead">For Seedance 2.5 (up to 30 s). Upload <code>frames/01-hello.png</code> (or the Nextyy image) as the reference so the mascot stays identical. For Kling 3.0 (15 s max) run shots 1-3 with <code>01-hello.png</code> as the first frame, then shots 4-6 with the last frame of part 1 as the first frame.</p>{pre(COMBINED)}</section>

<section><h2>5. Putting it together</h2>
<table><tr><th>#</th><th>Clip</th><th>Length</th><th>Start frame</th><th>Overlay text (added afterwards)</th></tr>
<tr><td>1</td><td>Hello</td><td>4 s</td><td>frames/01-hello.png</td><td>Meet your AI growth team</td></tr>
<tr><td>2</td><td>Dashboard</td><td>5 s</td><td>frames/02-dashboard.png</td><td>6 AI agents, working daily</td></tr>
<tr><td>3</td><td>WhatsApp flow</td><td>5 s</td><td>frames/03-whatsapp-flow.png</td><td>Every enquiry answered in seconds</td></tr>
<tr><td>4</td><td>Lead capture</td><td>5 s</td><td>frames/04-lead-capture.png</td><td>Every lead captured</td></tr>
<tr><td>5</td><td>Content and websites</td><td>5 s</td><td>frames/05-content-website.png</td><td>Reels, ads and websites</td></tr>
<tr><td>6</td><td>Growth</td><td>6 s</td><td>frames/06-growth.png</td><td>Grow on one monthly plan</td></tr>
<tr><td>7</td><td>Logo animation + end card</td><td>2-3 s</td><td>logo/logo-frame-16x9.png → frames/07-end-card.png</td><td>Book a free call · nxtlvlsocial.ai</td></tr></table>
<div class="note"><b>Rules we follow:</b> open on the mascot and headline (hook in the first 1.5 s, no logo-first intro); burn in the text because most viewers watch muted; end on the call to action for at least 1.5 s; only licensed or generated music. Text, numbers and the logo are always added afterwards, never generated.</div>
<h3 style="margin:12px 0 6px">Settings</h3>
<table><tr><th>Where</th><th>Format</th></tr><tr><td>Website, YouTube, LinkedIn</td><td>16:9 · 1920 x 1080 · 30 fps</td></tr><tr><td>Reels, Shorts, TikTok</td><td>9:16 cut-down · keep text out of the top 250 px and bottom 400 px</td></tr><tr><td>Each AI clip</td><td>5 s, no audio, image to video from the start frame</td></tr></table>
<h3 style="margin:12px 0 6px">Cost if generated (YepAPI prices, 21 Nov 2026)</h3>
<table><tr><th>Item</th><th>Cost</th></tr><tr><td>Logo animation (Kling 3.0 Pro, 5 s, no audio)</td><td>about $0.95</td></tr><tr><td>Six scene clips (5 s each)</td><td>about $5.70</td></tr><tr><td>Or the combined film as two 15 s Kling clips</td><td>about $5.70</td></tr><tr><td>Start frames and logo files</td><td>$0, made in code (this kit)</td></tr></table>
<p style="margin-top:10px;color:#7B7499;font-size:8.6pt">Files: <code>brands/nxtlvl/saas-film-kit/</code> → <code>logo/</code> and <code>frames/</code>. Mascot images were made earlier with Nano Banana 3 Pro from the chosen blob design.</p></section>
</body></html>'''
open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'doc.html'), 'w').write(doc)
print('ok')
