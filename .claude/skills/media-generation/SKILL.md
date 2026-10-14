---
name: media-generation
disable-model-invocation: true
description: Plan site media as a slot-named shopping list (operator
  generates in Higgsfield manually) or storyboard for paid auto-generation
  behind the human approval gate - all logged to MEDIA_LOG.md. Use in
  pipeline Phase 4 or whenever new media is needed. Not for
  optimizing/ingesting files (image-optimization, /ingest) or hero
  playback code (hero-media).
metadata: {version: 1.3.0, category: media, tier: C}
---
# Media Generation

## Purpose
Consistent, on-direction media at controlled credit cost, with a hard
human gate before any credit is spent.

## Inputs
Design direction imagery style (DECISIONS.md), client.md Photos section
(what exists vs what's needed), system/contracts/media-log.md.

## Outputs
input/assets-intake/slots/SHOPPING_LIST.md (the operator's worksheet)
+ mirrored rows (id = slot filename, status=planned) in system/state/MEDIA_LOG.md.
Assets arrive via /ingest (operator path) or, after human approval,
paid generation.

## Rules
1. HARD INVARIANT (CLAUDE.md): no paid generation without a MEDIA_LOG
   row whose storyboard-approved column reads YES. Two valid paths:
   the human types YES in the file, or the human approves the NAMED
   slot(s) in-chat ("approve hero-loop and gallery-01" / "approve
   all listed") and Claude transcribes `YES [in-chat <date>]` to
   exactly those rows. Claude never writes YES from inference,
   ambiguity, or blanket permission - when in doubt, ask again with
   the row names and estimated credits.
2. Shopping list first: for each needed asset write one
   SHOPPING_LIST.md block per system/contracts/asset-slots.md - exact slot
   filename, its `folder:` line, treatment, spec, and the FULL
   copy-paste generation prompt - plus a mirrored MEDIA_LOG row
   (id = slot filename, status=planned, model = operator until the
   human opts into auto-generation). CREATE the placement folders,
   named per THIS project's page/section map + niche
   (`Home - Hero coffee/`, `About us - Before and after/`, ... —
   every project's set differs; asset-slots contract). BEFORE writing
   prompts, sweep input/assets-intake/ (Phase 0 inventory): move
   matching client files into their placement folders under their slot
   names, pre-tick those blocks `[x]`, log rows as model=client /
   credits 0 — only the GAPS get prompts. Present the list, STOP.
2a. Default path is OPERATOR-GENERATED (credits 0, model=operator): the
   human generates in Higgsfield themselves, drops each file in its
   placement folder, ticks `[x]` on the list, runs /ingest. Slots left
   unticked with no file are Higgsfield candidates: /ingest lists them
   and Claude asks in-chat - named slots + estimated credits - and
   only generates what the operator explicitly approves (rule 1).
   Intro-loop pairs: write both slots; the loop's prompt must
   reference matching its intro's final frame.
2b. HERO STORY slots are an UPGRADE, never a default spend. When client.md
   `## Hero story` is written, Phase 2 already shipped it as a polygon
   graphic hero at zero cost. Write footage slots for it ONLY after the
   operator approved that graphic hero at the Phase 2 gate, name them after
   the same beats (`hero-beat-1`, `hero-beat-2`, ...) so the herostory
   config swaps layer types without touching its windows, and mark the
   block `upgrade - the graphic hero ships if you skip this`. An empty
   `## Hero story` means NO hero media slots at all: the colour-progression
   hero is complete as built, and inventing slots for it would manufacture
   a spend the design does not need.
3. Real client photos beat generated media - generate only what intake
   says is missing. Never generate fake team members, fake premises
   interiors presented as real, or fake review/before-after imagery.
   Overrides "Photos policy" (real-only | ai-allowed | mix) and "People
   in imagery" (yes | no) are hard constraints on the shopping list:
   real-only = no generation slots at all, only client-photo
   optimization; no people = no faces in any prompt.
4. Prompt consistency: one style block (built per the image-prompt section
   below, from the design direction) reused verbatim across all prompts
   for the site.
5. Video for hero per hero-media constraints (duration/weight targets
   inform the generation settings - see the video-prompt section below).
6. After generation (either path): files land in
   input/assets-intake/slots/ under their slot names; /ingest converts,
   places them under output/assets/, ticks the list, and flips MEDIA_LOG
   rows to in-use. Paid generations additionally record actual credits.
7. Budget per the credit-budgeting section below; nearing the cap ->
   stop and ask.

## Image prompt construction
Structure: [subject + action] + [environment matching the niche] +
[STYLE BLOCK] + [composition note] + [negative/avoid note]. The STYLE BLOCK
is written ONCE per site from the design direction (e.g. "warm natural
light, shallow depth of field, editorial photography, muted earthy palette,
no text, no watermarks") and pasted verbatim into every prompt for the
site - that verbatim reuse is what makes the set look like one shoot.
Composition: leave copy space where the layout needs it (hero: subject
off-centre toward the media side). Aspect ratios decided per layout BEFORE
generating and logged in the row - hero 16:9, cards 4:3 or 1:1.
Ethics: generated people are obviously ambient/lifestyle, never presented
as the actual staff; interiors are ambiance, not the actual premises,
unless the client approves the substitution in writing (QUESTIONS.md).

## Video prompt construction (hero clips)
Target 5-8s, one continuous motion, ending on a frame that works FROZEN -
hero playback freezes on the last frame, so prompt for a settling,
resolving final composition, never mid-action. Slow camera moves (push-in,
drift) freeze better than subject action. Same STYLE BLOCK as images.
Request the highest available resolution >= 1080p and re-encode per
hero-media's MP4 settings after download. One concept = one generation;
iterate on the prompt in the log (keeping rejected rows) rather than
burning credits on shotgun variants.

## Credit budgeting
Set a per-site credit cap at storyboard time (default proposal: planned
assets + 30% iteration margin) and write it at the top of the build's
MEDIA_LOG table. Track actual credits per row with a running total in the
footer. At 80% of cap: warn. At cap: stop, present spend vs plan, ask
before continuing. Video costs far more than images - storyboard images
first and confirm direction on cheap assets before any video generation.

## Anti-patterns
- "Client said generate whatever" as gate bypass (invariant holds);
  regenerating on taste without logging the rejected row.

## Changelog
- 1.3.0 image/video prompt construction + credit budgeting inlined from references/ (v1.13.0)
- 1.2.0 rule 2b: hero-story footage is an approved-only upgrade over the
  zero-cost polygon graphic hero; no hero story = no hero slots (v1.11.0)
- 1.1.0 shopping-list workflow: slot-named worksheet, operator-generated
  default path, /ingest handoff (v1.3.0)
- 1.0.0 initial (encodes the storyboard-approval workflow)
