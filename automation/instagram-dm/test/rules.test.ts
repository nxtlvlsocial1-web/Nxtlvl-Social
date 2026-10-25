import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { loadRules, matchesKeyword, parseRules, renderDm } from '../src/rules.ts';

test('keywords match whole words in any case, ignoring punctuation and emoji', () => {
  assert.ok(matchesKeyword('FIGHT', ['fight']));
  assert.ok(matchesKeyword('fight!!! 🥊🥊', ['FIGHT']));
  assert.ok(matchesKeyword('I want the FIGHT skill please', ['fight']));
  assert.ok(matchesKeyword('how much does it cost?', ['how much']));
  assert.ok(!matchesKeyword('fighter', ['fight']));
  assert.ok(!matchesKeyword('', ['fight']));
});

test('renderDm fills {link} or adds the link at the end', () => {
  const base = { keywords: ['x'], media_ids: [], public_replies: [] };
  assert.equal(renderDm({ ...base, dm: 'Here: {link}', link: 'https://a.b' }), 'Here: https://a.b');
  assert.equal(renderDm({ ...base, dm: 'Here you go', link: 'https://a.b' }), 'Here you go\nhttps://a.b');
  assert.equal(renderDm({ ...base, dm: 'No link' }), 'No link');
});

test('parseRules accepts a single keyword string and lowercases the account', () => {
  const rules = parseRules('account: "@Client.Name"\ncomment_triggers:\n  - keyword: TV\n    dm: Guide\n', 'x.yaml');
  assert.equal(rules.account, 'client.name');
  assert.deepEqual(rules.comment_triggers[0]!.keywords, ['TV']);
});

test('parseRules explains what is wrong, with the file name', () => {
  assert.throws(() => parseRules('comment_triggers: []', 'brands/a/dm-automations.yaml'), /brands\/a\/dm-automations\.yaml: account/);
  assert.throws(() => parseRules('account: a\ncomment_triggers:\n  - keywords: [X]\n', 'f'), /comment_triggers\[0\]\.dm/);
  assert.throws(() => parseRules('account: a\ncomment_triggers:\n  - keywords: [X]\n    dm: hi\n    link: http://a\n', 'f'), /https/);
  assert.throws(() => parseRules('account: a\ncomment_triggers:\n  - keywords: ["🥊"]\n    dm: hi\n', 'f'), /no letters or digits/);
  const five = Array.from({ length: 5 }, (_, i) => `  - question: q${i}\n    reply: r`).join('\n');
  assert.throws(() => parseRules(`account: a\nice_breakers:\n${five}\n`, 'f'), /at most 4/);
});

test('loadRules reads brands/<client>/dm-automations.yaml and rejects duplicate accounts', () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'brands-'));
  mkdirSync(path.join(dir, 'one'));
  mkdirSync(path.join(dir, 'two'));
  mkdirSync(path.join(dir, 'no-rules'));
  writeFileSync(path.join(dir, 'one', 'dm-automations.yaml'), 'account: one\n');
  writeFileSync(path.join(dir, 'two', 'dm-automations.yaml'), 'account: two\n');
  assert.deepEqual([...loadRules(dir).keys()].sort(), ['one', 'two']);

  writeFileSync(path.join(dir, 'two', 'dm-automations.yaml'), 'account: ONE\n');
  assert.throws(() => loadRules(dir), /already set up/);
});
