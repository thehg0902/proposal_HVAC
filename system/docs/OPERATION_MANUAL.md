# Operation Manual — Presentation OS

Last updated: v2.0.0

## 1. Set up the template once

Fill `input/client.md` > Agency (agency name, prepared by, contact or
booking link, hosting plan, how I help, process / next step), commit,
push, and tick **Settings > Template repository** on GitHub. Every clone
then starts with those fields filled.

## 2. Start a prospect

1. "Use this template" on GitHub (or clone), name it for the prospect,
   open it in Claude Code.
2. Fill `input/client.md`: Business name, optional Palette / Fonts, one
   `### Creative N` block per creative (type, platform, aspect, headline,
   primary text, CTA), optional Demo website URL.
3. Drop the research PDF into `input/research/`. Screenshots and
   creative can come now or at Phase 4.
4. Run `/build`.

## 3. What each phase does

| phase | what happens | you |
|---|---|---|
| 0 intake | validates client.md, reads the research, lists empty WWP fields and media counts | only if blocked (no name / no research) |
| 1 content-map | maps the research onto the page sections in system/state/COPY_DRAFTS.md, every line source-tagged | - |
| 2 brand | palette -> logo colours -> niche default; writes tokens.css, checks contrast | - |
| 3 draft | builds the page with empty carousels and creative frames, runs /ingest, self-reviews at 3 widths | **review the draft**: reply with edits or "approve" |
| 4 media | waits for missing screenshots / creative | **drop files, run /ingest** |
| 5 polish | animation, phone polish, performance, accessibility | - |
| 6 qa | check script + visual QA + facts pass | fix what it lists, if anything |
| 7 deploy | asks how to ship | **pick (a) /deploy, (b) /package, (c) GitHub Pages** |

Empty research fields show as `[PLACEHOLDER: ...]` and a question in
`system/state/QUESTIONS.md`. Fill the research or client.md, or hide the
section (client.md > Sections > Hide). QA fails while any placeholder
remains.

## 4. Media rules

- Reviews: `input/reviews/<platform>/` (google/, yelp/, facebook/ ...).
- Competitors: `input/competitors/<competitor-name>/`.
- Optional `source.txt` with one URL in any of those subfolders: shown
  in the browser-frame address bar.
- Creative: `input/creative/creative-1.mp4`, `creative-2.png` ... matching
  the client.md blocks. Video is re-encoded (audio kept) with a poster.
- Logo: `input/assets-intake/logo.svg|png|jpg`. Demo-site screenshot:
  `input/assets-intake/website.png`.
- `/ingest` is safe to re-run; deleting a screenshot removes its slide.

## 5. Hosting

`/demo` once per clone (creates staging + deploy branches, pushes the
current page to staging). `/stage` after any edit. `/deploy` goes live
after QA and your explicit go. `/package` makes a zip in deliverables/.

## 6. Troubleshooting

- `python` opens the Microsoft Store: use `py -3` (commands already do).
- Research PDF over 10 pages will not read: install poppler, or
  `py -3 -m pip install pypdf`, or export the Notion page as Markdown &
  CSV into `input/research/`.
- A skill you need is manual-only: invoke it by name (`/seo-technical`).
  The full list with load mode is in `system/docs/REGISTRY.md`.
