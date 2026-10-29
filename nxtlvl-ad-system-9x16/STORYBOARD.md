# Nxtlvl Social — "Not luck. A system." ad (9:16 split screen, 21.8 s) — v2

Meta click-to-message ad (Reels / Stories placement) built on the selfie take.

**v2 changes (from the person's notes):** split screen; captions and statements in the "Not luck." serif
(Instrument Serif italic), placed under the seam; jump cuts that remove every pause; a cleaned, levelled voice;
more motion in the panels.

## Edit and sound

- `tools/cut.py` cuts the take into nine sentences (each ~80 ms before the first word and after the last), joins
  them with 12 ms audio fades, and cleans the voice: high-pass 80 Hz, light de-noise, −2.5 dB at 250 Hz, +2.5 dB at
  3.5 kHz, compression 3.5:1, two-pass loudness normalisation to −16 LUFS / −1.5 dBTP. 23.8 s became 21.8 s; the
  voice's loudness range went from 7.4 LU to 2.3 LU.
- Every cut changes the framing (1.0 / 1.15 / 1.0 / 1.1 / 1.0 / 1.1 / 1.22 / 1.0 / 1.12, plus 1.26 on "A system."),
  so each jump lands as a new shot.
- Music: the Nxtlvl brand bed at 0.13 under the voice. SFX on the counter, strikes, row ticks, ₹999, the tap and
  the end card. Final mix measured at −15 LUFS, −1.2 dBTP.

## Layout (1080×1920)

Top half (0–960): the take, cropped to the face. A glowing seam at 960. Captions just under it (y 984–1080),
word by word in the serif. Panel graphics in y 1100–1500. Below that only decoration (Meta's caption and
Send message button sit there).

| Film time | Speech | Panel |
|---|---|---|
| 0.00–3.84 | "We took @ai.nxtlvl from zero to 7,100 followers with just 22 posts." | @ai.nxtlvl profile row; a giant counter 0 → 7,100 while a growth line draws; posts 0 → 22; "in 22 posts" chip |
| 3.84–5.60 | "Not luck, a system," | "Not luck." in the serif, struck through; "A system." lands big with a flash (no captions here) |
| 5.45–12.80 | "and here's what's inside it." + the three services | "Inside the system" checklist: three rows light up as they are named (bookmarks fill, a month fills, four weeks tick) and turn into green ticks |
| 12.77–16.82 | "Most agencies charge ₹25,000 for this, but we start at ₹999." | Two tiles, VS: ₹25,000 struck through, ₹999 lands with a "96% less" chip |
| 16.80–18.04 | "Want this for your own brand?" | "@yourbrand" chip and "Your brand, next." |
| 18.04–19.66 | "Reach out to us and tap Send Message." | A big Send message button; a finger taps it on "tap" |
| 19.66–21.83 | (end) | Full-frame end card: Shooting Star + nxtlvl social, "Not luck. A system.", Tap Send Message, "Plans from ₹999" (holds 2.2 s) |

## Rebuilding

- `assets/video/footage.mp4` and `assets/video/aroll.mp4` are kept out of git. Recreate the footage from the
  original take: `ffmpeg -i <original>.mp4 -vf scale=1080:1920:flags=lanczos -c:v libx264 -crf 17 -g 30 -keyint_min 30 -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 192k assets/video/footage.mp4`
- Then `python3 tools/cut.py` (the cut + `transcript-cut.json`), `python3 tools/build.py` (index.html and the caption
  track), `npx hyperframes check`, `npx hyperframes render --quality draft|delivery`.
- `transcript.json` is the ElevenLabs Scribe transcript of the take, corrected (handle, figures, prices) with its
  original word timings.
