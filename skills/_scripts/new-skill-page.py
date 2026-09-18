#!/usr/bin/env python3
"""
new-skill-page.py — SK 頁骨架產生器（反補丁機制 M6，2026-09-18 kaecer 拍板）

為什麼需要：手寫標題最容易寫成 `## [INTERNAL] …` 或 `## §1 …` 這類**非標準段名**；
一旦段名不符，後續檢查器抓不到，就會有人用「加別名空殼段」補丁（2026-09-06 事故型態）。
本產生器直接輸出**合規骨架**（段名/段序取自 `skill-page-schema.json`），讓正確做法比補丁省力。

用法:
  python3 skills/_scripts/new-skill-page.py --id SK-37 --title "..." [--slug 描述] [--out-dir skills] [--print]
"""
import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA_PATH = HERE / "skill-page-schema.json"


def main():
    ap = argparse.ArgumentParser(description="SK 頁骨架產生器（M6）")
    ap.add_argument("--id", required=True, help="SK 編號，如 SK-37")
    ap.add_argument("--title", required=True)
    ap.add_argument("--slug", default="<slug>", help="檔名描述段（小寫連字號）")
    ap.add_argument("--out-dir", default="skills")
    ap.add_argument("--print", dest="to_stdout", action="store_true")
    args = ap.parse_args()

    schema = json.load(open(SCHEMA_PATH, encoding="utf-8"))
    today = date.today().isoformat()
    fm_keys = schema["frontmatter_required"]
    fm_values = {
        "title": args.title,
        "type": "skill-inbound",
        "source": "~/workspace/Fin-Skills/Fin-Skills.md",
        "ingested_at": today,
        "status": "draft",
        "tier": "T3",
        "confidence": "low",
        "atlas_go_relevance": "high",
        "mcp_tools_used": "[]",
        "verification": "L3 端點未跑 = draft（鐵律三：不裝完成）",
    }
    fm = "\n".join(f'{k}: {fm_values.get(k, "<待填>")}' for k in fm_keys)
    hints = {
        "一句話定位": "一句話定位 + 重要結論 + 讀者分流（散戶讀 §散戶解讀；開發者讀 §atlas 對位）",
        "論文版概念": "忠實還原 Fin-Skills 原文（不搬運,翻譯）：輸入/動作/輸出/預設 + 論文未提但實務重要",
        "atlas 對位": "對位表（論文概念 | atlas 對位 | 工具）+ 論文 vs atlas 差異 + 沒有對位的部分（替代路徑）",
        "散戶解讀": "GROW+ 引用點；若無原生對位，寫替代路徑 SOP（並註明「不是嚴格 X，是最接近的實務近似」）",
        "驗證方式": "L3 端點實跑（附 timestamp 與端點名；鐵律五）；未跑就維持 draft",
        "未消化": "只放**未結**項（- [ ]）；已結項的精華落對位/驗證段，敘事屬歷史（不進 SK 頁）",
    }
    body = "\n\n".join(f"## {s['key']}\n\n<!-- {hints[s['key']]} -->\n" for s in schema["canonical_sections"])
    out = f"---\n{fm}\n---\n\n{body}"
    if args.to_stdout:
        print(out)
        return 0
    path = Path(args.out_dir) / f"{args.id}-{args.slug}.md"
    if path.exists():
        print(f"❌ {path} 已存在，不覆寫")
        return 1
    path.write_text(out, encoding="utf-8")
    print(f"✅ 已產生合規骨架 {path}（{len(out.encode())} bytes）")
    print("   段名/段序取自 skill-page-schema.json；完成後跑 make check-skill-structure 自查")
    return 0


if __name__ == "__main__":
    sys.exit(main())
