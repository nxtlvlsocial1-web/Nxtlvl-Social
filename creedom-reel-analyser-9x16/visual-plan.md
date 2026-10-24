# Creedom Reel Analyser: visual plan v1

1080x1920 · 30 fps · ~33.5 s (VO 32.1 s + 1.4 s end hold) · voiceover: ElevenLabs Nota 3 take
`ElevenLabs_2026-10-24T22_01_18_V_eleven_v4.mp3` · built in HyperFrames.

## References and what we take from them

Two @ai.nxtlvl reels (36 s "Limit hit by lunch?" dark, 38.6 s "STOP paying for every Claude Code token" light):

- **Layout:** top status row ("● AI.NXTLVL" left, progress pill right); headline block at the top; one hero object
  in the middle; the mascot reacting beside it; word-by-word captions at the bottom.
- **Headline:** heavy sans plus one italic-serif accent word ("Limit hit by *lunch?*", "Lasted the whole *day.*").
- **Captions:** one word at a time, with the active word in a filled pill.
- **Hero objects:** clean UI cards with soft shadows (Claude usage card, router card, terminal); big serif numerals
  that count ("0.0B → 7.4B", "+1.6B"); faint giant numerals or words in the background.
- **Mascot:** the pixel character does something on almost every line (reacts, carries, points, thinks).
- **CTA:** a "COMMENT" chip, a big keyword pill, a comment box typing the keyword, then the IG logo and @AI.NXTLVL.
- **Light reel's background:** warm paper with a faint dot grid and floating code glyphs. It's the closer match to
  Creedom, so it's our base. We borrow the dark reel's look for one beat only (the twist).

## Creedom look (sampled from the app screenshots)

| Token | Value | Use |
|---|---|---|
| Paper | `#F6F6F4` | background (+ faint dot grid) |
| Ink | `#0B0B0B` | score card, chat bubbles, CTA button |
| Pink | `#EE688B` | progress bars, active caption pill, accents |
| Deep pink | `#B1476B` on `#FEF8FA` | inline chips ("YouTube Agent Skill" style) |
| Mascot pink | `#F343A2` | the bird; glow behind it |
| Green | `#3E8E62` | ticks, "Very good" bar |
| Amber | `#C8902E` | the "3/5" timeline dot |
| Type | Serif display (Fraunces) for numbers and serif lines like "Give me 20 seconds."; heavy sans (Manrope 800) for headlines and captions; mono for small labels ("READING @AI.NXTLVL") |

## The mascot (the pink bird) is the lead

Asset: `d146181c-image.png` (waving pose, transparent). On its own it gives us hop, squash and stretch, tilt, wing
wiggle, peeking from behind cards, and spin. I add vector props and overlays:

- magnifying glass (Creedom's own "reading" pose)
- "?" and "!" thought bubbles
- blink lids
- sweat drop
- sparkles
- a pink glow under it

It moves through the whole video like the reference characters do: it's never a static sticker.

Extra poses would make it much better (thinking, magnifier, cheering, pointing). See question 1 at the end.

## Scene by scene (times are the VO's real phrase timings)

| # | Time | VO | Headline (accent in pink italic serif) | Hero visual + motion | Mascot |
|---|---|---|---|---|---|
| 1 | 0.0–3.3 | One reel did 85x my usual views | One reel. ***85x.*** | A reel card (phone-shaped thumbnail of the YouTube Agent Skill reel) slams in. Its play counter rolls 0 → **126,000+** while a spike chart shoots up. Hearts and play icons burst out like the coins in ref 2. Camera punch-in on "85". | Pops up from the bottom on beat one, eyes wide, wings flapping, riding the spike. |
| 2 | 3.3–5.3 | ...and I had no idea why | No idea ***why.*** | The counter freezes and desaturates. A faint giant "?" sits in the background. | Lands, tilts its head, blinks twice. A "?" bubble pops above it (ref 2's "CODE" bubble style). |
| 3 | 5.5–8.9 | The next one? A few thousand. Numbers... | The next one? ***~3K.*** | A second reel card slides in beside the first. Its counter crawls and stalls at **2,9xx**, with a red down-arrow chip. | Droops (squash down), with a sweat drop. |
| 4 | 8.9–10.5 | ...never reasons. | Numbers ≠ ***reasons.*** | A messy analytics grid flies in (plays, reach, saves, watch time), shakes, then blurs out. | Shrugs: a quick left-right wing wiggle. |
| 5 | 10.5–13.7 | So I gave my page to Creedom. Twenty seconds. | Give me ***20 seconds.*** (Creedom's own line, in serif) | Pink wipe into the Creedom app screen: bird logo + "creedom", "READING @AI.NXTLVL" in mono, the pink progress bar filling, "Public data only". Then the white ticks card: Found Nxtlvl.ai: 6,205 followers ✓ · Scanned 6 recent posts ✓ · Creator audit ready ✓. | Takes the magnifier and scans across the card (the app's own "reading" pose). |
| 6 | 13.7–17.0 | Content score. 82 out of 100. | Content ***score.*** | The 6 post thumbnails (cropped from the screenshot) fly into a 3+3 grid, then fold into the black score card. "YOUR CONTENT SCORE" counts **0 → 82** in big serif, "/100", and a pink ring fills. | Perched on top of the black card, it cheers on "82": bounce + sparkles. |
| 7 | 17.0–21.2 | Then its reel analyser watched my reel... second by second. | Reel ***analyser.*** | The chat screen. A black user bubble slides up ("Check 'Comment TRADE and I'll DM you all 11 skills.'"), then a "CREEDOM · ON IT" card ticks through its three steps. A reel thumbnail gets a playhead scan line. Then the **SECOND BY SECOND** timeline draws down: Hook 0:00–0:05 · Skills grid 0:05–0:19 · Time machine 0:19–0:34 · Safety & Congress 0:34–0:41 · Close. | Rides the playhead down the timeline. |
| 8 | 21.2–26.0 | ...and found what I'd missed... my best hook was buried at 34 seconds. | Buried at ***0:34.*** | **Twist beat.** The room dims to a warm dark (ref 1's look) and everything else fades. The 0:34 segment glows pink with a "BEST HOOK" chip. It lifts out of the timeline and flies up to the 0:00 slot with a whoosh. A small chip reads "4.2/5 · Very good" (on screen only, not spoken). | Magnifier on the 0:34 row, then a "!" bubble. It jumps back in surprise, then follows the segment up. |
| 9 | 26.2–29.4 | Now I edit with reasons. Not guesses. | ***Reasons*** > guesses. | Lights back up. Split card: left "GUESSES" (a tumbling dice icon, crossed out) vs right "REASONS" (Creedom's real fixes: "Lead with the Congress tracker" ✓, "Trim two tool cards at 0:10–0:19" ✓). | Hops from the left card to the right one and lands happy. |
| 10 | 29.4–33.5 | Comment CREEDOM and I'll DM you the link. | (none; the CTA is the headline) | A black "COMMENT" chip, then a big pink **CREEDOM** pill slams in. A comment box types C-R-E-E-D-O-M, and the send button pulses. Small floating keyword chips drift around (no fake usernames). It ends on the IG logo + @AI.NXTLVL. | Holds a "CREEDOM" thought bubble, points at the box, then waves goodbye (its original pose) on the end card. |

## Always on

- **Top row:** "● AI.NXTLVL" (mono) on the left. On the right, a pill with the bird icon whose bar fills pink with
  the video's progress (ref 1's progress pill).
- **IG icon + @AI.NXTLVL:** small, mid-right, as in both references.
- **Captions:** word by word, heavy sans, bottom third, inside the safe zone (above y≈1520). The active word sits in
  a pink pill, the rest in ink.
- **Background:**
  - paper `#F6F6F4` with a faint dot grid;
  - a faint giant serif numeral per scene (85x, ?, 3K, 20, 82, 0:34);
  - a few slow-drifting glyphs (▶, ♥, %, 0:00).
- **Transitions:** cut on the voice, with the reference's quick moves (card slams with spring overshoot, push-ins on
  key numbers, one pink wipe at the Creedom reveal, one dim to dark for the twist).

## Sound

- **Music:** an original upbeat lo-fi/pop bed, synthesized (no rights issues), ducked under the VO.
- **SFX:** pop on each card, tick per green check, counter rattle, whoosh on the hook lift, sparkle on 82, keyboard
  clicks for the CTA typing, soft "ding" on send.

## Production notes

- **Caption timing:** the voiceover's phrase timings are measured (from pauses plus a local transcription). Words
  are spread across each phrase, which is close but not exact. For perfectly locked captions, the ElevenLabs
  connector can return word timestamps (uses a few transcription credits).
- **Numbers:** every number shown comes from the user's Creedom screenshots. "4.2/5" and the 6,205 followers are
  shown, not spoken.
- **Process:** build → preview frames → your approval → final render.

## Open questions

1. **More mascot poses?** I only have the waving bird. Options:
   - (a) you send Creedom's other mascot images (the magnifier pose, etc.);
   - (b) I generate 4–5 matching poses with an AI image tool (costs credits; I'd confirm the price first);
   - (c) I animate the one pose plus vector props, as planned above.
2. **Background:** light Creedom paper throughout with one dark twist beat (planned), or fully dark like the
   "Limit hit by lunch?" reel?
3. **Website:** creedom.ai doesn't load from my sandbox. If you want site copy or visuals on screen, send screenshots.
