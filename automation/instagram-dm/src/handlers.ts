import type { Config } from './config.ts';
import type { GraphClient } from './meta/graph.ts';
import type { OAuthClient } from './meta/oauth.ts';
import {
  iceBreakerPayload,
  matchesKeyword,
  renderDm,
  type AccountRules,
  type RulesByAccount,
} from './rules.ts';
import type { Account, Store } from './store.ts';

export type Logger = (level: 'info' | 'warn' | 'error', message: string, data?: Record<string, unknown>) => void;

export interface Context {
  config: Config;
  store: Store;
  graph: GraphClient;
  oauth: OAuthClient;
  rules: () => RulesByAccount;
  reloadRules: () => void;
  log: Logger;
  now: () => number;
  random: () => number;
  /** Runs work after the webhook has been acknowledged. */
  defer: (work: Promise<unknown>) => void;
}

// Shapes of the webhook payloads we read. Meta sends more fields than these.
export interface WebhookPayload {
  object: string;
  entry?: WebhookEntry[];
}

interface WebhookEntry {
  id: string;
  time: number;
  changes?: { field: string; value: CommentValue }[];
  messaging?: MessagingEvent[];
}

interface CommentValue {
  id: string;
  text?: string;
  parent_id?: string;
  from?: { id: string; username?: string };
  media?: { id: string; media_product_type?: string };
}

export interface MessagingEvent {
  sender: { id: string };
  recipient: { id: string };
  timestamp: number;
  message?: { mid: string; text?: string; is_echo?: boolean; quick_reply?: { payload: string } };
  postback?: { mid: string; title?: string; payload: string };
  referral?: { ref?: string; source?: string; type?: string };
}

const HOUR = 60 * 60 * 1000;
const DAY = 24 * HOUR;
/** Meta allows one private reply per comment, within 7 days of it. */
const PRIVATE_REPLY_WINDOW = 7 * DAY;
export const WEBHOOK_FIELDS = ['comments', 'messages', 'messaging_postbacks', 'messaging_referral'];

export async function processWebhook(payload: WebhookPayload, ctx: Context): Promise<void> {
  if (payload.object !== 'instagram') return;
  for (const entry of payload.entry ?? []) {
    const account = await ctx.store.getAccount(entry.id);
    if (!account) {
      ctx.log('warn', 'webhook for an account that is not connected', { igUserId: entry.id });
      continue;
    }
    const rules = ctx.rules().get(account.username.toLowerCase());
    for (const change of entry.changes ?? []) {
      if (change.field !== 'comments') continue;
      await guard(ctx, 'comment', () => handleComment(ctx, account, rules, change.value, entry.time * 1000));
    }
    for (const event of entry.messaging ?? []) {
      await guard(ctx, 'messaging', () => handleMessaging(ctx, account, rules, event));
    }
  }
}

async function guard(ctx: Context, kind: string, work: () => Promise<void>): Promise<void> {
  try {
    await work();
  } catch (error) {
    ctx.log('error', `${kind} event failed`, { error: String(error) });
  }
}

export async function handleComment(
  ctx: Context,
  account: Account,
  rules: AccountRules | undefined,
  comment: CommentValue,
  commentedAt: number,
): Promise<void> {
  const acct = account.igUserId;
  const from = comment.from?.id;
  // Our own comments include the public "check your DMs" replies we post.
  if (!rules || !from || from === acct || !comment.text) return;

  const mediaId = comment.media?.id ?? '';
  const index = rules.comment_triggers.findIndex(
    (t) => (t.media_ids.length === 0 || t.media_ids.includes(mediaId)) && matchesKeyword(comment.text!, t.keywords),
  );
  if (index === -1) return;
  const trigger = rules.comment_triggers[index]!;

  if (ctx.now() - commentedAt > PRIVATE_REPLY_WINDOW) {
    ctx.log('info', 'comment is older than 7 days, skipping', { commentId: comment.id });
    return;
  }
  const commentKey = `comment:${acct}:${comment.id}`;
  if (!(await ctx.store.claim(commentKey, 8 * DAY))) return;
  // One DM per person per post, even if they comment the keyword again.
  const personKey = `commenter:${acct}:${mediaId}:${from}:${index}`;
  if (!(await ctx.store.claim(personKey, 90 * DAY))) {
    ctx.log('info', 'already sent this person the DM for this post', { commentId: comment.id });
    return;
  }

  try {
    const sent = await ctx.graph.sendMessage(account.accessToken, acct, { comment_id: comment.id }, { text: renderDm(trigger) });
    await rememberSent(ctx, acct, sent.message_id);
  } catch (error) {
    // Let Meta's retry, or the person's next comment, try again.
    await ctx.store.release(commentKey);
    await ctx.store.release(personKey);
    throw error;
  }
  ctx.log('info', 'sent comment-to-DM', {
    account: account.username,
    keyword: trigger.keywords[0],
    project: trigger.project,
    commentId: comment.id,
  });

  if (trigger.public_replies.length > 0) {
    const reply = trigger.public_replies[Math.floor(ctx.random() * trigger.public_replies.length)]!;
    try {
      await ctx.graph.replyToComment(account.accessToken, comment.id, reply);
    } catch (error) {
      ctx.log('warn', 'public comment reply failed', { commentId: comment.id, error: String(error) });
    }
  }
}

export async function handleMessaging(
  ctx: Context,
  account: Account,
  rules: AccountRules | undefined,
  event: MessagingEvent,
): Promise<void> {
  const acct = account.igUserId;

  if (event.message?.is_echo) {
    // An echo we didn't send means someone on the team replied in the Instagram app.
    if (!(await ctx.store.has(`sent:${acct}:${event.message.mid}`))) {
      const key = `human:${acct}:${event.recipient.id}`;
      await ctx.store.release(key);
      await ctx.store.claim(key, ctx.config.humanTakeoverHours * HOUR);
      ctx.log('info', 'team replied by hand, pausing automation for this conversation', { user: event.recipient.id });
    }
    return;
  }

  const user = event.sender.id;
  if (user === acct || !rules) return;

  const eventId = event.message?.mid ?? event.postback?.mid ?? `referral:${user}:${event.timestamp}`;
  if (!(await ctx.store.claim(`event:${acct}:${eventId}`, 2 * DAY))) return;

  if (await ctx.store.has(`human:${acct}:${user}`)) {
    ctx.log('info', 'conversation is with the team, not replying', { user });
    return;
  }

  const reply = await chooseReply(ctx, acct, rules, user, event);
  if (!reply) return;
  const sent = await ctx.graph.sendMessage(account.accessToken, acct, { id: user }, { text: reply.text });
  await rememberSent(ctx, acct, sent.message_id);
  ctx.log('info', 'sent DM reply', { account: account.username, kind: reply.kind });
}

async function chooseReply(
  ctx: Context,
  acct: string,
  rules: AccountRules,
  user: string,
  event: MessagingEvent,
): Promise<{ kind: string; text: string } | undefined> {
  const firstContact = await ctx.store.claim(`welcomed:${acct}:${user}`, 365 * DAY);

  if (event.postback) {
    const index = rules.ice_breakers.findIndex((_, i) => iceBreakerPayload(i) === event.postback!.payload);
    return index === -1 ? undefined : { kind: 'ice_breaker', text: rules.ice_breakers[index]!.reply };
  }

  if (event.referral && !event.message) {
    const referral = rules.referrals.find((r) => r.ref === event.referral!.ref);
    if (referral) return { kind: 'referral', text: referral.reply };
    return firstContact && rules.welcome ? { kind: 'welcome', text: rules.welcome } : undefined;
  }

  const text = event.message?.text ?? '';
  // Someone who DMs the keyword instead of commenting it still gets the link.
  const trigger = rules.comment_triggers.find((t) => matchesKeyword(text, t.keywords));
  if (trigger) return { kind: 'keyword', text: renderDm(trigger) };
  const dmReply = rules.dm_replies.find((r) => matchesKeyword(text, r.keywords));
  if (dmReply) return { kind: 'dm_reply', text: dmReply.reply };

  if (firstContact && rules.welcome) return { kind: 'welcome', text: rules.welcome };
  // The fallback goes out at most once per half day, so a back-and-forth isn't answered by a bot every time.
  if (rules.fallback && (await ctx.store.claim(`fallback:${acct}:${user}`, 12 * HOUR))) {
    return { kind: 'fallback', text: rules.fallback };
  }
  return undefined;
}

async function rememberSent(ctx: Context, acct: string, messageId: string | undefined): Promise<void> {
  if (messageId) await ctx.store.claim(`sent:${acct}:${messageId}`, 2 * DAY);
}

/** Pushes an account's ice breakers to Instagram (or clears them when there are none). */
export async function syncIceBreakers(ctx: Context, account: Account, rules: AccountRules | undefined): Promise<void> {
  const questions = (rules?.ice_breakers ?? []).map((item, i) => ({ question: item.question, payload: iceBreakerPayload(i) }));
  if (questions.length === 0) return;
  await ctx.graph.setIceBreakers(account.accessToken, questions);
}

/** Refreshes long-lived tokens that expire within 15 days. Run daily. */
export async function refreshExpiringTokens(ctx: Context): Promise<{ refreshed: string[]; failed: string[] }> {
  const refreshed: string[] = [];
  const failed: string[] = [];
  for (const account of await ctx.store.listAccounts()) {
    if (account.expiresAt - ctx.now() > 15 * DAY) continue;
    try {
      const token = await ctx.oauth.refresh(account.accessToken, ctx.now());
      await ctx.store.saveAccount({ ...account, accessToken: token.accessToken, expiresAt: token.expiresAt });
      refreshed.push(account.username);
    } catch (error) {
      failed.push(account.username);
      ctx.log('error', 'token refresh failed; the client needs to reconnect', { account: account.username, error: String(error) });
    }
  }
  return { refreshed, failed };
}
