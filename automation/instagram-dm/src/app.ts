import { randomBytes } from 'node:crypto';
import {
  processWebhook,
  refreshExpiringTokens,
  syncIceBreakers,
  WEBHOOK_FIELDS,
  type Context,
  type WebhookPayload,
} from './handlers.ts';
import { authorizeUrl, isValidState, makeState } from './meta/oauth.ts';
import { isValidSignature, parseSignedRequest, safeEqual } from './meta/signature.ts';

export const WEBHOOK_PATH = '/webhooks/instagram';

/** A fetch-style handler, so the same app runs on Node, Workers or Vercel. */
export function createApp(ctx: Context): (request: Request) => Promise<Response> {
  return async (request) => {
    const url = new URL(request.url);
    const route = `${request.method} ${url.pathname}`;
    try {
      switch (route) {
        case 'GET /healthz':
          return text('ok');
        case `GET ${WEBHOOK_PATH}`:
          return verifyWebhook(ctx, url);
        case `POST ${WEBHOOK_PATH}`:
          return await receiveWebhook(ctx, request);
        case 'GET /oauth/start':
          return Response.redirect(authorizeUrl(ctx.config, makeState(ctx.config.appSecret, ctx.now())), 302);
        case 'GET /oauth/callback':
          return await oauthCallback(ctx, url);
        case 'POST /meta/deauthorize':
          return await deleteFromSignedRequest(ctx, request, false);
        case 'POST /meta/data-deletion':
          return await deleteFromSignedRequest(ctx, request, true);
        case 'GET /meta/deletion-status':
          return text(`Deletion request ${url.searchParams.get('code') ?? ''}: all stored data for this account has been deleted.`);
        case 'POST /admin/reload':
          return isAdmin(ctx, request) ? await reload(ctx) : text('unauthorized', 401);
        case 'POST /admin/refresh-tokens':
          return isAdmin(ctx, request) ? Response.json(await refreshExpiringTokens(ctx)) : text('unauthorized', 401);
        default:
          return text('not found', 404);
      }
    } catch (error) {
      ctx.log('error', 'request failed', { route, error: String(error) });
      return text('internal error', 500);
    }
  };
}

function verifyWebhook(ctx: Context, url: URL): Response {
  const params = url.searchParams;
  if (params.get('hub.mode') === 'subscribe' && safeEqual(params.get('hub.verify_token') ?? '', ctx.config.verifyToken)) {
    return text(params.get('hub.challenge') ?? '');
  }
  return text('forbidden', 403);
}

async function receiveWebhook(ctx: Context, request: Request): Promise<Response> {
  const body = new Uint8Array(await request.arrayBuffer());
  if (!isValidSignature(body, request.headers.get('x-hub-signature-256'), ctx.config.appSecret)) {
    ctx.log('warn', 'webhook with a bad signature');
    return text('bad signature', 401);
  }
  let payload: WebhookPayload;
  try {
    payload = JSON.parse(Buffer.from(body).toString('utf8'));
  } catch {
    return text('bad json', 400);
  }
  // Meta wants a 200 within a few seconds; the replies happen after.
  ctx.defer(processWebhook(payload, ctx).catch((error) => ctx.log('error', 'webhook processing failed', { error: String(error) })));
  return text('EVENT_RECEIVED');
}

async function oauthCallback(ctx: Context, url: URL): Promise<Response> {
  const error = url.searchParams.get('error_description') ?? url.searchParams.get('error');
  if (error) return page(`Instagram didn't connect: ${error}`, 400);
  if (!isValidState(url.searchParams.get('state'), ctx.config.appSecret, ctx.now())) {
    return page('This login link has expired. Start again from the connect link.', 400);
  }
  const code = url.searchParams.get('code');
  if (!code) return page('Missing login code.', 400);

  const short = await ctx.oauth.exchangeCode(code);
  const token = await ctx.oauth.toLongLived(short.accessToken, ctx.now());
  const me = await ctx.graph.getMe(token.accessToken);
  const account = {
    igUserId: String(me.user_id),
    appUserId: short.appUserId,
    username: me.username,
    accessToken: token.accessToken,
    expiresAt: token.expiresAt,
  };
  await ctx.store.saveAccount(account);
  await ctx.graph.subscribeApp(account.accessToken, WEBHOOK_FIELDS);
  const rules = ctx.rules().get(account.username.toLowerCase());
  await syncIceBreakers(ctx, account, rules);
  ctx.log('info', 'account connected', { account: account.username, igUserId: account.igUserId });

  const note = rules
    ? `Its rules come from ${rules.file.split(/[\\/]/).slice(-2).join('/')}.`
    : `There is no brands/&lt;client&gt;/dm-automations.yaml with <code>account: ${escapeHtml(account.username)}</code> yet, so nothing will be sent until one is added.`;
  return page(`Connected @${escapeHtml(account.username)}. ${note} You can close this page.`);
}

async function deleteFromSignedRequest(ctx: Context, request: Request, wantsStatus: boolean): Promise<Response> {
  const form = await request.formData();
  const payload = parseSignedRequest(String(form.get('signed_request') ?? ''), ctx.config.appSecret);
  if (!payload?.user_id) return text('bad signed_request', 400);
  const removed = await ctx.store.deleteAccount(String(payload.user_id));
  ctx.log('info', 'deleted account data on Meta request', { found: Boolean(removed) });
  if (!wantsStatus) return text('ok');
  const code = randomBytes(8).toString('hex');
  return Response.json({ url: `${ctx.config.publicUrl}/meta/deletion-status?code=${code}`, confirmation_code: code });
}

async function reload(ctx: Context): Promise<Response> {
  ctx.reloadRules();
  const rules = ctx.rules();
  const accounts = await ctx.store.listAccounts();
  for (const account of accounts) await syncIceBreakers(ctx, account, rules.get(account.username.toLowerCase()));
  return Response.json({
    rules: [...rules.keys()],
    connected: accounts.map((a) => a.username),
    connectedWithoutRules: accounts.filter((a) => !rules.has(a.username.toLowerCase())).map((a) => a.username),
  });
}

function isAdmin(ctx: Context, request: Request): boolean {
  return safeEqual(request.headers.get('authorization') ?? '', `Bearer ${ctx.config.adminToken}`);
}

function text(body: string, status = 200): Response {
  return new Response(body, { status, headers: { 'content-type': 'text/plain; charset=utf-8' } });
}

function page(message: string, status = 200): Response {
  const html = `<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Nxtlvl Social</title><body style="font:16px system-ui;max-width:32rem;margin:4rem auto;padding:0 1rem"><p>${message}</p>`;
  return new Response(html, { status, headers: { 'content-type': 'text/html; charset=utf-8' } });
}

function escapeHtml(value: string): string {
  return value.replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);
}
