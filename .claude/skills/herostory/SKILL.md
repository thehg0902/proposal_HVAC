---
name: herostory
disable-model-invocation: true
description: Compose cinematic page openers - optional intro video, looping
  hero, polygon/SVG graphic beats, and N pinned scroll-scrub story beats -
  as ONE stage with opacity-only handoffs. Use for the signature
  continuous-shot opener, or to stage client.md's `## Hero story`.
  Not for single-treatment playback (hero-media) or page animation
  (frontend-animation).
metadata: {version: 1.1.1, category: frontend, tier: B}
---
# Herostory

## Purpose
The agency's signature opener: the page begins as a cinematic shot -
(intro) -> looping hero or graphic -> scroll-scrubbed story beats -
experienced as ONE unbroken take. This skill is a composition grammar plus
the proven stage architecture, not a fixed layout: every beat is optional
and the story count is per-project.

## Inputs
client.md `## Hero story` (the sentence to stage), Stack hero-media and
animation flags, ingested assets in output/assets/ (scrub manifests per
system/contracts/asset-slots.md), tokens.css, system/contracts/file-structure.md.

## Outputs
Opening-stage markup in the hero page + driver JS in that page's script.js
+ stage CSS in that page's style.css, assets wired per
system/contracts/file-structure.md.

## Composition grammar
A herostory is a chain of BEATS rendered inside one pinned stage:

    [intro video]? -> [looping hero | graphic]? -> [story 1]? -> ... -> [story N]?

- Any subset is valid. Examples:
  - loop hero only -> this degenerates to hero-media's loop treatment;
    use hero-media directly, no stage needed.
  - loop hero + 2 scrub stories -> the classic run (reference build).
  - intro + loop + 3 stories -> intro plays once (hero-media
    intro-loop handoff), then the run continues as normal.
  - stories only -> the page opens already inside story 1's first frame
    (frame 0001 doubles as poster/LCP).
  - GRAPHIC beats only -> the zero-media default: polygon/SVG scenes
    staged from `## Hero story`. Ships with no media spend at all.
- Each beat = one MEDIA LAYER (scrub frame-sequence on canvas, video,
  still image, or inline SVG graphic) + optionally one COPY LAYER
  (headline/body/CTA lines).
- Every seam between beats is an opacity-only crossfade at a tuned
  progress window. Never a cut, slide, or z-index swap.
- Copy beats are independent of media beats: a copy layer may fade out
  before, during, or after its media layer hands off.

## Graphic beats (the zero-media path)
1. Source of truth is client.md `## Hero story` - one plain sentence
   ("a car driving and stops at a house"). Break it into 2-4 BEATS along
   its verbs: approach -> arrive -> stop. Each beat is one graphic layer.
2. Build each beat as inline SVG built from POLYGONS and simple primitives
   (polygon, path, circle, rect) in token colours - a designed abstraction
   of the scene, never clip-art and never a literal illustration attempt.
   Two to six shapes per beat reads better than twenty.
3. The driver publishes a per-beat progress custom property on the layer
   (`--beat-p`, 0..1). All motion inside a graphic beat is CSS reading that
   property - transform and opacity only, no transitions (they lag reverse
   scrubbing). This keeps choreography in CSS and the driver generic.
4. Graphic beats obey the same seam rules as media beats: opacity-only
   handoff, epsilon start, held boundary states across a long blend.
5. A graphic beat is a complete hero on its own at progress 0 - that first
   composed frame is what a no-JS or reduced-motion visitor sees, and it
   must read as finished design.
6. Upgrade path: when the operator approves the graphic hero at the Phase 2
   gate, matching footage slots go on the Phase 4 shopping list under the
   same beat names, so the same story can become filmed or generated media
   later with no markup change - the layer type swaps, the windows do not.
   Media generation stays behind its own per-slot approval.

## Architecture rule (the shipped pattern)
ONE wrapper, ONE sticky stage, ALL layers stacked inside:

- Wrapper `.hero-stage` = the RUNWAY. Height = (100 + sum of per-beat
  runways)svh, `padding-block:0` (padding desyncs the driver). Budget
  ~90-120svh of runway per story beat plus ~10-15svh per crossfade.
- `.hero-stage__inner` = sticky, `top:0`, 100svh, `overflow:hidden`.
- Media well at z-index 0; DOM order = stacking order (base first,
  last story on top). Reordering markup silently reverses dissolves.
- Copy layers at z-index 1, absolutely stacked, `pointer-events:none`
  when not the active beat (their own links opt back in).
- Driver: templates/herostory-driver.js - a config array of beats;
  add a story by adding a config entry + a canvas/SVG + a copy layer.

## Rules
1. Progress = -rect.top / (wrapperHeight - stickyHeight). Size BOTH in
   svh (vh fallback first, svh second) and cache the sticky height -
   never window.innerHeight, which breathes with the mobile URL bar and
   makes the scrub drift against the scroll.
2. Scroll driver: passive scroll listener guarded by an actual scrollY
   change; deliberately NOT requestAnimationFrame (rAF suspends in
   hidden/background/preview panes and freezes the run on frame 0).
   No CSS transition on any driver-written property - it lags reverse
   scrubbing.
3. Crossfade windows start at epsilon (0.01), never 0.00: at rest,
   resize/sub-pixel jitter around 0 flips the base<->layer swap.
4. Seam quality dictates the dissolve. Compare the two boundary frames
   (SSIM or by eye): near-identical (>~0.98) -> short blend while both
   keep scrubbing; visibly different -> LONGER window and HOLD both
   sequences on their boundary frames for the whole blend (a clean
   still-to-still dissolve, never two moving images cross-dissolving).
5. Scrub = canvas + preloaded stills. NEVER video.currentTime
   (hero-media references/scroll-scrub.md). Manifest values come from
   data-* attributes, not fetch() - the page must scrub from file://.
   Preload with a stride (every 4th frame) then backfill; draw the
   nearest loaded frame while the exact one loads (never blank); defer
   later sequences' bulk preload until the run is underway.
6. Loop video: native `loop` ONLY for footage confirmed seamless;
   otherwise restart on 'ended' (an honest hard cut, fixable in the
   footage, not hidden in the player). Pause the video once fully
   covered by the next layer - stop decoding what nobody sees.
7. Copy layers: stagger lines within their own layer only (a stage-wide
   query smears the staggers together). Fully-faded layers also get
   visibility:hidden - keeps invisible links out of the tab order and
   the a11y tree.
8. Reduced motion: CSS collapses the wrapper to a normal stacked
   document (height:auto, static layers, canvases hidden) and the
   driver returns before binding anything. The poster or the graphic's
   rest state stands. Poster, LCP, autoplay (muted+playsinline), and
   weight budgets all inherit from hero-media rules 4-7.
9. Scrims and focal-point tracking are published as CSS custom
   properties per tick (--hero-scrim, --story-scrim, --hero-focal-x).
   Portrait crops track the subject across beats via object-position.
10. No-JS: a <noscript> block collapses the runway to 100svh and shows
    only the first copy beat over the poster or the graphic's rest state -
    the frozen frame must read as a finished hero on its own.

## Tuning workflow
The TUNING CONSTANTS block in the driver is the contract. All windows
are progress 0..1 along the runway, ordered, non-overlapping except
designed blends. Choreography changes = window changes; touch code only
when a new capability is needed. Verify seams at the exact boundary
pixel (scroll there, screenshot, check for gaps/jumps).

## References
- references/stage-architecture.md - timeline model, runway math, seam
  guidance, portrait focal tracking, and the alternate GSAP
  pinned-sections pattern (with the exact-pixel pin-end fix).

## Scripts / Templates
- templates/herostory-driver.js - config-driven N-beat driver (copy
  into the page's script.js; keep the defensive guards and comments)
- templates/herostory-stage.html - stage markup skeleton
- templates/herostory-stage.css - stage CSS incl. reduced-motion
  collapse and noscript notes
- templates/herostory-graphic-beat.html - a worked polygon graphic beat
  (the "car stops at a house" example) with its CSS choreography

## Anti-patterns
- Scrubbing via video.currentTime; rAF-driven scroll reading; vh-only
  sizing; CSS transitions on driver-written properties.
- Separate adjacent pinned sections when one shared stage would do; if
  they ARE needed, GSAP pins without explicit end:'+='+sectionHeight
  leave a 1-viewport gap (see references).
- Native loop on unverified footage; lazy-loading the poster; copy
  layers left focusable while invisible.
- Literal clip-art illustration in a graphic beat, or a graphic beat
  whose rest state does not read as a finished hero.

## Changelog
- 1.1.1 description trimmed (v1.13.0)
- 1.1.0 graphic beat type: polygon/SVG scenes staged from client.md
  `## Hero story`, per-beat progress custom property, footage upgrade
  path under the same beat names (v1.11.0)
- 1.0.0 extracted from a shipped HVAC build (2026-07): single pinned
  stage, 3 media layers, 3 copy beats, verified 0px seams.
