# Niche map — typed niche → audience study + design playbook

Resolution is deterministic so it is never re-litigated per build. Phase 0
writes ONE line to `system/state/DECISIONS.md`:

```
YYYY-MM-DD | niche-resolution | niche: <as typed> | study: <file|none> (<exact|adjacent|none>) | playbook: <file> (<exact|adjacent|closest-by-mode:<mode>>) | by: operator|detected
```

## The ladder

1. **Slug match** — lowercase the typed niche, spaces to hyphens, drop legal
   suffixes (inc, ltd, co). Exact filename hit in
   `.claude/skills/audience-research/references/` (11 studies) or
   the block list of
   `.claude/skills/design-direction/references/niche-playbooks.md` (16
   playbook blocks) wins as `exact`.
2. **Alias table** — the table below. Marked `adjacent` when the study is a
   psychology neighbour rather than the same trade.
3. **Family fallback** — urgent-trade / planned-exterior / large-planned-build
   / health-clinic / aesthetic → that family's default study.
4. **No match** — the study is **skipped entirely** (`prior: none`). Never
   substitute a wrong study: a wrong prior is worse than no prior, because
   every later phase treats the brief as evidence. The playbook is then
   chosen by **conversion mode**, and a `niche-gap` line goes to DECISIONS.md
   so the library can grow.

## Conversion-mode fallback (playbook only, when nothing matches)

| mode | what the visitor does | playbook |
|---|---|---|
| call-first | phones now, urgency | hvac |
| book-first | schedules an appointment | dental |
| browse-first | reads/looks before deciding | restaurant |
| membership | signs up for ongoing access | gym |
| visit/experience | comes in person, atmosphere sells | coffee-shop |

## Alias table

| typed niche (aliases) | study | playbook |
|---|---|---|
| roofing, roofer, shingles, flat roof | roofing (exact) | roofing (exact) |
| electrician, electrical, EV charger, panel upgrade | electrician (exact) | electrician (exact) |
| hvac, heating, a/c, air conditioning, furnace | electrician (adjacent) | hvac (exact) |
| plumber, plumbing, drain, water heater | electrician (adjacent) | hvac (exact) |
| garage door, overhead door, door spring | garage-door-repair (exact) | garage-door-repair (exact) |
| paving, asphalt, driveway sealing | paving (exact) | paving (exact) |
| concrete, foundation, flatwork, stamped concrete | concrete-contractor (exact) | concrete-contractor (exact) |
| fencing, decks, interlock, hardscaping | concrete-contractor (adjacent) | concrete-contractor (adjacent) |
| tree service, arborist, stump removal | tree-service (exact) | tree-service (exact) |
| landscaping, lawn care, snow removal | tree-service (adjacent) | tree-service (adjacent) |
| windows and doors, siding, eavestrough | roofing (adjacent) | roofing (adjacent) |
| painter, drywall, flooring, handyman | kitchen-bath-reno (adjacent) | kitchen-bath-reno (adjacent) |
| kitchen reno, bathroom reno, renovation | kitchen-bath-reno (exact) | kitchen-bath-reno (exact) |
| home builder, custom home, general contractor | home-builder (exact) | home-builder (exact) |
| real estate agent, realtor | home-builder (adjacent — high-ticket, life-stage) | home-builder (adjacent) |
| dentist, dental, orthodontist, denturist | physiotherapy (adjacent — clinic trust) | dental (exact) |
| physiotherapy, physio, rehab | physiotherapy (exact) | physiotherapy (exact) |
| chiropractor, chiro | chiropractor (exact) | chiropractor (exact) |
| massage, RMT, naturopath, acupuncture | chiropractor (adjacent) | chiropractor (adjacent) |
| optometrist, audiologist, podiatrist | physiotherapy (adjacent) | physiotherapy (adjacent) |
| med spa, medspa, injectables, botox | med-spa (exact) | med-spa (exact) |
| salon, barber, nails, lashes, brows | med-spa (adjacent) | med-spa (adjacent — take the editorial restraint, not the clinical register) |
| gym, crossfit, yoga, pilates, personal training | physiotherapy (adjacent — body outcome) | gym (exact) |
| restaurant, pizzeria, bistro, catering | none | restaurant (exact) |
| cafe, coffee, bakery, roastery | none | coffee-shop (exact) |
| auto repair, mechanic, detailing, tires | garage-door-repair (adjacent — scam-polluted, price fear) | garage-door-repair (adjacent) |
| moving, junk removal, cleaning service | none | hvac |
| law, accounting, insurance broker, financial advisor | none | dental |
| pet grooming, dog training, veterinary | none | dental |

## Notes

- `adjacent` is honest, not a hedge: an HVAC company reading the electrician
  study gets the right three-lane buyer model (panic / planned / compelled)
  even though the trade differs. The brief must SAY it is adjacent so later
  phases discount province- or trade-specific detail.
- The 11 studies are Ontario-market research. Outside Ontario keep the
  psychology, drop the province-specific claims (WSIB, seasonality) unless
  the client's market genuinely matches.
- When the operator's typed niche disagrees with the GBP category line, the
  typed one wins and the disagreement is one logged line — owners mis-set
  their own GBP category constantly, and it is never worth a question.
- Growing the library: a `niche-gap` line is the signal that a new study is
  worth writing. Studies live in
  `.claude/skills/audience-research/references/` and follow the shipped
  9-section format ending in "Website Conversion Implications". A new study
  gets a matching block in
  `.claude/skills/design-direction/references/niche-playbooks.md`, distilled
  from that section 9 — add both or the visual half stays generic.
