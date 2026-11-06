# PROGRESS: surrender-ad-9x16 (updated 2026-11-06)
Phase: v2 PREVIEW rendering (1080p original, repeats cut: 117.1 s, faster motion, name Kanav); final after approval.
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

v2 (owner, 2026-11-06):
- The source is now the owner's 1080p original (assets/video/drive2/raw_hq.mp4, from Drive, not in git; 0.048 s
  later than the 720p copy Scribe transcribed).
- Each piece is cut on whole frames, so picture and sound stay locked.
- Repeated lines cut (tight.py CUT_WORDS): mehnat x2, an ego line, "surrender karne ka matlab" x2, the courses list
  repeated in his story, "naye perspective" x2, three "guys". 136.6 s down to 117.1 s.
- His name is Kanav Kesar (Scribe heard Kanak). A liquid-glass name card sits under the captions.
- Faster motion elements: 0.5 s entrances and 0.22 s exits, an icon pop on every card, a faster float and a slow push
  on the top half.
