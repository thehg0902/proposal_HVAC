---
name: layout-systems
description: Compose page layouts - section rhythm, grid, container, and
  responsive behavior - implementing the architecture and design direction.
  Use in Phase 5 when building page structure. Not for individual component
  markup (components) or hero media logic (hero-media).
metadata: {version: 1.4.0, category: frontend, tier: B}
---
# Layout Systems

## Purpose
Pages that feel designed, not stacked: deliberate rhythm, alignment, and
responsive behavior per system/contracts/component-api.md and file-structure.

## Inputs
Architecture + design rationale in DECISIONS.md, tokens.css, contracts.

## Outputs
Page HTML skeletons + base.css layout layer.

## Rules
1. One .container (max-width var(--container-max), inline padding
   var(--space-4)) per section; full-bleed backgrounds on the section.
2. Section vertical rhythm via var(--section-pad-y); vary background
   (bg/surface alternation or one accent-tinted band) to create rhythm -
   never vary padding randomly.
3. Grids: CSS grid with repeat(auto-fit, minmax(min(100%, Xrem), 1fr))
   for card sets - EXCEPT when the item count strands a widow (count
   mod columns = 1 at any breakpoint): then use explicit repeat(N,1fr)
   per breakpoint, or span/center the last card deliberately
   (rules/css.md). Check the actual card count before choosing.
4. Mobile-first (rules/css.md); test composition at 360/768/1280 widths
   mentally before writing; no horizontal scroll ever.
5. Asymmetry/overlap only if the design direction's distinctive element
   calls for it - and contained so it degrades safely.
6. The hero-composition patterns below govern above-the-fold layout;
   the responsive-behavior section covers breakpoint details.
7. The Phase 2 layout preview (system/preview/layout-preview.html) is BINDING:
   it was authored with this skill's patterns and approved by the
   operator - Phase 5 reproduces its section order, grid, spacing
   rhythm, and animation timing exactly; any deviation the build
   requires gets one line in DECISIONS.md before it ships.
8. Each section declares its step in the SECTION COLOUR PROGRESSION
   (`--section-bg-N` from design-tokens) as a data attribute or class the
   backdrop driver reads - sections themselves stay transparent so the one
   fixed backdrop can blend between steps (frontend-animation 3a). This
   replaces the old background-alternation habit in rule 2: alternation is
   a two-value loop, the progression is a path. Full-bleed section
   backgrounds are still allowed where a section needs its own surface -
   they sit above the backdrop and opt out of the blend deliberately.

## Hero composition patterns (pick per direction + media availability)
1. Full-bleed media + overlay copy - needs strong media; the overlay keeps
   AA contrast via a gradient scrim token, never a guessed opacity.
2. Split hero (copy | media) - safest for trades and clinics; copy left on
   LTR.
3. Contained media card on a tinted band - premium feel, survives weaker
   media.
4. Type-only hero - when no good media exists, lean on the direction's
   distinctive typography. Usually better than bad stock.
All four: H1 + subhead + primary CTA visible without scrolling at 360x640;
phone-first niches put tap-to-call beside or above the CTA.

## Responsive behavior
Breakpoints are base / 640 / 1024 only (rules/css.md) - resist adding more.
Nav: <= 5 links can stay inline-condensed on mobile if they fit, else
hamburger with a no-JS fallback (nav visible, toggle hidden). Tables become
stacked cards under 640px. Media boxes use object-fit: cover. Verify
tap-to-call visibility at 360px before anything else.

## Anti-patterns
- Same centered-text-over-image hero for every client.
- min-height: 100vh on mobile (browser chrome jump) - use svh or budget.

## Changelog
- 1.4.0 hero composition patterns + responsive behavior inlined from references/ (v1.13.0)
- 1.3.0 rule 8: sections declare their step in the section colour
  progression; one fixed backdrop blends between steps (v1.11.0)
- 1.2.0 binding Phase 2 layout preview (v1.7.1)
- 1.1.0 grid widow exception on rule 3 (v1.6.0 - found in build #2)
- 1.0.0 initial
