# Creedom (creedom.ai): client knowledge export

Prepared for Nxtlvl Social. Built from the session chat, the repo files and the owner's uploads, up to 2026-11-17.
All times are UTC. Owner quotes are verbatim, typos included. "UNKNOWN" means the notes do not contain it.
"(uncertain: ...)" marks anything that could not be confirmed.

*Sources: scratchpad/notes_chat.md (cited "chat"), scratchpad/notes_creedom_files.md (cited "files"), scratchpad/notes_c100x.md (cited "c100x"). Repo root: /home/user/Nxtlvl-Social. Uploads folder: /root/.claude/uploads/b1c6bbee-7bc1-59ac-ac25-7b3da31f270a/ (cited "UP/").*

## Contents

1. [What Creedom is](#1-what-creedom-is)
2. [Features](#2-features)
3. [App UI: every label and number seen](#3-app-ui-every-label-and-number-seen)
4. [Website and brand look](#4-website-and-brand-look)
5. [Pricing, links, founders, contacts](#5-pricing-links-founders-contacts)
6. [Target audience, goals and KPIs](#6-target-audience-goals-and-kpis)
7. [The deal](#7-the-deal)
8. [Rules, dos and don'ts](#8-rules-dos-and-donts)
9. [Reels made for Creedom, with all feedback in date order](#9-reels-made-for-creedom-with-all-feedback-in-date-order)
10. [Voiceover facts](#10-voiceover-facts)
11. [Delivered files](#11-delivered-files)
12. [Open items](#12-open-items)

---

## 1. What Creedom is

- **Name and site:** Creedom, website **creedom.ai**. Spelling variants seen in owner messages: "creedom", "Creedum" (voice-typed, 2026-11-17T13:00:13), "creedom mascor" (typo for mascot). Pronounced "CREE-dum" (spelled "Cree-dum" for text-to-speech; IPA override used in code: `[Creedom](/kɹˈidəm/)`).
- **What it does (owner's framing):** an AI app for Instagram creators that analyses reels and accounts. The owner calls it "an app that can rate your video before you post" (2026-11-13T03:40:15).
- **In-app assistant:** the AI assistant inside the app is called **Cree** (home screen "How can Cree help?"; status cards "CREE · ON IT" and "CREE · DONE"; "Cree is thinking"). Cree is also the name of the mascot (see creedom-mascot.md).
- **Claim recorded in the repo:** "Creedom's AI companion explains why posts performed well or poorly; Creedom is an Official Meta Business Partner (Dec 2025): Indian Startup Times / Ascendants seed-round coverage." *(files 1.1, from creedom-reel-analyser-9x16/script.md "Claims and sources")* (uncertain: written in an earlier session; the press source itself was not re-checked in this session).
- **Positioning line we wrote** (after the owner asked "But when does instagram tells your reel flopped?", 2026-11-13T03:35:01): "Instagram never tells you a reel flopped. You just see the numbers in Insights, and Insights can now even show where people stopped watching. What it can't do is warn you before you post, or tell you why people left. That's the gap Creedom fills" (assistant, 2026-11-13T03:35:16).
- **Accounts seen connected to Creedom:** `ai.nxtlvl` (owner's screen recording, 2026-11-10; greeting "Afternoon, ai.nxtlvl.") and `creators.100x` (owner's home-screen screenshot, 2026-11-17). Creedom reels from 2026-11-13 on are posted on the Creators 100X page (owner: "it will be posted on Creators.100x but it is based on Creedom's feature of checking your reel before you post it", 2026-11-13T03:28:39).
- **Website load history:** in the October reel-analyser session "creedom.ai doesn't load from my sandbox. If you want site copy or visuals on screen, send screenshots." On 2026-11-10T12:50 creedom.ai did load in Playwright (screenshot and computed fonts only; page text not stored).

## 2. Features

Every feature named anywhere in the notes, with its source.

| Feature | What it does (as recorded) | Source |
|---|---|---|
| **Reel Analyzer** ("Creedom's Reel Analyzer") | Watches a reel "second by second"; says the hook worked / energy dropped / where people swiped away; gives "new hooks" and "what to fix before I post the next one". | Client script card UP/61a1bad2-image.jpg (= creedom-explainer-9x16/plan/script_card.jpg) |
| **Free account audit / content score /100** | "You can even get a free audit of your whole account. Just type your handle, and in about 20 seconds you get a score out of 100 and the first thing to fix." Reads public posts only. | Script card; reel-analyser files |
| Content score details (from the owner's Oct 2026 @ai.nxtlvl screenshots) | "YOUR CONTENT SCORE" 82 "/100"; "YOUR TOP INSIGHT" ("The next job is repeatability."); "READING YOUR PAGE" / "READING @AI.NXTLVL"; "Public data only"; ticks "Found your page: 6,205 followers" (also written "Found Nxtlvl.ai: 6,205 followers"), "Scanned 6 recent posts", "Creator audit ready"; app line "Give me 20 seconds." (Creedom's own line, in serif) | creedom-reel-analyser-9x16/build/generate.py lines 273-297, visual-plan.md |
| **Check a reel before you post** (reel score out of 5) | Scores a reel out of 5 with a word rating ("Good", "Very good"), a SECOND BY SECOND timeline of segments each with a score and a note, flagged moments each with a timestamp and a "→ Fix" line, per-category SCORES chips, better hooks, better CTAs and closing advice. Chat command seen: "@analyze-reels". | Owner recordings 2026-11-10 and 2026-11-13; START SOMETHING card |
| **@write-script** = "Get a script in your voice" | Typed in the chat box; returns a script with a hook, a story and a call to action. Owner confirmed only this ("yeah your 2nd assumption is correct", 2026-11-17T11:13:55). How Cree learns "your voice" is UNKNOWN (never confirmed). | UP/b4140fd8-image.jpg; script_options.md |
| **Ideas tuned to your account** | START SOMETHING card. No detail. | Screenshot, recording |
| **Send a DM to your comments** (DM to comments) | START SOMETHING card. No detail. | Screenshot, recording |
| **Your saved reels, organized** | Fifth START SOMETHING card, seen in the 2026-11-10 recording only (not on the 2026-11-17 screenshot). | Recording |
| Chat chips | "Audit my Instagram profile" / "Use one of my Reels and give me insights" / "Analyse one of my latest reels" | Screenshot, recording |
| Follow-up chips after a reel check | "Give me editing instructions for the first 5 seconds" / "Compare this with my best Reel" / "Write a script fixing these issues" | Recording |
| Reel input options | "Upload from phone", "Paste a link", or pick from your reel thumbnails | Recording |
| Result actions | "In your library", "Copy", "Share"; thumbs-up / thumbs-down / copy icons | Recording |

What we are allowed to claim (3D guide, creedom-3d-story/build/guide.cjs page 3, "What we can show", verbatim):
1. "It watches the whole reel, second by second, like a real viewer would."
2. "It scores the reel before you post, so you know where it stands."
3. "It flags the exact moments that need work: a weak hook, a claim with no proof, a moment that loses trust."
4. "Each flag comes with the timestamp and the fix, so you change the right second, not the whole video."
5. "It reads a creator's page and gives a content score from public posts."
Warning: "Don't claim guaranteed views, virality or follower numbers. Any score or view count in the story is shown as an example, never as a promise."

Features not yet covered by any reel: "Send a DM to your comments", "Ideas tuned to your account", "Your saved reels, organized", "Analyse one of my latest reels"; "Audit my Instagram profile" was covered only by the explainer's free-audit line.

## 3. App UI: every label and number seen

### 3.1 Home screen screenshot (UP/b4140fd8-image.jpg, sent 2026-11-17T11:06:36)
- Native size 1320 x 1734.
- Light warm-grey ground (about #f6f6f3), white rounded buttons.
- Top bar: round menu (hamburger) button; account pill "creators.100x" with a pink Instagram glyph and a dropdown chevron; round compose (pencil-square) button.
- Title, bold serif: "How can Cree help?"
- Three white pill chips: "Audit my Instagram profile" / "Use one of my Reels and give me insights" / "Analyse one of my latest reels".
- Label "START SOMETHING" (letter-spaced grey caps).
- Four white rounded cards with line icons: lightning "Ideas tuned to your account"; film strip "Check a reel before you post"; pen "Get a script in your voice"; paper plane "Send a DM to your comments".
- Input bar with a pink border: "+" button, text "@write-script" with a blue caret, black round send button with a white up-arrow.
- Bottom nav (from recording): "Chat" | "Tools".
- Input placeholder rotations: "Give me hook ideas", "What should I post next?", "Why didn't my last reel work?", "Write my next reel script".

### 3.2 Owner's app screen recording, 2026-11-10 (UP/3ad41639-ScreenRecording_11-10-2026_14-26-30_1.mp4 = creedom-explainer-9x16/assets/video/screen.mp4)
iPhone, 1320 x 2868, 60 fps, 113.48 s, HEVC 10-bit, recorded dimmed (brightened x2.02 in the edit). Account "ai.nxtlvl". Clock 14:26-14:28.
- 0 s home: Cree avatar + "Afternoon, ai.nxtlvl."; "How can Cree help?"; the 3 chips; START SOMETHING with 5 cards ("Ideas tuned to your account", "Check a reel before you post", "Get a script in your voice", "Send a DM to your comments", "Your saved reels, organized"); input "Give me hook ideas"; nav "Chat | Tools".
- 1 s: chip tapped; black user bubble "Use one of my Reels and give me insights"; "Cree is thinking ...".
- 9 s: card "CREE · ON IT": ✓ "Working out what you need..." / "Looking up your reels...".
- 14-16 s: Cree reply "Pick one Reel and I'll break down what's working, what's costing you retention, and the first change to make." Options "Upload from phone", "Paste a link", and reel thumbnails captioned 'Comment "JARVIS" [pointing emoji] a...' (thumbnail text "Jarvis is real now.") and 'Comment "WATCH" [pointing emoji] a...' (thumbnail "Claude Code can watch YouTube.").
- 23 s: user bubble 'Check "Comment "JARVIS" [pointing emoji] and I'll DM you the link."'. CREE · ON IT steps: "Working out what you need..." ✓, "Sending the reel to the feedback engine..." ✓, "Downloading and processing the video...", "Downloading and processing the video... (30s)", "Watching the reel end to end...", "Reading the scorecard...", "Working out the one change that matters...". Reply: "I'm sending that reel through the feedback engine. It watches the whole video, so give it a few minutes." (wait roughly 23 s to 98 s).
- 98 s: "CREE · DONE"; result card "OpenJarvis Stanford AI Assistant", big serif "4 / 5", "Good", green progress bar; summary "Your visual countdown at 0:00 hooks fast. Missing words in captions can look unpolished. Fix the on-screen grammar."
- "SECOND BY SECOND" (right side: "2 changes"):
  - Hook 0:00-0:05 (4): "Your inbox counter animation at 0:00 shows the exact problem in five seconds."
  - Repo Reveal 0:05-0:15 (3, amber dot): "Showing Stanford's GitHub star count at 0:09 proves credibility quickly." Fix: "→ Fix caption at 0:12: add 'has' before 'over 14,000 stars'."
  - Features & Setup 0:15-0:24 (3): "You show local privacy and one-command install with clear terminal visuals at 0:23." Fix: "→ Fix caption at 0:20: change 'It on' to 'It runs on'."
  - Close 0:24-0:30 (4): "Your automated comment ask at 0:25 gives a clear reason to reply."
- "SCORES" chips: Pacing 4, Hook 4, Ending 4, Visuals 4, Audio 4, CTA 4.
- "The breakout version of this idea": "The biggest upside sits in Stanford's name and running personal AI locally on your device."
- "Hooks that would've made this reel go viral": "Opening with inbox emails delays the reveal of Stanford's real open-source AI assistant." 1. "Stanford just open-sourced a real Jarvis that runs on your laptop." 2. "Stop paying for AI assistants when Stanford gave this away free." 3. "This open-source AI runs locally and sorts your entire day."
- "CTA that would've driven more shares & saves": "The ending asks for comments without prompting people to save the installation command." 1. "Save this command so you can install Jarvis on your laptop later." 2. "Share this with a developer who wants a local personal AI assistant."
- Closing advice: "Make the next revision in the opening: put the complete Stanford-and-local-AI promise on screen before the inbox counter. Then clean up the two grammar errors—polish matters when the reel is built around technical credibility."
- Clips used in the explainer (build/clips.py): c1_pick 12.6-15.6 s; c2_steps 15.6-30.0; c3_score 95.5-103.5 ("the score lands (3 -> 4 / 5)"); c4_fixes 103.5-113.4; scaled 660 x 1434; top 100 px painted #FDFDFD to hide the status bar.

### 3.3 Owner's "dummy" CHECK recording, 2026-11-13 (UP/45c9c5fc-ScreenRecording_11-13-2026_08-42-47_1.mov = creedom-check-9x16/footage/screenrec.mov)
1320 x 2140, 38.66 s, dimmed. Reel thumbnail ("8-HOUR STREAM INTO", 0:30), user bubble "@analyze-reels"; CREE · ON IT: "Sending the reel to the feedback engine...", "Downloading and processing the video...", "(30s)", "Watching the reel end to end...", "Reading the scorecard..."; same "I'm sending that reel through the feedback engine..." line. Result at about 34 s: "GTA 6 Creator Playbook", "3.8 / 5", "Good" (gold bar). Summary: "Your cuts at 0:05 keep rhythm. Hiding tool names might frustrate viewers. Name the AI tool at 0:14." SECOND BY SECOND ("1 change"): Hook 0:00-0:04 (4) "You pair trending game art with bold text by 0:02 to grab attention."; Proof 0:04-0:12 (4) "At 0:06 you show real view counts to validate your claim."; Tool and Settings Steps 0:12-0:25 (3) "You blur the tool name at 0:14, so viewers may lose trust." Fix: "→ Show the real name of the clipping tool on ..." (cut off). This is our own GTA 6 reel being scored.

### 3.4 Earlier (October) Creedom screenshots of @ai.nxtlvl (used in the reel-analyser reel; images themselves NOT FOUND in this session)
- Chat rebuild: user bubble 'Check "Comment TRADE and I'll DM you all 11 skills."'; "CREEDOM · ON IT" card with three steps.
- SECOND BY SECOND: Hook 0:00-0:05 (5), Skills Grid & Tour 0:05-0:19 (3), Time Machine Simulation 0:19-0:34 (5), Safety & Congress Tracker 0:34-0:41 (4), Close 0:41-0:46 (4).
- "4.2/5 · Very good".
- Fixes: "Lead with the Congress tracker", "Trim two tool cards (0:10–0:19)", "Keep the 0:03 simulation proof".
- Stats: 85x usual views, 126,000+ plays (draft 4 used "366K PLAYS"), "low thousands" typical, 82/100, 6 posts, 20 seconds, best hook buried at 0:34. These are real @ai.nxtlvl numbers from Oct 2026, not Creators 100X numbers.

### 3.5 Numbers that are ours (illustrations, not app output)
- Explainer: audit 78/100 and "First thing to fix: Show the payoff in your first 2 seconds"; hook ring 92/100; "−62% viewers"; retention 100% -> 96% -> 38%; "312 views", "↓ 84%"; "62% here", "viewers left at 0:03" (cover).
- CHECK: 4.2/5 "EXAMPLE REEL"; flags "0:01 · Weak hook", "0:07 · Claim, no proof", "0:14 · Loses trust"; "Fix: Name the tool on screen at 0:14"; demo reel "3 AI tools I use daily" (Pexels), handle "creator.daily".
- @write-script: Cree reply "On it. First, I'll take your measurements: your openers, your pauses, your words." (written by us); "40 scripts", tailor's ticket ("Here's the thing…", "honestly", "low-key").

## 4. Website and brand look

*Full colour tables for each reel are in files 3.2; the main brand values are below.*

- **Logo (client file):** UP/2077e237-image.jpg = creedom-explainer-9x16/assets/img/logo_src.jpg (1920 x 1080): Cree (waving, one foot kicked) left of the wordmark "Creedom" in a geometric rounded sans, title case, horizontal gradient magenta to pink to coral on white. Also UP/7920e74f-image.jpg (the logo whose font and colour the owner told us to use on the end card).
- **Logo gradient:** code value `linear-gradient(90deg,#F515E8 0%,#F54BA8 50%,#F5876C 100%)`. Pixel samples: x500 [245,16,231] magenta, x1400 [245,115,127] coral; read across letters C #f60fe9 -> #f629cc -> #f641b2 -> #f5599a -> m #f4856a.
- **Wordmark cut-out:** creedom-explainer-9x16/assets/img/wordmark.png (1426 x 269, transparent), cut from the client logo (exact letterforms and gradient). Wordmark-only version creedom-check-9x16/assets/img/creedom_logo.png (993 x 185).
- **Wordmark font:** the reel-analyser files call it Google Sans ("Google Sans, the face of the Creedom wordmark", commit 22004f2) (uncertain: not confirmed by the client).
- **Website look (creedom.ai, read 2026-11-10):** warm off-white fading into soft pink, gentle pink glows and glass bubbles; the hero has faint grey "creator worries" drifting past; headline serif **Fraunces** (sentence case, two-tone warm grey over black, key words pink italic); UI sans **Manrope**; black pill buttons; a lowercase serif "creedom" logotype on the site. Creator worries list used: "Why did my views drop?", "Algorithm changed again", "Is my content bad?", "No clarity", "What should I post?", "200 views", "Drowning in drafts", "Why isn't this working?", "Am I even good at this?", "15 hours, 200 views".
- **Site ink and accent:** `#0b0b0b` ink, `#e0187e` accent pink.
- **App colours (sampled from screenshots, Oct):** Paper #F6F6F4, Ink #0B0B0B, Pink #EE688B (progress bars, active caption pill, accents), Deep pink #B1476B on #FEF8FA (inline chips), Mascot pink #F343A2, Green #3E8E62 (ticks, "Very good" bar), Amber #C8902E (the "3/5" timeline dot).
- **App type (seen):** a bold serif for "How can Cree help?" and scores ("4 / 5", "3.8 / 5"); a geometric sans for the rest.
- **Official brand font:** UNKNOWN (uncertain: Google Sans in the older reel vs Fraunces/Manrope from the website).
- **Pink background is part of the look:** owner, 2026-11-17T13:00:13: "Keep the Creedum background as it is, like that pink type of background".
- **No star on the logo:** owner, 2026-11-10T13:57:39: "Just remove this star from creedom logo" (UP/1b4cb69f-image.jpg shows the pink-magenta 4-point star we had added).

## 5. Pricing, links, founders, contacts

| Item | Value |
|---|---|
| Pricing / plans | UNKNOWN. Only commercial claim: "a free audit of your whole account" (client's own script). |
| Website | creedom.ai |
| App store links | UNKNOWN |
| Link for the keyword auto-DMs ("[CREEDOM LINK]") | UNKNOWN. Asked for on 2026-11-13 (03:30:50, 04:02:04, 04:11:04, 04:22:45, 04:45:19, 05:42:22, 06:04:52, 06:17:54) and 2026-11-17 (11:43:19, 16:34:56). Never sent. |
| Founders | UNKNOWN |
| Client contacts (names, email, phone, WhatsApp) | UNKNOWN |
| Google Drive folder | UNKNOWN (no Drive link exists for Creedom; files were delivered as chat attachments) |
| Paid partnership | UNKNOWN. Repo note: "If this is a paid partnership: use Creedom's approved CTA and add Instagram's paid-partnership label." |
| Related workspace links | ElevenLabs flow used for the explainer VO and Cree poses: [link removed] (owner's workspace). Adobe asset [asset id removed] (cree_ref_white.png in folder "nxtlvl-creedom"). |

## 6. Target audience, goals and KPIs

- **Audience (from our 3D guide, "Who"):** "Creators who post reels and have no idea why one works and the next one doesn't." The Creedom reels on Creators 100X sit on a page whose audience the owner defined as "beginner creators that want to use ai" (2026-11-15T10:17:02).
- **Goal of the content (3D guide, "Goal"):** "Make one idea feel obvious: Creedom shows you why a reel will flop, before you post it, with the exact second and the fix."
- **Conversion mechanic:** every reel ends on a keyword CTA ("Comment CREE / CREEDOM / CHECK / SCRIPT") that triggers an auto-DM with the Creedom link.
- **KPIs, targets, sign-up goals:** UNKNOWN. No views, follows, sign-ups or results were ever reported for any Creedom reel. Posting dates: UNKNOWN.

## 7. The deal

| Term | Status |
|---|---|
| Deliverables per month | UNKNOWN |
| Promo vs non-promo split | UNKNOWN |
| Timelines / deadlines | UNKNOWN (no posting dates given) |
| Payment / fee / retainer | UNKNOWN |
| Approval process | UNKNOWN as a stated client process. In practice the owner reviews each preview and gives notes, then asks for the final ("Render in final", "give that in final export quality"). Possible relayed client feedback once: 2026-11-17T14:59:19 "Good concept! Just a few suggestions: ..." (uncertain: may be from the Creedom client or another reviewer). |
| Is Creedom a paying client or a partner of Creators 100X | UNKNOWN |

What has been delivered so far (5 pieces, no stated quota): reel-analyser reel (Oct, drafts), explainer (Nov 10-11), CHECK reel (Nov 13), 3D storytelling guide + Cree 3D model sheet + reference pack (Nov 14), @write-script reel (Nov 17).

## 8. Rules, dos and don'ts

Owner rules that apply to every Creedom reel, with the quote behind each.

**Mascot** (full detail in creedom-mascot.md)
- Never redraw or restyle Cree: "No you are changing the art style of it make him exactly like that i sent" (2026-11-10T10:52:00).
- He is not a bird: "Firstly that is not a bird so dont treat him like that" (2026-11-13T04:14:44). No flapping, waddle-as-bird, flying or spins; arms are arms.
- Always use the 13 3D poses, never the flat puppet: "when i say the mascot looks bad then it is bad , look how full he looks in the previous video make him like that" (2026-11-13T05:32:39).
- Use him, but "time to time": "use the Creedum mascot time to time" (2026-11-17T13:00:13).

**Concept and script**
- Hooks must sell the unique point: "No these dont hooks dont emphasize on the fact that there is an app that can rate your video before you post" (2026-11-13T03:40:15).
- Claims must be accurate: "But when does instagram tells your reel flopped?" (2026-11-13T03:35:01).
- No GTA in Creedom reels: "Na make the script better and also dont include the gta aspect" (2026-11-13T03:32:05).
- Each Creedom reel must look new, not a part 2: "this looks like the rebranding or some kind of part 2 of that earlier video we made, and I don't want to do that" (2026-11-17T12:24:23). Vary concept, voice, look and footage, but keep the Creedom pink background.
- Only real product features; no promised views or viral numbers; example numbers are labelled as examples (3D guide; CHECK "EXAMPLE REEL").
- "The creator is the hero, Cree is the guide ... he never takes the creator's win" (3D guide).
- Every script on the house arc: hook at 70 dropped mid-story, first peak by 5-15 s, peak/release, end on the CTA (CLAUDE.md).

**Look and motion**
- Premium glass, never paper: "everything should be in premium glass fluid animations nothinh should feel like paper/cardboard animation, keep that premium feel with it and also the transitions" (2026-11-13T03:28:39).
- No background bubbles: "Remove these bubble things in background it looks like an pimple" (2026-11-13T04:03:50).
- White/pink background from the website, not dark: "Keep the background white/pinkish gradient take the reference from their website" (2026-11-10T12:50:23).
- Use the client's own wordmark image (not retyped), no added star: "In the end just use this font for creedom and also the same color of this image" (2026-11-10T14:58:13); "Just remove this star from creedom logo" (2026-11-10T13:57:39).
- Don't show the brand name twice: "No need put the creedom text twice" (2026-11-13T05:32:39).
- Clean alignment, nothing colliding: "there are many frames that feel cluttered and out of proportion so use the space properly make sure everything is not colapsing on each other" (2026-11-10T11:39:30); "Look at all these alignment issues amd fix them" (2026-11-13T04:26:48).
- Build a clean notch, never the phone's real status bar: "crop the notch part just build a separate notch dont add my notch from the recording just add a clean notch with no other time details and all" (2026-11-10T11:39:30).
- Demo footage must not loop: "the dummy video you have used just loops for those few frames make sure there duration is a lot more then those few frames" (2026-11-13T04:14:44).
- Words appear only as they are spoken: "Animate this in a way they only appear when it's spoken not every word already there before even spoken" (2026-11-11T00:34:34).
- No dull frames; keep pace high: "videos feels very static in terms pacing", "Idk what is in this whole video but it still doesn't feel that engaging", "it still feels very slow in terms of pace".
- Bottom captions were removed on the explainer: "remove the bottom captions cause they do feel uneccesary" (2026-11-10T14:00:55).
- Frame rate chosen by the owner for the explainer: 40 fps (2026-11-10T13:24:25), then 37 fps (2026-11-10T14:58:13). Later Creedom reels: 30 fps.

**Audio**
- Never reuse a track already used: "change the background music we have already used that" (2026-11-13T04:03:50). Check Jamendo IDs used before.
- No singing in music: "i dont need singing in background it is very distracting" (2026-11-11T12:08:22, hook reel; applies house-wide).
- Music lower under the voice: "reduce the volume of the background music" (2026-11-17T13:00:13).
- SFX from Openverse first (CC0 / CC BY only), credit CC BY in the post (CLAUDE.md; owner: "Use this to add sound effects / npx "@opendirectory.dev/skills" install openverse-sfx --target claude", 2026-11-10T14:22:43).
- Text-to-speech must say "CREE-dum" (spell "Cree-dum").

**Posts and DMs** (house rules, CLAUDE.md)
- Description starts with the CTA keyword line; no emojis; numbered lists as "1."; up to 5 hashtags then one SEO keyword line; one paste-ready block; music credit line when CC BY.
- Auto-DM = the Creedom link plus setup steps only.
- Deliver the final with a cover and an SEO description: "Send final render with cover page and perfect seo description" (2026-11-17T16:29:45).
- The owner is often on a phone: "Im on a phone and cant download it there is no option" (2026-11-10T23:54). Keep files under 100 MB.

## 9. Reels made for Creedom, with all feedback in date order

### 9.1 Reel analyser: "My reel did 85x my usual. I had no idea why." (creedom-reel-analyser-9x16, October 2026)

- **Made:** before this session (folder created 2026-10-25; VO file dated 2026-10-24T22:01). Drafts 1-6 only; no renders folder; final delivery UNKNOWN.
- **Page:** most likely @ai.nxtlvl (end card "IG logo + @AI.NXTLVL"; uses @ai.nxtlvl stats) (uncertain: page not stated).
- **Brief:** "TITLE / ANGLE: "My reel did 85x my usual. I had no idea why." Creedom's reel analyser finds the reason, second by second." / "LENGTH: 32–35s · ~76 spoken words · LANGUAGE: English · VOICE: ElevenLabs "Nota 3" (rTMkoe3NzNrEOgFeBwY2), Eleven v3" / "FORMAT: faceless motion graphics · CTA KEYWORD: CREEDOM".
- **Script v1** (git 5662428, about 38 s, about 95 words, CTA CREE): "One reel did eighty-five times my usual views... and I had no idea why. / Next reel? A few thousand plays. Instagram shows you the numbers. Never the reason. / So I handed my page to Creedom. Twenty seconds. Public data only. / It read my last six posts... and scored my content. Eighty-two out of a hundred. / Then I dropped in a reel. Its reel analyser watches the whole video... and breaks it down, second by second. / Four point two out of five. And one fix I'd never have spotted... my best hook was buried at thirty-four seconds. / Now I edit with reasons. Not guesses. / Comment CREE... and I'll DM you the link to audit your own page."
- **Script v2 (final, script.md):** "[curious] One reel did eighty-five times my usual views... [softly] and I had no idea why. / [thoughtful] The next one? A few thousand. [softly] Numbers... never reasons. / [warmly] So I gave my page to Creedom. [smiling] Twenty seconds. / [impressed] Content score: eighty-two out of a hundred. / [intrigued] Then its reel analyser watched my reel... second by second. / [whispers] And found what I'd missed... [amazed] my best hook was buried at thirty-four seconds. / [confident] Now I edit with reasons. [smiling] Not guesses. / [playful] Comment CREEDOM... [warmly] and I'll DM you the link."
- Arc: Hook -> Stakes -> Turn (meet Creedom) -> Journey (score, reel analysis) -> Twist (buried hook) -> Resolution -> CTA; timing 0-4 / 4-8 / 8-11 / 11-14 / 14-19 / 19-26 / 26-30 / 30-34 s.
- Alt hooks: "126,000 plays on one reel. The next one? Barely three thousand." / "Your reel didn't flop. Your hook was just in the wrong second." / "I let an AI watch my reel... it found the mistake in 34 seconds."
- CTA keyword: CREEDOM (v1: CREE). Commits: e129911 "CTA keyword CREEDOM"; 59899a7 "say Creedom throughout, not Cree"; c7b7c3c mood tags; da02d91 "mood tags tuned for Nota 3"; 6d5fde0 "v2: trimmed to 35 s max (~76 words)".
- Caption (script.md; written before the no-emoji rule, emoji shown as text here): "One reel did 85x my usual views and I couldn't tell you why. [eyes emoji] / Comment CREEDOM and I'll DM you the link to audit your own page. / What Creedom's reel analyser gave me: / → a content score for my whole page (82/100) / → a second-by-second breakdown of one reel / → the exact fix: my best hook was buried at 0:34 / Save this for the next time a reel flops. / #instagramtips #contentcreator #reelstips #aitools #creatorgrowth". Cover text: "Why did this reel hit 85x?". Auto-DM: UNKNOWN.
- Format: 1080 x 1920, built at 60 fps, 33.6 s (VO 32.13 s). Look: "Creedom's app (paper #F6F6F4, ink #0B0B0B, pink) on the soft grid-and-pastel-glow background of the reference covers. All type is Google Sans ... headlines carry one accent in the wordmark's magenta-to-coral gradient ... the pink bird as the lead: it never stands still ... Every cut is a whip pan; one dark beat for the twist. No account handles on screen."
- Music: original synthesized "light, bouncy 100 bpm pop bed in F major"; synthesized SFX.
- Draft history: d497785 draft 1; 5af50ae draft 2 (no handles, wing rig); a8bc719 draft 3 (face rig); 3c3b3ec draft 4 ("standing bird puppet ... walk cycle, 366K views, Creedom wordmark and gradient"); 22004f2 (Google Sans, 60 fps); 1671a95 draft 6 ("immersive scenes, magnifier film-strip world, calmer bird, one CREEDOM"; end card logo with "Your reels, explained.").
- Client/owner feedback: none in this session's logs (UNKNOWN).

### 9.2 Creedom explainer: "This AI told me the exact second people stopped watching my reel" (creedom-explainer-9x16, 2026-11-10 to 2026-11-11)

- **Page:** Nxtlvl (file prefix `nxtlvl_`) (uncertain: exact page not stated).
- **Client inputs:** script card UP/61a1bad2-image.jpg (heading "CREEDOM" / "This AI told me the exact second people left my reel" / button 'COMMENT "CREE"'), mascot UP/91192a5a-image.png, logo UP/2077e237-image.jpg, app recording UP/3ad41639, pacing reference reference/promo_ref.mov (the Nxtlvl promo).
- **Script (client's own, verbatim):** "This AI told me the exact second people stopped watching my reel. I uploaded a reel that flopped into Creedom's Reel Analyzer, and it watched it second by second. It told me my hook worked, but my energy dropped in the middle, and that's exactly where people swiped away. It also gave me new hooks and showed me what to fix before I post the next one. You can even get a free audit of your whole account. Just type your handle, and in about 20 seconds you get a score out of 100 and the first thing to fix. Comment "CREE" and I'll send you the link." (108 words.)
- **CTA keyword:** CREE.
- **Final:** renders/nxtlvl_creedom-explainer_reels_9x16_v10.mp4, 1080 x 1920, 37 fps, 37.5 s, 51 MB (49.1 MB master), -16.0 LUFS, -4.4 dBTP, verify PASS. Cover: nxtlvl_creedom-explainer_reels_9x16_v10_cover.png.
- **Owner feedback, verbatim, in order:**
  - 2026-11-10T10:26:02 (brief): "Leave that for now i need you to make an explainer video on creedom.ai based on these scripts and context, follow the animation pacing and concepts from this promo video and use the screen recording however the script demands, make it highly interactive and immersive from the hook and till the end ,  this is the mascot of creedom, you can animate him to be very expressive and doing things ad per the script , you can take the idea of colors schemes from their logo, app or website, make a unique music that fits the context and also an good female voiceover from elevenlabs"
  - 2026-11-10T10:48:41: "What i meant was make the cree mascot lively make him walk or change his posture or pose he is in a single pose change that, make him stand on two legs aur move his hands and all and make his face expressive"
  - 2026-11-10T10:52:00: "No you are changing the art style of it make him exactly like that i sent"
  - 2026-11-10T11:39:30 (on v2): "Firstly the text animations on those top texts are really poor it doesnt even feels good and there are many frames that feel cluttered and out of proportion so use the space properly make sure everything is not colapsing on each other also crop the notch part just build a separate notch dont add my notch from the recording just add a clean notch with no other time details and all , videos feels very static in terms pacing there are not much motion elements and animations soo fix that add glass fluid ui type animations"
  - 2026-11-10T12:16:36 (on v3): "Idk what is in this whole video but it still doesn't feel that engaging"
  - 2026-11-10T12:50:23 (on v4, dark plum): "Keep the background white/pinkish gradient take the reference from their website rest improve how the font enters on the screen and give that in final export quality"
  - 2026-11-10T12:52:15: "Also also try to use the font styles in this website and animate them in a proper order type animation"
  - 2026-11-10T13:24:25 (on v5 final): "The starting hook texting,styling and how the text appears feels very dull and basic make it feel premium, take this animation and font style for reference this should be the exact motion tracking for it and keep the video in 40 fps" (reference: ScreenRecording_11-10-2026_18-52-51_1.mov, a 4.69 s iOS picker-wheel title; rebuilt in Inter)
  - 2026-11-10T13:57:39: "Just remove this star from creedom logo"
  - 2026-11-10T14:00:55: "And also change the font style and how these texts comes on screen with this style  preseny in the hook , and also remove the bottom captions cause they do feel uneccesary, keep the above caption type texts as i mentioned give them more glass liquid type of feel"
  - 2026-11-10T14:22:43: "Use this to add sound effects / npx "@opendirectory.dev/skills" install openverse-sfx --target claude"
  - 2026-11-10T14:42:07: "Can you also add a better background music with the help of openverse which fits the context and script"
  - 2026-11-10T14:58:13: "In the end just use this font for creedom and also the same color of this image and rest reduce the fps to 37"
  - 2026-11-11T00:30:55: "Now go back to the creedom edit"
  - 2026-11-11T00:34:34: "Animate this in a way they only appear when it's spoken not every word already there before even spoken so fix that and in many frames starting from hook the video feels dull so improve the colors and different motion elements that look very dull so improve them for whole video find all of those dull parts, improve hook on the basis of elements if it can make viewers stick to the video, dont change font placements in whole video just focus on removing dullness from video and also export it in final quality" ("this" = the hook side block "people / stopped / watching / my reel.") -> v10 final delivered 00:48:08.
  - 2026-11-11T12:44:12: "Meanwhile you work on this pls provide me with a good cover page for the creedom reel that represents the context of video" -> cover delivered 12:45.
- **Rejected or replaced along the way:** one-pose Cree ("single pose"); vector rig ("changing the art style"); v3 headline animations ("really poor"), clutter and the recording's notch; v3 overall ("doesn't feel that engaging"); v4 dark plum look; v5 hook ("dull and basic"); the logo star; bottom captions; synthesised music (replaced by Openverse "Inspiring Technology"); retyped wordmark (replaced by the client's wordmark image); 30 -> 40 -> 37 fps; side block shown up front (now appears as spoken).
- **Version dates:** v2 11:31:26; v3 12:09:33; v4 12:36:13; v5 "final export" 13:13:29; v6 13:44:08; v7 14:16:09; v7b 14:28:59; v8 14:48:15; v9 15:06:39 (all 2026-11-10); v10 final 2026-11-11T00:48:08.
- **Final build:** hook = iOS-style picker wheel in Inter ("This AI / told me / the exact / second.") with the focus line in the pink gradient and the side block appearing as spoken, live RETENTION card (100% -> 96% -> 38%, 7 viewer avatars, "0:07 · they left here"); upload scene ("my_reel.mp4", "Uploading 0-100%", "312 views", "↓ 84%", FLOPPED stamp); phone with app clips and tickers "REEL ANALYZER · SECOND BY SECOND · HOOK SCORE · RETENTION" / "CREEDOM · AI FEEDBACK · WHAT TO FIX · NEW HOOKS", chip "Creedom · Reel Analyzer", "Second by second."; rolling pill "HOOK WORKED ✓ / ENERGY DROPPED ↓ / PEOPLE SWIPED ←", hook ring 92/100 "HOOK · 0:00-0:03 Strong start", "↓ dropped at 0:07", "−62% viewers"; 3D wall of hook cards ("Stanford just open-sourced a real Jarvis", "Stop paying for AI assistants", "This open-source AI sorts your day", "Nobody tells you this about reels", "I tested 5 hooks so you don't have to", "Your first 2 seconds decide it"), "New / hooks.", "What to fix." chips "Caption at 0:12", "Caption at 0:20", "Save-worthy CTA"; liquid blob wipe to "Free." / "Account / audit." with steps "@ Type your handle", "About 20 seconds" (20 -> 0 ring), "Your score" (78/100), "FIRST THING TO FIX / Show the payoff in your first 2 seconds"; CTA "Comment" + black pill typing "CREE", paper plane, glass DM "Creedom / Here's your link [link emoji]"; end card Cree icon + client wordmark + "creedom.ai", pink grid floor, sparkles. Titles on liquid-glass capsules; background white to hot pink with magenta, coral and violet glows.
- **Voice:** ElevenLabs "Hallie - Fun, Young & Feminine" (jpICOesdLlRSc39O1UB5), eleven_v3, 2 takes at 654 credits each (39.12 s and 42.64 s), take 1 tightened from 39.16 to 35.43 s.
- **Music:** final "Inspiring Technology" by Soundrider/Dope (Openverse/Jamendo, CC BY 3.0), cut so its drums kick in on "second.", low-pass dip on "energy dropped", jump to the track ending at "Comment". Before: original synth, 120 BPM, A major (build/music.py).
- **SFX:** Openverse searched first; Freesound refused (HTTP 403), so CC0 OpenGameArt packs: 100-cc0-sfx (rubberduck), 75-cc0-breaking-falling-hit-sfx (rubberduck), bell-dingschimes (PWL), fantasy-magic-spell (Almitory), fantasy-sound-effects-tinysized-sfx (Vehicle), interface-sounds (Kenney), swishes-sound-pack (artisticdude), ui-sounds (StumpyStrust), wind-hit-time-morph (qubodup). 54 cues from 23 sounds.
- **Post description (2026-11-10T14:48:25, kept for v10), verbatim:**
```
Comment "CREE" and I'll send you the link.

This AI told me the exact second people stopped watching my reel.

I put a reel that flopped into Creedom's Reel Analyzer. It watched it second by second and showed me my hook worked, but my energy dropped in the middle, and that's exactly where people swiped away. Then it gave me new hooks and told me what to fix before I post the next one.

You can also get a free audit of your whole account. Type your handle and in about 20 seconds you get a score out of 100 and the first thing to fix.

Music: "Inspiring Technology" by Soundrider/Dope (CC BY 3.0)

#reelstips #instagramgrowth #contentcreator #aitools #creedom
instagram reel analyzer, why my reels flop, instagram retention, reel hook ideas, free instagram account audit, ai tool for creators, how to grow on instagram, instagram reels tips
```
- **Cover (2026-11-11T12:45:49):** "This AI found / the exact second / people stopped watching", "exact second" in the pink-to-violet gradient (#ff2a6d -> #e0187e -> #b14dff); "Audience retention" card, chip "↓ 62% here", line falling off a cliff at a red dashed 0:03 playhead, black tag "viewers left at 0:03"; Cree in the "mag" pose on the drop; Creedom wordmark at the bottom; Inter 600-800; key content inside the 3:4 grid crop.
- **Auto-DM (CREE):** never written (link missing).

### 9.3 CHECK: "An app that rates your reel before you post" (creedom-check-9x16, 2026-11-13, posted on Creators 100X)

- **Final:** renders/creators100x_creedom-check_reels_9x16_v1.mp4, 1080 x 1920, 30 fps, 23.5 s, 27 MB, -14 LUFS, -1.5 dBTP (house check wants -4 dBTP: "NEEDS FIX"), 72 SFX cues. Cover: _v1_cover.png. Delivered 2026-11-13T06:17:42.
- **Owner feedback, verbatim, in order:**
  - 2026-11-13T03:28:39 (brief): "Now i need you to work for another reel it will be posted on Creators.100x but it is based on Creedom's feature of checking your reel before you post it soo i will share you a dummy screen recording based on that but you need to add a concept of your own for that visual and everything should be in premium glass fluid animations nothinh should feel like paper/cardboard animation, keep that premium feel with it and also the transitions" (with the dummy recording and a reference reel: bright fluid gradients, dark glow scenes, frosted-glass pills, tilting 3D glass cards, motion-blurred text, italic serif accents)
  - 2026-11-13T03:32:05: "Na make the script better and also dont include the gta aspect" (rejected the "Pre-flight check" script about our GTA 6 reel and its real 3.8/5)
  - 2026-11-13T03:35:01: "But when does instagram tells your reel flopped?" (rejected the hook "Instagram tells you your reel flopped. It never tells you which second killed it.")
  - 2026-11-13T03:40:15: "No these dont hooks dont emphasize on the fact that there is an app that can rate your video before you post"
  - 2026-11-13T03:42:26: "Okay perfect start making" (approved hook 1, keyword CHECK, voice af_heart)
  - 2026-11-13T04:03:50 (on v1): "Remove these bubble things in background it looks like an pimple and why didnt you use the creedom mascot that we made for this, use him and also change the background music we have already used that"
  - 2026-11-13T04:14:44 (on v2): "Firstly that is not a bird so dont treat him like that and secondly his animations look very bad the last time you made him it was better so fix that and there are many alignment issues in text placements soo fix that, the dummy video you have used just loops for those few frames make sure there duration is a lot more then those few frames"
  - 2026-11-13T04:26:48 (on v3, 4 screenshots): "Look at all these alignment issues amd fix them and also the creedom mascor still looks bad he is not in the same quality as previous reel on creedom, and there are still very less glass animations"
  - 2026-11-13T05:32:39 (on v4, 3 screenshots): "No need put the creedom text twice and secondly when i say the mascot looks bad then it is bad , look how full he looks in the previous video make him like that"
  - 2026-11-13T05:46:24 (on v5): "Now in terms of detailing everything is on point but i have noticed it still feels very slow in terms of pace it could be the background music or less motion graphics and transitional elements or many other animations being less, lemme know some suggestions"
  - 2026-11-13T05:48:02: "Go with all of them" (8 pace fixes: voice 1.12x, punchier 120-128 BPM track, split score scene, snappier transitions, punch-ins on key words, more in-between motion, busier sound, start in motion)
  - 2026-11-13T06:12:05 (on v6): "Fix this flickering from 0:13 rest give it in the final render quality"
- **Rejected hooks:** "I almost posted this reel. Then an AI watched it first." (GTA version); "Instagram tells you your reel flopped. It never tells you which second killed it."; "By the time Instagram shows you where people swiped away, it's already posted. And it never tells you why."
- **Final script (approved 2026-11-13T03:42), arc-labelled:**
  - Hook (70): "There's an app that rates your reel before you post it, and tells you exactly what to fix."
  - Peak 1 (contrast): "Not views after you post. Reasons, before."
  - Release: "It's called Creedom. It watches your whole reel, second by second, like a real viewer."
  - Peak 2: "Then it scores it out of five…"
  - Peak 3: "…and flags the exact moments that need work: a weak hook, a claim with no proof, a moment that loses trust."
  - Peak 4: "With the timestamp, and the fix."
  - Release: "So you fix it before anyone ever sees it."
  - CTA: "Comment CHECK and I'll send you the link."
- **Scene timings:** hook 0-3.92, contrast 3.92-6.34, creedom 6.34-9.96, score 9.96-17.21, fix 17.21-18.72, post 18.72-20.83, cta 20.83-23.54 s.
- **Versions:** v1 (35fac60) liquid-glass lens orb, Pexels demo reel, "Inspiring Technology"; v2 (27ef1e7) flat puppet replaces the orb, no background spheres, music "Down For You"; v3 (041ffdb) calm face-led mascot, clean headline breaks, 30 s demo reel; v4 (38a82c6) one layout grid, glass transitions, shine and tilt; v5 (e0ce853) Cree as the 13 3D poses, one Creedom in the intro; v6 (00a584a) faster pace; v6.1 (8eaf68b) chips leave as one group (0:13 flicker fixed). Preview times: v1 04:01:55; v2 04:10:56; v3 04:22:38; v4 04:45:05; v5 05:42:12; v6 06:04:40.
- **On-screen copy:** "An app that rates your reel before you post." chip "tells you exactly what to fix"; Share pill with lock -> "Post it"; cards "AFTER YOU POST / Views / numbers, no reasons" vs "BEFORE YOU POST / Reasons / Hook Proof Trust / with the exact second"; "It's called" + Creedom logo pill; "WATCHING 0:00-0:15"; frame strip 0:01 0:04 0:07 0:10 0:14; gauge 0.0 -> 4.2 "/5" "EXAMPLE REEL"; "Scores it out of five."; "Flags the exact moments."; flags "0:01 Weak hook", "0:07 Claim, no proof", "0:14 Loses trust"; fix card "The tool is never named, so viewers can't follow along. / FIX Name the tool on screen at 0:14."; "Fix it before anyone sees it." "✓ 0:14 fixed"; CTA "Comment" / "CHECK" / "Add a comment…" / "and I'll send you the link." / "Creedom sent you the link now".
- **Voice:** Kokoro-82M af_heart (Apache 2.0), v6 about 1.12x faster (generated faster, not time-stretched), "Creedom" as CREE-dum.
- **Music:** v1 "Inspiring Technology" (rejected, already used); v2-v5 "Down For You (chillout lounge track 2016)" by Dj Quincy Ortiz (CC BY 3.0); v6/final "Corporate Music" by Ruslan Latypov (Jamendo 1693123, CC BY 3.0, 99.4 bpm).
- **SFX (all CC0, Freesound previews via Openverse):** "Swosh swoosh whoosh air sound, free, high quality" and "Swipe Whoosh" (qubodup), "Deep Whoosh #1" (Kinoton), "Cinematic Impact" and "Riser" (Rizzard), "Thump.mp3" (mpuffenbarger), "Padlock Closing" (Rudmer_Rotteveel), "UI Button Click" (benzix2), "Mouth pop" (jcallison), "cash register chching" (disman), "buzzer.mp3" (Loyalty_Freak_Music), "Notification Sound" (Rickplayer), "[SFX] car screech 2" (waveplaySFX), "Camera Shutter" (roachpowder).
- **Post description (2026-11-13T06:17:54), verbatim:**
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
- **Cover:** light pink fluid-glass world; "An app that *rates* / your reel *before* / you post." (Inter 700 + Instrument Serif italic; "rates" #B1476B, "before" #EE688B -> #F343A2); tilted phone with "3 AI tools I use daily"; glass badge "4.2/5 EXAMPLE REEL"; pill "0:14 Loses trust"; Cree cheering; black pill "COMMENT CHECK".
- **Auto-DM (CHECK):** never written; still needs the Creedom link.

### 9.4 Creedom 3D storytelling guide and Cree 3D pack (creedom-3d-story, 2026-11-14)

- 2026-11-14T04:28:46 OWNER: "Now i need you to make a 3d render storytelling for creedom but i think this session is not trained to make 3d renders soo give me a pdf for the Concept/NxtlvlSocial cause that is where 3d render happens so provide me with the perfect guideline how and what topic/concept should be used for story telling and also the art/visual style, how the creedom mascot should look" -> delivered 04:35:27: renders/creedom_3d-storytelling-guide.pdf (14 pages, 1080 x 1350, 5.99 MB).
- 2026-11-14T08:08:32 OWNER: "Okay, before this edit, can you help me with the Creedom mascot? Like I wanted to, build a 3D render around that mascot. So just, give me all the images or how you made that mascot to be, fully animated in 3D. So give me those files or PDF or any images that can be helpful for making the 3D render." -> delivered 08:12:11: creedom_cree-3d-model-sheet.pdf (7 pages, 2.79 MB) and creedom_cree-3d-reference-pack.zip (32 files, 15.0 MB).
- Guide "At a glance": What "A 3D animated storytelling reel for Creedom, starring its mascot Cree." Goal "Make one idea feel obvious: Creedom shows you why a reel will flop, before you post it, with the exact second and the fix." Who "Creators who post reels and have no idea why one works and the next one doesn't." Length "35 to 45 seconds. Vertical 9:16, 1080 x 1920." Format "Character story, no talking head. Voiceover plus Cree's acting. Minimal on-screen text." CTA "Comment CREEDOM and we DM the link." Hero "The creator is the hero; Cree is the guide who shows the way. Cree never takes the credit."
- Story rules: 1 "Open mid-story at full tension. The first 2 seconds already show the problem; no logo, no intro." 2 "First peak by 5 to 15 seconds: a contrast or a surprise (the best moment was hiding at 0:34)." 3 "Then peak, release, peak, release. Each beat is one clear visual idea." 4 "Make the product moment physical. The timeline is a path Cree walks; a flag is a glowing tag; the fix is something he picks up and moves." 5 "One problem, one creator, one fix. Don't explain every feature." 6 "End on the CTA, with Cree and the Creedom wordmark on screen."
- Concepts: A "The Buried Hook" (recommended), B "The Screen Test", C "The Reel Gym", D "The Case of the Missing Views". Concept A VO, shot list, art direction and render spec: see creedom-mascot.md section 9.
- Feedback on either 3D deliverable: UNKNOWN (none received). Whether the render was made in Concept/NxtlvlSocial: UNKNOWN.

### 9.5 @write-script: "MADE TO MEASURE" (creedom-write-script-9x16, 2026-11-17, posted on Creators 100X)

- **Final:** renders/creators100x_creedom-write-script_reels_9x16_v4.mp4, 1080 x 1920, 30 fps, 38.5 s, 40 MB, -14 LUFS, -1.5 dBTP, 95 SFX cues, delivery quality. Cover _v4_cover.png. Delivered 2026-11-17T16:34:42.
- **Owner feedback, verbatim, in order:**
  - 2026-11-17T11:06:36 (with home-screen screenshot): "Make another reel for creedom based on this context and give me suggestions for visuals and scripts"
  - 2026-11-17T11:13:55: "Go with option A and every single visuals ideas in this reel that you mentioned, yeah your 2nd assumption is correct" (2nd assumption: "What `@write-script` returns. I've assumed a script with a hook, a story and a call to action." 1st assumption, how Cree learns "your voice", never confirmed.)
  - 2026-11-17T12:24:23 (on v1): "See, this looks like the rebranding or some kind of part 2 of that earlier video we made, and I don't want to do that. So change the voiceover style, like make it more expressive and add some different concepts, and use a different video, or don't use a video at all. Try to explain or make the things with more animation elements, because it looks the same as the previous reel we made. So try something unique."
  - 2026-11-17T13:00:13 (on v2): "Keep the Creedum background as it is, like that pink type of background, and also use some more animations in the first hook person, like add a mascot, like add a person, okay, and use the Creedum mascot time to time. Just show the exact UI of that screenshot that I send you and animate it accordingly, like write something related to that context. Rest, yeah, you can add more animations and more elements. So yeah, and also change the sound effects a little bit. Rest, also reduce the volume of the background music."
  - 2026-11-17T13:29:08: "Render in final" (v3 final delivered 13:33:39)
  - 2026-11-17T14:57:56: "Do one thing firstly give me a good expressive voiceover script of an female from elevenlabs with moodbrackets"
  - 2026-11-17T14:59:19: "Good concept! Just a few suggestions: / 0:01-0:03 - can we make the scripts come in front of the person instead of behind them? / 0:03 - Not one fit -> Not one worked / 0:06 - off the rack -> off the shelf / 0:15 - @writescript need not be spoken out loud / Make the changee accordingly and now give me the script" (uncertain: phrased like forwarded client or reviewer feedback)
  - 2026-11-17T15:03:24: uploads ElevenLabs_2026-11-17T15_02_49_Blondie_-_Conversational_eleven_v4.mp3 (his own take; became the VO, 37.8 s)
  - 2026-11-17T16:29:45: "Send final render with cover page and perfect seo description"
- **Options offered (11:08):** A "The blank screen" (chosen); B "Stop asking ChatGPT for scripts" (contrarian): "Stop asking AI to write your reel scripts. / Every one of them sounds the same, because it has never heard you talk. / Here's the same idea, two ways. / Left: a generic AI script. Right: Creedom's write-script, after it read my last reels. / Same topic. Only one of them sounds like me. / It even kept my opener and my sign-off. / Comment SCRIPT and I'll send you the link."; C "Which one did I write?" (comment bait): "One of these scripts I wrote. One an AI wrote. / Script one... (reads 2 lines). Script two... (reads 2 lines). Which one's mine? / Lock in your guess. Three, two... / Neither. Both came from Creedom's write-script. / It reads your reels first, so the script comes back in your voice. / Which is why you couldn't tell. / Comment SCRIPT for the link. And tell me which one you picked."
- **v1 VO (Option A, rejected):** 0-3 s "Camera's set up. Lights on. And I've got nothing to say." / 3-8 s "So I asked AI for a script... and it sounded like a LinkedIn post." / 8-12 s "Because it's never seen a single one of my reels." / 12-16 s "So I typed one thing into Creedom. At write-script." / 16-22 s "It read my reels first. My openers, my pauses, the words I actually use." / 22-27 s "Then it wrote the script... and it opened the way I always open." / 27-30 s "Hook, story, call to action. In my words." / 30-34 s "Comment SCRIPT and I'll DM you the link." (Kokoro af_heart, 26.4 s, glass look, Pexels footage, Cree, music "Corporate Music".)
- **v2 "Made to measure" (rejected for losing the Creedom look):** AI scripts as off-the-rack clothes, write-script as a tailor; sewing-pattern paper in Creators 100X colours; no glass, no Cree, no footage; Chatterbox voice with an af_bella reference.
- **v3 (final at 13:33):** Creedom pink fluid worlds back; cartoon person in a mirror; Cree as the tailor; app home screen rebuilt from the screenshot with "@write-script my 5am routine reel" typed and Cree replying "On it. First, I'll take your measurements: your openers, your pauses, your words."; music about 5 dB lower.
- **v4 (final):** scripts in front of the person; "Not one worked"; "off the shelf"; "@write-script" typed on screen, not spoken; the owner's ElevenLabs voice.
- **Final VO script with mood brackets (2026-11-17T15:00:22), verbatim:**
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
  Earlier version (14:58:42) had "Not one of them fit.", "They're all off the rack." and "[curious] So I opened Cree-dum, and typed... [playful] at write script."
- **On-screen headlines v4:** "I tried on 40 AI scripts." / "Not one worked." / "Off the shelf." / "Every creator. On earth." / "None of them ever heard you." / "I opened Creedom, and typed this:" / "It takes your measurements." / "It cuts to fit." / "Stitched in your voice." / "Sounds like me."; shelf cards "Hey guys!", "Let's dive in!", tag "ONE SIZE FITS ALL", stamp "DIDN'T WORK"; ticket "MEASUREMENTS @creators.100x": OPENER "Here's the thing…", PAUSES "right after the hook", WORDS "honestly", "low-key"; "MADE TO MEASURE"; DM "creators.100x sent you the link now"; badge Creedom logo + "@write-script".
- **Music:** v1 "Corporate Music" (Ruslan Latypov); v2+ "Swinging Around" by Daniel Bautista (Jamendo 2126278, CC BY 3.0, 117.45 bpm).
- **SFX v3/v4:** "Scissor Snip 02" jayroo9 CC0; "Sewing machine" Jagadamba CC BY 4.0; "Fabrics.mp3" livvy0221 CC0; "37-cloth.wav" tilano408 CC0; "Coathanger Clothes Hanger" dersuperanton CC BY 4.0; "Sliding Clothes on Rail 2" _MC5_ CC BY 4.0; "Cartoon Boing.wav" reelworldstudio CC0; "Tape Measure Open and Close 2.wav" sophiehall3535 CC0; "Keyboard Typing Tapping.wav" Psykophobia CC0; "GLEAM-GLOW-SFX-CHIME.wav" newagesoup CC0; "Message sound.wav" Sunart1 CC0.
- **v1 post description (git 46a7ae5, superseded):** 'Comment "SCRIPT" and I'll DM you the link. / Camera set up, lights on, and nothing to say. / Most AI scripts sound the same because they've never seen a single one of your reels. Creedom's write-script reads your reels first, then writes the script the way you actually talk: / 1. An opener that sounds like yours / 2. The story in your words / 3. A call to action that sounds like you / Save this for the next time you stare at a blank page. / Music: "Corporate Music" by Ruslan Latypov, CC BY 3.0 / #reelscript #contentcreator #instagramreels #aitools #creedom / how to write reel scripts, reel script ideas, ai script writer for reels, instagram reel hooks, content ideas for creators, how to sound natural on camera, ai tools for content creators, script writing for instagram'
- **Final post description (2026-11-17T16:34:56), verbatim:**
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
- **Auto-DM (SCRIPT), verbatim:**
```
Creedom: [CREEDOM LINK]
1. Open the link and connect your Instagram account.
2. Type @write-script in the chat box.
3. Tell it what your reel is about and send. It comes back with a hook, a story and a call to action.
```
  "[CREEDOM LINK] is the same link as the CHECK reel's DM." (link UNKNOWN)
- **Cover:** "I TRIED 40 AI SCRIPTS / Not one worked." over the mirror shot with the "DIDN'T WORK" stamp, Cree sad with a sweat drop, badge "SCRIPT 40 / 40", badge "Creedom @write-script fits you".

## 10. Voiceover facts

| Reel | Voice | Notes |
|---|---|---|
| Reel analyser | ElevenLabs "Nota 3" (rTMkoe3NzNrEOgFeBwY2), Eleven v3 | file ElevenLabs_2026-10-24T22_01_18_V_eleven_v4.mp3; Stability "Natural", 3-4 takes, 1.05-1.1x if over 35 s |
| Explainer | ElevenLabs "Hallie - Fun, Young & Feminine" (jpICOesdLlRSc39O1UB5), eleven_v3 | brief asked for "an good female voiceover from elevenlabs"; other candidates: "Laura - Enthusiast, Quirky Attitude" (FGY2WhTYpPnrIDTdsKH5), "Emotional Expressive Alexis" (FCdKzv68Ofr4VUDcZXIy), "Haley Maven - Social Media Bestie" (S9NKLs1GeSTKzXd9D0Lf) |
| CHECK | Kokoro-82M af_heart (open source, local) | the Creators 100X house voice |
| @write-script v1 | Kokoro af_heart | rejected style |
| @write-script v2/v3 | Chatterbox (MIT) with Kokoro af_bella reference | "a different voice from the earlier reels" |
| @write-script v4 | ElevenLabs "Blondie - Conversational" (owner's own take) | filename says eleven_v4; our build notes say Eleven v3 (uncertain which model) |

- ElevenLabs guidance we gave the owner: "choose the Eleven v3 model, because the tags only work on v3"; "Stability: "Creative" gives the most emotion. Switch to "Natural" if a take sounds overdone."; "pick a warm, young female narrator"; "make 3–4 and keep the best one. It should land around 35 s; if it runs long, speed it up 1.05–1.1x."
- Language: English only.
- Credits: explainer VO 2 x 654 ElevenLabs credits; Scribe 0 credits. On 2026-11-12T19:01:13 the owner mentioned "not having credits" on ElevenLabs (about another reel) (uncertain).

## 11. Delivered files

*All under /home/user/Nxtlvl-Social. MP4s and client media are kept out of git (the repo is public).*

- Explainer: creedom-explainer-9x16/renders/ preview_creedom-explainer_reels_9x16_v2/v3/v4/v6/v7/v7b/v8/v9.mp4; nxtlvl_creedom-explainer_reels_9x16_v5.mp4 (first "final"); nxtlvl_creedom-explainer_reels_9x16_v10.mp4 (final); nxtlvl_creedom-explainer_reels_9x16_v10_cover.png.
- CHECK: creedom-check-9x16/renders/creators100x_creedom-check_reels_9x16_draft.mp4; creators100x_creedom-check_reels_9x16_v1.mp4 (final); _v1_cover.png; caption.md.
- 3D: creedom-3d-story/renders/creedom_3d-storytelling-guide.pdf, creedom_cree-3d-model-sheet.pdf, creedom_cree-3d-reference-pack.zip.
- @write-script: creedom-write-script-9x16/renders/creators100x_creedom-write-script_reels_9x16_draft.mp4 (v1), _v2_draft.mp4, _v3_draft.mp4, _v3.mp4, _v4_draft.mp4, _v4.mp4 (final), _v4_cover.png; caption.md; plan/script_options.md; plan/elevenlabs_vo.md.
- Reel analyser: creedom-reel-analyser-9x16/ (script.md, visual-plan.md, build/; no renders).

## 12. Open items

- The Creedom link for every keyword DM (CREE, CHECK, SCRIPT): never received.
- How Cree learns "your voice" for @write-script: unconfirmed (asked 2026-11-17T12:54:30 and 13:13:24).
- Peak level: delivered at about -1.5 dBTP vs the house -4 dBTP; offer to redo the sound mix unanswered (2026-11-17T13:33:49, 16:34:56).
- Mascot crops still in old git commits; removal offer unanswered (2026-11-10T11:12:51).
- 3D render: no feedback; Higgsfield image-to-3D offer unanswered.
- Unused feature ideas: "Send a DM to your comments", "Ideas tuned to your account", "Your saved reels, organized", "Analyse one of my latest reels"; @write-script options B and C (C needs two real Cree scripts from the Creators 100X account); 3D concepts B, C, D.
- Deal terms, contacts, pricing, KPIs: all UNKNOWN; ask the owner.
