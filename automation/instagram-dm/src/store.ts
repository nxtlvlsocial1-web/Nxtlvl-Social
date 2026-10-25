import { existsSync, mkdirSync, readFileSync } from 'node:fs';
import { rename, writeFile } from 'node:fs/promises';
import path from 'node:path';

export interface Account {
  /** Professional account id; webhooks name the account by this in entry.id. */
  igUserId: string;
  /** App-scoped id from the login; Meta's deletion callbacks use this one. */
  appUserId: string;
  username: string;
  accessToken: string;
  expiresAt: number;
}

export interface Store {
  getAccount(igUserId: string): Promise<Account | undefined>;
  listAccounts(): Promise<Account[]>;
  saveAccount(account: Account): Promise<void>;
  /** Removes the account and everything keyed under it. Matches either id. */
  deleteAccount(id: string): Promise<Account | undefined>;
  /** Sets the key and returns true, unless it is already set and unexpired. */
  claim(key: string, ttlMs: number): Promise<boolean>;
  release(key: string): Promise<void>;
  has(key: string): Promise<boolean>;
}

interface Snapshot {
  accounts: Record<string, Account>;
  keys: Record<string, number>;
}

export class MemoryStore implements Store {
  protected data: Snapshot = { accounts: {}, keys: {} };
  protected now: () => number;

  constructor(now: () => number = Date.now) {
    this.now = now;
  }

  async getAccount(igUserId: string) {
    return this.data.accounts[igUserId];
  }

  async listAccounts() {
    return Object.values(this.data.accounts);
  }

  async saveAccount(account: Account) {
    this.data.accounts[account.igUserId] = account;
    await this.changed();
  }

  async deleteAccount(id: string) {
    const account = Object.values(this.data.accounts).find((a) => a.igUserId === id || a.appUserId === id);
    if (!account) return undefined;
    delete this.data.accounts[account.igUserId];
    for (const key of Object.keys(this.data.keys)) {
      if (key.split(':')[1] === account.igUserId) delete this.data.keys[key];
    }
    await this.changed();
    return account;
  }

  async claim(key: string, ttlMs: number) {
    if (await this.has(key)) return false;
    this.data.keys[key] = this.now() + ttlMs;
    await this.changed();
    return true;
  }

  async release(key: string) {
    delete this.data.keys[key];
    await this.changed();
  }

  async has(key: string) {
    const expires = this.data.keys[key];
    return expires !== undefined && expires > this.now();
  }

  protected async changed(): Promise<void> {}
}

/**
 * MemoryStore saved to a JSON file after every change. Fine for one small server;
 * move to Postgres or a KV store before running several instances.
 */
export class FileStore extends MemoryStore {
  #file: string;
  #writing: Promise<void> = Promise.resolve();

  constructor(file: string, now: () => number = Date.now) {
    super(now);
    this.#file = file;
    mkdirSync(path.dirname(file), { recursive: true });
    if (existsSync(file)) this.data = JSON.parse(readFileSync(file, 'utf8'));
  }

  protected override changed(): Promise<void> {
    const now = this.now();
    for (const [key, expires] of Object.entries(this.data.keys)) {
      if (expires <= now) delete this.data.keys[key];
    }
    const json = JSON.stringify(this.data);
    this.#writing = this.#writing.then(async () => {
      const tmp = `${this.#file}.tmp`;
      await writeFile(tmp, json, { mode: 0o600 });
      await rename(tmp, this.#file);
    });
    return this.#writing;
  }
}
