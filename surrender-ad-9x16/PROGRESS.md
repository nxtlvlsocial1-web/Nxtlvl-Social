# PROGRESS: surrender-ad-9x16 (updated 2026-11-06)
Phase: v1 PREVIEW rendering (draft); final after the owner's approval.
What it is:
- Talking-head ad for Kanak Kesar (The Conscious Millionaire): "comment SURRENDER". 9:16, 1080x1920, 30 fps, 137 s.
- Raw take: 145 s, landscape 720p (assets/video/raw.mp4, not in git).

References (reference/, not in git):
- ref_elevenlabs.mp4 (the girl's ElevenLabs reel). Copied:
  - The pink dotted background.
  - The Before / After two-screen opening.
  - The split: top screen, bottom face, a black-box white caption on the seam.
  - Full-frame punches: script word plus a big Anton word, red on key words.
  - Its transitions frame by frame, the yellow COMMENT box CTA and its sound grammar.
- ref_nxtlvl_promo.mov (the Nxtlvl Social promo). Copied:
  - The smoothness and pacing of its motion elements, in the top half.
  - Restyled to the pink with liquid glass.

Pipeline:
1. build/tight.py: every pause under -30 dB longer than 0.1 s cut to 0.08 s. Gives assets/video/tight.mov and
   plan/words_tight.json. 145.4 to 136.6 s: the speaker barely pauses.
2. The grade and crops (in this file's history): face_full.mp4 (405x720 crop to 1080x1920) and face_split.mp4
   (810x720 crop to 1080x960).
3. build/music_bed.py: the owner's track from 0:46, looped on downbeats (2:03.78 back to 1:19.32) to cover 139 s.
4. build/generate.py writes index.html (sections, transitions, captions, glass graphics, sound moments).
5. build/sfx_sheet.py: plan/sfx_events.json mapped to CC0 OGA recordings. Openverse/Freesound refuses cloud
   downloads.
6. build/render_draft.sh / render_final.sh: render, then voice + ducked music, then the SFX mix.

Captions: Hinglish in Latin script (generate.py ROMAN maps the Devanagari Scribe words).
Notes:
- The full-frame shots are a 2.7x upscale of 720p footage, so they are softer than the split-screen ones.
- The music is a commercial track (Melly Mike). As a paid ad it needs a licence, or the in-app library.
