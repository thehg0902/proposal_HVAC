---
name: agent-orchestration
description: Delegate build work to fresh-context subagents and merge their
  reports - fan-out, refuting pre-gate review, labelled variants,
  draft-ahead, context firewall. Use when a phase has independent parallel
  work, before any human gate, or when a loop will exceed ~10 tool calls.
  Not the interface law itself (the agent-protocol contract) or phase
  sequencing (the pipeline command).
metadata: {version: 1.0.1, category: process, tier: A}
---
# Agent Orchestration

## Purpose
Buy back operator attention. Fresh contexts do the wide, cheap, refutable
work; the master keeps one thread, one set of writes, and one message per
gate. The cost being minimized is operator round-trips, not tokens.

## Inputs
system/contracts/agent-protocol.md (ownership, report block, limits, evidence
standard); system/state/BUILD_STATE.md (phase + gate); the current phase's inputs.

## Outputs
Merged results written by the master; one line per delegation, review round,
and gate in system/state/AGENT_LOG.md; one gate card per human gate.

## Rules
1. Delegate on one of four triggers, never by habit: (a) two or more units
   of work whose inputs do not depend on each other's outputs; (b) a claim
   is about to be presented at a human gate; (c) a taste decision needs
   alternatives; (d) a debug or research loop will exceed ~10 tool calls or
   pull in evidence the master must not keep (screenshots, logs, search
   results). Everything else is cheaper inline.
2. Every prompt is self-contained. A worker has no memory of this session
   and no operator. Never write "as discussed" or "continue the previous
   work". Correctness must not depend on what a worker inherits.
3. Prompt template - all eight lines, in this order:

       ROLE <phase>.<role>. Fresh context: assume nothing about this build.
       GOAL: <one sentence, one deliverable>
       READ: <exact paths, nothing else - do not explore the repo>
       LEASE: <exact writable paths> | none (read-only)
       LAW: system/contracts/agent-protocol.md applies in full. You are a WORKER:
            write only your lease, never write system/state/, never approve
            anything, return one report block and nothing else.
       TASK: <the specifics, including what NOT to decide>
       BUDGET: <= <N> tool calls.
       RETURN: the report block from system/contracts/agent-protocol.md section 3.

4. Batch shape: at most four concurrent workers, each with a budget, total
   batch under 60 calls. When leases would collide, sequence - never widen.
   Anything driving the browser runs one at a time.
5. Refute, never confirm. Before every human gate, add to the template:

       CLAIM TO REFUTE: "<the claim verbatim, as the operator would read it>"
       ARTIFACT: <path>   SERVE: preview URL <url> - never file://
       ACCEPTANCE: <the gate's criteria, verbatim>
       METHOD: capture 360, 768, 1280 in the state where the defect would
               show; look at the images; measurements may corroborate,
               never replace them.
       You get no credit for agreeing. If you cannot break the claim, write
       `result: refutation failed - claim holds` and list what you tried.

6. One fix pass, one re-run, then the operator. Present the remaining defects
   instead of starting a third round: the operator's judgment is cheaper
   than an unbounded loop, and by round three a model starts defending its
   own work.
7. Taste decisions ship as 2-3 LABELED variants in ONE artifact, never as one
   option plus "does this work?". Build the RECOMMENDED label at full
   fidelity, alternatives at swatch fidelity; label them A/B/C with one line
   of intent each and one line on the cost of switching later. The operator
   replies with a letter. Never four labels; never a naked "approve?".
8. Gate card - exactly this, max 8 lines, no recap of the work:

       GATE <phase> - <name>
       Artifact: <paths or URLs>
       Options: A <one line> | B <one line, RECOMMENDED> | C <one line>
       Reviewed: <r> rounds, <d> defects found, <f> fixed (ev: <paths>)
       Open: <remaining defects> | none
       Decide: <the single question, answerable in one word>

9. Launch draft-ahead work IN THE SAME TURN as the gate card, after it: the
   card streams to the operator while the workers run. Only work that passes
   rule 10 is eligible.
10. Independence test - draft ahead only if BOTH hold: (a) every input is
    already approved, operator-typed, or immutable; (b) if the gate goes the
    other way the work is DISCARDED, not corrected. Output lands in
    system/preview/drafts/ (ephemeral, outside the deliverable) and the master
    promotes it only after the gate. Anything that would have to be edited
    to survive a different answer is gate-DEPENDENT: do not start.
11. Context firewall: competitor scans, screenshot loops, log digestion, and
    long research happen in a worker. What returns is the report block. If
    the master later needs the raw material it reads the leased file - it
    never asks the worker to paste it.
12. Merge mechanically, then log: decisions to the decisions log, questions
    to the questions file, `result` lines condensed into the phase report,
    one ledger line per batch, round, and gate. Never quote a report block
    into chat.
13. Blocked worker: read `blocked:`, resolve it (usually a lease), re-issue
    ONCE. Two failures on the same unit = do it inline. Never re-issue a
    third time with a bigger budget.

## Decision guide
| situation | move |
|---|---|
| 3 independent research questions | fan out read-only, budget 12 each |
| a visual claim heading to a gate | refuting reviewer, images at 3 widths |
| "which of these feels right?" | 2-3 labeled variants, one artifact |
| operator away for hours | draft-ahead the gate-independent set |
| 25-call debug hunt | one worker, conclusion only |
| one file, one known fix | inline - delegation costs more than it saves |

## Anti-patterns
- One worker asked to "review, fix, and update the state file" - three
  roles, one of them forbidden.
- Two workers leased the same file "but different sections".
- A reviewer prompt that asks "does this look good?" (it will say yes).
- Presenting one option and calling it a gate; presenting four.
- Draft-ahead that writes into the deliverable before its gate.
- Re-reading a worker's files to write a phase report its report already
  contained.

## Changelog
- 1.0.1 description trimmed (v1.13.0)
- 1.0.0 initial (v1.11.0)
