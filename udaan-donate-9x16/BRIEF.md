---
workflow: faceless-explainer
flow: automation
storyboard: no
message: "Every girl deserves safety and a future. Support UDAAN, donate today."
destination: instagram-reels
aspect: 9:16
language: hi
length: 66s
vo_mode: restructured (client script tightened from ~2.5 min to ~60 s)
voice: kokoro hf_alpha (local; ElevenLabs had no credits, HeyGen not signed in)
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
