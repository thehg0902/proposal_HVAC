/* Herostory driver — one pinned stage, N media beats + M copy beats,
   opacity-only handoffs, all a pure function of scroll progress.
   Copy into the hero page's script.js and tune BEATS/COPY below.
   Generalized from a shipped build; the comments encode the WHY —
   keep them. */
(function () {
  'use strict';

  /* ==========================================================
     TUNING — all values are progress 0..1 along the runway
     (wrapper height − 100svh stage = the travel distance).

     MEDIA beats stack in DOM order and hand off by opacity only:
       base (loop video, graphic, or first canvas)
         --xfade--> beat 1 --xfade--> beat 2 --> ...
     Windows must be ordered and non-overlapping except designed
     blends. First xfade starts at 0.01 (epsilon, NOT 0 — at rest,
     resize/sub-pixel jitter around 0 flips the swap back and forth).

     Seam rule: if a seam's boundary frames are visibly different,
     lengthen its xfade window and leave a gap between the previous
     beat's end and the next beat's start — both sides HOLD their
     boundary state through the blend (clean dissolve, not two moving
     images). Near-identical seams can blend short and keep moving.

     Beat types:
       'video'   — the looping base layer, no windows needed
       'scrub'   — canvas + preloaded frame stills (needs data-scrub-*)
       'graphic' — inline SVG polygon scene; the driver publishes
                   --beat-p (0..1) on the layer and CSS does the rest */
  var MEDIA = [
    /* beat 0 — looping hero video (optional; delete if none).
       No windows: it is the base layer, covered by whatever follows. */
    { sel: '[data-hero-loop]', type: 'video' },
    /* beat 1 — first story beat. Swap type:'graphic' <-> type:'scrub'
       WITHOUT touching the windows: that is the upgrade path from the
       zero-media polygon hero to real footage.
       NOTE: omit `xfade` when this beat is the BASE layer (no video
       above it) — a base layer's opacity belongs to CSS, so the scene is
       already composed at scroll position 0. Give it an xfade ONLY when
       something underneath it must show first. */
    { sel: '[data-graphic="1"]', type: 'graphic',
      xfade: [0.01, 0.05],      // near-identical seam: short blend
      scrub: [0.01, 0.42] },    // then HOLDS its end state
    /* beat 2 — second story beat */
    { sel: '[data-scrub="2"]', type: 'scrub',
      xfade: [0.44, 0.56],      // different seam: long, held dissolve
      scrub: [0.56, 0.95],      // final 5% holds the end frame
      preloadAt: 0.25 }         // defer bulk preload until underway
    /* add beats here; extend the wrapper height accordingly
       (~90–120svh of runway per footage story, ~70–90svh per graphic). */
  ];

  /* COPY beats — independent of media beats. in/out are progress
     windows; omit `in` for a layer visible at rest (the lead), omit
     `out` for one that stays to the end. rise = px drift while
     arriving (positive) / leaving (negative). A copy beat should
     clear BEFORE the next media dissolve begins. */
  var COPY = [
    { sel: '[data-hero-layer="lead"]', out: [0.00, 0.14], rise: -40 },
    { sel: '[data-hero-layer="s1"]',   in: [0.16, 0.38],
      out: [0.42, 0.48], rise: 40 },
    { sel: '[data-hero-layer="s2"]',   in: [0.60, 0.92], rise: 40 }
  ];

  var PRELOAD_STRIDE = 4;   // load every Nth frame, then backfill

  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  function clamp01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function range(p, w) { return w ? clamp01((p - w[0]) / (w[1] - w[0])) : 0; }

  /* ==========================================================
     Scroll-scrub frame sequence (canvas + preloaded WebP stills).
     NEVER video.currentTime — keyframe seeking is janky on mobile
     Safari. Manifest values come from data-* attributes, NOT fetch():
     fetch is blocked under file:// and the page must open standalone.
     ========================================================== */
  function createFrameSequence(canvas) {
    if (!canvas || !canvas.getContext) return null;
    var total = parseInt(canvas.getAttribute('data-scrub-frames'), 10);
    var base = canvas.getAttribute('data-scrub-base');
    var pattern = canvas.getAttribute('data-scrub-pattern') || 'frame-%04d.webp';
    if (!total || !base) return null;

    var ctx = canvas.getContext('2d');
    var frames = new Array(total);
    var exact = -1;   // index currently drawn, only when exact

    function src(i) {
      return base + pattern.replace('%04d', String(i + 1).padStart(4, '0'));
    }
    function load(i, cb) {
      if (frames[i]) { if (cb) cb(); return; }
      var img = new Image();
      img.onload = function () { frames[i] = img; if (cb) cb(); };
      img.src = src(i);
    }
    function nearestLoaded(i) {
      for (var d = 1; d < total; d++) {
        if (frames[i - d]) return frames[i - d];
        if (frames[i + d]) return frames[i + d];
      }
      return null;
    }
    function draw(i) {
      if (i === exact) return;
      var hit = frames[i];
      var img = hit || nearestLoaded(i);   // never blank while loading
      if (!img) return;
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      exact = hit ? i : -1;                // fallback doesn't lock in
    }
    function preload() {
      var order = [], i;
      for (i = 0; i < total; i += PRELOAD_STRIDE) order.push(i);
      for (i = 0; i < total; i++) if (i % PRELOAD_STRIDE) order.push(i);
      order.forEach(function (i) { load(i); });
    }
    return {
      draw: draw, load: load, preload: preload,
      indexFor: function (t) { return Math.round(t * (total - 1)); }
    };
  }

  /* Progress along the pinned stage: 0 when its top hits the viewport
     top, 1 when the sticky child has travelled the full runway.
     Denominator = the STICKY CHILD's height (cached), not
     window.innerHeight: both are sized in svh, which stays put when
     the mobile URL bar retracts — innerHeight does not. */
  function stageProgress(el, stickyH) {
    var rect = el.getBoundingClientRect();          // READ before writes
    var runway = el.offsetHeight - (stickyH || window.innerHeight);
    if (runway <= 0) return null;
    return clamp01(-rect.top / runway);
  }

  /* Scroll driver: passive, guarded by an actual scrollY change, and
     deliberately NOT requestAnimationFrame — rAF suspends in hidden/
     background/preview panes, freezing the scrub on frame 0. */
  function onScrollDrive(update, remeasure) {
    var lastY = -1;
    function tick() {
      var y = window.pageYOffset;
      if (y === lastY) return;
      lastY = y;
      update();
    }
    window.addEventListener('scroll', tick, { passive: true });
    window.addEventListener('resize', function () {
      if (remeasure) remeasure();
      lastY = -1;
      update();
    });
    if (remeasure) remeasure();
    update();
  }

  (function heroStage() {
    var stage = document.querySelector('[data-hero-stage]');
    if (!stage) return;
    var inner = stage.querySelector('.hero-stage__inner');
    if (!inner) return;

    /* Resolve MEDIA beats. Missing elements are skipped, so the same
       driver serves loop-only, graphic-only, stories-only, or the full
       chain — and swapping a graphic beat for a scrub beat is a config
       edit, not a rewrite. */
    var media = MEDIA.map(function (m) {
      var el = stage.querySelector(m.sel);
      if (!el) return null;
      var beat = { cfg: m, el: el };
      if (m.type === 'scrub') {
        beat.seq = createFrameSequence(el);
        beat.preloaded = false;
      }
      return beat;
    }).filter(Boolean);

    var video = null;
    media.forEach(function (b) { if (b.cfg.type === 'video') video = b.el; });

    /* No native `loop`: unless footage is confirmed seamless, a native
       loop can silently freeze on the last frame. Restarting on
       'ended' makes a non-seamless clip cut visibly — honest, and
       fixable in the footage rather than hidden in the player. */
    if (video) {
      video.addEventListener('ended', function () {
        video.currentTime = 0;
        var pr = video.play();
        if (pr && pr.catch) pr.catch(function () {});
      });
    }

    /* Reduced motion: the driver never runs. CSS has already collapsed
       the runway to a normal stacked document; the poster — or the
       graphic beat's rest state — stands as the finished hero. */
    if (reduced) { if (video) video.pause(); return; }

    /* Kick off first frames + eager preloads. Graphic beats need no
       preload: their shapes are already in the DOM. */
    media.forEach(function (b) {
      if (!b.seq) return;
      b.seq.load(0, function () { b.seq.draw(0); });
      if (!b.cfg.preloadAt) { b.seq.preload(); b.preloaded = true; }
    });

    /* Resolve COPY beats; scope .line queries to their OWN layer — a
       stage-wide query would smear all staggers together. */
    var copy = COPY.map(function (c) {
      var el = stage.querySelector(c.sel);
      if (!el) return null;
      return { cfg: c, el: el, lines: el.querySelectorAll('.line') };
    }).filter(Boolean);

    /* Fully-faded layers keep their links out of the tab order. */
    function setLayer(el, opacity, rise) {
      el.style.opacity = opacity;
      el.style.transform = 'translate3d(0,' + rise + 'px,0)';
      el.style.visibility = opacity <= 0.001 ? 'hidden' : 'visible';
    }
    function stagger(lines, p, w) {
      var span = (w[1] - w[0]) / Math.max(lines.length, 1);
      for (var i = 0; i < lines.length; i++) {
        var start = w[0] + i * span;
        var t = clamp01((p - start) / (span * 1.4));
        lines[i].style.opacity = t;
        lines[i].style.transform = 'translate3d(0,' + ((1 - t) * 24) + 'px,0)';
      }
    }

    var stickyH = 0;
    function measure() { stickyH = inner.offsetHeight; }

    onScrollDrive(function update() {
      var p = stageProgress(stage, stickyH);
      if (p === null) return;

      /* Media beats: opacity from the xfade window, internal state from
         the scrub window (holds automatically outside it — range
         clamps). A scrub beat draws a frame; a graphic beat publishes
         --beat-p and its own CSS moves the shapes. */
      var coverP = 0;   // opacity of the topmost fully-visible overlay
      media.forEach(function (b) {
        var type = b.cfg.type;
        if (type === 'video') return;
        /* A beat with NO xfade window is the BASE layer: the driver must
           never write its opacity. Driving it would resolve to 0 at rest
           (range() of an undefined window is 0), leaving the hero blank
           until the visitor scrolls — and blank is exactly what a no-JS or
           reduced-motion visitor would keep. CSS owns the base layer's
           opacity; the driver only owns the layers that fade IN over it. */
        if (b.cfg.xfade) {
          var fade = range(p, b.cfg.xfade);
          b.el.style.opacity = fade;
          if (fade >= 1) coverP = 1;
        }
        var t = range(p, b.cfg.scrub);
        if (type === 'graphic') {
          /* No transition may read this property — reverse scrubbing
             would lag behind the scroll. */
          b.el.style.setProperty('--beat-p', t.toFixed(4));
        } else if (b.seq) {
          b.seq.draw(b.seq.indexFor(t));
          if (!b.preloaded && b.cfg.preloadAt && p >= b.cfg.preloadAt) {
            b.preloaded = true;
            b.seq.preload();
          }
        }
      });

      copy.forEach(function (c) {
        var tIn = c.cfg.in ? range(p, c.cfg.in) : 1;
        var tOut = c.cfg.out ? range(p, c.cfg.out) : 0;
        var rise = c.cfg.in ? (1 - tIn) * c.cfg.rise : tOut * c.cfg.rise;
        setLayer(c.el, tIn * (1 - tOut), rise);
        if (c.cfg.in && tIn > 0 && tOut < 1) stagger(c.lines, p, c.cfg.in);
      });

      /* PER-BUILD EXTRAS go here, published as CSS custom properties
         with NO transitions (they'd lag the scroll). Examples from the
         reference build:
           inner.style.setProperty('--hero-scrim', ...)   scrim ramps
           inner.style.setProperty('--story-scrim', ...)  copy contrast
           inner.style.setProperty('--hero-focal-x', ...) portrait
             focal tracking, lerped per beat, continuous across seams */

      /* The loop is fully covered once an overlay is opaque — stop
         decoding it. Resume if the user scrolls back up. */
      if (video) {
        if (coverP >= 1) { if (!video.paused) video.pause(); }
        else if (video.paused && !video.ended) {
          var pr = video.play();
          if (pr && pr.catch) pr.catch(function () {});
        }
      }
    }, measure);
  })();

})();
