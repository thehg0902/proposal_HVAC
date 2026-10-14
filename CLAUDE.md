# Presentation OS — Constitution

This repository is a reusable PITCH-PAGE template. One prospect = one clone
of this repo. A "build" turns the prospect's research (the WWP Structure
file in `input/research/`), `input/client.md`, and the operator's
screenshots and creative into ONE single-page, educational landing page
that walks the prospect through their market, the gap, and the proposed
creative - hosted on the operator's own server like an AgencyOS demo.
Full websites are NOT built here; they are built in AgencyOS and linked
from the pitch's "Your new website" section.

## How to work in this repo

- Start or resume any build with `/build`. It reads
  `system/state/BUILD_STATE.md` and continues from the current phase.
- `/ingest` wires dropped media in; `/qa` is the gate; `/demo`, `/stage`,
  `/deploy` host it; `/package` zips it; `/save` backs up to main.
- All expertise lives in skills (`.claude/skills/`). Trust skill
  descriptions to load what the task needs. Skills marked
  `disable-model-invocation: true` are MANUAL-ONLY (website-only:
  forms, booking, newsletter, analytics, legal, maps, SEO, hosting/DNS,
  security, multi-page architecture, intake enrichment, retainer, hero
  video, 3D, paid media, copywriting): never load or read one unless the
  operator invokes it by name or a command points at its file by path.
- All shared interfaces live in `system/contracts/`. Skills obey contracts.
- All mutable project state lives in `system/state/`. Never store state in this file.
- Python: on Windows run scripts with `py -3` (`python` / `python3` hit
  the Microsoft Store stub on the operator machine); `python3` elsewhere.

## Precedence ladder (conflict resolution — highest wins)

1. Explicit user instruction in the current session
2. `input/client.md` (operator-typed prospect sheet)
3. The research file in `input/research/` (the source of every
   per-prospect claim on the page)
4. `system/state/DECISIONS.md` (previously resolved ambiguities)
5. Hard invariants below (these beat 2-4 ONLY for the enumerated items)
6. `system/contracts/*` (interface law between skills)
7. Skill bodies (`.claude/skills/*/SKILL.md`) — where a kept skill assumes
   a multi-page website, forms, SEO or a GBP intake, the contracts win
8. Skill reference files
9. General knowledge

Tie-breaker within a level: more specific beats more general. If two
same-level sources genuinely conflict: do NOT silently pick — log the
conflict to `system/state/QUESTIONS.md` and take the reversible option.

## Hard invariants

- NEVER trigger paid media generation (Higgsfield or any paid API) without
  operator approval recorded per row in `system/state/MEDIA_LOG.md`. Approval =
  the operator types YES in the file OR explicitly approves NAMED rows
  in-chat (Claude then records `YES [in-chat <date>]`). Blanket "generate
  whatever you want" never counts. No exceptions.
- NEVER deploy without RUNNING the QA gate and getting the operator's
  explicit in-session go. /deploy always runs the QA advisory and presents
  every unresolved item; if QA hasn't passed, deploying requires the
  operator's explicit override, recorded with the outstanding list in
  `system/state/BUILD_STATE.md` notes. Claude never adds `--force-deploy` on
  its own judgment.
- NEVER invent prospect facts: no claim, number, score, review, quote or
  competitor fact the research file or client.md does not contain. Every
  per-prospect line traces to a source tag in the content map; review
  quotes stay verbatim. Missing facts go to `system/state/QUESTIONS.md`
  with clearly marked `[PLACEHOLDER: ...]` text in the meantime.
- NEVER commit secrets, API keys, or credentials to the repo.
- NEVER remove or rename files under `system/contracts/` during a build.

## Interpretation principle (soft — sits below the invariants)

client.md content is never "invalid." Unrecognized values (an unusual
creative type or platform, a palette in words) are intent to interpret:
recommend an approach, log it in `system/state/DECISIONS.md` as
claude-proposed, and proceed. Only a missing business name or research
file blocks Phase 0.

## Terminal protocol (always on, during any build or edit)

- START every reply with the position line: `[Phase N — <name> | <status>]`
  (from system/state/BUILD_STATE.md; use `[OS maintenance]` for work on
  the template itself).
- END every reply with a `NEXT:` line — the exact next action and whose
  it is: `NEXT (you): ...` for operator input (say precisely what to
  provide), `NEXT (me): ...` when work continues automatically.
- At a gate, list what is required to pass it — never a vague "let me
  know".

## Delegation (always on)

- ONE master per session: the context the operator is talking to. It owns
  the pipeline, every write to `system/state/`, `input/client.md` and
  `output/`, and every gate.
- Subagents are WORKERS. They inherit every hard invariant above and can
  satisfy none of them: a worker's report is never a gate approval, a QA
  pass, media approval, or a client fact.
- A worker writes only the paths its prompt leases, under `output/` or
  `system/preview/`; parallel leases never share a file. Law and return format:
  `system/contracts/agent-protocol.md`.

## Token economy (always on)

- Never re-read a file already in context unless it changed. Grep/glob to
  locate before reading; read line-ranges, not whole files, for files
  over 200 lines.
- Never print file contents, diffs, or code into chat that were written
  to disk; report paths + one-line summaries only.
- One skill body at a time: load a skill only at the phase that needs it;
  never preload; never re-read a skill already loaded this session.
- Prefer running scripts over reasoning through checklists in prose.
- Prefer targeted edits over rewrites.
- Never narrate reasoning into chat: no thinking-out-loud paragraphs,
  no option surveys - output the conclusion/result only.
- Phase reports: max 5 lines. No recaps of prior phases.
- Batch related small edits into single operations; no exploratory
  reading "to understand the codebase" — the OS map is in this file.

## Map

Three top-level folders: `input/` (what the operator fills in) →
`system/` (the OS) → `output/` (the deliverable). `CLAUDE.md` and
`.claude/` stay at the repo root because Claude Code loads project
config only from there.

- `input/client.md` — the prospect sheet. `input/client.schema.md` — its rules.
- `input/research/` — the WWP Structure research (PDF or Notion Markdown export).
- `input/reviews/` — review screenshots, one subfolder per platform.
- `input/competitors/` — competitor screenshots, one subfolder per competitor.
- `input/creative/` — the final creative files (creative-N.*).
- `input/assets-intake/` — logo.*, optional website.* screenshot, optional vibe/ refs.
- `system/contracts/` — pitch-sections (section map, sources, fixed
  content, media hooks), file-structure, component-api, design-tokens,
  asset-slots, media-log, agent-protocol.
- `system/state/` — BUILD_STATE.md, DECISIONS.md, QUESTIONS.md, MEDIA_LOG.md,
  AGENT_LOG.md, COPY_DRAFTS.md (the content map).
- `output/` — the single pitch page per system/contracts/file-structure.md.
  The OS never leaks into output/.
- `system/scripts/` — repo utilities (validate, ingest, logo palette,
  style preview, lint, registry, branch splits). Run, don't read.
- `system/preview/` — gate artifacts + drafts. Never ships. `system/docs/` —
  manual, architecture, changelog, registry. `system/archive/` — retired
  AgencyOS commands and docs. `system/sales-skills/` — parked skills.
- `UPDATE_LOG.md` (repo root) — operator's private notes. NEVER read it.
