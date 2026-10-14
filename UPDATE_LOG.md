# Update Log — HUMAN READ ONLY

<!-- Claude: NEVER read, parse, or summarize this file (CLAUDE.md rule).
     This is the operator's private notebook. It is not a source of
     truth for builds; docs/CHANGELOG.md is the technical record. -->

Personal notes on why each update happened and what to remember.
Write freely — nothing here affects the pipeline.

---

## V1.11.4 — Titles that don't get cut off (2026-08-20)
Dry-ran the new page matrix against a realistic business name and caught
what the short test fixtures had been hiding: "heat pump installation
Richmond Hill | Apex Heating & Cooling" is 61 characters, one over the
cap, and no rule said what to do about it. Now there's a ladder — keep
the brand if it fits, drop the brand on deep matrix pages (the H1, the
NAP block and the schema still carry it), and if my own keyword is still
too long, ship it and log one line rather than quietly rewriting the
thing I asked to rank for. The QA script now warns over 60 characters
and fails on missing or duplicate titles, which the SEO skill had been
assuming QA did all along but nothing actually checked.

## V1.11.3 — One box drives all the SEO (2026-08-20)
"Target search terms" in Overrides is now THE keyword input. Fill it and
those exact phrases become the titles, H1s, schema and the whole page
matrix. Leave it empty and it falls back to a plain [service] [location]
template built from my services and service areas. There is no third
option: the keyword the research agents suggest is a suggestion only,
sitting in the brief for me to copy across if I like it — it never
sneaks into the build on its own.

Service x location pages also actually get generated now (2+ service
areas or 3+ services triggers it), aiming at 30 indexed pages, with
internal linking rules and per-page word counts. The QA script checks
those pages aren't clones of each other, because that's the one way this
kind of page farm goes wrong.

## V1.11.2 — Stop typing what the paste already knows (2026-08-20)
Went through an SEO skill that wanted nine fields typed in by hand and
mapped every one of them to something I already provide. Twelve of the
fourteen needed no work at all. Service area now takes a list
(Markham / Richmond Hill / Vaughan) and gets pulled straight out of the
GBP paste. The target keyword and the local landmarks per area now
arrive from the Phase 1 research agents as visible, correctable
proposals instead of blank fields waiting on me. Net effect: nothing new
to fill in.

## V1.11.1 — WWP modelling and drafting discipline (2026-08-13)
Merged my compiled Winner's Writing Process notes into the two skills
that own each half, rather than dropping in another standalone document.
The research skill gained the real modelling method — find 2-3 pieces of
copy that already got the result, break them down line by line, keep the
skeleton and swap in our specifics — plus the rule that a generic draft
means the research was thin, not that I should grind harder on the
draft. The frameworks skill gained the drafting discipline: filter off
while drafting, multiple hooks, read it out loud, two or three passes,
never ship the first draft.

### Outstanding after this batch
- The earlier usage-audit optimisations are NOT in main. They were
  pushed to a branch that later got deleted, and nothing from them
  survives here: scripts/mark-phase.py, the usage-audit skill and its
  scorecard, allowed-tools on seven skills, the lint nudge for it, and
  the "never read docs/ during builds" line in CLAUDE.md. Redoing them
  is a fresh job if I still want them.
- .claude/settings.json still has no permissions.allow block, so the
  repeated script commands prompt every build. Claude can't edit that
  file (self-modification guard) — it's a manual paste.

## V1.11.0 — The Studio Update (2026-07-29)
The big one. I now fill FOUR things and hit /build: the GBP paste, the
niche, any special requests, and optionally a hero story sentence like
"a car driving and stops at a house".

Phase 0 stopped stopping me. Facts I need to confirm become a checklist
I answer whenever, and the QA script refuses to ship until they're
ticked — so the safety net got stronger, not weaker. Instead of waiting
on me, it hands me one job (go find design references) and immediately
starts Phase 1, where four agents research the market in parallel — what
the top-ranking competitors promise, the exact words customers use in
5-star and 1-star reviews, what people actually search, and what proof
this client can genuinely back — while a fifth drafts copy and a sixth
tears that copy apart. My references and their research now happen at
the same time instead of one after the other.

Phase 2 is now one decision: I get 2-3 named directions side by side and
reply with a letter. Before I ever see it, a fresh agent has tried to
BREAK the preview with real screenshots at three widths — because the
CopperCraft build taught me that "gap: 0px" in the DOM can sit right next
to a visible gap on screen.

Every site gets a real hero now. Write a hero story and it gets built as
a polygon graphic scene that animates on scroll, costing zero credits;
approve it and matching footage slots show up at Phase 4 as an optional
upgrade. Skip the hero story and I get a solid-colour hero where the page
background blends between section colours as you scroll — which is also
what stops every site feeling the same.

Under all of it: Claude is the master, subagents are workers, and a new
contract says workers can never approve a gate, spend media credits,
deploy, or write my state files. Their report format literally has no
field for saying "approved".

## V1.10.0 — The Control Update (2026-07-12)
Deploy is now four separate commands instead of one gated path. /stage
pushes whatever's in my local site/ folder right now — even unsaved
changes — to a demo branch, no questions asked, for a quick client
look. /save just backs up and pushes to main, no gate. /deploy still
runs the QA checks first, but it's advisory now, not a wall — it shows
me what's outstanding (failures, unanswered questions, leftover
placeholders) and I decide whether to push anyway. /demo sets up both
branches fresh and fires the first staging push. Renamed the demo
split script to stage-split.sh to match the new naming.

## V1.9.0 — Pre-QA client demos (2026-07-11)
New /demo command: pushes a staging branch I can point a demo
subdomain at, so clients can see progress before QA and deploy are
done. It automatically forces noindex so search engines never index an
unfinished site. Completely separate from the live deploy branch — I
connect and deploy this one manually in hPanel, and it never touches
the client's real domain.

## V1.8.0 — The Copywriting Update (2026-07-09)
Folded 8 of my TRW/HU copywriting skills straight into the template:
market research (winners-writing-process), persuasion psychology, the
copy-drafting frameworks (PAS/DIC/HSO), objections & closes, cold
outreach, sales calls & pricing, funnel playbooks, and local SEO/GBP.
These now sync with every client clone instead of living somewhere
outside the repo.

## V1.7.1 — Layout preview at the design gate (2026-07-08)
The Phase 2 gate now shows me TWO pages before anything gets built:
the style preview (colors/type/vibe) and a new layout preview — the
actual home page skeleton with grey boxes labeled by asset slot,
real spacing, and the exact animations, transitions and mobile nav
the final build will use. What I approve is what gets built; QA
compares the finished page against it.

## V1.7.0 — The Audience Library (2026-07-08)
My 11 niche audience studies are now built in (roofing, electrician,
garage door, paving, concrete, tree service, home builder, kitchen &
bath, med spa, physio, chiro). When I don't paste custom research into
Target Audience, the build reads the matching study once at Phase 1
and distills an audience brief — persona, pains, motivator, objections,
CTA and trust stack — that drives the page structure and every line of
copy. My pasted research always wins over the library when both exist.

## V1.6.1 — Branch bootstrap (2026-07-07)
Fresh projects now set up their own branches: first /build creates
staging (push work-in-progress there for client previews — QA gate
doesn't block it) and deploy (the generated site-only branch hosting
pulls; renamed from "production" so the names finally make sense).
GitHub Pages and Hostinger now share the exact same deploy mechanism.

## V1.6.0 — The Intake Update (2026-07-07)
Drop files in assets-intake with sensible names (logo.png, hero1.mp4,
gallery1.jpg) and the build finds, sorts, and uses them — only what's
missing gets prompts. Placement folders are now custom per project
(Home - Hero coffee for a café, About us - Before and after for a
roofer). {Curly braces} work as my comments anywhere in client.md. New
Target Audience paste section steers the whole conversion design and
CTA wording. Claude stops narrating its thinking (conclusions only).
Plus the grid widow fix from build #2 (lone card stranded in the last
row) is now law in the CSS rules.

## V1.5.0 — Second Iteration Feedback (2026-07-07)
Fixes from build #2. Approving Higgsfield generation is now one chat
reply (name the slots, Claude records it in MEDIA_LOG) — no more file
editing. Every Claude reply during a build starts with the phase
position and ends with NEXT: so I always know what's needed. The slots
folder now has placement subfolders (Home - Hero, Contact - pictures…)
— drop the file in its folder, tick the list; anything I skip comes
back as a "want me to generate this?" question. New mobile-polish
skill: the phone version is the showpiece — sticky call bar, touch
feedback, sheet nav, slick-but-fast motion, audited first at 360px.

## V1.4.1 — Adaptive Optimization (2026-07-06)
Performance first, quality second — automatically. Ingest now starts
every image/video at high quality and only compresses harder if it
breaks the budget, so nothing gets crushed when there's headroom. The
budget itself now depends on the client's Hostinger plan (new "Hosting
plan:" field): Business has a CDN so it affords bigger assets; Premium
doesn't, so budgets tighten and browser-cache headers become mandatory.
QA now weighs every page's real bytes and names the heaviest files if
over. ffmpeg + Pillow installed — video and image slots now process
fully hands-off, no more PENDING.

## V1.4.0 — The Clear Sight Update (2026-07-06)
Big one: debugging is now visual, not code. Phase 2 generates a style
preview page (palette, contrast ratios, type, mock hero from the real
tokens) that I approve BEFORE anything gets built on top — vibe debug
at the cheapest moment. Phase 6 gained /visual-qa: Claude serves the
site, audits every page at 360/768/1280 against the design rationale
and my vibe refs, and fixes what looks wrong. Also: the QA-gate hook
was silently broken (Windows python issue) — now fixed, tested, and
fail-closed; Overrides got grouped headers + Audience; frameworks are
accepted when requested (vanilla stays the default); the operation
manual now explains every phase (what it does / what I do / what comes
out) and lint forces it to stay current.

## V1.3.4 — First-generation accuracy fields (2026-07-06)
17 more optional Overrides lines that make build #1 land closer: trust
facts (years, service area, certifications, prices, payment, 24/7),
conversion steering (primary action, search terms, languages),
integration IDs (domain, Formspree, GA4 — each one kills a mid-build
question), media policy (real-only vs AI, people yes/no), and visual
hard constraints (brand fonts, light/dark, visual avoids). Fill what I
know, skip the rest — empty lines are ignored.

## V1.3.3 — Overrides scaffold (2026-07-06)
The Overrides section in client.md now shows every field I can force as
ready-to-fill lines (contact, hours, pages markup, links, testimonials,
autonomy, all Stack flags with their known values in the comment).
Empty lines are ignored — fill only what I want, delete nothing.

## V1.3.2 — Vibe files travel (2026-07-06)
Changed my mind on the gitignore: vibe reference images are now
committed so I can work away from my laptop and still have them on any
clone or cloud session. Keep each under ~500KB (validator nags above
that). They still never ship — the deliverable is site/ only.

## V1.3.1 — The Vibe Update (2026-07-06)
client.md now has a ## Vibe section: I describe the feel I want in my
own words and drop reference images/screenshots into
client/assets-intake/vibe/ (gitignored — purely local so Claude can SEE
the aesthetic I'm going for). Claude views them once at Phase 2 and
bakes named elements into the design rationale. References never get
committed or shipped.

## V1.3.0 — The Shopping List Update (2026-07-05)
Asset creation is now streamlined: Phase 4 writes a shopping list into
client/assets-intake/slots/ with exact filenames and full ready-to-paste
Higgsfield prompts. I generate the media myself (keeps credit control),
save each file under its slot name in that same folder, then run
/ingest — it converts everything, extracts scroll-scrub frames, places
files into site/assets/, and logs it all without me touching anything.
Three new hero treatments with ready code: loop (crossfade hides the
cut), intro+loop handoff, and canvas scroll-scrub.
REMEMBER: install ffmpeg + cwebp once, or video slots come back PENDING.

## V1.2.1 — Clean deploy branch (2026-07-05)
Hostinger now pulls a generated `production` branch that contains ONLY
the site files — scripts/deploy-split.sh builds it from site/ and
proves no OS files leak. Never commit to production by hand; the script
is its only writer. Rollback = rerun the script with the previous good
commit.

## V1.2.0 — Paste-based intake (2026-07-05)
client.md v2: I just paste the business's GBP/Maps text into "Business
Profile Paste" and optionally answer Creative questions; Claude parses
facts into an Auto section and shows ONE confirmation table at Phase 0
(reply once — corrections go to Overrides). Only hard blocker is a
missing business name; unconfirmed facts ship as [PLACEHOLDER] and QA
blocks deploy until fixed. 2-minute setup per client.

## V1.1.0 — First test-run change order (2026-07-03)
Fixes from the first real client build. client.md never gets rejected
anymore — weird flag values become recommendations, and every
integration has a "placeholder" mode (build the UI, wire the provider
later). Pages can declare their sections in one line
(home | hero | about / menu | ...). The website now lives standalone in
site/ — zip it with /package, double-click index.html works. Logos keep
their transparency (PNG allowed, no more white boxes). Deploy is a
choice: manual handoff / GitHub Pages / Hostinger. Token-economy rules
added because the first run burned usage way too fast — one session per
phase, /compact between phases.

## V1.0.0 — Initial template (2026-07-02)
The starting point: CLAUDE.md constitution, 27 skills, 4 contracts,
pipeline commands (/build /qa /deploy /handoff /client-edit /lint-os),
enforcement hooks, and the validate/lint/registry scripts. One client =
one clone, only client/client.md changes.
