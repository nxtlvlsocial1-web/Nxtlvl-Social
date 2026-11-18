# Dr S Kokila - brand and style guide

> Public part of this client's memory: look and workflow only. The brief, feedback, scripts, footage list,
> hooks/CTAs, calendar and open items live in the private `nxtlvl-client-memory` account skill.

What her reels look and sound like, as built and approved in `kokila-peace-9x16` (v4 is the current look).

**Index**
- [1. Logos and brand kit](#1-logos-and-brand-kit)
- [2. Colours](#2-colours)
- [3. Fonts](#3-fonts)
- [4. Captions (subtitles)](#4-captions-subtitles)
- [5. Hook text box](#5-hook-text-box)
- [6. Other on-screen graphics](#6-other-on-screen-graphics)
- [7. Layout: split screen, reference full screen, her full screen](#7-layout-split-screen-reference-full-screen-her-full-screen)
- [8. Edit style: pacing, transitions, zooms, text animation](#8-edit-style-pacing-transitions-zooms-text-animation)
- [9. Sound: voice, echo, music, SFX](#9-sound-voice-echo-music-sfx)
- [10. Voice and language](#10-voice-and-language)
- [11. Formats, safe zones, naming, export, loudness](#11-formats-safe-zones-naming-export-loudness)
- [12. Reference videos and footage, and what was used](#12-reference-videos-and-footage-and-what-was-used)
- [13. People in footage: religion-neutral, Indian people](#13-people-in-footage-religion-neutral-indian-people)
- [14. Cover style](#14-cover-style)
- Related: dr-kokila-brief.md (private memory skill), footage-and-assets.md (private memory skill), [workflow-and-skills.md](workflow.md)

*Sources: `scratchpad/notes_kokila.md` §5-§6; `/home/user/Nxtlvl-Social/kokila-peace-9x16/build/generate.py` (colours,
layout), `plan/edit.json`, `plan/music_edit.json`, `plan/sfx_cues_final_A.json`, `build/render_v2.sh`.*

---

## 1. Logos and brand kit

- Logo: UNKNOWN (none supplied, none used).
- Brand kit: none in the repo (no `brands/kokila...` folder). The look was set by the assistant as "her branding (calm
  blue pill, warm accents)", matching the royal-blue pill captions of her own reels. Suggestion (not done): save this
  guide as `brands/<kokila-slug>/brand.md`; see open-items.md (private memory skill).
- Name mark used: white name chip "Dr S Kokila"; cover card "DOCTOR'S TAKE / Dr S Kokila".

## 2. Colours

From `build/generate.py`:

| Token | Hex | Used for |
| --- | --- | --- |
| BLUE | `#2448E8` | Caption pill (royal blue), seam line ends, cover "DOCTOR'S TAKE" label, cover glow |
| NAVY | `#0E1A3A` | Root background, v1 hook text, cover background, cover name |
| YEL | `#FFD23F` | Caption keywords, "AROUND YOU" line, seam line centre, v1-v3 hook ₹85,000 highlight, cover highlights |
| CORAL | `#E8443A` | Strike-through lines on "Subscription" / "Your time" chips |
| GREEN | `#13895A` | "FREE" badge |
| CREAM | `#FFF6EA` | Default top-half background (with soft blue / yellow radial glows) |
| RED | `#E0182D` | Hook text (whole line from v4) |
| White | `#FFFFFF` | Hook box background, caption text, name chip |

- Cover glow gradient: `#2448E8 -> #13245F -> #0E1A3A`.
- Seam line gradient: `#2448E8 -> #FFD23F -> #2448E8`.
- Grain overlay: `assets/img/grain.png`, opacity .05, blend overlay.
- White flash on transitions: opacity .45/.55 -> 0 in .25 s.

## 3. Fonts

- Inter (OFL), weights 600 / 700 / 800: `assets/fonts/inter-latin-{600,700,800}-normal.woff2`.
- Captions and hook: Inter 800. Cover headline: Inter 800 86 px.

## 4. Captions (subtitles)

- Inter 800, 62 px, white text on a royal-blue pill `#2448E8` (radius 22 px, padding 12/30/16), keywords in `#FFD23F`,
  drop shadow.
- 1-3 words per pill. Break at 3 words, at punctuation, at a gap over 0.45 s, at a section cut, or at over 18 characters.
- Animation: pop in 0.16 s, `back.out` ease.
- Positions by mode: "seam" top 868 in split screen (sits on the seam); "hk" top 1000 while the hook shows (just above
  her head, under the hook); "rf" top 1480 on full-screen reference footage; "low" top 1380 on her full screen.
- Case: as spoken (sentence case). Language: English only.
- Keywords highlighted yellow: temple, 85,000, rupees, brain's, blood, flow, stress, sleep, exercise, afford, work, free,
  subscription, time, people, complaining, criticizing, disrespecting, loving, supporting, inspiring, best, peace, mind,
  mental, health, beautiful, greatest, upgrade, device, life.
- 71 caption groups in v3/v4 (70 in v2).
- Client rule: subtitles stay as they are (blue pill, yellow keywords) - only the hook turned red (voice note: "remaining
  apnejo subtitle diaha there it is fine").
- Her own reels' captions (reference): "1-2 words at a time, white on a small royal-blue pill, sitting low in the middle."

## 5. Hook text box

- Text: "Can an ₹85,000 device / measure your peace of mind?" (two lines).
- v4 (current): white box, radius 26 px, text red `#E0182D` on the whole line including ₹85,000; Inter 800 58 px,
  line-height 1.08; top 800 (SEAM - 120). Pops in at the split (scale 1.25 -> 1), holds 5.5 s, exits upward.
- Placement: only on the split screen after the opening (never over Deepinder's full screen).
- History:
  - v1 (2026-11-12): navy text with yellow highlights, on the seam; in v1 it appeared at 0:00 over Deepinder's clip.
  - final v1 (2026-11-12 12:39, internal "v5"): moved off Deepinder's full screen to the split screen after the black
    (owner 12:37:49).
  - v2 (2026-11-13): "peace of mind?" red, ₹85,000 kept on a yellow highlight; held 5.5 s (was ~2 s).
  - v3: same styling; the separate "TEMPLE by Deepinder Goyal ₹85,000" glass tag removed (no second 85,000).
  - v4: whole line red on white, the yellow box gone (owner 2026-11-13T14:32:23).
- Duration rule: 5-6 s on screen (she said "five to eight seconds", then "five to six seconds"); delivered 5.5 s.

## 6. Other on-screen graphics

Kept minimal from v3 on ("less animated explanations"). v4 graphics:
- Labels on footage (small white glass chips): "Stress", "Sleep", "Exercise", "Results: not yet known".
- Free-tracker card: "A tracker that is" + price counting down 85,000, 61,000, 38,000, 17,000, 6,000, 900, 0 to "₹0";
  "FREE" badge (green, rotated 6deg); chips "Subscription" and "Your time" struck through with a coral line.
- Big type "THE PEOPLE / AROUND YOU" (second line yellow) over footage.
- Her full screen: "₹85,000?" then a stamp "MAYBE NOT." (rotated -6deg).
- Name chip on the doctor line: "Dr S Kokila".
- Credit pill on podcast shots: "Source: Raj Shamani podcast".
- On Deepinder's full screen (cut A): his quote in italic white, "It measures blood flow to your brain."
- Removed over the versions (do not bring back unless asked): v1 metric cards (Brain blood flow, Stress, Sleep,
  Exercise) with pulse line; test loader stuck on "pending"; people circle with red X's and hearts; stress meter
  (92% / 12%); draining battery; orbiting avatars; "greatest upgrade" cards; end cards; "As a doctor" label; the "TEMPLE
  by Deepinder Goyal ₹85,000" glass tag.

## 7. Layout: split screen, reference full screen, her full screen

- Canvas 1080x1920, 30 fps.
- Split screen: top 0-920 = screen / footage; bottom 920-1920 = her face (`tight_bot` = crop 1080:1000:0:330 of her
  cut). Seam line 6 px at y 917, gradient blue-yellow-blue; hidden during Deepinder's full screen.
- Three modes: "split", "ref" (reference footage fills 1080x1920, her voice and subtitles over it), "full" (her face full
  frame).
- Client direction (2026-11-13T12:47:32): reference footage full screen most of the time; her full screen / split screen
  only now and then; split screen for the opening text hook.
- v4 section timing, cut B (`plan/edit.json`, 59.54 s, offset 2.94):

| Mode | From (s) | To (s) | Content |
| --- | --- | --- | --- |
| split | 0.0 | 5.5 | opening hook (5.5 s) over Deepinder's clip, her below |
| ref | 5.5 | 10.0 | device / Deepinder full-screen crops; stress / sleep / exercise |
| full | 10.0 | 12.38 | her: "But can you afford it? Maybe not." with "₹85,000?" / "MAYBE NOT." |
| split | 12.38 | 21.54 | "Does it work? We don't know yet." + free-tracker graphic |
| ref | 21.54 | 32.18 | "the people around you"; complaining / criticising / disrespecting |
| split | 32.18 | 36.72 | one beat of "loving you" |
| ref | 36.72 | 41.06 | supporting / inspiring |
| full | 41.06 | 47.26 | doctor line with her name chip |
| ref | 47.26 | 56.36 | "surround yourself with people", "the greatest upgrade" |
| split | 56.36 | 59.54 | closing line, ends on her face |

  Cut A = the same plus 2.94 s of opening: Deepinder full screen 0-2.56, black 2.56-~2.94.
  (Content column partly inferred from the notes' v3/v4 description; times are exact.)
- Cut A balance (v3, same in v4): ~29 s full-screen reference, ~9 s her full screen, ~22 s split.
- Cut A opening: Deepinder full screen (`pod_full`, crop 741:1318 of the recording, graded brightness 1.42, contrast
  1.18, saturate 1.18, slow 1.0 -> 1.06 push), credit pill, quote; black at 2.56 s; split screen zooms in from blur at
  ~2.94 s with a hit.
- Frames checked in v4 cut A: 1.2 s Deepinder full screen with the Temple patch; 4.5 s split, red-on-white hook over the
  Deepinder clip, caption "temple costs"; 9 s Deepinder full-screen crop, caption "and how your"; 20 s split with "₹0 /
  FREE" glass card, caption "free."; 26 s full-screen Indian family dinner with "THE PEOPLE AROUND YOU", caption "is the
  people"; 33 s full-screen upset Indian woman, caption "complaining,"; 45 s her full screen with "Dr S Kokila" chip,
  caption "Because the people"; 60 s split, father and son top, her bottom, caption "the beautiful".

## 8. Edit style: pacing, transitions, zooms, text animation

- Pacing: tight cut of her talking, sped 1.08x (pitch kept). Gap between lines 0.06 s (two frames); pauses 0.1-0.18 s
  (capped at 0.18 s, natural/proportional, not all 0.1 s); hold after her last word 0.3 s. Only her speaking, no
  glances or head turns between cuts.
- Reference reel benchmark: about 62 cuts in 105 s (one every ~1.7 s).
- Transitions (zoom-blur in):
  - into split: bottom 1.45 -> 1 with 10 px blur; top 1.12 -> 1 with 12 px blur.
  - into ref: top 1.14 -> 1 with 12 px blur, .42 s `expo.out`.
  - into full: 1.2 -> 1 with 14 px blur, then slow 1.0 -> 1.1 push.
  - White flash on transitions (.45/.55 -> 0 in .25 s).
  - Hard cut to black after Deepinder's line (cut A).
- Zooms: slow 1.0 -> 1.08 push on every B-roll clip; 1.0 -> 1.06 push on Deepinder's full screen; 1.0 -> 1.1 on her full
  screen.
- Text animation: caption pills pop in 0.16 s `back.out`; hook pops scale 1.25 -> 1 and exits up; price counts down to
  ₹0; strikes draw across chips; "MAYBE NOT." stamp.
- Echo: on Deepinder's last word "brain" (see section 9).
- Overlays: grain .05 overlay; credit pill on podcast shots; glass label chips.

## 9. Sound: voice, echo, music, SFX

**Her voice (her own voice, no voiceover):** her cut cleaned with highpass 80 Hz, afftdn nf -28, compressor threshold
-20 dB ratio 3 attack 8 release 120 makeup 2, loudnorm -16 LUFS; tight cut sped 1.08 (pitch kept). Audio pieces carry
PCM (AAC pieces drifted the voice ~1 s over 50 joins).

**Deepinder's line (cut A only):** "It's super easy and it measures blood flow to your brain." levelled to -16 LUFS with a
measured gain + alimiter 0.7, as loud as her; full screen 0-2.5 s.

**Echo:** on his last word "brain" (from 2.30 s of the bite): copies at +0.24 s (vol 0.55, highpass 200 / lowpass 3000),
+0.5 s (0.32, lowpass 2200), +0.78 s (0.18, lowpass 1500). "To your brain" repeats twice, quieter / darker, through the
black (2.5-3.0 s), ~9 dB under the voice. Done in three separate passes (not loudnorm inside asplit, which made his dry
line silent in the first final).

**Music:**
- Current (v2-v4): "Hope" by Yakov Golman, CC BY 3.0, Jamendo 1559870 (https://www.jamendo.com/track/1559870) via
  Openverse. Tags happy, peaceful, piano, speed_medium. earshot: "solo piano music ... uplifting and hopeful", no drums, no
  vocals. 2 min long; runs from 0; fade in 0.3 s, out over the last 0.8 s. Bed at -19 LUFS, sidechain-ducked under the
  voice (threshold 0.02, ratio 6, attack 20, release 380). File `sfx/music/hope_golman.mp3`. Credit line required:
  `Music: "Hope" by Yakov Golman, CC BY 3.0`.
- v1 (replaced): "Finding Hope" by Blindmoore, CC BY 3.0, Jamendo 1336230 via Openverse (earshot: "inspirational
  corporate background music"; Demucs vocals -54.6 dB; tempo 129.2). The band landed on "people" (the reveal); intro
  lifted 14 dB. Client: "the music it is little too fast is it for my niche".
- Client rule: calm music for her niche; calm solo piano accepted.
- Shortlists and candidates: see footage-and-assets.md (private memory skill).

**SFX:**
- Openverse searched first (`sfx/search/*.json`); all effect results were Freesound files and Freesound returned 403 to the
  cloud machine (site, API, files). The owner chose the CC0 OpenGameArt fallback (`../spin-bout-u-drake/assets/sfx/oga`,
  mapped in `build/sfx_sheet.py`), no credit needed.
- Kinds used and files: hit (100-cc0-sfx/hit_01.ogg); whoosh (swishes__swish-4 / -8, tube-plastic-whoosh-02);
  whoosh_big (qubodup-megaswosh1, 60009__qubodup__swosh_22); stamp (bfh1_hit_02); success (Audio__confirmation_001);
  scratch (Audio__scratch_003); rise (fantasy_magic_button_1); sparkle (bell_ding2); error (Audio__error_004); sub
  (sci-fi-sounds/Audio__lowFrequency_explosion_000); ding (ui-sounds/complete).
- Peak-normalised per kind (e.g. hit -7, whoosh -11, sub -5); whooshes pan-swept, others panned ±0.2.
- No whooshes on quick footage cuts (earshot flagged "salient hit density 2.0/s, high").
- v4 cue lists are in footage-and-assets.md (private memory skill).

## 10. Voice and language

- She speaks her own lines to camera, in English, with a handheld mic. No AI voice, no voiceover.
- Her messages to the agency mix English and Hindi (Hinglish); her reference reel had Hindi TV content.
- Tone of her lines: calm, caring doctor; second person ("Just ask yourself..."); rhetorical questions ("But can you
  afford it? Maybe not. Does it work? We don't know yet."). (Tone description is the export author's reading of the
  script, not a stated rule.)
- On-screen text and captions: English only, sentence case as spoken.
- Descriptions: plain text, no emojis (agency rule), numbered lists "1.", British spellings used in our copy
  ("criticise").

## 11. Formats, safe zones, naming, export, loudness

| Item | Value |
| --- | --- |
| Aspect / size | 9:16, 1080x1920 |
| Frame rate | 30 fps |
| Duration | Cut A (Deepinder open) 62.5 s; cut B (direct open) 59.567 s. Earlier: preview v1b 72.5 s, v2/v3 previews 67.7 s. |
| Codec | H.264 video ~10.77 Mb/s; AAC 48 kHz stereo ~195 kb/s (192k target) |
| Render command | `npx --yes hyperframes@0.8.203 render --quality high --video-bitrate 11M --sdr -w 3` (detached) |
| Mux | `build/sfx_mix.py` muxes the audio with video stream copy (AAC 192k, faststart) - no second video encode |
| Loudness master | two-pass loudnorm I=-14, TP=-2, LRA=11. Measured -14.0 LUFS, -1.8 / -1.9 dBTP |
| Verify | `verify_mix.py --target -14` (flags "NEEDS FIX" on its fixed -4 dBTP rule; accepted at the -2 dBTP house ceiling) |
| Size cap | Under 100 MB, no second encode (A 85,680,899 bytes; B 81,431,472 bytes) |
| File names | `nxtlvl_kokila-peace_reels_9x16_v<N>[_deepinder-open|_direct-open].mp4`; previews `preview_kokila-peace_reels_9x16_v<N>.mp4`; cover `nxtlvl_kokila-peace_reels_9x16_v1_cover.png` |
| HyperFrames | 0.8.203; `--sdr` (HDR pre-extraction needed 4.6 GB) |
| Safe zones | House rule for 9:16: text, faces and logos out of the top 250 px and the bottom 400 px, 60 px from each side. Cover checked against Instagram's 3:4 profile-grid crop (y 240..1680). Whether the reel itself was checked against the house safe zones: UNKNOWN. Note (uncertain): the "rf" caption position (top 1480) may reach into the bottom 400 px zone (y > 1520). |

## 12. Reference videos and footage, and what was used

- **Her reel DbVgs57zdhq (style reference):** matched its royal-blue pill captions, talking-head plus B-roll structure;
  "make it better" with split screen, our own graphics, 2-3 word pills, zoom-blur transitions, Openverse music + SFX,
  earshot check. Not copied: celebrity photos, TV clip, film clip (copyright). Its "Comment" CTA was not used (no CTA).
- **"Surrender reel"** (an earlier agency reel; owner: "take the surrender reel for some reference"): used for the split
  screen style. Its file location: UNKNOWN.
- **Raj Shamani podcast ("Figuring Out") with Deepinder Goyal**, owner's screen recording (mostly Hindi, a few English
  lines; picture "flat (log-like)", graded up). Used:
  - Cut A opening: his own line 47.15-49.65 s, "It's super easy and it measures blood flow to your brain." (2.62 s bite;
    2.75 s clip `pod_full`), full screen, with echo.
  - Silent B-roll under her lines: `pod_c` from 29.0 s (4.5 s), `pod_d` from 33.8 s (3.7 s); full-screen crops
    `pod_cF` / `pod_dF` from v3.
  - Cover still from 46.0 s.
  - Always credited "Source: Raj Shamani podcast" on screen and "Clip: Raj Shamani podcast with Deepinder Goyal" in the
    description. Each use kept short (4 s or less).
- **Pexels stock clips** (Pexels licence: free commercial use, no credit), fetched by id with `tools/pexels_fetch.py`.
  v4 uses only Indian people / no-person shots: 8632780, 7164569, 4763892, 10515013, 8811044, 4584772, 4334053, 8187787,
  5034858, 6956640. Full list per version with ids in footage-and-assets.md (private memory skill).

## 13. People in footage: religion-neutral, Indian people

- **Religion-neutral (client, voice note 2026-11-13):** she prefers neutral footage with no religious identity shown. No hijab, bindi, turban, cross or other religious
  marks.
  - Hijab couple clip 8135467 replaced (v2) by 8557555.
  - Bindi clips left out (9346274; 8811044 used only before the woman with a bindi comes in).
  - Turban husband in 4334053 cropped out (woman only).
- **"Neutral races" (owner relaying, 2026-11-13T14:32:23):** "try to use neutral races for the reference videos, dont add
  black or any other races" -> implemented as Indian people only in stock clips, or shots with no face (alarm clock,
  running legs, hands on laptop). Podcast clips unchanged.
- Limited free Indian footage means clips get reused (family dinner, father and son, laughing couple, upset woman).

## 14. Cover style

`renders/nxtlvl_kokila-peace_reels_9x16_v1_cover.png` (1080x1920), built by `build/cover.cjs` (Playwright screenshot of
HTML):
- Top: navy `#0E1A3A` with blue radial glow; headline Inter 800 86 px white: "Can an [₹85,000 on a yellow `#FFD23F` pill,
  navy text] device measure your [peace of mind? in yellow]".
- Middle panel (y 560-1180): Deepinder at 46.0 s of the recording, facing camera, mouth closed (crop 1346x773 at x 917;
  graded brightness .07 contrast 1.16 saturation 1.15 gamma 1.12); yellow ring around the Temple patch with yellow pill
  label "The Temple device"; credit pill "Source: Raj Shamani podcast".
- Bottom panel (y 1180-1920): Dr Kokila at 45.5 s of the cut, eyes to lens; white card "DOCTOR'S TAKE" (blue, uppercase,
  letter-spaced) / "Dr S Kokila" (navy 44 px). Seam lines blue-yellow-blue at y 556 and 1176.
- Fits the 3:4 grid crop (y 240..1680).
- OUTDATED: still the v1 yellow-highlight hook styling, not the v4 red-on-white. The assistant said on 2026-11-13: "The
  cover still works for both." No request to rebuild found. See open-items.md (private memory skill).
