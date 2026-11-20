# Google Workspace logo

The Shooting Star with the nxtlvl social wordmark, sized for Google Workspace's custom logo
(Admin console → Account → Account settings → Personalization → Custom logo): transparent PNG, 320 × 132, ~3 KB.

| File | Use |
|---|---|
| `workspace-logo-light.png` | **Upload this one.** Dark ink for Google's white header |
| `workspace-logo-light-tagline.png` | Same, with "AI-DRIVEN CREATIVE" under the name |
| `workspace-logo-dark.png`, `workspace-logo-dark-tagline.png` | White version, for dark backgrounds (decks, docs) |

On light backgrounds the star and main trail are Ink `#0B0816` (the white trail would vanish on white), the other
trails Violet `#7D18FC` and Lift `#A95CFF`; "social" and the tagline are `#6B6391` as in `../logo.svg`.
Rebuild with `python3 workspace/source/build.py` from `brands/nxtlvl/`.
