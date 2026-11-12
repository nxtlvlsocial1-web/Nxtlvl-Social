#!/usr/bin/env bash
# Preview render (draft quality), then sound twice: with the owner's song and without it (for Instagram's audio picker).
# Run detached:  setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
rm -f renders/master_draft.mp4
npx --yes hyperframes@0.8.203 render --quality draft --sdr -w 3 -o renders/master_draft.mp4 > renders/draft.log 2>&1
RC=$?
echo "EXIT $RC" >> renders/draft.log
if [ $RC -ne 0 ] || [ ! -s renders/master_draft.mp4 ]; then echo "SFX EXIT skipped (render failed)" >> renders/draft.log; exit 1; fi
python3 build/sfx_mix.py renders/master_draft.mp4 renders/nxtlvl_gta6-playbook_reels_9x16_draft.mp4 >> renders/draft.log 2>&1
python3 build/sfx_mix.py renders/master_draft.mp4 renders/nxtlvl_gta6-playbook_reels_9x16_draft_nomusic.mp4 --no-music >> renders/draft.log 2>&1
echo "SFX EXIT $?" >> renders/draft.log
