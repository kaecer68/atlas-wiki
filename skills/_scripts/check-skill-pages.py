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
        "--min-l3-coverage", type=float,
        default=float(os.environ.get("ATLAS_WIKI_MIN_L3_COVERAGE", "90")),
        help="L3 覆蓋率門檻 %%（0 = 停用；預設 90）",
    )
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


def check_l3_coverage(skills_dir, min_pct):
    """L3 覆蓋率門檻（2026-09-27 kaecer 拍板: 由「可見度指標」升為 CI 門檻）。

    定義: `status: active` 的 SK 頁中，frontmatter 同時具備
    `l3_run_at` + `l3_run_by` + `l3_endpoints_probed` 的比例。
    低於門檻 ⇒ 失敗（避免「宣稱 active 卻沒有可驗證證據」的頁面繼續累積）。
    """
    files = sorted(glob.glob(os.path.join(skills_dir, "SK-*.md")))
    files = [f for f in files if ".bak" not in f]
    active, covered, missing = 0, 0, []
    for f in files:
        c = open(f, encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---", c, re.DOTALL)
        if not m:
            continue
        fm = m.group(1)
        if not re.search(r"^status:\s*active\s*$", fm, re.MULTILINE):
            continue
        active += 1
        if all(re.search(rf"^{k}:", fm, re.MULTILINE) for k in
               ("l3_run_at", "l3_run_by", "l3_endpoints_probed")):
            covered += 1
        else:
            missing.append(os.path.basename(f))
    pct = round(100.0 * covered / active, 1) if active else 100.0
    ok = (min_pct <= 0) or (pct >= min_pct)
    if not ok:
        print(f"❌ L3 覆蓋率 {pct}% < 門檻 {min_pct}%（{covered}/{active} active 頁具 l3_* 三欄）")
        for n in missing:
            print(f"   缺 L3: {n}")
    else:
        print(f"✅ L3 覆蓋率 {pct}%（{covered}/{active} active 頁具 l3_* 三欄；門檻 {min_pct}%）")
    return (0 if ok else len(missing) or 1), active, pct



def check_l3_grammar(skills_dir):
    """L3 證據**文法**檢查（S1，2026-09-27 kaecer 拍板；原本只檢查三個 key 是否存在）。

    每條 `l3_endpoints_probed` 必須符合下列之一：
      1. 含本地時戳 `YYYY-MM-DDTHH:MM[:SS]+08:00`（秒可省略；不得逼出假精度）；
      2. 以 `N/A` 開頭（明示本頁無 atlas 端點，例：純索引頁 SK-00）；
      3. 含 `時間未記`（**僅限** `l3_run_at` ≤ 2026-08-31 的 legacy 紀錄；新頁不得使用）。
    """
    files = sorted(glob.glob(os.path.join(skills_dir, "SK-*.md")))
    files = [f for f in files if ".bak" not in f]
    ts_re = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?\+08:00")
    bad = []
    for f in files:
        c = open(f, encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---", c, re.DOTALL)
        if not m:
            continue
        fm = m.group(1)
        run_at = re.search(r"^l3_run_at:\s*(\S+)", fm, re.MULTILINE)
        run_at = run_at.group(1) if run_at else ""
        legacy = bool(run_at) and run_at <= "2026-08-31"
        mm = re.search(r"^l3_endpoints_probed:\n((?:  - .*\n)+)", fm, re.MULTILINE)
        if not mm:
            continue
        for line in mm.group(1).strip().split("\n"):
            item = line.strip()[2:].strip()
            if ts_re.search(item):
                continue
            if item.startswith(("N/A", "'N/A", '"N/A')):
                continue
            if "時間未記" in item and legacy:
                continue
            bad.append((os.path.basename(f), item[:90]))
    if bad:
        print(f"❌ L3 證據文法：{len(bad)} 條不合格（缺 +08:00 時戳，或用了不合規的 legacy 標記）")
        for n, item in bad[:12]:
            print(f"   {n}: {item}")
        if len(bad) > 12:
            print(f"   … 另有 {len(bad) - 12} 條")
    else:
        print(f"✅ L3 證據文法：全部合格（{len(files)} 頁）")
    return (len(bad) or 0), len(files)


def check_body_tz(skills_dir):
    """SK 頁**內文**的 L3 探針時間必須是本地時區（S1 文法擴充，2026-09-28）。

    為什麼：第六條鐵律要求 `+08:00`；原 S1 文法只覆蓋 frontmatter 的 `l3_*` 欄位，
    內文證據表格與行內探針標記不受檢（2026-09-28 CIO 試跑發現 SK-38 實例）。

    只抓「我們自己的探針時間」兩種寫法：
      1. 證據表格列的時間欄：`| <http_code> | <ts>Z |`
      2. 行內探針標記：`（HH:MM[:SS]Z）`
    **不抓 API 回傳的資料值**（`snapshot_time=…Z`／`last_run …Z`）——那些要忠實反映來源。
    """
    tbl = re.compile(r"\|\s*\**\d{3}\**\s*\|\s*\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?Z\s*\|")
    mark = re.compile(r"（\d{2}:\d{2}(?::\d{2})?Z）")
    bad = []
    for f in sorted(glob.glob(os.path.join(skills_dir, "SK-*.md"))):
        text = open(f, encoding="utf-8").read()
        end = text.find("\n---", 3)
        body = text[end:] if end > 0 else text
        for line in body.split("\n"):
            if tbl.search(line) or mark.search(line):
                bad.append(f"{os.path.basename(f)}: {line.strip()[:70]}")
    return bad


def main():
    args = parse_args()
    skills_dir = args.skills_dir

    print("=" * 60)
    print("SK 頁 size + frontmatter 檢查")
    print("=" * 60)

    sz_bad, total = check_size(skills_dir)
    # S8 護欄牙齒（2026-09-27）：掃到 0 檔 = 檢查沒有在驗任何東西 ⇒ 失敗，不得靜默全綠
    if total == 0:
        print(f"❌ 掃到 0 個 SK 頁（skills_dir={skills_dir}）— 路徑錯或目錄空；不得靜默全綠")
        return 1
    if sz_bad == 0:
        print(f"✅ size: {total} 頁全部 ≤ {MAX_SIZE} bytes")
    else:
        print(f"❌ size: {sz_bad}/{total} 頁超 {MAX_SIZE} bytes")

    fm_bad, _ = check_frontmatter(skills_dir)
    if fm_bad == 0:
        print(f"✅ frontmatter: {total} 頁核心欄位齊全")
    else:
        print(f"❌ frontmatter: {fm_bad}/{total} 頁有缺欄")

    l3_bad, l3_active, l3_pct = check_l3_coverage(skills_dir, args.min_l3_coverage)
    gram_bad, _ = check_l3_grammar(skills_dir)
    tz_bad = check_body_tz(skills_dir)
    if tz_bad:
        print(f"❌ 內文 L3 探針時區: {len(tz_bad)} 條（應為 +08:00；API 資料值不受檢）")
        for b in tz_bad[:8]:
            print(f"   - {b}")
    else:
        print("✅ 內文 L3 探針時區: 全部 +08:00")
    yml_bad, _, have_yaml = check_frontmatter_yaml(skills_dir)
    mode = "PyYAML 實parse" if have_yaml else "fallback(未加引號 ': ' 偵測;PyYAML 未安裝)"
    if yml_bad == 0:
        print(f"✅ frontmatter YAML 合法: {total} 頁({mode})")
    else:
        print(f"❌ frontmatter YAML: {yml_bad}/{total} 頁不合法({mode})")

    print()
    if sz_bad == 0 and fm_bad == 0 and yml_bad == 0 and l3_bad == 0 and gram_bad == 0 and not tz_bad:
        print(f"✅ 全 {total} 頁合規")
        return 0
    print(f"❌ 共 {sz_bad + fm_bad + yml_bad + l3_bad + gram_bad + len(tz_bad)} 條違規(需修)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
