#!/usr/bin/env bash
# v2 voice: Kokoro references, Chatterbox takes per reference, one pick per reference. Detached:
#   setsid nohup bash build/vo_run.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HF_HOME=/root/tts/hf
P=/root/tts/.venv/bin/python
: > cache/vo.log
HF_HUB_OFFLINE=1 $P build/ref_kok.py >> cache/vo.log 2>&1
echo "REF EXIT $?" >> cache/vo.log
for r in am_michael am_fenrir; do
  $P build/vo_cb.py $r >> cache/vo.log 2>&1
  echo "CB EXIT $r $?" >> cache/vo.log
  VO_TAKES=assets/audio/vo_takes/$r VO_TAG=$r $P build/vo_pick.py >> cache/vo.log 2>&1
  echo "PICK EXIT $r $?" >> cache/vo.log
done
echo "ALL DONE" >> cache/vo.log
