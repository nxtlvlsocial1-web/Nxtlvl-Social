# Dr S Kokila - workflow, tools and lessons

> Public part of this client's memory: look and workflow only. The brief, feedback, scripts, footage list,
> hooks/CTAs, calendar and open items live in the private `nxtlvl-client-memory` account skill.

How her talking-head reels are made, the settings that worked, and every mistake and fix so far.

**Index**
- [1. Step-by-step process](#1-step-by-step-process)
- [2. Skills and tools used](#2-skills-and-tools-used)
- [3. Settings that worked](#3-settings-that-worked)
- [4. Mistakes, fixes and lessons](#4-mistakes-fixes-and-lessons)
- [5. Delivery rules](#5-delivery-rules)
- [6. Checklist for the next Kokila reel](#6-checklist-for-the-next-kokila-reel)
- Related: [brand-style-guide.md](brand.md), footage-and-assets.md (private memory skill), open-items.md (private memory skill)

*Sources: `scratchpad/notes_kokila.md` §2, §5, §9, §10; `kokila-peace-9x16/build/render_v2.sh`; `/home/user/Nxtlvl-Social/CLAUDE.md`
and `.claude/skills/nxtlvl-social-video/SKILL.md` (read-only).*

---

## 1. Step-by-step process

As used for `kokila-peace-9x16`:

1. **Brief in.** Owner sends the script, the text hook, her raw take (Drive link) and any reference (her reel link, the
   podcast screen recording). Look at reels from a link with `python3 tools/see_link.py URL --ears` (frames, transcript,
   sound timeline).
2. **Plan.** Break down her reference reel; propose the structure (split screen, reference footage, captions, music,
   SFX); flag script lines she did not record, missing CTA, and copyright risks (podcast clips 4 s or less, credited).
   Fact-check claims (sources used: Digit, Notebookcheck, GSMGOTECH, ThePrint; "Temple is reported at about ₹85,000
   (about $1,000), and its brain-blood-flow claims haven't been independently validated yet.").
3. **Download sources directly** (the 303 MB `.mov` was too big for the Drive connector). Keep the 4K original.
4. **Transcribe** the raw take (faster-whisper small.en -> `plan/words_raw.json`). Map the script onto the words; pick the
   clean take of each line (`build/tight.py` LINES).
5. **Tight cut** (`build/tight.py`): speech edges from silencedetect; gap between lines 0.06 s; pauses 0.1-0.18 s
   (proportional, capped); last hold 0.3 s; drop false starts, lip noises, glances; sped 1.08x with pitch kept; cut from
   the 4K original with full -> TV range conversion, lanczos, unsharp; pieces at crf 10 with PCM audio; `tight.mp4` crf 12.
6. **Transcribe every cut piece separately** to catch restarts (Whisper smooths over false starts). Final words ->
   `plan/words_tight.json`, `plan/words_final.json`.
7. **Pick podcast moments** (`plan/podcast_picks.json`), cut once from the original screen recording at panel size, grade
   up the flat picture.
8. **Fetch stock footage** by id with `tools/pexels_fetch.py` (videos.pexels.com, no key); check every clip for the
   client's people rules (Indian people, no religious marks); make vertical full-screen crops from 4K
   (`build/broll_vertical.py`, x264 crf 14).
9. **Compose** in HyperFrames (`build/generate.py` writes `index.html`; `VARIANT=A|B` for the two trial cuts): modes split /
   ref / full, hook box, captions, minimal graphics, zoom-blur transitions.
10. **Music** (`build/music.py`): Openverse track, bed at -19 LUFS, sidechain-ducked; check with earshot.
11. **SFX** (`build/sfx_sheet.py`, `build/sfx_mix.py`): Openverse first; OGA CC0 fallback was used; cue list per cut.
12. **Preview** (draft quality) -> owner / client notes -> repeat. Never render a final before the preview is approved,
    unless the person asks for the final directly (then delivery quality straight away).
13. **Render detached** (`setsid nohup bash build/render_v2.sh > /dev/null 2>&1 < /dev/null &`): per cut generate ->
    music -> picture render -> stop if the render failed -> sound mix with video stream copy -> verify.
14. **Verify**: `verify_mix.py --target -14`, ffprobe (size, duration, fps), frame checks, Whisper on the final (hears every
    word, including Deepinder's).
15. **Deliver** both cuts + cover + post description (one paste-ready block; also saved in `caption.md`). Commit code and
    plans, never media.

## 2. Skills and tools used

| Tool / skill | Used for |
| --- | --- |
| `nxtlvl-social-video` -> `hyperframes` skills | House rules, formats, naming; HyperFrames composition and render (HyperFrames 0.8.203) |
| `tools/see_link.py` (built 2026-11-12 for this job) | Seeing her reference reel from its Instagram link (yt-dlp; frames, transcript, earshot) |
| `tools/pexels_fetch.py` (built 2026-11-12 for this job) | Fetching Pexels clips by id from videos.pexels.com without an API key |
| faster-whisper small.en | Word timings of her take, of each cut piece, of the voice note and of the final |
| ffmpeg (silencedetect, afftdn, compressor, loudnorm, alimiter, asplit, sidechaincompress) | Cut, voice clean-up, echo, music ducking, loudness |
| earshot | Music character / ranking, mix checks ("launch-grade, 23 of 23"), hit density warnings |
| Demucs | Checking the music for vocals (v1 track: vocals -54.6 dB) |
| `openverse-sfx` skill scripts (`verify_mix.py`) | Loudness / true-peak verification |
| Openverse API | Music (Jamendo tracks) and SFX search |
| Playwright (`build/cover.cjs`) | Cover PNG from HTML |
| GSAP (`assets/vendor/gsap.min.js`) | Animation inside the composition |

## 3. Settings that worked

- **Voice:** highpass 80 Hz, afftdn nf -28, compressor threshold -20 dB ratio 3 attack 8 release 120 makeup 2, loudnorm
  -16 LUFS; speed 1.08 (pitch kept).
- **Guest bite:** levelled to -16 LUFS with a measured gain + alimiter 0.7, in three separate passes (dry, echo, mix).
- **Echo:** copies at +0.24 s (vol 0.55, hp 200 / lp 3000), +0.5 s (0.32, lp 2200), +0.78 s (0.18, lp 1500), from the
  start of the last word; ~9 dB under the voice through the black.
- **Music:** bed -19 LUFS; sidechain threshold 0.02, ratio 6, attack 20, release 380; fade in 0.3 s, out 0.8 s.
- **Master:** two-pass loudnorm I=-14, TP=-2, LRA=11 -> -14.0 LUFS, -1.8 / -1.9 dBTP.
- **Render:** `npx --yes hyperframes@0.8.203 render --quality high --video-bitrate 11M --sdr -w 3`; mux with video stream
  copy (AAC 192k, faststart). Result 81-86 MB for ~60 s, under 100 MB without a second encode.
- **Her footage:** cut straight from the 4K iPhone original; `in_range=full:out_range=tv`, lanczos, unsharp 5:5:0.45.
- **Podcast:** cut once from the original recording at panel size; grade brightness 1.42 contrast 1.18 saturate 1.18
  (full screen); `--sdr`.
- **Stock:** 4K sources where available; crop with `force_original_aspect_ratio=increase` + centred crop; slow 1.0 -> 1.08
  push.
- **Wait-loop markers** for detached renders: `^ALL DONE|^GEN . FAILED|^MIX . skipped`.
- Render times seen: v4 A 5m 59.3s, v4 B 13m 32.6s; v2 A 12m 19.4s, v2 B 11m 11.5s.

## 4. Mistakes, fixes and lessons

| # | Problem | Cause | Fix | Lesson |
| --- | --- | --- | --- | --- |
| 1 | v1 music cut off after ~12 s (earshot: "music is heard in only 27% of the film"); soft intro too quiet | Music input used twice without asplit | asplit + two passes, 14 dB intro lift (v1b) | ffmpeg rejects ".6"-style durations; write "0.6" |
| 2 | Her rhythm sounded clipped / mechanical (v1) | All pauses forced to 0.1 s | Proportional pauses; slivers merged (v2) | Keep natural pause length, cap it instead |
| 3 | Clipped word "because" | It came after a 2.5 s pause, later than the transcript said | Cut starts earlier; full "because" restored | Check word edges against the waveform, not only the transcript |
| 4 | Render failed on low disk (0.7 GB free); the mix then ran onto the old v1 master (72.6 s with 5 s dead air) | Render scripts carried on after a failed picture render | Not sent; render scripts now stop when the picture render fails (commit c028187 "render scripts stop when the picture render fails (never mix onto an older master)"); `rm -f` the old master before rendering | Always check the render exit code and that the new master exists |
| 5 | Pexels API keys paused; credential form declined | Pexels stopped issuing keys | Direct file fetch by id from videos.pexels.com (`tools/pexels_fetch.py`), no faking | Owner doesn't want manual downloads |
| 6 | Freesound 403 to the cloud IP (site, API, files); Wikimedia API 429 | Cloud-machine blocks | Never spoof a browser; OGA CC0 fallback (owner's choice) | Current CLAUDE.md: Freesound preview files (`cdn.freesound.org/previews/...`) download fine via the `openverse-sfx` skill's `sfx_fetch.py` - try that first next time |
| 7 | Clip 8416831 came out 720p | `pexels_fetch` SIZES order preferred HD/720 before UHD | Noted in delivery | Prefer UHD first |
| 8 | Blank cream top half at 0:58 (preview v3) | tb14 clip 7223986 media start 7.5 s past usable footage | Media start 6.9 | Frame-check every section |
| 9 | Double take "sometimes the great-" left in (owner 12:19) | False start (raw 141.0-143.0); Whisper smooths over false starts | Dropped; L8 from the clean second take (144.95 s) | Transcribe each cut piece separately |
| 10 | "Many errors in the placement of talking after a frame was cut", head movement / glances between cuts (owner 12:28) | Gaps 0.22 s and loose edges | GAP 0.22 -> 0.06 s, speech-edge trims from silencedetect, pauses capped 0.18 s, last hold 0.55 -> 0.3 s, 0.3 s lip noise dropped | Only her speaking; nothing between words |
| 11 | Seam line showed over Deepinder's full screen | Always-on seam | Hidden until the split | |
| 12 | Hook text over Deepinder's full screen (owner 12:37) | Hook placed at 0:00 | Moved to the split screen after the black | Hook never over the celebrity clip |
| 13 | Deepinder's line silent in final v1 (owner 12:50) | loudnorm inside asplit on a 2.6 s clip gave a silent dry branch (measured -180 dB from 0 to 2.25 s; only the echoes from 2.5 s on) [summary] | Three separate passes with a measured gain; Whisper confirms his words in the final | Listen to / measure every branch; verify the final with Whisper |
| 14 | Quality loss in final v1 ("both of the videos and talking head quality decreased") | 1080 working-copy generation chain; uncorrected full-range iPhone source; podcast clips downscaled then upscaled; crf 19 re-encode to fit 100 MB; HyperFrames' JPEG frame extraction | Cut from 4K with range conversion; podcast clips at panel size; render once at 11 Mb/s; no second encode | PNG frame extraction would need ~10 GB temp disk (not available) |
| 15 | Voice drifted ~1 s over 50 joins | AAC audio in cut pieces | Pieces carry PCM audio | |
| 16 | HDR pre-extraction needed 4.6 GB | HDR path | `--sdr` | |
| 17 | Render cancelled when launched chained | Parent shell exited | Launch fully detached with `setsid nohup` | House rule: never a time-limited background job |
| 18 | Wait loop reported a false finish | It matched "skipped" in the render trace log | Exact markers `^ALL DONE|^GEN . FAILED|^MIX . skipped` | |
| 19 | Vertical crop failed on 1080x2048 clips | Fixed crop maths | `force_original_aspect_ratio=increase` + centred crop | |
| 20 | Disk full repeatedly; git push 503 | Large masters, caches, UHD sources | Deleted masters, caches, unused clips, UHD sources; push retried with backoff | Earlier deliveries are gone from disk as a result |
| 21 | Religious marks slipped in | Hijab in 8135467; bindi in family clips; turban in 4334053 | Replaced / cropped | Check every frame of every stock clip for religious signs |
| 22 | earshot "salient hit density 2.0/s, high" | Tight cut + whoosh on every quick footage cut | Whooshes removed from quick footage cuts | |
| 23 | verify_mix "VERDICT: NEEDS FIX" on every render | Its fixed -4 dBTP rule vs our -2 dBTP master | Accepted at the -2 dBTP house ceiling | Known false alarm |
| 24 | Copyright risk | Reference reel used celebrity photos / TV / film clips | Not copied; podcast clips short and credited | |
| 25 | Unrecorded script lines | Script and take differ | First as on-screen text, then removed (owner) | Only her spoken lines |

## 5. Delivery rules

- **What to send:** both trial cuts (when the opening can work two ways), the cover PNG, and the full post description in
  one paste-ready block (no CTA unless given; music credit line; podcast credit line; 5 hashtags; one SEO keyword line; no
  emojis). Say the size, duration and format of each file.
- **Formats:** MP4, H.264 + AAC, 1080x1920, 30 fps, -14 LUFS, true peak about -2 dBTP, under 100 MB with no second encode.
  Cover 1080x1920 PNG inside the 3:4 grid crop (y 240..1680).
- **Names:** `nxtlvl_kokila-peace_reels_9x16_v<N>_deepinder-open.mp4` / `_direct-open.mp4`; cover
  `nxtlvl_kokila-peace_reels_9x16_v1_cover.png`; previews `preview_kokila-peace_reels_9x16_v<N>.mp4`.
- **Where files are stored:** `/home/user/Nxtlvl-Social/kokila-peace-9x16/renders/`. Only the **v4 cuts and the cover**
  remain on disk:
  - `/home/user/Nxtlvl-Social/kokila-peace-9x16/renders/nxtlvl_kokila-peace_reels_9x16_v4_deepinder-open.mp4`
  - `/home/user/Nxtlvl-Social/kokila-peace-9x16/renders/nxtlvl_kokila-peace_reels_9x16_v4_direct-open.mp4`
  - `/home/user/Nxtlvl-Social/kokila-peace-9x16/renders/nxtlvl_kokila-peace_reels_9x16_v1_cover.png`
  Earlier previews and finals were deleted for disk space. Description: `kokila-peace-9x16/caption.md`.
- **Git:** code, plans and caption.md committed (branch `claude/console-skill-reel`); media gitignored (footage/,
  assets/audio/, renders/, cache/, sfx/, assets/video/). Never commit MP4s.
- **Credits:** music CC BY 3.0 credit required in the post; SFX CC0 (no credit); Pexels no credit required; podcast
  credited on screen and in the post.

## 6. Checklist for the next Kokila reel

1. Get the original phone file (not a WhatsApp copy), the script, any clips and where they go, and CTA keyword or "no CTA".
2. Text hook held 5-6 s on the split screen, red text on a white box; subtitles royal-blue pill with yellow keywords.
3. Reference footage full screen most of the time; her full screen / split only now and then.
4. Stock clips: Indian people only (or no faces), nothing religious (no hijab, bindi, turban, cross); frame-check each.
5. Calm music (solo piano worked); Openverse CC0 / CC BY only, credit CC BY; SFX from Openverse first (try Freesound
   previews via `sfx_fetch.py`), OGA CC0 as fallback.
6. Only her clean spoken lines; no glances, no false starts, no end gap; transcribe each piece separately.
7. Two trial cuts if the opening can work two ways (guest clip first vs her first). Guest clip: audible line full screen,
   instant black, echo on the last word, hook after the black.
8. No repeated number on one screen; minimal animation.
9. Cut from the 4K original; render once at 11 Mb/s with `--sdr`, detached; scripts stop if the render fails; under
   100 MB.
10. Verify with verify_mix, ffprobe and Whisper; check the house 9:16 safe zones; make a matching cover.
