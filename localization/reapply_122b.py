#!/usr/bin/env python3
"""Re-apply ONLY the 122B legal_sphere / publication_reference translations to the
already-localized data/adiletcodex.jsonl (which already carries *_ru provenance
columns from the earlier 32B pass). Keyed on the existing *_ru columns:
  eng rows -> new EN, kaz rows -> new KK, rus rows keep RU.
Provenance *_ru columns stay unchanged; all other fields untouched.
Regenerates adiletcodex.csv and both .gz.
"""
import json, os, csv, gzip, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOC = os.path.join(ROOT, "localization")
JSONL = os.path.join(ROOT, "data", "adiletcodex.jsonl")
CSV = os.path.join(ROOT, "data", "adiletcodex.csv")
FIELDS = ["legal_sphere", "publication_reference"]
LANGKEY = {"eng": "en", "kaz": "kk"}  # rus -> keep RU


def load_map(field):
    m = {}
    with open(os.path.join(LOC, f"{field}_map.jsonl")) as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                m[r["ru"]] = {"en": r["en"], "kk": r["kk"]}
    return m


MAPS = {f: load_map(f) for f in FIELDS}

# CSV columns as in the original packaging
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


def main():
    out_path = JSONL + ".new"
    n = 0
    missing = 0
    changed = {f: 0 for f in FIELDS}
    with open(JSONL) as fi, open(out_path, "w", encoding="utf-8") as fo:
        for line in fi:
            if not line.strip():
                continue
            d = json.loads(line)
            lang = d.get("lang")
            lk = LANGKEY.get(lang)
            for field in FIELDS:
                ru = d.get(field + "_ru")
                if ru in (None, ""):
                    continue
                if lk is None:  # rus row keeps the Russian original
                    d[field] = ru
                    continue
                tr = MAPS[field].get(ru)
                if tr is None:
                    missing += 1
                    continue  # leave as-is
                new_val = tr[lk]
                if d.get(field) != new_val:
                    changed[field] += 1
                d[field] = new_val
            fo.write(json.dumps(d, ensure_ascii=False) + "\n")
            n += 1
    os.replace(out_path, JSONL)
    print("records written:", n)
    print("unmapped (_ru not in map):", missing)
    print("values changed:", changed)

    with open(CSV, "w", encoding="utf-8", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=CSV_COLS, extrasaction="ignore")
        w.writeheader()
        with open(JSONL) as fi:
            for line in fi:
                if line.strip():
                    w.writerow(json.loads(line))
    print("csv written")

    for base in (JSONL, CSV):
        with open(base, "rb") as fi, gzip.open(base + ".gz", "wb", compresslevel=6) as fo:
            shutil.copyfileobj(fi, fo)
        print("gz written:", os.path.basename(base) + ".gz")


if __name__ == "__main__":
    main()
