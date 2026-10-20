---
workflow: product-launch-video
flow: automation
storyboard: yes
message: "Your entire creative team, from $5 a month"
destination: youtube-website
aspect: 1920x1080
language: en
audience: "Owners of cafés, salons, gyms and shops who need a feed but not an agency"
length: 30s
angle: promo
narration: no
---

## Intent

A 30-second promo for Nxtlvl Social itself, a creative + automation studio for small businesses.
Concept A, "The feed fills itself": an empty Instagram grid on a phone fills tile by tile, on the
beat, with the things Nxtlvl makes (reels, Diwali posters, carousels, menu cards, offers). It then
pulls back to a wall of feeds for many kinds of business (cafés, salons, gyms) and lands on
"from $5 a month". The user asked for it to be "cool, smooth, with music and SFX — 10/10".

Hook: a "0 posts" profile, and the first tile slams in on the first beat. No logo-first intro.
At 16:9 the phone leaves both sides of the frame open: they carry big kinetic type that changes
with each beat. Ends on a call-to-action card held ≥ 2 s: "Book a free call" + the web address.

## Assets

- website/index.html (repo root) — the Nxtlvl landing page: copy, palette, fonts and the logo
  (embedded PNG) are the source of the look. Captured from a local preview server.

## Customizations

- Cuts on the beat: every tile slam, cut and SFX lands on the music's beat grid. The music is
  composed in code, so the beat grid is known exactly and written alongside the track.
- Original music track composed in code (no licensing questions): placed as host BGM
  (`"source": "host"` in audio_meta.json) with `music: none` in the storyboard.
- SFX from the bundled HyperFrames library (no account needed).
- Posts on the grid are designed sample posts in the Nxtlvl style (no client work supplied).

## Notes

- No voiceover. Plays muted on the website too, so every message is carried by on-screen type.
- Keep the website's colour theme: ink #05030C, violet #7D18FC, lift #A95CFF, deep #3D0789,
  pale #D8BBFF; fonts Archivo (display), Instrument Sans (body), Instrument Serif (accent).
- Don't overclaim. Price line is "from $5 a month" exactly as on the site.
- Deliver as nxtlvl_promo_youtube_16x9_v1.mp4 plus a 1-frame cover PNG (nxtlvl-social-video § 6).
