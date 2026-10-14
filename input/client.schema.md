# client.md Schema  (PresentationOS v2.0.0)

`input/client.md` is the prospect sheet. It is short on purpose: the
substance of every pitch lives in the research file
(`input/research/`), which follows the operator's WWP Structure. Checked
by `system/scripts/validate-client-md.py` at Phase 0.

Parsing: HTML comments and `{curly brace notes}` are stripped first.
Fields are `- Key: value` lines under `## Section` headings.

## Sections

| section | field | required | rule |
|---------|-------|----------|------|
| Prospect | Business name | **BLOCKER** | The only client.md blocker. |
| Prospect | Website, Location, Niche | no | Niche drives the default design when there is no logo/palette. |
| Research | File | conditional | Blank is fine when input/research/ holds exactly one .pdf or .md file (or one folder of .md files = a Notion export). No research file at all = **BLOCKER**. Several and none named = **BLOCKER**. |
| Brand | Palette | no | Hex codes (`#1f6feb, #f59e0b`) or plain words ("navy and gold" - interpreted, logged). First = primary, second = accent. |
| Brand | Fonts | no | Font names; blank = chosen by design-direction. |
| Creative | `### Creative N` blocks: Type, Platform, Aspect, Headline, Primary text, CTA | soft | At least one block expected. Unknown types/platforms are interpreted (interpretation principle), never rejected. Empty copy fields render as [PLACEHOLDER]. |
| Demo website | URL | no | Must start with http(s). Present = the `website` section is shown. |
| Sections | Hide, Show, Order | no | Comma-separated ids from system/contracts/pitch-sections.md. Unknown ids = soft warning. |
| Notes | free text | no | Read at Phase 1; interpreted, logged. |
| Agency | Agency name, Prepared by, Contact / booking link, Hosting plan, How I help, Process / next step | soft | Filled once in the template. Empty = [PLACEHOLDER] in the `next` section. Hosting plan sets the QA page-weight budget (business/cloud = CDN profile). |

## Precedence inside a build

client.md (operator-typed) > research file > system/state/DECISIONS.md.
When client.md and the research disagree on a fact, client.md wins and
the disagreement is one line in DECISIONS.md.

## Research file

The WWP Structure, in order: 1. Profile the buyer (target market,
customer language: good/bad reviews, current-state pains, dream-state
desires) - 2. Market Research (roadblocks, possible solutions, what
they've tried, how they pick a provider, awareness level, attention,
platform, TPA, THE GAP) - 3. CIA Interview - 4. Engineering (main action,
thresholds, the gap, mental chain, the creative second by second).
Section mapping to the page: system/contracts/pitch-sections.md.
Reading limits: PDFs over 10 pages need poppler (pdftoppm) or `pypdf`
for text extraction; a Notion Markdown export has no limit and is read
exactly.
