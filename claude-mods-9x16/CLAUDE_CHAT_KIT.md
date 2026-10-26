# Claude Code mods reel: kit for making it in Claude chat

Reel for the ai.nxtlvl page. No talking head: motion graphics plus an AI voiceover.
Look: a mix of a pixel-art world and the ai.nxtlvl light-cream style. 9:16, 1080×1920, about 36 s. CTA keyword **MOD**.

---

## 1. Script (modern story arc)

| Beat | Time | Voiceover |
|---|---|---|
| Hook | 0–3 s | Claude Code just got mods… and they change how Claude looks and works. |
| Proof | 3–6 s | Small plugins, live since October first. |
| Open loop | 6–9 s | Here are three worth installing… and one thing nobody checks. |
| 1 | 9–14 s | One: a live usage meter. See your limits before you hit them. |
| 2 | 14–19 s | Two: Collision Guard. It stops two sessions from overwriting each other's files. |
| 3 | 19–24 s | Three: Pixpal. A pixel-art pet that lives next to your chat. |
| Twist | 24–32 s | But here's the catch… some mods can read every prompt you type. So check what one touches before installing. |
| CTA | 32–36 s | Comment MOD and I'll DM you all three setups. |

About 92 words, roughly 36 s at a natural creator pace.

**Alternative hooks** (swap into the first line):

1. "Your Claude Code is still stock… mods just changed that."
2. "Claude Code just got mods, and number three is my favourite."
3. "Install these three Claude mods… but check this first."

---

## 2. Voiceover (paste into ElevenLabs)

- **Voice:** Liam, Energetic Social Media Creator (premade, voice id `TX3LPaxmHKxFdv7VOQHJ`).
- **Model:** Eleven v4 (or v3).
- **Speed:** 1.0–1.05. If it runs long, speed it up to about 1.1× in the edit.

```
Claude Code just got mods... and they change how Claude looks and works.
Small plugins, live since October first.
Here are three worth installing... and one thing nobody checks.
One: a live usage meter. See your limits before you hit them.
Two: Collision Guard. It stops two sessions from overwriting each other's files.
Three: Pixpal. A pixel-art pet that lives next to your chat.
But here's the catch... some mods can read every prompt you type.
So check what one touches before installing.
Comment MOD, and I'll DM you all three setups.
```

Export it as MP3 or WAV. For word-synced captions, run it through ElevenLabs Speech to Text (Scribe) to get word timestamps.

---

## 3. Look

**Palette (ai.nxtlvl cream × pixel world)**

| Role | Hex |
|---|---|
| Background, cream | `#F1E9DC` (grid lines `#E4D9C7`) |
| Ink, text | `#1E1B18` |
| Coral, accent and mascot | `#E8735A` (shadow `#B9523D`) |
| Green, numbers and "go" | `#3FA372` |
| Amber, warning | `#F2B33D` |
| Terminal dark | `#1B1A1F` |
| Card white | `#FFFDF8`, border `#E2D6C3` |

**Type**
- Big words: Instrument Serif *Italic* or Fraunces *Italic*, for example "*mods*" or "*Pixpal*".
- Punch words: Manrope ExtraBold, for example "STOP" or "CHECK".
- Labels: JetBrains Mono, letter-spaced caps, for example "STEP 1/3" or "MOD · INSTALLED".
- Pixel world: Silkscreen or Press Start 2P, used only inside pixel scenes.

**Recurring elements** (from the ai.nxtlvl reels)
- A faint cream grid background.
- A giant, very faint outlined word behind each scene ("MODS", "LIMIT", "GUARD", "PIXPAL", "CHECK").
- A top bar: "● AI.NXTLVL" at the top left and a thin progress bar at the top right.
- A step header "STEP 1/3" with three segments.
- White cards with soft shadows; a coral pill chip for alerts.
- A **pixel mascot**: a small coral pixel creature, about 16×16 pixels scaled up crisply. It reacts in every scene (points, jumps, panics, celebrates).
- Captions: lower third, Manrope ExtraBold, ink text with no shadow. The active word sits on a coral pill with cream text.

**Safe zones:** keep text out of the top 250 px and the bottom 400 px, and 60 px in from each side.

---

## 4. Scene beats (visual and sound per line)

| Time | Visuals | SFX |
|---|---|---|
| 0–3 s Hook | First frame already busy: a pixel console in a cream room. The mascot slams a coral cartridge labelled **MOD** into it. The screen glitches from a plain grey chat to a modded one, with panels sliding in. Giant faint "MODS" behind. | Cartridge click, glitch zap, bass hit |
| 3–6 s Proof | A version chip and an "OCT 1" calendar page flipping. Four plugin tiles snap onto a chat window (a panel, an alert toast, a "/command" chip, a status bar). | Calendar flip, four snap pops |
| 6–9 s Open loop | The step header builds as 1 · 2 · 3, then a 4th slot with a pulsing "?". The mascot tilts its head. | Three ticks, a "?" boing |
| 9–14 s #1 | "STEP 1/3". A pixel energy bar fills (session 62%, weekly 38%) in a status line under a chat box. The mascot runs toward a red pixel wall labelled LIMIT and stops just short. Green check. Big italic "*usage meter*". | Meter fill riser, skid, check ping |
| 14–19 s #2 | "STEP 2/3". Two pixel workers (two sessions) grab the same file icon "app.tsx". A guard character pops up between them with a coral chip "⚠ IN USE · 2 MIN AGO". The second worker steps aside to its own folder. Big italic "*Collision Guard*". | Two footstep blips, alarm chirp, shield pop |
| 19–24 s #3 | "STEP 3/3". A pixel egg beside a cream chat window cracks open into a tiny pixel pet that waves and bounces as chat bubbles appear. Big italic "*Pixpal*". | Egg crack, cute blip, sparkle |
| 24–32 s Twist | The background flashes to the dark terminal colour. Amber caution tape slides across. A pixel eye scans prompt bubbles going into a mod box. A checklist ticks in: "reads your prompts", "writes files", "goes online". Then a green "✓ CHECKED" stamp. The mascot holds a magnifying glass. | Bass drop, tape rip, scan beeps, stamp |
| 32–36 s CTA | Back to cream. A comment box types **MOD**; the send button presses. Floating chips: "setup 1", "setup 2", "setup 3". The mascot waves. A "Follow · Comment MOD" card is held for at least 1.5 s. | Keyboard taps, send whoosh, success chime |

**Music:** an upbeat lo-fi chiptune bed at about 100 bpm, dipped under the voice. It cuts out for one beat at the twist ("But here's the catch…"), then comes back. Use only royalty-free or generated music.

---

## 5. Paste-ready prompt for Claude chat

Use this with the **HyperFrames by HeyGen** connector enabled in Claude chat. Without the connector, ask for a single self-contained HTML/GSAP animation you can screen-record or render instead.

```
Make a 9:16 (1080x1920) Instagram Reel, about 36 seconds, 30 fps, as a HyperFrames project.
Topic: Claude Code mods. No talking head: pure motion graphics with an AI voiceover I'll add.

LOOK: a mix of a pixel-art world and a clean light-cream editorial style.
- Background #F1E9DC with a faint grid (#E4D9C7). Ink #1E1B18. Coral accent #E8735A. Green #3FA372.
  Amber warning #F2B33D. Dark terminal #1B1A1F. White cards #FFFDF8 with soft shadows.
- Fonts: Instrument Serif Italic for the big words, Manrope ExtraBold for punch words,
  JetBrains Mono letter-spaced caps for labels, and Silkscreen only inside pixel scenes.
- A small coral pixel mascot (about 16x16 px art scaled up crisply, nearest-neighbour) appears and
  reacts in every scene.
- Persistent top bar: "● AI.NXTLVL" at the top left, a thin progress bar at the top right.
- A giant, very faint outlined word behind each scene. A step header "STEP 1/3" with segments.
- Captions in the lower third (around y 1300–1450): Manrope ExtraBold, ink colour, no text shadow;
  the active word on a coral pill with cream text. Keep text out of the top 250 px and bottom 400 px.
- Something new moves every 1.5–2.5 s. Snappy expo/back eases, pops, slides, glitch hits.
  No slow fades. The first frame must already show the subject.

SCRIPT AND SCENES (voiceover line, then visuals):
0-3s  "Claude Code just got mods... and they change how Claude looks and works."
      The mascot slams a coral MOD cartridge into a pixel console; the chat glitches from plain to
      modded with panels sliding in. Faint "MODS" behind.
3-6s  "Small plugins, live since October first."
      An "OCT 1" calendar flip; four plugin tiles (panel, toast, /command, status bar) snap onto
      a chat window.
6-9s  "Here are three worth installing... and one thing nobody checks."
      Step circles 1, 2, 3 build, then a 4th slot with a pulsing "?".
9-14s "One: a live usage meter. See your limits before you hit them."
      STEP 1/3. A pixel energy bar (session 62%, weekly 38%) fills in a status line; the mascot
      runs toward a red LIMIT wall and stops just short; green check. Big italic "usage meter".
14-19s "Two: Collision Guard. It stops two sessions from overwriting each other's files."
      STEP 2/3. Two pixel workers grab the same "app.tsx" file; a guard pops up with a coral chip
      "IN USE · 2 MIN AGO"; the second worker steps aside. Big italic "Collision Guard".
19-24s "Three: Pixpal. A pixel-art pet that lives next to your chat."
      STEP 3/3. A pixel egg beside a cream chat window hatches into a tiny waving pet as chat
      bubbles appear. Big italic "Pixpal".
24-32s "But here's the catch... some mods can read every prompt you type. So check what one
      touches before installing."
      Flash to the dark terminal colour, amber caution tape slides across, a pixel eye scans prompt
      bubbles going into a mod box, a checklist ticks "reads your prompts / writes files /
      goes online", then a green "CHECKED" stamp. The mascot holds a magnifying glass.
32-36s "Comment MOD and I'll DM you all three setups."
      Back to cream. A comment box types MOD, the send button presses, chips "setup 1/2/3" float
      up, and a "Follow · Comment MOD" card holds for at least 1.5 s.

Leave an audio track for my voiceover file and a music bed. Mark where each SFX hits:
cartridge click, glitch, pops, meter riser, alarm chirp, egg crack, bass drop at the twist,
tape rip, scan beeps, stamp, keyboard taps, send whoosh.
```

When the voiceover is ready, upload it and ask Claude to retime every scene and caption to the real word timestamps.

---

## 6. Post copy

**Caption**

> Claude Code just got mods 🧩
> 3 worth installing (+ the one check most people skip):
> 1️⃣ a live usage meter, so you never hit your limit blind
> 2️⃣ Collision Guard, so two sessions never overwrite each other
> 3️⃣ Pixpal, a pixel pet next to your chat
> ⚠️ Some mods can read every prompt. Check before you install.
> Comment **MOD** and I'll DM you all three setups 👇
> Save this for later.
> #claudecode #claudeai #aitools #productivity #developer

**Cover text:** 3 CLAUDE MODS (+1 catch)

**Auto-DM:** set the keyword **MOD** in ManyChat or SuperProfile to send the three setup links. Check each mod's repository and what it can access before sharing it.

---

## 7. Facts behind the script

- Claude Mods went live on October 1, 2026. The team posted "We're live!" in the main thread: <https://github.com/anthropics/claude-code/issues/91870>
- Collision Guard warns when one session tries to edit a file another session touched recently (default window: 30 minutes).
- Pixpal (a pixel-art companion) is one of the community mods showcased in the thread above.
- Usage limits (5-hour session and 7-day weekly) can be shown live in Claude Code's status line: <https://code.claude.com/docs/en/statusline>
- The twist line comes from a community audit of 359 mods: 111 see every prompt, 95 write files, 75 reach the network. Mods are third-party code, not run by Anthropic.
- Left out on purpose: the reference reel's "chats talk to each other" and "cheapest-model" claims. I couldn't verify either as an existing mod.
