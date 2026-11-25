#!/usr/bin/env bash
# UDAAN 9:16 v2 (3D) draft render (preview for approval). Audio is assets/audio/mix_v2.wav (build/voice_v2.py + build/mix_audio_v2.py),
# placed in index.html, so the render carries it. Run detached:
#   setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
OUT=renders/preview_udaan_9x16_v2.mp4
npx --yes hyperframes@0.9.93 render --quality draft -w 3 -o "$OUT" > renders/draft_v2.log 2>&1
RC=$?
echo "EXIT $RC" >> renders/draft_v2.log
[ $RC -eq 0 ] || exit $RC
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of compact "$OUT" >> renders/draft_v2.log 2>&1
