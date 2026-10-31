# TASTE: spin-bout-u-drake

Updated 2026-10-31. Current version: final v2, renders/nxtlvl_spin-bout-u_reels_1x1_v2.mp4 (1080x1080, 20 fps, 60 s).

## Brief
- Spin Bout U (Drake & 21 Savage): 60 s from the 2:13 bass drop, the owner's lyrics, the owner's images (plan/assets.md).
- References: a Spin Bout U edit (square; the main look) and an MJ "Smooth Criminal" edit (extra effects). Follow both.

## Look
- Palette: near-black #191919, maroon #5f1b30, magenta #a3214c, off-white #f0f2f2 (sampled from the reference).
- Photos: hard black and white with a coarse 45-degree halftone screen (build/assets.py); cut-outs by local
  segmentation; the dumb white cat and Drake from behind go in whole (their cut-outs were not clean).
- Type:
  - Anton caps, huge and layered behind the subject.
  - Kaushan Script accents (Spin, Vogue, these days, baby girl) and Permanent Marker accents (girl, yeah, for real,
    snotty).
  - Tag boxes, magenta starburst badges, and corner credits typed on.
- Lyric references:
  - **Vogue lines:** the cat Vogue cover, and En Vogue for the '90s R&B group.
  - **Call lines:** an iPhone call screen, accepted for Vogue and declined for the ex.
  - **"Dumb":** the dumb white cat.
  - **"Globe":** our own wireframe globe with planes (the supplied one had a stock watermark).
  - **"End of the road":** a perspective road over the boat.
  - **"Baby girl":** the black cat.

## Motion and pacing
- Everything steps at 20 fps and the render is 20 fps, matching the references (18 and 20 fps, almost every frame
  unique).
- Element entrances:
  - Letters snap on one per frame.
  - Slide or zoom-blur entrances, starbursts spin in, scribbles draw on, and DROPPED's letters fall.
  - SMOKE blurs in and BURN flickers.
  - The hooks build as photo collages, one panel per sung word.
- Cuts rotate through zoom blur, white flash, horizontal smear, invert and a magenta sweep.
- The frame bumps on the half-time beat.

## Sound
- The song only, no sound effects.

## v2 (owner, 2026-10-31)
- Every cuss word (ass, hoes, the n-words, shit'll) is shown only as a blurred ****.
- No corner credits or "edited by" text.
- Each owner photo is used once. Every other line has its own 3D render (assets/js/g3d.js): the ex's phone, the
  globe, the road, 3D hook words, diamonds, smoke, a burning city block, a chrome heart, exploding BODY, a tissue
  box, and the 3D logo.
- The 3D is pre-rendered by build/render3d.cjs. Headless SwiftShader WebGL deadlocks with page screenshots, so the
  frames are read back from the canvas into MP4s on the scene's own colour.
- Reference cuts: whip-smear with a light streak, zoom blur to white, circle reveal, perspective tilt, vertical drop
  blur, sliding strips, white swoosh, spinning card zoom-up, invert.
- Motion tracking: three depth layers per scene ride one camera path (background .35, subject and attached words 1,
  overlay type 1.45). Text letters arrive as tilted blocks.
- Every caption has an outline in the opposite tone, so nothing disappears on white.

## Feedback rules
| Date | User said | Rule |
|---|---|---|
| 2026-10-31 | blur all cuss words as ****; unique picture per lyric, 3D renders allowed; match the reference transitions and tracking; fix text hidden on white; no edited-by credits | v2 above |
