// Runs the Worker's fetch handler in Node with a fake Resend, no Cloudflare account needed: `npm test`
import assert from 'node:assert/strict';
import worker from '../src/index.js';

const sent = [];
globalThis.fetch = async (url, init) => { sent.push(JSON.parse(init.body)); return new Response('{}', { status: 200 }); };

const env = { RESEND_API_KEY: 'test', LEAD_TO: 'connect@nxtlvlsocial.ai', LEAD_FROM: 'Nxtlvl Social <bookings@nxtlvlsocial.ai>', ALLOWED_ORIGINS: 'https://nxtlvlsocial.ai' };
const ctx = { waitUntil: (p) => p };
const post = (body, origin = 'https://nxtlvlsocial.ai') => worker.fetch(new Request('https://nxtlvlsocial.ai/api/book', {
  method: 'POST', headers: { 'Content-Type': 'application/json', Origin: origin, 'cf-connecting-ip': '1.2.3.4' }, body: JSON.stringify(body) }), env, ctx);

let r = await post({ name: 'Asha', business: 'The Corner Café', phone: '+91 98765 43210', email: 'asha@example.com', need: 'video', message: 'Reels for Diwali', t: Date.now() - 10000 });
assert.equal(r.status, 200); assert.deepEqual(await r.json(), { ok: true });
assert.equal(sent.length, 2, 'lead email + confirmation');
assert.equal(sent[0].to[0], 'connect@nxtlvlsocial.ai');
assert.match(sent[0].subject, /Asha · The Corner Café/);
assert.match(sent[0].text, /Video & Editing/);
assert.equal(sent[0].reply_to, 'asha@example.com');
assert.equal(sent[1].to[0], 'asha@example.com');
assert.equal(r.headers.get('Access-Control-Allow-Origin'), 'https://nxtlvlsocial.ai');

sent.length = 0;
r = await post({ name: 'A', phone: '+91 98765 43210', t: Date.now() - 10000 });
assert.equal(r.status, 400); assert.match((await r.json()).error, /name/);

r = await post({ name: 'Ravi', t: Date.now() - 10000 });
assert.equal(r.status, 400); assert.match((await r.json()).error, /WhatsApp number or an email/);

r = await post({ name: 'Bot', phone: '+91 98765 43210', website: 'http://spam', t: Date.now() - 10000 });
assert.equal(r.status, 200); assert.equal(sent.length, 0, 'honeypot: accepted silently, nothing sent');

r = await post({ name: 'Fast', phone: '+91 98765 43210', t: Date.now() });
assert.equal(r.status, 200); assert.equal(sent.length, 0, 'too fast: accepted silently, nothing sent');

r = await post({ name: 'Priya', phone: '98765 43210', need: 'nope', t: Date.now() - 10000 });
assert.equal(r.status, 200); assert.match(sent[0].text, /Not sure yet/); assert.equal(sent.length, 1, 'no email given: no confirmation');

r = await post({ name: 'X', phone: '+91 98765 43210' }, 'https://evil.example');
assert.equal(r.headers.get('Access-Control-Allow-Origin'), null, 'unknown origin gets no CORS header');

r = await worker.fetch(new Request('https://nxtlvlsocial.ai/api/health'), env, ctx);
assert.deepEqual(await r.json(), { ok: true });

r = await worker.fetch(new Request('https://nxtlvlsocial.ai/api/book', { method: 'POST', body: '{"name":"Zara","phone":"+91 12345 67890"}' }), { ...env, RESEND_API_KEY: '' }, ctx);
assert.equal(r.status, 503);

console.log('backend tests passed');
