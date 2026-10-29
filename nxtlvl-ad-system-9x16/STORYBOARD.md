# Nxtlvl Social — "Not luck. A system." ad (9:16, 23.3 s)

Meta click-to-message ad (Reels / Stories placement) built on the selfie take. The footage plays with its own
sound; the first 1.2 s of silence is trimmed so he speaks at 0.24 s. Times below are film time (source − 1.2 s).

Safe zones on 1080×1920: nothing readable above y 270 (status bar, ad label) or below y 1330 (Meta's caption,
"Send message" button). The face sits at y 450–1180 at full frame.

| Time | Speech | Picture | Sound |
|---|---|---|---|
| 0.00–4.34 | "We took @ai.nxtlvl from zero to 7,100 followers with just 22 posts." | Full frame. An Instagram-profile card for @ai.nxtlvl sits above his head from frame 0: followers count 0 → 7,100 on "7,100", posts 0 → 22 on "22", a "+7,100" chip pops. Word-by-word captions on the chest. | pop on 7,100, pop on 22 |
| 4.34–6.50 | "Not luck, a system, and here's what's inside it." | Punch-in on "Not luck" (hard cut to 1.16×), "Not luck." in serif with a strike-through, then "A system." slams in violet (1.26×). Captions return for "and here's what's inside it". | whoosh on punch-in, soft impact on "system" |
| 6.50–14.20 | the three services | Camera pulls back into a rounded face window at the top; the brand stage fills the frame. Three cards land one by one under it, synced to speech: 01 designs made to be saved (bookmark fills), 02 a content calendar a month ahead (month grid fills), 03 reels edited and posted every week (week chips tick). | whoosh into the window, pop per card |
| 14.20–18.45 | "Most agencies charge ₹25,000 for this, but we start at ₹999." | Same window. Price card: "Most agencies ₹25,000" is struck through, then "Nxtlvl Social, starts at ₹999" lands with a "96% less" chip. | pop, strike tick, sparkle on ₹999 |
| 18.45–21.50 | "Want this for your own brand? Reach out to us and tap Send Message." | Camera opens back to full frame. Captions. A "Tap Send Message" chip drops in above his head on "Reach out". | whoosh, notification on the chip |
| 21.50–23.30 | (end) | End card over the dimmed take: Shooting Star + nxtlvl wordmark, "Your social, on a system.", a big "Tap Send Message" button with an arrow down to Meta's button, "Plans from ₹999". Holds 1.8 s. | soft impact + sparkle |

Music: the Nxtlvl brand bed (our own track from `nxtlvl-brand-16x9`), entered at its 4 s drop, 0.14 under the voice,
fading out over the last second.

## Rebuilding

- The footage (`assets/video/footage.mp4`) is kept out of git. Recreate it from the original selfie take with dense
  keyframes (the original has one every 5 s, which freezes on seek):
  `ffmpeg -i <original>.mp4 -vf scale=1080:1920:flags=lanczos -c:v libx264 -crf 17 -g 30 -keyint_min 30 -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 192k assets/video/footage.mp4`
- `transcript.json` is the ElevenLabs Scribe transcript of the take, corrected (handle, figures, prices) with the
  original word timings. `python3 tools/build.py` writes `index.html` (camera, scene hosts, music, SFX) and
  `compositions/captions.html` from it; the cards are hand-written scenes in `compositions/`.
- Check with `npx hyperframes check`, render with `npx hyperframes render --quality draft|delivery`.
