# Klap brand reel: GTA 6 clippers (Instagram Reels, 9:16, ~43 s)

v2 (owner on v1: "remove that next level logo completely", "fonts are very bad", "animation, style and smoothness not up
to match", "no alignment", "voiceover looks very generic"):

- No AI.NXTLVL branding anywhere. Klap's own mark sits top-right after the reveal.
- Type: Clash Display 700 for headlines and big numbers, Poppins (Klap's own UI font) for UI and captions. Headlines
  reveal word by word, the key phrase on a violet pill (Klap's violet-500).
- Palette: Klap's ink #020617 and violet #8b5cf6; green only for money and "Posted"; red only for LIVE and the chase.
- One grid: headline band 300-540, stage 600-1400, live caption 1470; every stage element centred or symmetric.
- Motion: speed-ramped GTA 6 cuts that whip into each beat, a 3D feed wall with reel UI, payout cards and a rolling
  counter, campaign cards and the $1 / 1K rate with a filling view bar, a tilted 3-hour filmstrip scrub that stops on
  the chase (colour pop, red spike, punch-in), a scan beam and a drawn selection box, the Klap logo built on the music
  drop (icon snaps in, K-l-a-p rise one by one, shockwaves, particles), Klap's app with cursor, Ctrl+V, typed URL,
  Generate press and a shimmering progress bar, three clips with virality rings counting to 94 / 99 / 87 and a TOP PICK,
  a 16:9 stream with an "active speaker" tracking box folding into the phone's Gaming layout, word-pop captions, the
  "other clippers vs you" split (rendering 31 % vs Posted, 12.4K to 184K views) and the comment-box CTA.
- Voice: Chatterbox read in passages with per-beat intensity, timbre from a synthetic Kokoro am_fenrir reference
  (nobody real is cloned), mastered (de-ess, compression, presence, limiter). ElevenLabs was the first choice, but the
  account is on the free tier with 9 credits left this month and Flashloop has 126 credits: both too low. The ElevenLabs
  pipeline is ready in build/vo_eleven.py (voice "Liam", v3 with audio tags) for the day credits are topped up.

Build: build/ref_kok.py, build/vo_cb.py, build/vo_pick.py, build/vo_run.sh (voice), build/prep_footage.sh,
build/generate.py (scenes, timing, SFX cues), build/music.py (music edit), build/sfx_mix.py (mix). v1 kept as
build/generate_v1.py.

## Owner decisions

- MrBeast and IShowSpeed appear by name only, on campaign cards: no faces in a paid ad.
- Klap's own screen recording is not shown (its thumbnails carry other creators' faces); the Klap screens are rebuilt
  with Klap's own wording and the logo vectorised from the supplied PNG.

## Facts used (checked 2026-11-25)

- GTA 6 launch: November 19, 2026 (Rockstar's announced date).
- Clipping pay: IShowSpeed x Expedia campaign on Content Rewards listed at $1 per 1,000 views; MrBeast clipping deals
  reported at about $0.50 to $3 per 1,000 views (Bloomberg; Tubefilter on Vyro). The video says "around a dollar".
- Klap (klap.app, klap.app/for/clippers, "Updated November 2026"): paste a YouTube, Twitch or Kick link, live streams
  included (first clips in about 15 minutes); every clip gets a virality score and clips are ranked by it; Split,
  Gaming and Bubble layouts; animated captions; up to 3 hours per video; schedules to TikTok, YouTube, Instagram,
  LinkedIn and Facebook; free to try on 1 video, downloading needs a paid plan.
- Illustrative UI, not claims: the payout amounts and counter, the view counts on the wall, the timecodes, the virality
  scores, the Twitch link, the handles.

## Script (the brand's, kept word for word; delivery marks only)

| Line | Beat |
|---|---|
| GTA 6 is out... and GTA clips are taking over every feed. And clippers? Are getting paid for views. | hook: car flip on frame 1, beat cuts, the feed wall, payouts |
| MrBeast and IShowSpeed campaigns pay around a dollar for every thousand views. | first peak: the money |
| But the hard part... is finding the moment. A three-hour stream. One crazy chase. | problem: the music drops to its breakdown |
| This tool finds it for you. It's called... Klap. | product at ~48 %: the kick lands on the name |
| You paste the stream link. It picks the best moments, and scores each one for how viral it could go. | how it works |
| It cuts them vertical, keeps the gameplay and the streamer in frame, and adds captions that pop. | Gaming layout, captions |
| So while other clippers are still scrubbing hour two... your clip is already up. | payoff |
| Comment Klap, and I'll send you the link. Or hit the link in my bio. | CTA |

Hook variants to test (re-cuts 5-7 days apart, or Trial Reels):
- A (built): "GTA 6 is out, and GTA clips are taking over every feed."
- B: "Clippers are making money off GTA 6 streams they didn't even play."
- C: "A three-hour GTA 6 stream has one clip worth posting. Here's how to find it in minutes."

## Post description (ready to paste)

```
Comment "KLAP" and I'll send you the link.

GTA 6 is out, and GTA clips are taking over every feed. Clippers are getting paid for views: big clipping campaigns like MrBeast's and IShowSpeed's pay around $1 for every 1,000 views.

The hard part is finding the moment. A 3-hour stream, one crazy chase. Klap finds it for you:
1. Paste the stream link (YouTube, Twitch or Kick, even while the stream is still live)
2. It picks the best moments and gives every clip a virality score
3. It cuts them vertical and keeps the gameplay and the streamer in frame
4. It adds animated captions that pop
5. Schedule them straight to TikTok, YouTube and Instagram

While other clippers are still scrubbing hour two, your clip is already up.

Campaign rates vary, so check each brief. Not affiliated with MrBeast, IShowSpeed or Rockstar Games.

Music: "Miami" by Lyvo, CC BY 3.0

#ad #gta6 #clipping #klap #aitools
gta 6 clips, how to make money clipping, clipping campaigns, ai clip maker, twitch clip maker, how to clip live streams, turn streams into shorts, klap ai, gta 6 stream highlights, clipping side hustle
```

## Auto-DM for KLAP (link and setup only)

```
https://klap.app

1. Sign up and try it free on your first video (no card needed).
2. Paste a stream link (YouTube, Twitch or Kick) or upload the recording.
3. Open the clips with the highest virality score and pick the Gaming layout.
4. Download or schedule them to TikTok, YouTube and Instagram (needs a paid plan).
```

If Klap gave you a tracking or affiliate link, swap it in for https://klap.app (in the DM and the bio).

## Posting notes

- Paid partnership: tag Klap with Instagram's "Paid partnership" label (#ad is also in the post).
- AI label: turn on "AI label" in Advanced settings (the voiceover is synthetic and sounds real; Meta requires it).
- GTA 6 footage: Rockstar Games' official promo clips, muted, under the owner's standing exception. It is a paid post,
  so if Klap's or Instagram's review flags the footage, the fallback is a re-cut around the Klap UI scenes.
- Facecam: Pexels 6878208 by cottonbro studio (Pexels licence, commercial use allowed). Sound effects: the series'
  Openverse CC0 / OpenGameArt CC0 set (plan/sfx_library.json). Music: "Miami" by Lyvo (Jamendo 1440523, CC BY 3.0),
  credited above. Fonts: Clash Display and Satoshi (Fontshare licence, kept out of git), Poppins (OFL).
