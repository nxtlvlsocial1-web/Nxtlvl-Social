# AI.NXTLVL: Prism, a free download manager (Instagram Reels, 9:16, ~48 s)

Recreated from a reference reel (the Prism explainer) with a proof-first hook, a strict layout grid (headline band /
3D stage / live caption, all centred) and our own 3D build. Build: build/vo_cb.py + build/vo_pick.py (voice: Chatterbox
with the synthetic Kokoro am_puck reference, the AI.NXTLVL page voice), build/generate.py (type, timing, SFX cues),
assets/js/scene.js (Three.js stage), build/sfx_mix.py (mix). Facts: plan/prism_readme.md (the project's own README).

## Facts used (all from github.com/FortoGraphy/prism-download-manager, checked 2026-11-25)

- Free, MIT licence, no ads, no account, no telemetry; Windows, macOS, Linux; 1.6k GitHub stars (shields.io).
- Up to 32 parallel connections; up to 15x faster than a normal download on servers that throttle each connection.
- Benchmark (their docs, SHA-256 verified): 1 GiB from a throttling server, 1 connection 4.0 MiB/s = 4:16, Prism
  60.9 MiB/s = 0:17. On a real ~200 Mbit/s line: 1 connection 25.9 MiB/s, Prism 25.1 MiB/s (the honest catch).
- When a connection finishes its part it takes over half of the largest part still remaining.
- Resumes after crashes, sleep or power loss, from where it stopped.
- Video from YouTube and 1,800+ sites (via yt-dlp), MP4 up to 8K/HDR or MP3 only.
- BitTorrent and magnet links; Hugging Face models by name (e.g. Qwen/Qwen3-8B), SHA-256 checked.
- The app is independent of Internet Download Manager / Tonec (its README says so); IDM is named only as the comparison.

## Script and arc

| Line | Beat |
|---|---|
| A one gigabyte file, in seventeen seconds. On the same server, one connection took over four minutes. | hook: proof on frame 1 (two timer rings) |
| It's called Prism. A free, open source alternative to Internet Download Manager. | name |
| Your browser pulls a file through one single connection. And a lot of servers cap the speed of each one. | problem |
| So Prism splits that same file into up to 32 parts, and pulls them all at once. | peak |
| When one part finishes early, it takes over half of the biggest part still left. Nothing sits idle. | how |
| It grabs videos too. YouTube and 1,800 other sites, up to 8K, or just the MP3. | feature |
| Laptop dies halfway? It picks up exactly where it stopped. | feature |
| It even does torrents, and Hugging Face models. | feature |
| One honest catch. If your own internet is the slow part, no app can fix that. | trust |
| Send this to the friend who's still waiting on a download. | share trigger |
| Comment PRISM, and I'll send you the link. | CTA |

Hook variants to test:
- A (built): "A one gigabyte file, in seventeen seconds. On the same server, one connection took over four minutes."
- B: "Your browser downloads with one hand tied behind its back."
- C: "This free app splits every download into 32 pieces at once."

## Post description (ready to paste)

```
Comment "PRISM" and I'll send you the link.

A 1 GB file in 17 seconds. On the same server, one connection took over 4 minutes.

Prism is a free, open-source alternative to Internet Download Manager:
1. Splits every file into up to 32 parts and downloads them all at once
2. When one part finishes early, it takes over half of the biggest part left, so nothing sits idle
3. Grabs video from YouTube and 1,800+ sites, up to 8K, or just the MP3
4. Laptop dies halfway? It resumes exactly where it stopped
5. Also does torrents, magnet links and Hugging Face models

Windows, Mac and Linux. No ads, no account. One honest catch: if your own internet is the slow part, no app can fix that.

Send this to the friend who's still waiting on a download.

Music: "Funky Nurykabe (Spinningmerkaba Mix)" by ccMixter, CC BY 3.0

#opensource #downloadmanager #techtools #productivity #freesoftware
free download manager, idm alternative, internet download manager free, fast download manager, open source download manager, download youtube videos 8k, resume broken downloads, torrent client, hugging face model download, best free software 2026
```

## Auto-DM for PRISM (link and setup only)

```
https://github.com/FortoGraphy/prism-download-manager

1. Open the latest release and download the installer for your system (Windows .exe, Mac .dmg, Linux .deb, .rpm or .AppImage).
2. First start: the installers are not code-signed. Windows: More info, then Run anyway. Mac: System Settings, Privacy & Security, Open Anyway.
3. Add the Prism extension from the Chrome Web Store and pin it.
4. Click any download link and Prism takes over.
```

Notes:
- The two timers are Prism's own published benchmark (a throttling test server), not a claim about every connection.
- Download only content you have the right to download (Prism's own FAQ says the same).
- Music: "Funky Nurykabe (Spinningmerkaba Mix)" by ccMixter (Jamendo 1468789, CC BY 3.0), the AI.NXTLVL bed.
