"""Shot prompts and asset checklist for the Vitonnix Biotin reel final.

python3 build/brief.py <out.html>     (from the project root)

Writes ASSET-BRIEF.md (kept in the repo) and a self-contained HTML page with copy buttons (published as an
Artifact). One data source, so the two never drift. Prompts follow the commercial skill's build order: product
invariant, role, setting, light, camera, composition, guardrails.
"""
import base64
import html
import io
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOCK = ("Use the attached reference photo as the exact product: the Vitonnix Biotin sublingual oral spray, a white "
        "bottle with a magenta-plum label band, the blue oval Vitonnix logo, a chrome collar and a white spray cap. Keep "
        "the bottle shape, label and every word on it exactly as in the reference. Do not redraw, add or translate any text.")
PALETTE = "Colour palette: deep plum #5A0230, plum #890045, magenta glow #C2187A, blush #FFF0F6."
AVOID = ("extra text, captions, watermark, misspelled or changed label, changed logo, warped or melted bottle, two bottles, "
         "extra caps, blurry label, plastic-looking skin, extra fingers, cluttered background")
VLOCK = ("Keep the bottle's shape, label, logo and colours exactly as in the start frame for the whole clip. No text, no new "
         "objects, no morphing, no cuts, no camera shake. Smooth, slow, constant motion. 5 seconds, 9:16, no audio.")

STILLS = [
    dict(id="P1", file="P1-hero-34.png", must=True, aspect="9:16", scene="Product reveal and the final CTA card",
         prompt=f"{LOCK} Premium beauty hero photograph. The bottle stands on a round, glossy plum acrylic pedestal, turned "
                "about 30 degrees to its right so the front label and the chrome collar both catch the light. Seamless deep "
                "plum background that darkens toward the edges, a soft magenta glow directly behind the bottle and a few "
                "out-of-focus sparkle highlights. Lighting: large soft key light from the front left, a thin strip light rim "
                "along the right edge, a gentle reflection on the pedestal top. Camera at label height, 85 mm lens look, the "
                "whole bottle sharp. Vertical 9:16. Bottle centred in the lower half, about 45 percent of the frame height. "
                f"Keep the top 30 percent empty for headline text and the bottom 20 percent free of anything important. {PALETTE} "
                "No text, no props, no hands."),
    dict(id="P2", file="P2-hero-low.png", must=True, aspect="9:16", scene="The music drop on \"Vitonnix Biotin\"",
         prompt=f"{LOCK} Low-angle hero shot looking up at the bottle, which stands tall like a monument against a deep "
                "plum sky of soft magenta haze and tiny floating sparkles. Bottle facing the camera, standing on a mirror-gloss "
                "plum surface that reflects it. Strong backlight rim outlining the cap and shoulders, soft front fill so the "
                "label reads clearly. Wide 24 mm lens look from just above the surface, gentle perspective with no distortion "
                f"of the label. Vertical 9:16, bottle centred, top of the cap about 25 percent from the top. {PALETTE} "
                "No text, no hands."),
    dict(id="P3", file="P3-spray-macro.png", must=True, aspect="9:16", scene="\"One spray under your tongue\"",
         prompt=f"{LOCK} Side-on macro of the bottle mid-spray. The cap is pressed and a fine, airy mist bursts from the "
                "nozzle toward the upper left, catching the light as thousands of tiny glowing droplets with a few pink "
                "sparkles. Bottle tilted about 20 degrees, filling the lower right of the frame, label readable. Background "
                "deep plum to near-black plum, the mist lit from behind so it glows magenta-white. 100 mm macro look, mist "
                "edges soft, bottle and nozzle sharp. Vertical 9:16, mist cloud filling the upper left half, bottom 20 percent "
                f"clear. {PALETTE} No text, no hands, no water splash."),
    dict(id="P4", file="P4-lifestyle-glow.png", must=True, aspect="4:5", scene="\"Made for your hair, skin and nails\"",
         prompt=f"{LOCK} Beauty editorial portrait. An Indian woman in her late twenties with glowing, healthy skin and "
                "glossy, voluminous dark hair laughs with her eyes closed and holds the bottle at shoulder height, label facing "
                "the camera. Natural makeup, soft blush top. Background: seamless blush pink fading into plum at the edges. "
                "Soft beauty-dish key light from the front, a hair light from behind so the hair shines. 85 mm lens look, "
                "f/2.8, face and bottle both sharp. Portrait 4:5, face in the upper half, bottle in the lower third. "
                f"Realistic skin texture with pores, natural hands with five fingers. {PALETTE} No text."),
    dict(id="P5", file="P5-flavour.png", must=True, aspect="9:16", scene="\"Lychee and mint flavour\"",
         prompt=f"{LOCK} Fresh flavour still life. The bottle stands on a pale blush marble surface, surrounded by fresh "
                "lychees (two whole with bumpy red skin, one peeled to show glossy translucent white flesh) and sprigs of "
                "bright green mint. Tiny water droplets on the fruit and leaves. A few lychees and mint leaves hang mid-air "
                "above, as if falling. Background deep plum with a soft magenta glow behind the bottle. Soft diffused key "
                "light from the left, crisp rim light on the right. 70 mm lens look at eye level, bottle sharp, falling fruit "
                f"with slight motion blur. Vertical 9:16, bottle centred, top 25 percent and bottom 20 percent kept simple. {PALETTE} "
                "No text, no hands, no other drinks or packaging."),
    dict(id="P6", file="P6-packshot-white.png", must=False, aspect="1:1", scene="Clean cutout I can move between scenes (skip if the client sends their original render)",
         prompt=f"{LOCK} E-commerce packshot. The bottle faces the camera, perfectly upright and centred on a pure white "
                "seamless background. Even soft light from both sides, a soft shadow only directly under the base. 100 mm "
                "lens look from label height, no perspective distortion, the whole bottle sharp and filling 85 percent of the "
                "frame height. Highest resolution available. No props, no reflections, no text."),
    dict(id="P7", file="P7-nails.png", must=False, aspect="4:5", scene="The \"nails\" beat",
         prompt=f"{LOCK} Close-up of a woman's hand with healthy, glossy natural nails in a nude-pink polish, holding the "
                "bottle by its body with the label facing the camera, against a soft plum background. Soft diffused light, "
                f"100 mm macro look, five natural fingers, realistic skin. Portrait 4:5. {PALETTE} No text, no rings."),
    dict(id="P8", file="P8-hair.png", must=False, aspect="9:16", scene="Background for the \"hair\" beat (no product)",
         prompt="Close-up of glossy, healthy dark hair in motion, backlit so the strands shine, soft plum and magenta "
                f"backdrop, shallow depth of field. Vertical 9:16. {PALETTE} No face, no product, no text."),
    dict(id="P9", file="P9-lychee-mint-cutouts.png", must=False, aspect="1:1", scene="Floating fruit and leaves I animate around the bottle",
         prompt="Isolated on a pure white background: one whole lychee with bumpy red skin, one peeled lychee with glossy "
                "translucent flesh, and one small sprig of fresh mint, each separated by clear space so they can be cut out. "
                "Bright, even studio light, everything sharp, square 1:1. No shadows touching each other, no text."),
    dict(id="P10", file="P10-levitate.png", must=False, aspect="9:16", scene="Transitions and the CTA background",
         prompt=f"{LOCK} The bottle floats at a slight angle above a glossy plum surface, wrapped in a slow swirl of fine "
                "glowing mist and tiny sparkles, with a soft mirror reflection below. Deep plum background with a magenta "
                f"glow. 85 mm lens look, bottle sharp. Vertical 9:16, bottle centred. {PALETTE} No text, no hands."),
    dict(id="P11", file="P11-bottle-box.png", must=False, aspect="9:16", scene="CTA card (needs a sharp photo of the carton as a second reference)",
         prompt=f"{LOCK} Also use the attached photo of its retail carton as the exact box, with its printing unchanged. "
                "The bottle stands in front of and slightly to the right of the carton on a glossy plum surface. Deep plum "
                "background with a soft magenta glow, soft key light from the front left, rim light on the right. 85 mm lens "
                f"look, both items sharp. Vertical 9:16, products in the lower half, top 30 percent empty. {PALETTE} No text."),
]

VIDEOS = [
    dict(id="V1", file="V1-orbit.mp4", must=True, start="P1", scene="Product reveal",
         prompt="Slow, smooth orbit of about 40 degrees around the bottle from left to right at label height, ending on a "
                f"straight front view of the label. The magenta glow behind it breathes gently and a few sparkles drift upward. {VLOCK}"),
    dict(id="V2", file="V2-spray.mp4", must=True, start="P3", scene="\"One spray under your tongue\"",
         prompt="The cap presses down once and a fine mist bursts from the nozzle in slow motion, spreading toward the upper "
                "left, then drifting and glittering as it fades. Camera locked off with a very slow push-in toward the nozzle. "
                f"{VLOCK}"),
    dict(id="V3", file="V3-flavour-fall.mp4", must=False, start="P5", scene="\"Lychee and mint flavour\"",
         prompt="Lychees and mint leaves fall slowly past the bottle in slow motion and a few water droplets catch the light. "
                f"The bottle stays perfectly still and sharp. Camera static. {VLOCK}"),
    dict(id="V4", file="V4-lifestyle.mp4", must=False, start="P4", scene="\"Made for your hair, skin and nails\"",
         prompt="She laughs softly and turns her head a little toward the light, her hair moves naturally, and her hand holds "
                "the bottle steady with the label facing the camera. Very slow push-in. She stays the same person throughout. "
                f"{VLOCK}"),
    dict(id="V5", file="V5-label-push.mp4", must=False, start="P2", scene="The music drop",
         prompt="Slow dolly-in from the full bottle toward the Vitonnix logo and the word Biotin on the label while a soft "
                f"light sweep crosses the bottle from left to right. Stop before the logo fills the frame. {VLOCK}"),
    dict(id="V6", file="V6-levitate.mp4", must=False, start="P10", scene="Transition into the CTA",
         prompt=f"The bottle rises slowly from below into the centre of the frame while the mist swirls around it in a spiral and settles. {VLOCK}"),
]

RULES = [
    ("Always attach the reference bottle image.", "Use an edit or reference mode, for example Nano Banana Pro, GPT Image 2, "
     "Seedream 4 edit, Flux Kontext or Higgsfield Product Photoshoot. Text-only prompts redraw the label and garble \"Vitonnix\"."),
    ("Zoom in on the label before you keep a take.", "Reject any image where the logo, \"Biotin\" or the small print changed. "
     "Make 3 or 4 takes of each shot and keep the cleanest."),
    ("No text inside the images.", "I set all type in the edit, so the images stay clean and the words stay sharp."),
    ("Size.", "Stills at 2160x3840 for 9:16 (at least 1080x1920), PNG or best-quality JPG, no watermark. "
     "Videos: 9:16, 5 seconds, MP4, no audio, no watermark."),
    ("Videos start from an approved still.", "Use image-to-video (Kling, Veo 3, Seedance, Runway or Higgsfield) with the "
     "listed start frame. Smooth, slow camera moves cut together best."),
    ("Name files by ID.", "For example P1-hero-34.png and V1-orbit.mp4, then upload them in this chat."),
]

NEEDS = [
    (True, "Your verdict on draft v2: approve as it is, or list the changes."),
    (True, "Stills P1 to P5, the best take of each."),
    (True, "Video clips V1 and V2."),
    (True, "The Vitonnix logo as SVG, or PNG with a transparent background."),
    (True, "The right absorption figure (the creative says 9X, the website says 5X) and the client's OK to use it."),
    (True, "Confirmation that the comment keyword stays BIOTIN, with an auto-DM set up for it."),
    (False, "The client's original packshot render with a transparent background (replaces P6)."),
    (False, "A sharp photo of the Biotin carton (needed for P11)."),
    (False, "Any of P6 to P11 and V3 to V6."),
    (False, "Script changes, if any. A new voiceover needs an ElevenLabs top-up: 143 credits are left and a full read costs about 390."),
    (False, "Extra formats: a 4:5 feed version or a 1:1 version."),
]

PLAN = [
    "Swap the new shots into each scene: P1 and V1 on the reveal, P2 on the drop, P3 and V2 on \"one spray\", P4 on hair, skin and nails, P5 on flavour.",
    "Keep the bottle on screen as one element that glides between scenes instead of cutting.",
    "Replace the hard white flashes with softer blur-zoom and mist wipes, and add motion blur to fast moves.",
    "Re-time the music hits to the new cuts, then render the final at delivery quality and 60 fps, with a cover image.",
]


def md():
    out = ["# Vitonnix Biotin reel: shot prompts and asset checklist", "",
           "Generate these, send them back named by ID, and I build the smooth final.", "",
           "Reference image to attach to every product prompt: `source/ref-biotin-bottle.png`.", "", "## Before you start", ""]
    out += [f"- **{a}** {b}" for a, b in RULES]
    for title, items, must in (("Stills you must send", STILLS, True), ("Optional stills", STILLS, False)):
        out += ["", f"## {title}", ""]
        for s in [x for x in items if x["must"] == must]:
            out += [f"### {s['id']}: {s['file']} ({s['aspect']})", "", f"For: {s['scene']}", "", "```text", s["prompt"], "```", "",
                    f"Avoid (negative prompt, if your tool has one): {AVOID}", ""]
    for title, must in (("Video clips you must send", True), ("Optional video clips", False)):
        out += ["", f"## {title}", ""]
        for v in [x for x in VIDEOS if x["must"] == must]:
            out += [f"### {v['id']}: {v['file']} (start frame {v['start']})", "", f"For: {v['scene']}", "", "```text", v["prompt"], "```", ""]
    out += ["", "## What I need from you", ""]
    out += [f"- [ ] {'(must) ' if m else '(optional) '}{t}" for m, t in NEEDS]
    out += ["", "## What I will do with them", ""] + [f"1. {p}" for p in PLAN]
    return "\n".join(out) + "\n"


def ref_thumb():
    im = Image.open(os.path.join(ROOT, "source", "ref-biotin-bottle.png")).convert("RGB")
    im.thumbnail((300, 400))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def card(item, kind):
    e = html.escape
    meta = (f'<span class="ratio">{e(item["aspect"])}</span>' if kind == "still" else f'<span class="ratio">from {e(item["start"])}</span>')
    avoid = "" if kind == "video" else (
        f'<div class="avoid"><span class="lbl">Avoid</span><p id="{item["id"]}-avoid">{e(AVOID)}</p>'
        f'<button type="button" class="copy ghost" data-target="{item["id"]}-avoid">Copy</button></div>')
    return f'''<article class="shot" id="shot-{item["id"].lower()}">
  <header><span class="sid">{item["id"]}</span><code class="file">{e(item["file"])}</code>{meta}</header>
  <p class="for"><span class="lbl">For</span> {e(item["scene"])}</p>
  <div class="prompt"><p id="{item["id"]}-p">{e(item["prompt"])}</p><button type="button" class="copy" data-target="{item["id"]}-p">Copy prompt</button></div>
  {avoid}
</article>'''


def page():
    e = html.escape
    still_must = "".join(card(s, "still") for s in STILLS if s["must"])
    still_opt = "".join(card(s, "still") for s in STILLS if not s["must"])
    vid_must = "".join(card(v, "video") for v in VIDEOS if v["must"])
    vid_opt = "".join(card(v, "video") for v in VIDEOS if not v["must"])
    rules = "".join(f"<li><strong>{e(a)}</strong> {e(b)}</li>" for a, b in RULES)
    needs = "".join(f'<li><label><input type="checkbox" id="need-{i}"> <span class="tag {"must" if m else "opt"}">{"Must" if m else "Optional"}</span> {e(t)}</label></li>'
                    for i, (m, t) in enumerate(NEEDS))
    plan = "".join(f"<li>{e(p)}</li>" for p in PLAN)
    return f'''<title>Vitonnix Shot Prompts</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,700;0,9..144,900;1,9..144,600&family=Montserrat:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
/* Layout: one reading column; each shot is a card with its prompt in a copyable well. Plum world from the client's creatives. */
:root {{
  --paper: #fbf3f6; --card: #ffffff; --ink: #2a0a1b; --muted: #75566a; --line: #ecd8e2;
  --plum: #890045; --accent: #b0105f; --well: #f7e8ef; --must: #890045; --opt: #6d6f8a; --ok: #1f7a4d;
  --display: "Fraunces", Georgia, serif; --body: "Montserrat", system-ui, sans-serif; --mono: "JetBrains Mono", ui-monospace, Menlo, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --paper: #1a0710; --card: #230b17; --ink: #fbeef4; --muted: #c9a7b8; --line: #3d1a2b;
  --plum: #ff5fae; --accent: #ff7cbd; --well: #2c0f1e; --must: #ff7cbd; --opt: #a9abc7; --ok: #6fd39a; color-scheme: dark }} }}
:root[data-theme="dark"] {{
  --paper: #1a0710; --card: #230b17; --ink: #fbeef4; --muted: #c9a7b8; --line: #3d1a2b;
  --plum: #ff5fae; --accent: #ff7cbd; --well: #2c0f1e; --must: #ff7cbd; --opt: #a9abc7; --ok: #6fd39a; color-scheme: dark }}
* {{ box-sizing: border-box; }}
body {{ background: var(--paper); color: var(--ink); font-family: var(--body); font-size: 16px; line-height: 1.55; margin: 0;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 40px 72px; }}
.wrap {{ max-width: 760px; margin: 0 auto; display: flex; flex-direction: column; gap: 40px; }}
h1, h2 {{ font-family: var(--display); text-wrap: balance; margin: 0; line-height: 1.1; }}
h1 {{ font-size: clamp(34px, 7vw, 52px); font-weight: 900; letter-spacing: -0.01em; }}
h1 em {{ font-style: italic; font-weight: 600; color: var(--plum); }}
h2 {{ font-size: 28px; font-weight: 700; }}
.lede {{ font-size: 18px; color: var(--muted); margin: 14px 0 0; max-width: 60ch; }}
.eyebrow {{ font-size: 12px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--plum); }}
section {{ display: flex; flex-direction: column; gap: 16px; }}
.sub {{ color: var(--muted); margin: 0; font-size: 15px; }}
.start {{ display: grid; grid-template-columns: 150px minmax(0, 1fr); gap: 24px; align-items: start; }}
.start figure {{ margin: 0; display: flex; flex-direction: column; gap: 8px; }}
.start img {{ width: 150px; border-radius: 14px; border: 1px solid var(--line); background: #fff; }}
.start figcaption {{ font-size: 13px; color: var(--muted); }}
.start figcaption code {{ font-family: var(--mono); font-size: 12px; }}
ul.rules {{ margin: 0; padding-left: 1.1em; display: flex; flex-direction: column; gap: 10px; }}
ul.rules strong {{ font-weight: 700; }}
.shot {{ background: var(--card); border: 1px solid var(--line); border-radius: 18px; padding: 18px 18px 16px; display: flex; flex-direction: column; gap: 12px; }}
.shot header {{ display: flex; flex-wrap: wrap; align-items: center; gap: 10px; }}
.sid {{ font-family: var(--display); font-weight: 900; font-size: 22px; color: var(--plum); min-width: 2.2em; }}
.file {{ font-family: var(--mono); font-size: 13px; background: var(--well); padding: 3px 8px; border-radius: 6px; overflow-wrap: anywhere; }}
.ratio {{ margin-left: auto; font-size: 12px; font-weight: 700; letter-spacing: .06em; color: var(--muted); border: 1px solid var(--line); border-radius: 999px; padding: 2px 10px; }}
.for {{ margin: 0; font-size: 15px; }}
.lbl {{ font-size: 11px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); margin-right: 6px; }}
.prompt {{ background: var(--well); border-radius: 12px; padding: 14px 14px 12px; display: flex; flex-direction: column; gap: 10px; }}
.prompt p {{ margin: 0; font-family: var(--mono); font-size: 13.5px; line-height: 1.6; overflow-wrap: anywhere; }}
.avoid {{ display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 10px; font-size: 13px; color: var(--muted); }}
.avoid p {{ margin: 0; flex: 1 1 260px; min-width: 0; }}
button.copy {{ align-self: flex-start; font: 600 14px var(--body); color: #fff; background: var(--accent); border: 0; border-radius: 999px; padding: 8px 18px; cursor: pointer; }}
button.copy.ghost {{ background: transparent; color: var(--accent); border: 1px solid var(--line); padding: 4px 12px; font-size: 13px; }}
button.copy.done {{ background: var(--ok); color: #fff; }}
button.copy:focus-visible, input:focus-visible {{ outline: 3px solid var(--accent); outline-offset: 2px; }}
.group-title {{ display: flex; align-items: baseline; gap: 12px; flex-wrap: wrap; }}
.group-title span {{ font-size: 14px; color: var(--muted); }}
ul.needs {{ list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 2px; }}
ul.needs li {{ border-bottom: 1px solid var(--line); }}
ul.needs label {{ display: flex; gap: 10px; align-items: baseline; padding: 10px 2px; cursor: pointer; }}
ul.needs input {{ accent-color: var(--accent); width: 18px; height: 18px; flex: none; transform: translateY(3px); }}
.tag {{ flex: none; font-size: 11px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; border-radius: 999px; padding: 1px 8px; border: 1px solid currentColor; }}
.tag.must {{ color: var(--must); }} .tag.opt {{ color: var(--opt); }}
ol.plan {{ margin: 0; padding-left: 1.3em; display: flex; flex-direction: column; gap: 8px; }}
footer {{ font-size: 13px; color: var(--muted); border-top: 1px solid var(--line); padding-top: 16px; }}
@media (max-width: 520px) {{ .start {{ grid-template-columns: minmax(0, 1fr); }} .start img {{ width: 120px; }} }}
@media (prefers-reduced-motion: no-preference) {{ button.copy {{ transition: background .15s ease; }} }}
</style>
<div class="wrap">
  <header>
    <div class="eyebrow">Nxtlvl Social · Vitonnix Biotin reel</div>
    <h1>Shot prompts for the <em>final cut</em></h1>
    <p class="lede">Generate these, send them back named by ID, and I build the smooth final. The must-haves are P1 to P5, V1 and V2. Everything else makes it richer.</p>
  </header>

  <section aria-labelledby="h-start">
    <h2 id="h-start">Before you start</h2>
    <div class="start">
      <figure><img src="{ref_thumb()}" alt="Reference photo of the Vitonnix Biotin spray bottle on white"><figcaption>Attach this to every product prompt. Full size: <code>ref-biotin-bottle.png</code>, sent in the chat.</figcaption></figure>
      <ul class="rules">{rules}</ul>
    </div>
  </section>

  <section aria-labelledby="h-must">
    <div class="group-title"><h2 id="h-must">Stills you must send</h2><span>P1 to P5</span></div>
    {still_must}
  </section>

  <section aria-labelledby="h-vmust">
    <div class="group-title"><h2 id="h-vmust">Video clips you must send</h2><span>image-to-video from the listed still</span></div>
    {vid_must}
  </section>

  <section aria-labelledby="h-opt">
    <div class="group-title"><h2 id="h-opt">Optional stills</h2><span>richer scenes and transitions</span></div>
    {still_opt}
  </section>

  <section aria-labelledby="h-vopt">
    <div class="group-title"><h2 id="h-vopt">Optional video clips</h2></div>
    {vid_opt}
  </section>

  <section aria-labelledby="h-needs">
    <h2 id="h-needs">What I need from you</h2>
    <p class="sub">Tick items off as you go. The ticks stay in this browser only.</p>
    <ul class="needs">{needs}</ul>
  </section>

  <section aria-labelledby="h-plan">
    <h2 id="h-plan">What I do with them</h2>
    <ol class="plan">{plan}</ol>
  </section>

  <footer>Prompts write no text into the images on purpose. Headlines, stats and captions are set in the edit in Fraunces and Montserrat.</footer>
</div>
<script>
(function () {{
  function flash(btn, label) {{ var old = btn.dataset.label || btn.textContent; btn.dataset.label = old; btn.textContent = label; btn.classList.add('done');
    setTimeout(function () {{ btn.textContent = old; btn.classList.remove('done'); }}, 1600); }}
  function selectText(el) {{ var r = document.createRange(); r.selectNodeContents(el); var s = window.getSelection(); s.removeAllRanges(); s.addRange(r); }}
  document.querySelectorAll('button.copy').forEach(function (btn) {{
    btn.addEventListener('click', function () {{
      var el = document.getElementById(btn.dataset.target); var text = el.textContent;
      try {{
        navigator.clipboard.writeText(text).then(function () {{ flash(btn, 'Copied'); }}, function () {{ selectText(el); flash(btn, 'Selected, press copy'); }});
      }} catch (e) {{ selectText(el); flash(btn, 'Selected, press copy'); }}
    }});
  }});
  document.querySelectorAll('ul.needs input').forEach(function (box) {{
    try {{ box.checked = localStorage.getItem('vx-' + box.id) === '1'; }} catch (e) {{}}
    box.addEventListener('change', function () {{ try {{ localStorage.setItem('vx-' + box.id, box.checked ? '1' : '0'); }} catch (e) {{}} }});
  }});
}})();
</script>
'''


if __name__ == "__main__":
    open(os.path.join(ROOT, "ASSET-BRIEF.md"), "w").write(md())
    if len(sys.argv) > 1:
        open(sys.argv[1], "w").write(page())
    print("ASSET-BRIEF.md written" + (f"; page {sys.argv[1]}" if len(sys.argv) > 1 else ""))
