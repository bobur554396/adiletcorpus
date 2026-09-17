#!/usr/bin/env python3
"""Scrape document metadata from the old.adilet.zan.kz requisites page
(/rus/docs/<id>/info), a clean 'Параметр => Значение' table. Language-independent, so one
fetch per document. Writes data/meta/<doc_id>.json. Resumable, gentle rate limit.

Covers all docs in codes_current.tsv + laws_current.tsv.
"""
import json, re, time, subprocess
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "meta"; OUT.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
DELAY = 2.5

# label on the /info page -> clean field name
FIELDS = {
    "Дата принятия акта": "adoption_date",
    "Дата изменения акта": "change_date",
    "Дата официальной публикации": "publication_date",
    "Информация об официальном опубликовании": "publication_reference",
    "Форма акта": "act_form",
    "Сфера правоотношений": "legal_sphere",
    "Юридическая сила": "legal_force",
    "Орган, принявший акт": "adopting_organ",
    "Регион действия": "region_action",
    "Регистрационный номер акта в Государственном реестре": "state_registry_number",
    "Регистрационный номер НПА": "npa_registration_number",
    "Орган разработчик НПА": "developer_organ",
    "Раздел Базы данных": "database_section",
    "Место принятия акта": "adoption_place",
}

def fetch(url):
    for a in range(3):
        r = subprocess.run(["curl", "-sS", "-A", UA, "--connect-timeout", "20",
                            "--max-time", "60", url], capture_output=True, text=True)
        if r.returncode == 0 and len(r.stdout) > 1000:
            return r.stdout
        time.sleep(3 * (a + 1))
    return ""

def parse_meta(html):
    s = BeautifulSoup(html, "html.parser")
    raw = {}
    for tr in s.select("tr"):
        cells = [re.sub(r"\s+", " ", c.get_text(" ", strip=True)) for c in tr.select("td,th")]
        cells = [c for c in cells if c]
        if len(cells) >= 2:
            raw[cells[0]] = cells[1]
    out = {}
    for label, val in raw.items():
        for pref, field in FIELDS.items():
            if label.startswith(pref):
                out[field] = (None if val in ("НЕТ", "") else val)
                break
    return out

def doc_ids():
    ids = []
    for fn in ["codes_current.tsv", "laws_current.tsv"]:
        for ln in (ROOT / fn).read_text(encoding="utf-8").splitlines()[1:]:
            d = ln.split("\t")[0].strip()
            if d:
                ids.append(d)
    seen = set(); res = []
    for d in ids:
        if d not in seen:
            seen.add(d); res.append(d)
    return res

def main():
    ids = doc_ids()
    print(f"docs: {len(ids)}", flush=True)
    ok = 0
    for i, doc in enumerate(ids):
        fp = OUT / f"{doc}.json"
        if fp.exists():
            try:
                if json.load(open(fp)):
                    ok += 1; continue
            except Exception:
                pass
        html = fetch(f"https://old.adilet.zan.kz/rus/docs/{doc}/info")
        meta = parse_meta(html) if html else {}
        json.dump(meta, open(fp, "w", encoding="utf-8"), ensure_ascii=False)
        if meta:
            ok += 1
        if i % 20 == 0:
            print(f"  {i}/{len(ids)} ok={ok}", flush=True)
        time.sleep(DELAY)
    print(f"DONE. metadata scraped: {ok}/{len(ids)}", flush=True)

if __name__ == "__main__":
    main()
