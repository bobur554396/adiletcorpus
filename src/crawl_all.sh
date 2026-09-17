#!/bin/sh
# Crawl all current codes listed in ../codes_current.tsv, in rus/kaz/eng, into ../data/raw/.
# Uses the `adilet-parser` scrapy tool, expected as a sibling directory of this corpus
# project (override with ADILET_PARSER=/path/to/adilet-parser).
# Output files: data/raw/<doc_id>-<lang>-<slug>.json
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"          # adiletcorpus/src
CORPUS="$(cd "$HERE/.." && pwd)"               # adiletcorpus
PARSER="${ADILET_PARSER:-$(cd "$CORPUS/../adilet-parser" && pwd)}"
RAW="$CORPUS/data/raw"; mkdir -p "$RAW"
TSV="$CORPUS/codes_current.tsv"
export PATH="$HOME/anaconda3/envs/ml311/bin:$PATH"
LOG="${LOG:-$CORPUS/crawl_all.log}"; : > "$LOG"

echo "parser: $PARSER" | tee -a "$LOG"
tail -n +2 "$TSV" | while IFS="$(printf '\t')" read -r doc short title; do
  [ -z "$doc" ] && continue
  for lang in rus kaz eng; do
    out="$RAW/${doc}-${lang}-${short}.json"
    ( cd "$PARSER" && scrapy crawl codex -a doc_id="$doc" -a lang="$lang" \
        -O "$out" -s LOG_LEVEL=ERROR ) >>"$LOG" 2>&1
    n=$(python -c "import json;print(len(json.load(open('$out',encoding='utf-8'))))" 2>/dev/null || echo ERR)
    printf '%s | %-3s | %5s | %s\n' "$doc" "$lang" "$n" "$short" | tee -a "$LOG"
    sleep 1
  done
done
echo "DONE -> $RAW" | tee -a "$LOG"
