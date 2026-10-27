# Schema / Structured Data: 80/100 (was 5)

## What works

- Fixed: Organization and WebSite JSON-LD (valid JSON) with name, URL, logo, image, description, slogan, areaServed (India) and knowsAbout.
- Fixed: an OfferCatalog of the three plans (Content & Design, Video & Editing, Social + Automation) with their monthly starting prices in USD.

## Open findings

### Medium: Add contact details and profiles to the schema once they are real

email, telephone and sameAs are left out on purpose while the contact details are placeholders.

**Fix:** When the real email, WhatsApp number and Instagram handle are in, add "email", "telephone" and "sameAs" to the Organization block, then test with the Rich Results Test and validator.schema.org.

### Info: Do not add FAQPage or Review markup yet

Google retired FAQ rich results for all sites on 7 May 2026, and there are no real reviews yet.

**Fix:** Add Review markup only for real, attributable client reviews.
