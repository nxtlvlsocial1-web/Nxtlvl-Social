# NXTLVLSOCIAL.AI: 5 free Claude Code plugins (Instagram Reels, 9:16, 52.5 s), v1

Owner: "Audit this reel and recreate this reel like this, take visuals from this reel for nxtlvl." Reference:
refs/ref_34964.mp4 (48 s, a creator's talking head over GitHub screenshots, "25 best Claude Code plugins", comment
"Claude"). The reference's own footage (the creator, his edit) is not reused (CLAUDE.md: reels are references only). Its
look is rebuilt from our own material: fresh captures of the same public pages (build/capture.cjs,
build/capture_targets.cjs), a light grid-paper page, browser-window cards with the real URLs, a zoom onto the sentence that
proves each line with a selection frame and handles, keyword chips, word-by-word captions. In NXTLVLSOCIAL.AI colours
(brands/nxtlvl: violet, ink, the comet-star mark on a dark chip).

Build: build/vo_cb.py + vo_pick.py + relabel.py (voice: Chatterbox with the synthetic Kokoro am_puck reference, performed
`say` lines, 4 takes per passage, clean livelier take picked, 1.1x), build/generate.py, build/sfx_mix.py.

## Audit of the reference

- Hook: "25 best Claude Code plugins ... 10 times better ... all free". Strong list-and-number hook, but "10 times
  better" is unprovable and only 5 of the 25 are shown (the CTA sells "20 more I couldn't fit").
- Visuals: a talking head in the bottom half, GitHub screenshots in a card above, a blue keyword chip, word captions.
  Clean and readable; the face does most of the work.
- Claims checked against each README (most are overstated):
  1. Ponytail "cuts usage by over 50%": not stated. Its own benchmark says -53% code, -26% cost, -45% output tokens,
     -41% time, accuracy level (hidden checks 95.6% vs 96.7%).
  2. "Unslopped" is heydamir/unslop (CC BY 4.0, 22.8k stars).
  3. Elephant-Goldfish "stops buggy code": not stated (it reviews specs before coding; "A review does not replace tests or
     human judgment"). "Google's engineers use it every day" is true per Google's Open Source Blog (22 Oct 2026); the repo
     says it is "not an officially supported Google product".
  4. Agent Reach "scrape LinkedIn, Instagram, X, Reddit for free": LinkedIn is job listings only, Instagram and X are
     "experimental", all through your own logins; speech-to-text needs a paid key; it is read-only.
  5. Claude Code Setup "removes the useless stuff": false. "This skill is read-only - it analyzes but doesn't modify files."
- Fixed here: 5 plugins, all claims as their sources state them, a source line on every number, a real star count on frame
  1, a share trigger, a CTA keyword that delivers exactly what is promised (all five links).

## Script and arc

| Voiceover | Beat |
|---|---|
| Five free Claude Code plugins, and the first one has 200,000 stars on GitHub. | hook 70 (number on frame 1: "200.3k stars" framed) |
| Number one, Ponytail. It makes Claude code like the laziest senior dev in the room. In its own tests: about half the code, a quarter cheaper, same accuracy. | first peak |
| Two, Unslop. It strips the purple gradients and emoji labels out of vibe-coded apps, and makes them look designed. | release |
| Three, Elephant-Goldfish, open-sourced by Google. Fresh reviewers check the plan before any code gets written. Google says thousands of its engineers use it every day. | peak |
| Four, Agent Reach. It lets your agent read YouTube, GitHub and Reddit through your own logins, and it never posts. | release |
| And five, Claude Code Setup, from Anthropic. It scans your codebase and recommends the hooks, skills and MCP servers that fit. | peak (official plugin) |
| Send this to the friend still running Claude Code with zero plugins. | share trigger |
| Comment PLUGINS, and I'll send you all five. | CTA |

Hook variants to test:
- A (built): "Five free Claude Code plugins, and the first one has 200,000 stars on GitHub."
- B: "This one prompt makes Claude write half the code. It's the first of five free plugins."
- C: "Thousands of Google engineers use plugin number three every day."

## Post description (ready to paste)

```
Comment "PLUGINS" and I'll send you all five links.

Five free Claude Code plugins, and the first one has 200,000 stars on GitHub.

1. Ponytail: makes Claude code like the laziest senior dev in the room. In its own benchmark: 53% less code, 26% lower cost, same accuracy
2. Unslop: strips the purple gradients and emoji labels out of vibe-coded apps and makes them look designed
3. Elephant-Goldfish: open-sourced by Google. Fresh reviewers check your plan before any code is written. Google says thousands of its engineers use it every day
4. Agent Reach: lets your agent read YouTube, GitHub and Reddit through your own logins. Read-only, it never posts
5. Claude Code Setup: an official Anthropic plugin that scans your codebase and recommends the hooks, skills and MCP servers that fit

Send this to the friend still running Claude Code with zero plugins.

Music: "Funky Nurykabe (Spinningmerkaba Mix)" by ccMixter, CC BY 3.0
Sounds: "Bubble Pop - High Pitched Short" by elmasmalo1, CC BY 3.0; "Upgrade" by mokasza, CC BY 4.0

#claudecode #claude #aitools #aicoding #anthropic
claude code plugins, best claude code plugins, free claude code plugins, claude code skills, ponytail claude, unslop, elephant goldfish model, agent reach, claude code setup, ai coding tools
```

## Auto-DM for PLUGINS (links and setup only)

```
1. Ponytail: https://github.com/DietrichGebert/ponytail
   In Claude Code: /plugin marketplace add DietrichGebert/ponytail
   then: /plugin install ponytail@ponytail

2. Unslop: https://github.com/heydamir/unslop
   In a terminal: claude plugin install unslop --marketplace heydamir/unslop

3. Elephant-Goldfish: https://github.com/google/elephant-goldfish-model
   In a terminal: claude plugin marketplace add google/elephant-goldfish-model
   then: claude plugin install egm@egm (start a new session after)

4. Agent Reach: https://github.com/Panniantong/Agent-Reach
   Send your agent: Install Agent Reach: https://raw.githubusercontent.com/Panniantong/Agent-Reach/main/docs/install.md

5. Claude Code Setup: https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-code-setup
   In Claude Code: /plugin install claude-code-setup@claude-plugins-official
   then ask: recommend automations for this project
```

Notes:
- When posting: turn on the "AI label" (Advanced settings); the voiceover is synthetic but sounds real.
- Star counts are from the pages on 2026-11-28 (Ponytail 200.3k, Unslop 22.8k, Agent Reach 115k); recheck on posting day.
- The screenshots are our own captures of public pages, used to show what the reel talks about. No logo of Anthropic or
  Google is used as our branding; names appear as plain text.
- Agent Reach reuses your own browser logins for gated sites; its README advises a secondary account because platforms may
  restrict automated accounts. Unslop's generated hero images use paid services, and it asks before each one.
- The Claude Code Setup install line follows the official marketplace's `/plugin install {name}@claude-plugins-official`
  pattern (the plugin also appears under /plugin > Discover).
- Credits: music CC BY 3.0 (Jamendo 1468789); sound effects from Openverse (plan/sfx_library.json, plan/sfx_credits.txt),
  CC0 except the two CC BY sounds credited above.
