# Content calendar: Creedom and Creators 100X

Knowledge export for Nxtlvl Social. Covers every reel, PDF and guide made, in progress or planned for Creedom
(creedom.ai, mascot Cree) and the Instagram page Creators 100X (@creators.100x), plus the Creedom reels made for the
NXTLVL pages. Written 2026-11-17.

## Index

1. [How to read this file](#1-how-to-read-this-file)
2. [Summary table](#2-summary-table)
3. [Timeline by date](#3-timeline-by-date)
4. [Item details](#4-item-details)
   - [4.1 Creedom Reel Analyser (drafts only)](#41-creedom-reel-analyser-my-reel-did-85x-my-usual)
   - [4.2 Creedom explainer (CREE)](#42-creedom-explainer-cree)
   - [4.3 Hook reel / reel-flop (HOOK)](#43-hook-reel--reel-flop-hook)
   - [4.4 PDF: 20 Hooks That Work](#44-pdf-20-hooks-that-work-hook)
   - [4.5 STUDY manga reel (STUDY) and PDF: 5 Study Prompts](#45-study-manga-reel-study-and-pdf-5-study-prompts)
   - [4.6 Creedom CHECK reel (CHECK)](#46-creedom-check-reel-check)
   - [4.7 Creedom 3D storytelling guide](#47-creedom-3d-storytelling-guide-pdf)
   - [4.8 Cree 3D model sheet and reference pack](#48-cree-3d-model-sheet-and-reference-pack)
   - [4.9 Prompt reel "Stop typing 'write me a script'" (PROMPT) and PDF: 10 Prompts](#49-prompt-reel-stop-typing-write-me-a-script-prompt-and-pdf-10-prompts)
   - [4.10 Riya paper cut-out story (PROMPT)](#410-riya-paper-cut-out-story-prompt)
   - [4.11 Creedom @write-script reel (SCRIPT)](#411-creedom-write-script-reel-script)
5. [Backlog: ideas not made yet](#5-backlog-ideas-not-made-yet)

---

## 1. How to read this file

- Times are UTC, taken from the chat timestamps. Git dates are commit dates (`git log --date=short`).
- "Request" = the owner's first message asking for the item. "Preview" = a draft render sent for review. "Final" =
  the delivery-quality render sent to the owner.
- **Posting date: UNKNOWN for every item.** No posting date, link to a live post, or performance number (views, likes,
  follows, DMs) was ever reported for Creedom or Creators 100X.
- Status values: **final delivered**, **waiting on approval**, **parked** (stopped with no final and no decision),
  **delivered (guide)**.
- Pages: "Creators 100X" = @creators.100x. "NXTLVL" = one of the owner's own pages (NXTLVLSOCIAL.AI or AI.NXTLVL);
  where the exact page is not stated, it says so.
- Quotes are verbatim, typos kept. "UNKNOWN" = not in any source. "UNCERTAIN" = inferred, not confirmed.
- Sources: *scratchpad/notes_chat.md* (chat), *scratchpad/notes_creedom_files.md* (repo files),
  *scratchpad/notes_c100x.md* (Creators 100X files), the project folders in `/home/user/Nxtlvl-Social/`, and git log.

---

## 2. Summary table

| # | Item | Brand / feature | Page | Project folder | CTA keyword | Request | Final | Status | Posting |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Reel Analyser "My reel did 85x my usual" | Creedom: reel analyser + content score | AI.NXTLVL (UNCERTAIN) | `creedom-reel-analyser-9x16/` | CREEDOM (v1: CREE) | before 2026-10-24 (UNKNOWN exact) | NOT FOUND (drafts 1-6, 2026-10-24/25) | parked / UNKNOWN | UNKNOWN |
| 2 | Explainer "This AI told me the exact second people stopped watching my reel" | Creedom: Reel Analyzer + free account audit | NXTLVL (file prefix `nxtlvl_`; which NXTLVL page UNKNOWN) | `creedom-explainer-9x16/` | CREE | 2026-11-10 10:26 | v10: 2026-11-11 00:48; cover 2026-11-11 12:45 | final delivered | UNKNOWN |
| 3 | Hook reel "This video already lost you" | Creators 100X: hooks / first 3 s | Creators 100X per later references (files named `nxtlvl_`, UNCERTAIN) | `reel-flop-9x16/` | HOOK | 2026-11-11 09:12 | v13: 2026-11-12 08:51; cover 08:55 | final delivered | UNKNOWN |
| 4 | PDF "20 Hooks That Work" | Creators 100X lead magnet | Creators 100X | `brands/creators-100x/pdf/` | HOOK | 2026-11-12 08:57 | 2026-11-12 09:01 | final delivered (not hosted) | n/a |
| 5 | STUDY manga reel "I made the hardest chapter ... into a manga" | Creators 100X: AI study prompts | Creators 100X | `study-manga-9x16/` | STUDY | chosen 2026-11-12 22:07 | 2026-11-13 03:14 (video, cover, PDF) | final delivered | UNKNOWN |
| 6 | PDF "5 Study Prompts" | Creators 100X lead magnet | Creators 100X | `brands/creators-100x/pdf/` | STUDY | with item 5 | 2026-11-12 22:32 (with VO), re-sent 2026-11-13 03:14 | final delivered (not hosted) | n/a |
| 7 | CHECK reel "There's an app that rates your reel before you post it" | Creedom: check a reel before you post | Creators 100X | `creedom-check-9x16/` | CHECK | 2026-11-13 03:28 | 2026-11-13 06:17 (video + cover) | final delivered | UNKNOWN |
| 8 | 3D storytelling guide (PDF, 14 pages) | Creedom: 3D story brief for Concept/NxtlvlSocial | n/a (brief) | `creedom-3d-story/` | CREEDOM (in the guide) | 2026-11-14 04:28 | 2026-11-14 04:35 | delivered (guide); 3D reel itself UNKNOWN | UNKNOWN |
| 9 | Cree 3D model sheet (PDF, 7 pages) + reference pack (ZIP) | Creedom: mascot for 3D | n/a (asset pack) | `creedom-3d-story/` | n/a | 2026-11-14 08:08 | 2026-11-14 08:12 | delivered (guide) | n/a |
| 10 | Prompt reel "Stop typing 'write me a script' into ChatGPT" | Creators 100X: 4-part prompt formula | Creators 100X | `creators100x-prompt-9x16/` | PROMPT | 2026-11-15 10:17 (picked 10:38) | v1 11:16; new-hook final 11:58 | final delivered (no cover) | UNKNOWN |
| 11 | PDF "10 Prompts That Sound Like You" | Creators 100X lead magnet | Creators 100X | `brands/creators-100x/pdf/` | PROMPT | with item 10 | 2026-11-15 11:00 (with preview), re-sent 14:05 | final delivered (not hosted) | n/a |
| 12 | Riya paper cut-out story "Why her AI scripts got 200 views" | Creators 100X: 4-part prompt formula as a story | Creators 100X | `creators100x-prompt-story-9x16/` | PROMPT | 2026-11-15 11:59 | 2026-11-15 12:17; cover 12:18; SEO description 14:07 | final delivered; owner may send changes | UNKNOWN |
| 13 | @write-script reel "I tried on forty AI scripts last week" | Creedom: get a script in your voice (@write-script) | Creators 100X | `creedom-write-script-9x16/` | SCRIPT | 2026-11-17 11:06 | v3 final 13:33; v4 final + cover + description 16:34 | final delivered (v4) | UNKNOWN |

Nothing is currently **waiting on approval**: every latest preview was approved and rendered as a final. The only
unfinished build is item 1 (drafts from October, outcome not in any source).

---

## 3. Timeline by date

| Date (UTC) | What happened |
|---|---|
| 2026-10-24 | Reel Analyser: script v1 (modern story arc), CTA changed CREE -> CREEDOM, "say Creedom throughout, not Cree", mood tags for ElevenLabs Nota 3, script v2 trimmed to 35 s (~76 words), visual plan v1, drafts 1-4 (git). |
| 2026-10-25 | Reel Analyser: Google Sans brand type, draft 6 "immersive scenes, magnifier film-strip world, calmer bird, one CREEDOM" (git). Last activity on this reel. |
| 2026-11-10 | Explainer brief 10:26. Previews v2 11:31, v3 12:09, v4 12:36, v5 "final export" 13:13, v6 13:44, v7 14:16, v7b 14:28, v8 14:48, v9 15:06. Cree's 13 poses generated (10:57-11:02). |
| 2026-11-11 | Explainer v10 final 00:48; cover 12:45. Hook reel brief 09:12; v1 09:48; v2 final 10:21; v3 final 10:42; v4 11:11; v5 11:43; v6 12:00; v7 12:29; v8 12:48; v9 15:19; v10 final 15:41. |
| 2026-11-12 | Hook reel v11 07:37, v12 07:56, v12b 08:32, v13 preview 08:44, v13 final 08:51, cover 08:55. 20 Hooks PDF 09:01 (Creators 100X brand kit made at the same time). Creators 100X ideas 15:25, creator audit 15:41, 10-day audit 22:06. STUDY chosen 22:07; Chatterbox VO + 5 Study Prompts PDF 22:32. |
| 2026-11-13 | STUDY preview 02:30, v2 03:00, manga pronunciation fix 03:08, final 03:14. CHECK brief 03:28; script approved 03:42; v1 04:01, v2 04:10, v3 04:22, v4 04:45, v5 05:42, v6 06:04; final 06:17. |
| 2026-11-14 | 3D storytelling guide 04:35. Cree 3D model sheet + reference pack 08:12. |
| 2026-11-15 | Creators 100X topics 10:17; picked 10:38; prompt reel preview + PDF 11:00; v1 final 11:16; new-hook final 11:58. Riya story requested 11:59; preview 12:13; final 12:17; cover 12:18. PDF + cover re-sent 14:05; SEO description 14:07. |
| 2026-11-17 | @write-script brief 11:06; option A approved 11:13; v1 11:43; v2 12:54; v3 13:13; v3 final 13:33; ElevenLabs mood-bracket script 14:58 / 15:00; owner's ElevenLabs VO 15:03; v4 preview 15:12; v4 final + cover + description 16:34. |

---

## 4. Item details

### 4.1 Creedom Reel Analyser ("My reel did 85x my usual")

- **Status:** parked / UNKNOWN. Drafts 1-6 exist in git (2026-10-24/25). No render folder, no final, no
  caption.md, and that chat is not in this session's logs. *Source: notes_creedom_files.md §2.1*
- **Page:** AI.NXTLVL (UNCERTAIN): the end card shows "IG logo + @AI.NXTLVL" and the stats come from "the user's own
  Creedom screenshots of @ai.nxtlvl (Oct 2026)".
- **Concept:** "TITLE / ANGLE: "My reel did 85x my usual. I had no idea why." Creedom's reel analyser finds the reason,
  second by second." Faceless motion graphics, the mascot (then drawn as a flat cut-out "pink bird" puppet) as the
  lead.
- **Length / format:** 32-35 s, ~76 spoken words, 1080x1920, built at 60 fps, DUR 33.6 s, VO 32.13 s.
- **Voice:** ElevenLabs "Nota 3" (rTMkoe3NzNrEOgFeBwY2), Eleven v3; take file
  `ElevenLabs_2026-10-24T22_01_18_V_eleven_v4.mp3`.
- **CTA keyword:** CREEDOM (script v1 used CREE).
- **Final VO script (script.md, verbatim):**
  "[curious] One reel did eighty-five times my usual views... [softly] and I had no idea why. / [thoughtful] The next
  one? A few thousand. [softly] Numbers... never reasons. / [warmly] So I gave my page to Creedom. [smiling] Twenty
  seconds. / [impressed] Content score: eighty-two out of a hundred. / [intrigued] Then its reel analyser watched my
  reel... second by second. / [whispers] And found what I'd missed... [amazed] my best hook was buried at thirty-four
  seconds. / [confident] Now I edit with reasons. [smiling] Not guesses. / [playful] Comment CREEDOM... [warmly] and I'll
  DM you the link."
- **Real stats used:** 85x / 126,000+ plays, 82/100 content score, 6 posts, 6,205 followers, buried hook at 0:34: real
  numbers of the owner's @ai.nxtlvl page, not Creators 100X.
- **Planned cover text:** "Why did this reel hit 85x?"
- **Draft caption (script.md):** contains an emoji (an eyes emoji), written before the no-emoji rule; must be rewritten if this
  reel is ever finished.
- **Music / SFX:** original synthesised bed (100 bpm pop in F major) and synthesised SFX.
- **Auto-DM:** NOT FOUND. **Final file:** none.

### 4.2 Creedom explainer (CREE)

- **Status:** final delivered (v10, 2026-11-11 00:48); cover delivered 2026-11-11 12:45.
- **Page:** NXTLVL (file prefix `nxtlvl_`). Which NXTLVL page: UNKNOWN. (The app recording used in it is logged in as
  ai.nxtlvl.)
- **Request:** 2026-11-10 10:26: "Leave that for now i need you to make an explainer video on creedom.ai based on these
  scripts and context, follow the animation pacing and concepts from this promo video and use the screen recording
  however the script demands, make it highly interactive and immersive from the hook and till the end ,  this is the
  mascot of creedom, you can animate him to be very expressive and doing things ad per the script , you can take the
  idea of colors schemes from their logo, app or website, make a unique music that fits the context and also an good
  female voiceover from elevenlabs"
- **Concept:** the owner's own script card (the client's script), paced like the Nxtlvl promo, with the owner's app
  screen recording and Cree acting out every line. Pink/white creedom.ai look, iOS picker-wheel hook, liquid-glass
  title capsules, live retention graph.
- **Script (client's, verbatim):** "This AI told me the exact second people stopped watching my reel. I uploaded a reel
  that flopped into Creedom's Reel Analyzer, and it watched it second by second. It told me my hook worked, but my
  energy dropped in the middle, and that's exactly where people swiped away. It also gave me new hooks and showed me
  what to fix before I post the next one. You can even get a free audit of your whole account. Just type your handle,
  and in about 20 seconds you get a score out of 100 and the first thing to fix. Comment "CREE" and I'll send you the
  link."
- **CTA keyword:** CREE.
- **Previews (2026-11-10):** v2 11:31:26, v3 12:09:33, v4 12:36:13, v6 13:44:08, v7 14:16:09, v7b 14:28:59, v8 14:48:15,
  v9 15:06:39. **Finals:** v5 "final export" 13:13:29 (superseded), v10 2026-11-11 00:48:08.
- **Spec of the final:** 1080x1920, 37 fps, 37.51 s, 51 MB, -16.0 LUFS, -4.4 dBTP (verify PASS).
- **Voice:** ElevenLabs "Hallie - Fun, Young & Feminine" (jpICOesdLlRSc39O1UB5), eleven_v3.
- **Music:** "Inspiring Technology" by Soundrider/Dope (CC BY 3.0). SFX: CC0 OpenGameArt packs (Freesound refused).
- **Post description (2026-11-10 14:48, verbatim; no caption.md exists in the repo):**
  ```
  Comment "CREE" and I'll send you the link.

  This AI told me the exact second people stopped watching my reel.

  I put a reel that flopped into Creedom's Reel Analyzer. It watched it second by second and showed me my hook worked, but my energy dropped in the middle, and that's exactly where people swiped away. Then it gave me new hooks and told me what to fix before I post the next one.

  You can also get a free audit of your whole account. Type your handle and in about 20 seconds you get a score out of 100 and the first thing to fix.

  Music: "Inspiring Technology" by Soundrider/Dope (CC BY 3.0)

  #reelstips #instagramgrowth #contentcreator #aitools #creedom
  instagram reel analyzer, why my reels flop, instagram retention, reel hook ideas, free instagram account audit, ai tool for creators, how to grow on instagram, instagram reels tips
  ```
- **Cover:** "This AI found / the exact second / people stopped watching", retention graph falling off a cliff at a red
  0:03 playhead, "viewers left at 0:03", "↓ 62% here", Cree with the magnifier on the drop, Creedom wordmark.
- **Auto-DM:** never written (Creedom link missing).
- **Final files:** `creedom-explainer-9x16/renders/nxtlvl_creedom-explainer_reels_9x16_v10.mp4`,
  `nxtlvl_creedom-explainer_reels_9x16_v10_cover.png`. Also on disk: `nxtlvl_creedom-explainer_reels_9x16_v5.mp4`
  (first final), `_v5_bed.mp4`, `mix_draft.mp4`, `mix_final.mp4`. The preview files
  `preview_creedom-explainer_reels_9x16_v2..v9.mp4` named in the chat are no longer in the folder.

### 4.3 Hook reel / reel-flop (HOOK)

- **Status:** final delivered (v13, 2026-11-12 08:51:48; cover 08:55:04).
- **Page:** Creators 100X per later references ("the creator 100x reel", 2026-11-12 22:53; "af_heart, the natural
  female voice you approved on the Creators 100X hook reel"), but the files carry the `nxtlvl_` prefix and on
  2026-11-11 09:16 the page answer was "No brand". UNCERTAIN where it was posted.
- **Request:** 2026-11-11 09:12: "Now i need you to make another explainer reel but dont include any @ handle in it the
  cta would be mentioned in the script rest keep a minimal gradient background maybe white and black gradient
  background, make a concept around this reel and discuss it with me what will the best approach"
- **Concept:** "3-second autopsy": why reels flop in the first three seconds, three mistakes. Opens on a fake skippable
  creator reel ("danny.daily.vlogs", "Hey guys, welcome back to my channel!") and a pixel mascot reel ("Pixo",
  "pixo.planet.fm", "PIXO PARTY!"), then the replay payoff.
- **Final script (v12/v13):** "This video already lost you." / "In the first three seconds." / "Here are three mistakes
  killing your views." / "One: your hook is a greeting." / "Nobody stays for "Hey guys."" / "Start with the result." /
  "Two: your first frame is still." / "If nothing moves, thumbs keep scrolling." / "Three: you explain before you show."
  / "Show the result first, then explain how you got it." / "Fix these three and watch your next reel." / "Save this so
  you don't forget, and comment "HOOK" for my list of twenty hooks that work."
- **CTA keyword:** HOOK -> PDF "20 Hooks That Work".
- **Versions:** previews v1 09:48:31, v4 11:11:28, v5 11:43:14, v6 12:00:27, v7 12:29:31, v8 12:48:20, v9 15:19:46
  (2026-11-11); v11 07:37:48, v12 07:56:46, v12b 08:32:21, v13 preview 08:44:08 (2026-11-12). Finals v2 10:21:50, v3
  10:42:38, v10 15:41:20 (2026-11-11), v13 08:51:48 (2026-11-12).
- **Spec of the final:** 35.7 s, 31 MB, 30 fps, -14.1 LUFS, -1.7 dBTP (verify NEEDS FIX against -4 dBTP).
- **Voice:** Kokoro-82M af_heart (v13). **Music:** "Future Inspiration" by Soundrider/Dope (CC BY 3.0, 123 BPM).
- **Post description (caption.md, verbatim):**
  ```
  Comment "HOOK" and I'll send you my list of 20 hooks that work.

  This video already lost you in the first three seconds. Here are 3 mistakes killing your views.

  1. Your hook is a greeting. Nobody stays for "Hey guys." Start with the result.
  2. Your first frame is still. If nothing moves, thumbs keep scrolling.
  3. You explain before you show. Show the result first, then explain how you got it.

  Fix these three and watch your next reel. Save this so you don't forget.

  Music: "Future Inspiration" by Soundrider/Dope, CC BY 3.0

  #reelstips #contentcreator #instagramgrowth #hooks #socialmediatips
  reel hooks, how to get more views on reels, why my reels flop, instagram algorithm, first 3 seconds of a reel, video hook ideas, reels retention tips, short form video tips, tiktok hooks, content creation tips
  ```
- **Cover (v13):** "This video / already / lost you." with a tilted greyscale phone of the dull creator reel and a red
  "SKIPPED" stamp, pill "Watched 0:03 of 0:48".
- **Auto-DM:** text NOT FOUND; resource = the 20 Hooks PDF, which has no hosted link.
- **Final files:** `reel-flop-9x16/renders/nxtlvl_reel-flop_reels_9x16_v13.mp4`, `nxtlvl_reel-flop_reels_9x16_v13_cover.png`.
  On disk too: previews `preview_reel-flop_reels_9x16_v11.mp4`, `_v12.mp4`, `_v12b.mp4`, `_v13.mp4`; covers `_v2_cover.png`,
  `_v3_cover.png`, `_v10_cover.png`. (The v2, v3 and v10 MP4s named in the chat are no longer in the folder.)

### 4.4 PDF: 20 Hooks That Work (HOOK)

- **Status:** final delivered 2026-11-12 09:01:30 (request 08:57:20). Not hosted anywhere (no link).
- **Request (verbatim):** "Also make pdf for 20 hooks so that i can put in automation and make the pdf with this
  creators 100x branding whenever i say to"
- **File:** `brands/creators-100x/pdf/creators100x_20-hooks-that-work.pdf` (10 pages, 4:5), content
  `pdf/20-hooks-that-work.json`.
- **Contents:** cover ("Free swipe file", "20 HOOKS THAT WORK"); the three rules page ("The first 3 seconds decide
  everything"); 20 hooks, three per page, in categories Result first, Mistake, Contrarian, Curiosity, Numbers, Story,
  Callout, Comparison, Insider, Pattern break, Challenge; checklist "Before you post"; closing "Pick one hook. Film it
  today. Ship it." Example numbers in it are illustrative.

### 4.5 STUDY manga reel (STUDY) and PDF: 5 Study Prompts

- **Status:** final delivered 2026-11-13 03:14:59 (video, cover, PDF).
- **Page:** Creators 100X.
- **Request chain (verbatim):** 2026-11-12 22:07:51 "Go with the STUDY manga idea, write the script"; 22:20:57
  "Chatterbox"; 22:34:45 "I record"; 22:44:04 "Where do i find the life processes images"; 22:53:06 "How bout you use
  canva to make those images and animate the chatgpt ui interface and then keep making them as per the script and rest
  follow the theme of chatgpt and also take the text styling , pacing animations and other things from the creator 100x
  reel"; 2026-11-13 02:48:56 "The video feels very dull including the voicover there is sooo less animation going on in
  this video, also the voiceover looks bad"; 03:05:23 "But she is pronouncing manga wrong"; 03:11:32 "Yeah give me the
  final render".
- **Concept:** NCERT Class 10 Science "Life Processes" turned into a manga with one ChatGPT prompt, inside an animated
  ChatGPT screen; five study prompts (manga, timeline, mind map, labelled diagram, revision sheet). Audience: students.
- **Final script:** "I made the hardest chapter in Class 10 Science into a manga. One prompt." / "Same chapter. Twelve
  pages you forget by tomorrow, or six panels you actually remember." / "Here are five prompts. Paste your chapter, pick
  one." / "One: manga. Two: timeline. Three: mind map. Four: labelled diagram. Five: a one-page revision sheet." /
  "Number five is the one you want the night before the exam." / "Comment STUDY, and I'll send you all five prompts,
  ready to copy." (The hook was "I turned..." until the voice dropped the "-ed".)
- **CTA keyword:** STUDY -> PDF "5 Study Prompts".
- **Previews:** VO + PDF 2026-11-12 22:32:01; preview 2026-11-13 02:30:43; v2 03:00:13; manga fix 03:08:52.
- **Spec of the final:** 26.16 s, 41 MB, -14.0 LUFS, -1.5 dBTP (verify NEEDS FIX).
- **Voice:** v1 Chatterbox (rejected), v2 Kokoro af_heart with "MAHNG-guh". **Music:** "Be Happy" by ANtarcticbreeze
  (CC BY 3.0).
- **Post description (caption.md, verbatim):**
  ```
  Comment "STUDY" and I'll send you all 5 prompts, ready to copy.

  I made the hardest chapter in Class 10 Science into a manga. One prompt.

  Same chapter: twelve pages you forget by tomorrow, or six panels you actually remember.

  The 5 prompts turn any chapter into:
  1. A manga page
  2. A timeline
  3. A mind map
  4. A labelled diagram
  5. A one-page revision sheet (the one you want the night before the exam)

  Works in ChatGPT or Gemini. Paste your chapter, pick a prompt, then check the facts against your textbook before you revise.

  Save this for exam season.

  Music: "Be Happy" by ANtarcticbreeze, CC BY 3.0

  #studytips #chatgptprompts #class10 #boardexams #aitools
  chatgpt prompts for students, how to study with ai, ncert class 10 science, life processes class 10, ai study hacks, mind map prompt, revision sheet chatgpt, board exam preparation tips, how to remember chapters, study smarter not harder
  ```
- **Cover:** "CLASS 10 · LIFE PROCESSES", "Your hardest / chapter, / as a manga.", the owner's real ChatGPT manga panels,
  "1 PROMPT" stamp, pill "5 PROMPTS · COMMENT STUDY".
- **Auto-DM:** text NOT FOUND (only "The STUDY keyword DM sends ... the PDF"); PDF not hosted.
- **Final files:** `study-manga-9x16/renders/creators100x_study-manga_reels_9x16_v1.mp4`, `_v1_cover.png` (draft:
  `_draft.mp4`); PDF `brands/creators-100x/pdf/creators100x_5-study-prompts.pdf` (6 pages).

### 4.6 Creedom CHECK reel (CHECK)

- **Status:** final delivered 2026-11-13 06:17:42 (video + cover; description at 06:17:54).
- **Page:** Creators 100X ("it will be posted on Creators.100x but it is based on Creedom's feature of checking your reel
  before you post it").
- **Request (2026-11-13 03:28:39, verbatim):** "Now i need you to work for another reel it will be posted on
  Creators.100x but it is based on Creedom's feature of checking your reel before you post it soo i will share you a
  dummy screen recording based on that but you need to add a concept of your own for that visual and everything should
  be in premium glass fluid animations nothinh should feel like paper/cardboard animation, keep that premium feel with
  it and also the transitions"
- **Concept:** premium liquid-glass world in Creedom pink; a neutral Pexels demo reel ("3 AI tools I use daily") gets
  scored 4.2/5 (labelled "EXAMPLE REEL"), three flagged moments, a fix card, Share unlocks to "Post it"; Cree (3D poses)
  as the checker.
- **Approved script (03:42:26), verbatim:** Hook 70 "There's an app that rates your reel before you post it, and tells
  you exactly what to fix." / Peak "Not views after you post. Reasons, before." / Release "It's called Creedom. It
  watches your whole reel, second by second, like a real viewer." / Peak "Then it scores it out of five…" / Peak "…and
  flags the exact moments that need work: a weak hook, a claim with no proof, a moment that loses trust." / Peak "With
  the timestamp, and the fix." / Release "So you fix it before anyone ever sees it." / CTA "Comment CHECK and I'll send
  you the link."
- **CTA keyword:** CHECK.
- **Previews:** v1 04:01:55, v2 04:10:56, v3 04:22:38, v4 04:45:05, v5 05:42:12, v6 06:04:40. Final 06:17:42 (v6.1,
  "chips leave as one group (no flicker at 0:13)").
- **Spec of the final:** 1080x1920, 30 fps, 23.54 s, 27 MB, -14.0 LUFS, -1.5 dBTP (verify NEEDS FIX), 72 SFX cues.
- **Voice:** Kokoro af_heart, ~1.12x faster in v6. **Music:** "Corporate Music" by Ruslan Latypov (CC BY 3.0); earlier
  "Down For You" (v2-v5) and "Inspiring Technology" (v1, rejected as already used).
- **Post description (caption.md, verbatim):**
  ```
  Comment "CHECK" and I'll send you the link.

  There's an app that rates your reel before you post it.

  Instagram only tells you a reel flopped after it's live. Views, reach, watch time: numbers, never reasons.

  Creedom watches your whole reel second by second, like a real viewer, then:
  1. Scores it out of 5
  2. Flags the exact moments that need work (a weak hook, a claim with no proof, a moment that loses trust)
  3. Gives you the timestamp and the fix for each one

  So you fix it before anyone ever sees it.

  Save this for your next edit.

  Music: "Corporate Music" by Ruslan Latypov, CC BY 3.0

  #reelstips #contentcreator #instagramgrowth #aitools #creedom
  how to check a reel before posting, why did my reel flop, instagram reel tips, reel hook tips, ai tools for content creators, how to improve reels, reel analyzer app, instagram growth tips, viral reel checklist, video editing tips for creators
  ```
- **Cover:** "An app that *rates* / your reel *before* / you post.", tilted phone with the demo reel, glass badge
  "4.2/5 EXAMPLE REEL", pill "0:14 Loses trust", Cree cheering, black pill "COMMENT CHECK".
- **Auto-DM:** never written: "For the CHECK auto-DM, I still need the Creedom link." (2026-11-13 06:17:54).
- **Final files:** `creedom-check-9x16/renders/creators100x_creedom-check_reels_9x16_v1.mp4`, `_v1_cover.png`
  (draft: `creators100x_creedom-check_reels_9x16_draft.mp4`).

### 4.7 Creedom 3D storytelling guide (PDF)

- **Status:** delivered (guide) 2026-11-14 04:35:27. The 3D reel itself (to be made in "Concept/NxtlvlSocial"):
  UNKNOWN; no owner feedback on the guide.
- **Request (2026-11-14 04:28:46, verbatim):** "Now i need you to make a 3d render storytelling for creedom but i think
  this session is not trained to make 3d renders soo give me a pdf for the Concept/NxtlvlSocial cause that is where 3d
  render happens so provide me with the perfect guideline how and what topic/concept should be used for story telling and
  also the art/visual style, how the creedom mascot should look"
- **Contents:** a 35-45 s vertical 3D story, "The creator is the hero, Cree is the guide", CTA "Comment CREEDOM".
  Recommended concept A "The Buried Hook"; others B "The Screen Test", C "The Reel Gym", D "The Case of the Missing
  Views". Script ~38 s / 75 words, 9-shot list, art direction, Cree character sheet, render spec (1080x1920, 24 or 30
  fps, ProRes master plus a no-text version), prompt pack.
- **Concept A VO (verbatim):** 0:00 "Her best moment was hiding at second thirty-four. Nobody ever got that far." 0:05
  "She posted anyway. A few hundred views. No idea why." 0:09 "So she asked Cree." 0:11 "Cree doesn't guess. He walks
  through her reel second by second, like a real viewer." 0:17 "Zero to three: a slow start. That's where people swipe."
  0:21 "Then, at thirty-four... there it is." 0:25 "Cree carries it to the front. Same reel, new first second." 0:31
  "She posts. This time, they stay." 0:35 "Check your reel before you post. Comment CREEDOM."
- **File:** `creedom-3d-story/renders/creedom_3d-storytelling-guide.pdf` (14 pages, 1080x1350, 5.99 MB).

### 4.8 Cree 3D model sheet and reference pack

- **Status:** delivered (guide) 2026-11-14 08:12:11. No owner feedback. Offer to make a first 3D model with Higgsfield
  image-to-3D (uses credits; Higgsfield balance was 0 on 2026-11-10) not answered.
- **Request (2026-11-14 08:08:32, verbatim):** "Okay, before this edit, can you help me with the Creedom mascot? Like I
  wanted to, build a 3D render around that mascot. So just, give me all the images or how you made that mascot to be,
  fully animated in 3D. So give me those files or PDF or any images that can be helpful for making the 3D render."
- **Files:** `creedom-3d-story/renders/creedom_cree-3d-model-sheet.pdf` (7 pages, 2.79 MB),
  `creedom-3d-story/renders/creedom_cree-3d-reference-pack.zip` (32 files, 15.0 MB: master reference
  `00_cree_original.png`, `01_proportions_front.png`, 13 poses + eye/box JSON, old rig layers, Cree icon and Creedom
  wordmark, both PDFs, README).

### 4.9 Prompt reel "Stop typing 'write me a script'" (PROMPT) and PDF: 10 Prompts

- **Status:** final delivered (v1 11:16:38; new-hook final 11:58:42, 2026-11-15). No cover was ever made.
- **Page:** Creators 100X. Audience: "beginner creators that want to use ai".
- **Request chain (verbatim):** 10:17:02 "Now i need you to make a reel for creators 100x , give me topic and visual
  style suggestions that have potential to get views, just remember the video should target beginner creators that want
  to use ai"; 10:38:03 "Go with the first idea and B visual style"; 11:10:25 "But there are few visual elements try to add
  more of them not a single frame should feel dull and also reduce the background music sound and send it in final
  quality"; 11:34:29 "Reduce it more and pls make the hook more engaging people may skip that"; 11:59:43 "Cant it be a
  visual storytelling concept in 2d" (led to item 12).
- **Concept:** topic 1 (the 4-part prompt formula) in visual style B (before / after split screen).
- **Final script (v3):** "Stop typing this into ChatGPT. It's why your scripts sound exactly like everyone else's." /
  "Same AI. One better prompt. Watch." / "First, tell it who you are. A fitness creator with three thousand followers." /
  "Then, who it's for. Busy beginners who keep skipping the gym." / "Now the hook. Open with a mistake they're making." /
  "And the format. Thirty seconds, three tips, one line each." / "Same AI. Thirty more seconds of typing. And now it
  actually sounds like you." / "Comment PROMPT, and I'll send you ten prompts like this, ready to copy."
- **CTA keyword:** PROMPT -> PDF "10 Prompts That Sound Like You".
- **Spec of the final:** 30.0 s, 45 MB, -14.0 LUFS, -1.8 dBTP (verify NEEDS FIX). The file is named v1 but carries the
  v3 content.
- **Voice:** Kokoro af_heart. **Music:** "Inspiring Ambient Motivation" by Soundrider/Dope (CC BY 3.0), bed -28 LUFS.
- **Post description (caption.md, verbatim):**
  ```
  Comment "PROMPT" and I'll send you 10 prompts that make AI sound like you, ready to copy.

  If your AI scripts sound like everyone else's, the problem is the prompt, and the fix takes 30 seconds.

  "Write me a reel script" gives you the same generic script every other beginner gets. Give the AI four things instead:
  1. Who you are: your niche and your size
  2. Who it's for: one audience with one problem
  3. The hook: how the first line should grab them
  4. The format: length and shape

  Same AI. Thirty more seconds of typing. A script that actually sounds like you.

  Save this for your next script.

  Music: "Inspiring Ambient Motivation" by Soundrider/Dope (CC BY 3.0)

  #chatgptprompts #aiforcreators #contentcreatortips #reelstips #aitools
  chatgpt prompts for content creators, how to write a reel script with ai, ai script writing, chatgpt for instagram reels, best chatgpt prompts, ai tools for beginners, how to use chatgpt for content creation, reel script ideas, content creation tips for beginners, prompt engineering for beginners
  ```
- **Auto-DM (verbatim, "once the PDF is hosted"):**
  ```
  Here are your 10 prompts: [PDF LINK]
  1. Open the PDF and start with the 4-part formula on page 2.
  2. Copy prompt 01, fill in the highlighted blanks with your niche and audience.
  3. Paste it into ChatGPT, Gemini or Claude.
  ```
- **Final files:** `creators100x-prompt-9x16/renders/creators100x_stop-write-me-a-script_reels_9x16_v1.mp4`; PDF
  `brands/creators-100x/pdf/creators100x_10-prompts-that-sound-like-you.pdf` (7 pages, made 2026-11-15 10:47). Cover: none.

### 4.10 Riya paper cut-out story (PROMPT)

- **Status:** final delivered 2026-11-15 12:17:37; cover 12:18:48; PDF + cover re-sent 14:05:38; SEO description
  14:07:53. The owner said on 14:05:30 "I'll tell you to make changes later" (no changes sent since).
- **Page:** Creators 100X.
- **Request:** 11:59:43 "Cant it be a visual storytelling concept in 2d"; owner picked "Paper cut-out" and "New
  story-led script" (12:00:45); 12:15:11 "Is this the final render?"; 12:15:32 "Go ahead with the final render";
  14:05:30 "I'll tell you to make changes later, before that give me the pdf and cover page for the creators 100x reel we
  made today"; 14:07:31 "And also the perfect seo keywords description".
- **Concept:** the same 4-part prompt lesson told as a story about Riya, a beginner creator stuck at 200 views; hand-cut
  paper in the Creators 100X colours, stop-motion at 12 fps, a paper robot as the AI, four puzzle pieces.
- **Script (verbatim):** "Riya just posted her fifth reel this week. Two hundred views. Again." / "Her script was written
  by AI. So was everyone else's." / "Because she typed what every beginner types: write me a reel script." / "So this
  time, she gave the AI four pieces instead of one." / "Who she is. A fitness creator with three thousand followers." /
  "Who it's for. Busy beginners who skip the gym." / "The hook. Open with a mistake they're making." / "And the format.
  Thirty seconds, three tips." / "Same AI. But this time, the script sounded like her." / "And her next reel didn't
  blend in." / "Comment PROMPT, and I'll send you ten prompts like hers, ready to copy."
- **CTA keyword:** PROMPT -> the same 10 Prompts PDF.
- **Spec of the final:** 35.8 s, 41 MB, -14.1 LUFS, -1.7 dBTP (verify NEEDS FIX).
- **Post description (SEO version, caption.md, verbatim):**
  ```
  Comment "PROMPT" and I'll send you 10 ChatGPT prompts that make AI write reel scripts that sound like you.

  Riya kept getting 200 views on her reels. Her AI scripts sounded exactly like everyone else's, because she typed what every beginner types into ChatGPT: "write me a reel script."

  So she gave the AI four pieces instead of one:
  1. Who she is: her niche and her follower count
  2. Who it's for: one audience with one problem
  3. The hook: how the first line should grab them
  4. The format: length and shape (30 seconds, 3 tips)

  Same AI. This time the script sounded like her, and her next reel didn't blend in.

  Save this for your next script and share it with a creator friend who uses AI.

  Music: "Inspiring Ambient Motivation" by Soundrider/Dope (CC BY 3.0)

  #chatgptprompts #aiforcreators #contentcreatortips #reelstips #aitools
  chatgpt prompts for content creators, how to write a reel script with ai, ai script writer for reels, chatgpt prompts for instagram reels, how to get more views on instagram reels, reel script ideas, ai tools for content creators, content creation tips for beginners, how to grow on instagram with ai, best chatgpt prompts for social media
  ```
- **Auto-DM:** identical to item 10 ("Here are your 10 prompts: [PDF LINK]" + the same 3 steps).
- **Cover:** torn-paper banner "WHY HER AI SCRIPTS / GOT 200 VIEWS", Riya with her "200 views" phone, the robot with
  the "GENERIC" slip, label "+ THE 4-PART FIX".
- **Final files:** `creators100x-prompt-story-9x16/renders/creators100x_riya-paper-story_reels_9x16_v1.mp4`,
  `_v1_cover.png`; also `preview_creators100x_riya-paper-story_9x16_v1.mp4`, `master_final.mp4`.

### 4.11 Creedom @write-script reel (SCRIPT)

- **Status:** final delivered (v4, 2026-11-17 16:34:42, with cover and description). v3 was also rendered as a final at
  13:33:39 before the v4 changes.
- **Page:** Creators 100X.
- **Request chain (verbatim):** 11:06:36 "[IMAGE ATTACHED] Make another reel for creedom based on this context and give me
  suggestions for visuals and scripts"; 11:13:55 "Go with option A and every single visuals ideas in this reel that you
  mentioned, yeah your 2nd assumption is correct"; 12:24:23 (on v1) "See, this looks like the rebranding or some kind of
  part 2 of that earlier video we made, and I don't want to do that. So change the voiceover style, like make it more
  expressive and add some different concepts, and use a different video, or don't use a video at all. Try to explain or
  make the things with more animation elements, because it looks the same as the previous reel we made. So try something
  unique."; 13:00:13 (on v2) "Keep the Creedum background as it is, like that pink type of background, and also use some
  more animations in the first hook person, like add a mascot, like add a person, okay, and use the Creedum mascot time
  to time. Just show the exact UI of that screenshot that I send you and animate it accordingly, like write something
  related to that context. Rest, yeah, you can add more animations and more elements. So yeah, and also change the sound
  effects a little bit. Rest, also reduce the volume of the background music."; 13:29:08 "Render in final"; 14:57:56 "Do
  one thing firstly give me a good expressive voiceover script of an female from elevenlabs with moodbrackets"; 14:59:19
  "Good concept! Just a few suggestions: / 0:01-0:03 - can we make the scripts come in front of the person instead of
  behind them? / 0:03 - Not one fit -> Not one worked / 0:06 - off the rack -> off the shelf / 0:15 - @writescript need
  not be spoken out loud / Make the changee accordingly and now give me the script"; 15:03:24 (uploads the ElevenLabs
  Blondie take); 16:29:45 "Send final render with cover page and perfect seo description".
- **Concept (final, "MADE TO MEASURE"):** AI scripts are off the shelf (one size fits all), Creedom's write-script is a
  tailor. Person in a mirror, Cree as the tailor, the real Creedom home screen rebuilt from the screenshot with
  "@write-script my 5am routine reel" typed, Cree replying "On it. First, I'll take your measurements: your openers, your
  pauses, your words." (our writing, not real app output).
- **Version history:** v1 Option A "The blank screen" (preview 11:43:04; rejected as "part 2" of CHECK); v2 sewing-pattern
  paper, no Cree, no footage (12:54:19); v3 Creedom pink back, person + Cree + exact UI, music ~5 dB lower (preview
  13:13:14, final 13:33:39); v4 scripts in front, "Not one worked", "off the shelf", @write-script typed not spoken, the
  owner's ElevenLabs voice (preview 15:12:08, final 16:34:42).
- **Final VO (ElevenLabs, mood brackets, verbatim):**
  ```
  [frustrated sigh] I tried on forty AI scripts last week... [deadpan] Not one of them worked.

  [sarcastic] They're all off the shelf. Same hook. Same "let's dive in!" [exasperated] For every creator on earth.

  [softly] Because none of them... have ever heard you talk.

  [curious] So I opened Cree-dum... [playful] and typed this.

  [intrigued] First, it takes your measurements. [upbeat] How you open. Where you pause. [laughs] The words you can't stop saying.

  [excited] Then it cuts a script to fit you. [building energy] Hook... story... call to action... [proud] stitched in your voice.

  [delighted laugh] It sounds like me... [warmly] on a really good day.

  [confident] Comment SCRIPT... [playful] and I'll send you the link.
  ```
- **CTA keyword:** SCRIPT.
- **Spec of the final:** 1080x1920, 30 fps, 38.46 s, 40 MB, `--quality delivery`, 95 SFX cues, -14.0 LUFS, -1.5 dBTP
  (verify NEEDS FIX).
- **Voice:** the owner's ElevenLabs file `ElevenLabs_2026-11-17T15_02_49_Blondie_-_Conversational_eleven_v4.mp3` (voice
  "Blondie - Conversational", eleven_v4 per the file name), 37.8 s.
- **Music:** "Swinging Around" by Daniel Bautista (CC BY 3.0). **CC BY SFX credited:** "Sewing machine" by Jagadamba,
  "Coathanger Clothes Hanger" by dersuperanton, "Sliding Clothes on Rail 2" by _MC5_.
- **Post description (caption.md, verbatim):**
  ```
  Comment "SCRIPT" and I'll send you the link.

  I tried 40 AI scripts last week. Not one of them worked.

  They're all off the shelf. Same hook, same "let's dive in", for every creator on earth. Because none of them have ever heard you talk.

  So I opened Creedom and used write-script. It works like a tailor for your reels:
  1. It takes your measurements: how you open, where you pause, the words you can't stop saying
  2. It cuts a script to fit you: hook, story and call to action
  3. It stitches it in your voice, so it sounds like you on a really good day

  Save this for the next time a script sounds like everyone else, and send it to a creator who's stuck on a blank page.

  Music: "Swinging Around" by Daniel Bautista, CC BY 3.0
  Sounds: "Sewing machine" by Jagadamba, "Coathanger Clothes Hanger" by dersuperanton, "Sliding Clothes on Rail 2" by _MC5_ (CC BY 4.0, Freesound)

  #reelscript #contentcreator #aitools #instagramreels #creedom
  how to write reel scripts, ai script writer for reels, reel script in your own voice, how to write a hook for reels, instagram reel script template, content ideas for creators, how to sound natural on camera, ai tools for content creators, script writing for instagram, ai script generator for instagram
  ```
- **Auto-DM (caption.md, verbatim; link missing):**
  ```
  Creedom: [CREEDOM LINK]
  1. Open the link and connect your Instagram account.
  2. Type @write-script in the chat box.
  3. Tell it what your reel is about and send. It comes back with a hook, a story and a call to action.
  ```
- **Cover:** pill "I TRIED 40 AI SCRIPTS", "Not one / worked.", the mirror with the "DIDN'T WORK" stamp, Cree sad with a
  sweat drop, badge "Creedom @write-script fits you".
- **Final files:** `creedom-write-script-9x16/renders/creators100x_creedom-write-script_reels_9x16_v4.mp4`,
  `_v4_cover.png`. Also on disk: `_draft.mp4` (v1), `_v2_draft.mp4`, `_v3_draft.mp4`, `_v3.mp4` (v3 final),
  `_v4_draft.mp4`, `master.mp4`, `master_draft.mp4`.

---

## 5. Backlog: ideas not made yet

None of these has been approved or scheduled. Where the notes hold only a name or one line, the rest is UNKNOWN.

### 5.1 Creedom: unused script options for @write-script (2026-11-17, `creedom-write-script-9x16/plan/script_options.md`)

**Option B: "Stop asking ChatGPT for scripts" (contrarian)**

| Time | Beat | Voiceover |
|---|---|---|
| 0-3 s | Hook 70 | Stop asking AI to write your reel scripts. |
| 3-8 s | Peak 90 | Every one of them sounds the same, because it has never heard you talk. |
| 8-12 s | Release | Here's the same idea, two ways. |
| 12-19 s | Peak | Left: a generic AI script. Right: Creedom's write-script, after it read my last reels. |
| 19-25 s | Peak | Same topic. Only one of them sounds like me. |
| 25-30 s | Release | It even kept my opener and my sign-off. |
| 30-34 s | CTA | Comment SCRIPT and I'll send you the link. |

Visual: "one split screen for most of the reel (grey generic card left, pink Creedom card right), both reading line by
line in sync, a highlighter marking "this is me" on the right. Simple, fast to build, very clear." Note: it says
write-script "read my last reels", which is the unconfirmed claim (see open-items.md).

**Option C: "Which one did I write?" (comment bait)**

| Time | Beat | Voiceover |
|---|---|---|
| 0-3 s | Hook 70 | One of these scripts I wrote. One an AI wrote. |
| 3-10 s | Peak 90 | Script one... (reads 2 lines). Script two... (reads 2 lines). Which one's mine? |
| 10-14 s | Release | Lock in your guess. Three, two... |
| 14-19 s | Peak (twist) | Neither. Both came from Creedom's write-script. |
| 19-26 s | Release | It reads your reels first, so the script comes back in your voice. |
| 26-30 s | Peak | Which is why you couldn't tell. |
| 30-34 s | CTA | Comment SCRIPT for the link. And tell me which one you picked. |

Visual: "two script cards labelled 1 and 2, a countdown ring, then both cards flip to show the Creedom logo." Needs
"two scripts that really are both from Creedom, so it needs real output from the owner's account."

### 5.2 Creedom: app features not covered yet

From the app home screen (owner's screenshot, 2026-11-17) and the owner's screen recording (2026-11-10):

| Feature (app wording) | Covered so far | Notes |
|---|---|---|
| "Send a DM to your comments" (START SOMETHING card) | No | What it does exactly: UNKNOWN (only the card label is known). |
| "Ideas tuned to your account" (card) | No | Behaviour UNKNOWN. |
| "Audit my Instagram profile" (chip) | Only one line in the explainer ("free audit of your whole account ... score out of 100 and the first thing to fix") and the October Reel Analyser draft (content score 82/100) | A dedicated audit reel has not been made. |
| "Analyse one of my latest reels" (chip) | Partly (explainer, Reel Analyser draft) | |
| "Use one of my Reels and give me insights" (chip) | Explainer used the recording of this flow | |
| "Your saved reels, organized" (fifth card, seen in the recording) | No | Behaviour UNKNOWN. |
| "Hooks that would've made this reel go viral" and "CTA that would've driven more shares & saves" (result sections in the recording) | Briefly in the explainer ("new hooks") | Could carry a reel of their own. |
| Follow-up chips "Give me editing instructions for the first 5 seconds", "Compare this with my best Reel", "Write a script fixing these issues" | No | |
| Input prompts "Give me hook ideas", "What should I post next?", "Why didn't my last reel work?", "Write my next reel script" | No | |
| "Creedom is an Official Meta Business Partner (Dec 2025)" (Reel Analyser sources: Indian Startup Times / Ascendants seed-round coverage) | Not used on screen | Verify before using. |

### 5.3 Creedom: other unused ideas

- Reel Analyser alternative hooks (script.md): "126,000 plays on one reel. The next one? Barely three thousand." / "Your
  reel didn't flop. Your hook was just in the wrong second." / "I let an AI watch my reel... it found the mistake in 34
  seconds."
- The Reel Analyser reel itself (item 1) could be finished; its numbers are @ai.nxtlvl stats and its caption needs the
  emoji removed.
- 3D concepts not chosen (guide, 2026-11-14): B "The Screen Test" ("2 a.m., about to post. Cree pops out of the phone and
  runs a tiny screening for a crowd of viewer-bubbles. They drift away at 0:03. He fixes the opening; the next screening,
  they stay."), C "The Reel Gym" ("Reels are athletes; Cree is the coach with a stopwatch. A flabby, slow-starting reel
  trains its hook until it sprints off the line."), D "The Case of the Missing Views" ("Cree as a pocket-sized detective
  with a magnifier. Clues on a pinboard (timestamps), the culprit is a 4-second intro."). Concept A "The Buried Hook" is
  the recommended one, for the 3D team; its production status is UNKNOWN.
- Rejected CHECK hooks (do not reuse as they stand; the owner found them off-message or inaccurate): "I almost posted
  this reel. Then an AI watched it first." (GTA version); "Instagram tells you your reel flopped. It never tells you which
  second killed it."; "By the time Instagram shows you where people swiped away, it's already posted. And it never tells
  you why."

### 5.4 Creators 100X: proposed reel ideas

*Source: notes_chat.md §K and §D4.* Only names and one-liners are recorded; scripts were not written.

- **First idea list (2026-11-12 15:26):** VOICE ("My AI captions sound like AI"), ASK, CONTEXT, NOTES (NotebookLM), EDIT
  (Claude Code + HyperFrames), REPURPOSE. (Details of ASK and CONTEXT: UNKNOWN.)
- **After the creator audit (2026-11-12 15:41):** "The best free AI tool for every job, India edition" (TOOLS); weekly
  "GitHub repo with ___ stars" series; "Same-day fixes"; "5 secret ChatGPT codes for exam prep" (CODES); ""I gave AI my
  ___" build demos"; VOICE reworked as "5 secret codes that make ChatGPT write like you".
- **10-day audit list (2026-11-12 22:06):** #1 STUDY (made, item 5); "I asked ChatGPT to find every photo of me online"
  (PHOTO); "ChatGPT can make GIFs now. Here are 5 codes." (GIF); "Claude's new model built this from one prompt"
  (Fable 5.2); "This free skill makes your AI emails sound like you wrote them" (HUMAN).
- **Beginner-creator topics (2026-11-15 10:18; topic 1 was made as items 10 and 12):** 2 "I made a faceless reel in 30
  minutes using only free AI" (FACELESS); 3 "AI can pick your niche in 60 seconds" (NICHE); 4 "One video, ten posts"
  (REPURPOSE); 5 "3 AI mistakes that make your content look fake" (REAL); 6 "Let ChatGPT plan your next 30 days of
  content" (PLAN).
- **Unused visual styles (2026-11-15):** A (animated ChatGPT window), C (phone feed), D (paper desk). (B split screen and
  the paper cut-out story were used.)
- **Audit takeaways the owner can act on (2026-11-12 15:41, verbatim):** "the hook and the topic drive reach, while the
  "Comment KEYWORD" line turns that reach into leads." / "Keep reach posts and lead posts separate. Use the keyword only on
  resource posts" / "I couldn't find a big Indian page running the keyword-DM model for AI tools. That's an open gap you
  could take."
- **Page scope to stay inside (owner, 2026-11-12 15:25):** "basically this page is made to provide day to day ai helping
  tools prompts hacks or guides, repos etc and i will post these things, suggest me ideas for my next reel and the script
  and hook should be based on the logic of people's problem they face and how we can provide a solution based on it"
- Topics already covered (avoid repeating): hooks / first 3 seconds (HOOK), prompts that sound like you (PROMPT x2), AI
  study prompts (STUDY), Creedom CHECK and SCRIPT.
