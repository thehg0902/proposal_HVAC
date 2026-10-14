---
name: seo-technical
disable-model-invocation: true
description: Technical + local SEO - titles, meta descriptions, Open Graph,
  schema.org LocalBusiness JSON-LD, sitemap.xml, robots.txt, GBP/NAP
  consistency. Use in Phase 5 finishing pass. Not copy tone (copywriting),
  GBP embeds (maps-gbp), or GBP optimization/reviews/SEO-vs-ads strategy
  (local-seo-gbp).
metadata: {version: 1.4.0, category: seo, tier: B}
---
# SEO Technical

## Purpose
Local businesses win on local pack + a technically clean site; this skill
covers the on-site half.

## Inputs
client.md (Business, Contact, Links, Services), final pages in output/.

## Outputs
Per-page head metadata, JSON-LD, sitemap.xml, robots.txt.

## Rules
1. Title pattern: {page keyword} | {Business Name} - <= 60 chars, unique
   per page. Meta description <= 155 chars, contains the page's
   conversion offer. Keyword source, exactly two states (client.schema.md,
   site-architecture references/service-location-matrix.md): Overrides
   "Target search terms" filled -> the phrase assigned to that page,
   verbatim; empty -> {Primary service/what} in {City} for ordinary
   pages, or the generic [service] [location] template for matrix pages.
   Never market-research's KEYWORD CANDIDATE directly - it only acts
   once the operator promotes it into Target search terms. "Domain"
   preempts the domain question; "Service area" and "Price range" feed
   areaServed and priceRange in the JSON-LD.
1a. Title overflow ladder (long service+city keywords blow the 60-char
   cap on matrix pages - "heat pump installation Richmond Hill | Apex
   Heating & Cooling" is 61). Apply IN ORDER, stop at the first that
   fits; never truncate mid-word, never abbreviate the keyword, never
   invent a short form of the business name:
   a. `{keyword} | {Business Name}` - preferred, always used on home.
   b. `{keyword}` alone - drop the brand suffix. Deep matrix pages are
      won by the keyword; the brand is carried by the H1, the NAP block
      and the JSON-LD on the same page, so nothing is lost.
   c. Keyword alone still > 60: ship it and log ONE line to
      system/state/DECISIONS.md (`title-overflow | <page> | <n> chars`). A
      keyword that long came from the operator's own Target search terms
      or their own service naming - the fix is theirs to make, not a
      silent rewrite of what they asked to rank for.
   Home ALWAYS keeps the business name (step a only) - it is the brand's
   own page. check.py warns on any title > 60 so a skipped ladder is
   visible.
2. NAP (name/address/phone) rendered in HTML footer/contact must match
   client.md and GBP EXACTLY, character for character
   (see "On-site local SEO" below). NAP source: Overrides or [confirmed] Auto
   facts ONLY. Never publish an [unconfirmed] NAP fact — it stays
   [PLACEHOLDER: value?] until confirmed.
3. JSON-LD: LocalBusiness (or subtype - Dentist, Restaurant, HVACBusiness
   etc.) per references/structured-data.md; one block, on every page,
   facts only from client.md. The same block already serves AI/LLM
   search engines - completeness is the only lever (references/
   structured-data.md LLM/GEO note), not separate markup.
4. OG/Twitter: og:title, og:description, og:image (1200x630 derived from
   hero poster), og:url per page.
5. sitemap.xml lists every page as a clean folder URL with the final
   domain — `https://domain/` for home, `https://domain/about/` for
   subpages, never `/about/index.html` (ask if domain unknown ->
   QUESTIONS.md); robots.txt allows all + sitemap line.
6. Canonical tag per page uses the same folder-URL form; no duplicate
   titles/descriptions (qa should catch, but own it here).

## On-site local SEO
NAP consistency is the highest-weight controllable: the exact string used
on GBP is canonical - copy it, never normalize it. City/area mentions go in
hero-adjacent copy, service sections, the footer address and the title tag,
about once per surface, naturally. Each service page targets one
"{service} {city}" intent. Every service named in copy links to its own
section or page. The contact section embeds the map (maps-gbp) and "Get
directions" points at the GBP-linked Maps URL from client.md, never a fresh
search URL.

## References
- references/structured-data.md - the JSON-LD template + the LLM/GEO
  completeness note

## Anti-patterns
- Keyword-stuffed titles; schema claiming ratings/reviews not on the page;
  guessing the domain.

## Changelog
- 1.4.0 on-site local SEO inlined from references/ (v1.13.0)
- 1.3.0 rule 1a title overflow ladder (brand-drop, then log-and-ship;
  never mid-word truncation or invented abbreviations) - long
  service+city keywords blew the 60-char cap on matrix pages;
  check.py now warns on >60 and fails on duplicate/missing titles
- 1.2.0 rule 1 keyword precedence formalized (Target search terms exact
  phrase > generic template > never the market-research candidate
  directly); rule 3 LLM/GEO completeness note added to structured-data.md
- 1.1.0 NAP from confirmed Auto/Overrides only; never publish
  unconfirmed NAP
- 1.0.0 initial
