#!/usr/bin/env bash
# Final render (owner approved the v3 preview): delivery quality, then sound twice (with the owner's song, and without
# it for Instagram's audio picker), then the openverse-sfx skill's verify_mix.py on the song version.
# Run detached:  setsid nohup bash build/render_final.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
rm -f renders/master.mp4
npx --yes hyperframes@0.8.203 render --quality high --sdr -w 3 -o renders/master.mp4 > renders/final.log 2>&1
RC=$?
echo "EXIT $RC" >> renders/final.log
if [ $RC -ne 0 ] || [ ! -s renders/master.mp4 ]; then echo "SFX EXIT skipped (render failed)" >> renders/final.log; exit 1; fi
python3 build/sfx_mix.py renders/master.mp4 renders/nxtlvl_gta6-playbook_reels_9x16_v1.mp4 >> renders/final.log 2>&1
python3 build/sfx_mix.py renders/master.mp4 renders/nxtlvl_gta6-playbook_reels_9x16_v1_nomusic.mp4 --no-music >> renders/final.log 2>&1
python3 ~/.claude/skills/openverse-sfx/scripts/verify_mix.py renders/nxtlvl_gta6-playbook_reels_9x16_v1.mp4 --target -14 --outdir renders/verify >> renders/final.log 2>&1
echo "SFX EXIT $?" >> renders/final.log
