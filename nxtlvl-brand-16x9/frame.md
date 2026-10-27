---
version: alpha
name: Nxtlvl Social — Frame (video / frame layer)
description: >
  The Nxtlvl Social brand at frame scale (1920×1080): ink ground with violet light, Archivo display,
  Instrument Serif for the one emphasised phrase, Instrument Sans for UI. Colours, fonts and weights
  are normative; sizes and decoration are scaled for video.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  bg: "#05030C"
  primary: "#7D18FC"
  text: "#F5F2FF"
  text-muted: "#9F97BE"
  text-light: "#6B6391"
  primary-lift: "#A95CFF"
  primary-pale: "#D8BBFF"
  primary-deep: "#3D0789"
  surface: "#110C22"
  accent-light: "rgba(125, 24, 252, 0.08)"
  accent-medium: "rgba(125, 24, 252, 0.15)"
  border: "rgba(125, 24, 252, 0.2)"
  card-bg: "rgba(125, 24, 252, 0.04)"
  positive: "#059669"
  negative: "#dc2626"

radii:
  pill: "100px"
  card-lg: "14px"
  card-md: "12px"
  card-sm: "10px"
  bar: "6px"
  circle: "50%"

typography:
  # — reading ramp (Archivo body + Archivo chrome) —
  body:    { fontFamily: "Instrument Sans", cqw: 0.85, weight: 400, lineHeight: 1.6, color: "text-muted" }
  h4-eyebrow:{ fontFamily: "Archivo", cqw: 0.8, weight: 600, tracking: "0.08em", upper: true, color: "primary" }
  tag:     { fontFamily: "Archivo", px: 12, weight: 500, color: "primary" }
  counter: { fontFamily: "Archivo", px: 13, weight: 500, tracking: "0.05em", color: "text-muted" }
  # — display / numerical ramp (Archivo, near-black headings / cobalt numerals) —
  h3:      { fontFamily: "Archivo", cqw: 1.25, weight: 500, lineHeight: 1.3, tracking: "-0.02em", color: "text" }
  stat-num:{ fontFamily: "Archivo", cqw: 1.9, weight: 700, lineHeight: 1.0, color: "primary" }
  blockquote:{ fontFamily: "Archivo", cqw: 2.4, weight: 500, lineHeight: 1.35, color: "text" }
  h2:      { fontFamily: "Archivo", cqw: 2.6, weight: 600, lineHeight: 1.1, tracking: "-0.02em", color: "text" }
  metric-value:{ fontFamily: "Archivo", cqw: 3.0, weight: 700, lineHeight: 1.0, color: "primary" }
  h1:      { fontFamily: "Archivo", cqw: 4.2, weight: 800, lineHeight: 0.98, tracking: "-0.035em", color: "text" }
  accent-serif:{ fontFamily: "Instrument Serif", weight: 400, color: "primary-lift", note: "upright (not italic); the one emphasised phrase in a headline" }
  quote-mark:{ fontFamily: "Archivo", cqw: 8.0, weight: 700, lineHeight: 0.5, color: "primary", opacity: 0.15 }

spacing:
  pad-x: "5cqw"
  pad-y-top: "5cqw"
  gap-cards: "1.4cqw"
  accent-line: "60px × 4px"

components:
  card-tinted:
    backgroundColor: "{colors.card-bg}"
    border: "1.5px solid {colors.border}"
    rounded: "{radii.card-lg}"
    shadow: "none"
    description: "Universal content card. Never solid-colored, never opaque-bordered, NO shadow."
  metric-card:
    backgroundColor: "{colors.card-bg}"
    border: "1.5px solid {colors.border}"
    rounded: "{radii.card-lg}"
    typography: "{typography.metric-value} ({colors.primary}) + {typography.metric-label} + {typography.metric-desc}"
    description: "+ optional inline ↑/↓ change chip ({colors.positive}/{colors.negative} text, no fill)."
  tag-pill:
    backgroundColor: "{colors.accent-light}"
    textColor: "{colors.primary}"
    rounded: "{radii.pill}"
    typography: "{typography.tag}"
    description: "Top-right of the slide-header."
  cta-button:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.text}"
    rounded: "{radii.pill}"
    typography: "Instrument Sans 600"
    shadow: "soft cobalt on hover only — the system's only shadow"
    description: "The one solid element."
  accent-line:
    backgroundColor: "{colors.primary}"
    size: "60×4, 2px radius"
    description: "Above cover titles / eyebrow separators."
  bar-track:
    backgroundColor: "{colors.accent-light}"
    fill: "{colors.primary} (display:block so width resolves)"
    rounded: "{radii.bar}"
    description: "28px track; fill carries the value."
  step-circle:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.text}"
    rounded: "50%"
    size: "56px"
    description: "Sequential steps fade opacity 1.0→0.85→0.7→0.55."
  split-highlight:
    backgroundColor: "{colors.accent-light}"
    borderLeft: "4px solid {colors.primary}"
    rounded: "{radii.card-md}"
    description: "Inline pull-quote callout."
  slide-header:
    typography: "{typography.h4-eyebrow} (cobalt) left, tag-pill right; {typography.h2} below"
    description: "Top band of every content frame."
  atmosphere:
    elements: "clipped diagonal cobalt-tint panel, 3×3 cobalt dot grid, concentric closing rings"
    description: "Cover/closing only. Never on content frames."
  progress-bar:
    backgroundColor: "{colors.primary}"
    size: "3px tall, bottom edge, width grows with index"
    description: "Persistent progress strip."
---

# Nxtlvl Social — Frame

The frontmatter is the source of truth: quote its hex values and families exactly.

- **Fonts**: Archivo (display, `font-variation-settings:'wdth' 112,'wght' 800`), Instrument Sans (body, UI),
  Instrument Serif (the one emphasised phrase per headline, upright, in primary-lift). Weights shipped:
  400, 500, 600, 700 (Instrument Sans); 100–900 (Archivo variable); 400 (Instrument Serif).
- **Ground**: ink `#05030C` with violet light (two radial glows, one blurred ribbon, a still star field),
  kept behind content; never a full-frame linear gradient.
- **Surfaces**: product UI is a tinted glass card: `rgba(17,12,34,.86)` fill, 2 px `rgba(169,124,255,.32)`
  border, 24 px radius, one soft shadow. Chips are pills with a 1.5 px border. The one solid element per
  frame is violet `#7D18FC` (a button, a badge).
- **Do**: one accent per shot; headlines 120–150 px; UI text 24–34 px; the emphasised phrase in serif.
- **Don't**: gradient text; prices; WhatsApp; the logo in a corner; glass as decoration.
