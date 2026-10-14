#!/usr/bin/env python3
"""PresentationOS /ingest: input/ drop folders -> output/assets/ -> the page's
ingest markers. Contract: system/contracts/asset-slots.md (+ pitch-sections
media hooks). Run from repo root: `py -3 system/scripts/ingest-assets.py`
(macOS/Linux: python3). Flags: --force re-encodes cached creative video.

Idempotent: review/competitor outputs are rebuilt from scratch every run and
every marker pair is rewritten. Tooling: images via Pillow (else cwebp),
video + posters via ffmpeg. A missing tool lists the file as PENDING.
"""
import datetime, html, re, shutil, subprocess, sys, pathlib, tempfile

ROOT = pathlib.Path(".")
INP, OUT = ROOT / "input", ROOT / "output"
IMG_OUT, VID_OUT = OUT / "assets" / "images", OUT / "assets" / "video"
PAGE = OUT / "index.html"
LOG = ROOT / "system" / "state" / "MEDIA_LOG.md"
IMG = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff", ".avif"}
VID = {".mp4", ".mov", ".webm", ".m4v", ".avi", ".mkv"}
MAX_IMG, MAX_VID_W, Q = 1600, 1080, 82
FORCE = "--force" in sys.argv
LABELS = {"google": "Google", "yelp": "Yelp", "facebook": "Facebook", "instagram": "Instagram",
          "tiktok": "TikTok", "youtube": "YouTube", "bbb": "BBB", "homestars": "HomeStars",
          "trustpilot": "Trustpilot", "reddit": "Reddit", "nextdoor": "Nextdoor",
          "angi": "Angi", "houzz": "Houzz", "linkedin": "LinkedIn", "x": "X"}

done, pending, unknown, empty = [], [], [], []

try:
    from PIL import Image, ImageOps
    PIL = True
except ImportError:
    PIL = False

def which(t): return shutil.which(t) is not None
def esc(s): return html.escape(s, quote=True)
def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "item"
def label(s): return LABELS.get(s.lower(), " ".join(w.capitalize() for w in re.split(r"[-_\s]+", s) if w))
def rel(p): return p.relative_to(OUT).as_posix()
def month(p): return datetime.datetime.fromtimestamp(p.stat().st_mtime).strftime("%b %Y")

def client_fields():
    p = INP / "client.md"
    if not p.exists(): return "", {}
    t = re.sub(r"<!--.*?-->", "", p.read_text(encoding="utf-8"), flags=re.S)
    t = re.sub(r"\{[^{}]*\}", "", t)
    m = re.search(r"^[-*]\s*Business name:[ \t]*(.*)$", t, re.M | re.I)
    blocks = {}
    for n, body in re.findall(r"^###\s*Creative\s*(\d+)\s*$(.*?)(?=^##|\Z)", t, re.M | re.S | re.I):
        blocks[int(n)] = {k.strip().lower(): v.strip()
                          for k, v in re.findall(r"^[-*]\s*([^:\n]+):[ \t]*(.*)$", body, re.M)}
    return (m.group(1).strip() if m else ""), blocks

BUSINESS, CREATIVES = client_fields()

def encode_image(src, out, max_side=MAX_IMG, keep_png=False):
    """Returns (width, height) or None when pending."""
    out.parent.mkdir(parents=True, exist_ok=True)
    if PIL:
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im)
            im.thumbnail((max_side, max_side))
            if keep_png:
                im.save(out, "PNG", optimize=True)
            else:
                if im.mode not in ("RGB", "RGBA"): im = im.convert("RGBA")
                im.save(out, "WEBP", quality=Q, method=6)
            return im.size
    if which("cwebp") and not keep_png:
        subprocess.run(["cwebp", "-q", str(Q), "-resize", str(max_side), "0", str(src), "-o", str(out)],
                       check=True, capture_output=True)
        return None
    pending.append((src.as_posix(), f"py -3 -m pip install pillow   (then re-run /ingest)"))
    return None

def dims_attr(wh): return f' width="{wh[0]}" height="{wh[1]}"' if wh else ""

def files_in(d, exts):
    return sorted(p for p in d.iterdir() if p.is_file() and p.suffix.lower() in exts) if d.exists() else []

def note_unknown(d, exts):
    if not d.exists(): return
    for p in d.rglob("*"):
        if p.is_file() and p.name not in ("README.md", "source.txt", ".gitkeep") and p.suffix.lower() not in exts:
            unknown.append(f"{p.as_posix()} - unsupported type (use png/jpg/webp)")

# ---------------------------------------------------------------- carousels
def carousel(kind):
    src_dir, out_dir = INP / kind, IMG_OUT / kind
    if out_dir.exists(): shutil.rmtree(out_dir)
    note_unknown(src_dir, IMG)
    groups = []
    if src_dir.exists():
        root_files = files_in(src_dir, IMG)
        if root_files: groups.append((src_dir, kind, root_files))
        for sub in sorted(p for p in src_dir.iterdir() if p.is_dir()):
            fs = sorted(p for p in sub.rglob("*") if p.is_file() and p.suffix.lower() in IMG)
            if fs: groups.append((sub, sub.name, fs))
    slides, counts = [], []
    for folder, name, fs in groups:
        lab = "Reviews" if (kind == "reviews" and folder == src_dir) else \
              "Competitor" if folder == src_dir else label(name)
        src_txt = folder / "source.txt"
        lines = src_txt.read_text(encoding="utf-8").split() if src_txt.exists() else []
        url = lines[0] if lines else ""
        bar = re.sub(r"^https?://(www\.)?", "", url) or lab
        counts.append(f"{name if folder != src_dir else '(root)'} {len(fs)}")
        for i, f in enumerate(fs, 1):
            out = out_dir / slug(name) / f"{i:02d}.webp"
            wh = encode_image(f, out)
            if not out.exists(): continue
            alt = ("Screenshot of a customer review" if lab == "Reviews" else
                   f"Screenshot of a {lab} review" if kind == "reviews" else
                   f"Screenshot of {lab}'s website or social media")
            slides.append((lab, bar, rel(out), wh, alt, month(f)))
    if not slides:
        empty.append(f"{kind}: no screenshots in input/{kind}/")
        return (f'<p class="proof__empty">[PLACEHOLDER: drop {kind} screenshots into '
                f'input/{kind}/ and run /ingest]</p>')
    n = len(slides)
    labs = list(dict.fromkeys(s[0] for s in slides))
    named = [l for l in labs if l != "Reviews"]
    head = (f"{n} review screenshot{'s' * (n != 1)}" + (f" from {', '.join(named)}" if named else "")
            if kind == "reviews"
            else f"{n} screenshot{'s' * (n != 1)} across {len(labs)} competitor{'s' * (len(labs) != 1)}: {', '.join(labs)}")
    out = [f'<p class="proof__count">{esc(head)}</p>', '<div class="proof__track" data-carousel-track>']
    for i, (lab, bar, src, wh, alt, mon) in enumerate(slides, 1):
        out.append(
            f'<figure class="proof__slide">'
            f'<div class="proof__frame"><div class="proof__bar"><span class="proof__dots" aria-hidden="true"></span>'
            f'<span class="proof__url">{esc(bar)}</span></div>'
            f'<img src="{src}" alt="{esc(alt)}"{dims_attr(wh)} loading="lazy" decoding="async"></div>'
            f'<figcaption class="proof__caption">{esc(lab)} · {mon} · {i} of {n}</figcaption></figure>')
    out.append("</div>")
    done.append(f"{kind}: {n} screenshot(s) ({', '.join(counts)})")
    return "\n".join(out)

# ---------------------------------------------------------------- creative
def creative(n, src):
    """Returns marker HTML for creative-n (src may be None)."""
    meta = CREATIVES.get(n, {})
    typ, plat = meta.get("type", ""), meta.get("platform", "")
    desc = " ".join(x for x in (typ, f"for {plat}" if plat else "") if x)
    alt = f"Ad creative {n}" + (f": {desc}" if desc else "")
    vid, img, poster = VID_OUT / f"creative-{n}.mp4", IMG_OUT / f"creative-{n}.webp", IMG_OUT / f"creative-{n}-poster.webp"
    if src is None:
        empty.append(f"creative-{n}: no file (drop input/creative/creative-{n}.*)")
        return (f'<div class="ad__empty">[PLACEHOLDER: drop creative-{n}.* into input/creative/ '
                f'and run /ingest]</div>')
    is_vid = src.suffix.lower() in VID
    for stale in ((img,) if is_vid else (vid, poster)):
        if stale.exists(): stale.unlink()
    if is_vid:
        if not which("ffmpeg"):
            pending.append((src.as_posix(), f"install ffmpeg, then re-run /ingest"))
            return f'<div class="ad__empty">[PLACEHOLDER: creative-{n} video pending ffmpeg]</div>'
        VID_OUT.mkdir(parents=True, exist_ok=True)
        fresh = vid.exists() and vid.stat().st_mtime >= src.stat().st_mtime and not FORCE
        if not fresh:
            subprocess.run(["ffmpeg", "-y", "-i", str(src), "-vf", f"scale='min({MAX_VID_W},iw)':-2",
                            "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(vid)],
                           check=True, capture_output=True)
        wh = None
        if not poster.exists() or not fresh:
            with tempfile.TemporaryDirectory() as td:
                png = pathlib.Path(td) / "poster.png"
                for ss in ("1", "0"):
                    subprocess.run(["ffmpeg", "-y", "-ss", ss, "-i", str(vid), "-frames:v", "1", str(png)],
                                   capture_output=True)
                    if png.exists(): break
                if png.exists(): wh = encode_image(png, poster)
        if wh is None and PIL and poster.exists():
            with Image.open(poster) as im: wh = im.size
        log_row(n, "video", vid)
        done.append(f"creative-{n}: video -> {vid.as_posix()} ({vid.stat().st_size / 1048576:.1f}MB) + poster")
        p_attr = f' poster="{rel(poster)}"' if poster.exists() else ""
        return (f'<video class="ad__media" src="{rel(vid)}"{p_attr}{dims_attr(wh)} '
                f'controls playsinline preload="none" aria-label="{esc(alt)}"></video>')
    wh = encode_image(src, img)
    if not img.exists():
        return f'<div class="ad__empty">[PLACEHOLDER: creative-{n} image pending]</div>'
    log_row(n, "image", img)
    done.append(f"creative-{n}: image -> {img.as_posix()}")
    return f'<img class="ad__media" src="{rel(img)}" alt="{esc(alt)}"{dims_attr(wh)} loading="lazy" decoding="async">'

def log_row(n, typ, path):
    if not LOG.exists(): return
    t = LOG.read_text(encoding="utf-8")
    if re.search(rf"^\|\s*creative-{n}\s*\|", t, re.M): return
    row = (f"| creative-{n} | {datetime.date.today()} | {typ} | operator | operator-made creative "
           f"({CREATIVES.get(n, {}).get('platform', '') or 'see client.md'}) | - | n/a (operator-made) | "
           f"{path.as_posix()} | in-use |")
    LOG.write_text(t.rstrip("\n") + "\n" + row + "\n", encoding="utf-8")

def creative_sources(page_ns):
    d = INP / "creative"
    note_unknown(d, IMG | VID)
    fs = files_in(d, IMG | VID)
    by_n = {}
    for f in fs:
        m = re.fullmatch(r"creative[-_ ]?(\d+)", f.stem, re.I)
        if m: by_n[int(m.group(1))] = f
    loose = [f for f in fs if f not in by_n.values()]
    wanted = sorted(set(page_ns) | set(CREATIVES) | set(by_n)) or [1]
    if len(wanted) == 1 and not by_n and len(loose) == 1:
        by_n[wanted[0]] = loose.pop()
    for f in loose:
        unknown.append(f"{f.as_posix()} - rename to creative-N.{f.suffix.lstrip('.')} to match a client.md block")
    return {n: by_n.get(n) for n in wanted}

# ---------------------------------------------------------------- logo / website
def logo():
    srcs = sorted((INP / "assets-intake").glob("logo.*"))
    for old in IMG_OUT.glob("logo.*"): old.unlink()
    name = esc(BUSINESS) if BUSINESS else "Business"
    if not srcs:
        return f'<span class="logo logo--text">{name}</span>'
    src = srcs[0]
    IMG_OUT.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() == ".svg":
        out = IMG_OUT / "logo.svg"; shutil.copyfile(src, out)
        vb = re.search(r'viewBox="[\d.\-]+\s+[\d.\-]+\s+([\d.]+)\s+([\d.]+)"', src.read_text(encoding="utf-8", errors="ignore"))
        wh = (round(float(vb.group(1))), round(float(vb.group(2)))) if vb else None
    elif src.suffix.lower() == ".png":
        out = IMG_OUT / "logo.png"; wh = encode_image(src, out, 640, keep_png=True)
    else:
        out = IMG_OUT / "logo.webp"; wh = encode_image(src, out, 640)
    done.append(f"logo: {out.as_posix()}")
    return f'<img class="logo" src="{rel(out)}" alt="{name} logo"{dims_attr(wh)}>'

def website():
    srcs = [p for p in sorted((INP / "assets-intake").glob("website.*")) if p.suffix.lower() in IMG]
    out = IMG_OUT / "website.webp"
    if out.exists(): out.unlink()
    if not srcs:
        return '<span class="device__empty">Open the demo to see it live</span>'
    wh = encode_image(srcs[0], out)
    done.append(f"website: {out.as_posix()}")
    return (f'<img class="device__screen" src="{rel(out)}" alt="Screenshot of the demo website"'
            f'{dims_attr(wh)} loading="lazy" decoding="async">')

# ---------------------------------------------------------------- markers
page = PAGE.read_text(encoding="utf-8") if PAGE.exists() else None
page_ns = [int(x) for x in re.findall(r"<!--\s*ingest:creative-(\d+)\s*-->", page or "")]
content = {"reviews": carousel("reviews"), "competitors": carousel("competitors"),
           "logo": logo(), "website": website()}
for n, src in creative_sources(page_ns).items():
    content[f"creative-{n}"] = creative(n, src)

filled, absent = [], []
if page is not None:
    for key, body in content.items():
        pat = re.compile(rf"(<!--\s*ingest:{re.escape(key)}\s*-->)(.*?)(<!--\s*/ingest:{re.escape(key)}\s*-->)", re.S)
        if pat.search(page):
            page = pat.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(3)}", page)
            filled.append(key)
        else:
            absent.append(key)
    PAGE.write_text(page, encoding="utf-8")

print("=== INGEST ===")
for d in done:          print(f"DONE     {d}")
for e in empty:         print(f"EMPTY    {e}")
for f, cmd in pending:  print(f"PENDING  {f}\n         -> {cmd}")
for u in unknown:       print(f"UNKNOWN  {u}")
if page is None:
    print("MARKERS  output/index.html not found - assets processed; markers fill on the next /ingest after Phase 3")
else:
    print(f"MARKERS  filled: {', '.join(filled) or '-'}" + (f" | not in page: {', '.join(absent)}" if absent else ""))
