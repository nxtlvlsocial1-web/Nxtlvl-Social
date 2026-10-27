import assert from 'node:assert/strict';
import { createHmac } from 'node:crypto';
import { test } from 'node:test';
import { createApp, WEBHOOK_PATH } from '../src/app.ts';
import { makeState } from '../src/meta/oauth.ts';
import { signBody } from '../src/meta/signature.ts';
import { account, commentPayload, config, fakeFetch, makeContext, NOW } from './helpers.ts';

const base = 'https://dm.example.com';

test('webhook verification echoes the challenge only for the right token', async () => {
  const { ctx } = await makeContext();
  const app = createApp(ctx);
  const ok = await app(new Request(`${base}${WEBHOOK_PATH}?hub.mode=subscribe&hub.verify_token=verify-me&hub.challenge=42`));
  assert.equal(ok.status, 200);
  assert.equal(await ok.text(), '42');
  const bad = await app(new Request(`${base}${WEBHOOK_PATH}?hub.mode=subscribe&hub.verify_token=wrong&hub.challenge=42`));
  assert.equal(bad.status, 403);
});

test('webhook POSTs need a valid signature, and are processed after the 200', async () => {
  const { ctx, calls, settle } = await makeContext();
  const app = createApp(ctx);
  const body = JSON.stringify(commentPayload('FIGHT 🥊'));

  const unsigned = await app(new Request(`${base}${WEBHOOK_PATH}`, { method: 'POST', body }));
  assert.equal(unsigned.status, 401);
  const forged = await app(
    new Request(`${base}${WEBHOOK_PATH}`, { method: 'POST', body, headers: { 'x-hub-signature-256': signBody(body, 'other-secret') } }),
  );
  assert.equal(forged.status, 401);

  const signed = await app(
    new Request(`${base}${WEBHOOK_PATH}`, { method: 'POST', body, headers: { 'x-hub-signature-256': signBody(body, config.appSecret) } }),
  );
  assert.equal(signed.status, 200);
  await settle();
  assert.equal(calls.length, 2);
});

test('oauth start redirects to Instagram with the messaging and comment scopes', async () => {
  const { ctx } = await makeContext();
  const response = await createApp(ctx)(new Request(`${base}/oauth/start`));
  assert.equal(response.status, 302);
  const location = new URL(response.headers.get('location')!);
  assert.equal(location.origin + location.pathname, 'https://www.instagram.com/oauth/authorize');
  assert.equal(location.searchParams.get('scope'), 'instagram_business_basic,instagram_business_manage_messages,instagram_business_manage_comments');
  assert.equal(location.searchParams.get('redirect_uri'), config.redirectUri);
});

test('oauth callback stores the account, subscribes webhooks and sets ice breakers', async () => {
  const { fn, calls } = fakeFetch((call) => {
    if (call.url.host === 'api.instagram.com') return { json: { data: [{ access_token: 'short', user_id: 9000001, permissions: 'x' }] } };
    if (call.url.pathname === '/access_token') return { json: { access_token: 'long', token_type: 'bearer', expires_in: 5184000 } };
    if (call.url.pathname.endsWith('/me')) return { json: { user_id: account.igUserId, username: 'nxtlvl.social' } };
    return { json: { success: true } };
  });
  const { ctx, store } = await makeContext({ fetch: fn, withAccount: false });
  const state = makeState(config.appSecret, NOW);
  const response = await createApp(ctx)(new Request(`${base}/oauth/callback?code=abc&state=${encodeURIComponent(state)}`));

  assert.equal(response.status, 200);
  assert.match(await response.text(), /Connected @nxtlvl\.social/);
  const saved = await store.getAccount(account.igUserId);
  assert.equal(saved?.accessToken, 'long');
  assert.equal(saved?.appUserId, '9000001');
  assert.equal(calls[0]!.body.code, 'abc');
  const subscribe = calls.find((c) => c.url.pathname.endsWith('/me/subscribed_apps'))!;
  assert.equal(subscribe.url.searchParams.get('subscribed_fields'), 'comments,messages,messaging_postbacks,messaging_referral');
  const ice = calls.find((c) => c.url.pathname.endsWith('/me/messenger_profile'))!;
  assert.equal(ice.body.ice_breakers[0].call_to_actions.length, 2);
});

test('oauth callback rejects a missing or stale state', async () => {
  const { ctx } = await makeContext();
  const app = createApp(ctx);
  assert.equal((await app(new Request(`${base}/oauth/callback?code=abc`))).status, 400);
  const old = makeState(config.appSecret, NOW - 60 * 60 * 1000);
  assert.equal((await app(new Request(`${base}/oauth/callback?code=abc&state=${encodeURIComponent(old)}`))).status, 400);
});

test('the data-deletion callback removes the account and returns a confirmation', async () => {
  const { ctx, store } = await makeContext();
  await store.claim(`welcomed:${account.igUserId}:u1`, 1000);
  const payload = Buffer.from(JSON.stringify({ user_id: account.appUserId, algorithm: 'HMAC-SHA256' })).toString('base64url');
  const signature = createHmac('sha256', config.appSecret).update(payload).digest('base64url');
  const response = await createApp(ctx)(
    new Request(`${base}/meta/data-deletion`, { method: 'POST', body: new URLSearchParams({ signed_request: `${signature}.${payload}` }) }),
  );
  assert.equal(response.status, 200);
  const json = (await response.json()) as { url: string; confirmation_code: string };
  assert.match(json.url, /^https:\/\/dm\.example\.com\/meta\/deletion-status\?code=/);
  assert.equal(await store.getAccount(account.igUserId), undefined);
  assert.equal(await store.has(`welcomed:${account.igUserId}:u1`), false);
});

test('admin routes need the admin token', async () => {
  const { ctx } = await makeContext();
  const app = createApp(ctx);
  assert.equal((await app(new Request(`${base}/admin/reload`, { method: 'POST' }))).status, 401);
  const ok = await app(new Request(`${base}/admin/reload`, { method: 'POST', headers: { authorization: 'Bearer admin-token' } }));
  assert.deepEqual(await ok.json(), { rules: ['nxtlvl.social'], connected: ['nxtlvl.social'], connectedWithoutRules: [] });
});
