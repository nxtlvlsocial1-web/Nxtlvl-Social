# TASTE: ashke-lyric-16x9

Updated 2026-10-30. Current version: preview v1 (renders/nxtlvl_ashke-lyric_youtube_16x9_preview.mp4). Status: draft.

## 1. Brief and story
- Lyric video for "Ashke" (Karan Aujla, Mxrci), 60 s from 2:14 of the song, 16:9 1920x1080, 30 fps.
- An original animation inspired by the music video's world (old-money English estate: manor, Aston-style GT,
  polo, tea party, speedboat, luxury watch, chess, gold), NOT built from its footage. Mix of 2D and 3D.
- Pipeline A (code-drawn): HyperFrames + GSAP for 2D/type, Three.js for 3D (assets/js/world3d.js).

## 2. Theme and feel
- Mood: luxurious, confident, cinematic, playful-flex.
- Insane fast transitions + liquid-glass fluid motion; one 3D hero object per lyric section, camera cuts every 2 beats.
- Must not feel like: the music video re-cut, cheap neon, cluttered.

## 3. Visual system
- Palette: gold #f1cf7a (keywords, 3D gold, frame), cream #f6efe2 (lyric words), emerald #0f4a35, burgundy #7a1a28,
  dusk #121833 > #b4643c, champagne #fbf4e4, his-jacket tartan (navy #283c5c lines, mustard #c48c3e on #c9b48d).
- Type: keywords Playfair Display 900 italic 88 px (hero 150 px), gold with 1.5 px dark outline; other words Inter
  Display 600 54 px cream. Lyric cards: smoked liquid glass (blur 24, brightness .72), radius 46, sheen sweep.
- Frame: thin gold art-deco border with corner brackets; corner tag "Ashke / KARAN AUJLA" in glass.
- Finish: grain 8 %, vignette 45 %, letterbox bars only in the finale.

## 4. Motion
- Words blur in on their sung syllable (blur 14 > 0, y 24, 0.22 s expo.out); keywords type in per letter with a 3D
  flip (rotationX -80, stagger 35 ms) and a gold glow pulse. Cards grow from a pill (elastic) and melt away.
- Transitions: zoom-through (stage 1.9x + blur), whip (x 1100 + blur 24), gold slices (9 bars), liquid-gold gooey
  blobs, iris, flash, glass panes with 3D glass-shard bursts (also on "daaka", where the diamond shatters).
- 3D: camera cuts every 2 beats + punch-in 1.07x; beat nudges; kick shakes; light sweep on each new hero.

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
