#!/bin/sh
# Crawl substantive in-force laws (../laws_current.tsv) in rus/kaz/eng into ../data/raw_laws/,
# using the `law` spider from the sibling adilet-parser tool.
# RESUMABLE: skips outputs that already exist and are non-empty. Safe to re-run.
# Output files: data/raw_laws/<doc_id>-<lang>.json
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
CORPUS="$(cd "$HERE/.." && pwd)"
PARSER="${ADILET_PARSER:-$(cd "$CORPUS/../adilet-parser" && pwd)}"
RAW="$CORPUS/data/raw_laws"; mkdir -p "$RAW"
TSV="$CORPUS/laws_current.tsv"
export PATH="$HOME/anaconda3/envs/ml311/bin:$PATH"
LOG="${LOG:-$CORPUS/crawl_laws.log}"

nonempty() {  # $1 = file -> returns 0 if file has a JSON array with >=1 item
  python -c "import json,sys
try:
    d=json.load(open('$1',encoding='utf-8')); sys.exit(0 if isinstance(d,list) and d else 1)
except Exception:
    sys.exit(1)" 2>/dev/null
}

done=0; skipped=0; empty=0
tail -n +2 "$TSV" | while IFS="$(printf '\t')" read -r doc status title; do
  [ -z "$doc" ] && continue
  for lang in rus kaz eng; do
    out="$RAW/${doc}-${lang}.json"
    if [ -f "$out" ] && nonempty "$out"; then
      printf 'SKIP %s %s (exists)\n' "$doc" "$lang" >> "$LOG"
      continue
    fi
    ( cd "$PARSER" && scrapy crawl law -a doc_id="$doc" -a lang="$lang" \
        -O "$out" -s LOG_LEVEL=ERROR ) >> "$LOG" 2>&1
    n=$(python -c "import json;print(len(json.load(open('$out',encoding='utf-8'))))" 2>/dev/null || echo 0)
    printf '%s | %-3s | %5s | %s\n' "$doc" "$lang" "$n" "$(echo "$title" | cut -c1-40)" >> "$LOG"
    sleep 1
  done
done
echo "CRAWL_LAWS DONE -> $RAW" >> "$LOG"
echo "done. files: $(ls "$RAW" | wc -l)"
