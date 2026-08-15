#!/usr/bin/env bash
# install-hooks.sh — 安裝 atlas-wiki 的 git hooks
# 從 scripts/dev/hooks/<hook> 範本複製到 .git/hooks/<hook>
# 用法: ./scripts/dev/install-hooks.sh [uninstall]

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
HOOKS_DIR="$REPO_ROOT/.git/hooks"
TEMPLATES_DIR="$(dirname "$0")/hooks"

install_hook() {
    local name="$1"
    local src="$TEMPLATES_DIR/$name"
    local dst="$HOOKS_DIR/$name"
    if [ ! -f "$src" ]; then
        echo "❌ 範本 $src 不存在"
        exit 1
    fi
    cp "$src" "$dst"
    chmod +x "$dst"
    echo "✅ $name hook 已安裝"
}

uninstall() {
    for name in pre-commit pre-push commit-msg; do
        rm -f "$HOOKS_DIR/$name"
    done
    echo "🗑️  hooks 已解除"
}

case "${1:-install}" in
    install)   install_hook pre-commit; install_hook pre-push; install_hook commit-msg ;;
    uninstall) uninstall ;;
    *) echo "用法: $0 [install|uninstall]"; exit 1 ;;
esac

