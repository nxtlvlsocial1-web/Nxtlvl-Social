# nxtlvl edits: logo concepts

Logo concepts for the new editing account (Instagram handle given as `nxtlvlledits`). They're built from the Nxtlvl Social
family: the Shooting Star, the Smooth N, the original "nxtlvl" lettering and the violet palette, with an editor's cut.

The comparison sheets show each concept as the Instagram profile picture, at full size and at 110 / 56 / 32 px, with
a lockup: **`concepts-preview.png`** (round 1, A to D), **`concepts-preview-2a.png`** (E to H),
**`concepts-preview-2b.png`** (I to L), **`concepts-preview-3a.png`** (M to P) and **`concepts-preview-3b.png`** (Q to T).

Round 1:

| Concept | Idea |
|---|---|
| **A · Cut Star** | The Nxtlvl star, sliced by two razor cuts through all three trails, like one cut through every track of a timeline. The closest sibling to the main account. |
| **B · Clip N** | The Smooth N from the Nxtlvl logo, cut into three clips. |
| **C · Timeline Steps** | Three clips on a timeline, each track a step higher (the next level), cut by a star-headed playhead. |
| **D · Wordmark** | "nxtlvl" over "edits" inside camera viewfinder corners with a REC dot. |

Round 2 (more variations):

| Concept | Idea |
|---|---|
| **E · Play Star** | A rounded play button in the brand gradient with the star cut out of it. |
| **F · Film nx** | A film frame with sprocket holes and "nx" (original lettering) in the window. |
| **G · ne Monogram** | The "n" from the nxtlvl lettering with a serif "e" biting into it. |
| **H · Star in Frame** | The Shooting Star inside camera viewfinder corners with a REC dot. |
| **I · Beat Bars** | Audio levels climbing to the next level; the tallest bar wears the star. |
| **J · Clapper** | A clapperboard in the brand violet with the star on the board. |
| **K · Violet Stack** | D's wordmark without the frame, white on full violet. |
| **L · Cut Star, Light** | A's Cut Star in violet on a light ground. |

Round 3 (minimal and classy: flat colour, no glow, one violet accent at most):

| Concept | Idea |
|---|---|
| **M · Serif e** | One italic "e" in the serif, Mist on Ink, with a tiny violet star. |
| **N · Seal** | A fine double ring with NXTLVL · EDITS set around it and the star at the centre. |
| **O · Split Star** | The star cut once on the diagonal, its halves slipping along the cut. Ink on Mist. |
| **P · Editorial Stack** | "nxtlvl" small over "edits" large, Ink on Mist, like a masthead. |
| **Q · Sliced edits** | The word "edits" with one hairline cut through it, the top half nudged over. |
| **R · Monoline N** | The Smooth N as a single fine line, with the violet star at its tip. |
| **S · ne Ligature** | "ne" in the serif, set tight on flat night violet. |
| **T · Cut Line** | A timeline as one line with a single cut, and the star above the cut. |

Every concept shares one wordmark: "nxtlvl" in the original logo lettering (traced from `website/logo.png`), then "edits" in
Instrument Serif Italic with the four-point star over the i.

## Files

`concepts/<concept>/`:

| File | What |
|---|---|
| `profile.svg`, `profile-1080.png` | Instagram profile picture (square; Instagram crops the circle, everything sits inside it) |
| `lockup.svg`, `lockup.png` | Mark + wordmark on one line, on Ink |

The SVGs are pure vector (text outlined), so they open anywhere without fonts. These are concepts: once one is picked,
the full kit follows (light and one-colour versions, stacked lockup, favicon and icon sizes, highlight covers).

## Rebuilding

```bash
cd brands/nxtlvl-edits/source
python3 build.py && python3 sheet.py      # round 1: concepts A-D, concepts-preview.png (needs Playwright)
python3 build2.py && python3 sheet.py 2   # round 2: concepts E-L, concepts-preview-2a.png and -2b.png
python3 build3.py && python3 sheet.py 3   # round 3: concepts M-T, concepts-preview-3a.png and -3b.png
```

`vector.py` outlines text with fontTools and traces the wordmark (cached in `nxtlvl-wordmark.svgfrag`).
`fonts/instrument-serif-italic-400.woff2` is Instrument Serif Italic from Google Fonts (SIL Open Font License, see
`fonts/OFL-Instrument-Serif.txt`).
