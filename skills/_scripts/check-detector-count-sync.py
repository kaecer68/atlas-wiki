#!/usr/bin/env python3
"""check-detector-count-sync.py — wiki 的 detector 數與 atlas-go 權威值對齊（2026-09-27）

為什麼需要：atlas-go 有守門測試把 detector 數釘住（`internal/narrative/detector_count_gate_test.go`
的 `documentedDetectorCount`），但 **wiki 是另一個 repo，那個閘門掃不到它** ⇒ 下游會漂移
（2026-09-27 實例：wiki 兩處仍寫 24，權威值已是 29）。

權威值解析順序（取不到就**失敗**，不得靜默放行）：
  1. `<atlas-go>/internal/narrative/detector_count_gate_test.go` 的 `documentedDetectorCount = N`
  2. 退回 `<atlas-go>/internal/narrative/detector_impls.go` 的 `MustRegister(` 出現次數
然後掃 wiki 的知識頁，找出所有「N 個 template trigger detectors」型敘述並比對。

用法:
  python3 skills/_scripts/check-detector-count-sync.py [--repo-root .] [--atlas-go-dir ~/workspace/atlas]
  exit 0 = 對齊（或 wiki 沒有此數字的主張）；exit 1 = 不一致／無法解析權威值
"""
import argparse, glob, os, re, sys

CLAIM_RE = re.compile(r"(\d+)\s*\**\s*個\s*\**\s*template trigger detectors")

def authority(atlas_go_dir):
    """回傳 (value, source_desc) 或 (None, reason)"""
    gate = os.path.join(atlas_go_dir, "internal/narrative/detector_count_gate_test.go")
    if os.path.exists(gate):
        t = open(gate, encoding="utf-8").read()
        m = re.search(r"documentedDetectorCount\s*=\s*(\d+)", t)
        if m:
            return int(m.group(1)), "detector_count_gate_test.go documentedDetectorCount"
        return None, f"{gate} 存在但找不到 documentedDetectorCount"
    impl = os.path.join(atlas_go_dir, "internal/narrative/detector_impls.go")
    if os.path.exists(impl):
        n = open(impl, encoding="utf-8").read().count("MustRegister(")
        if n:
            return n, f"detector_impls.go MustRegister( 計數（gate test 不在本 checkout）"
        return None, f"{impl} 存在但 0 個 MustRegister("
    return None, f"找不到 atlas-go 來源（{atlas_go_dir}/internal/narrative）"

def wiki_claims(root):
    out = []
    for pat in ("skills/SK-*.md", "concepts/*.md", "entities/*.md", "summaries/*.md", "templates/*.md"):
        for f in sorted(glob.glob(os.path.join(root, pat))):
            if ".bak" in f:
                continue
            for i, line in enumerate(open(f, encoding="utf-8").read().split("\n"), 1):
                for m in CLAIM_RE.finditer(line):
                    out.append((os.path.relpath(f, root), i, int(m.group(1)), line.strip()[:110]))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    ap.add_argument("--atlas-go-dir", default=os.path.expanduser("~/workspace/atlas"))
    a = ap.parse_args()

    val, src = authority(a.atlas_go_dir)
    claims = wiki_claims(a.repo_root)
    print("═" * 64)
    print("detector 數對齊檢查（wiki ↔ atlas-go）")
    print("═" * 64)
    if val is None:
        print(f"❌ 無法解析 atlas-go 權威值：{src}")
        print("   （照 S8 原則：解析不到不得靜默放行）")
        return 1
    print(f"權威值 = {val}（來源：{src}）")
    print(f"wiki 主張 = {len(claims)} 處")
    bad = [c for c in claims if c[2] != val]
    for rel, ln, n, text in claims:
        flag = "✅" if n == val else "❌"
        print(f"  {flag} {rel}:{ln} → {n} ｜ {text}")
    if not claims:
        print("❌ wiki 掃到 0 處 detector 數敘述（--repo-root 可能錯、或敘述被移除）")
        print("   （S8 原則：掃 0 檔即失敗，不得靜默放行）")
        return 1
    if bad:
        print(f"\n❌ {len(bad)} 處與權威值 {val} 不一致 ⇒ 請同步（數值由 atlas-go registry 決定）")
        return 1
    print(f"\n✅ 全部 {len(claims)} 處與 atlas-go 權威值一致（{val}）")
    return 0

if __name__ == "__main__":
    sys.exit(main())
