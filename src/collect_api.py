#!/usr/bin/env python3
"""Fast single-process collector via the adilet JSON API.

Re-implements what `scrapy crawl codex_api` does, but in one process with a reused HTTP
session (no per-doc scrapy startup): for every code + law (codes_current.tsv,
laws_current.tsv) and every language (rus/kaz/eng) it calls the API, parses the text via
the shared CodexApiSpider logic, and writes data/raw_api/<doc_id>-<lang>.json with the
full article text + rich metadata. Resumable (skips non-empty outputs), rate-limited.
"""
import sys, json, time
from pathlib import Path
import requests
from scrapy.http import TextResponse

ROOT = Path(__file__).resolve().parents[1]
PARSER = ROOT.parent / "adilet-parser"
sys.path.insert(0, str(PARSER))
from AdiletParser.spiders.codex_api import CodexApiSpider

RAW = ROOT / "data" / "raw_api"; RAW.mkdir(parents=True, exist_ok=True)
API = "https://adilet.zan.kz/api/documents/by-ngr/{doc}?language={lang}"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
LANGS = ["rus", "kaz", "eng"]

def doc_ids():
    out = []
    for fn in ["codes_current.tsv", "laws_current.tsv"]:
        for ln in (ROOT / fn).read_text(encoding="utf-8").splitlines()[1:]:
            d = ln.split("\t")[0].strip()
            if d:
                out.append(d)
    # dedup preserving order
    seen = set(); res = []
    for d in out:
        if d not in seen:
            seen.add(d); res.append(d)
    return res

def nonempty(fp):
    try:
        return bool(json.load(open(fp, encoding="utf-8")))
    except Exception:
        return False

def fetch(sess, url):
    for a in range(3):
        try:
            r = sess.get(url, headers={"User-Agent": UA}, timeout=(15, 120))
            if r.status_code == 200 and r.content:
                return r.content
        except Exception:
            pass
        time.sleep(3 * (a + 1))
    return None

def main():
    docs = doc_ids()
    print(f"docs: {len(docs)} x {len(LANGS)} langs = {len(docs)*len(LANGS)} calls", flush=True)
    sess = requests.Session()
    done = ok = empty = 0
    for i, doc in enumerate(docs):
        for lang in LANGS:
            fp = RAW / f"{doc}-{lang}.json"
            if fp.exists() and nonempty(fp):
                continue
            body = fetch(sess, API.format(doc=doc, lang=lang))
            if not body:
                json.dump([], open(fp, "w")); empty += 1
                print(f"  {doc} {lang}: FETCH-FAIL", flush=True); time.sleep(1); continue
            sp = CodexApiSpider(doc_id=doc, lang=lang)
            resp = TextResponse(url=API.format(doc=doc, lang=lang), body=body, encoding="utf-8")
            try:
                items = [dict(x) for x in sp.parse(resp)]
            except Exception as e:
                items = []; print(f"  {doc} {lang}: PARSE-ERR {e}", flush=True)
            json.dump(items, open(fp, "w", encoding="utf-8"), ensure_ascii=False)
            done += 1
            if items:
                ok += 1
            else:
                empty += 1
            time.sleep(float(__import__("os").environ.get("API_DELAY", "3.0")))  # gentle default
        if i % 20 == 0:
            print(f"  {i}/{len(docs)} docs | wrote={done} nonempty={ok} empty={empty}", flush=True)
    print(f"DONE. wrote={done} nonempty={ok} empty={empty}", flush=True)

if __name__ == "__main__":
    main()
