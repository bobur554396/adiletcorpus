---
license: cc-by-4.0
language:
- kk
- ru
- en
multilinguality: multilingual
pretty_name: 'AdiletCodex: Trilingual (KK/RU/EN) Article-Level Corpus of Kazakh Legal Codes and Laws'
tags:
- legal
- law
- legal-nlp
- kazakhstan
- kz
- kazakh
- russian
- english
- legislation
- statute
- codes
- laws
- adilet
- article-level
- trilingual
- multilingual
- low-resource
- central-asia
- legal-information-retrieval
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

- **65,807** article records across **343** documents (**24 codes + 319 laws**, incl. the Constitution)
- **296** documents present in all three languages (RU 22,112 / KK 22,098 / EN 21,597)
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
`doc_id, doc_type, slug, lang, title, status, act_form, act_form_ru, legal_sphere, legal_sphere_ru,
adopting_organ, adopting_organ_ru, database_section, database_section_ru, state_registry_number,
npa_registration_number, adoption_date, change_date, publication_date, publication_reference,
publication_reference_ru, adoption_place, region_action, citation, doc_date, doc_number, part,
section, chapter, article_id, article_no, article_title, article_text, paragraphs, notes, links, url`

(37 fields total; `paragraphs`, `notes`, `links` are nested and JSONL-only, so the CSV carries
the 34 scalar fields. `citation` is the human-readable source citation, with `doc_date` /
`doc_number` parsed from it.)

**Language of metadata fields.** Only `title`, `status`, `article_title`, `article_text` are
truly per-language and are the **official** adilet translations. The document-"passport" fields
come from adilet's Russian-only document card; in v2.0 several are **localized** to the row's
language, each with an `*_ru` companion preserving the Russian source (Russian rows keep the
Russian value):

- **Curated term map** (hand-reviewed, not machine translation): `act_form`, `adopting_organ`,
  `database_section`.
- **Machine-translated (local Qwen3.5-122B-A10B, thinking disabled) reference metadata** -
  convenience only, not authoritative, with the Russian source kept in the `*_ru` companion:
  `legal_sphere`, `publication_reference`. The Kazakh output uses correct Kazakh legal
  terminology (the earlier Qwen2.5-32B Kazakh was replaced). A number-preservation check
  protects all digits/dates/article numbers in `publication_reference` (Russian original kept
  on any mismatch).
- **Still Russian-by-source:** `region_action`, `adoption_place`.

Use `status` for validity/in-force state. Reproducibility artifacts (term + translation maps,
QA-failure log, scripts) are in `localization/`.

> **Changed in v2.0 (major):** `act_form`, `adopting_organ`, `database_section` are localized per
> `lang` via a curated map, and `legal_sphere`, `publication_reference` via machine translation
> (all with `*_ru` provenance companions); the redundant/mislabeled `legal_force` field was
> removed (use `status` for in-force state). Separately, 18 parser-artifact records (split-off
> entry-into-force / amendment fragments, a quoted old-code article, truncated compound article
> numbers, and stale same-language duplicates) were repaired without dropping any wording, so the
> record count is 65,807 (was 65,825 in v1.0) with 0 duplicate `(doc_id, lang, article_no)` keys.

## License & source
Compilation: CC-BY-4.0. Underlying texts are official public acts of the Republic of
Kazakhstan (source: adilet.zan.kz). Unofficial research copy; verify in-force text on adilet.

## Citation
Mukhsimbayev, B., Pak, A., & Kuralbayev, A. (2026). *AdiletCodex: A Trilingual (Kazakh-Russian-English)
Article-Level Corpus of the Codes and Laws of Kazakhstan* (v2.0) [Data set]. Zenodo.
https://doi.org/10.5281/zenodo.22812625 (concept DOI, always resolves to the latest version).
Latest is v2.0 (version DOI 10.5281/zenodo.23260689, published 2026-10-09); v1.0 version DOI:
10.5281/zenodo.22812626.
