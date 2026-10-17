# Decisions Log
<!-- Besides the one-line format below, this file holds ONE fixed block
     written by Phase 2 and regenerated in place, never duplicated: the
     BRAND block (colour source: palette / logo / niche default, the hexes,
     fonts, and any contrast adjustment). -->
<!-- Resolved ambiguities. Once logged here, a decision outranks skills
     and contracts (precedence level 4). Format:
     YYYY-MM-DD | topic | decision | decided-by (human/claude) | why -->

2026-10-15 | prospect | generic HVAC pitch: Business name = [PLACEHOLDER: HVAC business name]; Niche = HVAC; all client facts ship as placeholders | human | operator in-chat: "just run a generic HVAC, placeholders for all the client information for now"
2026-10-15 | niche-resolution | niche: HVAC | study: electrician.md (adjacent) | playbook: hvac (exact) | by: operator
2026-10-15 | sources | page copy uses ONLY the research PDF + client.md; system/preview/research-audit.md (web research) is context for the operator, never a page source | claude | content rules 1-2 + no-invented-facts invariant
2026-10-15 | reviews | fireplace review ("Max ... century-old fireplace") left off the page: not HVAC work | claude | reversible - re-add from pdf p.1 if wanted
2026-10-15 | reviews | ice build-up review trimmed with a leading ellipsis, dropping the sentence that names Mr. Heat Mechanical | claude | a generic pitch must not name a third business in a 1-star quote; content rule 3 allows ellipsis trims
2026-10-15 | quotes | spaces restored where the PDF wraps a line mid-quote (verified with pypdf layout mode) | claude | extraction artifact, not rewording
2026-10-15 | creative | Creative 1 platform = facebook feed, aspect 4:5 | claude-proposed | client.md Creative 1 empty; research Platform "Meta ads" (pdf p.4); 4:5 is the feed default
2026-10-15 | competitors | card titles use the domains as the research records them; TPA typos fixed ("Plumming" -> "Plumbing", "247" -> "24/7", "7500" -> "$7,500") | claude | content rule 2 (fix grammar, plain words)
2026-10-15 | design-rationale | 1 direction: "Cold front, warm front" - the page walks the owner from their customer's cold, worried winter to warmth and certainty, mirroring the research's own arc ("Home feeling cold already?" -> "stay warm this winter")
2026-10-15 | design-rationale | 2 type: sturdy gauge-like sans for headings (Bahnschrift / DIN Alternate system stack, tabular numerals for scores); plain system UI body. No webfonts (no CDN; nothing to self-host yet)
2026-10-15 | design-rationale | 3 colour: hvac playbook - furnace-steel blue primary #1d4f7c, one warm ember accent #b8501b used scarcely (60-30-10), cool-to-warm tinted neutrals; light scheme
2026-10-15 | design-rationale | 4 imagery: none generated; real screenshots only (reviews, competitors, creative) in browser/device frames; small line-icon glyphs in CSS only
2026-10-15 | design-rationale | 5 layout personality: straightforward, zero cleverness (playbook); one idea per section, generous whitespace, presentation-deck rhythm (one section = one slide)
2026-10-15 | design-rationale | 6 distinctive element: the THERMAL PROGRESSION - 12 section backgrounds walk icy blue -> neutral -> warm ember cream, and the presentation progress bar is a thermometer that warms from blue to ember as you advance
2026-10-15 | design-rationale | 7 hero concept: "cold-front cover" - solid-colour cover on --section-bg-1 (no hero story, no media), large prepared-for line, a thermometer rule under the title; the progression is the hero
2026-10-15 | design-rationale | 8 signature component: the threshold meters render as thermometer gauges (before -> after), the gap section is the warmest-but-one step and the page's climax
2026-10-15 | design-rationale | 9 motion: subtle, CSS-only (no Stack flag -> css-only); reveal-on-scroll + background blend, all gated by prefers-reduced-motion
2026-10-15 | design-rationale | 10 anti-generic test: a competitor could not paste this - the arc is this research's winter pain -> warm-home desire, and the gauges show this research's own 6/4/4 -> 8/8/7 scores
2026-10-15 | contracts | design-tokens contract v1.2.0 -> v1.3.0: appended --section-bg-N + --page-bg-blend (contract rule 4: add to the contract first) | claude | the design-tokens, layout-systems and frontend-animation skills already emit/consume them; additive, non-breaking

## BRAND
- source: niche default (no client.md palette, no logo) - hvac playbook
- primary #1d4f7c · primary-dark #13314f · accent #b8501b · bg #f6f8fb · surface #ffffff · text #0f1c2b · text-muted #46566a · border #c9d3df (decorative only) · success #1d7048 · error #b42318
- progression (12): #e6eef8 -> #eaf1f8 -> #eef3f8 -> #f1f4f7 -> #f4f5f6 -> #f6f5f2 -> #f8f3ec -> #faf0e4 -> #fbede0 -> #fcebdc -> #fdeee2 -> #fef2e8 (text >= 14.7:1, muted >= 6.4:1 on every step)
- fonts: heading "Bahnschrift", "DIN Alternate", system fallbacks · body system-ui stack (no webfont files)
- contrast adjustments: none needed; ember accent is text-safe (4.7:1 on bg, 4.54:1 on the warmest step; white label on it 5.0:1); --color-border is 1.4:1 so it is never a control's only boundary
2026-10-15 | design-rationale | correction to line 8: the gap section is the page's ONE dark full-bleed band (primary-dark, opts out of the blend) - the climax; meters are 10-segment gauges matching the 10-tick thermometer rule on the cover | claude | built that way in Phase 3
2026-10-15 | layout | presentation layer, colour progression, shared type, motion and print rules live in shared/base.css (print selectors carry an html prefix to outrank style.css); style.css still 23KB (QA warn, not fail) | claude | page-css size budget
2026-10-15 | customer | desire "Warmth and comfort that transform the room" dropped: it comes from the same fireplace review already left off | claude | pre-gate review nit 9, consistency
2026-10-15 | mental-chain | quoted thoughts now use the research wording (grammar fixed only) instead of paraphrase | claude | pre-gate review nit 8: quote marks imply verbatim
2026-10-15 | competitors | "$7,500" kept (research shorthand "Up to 7500 Government rebate"); Phase 6 facts pass to treat "$" as the logged typo fix | claude | pre-gate review nit 10 - reversible
2026-10-15 | logo | text-logo placeholders inside ingest:logo markers stay unwrapped (ingest rewrites them each run); still caught by QA as [PLACEHOLDER | claude | pre-gate review nit 12
2026-10-15 | presentation | Left/Right/PageUp/PageDown/Space page by 0.85 of the screen inside sections taller than the viewport, then jump to the next section; Home/End jump | claude | pre-gate nit 5: a slide clicker skipped content; component-api row also says 'never hijacks normal scrolling'
