#!/usr/bin/env python3
"""Generate system/docs/REGISTRY.md from skill frontmatter. Never hand-edit it."""
import re, pathlib

SKILLS = pathlib.Path(".claude/skills")
rows = []
for d in sorted(SKILLS.iterdir()):
    sk = d / "SKILL.md"
    if not d.is_dir() or not sk.exists(): continue
    text = sk.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    fm = m.group(1) if m else ""
    def grab(key, default="-"):
        mm = re.search(rf"{key}:\s*(.+)", fm)
        return mm.group(1).strip() if mm else default
    desc = re.search(r"description:\s*(.+?)(?=\nmetadata:|\Z)", fm, re.S)
    desc = re.sub(r"\s+", " ", desc.group(1)).strip() if desc else "-"
    meta = re.search(r"metadata:\s*\{(.*?)\}", fm)
    meta = meta.group(1) if meta else ""
    ver = re.search(r"version:\s*([\d.]+)", meta)
    cat = re.search(r"category:\s*(\w+)", meta)
    tier = re.search(r"tier:\s*(\w+)", meta)
    manual = "manual" if re.search(r"^disable-model-invocation:\s*true", fm, re.M) else "auto"
    rows.append((d.name, manual, tier.group(1) if tier else "-",
                 cat.group(1) if cat else "-",
                 ver.group(1) if ver else "-", desc))

out = ["# Skill Registry (auto-generated - do not hand-edit)",
       "", "Regenerate: `py -3 system/scripts/generate-skill-registry.py` (macOS/Linux: python3)",
       "", "load: auto = Claude loads it when the task matches; manual = only when the operator invokes it by name.", "",
       "| skill | load | tier | category | version | description |",
       "|---|---|---|---|---|---|"]
for name, manual, tier, cat, ver, desc in sorted(rows, key=lambda r: (r[1], r[2], r[0])):
    out.append(f"| {name} | {manual} | {tier} | {cat} | {ver} | {desc} |")
pathlib.Path("system/docs").mkdir(parents=True, exist_ok=True)
pathlib.Path("system/docs/REGISTRY.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"wrote system/docs/REGISTRY.md ({len(rows)} skills)")
