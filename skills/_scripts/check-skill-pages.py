#!/usr/bin/env python3
"""
check-skill-pages.py — 一次跑 SK 頁 size + frontmatter 兩項檢查
對位 _method.md §規範速查:
- 單頁 ≤ 9,000 bytes
- frontmatter 10 欄齊全

執行:
  python3 skills/_scripts/check-skill-pages.py [skills-dir]
  # CI: python3 skills/_scripts/check-skill-pages.py skills

退出碼:0 全綠 / 1 有違規
"""
import glob
import re
import sys
import argparse
import os

# T3 修補(2026-08-16):預設值跟著 repo 走,不綁 home(避免 CI 掃 0 檔假綠)
DEFAULT_SKILLS_DIR = os.environ.get("ATLAS_WIKI_SKILLS_DIR") or str(
    __import__("pathlib").Path(__file__).resolve().parents[1]
)
MAX_SIZE = 9000
REQUIRED_FM = [
    "title", "type", "source", "ingested_at", "status", "tier",
    "confidence", "atlas_go_relevance", "mcp_tools_used", "verification",
]


def parse_args():
    p = argparse.ArgumentParser(description="SK 頁 size + frontmatter 兩項檢查")
    p.add_argument(
        "--skills-dir",
        default=os.environ.get("ATLAS_WIKI_SKILLS_DIR", DEFAULT_SKILLS_DIR),
        help="skills 目錄(預設絕對路徑,CI 用相對路徑)",
    )
    return p.parse_args()


def check_size(skills_dir):
    files = sorted(glob.glob(os.path.join(skills_dir, "SK-*.md")))
    files = [f for f in files if ".bak" not in f]
    bad = []
    for f in files:
        size = len(open(f, "rb").read())
        if size > MAX_SIZE:
            bad.append((f, size))
    if bad:
        for f, s in bad:
            print(f"❌ {f}: {s} bytes > {MAX_SIZE}")
        return len(bad), len(files)
    return 0, len(files)


def check_frontmatter(skills_dir):
    files = sorted(glob.glob(os.path.join(skills_dir, "SK-*.md")))
    files = [f for f in files if ".bak" not in f]
    bad = []
    for f in files:
        c = open(f, encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---", c, re.DOTALL)
        if not m:
            bad.append((f, "no frontmatter"))
            continue
        fm = m.group(1)
        miss = [k for k in REQUIRED_FM if not re.search(rf"^{re.escape(k)}:", fm, re.MULTILINE)]
        if miss:
            bad.append((f, "缺: " + ",".join(miss)))
    if bad:
        for f, msg in bad:
            print(f"❌ {f}: {msg}")
        return len(bad), len(files)
    return 0, len(files)



def _unquoted_colon_lines(fm):
    """回傳含未加引號 `: ` 的 frontmatter 行（dependency-free fallback）。

    YAML 純量若含 ASCII 冒號+空格(`: `)、或以反引號開頭,必須加引號;否則整段
    frontmatter 不是合法 YAML(2026-09-27 實證:8 頁中招,含 3 頁完全無法解析)。
    """
    hits = []
    for i, line in enumerate(fm.split("\n"), 1):
        m = re.match(r"^([A-Za-z_][\w]*):\s(.*)$", line) or re.match(r"^(\s+- )(.*)$", line)
        if not m:
            continue
        val = m.group(2)
        if val[:1] in ('"', "'") or val[:1] in ("[", "{"):
            continue
        if ": " in val or val.startswith("`"):
            hits.append((i, line.strip()[:100]))
    return hits


def check_frontmatter_yaml(skills_dir):
    """frontmatter 必須是合法 YAML(2026-09-27 新增,對位 batch #1/#2 的實際缺陷)。

    有 PyYAML 時做真正的 parse;沒有時退回「未加引號 `: ` 偵測」——兩者都能抓到
    今天這批缺陷(未加引號的 verification/l3_endpoints_probed 值)。
    """
    files = sorted(glob.glob(os.path.join(skills_dir, "SK-*.md")))
    files = [f for f in files if ".bak" not in f]
    bad = []
    try:
        import yaml  # noqa
        have_yaml = True
    except Exception:
        have_yaml = False
    for f in files:
        c = open(f, encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---", c, re.DOTALL)
        if not m:
            continue
        fm = m.group(1)
        if have_yaml:
            try:
                import yaml
                yaml.safe_load(fm)
            except Exception as e:
                bad.append((f, f"YAML parse fail: {str(e).splitlines()[0][:70]}"))
                continue
        hits = _unquoted_colon_lines(fm)
        if hits:
            bad.append((f, f"{len(hits)} 行未加引號的 ': '(例: {hits[0][1]})"))
    if bad:
        for f, msg in bad:
            print(f"❌ {f}: {msg}")
        return len(bad), len(files), have_yaml
    return 0, len(files), have_yaml

def main():
    args = parse_args()
    skills_dir = args.skills_dir

    print("=" * 60)
    print("SK 頁 size + frontmatter 檢查")
    print("=" * 60)

    sz_bad, total = check_size(skills_dir)
    if sz_bad == 0:
        print(f"✅ size: {total} 頁全部 ≤ {MAX_SIZE} bytes")
    else:
        print(f"❌ size: {sz_bad}/{total} 頁超 {MAX_SIZE} bytes")

    fm_bad, _ = check_frontmatter(skills_dir)
    if fm_bad == 0:
        print(f"✅ frontmatter: {total} 頁核心欄位齊全")
    else:
        print(f"❌ frontmatter: {fm_bad}/{total} 頁有缺欄")

    yml_bad, _, have_yaml = check_frontmatter_yaml(skills_dir)
    mode = "PyYAML 實parse" if have_yaml else "fallback(未加引號 ': ' 偵測;PyYAML 未安裝)"
    if yml_bad == 0:
        print(f"✅ frontmatter YAML 合法: {total} 頁({mode})")
    else:
        print(f"❌ frontmatter YAML: {yml_bad}/{total} 頁不合法({mode})")

    print()
    if sz_bad == 0 and fm_bad == 0 and yml_bad == 0:
        print(f"✅ 全 {total} 頁合規")
        return 0
    print(f"❌ 共 {sz_bad + fm_bad + yml_bad} 條違規(需修)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
