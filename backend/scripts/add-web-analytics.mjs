// Adds the Cloudflare Web Analytics beacon to every page in ../website before a deploy.
// The token comes from the CF_WEB_ANALYTICS_TOKEN environment variable (a GitHub secret in the deploy workflow).
// Without a token it does nothing, so deploys keep working before analytics is set up.
// Usage: node scripts/add-web-analytics.mjs [websiteDir]
import { readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = process.argv[2] || join(dirname(fileURLToPath(import.meta.url)), '..', '..', 'website');
const token = (process.env.CF_WEB_ANALYTICS_TOKEN || '').trim();

if (!token) {
  console.log('CF_WEB_ANALYTICS_TOKEN not set: skipping Web Analytics.');
  process.exit(0);
}
if (!/^[a-f0-9]{32}$/i.test(token)) {
  // warn and carry on: a mistyped analytics token should never block a site deploy
  console.log('::warning::CF_WEB_ANALYTICS_TOKEN should be the 32-character token from the Web Analytics snippet. Skipping Web Analytics.');
  process.exit(0);
}

const tag = `<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "${token}"}'></script>`;
let added = 0;
for (const file of readdirSync(dir).filter((f) => f.endsWith('.html'))) {
  const path = join(dir, file);
  const html = readFileSync(path, 'utf8');
  if (html.includes('static.cloudflareinsights.com/beacon')) continue;
  if (!html.includes('</body>')) { console.error(`${file}: no </body>, skipped`); continue; }
  writeFileSync(path, html.replace('</body>', `${tag}\n</body>`));
  added++;
}
console.log(`Web Analytics beacon added to ${added} page(s).`);
