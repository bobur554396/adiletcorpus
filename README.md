# AdiletCodex - trilingual article-level corpus of the Codes and Laws of Kazakhstan

An article-level, trilingual (Kazakh / Russian / English) corpus of the currently in-force
**codes and laws** of the Republic of Kazakhstan, parsed from the official legal database
[adilet.zan.kz](https://adilet.zan.kz).

**On Zenodo:** https://doi.org/10.5281/zenodo.22812625 (concept DOI, always resolves to the
latest version; the v1.0 version DOI is 10.5281/zenodo.22812626).
**On HuggingFace:** https://huggingface.co/datasets/bobur-m/adiletcodex

343 documents, 65,807 article records (RU 22,112 / KK 22,098 / EN 21,597). License
CC-BY-4.0. See [`README_DATASET.md`](README_DATASET.md) for the full schema and usage.

## Why this corpus
Existing Kazakh legal datasets are either metadata-only (KazakhLawCorpus) or full text at the
whole-document level, or QA sets. None provides clean **article-level segmentation with
structural hierarchy**, and none is **trilingual** (KK+RU+EN) at the article level. See
`docs/PACKAGING_NOTES.md`.

## Contents
- 343 documents (24 in-force codes + 319 laws, including the Constitution and 16 constitutional
  laws) x {kaz, rus, eng} at the article level: 65,807 article records; 21,445 article numbers
  aligned across all three official languages.
- QC passed: languages are genuinely distinct (100% of KZ records carry Kazakh-specific
  letters; 0 cross-language byte-identical texts), structural hierarchy populated, repealed
  articles left as heading-only stubs.

## Layout
```
adiletcorpus/
  codes_current.tsv   # the in-force codes (doc_id, slug, title)
  data/               # packaged release (jsonl/csv, git-ignored - download from Zenodo/HF)
  docs/               # CODEBOOK.md, PACKAGING_NOTES.md, HF_DATASET_CARD.md, ZENODO_METADATA.md
  notebooks/          # QC + EDA
  CHANGELOG.md        # dataset versions
```

## Data
The packaged dataset (`adiletcodex.jsonl` / `.csv`) is published on Zenodo and the Hugging Face
Hub (links above); because of its size it is not stored in this repository. See
`docs/CODEBOOK.md` for field definitions and `CHANGELOG.md` for the version history.

## Status
v2.0 is published (2026-10-09) on Zenodo (version DOI 10.5281/zenodo.23260689) and HuggingFace,
under the concept DOI 10.5281/zenodo.22812625 (always resolves to the latest version). v2.0 is a
major release: breaking schema changes plus a duplicate/fragment data fix (see `CHANGELOG.md`).
v1.0 remains available as an earlier version (version DOI 10.5281/zenodo.22812626). A data
descriptor is in preparation (target: *Data* / MDPI).
