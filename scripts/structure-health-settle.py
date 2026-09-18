#!/usr/bin/env python3
"""
structure-health-settle.py — 把結構健康度**自動接進結算**（M7 常態化，2026-09-18 kaecer 拍板）

## 為什麼
`make structure-metrics` 只在你記得跑時才有用；漂移會再次靜默累積（2026-09-06 事故：補丁躺 12 天）。
本檔把量測結果**追加**進結算檔，讓每次結算都看得到，不必靠人記得。

## 寫到哪裡（都不改 hermes 的結算腳本，純加法）
1. `skills/_structure-health-log.md`（本檔自建、append-only、gitignored）— 每次一筆
2. `skills/_self-audit.md` 尾端（若存在）— 追加同一筆（該檔為跨 session 審計日誌，本 repo 既有結算落點；gitignored）
   ※ 只在檔案已存在時追加，不建立也不覆寫 hermes 的結算流程

## 用法
  python3 scripts/structure-health-settle.py            # 追加一筆
  python3 scripts/structure-health-settle.py --dry-run  # 只印不寫
退出碼：0（PASS 或 DRIFT 都寫入）；2 環境異常（掃不到 SK 頁）
"""
import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "skills" / "_structure-health-log.md"
SELF_AUDIT = ROOT / "skills" / "_self-audit.md"


def run_metrics():
    out = subprocess.run(
        [sys.executable, str(ROOT / "skills" / "_scripts" / "structure-health-metrics.py"), "--skills-dir", "skills"],
        cwd=ROOT, capture_output=True, text=True)
    return out.returncode, out.stdout.strip()


def main():
    ap = argparse.ArgumentParser(description="結構健康度 → 結算（M7 常態化）")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    rc, block = run_metrics()
    if rc != 0 or not block:
        print("⚠️ 量測失敗（未寫入結算）")
        return 2

    stamp = dt.datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
    entry = f"\n## {stamp} 結構健康度（自動，structure-health-settle.py）\n\n{block}\n"
    if args.dry_run:
        print(entry)
        return 0

    if not LOG.exists():
        LOG.write_text("# 結構健康度日誌（自動 append；對位 `_method.md` 第九條 M7）\n", encoding="utf-8")
    with LOG.open("a", encoding="utf-8") as f:
        f.write(entry)
    print(f"✅ 已寫入 {LOG.relative_to(ROOT)}")

    if SELF_AUDIT.exists():
        with SELF_AUDIT.open("a", encoding="utf-8") as f:
            f.write(entry)
        print(f"✅ 已追加至 {SELF_AUDIT.relative_to(ROOT)}（結算落點）")
    else:
        print("ℹ️  找不到 skills/_self-audit.md → 只寫本檔日誌")
    return 0


if __name__ == "__main__":
    sys.exit(main())
