# TASTE: ashke-lyric-16x9

Updated 2026-10-30. Current version: final v1 (v4 build: collage fusion + reference frame pacing), renders/nxtlvl_ashke-lyric_youtube_16x9_v1.mp4.

## 1. Brief
- Lyric edit for "Ashke" (Karan Aujla, Mxrci), 60 s from 2:14 of the song, 16:9 1920x1080, 30 fps. Lyrics confirmed.
- A fusion of the music video with the owner's collage references: YouMotion paper-zine lyric edit (look) and the
  J3nn1f3rJun1p3r punk collage (frame pacing: 12 fps stop-motion, scenes built piece by piece, texture-strip wipes).

## 2. Feel
- Punk-zine paper collage, black and white with red, sharp and very fast: footage cuts every half beat (5-frame cuts in
  the bursts), one scene per lyric line built up on the half beats, everything stepped (15 fps), hard edges, hard shadows.
- Must not feel like: a straight copy of one reference, a plain re-cut of the music video, glossy 3D.

## 3. Visual system
- Footage: the music video cut on the beat, synced shots keep lip-sync (MV time = edit time + 134.40), cutaways from the
  estate/tea party/Aston Martins/polo; photocopy look: grey, auto-levels per shot, contrast 1.75, double sharpen, fine
  fixed grain, stepped to 15 fps.
- Paper: procedural crumpled paper (build/paper.py), hand-drawn grid lines, torn paper edges top and bottom (no blur,
  no window-blind shadows).
- Texture panels per scene (build/textures.py + CSS): hazard stripes, halftone dots, line pattern, diamond plate, pixel
  blocks, greeked newsprint, grid; stair-step and slanted edges; starbursts, a barcode ticket, a road-sign arrow.
- Cards: the footage in a torn-edge card that changes size, tilt and edge on every cut; red #e3262e torn shape behind;
  every fourth layout red duotone (multiply); hit lines full-bleed; photocopied stills with white borders and hard shadows.
- Type: Bebas Neue labels (black / white / red tape, rotated, roughened with an SVG displacement filter), keywords in
  Oswald 700 caps 190 px red with a black offset shadow on a white starburst (or white on a red label), blue #2aa7d8
  hand-drawn circles; black 8-point stars. No caption of the line at the bottom.
- Title card: ASHKE circled + KARAN AUJLA · MXRCI label, at the start and at the end.

## 4. Motion
- Labels slam in from the side on their sung word (two stepped frames), keywords smash in from 1.7x; stop-motion boil at
  15 fps, harder on the beat; card bumps on every beat.
- Velocity strips (texture or ASHKE / KARAN AUJLA type) shoot across in five stepped frames with speed lines, every
  two beats, every half beat in the bursts.
- Line changes: eight texture strips land one frame apart (slanted, vertical or horizontal) then the new scene; paper
  tear; white flash; red flash into the full-bleed lines.

## 5. Sound
- The song section only (assets/audio/section.wav, -14 LUFS).

## 6. Technical
- python3 build/paper.py, build/textures.py, build/footage.py, build/audio.py, build/generate.py; renders detached (build/render_*.sh).
- The song, the music video, its stills and the cover art stay out of git (artist's material).

## 7. Feedback rules
| Date | User said | Rule |
|---|---|---|
| 2026-10-30 | music video is a reference, animate with our own 2D/3D | do not just cut lyrics onto the footage |
| 2026-10-30 | insane fast transitions + glass fluid, 2D+3D | (superseded by the collage reference) |
| 2026-10-30 | references 77393 / 7679: "make it like this" | (v2, then:) |
| 2026-10-30 | "looks straight up copy": fuse the music video with the collage reference | blend the real footage into the reference style; never copy one reference's elements one to one |
| 2026-10-30 | copy the J3nn1f3rJun1p3r frame pacing, sharper frames, more elements, no lyrics at the bottom, quicker strips, final quality | stepped frames, scene builds, strip wipes, velocity strips, no blur; never put a caption of the line at the bottom |
