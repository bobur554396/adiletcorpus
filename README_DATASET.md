# AdiletCodex: A Trilingual (Kazakh-Russian-English) Article-Level Corpus of the Codes and Laws of Kazakhstan

**Version 1.0** - Source: adilet.zan.kz (Information and Legal System of Normative Legal Acts of the Republic of Kazakhstan, "Adilet")

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
`doc_id, doc_type (code|law), lang (rus|kaz|eng), title, status, act_form, legal_sphere,
legal_force, adopting_organ, database_section, state_registry_number, npa_registration_number,
adoption_date, change_date, publication_date, adoption_place, region_action,
part, section, chapter, article_id, article_no, article_title, article_text, paragraphs,
notes, links, url`

`article_text` is the full article body; `paragraphs` holds the numbered points with their
own inline links; `notes` holds amendment/editorial footnotes.

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
- Empty / repealed-article stubs removed; duplicate article numbers collapsed
- Metadata coverage ~100% of documents
See `notebooks/kz_codes_qc.ipynb`.

## License
- **Dataset compilation** (structure, parsing, article segmentation, alignment, metadata):
  Creative Commons Attribution 4.0 International (CC-BY-4.0) - see `LICENSE`.
- **Underlying legal texts**: official normative legal acts of the Republic of Kazakhstan,
  which are public. Source attribution: adilet.zan.kz.

## How to cite
Mukhsimbayev, B., Pak, A., & Kuralbayev, A. (2026). *AdiletCodex: A Trilingual (Kazakh-Russian-English)
Article-Level Corpus of the Codes and Laws of Kazakhstan* (Version 1.0) [Data set]. Zenodo.
https://doi.org/XX.XXXX/zenodo.XXXXXXX  *(DOI assigned on deposit)*

## Quick start
```python
import json
recs = [json.loads(l) for l in open("adiletcodex.jsonl", encoding="utf-8")]
# all articles of the Criminal Code in Kazakh:
crim_kk = [r for r in recs if r["doc_id"]=="K1400000226" and r["lang"]=="kaz"]
```
