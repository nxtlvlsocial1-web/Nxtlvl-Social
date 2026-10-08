# Nxtlvl Social

Nxtlvl Social makes social media content for clients. This repo holds the Claude Code skills used to
produce that content, mainly short videos built with [HyperFrames](https://github.com/heygen-com/hyperframes)
(videos authored as HTML and rendered to MP4).

## Skills

All skills live in `.claude/skills/`.

**Start here for any video request:** `/nxtlvl-social-video`. It sets our formats, brand and delivery
rules, then hands off to `/hyperframes`, which picks the right workflow.

| Need                                                    | Skill                                         |
| ------------------------------------------------------- | --------------------------------------------- |
| Our rules: formats, safe zones, captions, naming        | `nxtlvl-social-video`                         |
| Routing any video request                               | `hyperframes`                                 |
| Short motion graphic, kinetic text, stat, logo sting    | `motion-graphics`                             |
| Captions on talking-head footage                        | `embedded-captions`                           |
| Graphic overlays on interview / podcast footage         | `talking-head-recut`                          |
| Beat-synced video from a music track                    | `music-to-video`                              |
| Product or brand promo from a URL or brief              | `product-launch-video`                        |
| Explainer / listicle / how-to with no footage           | `faceless-explainer`                          |
| Longer, multi-scene or freeform video                   | `general-video`                               |
| Presentation or pitch deck                              | `slideshow`                                   |
| Bringing in a Figma design                              | `figma`                                       |
| Music, SFX, voiceover, images, logos, colour grade      | `media-use`                                   |
| Lip-sync a face to audio (via RunComfy)                 | `lipsync`                                     |
| Building blocks, effects, transitions                   | `hyperframes-registry`                        |
| Composition HTML, animation, audio mix, camera moves    | `hyperframes-core`, `-animation`, `-audio`, `-keyframes` |
| Design direction: palette, type, pacing                 | `hyperframes-creative`                        |
| Working with a person in Studio, storyboards            | `hyperframes-studio`                          |
| CLI: init, check, preview, render, troubleshooting      | `hyperframes-cli`                             |

The HyperFrames skills are third-party (from `heygen-com/hyperframes`); their versions are pinned in
`skills-lock.json`. Don't edit them by hand. Update them with:

```bash
npx skills add heygen-com/hyperframes --skill <name> --agent claude-code -y
```

`lipsync` is also third-party (from `prime-skills/runcomfy-agent-skills`, pinned in `skills-lock.json`).
It runs the RunComfy CLI (`npm i -g @runcomfy/cli`, then `runcomfy login` or set `RUNCOMFY_TOKEN`), which
is paid. Only lip-sync people who have consented to it, for both their face and their voice. Update it with:

```bash
npx skills add prime-skills/runcomfy-agent-skills --skill lipsync --agent claude-code -y
```

Our own skills (currently `nxtlvl-social-video`) are ours to edit.

## Setup

- Node.js 22 or newer and FFmpeg.
- Run the CLI as `npx hyperframes ...`.
- Voiceover and generated music need a HeyGen account (`npx hyperframes auth`) or a Gemini API key.
- Telemetry: set `HYPERFRAMES_NO_TELEMETRY=1` to turn it off.

## Repo layout

```
.claude/skills/       Claude Code skills
brands/<client>/      Brand kits: brand.md, logo.svg, fonts/ (see nxtlvl-social-video § 4)
<project>/            One HyperFrames project per video and aspect ratio, e.g. spring-drop-9x16/
```

## Rules

- Never render a final until the person has approved the preview.
- Never use music or images we don't have the rights to; source them through `media-use`.
- Keep rendered MP4s out of git; deliver them, don't commit them.
