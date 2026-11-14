// Creedom 3D storytelling guide: the brief the Concept / NxtlvlSocial workspace builds the 3D render from.
// Story concepts and the recommended script + shot list, art direction, the Cree character sheet (Creedom's own mascot:
// the client's 3D render poses from creedom-explainer-9x16), worlds and props, render spec and an AI prompt pack.
// Creedom look: blush-white paper, ink #0b0b0b, the wordmark's magenta -> pink -> coral, Manrope + Fraunces italic.
// Phone-friendly 1080 x 1350 pages, rasterised so every viewer draws them the same.
// node build/guide.cjs   -> renders/creedom_3d-storytelling-guide.pdf (page images in cache/guide/)
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "renders", "creedom_3d-storytelling-guide.pdf");
const A = (p) => "file://" + path.join(ROOT, p);
const PAGES = [];
const TOTAL = 14;

function page({ kicker, title, body, cls = "" }) {
  const n = PAGES.length + 1;
  PAGES.push(`<section class="pg ${cls}"><header><div class="kick">${kicker}</div><h2>${title}</h2>
    <img class="wm" src="${A("assets/img/wordmark.png")}"></header>
    <main>${body}</main>
    <footer><span>CREEDOM · 3D STORYTELLING GUIDE</span><span>${String(n).padStart(2, "0")} / ${String(TOTAL).padStart(2, "0")}</span></footer></section>`);
}
const steps = (items) => `<ol class="steps">${items.map((s) => `<li><span class="bd">${s[0]}</span><p>${s[1]}</p></li>`).join("")}</ol>`;
const note = (t, c = "") => `<div class="note ${c}">${t}</div>`;
const kv = (rows) => `<div class="kv">${rows.map(([k, v]) => `<div class="k">${k}</div><div class="v">${v}</div>`).join("")}</div>`;
const pose = (n, cap) => `<figure><img src="${A(`assets/img/poses/${n}.png`)}"><figcaption>${cap}</figcaption></figure>`;

// 1 cover
PAGES.push(`<section class="pg cover"><div class="cglow"></div><div class="cwrap">
  <img class="cwm" src="${A("assets/img/wordmark.png")}">
  <div class="ckick">BRIEF FOR THE 3D RENDER · CONCEPT / NXTLVLSOCIAL</div>
  <h1>3D Storytelling<br><em>Guide</em></h1>
  <img class="chero" src="${A("assets/img/mascot_src.png")}">
  <div class="csub">The story, the look, and exactly how <em>Cree</em> should look and move.</div>
  <div class="cpills"><span>STORY</span><span>SHOT LIST</span><span>ART STYLE</span><span>CREE</span><span>RENDER SPEC</span></div>
</div></section>`);

// 2 brief at a glance
page({ kicker: "01 · THE BRIEF", title: 'At a <em>glance</em>',
  body: kv([
    ["What", "A 3D animated storytelling reel for Creedom, starring its mascot Cree."],
    ["Goal", "Make one idea feel obvious: <b>Creedom shows you why a reel will flop, before you post it, with the exact second and the fix.</b>"],
    ["Who it's for", "Creators who post reels and have no idea why one works and the next one doesn't."],
    ["Length", "35 to 45 seconds. Vertical 9:16, 1080 x 1920."],
    ["Format", "Character story, no talking head. Voiceover plus Cree's acting. Minimal on-screen text."],
    ["CTA", "Comment <b>CREEDOM</b> and we DM the link."],
    ["Hero", "The creator is the hero; <b>Cree is the guide</b> who shows the way. Cree never takes the credit."],
  ]) + note("Everything in this guide is a starting point for the 3D team. The story, look and Cree's design rules are the parts to keep fixed.") });

// 3 what creedom does
page({ kicker: "02 · THE PRODUCT, TRUTHFULLY", title: 'What we can <em>show</em>',
  body: steps([
    ["1", "<b>It watches the whole reel, second by second,</b> like a real viewer would."],
    ["2", "<b>It scores the reel</b> before you post, so you know where it stands."],
    ["3", "<b>It flags the exact moments</b> that need work: a weak hook, a claim with no proof, a moment that loses trust."],
    ["4", "<b>Each flag comes with the timestamp and the fix,</b> so you change the right second, not the whole video."],
    ["5", "<b>It reads a creator's page</b> and gives a content score from public posts."],
  ]) + note("<b>Don't claim</b> guaranteed views, virality or follower numbers. Any score or view count in the story is shown as an example, never as a promise.", "warn") });

// 4 story rules
page({ kicker: "03 · STORY RULES", title: 'How the story <em>moves</em>',
  body: steps([
    ["1", "<b>Open mid-story at full tension.</b> The first 2 seconds already show the problem; no logo, no intro."],
    ["2", "<b>First peak by 5 to 15 seconds:</b> a contrast or a surprise (the best moment was hiding at 0:34)."],
    ["3", "<b>Then peak, release, peak, release.</b> Each beat is one clear visual idea."],
    ["4", "<b>Make the product moment physical.</b> The timeline is a path Cree walks; a flag is a glowing tag; the fix is something he picks up and moves."],
    ["5", "<b>One problem, one creator, one fix.</b> Don't explain every feature."],
    ["6", "<b>End on the CTA,</b> with Cree and the Creedom wordmark on screen."],
  ]) });

// 5 concepts
const CON = [
  ["A", "The Buried Hook", "RECOMMENDED", "A creator's reel flops. Cree jumps into the reel, a world made of film frames, walks the timeline with his magnifier, finds her best moment buried at 0:34 and carries it to the front."],
  ["B", "The Screen Test", "", "2 a.m., about to post. Cree pops out of the phone and runs a tiny screening for a crowd of viewer-bubbles. They drift away at 0:03. He fixes the opening; the next screening, they stay."],
  ["C", "The Reel Gym", "", "Reels are athletes; Cree is the coach with a stopwatch. A flabby, slow-starting reel trains its hook until it sprints off the line."],
  ["D", "The Case of the Missing Views", "", "Cree as a pocket-sized detective with a magnifier. Clues on a pinboard (timestamps), the culprit is a 4-second intro."],
];
page({ kicker: "04 · CONCEPTS", title: 'Four ways in,<br><em>one pick</em>',
  body: `<div class="cons">${CON.map(([l, t, r, d]) => `<div class="con ${r ? "rec" : ""}"><div class="ch"><span class="bd">${l}</span><b>${t}</b>${r ? `<i>${r}</i>` : ""}</div><p>${d}</p></div>`).join("")}</div>`
    + note("<b>Why A:</b> it shows the product's one real superpower (the exact second and the fix) as a single physical action anyone understands without reading.") });

// 6 script
const VO = [
  ["0:00", "Her best moment was hiding at second thirty-four. Nobody ever got that far."],
  ["0:05", "She posted anyway. A few hundred views. No idea why."],
  ["0:09", "So she asked Cree."],
  ["0:11", "Cree doesn't guess. He walks through her reel second by second, like a real viewer."],
  ["0:17", "Zero to three: a slow start. That's where people swipe."],
  ["0:21", "Then, at thirty-four... there it is."],
  ["0:25", "Cree carries it to the front. Same reel, new first second."],
  ["0:31", "She posts. This time, they stay."],
  ["0:35", "Check your reel before you post. Comment CREEDOM."],
];
page({ kicker: "05 · THE STORY · CONCEPT A", title: 'The Buried Hook:<br><em>voiceover</em>',
  body: `<div class="vo">${VO.map(([t, l]) => `<div class="vl"><span>${t}</span><p>${l}</p></div>`).join("")}</div>`
    + note("About 38 seconds, 75 words. Voice: warm, conversational storyteller. The view count and scores in the story are illustrative.") });

// 7-8 shot list
const SHOTS = [
  ["1", "0:00–0:05", "Night bedroom-studio, ring light on. Slow push-in over the creator's shoulder to her phone: her reel plays, the view counter sits still. Camera drifts past the phone into the reel's timeline; a faint gold glow far down the track.", "Her best moment was hiding at second thirty-four..."],
  ["2", "0:05–0:09", "Close on the phone: a flat graph, a small number. She sighs, drops the phone on the bed, screen up.", "She posted anyway..."],
  ["3", "0:09–0:11", "The screen glows pink. Cree pops up out of the screen like a jack-in-the-box, lands with a squash, waves at her.", "So she asked Cree."],
  ["4", "0:11–0:17", "Cree dives into the screen. Inside the reel: a long glowing timeline track running through a valley of giant film frames. Cree walks it, magnifier up, frames lighting as he passes. Low tracking shot.", "Cree doesn't guess..."],
  ["5", "0:17–0:21", "At 0:03 a crowd of small translucent viewer-bubbles drifts away. A glass tag pops up: 0:03 · Weak hook. Cree frowns, taps it.", "Zero to three: a slow start..."],
  ["6", "0:21–0:25", "Deep in the track, a dusty frame. Cree wipes it: gold light floods out, the frame glows. Tag: 0:34 · Best moment. Cree's eyes go wide.", "Then, at thirty-four..."],
  ["7", "0:25–0:31", "Cree lifts the glowing frame overhead and runs it back along the track (comic waddle, speed lines), slots it in at 0:00. Every frame behind re-sorts with a satisfying cascade.", "Cree carries it to the front..."],
  ["8", "0:31–0:35", "Back in the bedroom. She taps Post. The counter starts rolling; little hearts float up. Cree hops on the phone edge and cheers.", "She posts. This time, they stay."],
  ["9", "0:35–0:40", "End card: Cree in front of a soft pink glow, pointing to the Creedom wordmark. A comment box types CREEDOM.", "Check your reel before you post..."],
];
const shotRows = (a, b) => `<div class="shots">${SHOTS.slice(a, b).map(([n, t, v, l]) => `<div class="shot"><div class="sh1"><span class="bd">${n}</span><em>${t}</em></div><p>${v}</p><q>${l}</q></div>`).join("")}</div>`;
page({ kicker: "06 · SHOT LIST · 1 OF 2", title: 'Shots <em>1 to 4</em>', body: shotRows(0, 4)
  + note("Cut on the music's beat. Hold the gold-frame reveal (shot 6) half a second longer than feels comfortable.") });
page({ kicker: "06 · SHOT LIST · 2 OF 2", title: 'Shots <em>5 to 9</em>', body: shotRows(4, 9) });

// 9 cree sheet
page({ kicker: "07 · CREE · CHARACTER SHEET", title: 'How Cree <em>looks</em>',
  body: `<div class="poses">${pose("stand", "Neutral")}${pose("wave", "Wave")}${pose("mag", "Magnifier")}${pose("cheer", "Cheer")}</div>`
    + kv([
      ["Shape", "One soft egg-shaped body: head and body are a single form, no neck. Slightly wider at the bottom."],
      ["Colour", "Hot magenta-pink all over (base #F343A2, shading #E0187E, highlights #FF8CC6). Never another colour."],
      ["Eyes", "Big, round, glossy: white with a large black pupil and two white catchlights. Thin darker-pink brows above."],
      ["Beak", "Small, rounded, yellow-orange (#FFC21A to #F2A516). Open in a smile, red inside."],
      ["Wings and feet", "Short rounded wing-arms used like hands. Stubby yellow-orange feet."],
      ["Surface", "Soft matte, velvety plush-toy feel with gentle subsurface glow. No visible feathers."],
    ]) });

// 10 cree acting
page({ kicker: "07 · CREE · ACTING", title: 'How Cree <em>moves</em>',
  body: `<div class="poses">${pose("point", "Point")}${pose("think", "Think")}${pose("shock", "Shock")}${pose("proud", "Proud")}</div>`
    + `<div class="dd"><div class="do"><b>DO</b><ul><li>Bouncy, squash-and-stretch hops</li><li>A little waddle when he walks</li><li>Use the wings as hands: point, wave, hold, carry</li><li>Big readable expressions: curious, shocked, proud</li><li>Keep him small next to people, heroic in the reel world</li></ul></div>
       <div class="dont"><b>DON'T</b><ul><li>Flap the wings or fly: he isn't treated as a bird</li><li>Change his colour, proportions or eye style</li><li>Add clothes or accessories (props are fine)</li><li>Make him look sad for long; the dip is one beat</li><li>Let him take the creator's win</li></ul></div></div>` });

// 11 art direction
page({ kicker: "08 · ART DIRECTION", title: 'The <em>look</em>',
  body: kv([
    ["Style", "Premium stylised 3D, like a feature-animation short: soft, rounded shapes and designer-toy materials. Not realistic, not cartoon-flat."],
    ["Palette", '<span class="sw" style="background:#F343A2"></span><span class="sw" style="background:#E235DD"></span><span class="sw" style="background:#E68B70"></span><span class="sw" style="background:#FFC21A"></span><span class="sw" style="background:#FFF4F8"></span><span class="sw" style="background:#0B0B0B"></span> Creedom magenta to coral, warm gold for the "found it" moments, blush-white and ink.'],
    ["Light", "Warm key, soft fill, a strong pink rim on Cree. Night scenes lit by the ring light and the phone's glow. The reel world glows from within."],
    ["Materials", "Matte plush for Cree, frosted glass for every interface element, soft fabric and wood in the room. Gold only for the buried hook."],
    ["Camera", "35 to 50 mm, shallow depth of field, slow dollies and low tracking shots. One fast whip into the reel and one out."],
    ["People", "The creator is stylised to match Cree's world: soft proportions, simple friendly face, casual clothes, no logos."],
  ]) });

// 12 worlds and props
page({ kicker: "09 · WORLDS AND PROPS", title: 'Where it <em>happens</em>',
  body: steps([
    ["1", "<b>The bedroom-studio at night:</b> desk, ring light, plants, fairy lights, a phone on a tripod. Cosy, a little messy, believable."],
    ["2", "<b>Inside the reel:</b> a glowing timeline track (second markers every few metres) running through a valley of giant film frames that play softly."],
    ["3", "<b>Viewer-bubbles:</b> small translucent spheres that float near the track and drift away when the reel gets boring."],
    ["4", "<b>Flags:</b> frosted-glass tags with a timestamp and two or three words, e.g. 0:03 · Weak hook."],
    ["5", "<b>The buried hook:</b> one dusty frame that floods gold light when Cree wipes it."],
    ["6", "<b>Cree's magnifier:</b> clear glass lens, thin gold rim, wooden handle."],
  ]) + note("Use a generic phone and a generic reels interface. No real app interfaces, logos or brands other than Creedom's.", "warn") });

// 13 render spec
page({ kicker: "10 · RENDER SPEC", title: 'What to <em>deliver</em>',
  body: kv([
    ["Frame", "1080 x 1920 (9:16), 24 or 30 fps, 35 to 45 s."],
    ["Safe zones", "Keep faces, Cree and any text out of the top 220 px and the bottom 380 px (platform UI)."],
    ["Text", "Minimal and big. Timestamps on the flags, the wordmark, CREEDOM on the end card. Captions are added in the edit."],
    ["Files", "Master: ProRes 422 HQ or a high-bitrate MP4 (H.264, 40 Mb/s+). Plus a clean version with no on-screen text."],
    ["Sound", "Deliver picture-only; voiceover, music and sound effects are mixed in our edit (licensed music only)."],
    ["Extras", "A 3:4 cover still (Cree holding the glowing frame) and 3 to 4 stills for the carousel."],
  ]) + `<ul class="check">${["Cree on model in every shot", "Creator stays the hero", "Product moments are physical, not screens of text", "Nothing in the safe zones", "Ends on Cree + wordmark + CREEDOM"].map((c) => `<li><i></i><p>${c}</p></li>`).join("")}</ul>` });

// 14 prompt pack
page({ kicker: "11 · PROMPT PACK", title: 'If the team uses<br><em>AI image or video tools</em>',
  body: `<div class="pr"><div class="prl">STYLE (ADD TO EVERY PROMPT)</div><p>Premium stylised 3D animated short, soft rounded shapes, designer-toy materials, warm key light with a pink rim light, shallow depth of field, 35mm, vertical 9:16, Creedom palette of magenta, pink and coral with warm gold accents, cosy and cinematic.</p></div>
    <div class="pr"><div class="prl">CREE (ATTACH THE CREE REFERENCE IMAGE)</div><p>Cree, a small round egg-shaped magenta-pink mascot with no neck, big glossy black eyes with white catchlights, thin dark-pink brows, a small rounded yellow-orange beak open in a smile, short rounded wing-arms used like hands, stubby yellow-orange feet, soft matte plush texture, no feathers. Keep him exactly on model.</p></div>
    <div class="pr"><div class="prl">SHOT 6 EXAMPLE</div><p>Inside a glowing timeline track running through a valley of giant film frames, Cree wipes dust off one frame and warm gold light floods out across his face, eyes wide with surprise, frosted glass tag reading "0:34", low angle, magical.</p></div>`
    + note("Always attach Cree's reference image and check every generation against the character sheet before using it.") });

const CSS = `
@font-face { font-family: M; font-weight: 800; src: url("${A("assets/fonts/manrope-latin-800-normal.woff2")}"); }
@font-face { font-family: M; font-weight: 700; src: url("${A("assets/fonts/manrope-latin-700-normal.woff2")}"); }
@font-face { font-family: M; font-weight: 500; src: url("${A("assets/fonts/manrope-latin-500-normal.woff2")}"); }
@font-face { font-family: F; font-style: italic; src: url("${A("assets/fonts/fraunces-latin-600-italic.woff2")}"); }
@font-face { font-family: J; src: url("${A("assets/fonts/JetBrainsMono-Bold.ttf")}"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
:root { --m: 80px; --mag: #e0187e; --pink: #f343a2; --coral: #e68b70; --ink: #0b0b0b; --paper: #fff7fa; --mute: #5b4a55; }
body { font-family: M; color: var(--ink); background: var(--paper); }
.pg { position: relative; width: 1080px; height: 1350px; overflow: hidden; display: flex; flex-direction: column;
  background: radial-gradient(60% 30% at 100% 0%, rgba(243,67,162,.14), transparent 70%), radial-gradient(60% 30% at 0% 100%, rgba(230,139,112,.14), transparent 70%), var(--paper); }
header { position: relative; flex: none; padding: 70px var(--m) 30px; }
.wm { position: absolute; right: var(--m); top: 72px; height: 40px; }
.kick { display: inline-block; font-family: J; font-size: 21px; letter-spacing: .16em; color: #fff; background: var(--mag); padding: 8px 14px; border-radius: 8px; margin-bottom: 20px; }
h2 { font-weight: 800; font-size: 62px; line-height: 1.04; letter-spacing: -.03em; }
h2 em, h1 em, .csub em { font-family: F; font-style: italic; font-weight: 600; color: var(--mag); letter-spacing: -.01em; }
main { flex: 1; min-height: 0; padding: 20px var(--m) 20px; display: flex; flex-direction: column; gap: 26px; overflow: hidden; }
footer { flex: none; margin: 0 var(--m); padding: 20px 0 32px; border-top: 1.5px solid rgba(11,11,11,.12); display: flex; justify-content: space-between;
  font-family: J; font-size: 17px; letter-spacing: .14em; color: rgba(11,11,11,.45); }
.bd { flex: none; min-width: 52px; height: 52px; padding: 0 12px; border-radius: 14px; display: inline-flex; align-items: center; justify-content: center; font-weight: 800; font-size: 25px; color: #fff;
  background: linear-gradient(135deg, var(--pink), var(--coral)); }
.steps { list-style: none; display: flex; flex-direction: column; gap: 24px; }
.steps li { display: grid; grid-template-columns: 52px 1fr; column-gap: 24px; align-items: start; }
.steps p { font-size: 29px; line-height: 1.34; font-weight: 500; color: #2a1f26; padding-top: 6px; }
b { font-weight: 800; color: var(--ink); }
.note { padding: 22px 26px; border-radius: 18px; font-size: 25px; line-height: 1.38; color: #3a2b34; background: rgba(243,67,162,.08); border-left: 6px solid var(--pink); }
.note.warn { background: rgba(230,139,112,.12); border-left-color: var(--coral); }
.kv { display: grid; grid-template-columns: 210px 1fr; gap: 18px 26px; align-items: start; }
.kv .k { font-family: J; font-size: 20px; letter-spacing: .1em; color: var(--mag); padding-top: 7px; text-transform: uppercase; }
.kv .v { font-size: 27px; line-height: 1.36; font-weight: 500; color: #2a1f26; }
.sw { display: inline-block; width: 34px; height: 34px; border-radius: 9px; vertical-align: middle; margin-right: 6px; border: 2px solid rgba(11,11,11,.1); }
.cons { display: flex; flex-direction: column; gap: 14px; }
.con { padding: 18px 24px; border-radius: 22px; background: #fff; border: 2px solid rgba(11,11,11,.08); }
.con.rec { border-color: var(--pink); box-shadow: 0 16px 40px rgba(243,67,162,.18); }
.ch { display: flex; align-items: center; gap: 18px; margin-bottom: 10px; }
.ch b { font-size: 34px; letter-spacing: -.02em; }
.ch i { margin-left: auto; font-style: normal; font-family: J; font-size: 17px; letter-spacing: .14em; color: #fff; background: var(--mag); padding: 6px 12px; border-radius: 8px; }
.con p { font-size: 24px; line-height: 1.38; color: #3a2b34; font-weight: 500; }
.vo { display: flex; flex-direction: column; gap: 14px; }
.vl { display: grid; grid-template-columns: 96px 1fr; gap: 20px; align-items: baseline; padding: 14px 0; border-bottom: 1.5px solid rgba(11,11,11,.08); }
.vl span { font-family: J; font-size: 22px; color: var(--mag); }
.vl p { font-size: 30px; line-height: 1.3; font-weight: 700; }
.shots { display: flex; flex-direction: column; gap: 12px; }
.shot { padding: 16px 22px; border-radius: 20px; background: #fff; border: 2px solid rgba(11,11,11,.07); }
.sh1 { display: flex; align-items: center; gap: 16px; margin-bottom: 7px; }
.sh1 em { font-style: normal; font-family: J; font-size: 21px; color: var(--mag); }
.shot p { font-size: 21px; line-height: 1.3; font-weight: 500; color: #2a1f26; }
.shot q { display: block; margin-top: 5px; font-family: F; font-style: italic; font-size: 23px; color: var(--mute); quotes: none; }
.poses { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
figure { background: #fff; border-radius: 20px; border: 2px solid rgba(11,11,11,.07); padding: 10px 10px 12px; text-align: center; }
figure img { width: 100%; height: 190px; object-fit: contain; }
figcaption { font-family: J; font-size: 18px; letter-spacing: .1em; color: var(--mag); text-transform: uppercase; }
.dd { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
.dd > div { padding: 24px 26px; border-radius: 20px; }
.do { background: rgba(47,191,113,.1); border: 2px solid rgba(47,191,113,.45); }
.dont { background: rgba(230,60,90,.08); border: 2px solid rgba(230,60,90,.4); }
.dd b { font-family: J; font-size: 22px; letter-spacing: .14em; }
.dd ul { margin: 12px 0 0 26px; } .dd li { font-size: 25px; line-height: 1.36; margin: 6px 0; font-weight: 500; color: #2a1f26; }
.check { list-style: none; } .check li { display: grid; grid-template-columns: 38px 1fr; gap: 20px; align-items: center; padding: 12px 0; border-bottom: 1.5px solid rgba(11,11,11,.08); }
.check i { width: 38px; height: 38px; border-radius: 10px; border: 3px solid var(--pink); } .check p { font-size: 26px; font-weight: 700; }
.pr { padding: 22px 26px; border-radius: 18px; background: #fff; border: 2px dashed rgba(224,24,126,.45); }
.prl { font-family: J; font-size: 18px; letter-spacing: .14em; color: var(--mag); margin-bottom: 10px; }
.pr p { font-family: J; font-size: 21px; line-height: 1.5; color: #2a1f26; }
.cover { background: var(--paper); }
.cglow { position: absolute; inset: 0; background: radial-gradient(55% 35% at 50% 58%, rgba(243,67,162,.35), transparent 70%), radial-gradient(60% 30% at 100% 0%, rgba(230,139,112,.25), transparent 70%); }
.cwrap { position: relative; height: 100%; padding: 90px var(--m); display: flex; flex-direction: column; align-items: center; justify-content: space-between; text-align: center; }
.cwm { height: 74px; }
.ckick { font-family: J; font-size: 20px; letter-spacing: .14em; color: #fff; background: var(--mag); padding: 9px 16px; border-radius: 8px; }
h1 { font-weight: 800; font-size: 108px; line-height: 1; letter-spacing: -.04em; }
.chero { width: 470px; height: 470px; object-fit: contain; filter: drop-shadow(0 30px 50px rgba(224,24,126,.35)); }
.csub { font-size: 38px; font-weight: 700; line-height: 1.25; max-width: 860px; }
.cpills { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; }
.cpills span { padding: 9px 16px; border-radius: 999px; font-family: J; font-size: 19px; letter-spacing: .08em; border: 2px solid var(--pink); color: var(--mag); background: #fff; }
`;

(async () => {
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>${CSS}</style></head><body>${PAGES.join("")}</body></html>`;
  const f = path.join(ROOT, "cache", "guide.html");
  fs.mkdirSync(path.dirname(f), { recursive: true });
  fs.writeFileSync(f, html);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });
  await p.goto("file://" + f);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(500);
  const over = await p.evaluate(() => [...document.querySelectorAll(".pg main")].map((m, i) => (m.scrollHeight > m.clientHeight + 1 ? i + 2 : 0)).filter(Boolean));
  if (over.length) console.log("WARNING overflow on pages", over.join(", "));
  const d = path.join(ROOT, "cache", "guide");
  fs.rmSync(d, { recursive: true, force: true });
  fs.mkdirSync(d, { recursive: true });
  const els = await p.$$(".pg");
  const imgs = [];
  for (let i = 0; i < els.length; i++) {
    const o = path.join(d, `page-${String(i + 1).padStart(2, "0")}.jpg`);
    await els[i].screenshot({ path: o, type: "jpeg", quality: 90 });
    imgs.push(o);
  }
  const ih = path.join(ROOT, "cache", "guide_img.html");
  fs.writeFileSync(ih, `<!doctype html><html><head><style>@page { size: 1080px 1350px; margin: 0; } * { margin: 0; padding: 0; }
    img { display: block; width: 1080px; height: 1350px; page-break-after: always; }</style></head><body>${imgs.map((x) => `<img src="file://${x}">`).join("")}</body></html>`);
  const p3 = await b.newPage();
  await p3.goto("file://" + ih);
  await p3.waitForTimeout(300);
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  await p3.pdf({ path: OUT, width: "1080px", height: "1350px", printBackground: true });
  await b.close();
  console.log("wrote", OUT, PAGES.length, "pages");
})();
