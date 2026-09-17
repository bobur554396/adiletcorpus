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

## Document metadata (from the adilet requisites page; same across languages)
| Field | Type | Description |
|---|---|---|
| `status` | string | e.g. `upd` (updated / in force) |
| `act_form` | string | form of act, e.g. `Кодекс`, `Закон`, `Конституция` |
| `legal_force` | string | juridical force category |
| `legal_sphere` | string | subject area / legal-relations sphere |
| `database_section` | string | adilet database section (thematic classifier) |
| `adopting_organ` | string\|null | body that adopted the act |
| `state_registry_number` | string | number in the State Register of NLAs |
| `npa_registration_number` | string | act's own number, e.g. `226-v` |
| `adoption_date` | string | dd.mm.yyyy |
| `change_date` | string\|null | date of last amendment (null if never amended) |
| `publication_date` | string\|null | official publication date |
| `publication_reference` | string | official publication source(s) |
| `adoption_place` | string | e.g. `г. Астана` |
| `region_action` | string | territorial scope |
| `doc_date`, `doc_number` | string\|null | adoption date / number parsed from the citation |

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
- English exists for most but not all documents (adilet does not translate everything).
