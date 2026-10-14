# Herostory stage architecture

## The model

    .hero-stage                    height: (100 + R)svh   <- RUNWAY
      .hero-stage__inner           sticky top:0, 100svh   <- STAGE
        .hero-stage__media         z:0, absolute inset:0
          <video data-hero-loop>   beat 0 (optional loop hero)
          <div data-graphic="1">   beat 1 (inline SVG polygon scene)
          <canvas data-scrub="1">  beat 1 alt (opacity 0 until its window)
          <canvas data-scrub="2">  beat 2
          ...                      DOM order = stacking order
          .hero-stage__scrim--lead   gradient scrim, driver-dimmed
          .hero-stage__scrim--flat   flat wash behind centred copy
        .hero-stage__layer[data-hero-layer="lead"]   copy beat 0
        .hero-stage__layer[data-hero-layer="s1"]     copy beat 1
        ...

Progress p = -stage.getBoundingClientRect().top / (offsetHeight - stickyH),
clamped 0..1. Every visual is a pure function of p - scrolling backwards
replays the run in reverse for free.

## Timeline model
Lay all windows on one 0..1 ruler. Reference run (loop + 2 stories over
240svh of travel):

    p:      0    .05        .42  .44   .56              .95  1
    media:  loop |xfadeA| scrub A | HOLD |xfadeB| scrub B | hold
    copy:   lead-out .00-.14
                     story1-in .16-.38   story1-out .42-.48
                                          story2-in .60-.92

Rules of thumb:
- First crossfade starts at 0.01 (epsilon), not 0 - rest-state jitter.
- A copy beat clears BEFORE its media dissolve begins (story1-out ends
  at .48; xfadeB runs .44-.56) so text never rides a dissolve.
- Last scrub ends ~0.95; the final 5% holds the end frame so the unpin
  doesn't clip the last movement.

## Runway math
travel = wrapper - 100svh. Budget ~90-120svh per story's scrub + copy
dwell, ~10-15svh per held dissolve. 2 stories -> 240svh travel ->
340svh wrapper. 3 stories -> ~340-360svh travel -> ~440-460svh wrapper.
Longer runway = slower, more luxurious scrub; shorter = snappier.

Graphic beats are cheaper to dwell on than footage: 70-90svh per beat is
usually enough, because a polygon scene has less detail to read than a
filmed frame.

## Seam quality -> dissolve design
Measure or eyeball the similarity of the two frames at a seam:
- Near-identical (e.g. loop's rest frame vs sequence frame 0001,
  SSIM ~0.99): short window (~4% of progress), both may keep moving.
- Smooth-but-different (SSIM ~0.94): longer window (~12%), and HOLD
  both boundary frames for the whole blend - freeze A on its last
  frame, keep B on frame 0001, dissolve, then start B's scrub.
- Unrelated shots: consider a dip-to-black instead (hero-media
  loop-crossfade technique) or regenerate the footage so the seam
  matches (last frame of A ~= first frame of B is a media-generation
  requirement, not a code fix).
- Graphic-to-graphic seams are the easiest case: hold both beats'
  shape states across the blend and the dissolve reads as a morph.
  Graphic-to-footage seams are the hardest - match the footage's first
  frame composition to the graphic's last shape positions, or dip.

## Graphic beat choreography
The driver publishes `--beat-p` (0..1 within that beat's scrub window) on
each graphic layer. All motion is CSS reading that property:

    [data-graphic] .car {
      transform: translate3d(calc(var(--beat-p, 0) * 62vw), 0, 0);
    }
    [data-graphic] .house { opacity: calc(var(--beat-p, 0) * 1.4); }

Constraints that matter:
- transform and opacity only. A polygon scene tempts you to animate
  `points` or `d` - don't; it forces layout/paint on every tick.
- No `transition` on anything reading `--beat-p`. Reverse scrubbing lags
  visibly, and the whole point is that the run is a pure function of p.
- Use `will-change: transform` sparingly - one or two moving shapes, not
  every polygon.
- Give every shape a token colour (`var(--color-*)`), so the graphic hero
  re-skins with the direction instead of fighting it.

## Portrait focal tracking (mobile)
A portrait cover-crop discards most of a 16:9 frame and the subject
drifts across beats. Publish --hero-focal-x from the driver
(lerp between per-beat start/end percentages, continuous across seams)
and apply it only under @media(max-width:640px):
object-position:var(--hero-focal-x,40%) center.

Graphic beats don't need focal tracking - instead give the SVG a
viewBox and `preserveAspectRatio="xMidYMid slice"`, and shift the scene's
composition at narrow widths with a media query on the shape transforms.

## Alternate pattern: adjacent GSAP-pinned sections
Prefer the single shared stage. If a build genuinely needs separate
back-to-back pinned scrub sections (e.g. sections owned by different
templates), know this root cause: CSS position:sticky AND GSAP's
end:'bottom bottom' both release a pinned stage exactly ONE
VIEWPORT-HEIGHT before the section's true end - standard behavior, but
it leaves a 1-viewport gap between consecutive pinned sections. Fix:

    ScrollTrigger.create({
      trigger: sec, pin: stage, start: 'top top',
      end: '+=' + sec.offsetHeight,   // NOT 'bottom bottom'
      scrub: true
    });

Section 1 then unpins at the EXACT pixel section 2 pins (verified 0px
gap in the reference build). Re-measure offsetHeight on resize.

## Hard-won details worth keeping
- padding-block:0 on the wrapper is load-bearing: section padding sits
  inside offsetHeight but not inside the sticky travel -> driver desync.
- vh declared before svh: without svh support the svh line is invalid;
  if svh were the only declaration the wrapper collapses to auto,
  runway <= 0, and the driver silently disables itself.
- Cache the sticky height on resize; reading offsetHeight every tick
  forces a second layout.
- getBoundingClientRect() (READ) before any style writes in the tick.
- Scrims must ramp toward their maximum where the footage is brightest,
  measured against the WORST frame, not the average one.
