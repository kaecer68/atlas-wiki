#!/usr/bin/env python3
"""check-claim-rules.py — 禁用句型（S7，2026-09-27）

對位 `atlas-wiki-quality` skill 的「禁用主張」清單。只收**高精度**規則：每條都對應
2026-09-27 當天**實際發生過**的過度主張，且規則設計成「有正當說明就放行」。

規則（逐行；同一行同時命中 trigger 且缺 escape 才算違規）：
  R1  提到 `-synthetic` 與 `R²_OOS`，卻沒有「in-sample／不可當（市場結論）／存在性／模型層」⇒
      合成路徑的 R² 是 **in-sample**（`runSynthetic` 對同一份 X Fit→Predict），不可當 OOS。
  R2  斷言 `var_95`/`var_99`/`cvar_95` 為 0，卻沒有任何說明
      （`insufficient`／資料不足／`var_available`／未計算／資料可見性）⇒ 0 必須標明是「資料不足」或其原因。
  R3  寫到探測結果 `401`，卻沒提 `key`／授權 ⇒ atlas 未帶 `X-API-Key` 時先回 401，
      會蓋住真正的 404（判 route 必須帶 key）。

用法: python3 skills/_scripts/check-claim-rules.py [--repo-root .] [--json]
exit 0 = 無違規；exit 1 = 有違規（本檢查為**硬門檻**；規則刻意窄，避免誤報）
"""
import argparse, glob, json, os, re, sys

RULES = [
    ("R1", "synthetic 的 R²_OOS 未標 in-sample",
     re.compile(r"(?=.*(?:-synthetic|synthetic))(?=.*R²_OOS)"),
     re.compile(r"in-sample|不可當|存在性|模型層")),
    ("R2", "var/cvar 為 0 未說明（資料不足或原因）",
     re.compile(r"(?:var_9[59]|cvar_95)[^|\n]{0,40}?(?:=\s*0(?![\d.])|\*\*0\*\*|為\s*0(?![\d.])|皆\s*0(?![\d.])|:\s*0(?![\d.]))"),
     re.compile(r"insufficient|資料不足|var_available|未計算|可見性|not_available|不可行|非零")),
    ("R3", "401 探測結果未提 key/授權",
     re.compile(r"→\s*401|回\s*401|=\s*401"),
     re.compile(r"X-API-Key|key|授權|auth")),
]
PAGE_GLOBS = ("skills/SK-*.md", "concepts/*.md", "entities/*.md", "summaries/*.md", "templates/*.md")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    files = []
    for pat in PAGE_GLOBS:
        files += [f for f in sorted(glob.glob(os.path.join(a.repo_root, pat))) if ".bak" not in f]
    out = []
    for f in files:
        for i, line in enumerate(open(f, encoding="utf-8").read().split("\n"), 1):
            for rid, label, trig, esc in RULES:
                if trig.search(line) and not esc.search(line):
                    out.append({"rule": rid, "label": label, "file": os.path.relpath(f, a.repo_root),
                                "line": i, "text": line.strip()[:120]})
    if a.json:
        print(json.dumps({"files": len(files), "violations": out}, ensure_ascii=False, indent=1)); return 0
    print("═" * 64)
    print(f"禁用句型檢查（S7）— {len(files)} 頁")
    print("═" * 64)
    if not out:
        print("✅ 無違規（規則：R1 synthetic→in-sample／R2 零值須說明／R3 401 須提 key）")
        return 0
    print(f"❌ {len(out)} 條違規")
    for v in out[:20]:
        print(f"   [{v['rule']}] {v['file']}:{v['line']} — {v['label']}")
        print(f"        {v['text']}")
    if len(out) > 20:
        print(f"   … 另有 {len(out)-20} 條")
    return 1

if __name__ == "__main__":
    sys.exit(main())
