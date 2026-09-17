#!/bin/sh
# Re-collect all codes + laws via the adilet JSON API (codex_api spider) into data/raw_api/.
# Adds rich document metadata + all three languages. RESUMABLE (skips non-empty outputs).
# Output: data/raw_api/<doc_id>-<lang>.json
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
CORPUS="$(cd "$HERE/.." && pwd)"
PARSER="${ADILET_PARSER:-$(cd "$CORPUS/../adilet-parser" && pwd)}"
RAW="$CORPUS/data/raw_api"; mkdir -p "$RAW"
export PATH="$HOME/anaconda3/envs/ml311/bin:$PATH"
LOG="${LOG:-$CORPUS/crawl_all_api.log}"

nonempty() { python -c "import json,sys
try:
    d=json.load(open('$1',encoding='utf-8')); sys.exit(0 if isinstance(d,list) and d else 1)
except Exception: sys.exit(1)" 2>/dev/null; }

# doc ids: codes_current.tsv (col1) + laws_current.tsv (col1)
{ tail -n +2 "$CORPUS/codes_current.tsv" | cut -f1; tail -n +2 "$CORPUS/laws_current.tsv" | cut -f1; } | while read -r doc; do
  [ -z "$doc" ] && continue
  for lang in rus kaz eng; do
    out="$RAW/${doc}-${lang}.json"
    if [ -f "$out" ] && nonempty "$out"; then
      printf 'SKIP %s %s\n' "$doc" "$lang" >> "$LOG"; continue
    fi
    ( cd "$PARSER" && scrapy crawl codex_api -a doc_id="$doc" -a lang="$lang" \
        -O "$out" -s LOG_LEVEL=ERROR ) >> "$LOG" 2>&1
    n=$(python -c "import json;print(len(json.load(open('$out',encoding='utf-8'))))" 2>/dev/null || echo 0)
    printf '%s | %-3s | %5s\n' "$doc" "$lang" "$n" >> "$LOG"
    sleep 1
  done
done
echo "CRAWL_API DONE -> $RAW" >> "$LOG"
echo "done. files: $(ls "$RAW" | wc -l)"
