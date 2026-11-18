# Open items: Creedom and Creators 100X

Knowledge export for Nxtlvl Social. Pending tasks, unanswered questions, client requests and things to fix for Creedom
(creedom.ai, mascot Cree) and Creators 100X (@creators.100x), each with its source and date. Written 2026-11-17.
Times UTC. "UNKNOWN" = not in any source. "UNCERTAIN" = inferred, not confirmed.

## Index

1. [Summary](#1-summary)
2. [Blocking: links needed for the auto-DMs](#2-blocking-links-needed-for-the-auto-dms)
3. [Unconfirmed product facts and claims](#3-unconfirmed-product-facts-and-claims)
4. [Previews, approvals and pending client changes](#4-previews-approvals-and-pending-client-changes)
5. [Missing deliverables](#5-missing-deliverables)
6. [Technical fixes](#6-technical-fixes)
7. [Repo, privacy and documentation housekeeping](#7-repo-privacy-and-documentation-housekeeping)
8. [3D work for Creedom](#8-3d-work-for-creedom)
9. [Business unknowns: deal, stats, relationships](#9-business-unknowns-deal-stats-relationships)
10. [Uncertain facts to confirm](#10-uncertain-facts-to-confirm)

---

## 1. Summary

| # | Item | Brand | Type | Since | Who acts |
|---|---|---|---|---|---|
| 2.1 | Real Creedom link for the CREE, CHECK and SCRIPT auto-DMs | Creedom | blocking | 2026-11-13 | owner / client |
| 2.2 | Hosted links for the HOOK, STUDY and PROMPT PDFs | Creators 100X | blocking | 2026-11-12 | owner |
| 2.3 | CHECK and CREE auto-DM texts never written; HOOK and STUDY DM blocks never written | both | deliverable | 2026-11-12 / 13 | us, once links exist |
| 3.1 | "Reads your reels" / "takes your measurements" claim unconfirmed | Creedom | client question | 2026-11-17 | owner / client |
| 3.2 | What the other app features do (DM to comments, ideas, saved reels) | Creedom | client question | 2026-11-17 | owner / client |
| 3.3 | "Official Meta Business Partner (Dec 2025)" claim unverified | Creedom | fact check | 2026-10 | us |
| 4.1 | Previews awaiting approval: none | both | status | 2026-11-17 | n/a |
| 4.2 | Riya reel: owner said he will send changes later | Creators 100X | pending request | 2026-11-15 | owner |
| 4.3 | Reel Analyser (October) left at draft 6 | Creedom | parked | 2026-10-25 | owner decides |
| 5.1 | No cover for the split-screen prompt reel | Creators 100X | deliverable | 2026-11-15 | us (offer open) |
| 5.2 | No caption.md for the explainer and the Reel Analyser | Creedom | housekeeping | 2026-11-10 | us |
| 6.1 | True peak -1.5 to -1.8 dBTP vs the -4 dBTP check on six finals | both | technical | 2026-11-12 on | owner decides standard |
| 7.1 | brand.md PDF list outdated | Creators 100X | docs | 2026-11-15 | us |
| 7.2 | Logo and PDFs public in the repo: keep private? | Creators 100X | privacy question | 2026-11-12 | owner |
| 7.3 | Mascot crops still in git history | Creedom | privacy question | 2026-11-10 | owner |
| 8.1 | 3D reel status; Higgsfield image-to-3D offer | Creedom | unanswered | 2026-11-14 | owner |
| 9.x | Deal terms, posting dates, stats, page ownership | both | unknown | always | owner |

---

## 2. Blocking: links needed for the auto-DMs

### 2.1 The real Creedom link (CREE, CHECK, SCRIPT)

- Every Creedom keyword DM points at `[CREEDOM LINK]`. The owner never sent the link (NOT FOUND in chat or files).
- Asked on: 2026-11-13 03:30:50, 04:02:04, 04:11:04, 04:22:45, 04:45:19, 05:42:22, 06:04:52, 06:17:54 ("For the CHECK
  auto-DM, I still need the Creedom link. Send it and I'll hand over the DM text, or a PDF if you'd prefer one.");
  2026-11-17 11:43:19 and 16:34:56 ("still needs the Creedom link").
- Affected:
  - CREE (Creedom explainer, `creedom-explainer-9x16`): no DM text at all.
  - CHECK (`creedom-check-9x16/caption.md`): "The CHECK keyword DM sends the Creedom link (still needed from the owner)."
  - SCRIPT (`creedom-write-script-9x16/caption.md`): DM written with the placeholder; "[CREEDOM LINK] is the same link as the
    CHECK reel's DM."
  - CREEDOM (October Reel Analyser, if it is ever finished): DM NOT FOUND.
- Also unknown: whether the link is the website (creedom.ai), an app-store link, or a referral / tracked link. Creedom
  app-store link: NOT FOUND.
- *Sources: notes_chat.md §I2 and §K; notes_creedom_files.md §1.1.*

### 2.2 Hosted links for the PDFs (HOOK, STUDY, PROMPT)

- The three Creators 100X PDFs exist only as files: `brands/creators-100x/pdf/creators100x_20-hooks-that-work.pdf` (HOOK),
  `creators100x_5-study-prompts.pdf` (STUDY), `creators100x_10-prompts-that-sound-like-you.pdf` (PROMPT, used by both the
  split-screen reel and the Riya reel).
- No hosting link. 2026-11-12 09:01:45 offer: "I can upload it to your Google Drive and give you a share link if you want.
  That would also complete the "HOOK" auto-DM text." No reply (NOT FOUND).
- Drive uploads from the session failed on size for other projects (10 MB and 4.2 MB connector limits); the PDFs are 6-10
  pages and may fit, size per file UNKNOWN here.
- Where the owner hosts automation resources (Drive, Notion, website, DM tool): UNKNOWN.

### 2.3 Auto-DM texts still to write

| Keyword | Reel | DM text status |
|---|---|---|
| CREE | Creedom explainer | never written (needs 2.1) |
| CHECK | Creedom CHECK | never written (needs 2.1) |
| SCRIPT | Creedom @write-script | written with `[CREEDOM LINK]` placeholder |
| HOOK | reel-flop | text NOT FOUND; resource is the 20 Hooks PDF (needs 2.2) |
| STUDY | STUDY manga | text NOT FOUND (caption.md only says the DM "sends ... the PDF"); needs 2.2 |
| PROMPT | prompt reel + Riya | written with `[PDF LINK]` placeholder |

Format rule (CLAUDE.md): "The keyword auto-DM (automation) is only the resource link and its setup steps, nothing else: no
greeting, buttons, comment replies, follow line or caveats. Hand it over as one plain block, or as a PDF when the person
asks for one."

---

## 3. Unconfirmed product facts and claims

### 3.1 How Cree learns "your voice" (@write-script)

- The posted reel and description say write-script "takes your measurements: how you open, where you pause, the words you
  can't stop saying" (and v1 said "It read my reels first"). The owner confirmed only the second assumption: that
  write-script returns a script with a hook, a story and a call to action ("yeah your 2nd assumption is correct",
  2026-11-17 11:13:55).
- Asked and not answered: 2026-11-17 11:43:19 ("the voiceover says "It read my reels first." That fits Creedom's "Use one
  of my Reels" option, but you only confirmed the second assumption ... not this one."), 12:54:30 (""it takes your
  measurements… how you open, where you pause" assumes Cree learns your voice from your reels. Tell me if it works
  differently"), 13:13:24 (repeated).
- caption.md note: "still assumes Cree learns your voice from your reels; the owner has confirmed only that write-script
  returns a hook, a story and a call to action."
- Risk: the v4 final, its description and the unused options B and C all depend on this claim. If it is wrong, the
  description and possibly the VO need changing before posting.
- Also unconfirmed (script_options.md "Facts to confirm"): "roughly how long it takes" to return a script.

### 3.2 Other Creedom features not understood yet

- Behaviour of "Send a DM to your comments", "Ideas tuned to your account", "Your saved reels, organized": UNKNOWN (only
  the card labels are known). Needed before any reel about them (see content-calendar.md §5.2).

### 3.3 Claims to verify before reuse

- "Creedom is an Official Meta Business Partner (Dec 2025): Indian Startup Times / Ascendants seed-round coverage"
  (`creedom-reel-analyser-9x16/script.md`, "Claims and sources"). Not checked in this session (creedom.ai loaded only once,
  for a style read). Verify before putting it on screen.
- Explainer claims come from the client's own script card ("free audit ... about 20 seconds ... score out of 100"): taken
  as client-approved; the on-screen 78/100 and fix line were invented examples.
- Paid partnership: the Reel Analyser notes say "If this is a paid partnership: use Creedom's approved CTA and add
  Instagram's paid-partnership label." Whether the Creedom reels are paid partnerships: UNKNOWN (see 9.1).

---

## 4. Previews, approvals and pending client changes

### 4.1 Previews awaiting approval

- None. Every latest preview was approved and rendered as a final: explainer v10, reel-flop v13, STUDY v1, CHECK v1
  (v6.1), prompt reel (v3 content), Riya v1, @write-script v4. *Source: notes_chat.md §J.*

### 4.2 Riya reel: changes promised by the owner

- 2026-11-15 14:05:30 OWNER: "I'll tell you to make changes later, before that give me the pdf and cover page for the
  creators 100x reel we made today". No changes sent since (NOT FOUND). Ask whether changes are still coming before it is
  posted.

### 4.3 Reel Analyser (October) left at drafts

- `creedom-reel-analyser-9x16`: drafts 1-6 (2026-10-24/25), no render folder, no final, no caption.md; its chat is not in
  this session. Decide: finish, drop, or keep as backlog. If finished: remove the emoji from its draft caption (no-emoji
  rule), write the description in the house format, and note that its numbers are @ai.nxtlvl stats.

### 4.4 Possible client feedback channel

- 2026-11-17 14:59:19 OWNER: "Good concept! Just a few suggestions: ..." reads like forwarded client or reviewer feedback.
  Whether the Creedom client reviews reels, and through whom: UNKNOWN (UNCERTAIN). If the client reviews, confirm whether
  they approved the v4 final.

---

## 5. Missing deliverables

### 5.1 Cover for the split-screen prompt reel

- `creators100x-prompt-9x16` has no cover PNG. 2026-11-15 14:05:46 ASSISTANT: "it doesn't have a cover yet" (offered to make
  one). No answer. Needed if that version is posted.

### 5.2 Missing caption.md files

- `creedom-explainer-9x16/` and `creedom-reel-analyser-9x16/` have no caption.md. The explainer's final description exists
  only in the chat (copied in content-calendar.md §4.2). nxtlvl-social-video §6: "Save it in the project's `caption.md`
  too."

### 5.3 Other gaps

- reel-flop: the v2, v3 and v10 MP4s and the explainer previews named in the chat are no longer on disk (only covers /
  later versions remain). Not a problem unless the owner wants them again.
- HOOK / STUDY / PROMPT DM blocks: see 2.3.

---

## 6. Technical fixes

### 6.1 True peak above the -4 dBTP check (-1.5 dBTP flag)

- The masters are made at -14 LUFS with a -1.5 dBTP (or -2 dBTP) ceiling, but the house checker
  (`~/.claude/skills/openverse-sfx/scripts/verify_mix.py`) wants the true peak below -4 dBTP ("headroom for AAC / phone
  speakers"). Every Creators 100X final logs "VERDICT: NEEDS FIX ... true peak ... above -4 - lower gains and re-run
  loudnorm with true_peak=-4":

| Final | Integrated | True peak | Verdict |
|---|---|---|---|
| `reel-flop-9x16/renders/nxtlvl_reel-flop_reels_9x16_v13.mp4` | -14.1 LUFS | -1.7 dBTP | NEEDS FIX |
| `study-manga-9x16/renders/creators100x_study-manga_reels_9x16_v1.mp4` | -14.0 | -1.5 | NEEDS FIX |
| `creedom-check-9x16/renders/creators100x_creedom-check_reels_9x16_v1.mp4` | -14.0 | -1.5 | NEEDS FIX |
| `creators100x-prompt-9x16/renders/creators100x_stop-write-me-a-script_reels_9x16_v1.mp4` | -14.0 | -1.8 | NEEDS FIX |
| `creators100x-prompt-story-9x16/renders/creators100x_riya-paper-story_reels_9x16_v1.mp4` | -14.1 | -1.7 | NEEDS FIX |
| `creedom-write-script-9x16/renders/creators100x_creedom-write-script_reels_9x16_v4.mp4` | -14.0 | -1.5 | NEEDS FIX |
| `creedom-explainer-9x16/renders/nxtlvl_creedom-explainer_reels_9x16_v10.mp4` | -16.0 | -4.4 | PASS |

- Offered twice, no answer: 2026-11-17 13:33:49 and 16:34:56 ("I can redo just the sound mix").
- Decision needed: either keep -14 LUFS / -1.5 dBTP as the Creators 100X standard (and note the checker's -4 dBTP rule
  does not apply), or remix with `loudnorm ... TP=-4` (sound only; the picture is copied, so no re-render). The verify
  script's default target is -16 LUFS; these reels pass `--target -14`.

### 6.2 Smaller technical notes

- The HyperFrames CLI reports "7 HyperFrames skills out of date or missing. Run: npx hyperframes skills update"
  (`creedom-write-script-9x16/renders/final.log`). CLAUDE.md says third-party skills are pinned in `skills-lock.json` and
  updated only with `npx skills add ...`; decide whether to update.
- The prompt reel final is named `_v1` but carries the v3 content (new hook): naming could confuse later versions.
- CLAUDE.md says caption timing should come from ElevenLabs Scribe because local models can't download; in practice
  faster-whisper ran offline from a cached model (`/root/tts/hf`). If the cache is lost, the Scribe route applies.

---

## 7. Repo, privacy and documentation housekeeping

### 7.1 brand.md PDF list is outdated

- `brands/creators-100x/brand.md` line 45: "Made so far: `pdf/creators100x_20-hooks-that-work.pdf` (the "HOOK" keyword
  resource for the reel-flop reel)." Two more PDFs exist: `creators100x_5-study-prompts.pdf` (STUDY) and
  `creators100x_10-prompts-that-sound-like-you.pdf` (PROMPT). Update when the repo may be edited (this export did not
  modify the repo).

### 7.2 Creators 100X logo and PDFs are public

- The repo is public. Tracked in git: `brands/creators-100x/logo-square.png`, `logo.png`, `logo-mark.png`, and the three
  PDFs and their JSONs. 2026-11-12 09:01:45 ASSISTANT: "the repo is public, so the logo and this PDF can be seen on GitHub
  ... tell me if the logo should stay private." No answer (NOT FOUND). Note that the PDFs are the lead magnets people get
  by commenting, so being public may undercut them.

### 7.3 Creedom mascot crops in git history

- 2026-11-10 11:12:51 ASSISTANT: "the pose images, and your mascot image and crops I had committed earlier, are now out of
  git. Earlier commits still contain the mascot crops, though. Let me know if you want them removed from the history too."
  No answer. The CHECK commit "Creedom CHECK reel: track the mascot images (our own art, needed to rebuild)"
  (2026-11-13) tracked the flat puppet images (UNCERTAIN whether these are still tracked).

### 7.4 Wording that predates the rules

- Reel Analyser draft caption contains an emoji (an eyes emoji) and puts the CTA second: fix before any use.

---

## 8. 3D work for Creedom

- Delivered 2026-11-14: the 3D storytelling guide (14 pages) and the Cree 3D model sheet (7 pages) + reference pack (ZIP).
  No owner feedback on either (NOT FOUND).
- Unknown: whether the 3D render was made in "Concept/NxtlvlSocial" (the owner's 3D workspace), which concept was chosen
  (A "The Buried Hook" was recommended), and who renders it.
- Unanswered offer (2026-11-14 08:12): "put `00_cree_original.png` through an image-to-3D tool ... I can also generate that
  first 3D model with Higgsfield's image-to-3D here; it uses Higgsfield credits". Higgsfield balance on 2026-11-10: 0
  credits, free plan. "There is no 3D mesh yet."
- If the 3D reel happens: its CTA in the guide is "Comment CREEDOM", which needs the same Creedom link (2.1) and a fresh
  music track (never reused).

---

## 9. Business unknowns: deal, stats, relationships

### 9.1 Creedom deal terms

| Question | Status |
|---|---|
| Is Creedom a paying client, a partner of Creators 100X, or the owner's own product? | UNKNOWN |
| Fee / retainer / payment terms | UNKNOWN |
| Reels per month, promo vs non-promo split | UNKNOWN |
| Deadlines, posting schedule | UNKNOWN |
| Approval process (who signs off for Creedom) | UNKNOWN (in practice the owner reviews; one possibly forwarded note, 4.4) |
| Client contacts (names, email, WhatsApp) | UNKNOWN |
| Paid-partnership label needed on Creators 100X posts? | UNKNOWN |
| Pricing / plans of Creedom (to mention or avoid) | UNKNOWN; only "free audit" is stated |

### 9.2 Creators 100X

| Question | Status |
|---|---|
| Who owns the page (the owner, the Creedom client, joint)? | UNKNOWN; the owner says "i will post these things" and the Creedom app is connected to @creators.100x (UNCERTAIN: the owner runs it) |
| Followers, reach, growth goals, KPIs | UNKNOWN |
| Who designed the logo | UNKNOWN |

### 9.3 Posting and results (both brands)

- Posting dates: UNKNOWN for every reel (none reported).
- Live post links: UNKNOWN.
- Performance (views, likes, saves, comments, keyword DMs sent): UNKNOWN. Worth asking, to steer the backlog.

---

## 10. Uncertain facts to confirm

| Fact | What the sources say | Source |
|---|---|---|
| Page of the hook reel (reel-flop) | Treated as Creators 100X from 2026-11-12, but files are `nxtlvl_` and the page answer on 2026-11-11 was "No brand" | notes_c100x.md §3.1 |
| Page of the Creedom explainer | `nxtlvl_` prefix; which NXTLVL page (NXTLVLSOCIAL.AI or AI.NXTLVL) not stated | notes_creedom_files.md §2.2 |
| Page of the Reel Analyser | AI.NXTLVL (end card "@AI.NXTLVL"), not confirmed | notes_chat.md §B0 |
| Official Creedom brand font | Google Sans (October reel, "the face of the Creedom wordmark") vs Fraunces / Manrope (read from creedom.ai) vs Inter (later titles) | notes_chat.md §A4 |
| ElevenLabs model of the owner's v4 take | File name says eleven_v4; our script told him v3 (tags only work on v3); the build notes call it "Eleven v3 voice" | notes_chat.md §E |
| ElevenLabs credits | 2026-11-12 19:01 the owner mentioned "not having credits" (about a GTA reel); current balance UNKNOWN | notes_chat.md §E |
| Handle "07rinx" | A handle to avoid in fake UI; probably the owner's own (UNCERTAIN) | notes_chat.md §G |
| Whether the `real-sfx` skill was used | Explainer's cue report looks like its output; later reels used `build/sfx_mix.py` | renders/mix_final_cue_report.md |
| Who sent "Good concept! Just a few suggestions" | Owner's message, phrased like forwarded feedback | notes_chat.md §B4 |
