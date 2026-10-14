---
name: frontend-animation
description: Scroll, entrance, and micro-interactions for the page - CSS-only
  by default, GSAP when the Stack flag requests it. Use in Phase 5 when the
  Stack animation flag is css-only or gsap. Not for hero video/sequence
  logic (hero-media) or 3D (three-js).
metadata: {version: 1.2.0, category: frontend, tier: B}
---
# Frontend Animation

## Purpose
Motion that supports hierarchy and mood without hurting performance or
accessibility.

## Inputs
Stack animation flag, design rationale motion level, tokens (durations/easings).

## Outputs
Animation JS in output/shared/main.js (used by 2+ pages) or the page's own
script.js; animation CSS per the same shared-vs-per-page rule.

## Rules
1. Flag = none: no scroll/entrance animation; hover/focus transitions only.
   Flag = css-only: the CSS-only pattern below (IntersectionObserver
   adds .is-visible; CSS does the rest). Flag = gsap: the GSAP pattern below.
2. All motion gated by prefers-reduced-motion on BOTH sides: rules/css.md
   owns the CSS wrapper, and the JS trigger side is below.
3. Animate transform + opacity ONLY. Never layout properties, never
   width/height/top.
3a. ONE narrow exception - the SECTION COLOUR PROGRESSION: a single fixed
   full-viewport backdrop element whose `background-color` is interpolated
   between the `--section-bg-N` tokens as the page scrolls, so section
   change is felt as a continuous shift rather than announced. Rules that
   keep it honest: exactly one element, `position:fixed; inset:0; z-index:-1`
   (never per-section backgrounds animating in parallel); the driver writes
   ONE custom property and CSS consumes it; no transition on that property
   (it would lag the scroll); passive scroll listener guarded by an actual
   scrollY change, not rAF; and no layout property is touched at any point.
   Under prefers-reduced-motion the backdrop holds one static colour.
   This is the only paint-property animation the OS permits, and it exists
   because it is the site-wide custom-feel device (design-direction 5b).
3b. When client.md `## Hero story` is empty, this progression IS the hero
   backdrop - so it must read as designed at scroll position 0, not just
   in motion.
4. Entrance defaults: 16-24px translate + fade, var(--duration-slow),
   var(--ease-out-expo), stagger 60-90ms, trigger at 20% visibility, once.
5. Content must be visible without JS: the hidden initial state is applied
   by JS adding a class at init, never hardcoded in CSS (no-JS = no hiding).
6. Motion level "subtle": entrances only. "Expressive": may add parallax
   (transform-based, capped) and one signature moment - never on every section.

## CSS-only pattern (the default)
JS (shared/main.js when used on 2+ pages, else the page's script.js): on
init add `.anim-ready` to `<body>`; observe `[data-animate]` with an
IntersectionObserver `{threshold:.2}`; add `.is-visible`, unobserve.
Stagger via an inline `--stagger-i` set from the element index.

    .anim-ready [data-animate]{opacity:0;transform:translateY(20px);
      transition:opacity var(--duration-slow) var(--ease-out-expo),
                 transform var(--duration-slow) var(--ease-out-expo);
      transition-delay:calc(var(--stagger-i,0)*75ms)}
    .anim-ready [data-animate].is-visible{opacity:1;transform:none}

No `.anim-ready` (JS off) = fully visible content. The whole block sits in
`@media (prefers-reduced-motion: no-preference)` per rules/css.md.

## GSAP pattern (only when the Stack flag says gsap)
Load gsap + ScrollTrigger from cdnjs with `defer`, AFTER page content, and
version-pinned with SRI (security-basics). Confirm the licensing tier:
standard GSAP files are free, Club plugins are not. Init inside
DOMContentLoaded and guard `if(!window.gsap) return;` - the site must work
if the CDN fails. Use `gsap.matchMedia()` for reduced-motion and
breakpoint variants. Defaults mirror the CSS pattern (y:24, autoAlpha,
stagger .08, ease "expo.out", once via ScrollTrigger toggleActions).
Pin/scrub only for the single signature moment, desktop-only via
matchMedia. Kill triggers on bfcache restore (`pageshow`) to avoid ghost
states.

## Reduced motion, JS side
rules/css.md owns the CSS wrapper. Here: read
`matchMedia("(prefers-reduced-motion: reduce)").matches` at init and skip
observer/GSAP setup entirely when true. Reduced is not frozen - content
appears immediately, focus styles and non-movement feedback stay.

## Anti-patterns
- Animating everything; scroll-jacking; opacity:0 in stylesheet defaults.
- Per-section background transitions instead of one fixed backdrop (3a) -
  N animating elements where one belongs, and the seams show.

## Changelog
- 1.2.0 CSS-only and GSAP patterns inlined; reduced motion split - CSS wrapper is rules/css.md's, JS gating stays here (v1.13.0)
- 1.1.0 section colour progression: one fixed backdrop, single custom
  property, documented paint-property exception to rule 3 (v1.11.0)
- 1.0.0 initial
