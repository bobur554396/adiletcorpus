#!/usr/bin/env python3
"""Group B (FREE-TEXT) machine translation for AdiletCodex v1.1 extended localization.
Translates the UNIQUE Russian values of `legal_sphere` and `publication_reference`
to English and Kazakh using Qwen 2.5 32B (vLLM, OpenAI-compatible) over an SSH tunnel.

Number-preservation QA: the ordered sequence of digit-groups in source and translation
must match exactly; otherwise the Russian original is kept for that language and the
entry is logged in qa_failures.
"""
import json, os, re, sys, time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

ENDPOINT = "http://127.0.0.1:8088/v1/chat/completions"
MODEL = "qwen"
HERE = os.path.dirname(os.path.abspath(__file__))

SYS = ("You are a professional legal translator. Translate the Russian text to {lang}. "
       "Translate Russian words only. Preserve ALL digits, numbers, dates, "
       "article/issue/paragraph numbers and Latin/proper tokens EXACTLY as written. "
       "Do not add or remove any numbers. Return ONLY the translation, with no "
       "explanations, no surrounding quotes, and no commentary.")

LANG_NAME = {"en": "English", "kk": "Kazakh"}


def digit_groups(s):
    return re.findall(r"\d+", s or "")


def call(text, lang, retries=4):
    body = json.dumps({
        "model": MODEL,
        "temperature": 0,
        "max_tokens": 1024,
        "messages": [
            {"role": "system", "content": SYS.format(lang=LANG_NAME[lang])},
            {"role": "user", "content": text},
        ],
    }).encode("utf-8")
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(ENDPOINT, data=body,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                out = json.load(r)
            return out["choices"][0]["message"]["content"].strip().strip('"').strip()
        except Exception as e:  # noqa
            last = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"failed after {retries}: {last}")


def translate_value(ru):
    src_nums = digit_groups(ru)
    en = call(ru, "en")
    kk = call(ru, "kk")
    en_ok = digit_groups(en) == src_nums
    kk_ok = digit_groups(kk) == src_nums
    rec = {"ru": ru, "en": en if en_ok else ru, "kk": kk if kk_ok else ru,
           "numbers_ok": bool(en_ok and kk_ok)}
    fail = None
    if not (en_ok and kk_ok):
        fail = {"ru": ru, "src_numbers": src_nums,
                "en_raw": en, "en_numbers": digit_groups(en), "en_ok": en_ok,
                "kk_raw": kk, "kk_numbers": digit_groups(kk), "kk_ok": kk_ok}
    return rec, fail


def run(field, values, workers=8):
    print(f"[{field}] translating {len(values)} unique values ...", flush=True)
    results = {}
    failures = []
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(translate_value, v): v for v in values}
        for fut in as_completed(futs):
            v = futs[fut]
            rec, fail = fut.result()
            results[v] = rec
            if fail:
                failures.append(fail)
            done += 1
            if done % 25 == 0 or done == len(values):
                print(f"  {done}/{len(values)}", flush=True)
    # preserve input order
    ordered = [results[v] for v in values]
    out_path = os.path.join(HERE, f"{field}_map.jsonl")
    with open(out_path, "w") as f:
        for rec in ordered:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    fail_path = os.path.join(HERE, f"{field}_qa_failures.json")
    with open(fail_path, "w") as f:
        json.dump(failures, f, ensure_ascii=False, indent=2)
    passed = sum(1 for r in ordered if r["numbers_ok"])
    print(f"[{field}] done: {passed}/{len(values)} passed number-check, "
          f"{len(failures)} failed -> {out_path}", flush=True)
    return passed, len(failures)


if __name__ == "__main__":
    ls = json.load(open(os.path.join(HERE, "_work/legal_sphere.json")))
    pr = json.load(open(os.path.join(HERE, "_work/publication_reference.json")))
    p1, f1 = run("legal_sphere", ls)
    p2, f2 = run("publication_reference", pr)
    print("SUMMARY")
    print(f"  legal_sphere: {len(ls)} unique, {p1} pass, {f1} fail")
    print(f"  publication_reference: {len(pr)} unique, {p2} pass, {f2} fail")
