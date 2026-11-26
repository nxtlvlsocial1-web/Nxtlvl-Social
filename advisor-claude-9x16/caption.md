# AI.NXTLVL: the advisor strategy in Claude Code (Instagram Reels, 9:16), v1

Recreated from a reference reel (refs/ref_new.mp4: a 38 s talking head on Claude Code's advisor setup, "comment Claude")
with a new script, all-new 3D visuals and our own cast: Nyx (an original AI.NXTLVL robot with the page's violet star on
its antenna) plays the small, fast model; the Advisor (a glass four-point star with eyes) plays Opus and only beams down
at the hard moments. Word-by-word animated captions (each word pops in as it is spoken, the spoken word on a white chip),
a performed voiceover and an Openverse sound-effect set made for this reel.

Build: build/vo_cb.py + build/vo_pick.py + build/relabel.py (voice: Chatterbox with the synthetic Kokoro am_puck
reference, the AI.NXTLVL page voice, performed `say` lines, 4 takes per passage, the clean livelier one picked),
assets/js/scene.js (Three.js stage), build/generate.py (headlines, captions, labels, SFX cues), build/sfx_mix.py (mix).

## Audit of the reference reel

- Hook: "You're literally burning through your tokens" is about the viewer, but there is no number or proof on frame 1.
- Visuals: a talking head, browser screenshots and flat model cards. Nothing moves in depth, and no characters.
- Captions: one plain word at a time, with no animation.
- Facts: two of its claims are not in Anthropic's blog post or docs. It says "cut your usage by 50% or more" (there is
  no 50 % figure) and "it runs your subagents on Haiku" (the docs only say subagents inherit the configured advisor).
  Both are left out here.
- Fixed here: a before/after number on frame 1, a contrast peak at about 6 s, the twist (the big model never types), the
  product named at about 60 %, a real cost number as the last peak, a share trigger, and a keyword that matches the
  topic (ADVISOR).

## Facts used (claude.com/blog/the-advisor-strategy, 2026-04-09, and code.claude.com/docs/en/advisor, read 2026-11-26)

- The advisor pairs Opus as an advisor with Sonnet or Haiku as the executor. The executor runs the task; the advisor
  "never calls tools or produces user-facing output".
- BrowseComp: "Haiku with an Opus advisor scored 41.2%, more than double its solo score of 19.7%."
- SWE-bench Multilingual: Sonnet with an Opus advisor scored 2.7 percentage points higher than Sonnet alone while
  "reducing cost per agentic task by 11.9%". (Anthropic's footnote: Sonnet solo ran with adaptive thinking, the advisor
  run without, so the comparison is not exactly like for like. The script says "in Anthropic's tests".)
- When it consults: "before committing to an approach, when an error keeps recurring, and before declaring a task
  done" (the timing is model-driven).
- Claude Code: `/advisor opus` turns it on and saves `"advisorModel": "opus"` to user settings; `/advisor off` turns it
  off. Experimental; available to subscription and API accounts (Anthropic API, Claude Platform on AWS, Claude Models
  on Google Cloud; not Bedrock, Google's Agent Platform or Foundry).

## Script and arc

| Voiceover | Beat |
|---|---|
| The cheapest model scored 19.7% on a hard research test. Give it an advisor, and it jumps to 41.2%. | hook 70 (before/after formula) + first peak |
| Same cheap model. It just knows when to ask for help. | peak 90 (contrast) |
| Here's the trick. The small, fast model does all the work: it writes the code, runs it, and reads the files. | release (the how) |
| The big model never touches the keyboard. It only steps in at the hard parts: before picking a plan, when the same error keeps coming back, and before calling the job done. | peak (the twist) + save trigger (the three moments) |
| It's Anthropic's advisor strategy, and it's built into Claude Code. One command: /advisor opus. | release, product at ~60 % |
| In Anthropic's tests, Sonnet with an Opus advisor scored higher, and cost 11.9% less per task. | peak (real number) |
| Send this to the friend who runs Opus on everything. | share trigger |
| Comment ADVISOR, and I'll send you the setup. | CTA |

Hook variants to test (Trial Reels):
- A (built): "The cheapest model scored 19.7% on a hard research test. Give it an advisor, and it jumps to 41.2%."
- B (contrarian): "Stop running Opus on everything. Your cheap model just needs an advisor."
- C (test): "Same model. Same test. One setting more than doubled its score."

## Post description (ready to paste)

```
Comment "ADVISOR" and I'll send you the setup.

The cheapest Claude model scored 19.7% on a hard research test. Give it an Opus advisor, and it jumps to 41.2%.

How the advisor strategy works:
1. A small, fast model does all the work: it writes the code, runs it and reads the files
2. Opus never touches the keyboard. It only steps in at the hard parts
3. Before committing to a plan
4. When the same error keeps coming back
5. Before calling the job done

In Claude Code it's one command: /advisor opus

In Anthropic's own tests, Sonnet with an Opus advisor scored 2.7 points higher on SWE-bench Multilingual and cost 11.9% less per task.

Send this to the friend who runs Opus on everything.

Source: Anthropic, "The advisor strategy" (April 2026) and the Claude Code docs.
Music: "Funky Nurykabe (Spinningmerkaba Mix)" by ccMixter, CC BY 3.0
Sounds: "Bubble Pop - High Pitched Short" by elmasmalo1, CC BY 3.0; "Upgrade" by mokasza, CC BY 4.0

#claudecode #anthropic #aitools #aicoding #claude
claude code advisor, advisor strategy, claude opus, claude sonnet, claude haiku, save claude tokens, claude code usage limits, claude code tips, ai coding agent, anthropic claude
```

## Auto-DM for ADVISOR (link and setup only)

```
https://code.claude.com/docs/en/advisor

1. Open Claude Code.
2. Run: /advisor opus
3. Keep working as usual. Your main model now asks Opus at the hard moments.
4. To turn it off: /advisor off
```

Notes:
- When posting: turn on the "AI label" (Advanced settings). The voiceover is synthetic but sounds real.
- Nyx and the Advisor are original AI.NXTLVL characters, not any brand's mascot. No Anthropic logo is used; "Claude
  Code" appears as plain text on the terminal.
- The reference reel was used only as a reference: no face, footage or audio from it is in this video.
- Credits: music CC BY 3.0 (Jamendo 1468789); sound effects from Openverse (plan/sfx_library.json, plan/sfx_credits.txt),
  CC0 except the two CC BY sounds credited in the description.
