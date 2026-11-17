# Cree, the Creedom mascot: knowledge export

Everything known about Cree: who he is, how he looks, how we generated and animate him, the rules, the files and every
reel he appears in. All times UTC. Owner quotes verbatim, typos included. "UNKNOWN" = not in the notes.

*Sources: scratchpad/notes_chat.md (sections C, H, L), scratchpad/notes_creedom_files.md (section 4), repo files under /home/user/Nxtlvl-Social (images viewed directly for this export).*

## Contents

1. [Identity: name, personality, voice](#1-identity-name-personality-voice)
2. [How he looks](#2-how-he-looks)
3. [The 13 signature poses](#3-the-13-signature-poses)
4. [How we make him (generation log, verbatim)](#4-how-we-make-him-generation-log-verbatim)
5. [How we animate him](#5-how-we-animate-him)
6. [Consistency rules, mistakes and rejected versions](#6-consistency-rules-mistakes-and-rejected-versions)
7. [Where his files live](#7-where-his-files-live)
8. [Every reel he appeared in, and his role](#8-every-reel-he-appeared-in-and-his-role)
9. [3D direction (guide and model sheet)](#9-3d-direction-guide-and-model-sheet)
10. [Images to upload](#10-images-to-upload)

---

## 1. Identity: name, personality, voice

- **Name:** Cree. The owner calls him "the cree mascot" (2026-11-10T10:48:41). The Creedom in-app AI assistant is also called Cree ("How can Cree help?"); our notes describe him as "Cree, Creedom's assistant". The explainer's CTA keyword was "CREE".
- **Owner:** he is Creedom's own mascot, supplied by the client: "this is the mascot of creedom, you can animate him to be very expressive and doing things ad per the script" (2026-11-10T10:26:02). Male ("him").
- **Species:** he looks like a small round pink chick/bird, but the owner's rule is: "Firstly that is not a bird so dont treat him like that" (2026-11-13T04:14:44). Our earlier notes, file names (bird.py, bird.png) and the image prompts all say "pink bird mascot"; that wording is wrong per the owner. Treat him as "the Creedom mascot".
- **Personality:** UNKNOWN as an official brief. As performed in our reels (our choice, approved in use): very expressive, curious, helpful, quick to celebrate; a guide and reactor. The owner asked for him to be "lively" and "very expressive".
- **Voice and catchphrases:** NONE. Cree never speaks in any reel. No lip sync has ever been done. The only "Cree lines" are text: the app's own lines ("Give me 20 seconds."; "I'm sending that reel through the feedback engine. It watches the whole video, so give it a few minutes."; "Pick one Reel and I'll break down what's working, what's costing you retention, and the first change to make.") and one chat bubble we wrote for the @write-script reel: "On it. First, I'll take your measurements: your openers, your pauses, your words." Speech/thought bubbles carry only symbols ("!", "?", "...", "!?", heart).
- **Role principle (3D guide):** "The creator is the hero; Cree is the guide who shows the way. Cree never takes the credit."

## 2. How he looks

### 2.1 Body and proportions
- One rounded egg / bean-shaped body: head and body are a single form, **no neck**, slightly wider at the bottom.
- **As wide as he is tall** (arms included), width : height = 1 : 1.
- Eye centres **31% down** from the top of the head; each eye about **23% of his width**; eye centres **36% of his width apart**.
- Widest point (arms included) **67% down**; feet / ground at 100%.
- Beak "Centred, just below the eye line, between the eyes".
- "Short rounded wing-arms at about two-thirds of his height; two stubby oval feet set slightly apart."
*(creedom-3d-story/cache/pack/01_proportions_front.png; model sheet page 3)*

### 2.2 Face
- Big round eyes high on the face: white with a pale-pink rim, large glossy black pupils, two white catchlights (one large upper right, one small lower left).
- Thin darker-pink brows above the eyes (3D guide wording; in the master render they read as a soft darker-pink crease above each eye).
- Small rounded yellow-orange beak between and just below the eyes, open in a smile, red inside, darker orange outline.

### 2.3 Wings / arms and feet
- Short rounded wing-arms, used like hands (point, wave, hold, carry). Never flapped.
- Two stubby rounded yellow-orange oval feet.

### 2.4 Surface and materials (model sheet page 4)
- Body: "Soft matte, velvety plush-toy surface with light subsurface scattering so the pink glows at the edges. No feathers, no fur strands."
- Eyes: "Glossy: clear coat over a black pupil with two white catchlights (one large upper right, one small lower left). Pale pink rim around the white."
- Beak and feet: "Semi-gloss, like smooth vinyl. Slightly warmer than the body light."
- Lighting test: "Warm key, soft fill, pink rim. He should read as a premium designer toy."

### 2.5 Colours (hex)
Model sheet palette (creedom-3d-story/build/model_sheet.cjs):

| Part | Hex |
|---|---|
| Body base | #F343A2 |
| Body shadow | #E0187E |
| Body highlight | #FF8CC6 |
| Beak and feet | #FFC21A |
| Beak and feet shadow | #F2A516 |
| Mouth inside | #D81F3C |
| Eye white and catchlights | #FFFFFF |
| Pupil | #0B0B0B |

Other measured values:
- Body pixel samples from cree.png: [246,100,171], [247,112,179], [243,72,144], [247,122,181].
- Pixel samples from logo_src.jpg: body #f442a0 / #f653a6; eye rim #efd5e0; feet #e89201 / #f19702 / shadow #c87002; mouth #8d0100.
- "Mascot pink" in the app palette: #F343A2.
- Blink lid colours per pose: see section 5.3.
- Guide rule: "Hot magenta-pink all over (base #F343A2, shading #E0187E, highlights #FF8CC6). Never another colour."

### 2.6 Outfit, accessories, logo on him
- Outfit: none. Rule: "Add clothes or accessories (props are fine)" is a DON'T.
- Logo on him: none.
- Props used: gold-rimmed magnifying glass with a dark/wooden handle (the "mag" pose; Creedom's "reading" pose); a white smartphone (the "phone" pose). In CHECK the magnifier was restyled as a premium glass magnifier (frosted lens, pink rim, highlight) on the old puppet.

### 2.7 The master image
The client's original (creedom-explainer-9x16/assets/img/mascot_src.png, 1080 x 1080, transparent): Cree in three-quarter view, waving with his left wing-arm (frame right) raised high, the other arm low and out, one foot planted and the other kicked up behind/right, beak open in a happy smile, eyes looking at the viewer. The same waving pose appears left of the wordmark in the Creedom logo. Note: the source PNG has a faint semi-transparent pinkish rectangular fringe around the figure (a cut-out artefact); the cleaned crop cree.png removes it.

## 3. The 13 signature poses

All in creedom-explainer-9x16/assets/img/poses/ (copies in creedom-check-9x16, creedom-write-script-9x16 and creedom-3d-story). Transparent PNG, each on one shared **820 x 820** canvas, feet on y 800. Model-sheet captions in brackets. Descriptions checked against the images.

| # | File | Model sheet name | Description |
|---|---|---|---|
| 1 | stand.png | Stand | Front view, both feet planted side by side, both arms relaxed down at his sides, calm friendly open-mouth smile, looking at the viewer. The neutral reference pose; sets the scale (600 px tall). |
| 2 | walk.png | Walk A | Three-quarter view walking to frame right, one foot kicked back behind him, one arm raised and swung, happy open smile. Left half of take walk_a. Scaled to 610 px. |
| 3 | pass.png | Walk B | Passing position of the walk, turned three-quarters right; one foot planted under the body, the other lifted and kicked forward; arms close to the body. Scaled to 610 px. |
| 4 | wave.png | Wave | Front view on both feet, one wing-arm raised high waving hello (like the master render), other arm at his side, big excited smile. |
| 5 | point.png | Point | Body turned slightly to frame right, one arm stretched straight out pointing to frame right, other hand on his belly, eyes looking where he points, excited smile. |
| 6 | present.png | Present | Facing camera, one arm swept out to frame left palm-up like a host saying "ta-da", other arm raised slightly, warm welcoming smile. |
| 7 | cheer.png | Cheer | Jumping for joy: both arms thrown up, eyes squeezed shut in happy "^ ^" arcs, beak wide open laughing, one foot kicked up. |
| 8 | shock.png | Shock | Both hands pressed on his cheeks, eyes huge with tiny pupils, beak dropped open in a round "O". |
| 9 | sad.png | Sad | Slightly slumped, droopy half-lidded eyes looking down, small downturned frowning beak (closed), arms hanging. |
| 10 | mag.png | Magnifier | Body turned to frame left, holding a large gold-rimmed magnifying glass with a dark handle up to his eye (eye enlarged behind the lens), other hand on belly, curious focused look. |
| 11 | phone.png | Phone | Facing camera, holding a small white smartphone in front of his belly with both hands, typing, happy concentrated smile (back of phone faces viewer). |
| 12 | think.png | Think | One hand raised to the bottom of his beak like a hand on a chin, other arm folded across his belly, eyes glancing up and to the side, closed thoughtful smirk. |
| 13 | proud.png | Proud | Chest out, both hands on hips, smug happily narrowed eyes, big satisfied grin. |

Cut sizes before placing on the canvas (2026-11-10T11:02:38): cheer 643x566, mag 559x569, pass 706x680, phone 491x592, point 638x573, present 744x598, proud 577x565, sad 513x558, shock 494x579, stand 614x600, think 492x574, walk 729x665, wave 656x615.

## 4. How we make him (generation log, verbatim)

Tool: **ElevenLabs image edit (model gpt-image-2.5-sunburst)** in the owner's ElevenLabs flow, using the owner's own mascot image as the reference node. The section below is copied verbatim from the chat notes (section H).

### H1. Failed and rejected attempts (2026-11-10)
- v2 preview (before 10:47): one image of Cree moved around in a single pose. OWNER 10:48:41: "he is in a single pose change that".
- ~10:49-10:51 a vector SVG redraw (build/cree_rig.py). 2026-11-10T10:49:49 ASSISTANT: "Now drawing the rigged Cree. I'll prototype him standalone and compare him to the original mascot before wiring him into the reel." 10:51:30: "Very close to the original. Small tweaks next (bigger pupils, bigger mouth), then I'll wire the rig in with a walk cycle, waving, pointing, cheering, typing and changing expressions." OWNER 10:52:00: "No you are changing the art style of it make him exactly like that i sent". [summary]: "build/cree_rig.py: the vector SVG Cree rig. The user rejected it ("changing the art style"); do not use it."
- 10:53:17 a cut-out puppet (build/puppet.py), never shown to the owner: "cuts cree.png into body, arms, feet and pupils with ellipse fitting and diffusion inpainting. The result had visible seams (body clipped, dark smears); poor quality, not used." Layer metadata: {"size": [645, 649], "armL": [59, 452, ...], "armR": [582, 159, ...], "footL": [230, 605, ...], "footR": [533, 512, ...], "pupilL": [231, 222, ...], "pupilR": [419, 178, ...]}.

### H2. The approved method: ElevenLabs image edit from the owner's image
1. 10:54:35 [tool]: the mascot was flattened onto white: cache/cree_ref_white.png, 367,603 bytes.
2. 10:56:24 [tool] mcp__Adobe__asset_initialize_file_upload {"path": "nxtlvl-creedom/cree_ref_white.png", "file_size": 367603, "media_type": "image/png"}. A curl PUT returned 200. 10:56:45 finalize returned "assetId":"[asset id removed]", "presignedAssetUrl":"[link removed]". Reason, from the [summary]: "The ElevenLabs asset-upload tools are not available, so files go through an Adobe upload".
3. 10:56:48 [tool] mcp__ElevenLabs__creative_attach_reference_file {"url": "[link removed]", "flow_id": "[flow id removed]", "name": "cree_ref.png"}. Result: {"asset_id":"[asset id removed]", ..., "node_id":"[node id removed]"}. -> (ElevenLabs flow [flow id removed] is the same flow that made the Hallie VO. Reference node: [node id removed].)
4. Price checks (estimate_only, 2 generations each, 10:57:06-10:57:15):
   - gemini-3-pro-image: 4105 credits ($0.67).
   - gpt-image-2.5-sunburst: 972 credits ($0.159).
   - gemini-3.1-flash-image: 1368 credits ($0.22).
   - Choice: gpt-image-2.5-sunburst. 10:57:19 ASSISTANT: "Sunburst costs about 490 credits per image, so 10 poses with 2 takes each comes to roughly 5k credits. I'll test one pose before running the rest."
5. Every generation: model "gpt-image-2.5-sunburst", "generations_count": 2, "connect_from": ["[node id removed]"], output 1280x720, 486 credits per image. No seed was given. Aspect: the default 1280x720.
6. Shared prompt prefix, verbatim: "Use the reference image as the exact character: the same pink 3D bird mascot, with the same egg-shaped glossy pink body, the same soft 3D render, the same big black eyes with white highlights and pale pink rims, the same small yellow beak with a red open mouth, the same small rounded pink wings and the same orange oval feet. Keep its proportions, colours, materials and lighting identical; do not redesign or stylise it." (For sad and think it reads "the same small yellow beak," without "with a red open mouth".) Shared suffix: "Full body, centred, with empty space around it, on a plain pure white background, with no shadow, no text and no other objects."
7. Pose-specific prompt text, verbatim:
   - stand (10:57:24, test): "Change only the pose: the character stands upright facing the camera, balanced on both orange feet side by side, both wings relaxed down at its sides, with a calm friendly smile and the mouth slightly open." Sessions UrD2qw4527M3bHqXsXXS and bsoAikJCn4HwkMbkImfm (gens yvOIR8wB3YG8eYU0L3mu, RIjGNU5WliXi0jW86aZ9).
   - walk (10:58:36): "Show the character twice, side by side, at the same size and the same height, as two frames of a cheerful walk cycle. In both it walks towards the right of the image, body turned three-quarters to the right, eyes looking ahead with a happy open-mouth smile. Left copy: its front foot steps forward, its back foot lifts behind, the front wing swings back and the back wing swings forward. Right copy: the opposite step, with the other foot forward and the wings swapped. Full bodies with clear space between and around them, on a plain pure white background, with no shadow, no text and no other objects." (gens mTMLSnYCupJbx0ya3NMV, 4N0A0FcB20IinIspBgdf)
   - wave (10:58:40): "Change only the pose: the character stands upright facing the camera on both feet and waves hello enthusiastically, with one wing raised high above its head and the other wing relaxed at its side, a big excited open-mouth smile and slightly raised happy eyes." (IkOflzfHlUPvhb8bxfh1, IBzZ1laoOiAAZFXaaZzx)
   - point (10:58:44): "Change only the pose: the character stands on both feet with its body turned slightly to the right of the image and points energetically to the right of the image, with one wing stretched straight out towards the right like an arm pointing at something. The other wing rests on its belly. Its eyes look towards where it points, with an excited open-mouth smile." (yAipsyRHWL0QcHYMpUPu, VxZxoO54Ehy16y0WoQTa)
   - cheer (10:58:47): "Change only the pose and expression: the character jumps for joy, with both wings thrown up high above its head in celebration, both feet off the ground and tucked slightly, eyes squeezed shut in happy upside-down U shapes, and its beak wide open in a big laugh." (SIiIc7BfuYiZerkkaXAX, BJpdWz0OfGzMS1Q7qKxz)
   - shock (10:58:51): "Change only the pose and expression: the character is shocked and startled, standing on both feet and leaning back slightly, with both wings pressed against its cheeks, its eyes extra wide with small pupils, and its beak dropped open in a round O of surprise." (OgDlZhAenzJ9pignKwsF, pQNc2VtkttH8RhDYZWbk)
   - sad (10:58:55): "Change only the pose and expression: the character is sad and disappointed, standing on both feet slightly slumped forward, with both wings hanging limply down, its eyes droopy and half-closed looking down, and its beak closed in a small downturned frown." (WlqOUebbe5N8KBEqfEa0, aSwHWznvWId1VozHaBsw)
   - mag (10:58:59): "Change only the pose: the character stands on both feet, body turned slightly to the left of the image, and holds a large round magnifying glass with a gold rim and a dark handle in one wing, raised beside its face towards the left of the image as if inspecting something closely, with the other wing on its belly. Curious, focused expression with the beak slightly open." (ktMKNYqL1aTxj9ipMZvi, wlhNcALffELJWvKIbYWD)
   - phone (10:59:03): "Change only the pose: the character stands on both feet facing the camera and holds a small white smartphone in front of its belly with both wings, typing on it with the tip of one wing, eyes looking down at the screen, with a happy concentrated smile. The phone screen faces the character, so its back faces the viewer." (PKWZwDGsSc6SFqdz6IhH, tZJxoQryl7NWGUSriVS8)
   - think (10:59:07): "Change only the pose and expression: the character stands on both feet thinking hard, with one wing raised to touch the bottom of its beak like a hand on a chin, the other wing folded across its belly, eyes looking up and to the side, and its beak closed in a thoughtful little smirk." (Wg4s9wUfgAYlrgCZTqsj, r0QwCRDywGDi9XXCskS7)
   - proud (10:59:11): "Change only the pose and expression: the character stands proud and confident on both feet with its chest puffed out, both wings resting on its hips, chin raised slightly, and a big satisfied grin with its eyes happily narrowed." (YNrF7RJrjeDp1Knp6X7o, UVyxIM33d3IhsW3lpxwW)
   - present (10:59:16): "Change only the pose: the character stands on both feet facing the camera and presents something with a flourish, holding one wing out to the left of the image, palm up like a host saying "ta-da", with the other wing raised slightly. Warm, welcoming open-mouth smile, looking at the viewer." (gens pE4yIqGTwzGzGoEyQj3j, o4cBocz9LkmafShnYclX)
   - pass (11:00:31, added because "The two walk frames are almost identical"): "Change only the pose: the character is mid-walk towards the right of the image, with its body turned three-quarters to the right, caught in the passing position of a walk cycle. One orange foot is planted flat directly under the body, and the other foot is lifted high, tucked up under the belly as it swings forward. Both wings are held close to the body, slightly out for balance. Happy open-mouth smile, eyes looking ahead to the right." (bvDYk5hU3S2yxCtFaWTv, eAz3sVAGSIHNvvPiVhEg)
8. Picks (11:02:06 [tool], verbatim): picks={'stand':'stand_a','wave':'wave_a','point':'point_a','cheer':'cheer_a','shock':'shock_a','sad':'sad_a','mag':'mag_b','phone':'phone_a','think':'think_a','proud':'proud_a','present':'present_a','pass':'pass_a'}; walk = left half of walk_a ("w.crop((0,0,640,720))"). The raw takes were saved to cache/poses/gen/*_a.png / *_b.png, the picks to cache/poses/raw/<pose>.png, and build/poses.py turned them into assets/img/poses/<pose>.png plus plan/poses.json.
9. Cut-out and normalising (build/poses.py): background removed, one shared scale set by the standing pose ("BODY_H = 600", canvas "POSE_W, POSE_H = 820, 820", "BASE = 800" feet baseline); walk and pass scaled to height 610 ("FIT_H = {"walk": 610, "pass": 610}"); eye detection for blinks; "NOBLINK = {"cheer", "proud", "shock"}". Cut sizes (11:02:38): cheer 643x566, mag 559x569, pass 706x680, phone 491x592, point 638x573, present 744x598, proud 577x565, sad 513x558, shock 494x579, stand 614x600, think 492x574, walk 729x665, wave 656x615.
10. Cost: 2026-11-10T11:12:51 ASSISTANT: "They cost about 12,600 ElevenLabs credits (around $2), including spare takes I didn't use."
11. Owner reaction: no direct message about the 13 poses on 11-10. He then gave layout and pacing notes, not mascot notes. On 2026-11-13 he called this version the good one: "look how full he looks in the previous video make him like that" (05:32:39) and "he is not in the same quality as previous reel on creedom" (04:26:48).
12. Git: 2026-11-10T11:12:51 ASSISTANT: "the pose images, and your mascot image and crops I had committed earlier, are now out of git. Earlier commits still contain the mascot crops, though." [summary]: "Keep MP4s and media out of git; the repo is PUBLIC. That covers ... client mascot/logo images (cree.png, poses, wordmark.png)".

### H3. Reuse in later reels
- CHECK v1-v4 (2026-11-13) copied the flat puppet rig from creedom-reel-analyser-9x16 (bird.py / bird_clean.py), restyled with a glass magnifier. The owner rejected it three times. v5 (05:34:22 ASSISTANT): "Now I'll swap the mascot rig for the 3D poses and remove the second "Creedom"."
- 3D pack (2026-11-14T08:12): "`00_cree_original.png`: the master reference. `01_proportions_front.png`: the measured front view. `poses/`: the 13 transparent poses, plus a file of eye positions and sizes for each pose. `rig_layers/`: the old cut-out puppet layers (body, wings, beak, feet). `brand/`: the Cree icon and the Creedom wordmark. Both PDFs ... A README". Suggested next step: "put `00_cree_original.png` through an image-to-3D tool ... I can also generate that first 3D model with Higgsfield's image-to-3D here; it uses Higgsfield credits". Not taken up: NOT FOUND. (Higgsfield balance was 0 credits on 2026-11-10T10:28:29: {"credits":0,"subscription_plan_type":"free"}.)
- @write-script v1 and v3/v4 reused the explainer poses ("mag, phone, point, cheer, pass" listed in script_options.md).
- No other image generations of Cree (Canva, Higgsfield, generate_image) were found in the Creedom windows. The Canva generate-image calls in the session were on 2026-10-31 and 2026-11-01, for other projects. STUDY reel images: Canva create-design, 2026-11-12/13.

### 4.1 Notes on the generation log
- The prompts say "pink 3D bird mascot" and "wings". They worked for likeness, but the owner later said he is "not a bird". For new generations, keep the likeness wording but describe the wings as "short rounded wing-arms used like hands" and never ask for flapping or flying (uncertain whether changing "bird" in the prompt changes the output; never tested).
- Seeds: none used. Reference image: the owner's mascot flattened on white (cache/cree_ref_white.png; the cache folder no longer exists in the repo, so recreate it from mascot_src.png on white).
- Style keywords that worked: "same egg-shaped glossy pink body", "same soft 3D render", "big black eyes with white highlights and pale pink rims", "small yellow beak with a red open mouth", "small rounded pink wings", "orange oval feet", "Keep its proportions, colours, materials and lighting identical; do not redesign or stylise it", "Change only the pose", "on a plain pure white background, with no shadow, no text and no other objects".
- Settings: 2 generations per pose, default 1280 x 720 output, pick the best take, cut out, normalise to the shared canvas.
- Cost: about 486 credits per image; about 12,600 ElevenLabs credits (around $2) for all poses including spare takes.
- Raw takes (cache/poses/gen, cache/poses/raw) and the rejected build scripts (build/cree_rig.py, build/puppet.py) are no longer in the repo (checked 2026-11-17).

### 4.2 The older flat cut-out puppet (reel analyser, October; CHECK v2-v4)
- Built from the waving image cut into layers: bird.png (604 x 640) split into body (bird_core), two wings (bird_wing, bird_wingl), beak (bird_beak), feet (bird_foot, bird_foot_up); bird_clean.py rebuilt the lower body and made "both feet ... from the one foot the original art shows in full".
- SVG face rig: movable pupils, upper/lower lids, "^ ^" arcs, eyebrows, blushing cheeks, beak open/wide/closed ("chatters"), heart eyes (#ff3b6b), star eyes (#FFC531), tear. Expressions: neutral, smile, joy, excited, love, confused, hopeful, sad, shock, skeptical, annoyed, focused, curious, proud, wink. Postures: neutral, tall, slouch, leanin, leanback, crouch ("scale stays within about 3%": "the art is a 3D render and big squash reads as distortion"). Colours PINK #E2557D, lid colours L #f45ca3 / #ee4a99, R #f467ae / #f055a6.
- Status: **rejected** for Creedom reels from 2026-11-13 ("look how full he looks in the previous video make him like that"). Kept only as reference layers in the 3D pack.

## 5. How we animate him

Method used in the approved version (explainer, CHECK v5+, @write-script v1/v3/v4): **2D pose swaps** of the 13 cut-out 3D renders on a fixed 820 x 820 canvas, plus drawn overlays. There is no 3D mesh and no skeletal rig.

### 5.1 Core moves (from code)
- **Pose swap:** set opacity per pose plus a small squash (scaleX 1.07, scaleY 0.9 -> 1, 0.28 s, back.out(3)) so each change "pops". Flip left/right via a wrapper (#creef) scaleX -1.
- **Walk cycle:** walk and pass frames alternate every about 0.15 s, with a bob (y -22) and a rock of plus/minus 4 degrees, facing the way he goes.
- **Hop (cree_hop):** squash (scaleY 0.86, scaleX 1.1, y 10) -> stretch (scaleY 1.08, scaleX 0.94, y -h) -> fall -> land squash (scaleY 0.92, scaleX 1.06) -> settle. CHECK adds a shadow that shrinks while he is in the air.
- **Wiggle:** rotation plus/minus a small amplitude.
- **Idle:** bob y -10 over 0.8 s and breathing scaleY 1.015 (CHECK).
- **Shadow:** soft pink drop shadow rgba(200,40,120,.22); in CHECK rgba(226,53,160,.35).
- **Scale on screen (CHECK):** CS 0.52, so the 600 px pose shows about 312 px tall.

### 5.2 Overlays
- **Blinks:** a shaded lid ellipse (gradient of the two lid colours for that eye) plus a lash line #2a0c22, stroke 9, shown for 0.11 s, only on open-eyed poses. Explainer blink times: 6.9, 8.0, 12.95, 15.2, 20.4, 23.4, 26.0, 30.8, 33.0 s.
- **No-blink poses:** cheer, proud, shock (chat notes, build/poses.py) and also pass in the reel code ("eyes closed, narrowed or tiny; pass: a 3/4 eye overlaps the beak").
- **Sweat drop:** blue drop #7fd3ff with stroke #3aa6e6 sliding down.
- **Bubbles:** "!", "?", "...", "!?", heart. Explainer: white bubble with text #c40db8. CHECK: frosted-glass bubble with magenta-to-pink gradient text.
- **Sparkles:** four-point stars (#EE688B and #f2b134 in CHECK; #F515E8, #F5876C, #FFC83D, #ffffff in the explainer).
- **Star and heart eyes, confetti:** used in the explainer and the old puppet.

### 5.3 Eye and box data for each pose (plan/poses.json)
Format: box [x, y, w, h]; each eye [cx, cy, rx, ry, lid top colour, lid bottom colour].
- cheer box [88,234,643,566], no eyes.
- mag box [130,231,559,569], eye [508,422,66,66,#fb6db1,#f953a2].
- pass box [93,190,633,610], none.
- phone box [164,208,491,592], eyes [310,400,65,62,#fd54a3,#fd559d] [512,391,62,62,#fd62ae,#fc52a2].
- point box [91,227,638,573], eyes [264,408,66,64,#fc6bb3,#fa5aa9] [444,361,50,58,#fa6eb5,#f95fae].
- present box [38,202,744,598], eyes [344,394,69,68,#fb5ea9,#fa569f] [553,368,67,66,#fb6ab0,#f856a6].
- proud box [121,235,577,565], none.
- sad box [153,242,513,558], eyes [266,494,55,46,#f45da9,#f24995] [469,478,66,40,#f665af,#f44aa0].
- shock box [163,221,494,579], none.
- stand box [103,200,614,600], eyes [303,386,72,70,#fe61ae,#fd53a2] [526,382,71,70,#fd6ab5,#fc55ab].
- think box [164,226,492,574], eyes [310,414,68,63,#f85fa6,#f7569f] [506,365,62,62,#f866ab,#f754a2].
- walk box [75,190,669,610], eyes [346,378,72,68,#fc6db3,#f953a2] [538,340,58,64,#fa68b0,#f855a6].
- wave box [82,185,656,615], eyes [287,382,71,70,#fa5fa8,#f855a0] [500,344,70,67,#f96db0,#f658a7].
Body centre on the canvas: (410, 500).

### 5.4 Movements and gestures in use
Walk in / walk across, wave hello and goodbye, point at UI or text, present ("ta-da") the app, cheer and hop (single, double, triple hops), shock with sweat and "!", sad with "...", think with "?", magnifier scan of a reel or card, typing on his phone, proud stance after a win, kicks, shrugs and head scratches (old puppet only).

### 5.5 Lip sync
None. He does not speak in any reel.

### 5.6 Entrances and exits
- Pops up into frame (explainer hook: "pops up waving"; shock pop with sweat and "!").
- Walks or strolls in from the side ("strolls in from the left under "FREE"").
- Hops in place on beats; jumps under the logo.
- Exits: waves goodbye (CHECK end); end card shows him as a static icon beside the wordmark (explainer).
- 3D concept: pops out of the phone screen "like a jack-in-the-box, lands with a squash".

## 6. Consistency rules, mistakes and rejected versions

### 6.1 Owner rules, verbatim
- 2026-11-10T10:26:02: "this is the mascot of creedom, you can animate him to be very expressive and doing things ad per the script"
- 2026-11-10T10:48:41: "What i meant was make the cree mascot lively make him walk or change his posture or pose he is in a single pose change that, make him stand on two legs aur move his hands and all and make his face expressive"
- 2026-11-10T10:52:00: "No you are changing the art style of it make him exactly like that i sent"
- 2026-11-13T04:03:50: "why didnt you use the creedom mascot that we made for this, use him"
- 2026-11-13T04:14:44: "Firstly that is not a bird so dont treat him like that and secondly his animations look very bad the last time you made him it was better so fix that"
- 2026-11-13T04:26:48: "the creedom mascor still looks bad he is not in the same quality as previous reel on creedom"
- 2026-11-13T05:32:39: "when i say the mascot looks bad then it is bad , look how full he looks in the previous video make him like that"
- 2026-11-14T04:28:46: "how the creedom mascot should look" (asked for in the 3D guide)
- 2026-11-14T08:08:32: "give me all the images or how you made that mascot to be, fully animated in 3D"
- 2026-11-17T12:24:23 (indirect): v1 of @write-script looked like "part 2" of CHECK partly because of the same mascot.
- 2026-11-17T13:00:13: "add a mascot, like add a person, okay, and use the Creedum mascot time to time"

### 6.2 What must never change
- The art style of the client's image: same pink, same egg shape with no neck, same eye style (big glossy black pupils, white catchlights, pale-pink rim), same yellow-orange beak and feet, same plush matte 3D look. Pack README: "Rules: same pink, same eye style, no neck, arms used as hands, he never flaps or flies."
- He is never treated as a bird: no wing flapping, no flying, no bird waddle or spins; arms used as arms.
- Always use the 13 3D poses (or new poses generated the same way from the original image), never the flat puppet and never a vector redraw.
- He looks "full": judge quality at full render quality (draft renders made him look soft).
- No clothes or accessories (props are fine). No logo on him.
- He never takes the creator's win; sad is one beat only.
- He never covers text and stays in his own space in the layout (CHECK alignment fix; @write-script v1 "used for reactions only and never covering text").

### 6.3 3D guide DO / DON'T (verbatim)
- DO: "Bouncy, squash-and-stretch hops", "A little waddle when he walks", "Use the wings as hands: point, wave, hold, carry", "Big readable expressions: curious, shocked, proud", "Keep him small next to people, heroic in the reel world".
- DON'T: "Flap the wings or fly: he isn't treated as a bird", "Change his colour, proportions or eye style", "Add clothes or accessories (props are fine)", "Make him look sad for long; the dip is one beat", "Let him take the creator's win".
- Model sheet: "Check every shot against the original image: colour, eye size and the no-neck egg shape are the parts people recognise."
- Note: the 3D guide's "a little waddle" sits alongside the owner's "not a bird" rule; the 3D guide explicitly bans flapping and flying. (uncertain: whether the owner accepts a waddle; no feedback on the guide.)

### 6.4 Versions that went wrong and why
| Version | Date | What happened | Owner verdict |
|---|---|---|---|
| Single static image moved around | 2026-11-10 (explainer v2 preview) | one pose only | "he is in a single pose change that" |
| Vector SVG redraw (build/cree_rig.py) | 2026-11-10 10:49-10:51 | redrawn as vectors to rig | "No you are changing the art style of it make him exactly like that i sent" |
| Cut-out puppet with inpainting (build/puppet.py) | 2026-11-10 10:53 | visible seams, clipped body, dark smears | never shown; dropped by us |
| Flat cut-out "bird" puppet from the reel analyser | 2026-11-13 CHECK v2-v4 | flapping/bird behaviour, then calmer face-led version, then reel-analyser-style performance | "that is not a bird", "his animations look very bad", "not in the same quality as previous reel", "look how full he looks in the previous video" |
| No mascot | CHECK v1 (lens orb), @write-script v2 | mascot left out | "why didnt you use the creedom mascot that we made for this, use him"; "use the Creedum mascot time to time" |
| 13 3D poses | explainer (2026-11-10), CHECK v5+, @write-script v1/v3/v4 | approved | "look how full he looks in the previous video make him like that" |

Assistant admission (2026-11-13T05:42:22): "I had been using the flat cut-out version from the older reel-analyser reel. That was the wrong mascot, and you were right."

## 7. Where his files live

*Repo root /home/user/Nxtlvl-Social. Client mascot images are kept out of git (the repo is public); older commits still contain the mascot crops.*

| What | Path | Notes |
|---|---|---|
| Owner's original upload (explainer) | /root/.claude/uploads/b1c6bbee-7bc1-59ac-ac25-7b3da31f270a/91192a5a-image.png | 1080 x 1080 RGBA, transparent |
| Original, copied | creedom-explainer-9x16/assets/img/mascot_src.png; creedom-3d-story/assets/img/mascot_src.png | same image |
| Master reference (3D pack) | creedom-3d-story/cache/pack/00_cree_original.png | 1080 x 1080 RGBA |
| Clean crop / icon | creedom-explainer-9x16/assets/img/cree.png; creedom-3d-story/cache/pack/brand/cree_icon.png | 645 x 649 RGBA, crop of bbox 233,222 to 858,851 |
| Proportions sheet | creedom-3d-story/cache/pack/01_proportions_front.png | 1280 x 900 RGB |
| 13 poses (master set) | creedom-explainer-9x16/assets/img/poses/{stand,walk,pass,wave,point,present,cheer,shock,sad,mag,phone,think,proud}.png | 820 x 820 RGBA, transparent |
| Pose copies | creedom-check-9x16/assets/img/poses/; creedom-write-script-9x16/assets/img/poses/; creedom-3d-story/assets/img/poses/; creedom-3d-story/cache/pack/poses/ | same 13 files |
| Pose data | creedom-explainer-9x16/plan/poses.json (copies in check, write-script); creedom-3d-story/cache/pack/poses/poses_eyes_and_boxes.json | boxes + eye ellipses + lid colours |
| Pose build script | creedom-explainer-9x16/build/poses.py | cut-out and normalising |
| Old puppet layers | creedom-reel-analyser-9x16/assets/img/bird*.png (bird, bird_beak, bird_body, bird_core, bird_core_v4, bird_foot, bird_foot_up, bird_footr_up, bird_wing, bird_wingl); creedom-check-9x16/assets/img/bird*.png; creedom-3d-story/cache/pack/rig_layers/ | rejected style |
| Old puppet code | creedom-reel-analyser-9x16/build/bird.py, bird_clean.py; creedom-check-9x16/build/bird.py | rejected |
| Logo with Cree | /root/.claude/uploads/b1c6bbee-7bc1-59ac-ac25-7b3da31f270a/2077e237-image.jpg = creedom-explainer-9x16/assets/img/logo_src.jpg | 1920 x 1080 |
| Wordmark | creedom-explainer-9x16/assets/img/wordmark.png; creedom-3d-story/cache/pack/brand/creedom_wordmark.png | 1426 x 269 RGBA |
| Reel-analyser source image | d146181c-image.png (waving pose, transparent) | NOT FOUND in this session's uploads |
| White-flattened reference | cache/cree_ref_white.png (explainer) | no longer in the repo; Adobe asset [asset id removed] |
| Generation workspace | ElevenLabs flow [link removed], reference node [node id removed] | owner's workspace |
| 3D documents | creedom-3d-story/renders/creedom_3d-storytelling-guide.pdf (14 pages), creedom_cree-3d-model-sheet.pdf (7 pages), creedom_cree-3d-reference-pack.zip (32 files, 15.0 MB) | |
| Source files (PSD, AI, 3D mesh) | UNKNOWN / none: "There is no 3D mesh yet." | |
| Google Drive links | UNKNOWN (none exist for Creedom) | |

## 8. Every reel he appeared in, and his role

1. **Creedom Reel Analyser** (creedom-reel-analyser-9x16, October 2026; page likely @ai.nxtlvl, uncertain). Role: lead character. Flat cut-out puppet: "The mascot (the pink bird) is the lead"; "It moves through the whole video like the reference characters do: it's never a static sticker." Performance: walks in curious, sees the counter, "explodes on 85x"; confused, scratches head; deflates with tear and rain cloud; shrugs; takes the magnifier and scans ("Creedom's own 'reading' pose"); heart eyes on 82; surfs the playhead; finds 0:34 with star eyes; CTA points, chatters, winks; waves goodbye. Draft 6: "calmer bird". Owner feedback: UNKNOWN.
2. **Creedom explainer** (2026-11-10/11, final v10). Role: reactor and guide acting out the script. First use of the 13 poses. Assistant, 2026-11-10T11:12:51, verbatim: "Hook: pops up waving, thinks on "the exact second", points at the retention graph, then is shocked at "stopped watching". Upload: walks over and goes sad on "flopped", presents on "Creedom's Reel Analyzer", then holds the magnifier up while it watches "second by second". Analysis: cheers on "hook worked", thinks, goes sad and sweaty on "energy dropped", shocked on "swiped away". Fixes: walks across, cheers with confetti on "new hooks", stands proud, points at the fix list. Free audit: strolls in from the left under "FREE", waves, types the handle on his phone, thinks while the timer counts down, cheers at the score, points at "first thing to fix". CTA: waves big, types "CREE" on his own phone, points at the paper plane, cheers with a heart on "link"." End card: Cree icon beside the wordmark. Cover: Cree in the "mag" pose holding the magnifier right on the retention drop. **This is the version the owner holds up as the standard.**
3. **CHECK** (2026-11-13, Creators 100X). Role: the checker. v1 none (lens orb); v2-v4 flat puppet (rejected); v5+ the 13 poses. Assistant, 2026-11-13T05:42:22, verbatim: "Hook: walks in, studies the phone through his magnifier, cheers and jumps at "post", points at the phone. Views vs reasons: thinks at "views after" (with a "?"), looks sad at "numbers", cheers and jumps twice at "Reasons, before". Creedom intro: waves and jumps under the logo, then walks over and scans the reel with his magnifier. Score and flags: thinks while the score counts up and cheers when it lands. He thinks at "weak hook" and points at "claim". At "loses trust" he does the shock pose with a sweat drop and a "!", then looks sad. Fix card: reads it with his magnifier, then a proud jump. Fixed reel: points at the phone, then cheers when Share turns into "Post it". End: cheers at CHECK, types the comment on his phone, waves goodbye." Cover: Cree cheering.
4. **3D storytelling guide** (2026-11-14). Role: the guide. Concept A "The Buried Hook": he "jumps inside the reel, walks its timeline with his magnifier, finds her best moment buried at 0:34 and carries it to the front."
5. **@write-script** (2026-11-17, Creators 100X). v1: "used for reactions only and never covering text"; sweats beside the empty note, shocked at the stamp, peeks in with the magnifier, points at the comment. v2: no Cree. v3/v4: "Cree is the tailor who hands the scripts over in the hook and gets a fright when none fit. He shows up again for these moments: typing on his phone under the app / reading with his magnifier during the measurements / cheering beside the mirror at "sounds like me" / waving and pointing at the comment box at the end. He sits out the rails, waveform and stitching scenes." Chat avatar uses the wave pose. Cover: Cree sad with a sweat drop beside the "DIDN'T WORK" stamp.

**What worked best:** the 13 3D poses with frequent pose changes on script beats, walks between scenes, squash-and-stretch hops, blinks, sweat and glass "?"/"!" bubbles (explainer; CHECK v5+ "Now in terms of detailing everything is on point"). Using him "time to time" in key moments rather than in every scene (@write-script v3/v4, approved with "Render in final").

## 9. 3D direction (guide and model sheet)

*creedom-3d-story/build/guide.cjs and model_sheet.cjs. No owner feedback on these yet.*

### 9.1 What exists today (model sheet page 2)
1. Original waving 3D-style render (00_cree_original.png, master reference).
2. 13 poses generated from it as 2D renders, cut out.
3. "In the reels he is animated in 2D: pose swaps on the script beats, squash and stretch, a 2-frame walk cycle, blinks and a sweat drop drawn on top."
4. "An older cut-out puppet splits him into layers: body, wings, beak and feet (rig_layers/), with the face redrawn so he can emote."

### 9.2 Character sheet (guide page 9, verbatim)
- Shape: "One soft egg-shaped body: head and body are a single form, no neck. Slightly wider at the bottom."
- Colour: "Hot magenta-pink all over (base #F343A2, shading #E0187E, highlights #FF8CC6). Never another colour."
- Eyes: "Big, round, glossy: white with a large black pupil and two white catchlights. Thin darker-pink brows above."
- Beak: "Small, rounded, yellow-orange (#FFC21A to #F2A516). Open in a smile, red inside."
- Wings and feet: "Short rounded wing-arms used like hands. Stubby yellow-orange feet."
- Surface: "Soft matte, velvety plush-toy feel with gentle subsurface glow. No visible feathers."

### 9.3 Build and rig (model sheet page 6)
- Block out "one sphere scaled to an egg (slightly heavier at the bottom), two eye spheres set into the face, a rounded cone for the beak, flattened capsules for the arms, two ovals for the feet"; sculpt soft toy forms.
- "Rig: root, a body bone with squash-and-stretch, 2 arm bones each, 2 foot bones, eye bones for look direction, blend shapes for blink, lids, brows, smile and beak open".
- Animate "anticipation, squash on landing, a small waddle. Arms act like hands; he never flaps or flies".
- Image-to-3D route: feed 00_cree_original.png or poses/stand.png -> GLB, clean eyes/beak, re-topologise. "There is no 3D mesh yet."

### 9.4 Prompt pack (guide page 14, verbatim)
- STYLE: "Premium stylised 3D animated short, soft rounded shapes, designer-toy materials, warm key light with a pink rim light, shallow depth of field, 35mm, vertical 9:16, Creedom palette of magenta, pink and coral with warm gold accents, cosy and cinematic."
- CREE: "Cree, a small round egg-shaped magenta-pink mascot with no neck, big glossy black eyes with white catchlights, thin dark-pink brows, a small rounded yellow-orange beak open in a smile, short rounded wing-arms used like hands, stubby yellow-orange feet, soft matte plush texture, no feathers. Keep him exactly on model."
- SHOT 6: "Inside a glowing timeline track running through a valley of giant film frames, Cree wipes dust off one frame and warm gold light floods out across his face, eyes wide with surprise, frosted glass tag reading '0:34', low angle, magical."
- Note: "Always attach Cree's reference image and check every generation against the character sheet before using it."

### 9.5 Art direction (guide pages 11-13, verbatim)
- Style: "Premium stylised 3D, like a feature-animation short: soft, rounded shapes and designer-toy materials. Not realistic, not cartoon-flat."
- Light: "Warm key, soft fill, a strong pink rim on Cree. Night scenes lit by the ring light and the phone's glow. The reel world glows from within."
- Materials: "Matte plush for Cree, frosted glass for every interface element, soft fabric and wood in the room. Gold only for the buried hook."
- Camera: "35 to 50 mm, shallow depth of field, slow dollies and low tracking shots. One fast whip into the reel and one out."
- People: "The creator is stylised to match Cree's world: soft proportions, simple friendly face, casual clothes, no logos."
- Palette swatches: #F343A2, #E235DD, #E68B70, #FFC21A, #FFF4F8, #0B0B0B ("Creedom magenta to coral, warm gold for the 'found it' moments, blush-white and ink").
- Worlds and props: 1 bedroom-studio at night (desk, ring light, plants, fairy lights, phone on a tripod); 2 inside the reel: glowing timeline track (second markers every few metres) through a valley of giant film frames; 3 viewer-bubbles (translucent spheres that drift away when the reel gets boring); 4 flags: frosted-glass tags e.g. "0:03 · Weak hook"; 5 the buried hook: one dusty frame that floods gold light; 6 "Cree's magnifier: clear glass lens, thin gold rim, wooden handle." Warning: "Use a generic phone and a generic reels interface. No real app interfaces, logos or brands other than Creedom's."

### 9.6 Concept A "The Buried Hook" (recommended), VO about 38 s, 75 words, "warm, conversational storyteller"
0:00 "Her best moment was hiding at second thirty-four. Nobody ever got that far." 0:05 "She posted anyway. A few hundred views. No idea why." 0:09 "So she asked Cree." 0:11 "Cree doesn't guess. He walks through her reel second by second, like a real viewer." 0:17 "Zero to three: a slow start. That's where people swipe." 0:21 "Then, at thirty-four... there it is." 0:25 "Cree carries it to the front. Same reel, new first second." 0:31 "She posts. This time, they stay." 0:35 "Check your reel before you post. Comment CREEDOM."

Shot list (verbatim): 1 0:00–0:05 "Night bedroom-studio, ring light on. Slow push-in over the creator's shoulder to her phone: her reel plays, the view counter sits still. Camera drifts past the phone into the reel's timeline; a faint gold glow far down the track." 2 0:05–0:09 "Close on the phone: a flat graph, a small number. She sighs, drops the phone on the bed, screen up." 3 0:09–0:11 "The screen glows pink. Cree pops up out of the screen like a jack-in-the-box, lands with a squash, waves at her." 4 0:11–0:17 "Cree dives into the screen. Inside the reel: a long glowing timeline track running through a valley of giant film frames. Cree walks it, magnifier up, frames lighting as he passes. Low tracking shot." 5 0:17–0:21 "At 0:03 a crowd of small translucent viewer-bubbles drifts away. A glass tag pops up: 0:03 · Weak hook. Cree frowns, taps it." 6 0:21–0:25 "Deep in the track, a dusty frame. Cree wipes it: gold light floods out, the frame glows. Tag: 0:34 · Best moment. Cree's eyes go wide." 7 0:25–0:31 "Cree lifts the glowing frame overhead and runs it back along the track (comic waddle, speed lines), slots it in at 0:00. Every frame behind re-sorts with a satisfying cascade." 8 0:31–0:35 "Back in the bedroom. She taps Post. The counter starts rolling; little hearts float up. Cree hops on the phone edge and cheers." 9 0:35–0:40 "End card: Cree in front of a soft pink glow, pointing to the Creedom wordmark. A comment box types CREEDOM." Note: "Cut on the music's beat. Hold the gold-frame reveal (shot 6) half a second longer than feels comfortable."

Other concepts: B "The Screen Test": "2 a.m., about to post. Cree pops out of the phone and runs a tiny screening for a crowd of viewer-bubbles. They drift away at 0:03. He fixes the opening; the next screening, they stay." C "The Reel Gym": "Reels are athletes; Cree is the coach with a stopwatch. A flabby, slow-starting reel trains its hook until it sprints off the line." D "The Case of the Missing Views": "Cree as a pocket-sized detective with a magnifier. Clues on a pinboard (timestamps), the culprit is a 4-second intro."

### 9.7 Render spec (verbatim)
Frame "1080 x 1920 (9:16), 24 or 30 fps, 35 to 45 s." Safe zones "top 220 px and the bottom 380 px". Text "Minimal and big ... Captions are added in the edit." Files "Master: ProRes 422 HQ or a high-bitrate MP4 (H.264, 40 Mb/s+). Plus a clean version with no on-screen text." Sound "Deliver picture-only ... (licensed music only)." Extras "A 3:4 cover still (Cree holding the glowing frame) and 3 to 4 stills for the carousel." Checklist: "Cree on model in every shot", "Creator stays the hero", "Product moments are physical, not screens of text", "Nothing in the safe zones", "Ends on Cree + wordmark + CREEDOM".

## 10. Images to upload

All images below exist on disk (checked 2026-11-17). Upload the transparent PNGs as they are; do not flatten them.

| # | File path | Size / format | Description |
|---|---|---|---|
| 1 | /home/user/Nxtlvl-Social/creedom-3d-story/cache/pack/00_cree_original.png | 1080 x 1080, RGBA | THE MASTER REFERENCE (the client's original render, same as creedom-explainer-9x16/assets/img/mascot_src.png and upload 91192a5a-image.png). Cree in three-quarter view facing slightly left, waving: his left wing-arm (frame right) raised high, the other arm short and out to the side low; right foot planted, left foot kicked up and back to frame right. Hot magenta-pink plush egg body with a lighter highlight top-left, big round eyes with pale-pink rims, glossy black pupils and white catchlights, small yellow-orange beak open in a smile with a red mouth, orange-yellow oval feet. Faint semi-transparent pinkish rectangular fringe around the figure (cut-out artefact). Match this above all. |
| 2 | /home/user/Nxtlvl-Social/creedom-explainer-9x16/assets/img/cree.png | 645 x 649, RGBA | Clean tight crop of the master waving pose with the fringe removed; used as the end-card icon. Same file as creedom-3d-story/cache/pack/brand/cree_icon.png. |
| 3 | /home/user/Nxtlvl-Social/creedom-3d-story/cache/pack/01_proportions_front.png | 1280 x 900, RGB on blush white | Front view of Cree (stand pose) with measurement lines and labels: "top of head (0%)", "eye centres (31% down)", "eye: 23% of width each, centres 36% of width apart", "widest, arms included (67% down)", "feet / ground (100%)", "width : height = 1 : 1 (arms included)". Blue circles mark the detected eyes. |
| 4 | /home/user/Nxtlvl-Social/creedom-explainer-9x16/assets/img/poses/stand.png | 820 x 820, RGBA | Stand: front view, both feet planted side by side, both arms relaxed down, calm open-mouth smile, looking at the viewer. |
| 5 | /home/user/Nxtlvl-Social/creedom-explainer-9x16/assets/img/poses/walk.png | 820 x 820, RGBA | Walk A: three-quarter view heading to frame right, one foot kicked back, one arm swung up behind, happy open smile, eyes ahead. |
| 6 | /home/user/Nxtlvl-Social/creedom-explainer-9x16/assets/img/poses/pass.png | 820 x 820, RGBA | Walk B (passing frame): three-quarter view to frame right, one foot planted under him, other foot lifted forward, arms close to the body, open smile. |
| 7 | /home/user/Nxtlvl-Social/creedom-explainer-9x16/assets/img/poses/wave.png | 820 x 820, RGBA | Wave: front view, one wing-arm raised high waving (frame right), other arm low at his side, big excited smile. |
| 8 | /home/user/Nxtlvl-Social/creedom-explainer-9x16/assets/img/poses/point.png | 820 x 820, RGBA | Point: body turned slightly right, one arm stretched straight out pointing to frame right, other hand on belly, eyes looking toward the point, excited smile. |
| 9 | /home/user/Nxtlvl-Social/creedom-explainer-9x16/assets/img/poses/present.png | 820 x 820, RGBA | Present ("ta-da"): facing camera, one arm swept out to frame left palm-up, other arm raised to frame right, warm welcoming smile. |
| 10 | /home/user/Nxtlvl-Social/creedom-explainer-9x16/assets/img/poses/cheer.png | 820 x 820, RGBA | Cheer: both arms thrown up, eyes squeezed shut in happy "^ ^" arcs, beak wide open laughing, one foot kicked up. No blink overlay. |
| 11 | /home/user/Nxtlvl-Social/creedom-explainer-9x16/assets/img/poses/shock.png | 820 x 820, RGBA | Shock: both hands pressed on his cheeks, eyes very wide with tiny pupils, beak open in a round "O". No blink overlay. |
| 12 | /home/user/Nxtlvl-Social/creedom-explainer-9x16/assets/img/poses/sad.png | 820 x 820, RGBA | Sad: slightly slumped, droopy half-lidded eyes looking down, small closed frowning beak, arms hanging. |
| 13 | /home/user/Nxtlvl-Social/creedom-explainer-9x16/assets/img/poses/mag.png | 820 x 820, RGBA | Magnifier: turned to frame left, holding a large gold-rimmed magnifying glass with a dark handle up to his right eye (eye enlarged in the lens), other hand on belly, curious focused look. |
| 14 | /home/user/Nxtlvl-Social/creedom-explainer-9x16/assets/img/poses/phone.png | 820 x 820, RGBA | Phone: facing camera, holding a small white smartphone in both hands at his belly (back of phone to viewer), typing, happy concentrated smile. |
| 15 | /home/user/Nxtlvl-Social/creedom-explainer-9x16/assets/img/poses/think.png | 820 x 820, RGBA | Think: one hand up under his beak like a hand on a chin, other arm folded across his belly, eyes glancing up to the side, closed thoughtful smirk. |
| 16 | /home/user/Nxtlvl-Social/creedom-explainer-9x16/assets/img/poses/proud.png | 820 x 820, RGBA | Proud: chest out, both hands on hips, smug happily narrowed eyes, big satisfied grin. No blink overlay. |
| 17 | /home/user/Nxtlvl-Social/creedom-explainer-9x16/assets/img/logo_src.jpg | 1920 x 1080, JPG on white | The client's Creedom logo: the waving Cree (same as the master, one foot kicked up) left of the wordmark "Creedom" in a rounded geometric sans, horizontal gradient magenta (#F515E8) to pink (#F54BA8) to coral (#F5876C). Shows how Cree sits with the wordmark. |
| 18 | /home/user/Nxtlvl-Social/creedom-3d-story/cache/pack/brand/creedom_wordmark.png | 1426 x 269, RGBA | The "Creedom" wordmark cut from the client logo (exact letterforms and gradient), transparent; pair with the Cree icon on end cards. Same as creedom-explainer-9x16/assets/img/wordmark.png. |
| 19 | /home/user/Nxtlvl-Social/creedom-3d-story/cache/pack/rig_layers/bird.png | 604 x 640, RGBA | REJECTED-STYLE REFERENCE ONLY: the older flat cut-out puppet source (a tight crop of the waving master). Its layers (bird_core, bird_wing, bird_wingl, bird_beak, bird_foot, bird_foot_up) are in the same folder. Upload only if the 3D team needs layer references; label it "old 2D puppet, do not use for animation". |

Supporting documents to upload with the images: /home/user/Nxtlvl-Social/creedom-3d-story/renders/creedom_cree-3d-model-sheet.pdf, /home/user/Nxtlvl-Social/creedom-3d-story/renders/creedom_3d-storytelling-guide.pdf, /home/user/Nxtlvl-Social/creedom-3d-story/cache/pack/poses/poses_eyes_and_boxes.json, /home/user/Nxtlvl-Social/creedom-3d-story/cache/pack/README.txt (or the whole /home/user/Nxtlvl-Social/creedom-3d-story/renders/creedom_cree-3d-reference-pack.zip).

A contact sheet of all 13 poses (for a quick look, not for production) is at /tmp/claude-0/-home-user-Nxtlvl-Social/b1c6bbee-7bc1-59ac-ac25-7b3da31f270a/scratchpad/poses.jpg (2100 x 660, labelled with file names, on a pink ground).
