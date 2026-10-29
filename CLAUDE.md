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
| Explainer video from a GitHub pull request              | `pr-to-video`                                 |
| Port an existing Remotion project to HyperFrames        | `remotion-to-hyperframes`                     |
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
| Set up brand for motion: brand.md + MOTION.md (read first by the others) | `brand-intake`                    |
| Turn a rough idea into a precise motion build brief     | `motion-brief-writer`                         |
| Break down a reference video or website into a Motion prompt | `reference-to-motion`                    |
| Full 8-part Claude Motion prompt for one short loop     | `motion-prompt-writer`                        |
| 30-45 s product launch video in code                    | `launch-video`                                |
| Showreel-grade product film from an app's own codebase and design system (Remotion) | `product-film`  |
| Mac-style keynote launch film (menu bar, notch, widgets) | `apple-launch-film`                          |
| 30-60 s Vox-style documentary explainer in code         | `vox-explainer`                               |
| Looping animated chart; values stay exactly as given    | `animated-chart`                              |
| Looping milestone count-up (followers, customers, revenue) | `milestone-reveal`                         |
| 16 premium 8-second UI / data / type motion effects     | `motion-effects`                              |
| 8-15 s cinematic 3D title sequence (Three.js)           | `title-sequence-3d`                           |
| Same brief to three AI models, stacked comparison       | `model-showdown`                              |
| 12-20 s promo that drives readers to a newsletter edition | `newsletter-promo`                          |
| Newsletter cover as a seamless looping GIF              | `loop-cover`                                  |
| Any horizontal or square video to 1080x1920 Reel / TikTok | `reel-export`                               |
| Turn screenshots, URLs or "make it feel like this" into a DESIGN.md visual direction | `reference-design-contract` |
| Websites and new pages that look designed, not generated (50 themes, anti-AI-slop checks) | `hallmark`        |
| Research and profile competitors from their URLs (messaging, positioning, look) | `competitor-profiling`   |
| Drive a browser: open pages, take screenshots, pull page content for references | `agent-browser`          |
| Old opening-hook diagnosis, only when asked by name (Chinese) | `dbs-hook` (deprecated)                 |

**3D, animation code and web design:**

| Need                                                    | Skill                                         |
| ------------------------------------------------------- | --------------------------------------------- |
| Three.js scenes: setup, geometry, materials, lighting, textures | `threejs-fundamentals`, `-geometry`, `-materials`, `-lighting`, `-textures` |
| Three.js models, animation, input, shaders, post effects | `threejs-loaders`, `-animation`, `-interaction`, `-shaders`, `-postprocessing` |
| GSAP (official): tweens, timelines, plugins, utils, performance | `gsap-core`, `gsap-timeline`, `gsap-plugins`, `gsap-utils`, `gsap-performance` |
| GSAP scroll animation and framework use                 | `gsap-scrolltrigger`, `gsap-react`, `gsap-frameworks` |
| Copy a reference site's style into a design-DNA JSON and check the rebuild | `design-dna` |
| Timing, easing and Disney's 12 principles before writing motion code | `motion-design` |
| Build an animation the right way: should it animate, curve, duration, exit (Emil Kowalski) | `animate`, `animate-expo` (React Native) |
| Review, audit or find spots for motion in UI code       | `review-animations`, `improve-animations`, `find-animation-opportunities` |
| Janky animation, name an effect, Apple-style motion     | `animation-performance`, `animation-vocabulary`, `apple-design` |
| UI polish and stress tests                              | `emil-design-eng`, `break-ui`, `mobile-native`, `prototype`, `pick-ui-library` |
| Library-specific: Sonner toasts, modern Swift           | `ask-sonner`, `write-swift`                   |
| Motion and micro-interactions on an existing UI (Genjutsu) | `cast`                                     |
| Art direction, design system and build for a new look (Genjutsu) | `paint`                             |
| Whole website or app with parallel agents (Genjutsu; announces its cost first) | `bunshin`              |

HyperFrames compositions already use GSAP, so the `gsap-*` skills apply there too; keep HyperFrames'
own rules (one paused timeline, no `left`/`top` motion) when they differ.

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
- `brand-intake`, `motion-brief-writer`, `reference-to-motion`, `motion-prompt-writer`, `launch-video`, `apple-launch-film`, `vox-explainer`, `animated-chart`, `milestone-reveal`, `motion-effects`, `title-sequence-3d`, `model-showdown`, `newsletter-promo`, `loop-cover`, `reel-export`: `charlie947/motion-graphics-skills`
- `product-film`: `Rieranthony/product-film-skill`
- `hallmark`: `nutlope/hallmark` (its bundled Node scripts, e.g. `sloplint.mjs`, are third-party code; this session's safety check blocked running them)
- `reference-design-contract`, `agent-browser`: `nexu-io/open-design`; `competitor-profiling`: `coreyhaines31/marketingskills`
- `threejs-*`: `CloudAI-X/threejs-skills`; `gsap-*`: `greensock/gsap-skills`; `design-dna`: `zanwei/design-dna`;
  `motion-design`: `LottieFiles/motion-design-skill`; `cast`, `paint`, `bunshin`: `AThevon/genjutsu`
- `animate`, `review-animations` and the other Emil Kowalski skills: `emilkowalski/skills`
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
- `brand-intake` writes `brand.md` and `MOTION.md` into the project. The other `charlie947` motion skills read them first, so run `brand-intake` before any of them.
- Caption timing: local speech models can't download in cloud sessions, so get word timestamps from ElevenLabs Scribe through the ElevenLabs connector (transcription spends credits), then map the approved script words onto them. `agent-browser` needs `npm i -g agent-browser`.
- Genjutsu (`cast`, `paint`, `bunshin`) needs its modules in `.claude/skills/_jutsu/` (copied from the
  repo's `skills/_jutsu`; `npx skills add` does not install them). Update both together. `bunshin`
  spawns subagents and spends a lot of tokens; it states the cost and asks before starting.
- `media-use` can now search Openverse for sound effects. Openverse items carry Creative Commons licences;
  check each one allows commercial use (and credit it if required) before it goes in a client video.
- Telemetry: set `HYPERFRAMES_NO_TELEMETRY=1` to turn it off.

## Repo layout

```
.claude/skills/       Claude Code skills
brands/<client>/      Brand kits: brand.md, logo.svg, fonts/ (see nxtlvl-social-video § 4)
                      Our own two pages: brands/nxtlvl = NXTLVLSOCIAL.AI (comet-star mark),
                      brands/ai-nxtlvl = AI.NXTLVL (the "nxtlvl" wordmark with a violet star)
<project>/            One HyperFrames project per video and aspect ratio, e.g. spring-drop-9x16/
```

## Rules

- Never render a final until the person has approved the preview.
- Run every render detached (`setsid nohup bash <script> > /dev/null 2>&1 < /dev/null &`), never as a time-limited
  background job: 3D renders take hours and a background job is killed at its time limit. When the person asks for the
  final export directly, render it in delivery quality straight away (no draft first).
- Never use music or images we don't have the rights to; source them through `media-use`.
- Keep rendered MP4s out of git; deliver them, don't commit them.
- Never use emojis in post descriptions, captions or hashtag blocks we write for clients (number lists with "1.", not
  emoji digits). Plain text only.
- Start every post description with the video's CTA keyword line (e.g. `Comment "AGENT" and I'll DM you my whole
  setup.`), then the hook and the body; don't repeat the CTA further down.
