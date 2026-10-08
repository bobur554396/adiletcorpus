#!/usr/bin/env python3
"""
fix_duplicate_articles.py

Resolve the 19 (doc_id, lang, article_no) collision groups found in the v1.1
pre-release integrity audit of data/adiletcodex.jsonl, without dropping any
article wording.

The audit traced the collisions to three mechanisms:

  (a) a number that legitimately recurs across different structural parts of a
      document - NOT a true duplicate once part/chapter context is considered;
  (b) entry-into-force / amendment / old-redaction clauses that the parser split
      off from their parent article in the "Final and transitional provisions"
      (or an enactment) article as separate article records;
  (c) compound inserted article numbers (e.g. "15-24", "18-1") truncated to the
      base number ("15", "18") in one language while the other two languages
      already carry the correct full number.

Resolution, per group:
  (c) RENUMBER  - set article_no to the correct full value recovered from the
                  article title (and confirmed against the aligned KK/RU rows,
                  which already hold the full number). No record removed.
  (b) MERGE     - append the split-off fragment's title line and body text back
                  into the correct parent article record (document order
                  preserved), then drop the now-redundant fragment record.
                  Fragment paragraphs are appended to the parent's paragraphs.
  (d) MERGE     - three groups turned out to be a genuine second record for the
                  same in-force article in one language (a stale translation, a
                  future-effective redaction block, or a wrong-chapter copy).
                  The secondary record is merged into the canonical one (all
                  wording preserved) and dropped.

No group required the pure "(a) keep both" branch: every collision was either a
truncated compound number (c) or a split/duplicate record (b/d). Group 1 (the
Kazakh Criminal Code) was initially a candidate for (a) - the stray "51-бап"
sits in a different `part` - but it proved to be the old-code Article 51 wording
quoted by the enactment article 467 ("...51-бап мынадай редакцияда жазылсын:"),
i.e. a (b) fragment, and is merged back into article 467.

The collisions are language-specific; the other two languages parsed each
article cleanly. Fixing a broken language therefore brings it INTO alignment
with the already-correct languages - no cross-language renumbering is needed
beyond (c), where KK/RU are already correct.

Input : data/v1.1_predupfix_backup/adiletcodex.prefix.jsonl  (pre-fix snapshot)
Output: data/adiletcodex.jsonl                               (fixed, in place)

Each operation asserts the record it targets (doc_id, lang, article_id,
article_no, title prefix) so the script fails loudly rather than corrupting data
if run against a different input.

Author: Bobur Mukhsimbayev
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "data" / "v1.1_predupfix_backup" / "adiletcodex.prefix.jsonl"
DST = REPO / "data" / "adiletcodex.jsonl"

# ---------------------------------------------------------------------------
# Operation table. Line numbers are 0-based indices into the pre-fix snapshot
# and are validated by the accompanying (doc_id, lang, article_id, article_no,
# title-prefix) assertions before anything is changed.
# ---------------------------------------------------------------------------

# (c) truncated compound numbers -> set the correct full article_no
RENUMBER = [
    # line, new_no, (doc_id, lang, article_id, old_no, title_prefix)
    (34082, "18-1",  ("Z020000344_", "eng", "z110", "18", "Article 18 - 1.")),
    (36109, "15-24", ("Z030000474_", "eng", "z15",  "15", "Article 15")),
    (36110, "15-25", ("Z030000474_", "eng", "z15",  "15", "Article 15")),
    (36111, "15-26", ("Z030000474_", "eng", "z15",  "15", "Article 15")),
    (36112, "15-27", ("Z030000474_", "eng", "z15",  "15", "Article 15")),
]

# (b) + (d) merges -> target parent line, list of source fragment lines
# Each entry: (target_line, [source_lines...], cause, note,
#              target_expect, {source_line: source_expect})
MERGE = [
    # --- (b) K1700000125 Subsoil Code: Article 277 enforcement enumeration
    (16898, [16899, 16900, 16901, 16902, 16903], "b",
     "Article 277 entry-into-force enumeration split into 5 fragments (38/54/120/126/236)",
     ("K1700000125", "eng", "z277", "277", "Article 277."),
     {
        16899: ("K1700000125", "eng", "z38",  "38",  "article 38;"),
        16900: ("K1700000125", "eng", "z54",  "54",  "Article 54, and paragraphs"),
        16901: ("K1700000125", "eng", "z120", "120", "Article 120, except for positions"),
        16902: ("K1700000125", "eng", "z126", "126", "article 126, except for"),
        16903: ("K1700000125", "eng", "z236", "236", "article 236;"),
     }),
    # --- (b) Z090000191_ AML Law: Article 10 reporting-terms list split off
    (41424, [41425], "b",
     "Article 10 reporting-terms list split off (titled 'Article 4, paragraph 1 ...')",
     ("Z090000191_", "eng", "z10", "10", "Article 10."),
     {41425: ("Z090000191_", "eng", "z4", "4", "Article 4, paragraph 1, of this Law")}),
    # --- (b) Z1100000413 State Property Law (rus): amendment-addition fragments
    (43545, [43546, 43547], "b",
     "Статья 1: two added-subparagraph blocks (2-1, 6-1) split off",
     ("Z1100000413", "rus", "z4", "1", "Статья 1. Основные понятия"),
     {
        43546: ("Z1100000413", "rus", "z1840", "1", "Статья 1 дополнена подпунктом 2-1)"),
        43547: ("Z1100000413", "rus", "z1",    "1", "Статья 1 дополнена подпунктом 6-1)"),
     }),
    (43557, [43558], "b",
     "Статья 10: added-point block (1-1) split off",
     ("Z1100000413", "rus", "z1869", "10", "Статья 10. Передача коммунального имущества"),
     {43558: ("Z1100000413", "rus", "z1873", "10", "Статья 10 дополнена пунктом 1-1")}),
    (43727, [43728], "b",
     "Статья 164: added-point block (4-1) split off",
     ("Z1100000413", "rus", "z1221", "164", "Статья 164. Особенности создания"),
     {43728: ("Z1100000413", "rus", "z2215", "164", "Статья 164 дополнена пунктом 4-1")}),
    (43553, [43554], "b",
     "Статья 7: added-point block (4) split off",
     ("Z1100000413", "rus", "z89", "7", "Статья 7. Субъекты управления"),
     {43554: ("Z1100000413", "rus", "z1863", "7", "Статья 7 дополнена пунктом 4")}),
    # --- (b) Z1200000541 Energy Saving Law: Article 24 enforcement list split off
    (44853, [44854], "b",
     "Article 24 (order of entry into force) enumeration split off",
     ("Z1200000541", "eng", "z24", "24", "Article 24. Order of entering of this Law into force"),
     {44854: ("Z1200000541", "eng", "z9", "9", "Article 9 that enters into force from 1 January 2013;")}),
    # --- (b) Z1400000176 Rehabilitation/Bankruptcy Law: Article 26 quorum clause split off
    (46366, [46367], "b",
     "Article 26 (creditors' meeting decision procedure) competence clause split off",
     ("Z1400000176", "eng", "z26", "26", "Article 26. The decision making procedure"),
     {46367: ("Z1400000176", "eng", "z26", "26-2", "Article 26-2 of this Law - upon making amendments")}),
    # --- (b) Z1500000405 Compulsory Social Medical Insurance Law: Article 40 schedule split off
    (49758, [49759], "b",
     "Article 40 (transitional provisions) entry-into-force schedule split off",
     ("Z1500000405", "eng", "z40", "40", "Article 40. Transitional provisions"),
     {49759: ("Z1500000405", "eng", "z5", "5", "Article 5, paragraph 1, which shall enter into force")}),
    # --- (b) K1400000226 Criminal Code (kaz): Article 467 enactment quoting old Article 51 text
    (2813, [2814], "b",
     "Article 467 (enactment article) quotes the old-code Article 51 wording, split off as '51-бап'",
     ("K1400000226", "kaz", "z467", "467", "467-бап. Осы Кодексті қолданысқа енгізу"),
     {2814: ("K1400000226", "kaz", "z1735", "51", "51-бап. Мүлікті тәркілеу")}),
    # --- (d) K1400000235 Administrative Offences Code (eng): stale wrong-chapter copy of Art 187
    (6114, [6053], "d",
     "Article 187 (tourist activity) - canonical Chapter 14 record; stale Chapter-12 copy merged in",
     ("K1400000235", "eng", "z187", "187", "Article 187. Breach of the legislation of the Republic of Kazakhstan on tourist activity"),
     {6053: ("K1400000235", "eng", "z187", "187", "Article 187. Breach of the legislation of the Republic of Kazakhstan on tourism")}),
    # --- (d) K1500000414 Labour Code (eng): future-effective redaction block of Art 143
    (11899, [11900], "d",
     "Article 143 - current redaction canonical; future (01.07.2026) redaction block merged in",
     ("K1500000414", "eng", "z143", "143", "Article 143. Regulation of labor of civil servants"),
     {11900: ("K1500000414", "eng", "z143", "143", "Article 143. Regulation of the employment of civil servants")}),
    # --- (d) Z1100000380 Law on Law-Enforcement Service (eng): stale translation of Art 52
    (42691, [42692], "d",
     "Article 52 (attestation/certification committee decision) - detailed record canonical; stale short translation merged in",
     ("Z1100000380", "eng", "z1547", "52", "Article 52. Decision of the certification committee"),
     {42692: ("Z1100000380", "eng", "z1552", "52", "Article 52. Decision of attestation commission")}),
]


def check(rec, expect, line):
    doc, lang, aid, no, tprefix = expect
    assert rec["doc_id"] == doc, f"L{line} doc_id {rec['doc_id']!r} != {doc!r}"
    assert rec["lang"] == lang, f"L{line} lang {rec['lang']!r} != {lang!r}"
    assert rec["article_id"] == aid, f"L{line} article_id {rec['article_id']!r} != {aid!r}"
    assert rec["article_no"] == no, f"L{line} article_no {rec['article_no']!r} != {no!r}"
    title = rec.get("article_title") or ""
    assert title.startswith(tprefix), f"L{line} title {title[:60]!r} !startswith {tprefix!r}"


def merge_text(target, source):
    """Append the source fragment (its title line + body) to the target article,
    fully preserving wording. Also append the source paragraphs."""
    ttext = (target.get("article_text") or "").rstrip()
    stitle = (source.get("article_title") or "").strip()
    sbody = (source.get("article_text") or "").strip()
    piece = "\n".join(p for p in (stitle, sbody) if p)
    target["article_text"] = (ttext + "\n" + piece) if ttext else piece
    sp = source.get("paragraphs") or []
    if sp:
        target["paragraphs"] = (target.get("paragraphs") or []) + sp


def main():
    if not SRC.exists():
        sys.exit(f"missing input snapshot: {SRC}")
    records = []
    with SRC.open(encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            records.append(json.loads(line))
    n_in = len(records)

    drop = set()           # line indices to drop
    renumbered = 0
    merged_sources = 0
    parents_touched = set()

    # (c) renumber
    for line, new_no, expect in RENUMBER:
        rec = records[line]
        check(rec, expect, line)
        rec["article_no"] = new_no
        renumbered += 1

    # (b)/(d) merges
    for entry in MERGE:
        target_line, source_lines, cause, note, texp, sexp = entry
        target = records[target_line]
        check(target, texp, target_line)
        for sl in source_lines:
            src = records[sl]
            check(src, sexp[sl], sl)
            merge_text(target, src)
            drop.add(sl)
            merged_sources += 1
        parents_touched.add(target_line)

    out = [r for i, r in enumerate(records) if i not in drop]
    n_out = len(out)

    tmp = DST.with_suffix(".jsonl.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    tmp.replace(DST)

    print(f"input records        : {n_in}")
    print(f"renumbered (c)       : {renumbered}")
    print(f"fragments merged     : {merged_sources}")
    print(f"parents extended     : {len(parents_touched)}")
    print(f"records removed       : {len(drop)}")
    print(f"output records       : {n_out}  (delta {n_out - n_in})")


if __name__ == "__main__":
    main()
