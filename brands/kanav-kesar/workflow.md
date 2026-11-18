# Kanav Kesar: workflow and skills

> Public part of this client's memory: look and workflow only. The brief, feedback, scripts, footage list,
> hooks/CTAs, calendar and open items live in the private `nxtlvl-client-memory` account skill.

How his talking-head ad was made, step by step, with the settings that worked, the mistakes and fixes, and the delivery
rules. Paths relative to `/home/user/Nxtlvl-Social/surrender-ad-9x16/` unless absolute.

*Sources: notes `/tmp/claude-0/-home-user-Nxtlvl-Social/b1c6bbee-7bc1-59ac-ac25-7b3da31f270a/scratchpad/notes_kanav.md` § 2, § 5, § 9; `build/tight.py`, `build/music_bed.py`, `build/render_final.sh`, `build/render_draft.sh`, `build/render_hooks.sh`, `build/generate.py`; `/home/user/Nxtlvl-Social/CLAUDE.md`; `/home/user/Nxtlvl-Social/.claude/skills/nxtlvl-social-video/SKILL.md`.*

## Index

1. [Skills and tools used](#1-skills-and-tools-used)
2. [Step-by-step process (talking-head ad)](#2-step-by-step-process-talking-head-ad)
3. [Settings that worked](#3-settings-that-worked)
4. [Commands](#4-commands)
5. [Mistakes, fixes and lessons](#5-mistakes-fixes-and-lessons)
6. [Delivery rules](#6-delivery-rules)
7. [Checklist for the next Kanav video](#7-checklist-for-the-next-kanav-video)

---

## 1. Skills and tools used

| Tool / skill | Used for |
| --- | --- |
| `nxtlvl-social-video` (agency skill) | Formats, safe zones, naming, delivery rules |
| `hyperframes` / `hyperframes-core` / `-animation` / `-cli` | Composition (HTML + one paused GSAP timeline), render (`hyperframes@0.8.203`) |
| `hyperframes-creative` presets | Fonts (Inter, Anton, Kaushan Script) |
| `real-sfx` skill | `scripts/mix.py` to mix the SFX cue sheet under voice + music; cue reports, resolved cues |
| ElevenLabs Scribe | Transcript with word timestamps (supplied by the owner as `15_hin.json`) |
| FFmpeg / ffprobe | Silence detection, tight cut, crops, grade, speed-up, music bed, final mix and encode, loudness checks |
| Python scripts | `build/tight.py`, `build/generate.py`, `build/music_bed.py`, `build/sfx_sheet.py` |
| OpenGameArt CC0 SFX library | `../spin-bout-u-drake/assets/sfx/oga` (Openverse / Freesound downloads refused from the cloud session) |
| Google Drive | Receiving the >30 MB original from the owner |
| SendUserFile (chat) | Delivering previews and finals |

## 2. Step-by-step process (talking-head ad)

1. **Collect inputs.** Raw take (ask for the original camera file, not a compressed or edited copy; use a Drive link for
   files over ~30 MB), Scribe transcript JSON, reference reels, music file, client name spelling.
2. **Transcript.** Use the Scribe JSON (`plan/transcript_scribe.json`). Check names (Scribe heard "Kanak"; it is
   "Kanav"). If the transcript was made on another copy, measure the offset by audio cross-correlation (here the 1080p
   file runs 0.048 s later; `OFFSET = .048`).
3. **Tight cut** (`build/tight.py`): silencedetect after a 90 Hz high-pass; every pause under -30 dB for >= 0.1 s cut to
   0.08 s (half kept on each side so breaths and word tails are not clipped); 8 ms audio fades at joins. Word-gap cutting
   from Scribe times was tried first and saved only ~9 s.
4. **Remove repeated lines and fillers** (`CUT_WORDS`, Scribe indices inclusive): anything said twice, and "guys"
   fillers. A cut runs from just before its first word (-0.03 s) to just before the next kept word.
5. **Cut on whole frames:** `round(t*30)/30`; encode each piece separately with `-frames:v` and `apad` its audio to its
   frame length, then concat (one big filter graph ran out of memory). Picture and sound stay locked (117.100 s video /
   117.093 s audio).
6. **Speed-up:** `setpts=PTS/1.1` + `atempo=1.1` (pitch kept), output 30 fps, x264 CRF 14 + PCM 48 kHz to
   `assets/video/tight.mov`; `plan/words_tight.json` maps every word onto the final clock.
7. **Crops and grade:** face_full `crop=608:1080:717:0` -> 1080x1920 (lanczos, unsharp 5:5:0.45); face_split
   `crop=1215:1080:412:0` -> 1080x960; grade `eq=contrast=1.06:saturation=1.1:gamma=0.98,colorbalance=rs=0.02:bs=-0.03:rh=0.02`.
8. **Composition** (`build/generate.py` -> `index.html`): sections (intro / split / full / cta) by word index; glass
   Before/After opening; split = glass motion graphics top + face bottom + seam caption; full = face + script/Anton
   captions; CTA box; transitions; captions (ROMAN map to Latin-script Hinglish, name fix); optional text hook
   (`HOOK=1` / `HOOK=2`); writes `plan/sfx_events.json` (sound moments).
9. **Check motion timing:** short-lived elements enter faster so exits land (`d = min(d, max(.2, t1 - t0 - .3))`); no
   element over the seam caption (overlap check script); big full-frame words never on fillers (FUNC list, merge
   filler-only chunks, shrink to fit 880 px).
10. **Music bed** (`build/music_bed.py`): track from 0:46 (45.95 s, downbeat) to 2:12.12, then from 0:45.95 again; each
    piece cut to its own file first, then 80 ms tri crossfades; 1.2 s fade-out; 48 kHz.
11. **SFX cue sheet** (`build/sfx_sheet.py`): sound moments mapped to CC0 OGA files by kind (whoosh_big, boom, whoosh,
    swish, shimmer, hit, pop max one per 0.7 s, notify, cash, stamp, riser_hit).
12. **Render** (detached): HyperFrames `render --quality draft -w 3` for previews, `--quality delivery -w 3` for finals.
13. **Mix and encode** (`render_final.sh`): voice `loudnorm=I=-15:TP=-2:LRA=9`, `apad=whole_dur=107.5`; music -19 dB,
    `sidechaincompress=threshold=0.04:ratio=5:attack=15:release=320` keyed by the voice; amix, `atrim=0:107.5`,
    `afade=t=out:st=106.2:d=1.3`; x264 preset slow CRF 18 `-maxrate 6.8M -bufsize 13.6M` profile high yuv420p, AAC 320k,
    `+faststart`.
14. **SFX mix:** real-sfx `scripts/mix.py` on the cue sheet -> `<name>_sfx.mp4` plus cue report and resolved cues.
15. **Verify:** ffprobe size / duration / fps; loudness (-14.8 LUFS, TP -3.0 dBTP); **look at frames of every final**
    (opening, splits, full frames, CTA) before sending.
16. **Send:** preview (draft) for approval; after approval render the final; deliver the `_sfx.mp4` file with a one-line
    caption (version, specs, what changed). Keep the file under 100 MB.
17. **Record:** commit code/plan (not media), update PROGRESS.md.

## 3. Settings that worked

| Setting | Value |
| --- | --- |
| Silence cut | THRESH -30 dB, MINSIL 0.1 s, KEEP 0.08 s, highpass 90 Hz, 8 ms fades (write `d=0.008`) |
| Speed | 1.1x, pitch kept (atempo) |
| Canvas | 1080x1920, 30 fps |
| Motion | entrances 0.5 s expo.out (rise 90 px, blur 16 px, scale .86, rotationX 18), exits 0.22 s, icon pop back.out(3) 0.35 s, float 1.1 s, stage push 1.06 -> 1.13 |
| Music | from 0:46 (45.95 s), loop 45.95 -> 132.12 -> 45.95, 80 ms crossfades, -19 dB, sidechain ducked |
| Voice | loudnorm I=-15 TP=-2 LRA=9 |
| Final loudness | -14.8 LUFS, TP -3.0 dBTP |
| SFX track | -30.1 LUFS, 75 cues |
| Final encode | x264 slow CRF 18, maxrate 6.8M / bufsize 13.6M, AAC 320k -> 95 MB for 107.5 s |
| Draft encode | x264 veryfast CRF 24, AAC 192k |
| HyperFrames | 0.8.203, `-w 3`, `HYPERFRAMES_NO_TELEMETRY=1` |

## 4. Commands

```bash
# rebuild the cut, the bed and the page
python3 build/tight.py
python3 build/music_bed.py [length_s]   # optional length argument; default 140
python3 build/generate.py               # v4 look (no text hook)
HOOK=1 python3 build/generate.py        # v5 hook 1
HOOK=2 python3 build/generate.py        # v5 hook 2

# renders, always detached
setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
setsid nohup bash build/render_final.sh > /dev/null 2>&1 < /dev/null &
OUT=renders/nxtlvl_surrender-ad_reels_9x16_vN.mp4 setsid nohup bash build/render_final.sh > /dev/null 2>&1 < /dev/null &
setsid nohup bash build/render_hooks.sh > /dev/null 2>&1 < /dev/null &   # both hook versions, log in renders/hooks.log
```

Note: the exact length argument used for `music_bed.py` in the final is not recorded (uncertain); the default is 140 s and
the mix trims to 107.5 s.

## 5. Mistakes, fixes and lessons

| # | Problem | Fix / lesson |
| --- | --- | --- |
| 1 | Word-gap tight cut saved only ~9 s (Scribe word ends run into pauses) | Cut on the audio with silencedetect |
| 2 | ffmpeg `afade d=.008` rejected | Write `d=0.008` |
| 3 | One 50-branch filter graph on the 1080p file was OOM-killed | Encode each piece separately and concat |
| 4 | Picture/sound drift | Cut on whole frames (`round(t*30)/30`, `-frames:v`) and apad each piece's audio to its frame length |
| 5 | Wrong source: the first Drive link was an already-edited v8 9:16 file | Ask for the raw camera file; check resolution and look before using |
| 6 | 720p source made full-frame shots soft (2.7x upscale) | Ask for the 1080p/4K original up front |
| 7 | Drive large-file downloads return a virus-scan HTML page | Follow the form to `drive.usercontent.google.com/download` with `confirm=t&uuid` |
| 8 | "Hope it works" chip lingered on the seam line (stage push moved low elements onto the seam; a short window's entrance outlasted its exit) | Short windows enter faster (`d = min(d, max(.2, t1-t0-.3))`), lowest chips moved up, overlap check script |
| 9 | Big full-frame words landed on fillers ("HAI", "THA", "MAIN", "TOH", "J") | Wider FUNC list, merge filler-only chunks, "J." not a sentence end, shrink-to-fit |
| 10 | Music bed dropped the first piece: trimming one input twice in one filter graph gave a ~23 s bed, so v1-v4 previews had music only for the first 20-30 s | Cut each piece to its own file, then crossfade |
| 11 | CTA hold made the audio end in digital silence at 106.8 s | Pad the voice (`apad=whole_dur=107.5`) |
| 12 | Removing the notch CSS deleted the `#cbefore` rule; first final (95.6 MB) had the Before screen filling the frame | Caught on frame check, restored `#cbefore {left: 50px; top: 760px; width: 380px; height: 676px;}`, re-rendered. Lesson: check frames of every final before sending; make CSS edits with exact unique matches |
| 13 | End-hold still `assets/img/last_full.png` refused for commit ("Out-of-Place Publication") | Gitignored; footage stills stay out of the public repo |
| 14 | Background waiters time out (the v5 waiter was killed at its time limit while the detached render kept going) | Launch renders standalone and detached (`setsid nohup ...`); check the log / file instead of waiting in a background job |
| 15 | [summary] "A detached-frame error came after a pkill; clear chromium/hyperframes processes, then relaunch." | General to renders after a pkill; not specifically observed on this project |
| 16 | Disk at 97% (1.5 GB free) during v5 renders | Deleted `cache/pieces` (565 MB, rebuildable) on 2026-11-12; watch disk before long renders |
| 17 | AskUserQuestion about hook placement was denied by the owner | For client text, use the client's words directly and place them where the client marked |
| 18 | Reference SFX could not be copied exactly (not separable, not licensed) | Recreate the sound grammar with licensed CC0 sounds and tell the owner |
| 19 | Openverse / Freesound downloads refused from the cloud session | Fallback to the CC0 OpenGameArt packs, and say so (house rule) |
| 20 | Cue report: plop_02, click_002, button1, plop_01 used 6 times; tick_001, button2, fantasy_magic_button_1 5 times | Not acted on; vary the sounds next time |

## 6. Delivery rules

- What to send:
  - Previews: draft quality, file `preview_surrender-ad_9x16_vN_sfx.mp4`, caption "Surrender ad vN preview (draft quality,
    m:ss): <what changed>."
  - Finals: delivery quality, file `nxtlvl_surrender-ad_reels_9x16_vN_sfx.mp4` (hook versions `..._v5_hook1_sfx.mp4`,
    `..._v5_hook2_sfx.mp4`), caption with specs (e.g. "Surrender ad final: 1080x1920, 1:47.5, 95 MB.").
  - Send each file as soon as it is ready (v5: video 1 sent while video 2 was rendering).
- Format: MP4, H.264 + AAC, 1080x1920, 30 fps, under 100 MB (owner rule for this client and agency rule).
- How: as files in chat (SendUserFile). No Drive upload of finals found.
- Where stored: `/home/user/Nxtlvl-Social/surrender-ad-9x16/renders/` (not in git; MP4s are never committed).
- Approval: previews first; final only after the owner approves (17:50:33Z message). When the owner asks for full quality
  directly (v5), render in delivery quality straight away, no draft.
- Agency extras that are due but not yet sent: post description (CTA keyword line first, hook, body, up to 5 hashtags,
  SEO line; in `caption.md`), 1-frame cover .png per format, keyword auto-DM block. In the final reply list each file with
  platform, size, duration and path.

## 7. Checklist for the next Kanav video

1. Raw camera file (1080p or better) via Drive; Scribe JSON; confirm name spelling "Kanav".
2. Tight cut + repeats/fillers removed + 1.1x pitch kept.
3. Pink dotted background, glass Before/After opening (no notch), text hook at the top from frame 0 if the client sends one.
4. Black-box white seam captions and script + Anton full-frame captions in Latin-script Hinglish.
5. No name card when he introduces himself; no face pulsing; nothing lingering on the seam.
6. Music: confirm a licensed track first (the Melly Mike licence is unanswered); start point and loop back to the start.
7. SFX: Openverse first, OGA CC0 fallback; vary repeated files.
8. Detached renders; check frames of every final; under 100 MB; -14 to -15 LUFS.
9. Deliver with description, cover and auto-DM block; update PROGRESS.md.
