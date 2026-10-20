---
format: 1920x1080
duration: 30s
message: "Your entire creative team, from $5 a month"
arc: Feature-Benefit Cascade — hook → promise → what lands (cascade) → scale → price payoff → CTA
audience: Owners of cafés, salons, gyms and shops who need a feed but not an agency
mode: collaborative
music: none
tempo: 120 bpm · 4/4 · 1 beat = 0.5 s · 1 bar = 2 s · cuts land on bar lines
---

<!-- Music is an original track composed in code for this video (host BGM, assets/music/nxtlvl-theme.wav,
     beat grid in assets/music/beatgrid.json). SFX are bundled-library files placed by hand on the beat grid
     as host audio, so frames carry `sound:` notes rather than `sfx:` lookups. No narration: every message is
     on screen. -->

## Video direction

- **palette system** — `frame.md` roles: ink ground `bg` with violet light (`primary`, `primary-lift`, `primary-deep` glows);
  display type `text`; one serif emphasis per line in `primary-lift`; pills in tinted `card-bg` + `border`; the one solid
  element is the violet CTA. The posts inside the phone carry their own colours — they are the client work and the only
  off-palette colour in the film, always inside a phone.
- **shared kit** — every frame links `assets/css/kit.css` and builds the ground (`nx-ground`), the phone (`nx-phone`,
  380×780 at scale 1, placed at left 770 / top 80 when centred), the posts (`nx-post nx-p-*`), pills (`nx-pill`) and
  toasts (`nx-toast`) from its classes, copying the markup in the confirmed sketch file. Never redraw them, so every cut
  matches pixel for pixel.
- **reveal model (no narration)** — reveals are paced to the music, not a voice: each piece lands on its beat from
  `assets/music/beatgrid.json` (120 BPM, beat 0.5 s, bars on even seconds). Never front-load; something lands on
  most beats through frames 2–3.
- **motion grammar** — long-tail settles (`power3`; `expo.out` on fast arrivals); smooth, never bouncy. Kinetic type
  slams on the downbeat. Post landings are the signature: a quick scale-pop with a white flash that fades.
- **rhythm** — F1 sparse tension (two slams, one held line, a push into the drop); F2–F3 maximum density (a landing
  every beat); F4 the film's one big camera move; F5 a single hit then a held breather; F6 a calm held close.
- **aliveness during holds** — subtle jitter only. The ground stays still.
- **negative list** — no bounce or elastic overshoot; no lazy breathing; no slow back-half pans or pushes except F1's
  push into the drop and F4's designed pull-back; no screensaver floating; no exits on frames 1–5; no `Math.random`,
  CSS transitions or `@keyframes`; no emoji; no real platform logos (generic profile UI only).

## Frame 1 — Still 0 posts?

- scene: A phone shows an empty Instagram profile, "0 posts"; big type either side asks the question
- duration: 4s
- poster: 2.6s
- transition_in: cut
- status: animated
- src: compositions/frames/01-zero-posts.html
- type: hook
- persuasion: Pain validation
- beat: recognition + mild guilt
- blueprint: kinetic-type-beats
- adapt: keep the beat-slammed statement building to a payoff; the payoff is the empty phone itself
- focal: the phone (empty profile, built from the kit)
- roles: phone = hero, centred · "Still" / "0 posts?" = flanking display type · busy line = supporting · assets/nxtlvl-spark.svg = a faint glint top-right of the phone (supporting)
- handoff_out: phone — left 770, top 80, scale 1, opacity 1, static · stage camera (wrapper of phone + type) — scale 1.08 about the phone centre (960, 470), still accelerating inward at the cut
- onscreen: "Still" (0.0) · "0 posts?" (0.5) · "You're busy running the place." (2.0)
- sound: soft notification ping at 0.5 on "0 posts?"; riser 2.5→4.0 into the drop
- music: intro — filtered pad, ticking hats, muted pluck; tension builds into bar 3
- asset_candidates: assets/nxtlvl-spark.svg — four-point star, appears only as a faint glint here

narrativeRole: Open on the viewer's own situation — a business with an empty feed — in the first frame, no logo.
keyMessage: Your feed is empty because you're busy, not because you don't care.

Scene 1 (0.0–0.5s): the phone is already on screen at t=0 (empty profile, "0" posts), settling up from slightly lower on a long-tail ease; "Still" slams in on the downbeat left of the phone, right-aligned to it (`kinetic-beat-slam`). Centred hero, flanking type, three depth layers (ground, phone, type).
Scene 2 (0.5–2.0s): on beat 2 "0 posts?" slams in right of the phone; its "0" lights with a keyword glow (attack-decay glow + slight scale) and the phone's own "0" posts stat glows with it.
Scene 3 (2.0–3.0s): "You're busy running the place." reveals word by word under "0 posts?" in the serif (staggered word fade-up).
Scene 4 (2.5–4.0s): with the riser, the stage pushes in toward the phone, accelerating into the cut to scale 1.08 (camera push, accelerating ease-in) — the build into the drop. The type holds.

## Frame 2 — Meet your entire creative team

- scene: The drop hits; the grid fills tile by tile on every beat with real-looking posts while the promise lands beside the phone
- duration: 6s
- poster: 5s
- transition_in: cut
- status: built
- src: compositions/frames/02-meet-the-team.html
- type: product_intro
- persuasion: Show-don't-tell proof
- beat: relief + delight
- blueprint: grid-card-assemble
- adapt: keep cards landing into a grid one beat at a time; the grid is the phone's feed and every card is a finished post
- focal: the phone feed filling
- roles: phone = hero · posts = the landing cards · "Meet your entire" / "creative team." = flanking type · pills = supporting · assets/nxtlvl-wordmark.png = supporting sign-off ("by nxtlvl ✦")
- handoff_in: stage camera — scale 1.08 about (960, 470) at t=0, snapping to 1.0 by 0.25 s on `expo.out` (the drop) · phone — left 770, top 80, opacity 1, empty profile at t=0
- handoff_out: phone — left 770, top 80, scale 1, opacity 1, static · feed offset 0 · grid = 9 posts in order latte, diwali, menu, salon, offer, review, thali, navratri, hours, then 3 empty slots · posts stat "9"
- onscreen: "Meet your entire" (4.0) · "creative team." (5.0, serif accent) · "Design · Video · Posting · Automation" (8.0)
- sound: bass impact on the drop at 4.0; a soft pop on each tile slam (every beat 4.0–8.0); whoosh-short under each line
- music: drop A — four-on-the-floor kick, sub bass, clap on 2 and 4, bright pluck arpeggio; tiles land on the kicks
- asset_candidates: assets/nxtlvl-wordmark.png — appears small under the promise at 8.0

narrativeRole: State the value claim (the message) by beat 2 while the feed visibly fills — the proof arrives with the claim.
keyMessage: One studio becomes your whole creative team.

Scene 1 (0.0–0.25s): the drop — the stage snaps back from the push; the empty-state message clears on the beat as the first post (latte reel) slams into slot 1 with a scale-pop and a white flash that fades (`spring-pop-entrance`, smooth settle).
Scene 2 (0.0–4.0s): one post lands per beat — 0.0, 0.5 … 4.0, nine posts in reading order — each with the pop and flash; the posts stat ticks with each landing, quietly. "Meet your" slams in left on 0.0 and "entire" on 0.5 (`kinetic-beat-slam`); "creative" on 1.0 and "team." on 1.5 in the serif with a soft glow bloom (staggered word reveal + a text-shadow glow that blooms then settles).
Scene 3 (4.0–5.0s): the four pills pop in one per half-beat (4.0, 4.25, 4.5, 4.75) under "Meet your entire", right-aligned (`spring-pop-entrance`, staggered by index).
Scene 4 (5.0–6.0s): "by nxtlvl ✦" reveals under "creative team."; the spark twinkles once. Hold — subtle jitter only.

## Frame 3 — What lands in your feed

- scene: The phone feed keeps filling and scrolling; a fixed line holds while the thing being made swaps on the beat; "Posted" toasts pop in the phone
- duration: 8s
- poster: 3s
- transition_in: cut
- status: built
- src: compositions/frames/03-what-lands.html
- type: feature_showcase
- persuasion: Value stacking
- beat: momentum + ease
- blueprint: fixed-anchor-cycle
- adapt: keep the static lead with a carousel slot; the slot swaps by hard cut on the beat, and the phone shows each named thing as it is said
- focal: the phone feed
- roles: phone = hero · "We make" = static anchor · swap slot = the moving word · toasts = supporting
- handoff_in: phone — left 770, top 80, scale 1, opacity 1, static · feed offset 0 · grid = the 9 posts and 3 empty slots exactly as frame 2 ended
- handoff_out: phone — left 770, top 80, scale 1, opacity 1, static · feed scrolled up 170 px · grid = 15 posts: latte, diwali, menu, salon, offer, review, thali, navratri, hours, gym, drop, bake, latte, diwali, salon · no toast showing
- onscreen: lead "We make" (static) · swaps each second: "the reels." "the posters." "the carousels." "the menus." "the festival drops." "the captions." "the ads." · last bar: "We post it too." (16.0)
- sound: whoosh-short on every word swap (on the beat); click-soft + notification on each "Posted · 6 PM" toast (12.0, 14.0, 16.0)
- music: groove B — adds chord stabs and 16th hats; the swaps ride the stabs
- asset_candidates:

narrativeRole: Evidence for the claim — the breadth of what the studio makes, each named on the beat as it appears in the feed.
keyMessage: Reels, posters, carousels, menus, festival drops, captions, ads — and the posting is handled.

Scene 1 (0.0–4.0s): "We make" holds left of the phone from t=0. The slot on the right swaps on each bar beat by hard-cut in-place token swap (`discrete-text-sequence`): "the reels." 0.0 · "the posters." 1.0 · "the carousels." 2.0 · "the menus." 3.0. At each swap the matching post in the phone lights — a violet ring and a slight lift (`asr-keyword-glow` on the tile): reels → latte, posters → diwali, carousels → salon, menus → menu. Toast 1 "Posted · Diwali poster · Tue 6 PM" slides up inside the phone at 2.0.
Scene 2 (4.0–6.0s): "the festival drops." 4.0 (may wrap to two lines) · "the captions." 5.0 · "the ads." 5.5. New posts land in slots 10–12 on 4.0, 4.5 and 5.0 with the pop and flash while the feed scrolls up smoothly inside the phone to show them (`viewport-change` on the feed); highlights: festival → navratri, captions → review, ads → offer. Toast 2 "Posted · Navratri reel · Thu 7 PM" at 4.0 replaces toast 1.
Scene 3 (6.0–8.0s): last bar — "We make" hard-cuts to "We post" and the slot to "it too." in the serif; posts 13–15 land at 6.0, 6.5 and 7.0; toast 3 "Posted · Weekend offer · Sat 11 AM" at 6.0, cleared by 7.5. Hold 7.0–8.0, subtle jitter only.

## Frame 4 — For every kind of business

- scene: One continuous pull-back: the phone shrinks into a wall of phones — a café, salon, gym, boutique, bakery, clinic and studio — every feed filling at once
- duration: 6s
- poster: 4s
- transition_in: cut
- status: built
- src: compositions/frames/04-every-business.html
- type: benefit_highlight
- persuasion: Belonging / social fit
- beat: scale + aspiration
- blueprint: zoom-out-workspace-reveal
- adapt: keep the ONE continuous decelerating pull-back from a tight detail (the café phone, full size) to the whole (seven businesses' phones); element-level payoff carries on after the lock
- focal: the wall of phones
- roles: café phone = the continuing hero (slot 4, centre) · six other phones = the revealed world · label pills = the business types · headline = payoff
- handoff_in: café phone — left 770, top 80, scale 1, opacity 1, feed scrolled up 170 px, 15 posts exactly as frame 3 ended, no toast · ground identical
- onscreen-adapt: the confirmed sketch carries the business types as label pills under each phone (Salon · Gym · Boutique · Café · Bakery · Clinic · Studio) rather than big words; the pills are the cues
- onscreen: "Cafés." (18.0) · "Salons." (18.5) · "Gyms." (19.0) · "Shops." (19.5) · "Built for the businesses" (20.0) · "agencies won't call back." (21.0, serif accent)
- sound: whoosh-cinematic on the pull-back at 18.0; riser 22.0→24.0 with the snare roll
- music: lift — pads open, filter sweeps up, snare roll in the last bar into the hit at 24.0
- asset_candidates:

narrativeRole: Widen the frame from one business to many — the viewer sees their own kind of shop in the wall.
keyMessage: This is built for businesses like mine.

Scene 1 (0.0–1.8s): one continuous decelerating pull-back on a world wrapper (`viewport-change`, a pull-back): the world starts scaled so the café phone fills its frame-3 position, and eases out until the café phone sits in slot 4 at 0.6 scale with the six neighbours revealed on both sides; a light directional blur on the fastest part, settling on `expo.out`. Seven phones in one row across the top two-thirds; layered depth (ground, phones, labels).
Scene 2 (0.5–3.5s): the label pills light one per beat left to right (0.5 … 3.5), each with a small pop, and at the same instant that phone gets one new post landing (pop + flash) — a wave across the wall.
Scene 3 (2.0–3.5s): under the wall, "Built for the businesses" reveals word by word at 2.0 (`dynamic-content-sequencing`); "agencies won't call back." lands in the serif at 3.0 with a hand-drawn underline drawing in beneath it (`svg-path-draw`).
Scene 4 (3.5–6.0s): hold the wall and headline still while the music builds; subtle jitter only, no push.

## Frame 5 — From $5 a month

- scene: The wall dims and blurs back; the price lands huge in violet light; the reassurance line settles under it
- duration: 3s
- poster: 1.5s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/05-five-dollars.html
- type: benefit_highlight
- persuasion: Price anchoring + risk reversal
- beat: surprise → confidence
- blueprint: kinetic-type-beats
- adapt: keep the statement landing onto a spring-pop payoff; the payoff is the price
- focal: "$5"
- roles: "$5" = hero, centred, huge · "from" / "a month." = flanking serif · "Your entire creative team," = lead line above · terms pills = supporting · blurred wall = background (dim)
- onscreen: "Your entire creative team," (24.0) · "from $5 a month." (24.0, $5 spring-pops on the hit) · "No contracts · Cancel any month · You own every file" (25.0)
- sound: impact-bass on the price at 24.0; sparkle as the $5 settles
- music: the payoff hit at 24.0, then half-time — kick drops out, pad and sub hold
- asset_candidates:

narrativeRole: The payoff — the price lands after the viewer has seen everything it buys.
keyMessage: All of that, from $5 a month, no lock-in.

Scene 1 (0.0–0.6s): on the hit "$5" lands huge with the spring-pop entrance (one smooth settle — the film's one sanctioned payoff slam) and a glow blooms behind it (`spring-pop-entrance` + a glow bloom behind); "Your entire creative team," settles down into place above it; "from" and "a month." slide in toward the "$5" from either side at 0.1. Centred hero ~45% of the frame over a dimmed, blurred wall (background).
Scene 2 (1.0–1.6s): the three terms pills pop in on 1.0, 1.25 and 1.5 below (`spring-pop-entrance`, staggered by index).
Scene 3 (1.6–3.0s): hold still — the breather before the close.

## Frame 6 — Book a free call

- scene: The Nxtlvl spark ignites and the wordmark assembles; a "Book a free call" pill presses in; held calm to the end
- duration: 3s
- poster: 2s
- transition_in: crossfade
- status: built
- src: compositions/frames/06-book-a-call.html
- type: cta
- persuasion: Friction reduction
- beat: confidence + invitation
- blueprint: logo-assemble-lockup
- adapt: keep the brand sting: the mark ignites, the wordmark assembles around it, then the call to action
- focal: assets/nxtlvl-wordmark.png
- roles: assets/nxtlvl-wordmark.png = hero, centred · assets/nxtlvl-spark.svg = the igniting mark top-right of the wordmark · rings = closing atmosphere · CTA pill = the one solid element
- onscreen: wordmark "nxtlvl" + spark (27.0) · pill "Book a free call →" (27.5) — held ≥ 2 s (no web address: the user chose button only)
- sound: chime as the spark ignites at 27.0; click-soft as the pill presses in at 27.5
- music: outro — final chord rings out, tail fades to silence at 30.0
- asset_candidates: assets/nxtlvl-wordmark.png — the logo lockup; assets/nxtlvl-spark.svg — the spark that ignites

narrativeRole: One clear next step, held long enough to act on.
keyMessage: Book a free call.

Scene 1 (0.0–0.6s): the spark ignites at its spot top-right of the wordmark — grows from nothing with a quarter turn and a glow flash (`spring-pop-entrance`, smooth) — and the concentric rings expand outward from the logo centre and settle (rings scale out from the centre, staggered by index).
Scene 2 (0.1–0.9s): the wordmark assembles left to right through a soft mask wipe, blur to sharp.
Scene 3 (0.5–1.0s): the "Book a free call →" pill rises into place, then gives one tactile press (`press-release-spring`) with a soft glow.
Scene 4 (1.0–3.0s): hold the lockup still (a ≥ 2 s read); subtle jitter on the spark only. Final 0.4 s: everything fades to the ink ground with the music's tail (the final frame's exit).
