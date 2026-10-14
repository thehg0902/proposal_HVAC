Run or resume the pitch-page build pipeline.

You are the MASTER for this session (system/contracts/agent-protocol.md). Every
write to system/state/, input/client.md and output/ is yours; workers get
read-only reviews or explicit leases. Log every delegation, review round and
gate in system/state/AGENT_LOG.md. Python: `py -3` on Windows (`python` /
`python3` hit the Microsoft Store stub), `python3` elsewhere. Manual-only
skills (`disable-model-invocation: true`) are never loaded by this pipeline.

1. Read system/state/BUILD_STATE.md. If "Client:" is unset, this is a fresh
   build: set it from client.md Prospect > Business name, set Started, and
   BOOTSTRAP BRANCHES: `bash system/scripts/bootstrap-branches.sh` - creates
   any missing `staging` and `deploy` branch as a SAFE site-only placeholder
   and pushes when a remote is configured. Real content only ever comes from
   stage-split.sh (/stage, /demo) and deploy-split.sh (/deploy).
2. Find the first phase not marked done - match the phase NUMBER, not its
   name - and execute phases in order:

   - Phase 0 intake (no stop unless blocked):
     a. Run `py -3 system/scripts/validate-client-md.py`. Any BLOCKER (no
        business name, no research file, several unnamed research files)
        -> one question in system/state/QUESTIONS.md, mark phase 0
        blocked, STOP with the exact fix. SOFT lines are noted, not stops.
     b. Open the research file. PDF of 10 pages or fewer: Read it whole.
        Longer: Read with `pages` in chunks of 20 or fewer; if page
        rendering is unavailable (no pdftoppm), extract text with pypdf
        via `py -3 -c` when installed; otherwise STOP and ask for poppler
        or a Notion Markdown export. Markdown export: read its .md files.
     c. Check it against the WWP Structure (input/client.schema.md
        "Research file") and list every empty field. Empty fields never
        block - they become placeholders + questions in Phase 1.
     d. Report <=5 lines: prospect, research file + empty WWP fields,
        brand source (palette / logo / default), screenshot and creative
        counts, SOFT items. Mark phase 0 done and continue in the same
        turn (`NEXT (me): Phase 1 content map.`).

   - Phase 1 content map (no gate):
     a. Write the content map into system/state/COPY_DRAFTS.md: one block
        per section id from system/contracts/pitch-sections.md, honoring
        client.md Sections (Hide / Show / Order). Every line carries its
        source tag; review quotes verbatim; creative copy exactly as
        client.md gives it.
     b. Fill ONLY from the research file and client.md (pitch-sections
        content rules 2-6). Empty field -> `[PLACEHOLDER: ...]` + one
        `- [ ]` row in QUESTIONS.md. client.md beats the research on any
        conflicting fact; log the conflict as one DECISIONS.md line.
     c. Self-audit: no line without a source tag, no number or name the
        source lacks. persuasion-mechanics may guide ORDER and EMPHASIS
        inside a section, never new claims.
     d. Report <=5 lines (sections mapped, placeholders open). Continue.

   - Phase 2 brand (no gate - the draft review covers it):
     a. Colour source, first match wins: client.md Brand > Palette (hexes
        used exactly; colour words interpreted and logged) -> the logo:
        `py -3 system/scripts/logo-palette.py`, use its BRAND colours ->
        neither: the design-direction skill picks a default direction for
        the niche.
     b. design-tokens skill -> output/shared/tokens.css (design-tokens
        contract): brand primary/accent as given; neutrals, surfaces, type
        scale, spacing and motion derived. Fonts: client.md Brand > Fonts,
        else design-direction's pairing - self-hosted .woff2 or a system
        stack (no font CDN, file-structure rule 5).
     c. Run `py -3 system/scripts/generate-style-preview.py` and fix every
        CONTRAST FAIL. A brand colour that fails as text stays as accent /
        background only; log it.
     d. Write the BRAND block in DECISIONS.md (source, hexes, fonts,
        contrast adjustments). Report <=3 lines. Continue.

   - Phase 3 draft (HUMAN gate: the operator reviews the draft):
     a. Build output/ per system/contracts/file-structure.md (index.html,
        style.css, script.js, robots.txt, shared/base.css). Sections in
        content-map order, markup and components per component-api.md,
        copy taken from COPY_DRAFTS.md - place it, never re-draft it.
        Skills: frontend-design (distinctive, not templated), layout-systems
        (rhythm, grid, responsive), components (carousel and card patterns),
        accessibility (semantics, focus, keyboard). Where any of them
        assumes a multi-page site, forms, SEO or a GBP intake, the
        contracts win.
     b. Media hooks: every ingest marker pair from pitch-sections.md with
        its empty state; one `ingest:creative-N` per client.md Creative
        block inside a creative-frame sized to its Platform / Aspect; the
        logo pair in the cover and in each ad avatar; the website pair only
        when a Demo website URL exists. Never hand-write content between
        markers. Then run `py -3 system/scripts/ingest-assets.py` so files
        already dropped fill in now.
     c. Presentation layer + print stylesheet per component-api.md.
     d. PRE-GATE REVIEW (agent-orchestration rule 5): one read-only
        refuting worker against "the draft matches the content map,
        renders cleanly at 360/768/1280, keyboard section navigation and
        both carousels work, and nothing on the page lacks a source", with
        images at all three widths (agent-protocol section 4). Fix, re-run
        once, stop.
     e. GATE card: preview via the `site` server (.claude/launch.json,
        http://localhost:8080) or `/stage` for a shareable demo link; list
        open placeholders and empty media hooks. The operator replies with
        edits or "approve"; edits loop inside this phase.

   - Phase 4 media (HUMAN gate: files dropped):
     If every media hook is already filled, mark done and continue.
     Otherwise STOP and name exactly what is missing (input/reviews/,
     input/competitors/<name>/, input/creative/creative-N.*, optional
     input/assets-intake/website.*); the operator drops files and runs
     /ingest. Done when every marker holds real media or the operator
     hides that section in client.md. Never generate media here (CLAUDE.md
     invariant).

   - Phase 5 polish (no gate): frontend-animation (CSS-only reveals,
     reduced-motion safe), mobile-polish (the prospect may open the link on
     a phone: swipeable carousels, readable grids, thumb-reachable nav),
     performance (lazy screenshots, click-to-play video, page-weight
     budget), a final accessibility pass. Copy does not change here.

   - Phase 6 qa: run /qa. Mark done only when the check script passes
     (zero [PLACEHOLDER], every link resolves), /visual-qa passes, and the
     `6.facts` refuting reviewer finds every page line in its source
     (COPY_DRAFTS.md tags -> research file / client.md): quotes character
     by character, numbers, scores and competitor names.

   - Phase 7 deploy: after phase 6 = done, STOP and ask exactly:
     "Deploy how? (a) /deploy - deploy branch on your hosting (Hostinger
     Git), (b) /package - zip for manual upload, (c) GitHub Pages." Then run
     that command; for (c) read
     .claude/skills/deploy-hostinger/references/github-pages.md by path. The
     QA-gate hook and the /deploy advisory apply. NO WORKER EVER pushes,
     splits, or packages.
3. After each phase: update BUILD_STATE.md (status, completed date, notes)
   and append that phase's gate line to system/state/AGENT_LOG.md.
4. Respect all hard invariants in CLAUDE.md at every phase. A worker report
   never satisfies one.
