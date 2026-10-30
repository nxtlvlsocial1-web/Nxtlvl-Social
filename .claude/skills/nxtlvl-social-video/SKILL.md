---
name: nxtlvl-social-video
description: >
  Nxtlvl Social's house workflow for making social media videos with HyperFrames. Use for any request
  to make a Reel, TikTok, YouTube Short, Story, feed post video, carousel video, ad creative, captioned
  clip, or a set of cutdowns for several platforms. It fixes the platform formats, durations, safe
  zones, brand rules, file naming and delivery checklist, then hands authoring to the HyperFrames
  skills (/hyperframes first). Don't use for non-video work.
---

# Nxtlvl Social — social video

This skill holds the Nxtlvl Social rules. The HyperFrames skills hold how to build. Apply this skill's
rules on top of theirs; when they conflict, this skill wins on format, brand and delivery, and the
HyperFrames skills win on composition structure and rendering.

## 1. Before building

1. Find the **platforms** the video is for. If the request doesn't say, ask once and list the options
   in § 2. Don't guess a single platform for a client deliverable.
2. Find the **client / brand**. Load its brand kit (§ 4). If there's no kit, ask for logo, colours and
   fonts, or proceed with the Nxtlvl defaults and say so.
3. Then follow `/hyperframes` for routing. It picks the workflow skill (for example
   `/motion-graphics`, `/talking-head-recut`, `/embedded-captions`, `/music-to-video`,
   `/product-launch-video`, `/faceless-explainer`, `/general-video`).

## 2. Platform formats

Build the **master** at the first row the request needs, then make the other formats as cutdowns.

| Platform / placement                  | Aspect | Size (px)  | `init --resolution` | Length target     |
| ------------------------------------- | ------ | ---------- | ------------------- | ----------------- |
| Instagram Reels, TikTok, YT Shorts    | 9:16   | 1080×1920  | `portrait`          | 7–30 s (max 60 s) |
| Instagram / Facebook Stories          | 9:16   | 1080×1920  | `portrait`          | ≤ 15 s per card   |
| Instagram / Facebook feed (preferred) | 4:5    | 1080×1350  | custom (see below)  | 6–30 s            |
| Feed square, LinkedIn                 | 1:1    | 1080×1080  | `square`            | 6–30 s            |
| YouTube, LinkedIn landscape, X        | 16:9   | 1920×1080  | `landscape`         | 15–90 s           |

- 4:5 has no preset: scaffold with `portrait` and set the root composition's `data-width="1080"`
  `data-height="1350"`.
- 30 fps unless the brief says otherwise.
- A different aspect is a separate HyperFrames project (`/hyperframes-studio` rule). Name them
  `<campaign>-<aspect>`, e.g. `spring-drop-9x16`, `spring-drop-4x5`.

## 3. Social rules

- **Hook in the first 1.5 s.** The first frame must already show the subject or the headline — no
  slow fade-in from black, no logo-first intro.
- **Captions on by default.** Most social video plays muted. Burn in captions for any speech
  (`/embedded-captions` for existing footage, the workflow's caption track otherwise).
- **Safe zones for 9:16:** keep text, faces and logos out of the top 250 px and the bottom 400 px
  (platform UI: username, caption, buttons), and 60 px from each side. Follow `/hyperframes-studio`
  § 4 for how to lay this out on the timeline.
- **One message per video.** End on a clear CTA card (follow, link in bio, shop now) held ≥ 1.5 s.
- **Loopable** when it's a Reel/TikTok under 15 s: the last frame should cut cleanly back to the first.
- Music: only licensed or generated tracks (`/media-use`). Never pull audio from a random URL.

## 4. Brand kits

Brand kits live in `brands/<client-slug>/` at the repo root:

```
brands/<client-slug>/
  brand.md        # colours (hex), fonts, tone of voice, do / don't
  logo.svg        # primary logo; logo-light.svg for dark backgrounds
  fonts/          # licensed font files, if not on Google Fonts
```

Use the kit's colours and fonts exactly; pass them to `/hyperframes-creative` as the design spec.
Nxtlvl Social's own kit is `brands/nxtlvl/` — fill it in before using it as the default.

## 5. Review and render

1. `npx hyperframes check` must pass.
2. Open `npx hyperframes preview --background`, give the person the URL, and wait for approval.
3. Render with `--quality draft` while iterating and `--quality delivery` for the final.
4. Verify each file with `ffprobe`: size, duration, fps match § 2.

## 6. Delivery

- File name: `<client>_<campaign>_<platform>_<aspect>_v<n>.mp4`, e.g.
  `nxtlvl_spring-drop_reels_9x16_v1.mp4`.
- MP4, H.264, AAC audio, under 100 MB per file.
- Deliver every requested format plus a 1-frame cover image (`.png`, same size) per format.
- In the final reply, list each file with its platform, size, duration and path.

## 7. "What if" reels

Every "what if" reel (a hypothetical scenario, e.g. "What if one AI ran a city for 24 hours?") follows these rules.

**No keyword CTA.** No "comment X and I'll send you Y" in the script, on the end card or in the description; there is
nothing to DM. End instead on the follow prompt (spoken "Follow for more what-ifs" and the `@handle` on the end card)
and a question that invites comments ("Would you trust it?"). The description opens with the hook, not a CTA line.

**The modern story arc** (from the reference the owner shared): stack peaks, never one slow climb to a mid-video
climax. Plan every script as a list of beats on this curve before writing a line:

1. **Hook, 0-3 s, start at 70/100.** Drop the viewer into a story already happening: a time stamp and an absurd
   consequence, not a setup ("3:12 AM. The AI just admitted a patient who hasn't arrived yet."). No "Imagine if..."
   warm-up, no logo, no question the viewer can answer "no" to.
2. **First peak, by 5-10 s, spike to 90.** A contrast, a contrarian line or a shocking number that pays off the hook.
3. **Release, then peak again, every 8-15 s.** Each release is one or two lines of context; each peak is a new turn:
   a twist, a stat, a reversal, something going wrong. Aim for 4-5 peaks in a 45-70 s reel.
4. **The final peak is the biggest turn** (the thing nobody can explain, the reversal, the real-world fact that
   says "this is already happening"), then land on the question and the follow prompt. Leave no flat stretch longer
   than about 10 s.

On screen, every peak gets a visual event (a stamp, a counter, a camera move, a hit in the score), so the arc is
visible in the edit as well as the voice. Label the reel `WHAT IF` and keep any real-world claim verified and sourced
in the description; the scenario's own numbers are illustrative.
