#!/usr/bin/env bash
# after build/vo_run.sh: re-take g1 (the capitalised PAID came out as "PAAI"; the script now says "paid") for both
# references, then pick both again. Detached: setsid nohup bash build/vo_fix.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HF_HOME=/root/tts/hf
P=/root/tts/.venv/bin/python
until grep -q "ALL DONE" cache/vo.log; do sleep 10; done
for r in am_michael am_fenrir; do
  $P build/vo_cb.py $r >> cache/vo.log 2>&1
  VO_TAKES=assets/audio/vo_takes/$r VO_TAG=$r $P build/vo_pick.py >> cache/vo.log 2>&1
  echo "REPICK EXIT $r $?" >> cache/vo.log
done
echo "FIX DONE" >> cache/vo.log
