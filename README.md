# AdiletCodex - trilingual article-level corpus of the Codes and Laws of Kazakhstan

An article-level, trilingual (Kazakh / Russian / English) corpus of the currently in-force
**codes and laws** of the Republic of Kazakhstan, parsed from the official legal database
[adilet.zan.kz](https://adilet.zan.kz).

**Published on Zenodo:** https://doi.org/10.5281/zenodo.22812626 (concept DOI
10.5281/zenodo.22812625 always resolves to the latest version).
**On HuggingFace:** https://huggingface.co/datasets/bobur-m/adiletcodex

343 documents, 65,825 article records (RU 22,117 / KK 22,099 / EN 21,609). License
CC-BY-4.0. See [`README_DATASET.md`](README_DATASET.md) for the full schema and usage.

## Why this corpus
Existing Kazakh legal datasets are either metadata-only (KazakhLawCorpus) or full text at the
whole-document level, or QA sets. None provides clean **article-level segmentation with
structural hierarchy**, and none is **trilingual** (KK+RU+EN) at the article level. See
`docs/PACKAGING_NOTES.md`.

## Contents
- 343 documents (24 in-force codes + 319 laws, including the Constitution and 16 constitutional
  laws) x {kaz, rus, eng} at the article level: 65,825 article records; 21,440 article numbers
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
  paper/              # data descriptor manuscript
  CHANGELOG.md        # dataset versions
```

## Data
The packaged dataset (`adiletcodex.jsonl` / `.csv`) is published on Zenodo and the Hugging Face
Hub (links above); because of its size it is not stored in this repository. See
`docs/CODEBOOK.md` for field definitions and `CHANGELOG.md` for the version history.

## Status
Published on Zenodo (v1.0, DOI 10.5281/zenodo.22812626) and HuggingFace. A data descriptor is
in preparation (target: *Data* / MDPI).
