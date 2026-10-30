# TASTE: ashke-lyric-9x16

Updated 2026-10-30. Current version: final v2 (collage + cinema fusion), renders/nxtlvl_ashke-lyric_reels_9x16_v2.mp4.

## 1. Brief
- 9:16 version of the Ashke (Karan Aujla, Mxrci) lyric edit: 60 s from 2:14 of the song, 1080x1920, 30 fps.
- Look: the 16x9 v4 collage fusion. Cutting and camera: copied from the owner's YouMotion reference.

## 2. Cutting and camera (measured from the reference, frame by frame)
- 15 fps stop-motion: every frame is held twice.
- One scene per lyric line, each with a hard cut. Footage cuts on the beats inside a line, never closer than about
  0.55 s; half beats only in the bursts.
- Virtual camera over one big paper sheet (build/paper.py, 2600x3900). It moves in four ways:
  - Whip in: about 470 px, expo ease-out over 0.45 s, with a 4 degree rotation that settles.
  - Word tracking: the camera follows each label as it lands (power3 out, 0.3 s).
  - Hold: a slow drift or a push-in while the line holds.
  - Whip out: accelerates about 360 px over the last 0.2 s, along the next scene's direction, so the cut reads as
    one whip pan.
- Mostly down the page, sometimes sideways or diagonal.
- Hit lines zoom through their keyword into the cut.
- Type-only lines (5): the words run down the page, and the camera tracks them word to word at 1.22x.
- Cut accents: mostly clean whips. Now and then a white or near-black frame; a red flash into the hit lines.

## 2b. Cinema layer (eimantasbitinas23 reference, build/cine.py)
- On the hit lines (3, 12, 19, 26), the bursts (7, 24), the intro and the ending, the collage gives way to full-bleed
  footage cropped to 9:16 around Karan.
- Grades: red monochrome, film colour (teal shadows, warm highlights, heavy grain), one-bit threshold, silver B&W.
- Motion: smooth at the full frame rate, with a handheld drift and a slow push. The collage stays stepped at 15 fps.
- Hit lines open with black title cards (Inter Display, white): card, then a threshold footage flash, then the card
  again. They hold with a red picture-in-picture still, glass shards, torn paper slivers and a VHS scan line, then
  zoom through the keyword.
- Bursts are flurries of 4-frame cuts that cycle the grades.
- Torn paper rips with a photocopied still tear back into the collage. A red iris closes into the red segment.
- Lines 10 and 17 are a stop-motion photo grid of colour stills on white paper.

## 3. Visual system
- Same as 16x9 v4: photocopied music video in a torn card (on top, below, or full width), red torn shape, texture
  panels, starbursts, stills with white borders, the barcode ticket, the road-sign arrow, velocity strips.
- Hard edges and hard shadows, no blur, no caption of the line at the bottom.

## 4. Technical
- Build order (python3): build/paper.py, build/textures.py, build/footage.py, build/audio.py, build/generate.py.
- Renders run detached (build/render_final.sh).
- The song, the music video, its stills and the cover art stay out of git (artist's material).

## 5. Feedback rules
| Date | User said | Rule |
|---|---|---|
| 2026-10-30 | 9:16, plan the cutting and motion tracking exactly like the YouMotion reference, final quality | measured camera grammar above; final straight away |
| 2026-10-30 | add the eimantasbitinas23 style, plan clips and frame pacing like it, combine both | cinema layer above (v2) |
