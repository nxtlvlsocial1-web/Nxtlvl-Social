# REA reel: timing changes to match the final audio

Word timings come from ElevenLabs Scribe on the avatar clip (`build/scribe_words.json`).

**Head trim.** The avatar clip starts 0.30 s in (`data-media-start="0.3"`). That removes leading
silence only; the first word now lands at 0.12 s, and the last word ("link.") ends at 29.94 s,
so the reel is exactly 30.0 s as required.

| Scene | Brief | Final | Starts on |
| --- | --- | --- | --- |
| S1 Hook | 0.0–5.0 | 0.00–5.20 | — |
| S2 Proof | 5.0–8.0 | 5.20–9.74 | "It's called" |
| S3 Open loop | 8.0–12.0 | 9.74–13.70 | "Ask your agent" |
| S4 Evidence | 12.0–16.0 | 13.70–17.26 | "It reads" |
| S5 Rebuild | 16.0–19.0 | 17.26–20.58 | "and your agent" |
| S6 Targets | 19.0–22.0 | 20.58–23.72 | "Desktop" |
| S7 Local | 22.0–25.0 | 23.72–27.14 | "and it all runs" |
| S8 CTA | 25.0–30.0 | 27.14–30.00 | "Comment" |

In-scene beats follow the words they belong to:

- FREE stamp on "free" (2.90 s); REBUILT stamp on "rebuild" (4.16 s).
- Star counter runs over "two hundred and eighty-six thousand" (6.58 s); the star burst follows.
- The question types in from "Why" (10.94 s).
- Rule highlight on "finds" (15.54 s); value chips follow it; EVIDENCE stamp on "rule" (16.71 s).
- Slider drag ends on "slider" (19.51 s); REBUILT stamp follows.
- Target rows on "Desktop", "Android", "websites".
- X stamp on "Nothing" (25.56 s).
- REPO types on "repo" (27.58 s), the DM bubble on "DM" (28.58 s), the URL just before "link".

**Deviations from the brief.**

- S8 runs 2.86 s rather than at least 4 s. The CTA line starts at 27.14 s and the reel must end at
  30.0 s, so there was no room; everything in the scene still lands on its word.
- The avatar's move into the circle uses a transform plus a circular clip rather than animating
  its position, because HyperFrames rejects `left`/`top` motion (it stutters in frame capture).
  The look is the brief's: full frame → 300 px circle centred at (200, 1370) in 0.35 s, and back
  in 0.4 s.
- The star count (286K) is from the brief, dated 17 Oct 2026. It was not re-checked before render.
- Captions write the brand as REA, DM as DM, and the spoken number as 286K.

## v2: dual screen, faster motion, new palette, music and sound effects

- **Layout.** Visuals fill the top half (y 0–960); the talking head fills the bottom half
  (y 960–1920), as in the reference reel. Captions sit just under the split line. Scene content is
  laid out as before and scaled to fit y 270–930 of the top screen.
- **Motion.** Pops 0.3 → 0.18 s, slides 0.35–0.45 → 0.2–0.26 s, the S1 flip 0.45 → 0.28 s, the star
  counter 1.6 → 1.0 s, typing 25 → 40 characters/s. Every cut snaps in (0.2 s) with a white flash,
  and the talking head punches in on "free", "two hundred…", "Nothing" and "Comment".
- **Palette.** Violet-to-indigo top screen with drifting pink and cyan glows; lime, pink, yellow and
  cyan accents; white cards with dark ink; captions highlight the active word in lime.
- **Audio.** The voice is the clip's own audio from 0.30 s, levelled from −29 dB to about −18 dB mean
  (`assets/audio/voice.wav`). The music (120 bpm, A minor) and the 76 sound effects are synthesized by
  `build/generate.py`, so there are no licensing issues; the music dips under the voice.

Rebuild the audio and composition:

```bash
ffmpeg -y -ss 0.3 -t 30 -i assets/video/avatar.mp4 -vn \
  -af "highpass=f=70,acompressor=threshold=-24dB:ratio=3:attack=10:release=150,loudnorm=I=-15:TP=-1.5:LRA=9" \
  -ar 44100 -ac 1 assets/audio/voice.wav
python3 -I build/generate.py   # needs numpy and scipy
```
