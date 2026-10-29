#!/usr/bin/env bash
# Prod Guard: runs when a Claude Code session starts.
# What it prints goes into Claude's context.
dir="${CLAUDE_PROJECT_DIR:-.}"
[ -f "$dir/.claude/prod-guard.env" ] && . "$dir/.claude/prod-guard.env"
backups="${BACKUP_DIR:-/var/backups/postgres}"
max="${MAX_AGE_HOURS:-26}"

if [ -n "$(find "$backups" -type f -mmin "-$((max * 60))" 2>/dev/null | head -n 1)" ]; then
  echo "Prod Guard: backups OK (one newer than ${max}h in $backups)."
else
  echo "Prod Guard WARNING: no backup newer than ${max}h in $backups."
  echo "Treat production as having NO backup. Tell the user before anything else."
fi
exit 0
