#!/usr/bin/env python3
"""check-freshness.py — 時效宣告與逾期（S6，2026-09-27）

設計原則：**強制宣告、超期警告**。
  - 「這一頁的數字是哪一天驗的」是**可機械驗證**的事 ⇒ 沒宣告就是**違規**（硬）。
  - 「宣告的日期之後數字還是不是真的」不是機械可驗的事 ⇒ 超過 90 天只**警告**（warn），
    交由第六條鐵律的週期稽核處理。
  - 禁止把 `updated:`（改過字）當成驗證日；SK 頁例外允許用 `l3_run_at`（L3 實跑即驗證行為）。

規則：
  1. 頁面若含「日期＋量化」的快照行（`20YY-MM-DD` 與 %／億／兆／pp／倍／萬元 同行），
     frontmatter 必須有 `last_verified: YYYY-MM-DD`、或以 `待複驗` 明示**尚未驗**，
     SK 頁可用 `l3_run_at` 代替。三者皆無 ⇒ **違規**（未宣告時效狀態）。
  2. 有效驗證日 > 90 天 ⇒ **警告**（列入逾期清單，不是失敗）。

用法: python3 skills/_scripts/check-freshness.py [--repo-root .] [--days 90] [--json] [--strict]
  預設 **warn**（違規只報告）；`--strict` 時「未宣告」以非零 exit 結束（逾期仍只警告）。
"""
import argparse, datetime, glob, json, os, re, sys

DATE = re.compile(r"20\d\d-\d\d-\d\d")
QTY = re.compile(r"\d+\.?\d*\s*(%|％|億|兆|pp|倍|萬口|萬元|sessions)")
PAGE_GLOBS = ("skills/SK-*.md", "concepts/*.md", "entities/*.md", "summaries/*.md", "templates/*.md")

def fm_of(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    return m.group(1) if m else ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--today", default=None, help="覆寫今天（測試用，YYYY-MM-DD）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    today = datetime.date.fromisoformat(a.today) if a.today else datetime.date.today()
    files = []
    for pat in PAGE_GLOBS:
        files += [f for f in sorted(glob.glob(os.path.join(a.repo_root, pat))) if ".bak" not in f]
    undeclared, overdue = [], []
    for f in files:
        t = open(f, encoding="utf-8").read()
        fm = fm_of(t)
        body = t[len(fm) + 8:] if fm else t
        if not any(DATE.search(l) and QTY.search(l) for l in body.split("\n")):
            continue
        rel = os.path.relpath(f, a.repo_root)
        lv = re.search(r"^last_verified:\s*(\d{4}-\d{2}-\d{2})", fm, re.MULTILINE)
        l3 = re.search(r"^l3_run_at:\s*(\d{4}-\d{2}-\d{2})", fm, re.MULTILINE)
        pending = "待複驗" in fm
        if not (lv or l3 or pending):
            undeclared.append(rel); continue
        eff = lv or l3
        if eff:
            d = datetime.date.fromisoformat(eff.group(1))
            if (today - d).days > a.days:
                overdue.append((rel, eff.group(1), (today - d).days))
    if a.json:
        print(json.dumps({"files": len(files), "undeclared": undeclared,
                          "overdue": [{"file": f, "last_verified": d, "days": n} for f, d, n in overdue]},
                         ensure_ascii=False, indent=1))
        return 1 if (a.strict and undeclared) else 0
    print("═" * 64)
    print(f"時效宣告與逾期（S6，門檻 {a.days} 天；今天 {today}）— {len(files)} 頁")
    print("═" * 64)
    if undeclared:
        print(f"{'❌' if a.strict else '⚠️ '} 未宣告時效狀態：{len(undeclared)} 頁（含日期＋量化快照行，但無 last_verified／l3_run_at／待複驗）")
        for r in undeclared: print(f"   - {r}")
    else:
        print("✅ 所有含日期快照的頁面都已宣告時效狀態")
    print(f"\n⚠️  已宣告但逾期（>{a.days} 天）：{len(overdue)} 頁（僅警告；交第六條鐵律週期稽核）")
    for r, d, n in overdue[:15]: print(f"   - {r}（last_verified={d}，{n} 天）")
    if len(overdue) > 15: print(f"   … 另有 {len(overdue)-15} 頁")
    if a.strict and undeclared:
        return 1
    print(f"\n（warn 模式{'' if not undeclared else '；待上述未宣告頁補完後改 --strict'}）")
    return 0

if __name__ == "__main__":
    sys.exit(main())
