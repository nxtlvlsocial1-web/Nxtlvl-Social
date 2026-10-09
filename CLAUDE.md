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

### Marketing, sales and growth

| Need                                                              | Skill                     |
| ----------------------------------------------------------------- | ------------------------- |
| Ad creatives and performance marketing: copy, hooks, ad testing   | `ad-creative`             |
| Full campaign brief: goals, audience, channels, content calendar  | `campaign-plan`           |
| Running a multi-channel campaign or launch end to end             | `marketing-campaign`      |
| Captions, posts, emails, blogs, landing pages, press releases     | `content-creation`        |
| Landing page / conversion audits and A/B test ideas               | `cro-methodology`         |
| Quick CRO checklist: funnels, forms, checkout, A/B test basics    | `conversion-optimization` |
| Finding and qualifying new client leads                           | `lead-research-assistant` |
| Preparing for client pricing, contract or vendor negotiations     | `negotiation`             |
| Persuasive copy, social proof, urgency and trust signals          | `influence-psychology`    |
| Picking competitors / benchmark accounts worth copying            | `dbs-benchmark`           |
| Quiz / scorecard funnels and lead magnets that qualify leads      | `scorecard-marketing`     |
| Guided plan to turn lumpy revenue into a repeatable growth engine | `grow-business`           |
| Full marketing plan, stranger to raving fan (one page)            | `one-page-marketing`      |
| Irresistible offers: bonuses, guarantees, pricing packaging       | `hundred-million-offers`  |
| Outbound B2B sales: cold email, pipeline, qualification           | `predictable-revenue`     |
| Word-of-mouth, shareable content, referral programs               | `contagious`              |
| Going from early adopters to mainstream buyers                    | `crossing-the-chasm`      |
| Network effects, marketplaces, getting first users                | `cold-start-problem`      |
| Picking the one metric that matters, growth analytics             | `lean-analytics`          |
| New client brand strategy: questionnaire, then full report       | `brand-strategy`          |
| Choosing where to grow next: segment, region, channel or product  | `organic-growth-advisor`  |

### Third-party skills

The HyperFrames skills are third-party (from `heygen-com/hyperframes`); their versions are pinned in
`skills-lock.json`. Don't edit them by hand. Update them with:

```bash
npx skills add heygen-com/hyperframes --skill <name> --agent claude-code -y
```

The marketing skills are third-party too, pinned in the same lock file. Don't edit them by hand either;
update one by re-running its install command:

| Skill                     | Source                                |
| ------------------------- | ------------------------------------- |
| `ad-creative`             | `coreyhaines31/marketingskills`       |
| `campaign-plan`           | `anthropics/knowledge-work-plugins`   |
| `content-creation`        | `anthropics/knowledge-work-plugins`   |
| `marketing-campaign`      | `affaan-m/ecc`                        |
| `cro-methodology`         | `wondelai/skills`                     |
| `negotiation`             | `wondelai/skills`                     |
| `influence-psychology`    | `wondelai/skills`                     |
| `scorecard-marketing`     | `wondelai/skills`                     |
| `grow-business`           | `wondelai/skills`                     |
| `one-page-marketing`      | `wondelai/skills`                     |
| `hundred-million-offers`  | `wondelai/skills`                     |
| `predictable-revenue`     | `wondelai/skills`                     |
| `contagious`              | `wondelai/skills`                     |
| `crossing-the-chasm`      | `wondelai/skills`                     |
| `cold-start-problem`      | `wondelai/skills`                     |
| `lean-analytics`          | `wondelai/skills`                     |
| `lead-research-assistant` | `composiohq/awesome-claude-skills`    |
| `dbs-benchmark`           | `dontbesilent2025/dbskill`            |
| `brand-strategy`          | `arnabbagxd/brand-building-skills`    |
| `organic-growth-advisor`  | `deanpeters/Product-Manager-Skills`   |
| `conversion-optimization` | `kostja94/marketing-skills`           |

```bash
npx skills add <source> --skill <name> --agent claude-code -y
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
