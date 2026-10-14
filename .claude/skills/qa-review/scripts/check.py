#!/usr/bin/env python3
"""Agency OS automated QA gate. Run from repo root. Exit 1 on any FAIL."""
import html as _html, re, sys, pathlib

ROOT = pathlib.Path(".")
SITE = ROOT / "output"
fails, warns = [], []

def fail(msg): fails.append(msg)
def warn(msg): warns.append(msg)

# scan all of output/ recursively (root page, shared/, every page folder)
html_files = sorted(SITE.rglob("*.html"))
css_files  = sorted(SITE.rglob("*.css"))
js_files   = sorted(SITE.rglob("*.js"))

if not html_files:
    fail("no HTML files in output/ - nothing to QA")

# Deferred fact confirmations (v1.11.0): Phase 0 stopped blocking on the
# confirmation table, so this is where that debt is collected. Any row still
# open under the exact heading is a FAIL - unverified facts cannot ship.
DEFERRED_HEADING = "Fact confirmations (deferred from Phase 0)"
qfile = ROOT / "system" / "state" / "QUESTIONS.md"
if qfile.exists():
    qtext = re.sub(r"<!--.*?-->", "", qfile.read_text(encoding="utf-8",
                   errors="replace"), flags=re.S)
    dsec = re.search(r"^##\s*" + re.escape(DEFERRED_HEADING) + r"\s*$(.*?)(?=^##\s|\Z)",
                     qtext, re.M | re.S)
    if dsec:
        open_rows = re.findall(r"^\s*-\s*\[ \]\s*(.+)$", dsec.group(1), re.M)
        if open_rows:
            fail(f"system/state/QUESTIONS.md: {len(open_rows)} deferred fact "
                 f"confirmation(s) still open - first: {open_rows[0][:70]}")

for f in html_files + css_files + js_files:
    text = f.read_text(encoding="utf-8", errors="replace")
    if "[PLACEHOLDER" in text: fail(f"{f}: unresolved [PLACEHOLDER]")
    if re.search(r"\bTODO\b", text): fail(f"{f}: leftover TODO")
    if "lorem ipsum" in text.lower(): fail(f"{f}: lorem ipsum")

for f in html_files:
    text = f.read_text(encoding="utf-8", errors="replace")
    # local refs exist - resolved relative to each file's own folder, so
    # "../assets/..." from a page folder and "assets/..." from output/ root
    # both pass when the target exists. Folder refs (about/) hit index.html.
    for m in re.finditer(r'(?:src|href)="([^"#][^":]*?)"', text):
        ref = m.group(1)
        if ref.startswith(("http", "mailto:", "tel:", "//", "data:")): continue
        target = (f.parent / ref).resolve()
        if target.is_dir(): target = target / "index.html"
        if not target.exists():
            fail(f"{f}: broken local ref -> {ref}")
    # img alt + intrinsic size (CLS)
    for m in re.finditer(r"<img\b[^>]*>", text):
        tag = m.group(0)
        if "alt=" not in tag: fail(f"{f}: <img> missing alt")
        if "width=" not in tag or "height=" not in tag:
            warn(f"{f}: <img> missing width/height (CLS) -> {tag[:60]}")
    # single h1
    n_h1 = len(re.findall(r"<h1\b", text))
    if n_h1 != 1: fail(f"{f}: {n_h1} <h1> tags (need exactly 1)")
    if "<main" not in text: warn(f"{f}: no <main> landmark")
    # viewport meta
    if "viewport" not in text: fail(f"{f}: missing viewport meta")
    # stylesheet link order per file-structure contract:
    # tokens.css -> base.css -> the page's own style.css
    sheets = [s.split("/")[-1] for s in
              re.findall(r'<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"', text)
              + re.findall(r'<link[^>]+href="([^"]+)"[^>]+rel="stylesheet"', text)]
    order = [s for s in sheets if s in ("tokens.css", "base.css", "style.css")]
    if order and order != [s for s in ("tokens.css", "base.css", "style.css") if s in order]:
        fail(f"{f}: stylesheet order {order} (contract: tokens -> base -> style)")

# hardcoded colors outside tokens.css; per-page CSS health
for f in css_files:
    if f.name == "tokens.css": continue
    text = f.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"#[0-9a-fA-F]{3,8}\b|rgb\(", text):
        fail(f"{f}: hardcoded color '{m.group(0)}' (use var(--token))"); break
    if f.name == "style.css":  # per-page css: small + token-driven
        kb = f.stat().st_size // 1024
        if kb > 20:
            warn(f"{f}: {kb}KB page css (>20KB suggests shared/ leakage)")
        if text.strip() and "var(" not in text:
            warn(f"{f}: no var( usage - bypassing design tokens?")

# header/footer drift across page folders. Pages at different depths
# legitimately differ in relative href/src prefixes (../), so normalize
# those away before comparing - only real content drift warns.
def block(tag, text):
    m = re.search(rf"<{tag}\b.*?</{tag}>", text, re.S)
    if not m: return None
    b = re.sub(r"\s+", " ", m.group(0))
    return re.sub(r'((?:src|href)=")(?:\.\./)+', r"\1", b)
if len(html_files) > 1:
    base = html_files[0].read_text(encoding="utf-8", errors="replace")
    for tag in ("header", "footer"):
        ref_block = block(tag, base)
        for f in html_files[1:]:
            other = block(tag, f.read_text(encoding="utf-8", errors="replace"))
            if ref_block and other and ref_block != other:
                warn(f"{f}: <{tag}> differs from {html_files[0]} (drift?)")

# page-weight audit vs hosting-profile budgets (the "dip detector").
# Profile from client.md 'Hosting plan:' - business/cloud/cdn = cdn
# profile, anything else / unknown = the tighter no-cdn set (fail-safe).
def hosting_profile():
    try:
        txt = (ROOT / "input" / "client.md").read_text(encoding="utf-8")
        txt = re.sub(r"<!--.*?-->", "", txt, flags=re.S)  # docs comments lie
        txt = re.sub(r"\{[^{}]*\}", "", txt)              # {operator comments}
        m = re.search(r"^[-*]?[ \t]*Hosting plan[ \t]*:[ \t]*(.+)$", txt, re.M | re.I)
        v = m.group(1).strip().lower() if m else ""
        if v and ("business" in v or "cloud" in v or "cdn" in v):
            return "cdn"
    except OSError:
        pass
    return "no-cdn"

PROFILE = hosting_profile()
MB = 1024 * 1024
PAGE_CAP, HERO_CAP = (1.5 * MB, 4 * MB) if PROFILE == "cdn" else (1.0 * MB, 3 * MB)

LAZY_CAP = 12 * MB   # PresentationOS: screenshot carousels + click-to-play creative

def on_demand_refs(text):
    """Refs the browser fetches only on scroll/click: <img loading="lazy">
    (carousel screenshots) and media inside <video preload="none">
    (click-to-play creative). Excluded from the initial page-weight cap."""
    out = set()
    def grab(chunk):
        for attr in re.findall(r'(?:src|srcset)="([^"]+)"', chunk):
            for part in attr.split(","):
                if part.strip(): out.add(part.strip().split()[0])
    for tag in re.findall(r"<img\b[^>]*>", text, re.I):
        if re.search(r'loading="lazy"', tag, re.I): grab(tag)
    for vid in re.findall(r"<video\b[^>]*preload=\"none\"[^>]*>.*?</video>", text, re.I | re.S):
        grab(re.sub(r'poster="[^"]*"', "", vid))
    return out

for f in html_files:
    text = f.read_text(encoding="utf-8", errors="replace")
    refs = set(re.findall(r'(?:src|href|poster)="([^"#][^":]*?)"', text))
    for ss in re.findall(r'srcset="([^"]+)"', text):
        for part in ss.split(","):
            if part.strip(): refs.add(part.strip().split()[0])
    lazy = on_demand_refs(text)
    weights, video_bytes, lazy_bytes = [], 0, 0
    for ref in refs:
        if ref.startswith(("http", "mailto:", "tel:", "//", "data:")): continue
        target = (f.parent / ref).resolve()
        if not target.exists() or target.is_dir(): continue
        size = target.stat().st_size
        if ref in lazy:
            lazy_bytes += size           # on-demand: own (looser) cap below
            continue
        if target.suffix.lower() in (".mp4", ".webm", ".mov"):
            video_bytes += size          # video capped separately, not in page weight
        else:
            weights.append((size, ref))
    total = sum(s for s, _ in weights)
    top3 = ", ".join(f"{r} ({s // 1024}KB)" for s, r in sorted(weights, reverse=True)[:3])
    if total > PAGE_CAP:
        fail(f"{f}: page weight {total / MB:.2f}MB > {PAGE_CAP / MB:.1f}MB cap "
             f"[{PROFILE}]; heaviest: {top3}")
    elif total > PAGE_CAP * 0.8:
        warn(f"{f}: page weight {total / MB:.2f}MB is >80% of the "
             f"{PAGE_CAP / MB:.1f}MB cap [{PROFILE}]; heaviest: {top3}")
    if video_bytes > HERO_CAP:
        fail(f"{f}: video weight {video_bytes / MB:.1f}MB > {HERO_CAP / MB:.0f}MB cap [{PROFILE}]")
    elif video_bytes > HERO_CAP * 0.8:
        warn(f"{f}: video weight {video_bytes / MB:.1f}MB is >80% of cap [{PROFILE}]")
    if lazy_bytes > LAZY_CAP:
        warn(f"{f}: on-demand media {lazy_bytes / MB:.1f}MB > {LAZY_CAP / MB:.0f}MB - "
             f"re-run /ingest or trim screenshots")

# title/meta audit (seo-technical rules 1, 1a, 6). Rule 6 says "no
# duplicate titles/descriptions (qa should catch)" - this is that catch.
# Length is a WARN not a FAIL: the 60/155 figures are SERP display
# guidelines, and rule 1a step (c) legitimately ships a longer title when
# the operator's own keyword is that long. A warn keeps a skipped
# overflow ladder visible without blocking a deliberate choice.
titles, descs = {}, {}
for f in html_files:
    text = f.read_text(encoding="utf-8", errors="replace")
    tm = re.search(r"<title\b[^>]*>(.*?)</title>", text, re.S | re.I)
    if not tm or not tm.group(1).strip():
        fail(f"{f}: missing <title>")
    else:
        # unescape first: "&amp;" is ONE rendered character, and business
        # names with "&" are common - counting the entity inflates by 4.
        t = _html.unescape(re.sub(r"\s+", " ", tm.group(1))).strip()
        titles.setdefault(t, []).append(f)
        if len(t) > 60:
            warn(f"{f}: <title> {len(t)} chars (>60) - apply the seo-technical "
                 f"rule 1a overflow ladder: {t[:50]}...")
    dm = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', text, re.I)
    if dm:
        d = _html.unescape(dm.group(1)).strip()
        descs.setdefault(d, []).append(f)
        if len(d) > 155:
            warn(f"{f}: meta description {len(d)} chars (>155)")
for t, fs in titles.items():
    if len(fs) > 1:
        fail(f"duplicate <title> on {len(fs)} pages ({', '.join(str(x) for x in fs)}): {t[:60]}")
for d, fs in descs.items():
    if len(fs) > 1:
        fail(f"duplicate meta description on {len(fs)} pages ({', '.join(str(x) for x in fs)})")

# duplicate-content check: near-clone <main> body text across pages is the
# main risk site-architecture's service+location matrix introduces (rule
# 1c) - cloned pages (e.g. one paragraph with only the city name swapped)
# read as thin/spam content to search engines. Word-shingle Jaccard, not
# a character-level ratio: local-business pages legitimately share a lot
# of VOCABULARY ("serving", "same-day", "licensed") without being
# duplicates, and raw character similarity false-positives on that shared
# wording. 5-word shingles only match on repeated SEQUENCES, so a single
# swapped word (the city) still scores near-identical while independently
# written pages score low despite sharing individual words. Compares
# <main> text only (header/footer/nav are legitimately shared and already
# checked separately above) and skips short/stub content.
def main_text(html):
    m = re.search(r"<main\b[^>]*>(.*?)</main>", html, re.S)
    body = m.group(1) if m else html
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip().lower()

def shingles(text, n=5):
    words = text.split()
    return {tuple(words[i:i + n]) for i in range(len(words) - n + 1)}

if len(html_files) > 2:
    bodies = [(f, main_text(f.read_text(encoding="utf-8", errors="replace")))
              for f in html_files]
    shingled = [(f, shingles(t)) for f, t in bodies if len(t.split()) >= 80]
    for i in range(len(shingled)):
        f1, s1 = shingled[i]
        for f2, s2 in shingled[i + 1:]:
            if not s1 or not s2: continue
            jaccard = len(s1 & s2) / len(s1 | s2)
            if jaccard > 0.5:
                fail(f"{f1} and {f2}: main content {jaccard:.0%} overlapping "
                     f"5-word sequences - looks cloned, not unique per "
                     f"service/location")

# media log consistency. Cell indices assume the 9-column contract table
# with leading pipe: split("|") -> [ '', id, date, type, model, prompt,
# credits, approved, file, status, '' ] so cells[8] = file column.
log = ROOT / "system" / "state" / "MEDIA_LOG.md"
if log.exists():
    for line in log.read_text().splitlines():
        if "| generated" in line or "| in-use" in line:
            cells = [c.strip() for c in line.split("|")]
            if len(cells) > 8 and cells[8] not in ("-", "") and not (ROOT / cells[8]).exists():
                fail(f"MEDIA_LOG: file missing on disk -> {cells[8]}")

print("=== QA CHECK ===")
for w in warns: print(f"WARN  {w}")
for x in fails: print(f"FAIL  {x}")
print(f"{len(fails)} fail, {len(warns)} warn")
sys.exit(1 if fails else 0)
