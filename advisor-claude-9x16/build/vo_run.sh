#!/usr/bin/env bash
# The voice: 4 performed takes per passage, pick the clean livelier one, join, split into sentences. Run detached.
cd "$(dirname "$0")/.." || exit 1
export HF_HOME=/root/tts/hf
/root/tts/.venv/bin/python build/vo_cb.py > cache/vo.log 2>&1; echo "VO EXIT $?" >> cache/vo.log
/root/tts/.venv/bin/python build/vo_pick.py >> cache/vo.log 2>&1; echo "PICK EXIT $?" >> cache/vo.log
python3 build/relabel.py >> cache/vo.log 2>&1; echo "RELABEL EXIT $?" >> cache/vo.log
