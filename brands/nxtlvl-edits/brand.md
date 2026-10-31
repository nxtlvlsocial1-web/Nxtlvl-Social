# nxtlvl edits brand kit

The editing account of Nxtlvl Social, on Instagram as `@nxtlvlledits`. The logo is a symbol only, with no lettering.

**Logo: the N Disc** (concept Y, see `README.md` for how it was chosen). A solid disc with the N and the four-point
star cut out of it, like a coin or a seal. The N is the refined line from the Nxtlvl family: two uprights, two round
turns and a straight diagonal, the right upright climbing past the left (the next level) and tapering to a point under
the star. Because the N and the star are cut out, whatever is behind the disc shows through them.

`kit-preview.png` shows the whole kit on one page.

## Files

| File | Use |
|---|---|
| `profile.svg` / `png/profile-1080.png`, `png/profile-320.png` | Instagram profile picture (square; Instagram crops the circle) |
| `mark-pearl.svg` / `png/mark-pearl-1024.png` | The disc in pearl: on black, dark backgrounds, footage and video end cards |
| `mark-white.svg` / `png/mark-white-1024.png` | White: on violet or busy photos, watermarks on edits |
| `mark.svg` / `png/mark-1024.png` | Ink: on white or light backgrounds |
| `mark-violet.svg` / `png/mark-violet-1024.png` | Violet: on light backgrounds when you want colour |
| `icon.svg` / `png/icon-1024.png`, `icon-512.png`, `icon-192.png`, `icon-180.png` | App icon, WhatsApp Business, link-in-bio pages |
| `favicon.svg` / `png/icon-64.png`, `icon-48.png`, `icon-32.png` | Small sizes: a heavier cut on an Ink circle so it reads on light and dark tabs |
| `png/highlight-cover.png`, `png/highlight-cover-star.png` | Instagram story highlight covers (1080 × 1920; the centre shows) |

All SVGs are pure vector, so they open in Canva, Figma, Illustrator and any browser. The mark PNGs have transparent
backgrounds (the N and star are see-through).

## Colour

The Nxtlvl Social palette, used quietly.

| Name | Hex | Use |
|---|---|---|
| Ink | `#05030C` | Profile and dark backgrounds (with a faint `#110A24` lift in the middle) |
| Ink text | `#0B0816` | The disc on light backgrounds |
| Pearl | `#C9AEFF` → `#FFFFFF` → `#E4D3FF` → `#FFFFFF` → `#B794F6` | The disc's sheen on dark |
| Violet | `#7D18FC` | The colour disc on light |
| Mist | `#F5F2FF` | Light backgrounds |

## Rules

- Pearl or white on dark and photo backgrounds; Ink or violet on light.
- Keep the disc round and the cut-out intact: don't fill the N, add outlines, shadows or glows, or stretch it.
- Below 64 px use `favicon.svg` / `png/icon-64.png` and smaller.
- Clear space: a quarter of the disc's width on every side.
- Rebuild everything with `cd source && python3 final.py`.
