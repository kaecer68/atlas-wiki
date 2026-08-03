#!/usr/bin/env python3
"""
第 5 條鐵律 enforcement 工具 - 自動驗證 wiki 內快照值 timestamp
對位 _method.md 第五條鐵律:任何隨時間變動的數字引用必附 timestamp + 端點名稱

執行:
  python3 /Users/kaecer/workspace/atlas-wiki/skills/_scripts/validate-timestamp-rule.py

結果:
  0 違規 = 全 33 頁合規
  N 違規 = 列出失真位置

Author: Hermes agent (2026-08-03 v5.7 A 路徑 #3)
"""
import os
import re
import glob
import sys
import argparse

DEFAULT_SKILLS_DIR = "/Users/kaecer/workspace/atlas-wiki/skills"


def parse_args():
    parser = argparse.ArgumentParser(
        description="第 5 條鐵律 enforcement 工具(快照值必附 timestamp)"
    )
    parser.add_argument(
        "--skills-dir",
        default=os.environ.get("ATLAS_WIKI_SKILLS_DIR", DEFAULT_SKILLS_DIR),
        help="skills 目錄路徑(CI 用相對路徑,本地保留預設絕對路徑)",
    )
    return parser.parse_args()
# 隨時間變動的數字模式
TIMESTAMP_SENSITIVE_PATTERNS = [
    re.compile(r"session_count\s*=\s*\d+"),
    re.compile(r"sharpe[_\w]*\s*=\s*[\-\d\.]+"),
    re.compile(r"max_drawdown[_\w]*\s*=\s*[\-\d\.]+"),
    re.compile(r"var_9[59]\s*=\s*[\-\d\.]+"),
    re.compile(r"drawdown[_\w]*\s*=\s*[\-\d\.]+"),
    re.compile(r"volatility[_\w]*\s*=\s*[\-\d\.]+"),
]
# timestamp 關鍵字
TIMESTAMP_KEYWORDS = re.compile(
    r"2026-08|2026-07|2026-06|timestamp|snapshot|結算|實跑.*20"
)
# 例外:公式定義(line 開頭為 `sharpe_ratio = ...` 是公式不是快照)
FORMULA_PREFIX = re.compile(r"^\s*[\-\*\u2022]\s*`[a-z_0-9]+`")


def check_file(filepath):
    """回傳 (violations_count, violations_list)"""
    with open(filepath) as fh:
        content = fh.read()
    parts = content.split("---", 2)
    if len(parts) < 3:
        return 0, []
    body = parts[2]
    in_real_run = False
    violations = []
    for i, line in enumerate(body.split("\n"), 1):
        # 偵測進入「實跑/驗證」段(中英文都偵測)
        if re.search(r"verification|實跑|真實數據|確認|結算 snapshot|##\s*驗證方式|##\s*驗證", line):
            in_real_run = True
        # 跳過公式定義
        if FORMULA_PREFIX.match(line):
            continue
        # 跳過描述性「可能/待驗/過低/應改/可能正常/可能低估」字眼
        if re.search(r"可能|描述|定義|待驗|過低|應改|低估|可能正常|可能低估|可能問題", line):
            continue
        # 找實跑數字
        for pattern in TIMESTAMP_SENSITIVE_PATTERNS:
            if pattern.search(line):
                if in_real_run and not TIMESTAMP_KEYWORDS.search(line):
                    violations.append((i, line.strip()[:150]))
                break
    return len(violations), violations


def main():
    args = parse_args()
    files = sorted(glob.glob(os.path.join(args.skills_dir, "SK-*.md")))
    files = [f for f in files if ".bak" not in f]
    total = 0
    print("=" * 60)
    print("第 5 條鐵律自動驗證(快照值必附 timestamp)")
    print("=" * 60)
    for f in files:
        name = os.path.basename(f)
        count, violations = check_file(f)
        if count > 0:
            print(f"\n  ❌ {name}: {count} 條違規")
            for i, line in violations:
                print(f"    line {i}: {line}")
            total += count
    print()
    if total == 0:
        print(f"✅ 全 {len(files)} 頁第 5 條鐵律合規")
        return 0
    else:
        print(f"❌ 共 {total} 條違規(需修)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
