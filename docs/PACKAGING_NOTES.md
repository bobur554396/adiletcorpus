# Packaging notes / cross-language quirks (adilet KZ codes)

Findings during the full crawl (2026-09-15). These are NOT parser bugs - the parser
extracts real content; they must be handled at packaging/QC time.

## Civil Code: English merges both parts
- RU/KZ split the Civil Code into two documents:
  - `K940001000_` = General part (articles 1-405)
  - `K990000409_` = Special part (separate doc)
- ENG `K940001000_` contains BOTH parts in one document (articles 1-1124; distinct
  `part` values include "GENERAL PART ..." and "Special part) ... № 409").
- Consequence: for the Civil Code, cross-language alignment must be by (subject,
  article_no), NOT by doc_id. And ENG `K990000409_` likely re-contains the Special
  part -> DEDUP needed (drop the eng special-part articles already present under the
  eng general doc, or prefer one source).

## General packaging rules to apply
- Align languages by (code subject, article_no), since a given code can carry
  different doc_ids per language and (as above) different part groupings.
- Dedup at (doc_subject, lang, article_no) level; keep the richest record.
- LANGUAGE INTEGRITY CHECK (lesson from the UZ corpus disaster): verify that the
  `kaz` text is actually Kazakh (contains әғқңөұүһі / distinctive letters), `rus` is
  Russian, `eng` is Latin - and that uz/ru/eng of the same article are NOT byte-identical.
  Never ship a "trilingual" corpus whose languages are duplicates.
- Some codes may lack an ENG (or KAZ) version -> the crawl yields an empty file for
  that lang; record coverage honestly, do not fabricate.
- The Tax Code has two in-force docs during transition: K2500000214 (2025, new) and
  K1700000120 (2017, outgoing). Both included; mark which is which.
