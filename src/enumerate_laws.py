#!/usr/bin/env python3
"""Enumerate substantive, in-force Laws (ЗАК) of Kazakhstan from adilet search.

Paginates old.adilet.zan.kz/rus/search/docs/va=ЗАК (and optionally КЗАК, КОНС),
parses each result card (doc_id, title, status), and keeps only substantive in-force
laws: drops repealed / not-yet-in-force, and drops amendment / ratification acts that
have no article-level body.

Writes: adiletcorpus/laws_current.tsv  (doc_id \t status \t title)
Also writes laws_all_raw.tsv with everything seen (for auditing).
"""
import re, subprocess, sys, time, urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
TYPES = ["ЗАК", "КЗАК", "КОНС"]   # Law, Constitutional law, Constitution

IN_FORCE = {"Новый", "Обновленный", "Действующий"}
DROP_TITLE = re.compile(
    r"^\s*(о\s+внесении\s+(изменени|дополнени)|"
    r"о\s+ратификации|о\s+присоединении|"
    r"о\s+денонсации|о\s+признании\s+утратив)", re.I)

def fetch(url):
    for _ in range(3):
        r = subprocess.run(["curl", "-sL", "-A", UA, "--max-time", "40", url],
                           capture_output=True, text=True)
        if r.returncode == 0 and len(r.stdout) > 2000:
            return r.stdout
        time.sleep(2)
    return ""

def max_page(html):
    pages = [int(m) for m in re.findall(r"page=(\d+)", html)]
    return max(pages) if pages else 1

def parse_cards(html):
    s = BeautifulSoup(html, "html.parser")
    out = []
    for ph in s.select("div.post_holder"):
        a = ph.select_one("h4.post_header a[href*='/docs/']")
        if not a:
            continue
        did = a["href"].rstrip("/").split("/")[-1].split("#")[0]
        title = a.get_text(" ", strip=True)
        st = ph.select_one("span.status")
        status = st.get_text(strip=True) if st else ""
        out.append((did, status, title))
    return out

def main():
    seen = {}
    raw = []
    for t in TYPES:
        base = "https://old.adilet.zan.kz/rus/search/docs/va=" + urllib.parse.quote(t)
        html = fetch(base)
        mp = max_page(html) if html else 1
        print(f"[{t}] pages: {mp}", flush=True)
        for p in range(1, mp + 1):
            url = base if p == 1 else f"https://old.adilet.zan.kz/rus/search/docs/page={p}&va=" + urllib.parse.quote(t)
            h = fetch(url) if p > 1 else html
            cards = parse_cards(h)
            for did, status, title in cards:
                raw.append((t, did, status, title))
                if did in seen:
                    continue
                if status not in IN_FORCE:
                    continue
                if DROP_TITLE.search(title):
                    continue
                seen[did] = (status, title)
            if p % 20 == 0:
                print(f"  [{t}] page {p}/{mp}  kept so far {len(seen)}", flush=True)
            time.sleep(0.8)
    # write
    with open(ROOT / "laws_current.tsv", "w", encoding="utf-8") as f:
        f.write("doc_id\tstatus\ttitle\n")
        for did, (status, title) in seen.items():
            f.write(f"{did}\t{status}\t{title}\n")
    with open(ROOT / "laws_all_raw.tsv", "w", encoding="utf-8") as f:
        f.write("type\tdoc_id\tstatus\ttitle\n")
        for t, did, status, title in raw:
            f.write(f"{t}\t{did}\t{status}\t{title}\n")
    print(f"\nTOTAL raw results seen: {len(raw)} | distinct substantive in-force laws: {len(seen)}")

if __name__ == "__main__":
    main()
