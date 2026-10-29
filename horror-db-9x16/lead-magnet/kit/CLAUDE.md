## Database safety (Prod Guard)

- Before any destructive database change (DROP, TRUNCATE, DELETE without
  WHERE, migrate reset) a snapshot is taken first. The prod-guard hook does
  this. Never try to get around it.
- Say which database you are connected to before you run any SQL.
- Never run commands against production. If a task needs production, stop
  and give the exact command to the human.
- If the session-start message says backups are stale, say so first.
