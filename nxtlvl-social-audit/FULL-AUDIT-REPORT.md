# Nxtlvl Social: SEO Audit

**Page:** `website/index.html` (the landing page; served locally because it is not deployed yet)  
**Date:** 23 October 2026  
**Business type:** Agency (creative + automation studio for small businesses), with local service-area signals (India, on-site shoots)

## SEO Health Score: 50/100

| Category | Weight | Score |
|---|---|---|
| Technical SEO | 22% | 48/100 |
| Content Quality | 23% | 60/100 |
| On-Page SEO | 20% | 50/100 |
| Schema / Structured Data | 10% | 5/100 |
| Performance (CWV) | 10% | 62/100 |
| Images | 5% | 85/100 |
| AI Search Readiness | 10% | 45/100 |

The page itself is well written and works without JavaScript. The score is held down by launch blockers and missing metadata, not by the copy. The site isn't live yet; the contact details and testimonials are placeholders; and there is no title keyword, social card or structured data. Most of the fixes are small.

## Top 5 issues

1. **Critical:** The site is not live, so nothing can be indexed (Technical SEO)
2. **Critical:** Placeholder testimonials are on the page (Content Quality)
3. **High:** The file has no <!doctype>, <html lang> or <head>/<body> wrapper (Technical SEO)
4. **High:** 56% of text blocks stay invisible when the page is rendered without scrolling (Technical SEO)
5. **High:** Weak experience and trust signals (E-E-A-T) (Content Quality)

## Top 5 quick wins

1. Replace the title tag with "Social Media Content & Automation from $5/mo | Nxtlvl Social" (5 min).
2. Add Open Graph and Twitter card tags plus a 1200×630 share image (1 h).
3. Turn "Book a free call" into a wa.me WhatsApp link with a pre-filled message, once the real number is in (15 min).
4. Add Organization + WebSite JSON-LD from the template in findings/schema.md (30 min).
5. Add a favicon, apple-touch-icon and theme-color (20 min).

## Screenshots

| Desktop, above the fold | Mobile, above the fold |
|---|---|
| ![Desktop](screenshots/desktop-above-fold.jpg) | ![Mobile](screenshots/mobile-above-fold.jpg) |

Full-page desktop capture: `screenshots/desktop-full.jpg`.

## Technical SEO: 48/100

**What works**

- All page copy is in the HTML itself: 2,996 words read without JavaScript, so any crawler sees it.
- Mobile viewport tag is set; no sideways scroll at 390 px or 1440 px.
- No JavaScript errors on load (desktop, mobile, first visit).
- Skip link, a single h1, and a reduced-motion mode that shows everything without animation.
- If the animation library fails to load, the page still shows its content (the h1 has a 3 s safety timeout).

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

## Content Quality: 60/100

**What works**

- 2,937 words of plain, specific copy. The content checker found no filler and no AI-writing patterns (quality 95/100).
- A 12-question FAQ that answers the real objections (price, contracts, ownership, "will it look AI-made").
- Transparent pricing and a clear process: three steps, then a week-by-week first month.
- Industry examples (cafés, salons, gyms, clinics, real estate) show who it is for.

### Critical: Placeholder testimonials are on the page

The "What your customers will say here" section has made-up quotes, flagged in the page itself as placeholders. Publishing invented reviews breaks consumer-protection rules in many markets and destroys trust if spotted.

**Fix:** Before launch, either remove the section or replace it with real quotes from clients (with permission, name and business). Never mark up placeholder or self-written reviews with Review schema.

### High: Weak experience and trust signals (E-E-A-T)

The page names no founder or team, has no About section, shows no real client work or results, and gives no location. For an agency, the portfolio is the main proof of experience.

**Fix:** Add a short "Who makes this" block with names and faces, two or three real before/after client examples with numbers (reach, bookings, time saved), and the city you work from.

### High: One page has to rank for everything

All services, industries and prices sit on a single URL with anchor links only. That page cannot rank well for "reels for cafés", "salon social media", "Instagram automation" and "poster design" all at once.

**Fix:** After launch, add one page per core service and per main industry, each with its own examples and FAQ. Link them from the home page sections that already exist.

### Medium: The cost comparison figures have no source

"One freelance reel costs $35" and the savings calculator use "typical market rates" with no source. These are the claims searchers and AI answers are most likely to quote.

**Fix:** Cite where the rates come from (your own quotes from N freelancers, a published rate survey), or label them as your own estimate.

### Low: Repetition flag from the content checker

Repetition score 32 ("repetitive"), driven by words like post, reel and month. This is normal for a services page and not a quality problem.

**Fix:** No action needed. When writing new service pages, vary the wording rather than reusing the home page lines.

## On-Page SEO: 50/100

**What works**

- Exactly one h1 and a logical outline of 34 headings. The h2s map to real search topics (pricing, services, FAQ).
- Clear anchor navigation (Who it's for, The maths, Services, Pricing, FAQ).
- Meta description is present and accurate.

### High: The title tag is just the brand name

<title>Nxtlvl Social</title> is 13 characters and has no service words. Searchers who don't already know the brand get no reason to click.

**Fix:** Use something like "Social Media Content & Automation from $5/mo | Nxtlvl Social" (60 characters).

### High: No Open Graph or Twitter card tags

Links shared on WhatsApp, Instagram DMs, LinkedIn or X show no image and a bare title. For a social media agency whose main contact channel is WhatsApp, this is the first impression many prospects get.

**Fix:** Add og:title, og:description, og:url, og:type=website, og:image (1200×630, the violet hero with the headline) and twitter:card=summary_large_image.

### High: No city or service area anywhere on the page

The page signals India (+91 number, .in email, Diwali, chai) and offers on-site shoots "within our service area", but never names a city. You cannot rank for "social media agency in <city>" or appear in local results.

**Fix:** Name the city and the area you shoot in (hero trust line, FAQ answer about shoots, footer), and set up a Google Business Profile as a service-area business.

### Medium: The meta description is short

At 77 characters it uses about half the space Google shows, and it has no call to action.

**Fix:** For example: "Design, reels, posting and DM automation for cafés, salons, gyms and shops. Your whole social media team from $5 a month. No contracts. Book a free call." (153 characters).

### Low: Headings run words together where a <br> splits the line

Text extractors read "team,for less than one reel", "starts as noise" as "startsas noise", and "businessesagencies". Google usually handles <br>, but other crawlers and AI tools may not.

**Fix:** Put a space before each <br> inside headings.

### Low: No links to the business's social profiles

A social media agency with no link to its own Instagram is a missed proof point and a missed entity signal.

**Fix:** Link Instagram (and any other active profiles) from the footer and the contact section, and list them in schema sameAs.

## Schema / Structured Data: 5/100

**What works**

- The FAQ is already written as clean question-and-answer pairs, which makes Q&A content easy for parsers to extract.

### High: No structured data at all

There is no JSON-LD block on the page. Search engines and AI systems have to guess the business name, logo, offer and prices.

**Fix:** Add Organization (or ProfessionalService) and WebSite JSON-LD with name, url, logo, description, areaServed, contactPoint and sameAs. Add Service with Offer for the three plans once prices are final. A template is in findings/schema.md.

### Info: Do not add FAQPage or Review markup yet

Google retired FAQ rich results for all sites on 7 May 2026, so FAQPage markup brings no search-result feature. Review or AggregateRating markup on the current placeholder testimonials would be fake reviews.

**Fix:** Skip FAQPage for Google benefit. Add Review markup only for real, attributable client reviews.

## Performance (CWV): 62/100

**What works**

- Layout is stable: CLS 0.009 on desktop and 0.002 on mobile (good is under 0.1).
- Mobile lab LCP 1.05 s.
- three.js loads only when the finale is reached (dynamic import), and GSAP is deferred.
- Fonts use display=swap. Images total about 13 KB.

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

## Images: 85/100

**What works**

- Both images have alt text.
- Total image weight is about 13 KB; the sample posts are built in HTML/CSS, not heavy images.

### Medium: No social share image

There is no og:image, so shared links have no preview picture.

**Fix:** Create a 1200×630 share image in the brand violet with the headline and logo.

### Low: The logo is embedded twice as base64 PNG

Two copies of a 6.4 KB PNG are inlined as data URIs. They can't be cached and are blurry on high-DPI screens compared with vector.

**Fix:** Use one SVG logo file, referenced twice.

### Info: No real work in image form

The page shows mock posts, not real client work, so it has no image-search presence and no visual proof.

**Fix:** When real client work is approved for use, add it as WebP/AVIF with descriptive alt text and file names (e.g. cafe-diwali-carousel.webp).

## AI Search Readiness: 45/100

**What works**

- Content is server-rendered: AI crawlers that do not run JavaScript still get the full text.
- FAQ answers are short, direct and self-contained, so they are easy to quote.
- Concrete facts (prices, turnaround in 48 hours, month-to-month terms) are stated in plain text.

### High: No entity signals

There is no Organization schema, no sameAs links, no address or city, and no named people. AI answer engines can't tie "Nxtlvl Social" to a known business, so they are unlikely to recommend it by name.

**Fix:** Add the Organization schema and profile links (see Schema), name the city, and keep the business name, description and contact details identical across Instagram, Google Business Profile and directories.

### Medium: Animated numbers become digit strips in the rendered text

The odometer replaces values like "$405" with ten-digit columns, so the rendered text reads "$012345678901234567890123456789". The aria-label it adds sits on a plain <b>, where screen readers don't reliably announce it.

**Fix:** Mark the digit columns aria-hidden="true" and keep the real value next to them in a visually hidden span.

### Medium: No stated AI-crawler policy

With no robots.txt, there is no deliberate choice for OAI-SearchBot, PerplexityBot, ClaudeBot or Google-Extended.

**Fix:** Decide whether you want to appear in AI answers (for a lead-gen agency, usually yes) and say so in robots.txt.

### Low: No llms.txt

/llms.txt returns 404. It is listed for completeness only: no major AI search system is confirmed to use it, so it carries no weight in this score.

**Fix:** Optional. Add one only if it costs nothing to maintain.

## Search Experience (not weighted)

**What works**

- The mobile first screen shows the headline, the subhead, both buttons and the "No contracts · Cancel any month" trust line.
- The price ("from $5 a month") is in the hero, which matches what price-sensitive searchers are looking for.
- The FAQ handles the main objections before the contact section.

### High: "Book a free call" leads to a dead end

All nine "Book a free call" links jump to #contact. That section only shows a placeholder email and a +91 00000 00000 number to copy. There is no form, booking link, WhatsApp link (wa.me), mailto or tel link.

**Fix:** Make the main button open WhatsApp with a pre-filled message (wa.me/91XXXXXXXXXX?text=…). Make the email a mailto: link, and add a booking link (Calendly, Cal.com or Google Calendar) if you take scheduled calls.

### Medium: Prices in dollars, everything else says India

Prices are in USD ($5, $49) while the contact details, festivals and examples point to India. Indian searchers comparing agencies expect ₹.

**Fix:** Confirm the target market. If it is India, show ₹ prices (optionally with $ for overseas clients).

### Low: Many small tap targets

38 of 61 tappable elements on mobile are smaller than 44×44 px, mostly the industry chips and inline links.

**Fix:** Give chips and footer links at least 44 px of tappable height (padding, not larger text).

### Info: On desktop the headline is still assembling at 2 s

The above-the-fold screenshot at 2 s shows the h1 letters mid-flight. The rest of the hero (subhead, buttons, trust line) is readable.

**Fix:** See the Performance finding: show legible text first and animate on top of it.

## Limitations

- Not deployed: robots.txt, sitemap, HTTPS, redirects, security headers and field Core Web Vitals could not be tested.
- No Google Search Console, GA4, CrUX, Matomo, Moz or DataForSEO access: no rankings, traffic, backlinks or field data.
- Lab timings come from a sandboxed headless Chromium with a software GPU and the font CDN stubbed; treat them as indicative.

Raw tool output is in `raw/`; per-category detail is in `findings/`; the prioritised plan is in `ACTION-PLAN.md`.
