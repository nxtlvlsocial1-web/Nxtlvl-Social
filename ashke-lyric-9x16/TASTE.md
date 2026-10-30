# TASTE: ashke-lyric-9x16

Updated 2026-10-30. Current version: final v4, renders/nxtlvl_ashke-lyric_reels_9x16_v4.mp4 (63 s: 60 s song + logo).

## 1. Brief
- 9:16 Ashke (Karan Aujla, Mxrci) lyric edit: 60 s from 2:14, 1080x1920, 30 fps.
- v3 follows the owner's second YouMotion reference ("COUNTRY STREETS ... RIDE YOUR OWN ROAD") as closely as we can:
  every detail, camera move, text style and animation.
- Footage: the owner's estate clip (1276x718) and Manchester tour clip (1200x720), used at close to native size.

## 2. Look (from the reference)
- Warm crumpled paper under soft diagonal window-blind shadows; sparse hand-drawn grid lines.
- Torn crumpled paper in red, black, grey and white, with the white core showing along the tear (build/scraps.py).
- Photocopied cut-out stickers of Karan with a white paper border and a soft shadow (build/cutouts.py, local
  segmentation with no upload).
- Black-and-white photo prints with a white border (build/cards.py); a red duotone print.
- Type: Oswald Bold caps.
  - Labels: black, white, red-on-white, red, red-and-black.
  - Stamped grunge words, white and red 3D words, a keyword filled with a photo, a ghosted repeat.
- Accents: blue marker circles and arcs, black and red stars, a small print paragraph, a flame doodle.
- End: "Ashke" on white tape between grid lines, circled (the reference's logo beat).

## 3. Motion and pacing (from the reference)
- 15 fps stepped, cuts on the beat grid (the reference runs at 90 BPM, the song at 89).
- Labels type on letter by letter behind a grey cursor block; the first label of a scene can slam in big and settle.
- Camera:
  - It whips into every scene and tracks each label as it lands.
  - It pushes in, pulls out, zooms into the photo-filled keyword and back, then whips out.
- One-step flashes: colour invert, white, and a black/white split.
- Nine scene recipes in the reference's own order; the hit lines use the photo-filled keyword (build/plan.py).

## 3b. Owner additions (2026-10-30)
- Prints open on the sharpest frame of their shot, held 8 frames, then run into the footage.
- Each scene change gets two single-frame stills (one 15 fps step each) right before the cut.
- One element per lyric line, drawn from what the line says, as a doodle sticker (build/icons.py), popping on the
  keyword with a stop-motion wobble.

## 3c. v4 (owner, 2026-10-30)
- Cut-outs: only the owner's six photos of Karan (coat by the car, red-wall mic, crowd mic, red profile silhouette,
  Bugatti, private jet), cut to Karan alone, fitted into each slot by height. The video prints, fills and
  single-frame transitions keep the Karan-only shots from the estate and tour clips.
- Hit lines: the photo-filled keyword is red and white on black torn paper, with the sticker below it, so it reads.
- Every caption is in Punjabi (Gurmukhi): labels, the paragraph, the title, the end tape, and a word tag on each lyric
  element. Font: Anek Gurmukhi (Condensed ExtraBold, 600), OFL. Letters type on by grapheme cluster.
- The Gurmukhi spelling of the lyrics is ours, word for word with the confirmed romanization (generate.py GURMUKHI).
- Sound (build/sound.py, all synthesized):
  - Music edit: muffled intro, cut-out gaps with risers and booms on the hit lines, stutters on the bursts, a tape
    stop into the logo.
  - Effects on the picture events: typing, slams, stamps, pops, marker, shutter, paper, whooshes, glitch, flash,
    tear, sparkle.
- Logo outro (60-63 s): a black torn sheet tears across, the owner's N mark draws on over night-violet, and the star
  pops and twinkles, framed by torn black paper.

## 4. Removed
- v2's full-bleed 9:16 cinema layer (eimantasbitinas23 reference): it blew the footage up and looked blurry.

## 5. Feedback rules
| Date | User said | Rule |
|---|---|---|
| 2026-10-30 | 9:16, cut and track like YouMotion, final quality | v1 |
| 2026-10-30 | add the eimantasbitinas23 style | v2 (then removed) |
| 2026-10-30 | remove that concept (blurry 9:16 crops), add clips from the two videos, follow the new reference closely, every detail | never blow footage up to full 9:16; follow references closely, not loosely |
| 2026-10-30 | best single frame then into the video, focus the transitions' frame pacing, one element per line from the lyrics | 3b above |
| 2026-10-30 | only Karan in cut-outs, crop nicely, dope frames; Punjabi captions; lyric elements; sound effects; edit the music; blend the logo at the end | 3c |
| 2026-10-30 | use these six photos for the image elements, keep the selected videos | cut-outs from the photos only |
