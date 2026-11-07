#!/bin/bash
# build/eltake.sh <take> <generation_id> <session_id> <duration> <url>  (run from ai-posts-9x16): downloads an ElevenLabs take, records it in voice/el/done.json, commits and pushes
set -e
curl -sS -o voice/el/mp3/$1.mp3 "$5"
python3 -c "
import json;p='voice/el/done.json';d=json.load(open(p))
d['done']['$1']={'generation_id':'$2','session_id':'$3','duration':$4}
json.dump(d,open(p,'w'),indent=1)"
cd .. && git add ai-posts-9x16/voice/el && git commit -q -m "AI Posts: ElevenLabs take for line ${1%%_*}

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Q5ejV8r9QJ9PpM8e2qZhBr" && git push -q -u origin claude/hyperframes-cli-install-w6ziy7 && git log --oneline -1
