---
name: client-enrichment
disable-model-invocation: true
description: Parse the raw Business Profile Paste in input/client.md into
  structured business facts and write them into the Auto section. Use at
  Phase 0 whenever the Paste section is non-empty or changes. Not for
  validating structure (intake-validation) or inventing missing facts
  (never).
metadata: {version: 1.2.1, category: process, tier: A}
---
# Client Enrichment

## Purpose
Turn an unstructured GBP/Maps/old-site paste into tagged, provenance-
tracked business facts so the operator types almost nothing by hand.
Paste only — no API keys, no scraping.

## Inputs
input/client.md (`## Business Profile Paste` section).

## Outputs
Regenerated `## Auto (generated — do not hand-edit)` section in
input/client.md; suggestion comments under `## Creative`; entries in
system/state/QUESTIONS.md (conflicts) and system/state/DECISIONS.md (detected niche).

## Rules
1. Extract into the Auto section, one fact per line, each tagged with
   provenance and status: `- phone: 905-xxx-xxxx  [paste][unconfirmed]`.
   Fields to look for: name, category/niche, phone, email, address,
   hours, services, website, socials, review quotes, years/history
   claims, service area. SKIP any fact a filled Overrides field already
   answers (Name, Phone, Years in business, Service area, ...) —
   Overrides outrank Auto (schema precedence), so parsing a weaker
   duplicate only creates confirmation noise.
1a. Service area: when the paste states more than one place served
   ("serving Markham, Richmond Hill, Vaughan" / a GBP service-area list),
   extract the FULL list as `/`-separated, matching the Overrides list
   syntax (client.schema.md): `- service area: Markham / Richmond Hill /
   Vaughan  [paste][unconfirmed]`. A single named city stays a single
   value. Never infer an area not literally named in the paste.
2. Extract ONLY what is literally present in the paste. No inference of
   facts — a review saying "fixed my AC fast" is NOT evidence of a
   "24/7 emergency" service. Unclear or conflicting items become one
   line each in system/state/QUESTIONS.md, never a guess.
3. Review quotes go under a `Testimonial candidates` subsection of Auto,
   verbatim with reviewer first name, each marked [needs-approval]. They
   enter the site only if the operator approves — Google reviews on a
   site should be client-confirmed.
4. Mine the paste + reviews for differentiator language and write up to
   3 one-line SUGGESTIONS under the Creative section as HTML comments
   (`<!-- suggested: known for same-day service -->`). Suggestions only —
   never auto-fill the operator's answers.
5. Idempotent: on every run, regenerate the WHOLE Auto section in place;
   never append a duplicate. Auto is machine-owned; hand edits belong in
   Overrides (which always outrank Auto).
6. The niche is OPERATOR-TYPED in client.md `## Niche` and always wins.
   Read the GBP category line only to COMPARE: agreement needs no note;
   disagreement is ONE line in system/state/DECISIONS.md
   (`niche-conflict | typed "<x>" vs GBP category "<y>" | using typed`) and
   never a question — owners mis-set their own GBP category constantly.
   Only when `## Niche` is blank do you detect from the category line, log
   it claude-proposed, and print the guess in the Phase 0 report so it is
   correctable in one word. Never write the niche into `## Niche` yourself.

## Anti-patterns
- Promoting a parsed fact straight into copy/HTML while [unconfirmed] —
  the confirmation table (Gate 1) or [PLACEHOLDER] rendering must apply.
- Editing the Overrides or Creative answers themselves.
- "Improving" review wording, merging reviews, or inventing attribution.

## Changelog
- 1.2.1 extract a `/`-list service area from the paste when more than one
  place served is named, matching Overrides list syntax; frontmatter
  version corrected to match this changelog (was stale at 1.1.0)
- 1.2.0 typed `## Niche` always beats GBP-category detection; disagreement
  is one logged line, never a question (v1.11.0)
- 1.1.0 skip facts already answered by filled Overrides fields (v1.4.0)
- 1.0.0 initial (v1.2.0 change order)
