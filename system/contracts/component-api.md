# Contract: Component API  (v2.0.0 - PresentationOS)

The pitch page is composed of sections (ids and order in
pitch-sections.md). Every section follows this shape:

<section class="section section--{id}" id="{id}" data-slide>
  <div class="container"> ... </div>
</section>

Rules:
1. Class naming: BEM-lite. Block `.card`, element `.card__title`,
   modifier `.card--featured`. No utility soup, no inline styles.
2. Every section is self-contained: removing its HTML block and its CSS
   block must not break other sections.
3. Interactive components expose behavior via data attributes, all
   initialized from output/script.js.
4. Everything renders acceptably with JS disabled (progressive
   enhancement): carousels degrade to a horizontally scrollable strip,
   the presentation layer simply disappears. Animation is additive.
5. Anchors (id=) are the section ids; never rename one without updating
   the section nav in the same edit.

## Components

| component        | markup hook                    | behavior |
|------------------|--------------------------------|----------|
| presentation     | `<body data-present>`          | Section dots nav + progress bar; Left/Right, PageUp/PageDown, Space, Home/End jump section to section (works with a slide clicker); never hijacks normal scrolling or touch. |
| cover            | `.cover`                       | Logo, "Prepared for {business}", one-breath target market line, prepared-by + date. |
| track-diagram    | `.tracks`                      | Two columns (Track 1 / Track 2) converging on an Opportunity box. |
| pain-desire      | `.pain-desire`                 | Two lists side by side: current state (pains) vs dream state (desires). |
| quote-list       | `.quotes`                      | Verbatim review quotes, good and bad visually distinct. |
| proof-carousel   | `[data-carousel="reviews\|competitors"]` | Slides are `figure.proof__slide`, each inside a browser-window frame (`.proof__bar` shows the source URL or label). Arrows, swipe, keyboard, "n of N" counter, lazy images. A count line above it ("23 screenshots from Google, Yelp") proves the research was done by hand. Content between ingest markers only. |
| card-grid        | `.cards`                       | Roadblocks / solutions tried / look-for vs distrust. |
| awareness-grid   | `.awareness`                   | 4x2 grid from pitch-sections fixed content; matching cell(s) get `.is-here`; platform chip. |
| competitor-cards | `.competitors`                 | One card per top player: what's working / what's missing. |
| gap-statement    | `.gap`                         | The page's climax: the gap in one large statement + the supporting priority comparison. |
| chain-steps      | `.chain`                       | Ordered steps from relaxed scroll to click, objections called out. |
| threshold-meters | `.meters`                      | Desire / Certainty / Trust bars, before -> after (x/10). |
| storyboard       | `.storyboard`                  | Timeline of time ranges: what's on screen + what the viewer should think. |
| creative-frame   | `.ad[data-platform][data-aspect]` | Generic social/search ad mock (avatar, name, "Sponsored", media at the given aspect, primary text, headline, CTA). No official platform logos. Media between `ingest:creative-N` markers; video is click-to-play (`preload="none"`, controls, playsinline). |
| device-frame     | `.device`                      | Laptop/phone frame with the demo-site screenshot + "Open the demo" button (target=_blank, rel=noopener). |
| agency-block     | `.agency`                      | How I help, process / next step, contact or booking link. |
| qa-list          | `.interview`                   | Question -> what it reveals (only when shown). |

Print: a print stylesheet lays each section on its own page so the
prospect can save the pitch as a PDF; carousels print as a grid.
