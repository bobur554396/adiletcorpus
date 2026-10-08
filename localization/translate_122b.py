#!/usr/bin/env python3
"""Re-translate legal_sphere and publication_reference unique RU values to EN + KK
using the LOCAL Qwen3.5-122B (thinking disabled) over the SSH tunnel on :8092.
Replaces the weaker Qwen2.5-32B translations. Updates *_map.jsonl in place and logs
publication_reference number-QA failures to pubref_qa_failures_122b.json.

QA (intent-faithful):
  * KK: must be Cyrillic Kazakh. A "Latin leak" is a Latin-letter run that is NOT
    carried over from the RU source (Roman numerals / 'N' / 'c' that are part of the
    citation are allowed). CJK never allowed. One retry, then fall back to a clean
    32B value, else the RU original (logged).
  * EN (hard invariant): must contain NO Cyrillic. One re-translate retry, then
    transliterate as a last resort so eng rows never carry Cyrillic.
  * Number preservation (publication_reference, EN and KK): ordered digit-group
    sequence of translation must equal the RU source; mismatches are logged in
    pubref_qa_failures_122b.json. KK mismatch -> keep RU (Cyrillic, valid for kaz).
    EN mismatch -> prefer a clean number-matching 32B EN, else keep the non-Cyrillic
    122B EN (date-order differences are benign) rather than leak Cyrillic.
"""
import json, os, re, time, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

ENDPOINT = "http://127.0.0.1:8092/v1/chat/completions"
MODEL = "qwen"
MODEL_TAG = "qwen3.5-122b"
HERE = os.path.dirname(os.path.abspath(__file__))

NUMRULE = (" Все числа, даты, номера статей, выпусков и страниц передавай арабскими цифрами "
           "в точно том же порядке и формате, что и в оригинале (сохраняй ведущие нули, "
           "например 03.11.2015); никогда не заменяй числа или месяцы словами и не меняй их порядок.")
SYS_EN = ("Ты профессиональный переводчик юридических текстов. Переводи на английский "
          "язык точно, используя правильную юридическую терминологию. Выводи только "
          "перевод, без пояснений." + NUMRULE)
SYS_EN_STRICT = (SYS_EN + " В ответе не должно быть НИ ОДНОЙ кириллической буквы: все "
                 "названия, газеты и месяцы передавай латиницей (транслитерация или перевод).")
SYS_KK = ("Ты профессиональный переводчик юридических текстов. Переводи на казахский "
          "язык точно, используя правильную юридическую терминологию. Выводи только "
          "перевод, без латиницы и без пояснений." + NUMRULE)
SYS = {"en": SYS_EN, "kk": SYS_KK}

LATIN_RUN = re.compile(r"[A-Za-z]+")
CJK = re.compile(r"[　-鿿豈-﫿＀-￯]")
CYR = re.compile(r"[Ѐ-ӿ]")

TRANSLIT = {
    'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ё':'Yo','Ж':'Zh','З':'Z','И':'I',
    'Й':'Y','К':'K','Л':'L','М':'M','Н':'N','О':'O','П':'P','Р':'R','С':'S','Т':'T',
    'У':'U','Ф':'F','Х':'Kh','Ц':'Ts','Ч':'Ch','Ш':'Sh','Щ':'Shch','Ъ':'','Ы':'Y',
    'Ь':'','Э':'E','Ю':'Yu','Я':'Ya','Ә':'A','Ғ':'G','Қ':'Q','Ң':'Ng','Ө':'O','Ұ':'U',
    'Ү':'U','Һ':'H','І':'I',
}
TRANSLIT.update({k.lower(): v.lower() for k, v in TRANSLIT.items()})


def translit(s):
    return "".join(TRANSLIT.get(ch, ch) for ch in s)


def digit_groups(s):
    return re.findall(r"\d+", s or "")


def has_cjk(txt):
    return bool(CJK.search(txt))


def has_cyr(txt):
    return bool(CYR.search(txt))


def real_latin_leak(txt, ru):
    """A Latin run in txt is a leak only if it is not present in the RU source
    (Roman numerals / 'N' / 'c' belonging to citation numbers are carried over)."""
    ru_low = ru.lower()
    for run in LATIN_RUN.findall(txt):
        if run.lower() not in ru_low:
            return True
    return False


def call(text, lang, sys_override=None, retries=5):
    body = json.dumps({
        "model": MODEL,
        "temperature": 0,
        "max_tokens": 1200,
        "chat_template_kwargs": {"enable_thinking": False},
        "messages": [
            {"role": "system", "content": sys_override or SYS[lang]},
            {"role": "user", "content": "Переведи:\n" + text},
        ],
    }).encode("utf-8")
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(ENDPOINT, data=body,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as r:
                out = json.load(r)
            content = (out["choices"][0]["message"]["content"] or "").strip().strip('"').strip()
            if content:
                return content
            last = "empty content"
        except Exception as e:  # noqa
            last = e
        time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"call failed after {retries}: {last}")


def translate_value(ru, field, prev):
    src_nums = digit_groups(ru)
    prev = prev or {}
    info = {"kk_retried": False, "kk_fallback": None,
            "en_retried": False, "en_translit": False, "pubref_fail": None}

    # ---------- English (hard invariant: no Cyrillic) ----------
    en = call(ru, "en")
    if has_cyr(en):
        info["en_retried"] = True
        en2 = call(ru, "en", sys_override=SYS_EN_STRICT)
        if not has_cyr(en2):
            en = en2

    # ---------- Kazakh (Cyrillic; no real Latin leak; no CJK) ----------
    kk = call(ru, "kk")
    if real_latin_leak(kk, ru) or has_cjk(kk):
        info["kk_retried"] = True
        kk2 = call(ru, "kk")
        if real_latin_leak(kk2, ru) or has_cjk(kk2):
            prev_kk = prev.get("kk", "")
            if prev_kk and not real_latin_leak(prev_kk, ru) and not has_cjk(prev_kk):
                kk = prev_kk
                info["kk_fallback"] = "prev_32b"
            else:
                kk = ru
                info["kk_fallback"] = "ru"
        else:
            kk = kk2

    # ---------- number QA (publication_reference only) ----------
    if field == "publication_reference":
        en_ok = digit_groups(en) == src_nums
        kk_ok = digit_groups(kk) == src_nums
        if not en_ok or not kk_ok:
            fail = {"ru": ru, "src_numbers": src_nums}
            if not en_ok:
                fail["en_raw"] = en
                fail["en_numbers"] = digit_groups(en)
                prev_en = prev.get("en", "")
                if prev_en and not has_cyr(prev_en) and digit_groups(prev_en) == src_nums:
                    en = prev_en
                    fail["en_fallback"] = "prev_32b"
                else:
                    # keep the non-Cyrillic 122B EN (benign date-order diff) over RU-Cyrillic
                    fail["en_fallback"] = "kept_122b_nocyr"
            if not kk_ok:
                fail["kk_raw"] = kk
                fail["kk_numbers"] = digit_groups(kk)
                kk = ru
                fail["kk_fallback"] = "ru"
            info["pubref_fail"] = fail

    # ---------- final EN Cyrillic guarantee ----------
    if has_cyr(en):
        en = translit(en)
        info["en_translit"] = True

    numbers_ok = (digit_groups(en) == src_nums) and (digit_groups(kk) == src_nums)
    rec = {"ru": ru, "en": en, "kk": kk, "numbers_ok": numbers_ok, "model": MODEL_TAG}
    return rec, info


def run(field, workers=4):
    values = [json.loads(l)["ru"] for l in open(os.path.join(HERE, f"{field}_map.jsonl"))]
    prev_map = {}
    bpath = os.path.join(HERE, "32b_backup", f"{field}_map.jsonl")
    if os.path.exists(bpath):
        for l in open(bpath):
            r = json.loads(l)
            prev_map[r["ru"]] = {"en": r.get("en", ""), "kk": r.get("kk", "")}
    print(f"[{field}] re-translating {len(values)} unique values with {MODEL_TAG} ...", flush=True)
    results = {}
    kk_retries = kk_fallbacks = en_retries = en_translits = 0
    kk_fb_list = []
    pubref_fails = []
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(translate_value, v, field, prev_map.get(v)): v for v in values}
        for fut in as_completed(futs):
            v = futs[fut]
            rec, info = fut.result()
            results[v] = rec
            kk_retries += int(info["kk_retried"])
            en_retries += int(info["en_retried"])
            en_translits += int(info["en_translit"])
            if info["kk_fallback"]:
                kk_fallbacks += 1
                kk_fb_list.append({"ru": v, "fallback": info["kk_fallback"]})
            if info["pubref_fail"]:
                pubref_fails.append(info["pubref_fail"])
            done += 1
            if done % 25 == 0 or done == len(values):
                print(f"  {done}/{len(values)}", flush=True)
    ordered = [results[v] for v in values]
    out_path = os.path.join(HERE, f"{field}_map.jsonl")
    with open(out_path, "w") as f:
        for rec in ordered:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    passed = sum(1 for r in ordered if r["numbers_ok"])
    print(f"[{field}] done: numbers_ok={passed}/{len(values)}, kk latin/cjk retries={kk_retries}, "
          f"kk fallbacks={kk_fallbacks}, en cyr-retries={en_retries}, en translit={en_translits}, "
          f"pubref number-fails={len(pubref_fails)}", flush=True)
    return {"field": field, "n": len(values), "numbers_ok": passed,
            "kk_retries": kk_retries, "kk_fallbacks": kk_fb_list,
            "en_retries": en_retries, "en_translits": en_translits,
            "pubref_fails": pubref_fails}


if __name__ == "__main__":
    ls = run("legal_sphere")
    pr = run("publication_reference")
    with open(os.path.join(HERE, "pubref_qa_failures_122b.json"), "w") as f:
        json.dump(pr["pubref_fails"], f, ensure_ascii=False, indent=2)
    summary = {"legal_sphere": ls, "publication_reference": pr}
    with open(os.path.join(HERE, "retranslate_122b_summary.json"), "w") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print("\nSUMMARY")
    for d in (ls, pr):
        print(f"  {d['field']}: n={d['n']} numbers_ok={d['numbers_ok']} "
              f"kk_retries={d['kk_retries']} kk_fallbacks={len(d['kk_fallbacks'])} "
              f"en_retries={d['en_retries']} en_translits={d['en_translits']} "
              f"pubref_fails={len(d['pubref_fails'])}")
