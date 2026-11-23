---
workflow: general-video
flow: automation
storyboard: no
message: "One free skill finds and installs the right Claude skills for you"
destination: instagram-reels
aspect: 1080x1920
language: en
length: 27.7s
voice: am_michael
angle: concept
---

## Intent

A remake of the owner's 52 s find-skills reel (uploaded reference): under 40 s, a stronger hook, and full 3D motion
graphics in place of the split screen. Trend-paced: a scroll-stopping open, a visual event every 1-2 s, karaoke
captions, a comment-keyword CTA that loops back to the hook.

## Assets

- assets/audio/voice.wav - voiceover (local Kokoro, am_michael), from build/voice.py.
- assets/audio/music.wav - background music generated locally with MusicGen (build/music.py, fixed prompt and seed),
  the owner's choice over the HeyGen library or a CC track; ours, nothing to credit. Ducked under the voice in the mix.
- assets/sfx/, assets/audio/mix.wav - synthesised effects and the final mix (build/sfx.py), no third-party audio.

## Notes

- Facts checked on skills.sh, 23 Nov 2026: 1,528,982 skills; find-skills (vercel-labs/skills) #1 with 4.5M installs.
  The reference's spoken "700,000" and "3 million" were out of date and are not used.
- No Claude, Anthropic or Vercel logos; names as text only. Safe zones: x 60-950, y 250-1500.
