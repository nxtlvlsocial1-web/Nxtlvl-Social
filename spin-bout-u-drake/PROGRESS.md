# PROGRESS: spin-bout-u-drake (updated 2026-10-31)
Phase: v16 PREVIEW (with sound design) (draft for the owner's approval; final not rendered yet)
v11: Ashke-structure collage (build/collage.py) in the Spin colours over a live gradient background. The anime
pictures the owner sent back are removed; lyric concepts replace them (footsteps + counter, GPS route + pins +
compass, shockwaves, heart rings, BODY wisps); full-screen smoke, burn, drop and ghost on those lines. Vogue call screen shows the name
(assets/img/collage/call_vogue.jpg, not in git); the dumb cat has its own spot. After Effects finish: harder whips,
per-scene zoom snaps, random bloom + RGB split on cuts, light leaks.
Previous: final v2 → renders/nxtlvl_spin-bout-u_reels_1x1_v2.mp4; previews v3-v10.
Build: python3 build/clips_drake.py (owner clip segments), python3 build/pixel.py (pixel sprites), python3 build/fluidbg.py (liquid gradient bg video), python3 build/collage_tex.py (paper, scraps, stickers), node build/render3d.cjs [id] (3D WebMs from
plan/g3d.json and assets/js/g3d.js), python3 build/clips90.py (owner's Canva clips), python3 build/collage.py
(index.html); draft with build/render_draft.sh, final with build/render_final.sh (both detached with setsid nohup).
Not in git: the song, owner photos and their cut-outs/prints/stickers, Canva art and clips, renders.
Sound: python3 build/oga_sfx.py (CC0 packs -> assets/sfx/oga, not in git; credits plan/sfx_credits_oga.json, all CC0),
register once with the real-sfx skill (setup.py add-library oga_cc0 assets/sfx/oga --tier main --index), then
build/render_final.sh runs build/sfx_sheet.py + the skill's mix.py on the graded master. Pixel art: build/mascot.py.
