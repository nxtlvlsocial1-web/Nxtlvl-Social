#!/usr/bin/env bash
# v5 (client): two full-quality versions with a text hook on the opening screen.
#   HOOK=1  "For Coaches, Consultants, Experts / STOP LEARNING. START EARNING."
#   HOOK=2  "Coaches, Consultants, Experts / GET YOUR NEXT 3 HIGH-PAYING CLIENTS"
# Run detached: setsid nohup bash build/render_hooks.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
LOG=renders/hooks.log
: > $LOG
for h in 1 2; do
  HOOK=$h python3 build/generate.py >> $LOG 2>&1 || { echo "GEN FAILED $h" >> $LOG; exit 1; }
  OUT=renders/nxtlvl_surrender-ad_reels_9x16_v5_hook$h.mp4 bash build/render_final.sh
  tail -3 renders/final.log >> $LOG
  [ -s renders/nxtlvl_surrender-ad_reels_9x16_v5_hook${h}_sfx.mp4 ] && echo "HOOK $h DONE" >> $LOG || echo "HOOK $h FAILED" >> $LOG
  rm -f renders/master.mp4 renders/nxtlvl_surrender-ad_reels_9x16_v5_hook$h.mp4
done
echo "ALL DONE" >> $LOG
