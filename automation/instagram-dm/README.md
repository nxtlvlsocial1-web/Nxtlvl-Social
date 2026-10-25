# Instagram DM automation

A small service that answers on Instagram for Nxtlvl Social and its clients, using only Meta's official
Instagram API (Instagram API with Instagram Login):

- **Comment-to-DM.** Someone comments the keyword from a reel's CTA ("Comment FIGHT and I'll DM you the
  skill") and gets the DM within seconds, as a private reply to their comment. Optionally a short public reply
  ("Sent! Check your DMs 📩") goes under the comment.
- **DM auto-replies.** Keyword replies, a welcome for first-time messages, and a fallback that tells people
  the team will answer.
- **Welcome flows.** Up to 4 ice breakers on a new chat, and replies for `ig.me/<username>?ref=<ref>` links.
- **Human takeover.** When someone on the team replies in the Instagram app, the bot stays quiet in that chat
  for 12 hours.

It does **not** follow accounts or send DMs to people who haven't contacted the account. Meta has no API for
either, and doing them with bots breaks Instagram's terms and gets accounts banned.

## How it works

```
Instagram ──webhook──▶ POST /webhooks/instagram ──▶ check signature, reply 200
                                                      └─▶ match rules ──▶ Graph API: private reply / DM
Client ──▶ GET /oauth/start ──▶ Instagram login ──▶ /oauth/callback ──▶ save token, subscribe webhooks, set ice breakers
```

| Path                           | What it does                                                              |
| ------------------------------ | ------------------------------------------------------------------------- |
| `GET /webhooks/instagram`      | Meta's verification handshake (checks `WEBHOOK_VERIFY_TOKEN`)             |
| `POST /webhooks/instagram`     | Webhook events; rejects anything without a valid `X-Hub-Signature-256`    |
| `GET /oauth/start`             | Send a client here to connect their Instagram account                     |
| `GET /oauth/callback`          | Finishes the login                                                         |
| `POST /meta/deauthorize`       | Meta's deauthorize callback: deletes that account's data                  |
| `POST /meta/data-deletion`     | Meta's data-deletion callback: deletes and returns a confirmation code    |
| `POST /admin/reload`           | Re-reads the rules files and re-sends ice breakers (`Authorization: Bearer $ADMIN_TOKEN`) |
| `POST /admin/refresh-tokens`   | Refreshes tokens expiring within 15 days (the server also does this daily) |
| `GET /healthz`                 | Health check                                                               |

Code: `src/app.ts` (routes), `src/handlers.ts` (the flows), `src/rules.ts` (rules files), `src/meta/` (Graph
API, OAuth, signatures), `src/store.ts` (tokens and dedupe state, saved to `data/store.json`).

## Rules: one file per client

Each client's rules live with their brand kit in `brands/<client>/dm-automations.yaml`. Copy
[`examples/dm-automations.example.yaml`](examples/dm-automations.example.yaml) and edit it. The `account` must
be the Instagram username that connects through `/oauth/start`.

When a video with a "Comment KEYWORD" CTA is delivered, add a `comment_triggers` entry with the keyword from
its `script.md` / `CAPTION.md`, then:

```bash
npm run check-rules          # validates every rules file
curl -X POST -H "Authorization: Bearer $ADMIN_TOKEN" https://<host>/admin/reload
```

The `/nxtlvl-instagram-dm` skill does this for you.

Meta's limits the rules have to live with: a private reply can only be sent once per comment and within 7
days of it; DM replies only within 24 hours of the person's last message. Each person gets one DM per post
per trigger, however many times they comment.

## Run it

Node 22.18 or newer (it runs the TypeScript directly).

```bash
cd automation/instagram-dm
npm install
cp .env.example .env         # fill it in
node --env-file=.env src/server.ts
npm test                     # 27 tests, no network
npm run typecheck
```

It needs a public HTTPS URL for Meta's webhooks. For development, run it locally behind a tunnel
(`cloudflared tunnel --url http://localhost:3000` or ngrok). For production, any always-on Node host works
(Render, Railway, Fly.io, a small VPS). Keep `data/store.json` on a persistent disk: it holds the clients'
access tokens. `createApp` is a plain `fetch(Request) → Response` handler, so moving to Cloudflare Workers or
Vercel later only needs a new entry file and a database-backed `Store`.

## Meta app setup checklist

Do these in order. Steps 1 to 8 are enough to test on our own account; steps 9 to 11 are for client accounts.

1. **Professional account.** Each Instagram account must be a Business or Creator account
   (Instagram app → Settings → Account type and tools).
2. **Allow message access.** On each account: Instagram app → Settings → Messages and calls →
   Connected tools → turn on **Allow access to messages**. Without it, DM webhooks and sends fail.
3. **Business portfolio.** Create (or use) the Nxtlvl Social business portfolio at business.facebook.com.
4. **Create the app.** At developers.facebook.com → My Apps → Create App → type **Business**, owned by that
   portfolio. Add the **Instagram** product and choose **API setup with Instagram login**.
5. **Credentials.** Copy the Instagram app ID and app secret into `.env` (`IG_APP_ID`, `IG_APP_SECRET`).
6. **Business login settings.** Add `https://<host>/oauth/callback` as a valid OAuth redirect URI,
   `https://<host>/meta/deauthorize` as the deauthorize callback and `https://<host>/meta/data-deletion` as
   the data-deletion request URL.
7. **Webhooks.** In the Instagram product's webhook settings: callback URL `https://<host>/webhooks/instagram`,
   verify token = `WEBHOOK_VERIFY_TOKEN`. Subscribe to `comments`, `messages`, `messaging_postbacks` and
   `messaging_referral`. (Connecting an account through `/oauth/start` subscribes that account automatically.)
8. **Test on our account.** Add the Nxtlvl Instagram account as an Instagram tester (App roles), accept the
   invite in Instagram, open `https://<host>/oauth/start` and log in. Comment a keyword from a second account
   and check the DM arrives.
9. **App basics.** Fill in the privacy policy URL, terms URL, app icon, category and contact email. The privacy
   policy must say what we store (account tokens, message and comment ids for dedupe) and how to request
   deletion.
10. **Business verification.** Verify the business in the portfolio's Security Center. Needed for Advanced Access.
11. **App Review.** Request **Advanced Access** for `instagram_business_basic`,
    `instagram_business_manage_messages` and `instagram_business_manage_comments`. For each, record a
    screencast of the flow on our test account (login, a comment getting its DM, a DM auto-reply) and
    explain why we need it. Review usually takes 1 to 3 weeks. Once approved, switch the app to Live and send
    clients the `/oauth/start` link.
