# Contract: Pitch Sections  (v1.0.0)

The pitch page is ONE educational landing page (output/index.html) that
walks the prospect through the operator's research, the gap, and the
proposed creative. This contract is the interface between Phase 1 (content
map), Phase 3 (draft) and /ingest: section ids, order, sources, components.

## Section map (default order = the WWP Structure order)

| # | id           | default H2 (adapt to voice)      | source                                                    | component(s)                         | default |
|---|--------------|----------------------------------|-----------------------------------------------------------|--------------------------------------|---------|
| 1 | cover        | Prepared for {business}          | client.md Prospect + WWP "target market (in one breath)"  | cover                                | on |
| 2 | method       | How I researched your market     | FIXED CONTENT below                                       | track-diagram                        | on |
| 3 | customer     | Who your customer is             | 1. Profile the buyer: Current State pains, Dream State desires | pain-desire                     | on |
| 4 | reviews      | What your customers are saying   | Customer Language: Good Reviews / Bad Reviews             | quote-list + proof-carousel(reviews) | on |
| 5 | roadblocks   | What's stopping them             | 2. Market Research: Roadblocks, All possible solutions, What they've already tried, The Product (look for / distrust) | card-grid | on |
| 6 | awareness    | Where your customer is right now | Awareness Level, Attention, Platform                      | awareness-grid                       | on |
| 7 | competitors  | What your competitors are doing  | TPA (top player analysis): working / missing per player   | competitor-cards + proof-carousel(competitors) | on |
| 8 | gap          | The gap                          | THE GAP (Market Research) + The Gap (Engineering)         | gap-statement                        | on |
| 9 | mental-chain | How your customer decides        | 4. Engineering: Mental Chain                              | chain-steps                          | on |
| 10| plan         | The plan                         | Main Action + THRESHOLDS (Desire / Certainty / Trust)     | threshold-meters                     | on |
| 11| creative     | The creative                     | The Creative (total seconds + second-by-second) + client.md Creative blocks | storyboard + creative-frame | on |
| 12| website      | Your new website                 | client.md Demo website                                    | device-frame                         | only when a URL is given |
| 13| next         | How I help                       | client.md Agency                                          | agency-block                         | on |
| - | interview    | How we'll validate the gap       | 3. CIA Interview                                          | qa-list                              | OFF (internal) |

`client.md ## Sections` may hide any section, show `interview`, or
reorder. Section ids are stable anchors (component-api rule 6).

## Content rules

1. Every per-prospect line traces to the research file or client.md and
   carries its source tag in the content map (system/state/COPY_DRAFTS.md):
   `[pdf p.N: <field>]` or `[client: <section>]`.
2. Allowed edits: shorten, fix grammar, turn research shorthand into plain
   words a business owner reads in one pass. NEVER add a claim, number,
   score, review, quote or competitor fact the source does not contain.
3. Review quotes are verbatim (customer language is the point). Trim with
   an ellipsis only; never reword inside quotation marks.
4. Empty source field -> `[PLACEHOLDER: <what is missing>]` in the page +
   one row in system/state/QUESTIONS.md. The operator fills it or hides
   the section; QA fails while any placeholder remains.
5. Connective copy (section intros, transitions) is neutral and fact-free,
   one or two sentences max, written in plain second person ("your
   customers"). The page talks TO the prospect.
6. Tone: educational, confident, specific. Show the work; no hype words.

## Fixed content (same on every pitch - edit here, not per build)

### method - two research tracks -> one opportunity

- Track 1, Customer language: I read what your customers actually write
  (good reviews, bad reviews, before-and-after stories) and pull out
  their exact words: what hurts, what they want, and what they won't put
  up with.
- Track 2, Competitive landscape: I study your direct competitors and the
  top players in your category: what they say, what's working for them,
  and what they're leaving out.
- Opportunity: where the two tracks meet. The thing your customers care
  about that nobody is saying. That's the gap, and it's the angle your
  ads are built on.

### awareness - awareness x attention grid

Rows (awareness): Unaware (doesn't know they have the problem) ->
Problem aware (feels the pain, doesn't know the fix) -> Solution aware
(knows fixes exist, comparing options) -> Product aware (knows you,
deciding if you're right).
Columns (attention): Passive (not looking; scrolling, going about their
day) | Active (searching for a fix).

| awareness \ attention | Passive                                                                 | Active |
|-----------------------|-------------------------------------------------------------------------|--------|
| Unaware               | Disruption: story-style ad or video + long-form content + offer. Grab attention with a pain or dream they recognise. | Not searching yet. |
| Problem aware         | Interrupt: social ad + education page + intro offer. Name the pain, reveal the new solution. | "How do I fix...": articles / YouTube + email capture + follow-up. Answer the question, then sell. |
| Solution aware        | Differentiation: social ad + "why we're different" page + offer. Show why you're the best version of the solution. | Search: Google ads / SEO + landing page + booking. Stand out at the moment they search. |
| Product aware         | Retargeting: retargeting ad + offer page. Give them a reason to act now. | Branded search: branded search ad + booking page. Remove friction, take the booking. |

Rule of thumb under the grid: start with what they know, then show them
what's next. Highlight the cell(s) matching the research's Awareness
Level + Attention; show the research's Platform as a chip beside it.

## Media hooks (filled by /ingest - see asset-slots contract)

Phase 3 writes these marker pairs into index.html; /ingest replaces only
what sits between them and never touches anything else:

    <!-- ingest:reviews -->      ... <!-- /ingest:reviews -->
    <!-- ingest:competitors -->  ... <!-- /ingest:competitors -->
    <!-- ingest:creative-N -->   ... <!-- /ingest:creative-N -->   (one per client.md Creative block)
    <!-- ingest:logo -->         ... <!-- /ingest:logo -->         (cover + each ad-mockup avatar)
    <!-- ingest:website -->      ... <!-- /ingest:website -->      (only with the website section)

A pair may repeat (the logo does); /ingest fills every occurrence.
Until media arrives, each pair holds a visible empty state containing
`[PLACEHOLDER: drop files into input/<folder>/ and run /ingest]`.
