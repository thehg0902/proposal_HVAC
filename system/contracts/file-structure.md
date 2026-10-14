# Contract: File Structure  (v4.0.0 - PresentationOS)

The pitch page is a STANDALONE deliverable: everything the browser needs
lives under `output/`. Delivery = the CONTENTS of output/ (deploy branch
via /deploy, or a zip via /package).

Repo shape:

    input/    what the operator fills in (client.md, research/, reviews/,
              competitors/, creative/, assets-intake/)
    system/   the OS: contracts/, state/, scripts/, docs/, preview/, archive/
    output/   THE DELIVERABLE - this contract governs everything below it
    root      CLAUDE.md + .claude/ (Claude Code loads project config only
              from the repo root) + README.md + UPDATE_LOG.md

`input/` and `system/` contain ZERO files the page needs. `output/`
contains ZERO OS files - both split scripts prove this on every run, and
`deliverables/` (the /package zips) stays at the repo root.

Canonical tree - ONE page:

output/
  index.html        the pitch page (the only page)
  style.css         section + component styles
  script.js         presentation layer, carousels, small enhancements
  robots.txt        "User-agent: *" + "Disallow: /" (pitch pages are private)
  shared/
    tokens.css      design tokens ONLY (design-tokens contract)
    base.css        reset, element defaults, print base
  assets/
    images/
      logo.(svg|png|webp)
      website.webp                      demo-site screenshot (optional)
      reviews/<platform>/NN.webp        written by /ingest
      competitors/<competitor>/NN.webp  written by /ingest
      creative-N.webp | creative-N-poster.webp
    video/
      creative-N.mp4                    h.264 + aac, faststart
    fonts/          self-hosted .woff2 only

Stylesheet link order (exactly): 1. shared/tokens.css  2. shared/base.css
3. style.css

Rules:
1. Kebab-case file and folder names. No spaces, no uppercase.
2. No build step, no framework, no bundler: plain HTML/CSS/JS. output/
   must open standalone - double-clicking output/index.html works with no
   server.
3. Every image/video referenced from HTML lives in output/assets/ (no
   hotlinks). /ingest is the only writer of assets/images/reviews/,
   assets/images/competitors/ and the creative files.
4. Every generated media asset (the operator's creative included) has a
   row in system/state/MEDIA_LOG.md (media-log contract).
5. External references: none, except the demo-site link and an
   agency booking/contact link from client.md.
6. Head of index.html: <title>, meta description, and
   `<meta name="robots" content="noindex, nofollow">`.
