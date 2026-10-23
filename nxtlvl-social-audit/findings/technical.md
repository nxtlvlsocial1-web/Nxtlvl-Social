# Technical SEO: 68/100 (was 48)

## What works

- All page copy is in the HTML itself, so any crawler sees it without running JavaScript.
- Fixed: the file is now a complete document: `<!doctype html>`, `<html lang="en-IN">`, `<head>` and `<body>`.
- Fixed: canonical tag, robots.txt (welcomes search and AI crawlers, links the sitemap) and sitemap.xml are ready in website/.
- Fixed: favicon (SVG and 48 px PNG), apple-touch-icon and theme-color.
- Fixed: in a Googlebot-style render (viewport stretched to the page, no scrolling) 121 of 122 text blocks are visible, up from 61 of 139. The pinned manifesto no longer stretches the page to 128,000 px; renderers get it as plain text, and visitors still get the full animation.
- Fixed: GSAP is served from the site itself (website/vendor/gsap-3.14.2/), not a third-party CDN.
- Mobile viewport set, no sideways scroll at 390 px or 1440 px, no JavaScript errors, skip link, single h1, reduced-motion mode.

## Open findings

### Critical: The site is not live, so nothing can be indexed

The page only exists in the repo and as a private claude.ai artifact. HTTPS, redirects, security headers and real-user Core Web Vitals can only be checked once it is on a public domain.

**Fix:** Deploy the whole website/ folder (index.html, vendor/, the icons, og-image.png, logo.png, robots.txt, sitemap.xml) to the domain root over HTTPS with gzip or brotli on, then re-run this audit against the live URL.

### Medium: The domain is assumed, not confirmed

The canonical tag, og:url, og:image, the JSON-LD, robots.txt and sitemap.xml all use https://nxtlvlsocial.in/, the domain from the page's placeholder email.

**Fix:** If the real domain is different, replace nxtlvlsocial.in in those places before launch. A comment at the top of index.html lists them.

### Low: three.js still loads from a third-party CDN

The finale's three.js module is imported from cdn.jsdelivr.net, but only when the visitor reaches the end of the page, so it does not affect loading.

**Fix:** Optional: self-host it next to GSAP when the site is deployed.
