#!/usr/bin/env python3
"""Consolidate raw per-doc-per-lang JSON (codes + laws) into a clean release corpus.

Cleaning applied:
- English Civil Code (K940001000_) merges General+Special parts; drop its Special-part
  records (the Special part is provided separately by K990000409_).
- Drop KZ records that are byte-identical to the RU record of the same article
  (fake-Kazakh pages that served Russian).
- Drop empty-text records (repealed-article stubs) and dedup (doc_id, lang, article_no).
- Parse doc_date / doc_number from the citation line.

Outputs: data/adiletcodex.jsonl  and  data/adiletcodex.csv
"""
import json, glob, os, re, csv
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
RAW_CODES = ROOT / "data" / "raw"
RAW_LAWS = ROOT / "data" / "raw_laws"
OUT_JSONL = ROOT / "data" / "adiletcodex.jsonl"
OUT_CSV = ROOT / "data" / "adiletcodex.csv"

ART_PAT = {"rus": r"статья\s+(\d+(?:-\d+)?)",
           "kaz": r"(\d+(?:-\d+)?)-бап",
           "eng": r"article\s+(\d+(?:-\d+)?)"}
MONTHS = {"января":1,"февраля":2,"марта":3,"апреля":4,"мая":5,"июня":6,"июля":7,
          "августа":8,"сентября":9,"октября":10,"ноября":11,"декабря":12}

def art_no(title, lang):
    m = re.match(r"^\s*" + ART_PAT.get(lang, r"(\d+)"), title or "", re.I)
    return m.group(1) if m else None

def parse_citation(cit):
    cit = cit or ""
    d = m = y = None
    mm = re.search(r"от\s+(\d{1,2})\s+([А-Яа-я]+)\s+(\d{4})\s+года", cit)
    if mm:
        day, mon, year = int(mm.group(1)), MONTHS.get(mm.group(2).lower()), int(mm.group(3))
        if mon:
            d = f"{year:04d}-{mon:02d}-{day:02d}"
    num = re.search(r"№\s*([^\s.]+(?:\s*[IVXЗРКЗ-]+)?)", cit)
    return d, (num.group(1).strip() if num else None)

def iter_raw():
    for f in sorted(glob.glob(str(RAW_CODES / "*.json"))):
        b = os.path.basename(f)[:-5]; p = b.split("-")
        yield f, p[0], p[1], "-".join(p[2:]), "code"
    for f in sorted(glob.glob(str(RAW_LAWS / "*.json"))):
        b = os.path.basename(f)[:-5]; doc, lang = b.rsplit("-", 1)
        yield f, doc, lang, "", "law"

records = []
for f, doc_id, lang, slug, doc_type in iter_raw():
    try:
        d = json.load(open(f, encoding="utf-8"))
    except Exception:
        d = []
    for r in d:
        txt = (r.get("article_text") or "").strip()
        part = r.get("part")
        # English Civil Code: drop Special-part records (covered by K990000409_)
        if doc_id == "K940001000_" and lang == "eng" and part and "special" in part.lower():
            continue
        records.append({
            "doc_id": doc_id, "doc_type": doc_type, "slug": slug or None, "lang": lang,
            "title": r.get("title"), "status": r.get("status"),
            "doc_date": None, "doc_number": None, "citation": r.get("citation"),
            "part": part, "section": r.get("section"), "chapter": r.get("chapter"),
            "article_id": r.get("article_id"),
            "article_no": art_no(r.get("article_title"), lang),
            "article_title": r.get("article_title"), "article_text": txt,
            "paragraphs": r.get("paragraphs") or [], "notes": r.get("notes") or [],
            "links": r.get("links") or [], "url": r.get("url"),
        })

# attach rich document metadata scraped from old.adilet /info (data/meta/<doc_id>.json)
META_DIR = ROOT / "data" / "meta"
META_FIELDS = ["adoption_date", "change_date", "publication_date", "publication_reference",
               "act_form", "legal_sphere", "legal_force", "adopting_organ", "region_action",
               "state_registry_number", "npa_registration_number",
               "database_section", "adoption_place"]  # developer_organ dropped (always empty on adilet)
_meta_cache = {}
def load_meta(doc_id):
    if doc_id not in _meta_cache:
        try:
            _meta_cache[doc_id] = json.load(open(META_DIR / f"{doc_id}.json", encoding="utf-8")) or {}
        except Exception:
            _meta_cache[doc_id] = {}
    return _meta_cache[doc_id]
for rec in records:
    m = load_meta(rec["doc_id"])
    for f in META_FIELDS:
        rec[f] = m.get(f)

# doc_date/doc_number: parse from each citation, then propagate the best value
# (prefer the Russian citation) to every language version of the same document.
for rec in records:
    rec["doc_date"], rec["doc_number"] = parse_citation(rec["citation"])
docmeta = {}  # doc_id -> {"date","number"}: best non-empty value PER FIELD, Russian preferred
for rec in records:
    m = docmeta.setdefault(rec["doc_id"], {"date": None, "number": None})
    ru = rec["lang"] == "rus"
    if rec["doc_date"] and (m["date"] is None or ru):
        m["date"] = rec["doc_date"]
    if rec["doc_number"] and (m["number"] is None or ru):
        m["number"] = rec["doc_number"]
for rec in records:
    m = docmeta.get(rec["doc_id"])
    if m:
        rec["doc_date"] = rec["doc_date"] or m["date"]
        rec["doc_number"] = rec["doc_number"] or m["number"]
    # fallback: no date on any citation -> use adoption_date from the /info metadata (same
    # semantics = date the act was adopted). doc_number is NOT filled from the registry number:
    # the citation number and state/npa registry numbers are different identifiers.
    if not rec["doc_date"]:
        rec["doc_date"] = rec.get("adoption_date")

# Detect fake-Kazakh documents: a real KZ article text carries Kazakh-specific letters.
# If a doc's KZ side is overwhelmingly free of them, its /kaz/ page served Russian -> drop it.
KAZ = set("әғқңөұүһіӘҒҚҢӨҰҮҺІ")
kaz_docs = defaultdict(list)
for rec in records:
    if rec["lang"] == "kaz" and rec["article_text"]:
        kaz_docs[rec["doc_id"]].append(any(c in KAZ for c in rec["article_text"]))
fake_kaz = {d for d, flags in kaz_docs.items() if flags and sum(flags)/len(flags) < 0.30}

clean = []
seen = set()
dropped = {"empty": 0, "fake_kaz": 0, "dup_key": 0}
for rec in records:
    if not rec["article_text"]:
        dropped["empty"] += 1; continue
    if rec["lang"] == "kaz" and rec["doc_id"] in fake_kaz:
        dropped["fake_kaz"] += 1; continue
    key = (rec["doc_id"], rec["lang"], rec["article_no"], rec["article_title"])
    if key in seen:
        dropped["dup_key"] += 1; continue
    seen.add(key)
    clean.append(rec)
print("fake-Kazakh docs dropped:", sorted(fake_kaz))

with open(OUT_JSONL, "w", encoding="utf-8") as fo:
    for rec in clean:
        fo.write(json.dumps(rec, ensure_ascii=False) + "\n")

CSV_COLS = ["doc_id","doc_type","slug","lang","title","status","doc_date","doc_number",
            "act_form","legal_sphere","legal_force","adopting_organ",
            "database_section","state_registry_number","npa_registration_number",
            "adoption_date","change_date","publication_date","adoption_place","region_action",
            "part","section","chapter","article_id","article_no","article_title",
            "article_text","url"]
with open(OUT_CSV, "w", encoding="utf-8", newline="") as fo:
    w = csv.DictWriter(fo, fieldnames=CSV_COLS, extrasaction="ignore")
    w.writeheader()
    for rec in clean:
        w.writerow(rec)

from collections import Counter
print("raw records:", len(records), "| clean records:", len(clean))
print("dropped:", dropped)
print("by lang:", dict(Counter(r["lang"] for r in clean)))
print("by doc_type:", dict(Counter(r["doc_type"] for r in clean)))
print("distinct docs:", len(set(r["doc_id"] for r in clean)))
print("with doc_date parsed:", sum(1 for r in clean if r["doc_date"]), "/", len(clean))
print("wrote:", OUT_JSONL.name, OUT_CSV.name)
