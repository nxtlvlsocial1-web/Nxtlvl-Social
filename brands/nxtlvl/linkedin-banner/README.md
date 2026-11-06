# LinkedIn banners

Three options, each in both LinkedIn sizes. Upload the `@2x` file for the sharpest result; LinkedIn scales it down.

| Option | Personal profile (1584×396) | Company page (1128×191) |
|---|---|---|
| A · Shooting star: a big Shooting Star streaks in from behind the profile photo | `shooting-star-1584x396.png` | `shooting-star-1128x191.png` |
| B · Neon frame: the violet corner frame with the logo and headline centred | `neon-frame-1584x396.png` | `neon-frame-1128x191.png` |
| C · Bold type: oversized service words, outline and solid | `bold-type-1584x396.png` | `bold-type-1128x191.png` |

The bottom-left corner is kept clear in every option: LinkedIn puts the profile photo (personal) or page logo
(company) there. Copy: "Your entire creative team, in one studio", the four services, and nxtlvlsocial.ai.

Built from HTML with the brand colours (`#0A0620`→`#05030C`, glows `#7E1AF6` and `#5E06F2`) and the site's fonts
(Archivo, Instrument Serif, Instrument Sans).

## Set 2 (November): in the look of the v2 launch film

`preview-set2.png` shows each banner with the page-logo spot (company) and the photo spot (personal) marked.

| Option | Company page (1128×191) | Personal profile (1584×396) |
|---|---|---|
| D · Editorial blocks: violet, off-white and ink blocks; the headline, 01–04 services and nxtlvlsocial.ai | `editorial-blocks-1128x191.png` | `editorial-blocks-1584x396.png` |
| E · Film slate: the launch film's corner marks, REC timecode and "Your brand, *next level.*" | `film-slate-1128x191.png` | `film-slate-1584x396.png` |
| F · Price board: from $5 a month; Design $5 · Reels $15 · Automation $49 /mo, websites custom quote | `price-board-1128x191.png` | `price-board-1584x396.png` |

Each also has an `@2x` file: upload that one. Built by `source/v2.py` (HTML, rendered with Playwright).
Prices are the ones the site listed before prices came off it; update them in `prices()` if they change.

## Set 3: the same layouts in the logo's colours

The Shooting Star logo's own ground (near-black with violet light from the top-left and bottom-right corners), the
star and its trails as the graphic, white type with a lilac gradient accent. `preview-set3.png` shows them with the
logo / photo spot marked.

| Option | Company page (1128×191) | Personal profile (1584×396) |
|---|---|---|
| G · Logo streak: the Shooting Star, "Your entire creative team, *in one studio.*", 01–04 services | `logo-streak-1128x191.png` | `logo-streak-1584x396.png` |
| H · Logo slate: the film-slate frame around "Your brand, *next level.*" | `logo-slate-1128x191.png` | `logo-slate-1584x396.png` |
| I · Logo prices: "from $5 a month", Design $5 · Reels $15 · Automation $49 /mo, websites custom quote | `logo-prices-1128x191.png` | `logo-prices-1584x396.png` |

Each has an `@2x` file to upload. Built by `source/v3.py`.
