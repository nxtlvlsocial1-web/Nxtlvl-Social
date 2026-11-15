# AI.NXTLVL: GTA 6 clipping part 2, "chat already found your clips" (Instagram Reels, 9:16, 30 s)

Owner: "recreate this reel and make it better" (a creator's "Part 2 of GTA 6 clipping": a mascot explains a chat-spike
clip finder). v2 (owner: "looks like a reskin of the reference"): rebuilt as a Vox-style explainer, 30 s. Torn paper
cards, halftone, stepped motion on twos, over Rockstar's official GTA VI Miami album art (muted footage, owner
exception). v3 (owner: "don't keep that single robot mascot, build people types as per the frame requirements"):
Nyx is gone; each shot has its own paper cut-out people (build/people.py): the tired clipper and a chat viewer (hook),
three viewers losing it (chat explodes), an analyst with a pointer and a viewer calling "clip it" (spike), the builder
at a laptop (Claude), the editor with scissors (cuts), a late reactor and a clipper on the rewind dial (20 s early), the
clipper off duty in a beach chair while chat watches from the couch (Thursday), and the host waving (CTA).
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

## Keyword auto-DM (automation for "CHAT"; fill the link once the tool and guide are hosted)

```
Tool and setup guide: [LINK]
1. Install Python, FFmpeg and TwitchDownloader (guide page 3).
2. Download the stream's chat (.json) and VOD (.mp4) with TwitchDownloader (page 4).
3. Put chat_clips.py in the same folder and run: python chat_clips.py chat.json stream.mp4 (page 5).
4. Your vertical clips land in the clips folder, ready to post (page 7).
```

## Cover

`renders/ai-nxtlvl_gta6-chat-clipper_reels_9x16_v3_cover.png` (1080x1920, build/cover.py): "CHAT FINDS YOUR GTA 6
CLIPS" on torn paper, the skydive stream card (still from Rockstar's official clip), spike graph, FREE TOOL sticker,
chat bubbles and the three viewers, over the Miami palms art. Headline and faces sit inside the 3:4 profile crop.

## Notes

- GTA 6 releases Thursday, November 19, 2026: post before then, or change "drops Thursday" in the VO.
- The tool was tested on a synthetic 12-minute stream with three planted spikes: it found all three and cut three
  40-second 1080x1920 clips starting 20 s early.
- Proportions: every piece of footage sits in an aspect-locked box (16:9 stream cards, 9:16 clip cards); the Miami art
  is native 1080x1920. Each shot was checked in snapshots for text running off-frame or under the subtitles.
- Credits: music CC BY (above); SFX CC0 (Kenney "Interface Sounds" via OpenGameArt, because Freesound refused this
  machine; plan/sfx_library.json); every person and paper piece is our own drawing. GTA VI art and clips: Rockstar
  Games' official promo material, muted.
