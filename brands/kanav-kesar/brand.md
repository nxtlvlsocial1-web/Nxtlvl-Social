# Kanav Kesar: brand and style guide

> Public part of this client's memory: look and workflow only. The brief, feedback, scripts, footage list,
> hooks/CTAs, calendar and open items live in the private `nxtlvl-client-memory` account skill.

The look below is the look of his one ad so far, "Surrender" (project `surrender-ad-9x16`), final v4 approved by the
owner on 2026-11-06 ("everything else is perfect"). There is no separate brand kit for Kanav / The Conscious
Millionaire: treat this ad as the style reference.

*Sources: notes `/tmp/claude-0/-home-user-Nxtlvl-Social/b1c6bbee-7bc1-59ac-ac25-7b3da31f270a/scratchpad/notes_kanav.md` § 5 (style), § 2, § 9; `/home/user/Nxtlvl-Social/surrender-ad-9x16/build/generate.py`, `build/render_final.sh`, `build/music_bed.py`, `build/tight.py`; `/home/user/Nxtlvl-Social/.claude/skills/nxtlvl-social-video/SKILL.md`.*

## Index

1. [Logos and brand kit](#1-logos-and-brand-kit)
2. [Colours (hex)](#2-colours-hex)
3. [Fonts](#3-fonts)
4. [Layout and canvas](#4-layout-and-canvas)
5. [Captions (black-and-white Hinglish)](#5-captions-black-and-white-hinglish)
6. [Opening: glass Before/After screens and the text hook](#6-opening-glass-beforeafter-screens-and-the-text-hook)
7. [Motion graphics (liquid glass)](#7-motion-graphics-liquid-glass)
8. [Transitions](#8-transitions)
9. [CTA card](#9-cta-card)
10. [Overlays, grade, zooms](#10-overlays-grade-zooms)
11. [Sound effects](#11-sound-effects)
12. [Music](#12-music)
13. [Voice](#13-voice)
14. [Formats, safe zones, naming, export, loudness](#14-formats-safe-zones-naming-export-loudness)
15. [Reference videos and what was copied from each](#15-reference-videos-and-what-was-copied-from-each)
16. [Edit-style dos and don'ts](#16-edit-style-dos-and-donts)

---

## 1. Logos and brand kit

- Logo for Kanav Kesar / The Conscious Millionaire: UNKNOWN (none supplied, none used in the ad).
- Brand kit folder: none. `/home/user/Nxtlvl-Social/brands/` holds ai-nxtlvl, creators-100x, idigitalpreneur, nxtlvl,
  sports-science-technology, sucsess-maperrs; there is no Kanav / Conscious Millionaire kit.
- His brand colours and fonts: UNKNOWN. The colours and fonts below come from the reference reel the owner chose (the
  ElevenLabs girl reel's pink) plus our choices, not from a client brand book.
- The Nxtlvl Social website screenshot (`reference/nxtlvl_site.jpg`: "WHAT WE DO / Everything your brand needs.", purple
  glass cards Motion Graphics, Reels & Shorts, Creative Visuals, Brand Identity, Video Editing, Ad Creatives) was sent as
  a reference for the liquid-glass card look. Its purple was not used as a main colour (uncertain whether the magenta
  tint flash #d23cff was taken from it).

## 2. Colours (hex)

| Use | Value |
| --- | --- |
| Page background | `#f7b7c3` |
| Background radial gradient | `#fff4f6` -> `#ffd6de` -> `#f7a2b4` |
| Dot grid on the background | `rgba(190,40,80,.17)`, 26 px spacing |
| Dark text | `#3b0a1f` |
| Tag / hook near-black | `#1a0610` (kicker pill), `#160409` (hook lines) |
| Muted text | `#7a3a52` |
| Accent red/pink (main accent) | **`#ff2d55`** (also `#ff5a86`, `#ff7aa0`, `#ff4f7b`) |
| Seam line gradient (6 px) | `#ff2d55`, `#ff7aa0`, `#ff2d55` |
| Full-frame caption red (key words) | `#ff2d3d` |
| Script caption pink (intro captions) | `#ffd0dc` |
| Green (checks, growth arrow) | `#18b26b` |
| Dark glass | `rgba(90,10,40,.85)` |
| Bottom / full-frame fallback | `#2a0d14` |
| CTA yellow box | **`#e8ff2a`** with `#111` text |
| Seam caption box | `#000` with white text |
| Tint flash (screen blend) | `#d23cff` |
| White flash | `#fff8f0` |
| Light leak (warm) | `rgba(255,240,200)` -> `rgba(255,170,60)` |
| Glass fill | gradient `rgba(255,255,255,.62)` / `.2` / `.34`, 1.5 px white border, pink inner glow `rgba(255,80,130,.16)` |
| Grain overlay | 5% (`assets/img/grain.png`) |

## 3. Fonts

All in `surrender-ad-9x16/assets/fonts/`, copied from `spin-bout-u-drake-9x16` and the hyperframes-creative presets.

| Font | File | Used for |
| --- | --- | --- |
| Inter 500 | `inter-latin-500-normal.woff2` | small UI text |
| Inter 700 | `Inter-700.woff2` | intro captions inside the After screen (42 px) |
| Inter 800 | `inter-latin-800-normal.woff2` | seam captions (50 px), Before/After labels (62 / 104 px), hook kicker pill (40 px), card titles |
| **Anton** | `Anton.ttf` | big full-frame words (150 px), hook lines (92 px), CTA box |
| **Kaushan Script** | `KaushanScript.ttf` | small script word in full-frame captions (74 px), big pink script word in intro captions (84 px) |

Font licences: Inter, Anton and Kaushan Script are Google Fonts (SIL OFL) to our knowledge; not checked in the notes
(uncertain).

## 4. Layout and canvas

- Canvas 1080x1920, 30 fps, 9:16 (Reels). HyperFrames 0.8.203, one paused GSAP timeline. Generator `build/generate.py`
  writes `index.html`.
- Four section kinds: intro, split, full, cta. 15 sections (word indices from the Scribe transcript):
  `("intro",0,18), ("split",18,80), ("full",80,104), ("split",104,135), ("full",135,164), ("split",164,177),
  ("full",177,214), ("split",214,254), ("full",254,278), ("split",278,313), ("full",313,334), ("split",334,367),
  ("split",367,412), ("split",412,440), ("cta",440,None)`.
- **Intro**: two glass screens on the pink.
  - Before card: left 50, top 760, 380x676, desaturated (`saturate(.45) contrast(.9) brightness(1.06)`). Label "Before"
    (Inter 800, 62 px).
  - After card: left 460, top 500, 570x1013. Label "After" (104 px).
  - Both play `face_full.mp4`.
- **Split**: top half 1080x960 = glass motion graphics on the pink stage; bottom half 1080x960 = his face
  (`face_split.mp4`); a 6 px pink/red gradient seam line at y 957; seam caption at y 905.
- **Full**: his face full frame (`face_full.mp4`, a 608x1080 crop of the 1080p take scaled to 1080x1920); captions in the
  lower third (top 1250).
- **CTA**: full frame, punch-in from 1.8x, yellow box.
- Talking-head crops (the "talking head ratio" the owner later used as the reference for other videos):
  - 1080p source (final): face_full `crop=608:1080:717:0` -> 1080x1920 (unsharp 0.45); face_split
    `crop=1215:1080:412:0` -> 1080x960.
  - 720p source (v1 only): face_full 405x720 crop at x478 -> 1080x1920 (2.7x upscale, soft); face_split 810x720 at
    x275 -> 1080x960.

## 5. Captions (black-and-white Hinglish)

- Language: Hinglish written in Latin script. Scribe gave Devanagari words; generate.py's `ROMAN` dict maps them to
  romanised Hinglish. The name is forced to "Kanav" (word 181).
- **Seam captions** (split sections), the "black and white caption" copied from the ElevenLabs reel:
  - White Inter 800, 50 px, on a solid black box (`#000`), padding 12/24/14, radius 8.
  - Centred at y 905 (sitting on the seam line).
  - 1-3 words per caption (max 16 characters), lowercase as spoken (e.g. "hum bahut saare", "karta", "lekin jab mujhe",
    "tak aap scale").
  - Pop: scale 1.12 -> 1 in 0.16 s.
- **Full-frame captions**:
  - Small script word (Kaushan Script 74 px, white, lowercase) over a big word (Anton 150 px, uppercase, white with
    shadow; red `#ff2d3d` with a white offset shadow on key words). Example frame: "se / SEEKHI HAI".
  - Big word blurs and scales in, 1.3 -> 1 in 0.22 s.
  - Shrinks to fit 880 px (font-size min(150, 1780/len) px).
  - Never ends on a filler (FUNC list); filler-only chunks merge into the previous chunk; "J." is not a sentence end.
  - Red key-word indices `RED = {99, 100, 137, 168, 170, 182, 213, 268, 273, 275, 318, 319, 329, 402, 456}`
    (negative, belief, ego, past, future, Kesar, surrender., losses, trial, errors, approach, badal, ... surrender).
- **Intro captions** inside the After screen: Inter 700 42 px white line over Kaushan Script 84 px `#ffd0dc` word (e.g.
  "This is an / ad", "is going to / change", "your approach and your / perspective").
- The owner reuses this caption look for other talking-head clients ("use the black and white hinglish captions that we
  made for that surrender video", 2026-11-07T16:26:05Z).

## 6. Opening: glass Before/After screens and the text hook

- Copied from the ElevenLabs reel: two screens at the start, "Before" (small, desaturated, lower left) and "After"
  (large, right), both playing his face.
- v4 (owner 17:10:48Z "Give the starting two screens a liquid glass ui floating screen element"): floating liquid-glass
  panels.
  - Radius 46, 16 px glass frame, inner screen radius 32, diagonal sheen.
  - Rise from blur with a 3D tilt (rotationY 14 / -12 -> 8 / -6), float y -18 / -24 with yoyo.
  - **No notch** (a small notch existed in the v4 preview; the owner asked to remove it for the final, 17:50:33Z).
- v5 text hook (client request, 2026-11-16), placed in the empty pink area above the screens (the area the client
  circled):
  - `#hook` top 96 px, centred.
  - Kicker: dark pill `#1a0610`, white Inter 800 40 px, radius 18 ("For Coaches, Consultants, Experts" or "Coaches,
    Consultants, Experts").
  - Lines: Anton 92 px, line-height .98, uppercase, `#160409` with a white glow; second line red `#ff2d55`.
  - On screen from frame 0 ("it is the thumbnail too"), settles (scale 1.12 / 1.1 -> 1, stagger .08), exits with the
    cards at the end of the intro (~5 s; y -40, blur, 0.26 s).

## 7. Motion graphics (liquid glass)

- Pacing and smoothness from the Nxtlvl Social promo, restyled to the pink with a liquid-glass finish, in the top half
  of the split sections.
- Glass card: gradient `rgba(255,255,255,.62/.2/.34)`, 1.5 px white border, inner highlight, pink inner glow
  `rgba(255,80,130,.16)`, soft pink drop shadows, `backdrop-filter: blur(22px) saturate(1.7)`, diagonal sheen, radius 36.
- Entrance (final values, v2 onward): rise 90 px out of blur(16px), scale .86 -> 1, rotationX 18 -> 0, expo.out,
  **0.5 s** (v1 was 0.75 s).
- Icon pop on every card: `back.out(3)`, 0.35 s, 0.12 s after the card.
- Float: y -9, period **1.1 s** sine (v1 was 1.6 s).
- Exit: **0.22 s**, up 60 px + blur (v1 was 0.32 s).
- Top stage slow push: scale 1.06 -> 1.13 over each split.
- Short-lived elements enter faster so their exits always land: `d = min(d, max(.2, t1 - t0 - .3))`.
- Counters (92%, ₹25 crore, 100, ₹10 lakh) count with power3.out; lines and arrows draw with strokeDashoffset.
- Section graphics (text verbatim) are listed in `scripts-library.md` § 4.
- Rule: no element lingers; low chips sit above the seam caption (lowest element tops ~760 px on the stage); an overlap
  check script was used.

## 8. Transitions

Copied frame by frame from the ElevenLabs reel:

| Cut | What happens |
| --- | --- |
| Into a split | Face lands close (1.55x, blurred 10 px) and settles in 0.38 s; top screen 1.14x blurred -> 1 in 0.42 s |
| Split to split | Face 1.25x -> 1 (0.3 s); top slides in from x 140 with blur (0.4 s) |
| Split to full | Split zoom-blurs (1.22x, blur 16) 0.2 s; full frame lands from 1.18x in 0.3 s |
| Full to split | Two-frame magenta tint (`#d23cff`, .55), warm light leak sweeping, white flash .85 |
| Into CTA | Extreme punch-in (1.8x, 0.45 s), yellow line draws up (0.14 s) and opens into the box (0.24 s, back.out) |

The face never pulses: it moves only in these transitions.

## 9. CTA card

- Yellow box `#e8ff2a` tilted -6°, Anton, black text: "COMMENT" / '"SURRENDER"'. '"SURRENDER"' slams in (scale 1.7 -> 1).
- Below: "DETAILS IN YOUR DM" in yellow Anton, wipes in (clip-path, 0.35 s).
- Over his chest on the full-frame shot; holds 1 s on a still of his last frame (`assets/img/last_full.png`).
- SFX: riser_hit on the CTA, stamp on "SURRENDER".

## 10. Overlays, grade, zooms

- Footage grade: `eq=contrast=1.06:saturation=1.1:gamma=0.98,colorbalance=rs=0.02:bs=-0.03:rh=0.02`, lanczos scale,
  unsharp 5:5:0.45 on face_full.
- Grain overlay 5%.
- Light leak (warm) and white flash on full-to-split cuts; magenta tint flash.
- Zooms: only in transitions (1.55x, 1.25x, 1.22x, 1.18x, 1.8x CTA punch-in) and the slow push on the top stage. No zoom
  pulses on the face.

## 11. Sound effects

- The reference reel's exact SFX were not copied (cannot be separated from her voice/music; not licensed). CC0 sounds
  were placed the same way, following its "sound grammar".
- House rule is Openverse first, but Freesound downloads were refused from the cloud session, so the CC0 OpenGameArt
  packs were used (library built for Spin Bout U: `../spin-bout-u-drake/assets/sfx/oga`; credits
  `../spin-bout-u-drake/plan/sfx_credits_oga.json`). All CC0, no credit needed.
- Mapping (build/sfx_sheet.py KINDS):

| Kind | Where | Files |
| --- | --- | --- |
| whoosh_big | into splits | qubodup-megaswosh1.wav, 60009__qubodup__swosh_22.flac, sfx-cc0__tube-plastic-whoosh-01.wav, RPG swing; -6 dB, pitch -2 |
| boom | with whoosh_big into splits | Kenney lowFrequency_explosion_000 / 001, rubberduck bang_03.ogg; low-passed 300 Hz |
| whoosh | into full frames | swishes swish-4 / swish-8, tube-plastic-whoosh-02, RPG swing2, tin-whistle-whoosh-02 |
| swish | misc | swish-6, RPG swing3 |
| shimmer | colour flash | fantasy_magic_button_1.mp3 |
| hit | red words | untamedpixels impact_punch_medium |
| pop | motion elements (max one per 0.7 s) | plop_01 / plop_02.ogg, Kenney click_002 / tick_001, ui-sounds button1 / button2.ogg |
| notify | notification card | Kenney confirmation_001.ogg |
| cash | counters | coinsounds011015.wav |
| stamp | QUIT and "SURRENDER" | impact_punch_heavy |
| riser_hit | CTA | qubodup-megaswosh2.wav |

- Packs used (all CC0, OpenGameArt): wind-hit-time-morph (qubodup), sci-fi-sounds (Kenney), 25-cc0-bang-firework-sfx
  (rubberduck), swishes-sound-pack (artisticdude), fantasy-sound-effects-tinysized-sfx (Vehicle), rpg-sound-pack
  (artisticdude), fantasy-magic-spell (Almitory), 150-combat-sound-effects (untamedpixels), 100-cc0-sfx (rubberduck),
  interface-sounds (Kenney), ui-sounds (StumpyStrust), coin-sounds (syncopika).
- Final: 75 cues (whoosh_big 6, boom 6, pop 34, whoosh 8, hit 8, shimmer 5, notify 1, swish 2, stamp 2, cash 2,
  riser_hit 1), 31 distinct files, mixed with the real-sfx skill's `mix.py` under voice + music; SFX track -30.1 LUFS
  (true peak -9.2 dBTP per the v4 cue report).
- v1 preview had 85 cues (whoosh_big 7, boom 7, pop 39, whoosh 8, hit 10, shimmer 6, notify 1, swish 2, stamp 2, cash 2,
  riser_hit 1); v3 77 cues.
- Cue report warning: plop_02, click_002, button1, plop_01 used 6 times; tick_001, button2, fantasy_magic_button_1 5
  times (vary next time).

## 12. Music

- Track: "Young Black Rich (instrumental)" by **Melly Mike** (file `Young_Black_Rich_instrumental-Melly_Mike.m4a`,
  152.78 s), supplied by the owner. Commercial track; licence UNKNOWN (never answered; see `open-items.md`).
- 86.3 BPM, a bar is 2.78 s.
- Starts at **0:46** (45.95 s, a downbeat) per the owner.
- Final loop (v4, owner "loop the music from where it started"): 0:45.95 -> 2:12.12 (the last full-energy downbeat before
  the quiet outro), then back to 0:45.95; pieces `[(45.95,132.12),(45.95,68.88)]`; 80 ms triangular crossfades; 1.2 s
  fade-out on the bed. A soft dip is heard around 1:26 where it restarts (0:46 begins softly).
- v1 loop (replaced): from 0:46 looped on downbeats 2:03.78 -> 1:19.32 (16 bars), 40 ms crossfades.
- Level in the mix: music -19 dB, sidechain-ducked under the voice (threshold 0.04, ratio 5, attack 15 ms, release
  320 ms); final fade at 106.2 s for 1.3 s.

## 13. Voice

- His own voice from the take; no voiceover, no music-only sections.
- Language: Hinglish (Hindi + English), Scribe `language_code: "hin"`. Captions in romanised Hinglish.
- Processing:
  1. Tight cut: every pause quieter than -30 dB for >= 0.1 s cut to 0.08 s (90 Hz high-pass for detection, 8 ms audio
     fades at the joins).
  2. Repeated lines and filler "guys" cut (v2).
  3. **1.1x speed, pitch kept** (`setpts=PTS/1.1` + `atempo=1.1`) on picture and voice (v3, owner "fast forward the voice
     a little").
  4. `loudnorm I=-15, TP=-2, LRA=9`, padded to 107.5 s (`apad=whole_dur=107.5`) for the CTA hold.

## 14. Formats, safe zones, naming, export, loudness

| Setting | Value |
| --- | --- |
| Aspect / size | 9:16, 1080x1920 |
| Frame rate | 30 fps |
| Duration (final) | 107.5 s (video 106.5 s + 1 s CTA hold), 3225 frames |
| Codec | H.264 (x264 preset slow, CRF 18, profile high, yuv420p) + AAC 320k, `+faststart` |
| Bitrate cap (final) | `-maxrate 6.8M -bufsize 13.6M` (was 9M / 18M before the under-100 MB request) |
| Size cap | under 100 MB (final 95,061,561 B for 107.5 s; ~7.07-7.11 Mbps total) |
| Draft previews | x264 veryfast CRF 24, AAC 192k |
| HyperFrames render | `--quality delivery -w 3` (draft `--quality draft`) |
| Loudness (final) | -14.8 LUFS integrated, true peak -3.0 dBTP (v1 preview -14.9 / -3.2) |
| Preview names | `preview_surrender-ad_9x16_vN.mp4` / `preview_surrender-ad_9x16_vN_sfx.mp4` |
| Final names | `nxtlvl_surrender-ad_reels_9x16_vN_sfx.mp4`; hook versions `nxtlvl_surrender-ad_reels_9x16_v5_hook1_sfx.mp4` / `nxtlvl_surrender-ad_reels_9x16_v5_hook2_sfx.mp4` |

Safe zones as built:

- No notch on the opening screens (owner).
- Hook placed in the empty pink area above the screens (top 96 px), where the client circled.
- Chips kept above the seam caption (lowest element tops ~760 px on the stage).
- Full-frame captions at top 1250; seam captions at y 905.

Differences from the agency skill (`nxtlvl-social-video`), observed, not raised by the owner (uncertain whether they
matter for this client):

- Skill safe zone: keep text out of the top 250 px. The v5 hook sits at top 96 px (the client asked for the area above
  the screens).
- Skill length target for Reels 7-30 s (max 60 s). This ad is 107.5 s (the client's own 145 s take, accepted by the owner).
- Skill: CTA card held >= 1.5 s. Here the CTA hold after the last word is 1 s (the CTA box appears earlier, during the
  spoken CTA).
- Skill naming `<client>_<campaign>_...`: files use `nxtlvl` as the client slug, not a Kanav / Conscious Millionaire slug.
- Skill: deliver a 1-frame cover .png per format. Not done (the v5 hook frame is the thumbnail).

## 15. Reference videos and what was copied from each

| Reference | File | What was copied |
| --- | --- | --- |
| "The girl with the eleven labs reel" | `surrender-ad-9x16/reference/ref_elevenlabs.mp4` (upload `3a3bbd29-Video-28750.mp4`; 720x1280, 29.97 fps, 55.89 s) | The pink dotted background; the Before / After two-screen opening; the split layout (top screen, bottom face, black-box white caption on the seam); full-frame punches (script word plus a big Anton word, red on key words); its transitions frame by frame; the yellow COMMENT box CTA; its sound grammar (sound placement, with CC0 sounds) |
| "The second Nxtlvlsocial promo" | `surrender-ad-9x16/reference/ref_nxtlvl_promo.mov` (upload `d1190f83-6-Nov-2026-3-1793976383_8660622.mov`; HEVC 1280x720, 60 fps, 33.0 s) | The smoothness and pacing of its motion elements (cards rise out of a blur with a slight 3D tilt on expo curves, staggered, and float), in the top half; restyled to the pink with liquid glass |
| Nxtlvl Social website screenshot | `surrender-ad-9x16/reference/nxtlvl_site.jpg` (upload `611d38e5-image.jpg`) | Liquid-glass card look ("WHAT WE DO / Everything your brand needs.", purple glass cards) |
| Prior edit `conscious-millionaire_surrender_reels_9x16_v8.mp4` | `surrender-ad-9x16/assets/video/drive/orig_drive.mp4` | Nothing copied (it was sent by mistake as the source; it has its own graphics, captions and illustrated characters, footage inside a framed card) |

## 16. Edit-style dos and don'ts

Do:
- Tight, gapless speech; repeats and "guys" fillers cut; 1.1x speed with pitch kept.
- Pink dotted background, glass Before/After opening, split / full / CTA rhythm.
- Black-box white seam captions, script + Anton full-frame captions, red key words.
- Fast motion (0.5 s in, 0.22 s out), icon pops, float, slow push.
- A text hook on the opening screen from frame 0 (doubles as the thumbnail).
- Music from 0:46, looped back to 0:46.

Don't:
- Pulse, bounce or zoom the face outside the transitions.
- Add a name card or extra text when he introduces himself and his teacher.
- Let chips linger or sit on the seam line.
- Put a notch on the opening screens.
- Spell his name "Kanak".
- Export over 100 MB.
