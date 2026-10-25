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

## Script (ring announcer / play-by-play commentator)

| Beat | Time | Voiceover |
|---|---|---|
| Hook | 0–3s | Ladies and gentlemen... two Claudes. One idea. Only one leaves the ring! |
| Problem | 3–6s | See, Claude on its own agrees with everything you say. |
| Corners | 6–12s | So tonight, in the red corner... a Claude arguing your idea FAILS! And in the blue corner... one arguing it WORKS! |
| Rounds | 12–15s | Openings! Rebuttals! Every point lands a punch! |
| Judges | 15–20s | Ringside, twelve Claude judges score it blind... an accountant, a customer, a competitor... |
| Example | 20–25s | Tonight's challenger: quit nursing to sell candles. OH, it's a knockout! |
| Payoff | 25–30s | And the referee hands you exactly what to fix... before the rematch. |
| CTA | 30–34s | It's free! Comment FIGHT... and I'll DM you the skill! |

## Voiceover with mood tags (Eleven v3)

```
[booming announcer voice] Ladies and gentlemen... [dramatic pause] two Claudes. One idea. [shouting] Only one leaves the ring!
[wry, conversational] See, Claude on its own... agrees with everything you say.
[hyped] So tonight, in the red corner... [shouting] a Claude arguing your idea FAILS!
[hyped] And in the blue corner... [shouting] one arguing it WORKS!
[fast-paced, excited] Openings! Rebuttals! [intense] Every point lands a punch!
[low, intense commentary] Ringside, twelve Claude judges score it blind... [quick] an accountant, a customer, a competitor...
[dramatic] Tonight's challenger: quit nursing to sell candles. [pause] [shouting, ecstatic] OHHH, it's a KNOCKOUT!
[calm, slower] And the referee hands you exactly what to fix... [knowing] before the rematch.
[hyped] It's free! [booming] Comment FIGHT... [grinning] and I'll DM you the skill!
```

Delivery: big ring-announcer energy on the hook and the corner intros, fast play-by-play through the rounds, a hushed
build before the knockout call, then calm and warm on the payoff so the CTA lands. Settings: Eleven v3, Stability
"Creative" so the shouts come through; generate 3–4 takes. If it runs past 35 s, cut "an accountant, a customer, a
competitor" (the judges' props show it anyway).

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

## Caption (draft)

Two Claudes. One idea. Only one leaves the ring. 🥊
Comment FIGHT and I'll DM you the free skill.

/court puts your idea through a real fight: prosecution vs defense, 12 blind judges, and a referee who tells you
exactly what to fix.
Skill by @nocodealex (free, MIT). Not legal, financial or professional advice.
#claudeai #aitools #claudecode #startupideas #buildinpublic
