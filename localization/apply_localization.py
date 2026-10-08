#!/usr/bin/env python3
"""Apply v1.1 extended localization to data/adiletcodex.jsonl and regenerate CSV + gz.

Localizes four document-passport fields per the row's `lang`:
  - legal_sphere, publication_reference  (Group B: Qwen machine translation)
  - adopting_organ, database_section     (Group A: curated term map)
For every row a `<field>_ru` provenance column is added holding the pre-transform value.
eng rows get EN, kaz rows get KK, rus rows keep Russian. None/empty stays unchanged.
"""
import json, os, csv, gzip, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOC = os.path.join(ROOT, "localization")
JSONL = os.path.join(ROOT, "data", "adiletcodex.jsonl")
CSV = os.path.join(ROOT, "data", "adiletcodex.csv")

FIELDS = ["legal_sphere", "publication_reference", "adopting_organ", "database_section"]


def load_jsonl_map(path):
    m = {}
    with open(path) as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            m[r["ru"]] = {"en": r["en"], "kk": r["kk"]}
    return m


def load_json_map(path):
    raw = json.load(open(path))
    return {k: {"en": v["en"], "kk": v["kk"]} for k, v in raw.items()}


MAPS = {
    "legal_sphere": load_jsonl_map(os.path.join(LOC, "legal_sphere_map.jsonl")),
    "publication_reference": load_jsonl_map(os.path.join(LOC, "publication_reference_map.jsonl")),
    "adopting_organ": load_json_map(os.path.join(LOC, "adopting_organ_map.json")),
    "database_section": load_json_map(os.path.join(LOC, "database_section_map.json")),
}

LANGKEY = {"eng": "en", "kaz": "kk"}

# JSONL: insert each _ru immediately after its source field, preserving all other keys/order.
def relocalize_record(d):
    missing = []
    localized = {}
    for field in FIELDS:
        orig = d.get(field)
        lk = LANGKEY.get(d.get("lang"))  # None for rus
        if orig in (None, ""):
            localized[field] = orig
        elif lk is None:  # rus row keeps Russian source
            localized[field] = orig
        else:
            tr = MAPS[field].get(orig)
            if tr is None:
                missing.append((field, orig))
                localized[field] = orig
            else:
                localized[field] = tr[lk]
    # rebuild dict with _ru inserted after each source field
    out = {}
    for k, v in d.items():
        if k in FIELDS:
            out[k] = localized[k]
            out[k + "_ru"] = v  # provenance = pre-transform value
        else:
            out[k] = v
    return out, missing


def main():
    out_path = JSONL + ".new"
    n = 0
    all_missing = []
    with open(JSONL) as fi, open(out_path, "w", encoding="utf-8") as fo:
        for line in fi:
            if not line.strip():
                continue
            d = json.loads(line)
            out, missing = relocalize_record(d)
            all_missing.extend(missing)
            fo.write(json.dumps(out, ensure_ascii=False) + "\n")
            n += 1
    os.replace(out_path, JSONL)
    print("records written:", n)
    print("unmapped values encountered:", len(all_missing))
    if all_missing:
        for f, v in all_missing[:10]:
            print("  MISSING", f, repr(v)[:80])

    # CSV: flat columns; mirror localization, each _ru right after its field.
    CSV_COLS = ["doc_id", "doc_type", "slug", "lang", "title", "status", "doc_date",
                "doc_number", "act_form", "act_form_ru",
                "legal_sphere", "legal_sphere_ru",
                "adopting_organ", "adopting_organ_ru",
                "database_section", "database_section_ru",
                "state_registry_number", "npa_registration_number",
                "adoption_date", "change_date", "publication_date",
                "publication_reference", "publication_reference_ru",
                "adoption_place", "region_action",
                "part", "section", "chapter", "article_id", "article_no",
                "article_title", "article_text", "url"]
    with open(CSV, "w", encoding="utf-8", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=CSV_COLS, extrasaction="ignore")
        w.writeheader()
        with open(JSONL) as fi:
            for line in fi:
                if not line.strip():
                    continue
                w.writerow(json.loads(line))
    print("csv written")

    # gzip both
    for base in (JSONL, CSV):
        with open(base, "rb") as fi, gzip.open(base + ".gz", "wb", compresslevel=6) as fo:
            shutil.copyfileobj(fi, fo)
        print("gz written:", os.path.basename(base) + ".gz")


if __name__ == "__main__":
    main()
