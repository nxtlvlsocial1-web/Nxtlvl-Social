# openGym × Claude reel: laptop (GPU) setup and run order

The cloud session wrote the plan, the script and the voice tooling. Everything heavy runs here, on a machine with an
NVIDIA GPU (RTX 3050 Laptop, 4 GB): the open-source voices, the 3D preview and the final render.

Read first: `SCRIPT.md` (the locked script, under 35 s), `PLAN.md` (the 3D plan; section 3's script is superseded
by SCRIPT.md), and `BRIEF_original.md`.

## 1. One-time setup

1. Install these:
   - Git;
   - Node.js 22 or newer;
   - FFmpeg (`ffmpeg -version` must work);
   - Python 3.10–3.12;
   - an NVIDIA driver with CUDA (`nvidia-smi` must work);
   - Claude Code (`npm i -g @anthropic-ai/claude-code`), or the Claude Desktop app.
2. Get the project:
   ```
   git clone https://github.com/nxtlvlsocial1-web/Nxtlvl-Social
   cd Nxtlvl-Social
   git checkout claude/hyperframes-cli-install-w6ziy7
   ```
3. Start a session here with `claude remote-control`, or open this folder in the Claude Desktop Code tab. It then shows in the Claude Code app.
4. Python environment for the voices. This machine runs **Windows** with an **RTX 3050 Laptop GPU (4 GB VRAM)**, so
   use the small models, and close GPU-heavy apps (Wallpaper Engine, games, extra browser windows) while generating.
   ```
   python -m venv .venv-voice
   .venv-voice\Scripts\Activate.ps1        # if blocked: Set-ExecutionPolicy -Scope Process RemoteSigned
   pip install kokoro chatterbox-tts soundfile numpy "setuptools<81" faster-whisper
   python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
   ```
   - If that prints `False`, chatterbox-tts pulled in a CPU-only torch. Reinstall the **same torch version** with CUDA:
     `pip install --force-reinstall torch==<that version> torchaudio==<that version> --index-url https://download.pytorch.org/whl/cu124`.
     If cu124 has no wheel for that version, use cu121 or cu126.
   - Models download from Hugging Face on first use.
   - If Kokoro asks for espeak-ng, install it from the espeak-ng GitHub releases (MSI).
   - `setuptools<81` keeps `pkg_resources`, which Chatterbox's watermarker (resemble-perth) imports; without it
     Chatterbox fails with `'NoneType' object is not callable`. `faster-whisper` checks the takes and times the words.
   - On this laptop torch 2.6.0 came in CPU-only; `--force-reinstall --no-deps torch==2.6.0 torchaudio==2.6.0` from
     the cu124 index fixed it (`2.6.0+cu124 True`).

## 2. The two voices (open source, expressive)

| Character | Who | Sound |
|---|---|---|
| NXT | the violet AI robot in muscle mode | cocky, warm, playful, quick; a light robotic colour added in post |
| HUMAN | young guy, about 22 | casual, tired, then surprised, then laughing |

**Both voices: no Indian accent.** Use natural American young male voices that sound clearly different from each other.

**Engines (all open source, commercial use OK):**
- **Kokoro-82M (Apache-2.0)** designs the voices: 8 American male voices, small enough for any GPU or the CPU.
- **Chatterbox (MIT)** clones the picked voices and acts every line. Each line has its own emotion intensity
  (`exaggeration`) and pacing (`cfg_weight`) set in `LINES`.
- **Dia-1.6B** is too big for 4 GB, so don't use it here.

Steps:

1. **Design the voices.** This makes one sample per Kokoro voice for each character:
   ```
   python opengym-claude-9x16/voice/make_voices.py design
   ```
   Send the user `voice/design/` (nxt_* and human_*) and let them pick one voice per character. They must be different voices.
2. **Generate every line,** 3 takes each, acted in the picked voices:
   ```
   python opengym-claude-9x16/voice/make_voices.py lines --nxt am_puck --human am_liam
   ```
   (Use the user's picks.)
   - On "CUDA out of memory", close GPU apps and retry, or add `--device cpu`. That's slower, but it's only 12 short lines.
   - If `pip install -U chatterbox-tts` provides Chatterbox Turbo, `--engine chatterbox-turbo` is worth one test. It acts
     real [laugh] and [sigh] sounds.
   - `--only 3 10` regenerates just those lines.
3. **Pick the best takes and assemble.** Listen to `voice/lines/`, choose the most expressive take of each line, then run:
   ```
   python opengym-claude-9x16/voice/make_voices.py assemble --pick 02=3 10=2
   ```
   This writes `assets/audio/voice_nxt.wav`, `voice_human.wav`, `voice.wav` and `voice/lines.json`. The voice must end by
   **33.5 s**: the reel is under 35 s with the 1.5 s end card.
   - If a line sounds flat, raise its `exaggeration` in `LINES` (up to about 1.0), lower its `cfg_weight` (about 0.3), and regenerate that line.
4. Send the user `assets/audio/voice.wav` to approve **before** building the 3D.

What was run for v1 (26 Oct 2026; Rishabh approved every step in advance):
- Voices: NXT `am_fenrir`, HUMAN `am_puck` (both American; picked by Kokoro quality grade, pitch range and a clear
  pitch gap between the two).
- `python opengym-claude-9x16/voice/qa_takes.py` transcribes every take with Whisper and scores it (word accuracy,
  pauses, peaks, pitch movement) -> `voice/qa.json`.
- `assemble --pick 01=1 02=1 03=3 04=3 05=2 06=1 07=2 08=1 09=1 10=3 11=2 12=3 --tempo 1.09`: the clean takes ran
  36.4 s, so every line is sped up 9 % (pitch kept); the last word ends at 33.38 s.

## 3. 3D build and preview (after the voice is approved)

Build order (inside the voice venv, from the repo root):
```
python opengym-claude-9x16/build/timing.py     # words.json + env.json from voice.wav
python opengym-claude-9x16/build/generate.py   # index.html (cues, panel, captions, timeline)
python opengym-claude-9x16/build/audio.py      # music.wav + mix.wav, mastered to -14 LUFS / -1.5 dBTP
python opengym-claude-9x16/build/cover.py      # cover/index.html; then: npx hyperframes snapshot cover --at=0.5 --no-end
```
The 3D world is `assets/js/opengym.js`. The panel screens are mocks (no screen recordings were supplied).

- Follow `PLAN.md` sections 4–6 with the SCRIPT.md timings. Snap every scene start to the first word of its line: transcribe `voice.wav` to word timestamps, then use them.
- Three.js inside HyperFrames, seek-driven, with one paused GSAP timeline.
- Use the GPU:
  - preview: `npx hyperframes preview --background`;
  - stills: `npx hyperframes snapshot --at ...`;
  - drafts: `npx hyperframes render --quality draft --browser-gpu --workers auto`.
- The final render needs the user's approval of the preview first:
  ```
  npx hyperframes render --quality delivery --browser-gpu --gpu -o renders/nxtlvl_opengym-claude_reels_9x16_v1.mp4
  ```
  Then master the audio to −14 LUFS and −1.5 dBTP, and make the cover PNG (PLAN.md and the brief, section 8).
- Keep MP4s and WAV/MP3 renders out of git; deliver them. Commit the source.

## 4. Fix round 1 (the user reviewed v1)

1. **"Gym" pronounced "gim" (hard G), and "GYM" spelled out as letters.**
   - `voice/make_voices.py` now respells the words for the voice only: "gym" and "GYM" become "jim", and "openGym" becomes "Open jim". Captions keep the script spelling.
   - The sigh is no longer spoken as "huh, uh, uh". Line 4's take 1 also dropped the "open".
   - Regenerate the lines that contain these words. Lines 3, 4 and 12 have "gym"; line 1 had the sigh:
     ```
     python opengym-claude-9x16/voice/make_voices.py lines --nxt am_fenrir --human am_puck --only 1 3 4 12
     ```
   - Check every new take for "jim" (soft J), not "gim" or letters, and for a clean start on line 1. Then re-assemble with the same picks for the other lines and the same `--tempo`. The voice must still end by 33.5 s.
2. **The synthesized music sounds weird.** Replace it with a real, licensed track:
   ```
   python opengym-claude-9x16/build/find_music.py search
   python opengym-claude-9x16/build/find_music.py use <id>
   ```
   - Pick a modern, punchy gym or electronic track that fits a fun tech reel, with steady energy from the first second.
   - Avoid anything cheesy, chiptune, or with vocals that clash with the dialogue.
   - `build/audio.py` then uses it as the bed, ducked under the voice, with the SFX a little lower.
   - Put the credit line from `build/track.json` in the post caption (required for CC BY).
3. Re-run `build/timing.py`, `build/audio.py` and `build/generate.py`. Check the mix: the voice should always sit clearly on top. Then re-render the final.
