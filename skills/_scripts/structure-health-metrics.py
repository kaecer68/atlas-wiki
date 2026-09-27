#!/usr/bin/env python3
"""
structure-health-metrics.py — 結構健康度量測（反補丁機制 M7，2026-09-18 kaecer 拍板）

## 為什麼
反補丁機制（M1-M6）若沒有**可觀測量**，漂移只會在「撞上限」時才被發現（2026-09-06 事故即如此）。
本檔把結構健康度算成一份**可直接貼進結算**的 Markdown／JSON 區塊，接進既有結算流程
（`_self-audit.md` §6 結算、`hermes-governance-log.md`）。

## 指標（全部可重跑、可稽核；數字直接呼叫既有守衛的純函式，不另寫一套判準）
  1. SK 頁數
  2. 結構硬違規數（段名／段序／重複標準段／缺段／禁用標記）   ← 目標 0
  3. 禁用標記總數（別名段／補強備註／壓縮標籤／[INTERNAL]／行號指路）← 目標 0
  4. 「未消化」已結項數（warn 級）                        ← 目標 0
  5. 超 9000 bytes 頁數                                  ← 目標 0
  6. frontmatter 缺欄頁數                                ← 目標 0
  7. skills/ 未提交檔數＋最舊年齡（>48h 視為漂移）          ← 目標 0
  8. L3 覆蓋率：active 頁中具備三項 l3_* 欄位者（N/M ＋ %），並列出
     「active 但無 L3 證據」清單（claimed but unverified watch list）
     ※ 2026-09-27 kaecer 拍板：只做**可見度**，不設硬門檻、不進 verdict
       （37 頁合法頁從未跑過 L3；把 L3 變成硬 gate 會誤殺它們）。
       JSON key：active_pages / l3_covered_pages / l3_coverage_pct /
                 active_without_l3_pages（完整清單；Markdown 會截斷）

用法:
  python3 skills/_scripts/structure-health-metrics.py [--skills-dir skills] [--json]
輸出:--md（預設，可直接貼進結算）/ --json
退出碼:0 量測成功（即使指標不理想）；2 環境異常（掃不到頁面）
"""
import argparse
import importlib.util
import json
import os
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent

# 指標 8：L3 端點實測證據（三欄齊全才算「有證據」）
L3_FIELDS = ("l3_run_at", "l3_run_by", "l3_endpoints_probed")
# Markdown 的 watch list 最多列幾個名字（完整清單見 --json）
WATCHLIST_MD_LIMIT = 8
FM_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def _load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def l3_coverage(files):
    """指標 8：L3 覆蓋率（只做可見度,不設門檻）。

    回傳 (active 頁名, 具三欄 l3_* 的頁名, active 但無 L3 證據的頁名)。
    「有證據」= frontmatter 同時出現 l3_run_at / l3_run_by / l3_endpoints_probed。
    """
    active, covered, missing = [], [], []
    for f in files:
        m = FM_RE.match(Path(f).read_text(encoding="utf-8"))
        if not m:
            continue
        fm = m.group(1)
        st = re.search(r"^status:\s*(\S+)", fm, re.MULTILINE)
        if not st or st.group(1) != "active":
            continue
        name = os.path.basename(f)
        active.append(name)
        if all(re.search(rf"^{k}:", fm, re.MULTILINE) for k in L3_FIELDS):
            covered.append(name)
        else:
            missing.append(name)
    return active, covered, missing


def collect(skills_dir, repo_root):
    css = _load("css", "check-skill-structure.py")
    csp = _load("csp", "check-skill-pages.py")
    csw = _load("csw", "check-stale-worktree.py")

    schema = css.load_schema()
    files = sorted(f for f in csp.glob.glob(os.path.join(skills_dir, "SK-*.md")) if ".bak" not in f)
    if not files:
        return None

    hard = forbidden = done_items = 0
    done_pages = 0
    for f in files:
        r = css.analyse(f, schema)
        if r["renames"] or r["duplicated"] or r["missing"] or r["out_of_order"] or r["forbidden"]:
            hard += 1
        forbidden += len(r["forbidden"])
        page_done = 0
        for w in r["warn"]:
            if "已結項" in w:
                page_done += int("".join(ch for ch in w.split("含")[1].split("個")[0] if ch.isdigit()) or 0)
        if page_done:
            done_pages += 1
        done_items += page_done

    size_bad, _ = csp.check_size(skills_dir)
    fm_bad, _ = csp.check_frontmatter(skills_dir)

    paths = csw.git_status_paths(Path(repo_root).resolve())
    now = time.time()
    ages = []
    for p in paths:
        f = Path(repo_root) / p
        if f.exists():
            ages.append((now - f.stat().st_mtime) / 3600.0)
    oldest = max(ages) if ages else 0.0

    active, l3_covered, l3_missing = l3_coverage(files)

    return {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "pages": len(files),
        "structure_hard_violations": hard,
        "forbidden_markers": forbidden,
        "unconsumed_completed_items": done_items,
        "unconsumed_completed_pages": done_pages,
        "size_over_limit_pages": size_bad,
        "frontmatter_incomplete_pages": fm_bad,
        "uncommitted_skill_files": len(paths),
        "oldest_uncommitted_hours": round(oldest, 1),
        "active_pages": len(active),
        "l3_covered_pages": len(l3_covered),
        "l3_coverage_pct": round(100.0 * len(l3_covered) / len(active), 1) if active else 0.0,
        "active_without_l3_pages": l3_missing,
    }


def l3_md_lines(m):
    """指標 8 的 Markdown 兩行（覆蓋率＋watch list；watch list 過長則截斷）。"""
    missing = m["active_without_l3_pages"]
    lines = [
        f"- L3 覆蓋率：{m['l3_covered_pages']}/{m['active_pages']}"
        f"（{m['l3_coverage_pct']}%｜active 頁具 l3_run_at／l3_run_by／l3_endpoints_probed；可見度指標，非門檻）"
    ]
    if not missing:
        lines.append("- active 但無 L3 證據（claimed but unverified）：0 頁")
        return lines
    shown = "、".join(n[:-3] if n.endswith(".md") else n for n in missing[:WATCHLIST_MD_LIMIT])
    tail = f"…（餘 {len(missing) - WATCHLIST_MD_LIMIT} 頁見 --json）" if len(missing) > WATCHLIST_MD_LIMIT else ""
    lines.append(f"- active 但無 L3 證據（claimed but unverified）：{len(missing)} 頁｜{shown}{tail}")
    return lines


def verdict(m):
    """四項目標指標（皆應為 0）。"""
    zero_targets = ["structure_hard_violations", "forbidden_markers", "unconsumed_completed_items",
                    "size_over_limit_pages", "frontmatter_incomplete_pages"]
    bad = [k for k in zero_targets if m[k] != 0]
    stale = m["oldest_uncommitted_hours"] > 48
    return ("PASS" if not bad and not stale else "DRIFT"), bad, stale


def main():
    ap = argparse.ArgumentParser(description="結構健康度量測（M7）")
    ap.add_argument("--skills-dir", default="skills")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    m = collect(args.skills_dir, args.repo_root)
    if m is None:
        print("⚠️  掃到 0 個 SK 頁——請確認 --skills-dir（不得假綠）")
        return 2
    v, bad, stale = verdict(m)

    if args.json:
        print(json.dumps({**m, "verdict": v}, ensure_ascii=False, indent=2))
        return 0

    print(f"### 結構健康度（{m['generated_at']}）— **{v}**")
    print()
    print(f"- 頁數：{m['pages']}")
    print(f"- 結構硬違規：{m['structure_hard_violations']}（目標 0）")
    print(f"- 禁用標記（補丁痕跡）：{m['forbidden_markers']}（目標 0）")
    print(f"- 未消化含已結項：{m['unconsumed_completed_items']} 項（跨 {m['unconsumed_completed_pages']} 頁；目標 0）")
    print(f"- 超 9000 bytes 頁數：{m['size_over_limit_pages']}（目標 0）")
    print(f"- frontmatter 缺欄頁數：{m['frontmatter_incomplete_pages']}（目標 0）")
    print(f"- skills/ 未提交：{m['uncommitted_skill_files']} 檔，最舊 {m['oldest_uncommitted_hours']}h（目標：0 檔 >48h）")
    for line in l3_md_lines(m):
        print(line)
    if v != "PASS":
        print()
        print(f"⚠️ 漂移項：{'、'.join(bad) if bad else ''}{'｜未提交超過 48h' if stale else ''}")
        print("   依 `_method.md` 第九條：為通過檢查而做的變更須同 PR 收尾，或於 `_inbox.md` 立待辦（根因＋期限）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
