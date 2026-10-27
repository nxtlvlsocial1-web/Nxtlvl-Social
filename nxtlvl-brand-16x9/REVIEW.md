# Review — Nxtlvl Social brand film (32 s, 1920×1080, 30 fps)

## Creative calls

- Storyline A "One café, four screens" was built: one chai photo travels through design → reels →
  website → automation, then the Shooting Star strikes and the lockup lands. Not built: B "The feed
  fills itself" (the earlier promo's shape) and C "Type carries the argument" (a 10 s sting at best).
- Six scenes on a 120 BPM grid (2 s bars): hook 0–4, design 4–10, reels 10–16, website 16–22,
  automation 22–27, end card 27–32. Hard cuts on the drop (4 s) and the impact (22 s), whips between
  the three UI scenes, a dip cut into the impact, and the star streak covering the last seam.
- No prices and no WhatsApp anywhere (the site is email-only). The site copy is quoted verbatim.
- Registry blocks `logo-sting`, `kinetic-type-swap` and `shimmer-sweep` were read as reference and
  then removed: they ship their own fonts and colour variables, so the swap, the sting and the sweep
  were authored in the brand kit instead.

## Measured, looked at, nobody checked

- `npx hyperframes check`: 0 errors, 0 warnings across lint, runtime, layout, motion, contrast and
  craft. Remaining infos are the ground glows overflowing the canvas on purpose.
- Looked at: 24 snapshot frames (two contact sheets) at the QA moments in SPEC.md, including the
  two frames that first showed clipped headlines (fixed: card headline 54 px, reel captions 70 px).
- The sound was measured, not heard: the bed peaks at −4.6 dBFS, RMS 0.165 (about −14 LUFS); every
  effect is placed one frame after its picture from each file's measured peak. Nobody has listened
  to the mix against the picture.

## Weakest shot

Frame 4 (website): the real site hero is rebuilt in HTML inside the browser window, at 1:1 with the
live page's copy, but it is a rebuild, not a capture. With more time: capture the deployed site
with `npx hyperframes capture` once it is live and use the real plate.

## Warnings kept on purpose

- `panel_out_of_canvas` infos on the ground glows: the kit's atmosphere bleeds past the frame by
  design (marked `data-layout-allow-overflow`).
- The music is composed in code (`tools/compose_music.py`), as in the earlier promo, because no
  HeyGen sign-in and no local music model were available; the user approved that approach before.
