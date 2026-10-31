# PROGRESS: spin-bout-u-drake (updated 2026-10-31)
Phase: v5 PREVIEW (draft for the owner's approval; final not rendered yet)
v5: six scenes play the owner's Canva Image-to-Video clips through build/clips90.py (on threes, 90s broadcast look);
the other anime scenes keep the stepped wind/breathing. Clip sources: assets/video/anime/<name>_src.mp4 (not in git).
Previous: final v2 → renders/nxtlvl_spin-bout-u_reels_1x1_v2.mp4; v3 preview (MJ-reference cuts, still anime art)
v4 changes (owner feedback on v3): the anime illustrations move (wind displacement maps, breathing, flowing smoke and
fire, light sweeps, particles); type and cuts rebuilt from the Spin Bout U reference (giant pop-in letters grey to
white, block-shadow words, stickers, starbursts, brush "Spin", cones, rays, squiggles, floor type; whip with light
line, zoom-white, badge swing, push, drop, strips, glitch card, diagonal scroll, slide up); palette back to black /
maroon / magenta / off-white; the dance picture redone with a calm smile.
Build: python3 build/align.py, build/assets.py, build/anime.py, build/animaps.py, build/generate.py; draft with
build/render_draft.sh, final with build/render_final.sh (both detached). Anime art: export Canva design DAHZkxbQbhE
pages 2-15 as PNG into assets/img/anime/src/<name>.png (names in plan/anime.json order).
