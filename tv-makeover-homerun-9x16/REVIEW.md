# Review — final v1

- Structure: after the hit and the "4 STEPS" sky beat, the camera locks on the runner in a side-scrolling
  tracking shot; he never stops. Bases are placed so he touches each one on its call (10.3, 14.2, 19.3,
  slide home 24.0). Before 1st base only the runner is on screen; on each touch a retro TV powers on above
  him with that step. After the slide the shot pulls back into the family's TV: they cheer while the TV
  zaps the junk apps; the ending is a front-on shot of the family cheering under the CTA.
- Music: an original chiptune composed in code (build/chiptune.py), timed to the voiceover. Measured, not heard.
- Measured: check passes (kept: canvas is full-bleed on purpose). Draft 2: 1080x1920, 30 fps, 34.2 s,
  -15.2 LUFS, -1.3 dBTP, no clipping.
- Missing: crowd cheering and bat crack. Three Higgsfield clips with that audio are generated (jobs
  6f49d9d1, 08c7f5e1, 3ceb833d) but their host d8j0ntlcm91z4.cloudfront.net is blocked by the session's
  network policy. Caption timing is still estimated from the voiceover's pauses.
- Draft 3: the TV screens are now pixel versions of the two references the person supplied (a cluttered
  stock Android TV home and a premium tab/hero/poster home). Real app logos and film posters were replaced
  with original pixel art and generic names (PEAK+, ORBIT, MECHA, HERO, BOLD, HEIST, ROAD).
- Draft 4: chiptune replaced by a Higgsfield-generated instrumental stadium-rock bed; bat crack on "OUT";
  crowd cheers on each base, the home run and the CTA (sources in assets/audio/SOURCES.md). The 10 s
  "running crowd" clip was left out: its spectrum read as tonal (possible chanting/voices). Draft 4
  measured -15.1 LUFS, -1.2 dBTP, no clipping. Nobody has listened to the generated audio yet.
- Draft 5: constant elegant minimal bed (job 4307111c) from 0 to 34.19 s, levelled to within a few dB
  and looped with a crossfade; crowd and bat sounds unchanged. -15.5 LUFS, -1.3 dBTP, no silence gaps.
- Draft 6: voiceover at 1.1x (pitch kept), film 31.08 s; story clock mapped in game/hud, captions and
  audio retimed. Hook: BEFORE/AFTER split teaser on frame 0, wipe, six pop-up ads slamming in with pops
  and shakes, constant push-in, BILLBOARD punch. Base tracker in the commentator box. Punch zooms on base
  touches, push into the TV during the clean-up. Faster runner. Upbeat sports/tech bed (job 77913ff9)
  started past its soft intro. -16.2 LUFS, -1.8 dBTP, no clipping, no silence. Not listened to.
- Draft 7: a pixel Claude character bats; broadcast ball tracer from the pitcher's release through the hit,
  with AT BAT lower-third and pitch / exit-velocity / distance readouts. The run is a ground-level camera
  leading Claude (pseudo-3D field) that swings round each base. TV screens are realistic full-resolution
  UIs composited over the pixel world: a cluttered stock home and the person's reference home (greeting,
  clock, chips, app dock with real app tiles, focused-app artwork backdrop). -16.2 LUFS, -1.8 dBTP.
- Final v1: BEFORE/AFTER teaser removed (frame 0 is the cluttered screen); HBO Max added to the dock (logo
  supplied by the person) as the fifth app; app tiles keep their logo proportions; rendered at delivery
  quality, 60 fps, 1080x1920, 31.08 s, -16.4 LUFS, -1.9 dBTP, no clipping. Cover = frame 0.
