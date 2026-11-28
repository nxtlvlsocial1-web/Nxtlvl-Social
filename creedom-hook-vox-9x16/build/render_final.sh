#!/usr/bin/env bash
# Final: HyperFrames delivery render (silent) -> mux the SFX mix -> encode under 100 MB.
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
rm -f renders/master.mp4
npx --yes hyperframes@0.8.203 render --quality delivery --fps 42 -w 3 -o renders/master.mp4 > renders/final.log 2>&1 || { echo "RENDER FAILED" >> renders/final.log; exit 1; }
ffmpeg -y -v error -i renders/master.mp4 -i assets/audio/mix.m4a -map 0:v -map 1:a -c:v libx264 -preset slow -crf 19 -maxrate 15M -bufsize 30M \
  -profile:v high -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart renders/creedom_first-3-seconds_reels_9x16_vox_42fps.mp4
echo "DONE $?" >> renders/final.log
ls -la renders/
