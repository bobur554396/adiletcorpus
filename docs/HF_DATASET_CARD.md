---
license: cc-by-4.0
language:
- kk
- ru
- en
multilinguality: multilingual
pretty_name: AdiletCodex - Trilingual Article-Level Corpus of Kazakh Legislation
tags:
- legal
- law
- kazakhstan
- legislation
- adilet
- article-level
- trilingual
task_categories:
- text-retrieval
- text-classification
- text-generation
size_categories:
- 10K<n<100K
---

# AdiletCodex: A Trilingual (Kazakh-Russian-English) Article-Level Corpus of the Codes and Laws of Kazakhstan

A full-text, **article-level**, **trilingual (Kazakh + Russian + English)** corpus of the
currently in-force codes and substantive laws of the Republic of Kazakhstan, parsed from the
official legal database [adilet.zan.kz](https://adilet.zan.kz).

- **65,825** article records across **343** documents (**24 codes + 319 laws**, incl. the Constitution)
- **296** documents present in all three languages (RU 22,117 / KK 22,099 / EN 21,609)
- Adoption years **1991-2026**
- Each record: full article text + structural hierarchy (part/section/chapter/article) +
  numbered points + amendment notes + cross-reference links + rich document metadata
  (act form, legal sphere, adopting body, registration numbers, dates, status)

To our knowledge this is the **first article-structured, trilingual, full-text** corpus of
Kazakh legislation.

## Why this corpus
Kazakh legal NLP has lacked a **structured, full-text** foundation: existing resources are
either document-level metadata, Russian-only, or downstream QA sets built on top of statutes
they do not themselves release. AdiletCodex fills that gap with the **article** as the unit of
record, the **three official language versions** side by side, and the **structural +
amendment + metadata** context needed for legal information retrieval, cross-lingual and RAG
grounding, translation-fidelity study, and temporal ("law-as-of-date") modeling.

## Related datasets and how AdiletCodex differs
- **KazakhLawCorpus** (Tleubayeva, *Data* MDPI 2026; 215,889 records) - document-level
  **metadata only**, Kazakh only, no article text. AdiletCodex is complementary and strictly
  more granular: full text, article-level, trilingual.
- **justicedao/ipfs_kazakhstan_laws_ir** (HF, ~399k rows) - article-level but **Russian only**,
  undocumented, no hierarchy / amendments / status / KK / EN. AdiletCodex adds the two other
  official languages, the structural hierarchy, amendment notes, status, metadata, and docs.
- **olzhasAl/adilet-legal-qa-kz** (HF, 13,159 QA pairs, RU+KK) and other Kazakh legal-QA / LoRA
  sets - **downstream tasks**, not a source corpus. AdiletCodex provides the underlying statute
  text those tasks are grounded in.
- **Uzbek legal corpus** (Tomaris AI) - a methodological twin for a neighbouring jurisdiction
  (Uzbek-Latin only, no descriptor paper); AdiletCodex is the Kazakh, trilingual counterpart.
- **RusLawOD** (HF irlspbru/RusLawOD, 304k texts) - Russian national statutory corpus; a
  language / scope comparator, not Kazakh.

## Files
- `adiletcodex.jsonl` - one article per line (keeps nested paragraphs/notes/links)
- `adiletcodex.csv` - flat columns

## Load
```python
from datasets import load_dataset
ds = load_dataset("json", data_files="adiletcodex.jsonl", split="train")
```

## Schema
`doc_id, doc_type, lang, title, status, act_form, legal_sphere, legal_force, adopting_organ,
database_section, state_registry_number, npa_registration_number, adoption_date, change_date,
publication_date, adoption_place, region_action, part, section, chapter, article_id,
article_no, article_title, article_text, paragraphs, notes, links, url`

## License & source
Compilation: CC-BY-4.0. Underlying texts are official public acts of the Republic of
Kazakhstan (source: adilet.zan.kz). Unofficial research copy; verify in-force text on adilet.

## Citation
Mukhsimbayev, B., Pak, A., & Kuralbayev, A. (2026). *AdiletCodex: A Trilingual (Kazakh-Russian-English)
Article-Level Corpus of the Codes and Laws of Kazakhstan* (v1.0) [Data set]. Zenodo.
https://doi.org/10.5281/zenodo.22812626 (concept DOI: 10.5281/zenodo.22812625)
