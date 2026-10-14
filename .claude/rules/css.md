---
paths: ["**/*.css"]
---
# CSS rules (load only when editing CSS)
These are the SINGLE SOURCE for the mechanical constraints below; skills
add nuance on top and never restate them.
- var(--token) only; zero hardcoded colors/sizes/durations (system/contracts/design-tokens.md).
- Mobile-first: base styles are mobile; min-width media queries at 640/1024px.
  Resist adding breakpoints beyond 640/1024.
- BEM-lite per system/contracts/component-api.md. No !important except utilities.
- MOTION SAFETY (owner): wrap all keyframe/transition motion in
  @media (prefers-reduced-motion: no-preference). Reduced != frozen - keep
  instant state changes, focus styles, and non-movement hover feedback.
  JS-side motion gating is the animation/hero skills' job, not this file's.
- TOUCH + VIEWPORT (owner): tap targets >= 44px with >= 8px gaps; inputs
  font-size >= 16px (prevents iOS focus zoom); full-height sections use
  100svh, never 100vh; fixed bars pad with env(safe-area-inset-*); no
  horizontal overflow at 360px, ever.
- CONTRAST: use only token pairings design-tokens already verified
  (4.5:1 body / 3:1 large+UI). Text over imagery needs a scrim - verify
  against the worst-case frame, not the average one.
- Animate transform and opacity only. The one documented exception is the
  section colour progression's single fixed backdrop (frontend-animation).
- Max nesting depth 2. One component per block comment header.
- Card/column grids: auto-fit can strand a lone widow card in the last
  row - if item-count mod columns = 1, use explicit repeat(N,1fr)
  breakpoints or span/center the last item instead.
- Fluid type via clamp() from tokens; fluid space allowed on section
  padding. Tables become stacked cards under 640px.
