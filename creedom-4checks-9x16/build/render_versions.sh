#!/usr/bin/env bash
# v3 finals: version A (Comment CHECK) and version B (Install Creedom), delivery quality, 42 fps. Run detached.
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
for V in A B; do
  VERSION=$V python3 build/generate.py > renders/final_$V.log 2>&1
  cp assets/audio/vo_$V.wav assets/audio/vo.wav
  rm -f renders/master_$V.mp4
  npx --yes hyperframes@0.8.203 render --quality delivery --fps 42 -w 3 -o renders/master_$V.mp4 >> renders/final_$V.log 2>&1 || { echo "EXIT render failed" >> renders/final_$V.log; continue; }
  python3 build/sfx_mix.py renders/master_$V.mp4 renders/creedom_4-checks_reels_9x16_v3${V}_42fps.mp4 --no-music >> renders/final_$V.log 2>&1
  echo "SFX EXIT $?" >> renders/final_$V.log
done
