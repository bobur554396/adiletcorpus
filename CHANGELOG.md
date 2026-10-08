# Changelog

All notable changes to the AdiletCodex dataset are recorded here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [2.0] - 2026-10-08

Major release. This version makes **breaking schema changes** - a field was removed
(`legal_force`) and localized document-passport fields plus their `*_ru` provenance companions
were added - and also applies a **data fix** that consolidates 18 split/duplicate article
records. Because the schema is not backward-compatible with v1.0 and the record count changes,
the release is numbered 2.0 (the draft 1.1 schema-clarity notes are folded into this entry).

Record count is now **65,807** article records across 343 documents (Russian 22,112, Kazakh
22,098, English 21,597), down from 65,825 in v1.0: 18 records that were parser artifacts
(entry-into-force / amendment fragments split off from their parent article, a quoted old-code
article, truncated compound article numbers, and stale same-language duplicates) were repaired
without dropping any wording. The underlying official article texts, titles and status are
otherwise unchanged. Three-way (KK/RU/EN) article-number alignment is 21,445 (up from 21,440).

### Fixed - duplicate and fragment article records (2026-10-08)
The v1.1 pre-release integrity audit found 19 `(doc_id, lang, article_no)` collision groups.
All were resolved with `localization/fix_duplicate_articles.py` (reproducible; the pre-fix
snapshot is kept under `data/v1.1_predupfix_backup/`), preserving every article's wording:
- **Truncated compound article numbers (2 groups, 5 records renumbered).** English rows whose
  number had been truncated to the base were restored to the full inserted number recovered
  from the article title and confirmed against the already-correct Kazakh/Russian rows:
  `Z020000344_` Article 18 -> `18-1`; `Z030000474_` Article 15 -> `15-24`, `15-25`, `15-26`,
  `15-27`. This brought 5 more article numbers into three-way alignment.
- **Split-off entry-into-force / amendment / old-redaction fragments (13 records merged).**
  Clauses the parser had broken out of their parent article (chiefly from "Final and
  transitional provisions" / enactment articles, and РЦПИ amendment-addition blocks) were
  merged back into the correct parent article and the empty fragment removed. Affected parents
  include `K1700000125` Article 277 (5 fragments), `K1400000226` (kaz) Article 467 (the quoted
  old-code Article 51 text), `Z1100000413` (rus) Articles 1/7/10/164, `Z090000191_` Article 10,
  `Z1200000541` Article 24, `Z1400000176` Article 26, and `Z1500000405` Article 40.
- **Stale same-language duplicates (3 records merged).** A second in-force record for the same
  article in one language (`K1400000235` eng Art. 187 wrong-chapter copy, `K1500000414` eng
  Art. 143 future-effective redaction block, `Z1100000380` eng Art. 52 stale translation) was
  merged into the canonical record and removed, retaining all wording.
- **Net effect:** 18 records removed (12 English, 5 Russian, 1 Kazakh), 5 renumbered, 13 parent
  articles extended. After the fix there are **0** duplicate `(doc_id, lang, article_no)` keys.

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
  `docs/ZENODO_METADATA.md`; bumped version strings to 2.0.

### Files
- `data/adiletcodex.jsonl` (+ `.gz`) and `data/adiletcodex.csv` (+ `.gz`) regenerated.
- v1.0 originals preserved under `data/v1.0_backup/`.

### Added - extended metadata localization (2026-10-08)
Four more document-"passport" fields are now localized to each row's language, building on
the `act_form` work above. No records added or removed at this metadata stage (65,825 across
343 documents; the duplicate/fragment fix above brings the final count to 65,807);
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
  for reference/filtering only (this 32B Kazakh output was superseded by the Qwen3.5-122B-A10B
  re-translation below, which fixed the Kazakh terminology). The **substantive**
  content (article text, titles, status) remains the **official** adilet.zan.kz translation,
  **not** machine translation. Original Russian is preserved in the `*_ru` columns.
- **CSV:** `publication_reference` (previously omitted) and all four `*_ru` columns were added
  to the flat CSV (the `citation` scalar was added in the pre-release consolidation below,
  bringing the flat CSV to its final **34 columns** = all scalar fields; the three nested
  fields `paragraphs` / `notes` / `links` remain JSONL-only).
- v1.1 pre-localization files preserved under `data/v1.1_pre_qwen_backup/`.

### Changed - reference-metadata MT upgraded to Qwen3.5-122B-A10B (2026-10-08)
`legal_sphere` and `publication_reference` are now machine-translated with **Qwen3.5-122B-A10B**
(local, Q4_K_M GGUF served via llama.cpp, thinking disabled), replacing the earlier
Qwen2.5-32B translations. The 122B model
produces correct Kazakh legal terminology (e.g. "Уголовное право" -> KK "Қылмыстық құқық", EN
"Criminal Law"); the weaker 32B Kazakh was replaced. No records were added or removed
(65,825 across 343 documents at this metadata stage; final count 65,807 after the
duplicate/fragment fix above); article text, titles and status are untouched, and the
`legal_sphere_ru` / `publication_reference_ru` provenance columns still hold the Russian
originals. English (`eng`) rows carry the new EN, Kazakh (`kaz`) rows the new KK, Russian
(`rus`) rows keep the Russian source.

- Only the unique values were re-translated (254 `legal_sphere`, 333 `publication_reference`),
  then mapped back to rows. Each map line now records `model = "Qwen3.5-122B-A10B"`.
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

### Pre-release consolidation (2026-10-08)
Final tidy-up before the single v2.0 upload. No article records, titles or status changed at
this stage (65,825 records / 37 JSONL fields across 343 documents; final count 65,807 after the
duplicate/fragment fix above).
- **`citation` added to the flat CSV** so the CSV carries all 34 scalar fields and is at full
  parity with the JSONL (only the nested `paragraphs` / `notes` / `links` stay JSONL-only).
  `adiletcodex.csv` and `adiletcodex.csv.gz` regenerated from the current JSONL; row counts and
  gzip line counts verified against the JSONL.
- **Documentation completed and reconciled.** All 37 fields (adding `slug`, `citation`,
  `doc_date`, `doc_number`) are now listed in `README_DATASET.md`, `docs/CODEBOOK.md` and
  `docs/HF_DATASET_CARD.md`. The concept DOI (10.5281/zenodo.22812625) is used as the primary
  citation link across the docs. A "Known limitations" note (residual same-number articles;
  nullable `adopting_organ` / `publication_reference`) was added to the codebook, and the
  over-strong "duplicate article numbers collapsed" wording in `README_DATASET.md` was corrected.
- **Reproducibility artifacts tracked.** The `localization/` term maps, translation maps,
  QA-failure logs and build scripts are now committed to the repository.
- Added `CITATION.cff`.

## [1.0] - 2026-09-17

Initial public release. 65,825 article records across 343 documents (24 codes + 319 laws,
incl. the Constitution), trilingual (KK/RU/EN), article-level, full text with structural
hierarchy, amendment notes, cross-reference links and document metadata. Published to Zenodo
(10.5281/zenodo.22812626) and HuggingFace (bobur-m/adiletcodex).
