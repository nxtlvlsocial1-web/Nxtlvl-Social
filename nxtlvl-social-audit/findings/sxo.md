# Search Experience (SXO)

## What works

- The mobile first screen shows the headline, the subhead, both buttons and the "No contracts · Cancel any month" trust line.
- The price ("from $5 a month") is in the hero, which matches what price-sensitive searchers are looking for.
- The FAQ handles the main objections before the contact section.

## Findings

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
