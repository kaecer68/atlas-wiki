#!/usr/bin/env python3
"""
atlas-mcp 端點 audit 工具 — 自動掃描 109 端點 + 抓 Description

對位 SOUL §4.1 跨代理協作紀律:未來 atlas 端有問題時能快速 audit

執行:
  本地(預設絕對路徑):
    python3 ~/workspace/atlas-wiki/skills/_scripts/audit-atlas-endpoints.py
  CI(sparse-checkout atlas-go 後):
    python3 skills/_scripts/audit-atlas-endpoints.py --atlas-mcp-dir atlas-go/cmd/atlas-mcp/server
  或用環境變數覆寫:
    ATLAS_MCP_SERVER_DIR=path python3 skills/_scripts/audit-atlas-endpoints.py

2026-08-03 修:加 --atlas-mcp-dir 參數(CI 相對路徑可跑),預設路徑保留供本地直接呼叫。
"""
import os
import re
import glob
import argparse
from datetime import datetime
from collections import defaultdict

DEFAULT_ATLAS_MCP_DIR = os.path.expanduser("~/workspace/atlas/cmd/atlas-mcp/server")


def parse_args():
    parser = argparse.ArgumentParser(
        description="atlas-mcp 端點 audit 工具(掃描端點 + 抓 Description)"
    )
    parser.add_argument(
        "--atlas-mcp-dir",
        default=os.environ.get("ATLAS_MCP_SERVER_DIR", DEFAULT_ATLAS_MCP_DIR),
        help="atlas-mcp server 源碼目錄(CI checkout atlas-go 後用相對路徑,本地保留預設絕對路徑)",
    )
    return parser.parse_args()


def list_endpoints(atlas_mcp_dir):
    files = glob.glob(os.path.join(atlas_mcp_dir, "tools_*.go"))
    all_names = []
    for f in files:
        with open(f) as fh:
            c = fh.read()
        names = re.findall(r'Name:\s*"([a-z_]+)"', c)
        fname = os.path.basename(f).replace("tools_", "").replace(".go", "")
        for n in names:
            all_names.append((n, fname))
    seen = set()
    unique = []
    for n, f in all_names:
        if n not in seen:
            seen.add(n)
            unique.append((n, f))
    return sorted(unique, key=lambda x: x[0])


def get_endpoint_card(name, fname, atlas_mcp_dir):
    """從 tools_xxx.go 抓 Name + Description(autoDescOr 第二個 string)"""
    full = os.path.join(atlas_mcp_dir, f"tools_{fname}.go")
    if not os.path.exists(full):
        return "// 源碼未知"
    with open(full) as f:
        c = f.read()
    # 抓 autoDescOr("name", "desc") 模式
    pat = rf'autoDescOr\(\s*"{re.escape(name)}"\s*,\s*"([^"]+)"'
    m = re.search(pat, c)
    if m:
        return m.group(1)
    # 退而求其次:抓 Name 段後的 Description 任意 string
    pat2 = rf'Name:\s*"{re.escape(name)}"[^D]+?Description:\s*"?([A-Z][^"]+?)[",]'
    m2 = re.search(pat2, c, re.DOTALL)
    if m2:
        return m2.group(1)
    return "(無 Description)"


def main():
    args = parse_args()
    endpoints = list_endpoints(args.atlas_mcp_dir)
    print("=" * 70)
    print(f"atlas-mcp 端點 audit — {datetime.now().isoformat()}")
    print("=" * 70)
    print(f"\n總端點數: {len(endpoints)}\n")

    by_file = defaultdict(list)
    for n, f in endpoints:
        by_file[f].append(n)

    for f, names in sorted(by_file.items()):
        print(f"### tools_{f}.go ({len(names)} 端點)")
        for n in sorted(names):
            card = get_endpoint_card(n, f, args.atlas_mcp_dir)
            print(f"  - {n:38s} {card[:90]}")
        print()

    print("=" * 70)
    print(f"audit 完成 — {len(endpoints)} 端點已盤查")
    print("=" * 70)


if __name__ == "__main__":
    main()
