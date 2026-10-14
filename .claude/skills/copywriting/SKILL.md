---
name: copywriting
disable-model-invocation: true
description: Write all website copy for a local small business - headlines,
  section copy, CTAs, about pages - in the client's voice, conversion-first,
  locally grounded. Use in pipeline Phase 3 and for copy edits. Not for
  meta tags/schema (seo-technical) or marketing assets like ads, emails,
  and scripts (copy-frameworks, persuasion-mechanics).
metadata: {version: 1.5.0, category: content, tier: A}
---
# Copywriting

## Purpose
Copy that sounds like the specific business, addresses its specific
audience, and moves them to the page's one conversion action.

## Inputs
client.md (Creative answers, Overrides, confirmed Auto facts; legacy v1.1
sections for old repos), architecture in DECISIONS.md, niche playbook via
design-direction rationale.

## Outputs
Final copy written directly into the page HTML (never lorem ipsum).

## Rules
1. Every page has exactly one conversion action (from architecture);
   every section's copy points toward it. When client.md has a
   `## Target Audience` section, every CTA is written FOR that
   audience - their words for what they want, their objections
   pre-answered in the adjacent copy ("book a meeting" vs "order now"
   vs "call for same-day service" are different audiences, not
   interchangeable buttons).
2. NEVER invent facts: prices, years in business, certifications, "family
   owned", guarantees, review counts. Missing proof points ->
   [PLACEHOLDER: ...] + a question in system/state/QUESTIONS.md.
2b. Check the Overrides accuracy fields FIRST for proof points: Years in
   business / founded, Service area, Certifications / licenses, Price
   range, Payment methods, Emergency / after-hours. A filled field is a
   confirmed owner-typed fact - use it directly; these are the cheapest
   trust lines on the site.
2c. Write to the RESEARCH BRIEF and AUDIENCE BRIEF (DECISIONS.md): the
   research brief's `### Build directives` give the hero angle, the two
   registers to draft, the objection order, and the words-to-use /
   words-to-avoid lists; its verbatim phrase bank gives the audience's
   actual wording for pains and desires. Every CTA is phrased as the
   action THIS audience takes, objections pre-answered near the CTA.
   Research prose itself never ships verbatim - it is source, not voice -
   and a customer's quoted phrase is THE CUSTOMER's words, never restated
   as the business's own claim.
2d. DRAFT MODE (Phase 1, before any visual exists): write to
   system/preview/drafts/copy-<topic>.md, never into HTML, and draft only what
   is visual-independent - BOTH hero registers labelled A and B (unpicked),
   subhead, CTA labels, section H2s, objection block, trust lines, service
   blurbs, FAQ, about narrative, draft meta. When system/state/COPY_DRAFTS.md
   exists, Phase 3 is an EDIT pass: place the drafts, tighten to the built
   layout's word budgets, pick the register, re-run the claim audit against
   the final confirmed facts. Never re-draft from scratch; never ship a
   line the critic marked `block`.
2a. Voice sources in order: the Creative answers are PRIMARY;
   review-mined differentiator language (Auto suggestions) is secondary.
   Auto facts are usable in copy only when [confirmed] — an
   [unconfirmed] phone/address/hours/price renders as
   [PLACEHOLDER: value?] per rule 2.
3. Voice from Mood adjectives (Creative; Overrides may set them too):
   write 2 candidate hero headlines in different registers. The DRAFTING
   happens at Phase 1; the PICK happens at Phase 3 against the approved
   design rationale - a "quiet luxury" direction cannot carry a shouty
   headline, which is why the choice waits for the direction. Note the
   chosen register in DECISIONS.md and keep it consistent site-wide.
4. Local grounding: mention city/neighbourhood naturally in hero-adjacent
   copy and service copy (also serves local SEO) - never keyword-stuff.
5. Benefit before feature; reading level ~grade 7; sentences short;
   scannability over cleverness for trades, more voice allowed for
   food/lifestyle niches.
6. Testimonials: verbatim only, from client.md Overrides or from Auto
   "Testimonial candidates" the operator has APPROVED (never
   [needs-approval] ones); trimmed with [...] allowed, never rewritten
   or fabricated.

## Hero headline formulas (pick by visitor intent)
- Emergency / need-now (HVAC, plumbing, garage door): [Service] in [Area].
  [Speed or availability proof]. -> phone CTA
- Consideration (dental, physio, gym, reno): [Outcome] without [the common
  anxiety or objection]. -> book CTA
- Atmosphere (cafe, restaurant): an evocative fragment naming the
  experience and the place. -> menu / directions CTA
The subheadline carries the specifics the headline omitted (area served,
differentiator, offer) - never make the headline do both jobs. Test each
candidate with the anti-generic question: could a competitor paste this
unchanged? If yes, add the client's specific proof or place.

## CTA copy
Match the verb to the action: Call (tap-to-call, number visible in the
button on mobile), Book, Get a quote, See the menu, Get directions.
First-person converts in tests for consideration niches ("Book my visit").
Button copy is 2-4 words and starts with a verb. ONE primary CTA style per
page; the secondary is a text link, never a second button competing with
it. Repeat the primary CTA in the hero, after proof (testimonials), and at
the page bottom.

## Anti-patterns
- "Welcome to our website" openings; "we are passionate about" filler.
- Superlatives without proof ("best in Markham").

## Changelog
- 1.5.0 headline formulas + CTA copy inlined from references/ (v1.13.0)
- 1.4.0 draft mode at Phase 1 (visual-independent copy to
  system/preview/drafts/, both registers unpicked); research-brief build
  directives and verbatim phrase bank as sources; register picked at
  Phase 3; never ship a critic `block` (v1.11.0)
- 1.3.0 audience-brief-driven headlines/CTAs/objection copy (v1.7.0)
- 1.2.0 Overrides accuracy fields as primary proof-point source (v1.3.4)
- 1.1.0 v2 intake sources: Creative primary, confirmed-Auto-only facts,
  approved testimonial candidates
- 1.0.0 initial
