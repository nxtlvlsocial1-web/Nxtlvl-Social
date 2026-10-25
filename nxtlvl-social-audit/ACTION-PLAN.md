# Nxtlvl Social: SEO Action Plan

SEO Health Score: **76/100** (was 50, then 72). Phase 1 must be done before the page is shared publicly.

## Done: fixes applied on 23 Oct 2026

- [x] Complete document: `<!doctype html>`, `<html lang="en-IN">`, `<head>`, `<body>`.
- [x] New title, meta description and canonical tag.
- [x] Open Graph and Twitter card tags, with a new 1200×630 share image (website/og-image.png).
- [x] Favicon (SVG and PNG), apple-touch-icon and theme-color.
- [x] Organization and WebSite JSON-LD, including the three plans and their prices.
- [x] robots.txt and sitemap.xml.
- [x] Testimonial placeholders moved off the live page into a `<template>`.
- [x] "Book on WhatsApp" and "Email us" buttons in the contact section; the email, number and FAQ WhatsApp mention are now links.
- [x] Text stays visible for search-engine renderers: no manifesto pin, intro, letter flight or label scramble in a viewport taller than any screen.
- [x] Headline waits at most 1.5 s for the animation library; GSAP is self-hosted.
- [x] The savings odometer exposes its real value as text.
- [x] A space before each `<br>` inside headings.

## Phase 1: Before launch (Critical) (Week 1)

- [ ] Replace the WhatsApp number (910000000000 / +91 00000 00000) and the email in index.html, then remove the placeholder note.
- [ ] Confirm the domain; if it is not nxtlvlsocial.in, replace it in the head tags, JSON-LD, robots.txt and sitemap.xml.
- [x] Self-hosted fonts, web manifest, robots meta, keyword-rich hero copy, 44 px tap targets, cached logo, llms.txt (round 2).
- [ ] Deploy the whole website/ folder to the domain root over HTTPS with gzip or brotli.
- [ ] Verify the domain in Google Search Console, submit sitemap.xml, and check the URL Inspection rendered screenshot.
- [ ] Test the page with the Rich Results Test and validator.schema.org.

## Phase 2: High-impact (Weeks 2-3)

- [ ] Name the city and service area on the page and in areaServed; create a Google Business Profile as a service-area business.
- [ ] Add email, telephone and sameAs (Instagram and other profiles) to the JSON-LD; link the profiles in the footer.
- [ ] Decide between ₹ and $ pricing for the target market.

## Phase 3: Content and authority (Month 2)

- [ ] Add an About/team block with real names and faces.
- [ ] Publish two or three case studies of real client work with numbers; restore the testimonials with real quotes.
- [ ] Add one page per core service and per main industry, linked from the home page.
- [ ] Name the source of the "typical market rates" comparison.
- [ ] Collect real Google reviews through the Business Profile.

## Phase 4: Monitoring (Ongoing)

- [ ] Watch Search Console coverage, queries and Core Web Vitals monthly, especially first-visit LCP.
- [ ] Test INP on a mid-range Android phone after each motion change.
- [ ] Re-run the SEO audit against the live URL and store a drift baseline.

## Open findings by priority

| Priority | Finding | Area |
|---|---|---|
| Critical | The site is not live, so nothing can be indexed | Technical SEO |
| Critical | The contact details are still placeholders | Search Experience |
| High | Weak experience and trust signals (E-E-A-T) | Content Quality |
| High | One page has to rank for everything | Content Quality |
| High | No city or service area anywhere on the page | On-Page SEO |
| Medium | The domain is assumed, not confirmed | Technical SEO |
| Medium | Add contact details and profiles to the schema once they are real | Schema / Structured Data |
| Medium | First visits measure slower because of the opening intro | Performance (CWV) |
| Medium | One very large HTML file | Performance (CWV) |
| Medium | Large DOM: 2,230 elements | Performance (CWV) |
| Medium | Render-blocking Google Fonts stylesheet | Performance (CWV) |
| Medium | Entity signals are still thin | AI Search Readiness |
| Medium | Prices in dollars, everything else says India | Search Experience |
| Low | three.js still loads from a third-party CDN | Technical SEO |
| Low | Say where the "typical market rates" come from | Content Quality |
| Low | Repetition flag from the content checker | Content Quality |
| Low | No links to the business's social profiles | On-Page SEO |
| Low | Interaction responsiveness (INP) not measured | Performance (CWV) |
| Low | The logo is embedded twice as base64 PNG | Images |
| Low | No llms.txt | AI Search Readiness |
| Low | Many small tap targets | Search Experience |
| Info | Do not add FAQPage or Review markup yet | Schema / Structured Data |
| Info | No real work in image form | Images |
