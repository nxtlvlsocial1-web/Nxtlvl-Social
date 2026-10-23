# Technical SEO: 48/100

## What works

- All page copy is in the HTML itself: 2,996 words read without JavaScript, so any crawler sees it.
- Mobile viewport tag is set; no sideways scroll at 390 px or 1440 px.
- No JavaScript errors on load (desktop, mobile, first visit).
- Skip link, a single h1, and a reduced-motion mode that shows everything without animation.
- If the animation library fails to load, the page still shows its content (the h1 has a 3 s safety timeout).

## Findings

### Critical: The site is not live, so nothing can be indexed

The page only exists as website/index.html and a private claude.ai artifact. There is no public domain, so Google cannot crawl it. Because of this, robots.txt, sitemap.xml, HTTPS, redirects, security headers and real-user Core Web Vitals could not be tested.

**Fix:** Deploy to the business domain (the page uses nxtlvlsocial.in in its placeholder email; confirm the real one) over HTTPS, then re-run this audit against the live URL.

### High: The file has no <!doctype>, <html lang> or <head>/<body> wrapper

index.html starts at <meta charset>. The artifact host adds a wrapper, but a normal web host serves the file as-is. Browsers then use quirks mode, and search engines get no language declaration.

**Fix:** Wrap the file in <!doctype html><html lang="en-IN"> (or "en" if you target other countries), with <head> and <body>, before hosting it anywhere else.

### High: 56% of text blocks stay invisible when the page is rendered without scrolling

In a Googlebot-style render (tall viewport, no scrolling), 78 of 139 headings and paragraphs were still at opacity 0. These include "Every piece starts as noise", "Built for the businesses agencies won't call back" and the services cards. The text is in the HTML, so it can still be indexed. However, Google's rendered snapshot shows a mostly empty page, and text Google sees as hidden can be given less weight.

**Fix:** Show any element that is already on screen when the page loads straight away. Also add a timed fallback that reveals all remaining content a few seconds after load if the visitor has not scrolled. Every visitor gets the same page, so this is not cloaking. After launch, check the result with the URL Inspection rendered screenshot in Search Console.

### Medium: No canonical tag

There is no <link rel="canonical">. Without it, copies of the page under other URLs (www/non-www, query strings, the artifact URL) can split ranking signals.

**Fix:** Add <link rel="canonical" href="https://YOUR-DOMAIN/"> once the domain is final.

### Medium: No robots.txt or sitemap.xml

Both return 404 on the local server. Without robots.txt, all crawlers are allowed and you have not stated a preference for AI crawlers.

**Fix:** Publish a robots.txt that allows search crawlers and links the sitemap. Publish a sitemap.xml listing the page (and future pages).

### Medium: No favicon, apple-touch-icon or theme-color

Google shows the favicon next to your result on mobile. Without one, it shows a generic globe.

**Fix:** Add a 48×48 multiple favicon (SVG + ICO/PNG), a 180×180 apple-touch-icon and <meta name="theme-color" content="#05030C">.

### Low: Six scripts load from a third-party CDN

GSAP core and five plugins load from cdn.jsdelivr.net. That adds a DNS lookup and connection, and the hero headline waits for them (see Performance).

**Fix:** Self-host the GSAP files on the same domain, or bundle the plugins into one file.
