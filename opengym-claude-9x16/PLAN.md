# openGym × Claude: 3D reel plan (draft for approval)

For @ai.nxtlvl. Built on Rishabh's brief (`nxtlvl_opengym-claude_reel_BRIEF.md`), with the script rebuilt on the
modern story arc, a stronger hook, a "muscle mode" AI character, and facts updated to openGym v1.4.2 (23 Oct 2026).

---

## 1. Facts check: what changed since the brief was written

openGym shipped v1.4.0 (9 Oct) and v1.4.2 (23 Oct). Four lines in the brief are now wrong and would get
corrected in the comments:

| Brief says | The repo says today (README + CHANGELOG, `main`) | Script now says |
|---|---|---|
| 1,324 exercises | "**5,632 exercises instead of 1,324**" (v1.4.0) | "over fifty-six hundred exercises" |
| iPhone needs self-hosted setup | v1.4.2: "openGym comes to the **App Store**, with an Apple Watch app"; "in every App Store country" | "iPhone's on the App Store" |
| Deliberately not on the Play Store | "**A Google Play version is on its way**"; Android is a signed APK from GitHub Releases or opengym.ch | "Android's on GitHub" (Play is not promised on screen) |
| Copy a ready-made prompt into Claude, paste back, no key | No such flow in the current README or docs. The AI feature is the **AI Coach**: "drafts a week of routines and later suggests changes based on what you logged. **You approve every change.**" It runs with **your own provider key** (Anthropic/Claude, OpenAI, Gemini, any OpenAI-compatible endpoint, Ollama). Off by default. On the App Store build: bring your own key, or pair with your server. | "Its AI coach plans your week. Connect Claude with your own key… and you approve every change." |
| Muscle map: trained / fatigued / detrained | "three modes: where your volume went, what is still recovering, and what has gone untrained" | "Worked. Recovering. Or… untrained." |
| Site `opengym.duarte-santos.ch` | README links `https://opengym.ch` and `https://opengym.ch/demo/` | Use opengym.ch in the DM |

Also verified and usable:
- Free and open source: AGPL-3.0, "free and stays free: no paid tier".
- No account on someone else's server, no subscription, no ads, no telemetry.
- Guided sessions: weights pre-filled from last time, rest timer, PRs detected.
- Progression rules: "missed reps never add load, stalls trigger a deload".
- Imports from FitNotes, Strong and Hevy.
- **Built with Claude Code:** "a large share of the code, tests and documentation is drafted in Claude Code sessions" (README). Usable in the caption.
- **About 16.0k GitHub stars** (repo page, 26 Oct). Re-check on posting day and round down.

Not verified, so kept out: the brief's "no key, nothing leaves the device" AI claim.

---

## 2. Story arc

| Beat | Job | What happens |
|---|---|---|
| **Hook** (0–4 s) | Pain + payoff + a visual nobody scrolls past | The human gets a paywall pop-up. The AI robot drops in and **powers up into muscle mode**. The paywall shatters against its flexed bicep. "Free… and stays free." |
| **Proof** (4–8 s) | Earn belief | 16K-star GitHub card; "no subscription · no ads · no account" chips crossed out one by one. |
| **Open loop** (8–10 s) | Stop the drop-off | "And it shows the muscles you've been skipping." A hologram body flickers, the legs flash red, and it cuts out. |
| **List** (10–30 s) | Value, one idea per step | 1 PLAN (the AI coach with Claude drafts the week) · 2 TRAIN (5,600+ demos, pre-filled weights, rest timer) · 3 PROGRESS (adds weight when you're ready). |
| **Twist / payoff** (30–36 s) | Pay off the loop, with comedy | Hero shot of the hologram muscle map: worked green, recovering amber, untrained red. "Legs, bro." "…Fair." |
| **Trust** (36–41 s) | Honesty builds comments | "What's the catch?" → official links only: Android on GitHub, iPhone on the App Store. |
| **CTA** (41–end) | Convert | "Comment GYM and I'll DM you the links and my goal prompt." End card held at least 1.5 s. |

---

## 3. Script and voiceover (Eleven v3, mood tags in brackets, about 46 s)

Two voices, as in the brief: **NXT** uses the house voice "Nota2"; the **Human** is a different casual young male voice.

```
HUMAN: [annoyed] My gym app wants me to upgrade... again.
NXT:   [confident] Delete it. I found one that's free... and stays free.
HUMAN: [skeptical] Free... free?
NXT:   [proud] openGym. Open source, sixteen thousand stars on GitHub. No subscription. No ads. No account.
NXT:   [mysterious] And it shows the muscles you've been skipping.
NXT:   [upbeat] Step one: its AI coach plans your week. Connect Claude with your own key.
HUMAN: [thinking] Four days. Build muscle. Just dumbbells.
NXT:   [upbeat] Done. And you approve every change.
NXT:   [energetic] Step two: train. Over fifty-six hundred exercises with demos. Weights pre-filled. Rest timer running.
NXT:   [confident] Step three: it adds weight when you're ready... and deloads when you stall.
HUMAN: [curious] And the muscle thing?
NXT:   [playful] Worked. Recovering. Or... untrained. [short pause] Legs, bro.
HUMAN: [laughs] ...Fair.
HUMAN: [suspicious] What's the catch?
NXT:   [serious] Just use the official links. Android's on GitHub, iPhone's on the App Store.
NXT:   [friendly] Comment GYM, and I'll DM you the links and my goal prompt.
```

About 125 words. With the skit pauses it lands at about 45–47 s. If it runs long, cut the deload half of step three first.

**Alternative hooks** (A/B later)
1. NXT, flexing: "This gym app is free forever… and Claude helped code it."
2. HUMAN: "My gym app wants a subscription." NXT: "Mine wants nothing. Not even an account."
3. NXT: "Your gym app hides your weakest muscle. This free one shows it."

**Self-rating 8.5/10.**
- **Biggest risk:** the list stretch around 14–28 s. Each step therefore gets a new 3D event every 1.5–2 s.
- **Strongest moments:** the muscle-mode hook frame and "Legs, bro".

---

## 4. The muscular AI ("make Claude muscular")

We can't turn Claude's own logo or mascot into a character. The brief forbids recreating the Claude logo, and a
buff "Claude" figure would read as Anthropic's official branding. So the page's own robot carries the
muscle gag, and Claude is named as the coach it plugs in:

**NXT, MUSCLE MODE**
- **Rest form:** the brief's glossy violet sphere with the sparkle antenna, visor face, LED eyes and orbit ring.
- **Power-up (hook, 2.0–3.2 s):**
  - the orbit ring snaps into a "power belt" around its equator;
  - the sphere's shell splits along panel seams, and two chrome-and-violet **muscular arms** extrude out (sculpted biceps and forearms, PBR clearcoat);
  - a chest plate with pec definition pushes forward;
  - the eyes go "confident";
  - a shockwave ring and dust kick off the floor.
- **Hook beat:** a double-biceps flex. The paywall card hits the bicep and shatters into violet shards. Camera punch-in and a chromatic shake.
- **During the steps:** it keeps muscle mode and curls a glowing dumbbell between lines. On "you approve every change" it gives a thumbs-up.
- **Twist:** it points at the red legs on the hologram and flexes its own (comically tiny) legs on "Legs, bro".
- **End card:** it "powers down" with a puff, back to a cute sphere, and waves.

The human stays as in the brief: a low-poly young Indian guy in an oversized grey hoodie.

---

## 5. Scene plan (3D-heavy, about 46 s)

The layout follows the brief:
- top bar at y 0–250;
- UI panel at y 260–960, with a step chip above it;
- caption band at y 980–1110;
- 3D window at y 1110–1520, with the 3D scene running full-bleed behind everything, blurred behind the panel.

**Upgrade:** on hero beats the panel **folds away into 3D**, and the scene takes the whole frame for 1–3 s. The 3D isn't trapped in a strip.

| # | ≈Time | Line | 3D scene (full-bleed on hero beats) | Panel | SFX |
|---|---|---|---|---|---|
| 1 | 0.0–2.0 | Human: upgrade again | First frame: the human slumped on the bench. The phone buzzes and a red 3D **"UPGRADE TO PRO"** card bursts out with 3 padlocks spinning. Camera pushes in. | Fictional paywall "FitPro Premium" (no real brand). | buzz, error ding |
| 2 | 2.0–4.2 | NXT: Delete it… stays free | **HERO:** NXT slams down, powers up, and flexes. The card shatters on its bicep into violet shards; slow-mo, then speed ramp. Panel folds away. | Panel folds into 3D shards | slam, power-up riser, glass burst, bass hit |
| 3 | 4.2–5.0 | Human: Free… free? | Whip-pan punch-in on the human's raised eyebrow. | — | record-scratch blip |
| 4 | 5.0–8.5 | openGym, 16K stars… | NXT projects a 3D hologram **GitHub repo card** that spins in; a ★ counter rolls to 16K. Three 3D chips ("subscription", "ads", "account") get stamped ✗ and fall. | Repo card `github.com/DuarteSantos8/openGym` | counter roll, 3 stamp-x |
| 5 | 8.5–10.5 | Open loop | A hologram body flickers on, the legs flash red, a glitch, and it's gone. | Panel dims to "?" | glitch, low hum |
| 6 | 10.5–14.0 | Step 1: AI coach, Claude key | STEP 1/3. A violet "coach" orb wires into a 3D key card (generic key icon, no logos) labelled "your Claude key". The human's goal floats up as 3 chips: 4 DAYS · MUSCLE · DUMBBELLS. | **STEP 1/3 · PLAN**: recording of the AI Coach (provider chip + "draft my week") | key click, chips pop |
| 7 | 14.0–16.5 | Human goal / "Done. You approve" | **HERO:** 4 glowing routine cards (MON · TUE · THU · FRI) fly out and slot into a floating 3D week calendar. NXT stamps ✓ APPROVED. | Routines appear | 4 slot pops, approve stamp |
| 8 | 16.5–22.0 | Step 2: train | STEP 2/3. The human curls dumbbells on the beat; a 3D rest-timer ring counts down above him; a counter flips to "5,600+"; a weight plate reads "last time: 12.5 kg ✓ pre-filled". | **STEP 2/3 · TRAIN**: guided workout + exercise demo (from the live demo) | rep thuds, timer tick, flip |
| 9 | 22.0–26.0 | Step 3: progression | STEP 3/3. A 3D bar chart climbs. On "ready" a plate slides onto the bar (+2.5 kg). On "stall" the bar dips into a soft "DELOAD" step. | **STEP 3/3 · PROGRESS**: the progression target screen | plate clank, down-tone |
| 10 | 26.0–27.5 | Human: muscle thing? | The human turns to NXT. Camera arcs. | — | whoosh |
| 11 | 27.5–31.5 | Worked · Recovering · Untrained · Legs, bro | **HERO, full-bleed:** a big hologram body with the camera orbiting 120°. Chest and arms fill green on "Worked", shoulders amber on "Recovering", legs pulse red on "untrained". On "Legs, bro", NXT points, then flexes tiny legs. | Real muscle-map screen | 3 rising tones, boing |
| 12 | 31.5–32.5 | Human: Fair | The human looks at his legs and shrugs. | — | laugh sting |
| 13 | 32.5–33.5 | Human: the catch? | The lights shift amber and the music filters down. | — | filter sweep |
| 14 | 33.5–38.0 | NXT: official links | NXT holds a 3D amber caution sign. The cards "fake mirror ✗" → "GitHub Releases ✓ Android" → "App Store ✓ iPhone" (text only, no store logos). | Link cards | caution beep, verified ding |
| 15 | 38.0–end | CTA | Wide two-shot. NXT powers down with a puff and waves. Violet sparkle burst. End card held at least 1.5 s: "Comment **GYM** for the links + my goal prompt" · "Send this to your gym buddy who still pays for an app" · @ai.nxtlvl | End card | chime, button ending |

Retention rule: a new 3D event every 1.5–2.5 s, always with a slow camera drift and never a static frame.

---

## 6. How it gets built (3D pipeline)

- **Engine:** Three.js inside HyperFrames (one paused GSAP timeline drives the camera, characters and FX; no real-time clocks). Rendered frame by frame, so it is fully seekable and deterministic.
- **Look:**
  - PBR materials (clearcoat violet shell, brushed chrome muscles);
  - a RoomEnvironment HDR;
  - warm key light #FFB46B from the left, violet rim light #7B2FFB from behind;
  - post-processing: bloom on the neon and holograms, depth of field on the background, a light haze, film grain.
  - Palette and fonts exactly as in the brief.
- **Characters:**
  - NXT and its muscle mode are modelled procedurally in code (sphere shell, lathed and sculpted arm meshes, morph-like scaling), so no external model is needed.
  - The human: a CC0 rigged character (Quaternius or Kenney) recoloured, if the asset download works from this machine. Otherwise a stylized character built in code with the same poses (idle, sigh, talk, curl, count, look down).
- **Set:** the Delhi night apartment-gym from the brief (bench, dumbbells, mat, mirror, plant, window with bokeh city lights, violet neon sparkle sign).
- **Holograms:** the muscle body is a stylized anatomical mesh with per-group emissive colour (chest, arms, shoulders, legs), plus scan-line and fresnel shaders.
- **Panel and captions:** HTML on top. Captions follow the brief (Lora Italic 64 px, gold #FFE7A8, active word white with a violet underline, speaker dot). The brief asks for a soft drop-shadow; I'll keep it subtle, or drop it if you prefer, as on Sucsess Maperrs.
- **Audio:**
  - two ElevenLabs v3 voice takes;
  - transcribed to word timestamps, with every scene snapped to its first word;
  - an original synthesized gym track at 120 bpm, ducked under speech, dipping at the catch, with a button ending;
  - SFX per scene;
  - mastered to −14 LUFS, −1.5 dBTP.
- **Render time:** 3D at 1080×1920 on this machine's software GPU is slow. Expect roughly 2–4 hours per full render at 30 fps (the brief's spec). I'll iterate on stills and short preview clips and render the full reel only once the preview is approved.

---

## 7. What I need from you

1. **Approve the script** (or edit lines). It is the source for both voiceovers.
2. **Voices:** OK to generate both takes on ElevenLabs (spends credits)? I'll look up "Nota2" in your workspace for NXT and pick a casual young male voice for the human, unless you name one.
3. **Screen recordings** (any you can, 1080 px wide or more), updated for v1.4:
   - **R1:** guided workout from the live demo, https://opengym.ch/demo/
   - **R2:** AI Coach screen (Settings → AI Coach: Claude provider chip, "draft my week")
   - **R3:** coach-drafted routines appearing and being approved
   - **R4:** progression target screen
   - **R5:** muscle map in its three modes

   Anything missing I'll mock in the same layout and mark MOCK, so it can be swapped in later.
4. Post copy: update the DM to the opengym.ch links. The GitHub links are unchanged.
