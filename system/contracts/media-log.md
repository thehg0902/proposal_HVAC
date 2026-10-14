# Contract: MEDIA_LOG.md Format  (v1.0.0)

`system/state/MEDIA_LOG.md` is the ledger of ALL generated media. One markdown
table per build, columns exactly:

| id | date | type | model | prompt-summary | credits | storyboard-approved | file | status |

Rules:
1. A row with storyboard-approved = YES MUST exist BEFORE any paid
   generation is triggered (the CLAUDE.md hard invariant). YES is set:
   (a) by the human typing it in this file, OR (b) by Claude
   transcribing `YES [in-chat YYYY-MM-DD]` after the operator explicitly
   approved that NAMED row in the session. Claude never writes YES
   from inference, silence, or blanket permission.
2. `file` is the final path under assets/ (or "-" if rejected/unused).
3. `status` is one of: planned, approved, generated, in-use, rejected.
4. Credits column is required — it feeds cost tracking per client.
5. Never delete rows; mark rejected instead.
6. PresentationOS: creative the operator made outside the OS is logged by
   /ingest as `model = operator`, `credits = -`,
   `storyboard-approved = n/a (operator-made)`, `status = in-use`, with
   `file` as the repo-relative path (output/assets/...). Rule 1 still
   governs any generation Claude would trigger.
