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
import argparse, importlib.util, os, re, shutil, subprocess, sys, tempfile, time

HAS_YAML = importlib.util.find_spec('yaml') is not None

PASS, FAIL = "✅", "❌"
APP_LOGIN = "atlas-qc-reviewer[bot]"

MOCK_API = "import json,sys\nfrom http.server import BaseHTTPRequestHandler,HTTPServer\nPORT=int(sys.argv[1]); ACTOR=sys.argv[2]; APP=sys.argv[3] if len(sys.argv)>3 else ''\nclass H(BaseHTTPRequestHandler):\n    def log_message(self,*a): pass\n    def do_GET(self):\n        if '/timeline' in self.path:\n            b=[{'event':'labeled','label':{'name':'kaecer-reviewed'},'actor':{'login':ACTOR}}] if ACTOR else []\n        elif '/reviews' in self.path:\n            b=[{'state':'APPROVED','user':{'login':APP}}] if APP else []\n        else: b=[]\n        r=json.dumps(b).encode(); self.send_response(200)\n        self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(r)))\n        self.end_headers(); self.wfile.write(r)\nHTTPServer(('127.0.0.1',PORT),H).serve_forever()"


def run(cmd, cwd, env=None):
    e = dict(os.environ)
    # 清掉 git hook 匯出的 GIT_*（GIT_DIR/GIT_INDEX_FILE...）——否則 `git -C <sandbox>`
    # 仍會操作到呼叫端 repo（2026-09-28 實證：hook 內跑本套件會清空呼叫端索引、
    # 甚至切換其分支）。這是要在本套件內跑 git 的必要前置。
    for k in [k for k in e if k.startswith("GIT_")]:
        e.pop(k, None)
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
    results, checks, skips = [], 0, []

    def caller_state():
        """呼叫端 repo 的 (HEAD, branch)；用於自我保護檢查（2026-09-28 加入）。

        背景：本套件會在臨時 sandbox 內做 `git mv`/commit；若 sandbox 建立失敗而指令
        落到呼叫端 repo，會污染真實工作區。此檢查會在收尾時比對並失敗。
        """
        try:
            head = subprocess.run(["git", "-C", R, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
            br = subprocess.run(["git", "-C", R, "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
            return head, br
        except Exception:
            return "", ""

    caller_before = caller_state()

    def check(name, ok, detail=""):
        nonlocal checks
        checks += 1
        results.append((name, ok, detail))

    # === A. 空集合即失敗 + 正常不誤傷 ===
    # (script, 空集合參數, 正常 repo 參數, 需要的路徑或 None)：空集合必須失敗、正常必須通過
    GUARDS = [
        ("check-claim-rules.py", ["--repo-root", "/tmp/__no_such_repo__"], ["--repo-root", R], None),
        ("check-source-tiers.py", ["--repo-root", "/tmp/__no_such_repo__", "--strict"], ["--repo-root", R, "--strict"], None),
        ("check-freshness.py", ["--repo-root", "/tmp/__no_such_repo__", "--strict"], ["--repo-root", R, "--strict"], None),
        ("check-retrieval-integrity.py", ["--repo-root", "/tmp/__no_such_repo__", "--strict"], ["--repo-root", R, "--strict"], None),
        ("check-detector-count-sync.py",
         ["--repo-root", "/tmp/__no_such_repo__", "--atlas-go-dir", os.path.expanduser("~/workspace/atlas")],
         ["--repo-root", R, "--atlas-go-dir", os.path.expanduser("~/workspace/atlas")],
         os.path.expanduser("~/workspace/atlas")),
        ("check-wiki-pages.py", ["--repo-root", "/tmp/__no_such_repo__"], ["--repo-root", R], None),
        ("check-shell-var-ascii.py", ["--repo-root", "/tmp/__no_such_repo__", "--strict"], ["--repo-root", R, "--strict"], None),
        ("check-skill-index-sync.py", ["--repo-only", "--repo-root", "/tmp/__no_such_repo__"], ["--repo-only", "--repo-root", R], None),
        # 2026-09-28 補涵蓋（審查 M11：這四支先前未被自測套件涵蓋）
        ("check-skill-structure.py", ["--skills-dir", "/tmp/__no_such_skills__"], ["--skills-dir", os.path.join(R, "skills")], None),
        ("check-skill-pages.py", ["--skills-dir", "/tmp/__no_such_skills__"], ["--skills-dir", os.path.join(R, "skills")], None),
        ("validate-timestamp-rule.py", ["--skills-dir", "/tmp/__no_such_skills__", "--all-classes"],
         ["--skills-dir", os.path.join(R, "skills"), "--all-classes"], None),
        ("audit-file-index-sync.py", ["--repo-root", "/tmp/__no_such_repo__"], ["--repo-root", R], None),
    ]
    for script, empty_args, normal_args, requires in GUARDS:
        p_ = os.path.join(S, script)
        if not os.path.isfile(p_):
            check(f"A/{script} 存在", False, "找不到檔案")
            continue
        r_empty = run(["python3", p_] + empty_args, R)
        check(f"A/{script} 空集合失敗", r_empty.returncode != 0, f"exit={r_empty.returncode}")
        if requires and not os.path.exists(requires):
            checks += 1
            skips.append(f"A/{script} 正常 repo 通過（環境缺 {requires}；該護欄由專屬 CI step 覆蓋）")
            continue
        if script == "check-wiki-pages.py" and not HAS_YAML:
            checks += 1
            skips.append(f"A/{script} 正常 repo 通過（環境缺 PyYAML ⇒ 檢查器降級、可能誤報）")
            continue
        r_ok = run(["python3", p_] + normal_args, R)
        check(f"A/{script} 正常 repo 通過", r_ok.returncode == 0, f"exit={r_ok.returncode}")

    # === A2. 注入已知違規必失敗（審查 M18：證明 A 段正向檢查不是空的）===
    tmp2 = tempfile.mkdtemp(prefix="teeth-inject-")
    try:
        import shutil as _sh
        _sh.copytree(os.path.join(R, "skills", "_scripts"), os.path.join(tmp2, "skills", "_scripts"))
        for d in ("concepts", "entities", "summaries", "templates"):
            os.makedirs(os.path.join(tmp2, d), exist_ok=True)
        with open(os.path.join(tmp2, "concepts", "zz-inject.md"), "w") as f:
            print("---", file=f)
            print("title: zz-inject", file=f)
            print("description: inject", file=f)
            print("created: 2026-01-01", file=f)
            print("updated: 2026-01-01", file=f)
            print("type: concept", file=f)
            print("tags: []", file=f)
            print("sources: []", file=f)
            print("---", file=f)
            print("本頁引用 synthetic 的 R²_OOS 數值。", file=f)
        r = run(["python3", os.path.join(S, "check-claim-rules.py"), "--repo-root", tmp2], R)
        check("A2/注入 S7 違規 ⇒ check-claim-rules 必須失敗", r.returncode != 0, f"exit={r.returncode}")
        # 對照：拿掉違規句 ⇒ 必須通過（證明失敗來自注入內容）
        with open(os.path.join(tmp2, "concepts", "zz-inject.md"), "w") as f:
            print("---", file=f); print("title: zz-inject", file=f); print("description: inject", file=f)
            print("created: 2026-01-01", file=f); print("updated: 2026-01-01", file=f)
            print("type: concept", file=f); print("tags: []", file=f); print("sources: []", file=f)
            print("---", file=f); print("本頁無違規句。", file=f)
        r = run(["python3", os.path.join(S, "check-claim-rules.py"), "--repo-root", tmp2], R)
        check("A2/對照組（移除違規句）通過", r.returncode == 0, f"exit={r.returncode}")
    finally:
        shutil.rmtree(tmp2, ignore_errors=True)

    # === A2b. detector-count：注入錯誤宣稱必失敗（審查 F3/M18）＋對照組 ===
    tmp3 = tempfile.mkdtemp(prefix="teeth-det-")
    try:
        os.makedirs(os.path.join(tmp3, "concepts"), exist_ok=True)
        os.makedirs(os.path.join(tmp3, "skills", "_scripts"), exist_ok=True)
        fake_go = os.path.join(tmp3, "atlas-go", "internal", "narrative")
        os.makedirs(fake_go, exist_ok=True)
        with open(os.path.join(fake_go, "detector_count_gate_test.go"), "w") as f:
            print("package narrative", file=f)
            print("const documentedDetectorCount = 29", file=f)

        def write_claim(n):
            with open(os.path.join(tmp3, "concepts", "zz-det.md"), "w") as f:
                print("---", file=f); print("title: zz-det", file=f); print("description: d", file=f)
                print("created: 2026-01-01", file=f); print("updated: 2026-01-01", file=f)
                print("type: concept", file=f); print("tags: []", file=f); print("sources: []", file=f)
                print("---", file=f); print(f"`detector_registry_list` 回報 **{n}** 個 template trigger detectors。", file=f)

        write_claim(99)
        r = run(["python3", os.path.join(S, "check-detector-count-sync.py"),
                 "--repo-root", tmp3, "--atlas-go-dir", os.path.join(tmp3, "atlas-go")], R)
        check("A2b/注入錯誤 detector 數（99 vs 權威 29）⇒ 必須失敗且指出不一致",
              r.returncode != 0 and "不一致" in r.stdout, f"exit={r.returncode}")
        write_claim(29)
        r = run(["python3", os.path.join(S, "check-detector-count-sync.py"),
                 "--repo-root", tmp3, "--atlas-go-dir", os.path.join(tmp3, "atlas-go")], R)
        check("A2b/對照組（宣稱 29 == 權威）通過", r.returncode == 0, f"exit={r.returncode}")
    finally:
        shutil.rmtree(tmp3, ignore_errors=True)

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
        # B2：fixture 必須是「有 schema 的 repo」——否則紅的原因是找不到 schema（假牙）。
        # 2026-09-28 審查發現：舊版在孤立 tmp 目錄測，紅的原因不是 size。
        os.makedirs(os.path.join(tmp, "skills", "_scripts"), exist_ok=True)
        shutil.copy(os.path.join(S, "wiki-page-schema.json"),
                    os.path.join(tmp, "skills", "_scripts", "wiki-page-schema.json"))
        d = os.path.join(tmp, "docs"); os.makedirs(d, exist_ok=True)
        ok_doc = os.path.join(d, "ok.md")
        open(ok_doc, "w").write("x" * 100)
        r = run(["python3", os.path.join(S, "check-wiki-pages.py"), "--repo-root", tmp], R)
        check("B2/docs 合規檔通過（對照組）", r.returncode == 0, f"exit={r.returncode} {r.stdout[-80:]}")
        open(os.path.join(d, "big.md"), "w").write("x" * 12001)
        r = run(["python3", os.path.join(S, "check-wiki-pages.py"), "--repo-root", tmp], R)
        check("B2/docs 超標被抓（且訊息指向 size）",
              r.returncode != 0 and "12001" in r.stdout, f"exit={r.returncode}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # === B3. R3 情境（在**合成 git repo** 內測，完全不碰呼叫端；2026-09-28 改） ===
    if not a.quick:
        sb = tempfile.mkdtemp(prefix="teeth-git-")
        try:
            G = ["git", "-C", sb]
            os.makedirs(os.path.join(sb, "skills"), exist_ok=True)
            run(["git", "init", "-q", "-b", "main", sb], R)
            run(G + ["config", "user.email", "t@t"], R)
            run(G + ["config", "user.name", "t"], R)
            with open(os.path.join(sb, "skills", "SK-00-skill-index.md"), "w") as f:
                print("# index", file=f)
                print("- [[SK-01-probe]]", file=f)
            with open(os.path.join(sb, "skills", "SK-01-probe.md"), "w") as f:
                print("---", file=f); print("name: SK-01", file=f); print("status: draft", file=f)
                print("---", file=f); print("# a", file=f)
            run(G + ["add", "-A"], R)
            run(G + ["commit", "-qm", "base"], R)
            if not os.path.isdir(os.path.join(sb, ".git")):
                check("B3/sandbox 建立", False, "git init 未產生 .git")
                raise RuntimeError("sandbox-not-a-repo")

            run(G + ["checkout", "-q", "-B", "add", "main"], R)
            with open(os.path.join(sb, "skills", "SK-99-probe.md"), "w") as f:
                print("---", file=f); print("name: SK-99", file=f); print("status: draft", file=f)
                print("---", file=f); print("# p", file=f)
            run(G + ["add", "-A"], R)
            run(G + ["commit", "-qm", "add-unsynced"], R)
            r = run(["python3", os.path.join(S, "check-skill-index-sync.py"), "--repo-only",
                     "--repo-root", sb, "--base-ref", "main"], R)
            check("B3/R3 未同步新 SK 頁被抓", r.returncode != 0, f"exit={r.returncode}")

            r = run(["python3", os.path.join(S, "check-skill-index-sync.py"), "--repo-only",
                     "--repo-root", sb, "--base-ref", ""], R)
            check("B3/R3 空 base-ref fail-closed", r.returncode != 0, f"exit={r.returncode}")

            run(G + ["checkout", "-q", "-B", "ren", "main"], R)
            run(G + ["mv", "skills/SK-01-probe.md", "skills/SK-77-renamed.md"], R)
            run(G + ["add", "-A"], R)
            run(G + ["commit", "-qm", "rename"], R)
            r = run(["python3", os.path.join(S, "check-skill-index-sync.py"), "--repo-only",
                     "--repo-root", sb, "--base-ref", "main"], R)
            check("B3/R3 rename 不得逃逸", r.returncode != 0, f"exit={r.returncode}")

            run(G + ["checkout", "-q", "-B", "sync", "main"], R)
            with open(os.path.join(sb, "skills", "SK-98-probe.md"), "w") as f:
                print("---", file=f); print("name: SK-98", file=f); print("status: draft", file=f)
                print("---", file=f); print("# p", file=f)
            with open(os.path.join(sb, "skills", "SK-00-skill-index.md"), "a") as f:
                print("- [[SK-98-probe]]", file=f)
            run(G + ["add", "-A"], R)
            run(G + ["commit", "-qm", "synced"], R)
            r = run(["python3", os.path.join(S, "check-skill-index-sync.py"), "--repo-only",
                     "--repo-root", sb, "--base-ref", "main"], R)
            check("B3/R3 已同步索引通過", r.returncode == 0, f"exit={r.returncode}")
        except RuntimeError:
            pass
        finally:
            shutil.rmtree(sb, ignore_errors=True)

    # === D. 治理閘門「行為測試」（審查 C0/N1/N2：字串比對抓不到突變）===
    if not a.quick:
        wfpath = os.path.join(R, ".github", "workflows", "validate-wiki.yml")
        if not os.path.isfile(wfpath):
            check("D/找到 workflow", False, "缺 validate-wiki.yml")
        else:
            wt = open(wfpath, encoding="utf-8").read()
            try:
                # 抽取起點必須是 `set -euo pipefail`（否則抽出的步驟少了 set -e 與 MERGED 早退，
                # 會讓突變「移除 base 讀取 fallback」不被抓 ⇒ 保護不了 F2 死結；2026-09-28 審查）
                job_at = wt.index("governance-review-gate")
                i = wt.index("          set -euo pipefail", job_at)
                j = wt.index("  validate-timestamp-rule:")
                lines = [(l[10:] if l.startswith("          ") else l) for l in wt[i:j].split(chr(10))]
                gate = os.path.join(tempfile.mkdtemp(prefix="teeth-gate-"), "gate.sh")
                gate_src = chr(10).join(lines).replace("${{ github.event.pull_request.number }}", "${PR_NUM}")
                with open(gate, "w") as f:
                    print(gate_src, file=f)
                check("D/抽出閘門步驟", len(lines) > 5, f"{len(lines)} 行")
            except ValueError:
                gate = None
                check("D/抽出閘門步驟", False, "找不到 run 區塊邊界")

            if gate:
                sb = tempfile.mkdtemp(prefix="teeth-gate-repo-")
                try:
                    G = ["git", "-C", sb]
                    run(["git", "init", "-q", "-b", "main", sb], R)
                    run(G + ["config", "user.email", "t@t"], R)
                    run(G + ["config", "user.name", "t"], R)
                    os.makedirs(os.path.join(sb, "skills", "_scripts"), exist_ok=True)
                    os.makedirs(os.path.join(sb, ".github", "workflows"), exist_ok=True)
                    for rel in ("AGENTS.md", "SCHEMA.md", "docs/git-merge-protocol.md", "skills/_method.md"):
                        d = os.path.dirname(os.path.join(sb, rel))
                        if d:
                            os.makedirs(d, exist_ok=True)
                        with open(os.path.join(sb, rel), "w") as f:
                            print("v1", file=f)
                    with open(os.path.join(sb, ".github/workflows/validate-wiki.yml"), "w") as f:
                        print("name: x", file=f)
                    run(G + ["add", "-A"], R)
                    run(G + ["commit", "-qm", "base(no list)"], R)
                    base_nolist = run(G + ["rev-parse", "HEAD"], R).stdout.strip()

                    def gate_run(base_sha, labels):
                        env = {"BASE_SHA": base_sha, "LABELS": labels, "MERGED": ""}
                        return run(["bash", gate], sb, env=env).returncode

                    # case1 bootstrap：分支新增清單檔（base 沒有）＋動 AGENTS.md
                    run(G + ["checkout", "-q", "-B", "boot", base_nolist], R)
                    with open(os.path.join(sb, "skills/_scripts/governance-files.txt"), "w") as f:
                        print("AGENTS\\.md", file=f)
                    with open(os.path.join(sb, "AGENTS.md"), "w") as f:
                        print("v2", file=f)
                    run(G + ["add", "-A"], R)
                    run(G + ["commit", "-qm", "bootstrap"], R)
                    check("D/bootstrap 未貼標籤 ⇒ 紅", gate_run(base_nolist, "") != 0)
                    mock_py = os.path.join(sb, "mock_api.py")
                    with open(mock_py, "w") as f:
                        print(MOCK_API, file=f)

                    def gate_with_actor(actor, approver=""):
                        port = 8900 + (abs(hash(actor + approver)) % 90)
                        proc = subprocess.Popen([sys.executable, mock_py, str(port), actor, approver],
                                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        try:
                            time.sleep(0.6)
                            env = {"BASE_SHA": base_nolist, "LABELS": "kaecer-reviewed", "MERGED": "",
                                   "GITHUB_REPOSITORY": "x/y", "GITHUB_TOKEN": "t",
                                   "GITHUB_API_URL": "http://127.0.0.1:%d" % port, "PR_NUM": "1"}
                            return run(["bash", gate], sb, env=env).returncode
                        finally:
                            proc.kill()

                    check("D/App 身分貼標籤 ⇒ 綠（無死結）", gate_with_actor(APP_LOGIN) == 0)
                    check("D/作者自貼標籤 ⇒ 紅（洞已關）", gate_with_actor("kaecer68") != 0)
                    check("D/作者自貼＋App 核准 ⇒ 綠", gate_with_actor("kaecer68", APP_LOGIN) == 0)

                    # 以「已含清單」的 commit 為新 base，測攻擊
                    base2 = run(G + ["rev-parse", "HEAD"], R).stdout.strip()

                    def attack(name, mutate):
                        run(G + ["checkout", "-q", "-B", name, base2], R)
                        mutate()
                        run(G + ["add", "-A"], R)
                        run(G + ["commit", "-qm", name], R)
                        return gate_run(base2, "")

                    def drop_agents_line():
                        p2 = os.path.join(sb, "skills/_scripts/governance-files.txt")
                        keep = [l for l in open(p2).read().split(chr(10)) if "AGENTS" not in l]
                        with open(p2, "w") as f:
                            print(chr(10).join(keep), file=f)
                        with open(os.path.join(sb, "AGENTS.md"), "w") as f:
                            print("v3", file=f)

                    def drop_self_line():
                        drop_agents_line()
                        p2 = os.path.join(sb, "skills/_scripts/governance-files.txt")
                        keep = [l for l in open(p2).read().split(chr(10)) if "governance-files" not in l]
                        with open(p2, "w") as f:
                            print(chr(10).join(keep), file=f)

                    def delete_list():
                        os.remove(os.path.join(sb, "skills/_scripts/governance-files.txt"))
                        with open(os.path.join(sb, "AGENTS.md"), "w") as f:
                            print("v3", file=f)

                    check("D/攻擊A（刪 AGENTS 行＋改 AGENTS.md）⇒ 紅", attack("atkA", drop_agents_line) != 0)
                    check("D/攻擊B（連清單自身那行一起刪）⇒ 紅", attack("atkB", drop_self_line) != 0)
                    check("D/攻擊C（整檔刪除）⇒ 紅", attack("atkC", delete_list) != 0)

                    # case4 合法 routine（只改 concepts/）
                    run(G + ["checkout", "-q", "-B", "routine", base2], R)
                    os.makedirs(os.path.join(sb, "concepts"), exist_ok=True)
                    with open(os.path.join(sb, "concepts", "a.md"), "w") as f:
                        print("x", file=f)
                    run(G + ["add", "-A"], R)
                    run(G + ["commit", "-qm", "routine"], R)
                    check("D/合法 routine ⇒ 綠", gate_run(base2, "") == 0)
                finally:
                    shutil.rmtree(sb, ignore_errors=True)
                    shutil.rmtree(os.path.dirname(gate), ignore_errors=True)

    # === E. D 腳本（auto-commit-pr.sh）行為測試（審查 F2：本 PR 刪掉 C0 後 D 端零覆蓋）===
    if not a.quick:
        dpath = os.path.join(R, "scripts", "dev", "auto-commit-pr.sh")
        if not os.path.isfile(dpath):
            check("E/找到 auto-commit-pr.sh", False, "缺檔")
        else:
            dt = open(dpath, encoding="utf-8").read()
            try:
                i0 = dt.index('BASE_REF="origin/$BASE"')
                i1 = dt.index("GOV_HITS=")
                frag = dt[i0:i1]
                dtest = os.path.join(tempfile.mkdtemp(prefix="teeth-d-"), "d.sh")
                with open(dtest, "w") as f:
                    print("set -euo pipefail", file=f)
                    print(frag, file=f)
                    print('echo "GOV_RE=$GOV_RE"', file=f)
                check("E/抽出 D 端治理判定片段", len(frag) > 100, f"{len(frag)} bytes")
            except ValueError:
                dtest = None
                check("E/抽出 D 端治理判定片段", False, "找不到錨點")

            if dtest:
                sb2 = tempfile.mkdtemp(prefix="teeth-drepo-")
                try:
                    G = ["git", "-C", sb2]
                    run(["git", "init", "-q", "-b", "main", sb2], R)
                    run(G + ["config", "user.email", "t@t"], R)
                    run(G + ["config", "user.name", "t"], R)
                    os.makedirs(os.path.join(sb2, "skills", "_scripts"), exist_ok=True)
                    with open(os.path.join(sb2, "skills", "_scripts", "governance-files.txt"), "w") as f:
                        print("AGENTS\\.md", file=f)
                    with open(os.path.join(sb2, "AGENTS.md"), "w") as f:
                        print("v1", file=f)
                    run(G + ["add", "-A"], R)
                    run(G + ["commit", "-qm", "base"], R)

                    # case1：沒有 origin/main ⇒ 必須 fail-closed（原本 fallback 到本地分支 ⇒ fail-open）
                    # 注意：sandbox 必須「已 checkout 到 feat 且有非治理檔 diff」，否則退回本地分支後
                    # 會晚一步死在「diff 為空」⇒ 用錯的理由滿足斷言（2026-09-28 審查 E2）。
                    run(G + ["checkout", "-q", "-b", "feat"], R)
                    os.makedirs(os.path.join(sb2, "concepts"), exist_ok=True)
                    with open(os.path.join(sb2, "concepts", "zz.md"), "w") as f:
                        print("x", file=f)
                    run(G + ["add", "-A"], R)
                    run(G + ["commit", "-qm", "routine change"], R)
                    r = run(["bash", dtest], sb2, env={"BASE": "main", "GOV_LIST":
                             os.path.join(sb2, "skills", "_scripts", "governance-files.txt")})
                    check("E/無 origin/main ⇒ fail-closed（不得退回本地分支）",
                          r.returncode != 0 and "origin" in (r.stdout + r.stderr), f"exit={r.returncode}")

                    # case2：建立 origin/main 後，再做一個 commit 產生 diff
                    # ⇒ 應可計算 GOV_RE，且含寫死路徑（若無 diff，護欄會正確地 exit 1）
                    run(G + ["update-ref", "refs/remotes/origin/main", "HEAD"], R)
                    with open(os.path.join(sb2, "AGENTS.md"), "w") as f:
                        print("v2", file=f)
                    run(G + ["add", "-A"], R)
                    run(G + ["commit", "-qm", "touch AGENTS.md"], R)
                    r = run(["bash", dtest], sb2, env={"BASE": "main", "GOV_LIST":
                             os.path.join(sb2, "skills", "_scripts", "governance-files.txt")})
                    ok = r.returncode == 0 and "governance-files" in r.stdout and "AGENTS" in r.stdout
                    check("E/有 origin/main ⇒ GOV_RE 含寫死路徑與清單內容", ok, f"exit={r.returncode}")

                    # case3：base 清單有 AGENTS、head 清單刪掉它 ⇒ GOV_RE 仍須含 AGENTS（抓 head-only 回歸）
                    run(G + ["update-ref", "refs/remotes/origin/main", "HEAD"], R)
                    lp = os.path.join(sb2, "skills", "_scripts", "governance-files.txt")
                    with open(lp, "w") as f:
                        print("SCHEMA\.md", file=f)
                    with open(os.path.join(sb2, "AGENTS.md"), "w") as f:
                        print("v3", file=f)
                    run(G + ["add", "-A"], R)
                    run(G + ["commit", "-qm", "drop AGENTS from list"], R)
                    r = run(["bash", dtest], sb2, env={"BASE": "main", "GOV_LIST": lp})
                    check("E/base∪head：head 刪掉的行仍在 GOV_RE（抓 head-only）",
                          r.returncode == 0 and "AGENTS" in r.stdout, f"exit={r.returncode}")
                finally:
                    shutil.rmtree(sb2, ignore_errors=True)
                    shutil.rmtree(os.path.dirname(dtest), ignore_errors=True)

    # === C0. 治理檔清單自身受保護 ＋ base ∪ head（F2：不得靠 routine PR 解除保護）===
    gtxt = open(os.path.join(S, "governance-files.txt"), encoding="utf-8").read() if os.path.isfile(os.path.join(S, "governance-files.txt")) else ""
    check("C0/清單本身納入清單（可被自己的規則保護）", "governance-files" in gtxt)
    wtext = open(os.path.join(R, ".github", "workflows", "validate-wiki.yml"), encoding="utf-8").read()
    dtext = open(os.path.join(R, "scripts", "dev", "auto-commit-pr.sh"), encoding="utf-8").read()
    # base ∪ head 與攻擊矩陣改由 D 段以「真實閘門步驟」行為測試覆蓋（2026-09-28）。

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

    caller_after = caller_state()
    if caller_before != caller_after:
        check("Z/呼叫端 repo 未被本套件改動", False, f"before={caller_before} after={caller_after}")

    print("═" * 64)
    print(f"護欄自測（guard teeth）— {checks} 項檢查")
    print("═" * 64)
    bad = [(n, d) for n, ok, d in results if not ok]
    for n, ok, d in results:
        print(f"  {PASS if ok else FAIL} {n}{('  ' + d) if d and not ok else ''}")
    if checks == 0:
        print(f"{FAIL} 套件跑 0 項檢查 — 不得視為通過")
        return 1
    for s in skips:
        print(f"  ⏭️  skip: {s}")
    if bad:
        print(f"\n{FAIL} {len(bad)}/{checks} 項失敗 ⇒ 護欄沒有宣稱的牙齒")
        return 1
    if skips:
        print(f"\n{PASS} {checks - len(skips)} 項通過、{len(skips)} 項 skip（未測試，見上方 ⏭️）")
    else:
        print(f"\n{PASS} 全部 {checks} 項通過")
    return 0


if __name__ == "__main__":
    sys.exit(main())
