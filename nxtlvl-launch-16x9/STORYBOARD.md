# Nxtlvl Social launch film (16:9, 32 s): draft

YouTube / LinkedIn / website launch film for Nxtlvl Social, with voiceover. Different from `nxtlvl-brand-16x9` and
`nxtlvl-promo-16x9` (both silent service tours): this one tells a story, problem → studio → four services → real proof
→ "Not luck. A system." → end card.

## Sound

- Voiceover: local Kokoro TTS (`am_michael`, speed 1.05), one file per line in `work/`, placed on the film clock and
  levelled to −16 LUFS (`assets/voice/vo.wav`).
- Music: the Nxtlvl brand bed (120 bpm, drop at 4 s, impact at 22 s, star bell at 27.5 s), ducked under the voice.
- SFX: the Pixabay-licensed set (`assets/sfx/CREDITS.md`), placed in `SFX` in `tools/build.py`.

## Scenes

| Time | Voice | Picture |
|---|---|---|
| 0–4 | "Everyone's posting. Almost no one gets seen." | A wall of generic posts flies past, goes grey; the views stall at 12 |
| 4–9.6 | "Meet Nxtlvl Social. The creative studio that takes your brand to the next level." | On the drop the Shooting Star streaks in, the wordmark wipes on; Design · Reels · Automation · Websites pop on the beat |
| 9.6–11.6 | "Designs that stop the scroll." | 01 Design: three post designs fan out, "Designer-finished" stamp |
| 11.6–13.6 | "Reels, cut on the beat." | 02 Reels: our real System ad plays in a phone, a timeline is cut on each beat |
| 13.6–15.85 | "Automation that replies while you sleep." | 03 Automation: an 11:42 PM DM answered by itself, "Auto-reply · 3 sec" |
| 15.85–18.2 | "Websites that turn views into clients." | 04 Websites: nxtlvlsocial.ai (real screenshot), "Book a free call" clicked, a new enquiry arrives |
| 18.2–22 | "Zero to 7,000 followers. In 22 posts." | @ai.nxtlvl: the count climbs 0 → 7,100 with the growth line; "in 22 posts" |
| 22–24.3 | "Not luck. A system." | "Not luck." struck through, "A SYSTEM." lands on the impact |
| 24.3–32 | "Nxtlvl Social. Your brand, next level. Find us at nxtlvlsocial.ai" | Lockup, tagline, star glint on the bell, nxtlvlsocial.ai and connect@nxtlvlsocial.ai |

## Rebuilding

- `assets/video/edit.mp4` (out of git) = `nxtlvl-ad-system-9x16/renders/nxtlvl_system-ad_reels_9x16_v2.mp4` 0.2–4.8 s, `-an -g 15`.
- `assets/img/site-hero.png` is a 1440×900 capture of `website/index.html`.
- `python3 tools/build.py`, then `npx hyperframes check`, `npx hyperframes render`.
