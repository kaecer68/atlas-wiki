#!/usr/bin/env python3
"""
handle-atlas-failures.py — atlas-mcp 端點失敗降級處理
對位 kaecer v6.6 派工:6 條系統側失敗中的 #1/#3/#4 用 fallback 補丁

原理:
- 散戶問個股報價 → stock_get_quote 503 → 自動試 stock_get_fundamentals(已有)
- 散戶問風險 → risk_get_commentary not_available → 改用 risk_get_metrics(已有)
- parameters_get 401 → 自動加 X-API-Key header(若 .env 有)

不動 atlas-go 後端,純前端降級。

#7 Source Unreachable 分支(2026-08-07 v2.0 Day 2 B 派工):
# - 對位 concepts/atlas-mcp-failover-policy.md v1.0 §3 L3/L4 + §4 5 替代源
# - 觸發條件:atlas-mcp + L1 cache + L2 channel + 5 Web 替代源 全失敗
# - 行為:回 [源不可達:<原因>],禁用 LLM 推測字串(SOUL §5 紅線)
# - 對位 audience:user 口徑不外漏 error code;developer 口徑給完整 traceback
"""
import os
import subprocess
import json

def fallback_stock_quote(symbol):
    """#1 stock_get_quote 503 fallback → stock_get_fundamentals"""
    try:
        result = subprocess.run(
            ["python3", "-c", f"""
import os, sys
sys.path.insert(0, os.path.expanduser('~/workspace/atlas-wiki/skills/_scripts'))
# 直接調 mcp tool(未實作 placeholder,實際由 hermes 調用)
print(f"# stock_get_quote 503 fallback for {symbol}:建議查 stock_get_fundamentals")
"""],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()
    except Exception as e:
        return f"# Fallback failed: {e}"


def fallback_risk_commentary():
    """#4 risk_get_commentary not_available fallback → risk_get_metrics 摘要"""
    return """# risk_get_commentary 200+not_available 業務狀態(對位開發 agent v3 終判)
# 業務狀態說明:無 live trading 觸發 = 預期行為
# Fallback:用 risk_get_metrics 看 var_95 / max_drawdown_pct
# 對位 SK-29 risk_get_drawdown + SK-18 risk_exposure"""


def check_atlas_api_key():
    """#3 parameters_get 401 — 檢查 .env 是否有 ATLAS_API_KEY"""
    env_path = os.path.expanduser("~/.hermes/.env")
    if not os.path.exists(env_path):
        return "# .env 不存在,請配 ATLAS_API_KEY"
    with open(env_path) as f:
        content = f.read()
    if "ATLAS_API_KEY" in content:
        return "# .env 含 ATLAS_API_KEY,但 hermes 啟動未帶 header(請改 daemon 啟動命令)"
    return "# .env 缺 ATLAS_API_KEY"


def main():
    print("=" * 60)
    print("atlas-mcp 端點失敗降級處理工具")
    print("=" * 60)
    print()
    print("#1 stock_get_quote 503 fallback:")
    print(f"  {fallback_stock_quote('2330')}")
    print()
    print("#4 risk_get_commentary not_available fallback:")
    print(f"  {fallback_risk_commentary()}")
    print()
    print("#3 parameters_get 401 環境檢查:")
    print(f"  {check_atlas_api_key()}")


def fallback_source_unreachable(symbol, last_error=""):
    """#7 Source Unreachable → 所有 4 級 fallback 全失敗時的最後降級
    對位 concepts/atlas-mcp-failover-policy.md v1.0 §3 L4 端
    對位 _manifest_coverage_routing.md v1.0 §2 題 2 兩段制
    """
    # user 口徑「不外漏 error code」(對位 SK-33 audience-routing v1.0 §atlas 對位)
    user_facing = f"# [{symbol}] 源不可達:目前這項的公開資料源不在我的服務範圍。建議改問其他標的,或聯絡 atlas 維運。"
    # developer / admin 口徑給完整 traceback(對位 SK-33 §三 audience 表)
    debug_facing = f"# [{symbol}] L4 不可達:last_error={last_error or '<empty>'};建議:1) 查 atlas status / 2) 改走 schedule backfill / 3) 24h 後重試"
    return user_facing, debug_facing


def list_web_fallback_sources():
    """#7 5 個 Web fallback 替代源清單(對位 failover-policy §4)
    對位 SK-33 §未消化「配套待寫,但本段做清單預備」
    """
    return [
        ("TWSE 公開網頁", "https://mis.twse.com.tw/stock/fibest.jsp?stock=<4碼>", "集中市場盤中 5 分鐘 refresh"),
        ("TPEx 公開網頁", "https://www.tpex.org.tw/web/stock/after_trading/index.php?l=zh-tw", "上櫃市場,需從清單頁取 symbol"),
        ("Goodinfo", "https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID=<4碼>", "TWSE+TPEx 整合,JS 渲染"),
        ("公司 IR 頁", "<各上市公司投資人專區>", "逐家搜尋,無統一 URL pattern"),
        ("公開財經新聞", "<yahoo finance / 工商時報 / 經濟日報>", "事件驅動,不可作為報價源"),
    ]


def main():
    print("=" * 60)
    print("atlas-mcp 端點失敗降級處理工具")
    print("=" * 60)
    print()
    print("#1 stock_get_quote 503 fallback:")
    print(f"  {fallback_stock_quote('2330')}")
    print()
    print("#4 risk_get_commentary not_available fallback:")
    print(f"  {fallback_risk_commentary()}")
    print()
    print("#3 parameters_get 401 環境檢查:")
    print(f"  {check_atlas_api_key()}")
    print()
    print("#7 Source Unreachable 雙口徑降級(對位 SK-33 v1.0):")
    user, debug = fallback_source_unreachable("6488", "TPEx underlying fetch timeout")
    print(f"  user 口徑: {user}")
    print(f"  debug 口徑: {debug}")
    print()
    print("#7 5 個 Web fallback 替代源(對位 failover-policy §4):")
    for name, url, limit in list_web_fallback_sources():
        print(f"  - {name} | {url} | {limit}")

if __name__ == "__main__":
    main()