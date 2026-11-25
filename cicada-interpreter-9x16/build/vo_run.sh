#!/usr/bin/env bash
# Voice (Kokoro takes + pick). Run detached: setsid nohup bash build/vo_run.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
HF_HOME=/root/tts/hf HF_HUB_OFFLINE=1 /root/tts/.venv/bin/python build/vo_kok.py > cache/vo.log 2>&1
echo "VO EXIT $?" >> cache/vo.log
