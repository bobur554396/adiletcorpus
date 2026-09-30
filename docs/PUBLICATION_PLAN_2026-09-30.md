# AdiletCodex: publication plan (2026-09-30)

Scope: usage statistics, where to publish the data descriptor, article-paper ideas that do
not duplicate the authors' three existing works, and a combined plan with the UzCourtCorpus
papers (Paper A / Paper B). Supersedes the venue choice in `PUBLICATION_VENUES.md`
(IEEE Data Descriptions turned out NOT to be in Scopus, see section 2).

---

## 1. Usage statistics (read 2026-09-30, public APIs, no login)

| Source | Metric | Value |
|---|---|---|
| Zenodo record 22812626 (v1.0, published 2026-09-17) | views / unique views | 40 / 31 |
| | downloads / unique downloads | 17 / 17 |
| Hugging Face bobur-m/adiletcodex (created 2026-09-17) | downloads (rolling 30 days = all time here) | 61 |
| | likes | 0 |
| GitHub bobur554396/adiletcorpus | stars / forks / watchers | 0 / 0 / 0 |
| | clones, traffic | not available without the owner's token |

Caveats:
- No public history endpoint on Zenodo or HF, so the day-by-day curve since 17.09 cannot be
  reconstructed. The totals above cover 13 days.
- Some downloads are ours: on 2026-09-19 the two .gz files were pulled from Zenodo to verify
  md5 (about 2 of 17). HF counts file requests and includes crawlers and our own checks.
- Realistic reading: roughly 15 external Zenodo downloads and several dozen HF pulls in
  2 weeks with zero promotion. That is a real, modest signal of interest, enough to justify a
  descriptor, not enough to use as an argument in a paper.
- Suggestion: a daily cron that appends these four numbers to `docs/usage_log.csv`, so the
  descriptor can report a usage curve later. (Not set up; waiting for the author's go-ahead.)

---

## 2. Where to publish the data descriptor

### 2.1 What counts for the KZ PhD defence (from PHD_DEFENSE_REQUIREMENTS_KZ.md)
- Variant 1: 1 Scopus JOURNAL article with CiteScore percentile >= 25 plus Перечень articles.
  The author already has Herald of KBTU (Перечень Список 1, enough by itself) and Вестник КазАТК
  (Список 2). **So a single Scopus journal paper at >= 25 closes Variant 1.**
- Variant 2: 2 Scopus journal articles at >= 35 (or JCR Q1-Q3).
- Conference papers count only as a WoS-indexed conference paper in Variant 4.

### 2.2 Key risk found: Scopus document type "Data paper"
Scopus types data papers inconsistently (counted on scopus.com via KBTU IP):
Data in Brief 2024: 0 Article / 1311 Data paper; 2025: 180 / 912; 2026: 944 / 0.
Scientific Data 2025: 913 / 1076; 2026: 463 / 856. JOHD 2026: 96 / 27. Data (MDPI) 2026: 110 / 85.
Journals that never use the "Data paper" type (always "Article"): Language Resources and
Evaluation, AI and Law, IEEE Access. The Правила name "статья"; a "Data paper" tag is left to
the council's discretion. **Safest route = a venue where the descriptor is a regular article.**

### 2.3 Shortlist (facts checked on journal sites and scopus.com source pages, 2026-09-30)

| # | Venue | Paper type | Cost | Scopus best percentile (CiteScore 2025) | WoS | Speed | Defence effect |
|---|---|---|---|---|---|---|---|
| 1 | **Language Resources and Evaluation** (Springer, hybrid) | Full-length paper (18-25 pp) describing "a new and substantial major resource"; focus on less-resourced languages; resource must be public | **Free** via subscription route (Open Choice optional) | Language and Linguistics **95**; Library and Inf. Sci. 81 | SCIE, JIF 2.0 | median 36 days to first decision | Closes Variant 1 alone; counts toward Variant 2. Always typed Article. Needs a technical validation section, not a bare descriptor |
| 2 | **Data in Brief** (Elsevier, full OA) | Data article, journal template | APC **USD 1,600** (geo pricing at submission; KZ price not shown) | Multidisciplinary only, **76** | ESCI | 7 days first decision, ~84 days to acceptance | Passes >= 35, but "Multidisciplinary only" and Data paper typing risk |
| 3 | **Frontiers in Big Data** | Data Report (<= 3000 words, 2 fig/tables) | APC **CHF 990** | **74-78** | ESCI | not checked | Cheapest Scopus >= 35 data-report option; typing not checked |
| 4 | **Journal of Open Humanities Data** (Ubiquity) | Data Paper (1000-1500 words) | APC GBP 1,070; **waiver can be requested at submission only** | Arts and Humanities 76; Information Systems 27 | ESCI | not stated | >= 35 in humanities category; typing mixed; waiver makes it possibly free |
| 5 | **Artificial Intelligence and Law** (Springer, hybrid) | Research article; scope lists "datasets" but needs substantial empirical content | **Free** via subscription route | Law **99**; AI 89 | SCIE + SSCI, JIF 5.3 | median 6 days to first decision | Strongest, but is the planned home of the UZ Paper B line; better used for an article paper, not the descriptor |
| 6 | Scientific Data (Nature), for comparison | Data Descriptor | APC **USD 2,690** | Statistics 97; CS Applications 84 | SCIE | | Too expensive for an open-by-default resource; mixed typing |
| 7 | Data (MDPI), for comparison | Data Descriptor | APC **CHF 1,600** | Inf. Systems and Management 75 | ESCI | median 47 days | This is the "expensive MDPI" option, no advantage over #1 |
| 8 | IEEE Data Descriptions (previous plan) | Data descriptor | APC USD 2,160, temporary USD 600 promo; KBTU-IEEE deal coverage unverified | **NOT in Scopus** | not in MJL | | **Does not count for the defence now. Dropped.** |
| 9 | Research Data Journal for the Humanities and Social Sciences | Data paper <= 2500 words | Diamond OA, free | Scopus coverage **ends 2024** | not in MJL | | Free but new papers may not be indexed. Not recommended |
| 10 | Data Intelligence (now Science Press) | Data article | not verified | LIS 84; AI 68 | ESCI | | Possible backup; APC and rules could not be read |

Kazakhstan journals: Eurasian J. of Mathematical and Computer Applications (ENU) is Scopus
but only ~25th percentile (borderline); KazNU Bulletin (Math/Mech/CS) 37th in Mathematics
misc.; Herald of KBTU is in Scopus at the 1st percentile (useful only as Перечень). No
Kazakhstan law journal was found in Scopus. None of them is a good home for a descriptor.

Waivers: Kazakhstan is not in Research4Life A/B and not on the Springer Nature waiver list.
Subscription (non-OA) route at Springer is therefore the way to publish for free.

Conferences (visibility, not a closing line for the defence):
- ACL Rolling Review: October cycle **12 Oct 2026** (too soon); next cycle January 2027 (date TBA).
- ICAIL 2027 (Vienna, 5-9 July 2027): papers due **28 Jan 2027**; ACM OA proceedings.
- JURIX 2026 deadline passed; NLLP 2027, RANLP 2027 calls not yet out; LREC is 2028.

### 2.4 Recommendation for the descriptor
**Language Resources and Evaluation, full-length resource paper, subscription route (free).**
It is the only option that is at once free, Q1-level (95th percentile), always typed Article
and a direct fit ("new major resource for a less-resourced language"). The price is effort:
LRE expects more than a data sheet, so the paper needs a "technical validation" part:
alignment quality of the KK/RU/EN triples, the divergence statistics (section 3, idea A pilot),
a small baseline (cross-lingual retrieval with 2-3 embedders), and a comparison with
KazakhLawCorpus, kurumikz/kazakhstan_legal_corpus, ipfs_kazakhstan_laws, KazParC (legal part).
Fallbacks if LRE rejects: Frontiers in Big Data Data Report (CHF 990) or JOHD with a waiver
request; Data in Brief if speed matters and USD 1,600 is acceptable.

---

## 3. Article-paper ideas

### 3.1 What already exists (must not be duplicated, must be cited)
1. **Herald of KBTU 2025** (vol. 22 no. 4, pp. 227-243, DOI 10.55452/1998-6688-2025-22-4-227-243):
   "A computational pipeline for lexical and thematic analysis of the Code of Administrative
   Offenses of RK". One code, Russian, frequencies, keywords, topics, clustering, visualisation.
2. **Вестник КазАТК #3504** (accepted 28.08.2026): "A computational framework for comparative
   and historical analysis of the legal codes of RK". Five codes, Russian, 3062 articles; TF-IDF
   code classification (98.48%), penalty-type classification, E5+UMAP+HDBSCAN clustering,
   citation graph (6436 edges), penalty extraction incl. numbers in words (4524 records),
   563 historical versions 1996-2025, 8225 edits, 685 penalty transitions.
   Repo github.com/bobur554396/adilet-historical-analysis.
3. **EUSPN 2026** (Procedia CS, accepted, Oct 2026): KZ+UZ statute retrieval RAG over 9 codes,
   fine-tuned BGE-M3, synthetic vs real question gap (0.864 vs 0.422 acc@5), query rewriting,
   244+71 KZ and 120 UZ human questions. Retrieval is monolingual-per-country, Russian corpus side.

**Common gap of all three: everything is Russian-only (or UZ). Nothing uses the Kazakh and
English versions, nothing uses the laws beyond the codes, nothing measures cross-language
behaviour.** That is exactly what AdiletCodex adds (296 documents, 21440 article triples
KK/RU/EN aligned by document and article number).

Filtered out because they overlap: citation graph, edit dynamics / versions, code or sphere
classification, clustering, lexical/topic analysis, Russian penalty extraction, monolingual
statute RAG. Also dropped: generic Kazakh legal QA (saturated: MDPI Computers 14(9):354,
Applied Sciences 10.3390/app16136777, raiym76/kazlawbench, olzhasAl/adilet-legal-qa-kz).
Note: the name "KazLegalBench/KazLawBench" is taken on HF (raiym76/kazlawbench, May 2026).
Note: the `links` field in the release is empty for all records; any citation-based task
would need re-extraction from the HTML.

### 3.2 Ideas (novelty from the 2026-09-30 scan: arXiv, HF, web; Semantic Scholar was rate-limited)

**A. Do the three official versions say the same thing? A corpus-wide audit of KK/RU/EN
divergences in Kazakhstan legislation.** [TOP]
- Detectors: missing/extra paragraphs, numeric and date mismatches, cross-reference mismatches,
  sanction mismatches (reuses the КазАТК penalty parser, now across three languages),
  embedding-based semantic outliers (LaBSE / BGE-M3), stale English translations (version date).
  Precision on a lawyer-annotated sample (~300 flags), error taxonomy, breakdown by sphere and year.
- Pilot (raw heuristic, today): article triples where the multiset of numbers differs:
  KK vs RU **6.3%** (1341/21440), EN vs RU **10.4%** (2239). Upper bound (formatting noise
  included), but it shows the signal is there. Length ratios: 86 EN articles < half the RU
  length, 90 > double.
- Novelty: open. Only manual legal-linguistic studies exist (Karaganda Law Series on the Civil
  Code KK/RU; Int. J. Semiotics of Law 2024, 10.1007/s11196-024-10233-0) and EU doctrinal work.
  No computational audit for Kazakhstan, very little even for EU law.
- Why it matters: in RK the Kazakh and Russian texts are equally authentic; discrepancies are
  a real legal-certainty issue. Strong policy angle.
- Effort: 6-8 weeks; H100 for embeddings/LLM checks; needs 1 bilingual lawyer for annotation.
- Venue: **Artificial Intelligence and Law** (Law 99th) or LRE; conference version ICAIL 2027 (28 Jan).
- Builds on: КазАТК (penalty parser, versions), descriptor (data).

**B. Cross-lingual statute retrieval for Kazakh: 9-direction benchmark + human queries.**
- All KK/RU/EN -> KK/RU/EN directions over one article pool; gold comes free from alignment.
  Plus EUSPN human questions translated into Kazakh by a native speaker (real Kazakh queries).
  Measure the "Kazakh penalty" of BGE-M3, multilingual-E5, LaBSE, jina-v3, Qwen3-Embedding,
  Kazakh encoders; tokenizer fertility and context cost as a section.
- Novelty: open for the legal cross-lingual part (Taiwan CL statute retrieval 2410.11450,
  LEMUR 2602.09570 has no Kazakh; KazMTEB unverified model-card only).
- Builds directly on EUSPN (monolingual) and answers its own future-work line.
- Effort: 4-6 weeks, cheapest of all (data and code from EUSPN reused). H100 for embeddings.
- Venue: ARR January 2027 (ACL 2027) or ICAIL 2027; journal extension later. Submit as MTEB task.

**C. Legal MT for Kazakh: benchmarking LLMs and NMT on KK<->RU<->EN statutes.**
- Held-out test set (codes adopted/revised after LLM training cut-offs, deduplicated against
  KazParC legal part), metrics beyond BLEU: terminology accuracy, number/reference fidelity.
  Systems: NLLB, Tilmash, KazLLM, Sherkala, Qwen2.5-32B on our H100, GPT-class. Pivot via RU vs direct.
  Optional: fine-tune on the aligned corpus.
- Novelty: partially taken (KazParC has 77k legal sentences; kurumikz corpus KK-RU doc-level;
  LoResMT 2026 RU-KK general-domain). Legal-domain LLM MT benchmark for Kazakh not found.
- Effort: 6-8 weeks. Venue: LRE / ARR / LoResMT 2027. Shares machinery with A.

**D. Same model code, two countries: aligning the Civil (and Criminal) Codes of Kazakhstan
and Uzbekistan.**
- Cross-lingual alignment through RU (both have RU versions) of KZ and UZ Civil Codes, both
  derived from the CIS Model Civil Code; divergence map by chapter; gold on a sample.
- Novelty: open (only doctrinal comparative law). Unique to this team (AdiletCodex + lex.uz data).
- Links the KZ line to the UZ thesis line (cross-jurisdiction), and to EUSPN R2.2 (law differs).
- Effort: 8-10 weeks (needs a lawyer familiar with both). Venue: AI and Law / JURIX 2027.

**E. Is it the law or the language? Complexity of the same norms in three languages.**
- Readability/complexity metrics on parallel articles separate legal complexity from
  language complexity; link to amendment frequency (cite КазАТК, do not recompute its dynamics).
- Novelty: open for KZ and for trilingual framing (templates: Katz and Bommarito AI&Law 2014,
  Dutch JURIX 2022, Russian PLOS ONE 2022). Effort: 4 weeks. Venue: Перечень journal or JURIX.
  Weaker than A-D; good as a quick second Перечень/Scopus-borderline paper.

**F. Does the answer depend on the language of the question? LLM legal consistency KK/RU/EN.**
- Same question on the same article asked in three languages; measure answer and citation
  agreement. Narrow angle inside the saturated QA space. Effort 3-4 weeks. Better as a section of B.

Not recommended as standalone: sphere classification (weak, 343 docs), tokenizer tax (method
established; fold into B), generic QA.

### 3.3 Ranking
1. A (divergence audit): most novel, legally meaningful, reuses КазАТК parser, AI and Law fit.
2. B (cross-lingual retrieval): cheapest, direct continuation of EUSPN, fast conference slot.
3. D (KZ-UZ alignment): strongest for the thesis narrative, but needs more annotation.
4. C (legal MT): good, but must be positioned carefully against KazParC.

---

## 4. Recommended plan

### 4.1 One line of work, one dataset DOI
```
Herald KBTU 2025 (CAO, RU, 1 code) ─┐
КазАТК 2026 (5 codes RU, history) ──┼─> AdiletCodex descriptor (LRE) ──> A: KK/RU/EN divergence audit (AI&Law)
EUSPN 2026 (KZ+UZ RAG, RU) ─────────┘      DOI 10.5281/zenodo.22812626  └─> B: cross-lingual retrieval (ACL/ICAIL)
                                                                         └─> D: KZ-UZ code alignment (thesis link)
```
The descriptor's "Background and prior use" section cites all three earlier works as the
predecessors (single code -> five codes and history -> retrieval), then presents the corpus as
the generalisation (343 documents, all three languages). Every new paper cites the Zenodo DOI
and the descriptor. The Zenodo record gets each paper DOI under Related identifiers
("IsDescribedBy" for the descriptor, "IsSupplementTo" for the rest). This builds dataset
citations and a coherent publication track the council can read as one research line.

### 4.2 Timeline
| When | What |
|---|---|
| Oct 2026 | Start usage log. Draft LRE resource paper (70% exists: CODEBOOK, RELATED_WORK, packaging notes, HF card). Run idea A pilot properly (normalise numbers, annotate 100 flags) to serve as LRE technical validation. Present EUSPN (28-30 Oct) and announce AdiletCodex there. |
| Nov 2026 | Submit descriptor to **LRE** (subscription route, free). Start idea B (reuse EUSPN code). |
| Dec 2026 - Jan 2027 | Idea B to ARR January cycle or **ICAIL 2027 (28 Jan)**. Idea A: lawyer annotation, full audit. |
| Feb - Apr 2027 | Idea A to **AI and Law** (if the UZ Paper B is also going there, send A to LRE or Int. J. Semiotics of Law instead; do not stack two submissions in one journal at once). |
| 2027 | D as the cross-jurisdiction chapter of the thesis (JURIX 2027 / AI and Law). |

### 4.3 How it fits with UzCourtCorpus (Paper A / Paper B)
- The UZ line stays the flagship for strong venues once the Supreme Court of Uzbekistan
  answers: Paper A (corpus descriptor) and Paper B (leakage-aware benchmark). Nothing in the
  AdiletCodex track depends on that letter, so this track can run now and in parallel.
- Venue collision to avoid: Paper B / paper#1 targets AI and Law; Paper A may target
  Scientific Data or LRE. If Paper A goes to LRE, keep AdiletCodex at LRE only if timing
  does not overlap, otherwise move the AdiletCodex descriptor to Frontiers in Big Data / JOHD
  (waiver) and keep LRE for Paper A. Decision point: when the Supreme Court replies.
- Different content, no salami risk: KZ statutes (public legislation, trilingual) vs UZ court
  decisions (anonymised judgments). They meet only in idea D and in EUSPN.

### 4.4 What it gives for the defence
- Now: Перечень covered (Herald KBTU Список 1; КазАТК Список 2), EUSPN = Scopus proceedings
  (apробация, not a closing line).
- AdiletCodex descriptor in LRE (95th percentile, typed Article) = **the missing Scopus journal
  article. With Herald KBTU it closes Variant 1 on its own.**
- Plus idea A in AI and Law, or Paper B, = a second >= 35 article, so Variant 2 is closed
  with margin, independent of the Uzbek letters.
- Avoid relying on Data in Brief / Scientific Data / JOHD alone for the closing line because
  of the "Data paper" typing risk; confirm with the KBTU dissertation council how they treat it.

### 4.5 Open items to verify
- KBTU council position on Scopus "Data paper" type.
- Whether Kazakhstan has a Springer OA agreement (would make LRE / AI and Law open access free).
- IEEE Data Descriptions: re-check Scopus in 2027; KBTU-IEEE coverage of full-OA titles.
- Frontiers in Big Data Data Report typing in Scopus.
