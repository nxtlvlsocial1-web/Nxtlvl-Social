# Workflow and skills: Creedom and Creators 100X reels

Knowledge export for Nxtlvl Social. How the Creedom (creedom.ai, mascot Cree) and Creators 100X (@creators.100x) reels
are made, from idea to delivery: the steps, tools, skills, AI models, the settings that worked (copied from the build
scripts), the mistakes and the owner's lessons. Written 2026-11-17.

## Index

1. [Pipeline at a glance](#1-pipeline-at-a-glance)
2. [Brief and page check](#2-brief-and-page-check)
3. [Script: story arc, options, approval](#3-script-story-arc-options-approval)
4. [Voice](#4-voice)
5. [Edit: HyperFrames compositions written by Python](#5-edit-hyperframes-compositions-written-by-python)
6. [Footage and images](#6-footage-and-images)
7. [The mascot Cree](#7-the-mascot-cree)
8. [Sound: music, SFX, mix, loudness](#8-sound-music-sfx-mix-loudness)
9. [Review: draft render, preview, feedback loop](#9-review-draft-render-preview-feedback-loop)
10. [Final render](#10-final-render)
11. [Cover](#11-cover)
12. [Post description](#12-post-description)
13. [Auto-DM](#13-auto-dm)
14. [PDF lead magnets](#14-pdf-lead-magnets)
15. [Delivery rules and where files live](#15-delivery-rules-and-where-files-live)
16. [Tools, skills and AI models](#16-tools-skills-and-ai-models)
17. [Brand looks](#17-brand-looks)
18. [Mistakes, fixes and lessons learned](#18-mistakes-fixes-and-lessons-learned)
19. [Known costs](#19-known-costs)

Conventions: quotes are verbatim (typos kept); times UTC; "UNKNOWN" = not in any source; "UNCERTAIN" = inferred.
Repo: `/home/user/Nxtlvl-Social`. *Sources: CLAUDE.md, .claude/skills/nxtlvl-social-video/SKILL.md, the build/
folders named below, scratchpad/notes_chat.md, notes_creedom_files.md, notes_c100x.md.*

---

## 1. Pipeline at a glance

1. Brief from the owner (often with a screenshot, screen recording or reference reel). Confirm the page (Creators 100X
   vs NXTLVL) and the brand look.
2. Start from the `nxtlvl-social-video` skill, then `/hyperframes` routing.
3. Write two or three script options on the modern story arc, each line labelled with its beat, with a visual plan and
   the facts that need confirming. The owner picks one ("Go with option A ...", "Okay perfect start making").
4. Voice: Kokoro af_heart (house voice), Chatterbox with a Kokoro reference (more expressive), or an ElevenLabs take
   (mood-bracket script; the owner can record it himself). Pick takes with faster-whisper, write word timings.
5. Edit: a Python generator writes the HyperFrames composition (`index.html` with one paused GSAP timeline) plus
   `plan/edit.json` and `plan/sfx_events.json`, timed to the word timings and the music's beat grid.
6. Sound: Openverse music (CC BY) and SFX (CC0 / CC BY), mixed by `build/sfx_mix.py`: voice on top, music
   sidechain-ducked, SFX peak-normalised, master -14 LUFS.
7. Draft render (detached), send the preview, take notes, repeat. Never render the final before approval.
8. Final render in delivery quality (detached), then the mix and `verify_mix.py`.
9. Cover PNG from the composition (Playwright), post description in one block, auto-DM block, PDF if the keyword sends
   one.
10. Deliver: MP4 + cover + description (+ auto-DM, + PDF), all in the chat. MP4s stay out of git.

---

## 2. Brief and page check

- **Which page.** Creators 100X: "basically this page is made to provide day to day ai helping tools prompts hacks or
  guides, repos etc" (2026-11-12 15:25). Audience: "beginner creators that want to use ai" (2026-11-15 10:17), plus
  students (STUDY). Creedom feature reels go on Creators 100X: "it will be posted on Creators.100x but it is based on
  Creedom's feature" (2026-11-13 03:28). GTA content goes to AI.NXTLVL, not Creators 100X: "Okay, so this video is not
  supposed to be made under the creators 100x page. It's basically for ai.nextlevel" (2026-11-12 17:17).
- **Platform format** (nxtlvl-social-video §2): Instagram Reels 9:16, 1080x1920, length target 7-30 s (max 60 s),
  "30 fps unless the brief says otherwise". In practice: 23.5-38.5 s, 30 fps; the Creedom explainer at 37 fps (owner's
  choice).
- **Brand kit** (nxtlvl-social-video §1-4): load `brands/<client>/`. Creators 100X: `brands/creators-100x/` (brand.md,
  PNG logos, Inter fonts, PDF maker). Creedom has no brand folder; its look lives in the project generators (see §17).
- **Social rules** (nxtlvl-social-video §3, verbatim): "Hook in the first 1.5 s. The first frame must already show the
  subject or the headline — no slow fade-in from black, no logo-first intro." / "Safe zones for 9:16: keep text, faces
  and logos out of the top 250 px and the bottom 400 px (platform UI: username, caption, buttons), and 60 px from each
  side." / "One message per video. End on a clear CTA card (follow, link in bio, shop now) held ≥ 1.5 s." / "Captions on
  by default." (Exception: the owner removed the bottom captions on the Creedom explainer: "remove the bottom captions
  cause they do feel uneccesary", 2026-11-10 14:00. The reels show the spoken words as headlines instead.)

---

## 3. Script: story arc, options, approval

### 3.1 The arc (CLAUDE.md rule and nxtlvl-social-video §3a, verbatim)

> Write every video script on the modern story arc (`nxtlvl-social-video` § 3a): hook at 70 dropped mid-story, first
> peak (contrast, contrarian take or shocking stat) by 5-15 s, then peak, release, peak, release, ending on the CTA.

> 1. **Start at 70, not 0 (0–5 s).** The hook drops the viewer into the middle of a story that has already started: no
>    setup, no intro, no "today I'll show you".
> 2. **First peak at 90 (by 5–15 s).** A contrast moment, a contrarian statement or a shocking stat: the first hit of
>    dopamine.
> 3. **Release, then peak again.** Short release beats (context, the how) between peaks, then "boom", the next peak (a
>    reveal, a twist, a surprising capability). Peak, release, peak, release, until the video is done. No single climax
>    in the middle: stack mini peaks and re-hook as long as you can.
> 4. **Close on the CTA** (the keyword line, e.g. Comment "STORY" and I'll send it to you) with the value of what they
>    get, straight after the last peak.
> When presenting a script, label each line with its arc beat (hook 70, peak, release, CTA) so the person can see the
> shape.

Owner origin of the rule: 2026-10-30 06:59:02 "Use this formula to make script first" (reference video attached);
06:59:23 "And remember to follow this arc from now".

### 3.2 How options are presented

- Two or three options with time, beat, voiceover and visual per line, one marked "recommended", plus "Facts to confirm
  with the owner before building". Example: `creedom-write-script-9x16/plan/script_options.md` (A "The blank screen",
  B "Stop asking ChatGPT for scripts", C "Which one did I write?").
- Approval wording seen: "Okay perfect start making" (CHECK, 2026-11-13 03:42); "Go with option A and every single
  visuals ideas in this reel that you mentioned, yeah your 2nd assumption is correct" (2026-11-17 11:13); "Go with the
  first idea and B visual style" (2026-11-15 10:38); "Go with the STUDY manga idea, write the script" (2026-11-12 22:07).
- Creators 100X scripts start from a problem: "the script and hook should be based on the logic of people's problem they
  face and how we can provide a solution based on it" (2026-11-12 15:25).
- Length that worked: about 75-110 spoken words for 23-38 s.

### 3.3 Script rules learned (owner, verbatim)

- Hooks must sell the product's unique point: "No these dont hooks dont emphasize on the fact that there is an app that
  can rate your video before you post" (2026-11-13 03:40).
- Claims must be true: "But when does instagram tells your reel flopped?" (2026-11-13 03:35). Only real features; the 3D
  guide adds "Don't claim guaranteed views, virality or follower numbers. Any score or view count in the story is shown
  as an example, never as a promise."
- No GTA in Creedom reels: "Na make the script better and also dont include the gta aspect" (2026-11-13 03:32).
- Wording edits (2026-11-17 14:59): "Not one fit -> Not one worked", "off the rack -> off the shelf", "@writescript need
  not be spoken out loud" (show commands on screen, don't say them).
- The hook must work on the viewer: "if we're using the topic of making the hook strong, why are we not applying this to
  ourselves, try something miraculous in the first 6-7 seconds that really feels like " whoa what is happening in this
  reel"" (2026-11-11 10:08); "pls make the hook more engaging people may skip that" (2026-11-15 11:34).
- Illustrative numbers (4.2/5, "40 scripts", "200 views") are labelled "EXAMPLE REEL" on screen or noted as
  illustrations in caption.md.

---

## 4. Voice

### 4.1 Which voice when

| Voice | Where used | Status |
|---|---|---|
| Kokoro-82M `af_heart` (hexgrad, Apache 2.0, local) | reel-flop v13, STUDY v2, CHECK, prompt reel, Riya, @write-script v1 | **House voice for Creators 100X**: "Kokoro af_heart is the Creators 100X voice." Approved by the owner on reel-flop v13. |
| Chatterbox (Resemble AI, MIT, local CPU) with a 10 s Kokoro reference clip for the timbre | reel-flop v1-v12 (af_heart ref), STUDY v1 (am_michael / am_puck ref, rejected), @write-script v2-v3 (af_bella ref) | Use when more emotion is wanted; it sounded "weird" once sped up with atempo. |
| ElevenLabs "Hallie - Fun, Young & Feminine" (jpICOesdLlRSc39O1UB5), eleven_v3 | Creedom explainer | 2 takes at 654 credits each; take 1 used. |
| ElevenLabs "Nota 3" (rTMkoe3NzNrEOgFeBwY2), Eleven v3 | Creedom Reel Analyser (October) | Settings: Stability "Natural", 3-4 takes, speed up 1.05-1.1x if over 35 s. |
| ElevenLabs "Blondie - Conversational", the owner's own take (file says eleven_v4) | @write-script v4 final | The owner generated it from our mood-bracket script and uploaded the MP3. |

Owner tone requests (verbatim): "Use a very expressive female open source voice that has emotions in every word she
speaks" (2026-11-11 09:16); "Fix the voicover it got a bit weird try to make it more expressive" (2026-11-12 07:41); "Im
saying the voiceover done in the video is feeling weird fix that make it natural use voicestudio repo if needed"
(2026-11-12 08:35); "the voiceover looks bad" (STUDY v1, 2026-11-13 02:48); "change the voiceover style, like make it
more expressive" (2026-11-17 12:24); "give me a good expressive voiceover script of an female from elevenlabs with
moodbrackets" (2026-11-17 14:57). Language: English only for both brands.

### 4.2 Kokoro af_heart (exact code)

Run: `HF_HOME=/root/tts/hf HF_HUB_OFFLINE=1 /root/tts/.venv/bin/python build/vo_kokoro.py`

```python
pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
text = ln["text"].replace("Creedom", "[Creedom](/kɹˈidəm/)")   # say CREE-dum
audio = np.concatenate([np.asarray(a, dtype=np.float32) for _, _, a in pipe(text, voice="af_heart", speed=sp)])
sf.write(path, audio, 24000)
```

- Two takes per line at two speeds, no time-stretch. Speeds used: reel-flop v13 (1.06, 1.14); STUDY v2 (1.1, 1.18);
  CHECK v5 1.18, v6 (1.28, 1.34) "about 1.12x the v5 takes (1.18)" after "it still feels very slow". The prompt and Riya
  reels pass VOICE and SPEED on the command line (`vo_kokoro.py VOICE SPEED OUTDIR [ids]`); the speed used: UNKNOWN.
- Pronunciation fixes: IPA override `[Creedom](/kɹˈidəm/)` (Kokoro); "Cree-dum" spelling (Chatterbox, ElevenLabs);
  "manga" as MAHNG-guh with explicit phonemes (STUDY, after "But she is pronouncing manga wrong"). Kokoro dropped the
  "-ed" in "turned", so the STUDY hook became "I made ...".
- *Sources: creedom-check-9x16/build/vo_kokoro.py, creators100x-prompt-9x16/build/vo_kokoro.py.*

### 4.3 Chatterbox with a Kokoro reference (exact settings)

- Reference: 10 s of Kokoro speech (af_heart, af_bella, ...) saved as `ref_*.wav`: "a synthetic voice, nobody real is
  cloned". af_bella reference text: "Okay, so here's the thing nobody tells you about posting every day. It's not the
  editing. It's the blank page. And honestly? I used to stare at it for an hour." (speed 1.05).
- `m = ChatterboxTTS.from_pretrained(device="cpu")`; per line
  `m.generate(text.replace("Creedom", "Cree-dum"), audio_prompt_path=REF, exaggeration=min(1.25, ex + dex), cfg_weight=cfg, temperature=temp)`.
- Exaggeration per line set by the arc beat (peaks hotter, releases calmer), e.g. @write-script v2: hook .85, peak 1.0,
  release .6, turn .75, peaks .9, smile 1.0, CTA .75. reel-flop: 1.1, 1.0, 0.6, 0.7, 0.95, 0.6, 0.7, 0.85, 0.7, 0.6, 0.8,
  0.7.
- Takes (seed, extra exaggeration, cfg_weight, temperature): @write-script v2 three takes (7, 0, .4, .8), (23, .15, .32,
  .85), (61, .25, .3, .9). reel-flop v12 four takes (11, 0, .35, .8), (29, 0, .35, .8), (41, .2, .3, .85), (53, .2, .3,
  .85), after `m.prepare_conditionals(REF, exaggeration=.6)`.
- What went wrong: v4-v12 of reel-flop "spoke every line with Chatterbox cloning a synthetic reference, pushed to high
  emotion, then sped up 15 % with atempo: that chain is what sounded off." Fix: Kokoro af_heart spoken directly, no
  atempo.
- *Sources: creedom-write-script-9x16/build/vo2.py, reel-flop-9x16/build/vo.py, reel-flop-9x16/build/vo_kokoro.py.*

### 4.4 ElevenLabs with mood brackets

- Script format (plan/elevenlabs_vo.md, @write-script v4), tags used: [frustrated sigh] [deadpan] [sarcastic]
  [exasperated] [softly] [curious] [playful] [intrigued] [upbeat] [laughs] [excited] [building energy] [proud]
  [delighted laugh] [warmly] [confident]. The full script is in content-calendar.md §4.11.
- Settings handed to the owner (verbatim): "Model: Eleven v3 (the audio tags only work on v3)." / "Stability: Creative
  for the most emotion, or Natural if a take overacts." / "Voice: a warm, young female narrator. The Creedom
  reel-analyser script used "Nota 3" (rTMkoe3NzNrEOgFeBwY2)." / "Make 3 or 4 takes and keep the best one. If the take
  runs over 35 s, speed it up 1.05x to 1.1x in the edit." / ""Cree-dum" is spelled that way so the voice says Creedom
  right." (The owner's file name says eleven_v4.)
- Explainer (Hallie): voice search brief "Pick a warm, upbeat young female creator voice for an Instagram explainer reel
  voiceover"; other candidates "Laura - Enthusiast, Quirky Attitude" (FGY2WhTYpPnrIDTdsKH5), "Emotional Expressive
  Alexis" (FCdKzv68Ofr4VUDcZXIy), "Haley Maven - Social Media Bestie" (S9NKLs1GeSTKzXd9D0Lf). Prompt tags "[excited] ...
  [impressed] ... [cheerful]". Take 1 tightened from 39.16 to 35.43 s by `build/vo_tight.py`: pauses over 0.28 s cut,
  `loudnorm I=-16 TP=-1.5 LRA=9`, 48 kHz mono. Word timings from ElevenLabs Scribe (eleven_scribe_v1, 0 credits).

### 4.5 Take picking and word timings (faster-whisper)

`build/vo_pick.py` (copied between projects), run `/root/tts/.venv/bin/python build/vo_pick.py` with `HF_HOME=/root/tts/hf`
and `VO_TAKES=<takes dir>`:

- `WhisperModel("Systran/faster-whisper-small.en", device="cpu", compute_type="int8")`,
  `transcribe(path, word_timestamps=True, language="en", beam_size=5, vad_filter=False)`.
- Score per take: 1) words wrong against the script (word error count; numbers normalised, e.g. "forty" = "40"); 2) then
  the more expressive take: wider pitch range (5-95 % F0 spread, librosa pyin 80-600 Hz). A spread over 300 Hz is a
  squeak and counts as a slip.
- Trim each chosen take from 0.04 s before the first word to 0.12 s after the last, 12 ms fades; pause after each line by
  beat (e.g. 0.35 s after peaks, 0.3 s elsewhere, 0 after the CTA); LEAD 0.04 s of silence at the start.
- Polish chain:
  `atempo={TEMPO},highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2,loudnorm=I=-16:TP=-2:LRA=9`,
  48 kHz mono -> `assets/audio/vo.wav`. TEMPO defaults to 1.04 (env `VO_TEMPO`).
- Outputs: `plan/words.json` (word times with the script's spelling), `plan/vo_pick.json` (scores).
- Owner's own ElevenLabs take (`build/vo_el.py`): faster-whisper word times split into lines by the script's word counts;
  chain `adelay=60:all=1,apad=pad_dur=0.4,highpass=f=80,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80:makeup=1.5,loudnorm=I=-16:TP=-2:LRA=9`.
- Prompt and Riya reels: `build/vo_assemble.py` trims each line (threshold 0.008), lays lines out with scene gaps (e.g.
  p00 .3, p01 .35 ...), maps faster-whisper words onto the approved script words "so captions spell exactly what the
  brief says" -> `assets/audio/vo.wav`, `plan/words.json`, `plan/lines.json`.
- Note: CLAUDE.md says caption timing should come from ElevenLabs Scribe because "local speech models can't download in
  cloud sessions". In practice the models were already cached in `/root/tts/hf` and `HF_HUB_OFFLINE=1` worked.

---

## 5. Edit: HyperFrames compositions written by Python

- **Engine:** HyperFrames 0.8.203, pinned: `npx --yes hyperframes@0.8.203 render ...`, with `HYPERFRAMES_NO_TELEMETRY=1`.
- **Generator pattern:** `python3 build/generate.py` (or `generate2.py`, `generate3.py` per version) reads
  `plan/words.json` (and `plan/lines.json`) and writes `index.html`, `plan/edit.json` (scene times, duration) and
  `plan/sfx_events.json` (sound cues: `{"type", "t", "gain"}`). New versions keep the old generator file and add a new
  one; the docstring at the top records the owner's notes for that version.
- **Composition root:** `<div id="root" data-composition-id="main" data-start="0" data-duration="..." data-fps="30"
  data-width="1080" data-height="1920">`; one paused GSAP timeline registered as `window.__timelines["main"]`
  (`gsap.timeline({paused: true})`). Video clips are `<video>` elements with `data-start`, `data-duration`,
  `data-media-start`. CLAUDE.md: keep HyperFrames' own rules (one paused timeline, no `left`/`top` motion).
- **Timing:** words rise in on their spoken time (`T(word)` looks up the time in words.json); cuts snap to the music's
  half-beat grid: `BEAT = 60 / bpm`, `HB = BEAT / 2`, `snap(t) = round(t / HB) * HB` (CHECK 99.384 bpm; @write-script
  117.45 bpm; prompt reels on the 117.45 bpm grid of their track).
- **Frame 0:** "Sets at t=0 are skipped by cold render workers, so frame-0 visibility goes in CSS." The hook line is on
  screen from frame 0.
- **Text:** words appear only when spoken (owner, 2026-11-11 00:34: "Animate this in a way they only appear when it's
  spoken not every word already there before even spoken"). Explainer: words rise from masks with a vertical SVG motion
  blur (stdDeviation "0 18" -> 0), accent words in the brand gradient with an elastic punch. CHECK: "Type blurs into
  focus word by word" (blur 14 px, y 26). Fixed line breaks so headlines never re-wrap.
- **Layout grid (CHECK v4, after "Look at all these alignment issues"):** "headline block 190-470, hero band below it,
  everything centred on x=540 or on clean columns, nothing in the bottom caption zone (y > 1610) and no element covering
  another"; phone 540x960 at (270, 520) scale .78. Explainer v3: headline band y 230-620, stage y 630-1170, Cree in his
  own spot.
- **Glass recipe (Creedom):** "Every object is frosted glass (backdrop blur + saturate, white highlight edge, inner glow)
  that tilts slowly in 3D and catches a moving specular shine." CSS: gradient rgba(255,255,255,.62) -> (.22), backdrop
  blur 26px saturate 1.7, 1.5 px white border at .85, inset highlight.
- **Transitions used:** whip pans (0.3-0.38 s, 24 px blur), punch-ins (scale 1.055 + glass flash), liquid-glass morphs,
  frosted sweeps, zoom-throughs, light streaks, liquid blob wipe, glitch hits (RGB split); @write-script v2+: fabric swipe,
  fitting-room curtain, tape-measure wipe, scissor cut; Riya: stop-motion eases stepped to 12 fps with a 1-2 degree boil.
- **Checks and snapshots:** nxtlvl-social-video §5: "`npx hyperframes check` must pass" and "Open `npx hyperframes
  preview --background`, give the person the URL, and wait for approval." Whether `check` was run on every version is not
  recorded in the build scripts (UNCERTAIN). In practice frames were grabbed at key times into contact sheets (scratchpad
  `*_sheet.jpg`, `d_*.png`, `e_*.png` files) and looked at before sending; previews were sent as rendered MP4s, not
  Studio URLs.
- **HDR:** phone recordings must be tone-mapped to SDR first (nxtlvl-social-video §5:
  `ffmpeg -i in.mov -vf "zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0:peak=4,zscale=t=bt709:m=bt709:r=tv,format=yuv420p" -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:v libx264 -crf 17 out.mp4`).
  The explainer nearly rendered HDR because "The app screen-recording clips still carried the phone's HDR colour tags";
  fixed by tagging the clips BT.709. Final renders of the prompt and Riya reels add `--sdr`.

---

## 6. Footage and images

- **Owner's app recordings:** iPhone 1320x2868 (or 1320x2140), recorded dimmed. `creedom-explainer-9x16/build/clips.py`:
  `setpts=PTS/{speed},fps=30,format=rgb24,lutrgb=r='clip(val*2.02,0,255)':g=...:b=...` (brightened x2.02), scaled
  660x1434, top 100 px painted #FDFDFD to hide the status bar, `-color_primaries bt709 -color_trc bt709 -colorspace bt709`.
  Owner: "crop the notch part just build a separate notch dont add my notch from the recording just add a clean notch with
  no other time details" (2026-11-10 11:39).
- **Demo footage must not loop:** "the dummy video you have used just loops for those few frames make sure there duration
  is a lot more then those few frames" (2026-11-13 04:14). CHECK v3 built a 30 s demo reel from Pexels clips.
- **Stock video:** Pexels via `python3 tools/pexels_fetch.py OUT_DIR ID [ID ...]` -> `OUT_DIR/<id>.mp4` and
  `OUT_DIR/pexels.json`. It tries the public file names on videos.pexels.com with plain HEAD requests ("nothing is
  faked"); find ids with a web search restricted to pexels.com. Licence: free for commercial use, no credit. Used: 9384669,
  5075214, 7234061.
- **Creedom app UI:** rebuilt in HTML from the owner's screenshot (cream background, "How can Cree help?", chips, START
  SOMETHING cards, pink-bordered input) so it stays sharp. Owner: "Just show the exact UI of that screenshot that I send
  you and animate it accordingly" (2026-11-17 13:00).
- **Images:** STUDY used the owner's real ChatGPT manga output, Canva for the timeline and mind map ("Canva was on a
  credit cooldown" for the rest), and code-drawn diagram and revision sheet (`build/results.cjs`). Everything else
  (people, robot, props, phones) is drawn in code.
- Downloaded reels are references only, never reused (CLAUDE.md).

---

## 7. The mascot Cree

- **Use only the 13 3D poses** generated from the owner's mascot image: stand, walk + pass (2-frame walk), wave, point,
  present, cheer, shock, sad, mag (magnifier), phone, think, proud. Files: `creedom-explainer-9x16/assets/img/poses/*.png`
  plus `plan/poses.json` (boxes, eye ellipses and lid colours for blinks). Copies in the CHECK and @write-script projects.
- **How they were made (2026-11-10):** ElevenLabs image edit, model "gpt-image-2.5-sunburst", 2 generations per pose,
  reference = the owner's mascot flattened onto white (uploaded through Adobe because the ElevenLabs upload tool was not
  available), about 486 credits per image. Shared prompt prefix: "Use the reference image as the exact character: ...
  Keep its proportions, colours, materials and lighting identical; do not redesign or stylise it." Suffix: "Full body,
  centred, with empty space around it, on a plain pure white background, with no shadow, no text and no other objects."
  Cut out by `build/poses.py` on one 820x820 canvas, feet on y 800, standing height 600 px; NOBLINK = cheer, proud, shock
  (and pass). Cost about 12,600 credits ("around $2").
- **Rig in code:** pose swap with a small squash (scaleX 1.07, scaleY .9 -> 1, 0.28 s back.out(3)); walk cycle alternating
  walk/pass every ~0.15 s with bob and rock; hops with squash and stretch; blinks (lid ellipse, 0.11 s, open-eyed poses
  only); sweat drop; "?", "!", "...", "!?" and heart bubbles; idle bob and breathing; soft pink shadow.
- **Rejected:** a vector SVG redraw ("No you are changing the art style of it make him exactly like that i sent",
  2026-11-10 10:52); a cut-out puppet with seams (never shown); the flat "bird" puppet from the October reel (rejected
  three times on CHECK).
- **Owner rules (verbatim):** "make him exactly like that i sent"; "Firstly that is not a bird so dont treat him like that"
  (no flapping, no flying; arms used as arms); "when i say the mascot looks bad then it is bad , look how full he looks in
  the previous video make him like that"; "use the Creedum mascot time to time". Keep him off text; judge his quality at
  full render quality (draft renders made him look soft; previews were therefore rendered at CRF 16 "so the mascot stays
  sharp").
- Full mascot reference: `creedom-3d-story/renders/creedom_cree-3d-model-sheet.pdf` and the reference pack ZIP.

---

## 8. Sound: music, SFX, mix, loudness

### 8.1 Rules (CLAUDE.md, verbatim)

> Never use music or images we don't have the rights to; source them through `media-use`.

> Sound effects: always build the SFX library from Openverse first (`api.openverse.org`, licences CC0 or CC BY only,
> never NC, ND or SA; record each sound's title, creator, licence and link, and credit CC BY ones in the post). Then
> mix them with the `real-sfx` skill under the song. Most Openverse sound effects are Freesound files: Freesound's
> site and original-file downloads refuse cloud sessions, but its preview files (`cdn.freesound.org/previews/...`, the
> `audio_url` the `openverse-sfx` skill's `sfx_search.py` returns) download fine, so fetch them with that skill's
> `sfx_fetch.py` (install: `npx "@opendirectory.dev/skills" install openverse-sfx --target claude`). Never fake a
> browser to get around a block. Only when a download is refused, use the CC0 OpenGameArt packs
> (`spin-bout-u-drake/build/oga_sfx.py`) as the fallback and say so.

Owner origin: "Use this to add sound effects / npx "@opendirectory.dev/skills" install openverse-sfx --target claude"
(2026-11-10 14:22); "Can you also add a better background music with the help of openverse which fits the context and
script" (2026-11-10 14:42); "Also also use background music from openverse" (2026-11-11 09:23).

### 8.2 The openverse-sfx skill scripts (`~/.claude/skills/openverse-sfx/scripts/`)

| Script | Job |
|---|---|
| `sfx_search.py --query "whoosh" [--max-results 8]` | Anonymous Openverse search (~200 searches/day), only cc0 / by / pdm from freesound and jamendo. Search each kind once. |
| `sfx_fetch.py --audio-url URL --name NAME --attribution '...'` | Downloads into sfx/ and copies the attribution into credits.txt as is. |
| `sfx_normalize.py` | Normalises a short SFX by measured peak ("Never loudnorm a short SFX"). |
| `beat_grid.py <music> [--out beats.json] [--plot beatgrid.png]` | librosa beat grid with an off-beat lock check on the sub-120 Hz kick. |
| `verify_mix.py final.mp4 [--target -14] [--outdir verify]` | Measures the exported MP4: integrated loudness vs target, true peak below -4 dBTP, cue frames, waveform. |

### 8.3 Music

- Openverse -> Jamendo tracks, CC BY 3.0, credit line inside the post description. Instrumental only: "i dont need
  singing in background it is very distracting, add a music which does not have any singing" (2026-11-11 12:08); vocal
  stem checked with Demucs htdemucs (reel-flop: vocal stem -49 dB).
- Never reuse a track: "change the background music we have already used that" (2026-11-13 04:03). Lesson: "check against
  tracks used before (grep for jamendo IDs)".

| Reel | Track | Jamendo id | BPM / start | Bed level |
|---|---|---|---|---|
| Creedom explainer | "Inspiring Technology" by Soundrider/Dope | UNKNOWN in notes | 172 BPM half-time; video 0 s = track 12.75 s; splice at 31.48 s; low-pass dip 13.2-14.4 s | -20 LUFS, ducked; master -16 LUFS |
| reel-flop | "Future Inspiration" by Soundrider/Dope | 1671033 | 123 BPM; offset 16.312 | -20 LUFS ducked; master -14 |
| STUDY | "Be Happy - FREE MUSIC" by ANtarcticbreeze | 1210892 | from 0:20 | -18 LUFS; master -14 / -1.5 dBTP |
| CHECK | "Ruslan Latypov - Corporate Music" | 1693123 | 99.4 bpm, start 6.037 s | -16.5 LUFS; master -14 / -1.5 |
| Prompt reel, Riya | "Inspiring Ambient Motivation" by Soundrider/Dope | 1670558 | 117.45 bpm, from 8.196 s | -19 -> -24 -> -28 LUFS; master -14 / -2 dBTP |
| @write-script v2-v4 | "Swinging Around" by Daniel Bautista | 2126278 | 117.45 bpm, from 0.58 s | -16.5 -> -21.5 LUFS (v3); master -14 / -1.5 |

Used and dropped: "Hip-Hop 1" by Deff Syndicate (slow), "What Can Do" by Felixjd (vocals), "Down For You (chillout lounge
track 2016)" by Dj Quincy Ortiz (CHECK v2-v5, replaced for pace), original synthesised beds (explainer v1-v7, Reel
Analyser).

### 8.4 SFX

- Freesound preview files fetched through Openverse worked for CHECK, STUDY, @write-script. When previews were refused
  (HTTP 403: explainer, reel-flop, prompt reel), the CC0 OpenGameArt / Kenney packs were used and this was said.
- CHECK / STUDY library (all CC0): whoosh_a qubodup 60026, whoosh_b qubodup 60007, whoosh_deep Kinoton 351256, impact
  Rizzard 559387, stamp mpuffenbarger 683031, lock Rudmer_Rotteveel 536413, riser Rizzard 561207, click benzix2 467951,
  pop jcallison 258269, cash disman 728224, buzzer Loyalty_Freak_Music 407466, notify Rickplayer 530480, screech
  waveplaySFX 233558, shutter roachpowder 170229.
- @write-script v3/v4 (owner: "change the sound effects a little bit"): tailoring sounds; three CC BY 4.0 sounds credited
  in the post ("Sewing machine" by Jagadamba, "Coathanger Clothes Hanger" by dersuperanton, "Sliding Clothes on Rail 2" by
  _MC5_).
- The `real-sfx` skill named in CLAUDE.md: the explainer's `renders/mix_final_cue_report.md` looks like its output
  (UNCERTAIN); the Creators 100X and later Creedom reels were mixed with the project's own `build/sfx_mix.py`.

### 8.5 The mix (`build/sfx_mix.py`, exact values from creedom-write-script-9x16)

Run: `python3 build/sfx_mix.py PICTURE.mp4 OUT.mp4 [--no-music]` (env `SONG`, `SONG_AT`, `MUSIC_LUFS`).

- **Cues:** from `plan/sfx_events.json`; the same kind is skipped if less than 0.12 s after the last one; files rotate per
  kind.
- **SFX prep:** `silenceremove=start_periods=1:start_threshold=-50dB,atrim=0:{max_len},afade=t=out:...,aresample=48000`,
  then gain to a per-kind peak measured with volumedetect. Peaks (dBFS): whoosh -10, whoosh_big -9, swish -13, impact -7,
  pop -12, click -11, tick -17, stamp -7, riser -13, notify -12, snip -11, sew -15, typing -16, sparkle -14 (and so on).
- **Panning:** alternate cues ±0.22 left/right; impact, riser and stamp stay centre (from an earshot critique: "nearly
  mono, pan SFX with the motion").
- **Music bed:** `-ss {SONG_AT} ... afade=t=in:d=0.12,afade=t=out:st={DUR-1}:d=1.0,loudnorm=I={MUSIC_LUFS}:TP=-3:LRA=11`;
  ducked under the voice with `sidechaincompress=threshold=0.03:ratio=5:attack=15:release=300:makeup=1`.
- **Sum:** `amix=inputs=N:normalize=0:duration=longest`, trimmed and padded to the reel length.
- **Master:** two-pass loudnorm `loudnorm=I=-14:TP=-1.5:LRA=11` (measured values fed back, `linear=true`); muxed with
  `-map 0:v -c:v copy -map 1:a -c:a aac -b:a 256k -shortest -movflags +faststart`. Cue log to `plan/sfx_cues_final.json`.
- **Levels in practice:** voice -16 LUFS (loudest layer), bed -18 to -28 LUFS, master -14 LUFS with a -1.5 or -2 dBTP
  ceiling. Creedom explainer: two-pass -16 LUFS / -4.5 dBTP.
- **Verify:** `python3 ~/.claude/skills/openverse-sfx/scripts/verify_mix.py OUT.mp4 --target -14 --outdir renders/verify`.
  It checks true peak against -4 dBTP, so every -14 LUFS final reports "VERDICT: NEEDS FIX" (see open-items.md). Results:
  reel-flop -14.1 / -1.7; STUDY -14.0 / -1.5; CHECK -14.0 / -1.5; prompt -14.0 / -1.8; Riya -14.1 / -1.7; @write-script
  -14.0 / -1.5; explainer -16.0 / -4.4 (PASS).
- **earshot** (installed 2026-11-12 08:11 at the owner's request: "Can you install earshot ,ffpemg and these tools to get
  you ears and eyes") critiques mixes; reel-flop v12b was remixed after it (-14 LUFS, -2 dBTP ceiling, panned effects).
- Owner level notes: "reduce the background music sound" (2026-11-15 11:10), "Reduce it more" (11:34), "also reduce the
  volume of the background music" (2026-11-17 13:00).

---

## 9. Review: draft render, preview, feedback loop

- **Draft render** (`build/render_draft.sh`), always detached:
  `setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &`
  - @write-script / CHECK style: `npx --yes hyperframes@0.8.203 render -w 3 -o renders/master_draft.mp4` (default "looks"
    quality, CRF 16, "so the mascot stays sharp"), then `python3 build/sfx_mix.py renders/master_draft.mp4
    renders/<name>_draft.mp4`.
  - Prompt / Riya style: `PREVIEW=1 python3 build/generate.py`, then `render --quality draft -w 3`, then the mix to
    `renders/preview_<name>.mp4`.
  - Each step logs to `renders/draft.log` ("EXIT", "SFX EXIT" / "RENDER EXIT", "MIX EXIT", "ALL DONE").
- **Send the preview** as a file in the chat with a short list of what changed, open questions, and the assumptions still
  unconfirmed.
- **Feedback loop:** the owner reviews on his phone and replies with notes, often with screenshots marking problems. Each
  round becomes a new version (generator docstring records the notes; git commit per version, e.g. "Creedom CHECK reel v4:
  one layout grid, ..."). Rounds so far: explainer v1-v10, reel-flop v1-v13, CHECK v1-v6.1, STUDY v1-v2, prompt v1-v3,
  @write-script v1-v4.
- **Pace check:** when the owner says it feels slow, offer a list of concrete fixes; on CHECK he answered "Go with all of
  them" to: voice 1.12x, a punchier 120-128 BPM track (ended up 99.4 bpm with a strong kick), split score scene, snappier
  transitions, punch-ins on key words, more in-between motion, busier sound, start in motion.
- **Rule:** "Never render a final until the person has approved the preview." Approval wording seen: "Render in final",
  "Go ahead with the final render", "Yeah give me the final render", "Fix this flickering from 0:13 rest give it in the
  final render quality".

---

## 10. Final render

- CLAUDE.md (verbatim): "Run every render detached (`setsid nohup bash <script> > /dev/null 2>&1 < /dev/null &`), never as a
  time-limited background job ... When the person asks for the final export directly, render it in delivery quality
  straight away (no draft first)." Owner origin: "Never do renders in the limited time period remember that and also now
  make the export in final quality i need to post it asap just remember it" (2026-10-29 10:54). A render started as a
  child job died with "render_cancelled_parent_exited".
- `build/render_final.sh` variants actually used:

| Project | Render command |
|---|---|
| @write-script v4 | `npx --yes hyperframes@0.8.203 render --quality delivery -w 3 -o renders/master.mp4` |
| CHECK, STUDY, reel-flop | `npx --yes hyperframes@0.8.203 render --quality high -w 3 -o renders/master.mp4` |
| Prompt reel, Riya | `PREVIEW=0 python3 build/generate.py`, then `npx --yes hyperframes@0.8.203 render --quality high --video-bitrate 11M --sdr -w 3 -o renders/master_final.mp4` ("picture in delivery quality (11 Mb/s)") |
| Explainer v10 | `hyperframes@0.8.203 --quality high -w 3`, 1388 frames, 7 min 26 s |

  Each then runs `python3 build/sfx_mix.py <master> renders/<final name>.mp4` and `verify_mix.py <final> --target -14
  --outdir renders/verify`, logging to `renders/final.log`. @write-script v4: 1154 frames rendered in 3 min 40 s, 38.1 MB
  master.
- nxtlvl-social-video §5-6: verify each file with `ffprobe` (size, duration, fps); MP4, H.264, AAC, under 100 MB. Finals
  so far: 27-51 MB.
- Disk was often low and had to be cleared before renders.

---

## 11. Cover

- Owner rule (2026-10-30 11:40, verbatim): "Make the sure the cover image represents the actual context of video and
  viewers tap on the video to check it out and also make perfect seo description". He asks for it with each final:
  "Send final render with cover page and perfect seo description" (2026-11-17 16:29); "And cover page too" (2026-11-12
  08:54).
- **How (`build/cover.cjs`):** Playwright Chromium opens `index.html` at 1080x1920, waits for fonts, seeks the timeline to
  a strong frame (`window.__timelines.main.seek(4.8, false)` for @write-script), hides the reel's headline, shrinks the
  scene (`#cam { transform: translateY(110px) scale(.86) }`), adds a cover title and a badge, screenshots to
  `renders/<name>_cover.png`. Run: `node build/cover.cjs`. Riya: `python3 build/cover.py` (built from the generator's
  pieces).
- **Framing:** 1080x1920 PNG; everything important inside Instagram's 3:4 profile-grid crop (y 240..1680) and, for Riya,
  the centre 1080x1350 so the 4:5 grid crop keeps it.
- **Pattern that worked:** a short punchy headline (black Inter 800, one accent word in pink or a lime highlighter), the
  hook image (stamp, phone, mascot), and a black pill with the CTA keyword ("COMMENT CHECK", "5 PROMPTS · COMMENT STUDY").
- Covers made: explainer v10, reel-flop v2/v3/v10/v13, STUDY, CHECK, Riya, @write-script v4. Missing: the prompt reel
  (split screen).

---

## 12. Post description

Rules (CLAUDE.md and nxtlvl-social-video §6, verbatim):

> Never use emojis in post descriptions, captions or hashtag blocks we write for clients (number lists with "1.", not
> emoji digits). Plain text only.

> Start every post description with the video's CTA keyword line (e.g. `Comment "AGENT" and I'll DM you my whole
> setup.`), then the hook and the body; don't repeat the CTA further down.

> End every post description with up to 5 hashtags and then one plain line of relevant SEO keywords (the phrases
> people search for the topic, comma separated), and always hand over the full description in one block, ready to paste.

> Every video ships with its full post description in one paste-ready block, in this order: the CTA keyword line, the
> hook, the body (numbered lists as "1.", no emojis), up to 5 hashtags, then one plain line of relevant SEO keywords
> (comma separated: the topic's search phrases, the tools, products or games shown, the platforms). Save it in the
> project's `caption.md` too.

Owner origins: "Never add emojis in descriptions from now on remeber that" (2026-10-27 15:15); "Also remember to start
the description from Cta Keyword decided" (2026-10-27 15:22); "Add some seo keywords after the hashtags which are
relevant" (2026-10-30 11:54); "I mean provide it in a full description and always remember to put them from all videos
next time" (2026-10-30 11:55); "Also give an perfect Seo keywords description and 5 relevant hashtags in small letters"
(2026-11-07 22:28).

Template used for every Creedom / Creators 100X reel:

```
Comment "KEYWORD" and I'll send you <the thing>.

<hook line>

<one or two short body paragraphs; a numbered list "1." "2." "3.">

Save this <reason>.

Music: "<title>" by <artist>, CC BY 3.0
[Sounds: "<title>" by <creator> (CC BY 4.0, Freesound)]

#tag1 #tag2 #tag3 #tag4 #creedom
<10 comma-separated SEO search phrases>
```

- The music credit line is required by the CC BY licence; CC BY SFX are credited too; CC0 needs no credit.
- Hashtags are lowercase; Creedom reels end on #creedom.
- caption.md also holds notes (what is illustrative, voice and licence facts). Every final description is copied in
  content-calendar.md.

---

## 13. Auto-DM

- Rule (CLAUDE.md, verbatim): "The keyword auto-DM (automation) is only the resource link and its setup steps, nothing
  else: no greeting, buttons, comment replies, follow line or caveats. Hand it over as one plain block, or as a PDF when
  the person asks for one."
- Owner origin: "Provide the automation tool setup for it" (2026-10-30 12:04); "Just send me the link of the repo and its
  setup dont add anything else" (12:05); "Remember to always give the automation like this or in a pdf when said"
  (12:06).
- Shape: first line "<Name>: <LINK>" or "Here are your <thing>: <LINK>", then 3 numbered steps. Examples: SCRIPT (Creedom
  link) and PROMPT (PDF link) in content-calendar.md §4.9 and §4.11.
- Placeholders still open: `[CREEDOM LINK]` (CREE, CHECK, SCRIPT) and `[PDF LINK]` (HOOK, STUDY, PROMPT). See
  open-items.md.

---

## 14. PDF lead magnets

- Rule (CLAUDE.md, verbatim): "PDFs (lead magnets, automation resources) are made in the Creators 100X branding with its
  PDF maker: `brands/creators-100x/brand.md` and `make_pdf.cjs` (content JSON in, branded phone-friendly PDF out). Check the
  `--png` page previews before delivering." Owner origin: "make the pdf with this creators 100x branding whenever i say
  to" (2026-11-12 08:57).
- Command: `node brands/creators-100x/make_pdf.cjs brands/creators-100x/pdf/<topic>.json brands/creators-100x/pdf/creators100x_<topic>.pdf --png`
- Content JSON schema (header of make_pdf.cjs, verbatim):

```
// { "title": ["20 HOOKS", "THAT WORK"],      cover title lines; wrap a word in *stars* for hot pink
//   "kicker": "Free swipe file",             small label above the title
//   "subtitle": "...", "tagline": "...",     cover lines under the title
//   "blocks": [                              the pages after the cover, in order
//     { "type": "text", "heading": "...", "intro": "...", "steps": [["title", "body"], ...], "note": "..." },
//     { "type": "cards", "heading": "...", "per_page": 4,
//       "items": [{ "tag": "Result first", "line": "I got [result] in [time]...", "example": "...", "why": "..." }] },
//     { "type": "checklist", "heading": "...", "items": ["...", ...], "closing": "..." } ] }
// In card lines, [square brackets] mark the blanks to fill in (highlighted lime).
```

- Output: 4:5 pages, 1080x1350, Playwright Chromium; cover with logo, kicker pill, big title, pink-dot tagline; every page
  body auto-fitted above the footer (zoom down in 2 % steps, min 60 %); footer logo mark + "Creators 100X" + page number.
  `--png` writes `<out>_p<N>.png` previews (kept out of git by `.gitignore`).
- Naming `creators100x_<topic>.pdf`; no emojis in the copy. Made: 20 Hooks That Work (10 pp), 5 Study Prompts (6 pp), 10
  Prompts That Sound Like You (7 pp).
- Lessons: "Rasterising pages to images avoids iOS rendering bugs" (gradient text showed as boxes on iPhone in an
  AI.NXTLVL guide); "Chromium PDFs drop leading spaces on copy"; the cover's top padding (250 px) "keeps a long title clear
  of the logo" (fixed 2026-11-15).
- Creedom 3D PDFs (guide, model sheet) were built with their own builders in `creedom-3d-story/build/` (`guide.cjs`,
  `model_sheet.cjs`) in the Creedom palette, not the Creators 100X kit.

---

## 15. Delivery rules and where files live

### 15.1 What to send with every reel

1. The final MP4 (H.264 + AAC, 1080x1920, under 100 MB).
2. The cover PNG (1080x1920).
3. The full post description in one paste-ready block.
4. The auto-DM block (or PDF when asked), with the real link once known.
5. The PDF lead magnet if the keyword sends one.
In the reply: each file with platform, size, duration and path (nxtlvl-social-video §6). The owner is on a phone ("Im on
a phone and cant download it there is no option", 2026-11-10 23:54), so keep files small.

### 15.2 File names

- Pattern (nxtlvl-social-video §6): `<client>_<campaign>_<platform>_<aspect>_v<n>.mp4`.
- Creators 100X (including the Creedom feature reels posted there): `creators100x_<campaign>_reels_9x16_v<n>.mp4`, cover
  `..._v<n>_cover.png`, drafts `..._draft.mp4` / `..._v<n>_draft.mp4`, previews `preview_<...>.mp4`.
- NXTLVL-page Creedom reel: `nxtlvl_creedom-explainer_reels_9x16_v10.mp4`. reel-flop also uses `nxtlvl_`.
- PDFs: `creators100x_<topic>.pdf`; Creedom guides `creedom_<topic>.pdf`.
- Project folders: one per video and aspect, `<campaign>-9x16/`.

### 15.3 Where files are stored

| What | Where |
|---|---|
| Projects (generators, plans, caption.md, assets) | `/home/user/Nxtlvl-Social/<project>/` (creedom-reel-analyser-9x16, creedom-explainer-9x16, creedom-check-9x16, creedom-3d-story, creedom-write-script-9x16, reel-flop-9x16, study-manga-9x16, creators100x-prompt-9x16, creators100x-prompt-story-9x16) |
| Rendered MP4s, covers | `<project>/renders/` (MP4s kept out of git: "Keep rendered MP4s out of git; deliver them, don't commit them."; 0 MP4s are tracked) |
| Creators 100X brand kit, PDF maker, PDFs | `brands/creators-100x/` (PDFs and logos are tracked in git) |
| Creedom 3D PDFs and pack | `creedom-3d-story/renders/` |
| Client media (mascot, poses, wordmark) | in the projects' `assets/img/`, kept out of git ("the repo is PUBLIC") |
| Owner uploads | `/root/.claude/uploads/<session>/` (temporary) |
| Google Drive | UNKNOWN for these brands: no Drive folder or link exists for Creedom or Creators 100X. Everything was delivered as chat attachments. Drive uploads from the session failed on size for other projects (10 MB and 4.2 MB connector limits). |
| Other storage (Dropbox, client portal) | UNKNOWN |

---

## 16. Tools, skills and AI models

| Category | Name | Used for | Notes |
|---|---|---|---|
| House skill | `nxtlvl-social-video` | formats, safe zones, arc, naming, delivery | Start here for any video. |
| Video skills | `hyperframes`, `hyperframes-core`, `-animation`, `-cli`, `-creative`, `gsap-*` | composition rules, GSAP | HyperFrames 0.8.203 pinned in the scripts; the CLI says "7 HyperFrames skills out of date or missing". |
| Sound skills | `openverse-sfx` (opendirectory.dev), `media-use`, `real-sfx` (named in CLAUDE.md) | music and SFX search, fetch, verify | See §8. |
| Other skills | No use of `brand-intake` or `canvas-design` is recorded for these brands (no brand.md/MOTION.md from brand-intake exists in these projects) | | |
| Render engine | HyperFrames (`npx --yes hyperframes@0.8.203 render`) | HTML -> MP4 | `-w 3` workers. |
| Animation | GSAP (one paused timeline) | all motion | |
| Browser automation | Playwright Chromium | covers, PDFs, website style read | |
| Audio | FFmpeg (loudnorm, sidechaincompress, amix, volumedetect), librosa (pyin, beats), Demucs htdemucs | mix, take picking, vocal check | |
| TTS (local) | Kokoro-82M (hexgrad, Apache 2.0) voice af_heart (also af_bella, am_michael, am_puck references) | voices | `/root/tts/.venv`, models in `/root/tts/hf`. |
| TTS (local) | Chatterbox (Resemble AI, MIT) | expressive voices | CPU. |
| TTS (cloud) | ElevenLabs eleven_v3 (Hallie, Nota 3), owner's eleven_v4 take (Blondie) | voices | ElevenLabs connector / owner's account. |
| Speech-to-text | faster-whisper small.en (Systran, int8, local); ElevenLabs Scribe eleven_scribe_v1 (explainer) | take picking, word timings | |
| Image generation | ElevenLabs image edit, model gpt-image-2.5-sunburst (flow [flow id removed]) | Cree's 13 poses | Price check also of gemini-3-pro-image and gemini-3.1-flash-image. Adobe asset upload used to pass the reference. |
| Images | Canva (STUDY timeline and mind map) | study images | Canva credit cooldown hit once. |
| Stock | Pexels via `tools/pexels_fetch.py` | demo footage | |
| Music / SFX sources | Openverse -> Jamendo (music), Freesound previews (SFX), OpenGameArt / Kenney CC0 packs (fallback) | | |
| Mix critique | earshot | listening checks | Installed 2026-11-12. |
| Reference viewing | `python3 tools/see_link.py URL --ears` (CLAUDE.md) | reading reference reels | Instagram allows only a few anonymous fetches. |
| 3D | none in-house; "Concept/NxtlvlSocial" workspace (owner's) for 3D renders; Higgsfield image-to-3D offered, not used (0 credits) | | |

---

## 17. Brand looks

- **Creedom:** warm off-white to soft pink background (from creedom.ai), magenta-pink-coral logo gradient
  `linear-gradient(90deg,#F515E8 0%,#F54BA8 50%,#F5876C 100%)`, ink #0B0B0B, accent pink #e0187e; app tokens Paper
  #F6F6F4, Pink #EE688B, Deep pink #B1476B, Mascot pink #F343A2. Frosted liquid glass everywhere. Fonts seen: Fraunces +
  Manrope (from the website), Inter (titles from explainer v6 on), Instrument Serif Italic accents and JetBrains Mono
  labels (CHECK), Google Sans (October reel; which is official is UNCERTAIN). End card: the client's own wordmark image,
  no added star. Owner: "Keep the Creedum background as it is, like that pink type of background" (2026-11-17 13:00).
- **Creators 100X:** `brands/creators-100x/brand.md`: ink #101111, hot pink #FD0B68, lime #CCFB79, background #FDF4F4,
  corner glows lime #CEFB8F and pink #FE70B3; "an off-white page with soft lime and pink glows in the corners, black type,
  one hot-pink accent per line, lime highlighter on the words to fill in, black pills with lime text for labels"; Inter
  800 titles / 700 labels / 600 body, tight tracking (-0.035 to -0.045 em). The hook-reel look (reel-flop, STUDY) uses a
  red-pink-purple gradient (#ff2a2a, #ff3d7f, #d02cff) instead.

---

## 18. Mistakes, fixes and lessons learned

Owner quotes are verbatim with their date (UTC). "Fix" = what was done.

### 18.1 Creedom

| Date | Owner said | Fix / lesson |
|---|---|---|
| 2026-11-10 10:48 | "What i meant was make the cree mascot lively make him walk or change his posture or pose he is in a single pose change that, make him stand on two legs aur move his hands and all and make his face expressive" | 13 poses generated from his image; pose swaps, walk cycle, blinks. |
| 2026-11-10 10:52 | "No you are changing the art style of it make him exactly like that i sent" | Never redraw or restyle Cree; generate poses from the original image only. |
| 2026-11-10 11:39 | "Firstly the text animations on those top texts are really poor it doesnt even feels good and there are many frames that feel cluttered and out of proportion so use the space properly make sure everything is not colapsing on each other also crop the notch part just build a separate notch dont add my notch from the recording just add a clean notch with no other time details and all , videos feels very static in terms pacing there are not much motion elements and animations soo fix that add glass fluid ui type animations" | Layout grid, masked kinetic type, glass UI, clean notch. |
| 2026-11-10 12:16 | "Idk what is in this whole video but it still doesn't feel that engaging" | Rebuilt on the reference promo's grammar ("a new idea every half second to second"). |
| 2026-11-10 12:50 | "Keep the background white/pinkish gradient take the reference from their website rest improve how the font enters on the screen and give that in final export quality" | Website look (off-white to pink, Fraunces/Manrope). Don't drift to dark themes for Creedom. |
| 2026-11-10 12:52 | "Also also try to use the font styles in this website and animate them in a proper order type animation" | Words enter in reading order. |
| 2026-11-10 13:24 | "The starting hook texting,styling and how the text appears feels very dull and basic make it feel premium, take this animation and font style for reference this should be the exact motion tracking for it and keep the video in 40 fps" | iOS picker-wheel hook in Inter. |
| 2026-11-10 13:57 | "Just remove this star from creedom logo" | Never add decorations to the client logo. |
| 2026-11-10 14:00 | "And also change the font style and how these texts comes on screen with this style  preseny in the hook , and also remove the bottom captions cause they do feel uneccesary, keep the above caption type texts as i mentioned give them more glass liquid type of feel" | Titles in the hook's style on liquid glass; no bottom captions. |
| 2026-11-10 14:58 | "In the end just use this font for creedom and also the same color of this image and rest reduce the fps to 37" | Cut the client's own wordmark out of the image; don't retype it. 37 fps. |
| 2026-11-11 00:34 | "Animate this in a way they only appear when it's spoken not every word already there before even spoken so fix that and in many frames starting from hook the video feels dull so improve the colors and different motion elements that look very dull so improve them for whole video find all of those dull parts, improve hook on the basis of elements if it can make viewers stick to the video, dont change font placements in whole video just focus on removing dullness from video and also export it in final quality" | Words only on speech; live retention graph; richer colours; keep placements. |
| 2026-11-13 03:32 | "Na make the script better and also dont include the gta aspect" | No GTA (or other unrelated own content) in Creedom reels. |
| 2026-11-13 03:35 | "But when does instagram tells your reel flopped?" | Check every claim about platforms for accuracy. |
| 2026-11-13 03:40 | "No these dont hooks dont emphasize on the fact that there is an app that can rate your video before you post" | Lead with the product's unique point. |
| 2026-11-13 04:03 | "Remove these bubble things in background it looks like an pimple and why didnt you use the creedom mascot that we made for this, use him and also change the background music we have already used that" | No background spheres; use Cree; never reuse a track. |
| 2026-11-13 04:14 | "Firstly that is not a bird so dont treat him like that and secondly his animations look very bad the last time you made him it was better so fix that and there are many alignment issues in text placements soo fix that, the dummy video you have used just loops for those few frames make sure there duration is a lot more then those few frames" | Arms as arms, no flapping; demo footage long enough not to loop. |
| 2026-11-13 04:26 | "Look at all these alignment issues amd fix them and also the creedom mascor still looks bad he is not in the same quality as previous reel on creedom, and there are still very less glass animations" | One layout grid; more glass. |
| 2026-11-13 05:32 | "No need put the creedom text twice and secondly when i say the mascot looks bad then it is bad , look how full he looks in the previous video make him like that" | Use the 3D poses, never the flat puppet. Show the brand name once. Mistake: we had copied the wrong mascot rig from the October reel ("That was the wrong mascot, and you were right"). |
| 2026-11-13 05:46 | "Now in terms of detailing everything is on point but i have noticed it still feels very slow in terms of pace it could be the background music or less motion graphics and transitional elements or many other animations being less, lemme know some suggestions" | Eight pace fixes, all approved ("Go with all of them"). |
| 2026-11-13 06:12 | "Fix this flickering from 0:13 rest give it in the final render quality" | Chips leave as one group. Check exits for flicker. |
| 2026-11-17 12:24 | "See, this looks like the rebranding or some kind of part 2 of that earlier video we made, and I don't want to do that. ..." | Vary concept, voice, look and footage between Creedom reels. |
| 2026-11-17 13:00 | "Keep the Creedum background as it is, like that pink type of background, ... use the Creedum mascot time to time. Just show the exact UI of that screenshot ... also reduce the volume of the background music." | But keep the Creedom pink background and Cree; the variation is in concept and voice. Music about 5 dB lower. |
| 2026-11-17 14:59 | "0:01-0:03 - can we make the scripts come in front of the person instead of behind them? / 0:03 - Not one fit -> Not one worked / 0:06 - off the rack -> off the shelf / 0:15 - @writescript need not be spoken out loud" | Props in front of characters; plain wording; commands typed on screen, not spoken. |

### 18.2 Creators 100X

| Date | Owner said | Fix / lesson |
|---|---|---|
| 2026-11-11 10:08 | "Everything is fine but if we're using the topic of making the hook strong, why are we not applying this to ourselves, try something miraculous in the first 6-7 seconds that really feels like " whoa what is happening in this reel" so i need that feeling suggest me those ways" | The reel must do what it preaches; cold open with shock value. |
| 2026-11-11 10:23 / 10:44 | "It still does not feel that hooked as an viewer" / "Still feels dull" | More motion from frame 0. |
| 2026-11-11 11:21 | "The whole art style looks weird , go with profesional after effect type of feel for the motion graphics and texts , take this for reference" | Papercraft dropped for professional kinetic type. |
| 2026-11-11 11:45 | "Add some visual representations the video fully consists of just texts and all" | Icons, glass cards, phone, charts. |
| 2026-11-11 12:08 | "Pls change the background music, i dont need singing in background it is very distracting, add a music which does not have any singing just plane music ..." | Instrumental only; Demucs vocal check. |
| 2026-11-11 12:31 | "Remove these shapes that are floating around and try to improve the video in terms of more exciting motion graphic presentations and design" | No floating decorative shapes. |
| 2026-11-11 14:56 | "... make sure the username below should be random in both reels not 07rinx" | Never show real handles in fake UI. |
| 2026-11-11 15:23 | "... make it around 38 seconds and make sure not a single frame feels full in terms of styling and animations and give this video in final quality after making changes here" | |
| 2026-11-12 07:23 | "I feel like the dull intentional video may not be understood by many viewers so can we outplay that and also / And change the losing line - This video already lost you in first three seconds and continue with here are three mistakes killing your views" | Replay payoff; hook rewritten. |
| 2026-11-12 07:41 | "Fix the voicover it got a bit weird try to make it more expressive and find ways where you can add more animations so that it looks more immersive" | Four takes per line, clean-take picker. |
| 2026-11-12 08:35 | "Im saying the voiceover done in the video is feeling weird fix that make it natural use voicestudio repo if needed" | Kokoro af_heart spoken directly; no atempo, no cloning. Became the house voice. |
| 2026-11-12 22:53 | "How bout you use canva to make those images and animate the chatgpt ui interface ... and also take the text styling , pacing animations and other things from the creator 100x reel" | Reuse the approved look across the page. |
| 2026-11-13 02:48 | "The video feels very dull including the voicover there is sooo less animation going on in this video, also the voiceover looks bad" | Something moves at every moment; af_heart. |
| 2026-11-13 03:05 | "But she is pronouncing manga wrong" | Explicit phonemes (MAHNG-guh). Listen for every non-English or brand word. |
| 2026-11-15 11:10 | "But there are few visual elements try to add more of them not a single frame should feel dull and also reduce the background music sound and send it in final quality" | Living background, cursor, stickers, meters, confetti; bed -24 LUFS. |
| 2026-11-15 11:34 | "Reduce it more and pls make the hook more engaging people may skip that" | STOP stamp on frame 0; bed -28 LUFS. |
| 2026-11-15 11:59 | "Cant it be a visual storytelling concept in 2d" | Story-led paper cut-out version (Riya). |

### 18.3 Technical lessons (from the session summaries and scripts)

- HDR phone recordings must be tone-mapped or tagged SDR (BT.709) before they go in a composition.
- "Sets at t=0 are skipped by cold render workers, so frame-0 visibility goes in CSS."
- Freesound refuses cloud downloads of original files; preview files work; when refused, use the OGA / Kenney CC0 packs
  and say so. Never fake a browser.
- Renders must be launched standalone (`setsid nohup`) or they get "render_cancelled_parent_exited".
- Clear disk space before renders.
- Draft renders made the mascot look soft; judge mascot quality at full quality (previews at CRF 16).
- Chatterbox + atempo speed-up sounded unnatural; generate faster instead of time-stretching ("generated it faster
  instead of speeding up the audio", CHECK v6).
- Never loudnorm a short SFX (its dynamic mode buffers ~3 s); normalise one-shots by peak.
- The -14 LUFS masters at -1.5 / -2 dBTP fail the verify script's -4 dBTP check (open item).
- Keep client media (mascot, poses, wordmark) and MP4s out of git; the repo is public. Earlier commits still contain the
  mascot crops.
- PDFs: rasterise pages to avoid iOS rendering bugs; keep long titles clear of the logo.

---

## 19. Known costs

| Item | Cost |
|---|---|
| ElevenLabs VO, explainer (Hallie) | 2 takes x 654 credits |
| ElevenLabs Scribe word timings | 0 credits |
| Cree's 13 poses (gpt-image-2.5-sunburst, 2 per pose + spares) | about 12,600 ElevenLabs credits ("around $2"); about 486 credits per image |
| Kokoro, Chatterbox, faster-whisper | free, local |
| Openverse music / SFX, Pexels | free (licence credits in the post) |
| Higgsfield | not used (balance 0 credits, free plan, 2026-11-10) |
| Agency fee / client budget | UNKNOWN |
