---
name: hero-media
disable-model-invocation: true
description: Implement hero/section motion media - looping video
  (crossfade), intro+loop handoff, scroll-scrub frame sequences,
  play-once-then-freeze, reverse-then-freeze, returning-visitor
  detection. Use when building or editing any section with
  video/sequence media. Not for general page animation
  (frontend-animation), generating the media itself (media-generation), or
  composing multi-beat opening sequences (herostory).
metadata: {version: 1.2.0, category: frontend, tier: B}
---
# Hero Media

## Purpose
Cinematic hero motion that is fast, robust, and plays exactly once per
visitor - the agency's signature hero system.

## Inputs
client.md Stack hero-media flag, ingested assets in output/assets/ (with
MEDIA_LOG rows; scrub manifests per system/contracts/asset-slots.md),
tokens.css, system/contracts/file-structure.md.

## Outputs
Hero section markup + hero JS in the hero page's script.js + poster
assets wired in (assets central in output/assets/).

## Rules
1. Format decision per the MP4-vs-sequence table below. Default: MP4
   (h.264, muted, playsinline) with .webp poster. Sequence only when
   scroll-scrubbing or transparency is required.
2. Behavior default: play once on first visit, freeze on final frame;
   returning visitors (localStorage flag, site-slug prefixed) see the
   final frame immediately - templates/returning-visitor.js.
3. Play-once: templates/play-once-freeze.js (pause on 'ended', never
   loop). Reverse effects: templates/reverse-freeze.js (rAF-driven
   currentTime stepping - native reverse playback is not reliable).
4. Poster is mandatory and is the LCP candidate: preload it, size it,
   never lazy-load hero media.
5. Reduced motion: prefers-reduced-motion users get the poster only -
   wire in JS, not just CSS.
6. Autoplay requires muted + playsinline; never audio. If autoplay is
   blocked, the poster stands - design so the frozen frame is a complete
   hero on its own.
7. Weight budget: <= 8s duration, and bytes per the ACTIVE hosting
   profile in the performance skill's rule 1 table - it owns those
   numbers and they differ by profile, so read them rather than assuming
   the generous set. The no-cdn profile is the default whenever client.md
   `Hosting plan:` is unknown, and it is the tighter one. Over budget ->
   re-encode or cut before shipping; check.py audits real page weight.
8. Treatment selection follows the Stack flag / shopping-list treatment
   (system/contracts/asset-slots.md):
   - loop: templates/loop-crossfade.js - rAF dip-to-black hides the cut;
     use the native loop attribute ONLY for footage designed seamless.
   - intro-loop: templates/intro-loop.js - intro plays once, rAF
     crossfade hands off to the natively-looping loop video; poster =
     intro's first frame.
   - scroll-scrub: templates/scrub-player.js reads the /ingest manifest;
     canvas-based, never video.currentTime (references/scroll-scrub.md);
     scrub section is taller than the viewport with a sticky inner
     stage; frame 0001 doubles as poster.
   All three keep rules 4-6: poster mandatory, reduced-motion gets the
   poster, muted+playsinline, frozen frame is a complete hero.

## MP4 vs frame sequence

| Need | Use |
|---|---|
| Autoplay ambiance, play-once | MP4 h.264 |
| Scroll-scrubbed motion | JPEG/WebP sequence on canvas |
| Alpha over the page background | Sequence (or WebM+alpha with mp4 fallback) |
| Lowest effort, best compression | MP4 |

MP4 encoding: h.264 high profile, CRF 23-26, audio track STRIPPED (it
wastes bytes on a muted video), faststart flag, 1080p max (720p is often
indistinguishable in a hero), 24fps. Poster: extract the FINAL frame ->
.webp q80 - final, because the freeze and returning-visitor states land
there. Sequence: cap ~60-90 frames, .webp q75, preload progressively, draw
to a canvas sized by devicePixelRatio capped at 2.

## References
- references/scroll-scrub.md - canvas vs currentTime, budget math,
  section sizing, progressive loading

## Scripts / Templates
- templates/hero-video.html - canonical markup
- templates/play-once-freeze.js, reverse-freeze.js, returning-visitor.js
- templates/loop-crossfade.js, intro-loop.js, scrub-player.js
  (v1.3.0 slot treatments)
  (copy into the hero page's script.js and adapt; keep the defensive
  guards; asset paths: `assets/...` from output/ root, `../assets/...`
  from a page folder)

## Anti-patterns
- Looping hero video (distracting, battery); YouTube embeds as heroes;
  lazy-loading the poster; localStorage keys without site prefix.

## Changelog
- 1.2.0 MP4-vs-sequence table inlined; rule 7 now reads the ACTIVE hosting profile's byte budget from performance instead of restating the cdn numbers - it contradicted the tighter no-cdn default (v1.13.0)
- 1.1.0 slot treatments: loop-crossfade, intro-loop, scroll-scrub
- 1.0.0 initial (encodes patterns from prior client work)
