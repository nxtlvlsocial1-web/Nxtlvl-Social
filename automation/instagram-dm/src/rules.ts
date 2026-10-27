import { existsSync, readdirSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { parse } from 'yaml';

export const RULES_FILE = 'dm-automations.yaml';

export interface CommentTrigger {
  keywords: string[];
  /** Only these posts or reels. Empty means every post. */
  media_ids: string[];
  /** The video project this CTA belongs to, e.g. fight-night-9x16. For our records only. */
  project?: string;
  dm: string;
  link?: string;
  public_replies: string[];
}

export interface DmReply {
  keywords: string[];
  reply: string;
}

export interface IceBreaker {
  question: string;
  reply: string;
}

export interface Referral {
  ref: string;
  reply: string;
}

export interface AccountRules {
  /** Instagram username, lowercased, without the @. */
  account: string;
  file: string;
  comment_triggers: CommentTrigger[];
  dm_replies: DmReply[];
  welcome?: string;
  fallback?: string;
  ice_breakers: IceBreaker[];
  referrals: Referral[];
}

export type RulesByAccount = Map<string, AccountRules>;

/** Reads brands/<client>/dm-automations.yaml for every client that has one. */
export function loadRules(dir: string): RulesByAccount {
  const rules: RulesByAccount = new Map();
  if (!existsSync(dir)) return rules;
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const file = path.join(dir, entry.name, RULES_FILE);
    if (!existsSync(file)) continue;
    const parsed = parseRules(readFileSync(file, 'utf8'), file);
    if (rules.has(parsed.account)) {
      throw new Error(`${file}: account @${parsed.account} is already set up in ${rules.get(parsed.account)!.file}`);
    }
    rules.set(parsed.account, parsed);
  }
  return rules;
}

export function parseRules(source: string, file: string): AccountRules {
  const fail = (message: string): never => {
    throw new Error(`${file}: ${message}`);
  };
  const doc = parse(source) ?? {};
  if (typeof doc !== 'object' || Array.isArray(doc)) fail('expected a mapping at the top level');

  const text = (value: unknown, where: string): string => {
    if (typeof value !== 'string' || !value.trim()) fail(`${where} must be non-empty text`);
    return (value as string).trim();
  };
  const optionalText = (value: unknown, where: string): string | undefined =>
    value === undefined || value === null ? undefined : text(value, where);
  const list = (value: unknown, where: string): unknown[] => {
    if (value === undefined || value === null) return [];
    if (!Array.isArray(value)) fail(`${where} must be a list`);
    return value as unknown[];
  };
  const keywords = (value: unknown, where: string): string[] => {
    const items = typeof value === 'string' ? [value] : list(value, where);
    if (items.length === 0) fail(`${where} needs at least one keyword`);
    return items.map((item, i) => {
      const keyword = text(String(item ?? ''), `${where}[${i}]`);
      if (!normalize(keyword)) fail(`${where}[${i}] has no letters or digits`);
      return keyword;
    });
  };

  const account = text(doc.account, 'account').replace(/^@/, '').toLowerCase();

  const ice_breakers = list(doc.ice_breakers, 'ice_breakers').map((item: any, i) => ({
    question: text(item?.question, `ice_breakers[${i}].question`),
    reply: text(item?.reply, `ice_breakers[${i}].reply`),
  }));
  if (ice_breakers.length > 4) fail('Instagram allows at most 4 ice_breakers');

  return {
    account,
    file,
    comment_triggers: list(doc.comment_triggers, 'comment_triggers').map((item: any, i) => {
      const where = `comment_triggers[${i}]`;
      const link = optionalText(item?.link, `${where}.link`);
      if (link && !/^https:\/\//.test(link)) fail(`${where}.link must start with https://`);
      return {
        keywords: keywords(item?.keywords ?? item?.keyword, `${where}.keywords`),
        media_ids: list(item?.media_ids, `${where}.media_ids`).map(String),
        project: optionalText(item?.project, `${where}.project`),
        dm: text(item?.dm, `${where}.dm`),
        link,
        public_replies: list(item?.public_replies, `${where}.public_replies`).map((reply, j) =>
          text(reply, `${where}.public_replies[${j}]`),
        ),
      };
    }),
    dm_replies: list(doc.dm_replies, 'dm_replies').map((item: any, i) => ({
      keywords: keywords(item?.keywords ?? item?.keyword, `dm_replies[${i}].keywords`),
      reply: text(item?.reply, `dm_replies[${i}].reply`),
    })),
    welcome: optionalText(doc.welcome, 'welcome'),
    fallback: optionalText(doc.fallback, 'fallback'),
    ice_breakers,
    referrals: list(doc.referrals, 'referrals').map((item: any, i) => ({
      ref: text(item?.ref, `referrals[${i}].ref`),
      reply: text(item?.reply, `referrals[${i}].reply`),
    })),
  };
}

/** Lowercase letters and digits only, words separated by single spaces. */
export function normalize(value: string): string {
  return value
    .normalize('NFKC')
    .toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, ' ')
    .trim();
}

/** True when any keyword appears in the text as a whole word (or phrase). */
export function matchesKeyword(text: string, keywords: string[]): boolean {
  const haystack = ` ${normalize(text)} `;
  return keywords.some((keyword) => haystack.includes(` ${normalize(keyword)} `));
}

/** The DM text for a comment trigger, with {link} filled in (or the link added at the end). */
export function renderDm(trigger: CommentTrigger): string {
  if (!trigger.link) return trigger.dm;
  return trigger.dm.includes('{link}') ? trigger.dm.replaceAll('{link}', trigger.link) : `${trigger.dm}\n${trigger.link}`;
}

export function iceBreakerPayload(index: number): string {
  return `ICE_BREAKER_${index}`;
}
