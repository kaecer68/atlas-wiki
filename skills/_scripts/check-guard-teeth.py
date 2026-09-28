#!/usr/bin/env python3
"""check-guard-teeth.py — 護欄自測套件（2026-09-28 新增）

為什麼要這支：2026-09-27/28 的 incident 顯示——**改完護欄後自稱「有牙」是不可靠的**。
同一天內連續出現四個同型失誤，全部由外部審查才抓到：
  ① 同一邏輯在兩處實作 ⇒ 只修了 D、漏修 C（治理檔 regex）
  ② 護欄接了卻跑不動（CI 淺層 checkout ⇒ `git diff base...HEAD` 失敗）
  ③ falsy 判準靜默退化（`--base-ref ""` 退回「工作區 vs HEAD」＝假綠）
  ④ 自己的程式把資料吃掉（rename 被 `pass` 丟棄）
本套件把「每個護欄的失敗情境都要實跑」變成可重複執行的機械檢查。

檢查項：
  A. 每支護欄：**空集合必須失敗**（S8 原則）＋ 正常 repo 必須通過（不誤傷）。
  B. 針對性情境：shell 違規檔、引號 heredoc、docs 超標、R3（rename／空 base-ref／未同步）。
  C. 治理檔清單必須是**單一來源**：CI job 與 auto-commit-pr.sh 都不得再硬編 regex。

用法: python3 skills/_scripts/check-guard-teeth.py [--repo-root .] [--quick]
  任何一項失敗 ⇒ exit 1；檢查項為 0（＝套件自己空轉）⇒ exit 1。
"""
import argparse, os, re, shutil, subprocess, sys, tempfile

PASS, FAIL = "✅", "❌"


def run(cmd, cwd, env=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    ap.add_argument("--quick", action="store_true", help="跳過需要建立 git sandbox 的測試")
    a = ap.parse_args()
    R = os.path.abspath(a.repo_root)
    S = os.path.join(R, "skills", "_scripts")
    results, checks = [], 0

    def check(name, ok, detail=""):
        nonlocal checks
        checks += 1
        results.append((name, ok, detail))

    # === A. 空集合即失敗 + 正常不誤傷 ===
    GUARDS = [
        ("check-claim-rules.py", []),
        ("check-source-tiers.py", ["--strict"]),
        ("check-freshness.py", ["--strict"]),
        ("check-retrieval-integrity.py", ["--strict"]),
        ("check-detector-count-sync.py", ["--atlas-go-dir", os.path.expanduser("~/workspace/atlas")]),
        ("check-wiki-pages.py", []),
        ("check-shell-var-ascii.py", ["--strict"]),
        ("check-skill-index-sync.py", ["--repo-only"]),
    ]
    for script, extra in GUARDS:
        p = os.path.join(S, script)
        if not os.path.isfile(p):
            check(f"A/{script} 存在", False, "找不到檔案")
            continue
        r_empty = run(["python3", p, "--repo-root", "/tmp/__no_such_repo__"] + extra, R)
        check(f"A/{script} 空集合失敗", r_empty.returncode != 0, f"exit={r_empty.returncode}")
        r_ok = run(["python3", p, "--repo-root", R] + extra, R)
        check(f"A/{script} 正常 repo 通過", r_ok.returncode == 0, f"exit={r_ok.returncode}")

    # === B1. shell 護欄：違規要抓、引號 heredoc 不誤抓 ===
    tmp = tempfile.mkdtemp(prefix="teeth-")
    try:
        sc = os.path.join(S, "check-shell-var-ascii.py")
        os.makedirs(os.path.join(tmp, "scripts"), exist_ok=True)
        bad = os.path.join(tmp, "scripts", "bad.sh")
        open(bad, "w").write('#!/usr/bin/env bash\nset -u\nBASE=main\necho "x $BASE（離線）"\n')
        r = run(["python3", sc, "--repo-root", tmp, "--strict"], R)
        check("B1/shell 抓到違規", r.returncode != 0, f"exit={r.returncode}")
        good = os.path.join(tmp, "scripts", "good.sh")
        open(good, "w").write("#!/usr/bin/env bash\ncat <<'EOF'\n$x中\nEOF\n")
        os.remove(bad)
        r = run(["python3", sc, "--repo-root", tmp, "--strict"], R)
        check("B1/shell 引號 heredoc 不誤抓", r.returncode == 0, f"exit={r.returncode}")

        # === B2. docs 尺寸護欄 ===
        d = os.path.join(tmp, "docs"); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "big.md"), "w").write("x" * 12001)
        r = run(["python3", os.path.join(S, "check-wiki-pages.py"), "--repo-root", tmp], R)
        check("B2/docs 超標被抓", r.returncode != 0, f"exit={r.returncode}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # === B3. R3：rename / 空 base-ref / 未同步（需 git sandbox） ===
    if not a.quick:
        sb = tempfile.mkdtemp(prefix="teeth-git-")
        try:
            run(["git", "clone", "-q", "--local", R, sb], R)
            run(["git", "checkout", "-q", "-B", "teeth", "origin/main"], sb)
            open(os.path.join(sb, "skills", "SK-93-teeth.md"), "w").write("---\nname: SK-93\nstatus: draft\n---\n# t\n")
            run(["git", "add", "-A"], sb)
            run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "teeth"], sb)
            r = run(["python3", os.path.join(S, "check-skill-index-sync.py"), "--repo-only", "--repo-root", sb,
                     "--base-ref", "origin/main"], sb)
            check("B3/R3 未同步新 SK 頁被抓", r.returncode != 0, f"exit={r.returncode}")
            r = run(["python3", os.path.join(S, "check-skill-index-sync.py"), "--repo-only", "--repo-root", sb,
                     "--base-ref", ""], sb)
            check("B3/R3 空 base-ref fail-closed", r.returncode != 0, f"exit={r.returncode}")
            run(["git", "mv", "skills/SK-01-factor-library.md", "skills/SK-92-renamed.md"], sb)
            run(["git", "add", "-A"], sb)
            run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "rename"], sb)
            r = run(["python3", os.path.join(S, "check-skill-index-sync.py"), "--repo-only", "--repo-root", sb,
                     "--base-ref", "origin/main"], sb)
            check("B3/R3 rename 不得逃逸", r.returncode != 0, f"exit={r.returncode}")
        finally:
            shutil.rmtree(sb, ignore_errors=True)

    # === C. 治理檔清單單一來源 ===
    shared = os.path.join(S, "governance-files.txt")
    if not os.path.isfile(shared):
        check("C/共用治理檔清單存在", False, "缺少 skills/_scripts/governance-files.txt")
    else:
        for f, label in ((os.path.join(R, "scripts", "dev", "auto-commit-pr.sh"), "D 腳本"),
                         (os.path.join(R, ".github", "workflows", "validate-wiki.yml"), "C workflow")):
            text = open(f, encoding="utf-8").read()
            ok = "governance-files.txt" in text and "AGENTS\\.md|SCHEMA" not in text
            check(f"C/{label} 使用共用清單（無硬編 regex）", ok, "" if ok else "偵測到硬編治理檔 regex")

    print("═" * 64)
    print(f"護欄自測（guard teeth）— {checks} 項檢查")
    print("═" * 64)
    bad = [(n, d) for n, ok, d in results if not ok]
    for n, ok, d in results:
        print(f"  {PASS if ok else FAIL} {n}{('  ' + d) if d and not ok else ''}")
    if checks == 0:
        print(f"{FAIL} 套件跑 0 項檢查 — 不得視為通過")
        return 1
    if bad:
        print(f"\n{FAIL} {len(bad)}/{checks} 項失敗 ⇒ 護欄沒有宣稱的牙齒")
        return 1
    print(f"\n{PASS} 全部 {checks} 項通過")
    return 0


if __name__ == "__main__":
    sys.exit(main())
