"""The BACKUP lead magnet: "The setup that saved him", a Prod Guard kit for Claude Code, as a branded PDF.

python3 horror-db-9x16/lead-magnet/build_pdf.py      (needs node + the preinstalled Playwright)

Every script in the PDF is read from kit/ (the files that were tested against a real PostgreSQL 16), so the PDF and
the kit can't drift apart. Brand: brands/ai-nxtlvl (the nxtlvl wordmark with its violet star, night + violet glows,
Montserrat / Instrument Serif / JetBrains Mono). Writes prod-guard.html and nxtlvl_prod-guard_setup.pdf next to this file.
"""
import base64
import html
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
KIT = os.path.join(HERE, "kit")
WORDMARK = "data:image/png;base64," + base64.b64encode(
    open(os.path.join(ROOT, "brands", "ai-nxtlvl", "logo-wordmark.png"), "rb").read()).decode()
LOGO = f'<img class="wm" src="{WORDMARK}" alt="nxtlvl">'
# The wordmark's four-point star on its own, for the big cover art and the outro.
STAR = ('<svg viewBox="0 0 100 100"><defs><radialGradient id="sg" cx="50%" cy="50%" r="50%">'
        '<stop offset="0" stop-color="#c9a8ff"/><stop offset=".45" stop-color="#7a2ffb"/><stop offset="1" stop-color="#5a12e0"/>'
        '</radialGradient></defs><path fill="url(#sg)" d="M50 2 C53 36 62 46 98 50 C62 54 53 64 50 98 '
        'C47 64 38 54 2 50 C38 46 47 36 50 2Z"/></svg>')
TOTAL = 6


def kit(path):
    return open(os.path.join(KIT, path)).read().rstrip("\n")


def code(text, label=None, lang="sh"):
    """A code block; comment lines dimmed."""
    out = []
    for ln in text.split("\n"):
        e = html.escape(ln)
        s = ln.lstrip()
        if (lang in ("sh", "env") and s.startswith("#") and not s.startswith("#!")) or (lang == "sql" and s.startswith("--")):
            e = f'<span class="cm">{e}</span>'
        out.append(e)
    tab = f'<div class="tab">{html.escape(label)}</div>' if label else ""
    return f'<div class="code">{tab}<pre>{chr(10).join(out)}</pre></div>'


def page(n, body, cls=""):
    head = "" if n == 1 else (f'<div class="head"><div class="brand">{LOGO}<span>AI.NXTLVL</span></div>'
                              f'<div class="pg">PROD GUARD · {n:02d} / {TOTAL:02d}</div></div>')
    return f'<section class="page {cls}">{head}{body}</section>'


def step(n, title, accent, sub):
    return (f'<div class="step"><div class="num">{n:02d}</div><div><h2>{title} <em>{accent}</em></h2>'
            f'<p class="lede">{sub}</p></div></div>')


COVER = f"""
<div class="cover-brand">{LOGO}</div>
<div class="cover-body">
  <div class="kicker">FROM THE 03:07 AM REEL</div>
  <h1>The setup that<br><em>saved him.</em></h1>
  <p class="cover-sub">Prod Guard for Claude Code. Claude snapshots your database before every destructive command,
  and refuses to touch production at all.</p>
  <div class="chips"><span>5-minute install</span><span>Tested on PostgreSQL 16</span><span>Free to use</span></div>
</div>
<div class="cover-mark">{STAR}</div>
<div class="cover-foot"><span>A DROP DATABASE at 3 AM should cost you a minute, not your company.</span></div>
"""

LOCKS = [("Snapshot hook", "Destructive SQL anywhere? Claude takes a snapshot first, then asks you to confirm."),
         ("Production refusal", "Destructive SQL aimed at production is refused outright. A human runs it, or nobody does."),
         ("House rules", "CLAUDE.md tells Claude to name the database it is on and never touch production."),
         ("Backup alarm", "Every session starts by checking your last backup is fresh. No more \"stopped in March\"."),
         ("Production lock", "A read-only role for everyday access, and a red PRODUCTION prompt in psql.")]

P2 = f"""
<div class="intro">
  <div class="kicker">WHAT HAPPENED AT 03:07</div>
  <p class="story">He thought he was wiping the test database. He was connected to production. 1.2 million rows,
  gone, and the nightly backup had quietly died in March. The only copy was a snapshot his AI agent took first.</p>
  <p class="story strong">This kit makes that snapshot automatic. Five locks, all plain files in your repo:</p>
</div>
<div class="locks">{"".join(f'<div class="lock"><div class="ln">{i + 1}</div><div><h3>{t}</h3><p>{d}</p></div></div>' for i, (t, d) in enumerate(LOCKS))}</div>
<div class="two">
  <div>
    <div class="kicker">YOU NEED</div>
    <ul class="req"><li>Claude Code</li><li>bash and <b>jq</b></li><li>PostgreSQL client tools (<b>pg_dump</b>, <b>psql</b>)</li></ul>
    {code('# macOS' + chr(10) + 'brew install jq libpq && brew link --force libpq' + chr(10) + '# Ubuntu / Debian' + chr(10) + 'sudo apt install jq postgresql-client', 'install')}
  </div>
  <div>
    <div class="kicker">WHERE EVERYTHING GOES</div>
    {code('''your-project/
├── CLAUDE.md          rules (3)
├── .gitignore         (2)
└── .claude/
    ├── settings.json  hooks (2)
    ├── prod-guard.env URLs (2)
    └── hooks/
        ├── prod-guard.sh    (1)
        └── check-backups.sh (4)''', 'project layout', lang="tree")}
  </div>
</div>
"""

P3 = f"""
{step(1, "The snapshot", "hook", "A PreToolUse hook: Claude Code runs it before every Bash command Claude wants to run. Normal commands pass straight through. Destructive SQL on production is denied. Anywhere else, the database is dumped to <code>.snapshots/</code> first, and you're asked to confirm. If the snapshot fails, the command doesn't run.")}
{code(kit(".claude/hooks/prod-guard.sh"), ".claude/hooks/prod-guard.sh")}
{code("mkdir -p .claude/hooks" + chr(10) + "# save the script above as .claude/hooks/prod-guard.sh, then:" + chr(10) + "chmod +x .claude/hooks/prod-guard.sh", "terminal")}
"""

P4 = f"""
{step(2, "Wire it", "in", "Register the hooks and add two permission guard rails. Deny always wins in Claude Code: <code>dropdb</code> is blocked for good, and every <code>psql</code> call asks you first.")}
{code(kit(".claude/settings.json"), ".claude/settings.json", lang="json")}
<div class="two">
  <div>{code(kit(".claude/prod-guard.env"), ".claude/prod-guard.env", lang="env")}</div>
  <div>{code('echo ".claude/prod-guard.env" >> .gitignore' + chr(10) + 'echo ".snapshots/" >> .gitignore', "terminal")}
  <p class="note">Point <code>SNAPSHOT_DB_URL</code> at the database Claude works on. If it ever contains "prod", the hook refuses every destructive command, which is what you want.</p></div>
</div>
{step(3, "The house", "rules", "Hooks are the hard stop. These lines in CLAUDE.md make Claude careful before it ever gets there.")}
{code(kit("CLAUDE.md"), "CLAUDE.md (add to yours)", lang="md")}
"""

P5 = f"""
{step(4, "The backup", "alarm", "His backup job died in March and nobody looked. This runs at the start of every Claude Code session (the SessionStart hook from step 2), and what it prints goes straight into Claude's context: a stale backup is the first thing you hear about.")}
{code(kit(".claude/hooks/check-backups.sh"), ".claude/hooks/check-backups.sh")}
{code("chmod +x .claude/hooks/check-backups.sh", "terminal")}
{step(5, "Lock", "production", "The last line of defence is the database itself. Everyday production access goes through a read-only role: it can read everything and delete nothing. We tested it: DELETE, TRUNCATE, DROP TABLE and DROP DATABASE are all refused.")}
{code(kit("readonly-role.sql"), "readonly-role.sql (run once, as owner)", lang="sql")}
{code(kit("psqlrc-prod"), "~/.psqlrc-prod", lang="sql")}
{code("alias psql-prod='PSQLRC=~/.psqlrc-prod psql \"$PROD_DATABASE_URL\"'", "~/.zshrc or ~/.bashrc")}
<p class="note">Use the dev_readonly login in <code>PROD_DATABASE_URL</code>. The red prompt plus <code>AUTOCOMMIT off</code> means a stray DELETE or DROP TABLE is rolled back unless you type COMMIT. It can't stop DROP DATABASE (psql runs that outside a transaction), which is why the read-only role comes first.</p>
"""

CHECK = ["Hook scripts saved in .claude/hooks/ and executable", "settings.json in place",
         "prod-guard.env filled in, and in .gitignore with .snapshots/", "Rules added to CLAUDE.md",
         "The test above says \"ask\" (with a snapshot) and \"deny\" on prod", "Nightly backups land in BACKUP_DIR",
         "Everyday production access uses dev_readonly"]

P6 = f"""
{step(6, "Test it in", "60 seconds", "Feed the hook exactly what Claude Code sends it. You should get <b>ask</b> plus a new file in <code>.snapshots/</code> for the first, and <b>deny</b> for the second.")}
{code('''echo '{"tool_input":{"command":"psql -c \\"DROP TABLE users\\""}}' \\
  | CLAUDE_PROJECT_DIR=$PWD .claude/hooks/prod-guard.sh

echo '{"tool_input":{"command":"psql -h prod-db -c \\"DROP TABLE users\\""}}' \\
  | CLAUDE_PROJECT_DIR=$PWD .claude/hooks/prod-guard.sh''', "terminal")}
<div class="two">
  <div>
    <div class="kicker">IF IT HAPPENS ANYWAY</div>
    {code('''# rows or a table gone
pg_restore --clean --if-exists \\
  -d "$SNAPSHOT_DB_URL" .snapshots/<file>.dump

# the whole database gone
createdb app_dev
pg_restore \\
  -d "$SNAPSHOT_DB_URL" .snapshots/<file>.dump''', "restore")}
    <p class="note">Both tested: 1,000 rows deleted, then a dropped database, restored to 1,000 rows each time.</p>
  </div>
  <div>
    <div class="kicker">CHECKLIST</div>
    <ul class="check">{"".join(f"<li>{html.escape(c)}</li>" for c in CHECK)}</ul>
  </div>
</div>
<div class="outro">
  <div class="outro-mark">{LOGO}</div>
  <div><h3>A seatbelt, not a backup plan.</h3>
  <p>Snapshots protect the database Claude works on. Production still needs real, monitored backups, and now you'll
  know the day they stop. Follow <b>AI.NXTLVL</b> for more Claude setups like this one.</p></div>
</div>
"""

CSS = f"""
@font-face {{ font-family: "Montserrat"; font-weight: 100 900; src: url("fonts/montserrat.ttf"); }}
@font-face {{ font-family: "JBMono"; font-weight: 400; src: url("fonts/JetBrainsMono-Regular.ttf"); }}
@font-face {{ font-family: "JBMono"; font-weight: 700; src: url("fonts/JetBrainsMono-Bold.ttf"); }}
@font-face {{ font-family: "ISerif"; font-style: italic; src: url("fonts/InstrumentSerif-Italic.ttf"); }}
@page {{ size: A4; margin: 0; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ background: #07050f; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ font-family: "Montserrat", sans-serif; color: #cfc8dd; }}
.page {{ position: relative; width: 210mm; height: 297mm; overflow: hidden; padding: 44px 52px 40px; page-break-after: always;
  background: radial-gradient(ellipse 60% 45% at 0% 0%, rgba(127,27,248,.5), transparent 70%),
              radial-gradient(ellipse 55% 40% at 100% 100%, rgba(96,8,242,.45), transparent 70%), #07050f; }}
.page:last-child {{ page-break-after: auto; }}
svg {{ display: block; }}
.head {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 26px; }}
.brand {{ display: flex; align-items: center; gap: 10px; }}
.brand .wm {{ height: 22px; width: auto; display: block; }}
.brand span, .pg, .kicker, .tab {{ font: 700 10px "JBMono"; letter-spacing: 3px; color: #b687f9; }}
.pg {{ color: rgba(207,200,221,.55); }}
code {{ font-variant-ligatures: none; font: 400 .92em "JBMono"; color: #e3d2ff; background: rgba(167,91,252,.14); padding: 1px 5px; border-radius: 4px; }}
b {{ color: #fff; font-weight: 700; }}
.kicker {{ margin-bottom: 10px; }}
h1 {{ font: 800 64px/1.02 "Montserrat"; letter-spacing: -2.5px; color: #fff; }}
h1 em, h2 em {{ font-family: "ISerif"; font-style: italic; font-weight: 400; color: #b687f9; letter-spacing: 0; }}
h1 em {{ font-size: 76px; }}
h2 {{ font: 800 28px/1.1 "Montserrat"; letter-spacing: -.8px; color: #fff; }}
h2 em {{ font-size: 33px; }}
h3 {{ font: 700 14px/1.3 "Montserrat"; color: #fff; }}
p {{ font-size: 12px; line-height: 1.6; }}
/* cover */
.cover-brand {{ display: flex; align-items: center; gap: 12px; }}
.cover-brand .wm {{ height: 46px; width: auto; display: block; }}
.cover-body {{ position: absolute; left: 52px; right: 52px; top: 250px; z-index: 2; }}
.cover-sub {{ margin-top: 26px; max-width: 470px; font-size: 16px; line-height: 1.55; color: #ddd5ea; }}
.chips {{ margin-top: 30px; display: flex; gap: 10px; flex-wrap: wrap; }}
.chips span {{ font: 700 10.5px "JBMono"; letter-spacing: 1.5px; color: #fff; padding: 8px 14px; border-radius: 30px;
  border: 1px solid rgba(182,135,249,.5); background: rgba(101,22,199,.25); }}
.cover-mark {{ position: absolute; right: 36px; bottom: 130px; width: 340px; height: 340px; opacity: .95; z-index: 1;
  filter: drop-shadow(0 0 40px rgba(122,47,251,.75)) drop-shadow(0 0 90px rgba(122,47,251,.45)); }}
.cover-mark svg {{ width: 100%; height: 100%; }}
.cover-foot {{ position: absolute; left: 52px; right: 52px; bottom: 44px; z-index: 2; padding-top: 16px; border-top: 1px solid rgba(182,135,249,.25); }}
.cover-foot span {{ font: 400 italic 20px "ISerif"; color: #cfc8dd; }}
/* page 2 */
.story {{ font-size: 14px; line-height: 1.6; color: #ddd5ea; }}
.story.strong {{ margin-top: 10px; color: #fff; font-weight: 600; }}
.locks {{ margin: 20px 0 22px; display: grid; gap: 10px; }}
.lock {{ display: flex; gap: 16px; align-items: center; padding: 13px 18px; border-radius: 14px; background: rgba(20,10,46,.75);
  border: 1px solid rgba(167,91,252,.22); }}
.lock .ln {{ flex: none; width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
  font: 400 italic 22px "ISerif"; color: #fff; background: linear-gradient(135deg, #a75bfc, #4b06c1); }}
.lock p {{ margin-top: 2px; font-size: 11.5px; }}
.two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; align-items: start; }}
.req {{ list-style: none; margin-bottom: 10px; }}
.req li {{ font-size: 12px; line-height: 1.8; padding-left: 16px; position: relative; }}
.req li::before {{ content: ""; position: absolute; left: 0; top: 8px; width: 6px; height: 6px; border-radius: 50%; background: #a75bfc; }}
/* steps + code */
.step {{ display: flex; gap: 18px; align-items: flex-start; margin: 4px 0 14px; }}
.num {{ flex: none; font: 400 italic 54px/0.9 "ISerif"; color: #a75bfc; }}
.lede {{ margin-top: 6px; font-size: 12px; }}
.code {{ margin-bottom: 12px; border-radius: 12px; overflow: hidden; background: #110824; border: 1px solid rgba(167,91,252,.28); }}
.tab {{ padding: 7px 14px; font-size: 9px; letter-spacing: 1.5px; background: rgba(101,22,199,.3); border-bottom: 1px solid rgba(167,91,252,.22); }}
pre {{ font-variant-ligatures: none; padding: 12px 14px; font: 400 9.6px/1.5 "JBMono"; color: #eae4f5; white-space: pre-wrap; word-break: break-word; }}
.cm {{ color: #9a86b8; }}
.note {{ margin: -2px 0 14px; font-size: 10.5px; color: #b9b0c9; }}
/* last page */
.check {{ list-style: none; }}
.check li {{ position: relative; padding: 0 0 9px 26px; font-size: 11.5px; line-height: 1.45; }}
.check li::before {{ content: ""; position: absolute; left: 0; top: 1px; width: 14px; height: 14px; border-radius: 4px; border: 1.5px solid #a75bfc; }}
.outro {{ position: absolute; left: 52px; right: 52px; bottom: 40px; display: flex; gap: 18px; align-items: center; padding: 18px 22px;
  border-radius: 16px; background: linear-gradient(120deg, rgba(101,22,199,.45), rgba(20,10,46,.85)); border: 1px solid rgba(182,135,249,.35); }}
.outro-mark .wm {{ width: 118px; height: auto; display: block; }}
.outro h3 {{ font-size: 17px; margin-bottom: 4px; }}
.outro p {{ font-size: 11.5px; color: #e2daf0; }}
"""

SHOT = """
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + process.argv[1], { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: process.argv[2], preferCSSPageSize: true, printBackground: true });
  await p.setViewportSize({ width: 794, height: 1123 });
  const pages = await p.$$('.page');
  for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: process.argv[3] + '/page-' + (i + 1) + '.png' });
  await b.close();
})().catch((e) => { console.error(e); process.exit(1); });
"""


def main():
    body = "".join([page(1, COVER, "cover"), page(2, P2), page(3, P3), page(4, P4), page(5, P5), page(6, P6)])
    doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>The setup that saved him · Prod Guard</title>'
           f'<style>{CSS}</style></head><body>{body}</body></html>')
    src = os.path.join(HERE, "prod-guard.html")
    open(src, "w", encoding="utf-8").write(doc)
    out = os.path.join(HERE, "nxtlvl_prod-guard_setup.pdf")
    prev = os.environ.get("PREVIEW_DIR", os.path.join(HERE, "preview"))
    os.makedirs(prev, exist_ok=True)
    subprocess.run(["node", "-e", SHOT, src, out, prev], check=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
