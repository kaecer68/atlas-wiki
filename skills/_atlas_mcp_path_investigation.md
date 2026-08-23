# atlas-mcp 對外 HTTP 路由 — 盤查提示詞 v2

> **目標**:回答「`daily-atlas-health.py` 8:30 cron 跑時，怎麼打到 atlas-mcp 真實 backend」。
> **執行者**:kaecer(或 hermes 跑)
> **範圍**:只讀查證，不修任何 production 檔。
> **預期時間**:10-20 分鐘
> **回覆格式**:每個步驟的「回填區」段**整段貼回**(包括 `[空]` 的也要貼,讓我知道真有跑)
> **v2 修法**:從 v1 學到 — 移除硬寫假設的路徑、每步加 fallback、把 grep pattern 拆開、Step 1 改成讀 main.go 完整內容

---

## 現行有效結論（2026-07-30~08-03 查證結案,記錄於 _self-audit T3-A36）

- **atlas-mcp 在 18080 對外沒有可用的 MCP RPC 路徑**（`/` 301→/client/、`/mcp`、`/api/mcp*`、`/api/v1/mcp` 全 404/route not found,皆非 MCP endpoint）
- **atlas-mcp = stdio-only**:真正 MCP call 走 hermes daemon 內部 stdin/stdout pipe（mcp_stdio_watchdog PID 70257 → atlas-mcp PID 70258）
- **`daily-atlas-health.py` 從設計起就用錯 transport 假設** — 需 disable cron 或改寫（非 wiki 層可修）
- 判定框架:Step 6 三條路徑 A/B/C（見下）

## Step 6 — 三條路徑(寫前等的最終判斷)

跑完 Step 0-5,你看情境判定:

| 情境 | S3 結果 | S4 結果 | 路徑 |
|------|---------|---------|------|
| **A. atlas-mcp 對外 HTTP 在** | 有一個 path 回 200+JSON | 不重要 | 直接修 daily-atlas-health.py,把 `BASE = "127.0.0.1:18080/mcp"` 改成真實 path |
| **B. atlas-mcp 只走 stdio** | 全 404 | watchdog cmdline 含 atlas-mcp binary | `daily-atlas-health.py` 從根本上不能用 — 拍板 disable cron 或改寫用 atlas-mcp 二進制直接調用 |
| **C. 我原本的 (a)(b) 修法部分生效但路由錯** | 同 B | bearer 注入成功但路徑不對 | 同 B |

### 最終回報格式(把判斷 + 證據送出):

```
【S0】date/which hermes/version 全部輸出
【S1】file/ls-la/main.go 完整內容(把整個 main.go 貼出來,不要只 grep)
【S2】ls server/ 完整 + server.go head 60 行 + 四組 grep(每組含 fallback 行)+ tools.go head 40 行
【S3】7 個 endpoint 各自的 curl 完整輸出
【S4】config.yaml 結果 + agents/ 結果 + 2 個 PID cmdline
【S5】atlas-go cmd/ + 兩組 grep(每組含 fallback 行)
【最終判斷】A / B / C
【你建議】該怎麼處理(換 path / disable cron / 改架構 / 其他)
```

---

## 我這邊等你回答後會做什麼:

收到你回報後,我:
1. **若 S3 找到真實 path** → 我修 `daily-atlas-health.py` 路徑 + 重測
2. **若 S4 確認 stdio only** → 跟你提的是「disable 0cb1d0e9fb15 cron」還是「改架構」決定
3. **若其他** → 我接著查

**不會自己再跳探路徑** — 等你的答案。

---


> **調查過程全文**（通用提示 + Step 0-5 + v2 改進記錄）已 byte-preserving 歸檔 → [[_archive/_atlas_mcp_path_investigation_history.md]] [2026-08-22 iter2]
