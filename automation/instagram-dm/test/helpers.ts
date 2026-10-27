import { readFileSync } from 'node:fs';
import path from 'node:path';
import type { Config } from '../src/config.ts';
import type { Context } from '../src/handlers.ts';
import { GraphClient, type FetchFn } from '../src/meta/graph.ts';
import { OAuthClient } from '../src/meta/oauth.ts';
import { parseRules, type RulesByAccount } from '../src/rules.ts';
import { MemoryStore, type Account } from '../src/store.ts';

export const NOW = Date.UTC(2026, 9, 25, 12);

export const config: Config = {
  appId: 'app-id',
  appSecret: 'app-secret',
  verifyToken: 'verify-me',
  redirectUri: 'https://dm.example.com/oauth/callback',
  publicUrl: 'https://dm.example.com',
  adminToken: 'admin-token',
  graphVersion: 'v23.0',
  rulesDir: '/nowhere',
  dataFile: '/nowhere/store.json',
  port: 0,
  humanTakeoverHours: 12,
};

export const account: Account = {
  igUserId: '1784000000000001',
  appUserId: '9000001',
  username: 'nxtlvl.social',
  accessToken: 'token-1',
  expiresAt: NOW + 50 * 24 * 60 * 60 * 1000,
};

export function exampleRules(): RulesByAccount {
  const file = path.resolve(import.meta.dirname, '../examples/dm-automations.example.yaml');
  const rules = parseRules(readFileSync(file, 'utf8'), file);
  return new Map([[rules.account, rules]]);
}

export interface Call {
  method: string;
  url: URL;
  body: any;
  auth: string | null;
}

/** A fetch that records calls and answers from a list of handlers (default: 200 with a message id). */
export function fakeFetch(respond: (call: Call) => { status?: number; json?: unknown } | undefined = () => undefined) {
  const calls: Call[] = [];
  let counter = 0;
  const fn: FetchFn = async (input, init) => {
    const url = new URL(String(input));
    const raw = init?.body;
    const body = typeof raw === 'string' ? JSON.parse(raw) : raw instanceof URLSearchParams ? Object.fromEntries(raw) : undefined;
    const call = { method: init?.method ?? 'GET', url, body, auth: new Headers(init?.headers).get('authorization') };
    calls.push(call);
    const answer = respond(call) ?? { json: { recipient_id: 'r', message_id: `mid.sent.${++counter}` } };
    return Response.json(answer.json ?? {}, { status: answer.status ?? 200 });
  };
  return { fn, calls };
}

export async function makeContext(options: { fetch?: FetchFn; rules?: RulesByAccount; withAccount?: boolean } = {}) {
  const { fn, calls } = fakeFetch();
  const fetchFn = options.fetch ?? fn;
  let now = NOW;
  const store = new MemoryStore(() => now);
  if (options.withAccount !== false) await store.saveAccount(account);
  const deferred: Promise<unknown>[] = [];
  const logs: { level: string; message: string }[] = [];
  const rules = options.rules ?? exampleRules();
  const ctx: Context = {
    config,
    store,
    graph: new GraphClient({ version: 'v23.0', fetch: fetchFn, sleep: async () => {} }),
    oauth: new OAuthClient(config, fetchFn),
    rules: () => rules,
    reloadRules: () => {},
    log: (level, message) => logs.push({ level, message }),
    now: () => now,
    random: () => 0,
    defer: (work) => deferred.push(work),
  };
  return {
    ctx,
    calls,
    logs,
    store,
    advance: (ms: number) => {
      now += ms;
    },
    settle: () => Promise.all(deferred),
  };
}

export function commentPayload(text: string, overrides: { commentId?: string; from?: string; mediaId?: string; time?: number } = {}) {
  return {
    object: 'instagram',
    entry: [
      {
        id: account.igUserId,
        time: Math.floor((overrides.time ?? NOW) / 1000),
        changes: [
          {
            field: 'comments',
            value: {
              id: overrides.commentId ?? 'c1',
              text,
              from: { id: overrides.from ?? 'u1', username: 'fan' },
              media: { id: overrides.mediaId ?? 'm1', media_product_type: 'REELS' },
            },
          },
        ],
      },
    ],
  };
}

export function messagingPayload(event: Record<string, unknown>) {
  return {
    object: 'instagram',
    entry: [
      {
        id: account.igUserId,
        time: Math.floor(NOW / 1000),
        messaging: [{ sender: { id: 'u1' }, recipient: { id: account.igUserId }, timestamp: NOW, ...event }],
      },
    ],
  };
}
