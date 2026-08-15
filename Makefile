# atlas-wiki Makefile
# 對位 CLAUDE.md §「CI preflight gate」(atlas-go 版) — atlas-wiki 的 Python 等價
# 設計:本機先跑、綠了才 push,避免 GitHub Actions 來回空等。

SHELL := /bin/bash
PY    := python3

.PHONY: help ci-gate ci-fast ci-full check-actionlint check-timestamp check-audit check-skill-pages check-size check-frontmatter pre-commit-install uninstall-hooks verify-clean test sync-imac

help:                   ## 列出所有 target
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  %-22s %s\n", $$1, $$2}'

ci-gate:                ## 快速門禁(對位 GitHub CI 4 job)
ci-gate: check-timestamp check-audit check-size check-frontmatter check-actionlint
	@echo ""
	@echo "✅ local ci-gate: all 5 checks passed"

ci-fast: ci-gate        ## 別名

ci-full: ci-gate        ## 完整(對位 GitHub Actions 全部 local 化檢查;現等同 ci-gate)
	@echo "ℹ️  ci-full 等於 ci-gate(atlas-wiki 純 Python/Markdown,無 Go/go generate/golangci-lint 對位項)"

check-timestamp:        ## 1. 第 5 條鐵律 timestamp 驗證
	@$(PY) skills/_scripts/validate-timestamp-rule.py --skills-dir skills

check-audit:            ## 2. atlas-mcp 端點 audit
	@$(PY) skills/_scripts/audit-atlas-endpoints.py

check-skill-pages:      ## 內部 target:一次跑 size + frontmatter(被 size/frontmatter 共用)
	@$(PY) skills/_scripts/check-skill-pages.py --skills-dir skills

check-size:             ## 3. SK 頁大小 ≤ 9000 bytes
check-size: check-skill-pages

check-frontmatter:      ## 4. frontmatter 核心 10 欄齊全
check-frontmatter: check-skill-pages
check-actionlint:       ## 5. workflow YAML lint(本地端,可選)
	@if command -v actionlint >/dev/null 2>&1; then \
	  actionlint .github/workflows/validate-wiki.yml; \
	else \
	  echo "⚠️  actionlint 未安裝(brew install actionlint),跳過此項。CI 仍會跑。"; \
	fi

pre-commit-install:     ## 安裝 git hooks(commit 預檢 + push 預檢)
	@./scripts/dev/install-hooks.sh

uninstall-hooks:        ## 解除 git hooks
	@./scripts/dev/install-hooks.sh uninstall

verify-clean:           ## 收尾前檢查(無 .bak/__pycache__/未追蹤敏感檔)
	@echo "=== 應排除的暫存(不得出現) ==="
	@git ls-files | grep -E "\.bak|__pycache__|\.DS_Store" || echo "✅ 無暫存污染"

test:                   ## 跑 trigger-monitor pytest(對位 v0.5 F 議題 5/5 case 永久化)
	@$(PY) -m pytest skills/_scripts/tests/ -v

# ---- 雙機同步 (2026-08-15) ----

sync-imac: ## 同步 iMac atlas-wiki clone (a2a-sync)
	@echo "→ 同步 GitHub → iMac (atlas-wiki)"
	@~/bin/a2a-sync
	@echo "✓ 完成"
