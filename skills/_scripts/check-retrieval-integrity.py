#!/usr/bin/env python3
"""check-retrieval-integrity.py — 檢索性完整性（S5，2026-09-27）

回答一個問題：**agent 找得到這頁嗎？** 檢查三件事（皆以「知識頁」為對象）：

  1. **載入條件**：frontmatter 有 `description:`（或內文有明寫「何時載入」）——目前 0/94 頁有。
  2. **索引歸屬**：SK 頁 → `skills/SK-00-skill-index.md`；`templates/trigger-*.md` → `README.md`；
     `concepts|entities|summaries/*.md` → `index.md`。
  3. **反向連結**：至少一條來自**其他頁**的 `[[...]]`（不可是 orphan）。

用法:
  python3 skills/_scripts/check-retrieval-integrity.py [--repo-root .] [--strict] [--json]
  預設 **warn 模式**（永遠 exit 0，只報告）；`--strict` 才以違規數非零結束。
  理由：S5 是 2026-09-27 才新增的標準，內容需要時間補；先建基線、再收斂、最後才升硬門檻。
"""
import argparse
import glob
import json
import os
import re
from collections import defaultdict

def load(p):
    try:
        return open(p, encoding="utf-8").read()
    except Exception:
        return ""

def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    return m.group(1) if m else ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    R = args.repo_root

    def pages(pattern, skip_bak=True):
        fs = sorted(glob.glob(os.path.join(R, pattern)))
        return [f for f in fs if not (skip_bak and ".bak" in f)]

    groups = {
        "skills": (pages("skills/SK-*.md"), os.path.join(R, "skills/SK-00-skill-index.md")),
        "templates": (pages("templates/trigger-*.md"), os.path.join(R, "README.md")),
        "concepts": (pages("concepts/*.md"), os.path.join(R, "index.md")),
        "entities": (pages("entities/*.md"), os.path.join(R, "index.md")),
        "summaries": (pages("summaries/*.md"), os.path.join(R, "index.md")),
    }

    # 全站反向連結來源（所有知識頁的 [[...]]）
    inbound = defaultdict(set)
    for g, (files, _) in groups.items():
        for f in files:
            slug = os.path.basename(f)[:-3]
            for m in re.finditer(r"\[\[([^\]\|#]+)", load(f)):
                tgt = m.group(1).strip().split("|")[0].split("#")[0].strip()
                inbound[tgt.rsplit("/", 1)[-1].replace(".md", "")].add(slug)
                inbound[tgt.replace(".md", "")].add(slug)

    report = {"missing_description": [], "missing_index": [], "orphan": [], "counts": {}}
    for g, (files, idx_path) in groups.items():
        idx = load(idx_path)
        for f in files:
            name = os.path.basename(f)
            slug = name[:-3]
            text = load(f)
            fm = frontmatter(text)
            # 1) 載入條件
            if not re.search(r"^description:", fm, re.MULTILINE) and not re.search(r"何時載入|載入條件|when to load", text, re.I):
                report["missing_description"].append(f"{g}/{name}")
            # 2) 索引歸屬（SK/trigger 允許用編號或名稱 token 命中）
            token = re.match(r"(SK-\d{2}|trigger-[a-z0-9\-]+)", slug)
            keys = [slug, f"{g}/{slug}"] + ([token.group(1)] if token else [])
            if not any(k in idx for k in keys):
                report["missing_index"].append(f"{g}/{name}")
            # 3) 反向連結（僅供參考：SK 頁靠 SK-00 表格索引，不以 wikilink 為唯一可達途徑）
            if not {s for s in inbound.get(slug, set()) if s != slug}:
                report["orphan"].append(f"{g}/{name}")
        report["counts"][g] = len(files)

    # 4) 四個入口表面可達性（index.md／SK-00／_consult-index／_knowledge-router）
    ENTRY = ["index.md", "README.md", "skills/SK-00-skill-index.md", "skills/_consult-index.md", "skills/_knowledge-router.md"]
    entry_text = "\n".join(load(os.path.join(R, e)) for e in ENTRY if os.path.exists(os.path.join(R, e)))
    unreachable = []
    for g, (files, _) in groups.items():
        for f in files:
            name = os.path.basename(f)
            slug = name[:-3]
            token = re.match(r"(SK-\d{2}|trigger-[a-z0-9\-]+)", slug)
            keys = [slug, f"{g}/{slug}"] + ([token.group(1)] if token else [])
            if not any(k in entry_text for k in keys):
                unreachable.append(f"{g}/{name}")
    report["unreachable_from_entry_surfaces"] = unreachable

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1)); return 0
    total = sum(report["counts"].values())
    print("═" * 60)
    print(f"檢索性完整性（S5）— 知識頁 {total} 頁")
    print("═" * 60)
    for key, label in (("missing_description", "缺載入條件（description／何時載入）"),
                       ("missing_index", "未登錄於所屬索引"),
                       ("unreachable_from_entry_surfaces", "入口表面到不了（index.md／README／SK-00／_consult-index／_knowledge-router）"),
                       ("orphan", "[參考] 無反向 wikilink（仍可由索引到達）")):
        items = report[key]
        print(f"\n{label}: {len(items)}/{total}")
        for it in items[:10]:
            print(f"  - {it}")
        if len(items) > 10:
            print(f"  … 另有 {len(items) - 10} 頁")
    bad = (len(report["missing_description"]) + len(report["missing_index"])
           + len(report["unreachable_from_entry_surfaces"]))
    print(f"\n合計 {bad} 條（warn 模式: 不影響 exit code）")
    return 1 if (args.strict and bad) else 0

if __name__ == "__main__":
    raise SystemExit(main())
