# PROGRESS: ashke-lyric-1x1 (updated 2026-11-01)
Phase: v2 PREVIEW (gradient remake with sound effects from 3 s); waiting for the owner's approval before the final.
Current version: v2 preview → renders/preview_ashke-lyric_1x1_v2_sfx.mp4 (draft quality); final v1 delivered 2026-10-31.
What it is: the Ashke edit square (1080x1080, 60 s), built by `ASHKE_FORMAT=1x1 python3 build/generate.py` in
../ashke-lyric-9x16 (v10 build; see its TASTE.md § 3f). Assets are hard links to ../ashke-lyric-9x16/assets (not in git).
Render: build/render_draft.sh (preview + SFX mix), build/render_final.sh (delivery + SFX mix, after approval).
Sound: ../ashke-lyric-9x16/build/sfx_sheet.py maps plan/sfx_events_1x1.json to CC0 OpenGameArt recordings
(../spin-bout-u-drake/assets/sfx/oga); the real-sfx skill mixes them under the untouched song.
