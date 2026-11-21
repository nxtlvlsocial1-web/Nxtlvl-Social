---
workflow: general-video
flow: automation
storyboard: no
message: "A million-view clip pays $225 on a capped campaign; five 200K clips pay $900"
destination: instagram-reels
aspect: 1080x1920
language: en
length: 38.7s
voice: am_michael
angle: concept
---

## Intent

A neon Miami-night motion-graphics reel that does the payout math for one creator campaign's rules
(Dylan Page campaign, $1 per 1,000 views, $250 cap per clip, 10% platform fee). The numbers are
examples of how the campaign's rules work, never a promise of earnings. Built to the owner's
13-scene timing table. The first cut had no voiceover; the owner then asked for one: Kokoro "Michael" (am_michael,
picked from samples) reads the exact script, and the reel is retimed to the voice (38.7 s).

## Assets

- assets/fonts/ - Barlow Condensed 700-900 (headlines, numbers) and Inter 500-800 (labels, captions), both SIL OFL.
- assets/sfx/, assets/audio/mix.wav - whoosh, tick, pop and impact effects synthesised locally by build/sfx.py (no third-party audio).
- assets/audio/voice.wav - the voiceover (local Kokoro TTS, voice am_michael), from build/voice.py.

## Customizations

- Voiceover (owner's request, after the first cut): build/voice.py voices each line, transcribes it for word times,
  and writes a time warp so scenes and key hits land on the spoken words; captions use the spoken word times.
- "A little cleaner": softer camera moves, shake, flashes, bloom and grain; no glint light.

- Owner asked for it "3D, clean and aesthetic, more engaging": a Three.js layer (assets/js/scene3d.js) with a neon
  studio, extruded 3D numbers in Barlow Condensed Black (build/font3d.cjs), 3D objects per beat and a moving camera
  (whip into each scene, push-ins, orbit, punch-ins). Headlines, captions, warning card and comment box stay HTML.

- Word-by-word captions, 2-4 words at a time, accent word in pink/orange with a pop, lower middle.
- Thin progress bar along the top edge across the full length.
- Last frames wipe back to the opening layout so the reel loops into scene 1.
- Cover: cover.html, title inside the centre 1080x1350.

## Notes

- Text safe area: x 60-950, y 250-1500 (owner's zones: top 250, bottom 420, right 130; house rule 60 left).
- No Rockstar/GTA logos, artwork, fonts, footage. No photos or likenesses of real people; names as text only.
- No handle, logo intro or watermark. Red only for the strike-through and the cap.
- Scene 4 carries "Rates as of 20 Nov 2026. Check the campaign page."
- Never write "you will earn".
