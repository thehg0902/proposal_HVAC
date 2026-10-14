# Contract: Agent Protocol  (v1.1.0)

Interface law between the MASTER (the session that owns a build) and the
WORKERS it delegates to. Applies to every delegated unit of work in every
phase, whatever expertise the worker loads. Names roles and paths only —
never a skill, never a command.

## Roles

- MASTER — exactly one per session: the context the operator talks to.
  Owns the pipeline, all state, every write listed in section 1, and every
  gate.
- WORKER — a forked context with no operator channel and no memory of the
  session. Receives a self-contained prompt, does one job, returns one
  report. Depth is 1: a worker never delegates.

## 1. Write ownership (single writer)

1.1 Only the master writes `system/state/**`, `input/client.md`,
    `output/shared/**`, `system/contracts/**`, `.claude/**`,
    `system/docs/**`, and repo-root files. No delegated exception exists,
    including a correction a worker believes is obvious.
1.2 A worker writes ONLY the paths its prompt LEASES. Leasable paths are
    limited to `output/**` (excluding `output/shared/**`) and
    `system/preview/**`.
1.3 A lease is a list of concrete file paths, or a directory no other lease
    touches. It is fixed at delegation time and echoed back in the report's
    `wrote:` field.
1.4 Concurrent leases are pairwise disjoint at WHOLE-FILE granularity. Two
    workers never hold the same file, not even for different regions of it:
    there is no merge step, so the second writer destroys the first.
1.5 Shared surfaces are serialized, never held in parallel: `output/shared/**`,
    `output/assets/**`, `system/preview/style-preview.html`,
    `system/preview/layout-preview.html`, the local preview server, and the
    browser. Exactly one worker in a batch may hold one, or the master does
    that work itself.
1.6 A worker needing a path outside its lease STOPS and returns
    `status: blocked` naming the path. It never widens its own lease.
1.7 Files created inside a lease but not named by the delegation are listed
    in `wrote:`; the master adopts or deletes them. Nothing enters the
    deliverable unreviewed.
1.8 `input/assets-intake/**` is read-only to every role except the ingest
    script, which only the master runs.
1.9 The master applies reports in fan-out order. After any parallel batch
    that touched `output/**` it re-runs the QA check script before the next
    gate.

## 2. Delegation limits — a worker may NEVER

2.1 Write anything under `system/state/`: no phase status, no decision, no
    question, no media row. Findings return as report fields; the master
    transcribes.
2.2 Trigger paid media generation, or create or alter any approval value in
    the media ledger. The paid-media invariant is satisfied only by the
    operator, only in the master's session.
2.3 Run a publish or history operation: commit, push, the stage or deploy
    split scripts, branch bootstrap, packaging.
2.4 Mark a phase done, declare a gate passed, or report that the operator
    approved anything. The report block in section 3 has no field capable of
    expressing approval — that absence is deliberate.
2.5 Invent a client fact. Unknown facts become `questions:` lines; text in
    leased files uses the placeholder marker.
2.6 Emit a key, token, password, or credential — into a file or a report.
2.7 Delegate further, or address the operator. Text it writes for a human
    returns to the master, who decides what reaches chat.
2.8 Invoke a pipeline command verb. Commands belong to the master.

## 3. Report block (the only return surface)

A worker's final message is exactly this block: fixed keys, fixed order,
<=25 lines, no prose paragraphs, no code, no file contents. Empty keys read
`none`.

    REPORT <phase>.<role>
    status: ok | partial | blocked
    result: <one line - the answer, verdict, or deliverable location>
    wrote: <leased path>[, <leased path>...] | none
    findings:           <=5 lines, each  - <claim> [ev: <path|measurement>]
    proposed-decisions: <=3 lines, each  - <topic> | <decision> | <why>
    questions:          <=3 lines, each  - <one-line operator-facing question>
    blocked: <path or reason> | none
    cost: <n> calls

3.1 Evidence is a path or a measured value, never an adjective. "Looks
    correct" is not evidence.
3.2 Anything longer than a line goes into a leased file and is cited by
    path. Raw research, logs, transcripts, and screenshots never enter the
    master's context — this is the context firewall.
3.3 A report that does not parse is treated as `status: blocked`. The master
    re-issues once with the template repeated, then does the job itself.
3.4 The master merges mechanically: `proposed-decisions` -> the decisions
    log, `questions` -> the questions file, `result` -> the phase report,
    `wrote` -> the verification set. It never re-reads a worker's output to
    reconstruct what the report should have said.

## 4. Evidence standard for appearance

4.1 A claim about how something LOOKS is supported only by an image of the
    rendered artifact, served over the local preview server (never
    `file://`), at 360, 768, and 1280 px, captured in the state where the
    defect would appear: scrolled to the section, after the animation
    completes, mobile nav open.
4.2 Computed styles, bounding boxes, and DOM arithmetic may CORROBORATE an
    image; they never replace one. They cannot observe paint —
    letterboxed video inside a correctly sized box, background bleed,
    z-order, overflow clipping, font fallback, object-fit, composited
    transforms, first-frame poster state. A geometric "gap: 0" reported
    alongside a visible gap is the failure this rule exists to prevent.
4.3 If image capture is unavailable on the machine, the claim returns
    `status: partial` and the master presents it marked UNVERIFIED.
    Measurement never upgrades an unverified visual claim.
4.4 The master starts and stops the preview server. Workers are given the
    URL.

## 5. Review rounds

5.1 A reviewer is prompted to REFUTE a stated claim, in a context that did
    not produce the artifact.
5.2 Two review rounds per gate, maximum: review -> master fixes -> one
    re-run of the same prompt. A third round is forbidden; remaining
    defects go to the operator with the artifact.
5.3 A reviewer that cannot break the claim says so explicitly
    (`result: refutation failed - claim holds`) and lists what it tried.
    Silence, "looks good", or empty findings without a method trace is a
    failed review, not a pass.

## 6. Instrumentation

6.1 The master appends one line to `system/state/AGENT_LOG.md` per delegated batch,
    per review round, and per human gate:
    `YYYY-MM-DD | phase | pattern | role | rounds | defects | calls | outcome`
6.2 `pattern` is one of: fanout | review | variants | draftahead | firewall |
    gate | sync.
6.3 Gate lines: `role` = gate name, `rounds` = operator replies that gate
    consumed, `outcome` = passed | reworked, `defects` and `calls` = `-`.
6.4 Append-only, never rewritten. Derived metric: operator round-trips per
    human gate = sum of gate `rounds` / count of gate lines.

## 7. Versioning

Breaking change = any change to the section 3 keys or the section 1.1
ownership list. Bump this contract and the template minor version together.
