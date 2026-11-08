# Shooting Star: Instagram profile picture (final, option B "Balanced")

The chosen Instagram profile picture: a white four-point star with three tapered trails (white, lilac, violet),
centred on a near-black background with violet light glowing in from the top-left and bottom-right corners.

| File | Use |
|---|---|
| `instagram-profile-1200.png` | Upload to Instagram (square; Instagram crops it to a circle) |
| `instagram-profile-400.png` | Smaller copy |
| `instagram-profile.svg` | Vector master, no fonts needed |

The mark is sized to sit inside the circle crop with nothing clipped.

Colours: base `#0A0620` to `#05030C`, corner glows `#7E1AF6` (top-left) and `#5E06F2` (bottom-right),
star and main trail `#FFFFFF`, lower trail `#A95CFF`, upper trail `#B98AFF`.

## Animated GIF (`gif/`), no text: Google Workspace

A 3.2 s seamless loop: the logo at rest, the star turns a quarter with a soft flare, then the whole mark streaks out
to the top right and flies back in from the bottom left (motion-blurred). Frame one is the logo at rest, so anywhere
that shows only the first frame still shows the full mark.

| File | Use |
|---|---|
| `gif/nxtlvl-shooting-star-200.gif` | Gmail signature (Settings → Signature → insert image; ~137 KB) |
| `gif/nxtlvl-shooting-star-512.gif` | Google Sites, Slides, Chat; large copy (~500 KB) |
| `gif/nxtlvl-shooting-star-96.gif` | Small inline / footer use (~49 KB) |

Google account profile photos don't animate (they show frame one): use `instagram-profile-1200.png` there.
Rebuild with `python3 gif/source/build.py` (needs Playwright and FFmpeg).
