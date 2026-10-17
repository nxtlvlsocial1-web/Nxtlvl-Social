# Unrest launch: design spec

Brand truth: `../brands/unrest/brand.md`. This file adapts it for the 15 s launch film.

## Concept

A pulse of light becomes a campus. One white dot grows into every idea (icons, a network, a crowd) and collapses back
into the logo. The beat flips the frame between black and white, so contrast is the motion.

## Palette (exact; no other values)

- `--ink: #000000`, `--paper: #FFFFFF`.
- Inversions use a full-frame white layer with `mix-blend-mode: difference` toggled on beat hits.

## Type

- Display: Space Grotesk 700, letter-spacing −0.045em, line-height 0.86, uppercase for section words.
- Outline emphasis: `color: transparent; -webkit-text-stroke: 5px currentColor` (stroke scales with size).
- Small labels / metadata: Space Grotesk 500, 26–34 px, letter-spacing 0.18em, uppercase.
- Logo tagline: Liberation Serif regular (matches the logo).

## Frame system (1920×1080)

- 96 px outer margin. Corner metadata pinned to the margins: top-left section index ("01 — DISCOVER"), top-right
  "UNREST / DU", bottom-left a beat counter, bottom-right "unrestdu.in". 3 px hairline rules.
- Section words are huge, 70–80% of frame width, centred on the lower third or the middle.
- Line icons: 10 px stroke, square caps, no fills unless a shape is solid on purpose.

## Motion

- Snappy: entrances `expo.out` / `back.out(2.2)` in 0.18–0.35 s; exits are hard cuts, never fades.
- Every beat (0.5 s at 120 BPM) has a hit: a pop, a slam, a flip or an inversion.
- Impacts shake the camera for 4 frames (deterministic offsets: 14, −10, 6, −3 px).
- Morphs use scale-swap with overshoot; lines draw with stroke-dashoffset.
