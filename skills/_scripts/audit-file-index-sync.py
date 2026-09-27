#!/usr/bin/env python3
"""
audit-file-index-sync.py — 驗證 wiki 內落檔是否被索引引用(2026-08-07 Day 2+3 CI 補)

對位 kaecer 2026-08-07「你有記得更新文件索引嗎?若是沒有,你需要在 CI 的程序中加入」

規則:
- skills/SK-*.md 必須在 SK-00-skill-index.md 引用
- concepts/entities/summaries/*.md 必須在 index.md 引用(queries、comparisons 兩區 2026-08-22 知識路由已遷移 atlas-notes)
- templates/trigger-*.md 必須在 README.md §12 trigger 清單
- skills/_scripts/*.py 必須在 README.md §CI 章節列

對位 v6.18 README + v6.20 7 jobs CI(擴至 8 jobs)
"""
import argparse
import os
import re
import sys
from pathlib import Path


def _default_root() -> Path:
    '''Repo root, resolved portably.

    歷史:本檔原本硬編 `~/workspace/atlas-wiki`。在 GitHub runner(或任何非本機 checkout)
    該路徑不存在 ⇒ 各類 glob 全空 ⇒ 印出 `✅ 0/0 …` ⇒ CI job **假綠**(2026-09-27 實證,
    PR #65 job log)。改為依序嘗試:
      1. 本檔所在位置往上兩層(標準 repo 佈局)
      2. 當前工作目錄
      3. 舊的硬編路徑(向後相容:腳本被複製到他處執行時)
    取第一個「含 skills/SK-00-skill-index.md」者;全部落空則回傳 (1),由 main() 的守衛報錯。
    '''
    candidates = [
        Path(__file__).resolve().parents[2],
        Path.cwd(),
        Path(os.path.expanduser('~/workspace/atlas-wiki')),
    ]
    for c in candidates:
        if (c / 'skills' / 'SK-00-skill-index.md').exists():
            return c
    return candidates[0]


ROOT = _default_root()


def read_text(path):
    try:
        return Path(path).read_text(encoding='utf-8')
    except Exception:
        return ''


def list_files(pattern):
    return sorted(Path(ROOT).glob(pattern))


def has_ref(content, file_path_rel):
    """true if content references file_path_rel by 完整路徑/base 名/SK-NN/trigger-NNN/script-name"""
    fp = str(file_path_rel).lstrip('/')
    if fp in content:
        return True
    base = Path(fp).name
    if base in content:
        return True
    # SK-NN
    m = re.search(r'(SK-\d{2})', base)
    if m and m.group(1) in content:
        return True
    # trigger-name
    m = re.search(r'(trigger-[\w-]+)', base)
    if m and m.group(1) in content:
        return True
    # script-name
    m = re.search(r'([a-z][\w-]+)\.py', base)
    if m and m.group(1) in content:
        return True
    return False


def audit(group_name, pattern, ref_file, kind):
    files = list_files(pattern)
    ref_content = read_text(ref_file)
    matched = []
    missing = []
    for f in files:
        rel = str(f.relative_to(ROOT))
        if has_ref(ref_content, rel):
            matched.append(f.name)
        else:
            missing.append((rel, f'{kind} 未引用'))
    return files, matched, missing


def main():
    global ROOT
    ap = argparse.ArgumentParser(description='驗證 wiki 內落檔是否被索引引用')
    ap.add_argument('--repo-root', default=None,
                    help='wiki repo 根目錄(預設:由本檔位置推導,見 _default_root())')
    args = ap.parse_args()
    if args.repo_root:
        ROOT = Path(args.repo_root).resolve()

    bad = []
    summary = []

    # 守衛(2026-09-27 反假綠):找不到 ref 檔或某一類 0 檔 ⇒ 直接失敗,
    # 不可再印 ✅ 0/0 後 exit 0(root 設錯/checkout 不完整時必須吵,不能靜默全綠)。
    ref_missing = [str(r) for r in (ROOT / 'skills/SK-00-skill-index.md', ROOT / 'index.md', ROOT / 'README.md') if not r.exists()]
    if ref_missing:
        print(f'repo: {ROOT}')
        print(f'❌ 找不到索引參照檔:{ref_missing} —— repo root 可能錯(用 --repo-root 指定)')
        return 1
    print(f'repo: {ROOT}')

    # 1. SK 頁 → SK-00
    files, m, miss = audit('SK', 'skills/SK-*.md', ROOT / 'skills/SK-00-skill-index.md', 'SK-00-skill-index.md')
    bad += miss
    summary.append(f'✅ {len(m)}/{len(files)} SK 頁在 SK-00 索引')

    # 2-6. 各目錄 → index.md
    for kind, pat in [('concepts', 'concepts/*.md'),
                     ('entities', 'entities/*.md'),
                     ('summaries', 'summaries/*.md')]:
        files, m, miss = audit(kind, pat, ROOT / 'index.md', 'index.md')
        bad += miss
        summary.append(f'✅ {len(m)}/{len(files)} {kind}/ 在 index.md 引用')

    # 7. trigger → README.md §12
    files, m, miss = audit('trigger', 'templates/trigger-*.md', ROOT / 'README.md', 'README.md §12')
    bad += miss
    summary.append(f'✅ {len(m)}/{len(files)} trigger 在 README.md §12 列出')

    # 8. _scripts/*.py → README.md §CI
    all_py = list_files('skills/_scripts/*.py')
    py_files = [f for f in all_py if '__pycache__' not in str(f) and '.bak' not in f.name]
    ref_md = read_text(ROOT / 'README.md')
    py_matched = []
    for f in py_files:
        rel = str(f.relative_to(ROOT))
        if has_ref(ref_md, rel):
            py_matched.append(f.name)
        else:
            bad.append((rel, 'README.md §CI 未引用'))
    summary.append(f'✅ {len(py_matched)}/{len(py_files)} _scripts/ 在 README.md §CI 列出')

    print('\n'.join(summary))
    print()
    if bad:
        print(f'❌ {len(bad)} 個檔未索引:')
        for f, why in bad:
            print(f'  - {f}: {why}')
        return 1
    print('✅ 所有 wiki 內檔均已索引(8 類 sync 通過)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
