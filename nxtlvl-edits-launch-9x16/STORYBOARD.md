# @nxtlvlledits launch Reel (9:16, 26.5 s): draft

Instagram Reel announcing @nxtlvlledits, the editing account of Nxtlvl Social. All motion graphics, a voiceover,
the real before/after of an edit we made, and the N Disc logo.

## Sound

- Voiceover: local Kokoro TTS (voice `am_michael`), one file per line (`work/*.wav`), placed on the film clock and
  levelled to −16 LUFS in `assets/voice/vo.wav`. (ElevenLabs was out of credits.)
- Music: the Nxtlvl brand bed (120 bpm, drop at 4 s, impact at 22 s), ducked under the voice (`assets/music/bed-ducked.wav`).
- SFX: Pixabay-licensed set (`assets/sfx/CREDITS.md`), placed on the visible actions (`SFX` in `tools/build.py`).

## Scenes

| Time | Voice | Picture |
|---|---|---|
| 0–4 | "Most reels die in the first second. / Ours don't." | Title slams in, a heartbeat line flatlines as a 1.00 s clock runs out; "OURS don't." jolts it back |
| 4–8 | "Every cut, on the beat. Every frame, on purpose." | Edit timeline: the playhead hits a beat marker every beat and a razor cut lands; a film strip stops under a viewfinder |
| 8–12 | "Cut. Colour. Motion. Sound." | One word a beat: CUT splits on a razor line, COLOUR grade-wipes, MOTION streaks in with echoes, SOUND jumps with a waveform |
| 12–17.75 | "Raw footage in. / Next level reels out." | The real raw take, then a wipe reveals the finished ad (the System ad); the card closes into a pearl disc |
| 17.5–22 | "Next Level Edits. The edit room of Next Level Social." | The N is carved into the disc in one stroke, the star glints, a sheen runs across, orbits and rays |
| 22–26.5 | "Now live." | Impact flash and shockwaves; NOW LIVE, @nxtlvlledits, a Follow button that gets tapped |

## Rebuilding

- Clips (kept out of git): `assets/video/raw.mp4` = `nxtlvl-ad-system-9x16/assets/video/footage.mp4` 1.3–4.9 s;
  `assets/video/edit.mp4` = `nxtlvl-ad-system-9x16/renders/nxtlvl_system-ad_reels_9x16_v2.mp4` 0.2–4.8 s
  (both `-an -g 15`).
- `python3 tools/scenes.py && python3 tools/build.py`, then `npx hyperframes check`, `npx hyperframes render`.
