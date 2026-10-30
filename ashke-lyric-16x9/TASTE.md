# TASTE: ashke-lyric-16x9

Updated 2026-10-30. Current version: preview v3, collage fusion (renders/nxtlvl_ashke-lyric_youtube_16x9_preview.mp4). Status: draft.

## 1. Brief
- Lyric edit for "Ashke" (Karan Aujla, Mxrci), 60 s from 2:14 of the song, 16:9 1920x1080, 30 fps. Lyrics confirmed.
- A fusion of the music video with the owner's collage reference (YouMotion paper-zine lyric edit).

## 2. Feel
- Punk-zine paper collage, black and white with red, very fast (a cut on every beat, half beats in bursts).
- Must not feel like: a straight copy of one reference, a plain re-cut of the music video, glossy 3D.

## 3. Visual system
- Footage: the music video cut on the beat, synced shots keep lip-sync (MV time = edit time + 134.40), cutaways from the
  estate/tea party/Aston Martins/polo; photocopy look: grey, auto-levels per shot, contrast 1.6, sharpen, grain.
- Paper: procedural crumpled paper (build/paper.py), hand-drawn grid lines, window-blind shadows (multiply, blurred,
  drifting), torn paper edges top and bottom.
- Cards: the footage in a torn-edge card that changes size, tilt and edge on every cut; red #e3262e torn shape behind;
  every fifth card red duotone (multiply); hit lines full-bleed; photocopied stills as small secondary cards.
- Type: Bebas Neue labels (black / white / red tape, rotated, roughened with an SVG displacement filter), keywords in
  Oswald 700 caps 190 px red with a black offset shadow (or white on a red label), blue #2aa7d8 hand-drawn circles,
  Special Elite typewriter caption of the whole line; black 8-point stars.
- Title card: ASHKE circled + KARAN AUJLA · MXRCI label, at the start and at the end.

## 4. Motion
- Labels snap in on their sung word (steps easing, scale 1.25 > 1); stop-motion boil at 12 fps, harder on the beat.
- Cut transitions: hard cuts with a card punch-in; line changes: paper-tear wipe, white flash frame, red flash.

## 5. Sound
- The song section only (assets/audio/section.wav, -14 LUFS).

## 6. Technical
- python3 build/paper.py, build/footage.py, build/audio.py, build/generate.py; renders detached (build/render_*.sh).
- The song, the music video, its stills and the cover art stay out of git (artist's material).

## 7. Feedback rules
| Date | User said | Rule |
|---|---|---|
| 2026-10-30 | music video is a reference, animate with our own 2D/3D | do not just cut lyrics onto the footage |
| 2026-10-30 | insane fast transitions + glass fluid, 2D+3D | (superseded by the collage reference) |
| 2026-10-30 | references 77393 / 7679: "make it like this" | (v2, then:) |
| 2026-10-30 | "looks straight up copy": fuse the music video with the collage reference | blend the real footage into the reference style; never copy one reference's elements one to one |
