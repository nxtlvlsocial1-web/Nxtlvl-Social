# Nxtlvl Social: SEO Action Plan

Current SEO Health Score: **50/100**. Work top to bottom; Phase 1 must be done before the page is shared publicly.

## Phase 1: Before launch (Critical) (Week 1)

- [ ] Replace the placeholder email, WhatsApp number and Instagram handle; make "Book a free call" open WhatsApp (wa.me) and make the email a mailto: link.
- [ ] Remove the placeholder testimonials or replace them with real, attributed client quotes.
- [ ] Wrap index.html in <!doctype html><html lang="en-IN"><head>…</head><body>…</body></html>.
- [ ] Deploy to the real domain over HTTPS with robots.txt, sitemap.xml and a canonical tag; verify the domain in Google Search Console and submit the sitemap.

## Phase 2: High-impact fixes (Weeks 2-3)

- [ ] New title ("Social Media Content & Automation from $5/mo | Nxtlvl Social") and a fuller meta description.
- [ ] Open Graph and Twitter card tags with a 1200×630 share image; favicon set and theme-color.
- [ ] Organization/ProfessionalService + WebSite JSON-LD (template in findings/schema.md); Service + Offer once prices are final.
- [ ] Reveal fallback so all text is visible without scrolling; check the rendered screenshot with URL Inspection.
- [ ] Let the h1 paint immediately and animate over visible text; self-host GSAP.
- [ ] Name the city and service area on the page; create a Google Business Profile as a service-area business.
- [ ] Fix the odometer text (aria-hidden digit columns plus a hidden real value) and add spaces before <br> in headings.

## Phase 3: Content and authority (Month 2)

- [ ] Add an About/team block with real names and faces.
- [ ] Publish two or three case studies of real client work with numbers.
- [ ] Add one page per core service and per main industry (cafés, salons, gyms, clinics), linked from the home page sections.
- [ ] Cite the source of the "typical market rates" comparison, or label it as your own estimate.
- [ ] Decide between ₹ and $ pricing for the target market.
- [ ] Link the business's own Instagram and other profiles; mirror the same name, description and contact everywhere.
- [ ] Collect real Google reviews through the Business Profile.

## Phase 4: Monitoring (Ongoing)

- [ ] Watch Search Console coverage, queries and Core Web Vitals (LCP, INP, CLS) monthly.
- [ ] Test INP on a mid-range Android phone after each motion change.
- [ ] Re-run the SEO audit against the live URL, and store a drift baseline to catch regressions.

## All findings by priority

| Priority | Finding | Area |
|---|---|---|
| Critical | The site is not live, so nothing can be indexed | Technical SEO |
| Critical | Placeholder testimonials are on the page | Content Quality |
| High | The file has no <!doctype>, <html lang> or <head>/<body> wrapper | Technical SEO |
| High | 56% of text blocks stay invisible when the page is rendered without scrolling | Technical SEO |
| High | Weak experience and trust signals (E-E-A-T) | Content Quality |
| High | One page has to rank for everything | Content Quality |
| High | The title tag is just the brand name | On-Page SEO |
| High | No Open Graph or Twitter card tags | On-Page SEO |
| High | No city or service area anywhere on the page | On-Page SEO |
| High | No structured data at all | Schema / Structured Data |
| High | The hero headline waits for the animation library before it shows | Performance (CWV) |
| High | No entity signals | AI Search Readiness |
| High | "Book a free call" leads to a dead end | Search Experience |
| Medium | No canonical tag | Technical SEO |
| Medium | No robots.txt or sitemap.xml | Technical SEO |
| Medium | No favicon, apple-touch-icon or theme-color | Technical SEO |
| Medium | The cost comparison figures have no source | Content Quality |
| Medium | The meta description is short | On-Page SEO |
| Medium | One very large HTML file | Performance (CWV) |
| Medium | Large DOM: 2,256 elements | Performance (CWV) |
| Medium | Render-blocking Google Fonts stylesheet | Performance (CWV) |
| Medium | No social share image | Images |
| Medium | Animated numbers become digit strips in the rendered text | AI Search Readiness |
| Medium | No stated AI-crawler policy | AI Search Readiness |
| Medium | Prices in dollars, everything else says India | Search Experience |
| Low | Six scripts load from a third-party CDN | Technical SEO |
| Low | Repetition flag from the content checker | Content Quality |
| Low | Headings run words together where a <br> splits the line | On-Page SEO |
| Low | No links to the business's social profiles | On-Page SEO |
| Low | Interaction responsiveness (INP) not measured | Performance (CWV) |
| Low | No fetchpriority or speculation rules | Performance (CWV) |
| Low | The logo is embedded twice as base64 PNG | Images |
| Low | No llms.txt | AI Search Readiness |
| Low | Many small tap targets | Search Experience |
| Info | Do not add FAQPage or Review markup yet | Schema / Structured Data |
| Info | No real work in image form | Images |
| Info | On desktop the headline is still assembling at 2 s | Search Experience |
