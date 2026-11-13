#!/usr/bin/env bash
# v3 (client: reference footage full screen more, no second ₹85,000): same two cuts
# v2 finals (client voice note): two cuts for trial reels, each in delivery quality (11 Mb/s, under the 100 MB cap):
#   A  opens on Deepinder Goyal's own line, then the split screen  -> nxtlvl_kokila-peace_reels_9x16_v3_deepinder-open.mp4
#   B  opens straight on Dr Kokila                                  -> nxtlvl_kokila-peace_reels_9x16_v3_direct-open.mp4
# Each: generate (VARIANT), music, picture, sound, verify. Run detached:
#   setsid nohup bash build/render_v2.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
LOG=renders/v3.log
: > $LOG
for V in A B; do
  if [ $V = A ]; then OUT=renders/nxtlvl_kokila-peace_reels_9x16_v3_deepinder-open.mp4; else OUT=renders/nxtlvl_kokila-peace_reels_9x16_v3_direct-open.mp4; fi
  VARIANT=$V python3 build/generate.py >> $LOG 2>&1 && python3 build/music.py >> $LOG 2>&1 || { echo "GEN $V FAILED" >> $LOG; exit 1; }
  rm -f renders/master_$V.mp4
  npx --yes hyperframes@0.8.203 render --quality high --video-bitrate 11M --sdr -w 3 -o renders/master_$V.mp4 >> $LOG 2>&1
  RC=$?
  echo "RENDER $V EXIT $RC" >> $LOG
  if [ $RC -ne 0 ] || [ ! -s renders/master_$V.mp4 ]; then echo "MIX $V skipped (render failed)" >> $LOG; exit 1; fi
  python3 build/sfx_mix.py renders/master_$V.mp4 "$OUT" >> $LOG 2>&1
  echo "MIX $V EXIT $?" >> $LOG
  cp plan/sfx_cues_final.json plan/sfx_cues_final_$V.json
  python3 ~/.claude/skills/openverse-sfx/scripts/verify_mix.py "$OUT" --target -14 --outdir renders/verify_v3_$V >> $LOG 2>&1
done
echo "ALL DONE" >> $LOG
