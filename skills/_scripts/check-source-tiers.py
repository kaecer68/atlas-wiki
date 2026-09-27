#!/usr/bin/env python3
"""check-source-tiers.py — 外部事實的來源可追溯性（S3，2026-09-27）

對位第六條鐵律（外部權威報告週期稽核）。**頁級判準**（刻意不做行級 regex：實測行級會誤判
「(IMF)」「WGC 數據」「IMF COFER(季報)」這類合法內嵌來源）。

規則：
  若某知識頁的**內文**同時出現（a）外部權威機構名（IMF／BIS／UNCTAD／金管會／證交所／TWSE／
  TPEx／主計總處／央行／CBOE／OECD／FSC／Stanford HAI…）與（b）量化主張（%／億／兆／pp／倍／萬元），
  則該頁的 frontmatter 必須至少有一筆**可追溯來源**：URL／政府網域／法規名（辦法・條例・準則・要點・令・函）
  ／報告名（WIR・WEO・AI Index・Annual Report…）／`實務慣例` 標記。

三種合法結果：
  1. 有可追溯來源 ⇒ ✅
  2. 該數字其實是**實務慣例**或**本頁自算** ⇒ 在 frontmatter sources 明寫（例：`- 實務慣例（券商/證金）`）
  3. 查不到來源 ⇒ 在 frontmatter 明寫 `- 待查（YYYY-MM-DD）`（誠實標示，不假收斂）

用法: python3 skills/_scripts/check-source-tiers.py [--repo-root .] [--json] [--strict]
  預設 **warn**（只報告）；`--strict` 以違規數非零結束（待內容補完後開啟，與 S5 同一兩段式節奏）。
"""
import argparse, glob, json, os, re, sys

AUTH = re.compile(r"IMF|WEO|BIS\b|UNCTAD|Stanford HAI|OECD|金管會|FSC\b|證交所|TWSE|TPEx|櫃買|主計總處|CBOE|聯準會|央行|財政部")
QTY = re.compile(r"\d+\.?\d*\s*(%|％|億|兆|pp|倍|萬口|萬元)")
TRACE = re.compile(r"https?://|www\.|\.gov|\.tw|\.pdf|ISBN|第\s*\d+\s*條|辦法|條例|準則|要點|號令|函|報告|release|WIR|WEO|AI Index|Annual Report|COFER|實務慣例|慣例|待查|自算|live 實測|實測")
PAGE_GLOBS = ("skills/SK-*.md", "concepts/*.md", "entities/*.md", "summaries/*.md", "templates/*.md")

def frontmatter_sources(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return ""
    fm = m.group(1)
    out = []
    for mm in re.finditer(r"^\s*sources?:(.*?)(?=^[A-Za-z_]|\Z)", fm, re.S | re.M):
        out.append(mm.group(1))
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    files = []
    for pat in PAGE_GLOBS:
        files += [f for f in sorted(glob.glob(os.path.join(a.repo_root, pat))) if ".bak" not in f]
    if not files:
        print("❌ 掃到 0 頁（--repo-root 可能錯、或檔案缺失）— 護欄不得在空集合上通過")
        return 1
    viol = []
    for f in files:
        t = open(f, encoding="utf-8").read()
        body = re.sub(r"^---\n.*?\n---\n", "", t, flags=re.S)
        if not (AUTH.search(body) and QTY.search(body)):
            continue
        srcs = frontmatter_sources(t)
        if not TRACE.search(srcs):
            viol.append(os.path.relpath(f, a.repo_root))
    if a.json:
        print(json.dumps({"pages": len(files), "thin_source_pages": viol}, ensure_ascii=False, indent=1))
        return 1 if (a.strict and viol) else 0
    print("═" * 64)
    print(f"外部事實來源可追溯性（S3）— {len(files)} 頁")
    print("═" * 64)
    if not viol:
        print("✅ 所有引用外部權威＋量化主張的頁面，frontmatter 都有可追溯來源")
        return 0
    print(f"{'❌' if a.strict else '⚠️ '} {len(viol)} 頁引用外部權威／量化主張，但 frontmatter 無可追溯來源：")
    for v in viol:
        print(f"   - {v}")
    print("\n   合法補法（三選一）：① 補 URL／法規名／報告名 ② 明寫『實務慣例』 ③ 明寫『待查（YYYY-MM-DD）』")
    if a.strict:
        return 1
    print(f"\n   （warn 模式：不影響 exit code；待這 {len(viol)} 頁補完後改 --strict）")
    return 0

if __name__ == "__main__":
    sys.exit(main())
