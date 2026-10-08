# AdiletCodex - Codebook

One record = one article of one document in one language. Files: `adiletcodex.jsonl`
(nested fields kept) and `adiletcodex.csv` (flat; nested fields omitted).

## Identity & language
| Field | Type | Description |
|---|---|---|
| `doc_id` | string | adilet NGR of the document (same id across languages), e.g. `K1400000226` |
| `doc_type` | string | `code` or `law` |
| `slug` | string\|null | short mnemonic for codes (e.g. `criminal`), null for laws |
| `lang` | string | `rus` (Russian), `kaz` (Kazakh), `eng` (English) |
| `title` | string | document title in this language |
| `url` | string | canonical adilet URL |

## Document metadata (from the adilet requisites page)
The adilet document "passport" is published in **Russian only**. In v1.1 several passport fields
are **localized** to the row's `lang`; each keeps an `*_ru` companion with the original Russian
value for provenance. Russian (`rus`) rows keep the Russian value in the field itself. Two
localization methods are used, and they are **not** equivalent in authority:

- **curated term map** - hand-reviewed official translations (`act_form`, `adopting_organ`,
  `database_section`);
- **reference metadata (machine-translated)** - translated by local Qwen3.5-122B (thinking
  disabled) for convenience (filtering / search), **not** authoritative, with the original
  Russian kept in the `*_ru` companion (`legal_sphere`, `publication_reference`); the Kazakh
  output uses correct Kazakh legal terminology. The substantive text (`article_text`, `title`,
  etc.) is the official adilet translation, not machine translation.

Fields still marked **Russian-by-source** are not translated at all.

| Field | Type | Language | Description |
|---|---|---|---|
| `status` | string | per-language | e.g. `upd` (updated / in force). Use this for validity / in-force state. |
| `act_form` | string | **localized (curated)** | form of act, localized to `lang`: EN `Code`/`Law`/`Constitution`/`Constitutional Law`; KK `Кодекс`/`Заң`/`Конституция`/`Конституциялық заң`; RU `Кодекс`/`Закон`/`Конституция`/`Конституционный закон` (RU may include amendment-noise values). |
| `act_form_ru` | string | Russian source | original Russian `act_form` from the adilet card, kept on every row for provenance (v1.1). |
| `legal_sphere` | string | **reference metadata (machine-translated)** | subject area / legal-relations sphere; local Qwen3.5-122B MT (254 unique values), convenience only. |
| `legal_sphere_ru` | string | Russian source | original Russian `legal_sphere`, kept on every row for provenance (v1.1). |
| `database_section` | string | **localized (curated)** | adilet database section (thematic classifier), 35 fixed sections; curated EN/KK map. |
| `database_section_ru` | string | Russian source | original Russian `database_section`, kept on every row for provenance (v1.1). |
| `adopting_organ` | string\|null | **localized (curated)** | body that adopted the act (Parliament / President, with former-name notes); curated EN/KK map. |
| `adopting_organ_ru` | string\|null | Russian source | original Russian `adopting_organ`, kept on every row for provenance (v1.1). |
| `state_registry_number` | string | - | number in the State Register of NLAs |
| `npa_registration_number` | string | - | act's own number, e.g. `226-v` |
| `adoption_date` | string | - | dd.mm.yyyy |
| `change_date` | string\|null | - | date of last amendment (null if never amended) |
| `publication_date` | string\|null | - | official publication date |
| `publication_reference` | string | **reference metadata (machine-translated)** | official publication source(s); local Qwen3.5-122B MT (333 unique values) with a digit/date/number-preservation check (Russian kept on mismatch), convenience only. |
| `publication_reference_ru` | string | Russian source | original Russian `publication_reference`, kept on every row for provenance (v1.1). |
| `adoption_place` | string | **Russian-by-source** | e.g. `г. Астана` |
| `region_action` | string | **Russian-by-source** | territorial scope |
| `citation` | string | per-language | human-readable source citation of the act (e.g. `Code of the Republic of Kazakhstan dated 20 June, 2003 № 442`); `doc_date` / `doc_number` are parsed from it. |
| `doc_date`, `doc_number` | string\|null | - | adoption date (ISO `yyyy-mm-dd`) / number parsed from `citation` |

> **Removed in v1.1:** `legal_force`. It duplicated `act_form` in 323/343 documents and was
> mislabeled - it was never a validity indicator. Use `status` for validity and `act_form` for
> the type of act. See `../CHANGELOG.md`.

## Structural hierarchy & article
| Field | Type | Description |
|---|---|---|
| `part` | string\|null | top level (e.g. `ОБЩАЯ ЧАСТЬ` / `SPECIAL PART` / `Жалпы бөлік`) |
| `section` | string\|null | Раздел / N-бөлім / Section |
| `chapter` | string\|null | Глава / N-тарау / Chapter |
| `article_id` | string\|null | internal HTML anchor id |
| `article_no` | string\|null | article number (e.g. `99`, inserts like `50-1`) |
| `article_title` | string | full article heading |
| `article_text` | string | full article body (concatenated points) |
| `paragraphs` | list | numbered points: `{id, number, text, links}` (JSONL only) |
| `notes` | list | amendment/editorial footnotes: `{text, links}` (JSONL only) |
| `links` | list | article-level hyperlinks (JSONL only) |

## Notes
- Languages align by (`doc_id`, `article_no`). A document keeps the same `doc_id` across
  languages.
- Gaps in `article_no` within a document correspond to repealed articles.
- English exists for most but not all documents (adilet does not translate everything):
  296 of 343 documents are present in all three languages, 37 in Kazakh+Russian, 5 in Kazakh
  only, 3 in Russian only, 2 in Kazakh+English.
- `adopting_organ` / `adopting_organ_ru` are null for 288 records (documents whose adilet card
  lists no adopting body); `publication_reference` / `publication_reference_ru` are empty for
  127 records (documents with no publication source recorded).

## Known limitations
- **Residual same-number articles.** `article_no` is unique within most (`doc_id`, `lang`)
  groups, but 19 groups contain more than one record with the same `article_no`. These come
  from three causes and are retained as-is: (a) a displayed number that legitimately recurs
  across different structural parts of a code; (b) entry-into-force / amendment clauses inside
  "Final and transitional provisions" chapters that the parser emitted as separate records
  (their `article_title` is a clause fragment, e.g. `article 38;`); and (c) compound inserted
  numbers (e.g. `Article 15-24`) whose `article_no` was truncated to the base number (`15`).
  Disambiguate with `article_id` (unique HTML anchor), `article_title`, and the structural
  columns (`part` / `section` / `chapter`). This is inherited from v1.0 and is scheduled for a
  clean re-parse in a future major version.
- **Reference-metadata fields are machine translation.** `legal_sphere` and
  `publication_reference` (and only these) are translated by a local LLM for
  filtering/search convenience and are not authoritative; the original Russian is always kept in
  the `*_ru` companion column. The substantive article content (`title`, `status`,
  `article_title`, `article_text`) is the official adilet.zan.kz translation.
