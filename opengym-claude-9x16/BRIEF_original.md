# BRIEF — "Claude wrote my gym plan" (openGym + Claude) · Nxtlvl Social

You are building a 3D-rendered Instagram Reel for the page **@ai.nxtlvl** (Nxtlvl Social, Delhi).
Read this whole brief before writing any code. Do not invent facts, numbers, logos or UI that are not listed here.

---

## 1. Deliverable

| Spec | Value |
|---|---|
| Format | 9:16 vertical, **1080×1920**, **30 fps**, H.264 MP4 + AAC 48 kHz |
| Length | ~45–47 s (final length = voiceover length + 1.5 s end-card hold) |
| File name | `nxtlvl_opengym-claude_reels_9x16_v1.mp4` + `..._cover.png` |
| Stack | Three.js scene rendered deterministically frame-by-frame (seekable timeline, no real-time clocks), composited with the UI panel + captions. HyperFrames or a headless-Chromium frame renderer + ffmpeg are both fine. |
| Safe zones | Keep all text out of the **top 250 px** and **bottom 400 px**, and 60 px from each side. |
| Loudness | Final mix −14 LUFS integrated, true peak −1.5 dBTP. |

---

## 2. Format (structure copied from our reference video, look is our own)

Two-character skit: a **human** (the viewer's stand-in) and our **AI robot** talk at a desk/home-gym corner, while a **UI panel** on the top half demonstrates each step.

```
y 0–250      top bar: "● AI.NXTLVL" (left) + thin progress bar (right)
y 260–960    UI PANEL — rounded card (radius 36), shows screens / mock UI for the current step
             + step chip above it: "STEP 1/3 · PROMPT" etc.
y 980–1110   CAPTION BAND — current spoken line, one short phrase at a time
y 1110–1520  3D SCENE window (characters, props, holograms) — scene also continues
             behind the panel as a softly blurred background
y 1520–1920  keep clear (Instagram UI)
```
The 3D scene fills the full frame as the background; the panel and captions float above it.

### Characters (original designs — do NOT copy the orange robot from the reference)
- **NXT (the robot):** a glossy **violet** sphere (#7B2FFB → #4A0FC2 gradient material), a 4-point **sparkle antenna** (the nxtlvl logo sparkle, #A98BFF emissive), a black visor face with LED eyes made of rounded pixels. A thin orbit ring circles it slowly. It floats and bobs (amplitude 0.04 units, 1.6 s period). Eye expressions map to the voiceover mood tags: calm = soft ovals, confident = flat-top ovals, playful = ^ ^, serious = narrow slits, mysterious = one eye half-closed, friendly = smile curves.
- **The human:** stylized low-poly young Indian guy (~22), oversized grey hoodie, track pants, sneakers, short black hair. Use a CC0 rigged character (e.g. Quaternius or Kenney) recoloured, or build a simple stylized one. Needs idle, sigh, talk (head bob + hand gesture), dumbbell curl loop, counting-on-fingers, looking down at legs.

### Set
A cosy Delhi apartment corner at night turned home gym: a flat bench, a pair of dumbbells on a rubber mat, a mirror, a plant, a window with soft-blurred city lights, and a small **violet neon sparkle sign** on the wall. Warm key light (#FFB46B, from the left), violet rim light (#7B2FFB) from behind, gentle volumetric haze. Slow camera drift at all times; never a fully static frame.

### Brand palette
Black #07050D · violet #7B2FFB · light violet #A98BFF · lilac #D9CCFF · white #F4F1FA · muscle states: trained **#3FD69B**, tired **#FFC24A**, skipped **#FF6B6B**.
Fonts: **Poppins Bold** for UI/headlines, **Lora Italic** for captions, **DejaVu Sans Mono** (or JetBrains Mono) for code/labels.

### Captions
Lora Italic, 64 px, colour #FFE7A8 (warm gold, like the reference), soft dark drop-shadow for legibility. Show 2–4 words at a time; the currently spoken word turns white with a violet underline. Human lines and robot lines can have a tiny speaker dot (grey for human, violet for NXT).

---

## 3. Voiceover

Two separate ElevenLabs takes (Eleven v3, mood tags in brackets):
- **NXT (robot): voice "Nota2"** — the page's house voice.
- **Human:** a different young male voice, casual.

Retiming rule: when the final audio arrives, **transcribe it to word-level timestamps** and snap every scene start to the first word of its line. The times in section 4 are estimates only.

```
HUMAN: [annoyed] My gym app just asked me to upgrade... again.
NXT: [calm] Delete it. I'll write your plan. A free app tracks it.
HUMAN: [skeptical] Free free?
NXT: [confident] openGym. Open source, on GitHub. No subscription. No ads. No account.
NXT: [mysterious] And it shows the muscles you've been skipping.
NXT: [upbeat] Step one: copy openGym's ready-made prompt into Claude, with your goal.
HUMAN: [thinking] Four days a week. Build muscle. Just dumbbells.
NXT: [upbeat] Step two: paste my answer back. Your whole week imports.
NXT: [energetic] Step three: train. Over thirteen hundred exercises, with demos. Rest timer. Weights pre-filled.
HUMAN: [curious] And the muscle thing?
NXT: [playful] Trained. Tired. Or... skipped. [short pause] Legs, bro.
HUMAN: [laughs] ...Fair.
HUMAN: [suspicious] Okay, what's the catch?
NXT: [serious] It's not on the Play Store, so download it only from the official GitHub page. And on iPhone, it needs some setup for now.
NXT: [friendly] Comment GYM, and I'll DM you the link and my goal prompt.
```

---

## 4. Scene-by-scene (estimated times)

| # | Time | Line | 3D scene | UI panel | SFX |
|---|---|---|---|---|---|
| 1 | 0.0–3.2 | HUMAN: gym app asked me to upgrade | Human slumped on the bench, phone buzzes; a red "UPGRADE TO PRO" pop-up bursts out of the phone as a floating 3D card with lock icons. **First frame already shows human + pop-up.** | Fictional paywall mock ("FitPro Premium", 3 locked features). No real app brand. | phone buzz, error ding |
| 2 | 3.2–6.0 | NXT: Delete it… | NXT drops in from above with a soft bounce; flicks the pop-up, it shatters into violet particles. | Paywall card cracks and shatters. | whoosh, glass crack, sparkle |
| 3 | 6.0–7.0 | HUMAN: Free free? | Quick punch-in on human's raised eyebrow. | — (panel holds) | record-scratch blip |
| 4 | 7.0–11.0 | NXT: openGym. Open source… | NXT projects a hologram GitHub card. | Card: `github.com/DuarteSantos8/openGym` then three chips crossed out one by one on "subscription / ads / account". | 3 tick-cross pops |
| 5 | 11.0–13.5 | NXT: muscles you've been skipping (OPEN LOOP) | A hologram body silhouette flickers on for half a second, legs flash red, then it vanishes. Tease only. | Panel dims to a "?" | glitch, low hum |
| 6 | 13.5–17.5 | Step one: prompt → Claude | NXT projects a clipboard hologram that flies into the panel. | **STEP 1/3 · PROMPT** — screen recording R2 (openGym's AI routine prompt being copied) then R3 (pasting into a Claude chat). | copy click, paste whoosh |
| 7 | 17.5–20.5 | HUMAN: Four days… dumbbells | Human counts on fingers; the dumbbells on the floor glow. | R3 continues: goal being typed "4 days/week · build muscle · dumbbells only". | keyboard taps |
| 8 | 20.5–23.5 | Step two: paste back, imports | Four glowing routine cards (MON · TUE · THU · FRI) fly out of the panel and slot into a floating 3D week calendar. | **STEP 2/3 · IMPORT** — R4: Claude's answer pasted into openGym, routines appear. | 4 slot pops, success chime |
| 9 | 23.5–28.0 | Step three: train… | Human does a dumbbell curl loop; a circular rest-timer ring counts down above his head; a counter ticks up to "1,324". | **STEP 3/3 · TRAIN** — R1: guided workout with an animated exercise demo and pre-filled weight. | rep thuds on beat, timer tick |
| 10 | 28.0–29.5 | HUMAN: muscle thing? | Human turns to NXT. | — | — |
| 11 | 29.5–33.0 | NXT: Trained. Tired. Skipped. Legs, bro. | **Hero shot:** big hologram body; camera orbits. Chest/arms fill green on "Trained", shoulders amber on "Tired", legs pulse red on "skipped". | R5: openGym's real muscle-map screen. | three rising tones, comedic boing on "Legs, bro" |
| 12 | 33.0–34.0 | HUMAN: Fair. | Human looks down at his legs, small shrug. | — | soft laugh sting |
| 13 | 34.0–35.5 | HUMAN: what's the catch? | Lights shift warm amber, music dips. | — | music filter sweep |
| 14 | 35.5–41.5 | NXT: not on Play Store… iPhone needs setup | NXT holds a small amber caution sign. | Generic app-store card (no Google Play logo) with an ✗ → official **GitHub Releases** card with a ✓ VERIFIED badge and "Android APK". Then a chip: "iPhone: web version · needs setup". | caution beep, verified ding |
| 15 | 41.5–end | NXT: Comment GYM… | Pull back to a wide two-shot; NXT waves; violet sparkle burst. | **End card** (hold ≥1.5 s): "Send this to your gym buddy who still pays for an app" · "Comment **GYM** for the link + my goal prompt" · "@ai.nxtlvl". | success chime, music button ending |

Retention rule: something new must move or change every 1.5–2.5 s.

---

## 5. Screen recordings Rishabh will supply (composite into the panel)

Record at 1080 px wide or more, light UI preferred, cursor visible:
- **R1** — openGym live demo (`https://opengym.duarte-santos.ch/demo/`): Home → start a guided workout → an exercise with its animated demo and pre-filled weight.
- **R2** — openGym's "build a routine with any AI" screen: copying the ready-made prompt.
- **R3** — a Claude chat: pasting that prompt + typing the goal, Claude answering.
- **R4** — pasting Claude's answer back into openGym; the routines appear.
- **R5** — openGym's muscle map / stats screen.

If a recording is missing, build a clean mock in the same layout and mark it `MOCK` in the file name so it can be swapped later. Never recreate the Claude logo or the Google Play logo; show the real Claude UI only via R3.

---

## 6. Audio

- **Music:** royalty-free upbeat electronic/gym track ~120 bpm (or synthesize an original one). Full energy under the hook, ducked −14 dB under speech (sidechain to the VO), dips at scene 13, button ending on the final word.
- **SFX:** as listed per scene; keep them short and punchy, mixed so the VO always leads.
- No copyrighted songs.

---

## 7. Facts sheet (the only claims allowed on screen or in VO)

- openGym is a free, open-source (AGPL-3.0) gym and body-weight tracker. No subscription, no ads, no account on someone else's server.
- Library of **1,324 exercises** with animated demos; supersets, warm-ups, drop sets, cardio; weights pre-fill; rest timer.
- Muscle map shows what's **trained, fatigued or detrained**.
- "Build a routine with any AI": copy a ready-made prompt into Claude/ChatGPT, paste the answer back, openGym imports it as routines. No key, nothing leaves the device.
- Imports history from FitNotes, Strong or Hevy.
- Android: sideloadable APK from GitHub Releases; deliberately **not on the Play Store**. Standalone app needs no account or server (data stays on the phone).
- iPhone / sync across devices: needs the self-hosted web app (Docker).
- Optional: a read-only MCP server lets Claude Desktop answer questions about your training (self-hosted only). Not in this reel.

Official links only: `https://github.com/DuarteSantos8/openGym` · `https://opengym.duarte-santos.ch` · `https://github.com/DuarteSantos8/openGym/releases/latest`
(Do not use forks such as `arvids-unavailable/openGym`.)

---

## 8. Cover (separate PNG, 1080×1920)

Hero frame from scene 11 (hologram body, legs glowing red) with NXT beside it.
Headline (Poppins Bold, two lines, inside the centre 1080×1350): **"Claude wrote my gym plan."** · sub-chip: **"free app tracks every set"**.
Keep everything readable at thumbnail size.

---

## 9. Post copy (for Rishabh, not for the video)

**Caption**
Comment "GYM" and I'll DM you openGym's official link + the goal prompt I use with Claude 💪

openGym is a free, open-source gym tracker: no subscription, no ads, no account.
1️⃣ Copy its ready-made prompt into Claude with your goal
2️⃣ Paste the answer back and your whole week imports
3️⃣ Train with 1,300+ exercise demos, a rest timer and a muscle map that shows what you've been skipping 👀

Android app is on GitHub (not the Play Store). iPhone needs the web version for now.
Save this for your next gym day and send it to your gym buddy.

#gymtracker #workoutplan #claudeai #opensource #fitnessapp

**Auto-DM message (keyword GYM)**
Here you go 💪
openGym (official): https://github.com/DuarteSantos8/openGym
Android APK: https://github.com/DuarteSantos8/openGym/releases/latest
Try it in your browser first: https://opengym.duarte-santos.ch/demo/

My goal prompt for Claude (paste it after openGym's routine prompt):
"My goal: [build muscle / lose fat / get stronger]. Days per week: [4]. Time per session: [45 min]. Equipment: [dumbbells + bench / full gym]. Experience: [beginner]. Injuries or limits: [none]. Keep it realistic and progressive."

Only download from the links above. If you have an injury or a health condition, check with a trainer or doctor before starting a new plan.

**Alt hooks (A/B test later)**
1. "Claude wrote my entire gym plan… and a free app tracks every set."
2. "This free gym app shows which muscles you've been skipping."
3. "Your gym app wants a subscription. This one never will."

---

## 10. Sources (for accuracy checks)
- github.com/DuarteSantos8/openGym (README, releases v1.2.5 / v1.2.14 / v1.4.1)
- opengym.duarte-santos.ch
- openGym `mcp/README.md`
