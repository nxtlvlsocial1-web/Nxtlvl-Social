# clip-math-9x16

40 s vertical Instagram Reel (1080x1920, 30 fps): one campaign's payout math, as neon motion graphics.
Brief and rules: `BRIEF.md`.

## Files

| Path | What it is |
| --- | --- |
| `index.html` | The whole composition: 13 scenes, one paused GSAP timeline. Scene times are in the section `data-start` / `data-duration` attributes and the timeline script below them. |
| `build/captions.json` | Caption chunks and timings (2-4 words each). Edit captions here, not in `index.html`. |
| `build/captions.mjs` | Writes `out/captions.srt` and injects the caption data into `index.html`. |
| `build/sfx.py` | Mixes the sound effects into `assets/audio/sfx.wav` (cue times match the animation). |
| `build/grain.py` | Makes the film-grain tile `assets/img/grain.png`. |
| `cover/cover.html`, `build/cover.mjs` | The cover design and its renderer (writes `out/cover.png`). |
| `build/render_final.sh` | Detached final render, then the ffmpeg delivery encode to `out/reel.mp4`. |

## Rebuild

```bash
python3 build/sfx.py
```

```bash
node build/captions.mjs
```

```bash
npx hyperframes check
```

```bash
node build/cover.mjs
```

```bash
setsid nohup bash build/render_final.sh > /dev/null 2>&1 &
```

The render writes `DONE` or `FAILED` to `/tmp/clip-math-render/render.status` and logs to
`/tmp/clip-math-render/render.log`. `out/reel.mp4` and `renders/` stay out of git.

## Timing (no voiceover supplied)

| # | Time | On screen |
| --- | --- | --- |
| 1 | 0-3 s | 1,000,000 views = $225 (on screen at frame 0); counters climb, slam to $225 |
| 2 | 3-5 s | Not $1,000. (red strike) |
| 3 | 5-7 s | The math nobody shows you (wipe, receipt) |
| 4 | 7-11 s | $1 per 1,000 views; bar grows; Dylan Page campaign label; rates-date line |
| 5 | 11-15 s | Capped at $250 per clip; bar hits the red ceiling; views keep counting |
| 6 | 15-18 s | -10% platform fee; slice cut off; $250 becomes $225 |
| 7 | 18-21 s | Stops earning at 250K views; timeline greyed after 250K, labelled $0 |
| 8 | 21-23 s | Now watch this. (pink clean frame, horizontal motion) |
| 9 | 23-28 s | 5 clips x 200K views; five phone cards count to 200K / $200 |
| 10 | 28-32 s | Same 1M views = $900; $1,000 minus 10%; split $225 vs $900; 4x stamp |
| 11 | 32-34 s | Stop chasing one viral clip; the single card shrinks, five stay |
| 12 | 34-37 s | Budgets run out fast. Check the campaign page. (warning card) |
| 13 | 37-40 s | Comment MATH (typing); clears to the bare background so the loop cuts back to scene 1 |

If a voiceover is added later, put it in `assets/voiceover.wav`, get word timestamps (ElevenLabs Scribe per the
repo's CLAUDE.md), retime `build/captions.json` and the scene times to it, and add it as an `<audio>` track.
