# RESEARCH BRIEF template

Copy this shape literally into `system/state/DECISIONS.md`. It is the only
permitted output format. Omit any subsection with no evidence and leave a
`not-found:` line in its place - never fill a section to make it look
complete. Target 70 lines or fewer; three later phases re-read this.

Every line carries an evidence tag. `[client]` is the ONLY tag whose content
may become a published claim about the business.

```
## RESEARCH BRIEF — <business> | <niche> | <city, prov>
generated: <YYYY-MM-DD> | evidence: <web+prior+client | prior+client | client-only>
prior: <study.md | none> (<exact|adjacent|none>) · playbook: <file.md> (<exact|adjacent|closest-by-mode:<mode>>)
agents: <n> run, <n> returned | sources: <n> | tags: [client] [prior] [web:verified] [web:unverified] [model]

### Diagnosis
- Awareness level <1-4>: <what they already know when they land> [tag]
- Sophistication stage <1-5>: <what the market is tired of> [tag]
- Desire <n>/10 · Certainty <n>/10 · Trust <n>/10 — lowest is <x>, so the site's first job is <...> [tag]
- Roadblock: <the one thing blocking them> [tag]
- Solution: if they <solution>, then <dream outcome> [tag]
- Product: how this business makes that faster/safer/easier/more certain [tag]

### Avatar
- <label>, <age band>, <situation>. The moment they search: <trigger>. Device/context: <...> [tag]

### Verbatim phrase bank — the CUSTOMER'S words, never the business's claim
PAINS
- "<verbatim>" [web:verified · 1★ · <source>]
DESIRES
- "<verbatim>" [client · review in paste]
OBJECTIONS
- "<verbatim>" [web:unverified · <source>]
DELIGHT TRIGGERS
- "<verbatim>" [web:verified · 5★ · <source>]
not-found: <subsection> — <why>

### Top players (<n> analyzed)
| player | hero promise | primary CTA | trust stack | offer/guarantee | price shown | reviews | tag |
|---|---|---|---|---|---|---|---|
- Table stakes (everyone does this — we must too): <...>
- Gap (nobody does this — our wedge): <...> [tag]
- Keyword candidate: <service + city keyword> — difficulty <easy|medium|hard|unknown> (avg <n> reviews across players) [tag] — superseded by Overrides `Target search terms` if filled

### Search intent map
| query cluster | intent | answered by (page · section) | tag |
|---|---|---|---|

### Local details (per service area)
| service area | landmark / neighbourhood / corridor | tag |
|---|---|---|
not-found: <area> — <why>

### Offer sheet — client-side only
- Services / packages: <...> [client]
- Guarantee / risk reversal: <text or "none stated"> [client]
- Price posture: <published | ranges | quote-only | unknown> [client]
- PROOF WE HAVE: <...> [client]
- PROOF WE LACK (→ QUESTIONS.md; ships as [PLACEHOLDER] until answered): <...>

### Build directives — binding on Phases 1-3
- Primary conversion action: <call | book | form | visit | order> — because <...>
- Hero angle: <...> · registers to draft: A <...> / B <...>
- Section order consequence: <...>
- Objections to pre-answer, in order: 1 <...> 2 <...> 3 <...>
- Trust stack, in order: 1 <...> 2 <...> 3 <...>
- Words to use: <...> · Words to avoid: <...>

### Conflicts
- <client fact> vs <web finding> → resolved toward client. [client]

### Human check (5 min, non-blocking)
- [ ] <highest-leverage line to eyeball> — <source>
- [ ] <...>
```

## Notes on specific fields

**`evidence:` stamp** — set once, from what actually ran. It tells every
later phase how much weight the brief carries. `client-only` means the
diagnosis is inference; say so in the Human check too.

**Diagnosis** — this is the winners-writing-process diagnostic, filled. The
awareness level dictates the opening move; the sophistication stage dictates
whether to make a bigger claim or out-position instead. The lowest of the
three scores names the site's first job.

**Verbatim phrase bank** — the highest-value section, and the one most
likely to be faked. A phrase that cannot be quoted exactly does not belong
here. Star rating matters: 1-star reviews of competitors are where
objections come from, 5-star reviews are where delight triggers come from.

**Build directives** — the only section later phases are REQUIRED to obey.
site-architecture takes the primary action, section-order consequence,
objection order, and trust stack; copywriting takes the hero angle,
registers, and the words lists. Explicit `Overrides` values in client.md
still outrank this section.

**Conflicts** — a real disagreement between a client fact and a web finding
is worth one line and is always resolved toward the client. Do not resolve
it silently; the operator may want to know their GBP contradicts their site.

**Keyword candidate / Local details** — different consumption rules.
KEYWORD CANDIDATE is advisory only: it exists so the operator can SEE a
well-researched option and copy it into Overrides `Target search terms`
if they like it — the build itself never reads the candidate directly.
Downstream, exactly two states exist (client.schema.md, site-architecture
references/service-location-matrix.md): `Target search terms` filled →
use it; empty → the generic `[service] [location]` template, never the
candidate. Local details ARE consumed directly (no operator step needed)
to give location-page copy a real, findable specific instead of generic
filler — they carry no keyword-selection weight, only color.
