---
workflow: hyperframes
flow: automation
storyboard: no
message: "Your entire creative team, in one studio"
destination: website-hero
aspect: 1920x1080
language: en
audience: "Owners of cafés, salons, gyms, clinics and shops who need a feed and a website but not an agency"
length: 32s
angle: brand motion design (SaaS / After Effects style)
narration: no
---

## Intent

A 30–35 s motion-graphics brand film for the Nxtlvl Social website: smooth SaaS-style motion
design with floating UI surfaces, a brand cursor, kinetic type, SFX and an original music bed.
Storyline A from STORYLINES.md: one café's chai photo travels through the four services
(social media design, reels, websites, automation) and the Shooting Star lands the studio's name.
No prices, no WhatsApp (the site is email-only); ends on "Book a free call · nxtlvlsocial.ai".

## Assets

- assets/shooting-star.svg and assets/nxtlvl-wordmark.png — the brand mark and wordmark.
- assets/fonts/ — Archivo, Instrument Sans, Instrument Serif (OFL).
- assets/css/kit.css — the shared Nxtlvl ground, type and phone from the earlier promo.
- assets/sfx/ — bundled Pixabay-licensed sounds (see CREDITS.md).

## Customizations

- Music composed in code (tools/compose_music.py), 120 BPM, 32 s, deterministic; placed as BGM.
  No HeyGen sign-in and no local music model were available; the earlier promo used the same
  approach and the user approved it.
- SFX cues written on the beat grid by tools/sound_cues.py, assembled by tools/assemble_audio.py.
- Draft MP4 goes to the user for approval before the delivery render (CLAUDE.md rule).
