# openGym × Claude reel: laptop (GPU) setup and run order

The cloud session wrote the plan, the script and the voice tooling. Everything heavy runs here, on a machine with an
NVIDIA GPU: the open-source voices, the 3D preview and the final render.

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
4. Python environment for the voices:
   ```
   python -m venv .venv-voice && source .venv-voice/bin/activate     # Windows: .venv-voice\Scripts\activate
   pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124
   pip install git+https://github.com/nari-labs/dia.git chatterbox-tts soundfile numpy
   ```
   The models download from Hugging Face on first use. Dia-1.6B needs a GPU with roughly 8 GB of VRAM or more; Chatterbox needs less.

## 2. The two voices (open source, expressive)

| Character | Who | Sound |
|---|---|---|
| NXT | the violet AI robot in muscle mode | cocky, warm, playful, quick; a light robotic colour added in post |
| HUMAN | young Delhi guy, about 22 | casual, tired, then surprised, then laughing |

**Why Dia:** it performs dialogue with real non-verbals, like `(sighs)`, `(gasps)` and `(laughs)`, so it doesn't
sound like a flat narrator. Chatterbox is the fallback, with an emotion-intensity knob per line.

Steps:

1. **Design the voices.** This makes one sample per seed for each character:
   ```
   python opengym-claude-9x16/voice/make_voices.py design --seeds 3 7 11 19 23 31 42 58
   ```
   Listen to `voice/design/`. Pick one seed per character: for NXT, a confident young male; for HUMAN, a different young male. Generate more seeds if none fit.
2. **Generate every line,** 3 takes each, cloned from the picked voices:
   ```
   python opengym-claude-9x16/voice/make_voices.py lines --nxt-seed <N> --human-seed <M>
   ```
   - For an Indian accent on HUMAN, record a 10 s reference yourself (or use a friend's, with their consent). Then pass `--human-ref ref.wav --human-ref-text "<exact words in the clip>"`.
   - If Dia misbehaves, add `--engine chatterbox` (the same refs work).
   - **Check:** if a Dia take also contains the reference sentence at its start, trim that part before assembling.
3. **Pick the best takes and assemble:**
   ```
   python opengym-claude-9x16/voice/make_voices.py assemble --pick 02=3 10=2
   ```
   This writes `assets/audio/voice_nxt.wav`, `voice_human.wav`, `voice.wav` and `voice/lines.json`. The voice must end by **33.5 s**: the reel is under 35 s with the 1.5 s end card.
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
