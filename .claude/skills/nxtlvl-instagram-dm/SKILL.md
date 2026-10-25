---
name: nxtlvl-instagram-dm
description: >
  Set up or change Nxtlvl Social's Instagram DM automations: the "Comment KEYWORD and I'll DM you" keyword
  that sends a reel's link by DM, DM auto-replies, welcome messages, ice breakers and ig.me links. Use when a
  video with a comment CTA is delivered, when a client wants a keyword or auto-reply added, or when someone
  asks how the Instagram DM service works or how to connect an account. Never use it to follow accounts or
  DM people who haven't contacted the account.
---

# Nxtlvl Social — Instagram DM automations

The service is in `automation/instagram-dm/` (read its `README.md` for routes, setup and the Meta app
checklist). Rules live with each client's brand kit in `brands/<client>/dm-automations.yaml`; the format is
in `automation/instagram-dm/examples/dm-automations.example.yaml`.

## Hard limits

- No auto-follow, follow/unfollow, or DMs to people who never messaged or commented. Meta has no API for
  them and they get accounts banned. If asked, say so and offer a compliant option (comment CTA, `ig.me`
  ref link, Click-to-Instagram-Direct ad, collab post).
- Instagram only allows one private-reply DM per comment, within 7 days of it, and DM replies within 24
  hours of the person's last message. Don't promise anything outside that in a caption.
- Every DM goes to real people under the client's name. The person approves the wording and link before it
  goes live, like any other client copy.

## Add a comment keyword for a video

1. Find the keyword and the promise. Look in the project's `script.md` (`CTA KEYWORD:` in the header and the
   CTA line) and `CAPTION.md`. If the keyword is still marked "to confirm", ask.
2. Find what the DM must deliver: the link, file or guide the caption promises. If there is no link yet, ask
   for it; don't invent one.
3. Open (or create from the example) `brands/<client>/dm-automations.yaml`. `account` is the client's
   Instagram username without the @.
4. Add a `comment_triggers` entry: `keywords`, `project` (the video folder), `dm` with `{link}`, `link`
   (https only), and 2 or 3 short `public_replies` in the brand's voice. Leave `media_ids` empty unless the
   same keyword is reused on another post with a different link; then add the post's media id.
5. Check the keyword doesn't clash with another trigger or `dm_replies` keyword for that account, and that the
   DM delivers exactly what the caption promises.
6. Validate: `cd automation/instagram-dm && npm run check-rules`.
7. Show the person the entry (keyword, DM text, public replies) and get approval.
8. Commit the rules file. After it's deployed, reload:
   `curl -X POST -H "Authorization: Bearer $ADMIN_TOKEN" https://<host>/admin/reload`. The response lists
   accounts with rules and any connected account that has none.

## Other changes

- **DM auto-replies:** `dm_replies` (first match wins), `welcome` (first message ever), `fallback` (at most
  once per 12 h per person; it should say the team will reply).
- **Ice breakers:** at most 4. They're pushed to Instagram on connect and on `/admin/reload`.
- **ig.me links:** add a `referrals` entry and give the person `https://ig.me/m/<username>?ref=<ref>`.
- **Connect a client account:** they need a Professional account with "Allow access to messages" on, then
  open `https://<host>/oauth/start` and log in. Until App Review is approved, only accounts added as app
  testers can connect.

## When you change the service code

Run `npm test` and `npm run typecheck` in `automation/instagram-dm/`. Keep to the official Graph API.
