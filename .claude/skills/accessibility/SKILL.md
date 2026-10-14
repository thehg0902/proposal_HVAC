---
name: accessibility
description: Meet WCAG 2.1 AA across the site - semantics, contrast, focus,
  keyboard operability, motion safety. Use in Phase 5 while building and as
  an audit before QA. Not the generic QA gate (qa-review).
metadata: {version: 1.1.0, category: frontend, tier: B}
---
# Accessibility

## Purpose
AA compliance as a build property, not a retrofit.

## Inputs
output/, shared/tokens.css (contrast pairs), rules/html.md baseline.

## Outputs
Compliant markup/CSS; audit notes in BUILD_STATE.md.

## Rules
1. Semantics first: landmarks, heading order, lists as lists, buttons for
   actions / links for navigation - never divs with click handlers.
2. Contrast: design-tokens verified the PALETTE and rules/css.md carries
   the floors. Your job is USAGE - text over imagery (scrim against the
   worst-case frame, not the average), text over the section colour
   progression at every step, and state colours (hover, disabled, error).
3. Keyboard: everything operable; visible :focus-visible style (token-based,
   never outline:none without replacement); logical tab order; skip link
   to #main on multi-section pages.
4. Forms: label every input (visible label, not placeholder-as-label);
   errors announced via aria-live region; required marked in text.
5. Motion: delegated to frontend-animation reduced-motion reference - but
   audit that it actually happened.
6. Images: alt discipline per rules/html.md; decorative -> alt="".
7. Run the audit checklist below before handing to /qa.

## AA audit checklist (run per page)
- [ ] Tab through the whole page: order logical, focus always visible, no traps
- [ ] Zoom 200%: no loss of content or function, no horizontal scroll
- [ ] Heading outline reads as a sensible document (h1 > h2 > h3)
- [ ] Landmarks: exactly one main; nav labelled; footer present
- [ ] Every control reachable and operable by keyboard (accordion, nav
      toggle, lightbox close on Esc)
- [ ] Text over imagery: scrim present, worst-case frame still >= 4.5:1
- [ ] Forms: labels, error text, aria-live, autocomplete attrs (tel, email)
- [ ] Tap targets and link text: targets per rules/css.md, link text
      meaningful out of context
- [ ] Reduced-motion verified by emulation: no entrance motion, video still
- [ ] Page has a lang attribute, a unique title, and works with JS disabled

## Anti-patterns
- aria-* as a fix for wrong elements; contrast checked only on the palette
  page, not over photos.

## Changelog
- 1.1.0 audit checklist inlined; contrast rule now owns USAGE only - rules/css.md carries the floors (v1.13.0)
- 1.0.0 initial
