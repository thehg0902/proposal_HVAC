---
name: design-tokens
description: Produce output/shared/tokens.css - the complete design token set
  (colors, type scale, spacing, motion) implementing the approved design
  direction per system/contracts/design-tokens.md. Use in Phase 2 after
  design-direction. Not for component CSS (layout-systems, components).
metadata: {version: 1.2.0, category: design, tier: A}
---
# Design Tokens

## Purpose
One file, one source of truth for every visual value on the site.

## Inputs
Design rationale in system/state/DECISIONS.md, client.md Brand colors,
system/contracts/design-tokens.md (the required token list - obey exactly).

## Outputs
output/shared/tokens.css defining every token in the contract, nothing
else. Then `python3 system/scripts/generate-style-preview.py` renders the
tokens as system/preview/style-preview.html (palette, contrast pairings, type
scale, mock hero) for the Phase 2 approval gate — fix any CONTRAST
FAIL it prints before presenting.

## Rules
1. Emit the full required token set from the contract even if some tokens
   are initially unused - consumers rely on their existence.
2. Colors: build a palette around client brand colors; verify every
   text/bg pairing you intend to use hits WCAG AA (4.5:1 body, 3:1 large).
   Use the palette-construction section below.
2a. SECTION COLOUR PROGRESSION (every build): emit an ordered sequence
   `--section-bg-1 ... --section-bg-N` (N = the page's section count from
   the Phase 1 architecture, minimum 3) plus `--page-bg-blend` as the
   driver's output slot. The steps walk one deliberate path - light to
   deep, warm to cool, or tint to neutral - never random alternation, and
   every step must still pass AA against `--color-text` and
   `--color-text-muted`, because copy sits on all of them. This sequence
   is the site-wide custom-feel device and, when there is no hero story,
   the hero backdrop itself. Verify the WHOLE sequence, not just the ends.
3. Type: pick a pairing per the typography section below; self-host .woff2 in
   output/assets/fonts (file-structure contract); modular scale ratio per
   direction (calm 1.2, expressive 1.333).
4. Spacing/radius/shadow/motion values per the contract defaults unless
   the direction justifies deviation - note deviations in tokens.css
   comments.
5. tokens.css contains ONLY :root (and optional [data-theme=dark])
   custom properties + the @font-face rules. No selectors, no components.

## Palette construction
From one brand colour: derive primary-dark (same hue, -25 to -35 L in
HSL), accent (analogous for calm directions, complementary for energetic),
neutrals tinted 2-4% toward the primary hue (never the pure-gray #808080
family), bg near-white or near-black per direction, surface one step from
bg. Contrast method: compute ratios for text/bg, text-muted/bg, text on
primary buttons, accent on bg - body >= 4.5:1, large text and UI borders
>= 3:1. A client brand colour that fails as text is used only for large
elements and fills; derive a darker text-safe variant and log why in
DECISIONS.md so the client understands. Distribution 60-30-10: neutrals
dominate, primary structures, accent is scarce (CTAs, highlights) -
accent overuse is the #1 amateur tell.

## Typography
Pairings by direction (all have solid free/OFL options - verify the
current licence before shipping):
- Quiet luxury / premium: high-contrast serif display + neutral sans body
- Craft / warm: humanist serif or slab + humanist sans
- Clinical calm: geometric or humanist sans for both, weight contrast only
- Bold energy: condensed grotesque display + plain grotesque body
Max 2 families; 2-3 weights per family (file size); `--text-hero` uses
clamp() for fluid scale, e.g. clamp(2.25rem, 5vw + 1rem, 4.5rem); body
16px minimum on mobile. Loading: @font-face with font-display: swap,
preload only the heading woff2 used above the fold.

## Anti-patterns
- Hardcoding any visual value outside tokens.css anywhere in the project.
- Google Fonts <link> tags (privacy + performance): self-host instead.

## Changelog
- 1.2.0 palette construction + typography inlined from references/ (v1.13.0)
- 1.1.0 section colour progression tokens (--section-bg-N +
  --page-bg-blend), AA-verified across every step (v1.11.0)
- 1.0.0 initial
