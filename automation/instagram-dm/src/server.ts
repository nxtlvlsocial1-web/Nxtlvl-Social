import { createServer } from 'node:http';
import { createApp } from './app.ts';
import { loadConfig } from './config.ts';
import { refreshExpiringTokens, type Context, type Logger } from './handlers.ts';
import { GraphClient } from './meta/graph.ts';
import { OAuthClient } from './meta/oauth.ts';
import { loadRules } from './rules.ts';
import { FileStore } from './store.ts';

const config = loadConfig();
const log: Logger = (level, message, data) =>
  console[level === 'info' ? 'log' : level](JSON.stringify({ time: new Date().toISOString(), level, message, ...data }));

let rules = loadRules(config.rulesDir);
const ctx: Context = {
  config,
  store: new FileStore(config.dataFile),
  graph: new GraphClient({ version: config.graphVersion }),
  oauth: new OAuthClient(config),
  rules: () => rules,
  reloadRules: () => {
    rules = loadRules(config.rulesDir);
  },
  log,
  now: Date.now,
  random: Math.random,
  defer: (work) => void work,
};
const app = createApp(ctx);

const server = createServer(async (req, res) => {
  const chunks: Buffer[] = [];
  for await (const chunk of req) chunks.push(chunk as Buffer);
  const request = new Request(`http://${req.headers.host ?? 'localhost'}${req.url}`, {
    method: req.method,
    headers: Object.entries(req.headers).flatMap(([k, v]) => (v === undefined ? [] : [[k, String(v)]] as [string, string][])),
    body: req.method === 'GET' || req.method === 'HEAD' ? undefined : Buffer.concat(chunks),
  });
  const response = await app(request);
  res.writeHead(response.status, Object.fromEntries(response.headers));
  res.end(Buffer.from(await response.arrayBuffer()));
});

server.listen(config.port, () => {
  log('info', 'listening', { port: config.port, accountsWithRules: [...rules.keys()] });
});

// Long-lived tokens last about 60 days; check once a day.
const refresh = () => refreshExpiringTokens(ctx).catch((error) => log('error', 'token refresh run failed', { error: String(error) }));
setInterval(refresh, 24 * 60 * 60 * 1000).unref();
refresh();
