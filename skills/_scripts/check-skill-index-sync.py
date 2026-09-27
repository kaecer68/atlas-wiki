#!/usr/bin/env python3
"""
check-skill-index-sync.py — 強制 skills 建立/修改時索引同步更新
對位 kaecer 8/21 21:25 拍板：
  CI 腳本必須檢查 skills 建立/修改時,索引機制（skills-map.md + agents.md）必同步更新,
  避免「該呼叫的 skill 卻呼叫不到」的參數錯誤。

規則:
  R1: hermes SKILL.md 新建/修改 → ~/.hermes/skills/skills-map.md 必同步修改
  R2: skills-map.md 修改 → 對應 agents.md 必同步修改
  R3: atlas-wiki SK 頁新增/刪除 → skills/SK-00-skill-index.md 必同步（2026-09-27 收窄）
  R4: SKILL.md frontmatter 必含 status 欄位

執行:
  python3 skills/_scripts/check-skill-index-sync.py [--repo-root PATH] [--dry-run]

退出碼:0 全綠 / 1 有違規
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

HERMES_HOME = Path.home()
HERMES_SKILLS_DIR = HERMES_HOME / ".hermes" / "skills"
HERMES_SKILLS_MAP = HERMES_SKILLS_DIR / "skills-map.md"
HERMES_AGENTS_MD = HERMES_HOME / ".hermes" / "SOUL.md"  # hermes 無 AGENTS.md,用 SOUL.md 替代

VALID_STATUS = ["active", "draft", "deprecated", "in-transition", "archived", "stable", "cold"]


def get_git_changes(repo_root: Path, paths: list) -> dict:
    """跑 git diff + git status 找 staged/unstaged/untracked 變更"""
    changes = {"A": [], "M": [], "D": []}
    if not (repo_root / ".git").exists():
        return changes

    # git diff
    try:
        result = subprocess.run(
            ["git", "diff", "--name-status", "HEAD", "--"] + paths,
            cwd=str(repo_root), capture_output=True, text=True, timeout=30
        )
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            status = parts[0][0]  # A/M/D/R
            path = parts[-1]
            if status in changes:
                changes[status].append(path)
    except Exception:
        pass

    # git status --porcelain (untracked)
    try:
        result2 = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(repo_root), capture_output=True, text=True, timeout=30
        )
        for line in result2.stdout.strip().split("\n"):
            if not line:
                continue
            if line.startswith("??"):
                p = line[3:].strip()
                if any(p.startswith(pa) for pa in paths):
                    changes["A"].append(p)
    except Exception:
        pass

    return changes


def change_set_vs_base(repo_root: Path, base_ref: str) -> dict:
    """以 `git diff --name-status -M <base_ref>...HEAD` 取變更集（CI 用）。

    為什麼需要：R3 若只看「工作區 vs HEAD」，在 CI 的乾淨 checkout 下變更集**恆為空**
    ⇒ 護欄永遠通過（假綠）。2026-09-28 由獨立審查實測發現。
    """
    changes = {"A": [], "M": [], "D": []}
    res = subprocess.run(
        ["git", "diff", "--name-status", "-M", f"{base_ref}...HEAD"],
        cwd=str(repo_root), capture_output=True, text=True, timeout=60,
    )
    if res.returncode != 0:
        raise RuntimeError(f"git diff {base_ref}...HEAD 失敗：{res.stderr.strip()[:200]}")
    for line in res.stdout.strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0][0]
        for p in parts[1:]:          # rename/copy 會給舊路徑與新路徑，全部納入
            if status in changes:
                changes[status].append(p)
            elif status == "R":      # 舊路徑視為刪除、新路徑視為新增
                pass
    return changes


def check_skill_index_sync(repo_root: Path, dry_run: bool = False, repo_only: bool = False,
                           base_ref=None) -> list:
    violations = []

    # === R1: hermes SKILL.md 變更 → skills-map.md 必同步 ===
    if HERMES_SKILLS_DIR.exists() and not repo_only:
        all_skills = [str(p.relative_to(HERMES_SKILLS_DIR))
                      for p in HERMES_SKILLS_DIR.rglob("SKILL.md")
                      if "_archive" not in str(p)]

        changes = get_git_changes(HERMES_HOME, ["skills/"] + 
                                  [f"skills-map.md"])

        changed_skills = ([f for f in changes["A"] if "SKILL.md" in f and "_archive" not in f] +
                          [f for f in changes["M"] if "SKILL.md" in f and "_archive" not in f])
        skills_map_changed = bool(
            [f for f in changes["A"] if "skills-map.md" in f] +
            [f for f in changes["M"] if "skills-map.md" in f]
        )

        if changed_skills and not skills_map_changed:
            violations.append({
                "rule": "R1: hermes SKILL.md 變更 → skills-map.md 必同步",
                "details": f"{len(changed_skills)} SKILL.md 變更但 skills-map.md 未動",
                "files": changed_skills[:5],
                "fix": f"編輯 {HERMES_SKILLS_MAP} 加新 skill 到分層索引或更新現有"
            })

    # === R3（2026-09-27 收窄）: atlas-wiki SK 頁「新增/刪除」→ SK 索引頁必同步 ===
    # 舊版（至 2026-09-27）：任何 skills/ 變更都要求 AGENTS.md 同步 ⇒ 把 routine PR
    #   強制變成 git-merge-protocol §6.4.2 的「重大變更」（須人工 review），而
    #   auto-commit-pr.sh 又會自動 merge ⇒ 規則互撞（見 PR #133 前的 incident）。
    # 新版：索引紀律的對象是「SK 頁清單」⇒ 只在 SK 頁新增/刪除時要求索引頁同步；
    #   工具（skills/_scripts/**）、schema、_method 等變更不再觸發本規則。
    SK_INDEX = "skills/SK-00-skill-index.md"
    sk_pages_present = len(list((repo_root / "skills").glob("SK-*.md"))) if (repo_root / "skills").is_dir() else 0
    if sk_pages_present == 0:
        violations.append({
            "rule": "R3: 掃到 0 個 SK 頁 — 護欄不得在空集合上通過",
            "details": f"{repo_root}/skills 下找不到 SK-*.md（--repo-root 可能錯）",
            "files": [],
            "fix": "確認 --repo-root 指向 atlas-wiki repo",
        })
    if base_ref:
        try:
            atlas_changes = change_set_vs_base(repo_root, base_ref)
        except RuntimeError as e:
            violations.append({
                "rule": "R3: 無法對 base ref 取變更集 — 護欄不得靜默通過",
                "details": str(e), "files": [],
                "fix": "確認 --base-ref 指向存在的 commit（CI 應傳 PR base SHA）",
            })
            atlas_changes = {"A": [], "M": [], "D": []}
    else:
        atlas_changes = get_git_changes(repo_root, ["skills/"])
    sk_page_added_or_deleted = [
        f for f in (atlas_changes["A"] + atlas_changes["D"])
        if re.match(r"^skills/SK-(?!00)\d", f)
    ]
    sk_index_changed = bool(
        [f for f in atlas_changes["A"] if f == SK_INDEX] +
        [f for f in atlas_changes["M"] if f == SK_INDEX]
    )

    if sk_page_added_or_deleted and not sk_index_changed:
        violations.append({
            "rule": f"R3: SK 頁新增/刪除 → {SK_INDEX} 必同步",
            "details": f"{len(sk_page_added_or_deleted)} 個 SK 頁新增/刪除但索引頁未動",
            "files": sk_page_added_or_deleted[:5],
            "fix": f"在 {SK_INDEX} 登錄/移除該 SK 頁（並同步 README.md／index.md 的計數 SSOT）"
        })

    # === R4: SKILL.md frontmatter 必含 status 欄位 ===
    if HERMES_SKILLS_DIR.exists() and not repo_only:
        bad_frontmatter = []
        scanned = 0
        for skill_path in HERMES_SKILLS_DIR.rglob("SKILL.md"):
            if "_archive" in str(skill_path):
                continue
            scanned += 1
            try:
                with open(skill_path, encoding="utf-8") as f:
                    content = f.read(2000)  # 只讀前 2000 chars
                m = re.match(r"^---\n(.+?)\n---", content, re.DOTALL)
                if not m:
                    bad_frontmatter.append((str(skill_path), "no frontmatter"))
                    continue
                fm = m.group(1)
                if not re.search(r"^status:\s*\S+", fm, re.MULTILINE):
                    bad_frontmatter.append((str(skill_path), "missing status"))
                else:
                    # 檢查 status 值是否合法
                    m2 = re.search(r"^status:\s*(\S+)", fm, re.MULTILINE)
                    if m2 and m2.group(1) not in VALID_STATUS:
                        bad_frontmatter.append((str(skill_path), f"invalid status: {m2.group(1)}"))
            except Exception:
                pass

        if scanned == 0:
            violations.append({
                "rule": "R4: 掃到 0 個 SKILL.md — 護欄不得在空集合上通過",
                "details": f"{HERMES_SKILLS_DIR} 下找不到 SKILL.md",
                "files": [],
                "fix": "確認 hermes skills 目錄存在；若在 CI 請改用 --repo-only",
            })

        if bad_frontmatter:
            violations.append({
                "rule": "R4: SKILL.md frontmatter 必含合法 status 欄位",
                "details": f"{len(bad_frontmatter)} SKILL.md frontmatter 不合規",
                "files": [f"{p[0]}: {p[1]}" for p in bad_frontmatter[:5]],
                "fix": f"每個 SKILL.md frontmatter 加 status: {{{{active|draft|deprecated|in-transition|archived}}}}"
            })

    return violations


def main():
    parser = argparse.ArgumentParser(description="Skills 索引同步檢查")
    parser.add_argument("--repo-root", default=str(Path.cwd()))
    parser.add_argument("--dry-run", action="store_true", help="只顯示違規,不退出")
    parser.add_argument("--skip-r4", action="store_true", help="跳過 R4 frontmatter 檢查（Plan F Week 3 補完前用）")
    parser.add_argument("--repo-only", action="store_true", help="只檢查 atlas-wiki repo 側（R3）；CI 用（CI 無 ~/.hermes）")
    parser.add_argument("--base-ref", default=None,
                        help="對 base ref 取變更集（CI 必須傳 PR base SHA；不傳則只看工作區 vs HEAD ⇒ CI 下恆空＝假綠）")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()

    print("=== Skills 索引同步檢查 (Plan F CI) ===")
    print(f"atlas-wiki repo: {repo_root}")
    print(f"hermes skills dir: {HERMES_SKILLS_DIR}")
    print(f"dry-run: {args.dry_run}")
    print()

    violations = check_skill_index_sync(repo_root, dry_run=args.dry_run, repo_only=args.repo_only,
                                        base_ref=args.base_ref)
    if args.skip_r4:
        violations = [v for v in violations if not v["rule"].startswith("R4")]

    if violations:
        print(f"❌ {len(violations)} 條違規\n")
        for i, v in enumerate(violations, 1):
            print(f"[違規 {i}] {v['rule']}")
            if "details" in v:
                print(f"  {v['details']}")
            if v.get("files"):
                print(f"  涉及檔案:")
                for f in v["files"]:
                    print(f"    - {f}")
            if "fix" in v:
                print(f"  修法: {v['fix']}")
            print()
        if not args.dry_run:
            sys.exit(1)
    else:
        print("✅ 所有 skills 索引同步規則通過")
        sys.exit(0)


if __name__ == "__main__":
    main()


# =============================================================================
# Plan F Week 3 Day 4 (2026-08-22 kaecer 拍板): R5 護欄 — skill 競爭 SOP
# 規範本體: ~/workspace/atlas-wiki/_internal/_completed-plans-2026-08.md §3（原 skill-competitive-sop-design-2026-08-22.md，2026-09-27 併入）
# 規則: 新增 SKILL.md 必含 competition_sop_decision frontmatter 欄位
# =============================================================================
def check_skill_competition_sop_decision(skills_dir: Path) -> List[Dict[str, Any]]:
    """Plan F Week 3 Day 4 R5: 新增 SKILL.md 必含 competition_sop_decision frontmatter

    規則:
      - SKILL.md frontmatter 必含 competition_sop_decision 區塊
      - 區塊必含欄位: overlap_score (0.0-1.0), decision (extend/new), proposal_ref
      - 缺欄位 → 違規

    暫不啟用 R5（auto_archive 也是 false）— 等 Plan F Week 3 Day 4 完全實作後開啟
    目前只記錄到 governance-log，由 LLM 在 session 中提示。
    """
    violations = []
    for skill_md in skills_dir.rglob("SKILL.md"):
        if "_archive" in str(skill_md):
            continue
        try:
            content = skill_md.read_text(encoding="utf-8")
            m = re.match(r"^---\n(.+?)\n---", content, re.DOTALL)
            if not m:
                continue
            fm = m.group(1)
            # 檢查 competition_sop_decision 區塊
            if "competition_sop_decision:" not in fm:
                # 暫不視為違規（剛開始推 SOP）
                logger.debug(f"R5 (soft): {skill_md.name} missing competition_sop_decision")
        except Exception:
            pass
    return violations
