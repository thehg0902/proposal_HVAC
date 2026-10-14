---
name: design-direction
description: Translate client mood adjectives + niche into a concrete visual
  direction (style, imagery, layout personality) before any tokens or code.
  Use in pipeline Phase 2 before design-tokens. Not for producing CSS
  (design-tokens does that).
metadata: {version: 1.4.0, category: design, tier: A}
---
# Design Direction

## Purpose
Prevent generic template-looking output by committing to a specific,
client-appropriate visual direction and writing it down before building.

## Inputs
input/client.md (Mood from Creative; the Vibe section; niche from
Overrides if specified, else Auto's detected category; Brand/Style
references from Overrides; legacy v1.1 sections for old repos), vibe
reference images in input/assets-intake/vibe/, niche playbook in
references/.

## Outputs
A 10-line design rationale in system/state/DECISIONS.md: direction name, type
pairing intent, color intent, imagery style, layout personality, motion
level.

## Rules
1. Read ONE block of references/niche-playbooks.md first - the block the
   niche-resolution line named, not the file; it encodes what converts for
   that business type. Niche source: client.md `## Niche` when the operator
   typed one, else the category detected at Phase 0 - both resolved through
   the niche map at Phase 0 and recorded in the niche-resolution line.
   No block for the niche: take the one matching the CONVERSION MODE
   (call-first -> hvac, book-first -> dental, browse-first -> restaurant,
   membership -> gym, visit/experience -> coffee-shop) and note the
   adaptation in DECISIONS.md - the audience
   brief's emotional register (fear-relief vs aspiration vs trust) steers
   how far to bend it.
2. Mood adjectives (the Creative section's Mood line) are the brief. "Warm, premium, trustworthy" and
   "bold, energetic, young" must produce visibly different sites. Name
   the direction (e.g. "quiet luxury", "craft workshop", "clinical calm").
3. Client brand colors (if given) are constraints, not the whole palette -
   design-tokens expands them into the full token set. Same for the
   Overrides hard constraints: "Brand fonts" (use them, don't propose),
   "Color mode" (light | dark | either - decides the base scheme), and
   "Avoid (visual)" (negative constraints outrank any playbook or Vibe
   suggestion).
4. Decide imagery style here (photo-real warm / editorial / illustrative)
   so media-generation prompts stay consistent.
5. Pick ONE distinctive element per site (typography scale, unusual hero
   treatment, signature section shape). One, not five.
5a. Commit to a NAMED HERO CONCEPT every build - no site ships a default
   hero. Resolution order: Overrides `hero-media` if set, else client.md
   `## Hero story` if written (-> a polygon/SVG graphic hero, beats broken
   from the sentence, staged per herostory; zero media spend), else a
   solid-colour hero carried by the section colour progression (rule 5b).
   Name it in the rationale ("polygon drive-home, three beats"), and show
   it in the Phase 2 layout preview - the operator approves the hero
   concept at the same gate as the direction, not at Phase 5.
5b. Every build gets a SECTION COLOUR PROGRESSION: an ordered set of
   section colours that the page background blends between on scroll, so
   moving down the page reads as one continuous journey and each section
   change is felt rather than announced. This is the site-wide custom-feel
   device and the default hero backdrop when there is no hero story.
   design-tokens emits the sequence; frontend-animation drives the blend.
5c. ANTI-GENERIC TEST, applied to the rationale before the gate: could a
   competitor in this niche paste this direction unchanged onto their own
   site? If yes, it is not a direction yet - name what is unrepeatable
   here (this business's story, its actual materials, its town, its hero
   story) and make that the distinctive element. The Phase 2 pre-gate
   reviewer is prompted with this same question.
6. Motion level (none / subtle / expressive) must match both mood and the
   Stack animation flag; conflict goes to QUESTIONS.md.
7. Vibe references (client.md ## Vibe + images in
   input/assets-intake/vibe/): view each image ONCE, here at Phase 2,
   and distill what to take from each into the rationale as NAMED
   elements ("glassy pill nav", "serif-italic display over dark video" -
   never "looks nice"). The rationale is the artifact: never re-read the
   images in later phases (token economy). Vibe is part of client.md
   (precedence level 2): it outranks playbook aesthetics; playbook
   conversion must-haves still apply. Inspiration, never duplication -
   no wholesale copying of a reference's layout.

## References
- references/niche-playbooks.md - 16 niches, one block each (converts on /
  direction / hero / must-have sections / avoid). Read ONE block. The 11
  blocks that have a matching audience study are distilled from that
  study's section 9, so the two never disagree.

## Anti-patterns
- A direction a competitor in the same niche could paste unchanged (5c).
- Shipping a hero with no named concept, or discovering the hero at
  Phase 5 instead of committing to it at the Phase 2 gate.
- Defaulting to the same palette/typeface across clients.
- Trend-chasing that fights the niche playbook (brutalism for a dentist).

## Changelog
- 1.4.0 references/niche-playbooks.md: 16 playbook blocks in one file, 11 of them distilled from the matching audience study's section 9 - closes the gap where 11 studies had no matching visual playbook (v1.13.0)
- 1.3.0 named hero concept every build (hero story -> polygon graphic hero,
  else colour-progression hero), section colour progression as the
  custom-feel device, anti-generic test as a gate criterion, niche from
  `## Niche` with conversion-mode playbook fallback (v1.11.0)
- 1.2.0 vibe references: view once, distill to named elements (v1.3.1)
- 1.1.0 v2 intake sources: Mood from Creative, niche from detected
  category when Overrides silent
- 1.0.0 initial
