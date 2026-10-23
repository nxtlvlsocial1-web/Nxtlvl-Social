# Schema / Structured Data: 5/100

## What works

- The FAQ is already written as clean question-and-answer pairs, which makes Q&A content easy for parsers to extract.

## Findings

### High: No structured data at all

There is no JSON-LD block on the page. Search engines and AI systems have to guess the business name, logo, offer and prices.

**Fix:** Add Organization (or ProfessionalService) and WebSite JSON-LD with name, url, logo, description, areaServed, contactPoint and sameAs. Add Service with Offer for the three plans once prices are final. A template is in findings/schema.md.

### Info: Do not add FAQPage or Review markup yet

Google retired FAQ rich results for all sites on 7 May 2026, so FAQPage markup brings no search-result feature. Review or AggregateRating markup on the current placeholder testimonials would be fake reviews.

**Fix:** Skip FAQPage for Google benefit. Add Review markup only for real, attributable client reviews.

## Starter JSON-LD

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "ProfessionalService",
      "@id": "https://YOUR-DOMAIN/#org",
      "name": "Nxtlvl Social",
      "url": "https://YOUR-DOMAIN/",
      "logo": "https://YOUR-DOMAIN/logo.svg",
      "image": "https://YOUR-DOMAIN/og-image.png",
      "description": "Creative and automation studio for small businesses: social media design, video, posting and automation, from $5 a month.",
      "areaServed": "YOUR CITY OR REGION",
      "priceRange": "$5–$49 per month",
      "email": "YOUR REAL EMAIL",
      "telephone": "YOUR REAL NUMBER",
      "sameAs": ["https://www.instagram.com/YOUR-HANDLE/"]
    },
    {
      "@type": "WebSite",
      "@id": "https://YOUR-DOMAIN/#website",
      "url": "https://YOUR-DOMAIN/",
      "name": "Nxtlvl Social",
      "publisher": {"@id": "https://YOUR-DOMAIN/#org"}
    }
  ]
}
</script>
```

Replace every YOUR-… value with real details before publishing. Leave out any field you can't fill truthfully. Validate with
Google's Rich Results Test and validator.schema.org after deploy.
