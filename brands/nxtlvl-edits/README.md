# nxtlvl edits: logo concepts

Logo concepts for the new editing account (Instagram handle given as `nxtlvlledits`). They're built from the Nxtlvl Social
family: the Shooting Star, the Smooth N, the original "nxtlvl" lettering and the violet palette, with an editor's cut.

**`concepts-preview.png`** shows all four as the Instagram profile picture, at full size and at 110 / 56 / 32 px, with a
lockup for each.

| Concept | Idea |
|---|---|
| **A · Cut Star** | The Nxtlvl star, sliced by two razor cuts through all three trails, like one cut through every track of a timeline. The closest sibling to the main account. |
| **B · Clip N** | The Smooth N from the Nxtlvl logo, cut into three clips. |
| **C · Timeline Steps** | Three clips on a timeline, each track a step higher (the next level), cut by a star-headed playhead. |
| **D · Wordmark** | "nxtlvl" over "edits" inside camera viewfinder corners with a REC dot. |

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
python3 build.py   # writes concepts/*/profile.svg and lockup.svg
python3 sheet.py   # renders the PNGs and concepts-preview.png (needs Playwright)
```

`vector.py` outlines text with fontTools and traces the wordmark (cached in `nxtlvl-wordmark.svgfrag`).
`fonts/instrument-serif-italic-400.woff2` is Instrument Serif Italic from Google Fonts (SIL Open Font License, see
`fonts/OFL-Instrument-Serif.txt`).
