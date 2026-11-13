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
| Instagram Reels, TikTok, YT Shorts    | 9:16   | 1080×1920  | `portrait`          | 7–58 s (always under 60 s) |
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
   Run the final render fully detached with no time limit (a `setsid nohup` script, never a backgrounded tool
   command with a timeout), with `< <(sleep infinity)` as its input and `HYPERFRAMES_RENDER_DETACHED=1` in its environment, so the CLI does not
   cancel itself when its input
   closes. Check the log shows frames streaming, then keep the session active until it finishes (an idle cloud
   session's machine shuts down and kills the render).
4. Verify each file with `ffprobe`: size, duration, fps match § 2.

**Before every final render, check the frames yourself** (snapshot every scene, wide shots and every close-up, at
full size) and fix anything on this list first. The owner has had to point these out after a final; they must never
reach one again:

- **Characters in one piece:** head, neck, collar and torso connected with no gap or floating part in every pose
  (standing, sitting, lying, arms up); limbs joined at shoulders and hips; nothing intersecting the furniture.
- **Faces friendly, never creepy:** simple cartoon features (dark eyes with a highlight, small brows, small nose, a
  small mouth or a filled "o"); no dark patches from hair or helmet shells across the face, no oversized rings or
  bulges; expressions read clearly in the close-ups.
- **Faces and subjects not blocked:** no prop, phone, halo, wing or other object between the camera and a face or the
  action of the shot; no camera inside walls, furniture or crowds; the subject of each shot is actually in frame.
- **Nothing distorted or missing:** no stretched or squashed parts, objects popping in or out (frustum culling), or
  lights washing a face out; dark scenes still readable.
- **Overlays clear of faces:** cards, tags and the HUD do not cover the face or the key action in a shot.

## 6. Delivery

- File name: `<client>_<campaign>_<platform>_<aspect>_v<n>.mp4`, e.g.
  `nxtlvl_spring-drop_reels_9x16_v1.mp4`.
- MP4, H.264, AAC audio, under 100 MB per file.
- Deliver every requested format plus a 1-frame cover image (`.png`, same size) per format.
- In the final reply, list each file with its platform, size, duration and path.
- Post descriptions: hashtags all lowercase (`#instagramgrowth`, never `#InstagramGrowth`), no emojis.

## 7. "What if" reels

Every "what if" reel (a hypothetical scenario, e.g. "What if one AI ran a city for 24 hours?") follows these rules.

**No keyword CTA by default.** No "comment X and I'll send you Y" in the script, on the end card or in the
description when there is nothing to DM. End instead on the follow prompt (spoken "Follow for more what-ifs" and the
`@handle` on the end card) and a question that invites comments ("Would you trust it?"). The description then opens
with the hook, not a CTA line.

**Exception: a real resource to send.** When the scenario leads to a real tool, guide or template we actually DM
(e.g. the AI clone reel sends the auto-DM tool), the reel may close on a keyword CTA instead: spoken "Follow
@nxtlvlsocial.ai and comment KEYWORD", the keyword on the end card, and the description opening with the CTA keyword
line as for any other reel. Set up the comment-to-DM automation for that keyword before the post goes live.

**The modern story arc** (from the reference the owner shared): stack peaks, never one slow climb to a mid-video
climax. Plan every script as a list of beats on this curve before writing a line:

1. **Hook, 0-3 s, start at 70/100.** Drop the viewer into a story already happening: a time stamp and an absurd
   consequence, not a setup ("3:12 AM. The AI just admitted a patient who hasn't arrived yet."). No "Imagine if..."
   warm-up, no logo, no question the viewer can answer "no" to.
2. **First peak, by 5-10 s, spike to 90.** A contrast, a contrarian line or a shocking number that pays off the hook.
3. **Release, then peak again, every 8-15 s.** Each release is one or two lines of context; each peak is a new turn:
   a twist, a stat, a reversal, something going wrong. Aim for 4-5 peaks in a 45-58 s reel. Every reel stays under
   60 s: when a story has many steps (days, tools, swaps), show them as a fast montage with on-screen cards, not a line each.
4. **The final peak is the biggest turn** (the thing nobody can explain, the reversal, the real-world fact that
   says "this is already happening"), then land on the question and the follow prompt. Leave no flat stretch longer
   than about 10 s.

On screen, every peak gets a visual event (a stamp, a counter, a camera move, a hit in the score), so the arc is
visible in the edit as well as the voice. Label the reel `WHAT IF` and keep any real-world claim verified and sourced
in the description; the scenario's own numbers are illustrative.

## 8. Tutorial skit format (the default for tool and how-to reels)

For any reel that teaches a tool or a set of steps. The owner shared a reference reel (a creator and his AI sidekick
showing a free voice tool in four steps) as an example of **clarity**, not a template: keep its principles, and vary the
look, the screen device, the hook and the end card from reel to reel so no two look the same and none copies the
reference. Viewers must be able to follow every step on a phone.

**The principles (keep these every time):**
- One step at a time, on a screen big enough to read on a phone (illustrated, never a logo we don't own), acted out with
  small interactions: typing, a tap, a scan, a tick.
- Always show where the viewer is in the steps (a progress cue of some kind).
- Two characters in one cozy 3D scene (a person and a sidekick, usually an AI helper), faces clear of every overlay.
- Captions a few words at a time, between the screen and the characters.
- The script beats below.

**Vary these (pick a different mix each reel, and say which in the plan):**
- Screen device: a big app panel, a phone in the frame, a laptop screen rising from the desk, a tablet on a stand.
- Progress cue: a step pill and progress bar, a legal-pad checklist that ticks off, numbered sticky notes, a step counter
  on the screen.
- Hook: real-sounding comment questions, the tool's own result showing the problem (e.g. ChatGPT recommending the
  competitor), a stat, a reaction.
- Caption style: serif on the scene, boxed sans, speaker-coloured.
- End card: a full card, a sticky note over the dimmed scene, the last screen turning into the CTA.
- Camera: a still frame with a slow push, or gentle lean-ins on whoever is talking.

**Script:**
1. Hook (0-5 s), then a two-line setup. No title card, no "WHAT IF" label.
2. Each step: the sidekick says the step plainly once; the person asks the question a viewer would ask; the sidekick
   answers in one short line. Jokes are quick asides that reinforce the info ("No GPU works too. / Just slower. Like you.").
3. An honest beat near the end (what it can't do, what not to do, a caveat), shown as a stamp or note on screen.
4. A punchline, then the end card: a share prompt ("Send this to a friend who..."), `Comment KEYWORD for the full
   setup`, `Follow for the next one`. Under 60 s as always.
5. Music: pick an Openverse track that fits the mood of a cozy comedy (warm acoustic, light jazz, playful), CC0 or CC BY
   only, no lyrics, and credit it. Avoid heavy beats, 808s and anything odd that fights the dialogue.
