# nxtlvl edits brand kit

The editing account of Nxtlvl Social, on Instagram as `@nxtlvlledits`. The logo is the N on its own; the lettered
versions (`logo*.svg`, "nxtlvl edits") are kept for later and aren't in use yet.

**Logo: the Monoline N, Pearl** (concept R1, see `README.md` for how it was chosen). One fine line draws an N from two
uprights, two round turns and a straight diagonal. The right upright climbs past the left (the next level) and tapers
to a needle point, with the four-point star just above it, as if the line ends in a spark. Wordmark: "nxtlvl" in the
original Nxtlvl logo lettering, then "edits" in Instrument Serif Italic with the star over the i.

`kit-preview.png` shows the N kit on one page.

## Files

| File | Use |
|---|---|
| `profile.svg` / `png/profile-1080.png`, `png/profile-320.png` | Instagram profile picture (square; Instagram crops the circle) |
| `logo-pearl.svg` / `png/logo-pearl@4x.png` | Main logo on dark backgrounds and video end cards |
| `logo.svg` / `png/logo@4x.png` | On white or light backgrounds (Ink with a violet star) |
| `logo-pearl-stacked.svg`, `logo-stacked.svg` (+ `@4x.png`) | Square spaces: covers, stickers, merch |
| `logo-mono-white.svg`, `logo-mono-black.svg` (+ `@4x.png`) | One colour: watermarks on footage, print, stamps |
| `mark-pearl.svg`, `mark.svg`, `mark-white.svg`, `mark-black.svg` (+ `png/*-1024.png`) | The N alone, when the name is already next to it |
| `icon.svg` / `png/icon-1024.png` … `icon-180.png`, `icon-192.png` | App icon, WhatsApp Business, link-in-bio pages |
| `favicon.svg` / `png/icon-64.png`, `icon-48.png`, `icon-32.png` | Small sizes: a heavier line and a bigger star so it still reads |
| `png/highlight-cover.png`, `png/highlight-cover-star.png` | Instagram story highlight covers (1080 × 1920; the centre shows) |

All SVGs are pure vector (text outlined), so they open in Canva, Figma, Illustrator and any browser without fonts.
The logo PNGs have transparent backgrounds.

## Colour

The Nxtlvl Social palette, used quietly.

| Name | Hex | Use |
|---|---|---|
| Ink | `#05030C` | Profile and dark backgrounds (with a faint `#110A24` lift in the middle) |
| Ink text | `#0B0816` | Line and lettering on light |
| Pearl | `#C9AEFF` → `#FFFFFF` → `#E4D3FF` → `#FFFFFF` → `#B794F6` | The line's sheen on dark |
| Mist | `#F5F2FF` | Lettering on dark, light backgrounds |
| Pale | `#D8BBFF` | The star over the i, on dark |
| Violet | `#7D18FC` | The stars on light; one-colour white logo sits on it |

## Rules

- Use the pearl versions on dark or photo backgrounds, the Ink/violet versions on light.
- Keep the line fine: don't add strokes, outlines, shadows or glows, and don't stretch or rotate it.
- Below 64 px use `favicon.svg` / `png/icon-64.png` and smaller (the heavier small-size line).
- Clear space: half the N's height on every side.
- Rebuild everything with `cd source && python3 final.py`.
