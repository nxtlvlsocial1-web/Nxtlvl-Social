import assert from 'node:assert/strict';
import { test } from 'node:test';
import { processWebhook, refreshExpiringTokens, type WebhookPayload } from '../src/handlers.ts';
import { account, commentPayload, fakeFetch, makeContext, messagingPayload, NOW } from './helpers.ts';

const DAY = 24 * 60 * 60 * 1000;
const run = (payload: unknown, ctx: Parameters<typeof processWebhook>[1]) => processWebhook(payload as WebhookPayload, ctx);

test('a keyword comment gets a private reply DM and a public reply', async () => {
  const { ctx, calls } = await makeContext();
  await run(commentPayload('Fight!! 🥊'), ctx);

  assert.equal(calls.length, 2);
  const [dm, publicReply] = calls;
  assert.equal(dm!.url.pathname, `/v23.0/${account.igUserId}/messages`);
  assert.equal(dm!.auth, 'Bearer token-1');
  assert.deepEqual(dm!.body.recipient, { comment_id: 'c1' });
  assert.equal(dm!.body.message.text, "Here's the free /court skill 🥊 https://github.com/alexyc9381/court-skill");
  assert.equal(publicReply!.url.pathname, '/v23.0/c1/replies');
  assert.equal(publicReply!.body.message, 'Sent! Check your DMs 📩');
});

test('comments without the keyword, or where the keyword is only part of a word, are ignored', async () => {
  const { ctx, calls } = await makeContext();
  await run(commentPayload('love this'), ctx);
  await run(commentPayload('fighter', { commentId: 'c2' }), ctx);
  assert.equal(calls.length, 0);
});

test("the account's own comments are ignored", async () => {
  const { ctx, calls } = await makeContext();
  await run(commentPayload('FIGHT', { from: account.igUserId }), ctx);
  assert.equal(calls.length, 0);
});

test('a webhook delivered twice sends one DM, and one person gets one DM per post', async () => {
  const { ctx, calls } = await makeContext();
  await run(commentPayload('FIGHT'), ctx);
  await run(commentPayload('FIGHT'), ctx);
  await run(commentPayload('fight again', { commentId: 'c2' }), ctx);
  assert.equal(calls.filter((c) => c.url.pathname.endsWith('/messages')).length, 1);

  await run(commentPayload('FIGHT', { commentId: 'c3', mediaId: 'm2' }), ctx);
  assert.equal(calls.filter((c) => c.url.pathname.endsWith('/messages')).length, 2);
});

test('comments older than 7 days are skipped', async () => {
  const { ctx, calls } = await makeContext();
  await run(commentPayload('FIGHT', { time: NOW - 8 * DAY }), ctx);
  assert.equal(calls.length, 0);
});

test('media_ids limits a trigger to those posts', async () => {
  const { ctx, calls } = await makeContext();
  ctx.rules().get('nxtlvl.social')!.comment_triggers[0]!.media_ids = ['m9'];
  await run(commentPayload('FIGHT', { mediaId: 'm1' }), ctx);
  assert.equal(calls.length, 0);
  await run(commentPayload('FIGHT', { commentId: 'c2', mediaId: 'm9' }), ctx);
  assert.equal(calls.length, 2);
});

test('a failed DM is not marked as sent, so a retry can send it', async () => {
  let fail = true;
  const { fn, calls } = fakeFetch(() => (fail ? { status: 400, json: { error: { message: 'nope', code: 100 } } } : undefined));
  const { ctx, logs } = await makeContext({ fetch: fn });
  await run(commentPayload('FIGHT'), ctx);
  assert.ok(logs.some((l) => l.level === 'error'));
  fail = false;
  await run(commentPayload('FIGHT'), ctx);
  assert.equal(calls.filter((c) => c.url.pathname.endsWith('/messages')).length, 2);
});

test('rate-limit errors are retried', async () => {
  let attempts = 0;
  const { fn } = fakeFetch((call) => {
    if (call.url.pathname.endsWith('/messages') && ++attempts === 1) return { status: 400, json: { error: { message: 'slow down', code: 613 } } };
    return undefined;
  });
  const { ctx } = await makeContext({ fetch: fn });
  await run(commentPayload('FIGHT'), ctx);
  assert.equal(attempts, 2);
});

test('events for an account that is not connected do nothing', async () => {
  const { ctx, calls } = await makeContext({ withAccount: false });
  await run(commentPayload('FIGHT'), ctx);
  assert.equal(calls.length, 0);
});

test('a DM with a comment keyword gets that DM, and other keywords get their reply', async () => {
  const { ctx, calls } = await makeContext();
  await run(messagingPayload({ message: { mid: 'in.1', text: 'creedom' } }), ctx);
  await run(messagingPayload({ message: { mid: 'in.2', text: 'How much is it?' } }), ctx);
  assert.deepEqual(calls[0]!.body.recipient, { id: 'u1' });
  assert.equal(calls[0]!.body.message.text, "Here's the link to audit your own page: https://example.com/creedom");
  assert.match(calls[1]!.body.message.text, /^Our packages start at/);
});

test('first contact gets the welcome, later unmatched DMs get the fallback once per 12 hours', async () => {
  const { ctx, calls, advance } = await makeContext();
  await run(messagingPayload({ message: { mid: 'in.1', text: 'hi' } }), ctx);
  await run(messagingPayload({ message: { mid: 'in.2', text: 'are you there' } }), ctx);
  await run(messagingPayload({ message: { mid: 'in.3', text: 'hello?' } }), ctx);
  assert.deepEqual(
    calls.map((c) => c.body.message.text.split(' ')[0]),
    ['Hey,', 'Thanks'],
  );
  advance(13 * 60 * 60 * 1000);
  await run(messagingPayload({ message: { mid: 'in.4', text: 'hello?' } }), ctx);
  assert.equal(calls.length, 3);
});

test('a duplicate message event is answered once', async () => {
  const { ctx, calls } = await makeContext();
  const payload = messagingPayload({ message: { mid: 'in.1', text: 'creedom' } });
  await run(payload, ctx);
  await run(payload, ctx);
  assert.equal(calls.length, 1);
});

test('when the team replies by hand, the bot stays quiet in that chat', async () => {
  const { ctx, calls, advance } = await makeContext();
  // Our own sends come back as echoes and must not count as the team replying.
  await run(messagingPayload({ message: { mid: 'in.1', text: 'creedom' } }), ctx);
  await run(
    messagingPayload({ sender: { id: account.igUserId }, recipient: { id: 'u1' }, message: { mid: 'mid.sent.1', text: 'x', is_echo: true } }),
    ctx,
  );
  await run(messagingPayload({ message: { mid: 'in.2', text: 'creedom' } }), ctx);
  assert.equal(calls.length, 2);

  await run(
    messagingPayload({ sender: { id: account.igUserId }, recipient: { id: 'u1' }, message: { mid: 'typed.by.team', text: 'hi!', is_echo: true } }),
    ctx,
  );
  await run(messagingPayload({ message: { mid: 'in.3', text: 'creedom' } }), ctx);
  assert.equal(calls.length, 2);

  advance(13 * 60 * 60 * 1000);
  await run(messagingPayload({ message: { mid: 'in.4', text: 'creedom' } }), ctx);
  assert.equal(calls.length, 3);
});

test('ice breaker taps and ig.me referrals get their replies', async () => {
  const { ctx, calls } = await makeContext();
  await run(messagingPayload({ postback: { mid: 'pb.1', title: 'How much does it cost?', payload: 'ICE_BREAKER_1' } }), ctx);
  await run(messagingPayload({ sender: { id: 'u2' }, referral: { ref: 'bio', source: 'IGME', type: 'OPEN_THREAD' } }), ctx);
  assert.match(calls[0]!.body.message.text, /^Our packages start at/);
  assert.match(calls[1]!.body.message.text, /bio link/);
});

test('tokens close to expiry are refreshed', async () => {
  const { fn, calls } = fakeFetch((call) =>
    call.url.pathname === '/refresh_access_token' ? { json: { access_token: 'token-2', expires_in: 5184000 } } : undefined,
  );
  const { ctx, store, advance } = await makeContext({ fetch: fn });
  assert.deepEqual(await refreshExpiringTokens(ctx), { refreshed: [], failed: [] });
  advance(40 * DAY);
  assert.deepEqual(await refreshExpiringTokens(ctx), { refreshed: ['nxtlvl.social'], failed: [] });
  assert.equal(calls[0]!.url.searchParams.get('grant_type'), 'ig_refresh_token');
  assert.equal((await store.getAccount(account.igUserId))!.accessToken, 'token-2');
});
