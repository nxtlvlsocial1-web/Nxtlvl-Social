#!/usr/bin/env bash
# Dr Kokila "children" reel, 9:16 preview (draft quality). No music (owner): her cleaned voice, then the sound effects
# (build/sfx_sheet.py + the real-sfx skill's mix.py, voice-safe), master -14 LUFS.
# Run detached: setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
V=${V:-1}
OUT=renders/preview_kokila-kids_reels_9x16_v$V.mp4
LOG=renders/draft.log
: > $LOG
python3 build/generate.py >> $LOG 2>&1 || { echo "GEN FAILED" >> $LOG; exit 1; }
DUR=$(python3 -c "import re;print(re.search(r'data-duration=\"([0-9.]+)\" data-fps',open('index.html').read()).group(1))")
rm -f renders/draft_master.mp4
npx --yes hyperframes@0.8.203 render --quality draft --sdr -w 3 -o renders/draft_master.mp4 >> $LOG 2>&1
RC=$?; echo "RENDER EXIT $RC" >> $LOG
if [ $RC -ne 0 ] || [ ! -s renders/draft_master.mp4 ]; then echo "MIX skipped (render failed)" >> $LOG; exit 1; fi
ffmpeg -v error -y -i assets/audio/voice.wav -af "highpass=f=80,afftdn=nf=-28,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=2,loudnorm=I=-16:TP=-2:LRA=9,aresample=48000,apad=whole_dur=$DUR,atrim=0:$DUR" assets/audio/voice_clean.wav >> $LOG 2>&1
ffmpeg -v error -y -i renders/draft_master.mp4 -i assets/audio/voice_clean.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le renders/draft_voice.mov >> $LOG 2>&1
echo "VOICE EXIT $?" >> $LOG
SFX_SKILL=$(ls -d /root/.claude/skills/synced/*/real-sfx 2>/dev/null | head -1)
python3 build/sfx_sheet.py "$PWD/renders/draft_voice.mov" --out "$PWD/renders/cues_preview.json" >> $LOG 2>&1
(cd "$SFX_SKILL" && python3 scripts/mix.py "$OLDPWD/renders/cues_preview.json" --out "$OLDPWD/renders/draft_sfx.mp4" --voice-safe --target-lufs -14) >> $LOG 2>&1
echo "SFX EXIT $?" >> $LOG
ffmpeg -v error -y -i renders/draft_sfx.mp4 -map 0:v -map 0:a -c:v libx264 -preset veryfast -crf 23 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "$OUT" >> $LOG 2>&1
echo "ENC EXIT $?" >> $LOG
echo "ALL DONE" >> $LOG
