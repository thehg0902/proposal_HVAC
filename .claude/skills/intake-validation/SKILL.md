---
name: intake-validation
disable-model-invocation: true
description: Validate input/client.md against input/client.schema.md and
  turn every gap into a client question. Use at the start of every build
  (pipeline Phase 0) or whenever client.md changes. Not for validating
  code or site output (see qa-review) or parsing the Business Profile
  Paste (client-enrichment).
metadata: {version: 1.1.0, category: process, tier: A}
---
# Intake Validation

## Purpose
Convert an incomplete client brief into either a green light or a precise
confirmation/question list, so no phase ever runs on invented facts.

## Inputs
input/client.md, input/client.schema.md

## Outputs
Confirmation table in chat (Gate 1); system/state/QUESTIONS.md entries; phase 0
status in system/state/BUILD_STATE.md.

## Rules
1. Phase 0 order: if the Business Profile Paste is non-empty, enrichment
   runs first (Auto section written), THEN
   `python3 system/scripts/validate-client-md.py`. The validator is
   authoritative: in v2 the only BLOCKER is "no business name found
   anywhere"; everything else is SOFT. v1.1-format files validate under
   the old required-sections rules.
2. Fact confirmations are DEFERRED, not gated. Write one `- [ ]` row per
   [unconfirmed] Auto fact (field | value | source) under the exact heading
   `## Fact confirmations (deferred from Phase 0)` in system/state/QUESTIONS.md,
   then CONTINUE — never stop for a reply. The operator answers any time
   before /qa; corrections go to Overrides, confirmations flip the tag to
   [confirmed] and tick the box. Nothing in phases 1-3 (research,
   architecture, copy drafting) needs an exact phone number, so holding the
   pipeline for one is pure round-trip tax.
   EXCEPTION: client.md `Autonomy: low` restores the old blocking in-chat
   table (one compact table, operator replies once).
3. Write to system/state/QUESTIONS.md only what the table cannot resolve:
   genuine ambiguities, conflicts found in the paste, and creative gaps.
   Phrase each for a non-technical business owner. Bad: "Provide brand
   guidelines." Good: "Do you have exact brand colors (hex codes)? If
   not, reply 'propose' and I'll design a palette."
4. BLOCKER (no name anywhere): mark phase 0 blocked and stop. SOFT gaps:
   proceed. Deferring confirmations moves the risk to the QA gate, which is
   script-enforced rather than attention-enforced — a strictly stronger
   place than a chat prompt. Facts still [unconfirmed] may drive drafts, but
   phone/address/hours/prices ship as [PLACEHOLDER: value?] in HTML, and
   qa-review's script fails BOTH on placeholders AND on any row still open
   under the deferred-facts heading. Nothing unverified reaches deploy.
5. Empty Creative section: SOFT note listing which creative questions
   would most improve the result for the detected niche, then proceed on
   niche-playbook defaults.
6. Sanity-check consistency: pages listed vs services described, booking
   flag vs booking link, logo path actually exists in assets-intake,
   Overrides contradicting Auto (Overrides win — note it in the table).
   Inconsistencies are table rows or questions, not silent fixes.
6a. ASSET INVENTORY (v1.6.0): list every file in input/assets-intake/
   (root and subfolders, excluding slots/ and vibe/), classify by
   filename convention (logo*, hero1/2*, gallery1/2*, team*, menu*,
   before*/after* ...), and record the inventory in the Phase 0 notes /
   Photos context. Phase 4 consumes it: matching files are assigned to
   slots and pre-ticked so only genuine gaps reach the shopping list.
7. Free-text or `placeholder` Stack values are NOT blocking questions:
   write a short recommendation into system/state/DECISIONS.md (what will be
   built, what it is ready to accept later), marked claude-proposed, and
   proceed. Ask in QUESTIONS.md only when intent is genuinely ambiguous.

## Anti-patterns
- Filling a missing phone/address/price from the web without logging it.
  Facts enter ONLY via Overrides (owner-typed) or the Paste→Auto flow
  with its confirmation gate — never straight into the site.
- Asking vague or compound questions; re-asking facts already sitting
  [unconfirmed] in Auto instead of putting them in the table.

## Changelog
- 1.2.0 fact confirmations deferred to a non-blocking QUESTIONS.md ledger
  enforced by the QA script; blocking table only at Autonomy: low (v1.11.0)
- 1.1.0 v2 intake: enrichment-first order, Gate 1 confirmation table,
  name-only blocker, unconfirmed→placeholder ship rule
- 1.0.0 initial
