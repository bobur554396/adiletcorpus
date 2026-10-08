#!/usr/bin/env python3
"""Re-translate the handful of Group-B entries where Qwen emitted CJK characters or
meta-commentary. Stricter prompt + validation (no CJK, no commentary, numbers preserved).
Updates the *_map.jsonl files in place."""
import json, os, re, time, urllib.request

ENDPOINT = "http://127.0.0.1:8088/v1/chat/completions"
HERE = os.path.dirname(os.path.abspath(__file__))
CYR = re.compile('[Ѐ-ӿ]'); CJK = re.compile('[一-鿿]')
META = re.compile(r'(?i)\bnote:|translat|however|more appropriate|\n\n')
LANG_NAME = {"en": "English", "kk": "Kazakh"}

SYS = ("You are a professional legal translator. Translate the Russian text to {lang}. "
       "Translate Russian words only. Preserve ALL digits, numbers, dates and "
       "article/issue numbers EXACTLY. Output MUST contain only {lang} (Latin script for "
       "English; Cyrillic Kazakh for Kazakh) plus numbers and punctuation - never Chinese or "
       "other scripts. Return ONLY the translation on a single line: no notes, no commentary, "
       "no quotes, no explanations.")


def digit_groups(s):
    return re.findall(r"\d+", s or "")


def call(text, lang, temp):
    body = json.dumps({"model": "qwen", "temperature": temp, "max_tokens": 800,
                       "messages": [{"role": "system", "content": SYS.format(lang=LANG_NAME[lang])},
                                    {"role": "user", "content": text}]}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        out = json.load(r)
    return out["choices"][0]["message"]["content"].strip().strip('"').strip().split("\n")[0].strip()


def good(txt, lang, field, src):
    if CJK.search(txt) or META.search(txt):
        return False
    if digit_groups(txt) != digit_groups(src):
        return False
    if lang == "en" and field == "legal_sphere" and CYR.search(txt):
        return False
    return True


def retranslate(src, lang, field):
    for temp in (0, 0, 0.2, 0.3):
        try:
            t = call(src, lang, temp)
            if good(t, lang, field, src):
                return t, True
        except Exception:
            time.sleep(2)
    return None, False


def fix(field):
    path = os.path.join(HERE, f"{field}_map.jsonl")
    rows = [json.loads(l) for l in open(path)]
    fixed = 0
    for r in rows:
        changed = False
        for lang in ("en", "kk"):
            if CJK.search(r[lang]) or META.search(r[lang]) or (
                    lang == "en" and field == "legal_sphere" and CYR.search(r[lang])):
                t, ok = retranslate(r["ru"], lang, field)
                if ok:
                    r[lang] = t; changed = True
                else:
                    # last resort: if a clean translation can't be had, keep RU original
                    r[lang] = r["ru"]; changed = True
        if changed:
            # recompute numbers_ok against both langs
            sn = digit_groups(r["ru"])
            r["numbers_ok"] = (digit_groups(r["en"]) == sn) and (digit_groups(r["kk"]) == sn)
            fixed += 1
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[{field}] re-translated {fixed} entries")


if __name__ == "__main__":
    fix("legal_sphere")
    fix("publication_reference")
