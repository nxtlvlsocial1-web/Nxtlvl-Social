# Fight Night (the /court skill as a boxing match): script v1

Reference: the "I built a courtroom where 12 Claudes put your idea on trial" reel. Our version takes the same skill
(`/court` by Alex Chen, @nocodealex, MIT, free: github.com/alexyc9381/court-skill) and stages it as a fight night in a
3D voxel world with the orange pixel mascot. The README welcomes videos as long as the skill is credited and
@nocodealex is tagged.

LENGTH: ≤35 s · ~90 words (fast commentator pace) · VOICE: male fight commentator / ring announcer (user's own voice, Eleven v3 tags) · CTA KEYWORD: FIGHT (to confirm)

## How the fight maps to the skill (keeps every claim true)

| Skill | On screen |
|---|---|
| Prosecutor: "strongest honest case that your idea fails" | Red corner: IT'LL FAIL |
| Defense: "strongest honest case that it works" | Blue corner: IT'LL WORK |
| Openings, then rebuttals | Round 1, Round 2 |
| 12 jurors with personas, voting independently ("no juror sees another's vote") | 12 ringside judges behind dividers |
| Judge: verdict, charges that stuck, conditions for acquittal | Referee's decision and the "rematch checklist" |

## Script v2 (ring announcer, cut to fit 35 s; v1 ran 42 s)

| Beat | Time | Voiceover |
|---|---|---|
| Hook | 0–4s | Ladies and gentlemen... two Claudes, one idea. Only one leaves the ring! |
| Problem | 4–6s | Claude alone agrees with everything. |
| Corners | 6–11s | Red corner: a Claude arguing it FAILS! Blue corner: one arguing it WORKS! |
| Rounds | 11–14s | Openings! Rebuttals! Every point lands! |
| Judges | 14–17s | Twelve Claude judges score it blind. |
| Example | 17–22s | Tonight: quit nursing to sell candles... KNOCKOUT! |
| Payoff | 22–27s | Then the referee tells you what to fix for the rematch. |
| CTA | 27–31s | Free! Comment FIGHT for the skill! |

~67 words (v1 was ~90).

## Voiceover with mood tags (Eleven v3)

```
[booming announcer voice] Ladies and gentlemen... two Claudes, one idea. [shouting] Only one leaves the ring!
[wry] Claude alone agrees with everything.
[hyped] Red corner: a Claude arguing it FAILS! [hyped] Blue corner: one arguing it WORKS!
[fast-paced] Openings! Rebuttals! Every point lands!
[intense] Twelve Claude judges score it blind.
[dramatic] Tonight: quit nursing to sell candles... [shouting, ecstatic] KNOCKOUT!
[calm] Then the referee tells you what to fix for the rematch.
[hyped] Free! [booming] Comment FIGHT for the skill!
```

Delivery: big ring-announcer energy on the hook and corners, fast play-by-play through the rounds, one held beat
before KNOCKOUT, calm on the payoff, punchy CTA. Eleven v3, Stability "Creative", 3–4 takes; any take still over
35 s can be sped up 1.05–1.1x in the edit.

## Visual beats (3D voxel world, orange pixel mascot)

| Time | Visual |
|---|---|
| 0–3s | Dark arena; spotlights slam on; two voxel mascots in red and blue gloves bump fists; the big screen reads "QUIT NURSING TO SELL CANDLES?"; "ROUND 1" card |
| 3–6s | A lone mascot in front of a mirror nods at everything: speech bubbles "Genius!", "Love it!", "YES!" |
| 6–11s | Fighting-game VS screen: "THE PROSECUTOR · IT'LL FAIL" (red) vs "THE DEFENSE · IT'LL WORK" (blue), health bars full |
| 11–14s | Exchange of punches; each hit carries a real argument from the example: "Savings cover ~5 months of rent" (red), "40 sales at $28 already" (blue); health bars drop; ROUND 2 |
| 14–19s | Camera cranes over the ring: 12 voxel judges ringside, each with a prop (calculator, shopping bag, briefcase, gavel, skateboard, wrench...), cards hidden behind dividers |
| 19–25s | Cards flip to red; slow-motion uppercut; "K.O." slam; the idea card on the big screen shatters |
| 25–30s | Referee raises the red glove and unrolls the rematch checklist (the skill's real conditions): "Reach ~57 sales/month" · "Get your rehire in writing" · "Landlord OK + liability insurance" |
| 30–34s | A championship belt engraved FIGHT; comment box types FIGHT; the mascot winks |

## Facts on screen (from the repo)

- Workflow, personas, "no juror sees another's vote", free, MIT, "not made by Anthropic", "a structured second opinion,
  not legal, financial or professional advice": README.
- Candles case, punches and rematch checklist: `examples/candles/VERDICT.md`. That example was a **3-juror run (3–0)**,
  so the scorecard shows "3 judges · 3–0". The 12-judge line describes the default setting, not that run.

## Cover

`cover.html` reuses the 3D arena (fight.js poses the fighters when `window.FIGHT_COVER` is set). Snapshot it with
`node build/cover.cjs` → `renders/nxtlvl_fight-night_reels_9x16_cover.png` / `.jpg`. All text sits between y 268 and
1630, so the 4:5 and 3:4 grid crops keep it.

## Caption

Two Claudes. One idea. Only one leaves the ring. 🥊

Ask one AI about your idea and it'll call it genius. So we made them fight:
🔴 Red corner argues it'll FAIL
🔵 Blue corner argues it'll WORK
⚖️ 12 Claude judges score it blind, then the referee tells you exactly what to fix before the rematch.

It's a free Claude Code skill called /court.
Comment FIGHT and I'll DM you the link.

Skill by @nocodealex (free, MIT). A second opinion, not legal, financial or professional advice.

#claudeai #claudecode #aitools #startupideas #buildinpublic #founders #ai
