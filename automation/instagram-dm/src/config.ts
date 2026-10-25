import path from 'node:path';

export interface Config {
  appId: string;
  appSecret: string;
  verifyToken: string;
  redirectUri: string;
  publicUrl: string;
  adminToken: string;
  graphVersion: string;
  rulesDir: string;
  dataFile: string;
  port: number;
  humanTakeoverHours: number;
}

const DEFAULT_RULES_DIR = path.resolve(import.meta.dirname, '../../../brands');

export function loadConfig(env: NodeJS.ProcessEnv = process.env): Config {
  const required = (name: string): string => {
    const value = env[name];
    if (!value) throw new Error(`Missing environment variable ${name} (see .env.example)`);
    return value;
  };
  const redirectUri = required('IG_REDIRECT_URI');
  return {
    appId: required('IG_APP_ID'),
    appSecret: required('IG_APP_SECRET'),
    verifyToken: required('WEBHOOK_VERIFY_TOKEN'),
    redirectUri,
    publicUrl: env.PUBLIC_URL ?? new URL(redirectUri).origin,
    adminToken: required('ADMIN_TOKEN'),
    graphVersion: env.GRAPH_API_VERSION ?? 'v23.0',
    rulesDir: env.RULES_DIR ? path.resolve(env.RULES_DIR) : DEFAULT_RULES_DIR,
    dataFile: path.resolve(env.DATA_FILE ?? 'data/store.json'),
    port: Number(env.PORT ?? 3000),
    humanTakeoverHours: Number(env.HUMAN_TAKEOVER_HOURS ?? 12),
  };
}
