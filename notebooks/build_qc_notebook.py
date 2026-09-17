#!/usr/bin/env python3
"""Generate + execute the KZ-codes QC/EDA notebook from data/raw/*.json."""
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
from nbconvert.preprocessors import ExecutePreprocessor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks" / "kz_codes_qc.ipynb"

cells = []
def md(t): cells.append(new_markdown_cell(t))
def code(t): cells.append(new_code_cell(t))

md("# AdiletCodex - QC & EDA\n"
   "Quality control and exploratory analysis of the parsed current Codes of the "
   "Republic of Kazakhstan (trilingual: Kazakh / Russian / English), from adilet.zan.kz.\n\n"
   "Checks: coverage, structural hierarchy, article-length distribution, cross-language "
   "alignment, and **language integrity** (that KZ/RU/EN are genuinely different languages, "
   "not duplicates).")

code(r"""
import json, glob, os, re, unicodedata
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAW = "../data/raw"
FIGS = "figs"; os.makedirs(FIGS, exist_ok=True)

ART_PAT = {"rus": r"статья\s+(\d+(?:-\d+)?)",
           "kaz": r"(\d+(?:-\d+)?)-бап",
           "eng": r"article\s+(\d+(?:-\d+)?)"}

def art_no(title, lang):
    m = re.match(r"^\s*" + ART_PAT.get(lang, r"(\d+)"), title or "", re.I)
    return m.group(1) if m else None

rows = []
for f in sorted(glob.glob(RAW + "/*.json")):
    base = os.path.basename(f)[:-5]
    parts = base.split("-")
    doc_id, lang = parts[0], parts[1]
    short = "-".join(parts[2:])
    try:
        d = json.load(open(f, encoding="utf-8"))
    except Exception:
        d = []
    for r in d:
        txt = r.get("article_text") or ""
        rows.append({
            "doc_id": doc_id, "short": short, "lang": lang,
            "part": r.get("part"), "section": r.get("section"), "chapter": r.get("chapter"),
            "article_no": art_no(r.get("article_title"), lang),
            "article_title": r.get("article_title"), "text": txt, "char_len": len(txt),
            "n_par": len(r.get("paragraphs") or []), "n_notes": len(r.get("notes") or []),
            "n_links": len(r.get("links") or []),
            "title_doc": r.get("title"), "status": r.get("status"), "url": r.get("url"),
        })
df = pd.DataFrame(rows)
print("Total article records:", len(df))
print("Distinct codes:", df.short.nunique(), "| languages:", sorted(df.lang.unique()))
df.head(3)
""")

md("## 1. Coverage: records per language and per code")
code(r"""
print("Records per language:")
print(df.lang.value_counts().to_string())
piv = df.pivot_table(index="short", columns="lang", values="article_title",
                     aggfunc="count", fill_value=0)
piv = piv[["rus","kaz","eng"]] if set(["rus","kaz","eng"]).issubset(piv.columns) else piv
piv.loc["TOTAL"] = piv.sum()
piv
""")

md("## 2. Article length distribution (characters)")
code(r"""
print(df.groupby("lang")["char_len"].describe()[["count","mean","50%","max"]])
fig, ax = plt.subplots(figsize=(7,4))
for lang in ["rus","kaz","eng"]:
    s = df[df.lang==lang]["char_len"].clip(upper=6000)
    ax.hist(s, bins=50, alpha=0.5, label=lang)
ax.set_xlabel("article length (chars, clipped at 6000)"); ax.set_ylabel("articles")
ax.legend(); ax.set_title("Article length distribution by language")
plt.tight_layout(); plt.savefig(FIGS+"/len_by_lang.png", dpi=110); plt.show()
print("empty-text records:", int((df.char_len==0).sum()))
""")

md("## 3. Structural hierarchy coverage\n"
   "Share of articles that carry part / section / chapter context.")
code(r"""
cov = df.assign(has_part=df.part.notna(), has_sec=df.section.notna(), has_ch=df.chapter.notna())
print((cov.groupby("lang")[["has_part","has_sec","has_ch"]].mean()*100).round(1).astype(str)+" %")
""")

md("## 4. Language integrity (the key check)\n"
   "KZ must contain Kazakh-specific letters; RU Cyrillic without them; EN Latin. And no two "
   "languages of the same article may be byte-identical (that was the failure in the earlier "
   "Uzbek corpus).")
code(r"""
KAZ = set("әғқңөұүһіӘҒҚҢӨҰҮҺІ")
def profile(t):
    t = (t or "")[:800]
    cyr = sum(1 for c in t if "CYRILLIC" in unicodedata.name(c, ""))
    lat = sum(1 for c in t if "LATIN" in unicodedata.name(c, ""))
    kaz = any(c in KAZ for c in t)
    return cyr, lat, kaz
prof = df.assign(**{k: v for k, v in zip(["cyr","lat","kaz_letters"],
        zip(*df.text.map(profile)))})
# expected script per lang
def ok(row):
    if row.lang=="eng": return row.lat > row.cyr
    if row.lang=="kaz": return row.cyr > row.lat  # kaz is Cyrillic script
    if row.lang=="rus": return row.cyr > row.lat
    return True
prof["script_ok"] = prof.apply(ok, axis=1)
print("script matches expected, per lang (%):")
print((prof.groupby("lang")["script_ok"].mean()*100).round(2).to_string())
print("\nKZ records actually containing Kazakh-specific letters: %.1f%%" %
      (prof[prof.lang=="kaz"]["kaz_letters"].mean()*100))
# cross-language identical-text check
key = ["short","article_no"]
wide = df[df.article_no.notna()].pivot_table(index=key, columns="lang", values="text",
        aggfunc="first")
def same(a,b): return (a is not None) and (b is not None) and isinstance(a,str) and a==b
dups = 0; checked = 0
for _, r in wide.iterrows():
    for a,b in [("rus","kaz"),("rus","eng"),("kaz","eng")]:
        if a in wide.columns and b in wide.columns:
            checked += 1
            if same(r.get(a), r.get(b)): dups += 1
print("\ncross-language identical-text pairs:", dups, "(out of", checked, "compared) -> want 0")
""")

md("## 5. Cross-language alignment\n"
   "How many articles of each code are present in all three languages (matched by article number).")
code(r"""
align = (df[df.article_no.notna()]
         .groupby(["short","lang"])["article_no"].apply(set).unstack())
def tri(row):
    sets = [row[l] for l in ["rus","kaz","eng"] if l in row.index and isinstance(row[l], set)]
    if len(sets) < 3: return np.nan
    inter = set.intersection(*sets); uni = set.union(*sets)
    return round(100*len(inter)/len(uni), 1) if uni else np.nan
rep = pd.DataFrame({
    "rus": align.get("rus").map(lambda s: len(s) if isinstance(s,set) else 0),
    "kaz": align.get("kaz").map(lambda s: len(s) if isinstance(s,set) else 0),
    "eng": align.get("eng").map(lambda s: len(s) if isinstance(s,set) else 0),
})
rep["3-lang overlap %"] = align.apply(tri, axis=1)
rep.sort_values("3-lang overlap %")
""")

md("## 6. Content sanity: duplicates, gaps, empties")
code(r"""
dup = df[df.article_no.notna()].groupby(["short","lang","article_no"]).size()
dupd = dup[dup>1]
print("duplicate (code,lang,article_no) keys:", len(dupd))
print(dupd.head(10).to_string() if len(dupd) else "  none")
print("\nempty article_text:", int((df.char_len==0).sum()))
# numbering gaps per code (rus), base numbers only
def gaps(short):
    s = df[(df.short==short)&(df.lang=="rus")]["article_no"].dropna()
    base = sorted({int(x.split('-')[0]) for x in s})
    if not base: return 0
    full = set(range(base[0], base[-1]+1))
    return len(full - set(base))
gp = pd.Series({sh: gaps(sh) for sh in sorted(df.short.unique())}, name="rus_numbering_gaps")
print("\nnumbering gaps (repealed articles) per code - expected, not errors:")
print(gp.to_string())
""")

md("## 7. Random samples (eyeball check)")
code(r"""
import random
random.seed(2026)
for _ in range(4):
    r = df.iloc[random.randrange(len(df))]
    print("="*80)
    print(f"[{r.lang}] {r.short}  |  {r.article_title}")
    print(f"part={r.part} | section={r.section} | chapter={r.chapter}")
    print(r.text[:400])
    print()
""")

md("## 8. Articles per code (bar chart)")
code(r"""
by_code = df[df.lang=="rus"].groupby("short").size().sort_values()
fig, ax = plt.subplots(figsize=(8,7))
by_code.plot.barh(ax=ax)
ax.set_xlabel("articles (RU)"); ax.set_title("Articles per code (Russian)")
plt.tight_layout(); plt.savefig(FIGS+"/articles_per_code.png", dpi=110); plt.show()
print("saved figs/len_by_lang.png, figs/articles_per_code.png")
""")

nb = new_notebook(cells=cells)
nb.metadata.kernelspec = {"name": "python3", "display_name": "Python 3"}
ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
ep.preprocess(nb, {"metadata": {"path": str(ROOT / "notebooks")}})
nbf.write(nb, str(NB))
print("WROTE + EXECUTED:", NB)
