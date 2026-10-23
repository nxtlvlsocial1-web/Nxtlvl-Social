# AI Search Readiness: 45/100

## What works

- Content is server-rendered: AI crawlers that do not run JavaScript still get the full text.
- FAQ answers are short, direct and self-contained, so they are easy to quote.
- Concrete facts (prices, turnaround in 48 hours, month-to-month terms) are stated in plain text.

## Findings

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
