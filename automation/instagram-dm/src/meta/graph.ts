export type FetchFn = typeof fetch;

export interface OutgoingMessage {
  text: string;
  quick_replies?: { content_type: 'text'; title: string; payload: string }[];
}

/** A person by Instagram-scoped id, or a comment to answer with a private reply. */
export type Recipient = { id: string } | { comment_id: string };

export class GraphError extends Error {
  status: number;
  code: number | undefined;
  subcode: number | undefined;

  constructor(status: number, body: any) {
    const err = body?.error ?? {};
    super(`Graph API ${status}: ${err.message ?? JSON.stringify(body)}`);
    this.status = status;
    this.code = err.code;
    this.subcode = err.error_subcode;
  }

  get isRateLimit(): boolean {
    return this.status === 429 || [4, 17, 32, 613].includes(this.code ?? -1);
  }
}

interface GraphOptions {
  version: string;
  fetch?: FetchFn;
  sleep?: (ms: number) => Promise<void>;
  maxRetries?: number;
}

/** Calls to graph.instagram.com (Instagram API with Instagram Login). */
export class GraphClient {
  #base: string;
  #fetch: FetchFn;
  #sleep: (ms: number) => Promise<void>;
  #maxRetries: number;

  constructor(options: GraphOptions) {
    this.#base = `https://graph.instagram.com/${options.version}`;
    this.#fetch = options.fetch ?? fetch;
    this.#sleep = options.sleep ?? ((ms) => new Promise((resolve) => setTimeout(resolve, ms)));
    this.#maxRetries = options.maxRetries ?? 2;
  }

  async call(method: 'GET' | 'POST', path: string, token: string, body?: unknown, query?: Record<string, string>): Promise<any> {
    const url = new URL(this.#base + path);
    for (const [key, value] of Object.entries(query ?? {})) url.searchParams.set(key, value);
    for (let attempt = 0; ; attempt++) {
      const response = await this.#fetch(url, {
        method,
        headers: {
          Authorization: `Bearer ${token}`,
          ...(body === undefined ? {} : { 'Content-Type': 'application/json' }),
        },
        body: body === undefined ? undefined : JSON.stringify(body),
      });
      const json = await response.json().catch(() => ({}));
      if (response.ok) return json;
      const error = new GraphError(response.status, json);
      if (!error.isRateLimit || attempt >= this.#maxRetries) throw error;
      await this.#sleep(2000 * 2 ** attempt);
    }
  }

  /** Sends a DM, or a private reply when the recipient is a comment. */
  sendMessage(token: string, igUserId: string, recipient: Recipient, message: OutgoingMessage): Promise<{ recipient_id?: string; message_id?: string }> {
    return this.call('POST', `/${igUserId}/messages`, token, { recipient, message });
  }

  replyToComment(token: string, commentId: string, text: string): Promise<{ id: string }> {
    return this.call('POST', `/${commentId}/replies`, token, { message: text });
  }

  subscribeApp(token: string, fields: string[]): Promise<{ success: boolean }> {
    return this.call('POST', '/me/subscribed_apps', token, undefined, { subscribed_fields: fields.join(',') });
  }

  setIceBreakers(token: string, questions: { question: string; payload: string }[]): Promise<unknown> {
    return this.call('POST', '/me/messenger_profile', token, {
      platform: 'instagram',
      ice_breakers: [{ locale: 'default', call_to_actions: questions }],
    });
  }

  /** The professional account id (the id webhooks use in entry.id) and username. */
  getMe(token: string): Promise<{ user_id: string; username: string }> {
    return this.call('GET', '/me', token, undefined, { fields: 'user_id,username' });
  }
}
