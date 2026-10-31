# TASTE: spin-bout-u-drake

Updated 2026-10-31. Current version: v3 in preview (renders/preview_spin-bout-u_1x1_v3.mp4); last final v2.

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

## v3 (owner, 2026-10-31)
- Follow the MJ "Smooth Criminal" reference (sushiismissing) above all: black / white / red, cream script; subject
  with a cream outline and red offset rim; red energy slashes boiling round it; condensed red type behind, fat
  italic type on diagonal bands, cream brush script written on with a light spark; white X marks.
- Cuts from the reference: smear, zoom-out blur into a red ink burst and an inverted frame, red smear into a white
  radial burst, slice glitch, red blooms into a white negative and a flare, light burst with a red band, vertical
  scroll blur, defocus into a washed-out negative, smoke burst, zoom to white at the end. Inverted frames are grey.
- No constant camera shake. Scenes drift in slowly; beats land as punch-ins and single flashes.
- Pictures: the cats only in the opening (Vogue cover, pearl cat, dumb white cat); Drake photos at most twice
  (title, front row); every later line is an anime illustration that tells the story of one couple.
- Illustrations must look like real 1990s TV anime frames: simple 90s character design, flat two-tone cel
  paint, painted backgrounds, VHS softness and grain; the same couple kept consistent with a reference image. Both
  the glossy webtoon set and the clean modern cel set were rejected as "AI slop" (too detailed and polished).

## v4 (owner, 2026-10-31)
- The illustrations must move, not sit still: wind in hair and clothes, breathing, flowing smoke and fire, light
  sweeps, particles. Done in the browser (SVG displacement maps from build/animaps.py), no shake.
- Type and cuts follow the Spin Bout U reference again (see the v4 docstring in build/generate.py); the MJ look of
  v3 read as dull. Palette black / maroon / magenta / off-white; fonts Anton, Archivo Black, Dela Gothic One,
  Kaushan Script.

## v5 (owner, 2026-10-31)
- The anime must really act (expressions, the couple interacting), not just warp: the owner's Canva Image-to-Video
  clips (prompts in plan/anime_video_prompts.md) replace the stills where they exist (jealous, road, her, him, fire,
  spin; the Canva limit stopped the rest).
- AI video reads smooth and "slop"-like: build/clips90.py holds every clip on threes (8 drawings a second) and gives
  it a 90s broadcast look (soft 480-line picture, colour bleed, faded warm colour, light vignette, live grain). The
  still scenes' wind and breathing step on threes too.

## v9 (owner, 2026-10-31)
- Structure from the owner's Ashke edit (../ashke-lyric-9x16, square in ../ashke-lyric-1x1), colours from this edit:
  build/collage.py is the Ashke engine ported (one paper sheet the camera travels over, nine scene recipes per lyric
  line, typed labels with a cursor block, slammed and stamped words, 3D words, a picture-filled keyword with a 2.6x
  zoom, torn scraps, cut-out stickers with paper borders, photo prints, a doodle per line, single-frame stills before
  cuts, invert / white / split flashes, the spline camera with whips, motion blur and beat punches, 15 fps steps).
- Recoloured: maroon crumpled paper, magenta / black / maroon / off-white scraps, white marker circles, Anton type.
- Swooshes stay out (owner: they did not look good).
- v10: no grid lines. Behind the collage a lively gradient in screen space (soft magenta, hot pink, plum and maroon
  blobs drifting on slow loops, a little brighter on each beat) under the paper's crumple shading, which travels with
  the camera, so the sheet floats over moving colour.

- v11: the anime pictures the owner sent back are out (crew, point, diamonds, smoke, fire, spin, spirit,
  him_smitten). Lyric concepts take their place: footsteps marching with a 1-10 counter (ten toes), a GPS route with
  pins dropping on each "go" and a snapping compass (wherever I say go), shockwaves under the 3D diamonds (dropped),
  rings off the 3D heart, wisps out of the 3D BODY. The Vogue call screen is phone-shaped with the name on it; the dumb cat has its own
  spot. After Effects finish: harder whips, a zoom snap into every scene, bigger beat punches, a bloom and RGB split
  on about 60% of cuts, light-leak sweeps, mid-scene bloom pulses.
- Lines that say something physical happen to the whole screen (owner: no 3D render for burn, burn the whole
  screen; same for every such line): smoke a top fills the frame with procedural smoke, burn somebody block sends a
  fire front up the whole screen that leaves it charred with embers, dropped drops the whole frame out and slams it
  back with a white hit, comin' out my body lifts a ghost of the whole picture. These layers are pinned to the
  screen but sit under the lyric labels, so the words stay readable.

## Feedback rules
| Date | User said | Rule |
|---|---|---|
| 2026-10-31 | blur all cuss words as ****; unique picture per lyric, 3D renders allowed; match the reference transitions and tracking; fix text hidden on white; no edited-by credits | v2 above |
| 2026-10-31 | cats only at the start; 3D renders look mid; more motion and story built round the lyrics; don't repeat Drake photos; anime-style illustrations (not fully 3D); transitions up to the MJ reference; remove the constant shaking | v3 above |
| 2026-10-31 | the first anime images look like AI slop; make them better (owner bought Canva Pro) | 90s hand-painted cel style, consistent couple |
| 2026-10-31 | the Canva images still look AI slop; make them look like 90s anime | regenerated as 1993 TV-episode frames |
| 2026-10-31 | the images are still, animate them so they feel lively; fonts and transitions feel dull, take the Spin Bout U reference | v4 above |
| 2026-10-31 | his smile in the dance picture looks creepy | redone with a calm closed-mouth smile |
| 2026-10-31 | the art must act live (expressions, interaction), not a warp effect | Canva Image-to-Video clips |
| 2026-10-31 | the clips look a little AI; lower the frame rate and add a 90s anime filter | clips90.py: on threes, broadcast look |
| 2026-10-31 | remove the swoosh sounds; transitions still basic; bring the 3D globe and other 3D elements in with the characters | v8: song only, 3D with the art, layered cuts |
| 2026-10-31 | use the Ashke edit as the reference for the structure, keep the current colour theme | v9: build/collage.py |
| 2026-10-31 | remove the grids, add a lively gradient background so it feels immersive | v10 above |
| 2026-10-31 | Vogue name missing on the call screen; dumb cat hidden; more motion tracking and faster transitions; remove the attached anime pictures and build lyric visual concepts; random bloom on transitions; After Effects feel | v11 above |
| 2026-10-31 | don't add the 3D city for burn, burn the whole screen; same for all such context lyrics | full-screen smoke, burn, drop, ghost |
