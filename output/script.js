/* script.js - presentation layer (thermometer nav + keyboard), section
   colour progression backdrop, proof carousels. Progressive enhancement:
   without JS every section paints its own step and carousels scroll. */
(function () {
  "use strict";
  var root = document.documentElement;
  root.classList.add("js");

  /* ---------- Section colour progression ---------- */
  function parseHex(v) {
    var h = (v || "").trim().replace("#", "");
    if (h.length === 3) h = h.replace(/(.)/g, "$1$1");
    if (!/^[0-9a-f]{6}$/i.test(h)) return null;
    return [0, 2, 4].map(function (i) { return parseInt(h.slice(i, i + 2), 16); });
  }

  function initBackdrop(slides) {
    var styles = getComputedStyle(root);
    var stops = slides.map(function (s) {
      return parseHex(styles.getPropertyValue("--section-bg-" + s.getAttribute("data-step")));
    });
    if (stops.some(function (c, i) { return !c && !slides[i].classList.contains("section--gap"); })) return null;
    root.classList.add("has-backdrop");
    return function update(mid) {
      var i = 0;
      while (i < slides.length - 1 && slides[i + 1].offsetTop + slides[i + 1].offsetHeight / 2 <= mid) i++;
      var a = stops[i] || stops[i - 1] || stops[i + 1];
      var nextIdx = Math.min(i + 1, slides.length - 1);
      var b = stops[nextIdx] || a;
      var c0 = slides[i].offsetTop + slides[i].offsetHeight / 2;
      var c1 = slides[nextIdx].offsetTop + slides[nextIdx].offsetHeight / 2;
      var t = c1 > c0 ? Math.min(Math.max((mid - c0) / (c1 - c0), 0), 1) : 0;
      var mix = a.map(function (v, k) { return Math.round(v + (b[k] - v) * t); });
      root.style.setProperty("--page-bg-blend", "rgb(" + mix.join(" ") + ")");
    };
  }

  /* ---------- Presentation layer ---------- */
  function initPresentation() {
    if (!document.body.hasAttribute("data-present")) return;
    var slides = Array.prototype.slice.call(document.querySelectorAll("[data-slide]"));
    if (!slides.length) return;
    var cover = document.querySelector("[data-present-cover]");
    var dots = Array.prototype.slice.call(document.querySelectorAll(".present__dot"));
    var blend = initBackdrop(slides);
    var current = -1;
    var ticking = false;

    function indexAt(mid) {
      var idx = 0;
      slides.forEach(function (s, i) { if (s.offsetTop <= mid) idx = i; });
      return idx;
    }

    function render() {
      ticking = false;
      var y = window.scrollY;
      var mid = y + window.innerHeight / 2;
      var max = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1);
      if (cover) cover.style.setProperty("--progress", Math.min(y / max, 1).toFixed(4));
      if (blend) blend(mid);
      var idx = y >= max - 2 ? slides.length - 1 : indexAt(mid);
      if (idx !== current) {
        current = idx;
        dots.forEach(function (d, i) {
          if (i === idx) d.setAttribute("aria-current", "true");
          else d.removeAttribute("aria-current");
        });
      }
    }

    function onScroll() {
      if (!ticking) { ticking = true; window.requestAnimationFrame(render); }
    }

    function go(i) {
      var target = slides[Math.max(0, Math.min(i, slides.length - 1))];
      target.scrollIntoView({ block: "start" });
    }

    /* Clicker paging: inside a section taller than the screen, page by
       most of a screen until its bottom is visible, then jump. */
    function step(dir) {
      var i = Math.max(current, 0);
      var s = slides[i];
      var top = s.offsetTop, bottom = top + s.offsetHeight;
      var y = window.scrollY, h = window.innerHeight, page = Math.round(h * 0.85);
      if (dir > 0 && bottom > y + h + 2) window.scrollTo({ top: Math.min(y + page, bottom - h) });
      else if (dir < 0 && top < y - 2) window.scrollTo({ top: Math.max(top, y - page) });
      else go(i + dir);
    }

    document.addEventListener("keydown", function (e) {
      if (e.defaultPrevented || e.altKey || e.ctrlKey || e.metaKey) return;
      var t = e.target;
      if (t && t.closest && t.closest("input, textarea, select, button, video, [contenteditable], [data-carousel]")) return;
      var k = e.key;
      if (k === "ArrowRight" || k === "PageDown" || (k === " " && !e.shiftKey)) { e.preventDefault(); step(1); }
      else if (k === "ArrowLeft" || k === "PageUp" || (k === " " && e.shiftKey)) { e.preventDefault(); step(-1); }
      else if (k === "Home") { e.preventDefault(); go(0); }
      else if (k === "End") { e.preventDefault(); go(slides.length - 1); }
    });

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    render();
  }

  /* ---------- Proof carousels ---------- */
  function initCarousel(el) {
    var track = el.querySelector("[data-carousel-track]");
    var controls = el.querySelector("[data-carousel-controls]");
    if (!track || !controls) return;
    var slides = track.querySelectorAll(".proof__slide");
    if (!slides.length) return;
    var prev = el.querySelector("[data-carousel-prev]");
    var next = el.querySelector("[data-carousel-next]");
    var counter = el.querySelector("[data-carousel-counter]");
    var at = 0;
    controls.hidden = false;
    track.setAttribute("tabindex", "0");

    function update() {
      var left = track.scrollLeft;
      var best = 0;
      Array.prototype.forEach.call(slides, function (s, i) {
        if (Math.abs(s.offsetLeft - track.offsetLeft - left) < Math.abs(slides[best].offsetLeft - track.offsetLeft - left)) best = i;
      });
      if (left >= track.scrollWidth - track.clientWidth - 1) best = slides.length - 1;
      at = best;
      if (counter) counter.textContent = (at + 1) + " of " + slides.length;
      if (prev) prev.disabled = at === 0;
      if (next) next.disabled = at === slides.length - 1;
    }
    function show(i) {
      var s = slides[Math.max(0, Math.min(i, slides.length - 1))];
      track.scrollTo({ left: s.offsetLeft - track.offsetLeft });
    }
    if (prev) prev.addEventListener("click", function () { show(at - 1); });
    if (next) next.addEventListener("click", function () { show(at + 1); });
    el.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); show(at + 1); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); show(at - 1); }
    });
    var pending = false;
    track.addEventListener("scroll", function () {
      if (!pending) { pending = true; window.requestAnimationFrame(function () { pending = false; update(); }); }
    }, { passive: true });
    update();
  }

  function init() {
    initPresentation();
    Array.prototype.forEach.call(document.querySelectorAll("[data-carousel]"), initCarousel);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
