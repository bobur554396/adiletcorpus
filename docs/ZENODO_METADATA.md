# Zenodo deposit - metadata to paste into the upload form

**Upload type:** Dataset

**Title:**
AdiletCodex: A Trilingual (Kazakh-Russian-English) Article-Level Corpus of the Codes and Laws of Kazakhstan

**Authors / Creators** (Name; Affiliation; ORCID):
1. Mukhsimbayev, Bobur; Kazakh-British Technical University; 0009-0008-4606-3628
2. Pak, Alexandr; Kazakh-British Technical University; 0000-0002-8685-9355
3. Kuralbayev, Aibek; Kazakh-British Technical University; 0009-0001-0811-5385

**Description:**
AdiletCodex is a full-text, article-level, trilingual (Kazakh + Russian + English) corpus of
the currently in-force codes and substantive laws of the Republic of Kazakhstan, parsed from
the official legal database adilet.zan.kz. It contains 65,825 article records across 343
documents (24 codes + 319 laws, including the Constitution); 296 documents are present in all
three languages (Russian 22,117 + Kazakh 22,099 + English 21,609 article records). Each record
carries the full article text, structural hierarchy (part/section/chapter/article), enumerated
points, amendment notes, cross-reference links, and rich document metadata (act form, legal
sphere, adopting body, registration numbers, adoption/publication dates, status). To our
knowledge it is the first article-structured, trilingual full-text corpus of Kazakh
legislation. The dataset passed automated quality control (no cross-language duplicate texts,
script integrity, article-count alignment). It supports legal information retrieval,
cross-lingual legal NLP, statute grounding, legal-translation study, and computational legal
research.

**Keywords:**
Kazakh legislation; legal corpus; low-resource NLP; legal NLP; legal information retrieval;
codes; laws; trilingual corpus; Kazakh; Russian; English; adilet.zan.kz; article-level;
statute grounding; Kazakhstan

**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)
(note: underlying legal texts are official public acts of the Republic of Kazakhstan; source
adilet.zan.kz)

**Version:** 1.1

**Language:** Kazakh (kaz), Russian (rus), English (eng)

**v1.1 changes (2026-10-08):** five document-card fields are now localized to each row's
language, each with a companion `*_ru` column preserving the Russian source value:
`act_form`, `adopting_organ` and `database_section` via a hand-curated, reviewed term map;
`legal_sphere` and `publication_reference` via local machine translation (Qwen3.5-122B,
thinking disabled) provided as reference metadata only, with a digit/date/number-preservation
check that keeps the Russian original on a mismatch. Only `region_action` and `adoption_place`
remain Russian-by-source. The redundant/mislabeled `legal_force` field was removed (it
duplicated `act_form`; validity lives in `status`). No records were added or removed
(still 65,825 across 343 documents) and the article texts, titles and status are unchanged.
When uploading v1.1, add it as a **new version** of the existing concept DOI
10.5281/zenodo.22812625 (a new version DOI will be minted automatically). See `../CHANGELOG.md`.

**Files to upload:**
- adiletcodex.jsonl.gz
- adiletcodex.csv.gz
- README_DATASET.md
- LICENSE
- CODEBOOK.md   (docs/CODEBOOK.md)

**Related/Alternate identifiers (optional):** link the data-descriptor paper's DOI here once
the descriptor (Data / Data in Brief) is published.
