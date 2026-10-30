# TASTE: console-continue-9x16

Updated 2026-10-30, after the Motion Video Director rebuild. Current version: preview v3 (renders/nxtlvl_console-continue_reels_9x16_preview.mp4).
Status: draft (waiting for preview approval).

## 1. Brief and story
- Concept: the Reel is a game. GAME OVER countdown on real God of War gameplay, then Player 2 (Claude) joins and the
  pixel cast plays through Console Skill's features: title, rebuild, power-ups, boss fight, New Game+, early access,
  "Comment CONSOLE to continue".
- Instagram Reel for AI.NXTLVL, 9:16 1080x1920, 30 fps, 42.4 s. CTA keyword CONSOLE.
- Script approved, on the modern story arc. Voice: ElevenLabs "Stacey" (eleven_v4), assets/audio/voice.wav.
- Pipeline: A (code-drawn) plus the owner's own PS2 gameplay (GoW, RE4) where it proves the point.

## 2. Theme and feel
- Mood: playful, warm, arcade, confident.
- Feels like Video-44655 from 3 s on: one big pixel character plus one kinetic caption group on a warm colour field
  or soft-focus room; characters break into pixels and reform; cuts every 2 to 4 s, constant word-level change.
- Must not feel like: a UI dashboard, cluttered confetti, lavender Y2K stage, generic stock template.
- Intensity 4 to 5 (social reel).

## 3. Visual design system
- Palette: fields orange #e0561f to #ff9a4a, red #b3121f to #f0414a, dark #0c0306 to #2a0610; accent red #e8344e
  (highlight boxes, silhouettes); Claude orange #D97757 (Player 2, crab); white text; yellow pixel dots #ffcf5a.
- Type: keywords Anton 96 to 170 px caps or Lilita One 88 to 124 px lowercase (alternating); connector words Rubik 800
  62 px lowercase; tiny words Rubik 800 40 px; plain sentence lines Inter Display 600 62 px. 3D title and countdown:
  Lilita One glossy white face, violet sides.
- Text treatment: hard 4 to 7 px drop shadow in the scene's dark tone; keyword turns to the scene accent after it
  lands, one letter hollow (4 px stroke); plain lines get a red #e8344e highlight box behind the last word.
- Layout: caption zone y 270 to 670 (A: 236 to 496), character and hero object below it, nothing in the top 250 or
  bottom 400 px except the CTA box at 1210 to 1360.
- Finish: film grain 9 % (assets/img/grain.png, overlay, flickers at 15 fps), vignette to 42 % black, scanlines 5 %.

## 4. Motion language
- Captions: letter by letter, each letter flashes a random colour (#ff7ab8 #ffd36e #7fe7ff #b48cff #ff8a5c), skewed
  -16 deg at 1.4x, settles in 90 ms; colour smear behind the word; staircase stack tilted -5 to 4 deg, alternating
  left/right/centre; keywords Claude, emulator, Boss, Plus, CONSOLE fly in from the camera in 3D (rotateY -70);
  exit = letters scatter like pixels in 140 ms.
- Characters (assets/js/actors.js): assemble from 2x2 sub-pixels in 0.32 s, dissolve in 0.3 s; idle bob and breathe;
  hops with squash 0.84 / stretch 1.14 on landing; coin spins 0.5 s; lunges on hits; white hit flash; smear trail on
  fast moves; greyscale fade on "forever".
- Transitions: yellow pixel-dot sweep (A to B), warm block mosaic in random order (C1, E, G), white flash plus
  one-colour mascot silhouette breaking into pixels (D red Vesper, H orange crab), whip (C2), zoom-through (F).

## 5. Sound
- Music: owner-supplied track (videoplayback_2), 120 BPM, muffled until "player", ducked under the voice.
- SFX synthesised in build/audio.py: ticks, slams, swishes, hits, unlocks, stamp, keys, glitch, pixel sparkle ("pix")
  on every big character assemble/dissolve. Master -14 LUFS, limiter at -1 dBTP.

## 6. Technical
- Build: python3 build/generate.py, then python3 build/audio.py. Check: npx hyperframes@0.8.203 check.
  Renders run detached: build/render_preview.sh (draft) and build/render_final.sh (delivery).
- Look-defining code: build/generate.py captions(), transitions(), sp()/actor(); build/mascots.py pixel_map() poses;
  assets/js/actors.js; assets/js/world.js (3D props only).

## 7. Do / Don't
- DO: one focal character or object per moment; keep characters moving; give every change a sound.
- DON'T: floating confetti, chips, dashed slots, outline shapes in the margins, more than one caption group at once.

## 8. Feedback rules (append-only)
| Date | Version | User said | Rule |
|---|---|---|---|
| 2026-10-29 | v1 | voice too dull | expressive voice (v4 Stacey) |
| 2026-10-29 | v1 | still slow and dull | more motion and transitions, nothing static |
| 2026-10-30 | v2 | fonts weird, Steam Deck hidden | Lilita One 3D type; check every flag/label is visible |
| 2026-10-30 | v2 | follow Video-44655 incl. pacing and mascot spins | big pixel characters that dissolve/reform, kinetic letter-by-letter type |
| 2026-10-30 | v2 | "still look bad" | strip clutter: one character and one caption group per moment |
