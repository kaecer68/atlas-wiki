---
title: atlas-mcp 對外 HTTP 路由 — 盤查提示詞 v2（調查過程/歷史歸檔）
type: audit-archive
purpose: _atlas_mcp_path_investigation.md 瘦身時 byte-preserving 歸檔（Step 0-5 調查過程 + v2 改進記錄,歷史已結算）
created: 2026-08-22
created_by: iter2 方法論審計結案工人
archive_of: ~/workspace/atlas-wiki/skills/_atlas_mcp_path_investigation.md（盤查提示詞 v2）
conclusion_ref: skills/_self-audit.md T3-A36（atlas-mcp stdio-only 結論）
---

> 對位 `_method.md` 第七條例外模式（_inbox_archive 同款）:調查過程/歷史段歸檔,主檔保留現行有效結論 [2026-08-22 iter2]

# 調查過程全文（byte-preserving）

## 通用提示 — 寫滿回填區

每個步驟都有「回填區」。**不要**只貼結果,也不要只貼「無輸出」 — **把命令輸出整段貼進去**(`<empty output>` 也算回報)。否則我無從判斷「命令失敗」還是「真的沒有」。

---

## Step 0 — 環境確認

### 指令:

```bash
echo "DATE: $(date)" && \
echo "USER: $(whoami)" && \
echo "WD: $(pwd)" && \
echo "HERMES: $(which hermes 2>&1)" && \
hermes --version 2>&1 | head -3
```

### 回填區(S0):

```
【date 輸出】
【which hermes 輸出】
【hermes --version 輸出】
```

---

## Step 1 — atlas-mcp binary 性質(不是 grep pattern)

### 指令:

```bash
echo "===1a. file type===" && \
file /Users/kaecer/workspace/atlas/bin/atlas-mcp 2>&1 && \
echo "---" && \
echo "===1b. ls -la===" && \
ls -la /Users/kaecer/workspace/atlas/bin/atlas-mcp 2>&1 && \
echo "---" && \
echo "===1c. **完整** main.go(不是 grep)===" && \
cat /Users/kaecer/workspace/atlas/cmd/atlas-mcp/main.go 2>&1 | head -120
```

### 回填區(S1):

```
【1a file 輸出】
【1b ls -la 輸出】
【1c main.go 完整內容(前 120 行)】
```

### 判定門檻:

- `main.go` 開頭 imports 顯示用 `modelcontextprotocol/go-sdk` 或 `mcp-go` SDK → atlas-mcp 是用 SDK 寫的
- `main` 函式裡 `os.Args` / flag 解析後,呼叫了什麼:
  - `server.ServeStdio(...)` 或 `mcp.NewServer(...).ServeStdio()` → **stdio only**,不會開 HTTP
  - `http.ListenAndServe(addr, handler)` → 會開 HTTP,但路徑在 handler 內(繼續 Step 2)
  - `mcp.NewServer(...).ServeHTTP` → 不開 HTTP,需外部 mux 包

讀完貼出完整 main.go 即可判定。

---

## Step 2 — atlas-mcp server 程式結構(完整目錄 + 入口檔)

### 指令:

```bash
echo "===2a. ls server/ 全目錄===" && \
ls -la /Users/kaecer/workspace/atlas/cmd/atlas-mcp/server/ 2>&1 | head -30 && \
echo "---" && \
echo "===2b. server.go 完整 head(60 行)===" && \
head -60 /Users/kaecer/workspace/atlas/cmd/atlas-mcp/server/server.go 2>&1 && \
echo "---" && \
echo "===2c. 找 routing 檔案(每個 === 內單獨跑,不要管 grep 失敗)===" && \
echo "**Step 2c-1** chi.NewRouter:" && \
grep -n "chi\\.NewRouter\\|chi/v5" /Users/kaecer/workspace/atlas/cmd/atlas-mcp/server/*.go 2>/dev/null || echo "(grep failed or no match)" && \
echo "" && \
echo "**Step 2c-2** http.NewServeMux:" && \
grep -n "http\\.NewServeMux\\|ServeMux" /Users/kaecer/workspace/atlas/cmd/atlas-mcp/server/*.go 2>/dev/null || echo "(grep failed or no match)" && \
echo "" && \
echo "**Step 2c-3** router.Handle / .HandleFunc:" && \
grep -n "router\\.Handle\\|\\.HandleFunc" /Users/kaecer/workspace/atlas/cmd/atlas-mcp/server/*.go 2>/dev/null || echo "(grep failed or no match)" && \
echo "" && \
echo "**Step 2c-4** tools.go 開頭 40 行:" && \
head -40 /Users/kaecer/workspace/atlas/cmd/atlas-mcp/server/tools.go 2>&1
```

### 回填區(S2):

```
【2a ls server/ 輸出】
【2b server.go head 60 行】
【2c-1 grep chi 結果,連 "(grep failed or no match)" 也貼】
【2c-2 grep ServeMux 結果,連 "(grep failed or no match)" 也貼】
【2c-3 grep Handle 結果,連 "(grep failed or no match)" 也貼】
【2c-4 tools.go head 40 行】
```

### 判定門檻:

從 2c-4 (tools.go head) 即可看出:
- 若看到 `mcp.AddTool(mcpSrv, tool, handler)` 形式 → 用 Go MCP SDK;tool 是 **SDK 內註冊**,不暴露 HTTP path
- 若看到 `http.HandleFunc("/path/...", handler)` → MCP server 把 handler 註冊到 http.Server,有對外 path

具體路徑在 main.go(Step 1c)會呼叫什麼樣的 handler wrapper,如果 main.go 的 main 函式結尾用 `http.ListenAndServe(":18080", someHandler)`,那 `someHandler` 在哪定義的 path 就對外提供 — 答案在 server.go / router.go 之中。

---

## Step 3 — 直接試 HTTP endpoint(多 path,但**每個用獨立 sed 測**)

懷疑會是其中之一,逐個試,**不要用 for-loop 一鍋出**(便於每個獨立貼回):

### 指令:

```bash
KEY=$(grep "^ATLAS_API_KEY=" ~/.config/atlas-wiki/.env 2>/dev/null | cut -d= -f2-)
echo "KEY length chars: $(echo -n "$KEY" | wc -c)"
echo "(若 KEY length 是 0,表示 .env 沒讀到,先查證 .env 路徑)"
echo ""

# 每個 path 獨立驗證;回填每行 [HTTP xxx]

echo "===3-POST-1: /mcp==="
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${KEY}" \
  -d '{"method":"tools/list","params":{}}' \
  http://127.0.0.1:18080/mcp -w "\n[HTTP %{http_code}]\n"
echo ""

echo "===3-POST-2: /api/mcp==="
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${KEY}" \
  -d '{"method":"tools/list","params":{}}' \
  http://127.0.0.1:18080/api/mcp -w "\n[HTTP %{http_code}]\n"
echo ""

echo "===3-POST-3: /api/mcp/tools/list==="
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${KEY}" \
  -d '{"method":"tools/list","params":{}}' \
  http://127.0.0.1:18080/api/mcp/tools/list -w "\n[HTTP %{http_code}]\n"
echo ""

echo "===3-POST-4: /api/mcp/tools/call==="
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${KEY}" \
  -d '{"method":"system_get_health","params":{}}' \
  http://127.0.0.1:18080/api/mcp/tools/call -w "\n[HTTP %{http_code}]\n"
echo ""

echo "===3-POST-5: /api/v1/mcp==="
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${KEY}" \
  -d '{"method":"tools/list","params":{}}' \
  http://127.0.0.1:18080/api/v1/mcp -w "\n[HTTP %{http_code}]\n"
echo ""

echo "===3-GET-1: /=/(web server 入口探測)==="
curl -s -X GET http://127.0.0.1:18080/ -w "\n[HTTP %{http_code}]\n" 2>&1 | head -c 300
echo ""

echo "===3-GET-2: /client/(301 redirect 目標)==="
curl -s -X GET http://127.0.0.1:18080/client/ -w "\n[HTTP %{http_code}]\n" 2>&1 | head -c 200
```

### 回填區(S3):**每個 path 完整輸出**,含 `[HTTP xxx]` 與 response body。

```
【3-POST-1: /mcp】...
【3-POST-2: /api/mcp】...
【3-POST-3: /api/mcp/tools/list】...
【3-POST-4: /api/mcp/tools/call】...
【3-POST-5: /api/v1/mcp】...
【3-GET-1: /】...
【3-GET-2: /client/】...
```

### 判定門檻:

看 `3-POST-*` 哪一個回 `200 OK` + JSON 帶 `"result"` 或 `"tools"` 陣列 → **找到真實路徑**。
若全部 404 + atlas 自家 JSON `{"code":"404","error":"route not found"}` 或 Go stdlib 404 → **atlas-mcp **不對外** 開放 MCP HTTP RPC**。

注意判別:`{"code":"404","error":"route not found"}` 是 atlas 自己寫的 response(有 routing framework);Go stdlib 預設回 `404 page not found` 是不同字串 — 這是「哪個 framework 處理這個 path」的判斷依據。

---

## Step 4 — hermes daemon 怎麼接 atlas-mcp

### 指令:

```bash
echo "===4a. config.yaml 若有===" && \
ls -la /Users/kaecer/.hermes/config.yaml 2>&1 && \
echo "" && \
echo "===4b. config.yaml 內 atlas-mcp 相關段===" && \
grep -nE "atlas|mcp_stdio|MCP_STDIO|stdio_watchdog" /Users/kaecer/.hermes/config.yaml 2>/dev/null | head -20 || echo "(config.yaml not found or no match)"
echo "" && \
echo "===4c. ~/.hermes/hermes-agent/agents/ 是否存在===" && \
ls -la /Users/kaecer/.hermes/hermes-agent/agents/ 2>&1 | head -20
echo "" && \
echo "===4d. agents/ 內找 atlas MCP 設定===" && \
grep -rln "atlas-mcp" /Users/kaecer/.hermes/hermes-agent/ 2>/dev/null | head -10 || echo "(no match)"
echo "" && \
echo "===4e. 若找到,看對應檔===" && \
ls -la /Users/kaecer/.hermes/hermes-agent/agents/*.json 2>/dev/null | head -10
echo "" && \
echo "===4f. process 真實 cmdline(PID 70258 是 atlas-mcp)===" && \
ps -o pid,ppid,command -p 70258 2>&1
echo "" && \
echo "===4g. process 真實 cmdline(PID 70257 是 mcp_stdio_watchdog)===" && \
ps -o pid,ppid,command -p 70257 2>&1
```

### 回填區(S4):

```
【4a ls config.yaml】...
【4b grep atlas-mcp in config.yaml】...
【4c ls agents/】...
【4d grep atlas-mcp in agents/】...
【4e agents/*.json】...
【4f PID 70258 cmdline】...
【4g PID 70257 cmdline】...
```

### 判定門檻:

看 4f + 4g 兩個 PID 的 cmdline:
- 若 atlas-mcp 是以 stdio pipe 啟動(從 watchdog → atlas-mcp binary) → 它**沒有對外 HTTP**
- 若 atlas-mcp 帶 `--port 18080` 或類似 → 有對外但需看是否為 MCP endpoint

看 4b 若 config.yaml 沒 atlas 設定 + 4d grep 無結果 → hermes 是用「專屬 watchdog 進程」介接,不走 config 設定。

---

## Step 5 — atlas-go 主程式有沒有反代

懷疑:即使 atlas-mcp 走 stdio,但 atlas-go 主程式(web UI 那個)有可能反代 MCP 給 client。

### 指令:

```bash
echo "===5a. atlas-go cmd 結構===" && \
ls /Users/kaecer/workspace/atlas/cmd/ 2>&1
echo "" && \
echo "===5b. 找 atlas-go 是否 MCP-aware===" && \
grep -rln "mcp_anomaly\|MCP_PROXY\|mcpProxy\|ReverseProxy" /Users/kaecer/workspace/atlas/internal/ /Users/kaecer/workspace/atlas/cmd/atlas/ 2>/dev/null | head -10 || echo "(no match)"
echo "" && \
echo "===5c. 找 atlas-go main router 是否有 /mcp path===" && \
grep -rn '"/mcp"\|"/api/mcp"\|"/mcp/' /Users/kaecer/workspace/atlas/cmd/atlas/main.go /Users/kaecer/workspace/atlas/cmd/atlas/router*.go /Users/kaecer/workspace/atlas/internal/server* 2>/dev/null | head -10 || echo "(no match)"
```

### 回填區(S5):

```
【5a ls cmd/】...
【5b grep mcp-aware in atlas-go】...
【5c grep /mcp path in atlas-go router】...
```

### 判定門檻:

5b/5c 全無 → atlas-go 不代理 MCP,18080 HTTP server 純 web UI + API 業務,不開放 MCP RPC。

---



---

# v2 改進記錄（原始全文,byte-preserving）

## v2 改進記錄(給自己看的)

相比 v1,kacer 抓出 6 條問題:
1. **硬寫路徑的 grep 指令** → v2 每個 grep 都加 `|| echo "(grep failed or no match)"` fallback
2. **Step 1c grep 七個 pattern 混用** → v2 改成讀 main.go 完整內容(60 行 head)
3. **絕對路徑無 fallback** → v2 內部一致用 `/Users/kaecer/workspace/atlas/...`,提醒這是內部盤查限制
4. **Step 4 假設 hermes 結構** → v2 改成「先 ls 看是否存在,再 grep」
5. **缺 main.go 完整 dump** → v2 Step 1 改成 cat 完整 + 2b server.go 完整 head
6. **預設結論** → v2 結尾改成「三條路 A/B/C 由你判定」

修法主軸:**把所有「我已查過的部分路徑當獨立事實」改回「先驗證再依賴」**。

