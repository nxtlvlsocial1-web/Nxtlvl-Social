# nxtlvl edits: logo concepts

Logo concepts for the new editing account (Instagram handle given as `nxtlvlledits`). They're built from the Nxtlvl Social
family: the Shooting Star, the Smooth N, the original "nxtlvl" lettering and the violet palette, with an editor's cut.

The comparison sheets show each concept as the Instagram profile picture, at full size and at 110 / 56 / 32 px, with
a lockup: **`concepts-preview.png`** (round 1, A to D), **`concepts-preview-2a.png`** (E to H) and
**`concepts-preview-2b.png`** (I to L).

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

All four share one wordmark: "nxtlvl" in the original logo lettering (traced from `website/logo.png`), then "edits" in
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
```

`vector.py` outlines text with fontTools and traces the wordmark (cached in `nxtlvl-wordmark.svgfrag`).
`fonts/instrument-serif-italic-400.woff2` is Instrument Serif Italic from Google Fonts (SIL Open Font License, see
`fonts/OFL-Instrument-Serif.txt`).
