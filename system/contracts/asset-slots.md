# Contract: Asset Slots  (v2.0.0 - PresentationOS)

The interface between the operator's drop folders, ingestion
(system/scripts/ingest-assets.py via /ingest) and the page's ingest
markers (pitch-sections contract). Folders in, markers out - no
shopping list, no generation.

## Drop folders -> page

| drop here                                   | becomes                                        | fills marker |
|---------------------------------------------|------------------------------------------------|--------------|
| input/reviews/<platform>/*  (or reviews/*)   | assets/images/reviews/<platform>/NN.webp       | ingest:reviews |
| input/competitors/<competitor>/*            | assets/images/competitors/<competitor>/NN.webp | ingest:competitors |
| input/creative/creative-N.*  (one block = N)| assets/video/creative-N.mp4 + poster, or assets/images/creative-N.webp | ingest:creative-N |
| input/assets-intake/logo.*                  | assets/images/logo.(svg\|png\|webp)            | ingest:logo |
| input/assets-intake/website.*               | assets/images/website.webp                     | ingest:website |

Naming:
1. Subfolder names become labels: `google/` -> "Google",
   `acme-plumbing/` -> "Acme Plumbing". Files sit directly in reviews/
   -> label "Reviews".
2. Optional `source.txt` (one URL) in any reviews/competitors subfolder:
   shown in the browser-frame address bar - the visible proof that the
   screenshots were collected by hand from the real source.
3. Slide order = filename order. Screenshot month (file date) appears in
   the caption.
4. Creative: name files `creative-1.*`, `creative-2.*` to match the
   `### Creative N` blocks in client.md. With exactly one block and one
   file, any filename is accepted.

## Processing (deterministic, script-owned)

- Images: longest side capped at 1600px, WebP q82 (Pillow, else cwebp).
  SVG logos are copied as-is; PNG logos keep alpha.
- Video: h.264 CRF 23 + AAC 128k, width capped at 1080, +faststart, and a
  WebP poster from the first second (ffmpeg). Audio is KEPT - it is an ad.
- Missing tool -> the file is listed PENDING with the exact command.
- Re-running /ingest rebuilds every folder's output and every marker
  from scratch (idempotent). Removing a screenshot from input/ removes
  its slide on the next run.
- Originals in input/creative/ are gitignored (heavy); screenshots,
  logo and research are tracked so a clone can be rebuilt.
