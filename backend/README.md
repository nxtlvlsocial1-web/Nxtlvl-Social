# Nxtlvl Social backend

One Cloudflare Worker that serves the website (`../website`) and takes the "Book a call" form.
Leads are emailed to **connect@nxtlvlsocial.ai** through [Resend](https://resend.com) (free up to 3,000 emails a month).

```
POST /api/book     {name, business, email, need, message}  ->  {ok:true}
GET  /api/health   ->  {ok:true}
```

## Set up once

1. **Resend**: create an account, add the domain `nxtlvlsocial.ai` under *Domains* and add the DNS records it shows
   (so mail from `bookings@nxtlvlsocial.ai` is not marked as spam), then create an API key.
2. **Cloudflare**: a free account with the domain's DNS on Cloudflare (or just use the `*.workers.dev` address it gives you).
3. In this folder:

```bash
npm install
npx wrangler login
npx wrangler secret put RESEND_API_KEY     # paste the Resend key
npm run deploy
```

The deploy attaches `nxtlvlsocial.ai` and `www.nxtlvlsocial.ai` (the `routes` in `wrangler.toml`) once the domain is on
the Cloudflare account; `www` is redirected to the bare domain by the Worker. The GitHub Actions workflow in
`.github/workflows/deploy.yml` does the same from GitHub; see DEPLOY.md.

Optional: `npx wrangler kv namespace create LEADS`, paste the id into `wrangler.toml`, and every lead is also stored
(and the form is rate-limited to 5 requests per IP per hour).

## Run locally

```bash
cp .dev.vars.example .dev.vars   # put your Resend key in it
npm run dev                      # website + API on http://localhost:8787
npm test                         # handler tests with a fake Resend, no account needed
```

## Change the destination

`LEAD_TO`, `LEAD_FROM` and `ALLOWED_ORIGINS` live in `wrangler.toml`. The form on the website posts to `/api/book`
on the same domain; if the API is down it falls back to opening the visitor's email app with the message filled in.

## Hosting the site elsewhere

If the website is hosted somewhere else (Vercel, Netlify, a plain host), keep this Worker for the API only:
deploy it to `api.nxtlvlsocial.ai`, add the site's origin to `ALLOWED_ORIGINS`, and set
`data-endpoint="https://api.nxtlvlsocial.ai/api/book"` on the form in `website/index.html`.
