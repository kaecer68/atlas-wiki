#!/usr/bin/env python3
"""check-inbox-room.py — 顯示 `skills/_inbox.md` 兩區剩餘位元（第七條 v1.1，2026-09-28）

為什麼：`_inbox.md` 總量 12,000 B 且分兩區（active ≤8,000／已結案 ≤4,000）。
Agent 在 append 待辦前應該先知道「還塞不塞得下」——這支是**寫入前的量尺**；
預算本身的強制由 `check-wiki-pages.py` 負責（CI 紅燈）。

用法: python3 skills/_scripts/check-inbox-room.py [--repo-root .] [--json]
  超出預算或缺區標題 ⇒ exit 1；否則 exit 0。
"""
import argparse, json, os, sys

CAP_TOTAL, CAP_ACTIVE, CAP_CLOSED = 12000, 8000, 4000
H_ACTIVE, H_CLOSED = "## 待辦（active", "## 已結案（近期"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    path = os.path.join(a.repo_root, "skills", "_inbox.md")
    if not os.path.isfile(path):
        print(f"❌ 找不到 {path}")
        return 1
    text = open(path, encoding="utf-8").read()
    total = len(text.encode())
    if H_ACTIVE not in text or H_CLOSED not in text:
        print(f"❌ 缺區標題（需要 `{H_ACTIVE}…` 與 `{H_CLOSED}…`）⇒ 見 `_method.md` 第七條 v1.1")
        return 1
    ic = text.index(H_CLOSED)
    active, closed = len(text[:ic].encode()), len(text[ic:].encode())
    res = {
        "active": {"bytes": active, "cap": CAP_ACTIVE, "room": CAP_ACTIVE - active},
        "closed": {"bytes": closed, "cap": CAP_CLOSED, "room": CAP_CLOSED - closed},
        "total": {"bytes": total, "cap": CAP_TOTAL, "room": CAP_TOTAL - total},
    }
    over = [k for k, v in res.items() if v["room"] < 0]
    if a.json:
        print(json.dumps({"over": over, **res}, ensure_ascii=False, indent=1))
        return 1 if over else 0
    print("═" * 56)
    print("skills/_inbox.md 兩區剩餘位元（第七條 v1.1）")
    print("═" * 56)
    for k, label in (("active", "待辦（active）"), ("closed", "已結案（近期）"), ("total", "合計")):
        v = res[k]
        flag = "❌" if v["room"] < 0 else "✅"
        print(f"  {flag} {label:16s} {v['bytes']:6d} / {v['cap']:6d} B    剩 {v['room']:6d} B")
    if over:
        print("\n❌ 超出預算 — 依第七條 v1.1：先移最舊已結案條目到 `_inbox_archive.md` 再 append。")
        return 1
    print("\n✅ 兩區皆有餘裕，可直接 append。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
