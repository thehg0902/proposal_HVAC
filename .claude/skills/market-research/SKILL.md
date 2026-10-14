---
name: market-research
description: Automated per-client market research - a governed fan-out of
  parallel agents covering top players, verbatim review language, search
  intent, and the client's own proof, synthesized into one
  provenance-tagged RESEARCH BRIEF. Use at Phase 1 after the audience
  brief. Not the cached niche library (audience-research) or drafting the
  copy (copywriting).
metadata: {version: 1.1.1, category: process, tier: A}
---
# Market Research

## Purpose
Turn a niche plus a business paste into evidence about THIS market: what the
top players promise, the exact words customers use, what people actually
search, and what proof the client can and cannot back. One fixed-shape brief
that Phases 1-3 build against, with every line carrying the strength of its
evidence so nothing unverified can become a claim about the business.

## Inputs
system/state/DECISIONS.md (the AUDIENCE BRIEF prior and the niche-resolution line),
input/client.md (`## Business Profile Paste`, `## Niche`,
`## Special requests`, `## Creative`, `## Overrides`, `## Auto`),
WebSearch/WebFetch when available, references/niche-map.md,
references/agent-briefs.md, references/brief-template.md.

## Outputs
One `## RESEARCH BRIEF` block appended to system/state/DECISIONS.md (fixed shape,
see references/brief-template.md). Optional entries in system/state/QUESTIONS.md
(missing proof, minimum-facts block, niche gaps). Nothing is written to
output/.

## Automation boundary (read once, obey always)
Agents may RETRIEVE and CLUSTER language that is already public. Agents may
not decide what is true about this business. Only material tagged `[client]`
may ever become a published claim; everything else steers angle, order,
emphasis, and vocabulary. Absence of evidence produces an omitted section
and a `not-found:` line - never filler.

## Rules
1. Preconditions. Run only after the niche-resolution line and the AUDIENCE
   BRIEF exist in DECISIONS.md. Compress that brief to a 6-line PRIOR DIGEST
   and inject it into every agent brief with the instruction "confirm,
   refine, or contradict this with evidence" - agents challenge the prior,
   they never rediscover it.
2. Fan-out shape. Exactly FOUR research agents, dispatched in ONE message so
   they run in parallel, each in an isolated context, each read-only (no
   lease). The master does no research itself: it writes briefs, waits,
   synthesizes. Raw agent output is consumed and discarded; only the brief
   persists.
3. Agent 1 - TOP PLAYERS. Identify 3-5 businesses ranking for the niche plus
   city. Per player return: hero promise, primary CTA, trust stack, offer or
   guarantee, price transparency (yes/no/ranges), dual-path hero (yes/no),
   one notable omission, and review count where shown (Maps/GBP listing).
   Then three synthesis lines: TABLE STAKES (what all of them do), GAP
   (what none of them do), and KEYWORD CANDIDATE — propose one target
   keyword in service+city form (`[niche] [city]` or `[service] [city]`)
   and a difficulty tier from the average review count across players
   returned (avg <50 reviews = easy, 50-500 = medium/sweet spot, >500 =
   hard). No review counts found: omit the tier, keep the keyword
   proposal, tag `[model]`. Max 5 players, max 2 pages fetched per player.
4. Agent 2 - VERBATIM LANGUAGE. Mine customer wording from public reviews of
   competitors AND from any reviews inside the client paste. Read 5-star AND
   1-star: praise gives delight triggers, complaints give objections. Return
   12-20 VERBATIM phrases, never paraphrased, never merged, never cleaned
   up, sorted into PAINS / DESIRES / OBJECTIONS / DELIGHT TRIGGERS, each
   with source and star rating. A phrase you cannot quote exactly does not
   go in.
5. Agent 3 - SEARCH INTENT. Return query clusters real buyers type, each
   labelled with intent (emergency / planned / price-shopping / comparison /
   reassurance), plus the recurring questions people ask and the local
   modifiers in use. Each cluster names the page or section that should
   answer it. No volume estimates unless a source states one. Also return
   LOCAL DETAILS: one named landmark, neighbourhood, or corridor per
   service area in client.md's Service area list (Overrides or Auto),
   found in local search results or competitor location pages — never
   invented. Fewer service areas than found details: return only what
   evidence supports; a service area with nothing found gets a
   `not-found:` line, not a guess.
6. Agent 4 - OFFER AND PROOF. Client-side only: reads client.md and nothing
   else, so it ALWAYS runs even with no web access. Returns the service and
   package list, the guarantee or risk-reversal if one exists, PROOF WE HAVE
   (facts the client can back today), and PROOF WE LACK (every trust element
   the niche expects that client.md does not supply).
7. Return contract. Every agent returns ONLY the report block from
   system/contracts/agent-protocol.md section 3, with its own findings, no
   preamble, no reasoning narration, every line carrying an evidence tag.
   Nothing found for a subsection: emit `not-found: <what> <why>` and omit
   the subsection. Inventing a plausible-looking row is the single worst
   failure mode in this skill.
8. Evidence tags. Exactly five, on every line:
   `[client]` from client.md - the ONLY tag that may become a published
   claim about the business.
   `[prior]` from the niche study library - psychology, never a claim about
   this business.
   `[web:verified]` retrieved from a named source AND corroborated by a
   second independent source; record both.
   `[web:unverified]` single-source or paraphrased - hypothesis only.
   `[model]` Claude's inference, no source - structure only, never within
   reach of a fact.
   Any number, price, guarantee, credential, award, review count, or
   superlative that is not `[client]` becomes `[PLACEHOLDER: ...]` plus a
   system/state/QUESTIONS.md line. Verbatim customer phrases may be used as THE
   CUSTOMER'S words; never restated as the business's claim.
9. Synthesis. Write the brief in the fixed shape of
   references/brief-template.md, in this conflict order: `[client]` beats
   `[web:verified]` beats `[prior]` beats `[web:unverified]` beats
   `[model]`. A genuine `[client]`-vs-`[web:verified]` conflict gets one
   line in the brief and is resolved toward the client. Target 70 lines or
   fewer: this brief is re-read by three later phases. The KEYWORD
   CANDIDATE is always a proposal, never a fact: client.md's Overrides
   `Target search terms:` (when filled) outranks it outright — write the
   candidate anyway for visibility, marked superseded, rather than
   omitting it.
10. Degradation. No WebSearch/WebFetch: agents 1-3 do not run as designed -
    agent 1 falls back to the study's competitive content plus any Overrides
    `Competitors:` and OMITS the player table AND the keyword-difficulty
    tier (a bare niche+city keyword proposal may still be stated, tagged
    `[model]`); agent 2 mines only reviews inside the paste; agent 3 falls
    back to the study plus Overrides `Target search terms`, omitting the
    map and LOCAL DETAILS if both are empty; agent 4 is unaffected. Stamp
    `evidence: prior+client only`. Thin paste (fewer than
    six hard client facts): continue, and write ONE consolidated question
    block titled "Minimum facts for a non-generic site" listing the 6-8
    facts that would most change the output. No prior (niche matched no
    study): double agent 2's minimum phrase count; if web is also
    unavailable, stamp `evidence: client-only`, tag every diagnosis line
    `[model]`, and say so in the brief's Human check.
11. Human check. End every brief with 3-5 unticked boxes naming the
    highest-leverage lines to eyeball, each with its source. This is
    non-blocking and never becomes a gate - it exists so the operator can
    audit the machine's reading in five minutes.
12. Critic pass (agent 5, after drafts exist). Give it ONLY the drafts,
    client.md facts, and this brief. It returns FINDINGS, never rewrites,
    numbered, each `block | fix | nit`, across four audits: CLAIM (every
    asserted fact traced to a `[client]` source, else rewritten as a
    placeholder plus a question), PLACEHOLDER (every placeholder has a
    matching question and reads as a question, not a hole), TONE (against
    the Mood adjectives, the "Never say / avoid" line, and the brief's
    words-to-avoid), AUDIENCE (every CTA is the action THIS audience takes,
    objections appear before the ask, reading level around grade 7). The
    master applies `block` and `fix`; `nit` goes to DECISIONS.md as
    accepted.
13. Idempotent. Re-running regenerates the brief IN PLACE under the same
    heading. Never append a second brief; never leave two.
14. Budget and conduct. Max 5 agents per build (4 research + 1 critic), max
    5 sources per agent, no paid APIs, no scraping behind a login or a
    bot-check, no personal data collected about individuals. The client's
    own facts arrive by paste only.

## Decision guide
| Situation | Approach |
|---|---|
| Web available, study exists | Full 4-agent fan-out; `evidence: web+prior+client` |
| No web access | Agent 4 only + prior; omit player table and intent map; stamp `prior+client only` |
| Study exists but market is unusual | Run the fan-out; contradictions of the prior are the most valuable output - log them |
| No study, no web | Agent 4 only; `evidence: client-only`; every diagnosis line `[model]`; ask for research in QUESTIONS.md |
| Re-run after operator corrections | Regenerate in place (rule 13); do not re-fan-out unless the niche or paste changed |

## References
- references/brief-template.md - the fixed RESEARCH BRIEF shape, copied
  literally; the only permitted output format.
- references/agent-briefs.md - the five agent briefs verbatim, with their
  return contracts and line caps. Read when dispatching.
- references/niche-map.md - alias and family table mapping a typed niche to
  a study and a playbook, with the conversion-mode fallback.

## Anti-patterns
- Filling a section because it looked empty. Omit and say `not-found:`.
- Promoting a `[web:*]` finding into a sentence a visitor reads as a
  statement about the business.
- Re-reading the niche study here - it arrived as the PRIOR DIGEST.
- Letting agents write to client.md, output/, or QUESTIONS.md directly; only
  the master writes, and only to system/state/.
- Running the fan-out for a retainer edit, or for ads and funnels.
- Treating this brief as visual direction; it is silent on design.

## Changelog
- 1.1.1 niche-map playbook column repointed at the 16-block niche-playbooks file - studied niches now resolve exact instead of falling back to hvac/dental; description trimmed (v1.13.0)
- 1.1.0 Agent 1 proposes a KEYWORD CANDIDATE + reviewer-count difficulty
  tier; Agent 3 returns LOCAL DETAILS per service area - so `[kw]` and
  per-area landmarks arrive as agent proposals, never manual client.md
  fields; Overrides `Target search terms` still outranks the candidate
- 1.0.0 initial (v1.11.0 - governed 4-agent fan-out, evidence tags,
  fixed-shape brief, critic pass)
