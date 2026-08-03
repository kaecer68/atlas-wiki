# Makefile — atlas-wiki

> 本機先跑、綠了才 push,避免 GitHub Actions 來回空等。
> 對位 CLAUDE.md §「CI preflight gate」。

## 快速上手

```bash
make ci-gate               # 5 項檢查全綠(本機 0.5-1 秒)
make pre-commit-install    # 裝 pre-commit + pre-push hook(之後全自動)
```

完整說明見 [`docs/git-merge-protocol.md`](docs/git-merge-protocol.md)。

## 為何本地預檢

| 檢查 | GitHub CI | 本地 make ci-gate |
|------|-----------|-------------------|
| 速度 | 30-60 秒 | 0.5-1 秒 |
| 失敗定位 | log 查 | 直接 terminal |
| 來回成本 | push → 等 → 失敗 → 修 → 再 push → 再等 | 修 → 再跑 |
| Token 消耗 | 大 | 微 |

**結論**:每次 push 前必跑 `make ci-gate`(或用 pre-push hook 自動)。

## Targets

```
make help                 # 列所有 target
make ci-gate              # 5 項本地預檢
make check-timestamp      # 第 5 條鐵律
make check-audit          # atlas-mcp 端點
make check-size           # SK ≤ 9000 bytes
make check-frontmatter    # 10 欄齊全
make check-actionlint     # workflow YAML(需 actionlint)
make pre-commit-install   # 裝 git hooks
make uninstall-hooks      # 解除 hooks
make verify-clean         # 收尾無暫存污染
```

## 對位 CLAUDE.md CI preflight gate

| CLAUDE.md §  | atlas-wiki 對位 |
|--------------|-----------------|
| `make ci-gate`(atlas-go 版含 gofmt / go build / go vet) | `make ci-gate`(純 Python/Markdown,5 項檢查) |
| `make ci-full`(atlas-go 版含 golangci-lint / staticcheck / go test) | `make ci-full`(等同 ci-gate,無 Go 對位項) |
| 修改 .go / .ts / .tsx 後必跑 ci-gate | 修改 .py / .md / .yml 後必跑 ci-gate |

## 何時不適用

- 純文檔單行修正(影響小)——可跳過 ci-gate,但 pre-push hook 仍會跑
- CI 工作流本身壞掉導致 ci-gate 無法跑——用 `SKIP_CI_GATE=1 git push`,push 後 GitHub CI 最終驗證
