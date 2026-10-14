Push the current local website files to the `deploy` branch (live target).

1. QA ADVISORY (always run, never skip):
   a. If output/ exists, run `py -3 .claude/skills/qa-review/scripts/check.py`
      and note every FAIL.
   b. Read system/state/BUILD_STATE.md: is phase 6 (qa) done? Any phases blocked?
   c. Read system/state/QUESTIONS.md for unresolved client questions;
      grep output/ for [PLACEHOLDER (leftover placeholders).
2. Present the operator a short outstanding list (or "QA clean") and STOP
   for an explicit go/no-go. Never proceed without the go.
3. On go: run `bash system/scripts/deploy-split.sh` - snapshots the CURRENT LOCAL
   output/ files (uncommitted included), verifies zero OS files, and
   force-pushes the site-only result to `deploy`. If QA is not marked
   done, the script requires `--force-deploy` - add it ONLY with the
   operator's explicit go, and record in system/state/BUILD_STATE.md notes:
   deploy date + commit + "QA override" + the outstanding list.
   If QA was clean, record the deploy normally (URL, date, commit).
4. Report: deploy branch updated - the operator pulls it in hPanel
   (public_html) to go live. Rollback: `bash system/scripts/deploy-split.sh
   <previous-good-main-commit>` after the same advisory.
