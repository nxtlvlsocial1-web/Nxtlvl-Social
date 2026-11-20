# Nxtlvl Social launch film v2 (16:9, 32 s): draft

A full rework of v1 (the person asked for something different, more stylish, more transitions, prices in dollars).
Look: bold editorial colour blocks that flip on the beat (Mist, Violet, Ink), giant Archivo type with Instrument Serif
Italic accents, and a film-slate frame (corner marks, running timecode, REC dot) over everything (`hud.html`).

## Prices

From the site's earlier price list (before prices came off the website): design from $5/month, reel editing from
$15/month, automation from $49/month. Websites have no listed price: "custom quote / quoted on a free call".

## Sound

Voice: local Kokoro TTS (`am_michael`, speed 1.08), lines in `work/v2/`, placed by `LINES` in `tools/build.py`, −16 LUFS.
Music: the Nxtlvl brand bed (drop 4 s, impact 22 s, bell 27.5 s), ducked under the voice. SFX: Pixabay-licensed set.
Every spoken line is also on screen as type, so there is no separate caption track.

## Scenes and transitions

| Time | Voice | Picture | Out |
|---|---|---|---|
| 0–4 | "Stop posting. Start getting seen." | STOP on Mist → hard cut on the beat to START on Violet → SEEN rows on Ink, growing with the riser | T1 diagonal slices |
| 4–6.3 | "This is Next Level Social." | On the drop: the Shooting Star streaks in, the wordmark wipes on, NXTLVL/SOCIAL outline type drifts behind | T2 dive into the star's head, iris opens to Mist |
| 6.3–9.5 | "Your entire creative team, in one studio." | The site's headline, each line rising out of a mask; 01–04 service tags | T3 venetian blinds |
| 9.5–12.95 | "Social media design. From five dollars a month." | Violet: "Designs that stop the scroll.", three post designs fan out, Designer-finished stamp, **from $5/month** | T4 whip pan |
| 12.8–15.45 | "Reel editing. From fifteen dollars." | Ink: our real System ad plays in a phone, a timeline cut on each beat, **from $15/month** | T5 push-up |
| 15.25–19.45 | "Automation that replies while you sleep. From forty nine dollars." | Mist: an 11:42 PM DM answered by itself, **from $49/month** | T6 tile wipe |
| 19.4–22 | "And websites that turn views into clients." | Ink: the real nxtlvlsocial.ai scrolls, a visitor books a call, "New enquiry"; custom builds quoted on a call | T7 impact flash |
| 22–24.35 | "Your brand. Next level." | Violet: YOUR BRAND. slams with shockwaves, "next level." steps up | T8 iris closes to Ink |
| 24.2–32 | "No contracts. Cancel any month. Book a free call at nxtlvlsocial.ai" | Lockup, the price board ($5 · $15 · $49 · custom quote), terms, Book a free call tapped on the bell | hold |

## Rebuilding

- `assets/video/edit.mp4` (out of git) = `nxtlvl-ad-system-9x16/renders/nxtlvl_system-ad_reels_9x16_v2.mp4` 0.2–4.8 s, `-an -g 15`.
- `assets/img/site-long.png` = a 1440-wide capture of `website/index.html`.
- `python3 tools/build.py` (mixes voice and music, writes index.html), `npx hyperframes check`, `npx hyperframes render`.
