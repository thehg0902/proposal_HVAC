---
name: site-architecture
disable-model-invocation: true
description: Decide page map, navigation, and per-page section composition
  for a local small-business website. Use in pipeline Phase 1, or when
  adding/removing pages. Not for visual design (design-direction) or
  copy (copywriting).
metadata: {version: 1.5.0, category: process, tier: A}
---
# Site Architecture

## Purpose
Turn client.md Pages + Services + Audience into a concrete sitemap and a
section list per page that every later phase builds against.

## Inputs
input/client.md (Pages from Overrides if given; Services/Links from
Overrides or confirmed Auto; legacy v1.1 sections for old repos),
system/contracts/component-api.md

## Outputs
Sitemap + per-page section lists appended to system/state/DECISIONS.md.

## Rules
1. Pages source: Overrides when the owner specified pages (markup or
   list); otherwise propose the page map from the niche playbook —
   defaults below apply. Default for local businesses: fewer pages,
   stronger pages. If client listed only "Home", propose a single-page
   site with anchor nav
   (see "Single-page pattern" below). 5+ services with distinct search intent
   justify separate service pages (SEO), otherwise one Services page.
1a. If client.md Pages uses the markup syntax (pages separated by `/`,
   sections by `|` — see client.schema.md), that markup IS the
   authoritative page/section map. Never silently add or drop a
   user-specified page or section. The markup maps 1:1 to the
   file-structure contract layout: FIRST page group = output/ root
   (index.html), every other page group = its own folder
   (output/<page>/index.html).
1b. Compare the given sections against the niche playbook's
   `Must-have sections:` line (design-direction references). PROPOSE
   missing important ones as additions in system/state/QUESTIONS.md ("your niche
   usually needs X — add it? recommended yes"). If client.md Autonomy is
   `high`, default to including them, marked claude-proposed in
   DECISIONS.md, instead of asking.
1c. SEO page matrix (service+location pages, additive to rule 1). When
   Service area lists 2+ places (client.schema.md `/`-list syntax) and/or
   3+ services have distinct search intent, generate the service x
   location matrix per references/service-location-matrix.md. Keyword
   source, exactly two states, never a third: Overrides `Target search
   terms` filled -> use those exact phrases, one per page, in the order
   listed; empty -> the generic `[service] [location]` template built
   from Services x Service area. market-research's KEYWORD CANDIDATE is
   never read here directly - it is advisory only until the operator
   copies it into Target search terms. Single-location/few-service
   clients: skip the matrix entirely, rule 1's default (fewer pages,
   stronger pages) still governs.
2. Every page gets: purpose (one line), primary conversion action
   (call / book / form), ordered section list using standard names from
   system/contracts/component-api.md. Overrides "Primary action" (when filled)
   IS the site-wide default conversion action - never override it
   silently. When it is empty, the RESEARCH BRIEF's `### Build directives`
   in DECISIONS.md decide: primary conversion action, section-order
   consequence, objection order, and trust-stack order are BINDING there
   (they were derived from live evidence about this market). Below that:
   the `## Target Audience` section, then the Phase 1 AUDIENCE BRIEF.
   Tailor section ORDER to the audience's decision path - objections they
   hold get answered before the CTA that asks for commitment; the trust
   stack sits above the fold. "Target search terms" inform the
   service-page split (rule 1); "Languages" beyond one is a scope
   decision to log in DECISIONS.md before Phase 2.
3. Conversion action appears within the first viewport of every page and
   again at the bottom (cta section).
4. Nav: max 6 items; phone number always visible in header on mobile
   for call-first niches (HVAC, dental, restaurants).
5. Contact page exists whenever a physical address exists; embed map per
   maps-gbp skill flag.
6. Log the architecture in DECISIONS.md before proceeding - later phases
   treat it as level-3 precedence.

## Decision guide
| Situation | Approach |
|---|---|
| 1-3 services, walk-in business | Single page + anchors |
| Services with distinct search terms | one folder page each, /<service>/ |
| 2+ service areas listed | Rule 1c matrix - references/service-location-matrix.md |
| Client insists on many thin pages | Push back once in QUESTIONS.md with SEO reasoning, then obey |

## Single-page pattern
Default section order: hero, services, about, testimonials (if any),
gallery (if photos), faq (if provided), cta, contact + map, footer. Nav is
anchor links to section ids, active state via IntersectionObserver, smooth
scroll with a reduced-motion instant-jump fallback. Every anchor id is a
stable contract (component-api rule 6). Mobile nav: hamburger only above 5
items, otherwise inline condensed.

## Multi-page pattern
Header and footer markup is IDENTICAL on every page - static hosting, no
build step, so no JS includes. Keep the canonical copy in the root
index.html and propagate to every page in the same commit (check.py flags
drift). URLs are clean folder URLs per the file-structure contract:
`/about/`, `/ac-repair/`, each served by its own index.html - never
`/about.html`. Service page shape: specific hero, problem/solution copy,
proof, faq, cta. Breadcrumbs only when the site is 2+ levels deep.

## References
- references/service-location-matrix.md - rule 1c: keyword source, build
  priority, per-page requirements, internal linking

## Anti-patterns
- Blog scaffolding for clients with no content plan.
- Deep nav hierarchies for a 6-page site.
- Reading market-research's KEYWORD CANDIDATE directly into the matrix -
  it is advisory only until it reaches Target search terms.
- Padding the matrix with low-value combo pages to hit the 30-page target.

## Changelog
- 1.5.0 single-page and multi-page patterns inlined; corrected the stale `/about.html` URL guidance to the contract's clean folder URLs (v1.13.0)
- 1.4.0 rule 1c: service x location page matrix, gated on 2+ service
  areas or 3+ distinct-intent services, keyword source is Target search
  terms or the generic template (never market-research's candidate
  directly) - new references/service-location-matrix.md
- 1.3.0 RESEARCH BRIEF build directives outrank the audience brief for
  conversion action, section order, objections, trust stack (v1.11.0)
- 1.2.0 v2 intake sources: Pages from Overrides, else niche-playbook
  proposal (unchanged v1.1 behavior, new source location)
- 1.1.0 pages+sections markup is authoritative; niche must-have proposals
- 1.0.0 initial
