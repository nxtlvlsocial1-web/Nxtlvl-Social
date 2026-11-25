---
workflow: faceless-explainer
flow: automation
storyboard: no
message: "Every girl deserves safety and a future. Support UDAAN, donate today."
destination: instagram-reels
aspect: 9:16
language: hi
length: 74s (v2)
vo_mode: restructured (client script tightened from ~2.5 min to ~60 s)
voice: v2 = client-supplied ElevenLabs read ("Vikram S - Gripping Documentary Host"); v1 = kokoro hf_alpha
cta: "Donate Today / Link in bio" (generic, no org details yet)
---

# UDAAN: Let Her Be Safe. Let Her Rise.

Hindi donation-appeal reel for UDAAN (girls 10 to 19: safety, awareness, skills, independence).
Client script: `plan/client_script.md` (verbatim). Spoken script: `plan/vo_script.tsv`.

Arc: dreams (dawn) -> "is every girl safe?" (dusk) -> hidden truth, silence (night) -> not their fault, our responsibility
-> barriers (gender discrimination, child marriage, no schooling) -> walls shatter, UDAAN revealed (sunrise)
-> three stages 10-14 / 15-17 / 18-19 -> community together -> a better future -> Let Her Rise -> Donate CTA.
Child abuse is shown only symbolically (blur, silence rings, flat line); no child is depicted as a victim.

## Build
1. `bash build/vo.sh hf_alpha 1.05` (needs `/root/.venvs/kokoro` with kokoro-onnx + espeak-ng); s07 is split by hand
   into s07a/s07b (see build/timeline.py).
2. `python3 build/timeline.py` -> assets/audio/voice.wav, plan/timings.json
3. `python3 build/mix_audio.py` -> assets/audio/mix.wav (voice + ducked music + SFX)
4. `npx hyperframes check`, then `setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &`

## v2 (3D)
- Visuals: real-time 3D (three.js, vendored in assets/vendor/three) in `scene3d.js`: low-poly floating-island diorama,
  girl and kite, night, 3D walls with the barrier words that crack and shatter, three stage islands (10-14, 15-17,
  18-19), the community ring, flowers, a sky of kites. HTML overlays (headlines, cards, captions, CTA) in index.html.
- Voice: `python3 build/voice_v2.py` (adds 0.6 s before "उड़ान"), mix: `python3 build/mix_audio_v2.py`.
- Render: `setsid nohup bash build/render_draft_v2.sh > /dev/null 2>&1 < /dev/null &` (software WebGL, ~25 min).
- v1 (2D SVG version) is kept as plan/v1/index_v1.html.txt.
