# Architecture — Presentation OS v2.0.0

PresentationOS is a fork of AgencyOS v1.13.0 (its architecture doc is in
system/archive/docs/ARCHITECTURE-agencyos.md). The machinery is the same -
master/worker delegation, contracts, state files, gates, branch-split
hosting - pointed at a different deliverable: one pitch page.

## Data flow

    input/research/ (WWP Structure) ─┐
    input/client.md ─────────────────┼─> Phase 1 content map (COPY_DRAFTS.md, source-tagged)
                                     │        │
    logo / palette ──> Phase 2 tokens.css     ▼
                                     Phase 3 output/index.html  <── pitch-sections + component-api
    input/reviews/ competitors/ ─┐            ▲
    input/creative/ assets-intake/├─> /ingest ┘  (fills <!-- ingest:* --> markers)
                                 └─> output/assets/

## What changed from AgencyOS

| area | AgencyOS | PresentationOS |
|---|---|---|
| deliverable | multi-page website | one pitch page (noindex) |
| source of truth | GBP paste + web research | operator's WWP research file + client.md |
| design | 3 variants, operator picks | brand palette -> logo colours -> niche default, no gate |
| media | shopping list + Higgsfield slots | screenshots + operator's creative via /ingest |
| skills | 41 auto | 21 auto, 20 manual-only (website features) |
| commands | + /handoff, /client-edit | archived |

## Contracts

- pitch-sections.md - section ids, order, WWP sources, content rules,
  fixed content (research tracks, awareness grid), ingest markers.
- component-api.md - section shape + the pitch components.
- file-structure.md - the single-page output tree.
- asset-slots.md - drop folders -> assets -> markers.
- design-tokens.md, media-log.md, agent-protocol.md - unchanged law.

## Guarantees

- Facts: every page line traces to a source tag; QA's facts pass checks
  it; placeholders fail QA.
- Deploy: the pre-deploy hook blocks pushes to `deploy` until BUILD_STATE
  shows `| 6 | qa | done` (QA is still phase 6 for exactly this reason).
- Paid media: never part of the pipeline; the MEDIA_LOG approval
  invariant still governs any manual generation request.
- Output purity: stage-split.sh / deploy-split.sh verify zero OS files.
