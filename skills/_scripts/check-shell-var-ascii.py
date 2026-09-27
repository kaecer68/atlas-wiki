#!/usr/bin/env python3
"""check-shell-var-ascii.py — 掃描 shell 的「$VAR 緊接非 ASCII 字元」（2026-09-27 新增）

為什麼要這支：bash 會把緊接在 `$VAR` 後面的非 ASCII 字元視為**變數名的一部分**
（本機 /bin/bash 3.2.57、LANG=C.UTF-8 實測），例如：

    echo "找不到 ${BASE}（離線）"   # ✅ 安全
    echo "找不到 $BASE（離線）"     # ❌ set -u 下 unbound variable，且無任何輸出

2026-09-27 這個 bug 在同一天內被寫進 `scripts/dev/auto-commit-pr.sh` 兩次，
造成「宣稱會出聲警告、實際直接中止」的假訊號。此類 bug 可機械偵測，故設護欄。

掃描範圍：`scripts/**/*.sh`、`.git/hooks/pre-*`（若存在）、`.github/workflows/*.yml` 的 run 區塊。

用法: python3 skills/_scripts/check-shell-var-ascii.py [--repo-root .] [--json] [--strict]
  預設 warn（只報告）；`--strict` 時有違規即 exit 1。掃到 0 檔一律 exit 1（S8 原則）。
"""
import argparse, glob, json, os, re, sys

# $VAR 或 $VAR123 緊接一個非 ASCII 字元
BAD = re.compile(r"\$[A-Za-z_][A-Za-z0-9_]*[^\x00-\x7F]")


def strip_literals(line):
    """去掉單引號內的字面值（bash 不展開）與 `#` 註解，避免假陽性。"""
    out, in_sq = [], False
    for i, c in enumerate(line):
        if c == "'":
            in_sq = not in_sq
            out.append(" ")
            continue
        if not in_sq and c == "#" and (i == 0 or line[i - 1] in " \t;|"):
            break
        out.append(" " if in_sq else c)
    return "".join(out)


def scan_text(text):
    out = []
    for i, line in enumerate(text.split("\n"), 1):
        for m in BAD.finditer(strip_literals(line)):
            out.append({"line": i, "match": m.group(0), "text": line.strip()[:120]})
    return out


def targets(repo_root):
    files = []
    files += sorted(glob.glob(os.path.join(repo_root, "scripts", "**", "*.sh"), recursive=True))
    files += sorted(glob.glob(os.path.join(repo_root, ".git", "hooks", "pre-*")))
    return [f for f in files if os.path.isfile(f)]


def workflow_blocks(repo_root):
    """回傳 workflow 內 `run:` 區塊的所有行（含 `run: cmd` 單行形式）。

    以縮排追蹤：找到 `run:` 後，縮排更深的行都算區塊內容；縮排回到 <= 該鍵或遇到
    非空且同層的鍵即結束。逐行保留行號以便定位。
    """
    out = []
    for wf in sorted(glob.glob(os.path.join(repo_root, ".github", "workflows", "*.yml"))):
        lines = open(wf, encoding="utf-8").read().split("\n")
        i = 0
        while i < len(lines):
            line = lines[i]
            m = re.match(r"^(\s*)run:\s*(.*)$", line)
            if not m:
                i += 1
                continue
            base = len(m.group(1))
            rest = m.group(2).strip()
            if rest and rest not in ("|", ">", "|-", ">-"):
                out.append((wf, i + 1, line))  # 單行形式 run: cmd
                i += 1
                continue
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if nxt.strip() == "":
                    i += 1
                    continue
                indent = len(nxt) - len(nxt.lstrip())
                if indent <= base:
                    break
                out.append((wf, i + 1, nxt))
                i += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()

    files = targets(a.repo_root)
    viol = []
    for f in files:
        for v in scan_text(open(f, encoding="utf-8", errors="replace").read()):
            v["file"] = os.path.relpath(f, a.repo_root)
            viol.append(v)
    wf_lines = workflow_blocks(a.repo_root)
    for wf, ln, line in wf_lines:
        for m in BAD.finditer(line):
            viol.append({"file": os.path.relpath(wf, a.repo_root), "line": ln,
                         "match": m.group(0), "text": line.strip()[:120]})

    if a.json:
        print(json.dumps({"shell_files": len(files), "workflow_lines": len(wf_lines),
                          "violations": viol}, ensure_ascii=False, indent=1))
        return 1 if viol or not files else 0

    print("═" * 64)
    print(f"shell「$VAR 緊接非 ASCII」檢查 — {len(files)} 個 shell ＋ {len(wf_lines)} 行 workflow")
    print("═" * 64)
    if not files:
        print("❌ 掃到 0 個 shell 檔（--repo-root 可能錯）— 護欄不得在空集合上通過")
        return 1
    if viol:
        print(f"{'❌' if a.strict else '⚠️ '} {len(viol)} 條違規（set -u 下會 unbound 中止）：")
        for v in viol:
            print(f"   - {v['file']}:{v['line']}  {v['match']!r} ｜ {v['text']}")
        print("   修法：改用 ${VAR}（加大括號）")
        return 1 if a.strict else 0
    print("✅ 無違規")
    return 0


if __name__ == "__main__":
    sys.exit(main())
