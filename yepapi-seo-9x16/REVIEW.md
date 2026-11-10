# Review — YepAPI "SEO spy" Reel (9:16, 35 s) — v3 preview draft

## Creative calls

v3 (after "make it more engaging, clean visuals and captions"): restyled to the person's own reference video's
language — dark stage with ambient brand light (lemon/blue/pink), dot grid and a lit horizon arc; chrome
headlines; glass cards; glowing wave, lens, key and stamps; orbiting tools around the mark; LED lookup grid;
clean white captions with the spoken word in lemon. Glow and glass are used because the reference uses them.
Claude logo and mascot supplied by the person (nominative use: "works with Claude").
More SFX with on-screen causes: glitch cuts, ping on "Connected", sparkle on the wordmark, typing under the
lookup grid, notification on the DM.

v1 notes:

- Storyline A, "the question travels" (see STORYLINES.md). Not built: B "the case file", C "type on colour".
- Look from the brand: lemon / ink / thumb blue / sleeve pink / cuff green, ink outlines with hard offset
  shadows, Space Grotesk + Geist Mono captured from yepapi.com, the real logo files.
- Proof beat uses YepAPI's real endpoints (`/v1/seo/domain/keywords`, `/v1/seo/competitors/domain`) and
  the real `x-api-key: YOUR_API_KEY` header. Keywords, ranks, volumes and domains are example data and
  are labelled "example data" on screen.
- The chat box is a neutral input labelled "Claude", not a copy of Claude's UI.
- Captions: one group at a time, blue block behind the spoken word. Not captioned twice: the question
  (typed on screen in sync) and the CTA (the end card shows it).
- CTA changed from the script's "Comment SEO" to "Comment YEPAPI", as the client asked.
- Layout uses the Nxtlvl 9:16 safe zone (text in y 250–1520, x 60–960); scenes shifted 100 px down for balance.

## Measured

- `hyperframes check`: passes. Two warnings kept on purpose:
  - `line_unread` on "crm for small teams" (s2, 1.23 s vs 1.27 s floor): the keyword rows are a fast
    montage of "every keyword"; no single row needs reading.
  - `contrast_aa_failure` at 9.72 s: a caption group mid-fade (2–3 frames).
- Render: 1080x1920, 30 fps, 35.0 s, H.264 + AAC 48 kHz. Mix −14.5 LUFS integrated, true peak −1.1 dBTP.
- Sound was measured, not heard.

## Weakest shot / next

- No music bed (HeyGen not signed in, no local model). Sign in for the free catalog, or generate a track.
- Voice is a free draft (Kokoro af_heart x1.12). With the client's VO: put it at assets/voice/vo.wav, run
  `npx hyperframes transcribe assets/voice/vo.wav --model small.en`, then `python3 scripts/build_timed_text.py`,
  then re-time scene starts in index.html to the new word times.
- A real screen recording of Claude using YepAPI would make the proof beat (s4–s5) stronger than the drawn input.
