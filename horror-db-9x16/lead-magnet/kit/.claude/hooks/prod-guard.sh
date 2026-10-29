#!/usr/bin/env bash
# Prod Guard: a Claude Code PreToolUse hook for the Bash tool.
#   destructive SQL on production -> refused
#   destructive SQL anywhere else -> snapshot first, then you confirm
set -uo pipefail

cmd=$(jq -r '.tool_input.command // ""')
dir="${CLAUDE_PROJECT_DIR:-.}"
[ -f "$dir/.claude/prod-guard.env" ] && . "$dir/.claude/prod-guard.env"

decide() {  # decide allow|ask|deny "reason"
  jq -n --arg d "$1" --arg r "$2" '{hookSpecificOutput: {hookEventName: "PreToolUse",
    permissionDecision: $d, permissionDecisionReason: $r}}'
  exit 0
}

# 1. Is it destructive? If not, the normal permission flow applies.
shopt -s nocasematch
drop='drop[[:space:]]+(database|schema|table|owned)|truncate[[:space:]]|dropdb[[:space:]]'
reset='migrate[[:space:]]+reset|db:(drop|reset)'
wipe=no
[[ "$cmd" =~ $drop|$reset ]] && wipe=yes
[[ "$cmd" =~ delete[[:space:]]+from && ! "$cmd" =~ where ]] && wipe=yes
[ "$wipe" = no ] && exit 0

# 2. Production? Claude never runs it.
prod="${PROD_PATTERN:-(^|[^a-z])(prod|production)([^a-z]|$)}"
if [[ "$cmd ${SNAPSHOT_DB_URL:-}" =~ $prod ]]; then
  decide deny "Prod Guard: destructive command on production. Hand it to a human."
fi

# 3. Anywhere else: snapshot first, or it doesn't run.
if [ -z "${SNAPSHOT_DB_URL:-}" ]; then
  echo "Prod Guard: no SNAPSHOT_DB_URL in .claude/prod-guard.env. Blocked." >&2
  exit 2
fi
mkdir -p "$dir/.snapshots"
file="$dir/.snapshots/snapshot_$(date +%Y%m%d_%H%M%S)_$$.dump"
if ! pg_dump -Fc -f "$file" "$SNAPSHOT_DB_URL" 2>"$dir/.snapshots/error.log"; then
  echo "Prod Guard: snapshot failed (.snapshots/error.log). Blocked." >&2
  exit 2
fi
decide ask "Prod Guard: snapshot saved to .snapshots/$(basename "$file"). Run it?"
