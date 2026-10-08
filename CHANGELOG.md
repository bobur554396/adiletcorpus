# Changelog

All notable changes to the AdiletCodex dataset are recorded here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [1.1] - 2026-10-08

Schema-clarity release. No records were added or removed (still 65,825 article records across
343 documents); only the document-"passport" fields were corrected. The underlying article
texts are unchanged.

### Changed
- **`act_form` is now localized to each row's language.** Previously every language version
  carried the Russian act-form string (from adilet's Russian-only document card). Russian rows
  keep the Russian value; English and Kazakh rows now carry the localized term, mapped by
  contains-logic so compound/noisy source values resolve correctly:
  - contains "Конституционный"/"Конституциялық" -> EN `Constitutional Law`, KK `Конституциялық заң`
  - else contains "Кодекс" -> EN `Code`, KK `Кодекс`
  - else contains "Конституция" -> EN `Constitution`, KK `Конституция`
  - else (contains "Закон") -> EN `Law`, KK `Заң`

### Added
- **`act_form_ru`** - a new field on every record carrying the original Russian `act_form`
  value from the adilet card, so the source value is preserved alongside the localized one.
  In the JSONL it appears immediately after `act_form`; in the CSV it is the column after
  `act_form`.

### Removed
- **`legal_force`** - dropped from both the JSONL and the CSV. It duplicated `act_form`
  (identical in 323/343 documents) and was mislabeled: it is not a validity/in-force indicator.
  Use `status` for validity and `act_form` for the type of act.

### Documentation
- Documented that the remaining document-card fields - `legal_sphere`, `publication_reference`,
  `adopting_organ`, `region_action`, `database_section`, `adoption_place` - are
  **Russian-by-source** (adilet publishes the document card in Russian only) and are not
  translated across language versions.
- Updated `README_DATASET.md`, `docs/HF_DATASET_CARD.md`, `docs/CODEBOOK.md`,
  `docs/ZENODO_METADATA.md`; bumped version strings to 1.1.

### Files
- `data/adiletcodex.jsonl` (+ `.gz`) and `data/adiletcodex.csv` (+ `.gz`) regenerated.
- v1.0 originals preserved under `data/v1.0_backup/`.

### Added - extended metadata localization (2026-10-08)
Four more document-"passport" fields are now localized to each row's language, building on
the `act_form` work above. No records added or removed (still 65,825 across 343 documents);
the article texts, titles and status are untouched. English (`eng`) rows carry the English
value, Kazakh (`kaz`) rows the Kazakh value, Russian (`rus`) rows keep the Russian source.
A `<field>_ru` provenance column holding the original Russian value is added for **every** row.

- **`adopting_organ`** and **`database_section`** - localized with a small **curated,
  reviewed deterministic term map** (3 and 35 distinct source values respectively; these are
  official body names and the fixed adilet topic sections). Not machine-translated.
  New provenance columns: `adopting_organ_ru`, `database_section_ru`.
- **`legal_sphere`** (254 distinct values) and **`publication_reference`** (333 distinct
  non-empty values) - **machine-translated with Qwen 2.5 32B** (local vLLM) as convenience /
  **reference metadata**. Only the unique values were translated (then mapped back to rows).
  Prompts preserved all digits/dates/article numbers; proper nouns and Latin tokens were kept.
  New provenance columns: `legal_sphere_ru`, `publication_reference_ru`.
  - **Number-preservation QA on `publication_reference`:** the ordered sequence of digit-groups
    in source and translation must match; otherwise the Russian original is kept for that
    language. `legal_sphere`: 254/254 passed. `publication_reference`: 299/333 passed the joint
    check (29 English, 18 Kazakh per-language values fell back to Russian, logged in
    `localization/publication_reference_qa_failures.json`).
- **Reproducibility artifacts** under `localization/`: `adopting_organ_map.json`,
  `database_section_map.json` (curated), `legal_sphere_map.jsonl`,
  `publication_reference_map.jsonl` (each line `{ru, en, kk, numbers_ok}`), plus the build
  scripts (`build_group_a.py`, `translate_group_b.py`, `apply_localization.py`).
- **Disclosure:** `legal_sphere` and `publication_reference` are machine translation and are
  for reference/filtering only (this 32B Kazakh output was superseded by the Qwen3.5-122B
  re-translation below, which fixed the Kazakh terminology). The **substantive**
  content (article text, titles, status) remains the **official** adilet.zan.kz translation,
  **not** machine translation. Original Russian is preserved in the `*_ru` columns.
- **CSV:** `publication_reference` (previously omitted) and all four `*_ru` columns were added
  to the flat CSV; the CSV now has 33 columns.
- v1.1 pre-localization files preserved under `data/v1.1_pre_qwen_backup/`.

### Changed - reference-metadata MT upgraded to Qwen3.5-122B (2026-10-08)
`legal_sphere` and `publication_reference` are now machine-translated with **Qwen3.5-122B**
(local, thinking disabled), replacing the earlier Qwen2.5-32B translations. The 122B model
produces correct Kazakh legal terminology (e.g. "Уголовное право" -> KK "Қылмыстық құқық", EN
"Criminal Law"); the weaker 32B Kazakh was replaced. No records were added or removed
(still 65,825 across 343 documents); article text, titles and status are untouched, and the
`legal_sphere_ru` / `publication_reference_ru` provenance columns still hold the Russian
originals. English (`eng`) rows carry the new EN, Kazakh (`kaz`) rows the new KK, Russian
(`rus`) rows keep the Russian source.

- Only the unique values were re-translated (254 `legal_sphere`, 333 `publication_reference`),
  then mapped back to rows. Each map line now records `model = "qwen3.5-122b"`.
- **Quality controls:** Kazakh output is validated as Cyrillic with no invented Latin-script
  words (Roman numerals / `N` / `c` that are part of a citation and present in the Russian
  source are allowed) and no CJK; English output is guaranteed free of Cyrillic. Verified on
  the data: `eng` rows are 0% Cyrillic and `kaz` rows are 0 Latin-leak / 0 CJK in both fields.
- **Number-preservation QA on `publication_reference`** (ordered digit-groups of source vs
  translation): `legal_sphere` has no digits; `publication_reference` passed the joint EN+KK
  check for 312/333 unique values, with 78 per-language mismatches logged in
  `localization/pubref_qa_failures_122b.json`. These mismatches are benign date-formatting /
  date-ordering differences (Kazakh year-first dates, `dd.mm.yyyy` normalization) rather than
  loss of any reference number; on a mismatch the Russian original is kept for Kazakh, and for
  English a clean number-matching 32B value or the non-Cyrillic 122B text is kept (never
  Cyrillic).
- **Disclosure (unchanged intent):** `legal_sphere` and `publication_reference` remain machine
  translation for reference / filtering only; the substantive content (article text, titles,
  status) is the **official** adilet.zan.kz translation, not machine translation. Original
  Russian is preserved in the `*_ru` columns.
- **Reproducibility / backups:** new maps `localization/legal_sphere_map.jsonl` and
  `localization/publication_reference_map.jsonl` (each line `{ru, en, kk, numbers_ok, model}`);
  scripts `localization/translate_122b.py` and `localization/reapply_122b.py`; the 32B maps are
  preserved under `localization/32b_backup/` and the pre-122B data under `data/pre_122b_backup/`.

## [1.0] - 2026-09-17

Initial public release. 65,825 article records across 343 documents (24 codes + 319 laws,
incl. the Constitution), trilingual (KK/RU/EN), article-level, full text with structural
hierarchy, amendment notes, cross-reference links and document metadata. Published to Zenodo
(10.5281/zenodo.22812626) and HuggingFace (bobur-m/adiletcodex).
