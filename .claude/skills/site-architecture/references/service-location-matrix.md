# Service × Location Page Matrix

Trigger (rule 1c): Service area lists 2+ places (client.schema.md list
syntax) and/or 3+ services have distinct search intent (rule 1's
threshold). Skip entirely for single-location, single/few-service
clients — the default stays fewer pages, stronger pages.

## Keyword source — exactly two states, never a third
1. Overrides `Target search terms` filled — a `/`-separated list. Use
   these exact phrases, one per generated page, in the order listed. A
   service/location combo with no matching phrase falls to (2).
2. Empty — the generic `[service] [location]` template (e.g. "AC repair
   Markham"), built from Services × Service area (Overrides or confirmed
   Auto only). Never invent a service or area not present in client.md.

market-research's KEYWORD CANDIDATE (RESEARCH BRIEF) is advisory only —
it exists so the operator can review and copy it into Target search
terms. Never read it here directly; a candidate the operator hasn't
adopted has no weight in the matrix.

## Build priority
Log the chosen page count and anything skipped as `claude-proposed` in
DECISIONS.md — never silently truncate.
1. All service pages (`output/<service-slug>/`)
2. All location pages (`output/<location-slug>/`)
3. Highest-value service+location combo pages
   (`output/<service-slug>-<location-slug>/`) until the target is reached

Default target: 30 indexed pages site-wide (including non-matrix pages).
Fewer is fine if Services × Service area doesn't reach it — never pad
with low-value combos just to hit the number. Folder naming follows the
existing flat, kebab-case convention in system/contracts/file-structure.md — no
new nesting.

## Per generated page
- 500–700 unique words (copywriting drafts the prose; this sets the
  target it writes to)
- One service+location keyword; title/H1 per seo-technical rule 1
- A real local detail from market-research's LOCAL DETAILS table when
  available (a landmark, neighbourhood, or corridor) — never generic
  filler ("proudly serving the area") standing in for a specific detail
- Never clone another matrix page's body copy — qa-review's check.py
  flags near-duplicate main-content across pages; treat a FAIL there as
  a rewrite instruction, not a threshold to game

## Internal linking (matrix pages)
- Home → every service page + every location page
- Each service page → 2–4 relevant location pages
- Each location page → 3–6 relevant services
- Max 8–10 internal links per page; no footer link-dumping
- Anchor text varied, never identical across links to the same target
  ("AC repair in Markham" / "our Markham AC repair service" / "AC
  technicians serving Markham")
