# Agency OS — Operation Manual

Last updated: v1.13.0
(The lint script fails if this stamp lags the CHANGELOG — every update
must review this manual, especially the §3 phase rundown.)

Operator-facing guide. (Created at v1.1.0 — earlier versions had no
manual; §-references in change orders resolve here.)

## §1 What this is
One repo clone = one client website build, driven by Claude Code.

Three folders, in the order work flows through them (v1.12.0):

```
input/    what YOU fill in - client.md + assets-intake/ (slots, vibe refs)
system/   the brain - contracts/ state/ scripts/ docs/ preview/
output/   the website - THE deliverable, the only thing that ships
```

`CLAUDE.md` and `.claude/` (skills, commands, hooks) stay at the repo
root: Claude Code loads project config only from there, and moving them
would silently disable every skill and slash command. Nothing in
`input/` or `system/` ever reaches the client — the split scripts prove
it on every run.

## §2 Per-client workflow (4 inputs, ~1 minute)
Clone → open `input/client.md` and fill only the four sections above the
END OF REQUIRED INPUT banner:

1. **Business Profile Paste** — dump the GBP/Maps listing, hours,
   services, reviews, old website text. Unstructured is fine.
2. **Niche** — one line ("roofing contractor"). Picks the audience study,
   the design playbook, and the research angle.
3. **Special requests** — optional free text ("needs a French page").
4. **Hero story** — optional one sentence ("a car driving and stops at a
   house"). Becomes a polygon graphic hero at zero media cost; leave it
   empty for a solid-colour hero with scroll-blended section colours.

→ drop any client assets in `input/assets-intake/` → `/build`.

Everything below the banner is optional CONTROL: **Creative** (voice —
the biggest quality delta for 2 minutes of typing), **Vibe** (the feel,
plus reference images), **Target Audience** (only if you already have
research), **Overrides** (hard facts that beat everything). {Curly
braces} anywhere are private notes, stripped before parsing.

**What happens while you work:** Phase 0 does not stop you — fact
confirmations become a checklist in `system/state/QUESTIONS.md` you answer any
time before `/qa`. It hands you ONE job — drop 3-8 design references into
`input/assets-intake/vibe/` (committed, ~500KB each, read once at
Phase 2) — and immediately starts Phase 1 research and copy in parallel.
Your reference hunting and the agents' research happen at the same time.

## §3 Pipeline phases — full rundown

| # | phase | gate |
|---|-------|------|
| 0 | intake | auto — facts deferred, no stop |
| 1 | discovery | - (your reference-hunting window) |
| 2 | design | HUMAN: pick a direction (one letter) |
| 3 | content | - |
| 4 | media | HUMAN: fill slots (or approve paid gen) |
| 5 | build | - |
| 6 | qa | script + deferred facts + visual QA |
| 7 | deploy | HUMAN: choose + confirm |
| 8 | handoff | - |

Roughly **4-5 replies for a whole build**. Claude is the MASTER: it owns
every file write and every gate, and delegates wide work to fresh-context
workers that can never approve anything (system/contracts/agent-protocol.md).

**Phase 0 — intake (no stop).**
Does: inventories your dropped files in input/assets-intake/ (name them
by convention: logo.png, hero1.mp4, gallery1.jpg... and they get used
automatically); resolves your typed Niche to an audience study + design
playbook; client-enrichment parses your Paste into tagged Auto facts; the
validator checks structure; every unconfirmed fact becomes a `- [ ]` row
in system/state/QUESTIONS.md.
You: nothing right now. Answer those rows any time before `/qa` —
corrections go to Overrides. Only hard blocker: no business name anywhere.
Input: the four START HERE inputs.
Outcome: Auto facts + deferred-confirmation checklist; Phase 1 launched in
the same turn; your one job is dropping vibe references.
Why it is safe to defer: unconfirmed phone/address/hours/prices still
render `[PLACEHOLDER: ...]`, and the QA script fails both on placeholders
and on any unanswered row — enforcement moved from a chat prompt to a
script, which is stronger.

**Phase 1 — discovery (agents work while you hunt references).**
Does: distills an audience brief from the niche study library (11 niches),
then runs FOUR research agents in parallel — top players ranking in your
market, verbatim customer language from 5★ and 1★ competitor reviews,
search-intent clusters, and what proof this client can actually back —
and synthesizes one RESEARCH BRIEF. Then the page map, then the
visual-independent copy (both hero registers, section headings, objection
blocks, FAQ, about), then an adversarial critic pass over those drafts.
Every research line is provenance-tagged; only client-sourced material can
ever become a published claim, and anything unfound is left out rather
than invented.
You: gather design references into input/assets-intake/vibe/.
Input: the Niche, the Paste, the audience study.
Outcome: audience brief + research brief + page map + section lists in
system/state/DECISIONS.md; copy drafts in system/state/COPY_DRAFTS.md.

**Phase 2 — design (the one taste gate).**
Does: 2-3 agents each build a DIFFERENT labelled direction as a swatch —
palette, type specimen, hero mock, one section mock — in
system/preview/direction-variants.html. Claude recommends one, then builds it
for real: tokens.css, system/preview/style-preview.html (live WCAG contrast),
and system/preview/layout-preview.html (the home page as it will actually be
built — real section order, real grid and spacing, labeled grey
placeholder boxes naming the slot that fills each, the section colour
progression running, your hero concept as it will ship, and the EXACT
animations, transitions and mobile-nav behavior Phase 5 will use). A
fresh agent then tries to REFUTE that preview — with real screenshots at
360/768/1280, because DOM measurements cannot see a rendered gap — and
also answers "could a competitor paste this unchanged?" Defects are fixed
before you ever see it.
You: reply with ONE letter. That is the whole gate. The approved layout
preview is binding for the build.
Input: Vibe section + images, Mood, Brand fields, niche playbook, the
research brief's words-to-use/avoid.
Outcome: tokens.css + named direction, named hero concept, and section
colour progression in DECISIONS.md; binding layout preview; phase 2 done.
While you decide, Claude drafts ahead: page skeletons, SEO metadata, and
the slot name list.

**Phase 3 — content.**
Does: places the Phase 1 copy drafts into the skeletons, writes what the
direction governs (hero, headlines, CTA voice), and PICKS the hero
register against the approved rationale — a quiet-luxury direction cannot
carry a shouty headline, which is why the pick waited. One agent per page,
each leased only its own file. Unconfirmed facts render as [PLACEHOLDER].
You: nothing (answer any deferred rows when convenient).
Input: copy drafts, confirmed facts, Creative, architecture, rationale.
Outcome: every section of every page has real copy in output/.

**Phase 4 — media (gate).**
Does: media-generation writes the shopping list — exact slot filenames,
treatments, specs, full copy-paste Higgsfield prompts. Hero-story footage
appears here ONLY if you approved the polygon graphic hero at Phase 2, is
named for the same beats, and is marked an upgrade — the graphic hero
already ships if you skip it. No hero story means no hero media slots at
all.
You: generate at your pace, drop each file into its placement folder
(slots/<Page> - <Section>/) under the exact slot name, tick [x] on the
list, run /ingest. Slots you skip come back as Higgsfield candidates —
approve them with one chat reply naming the slots. Optionally let the
build proceed with poster placeholders.
Input: design rationale imagery style, section list, hero-media flag.
Outcome: processed assets in output/assets/ at the highest quality the
performance budget allows (adaptive ladder, tuned to the Hosting plan
field; + scrub manifests), MEDIA_LOG
rows in-use, list ticked.

**Phase 5 — build.**
Does: layout-systems + components + hero-media treatments +
frontend-animation + mobile-polish (phone experience as the showpiece,
default-on) + integrations (per Stack flags, incl. placeholder slots
and the framework flag) assemble the complete standalone output/. Then
the FINISHING PASS, always: seo-technical (titles, meta, OG, JSON-LD,
sitemap, robots), image-optimization (anything that skipped /ingest),
security-basics (.htaccess headers), and legal-pages whenever the site
collects anything at all.
You: nothing.
Input: tokens, copy-filled skeletons, ingested assets, contracts.
Outcome: finished output/ per file-structure contract.

**Phase 6 — qa (gate: must pass).**
Does: three layers — check.py (placeholders, refs, viewport, stylesheet
order, img sizing, token bypass, drift), /visual-qa (rendered audit of
every page at 360/768/1280 against the layout checklist + design
rationale + vibe refs, with fixes), then the manual fact/click-path
review.
You: nothing until it reports; spot-check anything it flags as accepted.
Input: built output/, DECISIONS.md rationale, vibe refs.
Outcome: per-page PASS block + results in BUILD_STATE notes; phase 6
done only when all three layers pass.

**Phase 7 — deploy (gate).**
Does/You: answers "Deploy how? (a) manual, (b) GitHub Pages,
(c) Hostinger" — see the deployment rundown below.
Outcome: live site (b/c) or deliverables zip (a) + record in BUILD_STATE.

**Phase 8 — handoff.**
Does: writes system/docs/HANDOFF.md (live URL, what was built, retainer scope,
how to request changes, credentials checklist — names only).
You: send it to the client. Optional after a manual deploy.
Outcome: handoff doc; workflow COMPLETE.

Phase 7 asks exactly: **"Deploy how? (a) manual — I'll hand off files
myself, (b) GitHub Pages from this repo, (c) Hostinger Git."**
- (a) manual: /package zips output/ contents to deliverables/; BUILD_STATE
  records `deploy: manual — packaged <zip path>`; phase 7 done; Phase 8
  offered, skippable — the workflow is COMPLETE either way.
- (b) GitHub Pages: deploy-hostinger references/github-pages.md
  (deploy-branch approach recommended); QA-gate hook applies to the push.
- (c) Hostinger Git: `bash system/scripts/deploy-split.sh` regenerates the
  site-only `deploy` branch and force-pushes it; the Hostinger
  webhook pulls it into public_html. Rollback: rerun the script with the
  previous good main commit as its argument.

Deployment rundown — the four control verbs (placeholder branches
auto-created at fresh-build start by system/scripts/bootstrap-branches.sh —
safe site-only stubs, so hosting can be connected at any time). Both
split scripts snapshot the CURRENT LOCAL output/ files (uncommitted +
untracked included) to the branch root:
```
main     = everything (OS + output/), the working branch
staging  = generated demo: local output/ snapshot at branch root +
           forced noindex robots.txt; NO gate (pre-QA by design);
           connect ONLY to the operator's demo subdomain
deploy   = generated live target: local output/ snapshot at branch
           root, zero OS files (proven on every run); QA advisory +
           the operator's explicit go
hosting  = manual hPanel Git pulls (staging -> demo subdomain,
           deploy -> public_html)

edit ──/stage──> stage-split.sh ──> staging ──hPanel pull──> demo subdomain
edit ──/save───> commit all + push ──> origin/main (backup/sync)
edit ──/deploy─(QA advisory + your go)──> deploy-split.sh ──> deploy ──hPanel pull──> live
/demo = bootstrap both branches + first /stage
```
Never commit manually to staging or deploy — their split scripts are
the only writers. On the FIRST Hostinger pull, check File Manager: the
target folder must contain only site files (leftovers from earlier
manual uploads — zips, .claude/, package.json, README, serve.ps1 —
have burned an operator before).

## §4 Commands
/build /qa /demo /stage /save /deploy /package /ingest /handoff
/client-edit /lint-os —
each is a file in .claude/commands/. /visual-qa is the visual-qa skill
invoked directly (skills are natively slash-invocable).

## §4.1 The asset-slot workflow
Phase 4 writes `input/assets-intake/slots/SHOPPING_LIST.md` — one block
per asset: exact filename, its placement folder, treatment, spec, and a
full copy-paste Higgsfield prompt — and creates the placement folders
(`Home - Hero/`, `Contact - onscreen pictures/`, ...). You generate at
your own pace, drop each file INTO ITS FOLDER under the exact slot
name, tick `[x]` on the list, run `/ingest`. The script converts
(adaptive quality ladder), extracts scrub frames + manifests, places
everything under output/assets/, updates MEDIA_LOG, and reports. Slots
you left unfilled come back as Higgsfield candidates: Claude asks you
in-chat (named slots + estimated credits) and generates ONLY what you
explicitly approve — approval is one chat reply now, no file editing.
Slot media files are gitignored (only the list is tracked).

## §5 Key files
input/client.md — v2 paste-based brief: Creative (hand-written) /
Overrides (owner-typed facts, beat everything) / Business Profile Paste
(raw GBP dump) / Auto (machine-written parsed facts; never hand-edit).
system/state/BUILD_STATE.md (resume point), DECISIONS.md (resolved ambiguities +
claude-proposed recommendations), QUESTIONS.md (open client questions),
MEDIA_LOG.md (paid-media ledger + approval gate).

## §6 Human gates
- Gate 1 (Phase 0) — REMOVED as a stop in v1.11.0. Parsed facts become a
  `- [ ]` checklist under "Fact confirmations (deferred from Phase 0)" in
  system/state/QUESTIONS.md; answer any time before `/qa`. Corrections land in
  Overrides; confirmed facts flip to [confirmed]. The safety net is
  stronger, not weaker: unconfirmed phone/address/hours/prices ship as
  [PLACEHOLDER], and check.py fails on placeholders AND on any unanswered
  row. `Autonomy: low` restores the old blocking table. The only hard
  blocker remains: no business name found anywhere.
- Gate 1b (Phase 2): pick a direction. system/preview/direction-variants.html
  shows 2-3 labelled directions as swatches; system/preview/layout-preview.html
  shows the recommended one built for real — home-page layout, labeled
  asset placeholders, section colour progression, your hero concept, and
  the exact animations/transitions the build will ship. A fresh agent has
  already tried to refute it with screenshots at 360/768/1280 and fixed
  what it found. Reply with ONE letter. The approved layout preview is
  binding for Phase 5. Skipped at Autonomy: high.
- Gate 2 (Phase 4): fill the shopping-list slots yourself (default,
  credits 0), or approve paid generation for the slots you skipped —
  one in-chat reply naming the slots (Claude records
  `YES [in-chat <date>]` in MEDIA_LOG), or type YES in the file
  yourself. Blanket "generate whatever" never counts — never
  delegable, protects paid credits.
- Gate 3 (Phase 7): the three-way deploy choice above. Choosing (a)
  manual ends the workflow at phase 7 done + package path recorded;
  (b)/(c) proceed to push-based deploy under the QA-gate hook.

## §7 The deliverable
`output/` per system/contracts/file-structure.md: home at output/ root, one folder
per additional page, shared/ + assets/ single-sourced. Double-clicking
output/index.html must work; /package ships exactly this.

## §8 Retainer edits
/client-edit <request> — minimal surgical edits under
maintenance-retainer rules; reduced QA; deploy per the client's mode.

## §9 Maintaining the OS
/lint-os after skill edits; system/scripts/generate-skill-registry.py refreshes
system/docs/REGISTRY.md; template versions in system/docs/CHANGELOG.md. Every version
bump updates: the README title "Agency OS(Vx.y.z) — ...", AND this
manual's "Last updated: vX.Y.Z" stamp (reviewing the §3 phase rundown
for accuracy). lint-skills.py enforces BOTH against the latest
CHANGELOG entry — an update that skips the manual fails lint.

## §10 Troubleshooting
Pipeline stuck → read system/state/BUILD_STATE.md notes. Validation refusing →
it shouldn't: only a missing business name blocks (interpretation
principle); unrecognized values are soft. Push blocked → phase 6 not
done, run /qa. Site looks wrong → this is a visual bug, not a code
bug: run /visual-qa (layout debug) or reopen
system/preview/style-preview.html (vibe debug) rather than reading code.

## §11 Usage economy (operator side)
Context re-sent every turn is the biggest hidden cost multiplier. Do:
- **One session per phase** (or per 2-3 phases) instead of a marathon:
  BUILD_STATE.md makes resume free; short sessions avoid paying for a
  huge accumulated context on every single message.
- **/compact at phase boundaries** if staying in one session.
- **Model choice:** Sonnet for phases 3/5/6 (content, build, qa); Opus
  only for phases 1/2 and hard debugging.
- **/context** to audit what's actually loaded when a session feels heavy.
- **Keep client.md tight** — it is read early and often; every stray
  paragraph is a recurring tax.
- The in-session levers live in the token-economy skill; behavioral
  always-on rules live in CLAUDE.md "Token economy".
