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
   pip install kokoro chatterbox-tts soundfile numpy
   python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
   ```
   - If that prints `False`, chatterbox-tts pulled in a CPU-only torch. Reinstall the **same torch version** with CUDA:
     `pip install --force-reinstall torch==<that version> torchaudio==<that version> --index-url https://download.pytorch.org/whl/cu124`.
     If cu124 has no wheel for that version, use cu121 or cu126.
   - Models download from Hugging Face on first use.
   - If Kokoro asks for espeak-ng, install it from the espeak-ng GitHub releases (MSI).

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

## 3. 3D build and preview (after the voice is approved)

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
