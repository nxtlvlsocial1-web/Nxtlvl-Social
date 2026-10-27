# Performance (CWV): 72/100 (was 62)

## What works

- Fixed: the headline no longer waits on a third-party CDN, and never waits more than 1.5 s for GSAP. Lab LCP is now 1.47 s on desktop (was 2.64 s) and 0.94–1.07 s on mobile.
- Fixed: GSAP is self-hosted; the page is ready (DOMContentLoaded) in 936 ms on desktop, down from 1624 ms.
- Layout stays stable: CLS 0.0005 desktop, 0.003 mobile.
- The 3D headline, manifesto and every other animation still play for visitors.

## Open findings

### Medium: First visits measure slower because of the opening intro

On a first visit the intro plays and the headline letters fly in, and LCP counts that flight. Lab LCP for first visits was 1.36–2.76 s across runs. That is within the 2.5 s limit at best and just over it at worst. The sandbox uses a software GPU, so real devices should be faster.

**Fix:** After launch, watch LCP in Search Console. If the 75th percentile is over 2.5 s, start the letters closer to their place or shorten the flight from 1.7 s.

### Medium: One very large HTML file

index.html is about 365 KB (about 100 KB gzipped) with the CSS and JS inline.

**Fix:** Serve it with gzip or brotli; move CSS and JS into cached files once there is more than one page.

### Medium: Large DOM: 2,230 elements

Mostly decorative layers (odometer columns, the sample feed, particles and glints).

**Fix:** Build the decorative parts when they scroll into view.

### Medium: Render-blocking Google Fonts stylesheet

Three font families load from fonts.googleapis.com before first paint.

**Fix:** Self-host Latin WOFF2 subsets and preload the two used above the fold.

### Low: Interaction responsiveness (INP) not measured

No field data before launch; several continuous animations run.

**Fix:** Test on a mid-range Android phone after launch; target INP under 200 ms.

## Lab measurements

| | Before | After |
|---|---|---|
| LCP, desktop repeat visit | 2.64 s | 1.47 s |
| LCP, mobile | 1.05 s | 0.94–1.07 s |
| LCP, desktop first visit (intro) | 2.83 s | 1.36–2.76 s |
| DOMContentLoaded, desktop | 1624 ms | 936 ms |
| CLS, desktop / mobile | 0.009 / 0.002 | 0.0005 / 0.003 |
| Text visible to a no-scroll renderer | 61 of 139 | 121 of 122 |

Measured in a sandboxed headless Chromium (software GPU, local server, font CDN stubbed), several runs. Field data from real visitors replaces these once the site is live.
