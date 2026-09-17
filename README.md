# AdiletCodex - trilingual article-level corpus of the Codes of Kazakhstan

An article-level, trilingual (Kazakh / Russian / English) corpus of the currently in-force
**codes** of the Republic of Kazakhstan, parsed from the official legal database
[adilet.zan.kz](https://old.adilet.zan.kz).

This is the **data / research project**. The crawler that produces it is a separate,
reusable tool: [`adilet-parser`](https://github.com/bobur554396/adilet-parser)
(expected as a sibling directory `../adilet-parser`).

## Why this corpus
Existing Kazakh legal datasets on HuggingFace are either metadata-only (KazakhLawCorpus) or
full text at the whole-document level (kurumikz, Any0ka), or QA sets. None provides clean
**article-level segmentation with structural hierarchy**, and none is **trilingual**
(KK+RU+EN) at the article level. See `docs/PACKAGING_NOTES.md` and, for the wider landscape,
`../uzlexcorpus/docs/RELATED_DATASETS.md`.

## Contents (current state)
- 24 in-force codes x {kaz, rus, eng}, article-level. ~29.5k article records.
- QC passed: languages are genuinely distinct (100% of KZ records carry Kazakh-specific
  letters; 0 real cross-language duplicate texts), hierarchy populated, repealed articles
  correctly left as heading-only stubs.

## Layout
```
adiletcorpus/
  codes_current.tsv        # the 24 in-force codes (doc_id, slug, title) = corpus scope
  src/
    crawl_all.sh           # crawl every code x {rus,kaz,eng} via ../adilet-parser -> data/raw
    (todo) package_corpus.py, qc_corpus.py
  data/
    raw/                   # per-doc-per-lang JSON from the parser (git-ignored; regenerate)
    (todo) adiletcodex.jsonl / .csv   # packaged release
  notebooks/
    kz_codes_qc.ipynb      # QC + EDA (built by build_qc_notebook.py)
    figs/
  docs/
    PACKAGING_NOTES.md      # cross-language quirks + packaging rules (read before packaging)
  (todo) README_DATASET.md, LICENSE, docs/CODEBOOK.md, docs/ZENODO_METADATA.md, descriptor/
```

## Rebuild
```bash
# 1. crawl (needs ../adilet-parser and the ml311 python env with scrapy)
sh src/crawl_all.sh
# 2. QC / EDA
python notebooks/build_qc_notebook.py     # regenerates & executes notebooks/kz_codes_qc.ipynb
```

## Status / next
Raw crawled and QC-clean. Next: packaging (JSONL/CSV + dedup + cross-language alignment by
(code, article_no) - note the English Civil Code merges General+Special parts, see
`docs/PACKAGING_NOTES.md`), then Zenodo + HuggingFace + a data descriptor (target:
Data / MDPI or Data in Brief).
