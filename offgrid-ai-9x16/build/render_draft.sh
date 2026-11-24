#!/usr/bin/env bash
# Preview render, then the sound mix: Kokoro voice + "Funky Nurykabe (Spinningmerkaba Mix)" (CC BY 3.0, plan/music.json)
# ducked under it + sound effects. Run detached:
#   setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
export SONG=funky_nurykabe.mp3 SONG_AT=115.96 MUSIC_LUFS=-22
rm -f renders/master_draft.mp4
npx --yes hyperframes@0.8.203 render -w 3 -o renders/master_draft.mp4 > renders/draft.log 2>&1
RC=$?
echo "EXIT $RC" >> renders/draft.log
if [ $RC -ne 0 ] || [ ! -s renders/master_draft.mp4 ]; then echo "SFX EXIT skipped (render failed)" >> renders/draft.log; exit 1; fi
python3 build/sfx_mix.py renders/master_draft.mp4 renders/ai-nxtlvl_offgrid-ai_reels_9x16_v1_draft.mp4 >> renders/draft.log 2>&1
echo "SFX EXIT $?" >> renders/draft.log
