import { createHmac } from 'node:crypto';
import type { Config } from '../config.ts';
import { GraphError, type FetchFn } from './graph.ts';
import { safeEqual } from './signature.ts';

export const SCOPES = [
  'instagram_business_basic',
  'instagram_business_manage_messages',
  'instagram_business_manage_comments',
];

const STATE_MAX_AGE_MS = 15 * 60 * 1000;

/** A signed, time-limited state value, so a callback can only come from a login we started. */
export function makeState(secret: string, now: number): string {
  const issued = String(now);
  return `${issued}.${createHmac('sha256', secret).update(issued).digest('base64url')}`;
}

export function isValidState(state: string | null, secret: string, now: number): boolean {
  const [issued, signature] = (state ?? '').split('.', 2);
  if (!issued || !signature) return false;
  const expected = createHmac('sha256', secret).update(issued).digest('base64url');
  return safeEqual(expected, signature) && now - Number(issued) <= STATE_MAX_AGE_MS;
}

export function authorizeUrl(config: Config, state: string): string {
  const url = new URL('https://www.instagram.com/oauth/authorize');
  url.searchParams.set('client_id', config.appId);
  url.searchParams.set('redirect_uri', config.redirectUri);
  url.searchParams.set('response_type', 'code');
  url.searchParams.set('scope', SCOPES.join(','));
  url.searchParams.set('state', state);
  return url.toString();
}

export interface LongLivedToken {
  accessToken: string;
  expiresAt: number;
}

export class OAuthClient {
  #config: Config;
  #fetch: FetchFn;

  constructor(config: Config, fetchFn: FetchFn = fetch) {
    this.#config = config;
    this.#fetch = fetchFn;
  }

  /** Swaps the login code for a short-lived token. user_id here is app-scoped. */
  async exchangeCode(code: string): Promise<{ accessToken: string; appUserId: string }> {
    const form = new URLSearchParams({
      client_id: this.#config.appId,
      client_secret: this.#config.appSecret,
      grant_type: 'authorization_code',
      redirect_uri: this.#config.redirectUri,
      code,
    });
    const json = await this.#json('https://api.instagram.com/oauth/access_token', { method: 'POST', body: form });
    const data = Array.isArray(json.data) ? json.data[0] : json;
    return { accessToken: data.access_token, appUserId: String(data.user_id) };
  }

  /** Short-lived (1 hour) to long-lived (about 60 days). */
  async toLongLived(shortToken: string, now: number): Promise<LongLivedToken> {
    const url = new URL('https://graph.instagram.com/access_token');
    url.searchParams.set('grant_type', 'ig_exchange_token');
    url.searchParams.set('client_secret', this.#config.appSecret);
    url.searchParams.set('access_token', shortToken);
    return this.#longLived(url, now);
  }

  /** Extends a long-lived token that is at least 24 hours old. */
  async refresh(token: string, now: number): Promise<LongLivedToken> {
    const url = new URL('https://graph.instagram.com/refresh_access_token');
    url.searchParams.set('grant_type', 'ig_refresh_token');
    url.searchParams.set('access_token', token);
    return this.#longLived(url, now);
  }

  async #longLived(url: URL, now: number): Promise<LongLivedToken> {
    const json = await this.#json(url, { method: 'GET' });
    return { accessToken: json.access_token, expiresAt: now + Number(json.expires_in) * 1000 };
  }

  async #json(url: string | URL, init: RequestInit): Promise<any> {
    const response = await this.#fetch(url, init);
    const json = await response.json().catch(() => ({}));
    if (!response.ok) throw new GraphError(response.status, json);
    return json;
  }
}
