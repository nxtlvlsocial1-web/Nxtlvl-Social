/* Nxtlvl Social backend: a Cloudflare Worker that serves the website and takes "Book a call" requests.
 *
 *   POST /api/book    JSON {name, business, email, need, message, website, t}  ->  {ok:true}
 *   GET  /api/health  ->  {ok:true}
 *
 * Every lead is emailed to LEAD_TO (connect@nxtlvlsocial.ai) through Resend, and the person gets a short
 * confirmation. Static files come from ../website (see wrangler.toml).
 */

const NEEDS = {
  design: 'Content & Design',
  video: 'Video & Editing',
  automation: 'Social + Automation',
  website: 'Website Development',
  unsure: 'Not sure yet',
};
const MAX = { name: 80, business: 120, email: 120, message: 2000 };

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === '/api/health') return json({ ok: true });
    if (url.pathname === '/api/book') {
      if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors(request, env) });
      if (request.method !== 'POST') return json({ ok: false, error: 'Use POST.' }, 405, cors(request, env));
      return book(request, env, ctx);
    }
    // everything else is the website (Workers static assets); an unknown path gets 404.html with a 404 status
    if (env.ASSETS) return env.ASSETS.fetch(request);
    return json({ ok: false, error: 'Not found.' }, 404);
  },
};

async function book(request, env, ctx) {
  const headers = cors(request, env);
  let body;
  try { body = await request.json(); } catch (e) { return json({ ok: false, error: 'Send JSON.' }, 400, headers); }
  const lead = clean(body);
  const problem = validate(lead, body);
  if (problem) return json({ ok: false, error: problem }, 400, headers);

  // simple abuse brakes: a hidden field that only bots fill, and a form that was submitted too fast
  if (body.website) return json({ ok: true }, 200, headers);
  if (typeof body.t === 'number' && Date.now() - body.t < 2500) return json({ ok: true }, 200, headers);

  const ip = request.headers.get('cf-connecting-ip') || 'unknown';
  if (env.LEADS) {
    const key = `rate:${ip}`;
    const n = Number((await env.LEADS.get(key)) || 0);
    if (n >= Number(env.RATE_LIMIT || 5)) return json({ ok: false, error: 'Too many requests. Please try again in an hour.' }, 429, headers);
    ctx.waitUntil(env.LEADS.put(key, String(n + 1), { expirationTtl: 3600 }));
    ctx.waitUntil(env.LEADS.put(`lead:${new Date().toISOString()}:${crypto.randomUUID()}`, JSON.stringify({ ...lead, ip, ua: request.headers.get('user-agent') || '' })));
  }

  if (!env.RESEND_API_KEY) return json({ ok: false, error: 'Email is not set up yet.' }, 503, headers);
  const to = env.LEAD_TO || 'connect@nxtlvlsocial.ai';
  const from = env.LEAD_FROM || 'Nxtlvl Social <bookings@nxtlvlsocial.ai>';

  const sent = await resend(env, {
    from, to: [to], reply_to: lead.email,
    subject: `New call request: ${lead.name}${lead.business ? ' · ' + lead.business : ''}`,
    text: leadText(lead, ip), html: leadHtml(lead, ip),
  });
  if (!sent.ok) return json({ ok: false, error: 'Could not send right now. Please email ' + to + ' directly.' }, 502, headers);

  ctx.waitUntil(resend(env, {
    from, to: [lead.email], reply_to: to,
    subject: 'Got it. Your free call with Nxtlvl Social',
    text: `Hi ${lead.name},\n\nThanks for reaching out. We've got your request and a person will reply by email within one business day to set up your 15-minute call.\n\nWhat you told us:\n${summary(lead)}\n\nIf anything changes, just reply to this email.\n\nNxtlvl Social\n${to}`,
  }));
  return json({ ok: true }, 200, headers);
}

function clean(b) {
  const s = (v, max) => (typeof v === 'string' ? v.replace(/[\u0000-\u001f\u007f]+/g, ' ').trim().slice(0, max) : '');
  return {
    name: s(b.name, MAX.name), business: s(b.business, MAX.business),
    email: s(b.email, MAX.email).toLowerCase(), need: NEEDS[b.need] ? b.need : 'unsure', message: s(b.message, MAX.message),
  };
}

function validate(l) {
  if (l.name.length < 2) return 'Please tell us your name.';
  if (!l.email) return 'Leave your email so we can reply.';
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(l.email)) return 'That email does not look right.';
  return null;
}

function summary(l) {
  return [`Name: ${l.name}`, l.business && `Business: ${l.business}`, `Email: ${l.email}`,
    `Looking for: ${NEEDS[l.need]}`, l.message && `Message: ${l.message}`].filter(Boolean).join('\n');
}
function leadText(l, ip) { return `${summary(l)}\n\nReceived ${new Date().toUTCString()} from ${ip}`; }
function leadHtml(l, ip) {
  const esc = (v) => String(v).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const row = (k, v) => v ? `<tr><td style="padding:6px 14px 6px 0;color:#6B6391">${k}</td><td style="padding:6px 0">${esc(v)}</td></tr>` : '';
  const reply = `<p><a href="mailto:${esc(l.email)}" style="display:inline-block;padding:10px 18px;border-radius:999px;background:#7D18FC;color:#fff;text-decoration:none;font-weight:600">Reply by email</a></p>`;
  return `<div style="font-family:Instrument Sans,Segoe UI,Arial,sans-serif;font-size:15px;color:#0B0816">
  <h2 style="margin:0 0 12px;font-size:20px">New call request</h2>
  <table style="border-collapse:collapse">${row('Name', l.name)}${row('Business', l.business)}${row('Email', l.email)}${row('Looking for', NEEDS[l.need])}${row('Message', l.message)}</table>
  ${reply}<p style="color:#9F97BE;font-size:12px">Received ${new Date().toUTCString()} from ${esc(ip)}</p></div>`;
}

async function resend(env, msg) {
  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST', headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' }, body: JSON.stringify(msg),
    });
    return { ok: r.ok, status: r.status };
  } catch (e) { return { ok: false, status: 0 }; }
}

function cors(request, env) {
  const origin = request.headers.get('Origin') || '';
  const allowed = (env.ALLOWED_ORIGINS || '').split(',').map((s) => s.trim()).filter(Boolean);
  const h = { 'Access-Control-Allow-Methods': 'POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type', 'Access-Control-Max-Age': '86400', Vary: 'Origin' };
  if (allowed.includes(origin) || allowed.includes('*')) h['Access-Control-Allow-Origin'] = origin;
  return h;
}

function json(data, status = 200, headers = {}) {
  return new Response(JSON.stringify(data), { status, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...headers } });
}
