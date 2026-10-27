// Validates every brands/<client>/dm-automations.yaml. Run before committing a rules change.
import path from 'node:path';
import { loadRules } from './rules.ts';

const dir = process.argv[2] ? path.resolve(process.argv[2]) : path.resolve(import.meta.dirname, '../../../brands');
try {
  const rules = loadRules(dir);
  if (rules.size === 0) console.log(`No dm-automations.yaml files under ${dir}`);
  for (const r of rules.values()) {
    const keywords = r.comment_triggers.flatMap((t) => t.keywords).join(', ') || 'none';
    console.log(`@${r.account}: ${r.comment_triggers.length} comment triggers (${keywords}), ${r.dm_replies.length} DM replies, ${r.ice_breakers.length} ice breakers`);
  }
} catch (error) {
  console.error(String(error instanceof Error ? error.message : error));
  process.exit(1);
}
