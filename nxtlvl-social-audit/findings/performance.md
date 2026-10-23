# Performance (CWV): 62/100

## What works

- Layout is stable: CLS 0.009 on desktop and 0.002 on mobile (good is under 0.1).
- Mobile lab LCP 1.05 s.
- three.js loads only when the finale is reached (dynamic import), and GSAP is deferred.
- Fonts use display=swap. Images total about 13 KB.

## Findings

### High: The hero headline waits for the animation library before it shows

The largest element on screen is the h1, and it stays hidden until GSAP loads from jsdelivr and assembles the letters. Lab LCP was 2.64 s on desktop and 2.83 s on a first visit with the intro, measured on a local server with no network delay. That is already over the 2.5 s "good" limit before any real-world latency.

**Fix:** Paint the h1 immediately and let the 3D assembly play over visible text (e.g. start from a soft, already-legible state), or shorten the gate. Self-host GSAP so it arrives with the page.

### Medium: One very large HTML file

index.html is 357 KB (97 KB gzipped): 127 KB inline CSS and 128 KB inline JS. All of it is parsed before first paint, and none of it can be cached separately.

**Fix:** When the site grows past one page, move the CSS and JS into cached files. Until then, make sure the host serves it with gzip or brotli.

### Medium: Large DOM: 2,256 elements

Lighthouse warns above about 1,400 elements. Much of it is decorative: odometer digit columns, the sample feed, and the particle and glint layers.

**Fix:** Build the decorative parts on demand (when scrolled into view) rather than in the initial HTML.

### Medium: Render-blocking Google Fonts stylesheet

Three families with variable axes (Archivo wdth+wght, Instrument Sans, Instrument Serif) load from fonts.googleapis.com before first paint.

**Fix:** Self-host Latin subsets as WOFF2 and preload the two used above the fold.

### Low: Interaction responsiveness (INP) not measured

There is no field data before launch. The page runs several continuous animations (burst canvas, rays, glints, the three.js finale), which can slow taps on low-end Android phones.

**Fix:** After launch, test on a mid-range Android phone and watch INP in Search Console (target under 200 ms).

### Low: No fetchpriority or speculation rules

Preload score 50/100. This matters little for a one-page site.

**Fix:** Revisit when there are more pages to navigate to.

## Lab measurements

| | Desktop 1440×900 | Mobile 390×844 | Desktop, first visit (intro) |
|---|---|---|---|
| LCP | 2.64 s (h1) | 1.05 s (h1) | 2.83 s (h1) |
| CLS | 0.009 | 0.002 | 0.0005 |
| DOMContentLoaded | 1624 ms | 615 ms | 1888 ms |
| DOM elements | 2,256 | 2,232 | 2,255 |

Measured in a sandboxed headless Chromium (software GPU, local server, font CDN stubbed). Indicative only; field data from real visitors (CrUX / Search Console) replaces these once the site is live.
