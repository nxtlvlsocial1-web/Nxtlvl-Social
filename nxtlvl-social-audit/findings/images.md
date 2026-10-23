# Images: 85/100

## What works

- Both images have alt text.
- Total image weight is about 13 KB; the sample posts are built in HTML/CSS, not heavy images.

## Findings

### Medium: No social share image

There is no og:image, so shared links have no preview picture.

**Fix:** Create a 1200×630 share image in the brand violet with the headline and logo.

### Low: The logo is embedded twice as base64 PNG

Two copies of a 6.4 KB PNG are inlined as data URIs. They can't be cached and are blurry on high-DPI screens compared with vector.

**Fix:** Use one SVG logo file, referenced twice.

### Info: No real work in image form

The page shows mock posts, not real client work, so it has no image-search presence and no visual proof.

**Fix:** When real client work is approved for use, add it as WebP/AVIF with descriptive alt text and file names (e.g. cafe-diwali-carousel.webp).
