# JSON-LD LocalBusiness Template
{
 "@context":"https://schema.org",
 "@type":"<subtype or LocalBusiness>",
 "name":"", "url":"", "telephone":"", "image":"<absolute hero/og url>",
 "address":{"@type":"PostalAddress","streetAddress":"","addressLocality":"",
   "addressRegion":"","postalCode":"","addressCountry":""},
 "geo":{"@type":"GeoCoordinates","latitude":0,"longitude":0},
 "openingHoursSpecification":[{"@type":"OpeningHoursSpecification",
   "dayOfWeek":[],"opens":"","closes":""}],
 "sameAs":[]
}
Rules: every value from client.md (hours -> QUESTIONS if absent); geo from
the client's Maps link coordinates; sameAs = social URLs; omit fields you
can't source rather than inventing. Validate structure mentally against
required-by-type fields; suggest the user run Google's Rich Results test
post-deploy (record as post-deploy check).

## LLM / GEO optimization (AI search engines)
No separate markup - the same JSON-LD block above is what AI answer
engines parse for citations too. The only actionable difference from
classic SEO is completeness, not format:
- Never leave `sameAs` empty when client.md lists any socials or an
  existing website - an LLM cross-references identity through this
  array.
- Fill `openingHoursSpecification`, `areaServed` (from Service area,
  including the full `/`-list on matrix builds - references/
  service-location-matrix.md), and a `hasOfferCatalog`/`services` list
  when the type supports it, even where Google's Rich Results test
  wouldn't flag the field as required - an LLM has no separate
  "required fields" concept and reads whatever is there.
- Keep the schema's name/address/phone text identical to the visible
  page (seo-technical rule 2) - an LLM that finds two different NAP
  strings on one page has no way to know which is authoritative.
