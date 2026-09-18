#!/usr/bin/env python3
"""
check-skill-structure.py — SK 頁**結構**守衛（反補丁機制 M2/M2′，2026-09-18 kaecer 拍板）

為什麼需要（2026-09-06 事故）：標準 6 段名被寫成 `## [INTERNAL] …`／`## §1…§6` 後，
覆蓋率檢查 grep `^## <標準段名>` 抓不到 → cron **追加別名空殼段**去滿足檢查器（+923/+956 bytes），
兩頁因此撞 9000 bytes 上限，且補丁躺在工作區 12 天沒人發現。

本守衛的三個設計原則：
  1. 讀 SSOT `skill-page-schema.json`（段名/段序/補充段上限/禁用標記），**不自行發明判準**。
  2. 段名比對採**正規化**（去 `§N`、`[INTERNAL]`、括號註記），使「正名」成為正解，而不是加空殼。
  3. 失敗時輸出**最小重構處方（rename plan）**：明確指出哪一行標題改成什麼、哪些段要刪/要搬，
     讓「正確做法」比「貼補丁」更省力（M2′）。

執行:
  python3 skills/_scripts/check-skill-structure.py [--skills-dir skills] [--plan] [--strict]
    --plan    只印最小重構處方（不視為違規）
    --strict  把 warn 級規則（未消化含已結項）也當違規

退出碼:0 綠 / 1 有硬違規
"""
import argparse
import glob
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA_PATH = HERE / "skill-page-schema.json"


def load_schema():
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


def norm_heading(text):
    """標題正規化：去 `§N`、`[INTERNAL]`/`[ARCHIVED]` 等方括號前綴、數字前綴、括號註記、`+ ...` 尾巴。"""
    t = text.strip()
    t = re.sub(r"^\[[A-Z]+\]\s*", "", t)          # [INTERNAL] / [ARCHIVED]
    t = re.sub(r"^§\s*\d+(?:\.\d+)?\s*", "", t)     # §1 / §3.5
    t = re.split(r"[（(]", t)[0]                     # 括號註記
    t = re.split(r"\s*[+＋]\s*", t)[0]               # 「一句話定位 + 讀者分流」
    return t.strip().rstrip("：: ")


def canonical_for(heading_text, schema):
    """段名比對：標準段名可用前綴（吃「+ 讀者分流」這類尾巴）；別名**只做完全相等**。

    為什麼別名不 prefix（2026-09-18 實測）：`散戶` 這類短別名用 prefix 會把
    `## 散戶稅後淨報酬三塊` 誤判成「散戶解讀」的重複段（SK-19 假陽性）。
    """
    n = norm_heading(heading_text)
    for sec in schema["canonical_sections"]:
        if n == sec["key"] or n.startswith(sec["key"]):
            return sec["key"]
    for sec in schema["canonical_sections"]:
        for a in sec["aliases"]:
            if n == a:
                return sec["key"]
    return None


def parse_page(path):
    src = open(path, encoding="utf-8").read()
    heads = [(m.group(1), m.group(2)) for m in re.finditer(r"^(#{2,3})\s+(.*)$", src, re.M)]
    return src, heads


def analyse(path, schema):
    """回傳 {renames, missing, duplicated, out_of_order, extras, forbidden, warn, size}。"""
    src, heads = parse_page(path)
    res = {"renames": [], "missing": [], "duplicated": [], "out_of_order": [],
           "extras": [], "forbidden": [], "warn": [], "size": len(src.encode())}
    keys = []
    h2 = [(h, t) for h, t in heads if h == "##"]
    for h, t in h2:
        key = canonical_for(t, schema)
        if key is None:
            n = norm_heading(t)
            if n in schema.get("extra_sections_allowed", []):
                continue
            res["extras"].append(t)
            continue
        if key in keys:
            res["duplicated"].append((t, key))
            continue
        if key not in norm_heading(t):
            res["renames"].append((t, key, "段名須為標準名（可保留括號註記）"))
        keys.append(key)

    canonical = [s["key"] for s in schema["canonical_sections"]]
    pos = [canonical.index(k) for k in keys if k in canonical]
    if pos != sorted(pos):
        res["out_of_order"] = keys
    for k in canonical:
        if k not in keys:
            res["missing"].append(k)

    if len(res["extras"]) > schema.get("max_extra_sections", 3):
        res["warn"].append(f"補充段過多（{len(res['extras'])} > {schema.get('max_extra_sections', 3)}）："
                           f"{'、'.join(res['extras'])}——請評估內容歸屬（是否該移到 concepts/endpoint card/_inbox）")

    for mk in schema["forbidden_markers"]:
        for m in re.finditer(mk["regex"], src, re.M):
            line_no = src[:m.start()].count("\n") + 1
            res["forbidden"].append((line_no, m.group(0), mk["why"], mk["fix"]))

    rule = schema.get("rules", {}).get("unconsumed_must_be_open")
    if rule:
        m = re.search(r"^##\s+.*未消化.*$", src, re.M)
        if m:
            rest = src[m.end():]
            nxt = re.search(r"^##\s+", rest, re.M)
            body = rest[:nxt.start()] if nxt else rest
            done = len(re.findall(r"^\s*-\s*\[x\]", body, re.M))
            if done:
                res["warn"].append(f"「未消化」含 {done} 個已結項（- [x]）——{rule['why']}")
    if res["size"] > schema["size_limit_bytes"]:
        res["warn"].append(f"超過 {schema['size_limit_bytes']} bytes（{res['size']}）")
    return res


def print_plan(path, r):
    print(f"\n--- 最小重構處方（rename plan）：{path}")
    if r["renames"]:
        for cur, want, why in r["renames"]:
            print(f"  [改名] `## {cur}` → `## {want}`（{why}）")
    if r["duplicated"]:
        for cur, key in r["duplicated"]:
            print(f"  [刪除] 重複段 `## {cur}`：同一標準段 `{key}` 已存在——"
                  f"若為補丁空殼段，直接刪除；若含獨有內容，併入正段後刪除（資訊不得遺失）")
    if r["missing"]:
        print(f"  [補段] 缺少標準段：{'、'.join(r['missing'])}——內容若在他檔（concepts/endpoint card/_inbox），"
              f"以 cross-ref 補上，不得以空殼標題充數")
    if r["out_of_order"]:
        print(f"  [重排] 段序不符標準序：目前 {' → '.join(r['out_of_order'])}；"
              f"標準序＝一句話定位 → 論文版概念 → atlas 對位 → 散戶解讀 → 驗證方式 → 未消化")
    if r["extras"]:
        print(f"  [歸屬] 非標準段：{'、'.join(r['extras'])}——依 `_manifest_coverage_routing.md §3.2` 判斷"
              f"是否為 SK 頁應有內容（否則移到 concepts/entities/endpoint card/_inbox）")
    if r["forbidden"]:
        for line_no, tok, why, fix in r["forbidden"]:
            print(f"  [禁用] L{line_no} `{tok}`：{why} → {fix}")
    if r["warn"]:
        for w in r["warn"]:
            print(f"  [警告] {w}")
    if not any([r["renames"], r["duplicated"], r["missing"], r["out_of_order"], r["forbidden"]]):
        print("  ✅ 結構就位，無需重構")


def main():
    ap = argparse.ArgumentParser(description="SK 頁結構守衛（反補丁 M2/M2′）")
    ap.add_argument("--skills-dir", default="skills")
    ap.add_argument("--plan", action="store_true", help="只印最小重構處方")
    ap.add_argument("--strict", action="store_true", help="warn 級也視為違規")
    args = ap.parse_args()

    schema = load_schema()
    files = sorted(f for f in glob.glob(os.path.join(args.skills_dir, "SK-*.md")) if ".bak" not in f)
    if not files:
        print("⚠️  掃到 0 個 SK 頁——請確認 --skills-dir（不得假綠）")
        return 2

    print("=" * 64)
    print(f"SK 頁結構檢查（SSOT: skill-page-schema.json v{schema['version']}）")
    print("=" * 64)

    hard = 0
    warns = 0
    for f in files:
        r = analyse(f, schema)
        bad = bool(r["renames"] or r["duplicated"] or r["missing"] or r["out_of_order"] or r["forbidden"])
        if bad or r["warn"]:
            print(f"\n❌ {os.path.basename(f)}  ({r['size']} bytes)" if bad else f"\n⚠️  {os.path.basename(f)}")
            if r["duplicated"]:
                for cur, key in r["duplicated"]:
                    print(f"   ❌ 重複標準段：`## {cur}`（= {key}）")
            if r["missing"]:
                print(f"   ❌ 缺標準段：{'、'.join(r['missing'])}")
            if r["out_of_order"]:
                print(f"   ❌ 段序錯誤：{' → '.join(r['out_of_order'])}")
            if r["renames"]:
                for cur, want, _ in r["renames"]:
                    print(f"   ❌ 段名不符：`## {cur}` → 應為 `## {want}`")
            if r["forbidden"]:
                for line_no, tok, why, _ in r["forbidden"]:
                    print(f"   ❌ 禁用標記 L{line_no} `{tok}`：{why}")
            for w in r["warn"]:
                print(f"   ⚠️  {w}")
            print_plan(os.path.basename(f), r)
            hard += 1 if bad else 0
            warns += len(r["warn"])

    print("\n" + "=" * 64)
    if hard == 0 and (warns == 0 or not args.strict):
        print(f"✅ 結構：{len(files)} 頁通過硬規則（warn {warns} 條）")
        return 0
    if hard == 0 and args.strict and warns:
        print(f"❌ strict：{warns} 條警告視為違規")
        return 1
    print(f"❌ 結構：{hard}/{len(files)} 頁有硬違規（warn {warns} 條）")
    print("修法：照上方「最小重構處方」逐條執行（改名／刪重複段／重排／移出非 SK 內容）；不得用加空殼標題的方式滿足檢查器。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
