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
| Building blocks, effects, transitions                   | `hyperframes-registry`                        |
| Composition HTML, animation, audio mix, camera moves    | `hyperframes-core`, `-animation`, `-audio`, `-keyframes` |
| Design direction: palette, type, pacing                 | `hyperframes-creative`                        |
| Working with a person in Studio, storyboards            | `hyperframes-studio`                          |
| CLI: init, check, preview, render, troubleshooting      | `hyperframes-cli`                             |
| Titles, cover text and video openings (Chinese)         | `dbs-title-cover-intro`                       |
| Polish/tune existing UI motion: durations, easing, stagger | `transitions-polish`                 |
| Visual style for music videos and moody edits (angelcore / hyperpop) | `taste`                    |
| iOS apps: control motorized camera docks / subject tracking (Swift) | `dockkit`                 |
| Talking-head / lip-sync videos via fal.ai (stub, see note) | `fal-lip-sync`                       |
| Remotion (React) video, only when explicitly asked (stub, see note) | `remotion`                   |
| Animation-principles guidance for After Effects / Premiere motion | `video-motion-graphics`      |
| Ad / product / e-commerce video production via fal.ai   | `commercial`                                  |
| UGC-style creator ads, testimonials, founder clips      | `ugc`                                         |
| Campaign kits and paid-social variants                  | `marketing`                                   |
| Multi-shot stories, storyboards, shot lists             | `storytelling`                                |
| Shot language, camera, lighting, colour grade prompts   | `cinematography`                              |
| Prompting a specific fal model / choosing a default one | `fal-prompting`, `model-routing`              |
| Title and outro frames: glitch, light-leak, logo outro  | `frame-glitch-title`, `frame-light-leak-cinema`, `frame-logo-outro` |
| Frame-sequence video (HyperFrames / Remotion style)     | `video-hyperframes`                           |
| Edit existing footage by conversation: transcribe, cut, grade, subtitles, overlays | `video-use` |
| Trim silence and speed up raw screen recordings (FFmpeg) | `raw-video-processing`                |
| Cinematic shot direction for AI video (Veo3 / Kling / Luma via muapi.ai) | `muapi-cinema-director`   |
| Retro pixel-art multi-scene video template (HyperFrames) | `8-bit-orbit-video-template`             |
| Product photo to cinematic video ad via muapi.ai (paid, needs key) | `muapi-product-video-ad-maker`      |
| Client brand interview + reference frames into `MOTION.md` (see note) | `brand-intake`                  |
| Rough idea into a build brief / 8-part Motion prompt    | `motion-brief-writer`, `motion-prompt-writer` |
| Reference reel or ad broken down into a Motion prompt   | `reference-to-motion`                         |
| 16 named UI / data / type motion effects, 8 s loops     | `motion-effects`                              |
| Looping animated chart, count-up, before / after        | `animated-chart`                              |
| Follower / revenue milestone particle reveal            | `milestone-reveal`                            |
| 30–45 s SaaS / offer launch video                       | `launch-video`                                |
| Apple-keynote-style Mac launch film                     | `apple-launch-film`                           |
| Vox-style documentary explainer, 30–60 s                | `vox-explainer`                               |
| Cinematic 3D title sequence (Three.js)                  | `title-sequence-3d`                           |
| Newsletter edition promo clip / looping cover GIF       | `newsletter-promo`, `loop-cover`              |
| Same brief to three AI models, side-by-side comparison  | `model-showdown`                              |
| 16:9 or square video into an upload-ready 9:16 Reel     | `reel-export`                                 |
| Old opening-hook diagnosis, only when asked by name (Chinese) | `dbs-hook` (deprecated)                 |

Note on `brand-intake`: it saves `brand.md` and `MOTION.md` to the project root and adds a
"read MOTION.md first" rule to CLAUDE.md. Our clients each have their own niche and look, so run
it once per client, save both files (and the `examples/` frames) in `brands/<client>/`, and don't
add that rule here.

**Carousels and static graphics:**

| Need                                                    | Skill                                         |
| ------------------------------------------------------- | --------------------------------------------- |
| Carousel structure, slide-by-slide copy, post captions  | `social`                                      |
| Website and landing-page copy, headlines, CTAs         | `copywriting`                                 |
| Content pillars, calendars, what to post and where      | `content-strategy`                            |
| Designing posters, slides and graphics as PNG / PDF     | `canvas-design`                               |
| Still images: social graphics, banners, mockups, OG     | `image`                                       |
| Paid-social ad statics, hooks, ad copy variations       | `ad-creative`                                 |
| AI product photos, lifestyle shots, ad packs (Higgsfield) | `higgsfield-product-photoshoot`             |
| General AI image / video generation (Higgsfield)        | `higgsfield-generate`                         |
| Client brand systems: palette, logo, social templates   | `higgsfield-brandkit`                         |
| YouTube thumbnails, Reel / Shorts covers                | `higgsfield-youtube-thumbnail`                |

All skills except our own are third-party, and their versions are pinned in `skills-lock.json`:

- HyperFrames skills: `heygen-com/hyperframes`
- `image`, `social`, `ad-creative`, `copywriting`, `content-strategy`: `coreyhaines31/marketingskills`
- `higgsfield-*`: `higgsfield-ai/skills`
- `canvas-design`: `anthropics/skills`
- `dbs-*`: `dontbesilent2025/dbskill`
- `transitions-polish`: `jakubantalik/transitions.dev`
- `taste`: `affaan-m/ecc`
- `dockkit`: `dpearson2699/swift-ios-skills`
- `fal-lip-sync`, `remotion`, `frame-*`, `video-hyperframes`: `nexu-io/open-design`
- `video-motion-graphics`: `dylantarre/animation-principles`
- code-built motion pack (`brand-intake`, `motion-brief-writer`, `motion-prompt-writer`,
  `motion-effects`, `animated-chart`, `milestone-reveal`,
  `launch-video`, `apple-launch-film`, `vox-explainer`, `title-sequence-3d`, `newsletter-promo`,
  `loop-cover`, `model-showdown`, `reel-export`, `reference-to-motion`): `charlie947/motion-graphics-skills`
- fal skills (`commercial`, `ugc`, `marketing`, `storytelling`, `cinematography`, `fal-prompting`,
  `model-routing`): `fal-ai-community/skills`

Don't edit them by hand. Update one with:

```bash
npx skills add <source-repo> --skill <name> --agent claude-code -y
```

Our own skills (currently `nxtlvl-social-video`) are ours to edit.

## Setup

- Node.js 22 or newer and FFmpeg.
- Run the CLI as `npx hyperframes ...`.
- The fal skills call the `genmedia` CLI and need a fal.ai account and API key; they spend credits, so confirm the cost before generating.
- `video-use` transcribes with ElevenLabs Scribe: put `ELEVENLABS_API_KEY` in a `.env`, and note that footage audio is uploaded to ElevenLabs. Its Python helpers need `ffmpeg`.
- Voiceover and generated music need a HeyGen account (`npx hyperframes auth`) or a Gemini API key.
- The `higgsfield-*` skills need the `higgsfield` CLI and a Higgsfield account (`higgsfield auth login`);
  each generation spends Higgsfield credits.
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
