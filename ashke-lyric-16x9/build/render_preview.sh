#!/usr/bin/env bash
# Draft preview for approval. Run detached: setsid nohup bash build/render_preview.sh > /dev/null 2>&1 < /dev/null &
# The renderer lowers the audio, so the mastered section is muxed back in afterwards.
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
npx --yes hyperframes@0.8.203 render --quality draft -w 3 -o renders/raw_preview.mp4 > renders/preview.log 2>&1
ffmpeg -v error -y -i renders/raw_preview.mp4 -i assets/audio/section.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart \
  renders/nxtlvl_ashke-lyric_youtube_16x9_preview.mp4 >> renders/preview.log 2>&1
echo "EXIT $?" >> renders/preview.log
