# Creators 100X

The owner's brand for lead magnets and automation resources (the PDFs sent by keyword auto-DMs). Owner's rule: **make
PDFs in this branding whenever asked** ("make the pdf with this creators 100x branding whenever i say to").

## Logo

- `logo-square.png`: the artwork as supplied (1254 x 1254, on the brand gradient).
- `logo.png`: tile + wordmark on a transparent background; `logo-mark.png`: the tile alone. Both cut by `make_logo.py`
  from the square artwork. For light backgrounds (the pink X and the black wordmark need them).
- The mark: a rounded black tile with a lightning bolt, top half white, bottom half lime. The wordmark: "Creators" in a
  heavy geometric sans, "100X" in a heavy italic with the X in hot pink.

## Colours (sampled from the artwork)

| role | hex |
| --- | --- |
| ink (tile, text) | `#101111` |
| hot pink (the X, accents, numbers) | `#FD0B68` |
| lime (the bolt, highlights, chips on black) | `#CCFB79` |
| background | `#FDF4F4` (warm off-white) |
| corner glows | lime `#CEFB8F` top-left / bottom-right, pink `#FE70B3` top-right / bottom-left |

The look: an off-white page with soft lime and pink glows in the corners, black type, one hot-pink accent per line,
lime highlighter on the words to fill in, black pills with lime text for labels.

## Type

Inter (OFL, `fonts/`): 800 for titles and hook lines, 700 for labels, 600 for body. Titles tight (-0.035 to -0.045 em).

## PDFs

`make_pdf.cjs` turns a content JSON into a branded, phone-friendly PDF (4:5 pages, 1080 x 1350): a cover (logo,
kicker pill, big title with a pink word, subtitle), text pages with numbered steps, card pages (number, category pill,
the line with [blanks] in lime, an example, why it works), and a closing checklist with the logo. Every page body is
auto-fitted above the footer (logo mark, "Creators 100X", page number).

```bash
node brands/creators-100x/make_pdf.cjs brands/creators-100x/pdf/20-hooks-that-work.json brands/creators-100x/pdf/creators100x_20-hooks-that-work.pdf --png
```

`--png` also writes a preview image per page (look at them before delivering; keep them out of git). The content
schema is at the top of `make_pdf.cjs`. Name outputs `creators100x_<topic>.pdf`. No emojis in the copy.

Made so far: `pdf/creators100x_20-hooks-that-work.pdf` (the "HOOK" keyword resource for the reel-flop reel).
