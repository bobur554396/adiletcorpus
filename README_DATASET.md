# AdiletCodex: A Trilingual (Kazakh-Russian-English) Article-Level Corpus of the Codes and Laws of Kazakhstan

**Version 1.1** - Source: adilet.zan.kz (Information and Legal System of Normative Legal Acts of the Republic of Kazakhstan, "Adilet")

## Authors
- Bobur Mukhsimbayev (corresponding), ORCID 0009-0008-4606-3628, b.mukhsimbaev@kbtu.kz
- Alexandr Pak, ORCID 0000-0002-8685-9355, a.pak@kbtu.kz
- Aibek Kuralbayev, ORCID 0009-0001-0811-5385, a.kuralbaev@kbtu.kz

Kazakh-British Technical University (KBTU), Almaty, Kazakhstan

## Description
AdiletCodex is a full-text, article-level, trilingual (Kazakh + Russian + English) corpus of
the currently in-force codes and substantive laws of the Republic of Kazakhstan, parsed from
the official legal database adilet.zan.kz. Each article carries the full text plus structural
hierarchy (part / section / chapter / article), enumerated points, amendment notes,
cross-reference links, and rich document-level metadata (act form, legal sphere, adopting
body, registration numbers, adoption/publication dates, status). To our knowledge it is the
first article-structured, trilingual full-text corpus of Kazakh legislation.

## Why this corpus
Kazakh legal NLP has lacked a structured, full-text foundation: existing resources are either
document-level metadata, Russian-only, or downstream QA sets built on top of statutes they do
not themselves release. AdiletCodex fills that gap with the article as the unit of record, the
three official language versions side by side, and the structural + amendment + metadata
context needed for legal information retrieval, cross-lingual and RAG grounding,
translation-fidelity study, and temporal ("law-as-of-date") modeling.

## Related datasets and how AdiletCodex differs
- **KazakhLawCorpus** (Tleubayeva, Data / MDPI 2026; 215,889 records) - document-level metadata
  only, Kazakh only, no article text. AdiletCodex is complementary and strictly more granular:
  full text, article-level, trilingual.
- **justicedao/ipfs_kazakhstan_laws_ir** (HF, ~399k rows) - article-level but Russian only,
  undocumented, no hierarchy / amendments / status / KK / EN. AdiletCodex adds the two other
  official languages, the structural hierarchy, amendment notes, status, metadata, and docs.
- **olzhasAl/adilet-legal-qa-kz** (HF, 13,159 QA pairs, RU+KK) and other Kazakh legal-QA / LoRA
  sets - downstream tasks, not a source corpus. AdiletCodex provides the underlying statute text
  those tasks are grounded in.
- **Uzbek legal corpus** (Tomaris AI) - a methodological twin for a neighbouring jurisdiction
  (Uzbek-Latin only, no descriptor paper); AdiletCodex is the Kazakh, trilingual counterpart.
- **RusLawOD** (HF irlspbru/RusLawOD, 304k texts) - Russian national statutory corpus; a
  language / scope comparator, not Kazakh.
See `docs/RELATED_WORK.md` for the full positioning and comparators.

## Contents / size
- 65,825 article records (one JSON object / one CSV row per article per language)
- 343 documents: 24 codes + 319 laws (incl. the Constitution); 296 documents present in all
  three languages
- Languages: Russian 22,117 + Kazakh 22,099 + English 21,609 article records
- Document adoption years: 1991-2026
- Article length (characters): median 1,062, mean 1,893, max 236,715

Files:
- `adiletcodex.jsonl` (`.gz`) - one article per line (primary format, keeps nested
  paragraphs/notes/links)
- `adiletcodex.csv` (`.gz`) - same records, flat columns
- `docs/CODEBOOK.md` - field definitions
- `docs/RELATED_WORK.md` - positioning vs prior datasets

## Record schema (key fields)
`doc_id, doc_type (code|law), slug, lang (rus|kaz|eng), title, status, act_form, act_form_ru,
legal_sphere, legal_sphere_ru, adopting_organ, adopting_organ_ru, database_section,
database_section_ru, state_registry_number, npa_registration_number, adoption_date, change_date,
publication_date, publication_reference, publication_reference_ru, adoption_place, region_action,
citation, doc_date, doc_number, part, section, chapter, article_id, article_no, article_title,
article_text, paragraphs, notes, links, url`

(37 fields. `slug` is a short code mnemonic (null for laws); `citation` is the human-readable
source citation, with `doc_date` / `doc_number` parsed from it. `paragraphs`, `notes` and
`links` are nested and kept in the JSONL only; the CSV carries the 34 scalar fields.)

`article_text` is the full article body; `paragraphs` holds the numbered points with their
own inline links; `notes` holds amendment/editorial footnotes.

### Language of the metadata fields (important)
Only `title`, `status`, `article_title` and `article_text` are genuinely per-language and are
the **official** adilet.zan.kz translations. The document-"passport" fields come from adilet's
document card, which adilet publishes in **Russian only**. In v1.1 several of them have been
**localized** to the row's `lang`; each keeps a companion `*_ru` column with the original
Russian value for provenance.

- **Official per-language text:** `title`, `status`, `article_title`, `article_text`.
- **Localized by a curated term map** (official body names / fixed topic sections, reviewed by
  hand - not machine translation): `act_form`, `adopting_organ`, `database_section`.
- **Localized by machine translation (local Qwen3.5-122B, thinking disabled), i.e. reference
  metadata only:** `legal_sphere` and `publication_reference`. These are provided for
  convenience (filtering / search) and are **not** authoritative; the original Russian is kept
  in the `*_ru` companion column. The Kazakh output uses correct Kazakh legal terminology (the
  earlier Qwen2.5-32B Kazakh was replaced). For `publication_reference` a number-preservation
  check guards all digits, dates and article/issue numbers; where a translation would alter
  them, the Russian original is kept (logged in `localization/pubref_qa_failures_122b.json`).
- **Still Russian-by-source (not translated):** `region_action`, `adoption_place`.

Every localized field `X` has an `X_ru` companion (`act_form_ru`, `legal_sphere_ru`,
`publication_reference_ru`, `adopting_organ_ru`, `database_section_ru`) carrying the original
Russian. Russian (`rus`) rows keep the Russian value in `X` itself. Use `status` (not act
form) for validity/in-force state. The former `legal_force` field was **removed in v1.1** (it
duplicated `act_form` in 323/343 documents and was mislabeled - it was never a validity
indicator). Reproducibility artifacts (term maps, translation maps, QA-failure log, build
scripts) live under `localization/`. See `CHANGELOG.md`.

## How it was built
Current codes were enumerated from the adilet codes catalogue; substantive in-force laws were
enumerated from the adilet law-type search (amendment and ratification acts, and repealed
acts, excluded). Each document was retrieved in Russian, Kazakh and English and segmented into
a consistent article-level schema; document metadata was taken from the official requisites
("info") page. A given act carries the same document id across the three languages, so the
languages are aligned by (document, article number). Where the English version of a code
merges parts that Russian/Kazakh keep as separate documents (Civil Code), the duplicate
records were removed.

## Data validation
- 0 cross-language identical article texts (Kazakh, Russian and English are genuinely distinct)
- Kazakh records carry Kazakh-specific letters (script integrity checked)
- Article-count alignment across languages (median difference 0 per document)
- Empty / repealed-article stubs removed; `article_no` is unique within almost every
  (document, language) group (19 residual same-number groups remain and are documented under
  "Known limitations" in `docs/CODEBOOK.md`; disambiguate with `article_id`)
- Metadata coverage ~100% of documents
See `notebooks/kz_codes_qc.ipynb`.

## License
- **Dataset compilation** (structure, parsing, article segmentation, alignment, metadata):
  Creative Commons Attribution 4.0 International (CC-BY-4.0) - see `LICENSE`.
- **Underlying legal texts**: official normative legal acts of the Republic of Kazakhstan,
  which are public. Source attribution: adilet.zan.kz.

## How to cite
Mukhsimbayev, B., Pak, A., & Kuralbayev, A. (2026). *AdiletCodex: A Trilingual (Kazakh-Russian-English)
Article-Level Corpus of the Codes and Laws of Kazakhstan* (Version 1.1) [Data set]. Zenodo.
https://doi.org/10.5281/zenodo.22812625

Concept DOI (always resolves to the latest version): 10.5281/zenodo.22812625
Version 1.0 DOI: 10.5281/zenodo.22812626 (v1.1 version DOI is assigned on upload; not yet published)
Record: https://zenodo.org/records/22812626
Also on HuggingFace: https://huggingface.co/datasets/bobur-m/adiletcodex

## Quick start
```python
import json
recs = [json.loads(l) for l in open("adiletcodex.jsonl", encoding="utf-8")]
# all articles of the Criminal Code in Kazakh:
crim_kk = [r for r in recs if r["doc_id"]=="K1400000226" and r["lang"]=="kaz"]
```
