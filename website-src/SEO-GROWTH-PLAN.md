# Nxtlvl Social: SEO, AEO and GEO growth plan

Goal: be found on Google, and recommended by AI assistants (ChatGPT, Gemini, Perplexity, Google AI Overviews, Copilot),
when someone in India looks for an AI-driven marketing, automation or creative partner.

## Expectations

- "AI marketing agency India" is a crowded head term. Expect 6 to 12 months of steady work before ranking there.
- Long, specific searches rank much sooner and convert better. Start with those, for example:
  - "WhatsApp automation agency India"
  - "Instagram DM automation for restaurants"
  - "AI social media management for clinics"
  - "reel editing services India"
- AI assistants recommend businesses they see named consistently across many trusted places. A good website alone is not
  enough: the brand also needs mentions, reviews and profiles elsewhere.

## Already done in the November 2026 relaunch

- One page per service, each targeting its own search terms. Every page has:
  - a unique title and description
  - a single H1
  - an answer-first intro and an "At a glance" facts box
  - an FAQ section
  - internal links to the other services
- Structured data on every page: Organization, WebSite, WebPage, BreadcrumbList, Service, FAQPage, AboutPage and ContactPage.
- `llms.txt` (a plain facts sheet for AI crawlers), `sitemap.xml`, and a `robots.txt` that welcomes search and AI crawlers.
- A fast, lightweight site: no animation libraries, self-hosted fonts, and pages of about 15 to 40 KB each.
- The old service URLs redirect permanently to the new pages (`_redirects`).
- A new share image (`og-image.png`) for WhatsApp, LinkedIn and X previews.

## Week 1: go live and get indexed

1. **Deploy the site** by following `DEPLOY.md`. None of the work counts until the site is live on nxtlvlsocial.ai.
2. **Google Search Console:**
   - Verify the domain and submit `https://nxtlvlsocial.ai/sitemap.xml`.
   - Use URL Inspection and click "Request indexing" for each page.
3. **Bing Webmaster Tools:** import the site from Search Console. Bing powers ChatGPT search and Copilot, so this matters
   for AI answers.
4. **Validate the structured data** with Google's Rich Results Test and validator.schema.org.
5. **Turn on analytics:** Cloudflare Web Analytics (already wired into the deploy) or GA4. Watch for visits referred by
   chatgpt.com, perplexity.ai, gemini.google.com and copilot.microsoft.com.

## Weeks 1 to 2: build the brand's identity online

AI systems decide who you are by matching the same facts across sources.

1. **Use one name and one description everywhere.**
   - Name: "Nxtlvl Social (Next Level Social)".
   - Description: "AI-driven growth company in India: marketing, automation and creative services."
2. **Google Business Profile:**
   - Create it as a *service-area business*: choose your city or state and hide the address if you work from home.
   - Category: "Marketing agency". Secondary categories: "Internet marketing service", "Website designer", "Video editing service".
   - Add photos, services, the website link and a weekly post.
   - This is the single biggest lever for "near me" and city searches.
3. **Profiles:** create or complete these, each with the same name, description and link:
   - LinkedIn company page
   - Instagram (@ai.nxtlvl, @nxtlvlledits)
   - YouTube channel
   - X
   - Crunchbase
4. **Agency directories** that AI assistants and Google trust:
   - Clutch, GoodFirms, DesignRush, Sortlist and TechBehemoths
   - Justdial and Sulekha, for India
5. **Add your details to the website.** Send me the following and I'll add them to the pages and the schema:
   - city
   - founder name and photo
   - business phone or WhatsApp
   - any registration (MSME/Udyam, GST)

## Month 1: proof (E-E-A-T)

Google and AI assistants favour businesses that show real experience.

1. **Two or three case studies** with real numbers: the brief, what you did, and the result. The growth timelapse
   (0 → 10K followers, 1M views) is a strong first one. Give each case study its own page, for example
   `/work/ai-nxtlvl-growth`.
2. **Reviews:** ask every happy client for a Google review, and a Clutch or GoodFirms review. Reply to every one.
3. **An About page with real people:** founder story, photo and LinkedIn link. Send me the details and I'll add them.

## Months 1 to 6: content that ranks and gets cited

Publish two useful articles a month in a `/guides` section. Answer one real question per page, answer it in the first
paragraph, then go deeper. These match how people search and how AI assistants pick their quotes.

**Topic ideas, by service:**

- **Automation:**
  - "How to automate WhatsApp replies for your business (2026 guide)"
  - "Instagram DM automation: what is allowed and how to set it up"
  - "WhatsApp Business app vs WhatsApp Business API: which do you need?"
- **Marketing:**
  - "AI marketing for small businesses in India: a practical guide"
  - "How much does social media management cost in India?" (give honest ranges; these pages attract buyers)
  - "Meta ads vs Google ads for local businesses"
- **Creative:**
  - "Reel ideas for restaurants / clinics / real estate (with examples)"
  - "How to brief a product shoot"
- **AEO:**
  - "How to get your business recommended by ChatGPT and Google AI Overviews"
- **Industry pages:**
  - "AI marketing for restaurants", "for clinics", "for real estate"
  - Each one needs real examples, so it isn't a thin page.

**Rules for every page:**

- Write for a person first.
- Use clear headings phrased as questions.
- Include real numbers and examples.
- Name the author.
- Add the update date.
- Link to the relevant service page.

## Ongoing: authority (links and mentions)

- **Guest posts and podcasts:** appear on Indian startup, marketing and D2C blogs and podcasts.
- **Answer questions** on Quora, Reddit (r/IndianStartups, r/digitalmarketing) and LinkedIn, and link to a guide only
  where it genuinely helps. AI assistants read these threads heavily.
- **Share your data:** publish your own numbers, for example "We analysed 500 reels from Indian brands". Original data
  earns links and gets quoted by AI answers.
- **Partnerships:** co-marketing with tool partners and local business associations.
- **"Best AI agencies in India" listicles:** ask to be included, and make sure the facts about you are correct where you
  already appear.

## Monthly check (30 minutes)

1. **Search Console:**
   - Which queries bring impressions?
   - Write or improve a page for any query where you rank on page two.
2. **AI answers:** ask ChatGPT, Gemini and Perplexity the questions a buyer would, and note whether Nxtlvl is mentioned.
   - "best AI marketing agency in India"
   - "who can automate WhatsApp replies for my clinic"
3. **Reviews:** count of new reviews and your average rating.
4. **Site health:** check the Core Web Vitals report in Search Console.

## Later: the platform

When the Nxtlvl growth platform launches:

- Give it its own pages: a features page, a pricing page if you publish prices, and a changelog.
- Add a `SoftwareApplication` schema.
- List it on Product Hunt and SaaS directories.

A product with a name gives AI assistants a second thing to recommend.
