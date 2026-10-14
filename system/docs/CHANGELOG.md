# Template Changelog
## v2.0.0 - 2026-10-13
PresentationOS fork. The repo now builds ONE educational pitch page per
prospect (market, reviews, competitors, the gap, mental chain, plan,
creative, optional demo-site link, how I help) instead of a website.
- /build rewritten: 0 intake -> 1 content-map -> 2 brand -> 3 draft (gate)
  -> 4 media (gate) -> 5 polish -> 6 qa -> 7 deploy. QA stays phase 6 so the
  deploy hook, /package and /deploy are unchanged.
- input/: client.md is now a short prospect sheet (prospect, research
  file, brand palette/fonts, Creative N blocks, demo website, sections,
  agency). New drop folders research/, reviews/, competitors/, creative/;
  assets-intake/ holds logo.* + website.* (+ vibe/). slots/ removed.
- New contract pitch-sections.md (section map, WWP sources, content rules,
  fixed content, ingest markers). file-structure, component-api and
  asset-slots rewritten for the single page; media-log rule 6 added.
- Scripts: validate-client-md.py and ingest-assets.py rewritten (carousels
  with browser-frame proof, creative video/poster, logo, demo screenshot,
  marker injection, idempotent); new logo-palette.py; registry gains a
  load column; check.py excludes lazy screenshots and click-to-play video
  from the initial page-weight cap (own 12MB warn cap).
- 20 website-only skills set to manual-only (disable-model-invocation).
  /handoff and /client-edit archived to system/archive/commands/; the
  AgencyOS architecture + operation manual archived to system/archive/docs/.
- Commands call scripts with `py -3` (Windows Store-stub python).

## v1.13.0 - 2026-10-01
Skill-library cleanup. 44 skills -> 41 active; the always-on description
tax drops from 2,035 words to ~1,700; 20 reference files holding 7-14
lines each are gone, inlined where they belong.
- PARKED to system/sales-skills/ (outside .claude/, so not discovered, not
  linted, not in the registry, byte-identical, one `git mv` to restore):
  objections-and-closes, cold-outreach, sales-calls-and-pricing. The five
  copy-facing skills stay (winners-writing-process, persuasion-mechanics,
  copy-frameworks, funnel-playbooks, local-seo-gbp). copy-frameworks 1.2.0
  absorbed the close/CTA guidance its Close section used to delegate.
- ORPHAN FIX (the one that could silently cost a client real traffic):
  seo-technical, image-optimization, security-basics and legal-pages all
  said "Phase 5" but build.md's Phase 5 named none of them - the entire
  SEO layer depended on Claude noticing a description mid-phase. Phase 5
  now names a FINISHING PASS explicitly, and the manual's §3 matches.
- NICHE GAP CLOSED: 11 audience studies existed against 5 design playbooks
  with zero overlap, so every studied niche fell through to the
  conversion-mode fallback. design-direction 1.4.0 ships
  references/niche-playbooks.md - 16 blocks in one file, the 11 new ones
  distilled from each study's section 9. niche-map's playbook column now
  resolves those niches `exact` instead of hvac/dental adjacent.
- ONE OWNER PER RULE: rules/css.md (auto-loads on every CSS edit) now owns
  motion safety, tap targets, 16px inputs, svh, safe-area and the contrast
  floors; accessibility, mobile-polish and three-js keep only the nuance
  they add. Restatements dropped from 8 files to 4 for reduced-motion and
  4 to 2 for the 44px target.
- BUG found while deduping: hero-media rule 7 hardcoded the cdn hero-video
  budget (2.5MB/4MB) while performance's DEFAULT profile is the tighter
  no-cdn set (2MB/3MB) - a hero encoded to hero-media's number would fail
  check.py on an unknown Hosting plan. Rule 7 now reads the active profile.
- Stale guidance corrected: site-architecture's multi-page pattern still
  said `/about.html` after the file-structure contract moved to clean
  folder URLs.
- Inlined (file deleted, content moved into the SKILL body): copywriting
  headlines+cta, design-tokens color-theory+typography, frontend-animation
  css-only+gsap+reduced-motion, layout-systems hero-patterns+responsive,
  three-js setup+budget, accessibility audit-checklist, performance
  loading-strategy, media-generation image+video prompts+credit-budgeting,
  hero-media mp4-vs-sequence, seo-technical local-seo, site-architecture
  single-page+multi-page. Kept as files: the 11 audience studies,
  market-research's three, herostory stage-architecture, seo-technical
  structured-data, service-location-matrix, github-pages, scroll-scrub,
  and every template/ and script/.
- Nine descriptions trimmed toward ~40 words (agent-orchestration 81 ->
  56, audience-research 74 -> 45, market-research 73 -> 50, and six more).
- frontend-design left untouched by request; its `license:` line still
  points at a LICENSE.txt that does not exist and still prints inside its
  REGISTRY.md description cell.
## v1.12.0 - 2026-10-01
Structural split: the OS and the deliverable are now separate top-level
folders, so the boundary the split scripts already enforced is visible in
the filesystem. Work flows `input/` -> `system/` -> `output/`.
- MOVES: client/ -> input/; contracts|state|scripts|docs|preview/ ->
  system/*; OPERATION_MANUAL.md -> system/docs/; site/ -> output/.
  CLAUDE.md and .claude/ STAY at the repo root - Claude Code discovers
  project skills, commands, hooks and settings only there, so moving them
  would silently disable all of it. deliverables/ also stays at the root:
  a /package zip inside output/ would ship to the live branch.
- file-structure 3.0.0 (breaking - the deliverable root changed):
  canonical tree rooted at output/, relative-path table updated, repo
  shape documented, framework exception paths updated.
- agent-protocol 1.1.0: section 1.1 ownership list, 1.2 leasable paths
  (output/** + system/preview/**), 1.5 shared surfaces, 1.8 intake path.
  asset-slots 1.2.0, design-tokens 1.2.0, component-api 1.2.0: paths only.
- Scripts repointed: validate-client-md, ingest-assets, generate-style-
  preview (its emitted <link> is now ../../output/shared/tokens.css - the
  preview sits two levels deep), generate-skill-registry, lint-skills,
  qa-review/check.py. Split scripts snapshot output/ and their OS_PATHS
  cleanliness regex now matches the new root set.
- ROLLBACK FALLBACK: both split scripts resolve `<commit>:output` first
  and fall back to `<commit>:site`, so rolling back or re-staging any
  pre-migration commit still works instead of aborting on the rename.
- pre-deploy-qa-gate.sh reads system/state/BUILD_STATE.md. launch.json
  serves output/ and now invokes `py -3` instead of a hardcoded
  interpreter path from another machine (the old value could not start).
- Existing client repos cloned from an earlier template keep the old
  layout and are unaffected; deploy branches are unaffected (their
  content is the site tree at branch root, which never had a folder
  name).
## v1.11.4 - 2026-08-20
Title overflow, found by a dry-run simulation of the matrix against a
realistic business name: "heat pump installation Richmond Hill | Apex
Heating & Cooling" is 61 chars, and rule 1 capped titles at 60 without
defining what to do when the generic template overflows.
- seo-technical 1.3.0: new rule 1a overflow ladder - (a) keyword +
  brand, (b) drop the brand on deep matrix pages (H1/NAP/JSON-LD still
  carry it), (c) if the keyword alone still overflows, ship it and log
  one DECISIONS.md line. Never mid-word truncation, never an invented
  abbreviation of the operator's own keyword or business name. Home
  always keeps the brand.
- qa-review 1.3.0: check.py gains the title/meta audit - FAIL on missing
  or duplicate title/description (closing the gap seo-technical rule 6
  had explicitly delegated to qa but nothing implemented), WARN above
  60/155 chars so a skipped ladder stays visible. Titles are HTML-entity
  decoded before measuring: "&amp;" is one rendered character, and
  counting the entity added 4 phantom chars to every business name
  containing "&".
## v1.11.3 - 2026-08-20
The whole SEO process now runs on one explicit keyword input: `Target
search terms` is formalized as THE keyword driver end to end. Filled ->
those exact phrases; empty -> the generic `[service] [location]`
template. Never a silent third state (market-research's candidate is
advisory-only, promoted only if the operator copies it in).
- client.schema.md + client.md: Target search terms documented as the
  keyword input, `/`-list syntax, precedence spelled out inline where the
  operator actually reads it.
- site-architecture 1.4.0: new rule 1c generates the service x location
  page matrix (gated on 2+ service areas or 3+ distinct-intent services)
  - new references/service-location-matrix.md covers keyword source,
  30-page build priority, per-page word count/local-detail requirements,
  and internal linking rules (hub structure, link caps, anchor variety).
- seo-technical 1.2.0: rule 1 title/H1 keyword precedence matches the two
  states exactly; rule 3 + structured-data.md gain an LLM/GEO completeness
  note (same JSON-LD block, no separate markup).
- qa-review 1.2.0: check.py gains a near-duplicate-content check across
  pages (5-word shingle Jaccard, >50% overlap fails) - guards the new
  matrix against cloned service/location pages. Tested against a real
  clone (62% overlap, correctly failed) and a genuinely distinct page
  (correctly passed) before shipping.
- market-research: brief-template.md wording corrected - the KEYWORD
  CANDIDATE was documented as an automatic fallback when Target search
  terms is empty; fixed to advisory-only, matching the exactly-two-states
  rule above.
## v1.11.2 - 2026-08-20
Minimize manual client.md input for SEO variables: every field the
`organic-seo-website-build` reference skill wanted as manual intake now
arrives by paste-parsing or agent proposal instead — zero new required
client.md fields.
- client.schema.md: Service area accepts a `/`-separated list (same
  syntax as Pages), feeding areaServed + future location pages.
- client-enrichment 1.2.1: extracts a service-area list from the paste
  when more than one place served is named; frontmatter version
  corrected to match the changelog (was stale at 1.1.0).
- market-research 1.1.0: Agent 1 proposes a KEYWORD CANDIDATE + reviewer-
  count difficulty tier (avg 50-500 reviews = sweet spot); Agent 3
  returns LOCAL DETAILS (a landmark/neighbourhood per service area).
  Both are visible, correctable proposals in the RESEARCH BRIEF, never
  blank fields to type; Overrides `Target search terms` still outranks
  the candidate. brief-template.md updated to match (reviews column,
  Keyword candidate line, Local details table).
## v1.11.1 - 2026-08-13
WWP doctrine merge: best-of-both-worlds from the operator's compiled WWP
module guide into the two owning skills (no monolithic doc):
- winners-writing-process 1.2.0: Top Player Analysis upgraded to the full
  modeling master-key method (2-3 same-result examples in and out of
  niche, line-by-line breakdown, skeleton extraction, swap specifics /
  keep structure; copy-frameworks skeletons demoted to fallback) +
  weak-draft rule (generic output = thin research, redo WWP, don't grind).
- copy-frameworks 1.1.0: new Drafting Discipline section (filter OFF,
  volume over quality, multiple hook variants, all-at-once vs
  piece-by-piece assembly) and Refinement Checklist extended (distance /
  overnight before judging, read out loud, >=2-3 passes, never ship the
  first draft, reviewer-advises-writer-judges).
## v1.11.0 - 2026-07-29 "The Studio Update"
Agent-driven builds: four operator inputs, a master governing a fleet of
workers, automated market research, and a signature hero on every site.
Derived from the CopperCraftHC retrospective (~7 round-trips in phases
0-2, 3 avoidable; a scroll-scrub gap that reached a gate twice because
DOM math was accepted as visual proof; taste shown as one option; idle
gate waits).
- NEW contract contracts/agent-protocol.md: one MASTER per session owning
  every write to state/, client.md and site/shared/; WORKERS get
  whole-file leases under site/ and preview/ only, pairwise disjoint
  (no merge step exists); shared surfaces (site/shared, site/assets, the
  preview server, the browser) serialized; 8 delegation prohibitions tied
  to the hard invariants; a 9-key report block with NO field able to
  express approval; the visual evidence standard (images of the served
  page at 360/768/1280 - DOM measurement may corroborate, never replace);
  2 review rounds maximum, then the operator.
- NEW skill agent-orchestration (tier A): delegation triggers, the
  self-contained prompt template, refute-framed review, 2-3 labelled
  variants for taste calls, the gate card, the draft-ahead independence
  test, context firewall. CLAUDE.md gains a 10-line always-on Delegation
  section; state/AGENT_LOG.md records every batch, round and gate so
  /usage-audit can score round-trips per gate.
- MINIMAL INTAKE (client.md v3): four inputs at the top - Business
  Profile Paste, Niche, Special requests, Hero story - above an END OF
  REQUIRED INPUT banner; the 48 Overrides lines are reframed as optional
  control below it. Typed `## Niche` always beats GBP-category detection
  and resolves through a new alias/family/conversion-mode niche map; no
  study match now yields NO audience brief rather than a wrong one.
- PHASE 0 NO LONGER STOPS: fact confirmations become a `- [ ]` ledger in
  QUESTIONS.md answered any time before /qa. Enforcement moved from a
  chat prompt to the QA script, which now fails on any open row as well
  as on placeholders. `Autonomy: low` restores the blocking table.
- NEW skill market-research (tier A) + 3 references: a governed 4-worker
  parallel fan-out (top players, verbatim 5*/1* review language, search
  intent, client-side offer and proof) plus a critic worker, synthesized
  into a fixed-shape RESEARCH BRIEF whose Build directives bind Phases
  1-3. Five evidence tags; only [client] material may become a published
  claim; absence of evidence emits `not-found:` and never filler.
  winners-writing-process 1.1.0 gains an Automation boundary section
  reconciling this with its "never delegated" doctrine.
- PHASE 1 RENAMED `discovery` and now runs research, architecture and
  visual-independent copy (both hero registers unpicked) while the
  operator gathers design references - the two happen in parallel
  instead of in series.
- PHASE 2 IS ONE TASTE GATE: 2-3 labelled direction variants in one
  preview, the operator replies with a letter, then the recommended
  label is built for real and adversarially reviewed with real
  screenshots before it is ever shown. Draft-ahead launches in the same
  turn as the gate card.
- SIGNATURE HERO: herostory skill installed (from the operator's port
  document) and extended with a `graphic` beat type - client.md
  `## Hero story` is broken into beats and rendered as a polygon/SVG
  scene driven by a per-beat progress property, at zero media cost.
  Approving it at Phase 2 adds matching footage slots to Phase 4 as an
  explicit upgrade; no hero story means no hero media slots at all.
  Empty hero story = a solid-colour hero plus a site-wide SECTION COLOUR
  PROGRESSION (one fixed backdrop blending between per-section colours -
  a documented, narrow exception to the transform/opacity-only rule).
  design-direction 1.3.0 requires a NAMED hero concept every build and
  adds the anti-generic gate test ("could a competitor paste this
  unchanged?").
- Consumers updated: site-architecture 1.3.0, copywriting 1.4.0 (draft
  mode + register picked at Phase 3), visual-qa 1.1.0 (pre-gate runs in a
  worker; screenshots mandatory), layout-systems 1.3.0, design-tokens
  1.1.0, frontend-animation 1.1.0, media-generation 1.2.0,
  audience-research 1.1.0, client-enrichment 1.2.0, intake-validation
  1.2.0, token-economy (structural containment), hero-media (herostory
  routing). BUILD_STATE rows 1/2/6 reworded; rows 0 and 6 kept
  byte-identical because the pre-deploy hook greps them.
## v1.10.0 - 2026-07-12 "The Control Update"
Four-verb manual control surface over where local site files go:
- /stage (new): stage-split.sh (renamed from demo-split.sh) snapshots
  the CURRENT LOCAL site/ working tree (uncommitted + untracked
  included) -> site-only staging branch + forced noindex robots.txt.
  No gates; view on the demo subdomain via manual hPanel pull.
- /save (new): commit ALL local changes + push origin/main. No gates;
  hook now exempts main pushes (previously wrongly blocked mid-build).
- /deploy (reworked): QA gate is now an ADVISORY, not a hard block -
  /deploy always runs check.py + reads BUILD_STATE/QUESTIONS/leftover
  placeholders, presents the outstanding list, and STOPs for the
  operator's explicit go. deploy-split.sh snapshots local site/ ->
  deploy branch; refuses without --force-deploy when QA isn't done
  (override recorded in BUILD_STATE notes). CLAUDE.md invariant
  reworded accordingly (operator-directed).
- /demo (reworked): bootstrap-branches.sh (both branches exist as safe
  placeholders) + first /stage push. Deploy branch content is written
  only by /deploy.
- Both splits now capture the working tree (clean-tree requirement
  dropped) and keep branch history via parent commits; `stage`/`save`
  reserved in lint-skills.py; deploy-hostinger 1.5.0.
## v1.9.0 - 2026-07-11 "The Demo Update"
Pre-QA client demos via a hosted staging branch, deployed MANUALLY by
the operator in hPanel (no webhooks or auto-deploy added):
- scripts/demo-split.sh: regenerates `staging` as a generated site-only
  branch (same subtree split + zero-OS-files check as deploy-split.sh,
  NO QA gate - demos are pre-QA by design) and forces a noindex
  robots.txt onto the demo branch so search engines never index a site
  that may still carry [PLACEHOLDER] text. --no-push flag for dry runs;
  optional commit arg like deploy-split.
- /demo command: repeatable any time site/index.html exists; pushes
  staging, operator then deploys manually in hPanel (branch `staging`
  -> demo subdomain's public folder; one-time connect documented in
  deploy-hostinger 1.4.0). Never the client's production domain.
- scripts/bootstrap-branches.sh: fresh-build bootstrap now creates
  missing staging/deploy branches as SAFE site-only placeholders
  (orphan commit: "coming soon" index.html + noindex robots.txt)
  instead of full-repo copies of HEAD - connecting hosting early can
  no longer leak OS files (client.md, state/) into a webroot.
- QA gate untouched: deploy-split.sh, /deploy, and the pre-deploy hook
  are unchanged (hook's staging exemption now documented as the demo
  path); `demo` added to the reserved command names in lint-skills.py.
## v1.8.0 - 2026-07-09 "The Copywriting Update"
Eight agency-ops skills (tier F) distilled from the operator's TRW/HU
copywriting archives, installed in the template by operator decision
(overriding ARCHITECTURE §4's user-level suggestion; they sync via git
with everything else):
- winners-writing-process: mandatory market-research diagnostic before
  any marketing asset (WWP questions, awareness/sophistication, MR
  template, avatar, top player analysis)
- persuasion-mechanics: psychology layer (value equation, attention,
  desire, curiosity, trust/belief, tribal marketing)
- copy-frameworks: drafting skeletons (DIC/PAS/HSO, long-form
  Lead/Body/Close, hooks, storytelling, refinement checklist)
- objections-and-closes: aikido moves, objection bank, CTA laddering,
  boost stack, close library
- funnel-playbooks: Google Ads lead-gen, Meta intro-offer, organic DM
  funnels + selection matrix and pricing
- local-seo-gbp: GBP optimization, review generation, local rankings,
  SEO-vs-ads logic
- cold-outreach: WOSS frame control, email/DM structure, call scripts,
  follow-up cadence
- sales-calls-and-pricing: SPIN bank, call flow, project-math pricing,
  recap emails, upsells, testimonials
Routing boundaries added both directions: copywriting 1.2.1,
audience-research 1.0.1, seo-technical 1.1.1, maps-gbp 1.0.1 point at
the new skills; build pipeline unchanged (agency-side skills, not
build phases). Deliberately excluded from the source archive: INDEX.md
(REGISTRY.md is the index) and the completed niche MRs (overlap with
the audience-research library; distillable later as a
niche-insights-vault if wanted).
## v1.7.1 - 2026-07-08
Phase 2 gate gains a LAYOUT preview beside the style preview:
preview/layout-preview.html - the home page as it will actually be
built (real section order from Phase 1, real grid/spacing via
layout-systems patterns, grey placeholder boxes labeled with the slot
that fills each, placeholder headings at real type sizes) with the
EXACT animation/transition/mobile-nav code Phase 5 will ship (same
css-only/gsap patterns, same tokens, mobile-polish behaviors). Claude
self-checks it on the preview server before presenting. The approved
layout preview is BINDING: layout-systems 1.2.0 reproduces it in
Phase 5 (deviations logged), and /visual-qa compares the built home
page against it.
## v1.7.0 - 2026-07-08 "The Audience Library"
Operator-supplied niche audience studies integrated (11 niches:
roofing, electrician, garage-door repair, paving, concrete, tree
service, home builder, kitchen-bath reno, med spa, physiotherapy,
chiropractor - identical 9-section format ending in Website Conversion
Implications; Ontario market):
- New audience-research skill (tier A): matches the detected niche to
  ONE study, reads it once at Phase 1, distills a ~12-line AUDIENCE
  BRIEF into DECISIONS.md (persona, top pains, deep desire, motivator,
  decision trigger, objections, CTA + trust stack). Downstream phases
  use the brief only (distill-once pattern).
- Precedence: client.md Target Audience outranks the library; studies
  fill the gap when the operator pastes nothing.
- Consumers wired: site-architecture (conversion action + section
  order + trust stack), copywriting 1.3.0 (headline angles, pains in
  the audience's words, objection-answering near CTAs),
  design-direction (emotional register steers no-playbook adaptation),
  build.md Phase 1 (brief distilled before the page map).
## v1.6.1 - 2026-07-07
Branch bootstrap: a fresh /build (Client unset) auto-creates `staging`
(preview branch - QA-gate EXEMPT for client previews, never connected
to hosting) and `deploy`, pushing both when origin is configured. The
generated site-only branch is RENAMED production -> deploy everywhere
(deploy-split.sh, deploy-hostinger, /deploy, build.md, manual diagram);
GitHub Pages now reuses the same generated deploy branch (one deploy
mechanism for both hosts). Hook: pushes naming staging are exempt
unless deploy/production is also named.
## v1.6.0 - 2026-07-07 "The Intake Update"
Six operator changes from build #2 continued:
1. Intake asset sweep: Phase 0 inventories client/assets-intake/
   (logo*, hero1/2*, gallery1/2*, team*, before*/after* naming);
   Phase 4 moves matching files into placement folders, pre-ticks
   their slots (model=client, credits 0) - only gaps get prompts.
2. {Curly-brace} operator comments valid anywhere in client.md -
   stripped globally before parsing (validator, ingest, check.py).
3. Placement folders are PER-PROJECT: named from this site's actual
   page/section map + niche (Home - Hero coffee / About us - Before
   and after), not a fixed set; created empty for drag-and-drop.
4. New `## Target Audience` paste section: site-architecture derives
   the conversion action + section order from it (when Primary action
   is unset); copywriting tailors every CTA to what this audience is
   looking for.
5. Token economy: never narrate reasoning into chat - conclusions only.
6. Grid widow rule: css.md + layout-systems rule 3 - auto-fit strands
   a lone last card when count mod columns = 1; use explicit columns
   or span/center the last item.
## v1.5.0 - 2026-07-07 "Second Iteration Feedback"
Four operator-requested changes from real build #2:
1. In-chat Higgsfield approval: the operator can approve NAMED slots in
   chat; Claude transcribes `YES [in-chat <date>]` to MEDIA_LOG. Hard
   invariant reworded (CLAUDE.md, media-log contract rule 1,
   media-generation rule 1) - blanket permission still never counts.
2. Terminal protocol (CLAUDE.md, always-on): every reply starts
   `[Phase N - name | status]` and ends with `NEXT (you/me): ...` -
   the operator always knows where the build is and what's required.
3. Placement folders + tick semantics (asset-slots v1.1.0): Phase 4
   creates slots/<Page> - <Section>/ folders; list blocks carry a
   folder: line; operator drops the file in its folder and ticks [x].
   /ingest matches recursively by filename (root still works,
   duplicates = conflict), warns on tick-without-file, and lists
   UNFILLED slots as Higgsfield candidates for in-chat approval.
4. New mobile-polish skill (tier B, default-on): phone experience as
   the showpiece - thumb-zone CTAs/sticky action bar, 44px targets,
   16px inputs, :active touch feedback, sheet-style mobile nav, svh +
   safe-area correctness, shorter/faster mobile motion; wired into
   build.md Phase 5 and audited FIRST in the /visual-qa 360 pass.
## v1.4.1 - 2026-07-06 "Adaptive Optimization"
Quality-first within the performance budget, tuned to the hosting plan:
- Priority law (performance rule 0): load/interaction targets are hard
  floors; media quality is maximized WITHIN them.
- Hosting budget profiles via new Overrides "Hosting plan:" field:
  cdn (hostinger-business/cloud: page 1.5MB, hero 2.5/4MB, scrub 10MB)
  vs no-cdn (premium/unknown, fail-safe: 1.0MB, 2/3MB, 8MB + REQUIRED
  Cache-Control headers - block added to security-basics; CDN/cache
  post-deploy checks added to deploy-hostinger).
- /ingest quality ladders: images q90->q82->q75, video CRF 20->23->26,
  scrub 12fps/q80->q70->10fps - each steps down ONLY while over its
  profile budget; report shows kept level + headroom. Pillow fallback
  for images (no cwebp needed); video/scrub/posters need only ffmpeg
  (direct WebP encode).
- check.py page-weight audit: sums each page's real referenced asset
  bytes vs profile caps; FAIL over cap with heaviest-3 named, WARN >80%.
- visual-qa: rendered waste checks (img naturalWidth > 2x displayed,
  below-fold images missing lazy).
- Machine: ffmpeg + Pillow installed - full ingest now runs hands-off.
## v1.4.0 - 2026-07-06 "The Clear Sight Update"
Full-system consistency audit + visual-first debugging:
- Consistency fixes: stale animations.js/hero.js refs (css-only,
  loading-strategy), component-api rule 4 -> shared/main.js (v1.1.0),
  enrichment skips Overrides-answered facts, schema/scaffold sync.
- HOOKS FIXED: python3-based extraction silently failed on Windows ->
  pure-bash extraction, CLAUDE_PROJECT_DIR paths, timeouts, FAIL-CLOSED
  deploy gate; 8 unit tests pass (block/allow/exemption/fail-closed).
- Overrides regrouped under ### sub-headers (Identity/Facts/Conversion/
  Integrations/Media policy/Visual/Stack/Meta) + Audience field added;
  Photos vs Photos-policy disambiguated.
- NEW Phase 2 gate: scripts/generate-style-preview.py renders
  preview/style-preview.html from real tokens (palette, live WCAG
  contrast ratios, type scale, spacing, mock hero) - approve the vibe
  before phases 3-5. Never ships (outside site/, gitignored).
- NEW visual-qa skill (/visual-qa): rendered audit per page at
  360/768/1280 against layout checklist + design rationale + vibe refs;
  wired into /qa as mandatory layer 2; .claude/launch.json preview
  servers added.
- check.py: viewport meta, stylesheet order, img width/height (CLS),
  per-page CSS size + token-bypass warnings.
- Framework acceptance: Stack `framework:` flag (vanilla default,
  react-cdn/tailwind-cdn known, any request honored - never rejected);
  file-structure v2.1.0 Framework exception (CDN+SRI or app/ -> site/).
- OPERATION_MANUAL: full per-phase rundown (does/you/input/outcome) +
  "Last updated" stamp now lint-enforced like the README title.
## v1.3.4 - 2026-07-06 "First-generation accuracy fields"
17 new optional Overrides fields, each with a named consumer:
- Trust facts (copywriting + JSON-LD): Years in business / founded,
  Service area, Certifications / licenses, Price range, Payment
  methods, Emergency / after-hours.
- Conversion steering (site-architecture + seo-technical): Primary
  action (call|book|form|visit|order), Target search terms, Languages.
- Integration IDs (each preempts a QUESTIONS.md stop): Domain,
  Formspree ID, Form notify email, GA4 ID / Plausible domain.
- Media policy (media-generation hard constraints): Photos policy
  (real-only|ai-allowed|mix), People in imagery (yes|no).
- Visual hard constraints (design-direction/tokens): Brand fonts,
  Color mode (light|dark|either), Avoid (visual).
Consumption rules added to copywriting (1.2.0), seo-technical,
site-architecture, media-generation, design-direction, forms,
analytics. Empty values ignored as before.
## v1.3.3 - 2026-07-06
Overrides scaffold: client.md's Overrides section now lists every
available field (contact/hours/services, Pages markup, Links,
Testimonials, Photos, Competitors, Style references, Special requests,
Autonomy, all 7 Stack flags) as ready-to-fill bullet lines with known
values documented in the comment block. Empty values are ignored
everywhere - validator treats an empty flag as unset (no noise), and
the flags-present check now requires a non-empty value.
## v1.3.2 - 2026-07-06
Vibe references are now COMMITTED (gitignore rule removed): operator
works from multiple machines/cloud sessions, so vibe context must
travel with the repo. Deliverable safety unchanged - deploy-split and
/package prove nothing outside site/ ships. Validator adds a SOFT
size nudge for vibe images over 500KB. Docs/schema/client.md wording
updated.
## v1.3.1 - 2026-07-06 "The Vibe Update"
Website vibe as first-class intake:
- client.md gains an optional `## Vibe` section (v2 and v1.1 formats):
  free-text feel description + reference images listed as
  `- vibe/<file>: what to take from it`.
- New drop zone client/assets-intake/vibe/ - GITIGNORED: local-only
  context so Claude understands the aesthetic; never committed, never
  shipped, never copied into site/.
- design-direction 1.2.0: views each vibe image ONCE at Phase 2,
  distills named elements into the DECISIONS.md rationale (the artifact;
  images never re-read - token economy). Vibe outranks playbook
  aesthetics (client.md precedence); playbook conversion must-haves and
  the inspiration-not-duplication rule still apply.
- Validator: SOFT notes for referenced-but-missing vibe images and
  unlisted images on disk; VIBE summary line.
## v1.3.0 - 2026-07-05 "The Shopping List Update"
Streamlined asset creation:
- New contract contracts/asset-slots.md: slot naming grammar, treatment
  vocabulary (loop, intro-loop, scroll-scrub, image, alpha),
  SHOPPING_LIST.md format, MEDIA_LOG mirroring, scrub manifest schema.
- Phase 4 now writes client/assets-intake/slots/SHOPPING_LIST.md - exact
  slot filenames + full copy-paste Higgsfield prompts; operator manual
  generation is the default path (credits 0); paid auto-generation stays
  behind the unchanged approval invariant.
- New /ingest command + scripts/ingest-assets.py: matches slots/ against
  the list, re-encodes video + posters, extracts scroll-scrub frame
  sequences + manifest.json, WebP-converts images (alpha passthrough),
  places outputs per file-structure, ticks the list, updates MEDIA_LOG,
  reports missing/unknown/over-budget. Idempotent.
- hero-media 1.1.0: three new templates - loop-crossfade.js (rAF
  dip-to-black loop), intro-loop.js (intro->loop handoff),
  scrub-player.js (canvas scroll-scrub with progressive frame loading) +
  references/scroll-scrub.md.
- performance: scrub sequence budget (<=10MB, progressive after first
  paint). hero-media flag values extended (loop | intro-loop |
  scroll-scrub). Slot media gitignored; SHOPPING_LIST.md tracked.
- Phase 5 may optionally build with poster placeholders while slots fill.
## v1.2.1 - 2026-07-05
Clean deploy branch: Hostinger auto-deploy now pulls a generated
`production` branch containing ONLY site/ contents at its root.
- New scripts/deploy-split.sh: preconditions (clean tree, site/index.html,
  qa done), `git subtree split --prefix site`, cleanliness check that
  FAILS if any OS path (CLAUDE.md, .claude/, contracts/, state/, scripts/,
  client/, docs/) appears in the split, force-push to production; optional
  commit arg for rollback; graceful no-remote mode.
- deploy-hostinger skill: hPanel points at `production`/public_html (branch
  root IS the site); deploy = run the script; anti-pattern amended to
  "never commit manually to production"; rollback via commit arg;
  first-pull File Manager cleanup checklist item.
- /deploy command routes the Hostinger path through the script.
- pre-deploy-qa-gate hook: matches "deploy-split" too (a `bash
  scripts/deploy-split.sh` command line contains no "git push"); script
  re-checks QA itself.
- OPERATION_MANUAL: Phase 7(c) + deployment rundown diagram
  (main = everything, production = generated site-only, hosting = mirror).
## v1.2.0 - 2026-07-05
Client intake overhaul (paste-based), six changes:
1. client.md v2: Creative / Overrides / Business Profile Paste / Auto;
   every field optional; only blocker = no business name anywhere;
   in-file precedence Overrides > Auto[confirmed] > Auto[unconfirmed]
   (noted in CLAUDE.md ladder level 2).
2. New client-enrichment skill: parses the paste into tagged Auto facts
   ([paste][unconfirmed]), literal-extraction-only, testimonial
   candidates [needs-approval], up to 3 Creative suggestions as HTML
   comments, idempotent regeneration, niche detection → DECISIONS.md.
3. Phase 0 = enrich → validate → ONE confirmation table (Gate 1);
   corrections → Overrides, confirmations → [confirmed]; unconfirmed
   phone/address/hours/prices ship as [PLACEHOLDER] (qa blocks deploy).
4. Validator rewrite: v2 section model, name-only blocker, SOFT notes
   (empty Creative/Paste, missing flags, unparsed paste), v1.1 files
   still validate under old rules, facts summary line.
5. Downstream skills updated: copywriting (Creative primary voice,
   confirmed-facts-only, approved testimonials), design-direction
   (detected niche + Creative mood), site-architecture (Overrides pages
   else playbook), seo-technical (never publish unconfirmed NAP),
   intake-validation (confirmation-table flow).
6. Docs: OPERATION_MANUAL §2/§3/§5/§6 (2-minute setup, Gate 1 table),
   README quick-start, this changelog.
Also: pre-deploy-qa-gate hook gains an OS-maintenance exemption — push
is allowed while no build has started (phase 0 pending); the QA gate
applies unchanged the moment a build is in progress.
## v1.1.0 - 2026-07-03
Change order from the first real test run, six changes:
1. Flags recommend-never-refuse: interpretation principle in CLAUDE.md;
   Stack flags free-text with `placeholder` universal value; unrecognized
   values downgraded BLOCKER->SOFT; placeholder modes in booking, forms,
   email-marketing, analytics; intake writes recommendations to DECISIONS.
2. Pages markup syntax (`page | section / page2 | ...`) documented in
   schema, parsed by validator (malformed = SOFT + corrected reading);
   site-architecture treats it as authoritative, proposes niche must-have
   sections (machine-readable line added to all 5 playbooks).
3. Standalone deliverable: src/+assets/ replaced by site/ (home at root,
   one folder per page, shared/ + assets/ single-sourced); contracts,
   skills, QA script, commands updated; new /package command zipping
   site/ contents to deliverables/ (gitignored).
4. Alpha assets never flattened: PNG explicitly permitted (perf exemption);
   optimize.sh auto-detects alpha and passes PNG through with a printed
   alpha-preservation check.
5. Deploy is a three-way choice at Phase 7 (manual /package, GitHub Pages
   via new reference, Hostinger); manual path ends the workflow at phase 7;
   Phase 8 optional after manual.
6. Token economy: CLAUDE.md section replaced/strengthened; new
   token-economy skill (unverified-savings note included); operator
   practices in OPERATION_MANUAL §11. docs/OPERATION_MANUAL.md created
   (did not previously exist).
## v1.0.0 - 2026-07-02
Initial Agency OS template: constitution CLAUDE.md, 27 skills (tiers A-E),
4 contracts, pipeline commands (/build /qa /deploy /client-edit /handoff
/lint-os), path-scoped rules, 2 enforcement hooks, validation/lint/registry
scripts. Per-client usage: replace client/client.md, run /build.
