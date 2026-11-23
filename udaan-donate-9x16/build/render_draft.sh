#!/usr/bin/env bash
# UDAAN 9:16 draft render (preview for approval). Audio is assets/audio/mix.wav (build/timeline.py + build/mix_audio.py),
# placed in index.html, so the render carries it. Run detached:
#   setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
OUT=renders/preview_udaan_9x16_v1.mp4
npx --yes hyperframes@0.9.86 render --quality draft -w 3 -o "$OUT" > renders/draft.log 2>&1
RC=$?
echo "EXIT $RC" >> renders/draft.log
[ $RC -eq 0 ] || exit $RC
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of compact "$OUT" >> renders/draft.log 2>&1
