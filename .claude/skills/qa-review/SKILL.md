---
name: qa-review
description: Pre-delivery quality gate - automated checks script plus manual
  review checklist covering correctness, contracts compliance, links, copy
  placeholders, and cross-page consistency. Use via /qa in Phase 6 and in
  reduced form for retainer edits. Not for performance budgets
  (performance) or WCAG depth (accessibility).
metadata: {version: 1.3.0, category: qa, tier: A}
---
# QA Review

## Purpose
Nothing ships with broken links, leftover placeholders, contract
violations, or drifted shared markup.

## Inputs
output/ (pages, shared/, assets/), state files, system/contracts/.

## Outputs
Pass/fail per check in BUILD_STATE.md notes; fixes applied.

## Rules
1. Run scripts/check.py FIRST; it is authoritative for its checks
   (placeholders, broken local refs, missing alt, hardcoded colors,
   header/footer drift, TODOs, near-duplicate main content across pages
   — the site-architecture service+location matrix's main risk —
   missing/duplicate titles and descriptions, and title length vs the
   seo-technical rule 1a overflow ladder). Fix and re-run to clean.
1a. The script also FAILS on any `- [ ]` row still open under
   `## Fact confirmations (deferred from Phase 0)` in system/state/QUESTIONS.md.
   Phase 0 stopped blocking on those in v1.11.0, so this is where that
   debt is collected: every deferred fact must be confirmed or corrected
   before the site can ship. Do not tick a row on the operator's behalf.
2. Manual review after the script, in this order:
   a. Read every page top-to-bottom as the target visitor; flag copy that
      contradicts client.md.
   b. Verify every client fact against client.md (phone, hours, address,
      prices) character-by-character.
   c. Click-path test: every nav link, every CTA, form submits to the
      real Formspree endpoint, Calendly loads, map centers correctly.
   d. Resize pass: covered by the rendered /visual-qa audit (Phase 6
      step 2) - do not repeat it mentally; verify its PASS block exists
      in BUILD_STATE notes.
   e. Disable JS mentally: does every section still make sense
      (component-api rule 5)?
3. Any MEDIA_LOG row with status=generated but file missing from
   output/assets/, or asset in use without a log row: FAIL.
4. Criticals block phase 6. Cosmetic nits: fix if <5 min, else log to
   DECISIONS.md as accepted.

## Scripts
- scripts/check.py - run from repo root: python3 .claude/skills/qa-review/scripts/check.py

## Anti-patterns
- Marking QA done from memory of earlier state instead of re-running.

## Changelog
- 1.3.0 check.py: title/meta audit - FAIL on missing or duplicate
  title/description (closes the "qa should catch" gap seo-technical
  rule 6 named), WARN over 60/155 chars; entity-decoded before
  measuring so "&amp;" is not counted as 5 characters
- 1.2.0 check.py: near-duplicate <main> content check across pages
  (5-word shingle Jaccard, >50% overlap fails) - guards the
  service+location matrix (site-architecture rule 1c) against cloned
  pages
- 1.1.0 rule 1a: the script fails on deferred fact confirmations left open
  in QUESTIONS.md - this replaces the removed Phase 0 stop (v1.11.0)
- 1.0.0 initial
