---
workflow: general-video
flow: automation
storyboard: no
message: "OpenAI killed Sora because every video cost them GPU money: in AI, cheap beats cool"
destination: youtube-shorts, instagram-reels
aspect: 1080x1920
language: en
audience: viewers of a faceless AI and business case-study channel
length: 30s
angle: narrated kinetic explainer
---

## Intent

v2 of the first Short for the Nxtlvl faceless AI case-study channel ("Why OpenAI Killed Sora"), rebuilt from the v1
scene plan with the open-source voiceover mixed in. Seven scenes on the script's cues: VIRAL (Sora icon, trend arrow,
reactions), KILLED (OpenAI logo, red X, glitch, SHUT DOWN stamp), GPU money (video tiles into a GPU chip, GPU BILL
meter, EVERY. SINGLE. TIME. slams), MORE USERS = MORE LOSS (illustrative chart), HYPE doesn't pay the BILLS (invoice,
HYPE coin, DECLINED stamp), CHEAP > COOL (balance scale), FOLLOW CTA. Dark blue / red / orange look, word-timed
kinetic captions with a red active-word sweep.

## Assets

- assets/img/sora-icon.png: the Sora app icon (user upload, white corners cut away)
- assets/img/openai-logo.png, openai-mark.png: the OpenAI logo (user upload, made transparent)
- assets/audio/vo_raw.wav: Kokoro (Apache-2.0) voice am_michael at 1.1x, build/vo.py; vo.wav is the levelled copy
- assets/audio/music.wav: original trap beat and SFX synthesized by build/audio.py, ducked under the voice
- fonts (all OFL): Archivo variable (wdth 62-125), Instrument Serif Italic, JetBrains Mono
- cover.html: the cover still, snapshot by build/cover.cjs

## Customizations

- No dollar figures and no "$500B" claim; the chart is labelled ILLUSTRATIVE and the invoice shows $$$ only.
- "#1 ON THE APP STORE" refers to Sora reaching the top of the US App Store after launch (Oct 2025 reporting).
- Captions are timed from the voiceover's speech runs (silence detection), words spread by length within each run.

- Type (v2 feedback: "premium and cool"): Archivo Expanded 800-900 for statements and captions (the economics
  voice), Instrument Serif Italic on the key words (viral, killed, loss, hype, cool, follow; the hype voice),
  JetBrains Mono for labels and data. Captions use a glowing underline on the spoken word instead of a red box.

## Notes

- Rebuild: python3 -I build/vo.py <kokoro model dir> && python3 -I build/generate.py && python3 -I build/audio.py
