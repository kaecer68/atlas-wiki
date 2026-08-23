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
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.path.expanduser('~/workspace/atlas-wiki'))


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
    bad = []
    summary = []

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
