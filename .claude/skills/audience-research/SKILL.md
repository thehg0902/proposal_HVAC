---
name: audience-research
description: Niche audience psychology library - personas, pains, desires,
  objections, decision triggers, and conversion implications for 11
  local-business niches. Use at Phase 1, and at Phase 3 when client.md's
  Target Audience is thin. Not visual direction (design-direction), live
  per-client research (market-research), or the doctrine
  (winners-writing-process).
metadata: {version: 1.1.1, category: process, tier: A}
---
# Audience Research

## Purpose
Conversion structure and copy grounded in who the visitor actually is
and what they fear/want - even when the operator pastes no research.
The studies are operator-authored (Studio Sol, Ontario market) and are
the niche-level default behind client.md's Target Audience section.

## Inputs
Detected niche (Phase 0, DECISIONS.md), client.md `## Target Audience`
(may be empty), references/<niche>.md.

## Outputs
A distilled AUDIENCE BRIEF (~12 lines) in system/state/DECISIONS.md, written
once at Phase 1 start; Phases 1-3 consume the brief. The master also
compresses it to a 6-line PRIOR DIGEST that the Phase 1 research fan-out
carries as a hypothesis to challenge - so the brief is a starting point for
live evidence, not the last word.

## Rules
1. Niche source: client.md `## Niche` when the operator typed one, else the
   category detected at Phase 0. Resolve it through the niche map
   (alias -> family -> conversion mode) and match ONE study. `adjacent`
   matches are honest and must be LABELLED as adjacent in the brief so later
   phases discount trade-specific detail.
1a. NO match: produce NO brief. Write `prior: none` and continue - a wrong
   study is worse than no study, because every later phase treats the brief
   as evidence about this audience. Log a `niche-gap` line instead.
2. Read the study ONCE, at Phase 1 start; distill the brief into
   DECISIONS.md: primary persona (one line), top 3 pains (their
   words), the deep desire, biggest motivator, decision trigger,
   objections to pre-answer, primary CTA + trust stack (study section
   9). Downstream phases use the BRIEF and never re-read the study
   (token economy - same pattern as vibe refs).
3. Precedence: client.md Target Audience is level 2; the study is a
   skill reference (level 7). When both exist, client-pasted facts WIN;
   the study supplies psychology depth underneath. Contradictions get
   one line in the brief, resolved toward the client's version.
4. Section 9 of every study ("Website Conversion Implications") is
   build-ready: architecture takes the CTA choice, dual-path/hero
   guidance, and trust-stack placement; copywriting takes headline
   angles and pain/desire phrasing verbatim-in-spirit.
5. The studies are Ontario-market research. Outside Ontario: keep the
   psychology (pains/desires travel), drop province-specific claims
   (WSIB, seasonality) unless the client's market matches.

## References
- references/roofing.md, electrician.md, garage-door-repair.md,
  paving.md, concrete-contractor.md, tree-service.md, home-builder.md,
  kitchen-bath-reno.md, med-spa.md, physiotherapy.md, chiropractor.md
  - identical 9-section format; section 9 is the build-notes payload.

## Anti-patterns
- Re-reading the full study at Phase 3 instead of using the brief.
- Copying study prose into site copy verbatim (it is research language,
  not customer-facing voice).
- Letting the study override client-pasted audience facts.
- Substituting a wrong study when the niche matches none (rule 1a).

## Changelog
- 1.1.1 description trimmed (v1.13.0)
- 1.1.0 niche from `## Niche` via the niche map; adjacent matches labelled;
  no match now yields NO brief rather than a wrong one; brief compressed to
  a PRIOR DIGEST for the research fan-out (v1.11.0)
- 1.0.0 initial (v1.7.0 - operator-supplied study library, 11 niches)
