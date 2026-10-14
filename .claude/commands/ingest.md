Ingest the operator's screenshots, creative, logo and demo-site screenshot.

1. Run `py -3 system/scripts/ingest-assets.py` (add `--force` to re-encode
   cached creative video). It processes input/reviews/, input/competitors/,
   input/creative/ and input/assets-intake/logo.* / website.* into
   output/assets/ per system/contracts/asset-slots.md, rewrites every
   ingest marker pair in output/index.html, and logs creative rows in
   system/state/MEDIA_LOG.md.
2. Read the report:
   - DONE = processed and wired.
   - EMPTY = a hook with no files; tell the operator the exact folder.
   - PENDING = a tool is missing; give the printed command.
   - UNKNOWN = a file that matches nothing (wrong type, or a creative not
     named creative-N); ask, never guess.
   - MARKERS = which hooks were filled. "output/index.html not found" =
     the draft does not exist yet; that's fine before Phase 3.
3. If Phase 4 is in progress and every hook is filled, mark Phase 4 done in
   system/state/BUILD_STATE.md and continue the pipeline.
4. Re-run any time; it is idempotent.
