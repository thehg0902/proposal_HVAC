---
paths: ["**/*.html"]
---
# HTML rules (load only when editing HTML)
- Semantic landmarks: one <main>, <header>, <footer>, <nav aria-label>.
- One <h1> per page; heading levels never skip.
- Every <img> has meaningful alt (or alt="" if decorative) + width/height
  attributes + loading="lazy" below the fold.
- Sections follow system/contracts/component-api.md shape exactly.
- Pitch page head: <title>, meta description, and
  `<meta name="robots" content="noindex, nofollow">` (pitch pages are
  private). No OG/schema needed - seo-technical is manual-only.
