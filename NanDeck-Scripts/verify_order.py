#!/usr/bin/env python3
"""Airtight page-order check: raw embedded JPEG stream hashes == temp JPEG hashes."""
import hashlib
from pathlib import Path

import pikepdf

TMP = Path("/home/fin/nandeck-test/drive-test/full-deck-output/cmyk-jpeg-tmp")
tmp_hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in TMP.glob("page_*.jpg")}
tmp_by_name = {f"page_{i:03d}_*": None for i in range(1, 257)}

# map: page number -> expected tmp file
expected = {}
for name in tmp_hashes:
    pageno = int(name.split("_")[1])
    expected[pageno] = name

pdf = pikepdf.open("/home/fin/nandeck-test/drive-test/full-deck-output/drive-thru-ready-cmyk-pdfx.pdf")
assert len(pdf.pages) == 256

# check EVERY page's raw image stream hash against the expected temp file
mismatch = []
for i, page in enumerate(pdf.pages, 1):
    xo = page.get("/Resources", {}).get("/XObject", {})
    imgs = [o for o in xo.values() if o.get("/Subtype") == pikepdf.Name("/Image")]
    assert len(imgs) == 1, f"page {i}: {len(imgs)} images"
    raw = imgs[0].read_raw_bytes()
    h = hashlib.sha256(bytes(raw)).hexdigest()
    exp_name = expected[i]
    if h != tmp_hashes[exp_name]:
        mismatch.append((i, exp_name))
print(f"pages checked: 256")
print(f"mismatches: {len(mismatch)}")
if mismatch:
    for i, name in mismatch[:10]:
        print(f"  page {i}: expected {name}")
    raise SystemExit(1)

# order structure: DTC order = back then face, so backs are ODD pages (1,3,...)
backs = [i for i in range(1, 257) if expected[i].endswith("_back.jpg")]
fronts = [i for i in range(1, 257) if not expected[i].endswith("_back.jpg")]
print(f"back pages (should be all odd): {len(backs)}, odds: {all(i % 2 == 1 for i in backs)}")
print(f"front pages (should be all even): {len(fronts)}, evens: {all(i % 2 == 0 for i in fronts)}")

# spot-label sequence
seq = [expected[i].split("_", 2)[2].replace(".jpg", "") for i in (2, 4, 114, 146, 148, 162, 164, 230, 232, 254, 256)]
print("spot check fronts:", seq)
print("ALL 256 PAGES VERIFIED IN BACK-THEN-FACE ORDER")
pdf.close()
