# Related work & positioning (for the AdiletCodex descriptor)

Scouted 2026-09-16. Verdict: **no published trilingual (KK/RU/EN), article-level, full-text,
structurally-modeled corpus of Kazakh legislation exists.** Our niche is open. Cite the items
below to position the contribution and pre-empt reviewers.

## Direct / overlapping (Kazakhstan)
- **KazakhLawCorpus** - Tleubayeva. *Data* (MDPI) 11(9):217, **28 Aug 2026**.
  215,889 **document-level METADATA** records (no article text), Kazakh only, 1947-2026.
  Zenodo 10.5281/zenodo.21787361; HF Arailym-tleubayeva/KazakhLawCorpus-clean.
  -> We are complementary and strictly more granular (full text, article-level, trilingual).
  Proves the target venue (*Data*, MDPI).
- **justicedao/ipfs_kazakhstan_laws_ir** (HF) - ~399k rows, **article-level but RUSSIAN ONLY**,
  IR-oriented Parquet, **no descriptor paper, undocumented, no hierarchy/amendments/status,
  no KK/EN**. The only resource partially occupying "article-level Kazakhstan legislation".
  MUST cite and contrast (a reviewer may know it); our trilingual+structured+documented niche
  remains open.

## Central Asian precedent
- **Uzbek legal corpus** (Tomaris AI) - github.com/javohirmat/uzbek-legal-corpus;
  HF sukhrobnurali/uzbek-legal-corpus. Article-level, structural hierarchy, Uzbek-Latin only;
  25 docs/7,368 arts (small) + a 24,267-act/54,173-row variant. **No descriptor paper (repo
  only).** Methodological twin, citable precedent, and a KZ+UZ cross-jurisdiction follow-up hook.

## Adjacent Kazakh legal-NLP (downstream tasks - none is a full-text article corpus)
- olzhasAl/adilet-legal-qa-kz (HF) - 13,159 QA pairs over 28 NPA, RU+KK.
- "Legal AI in Low-Resource Languages: ... Kazakh Legislation" - *Computers* (MDPI) 14(9):354
  (2025) - QA datasets + 7 LLMs.
- "Fine-Tuning Qwen3 ... Legal Domain of Kazakhstan" - *Applied Sciences* 16(13):6777, Jul 2026
  - 63,114 QA pairs (76% RU / 24% KK), LoRA on Qwen3.
- "Multilingual LLMs in the Legal Domain: ... Kazakh, Turkish and English" - IEEE conf 2026
  (Xplore 11207002) - evaluation study, not a dataset; KK/TR/EN (not KK/RU/EN).
-> All lack exactly our resource; our corpus is the missing structured foundation for them.

## Comparators to cite (positioning / schema precedent)
- **RusLawOD** - arXiv 2406.04855; HF irlspbru/RusLawOD. 304,382 texts/194M tokens, RU,
  1991-2025 (+CoNLL-U). National statutory-corpus + Russian-language comparator.
- **Bundesrecht** - arXiv 2605.31338. German federal law, full statutory hierarchy (down to
  Nummer/Buchstabe). Precedent for our part/section/chapter/article schema.
- **CLaw** - arXiv 2509.21208 (Sep 2026). 453 Chinese statutes, subparagraph + revision
  timesteps. Precedent for our amendment-note / temporal dimension.
- MultiLegalPile (arXiv 2306.02069, 24 langs, no Kazakh); KyrText (LoResLM 2026, Kyrgyz,
  incl. legal archives, general-domain); LOCUS/BLAD (other national legal corpora).

## Venues / deadlines
- **NLLP 2026** (co-located EMNLP 2026, Budapest, 28 Oct 2026) - submission deadline 11 Aug
  2026 PASSED -> target **NLLP 2027**.
- **Data (MDPI)** - proven (KazakhLawCorpus), rolling -> descriptor.
- **Data in Brief** (Elsevier) - rolling, fast, dataset-only.
- **Scientific Data** (Nature) - higher bar, prestige option.
- **LREV** journal / **LREC-COLING** - multilingual language-resource paper.

## Downstream paper ideas the corpus uniquely enables
1. Cross-lingual statutory alignment & translation-fidelity benchmark (KK<->RU<->EN) - aligned
   trilingual legal parallel resource; measure MT quality + legal-content divergence across the
   official versions. Niche empty.
2. Article-level trilingual statutory retrieval / legal-RAG benchmark (cf. French BSARD, but
   trilingual, with the cross-reference graph as gold links). Feeds the KZ QA/LoRA line + EUSPN.
3. Temporal / amendment-aware legal modeling ("law-as-of-date", detecting citations to repealed
   provisions) - enabled by our article-level amendment notes + status + dates. Cf. CLaw,
   Bundesrecht. Nobody has this for Kazakh.
4. (Follow-up) Cross-jurisdiction KZ+UZ(+RU) Central Asian article-level corpus.
