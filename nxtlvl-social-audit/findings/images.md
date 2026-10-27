# Images: 92/100 (was 85)

## What works

- Fixed: og-image.png (1200×630) in the brand violet with the headline, plus logo.png for the schema.
- Both inline images have alt text; total image weight on the page is about 13 KB.

## Open findings

### Low: The logo is embedded twice as base64 PNG

Two inline copies of a 6.4 KB PNG; they can't be cached.

**Fix:** Reference website/logo.png (or an SVG version) instead when the site is deployed.

### Info: No real work in image form

The page shows mock posts, not real client work.

**Fix:** Add approved client work as WebP/AVIF with descriptive alt text and file names.
