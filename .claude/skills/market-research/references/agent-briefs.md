# The five agent briefs

Dispatch agents 1-4 in ONE message so they run in parallel. Agent 5 runs
later, after copy drafts exist. Every brief below is a template: fill the
angle brackets, keep everything else verbatim.

All five are READ-ONLY (no lease). All five return only the report block
from `system/contracts/agent-protocol.md` section 3. None of them writes system/state/,
approves anything, or addresses the operator.

## Shared preamble (prepend to all five)

```
ROLE 1.<role>. Fresh context: assume nothing about this build.
LAW: system/contracts/agent-protocol.md applies in full. You are a WORKER:
     read-only (no lease), never write system/state/, never approve anything,
     return one report block and nothing else.

PRIOR DIGEST (the cached niche hypothesis - confirm, refine, or CONTRADICT
it with evidence; do not rediscover it):
<6 lines from the audience brief>

BUSINESS: <name> | NICHE: <niche> | LOCATION: <city, prov>

EVIDENCE TAGS - every line you return carries exactly one:
  [client] from client.md   [prior] from the digest above
  [web:verified] named source AND a second independent corroboration
  [web:unverified] single-source or paraphrased
  [model] your inference, no source
HARD RULE: if you find nothing for a subsection, write
`not-found: <what> <why>` and omit it. Never invent a plausible-looking
row. A fabricated row is worse than an empty section.
```

## Agent 1 - TOP PLAYERS

```
GOAL: what the businesses currently winning this market promise, and the gap
      none of them fill.
READ: web search results for "<niche> <city>" and the top-ranking sites.
TASK: identify 3-5 businesses ranking for the niche + city. For EACH return
      one row: hero promise | primary CTA | trust stack | offer or guarantee
      | price transparency (yes/no/ranges) | dual-path hero (yes/no) | one
      notable omission.
      Then exactly two synthesis lines:
        TABLE STAKES: what all of them do (we must too, or we look amateur)
        GAP: what none of them do (our wedge)
      Do NOT recommend a design. Do NOT copy their words as ours.
BUDGET: <= 12 tool calls. Max 5 players, max 2 pages fetched per player.
```

## Agent 2 - VERBATIM LANGUAGE

```
GOAL: 12-20 exact phrases real customers use about this service category.
READ: public reviews of competitors in this market (5-star AND 1-star), plus
      any reviews inside client.md's Business Profile Paste.
TASK: return VERBATIM phrases - never paraphrased, never merged, never
      cleaned up, never grammar-fixed. Sort into PAINS / DESIRES /
      OBJECTIONS / DELIGHT TRIGGERS. Each phrase carries its source and star
      rating.
      Read 1-star reviews for OBJECTIONS (what goes wrong, what people fear)
      and 5-star reviews for DELIGHT TRIGGERS (what actually earns praise).
      If you cannot quote a phrase exactly, leave it out.
      No personal data: no reviewer surnames, no contact details.
BUDGET: <= 12 tool calls.
```

## Agent 3 - SEARCH INTENT

```
GOAL: what people actually type, and which page must answer each cluster.
READ: search results, autocomplete/related-search surfaces, and the
      question sections for this niche + location.
TASK: return query CLUSTERS (not a keyword dump). Each cluster:
        cluster | intent | the page or section that should answer it
      Intent is one of: emergency | planned | price-shopping | comparison |
      reassurance.
      Also return the recurring QUESTIONS people ask and the local
      MODIFIERS in use (neighbourhood names, "near me" variants).
      No search-volume numbers unless a source explicitly states one - and
      then cite it.
BUDGET: <= 12 tool calls.
```

## Agent 4 - OFFER AND PROOF (always runs; needs no web access)

```
GOAL: what this business can actually claim today, and what it cannot.
READ: input/client.md ONLY - Business Profile Paste, Creative, Overrides,
      Auto, Special requests. Nothing else. Do not search the web.
TASK: return
        SERVICES / PACKAGES: what they sell, as stated [client]
        GUARANTEE / RISK REVERSAL: exact text, or "none stated"
        PRICE POSTURE: published | ranges | quote-only | unknown
        PROOF WE HAVE: every trust element the client can back TODAY
          (years, certifications, licences, review count, service area,
          payment methods, emergency hours, real testimonials)
        PROOF WE LACK: every trust element this niche expects that
          client.md does not supply - each becomes a QUESTIONS.md line and
          ships as [PLACEHOLDER] until answered
      Never infer a fact from a review. "Fixed my AC fast" is not evidence
      of a 24/7 emergency service.
BUDGET: <= 8 tool calls.
```

## Agent 5 - COPY CRITIC (runs after drafts exist)

```
ROLE 1.critic. Fresh context: assume nothing about this build.
GOAL: find everything wrong with these drafts. You return FINDINGS ONLY -
      never a rewrite.
READ: <draft paths>, input/client.md, and the RESEARCH BRIEF in
      system/state/DECISIONS.md. Nothing else.
LEASE: none (read-only).
TASK: four audits, numbered findings, each severity `block | fix | nit`:
      CLAIM       every asserted fact about the business traced to a
                  [client] source. Untraceable = block, and say what it
                  should become instead ([PLACEHOLDER] + a question).
      PLACEHOLDER every [PLACEHOLDER] has a matching QUESTIONS.md line and
                  reads as a question a client can answer, not a hole.
      TONE        against the Mood adjectives, the "Never say / avoid"
                  line, and the brief's words-to-avoid. Flag
                  "welcome to our website", "we are passionate about",
                  superlatives without proof, and upsell pressure.
      AUDIENCE    every CTA is the action THIS audience actually takes;
                  objections appear BEFORE the ask; reading level ~grade 7.
      You get no credit for approving. If a draft is genuinely clean, say
      `result: no blocking findings` and list what you checked.
BUDGET: <= 10 tool calls.
```

## Merge rules (master side)

`block` and `fix` are applied before anything proceeds. `nit` goes to
DECISIONS.md as accepted-with-note. A critic that returns nothing and lists
no method was a failed review, not a pass - re-issue once (see
system/contracts/agent-protocol.md section 5).
