#!/usr/bin/env python3
"""Validate input/client.md (PresentationOS prospect sheet) + inventory the
input/ folders. Run from repo root: `py -3 system/scripts/validate-client-md.py`
(macOS/Linux: python3). Exit 1 on any BLOCKER. Schema: input/client.schema.md.
"""
import re, sys, pathlib

ROOT = pathlib.Path(".")
INP = ROOT / "input"
CLIENT = INP / "client.md"
IMG = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff", ".heic", ".avif"}
VID = {".mp4", ".mov", ".webm", ".m4v", ".avi", ".mkv"}
SECTION_IDS = {"cover", "method", "customer", "reviews", "roadblocks", "awareness",
               "competitors", "gap", "mental-chain", "plan", "creative", "website",
               "next", "interview"}

blockers, soft, info = [], [], []

if not CLIENT.exists():
    print("BLOCKER  input/client.md missing"); sys.exit(1)

text = CLIENT.read_text(encoding="utf-8")
text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
text = re.sub(r"\{[^{}]*\}", "", text)

def sections(md, level="## "):
    out, cur = {}, None
    for line in md.splitlines():
        if line.startswith(level) and not line.startswith(level + "#"):
            cur = line[len(level):].strip(); out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return {k: "\n".join(v) for k, v in out.items()}

def fields(body):
    return {k.strip().lower(): v.strip()
            for k, v in re.findall(r"^[-*]\s*([^:\n]+):[ \t]*(.*)$", body, re.M)}

S = sections(text)
P = fields(S.get("Prospect", ""))
R = fields(S.get("Research", ""))
B = fields(S.get("Brand", ""))
D = fields(S.get("Demo website", ""))
SEC = fields(S.get("Sections", ""))
A = fields(S.get("Agency", ""))

# Prospect
name = P.get("business name", "")
if not name:
    blockers.append("Prospect > Business name is empty - the only client.md blocker")

# Research file
rdir = INP / "research"
cands = [p for p in rdir.iterdir() if p.name != "README.md"] if rdir.exists() else []
cands = [p for p in cands if p.is_dir() or p.suffix.lower() in (".pdf", ".md")]
named = R.get("file", "")
research = None
if named:
    target = (INP / named) if (INP / named).exists() else (rdir / named)
    if not target.exists():
        blockers.append(f"Research > File '{named}' not found in input/research/")
    else:
        research = target
elif len(cands) == 1:
    research = cands[0]
elif not cands:
    blockers.append("no research file in input/research/ (WWP Structure PDF or Notion Markdown export)")
else:
    blockers.append(f"{len(cands)} research files in input/research/ - name one under Research > File")
if research is not None:
    kind = "Notion export folder" if research.is_dir() else research.suffix.lower().lstrip(".").upper()
    info.append(f"RESEARCH {research.relative_to(ROOT).as_posix()} ({kind})")

# Brand
pal = B.get("palette", "")
hexes = re.findall(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", pal)
logo = sorted((INP / "assets-intake").glob("logo.*")) if (INP / "assets-intake").exists() else []
if pal and not hexes:
    soft.append(f"Brand > Palette has no hex codes ('{pal}') - will be interpreted and logged")
if hexes:
    brand_src = f"palette ({', '.join(hexes)})"
elif logo:
    brand_src = f"logo ({logo[0].name}) - colours extracted at Phase 2"
else:
    brand_src = "niche default (no palette, no logo)"
info.append(f"BRAND    {brand_src}")

# Creative blocks
cre = sections(S.get("Creative", ""), "### ")
blocks = {k: fields(v) for k, v in cre.items() if re.match(r"creative\s*\d+", k, re.I)}
if not blocks:
    soft.append("Creative: no '### Creative N' block - the creative section will be a placeholder")
for k, f in blocks.items():
    missing = [x for x in ("type", "platform", "aspect") if not f.get(x)]
    if missing:
        soft.append(f"{k}: {', '.join(missing)} empty - interpreted at Phase 3 or placeholder")
    copy_missing = [x for x in ("headline", "primary text", "cta") if not f.get(x)]
    if copy_missing:
        soft.append(f"{k}: copy {', '.join(copy_missing)} empty -> [PLACEHOLDER] until filled")

# Demo website
url = D.get("url", "")
if url and not re.match(r"https?://", url):
    soft.append(f"Demo website > URL '{url}' does not start with http(s)://")

# Sections
for key in ("hide", "show", "order"):
    ids = [x.strip() for x in SEC.get(key, "").split(",") if x.strip()]
    bad = [x for x in ids if x not in SECTION_IDS]
    if bad:
        soft.append(f"Sections > {key.title()}: unknown id(s) {', '.join(bad)}")

# Agency
empty_agency = [k for k in ("agency name", "prepared by", "contact / booking link",
                            "how i help", "process / next step") if not A.get(k)]
if empty_agency:
    soft.append(f"Agency: {', '.join(empty_agency)} empty -> [PLACEHOLDER] in the 'next' section "
                "(fill once in the template)")

# Inventory
def count(folder, exts):
    d = INP / folder
    if not d.exists(): return 0, []
    files = [p for p in d.rglob("*") if p.is_file() and p.suffix.lower() in exts]
    groups = sorted({(p.parent.name if p.parent != d else "(root)") for p in files})
    return len(files), groups

n, g = count("reviews", IMG)
info.append(f"REVIEWS  {n} screenshot(s)" + (f" - {', '.join(g)}" if g else ""))
n, g = count("competitors", IMG)
info.append(f"COMPET.  {n} screenshot(s)" + (f" - {', '.join(g)}" if g else ""))
n, _ = count("creative", IMG | VID)
info.append(f"CREATIVE {n} file(s) for {len(blocks)} block(s)")
if url:
    info.append(f"WEBSITE  {url}")

print("=== CLIENT.MD VALIDATION ===")
print(f"PROSPECT {name or '(missing)'}")
for b in blockers: print(f"BLOCKER  {b}")
for s in soft:     print(f"SOFT     {s}")
for i in info:     print(i)
sys.exit(1 if blockers else 0)
