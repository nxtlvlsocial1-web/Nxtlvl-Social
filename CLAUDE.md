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
| SEO audit or fixes for a site we build                  | `seo` (routes to `seo-audit`, `seo-page`, …)  |
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
| Old opening-hook diagnosis, only when asked by name (Chinese) | `dbs-hook` (deprecated)                 |

**Carousels and static graphics:**

| Need                                                    | Skill                                         |
| ------------------------------------------------------- | --------------------------------------------- |
| Carousel structure, slide-by-slide copy, post captions  | `social`                                      |
| Website and landing-page copy, headlines, CTAs         | `copywriting`                                 |
| Remove AI slop from captions, scripts, emails, site copy | `zero-slop`                                 |
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
- `zero-slop`: `manavmishra/ZeroSlop`, the portable skill only. Install or update it with
  `npx skills add https://github.com/manavmishra/ZeroSlop/tree/main/skills/zero-slop --agent claude-code -y`; the repo root brings
  the author's development files (including their own CLAUDE.md). Its scripts are local; never run its remote `deslop` service unasked.
- fal skills (`commercial`, `ugc`, `marketing`, `storytelling`, `cinematography`, `fal-prompting`,
  `model-routing`): `fal-ai-community/skills`

Don't edit them by hand. Update one with:

```bash
npx skills add <source-repo> --skill <name> --agent claude-code -y
```

The `seo*` skills and `.claude/agents/seo-*.md` are third-party too ([claude-seo](https://github.com/AgriciDaniel/claude-seo)
v2.5.0, copied in with `${CLAUDE_PLUGIN_ROOT}` paths rewritten to `.claude/skills/...`). Build its Python runtime once per
machine with `.claude/skills/seo/scripts/claude-seo setup`; run its scripts with `.claude/skills/seo/scripts/claude-seo run <script>.py`.

The design and UI skills (`ui-ux-pro-max`, `frontend-design`, `design-taste-frontend`, `web-design-guidelines`, `impeccable`,
the `plugin87/ux-ui-agent-skills` set such as `critique`, `a11y-audit`, `design-review`, and others listed in `skills-lock.json`)
are third-party as well. Don't edit them by hand; update them with `npx skills update -p -y`.

The `plugin87/ux-ui-agent-skills` set expects its shared kit (tokens/, workflows/) at the repo root, which `npx skills add` does
not install; without it those skills only apply their SKILL.md rules.

Our own skills (currently `nxtlvl-social-video`) are ours to edit.

## Setup

- Node.js 22 or newer and FFmpeg.
- Run the CLI as `npx hyperframes ...`.
- The fal skills call the `genmedia` CLI and need a fal.ai account and API key; they spend credits, so confirm the cost before generating.
- Voiceover and generated music need a HeyGen account (`npx hyperframes auth`) or a Gemini API key.
- The `higgsfield-*` skills need the `higgsfield` CLI and a Higgsfield account (`higgsfield auth login`);
  each generation spends Higgsfield credits.
- Telemetry: set `HYPERFRAMES_NO_TELEMETRY=1` to turn it off.
- Seeing a reel from its link: `python3 tools/see_link.py URL --ears` (yt-dlp; frames, transcript, sound timeline).
  Never use the owner's cookies or pose as a browser; for a refused link, ask for the file and run `--file VIDEO.mp4`.
  Downloaded reels are references only, never reused.
- Pexels stock clips by id without an API key: `python3 tools/pexels_fetch.py` (prefer UHD sources).

## Repo layout

```
.claude/skills/       Claude Code skills
brands/<client>/      Brand kits: brand.md, logo.svg, fonts/ (see nxtlvl-social-video § 4); brands/nxtlvl/ is our own logo kit,
                      brands/nxtlvl-edits/ the editing account's logo kit (the N Disc, brand.md) and concepts
website/              Our site (generated: don't hand-edit the .html): home, service pages (ai-marketing, ai-automation,
                      creative-studio, website-development), about, contact, 404, site.css, site.js, fonts/, icons,
                      og-image.png, manifest, robots.txt, sitemap.xml, llms.txt, _headers, _redirects (old URLs);
                      deployed by the Worker in backend/, step by step in DEPLOY.md
website-src/          Source of the site: build.py holds all page copy and schema; edit there, then
                      `python3 website-src/build.py`. SEO-GROWTH-PLAN.md is the ranking roadmap
backend/              Cloudflare Worker: serves website/ and the Book-a-call API (POST /api/book -> connect@nxtlvlsocial.ai
                      via Resend); npm test runs it locally, npm run deploy ships it. See backend/README.md
nxtlvl-social-audit/  SEO audit of website/index.html: FULL-AUDIT-REPORT.md, ACTION-PLAN.md, PDF, findings/
knowledge/            Client context exported from earlier sessions (briefs, scripts, brand rules, open items); index in
                      knowledge/README.md. Read the client's files before starting work for them
motion-canvas/        Motion Canvas project (code-driven animation in TypeScript): npm install, npm start
tools/               see_link.py (see a reel from its link), pexels_fetch.py (stock clips by id)
<project>/            One HyperFrames project per video and aspect ratio, e.g. spring-drop-9x16/
```

## Repeat clients

Before any video for these clients, read their kit in `brands/<client>/` (`brand.md` = look, `workflow.md` = process,
settings, past mistakes and the checklist for the next video) and reuse their project code as the template.
Their brief, verbatim feedback, scripts, footage list, hooks / CTAs and open items are private and live in the
`nxtlvl-client-memory` account skill, not in this public repo; load it too when it is available.

| Client | Kit | Template project |
| --- | --- | --- |
| Dr S Kokila (English talking-head reels with reference footage) | `brands/dr-kokila/` | `kokila-peace-9x16/` |
| Kanav Kesar / The Conscious Millionaire (Hinglish talking-head ads) | `brands/kanav-kesar/` | `surrender-ad-9x16/` |

Media (footage, music, renders) is not in git; ask for the raw camera files again.

## Rules

- Never render a final until the person has approved the preview.
- Never use music or images we don't have the rights to; source them through `media-use`.
- Keep rendered MP4s out of git; deliver them, don't commit them.
- Run every render detached (`setsid nohup bash <script> > /dev/null 2>&1 < /dev/null &`), never as a time-limited
  background job; render scripts stop when the picture render fails, and check every final's frames before sending.
- Sound effects: Openverse first (CC0 or CC BY only, never NC, ND or SA; record title, creator, licence and link; credit
  CC BY in the post), mixed with the `real-sfx` skill. Freesound preview files (`cdn.freesound.org/previews/...`)
  download from cloud sessions; never fake a browser. Only when downloads are refused, use the CC0 OpenGameArt packs
  (`spin-bout-u-drake/build/oga_sfx.py`) and say so.
- No emojis in post descriptions, captions or hashtag blocks we write for clients. Plain text, lists numbered "1.".
