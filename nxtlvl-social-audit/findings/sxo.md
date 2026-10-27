# Search Experience (SXO)

## What works

- Fixed: "Book a free call" now lands on a "Book on WhatsApp" button (opens WhatsApp with a pre-filled message) and an "Email us" button; the email and number are links too.
- The mobile first screen shows the headline, subhead, both buttons and the trust line.
- The price is in the hero and the FAQ handles the main objections.

## Open findings

### Critical: The contact details are still placeholders

The new buttons and links point to +91 00000 00000 (wa.me/910000000000) and hello@nxtlvlsocial.in, which the page itself flags as placeholders.

**Fix:** Replace the number and email everywhere they appear in index.html (the comment at the top lists the places), then remove the "Placeholder contact details" note.

### Medium: Prices in dollars, everything else says India

USD prices ($5, $15, $49) next to Indian contact details, festivals and examples.

**Fix:** Confirm the target market; if it is India, show ₹ (optionally with $ for overseas clients) and update priceCurrency in the JSON-LD.

### Low: Many small tap targets

40 of 66 tappable elements on mobile are under 44×44 px, mostly industry chips and inline links.

**Fix:** Give chips and footer links at least 44 px of tappable height.
