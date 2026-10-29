# Debit card skin: Rishabh Rana, CMO

Three front-of-card designs in the Nxtlvl brand. `all-options-preview.png` shows them side by side.

| Option | Look |
|---|---|
| A · Shooting star | Deep ink with violet light, a glowing star with lens flare, a sparkle field and fine wave lines; silver wordmark and "CMO" |
| B · Violet foil | Iridescent violet with glossy light bands, an embossed watermark star and a pearl wordmark |
| C · Black edition | Brushed graphite metal, a violet edge glow and frame, a chrome wordmark and name, a glowing star |

The "nxtlvl" wordmark is the original logo artwork (`website/logo.png`, kept as `source/nxtlvl-wordmark-mask.png`)
filled with metal and foil gradients; "social" is set beside it in Archivo at full width to match.

## Files in each option folder

| File | Use |
|---|---|
| `*_print-bleed.png` | Send this to the printer: 600 dpi, 89.6 × 58 mm (card plus 2 mm bleed) |
| `*_print.pdf` | The same artwork as a PDF, for printers who ask for one |
| `*_card-size.png` | Exact card size, 85.6 × 53.98 mm at 600 dpi, for apps that want no bleed |
| `*_cut-guide.png` | Shows the cut line, the 3 mm safe zone and the chip cut-out |
| `*_preview.png` | Mockup of the finished card |

## Notes for printing

- Card size is the standard ISO/IEC 7810 ID-1 (85.6 × 53.98 mm, 3.18 mm corners).
- The chip cut-out sits where the EMV chip is on almost all cards (13 × 11.5 mm, about 8.6 mm from the left edge
  and 18 mm from the top). Hold the card against the cut guide before ordering; if the chip sits elsewhere,
  ask the printer to move the cut-out.
- The design runs under the chip area, so the printer's cut-out never shows a gap.
- The skin is for the front only. Don't cover the back: the magnetic stripe, signature panel and printed card
  details must stay visible. Contactless payments work through a thin vinyl skin.
- Cards with raised, embossed numbers on the front won't take a flat skin well.
- No bank or card-network logos and no card numbers are included.

## Editing

`source/build.py` holds the designs (name, title and colours at the top). Rebuild with:

```bash
cd source && python3 build.py && node render.js && python3 finish.py && rm -rf html
```
