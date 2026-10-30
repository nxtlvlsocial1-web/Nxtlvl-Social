# TASTE: ashke-lyric-16x9

Updated 2026-10-30. Current version: preview v2 (reference style) (renders/nxtlvl_ashke-lyric_youtube_16x9_preview.mp4). Status: draft.

## 1. Brief and story
- Lyric video for "Ashke" (Karan Aujla, Mxrci), 60 s from 2:14 of the song, 16:9 1920x1080, 30 fps.
- An original animation inspired by the music video's world (old-money English estate: manor, Aston-style GT,
  polo, tea party, speedboat, luxury watch, chess, gold), NOT built from its footage. Mix of 2D and 3D.
- Pipeline A (code-drawn): HyperFrames + GSAP for 2D/type, Three.js for 3D (assets/js/world3d.js).

## 2. Theme and feel (v2, after the owner's references Video-77393 and Video-7679)
- Minimal and graphic: cream paper or warm black, one orange accent, one hero per lyric line (about 1.5 s each).
- Must not feel like: the music video re-cut, colourful gradients, generic 3D props, clutter.

## 3. Visual system
- Backgrounds: cream paper radial #f2ede5 > #b9b1a5; warm black radial #2a1d19 > #070505; vignette; grain 10 %.
- Accent: orange #ff5a1f (#cc3f0a on cream for text contrast). Text cream #efe9df / ink #17110f.
- Type: Outfit 600 54 px typed lines with a blinking caret; Outfit 800 250 px huge single words between dashed orange
  guide lines; Outfit 800 132 px keyword with a cream block cursor; Mrs Saint Delafield script accents and signature;
  Playfair Display 900 italic for the 3D hero words (Ashke, Jatt, Daaka, Zehri).
- 3D pixel icons (build/icons.py, voxels with a black outline): eye, sunglasses, car, shoe, shield, stones, shirt,
  teacup, trousers, wheel, heart, diamond, ring, falcon, snake, crown, chain, king, watch; dotted orange halftone halos.
- Halftone planets (assets/js/halftone.js): orange dot spheres with noise texture and a dotted halo.

## 4. Motion
- Icons assemble from flying voxels, pop with overshoot, sway, beat-pulse; fx: roll, drive, slide (row), fly,
  orbit ring, explode (stones on "paadh", diamond on "daaka"), get stolen (heart slides off on "chori").
- Hand-drawn orange scribble circles around keywords; 8-bit cursor clicks keywords; glitch lines; light arcs orbit
  the 3D hero words.
- Transitions: pixel mosaic, halftone dot wipe, orange wedge, black hole with orange rim, orange starburst, glitch
  bars, flash; every shot punches in 1.06x.

## 5. Sound
- The song section only (assets/audio/section.wav, -14 LUFS), no added SFX.

## 6. Technical
- python3 build/audio.py, python3 build/generate.py; check: npx hyperframes@0.8.203 check.
- Renders detached: build/render_preview.sh, build/render_final.sh.
- The song, the music video and the cover art stay out of git (artist's material).

## 7. Feedback rules
| Date | User said | Rule |
|---|---|---|
| 2026-10-30 | the music video is a reference, animate it with our own 2D/3D | never cut the reference footage in; build original scenes in its world |
| 2026-10-30 | insane fast transitions + glass fluid animations, 2D and 3D mix | transition on every scene change, camera cut every 2 beats, liquid-glass UI |
| 2026-10-30 | (references Video-77393, Video-7679) "make it like this" | cream/black + one orange accent, typed lines with caret, 3D pixel icons, halftone, scribble circles, script, glitch/mosaic/burst transitions |
