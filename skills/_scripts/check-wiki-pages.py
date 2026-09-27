#!/usr/bin/env python3
"""check-wiki-pages.py — 非 SK 類知識頁的 schema 護欄（S2，2026-09-27）

SSOT: `skills/_scripts/wiki-page-schema.json`（concepts／entities／summaries／templates／docs）。
SK 頁另有 `skill-page-schema.json` ＋ `check-skill-pages.py`，兩者欄位不同、不可混用。

對位審計（2026-09-27）：**54/94 頁**（concepts 22／entities 7／summaries 2／templates 22，不含 audit-report）
在此之前**沒有任何 schema 或護欄** —— 空的 concepts 頁只要列進 index.md 就過關。

用法:
  python3 skills/_scripts/check-wiki-pages.py [--repo-root .] [--strict] [--json]
  預設 **strict**（違規即 exit 1）；`--json` 供程式消費。
"""
import argparse, glob, json, os, re, sys
from collections import defaultdict

# 只有這些類別可宣告「本質上無 frontmatter」（避免任一類別靜默關掉檢查；2026-09-28 審查建議）
ALLOW_NO_FM_GROUPS = {"docs"}

def load(p):
    try: return open(p, encoding="utf-8").read()
    except Exception: return ""

def fm_of(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    return m.group(1) if m else None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    ap.add_argument("--strict", action="store_true", default=True)
    ap.add_argument("--no-strict", dest="strict", action="store_false")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    R = a.repo_root
    schema_path = os.path.join(R, "skills/_scripts/wiki-page-schema.json")
    if not os.path.isdir(R) or not os.path.isfile(schema_path):
        print(f"❌ 找不到 repo 或 schema（--repo-root={R}）— 護欄不得在空環境上通過")
        return 1
    schema = json.loads(load(schema_path))
    try:
        import yaml; HAS_YAML = True
    except Exception:
        HAS_YAML = False

    report = defaultdict(list); counts = {}
    for g, spec in schema["groups"].items():
        files = [f for f in sorted(glob.glob(os.path.join(R, spec["glob"]))) if ".bak" not in f]
        counts[g] = len(files)
        for f in files:
            name = os.path.relpath(f, R)
            text = load(f)
            size = len(text.encode())
            if size > spec["size_limit_bytes"]:
                report["size"].append(f"{name}: {size} > {spec['size_limit_bytes']}")
            fm = fm_of(text)
            if fm is None:
                if spec.get("allow_no_frontmatter") and g in ALLOW_NO_FM_GROUPS:
                    continue  # 例：docs/** 本質上無 frontmatter（2026-09-28）
                report["no_frontmatter"].append(name); continue
            if HAS_YAML:
                try:
                    d = yaml.safe_load(fm) or {}
                except Exception as e:
                    report["yaml_invalid"].append(f"{name}: {str(e).splitlines()[0][:60]}"); continue
            else:
                d = {}
                for k in re.findall(r"^([A-Za-z_][\w\-]*):", fm, re.M): d[k] = True
            missing = [k for k in spec["frontmatter_required"] if k not in d]
            if missing:
                report["missing_fields"].append(f"{name}: 缺 {','.join(missing)}")
            # created/updated 格式與順序
            c, u = d.get("created"), d.get("updated")
            pat = re.compile(r"^\d{4}-\d{2}-\d{2}$")
            if c and isinstance(c, str) and not pat.match(c):
                report["bad_date"].append(f"{name}: created={c!r}")
            if u and isinstance(u, str) and pat.match(u) and c and isinstance(c, str) and pat.match(c) and u < c:
                report["bad_date"].append(f"{name}: updated({u}) < created({c})")
            # contested ⇒ contradictions 非空
            if d.get("contested") is True:
                con = d.get("contradictions")
                if not con:
                    report["contested_without_contradictions"].append(name)
    # 入口/索引檔 size（2026-09-27：這類在 鐵律 6 有上限，但原本**沒有任何護欄**在檢查）
    ENTRY_LIMITS = {"AGENTS.md": 12500, "README.md": 9000, "index.md": 9000, "SCHEMA.md": 12000,
                    "skills/SK-00-skill-index.md": 9000, "skills/_consult-index.md": 9000,
                    "skills/_knowledge-router.md": 9000, "skills/_method.md": 9000}
    for rel, cap in ENTRY_LIMITS.items():
        fp = os.path.join(R, rel)
        if not os.path.exists(fp):
            continue
        sz = len(load(fp).encode())
        counts.setdefault("entry", 0)
        counts["entry"] += 1
        if sz > cap:
            report["entry_size"].append(f"{rel}: {sz} > {cap}")

    total = sum(v for k, v in counts.items() if k != "entry") + counts.get("entry", 0)
    if sum(v for k, v in counts.items() if k != "entry") == 0:
        print(f"❌ 掃到 0 頁（--repo-root={R} 可能錯）— 護欄不得在空集合上通過")
        return 1
    if a.json:
        print(json.dumps({"counts": counts, "violations": {k: v for k, v in report.items()}}, ensure_ascii=False, indent=1))
        return 0
    LABELS = {"no_frontmatter": "缺 frontmatter", "yaml_invalid": "YAML 不合法",
              "missing_fields": "缺必要欄位", "size": "超過 size 上限",
              "bad_date": "created/updated 日期異常",
              "contested_without_contradictions": "contested=true 但 contradictions 空",
              "entry_size": "入口/索引檔超過類別上限"}
    print("=" * 64)
    print(f"非 SK 類頁面 schema 檢查（S2）— {total} 頁 {'＋PyYAML' if HAS_YAML else '（無 PyYAML，僅鍵檢查）'}")
    print("=" * 64)
    bad = 0
    for k, label in LABELS.items():
        items = report.get(k, [])
        bad += len(items)
        print(f"{'✅' if not items else '❌'} {label}: {len(items)}")
        for it in items[:8]: print(f"    - {it}")
        if len(items) > 8: print(f"    … 另有 {len(items)-8} 條")
    print("\n" + "=" * 64)
    if bad == 0:
        print(f"✅ 全 {total} 頁符合 wiki-page-schema v{schema['version']}")
        return 0
    print(f"❌ 共 {bad} 條違規（schema: skills/_scripts/wiki-page-schema.json）")
    return 1 if a.strict else 0

if __name__ == "__main__":
    sys.exit(main())
