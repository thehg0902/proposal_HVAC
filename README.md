# Presentation OS(V2.0.0) — Pitch Page Template

Builds ONE educational, single-page pitch for a prospect: their market,
what their customers say, what competitors do, the gap, how the customer
decides, the plan, and the proposed creative, plus a link to the demo
website you built in AgencyOS. You host it on your own server.

## Per-prospect workflow

1. **Clone** this template, rename it for the prospect, point origin at
   the prospect's repo.
2. **Fill `input/client.md`**: business name (required), brand palette
   (optional), one `### Creative N` block per creative, demo website URL
   (optional). The Agency section is filled once in the template.
3. **Drop files:**
   ```
   input/research/                 the WWP Structure research PDF (required)
   input/reviews/<platform>/       review screenshots (google/, yelp/ ...)
   input/competitors/<competitor>/ website + social screenshots
   input/creative/creative-N.*     the final video or poster
   input/assets-intake/logo.*      the prospect's logo (optional)
   input/assets-intake/website.*   demo-site screenshot (optional)
   ```
   Optional `source.txt` (one URL) in a reviews/competitors subfolder
   shows that address in the screenshot's browser frame.
4. **Run `/build`** in Claude Code at the repo root. It stops twice for
   you: review the draft (Phase 3), and drop any missing media + `/ingest`
   (Phase 4). Then `/qa`, then the deploy choice.
5. **Host:** `/demo` (first-time branch setup + staging push), `/stage`
   (preview subdomain), `/deploy` (live, after QA + your go), or
   `/package` (zip). `/save` backs everything up to main.

Brand: palette in client.md is used exactly; no palette = colours from
the logo; no logo = a default design for the niche.

## Repo shape

```
input/    what you fill in (client.md, research/, reviews/, competitors/, creative/, assets-intake/)
system/   the OS (contracts, state, scripts, docs, preview, archive)
output/   the pitch page: the only thing that ships
```

```
output/
  index.html  style.css  script.js  robots.txt
  shared/     tokens.css  base.css
  assets/     images/ (logo, reviews/, competitors/, creative)  video/  fonts/
```

Operator guide: `system/docs/OPERATION_MANUAL.md`. Architecture:
`system/docs/ARCHITECTURE.md`. Skill index: `system/docs/REGISTRY.md`
(regenerate with `py -3 system/scripts/generate-skill-registry.py`).
Maintenance: `/lint-os` before committing skill changes.

Windows note: scripts run with `py -3` (`python` / `python3` open the
Microsoft Store stub). Tools used: Pillow (images), ffmpeg (video). PDFs
over 10 pages need poppler or pypdf, or export the Notion page as Markdown.

Hooks load at session start; after editing them, restart the session.
