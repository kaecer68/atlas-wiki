#!/usr/bin/env python3
"""
check-stale-worktree.py — 未提交內容偵測（反補丁機制 M5，2026-09-18 kaecer 拍板）

為什麼需要：2026-09-06 由 cron 產生的 alias 補丁段，**躺在工作區 12 天沒被發現**——
同時造成 (a) 未經審查、(b) 後續 session 在髒樹上繼續疊補丁、(c) 兩頁撞 9000 bytes 上限卻沒人處理。
為通過檢查器而做的變更，必須**同一 PR 收尾**或**立待辦**（見 `_method.md` 第九條）。

本檢查掃 `skills/` 的未提交（含未追蹤）檔案，任一檔的 mtime 早於 --hours（預設 48）即告警。
CI 看不到使用者工作區，故本檢查是**本機／session 開頭**用的（`make check-stale`）。

用法:
  python3 skills/_scripts/check-stale-worktree.py [--hours 48] [--strict]
退出碼:0 無告警（或未 --strict）/ 1 有超過門檻的未提交內容（--strict）
"""
import argparse
import os
import subprocess
import sys
import time
from pathlib import Path


def git_status_paths(repo_root):
    out = subprocess.run(["git", "-C", str(repo_root), "status", "--porcelain", "skills/"],
                         capture_output=True, text=True).stdout
    paths = []
    for line in out.splitlines():
        if not line.strip():
            continue
        p = line[3:].strip()
        if " -> " in p:
            p = p.split(" -> ")[-1]
        paths.append(p.strip('"'))
    return paths


def main():
    ap = argparse.ArgumentParser(description="未提交內容偵測（M5）")
    ap.add_argument("--hours", type=float, default=48.0)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--repo-root", default=".")
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    paths = git_status_paths(root)
    if not paths:
        print("✅ skills/ 無未提交內容")
        return 0

    now = time.time()
    stale = []
    fresh = []
    for p in paths:
        f = root / p
        if not f.exists():
            stale.append((p, "（檔案已刪除/不存在）"))
            continue
        age_h = (now - f.stat().st_mtime) / 3600.0
        (stale if age_h > args.hours else fresh).append((p, f"{age_h:.1f}h"))

    print(f"skills/ 未提交：{len(paths)} 檔（門檻 {args.hours}h）")
    for p, age in fresh:
        print(f"  ⏳ {age:>8}  {p}")
    for p, age in stale:
        print(f"  ❌ {age:>8}  {p}")
    if stale:
        print()
        print(f"❌ {len(stale)} 檔未提交超過 {args.hours}h——依 `_method.md` 第九條：")
        print("   (a) 同一 PR 收尾後 commit，或 (b) 在 skills/_inbox.md 立待辦（根因＋期限）。")
        print("   不得讓補丁留在工作區（2026-09-06 事故：補丁躺 12 天，兩頁撞 9000 bytes 上限）。")
        return 1 if args.strict else 0
    print("✅ 未提交內容皆在門檻內")
    return 0


if __name__ == "__main__":
    sys.exit(main())
