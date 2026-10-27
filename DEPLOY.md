# Deploying nxtlvlsocial.ai

The whole site (home page, service pages, 404 page) and the "Book a call" form run from **one Cloudflare Worker**
in `backend/`. It serves everything in `website/` and handles `POST /api/book`, which emails each booking to
connect@nxtlvlsocial.ai through Resend. Cloudflare's free plan is enough.

Budget about 45 minutes the first time. After that, an update is one command.

## What you need

- A computer with **Node.js 22 or newer** (nodejs.org) and **Git**.
- The domain **nxtlvlsocial.ai**, with access to its registrar (where you bought it).
- Free accounts at **cloudflare.com** and **resend.com**.

## 1. Get the code

```bash
git clone https://github.com/nxtlvlsocial1-web/Nxtlvl-Social.git
cd Nxtlvl-Social
git checkout claude/vibrant-feynman-gaxg7b    # or main, once this branch is merged
```

## 2. Put the domain on Cloudflare

1. In the Cloudflare dashboard: **Add a domain**, type `nxtlvlsocial.ai`, pick the Free plan.
2. Cloudflare shows two nameservers. At your registrar, replace the domain's nameservers with those two.
3. Wait until Cloudflare says the domain is **Active** (usually under an hour, sometimes up to a day).

## 3. Set up email sending (Resend)

1. In Resend: **Domains → Add domain → `nxtlvlsocial.ai`**.
2. Resend lists a few DNS records (SPF, DKIM, and so on). Add each one in Cloudflare under
   **DNS → Records**, exactly as shown. Turn the orange proxy cloud **off** for these records.
3. Wait for Resend to mark the domain **Verified**, then create an **API key** (Sending access). Copy it.

Without a verified domain, booking emails come from an unverified sender and land in spam.

## 4. Connect the domain (the automatic way, recommended)

The repository has a deploy workflow (`.github/workflows/deploy.yml`). Once three secrets are in GitHub, every
push to `main` deploys the site and the API and attaches `nxtlvlsocial.ai` and `www.nxtlvlsocial.ai` to it:
Cloudflare creates the DNS records and the HTTPS certificate on its own.

1. In Cloudflare, make an API token: **My Profile → API Tokens → Create Token → "Edit Cloudflare Workers"**
   template. Add the **Zone → DNS → Edit** permission for `nxtlvlsocial.ai` so the deploy can attach the domain.
   Copy the token. Your **Account ID** is on the right of the Workers & Pages overview page.
2. In GitHub: **Settings → Secrets and variables → Actions → New repository secret**, three times:
   - `CLOUDFLARE_API_TOKEN` — the token from step 1
   - `CLOUDFLARE_ACCOUNT_ID` — the account ID
   - `RESEND_API_KEY` — the key from step 3 (Resend)
3. Run it: **Actions → Deploy to Cloudflare → Run workflow**, pick the branch, Run. (It also runs by itself on
   every later push to `main`.) The last step opens the live site and fails loudly if any page is not a 200.

`www` is redirected to the bare domain by the Worker itself, so no dashboard redirect rule is needed.

## 4b. Deploy from your own computer instead

### Deploy the Worker

```bash
cd backend
npm install
npx wrangler login                        # opens the browser; allow access to your Cloudflare account
npx wrangler secret put RESEND_API_KEY    # paste the Resend key when asked
npm test                                  # optional: the form's tests, no accounts needed
npm run deploy
```

`npm run deploy` prints a test address like `https://nxtlvl-social.<your-name>.workers.dev`. Open it: the full
site should load, and the form should send you an email.

## 5. The domain is attached on deploy

`backend/wrangler.toml` lists both hostnames as custom domains, so `npm run deploy` (or the workflow) attaches
them and creates the DNS records. If Cloudflare refuses because the zone is not active yet, finish step 2 and
deploy again. The Worker answers `www` with a permanent redirect to `nxtlvlsocial.ai`.

## 6. Check it is live

- [ ] `https://nxtlvlsocial.ai` loads, and the padlock shows.
- [ ] `https://www.nxtlvlsocial.ai` redirects to it.
- [ ] `/social-media-design`, `/reel-editing` and `/social-media-automation` load.
- [ ] A made-up address like `/abc` shows the "page not found" page.
- [ ] `https://nxtlvlsocial.ai/api/health` shows `{"ok":true}`.
- [ ] Sending the booking form delivers an email to connect@nxtlvlsocial.ai, and a confirmation to the sender.
- [ ] `/sitemap.xml`, `/robots.txt` and `/llms.txt` open.

## 7. Tell search engines

1. **Google Search Console** (search.google.com/search-console): add a **Domain** property for `nxtlvlsocial.ai`.
   Verify with the TXT record it gives you (add it in Cloudflare DNS). Then go to **Sitemaps** and submit `sitemap.xml`.
   Use **URL Inspection → Request indexing** on the home page and the three service pages.
2. **Bing Webmaster Tools** (bing.com/webmasters): sign in and **import from Google Search Console**. Bing also feeds
   ChatGPT search and Copilot answers.
3. Check the structured data at **search.google.com/test/rich-results** and **validator.schema.org**.

## Updating the site later

Edit the files, then from `backend/`:

```bash
npm run deploy
```

The change is live within a few seconds.

### Optional: deploy automatically from GitHub

In Cloudflare: **Workers & Pages → nxtlvl-social → Settings → Build → Connect** to the GitHub repository.
- Root directory: `backend`
- Build command: leave empty
- Deploy command: `npx wrangler deploy`

Every push to the chosen branch then deploys on its own. Keep `RESEND_API_KEY` set as a secret in the Worker; never
commit it.

## Good to know

- **Lead storage and rate limits (optional):** `npx wrangler kv namespace create LEADS`, paste the id into
  `backend/wrangler.toml`, and deploy again. Every booking is then also saved, and each visitor is limited to
  5 bookings an hour.
- **Speed:** `website/_headers` caches fonts and libraries for a year and adds security headers. Cloudflare
  compresses everything automatically.
- **Motion testing:** add `?fx=lite` or `?fx=full` to any page address to force the light or the full
  animation mode on a device.
- **Other hosts:** to host the site on Netlify or Vercel instead, see "Hosting the site elsewhere" in
  `backend/README.md`.
