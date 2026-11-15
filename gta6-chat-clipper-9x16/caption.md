# AI.NXTLVL: GTA 6 clipping part 2, "chat already found your clips" (Instagram Reels, 9:16, 30 s)

Owner: "recreate this reel and make it better" (a creator's "Part 2 of GTA 6 clipping": a mascot explains a chat-spike
clip finder). v2 (owner: "looks like a reskin of the reference"): rebuilt as a Vox-style explainer, 30 s. Torn paper
cards, halftone, stepped motion on twos, over Rockstar's official GTA VI Miami album art (muted footage, owner
exception). Our mascot Nyx (the violet star-antenna robot) carries a prop or gag in every shot.
CTA keyword: CHAT. Lead magnets: `tool/chat_clips.py` (one file, tested) and `renders/ai-nxtlvl_gta6-chat-clipper-guide.pdf`.
v1 (40 s desk-and-monitor cut) is kept in `build/generate.py` and `plan/script_v1_40s.json`.

## Voiceover (v2, 30 s)

> You don't need AI to find the best GTA 6 clips. Chat already found them.
> When something crazy happens, chat explodes.
> That spike is your clip.
> So I had Claude build a tiny free tool.
> It counts the chat every ten seconds and cuts each spike into a vertical clip.
> Chat reacts late, so each clip starts twenty seconds early.
> GTA 6 drops Thursday. Let chat watch the streams for you.
> Comment CHAT for the tool and the setup guide.

## Post description (ready to paste)

```
Comment "CHAT" and I'll send you the free tool and the step-by-step setup guide.

You don't need AI to find the best GTA 6 clips. Chat already found them.

When something crazy happens on stream, chat explodes. That spike is your clip.

How the tool works:
1. A free app (TwitchDownloader) downloads the stream's chat
2. The tool counts the chat every 10 seconds and finds the spikes
3. Chat reacts late, so every clip starts 20 seconds early
4. One command cuts each spike into a vertical clip, ready for Reels, Shorts and TikTok

GTA 6 drops Thursday. Six-hour streams everywhere. Let chat watch them for you.

Only clip streams you own or have permission to clip, and credit the streamer.

Music: "Future Chiptune" by Andrey Avkhimovich (CC BY 3.0)
Not affiliated with Rockstar Games or Twitch.

#gta6 #gtavi #clipping #streamclips #aitools
gta 6 clips, gta 6 stream highlights, how to find stream highlights, twitch clip finder, how to clip twitch streams, twitch chat highlights, free clipping tool, how to make money clipping, vertical clips for shorts and reels, claude code projects
```

## Keyword auto-DM (once the files are hosted)

```
Here's the tool and the guide: [LINK]
1. Open the guide and install Python, FFmpeg and TwitchDownloader (page 3).
2. Download a stream's chat and VOD with TwitchDownloader (page 4).
3. Run: python chat_clips.py chat.json stream.mp4
```

## Notes

- GTA 6 releases Thursday, November 19, 2026: post before then, or change "drops Thursday" in the VO.
- The tool was tested on a synthetic 12-minute stream with three planted spikes: it found all three and cut three
  40-second 1080x1920 clips starting 20 s early.
- Proportions: every piece of footage sits in an aspect-locked box (16:9 stream cards, 9:16 clip cards); the Miami art
  is native 1080x1920. Each shot was checked in snapshots for text running off-frame or under the subtitles.
- Credits: music CC BY (above); SFX CC0 (Kenney "Interface Sounds" via OpenGameArt, because Freesound refused this
  machine; plan/sfx_library.json); Nyx and every paper piece are our own drawings. GTA VI art and clips: Rockstar
  Games' official promo material, muted.
