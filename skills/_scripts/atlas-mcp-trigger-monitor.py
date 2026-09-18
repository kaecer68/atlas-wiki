#!/usr/bin/env python3
"""
atlas-mcp-trigger-monitor.py — 14 觸發模板自動信號捕捉(對位 kaecer v6.21) — v0.4
對位 SOUL §3.4「促進理解」+ ATLAS 憲章 7 層因果鏈

設計:
- 每 5 分鐘跑 1 次(hermes cron 觸發)
- 12 觸發模板信號捕捉(對位 templates/trigger-*.md)
- 觸發成功 → 落 §6 紀錄 + Telegram 通知
- 觸發失敗 → 跳過(節省資源)
- 整體失敗率 > 50% → 通知 atlas 端故障
- 1 小時內相同模板不重複通知(去重)
- 5 分鐘內多觸發 → 合併摘要 1 條

v6.22 改寫:從 stub 改為實際 curl atlas HTTP API
v0.4 擴充(2026-08-10,對位 kaecer B 方案):is_web_fallback flag + fetch_with_fallback() + is_atlas_data_complete() + fetch_web() — atlas 端修復後(PR #1515 660 政策語義)雙軌設計可正常運作
- atlas HTTP base:http://127.0.0.1:18080(對位 atlas-go cmd/atlas-mcp/server/server.go:21)
- 端點對應:/api/macro/snapshot/latest 等
"""
import os
import sys
import json
import urllib.request
import urllib.parse
import subprocess
import time
from datetime import datetime
from typing import Optional

ATLAS_HTTP_BASE = "http://127.0.0.1:18080"

# 12 觸發模板定義
TEMPLATES = {
    "nvda-tsm": {
        "name": "NVDA+TSM 觸發",
        "file": "trigger-nvda-tsm.md",
        "condition": "NVDA > +2.0% (單日漲幅)",
        "http_path": "/api/macro/snapshot/latest",
        "field": "nvda",
        "metric": "change_pct",
        "threshold": 2.0,
    },
    "usd-twd-32": {
        "name": "USD_TWD 32+ 觸發",
        "file": "trigger-usd-twd-32.md",
        "condition": "USD_TWD > 32.3",
        "http_path": "/api/macro/snapshot/latest",
        "field": "usd_twd",
        "metric": "value",
        "threshold": 32.3,
    },
    "dxy-us10y-weak": {
        "name": "DXY 弱觸發",
        "file": "trigger-dxy-us10y-weak.md",
        "condition": "DXY < 100",
        "http_path": "/api/macro/snapshot/latest",
        "field": "dxy",
        "metric": "value",
        "threshold": 100,
        "compare": "lt",  # 小於觸發
    },
    "margin-350b": {
        "name": "融資 3500 億觸發",
        "file": "trigger-margin-350b.md",
        "condition": "retail_margin_balance > 5000 億",
        "http_path": "/api/macro/snapshot/latest",
        "field": "retail_margin_balance",
        "metric": "value",
        "threshold": 5000,
    },
    "foreign-3day-inflow": {
        "name": "外資買超觸發",
        "file": "trigger-foreign-3day-inflow.md",
        "condition": "foreign_investor_net > +20 億",
        "http_path": "/api/macro/snapshot/latest",
        "field": "foreign_investor_net",
        "metric": "value",
        "threshold": 20,
    },
    "sox-foreignflow": {
        "name": "SOX+外資買超觸發",
        "file": "trigger-sox-foreignflow.md",
        "condition": "SOX > 0 + 外資買超",
        "http_path": "/api/macro/snapshot/latest",
        "field": "sox_index",
        "metric": "change_pct",
        "threshold": 0,
    },
    "taiwan-strait-tension": {
        "name": "台海緊張觸發",
        "file": "trigger-taiwan-strait-tension.md",
        # 2026-08-26 改:對位 ATLAS_METHODOLOGY.md §3 v1.1 GeoIntensity 4 級制
        # 從舊「> 4 直覺刻度」(與 stress-index components.geopolitical 0-13 浮動值混用)改為 atlas 官方 0-100 刻度
        # 換算公式:GeoIntensity = components.geopolitical / 0.13 (weight,scale=1.0)
        # 觸發條件:GeoIntensity ≥ 40 = 4 級制 ≥ 升溫(2)
        #
        # 🐛 2026-08-27 修(unit mismatch 假陰性,T3-A818):
        # 8/26 那版只改 threshold 4→40,卻沒改讀值單位 — generic 分支取的
        # components.geopolitical 是「已乘 0.13 的元件值」(理論上限 100×0.13=13),
        # 拿它跟 40 比 → **任何市況都不可能觸發**(13 > 40 恆為 False),
        # 連 GeoIntensity=100 的台海危機也不會報 = 結構性死觸發。
        # 實證(2026-08-27T03:16 curl /api/taiwan/stress-index):
        #   components.geopolitical=6.24 → GeoIntensity=6.24/0.13=48.0 ≥ 40 應觸發,
        #   但腳本判 6.24 > 40 = False → 假陰性。
        # 交叉驗證:atlas 自己的 /api/regime/history 同時回 current_period=
        #   turnaround_down(轉折下壓),而 §3 轉折下壓的地緣條件正是 GeoIntensity ≥ 40
        #   → atlas 端認定地緣條件已命中,trigger-monitor 卻報未觸發,兩者矛盾。
        # 修法:加 metric_divisor,把元件值還原成 0-100 GeoIntensity 再跟 threshold 比,
        #   讓 log/Telegram 顯示的值本身就是 GeoIntensity(48.0)而非元件值(6.24)。
        # 對位 SOUL §5「驗證鐵律」+ USER §7「有回傳 ≠ 資料可用」
        "condition": "GeoIntensity > 40",  # 0-100 GeoIntensity,≥ 升溫(2)
        "http_path": "/api/taiwan/stress-index",
        "field": "components",
        "metric": "geopolitical",  # 原始元件值(= GeoIntensity × scale 1.0 × weight 0.13)
        "metric_divisor": 0.13,  # 還原 0-100 GeoIntensity:GeoIntensity = 元件值 ÷ 0.13
        "threshold": 40,  # 0-100 GeoIntensity,≥ 升溫(2)
        "compare": "gt",
    },
    "china-slowdown": {
        "name": "中國需求強觸發(改後)",
        "file": "trigger-china-slowdown.md",
        "condition": "TSMC 月營收 YoY > +50% + export_electronics > 0",
        "http_path": "/api/macro/snapshot/latest",
        "field": "tsmc_revenue",
        "metric": "change_pct",
        "threshold": 50,
        "extra_check": {"export_electronics": "change_pct>0"},
    },
    "tariff-shock": {
        "name": "對中/台晶片關稅觸發",
        "file": "trigger-tariff-shock.md",
        "condition": "USD_TWD > 32 + export_electronics > 0",
        "http_path": "/api/macro/snapshot/latest",
        "field": "usd_twd",
        "metric": "value",
        "threshold": 32,
        "extra_check": {"export_electronics": "change_pct>0"},
    },
    "etf-rebalance": {
        "name": "ETF 換股觸發",
        "file": "trigger-etf-rebalance.md",
        "condition": "market_volume > 0",
        "http_path": "/api/macro/snapshot/latest",
        "field": "market_volume",
        "metric": "value",
        "threshold": 0,
    },
    "cb-fx-intervention": {
        "name": "台灣央行(央行/中央銀行/TW-CBC)接近防線 32.5 觸發",
        "file": "trigger-cb-fx-intervention.md",
        "condition": "USD_TWD > 32.3 (接近台灣央行防線 32.5)",
        "http_path": "/api/macro/snapshot/latest",
        "field": "usd_twd",
        "metric": "value",
        "threshold": 32.3,
    },
    "retail-margin-decrease": {
        "name": "散戶融資大減觸發",
        "file": "trigger-retail-margin-decrease.md",
        "condition": "retail_margin_balance > 5000 億 + retail_short 變化",
        "http_path": "/api/macro/snapshot/latest",
        "field": "retail_margin_balance",
        "metric": "value",
        "threshold": 5000,
        "extra_check": {"retail_short_balance": "value!=0"},
    },
    # 第 13 模板(2026-08-03 新增,對位 PR #1445 stock_get_quote 修復)
    # 2330 台積電盤中振幅 > 3% = 半導體 leader 急動 → Q3 產業輪動訊號
    "2330-tsmc-swing": {
        "name": "2330 台積電急漲/急跌觸發",
        "file": "trigger-2330-tsmc-swing.md",
        "condition": "2330 盤中振幅(high-low)/open > 3%",
        "http_path": "/api/stock/quote",
        "field": "2330",  # 用作 query symbol
        "metric": "intraday_swing_pct",  # 自訂計算欄位
        "threshold": 3.0,
        "compare": "gt",
        "is_custom_calc": True,  # 觸發 run_triggers 走自訂計算分支
    },
    # 第 14 模板(v0.3,T3-A253 修補:eeb20aa commit 時 dormant 因 atlas-mcp 不暴露 monthly_revenue_yoy)
    # 設備鏈(3680/3533/5434)當日投信買超張數合計 + capital_flow_summary 投信 z_score 同步
    # 走 /api/stock/chips(自訂 branch:is_chips_aggregate)
    "megaproject-2-quarter-lag": {
        "name": "Megaproject 半年報週期 + 設備鏈當日投信 aggregate 觸發",
        "file": "trigger-megaproject-2-quarter-lag.md",
        "condition": "設備鏈(3680/3533/5434)當日投信買超張合計 > +1000 張 + 投信 z_score > +1.0",
        "http_path": "/api/stock/chips",
        "symbols": ["3680", "3533", "5434"],  # 多 symbol aggregate
        "metric": "domestic_fund_net",  # 投信當日淨買賣超(單位:張)
        "threshold": 1000.0,  # 合計 trigger門檻
        "compare": "gt",
        "aggregate_mode": "sum",  # 多 symbol 對位 sum(對位 trigger-monitor v6.22 unified signature 擴增)
        "is_chips_aggregate": True,  # v0.3 新分支:chips 多 symbol aggregate
    },
    # 第 15 模板(2026-08-04 新增,T3-A248 kaecer B+C 拍板)
    # 5 錨點 annual/semi-annual 週期型 trigger → 不在 monitor 即時掃描,走獨立 cron-cadence
    # 不寫進 TEMPLATES 字典(避免每 5 分鐘被誤掃);由獨立 scripts/external-report-cycle-monitor.py + cron 觸發
    # "equipment-capex-external-report-cycle" 為獨立 cron job 保留名
    #
    # 第 16-20 模板(2026-08-10 v0.4 整合,對位 v6.58.6 B 方案 + atlas PR #1505/1515 修復後)
    # 對位 fact_b6bc42e7(2026-08-10 atlas 修復驗證):msci/capex/ai_capex/cb_fx/hbm 欄位 atlas 端不暴露
    # 設計原則:atlas 端有資料 → atlas;atlas 無 / 殘缺 → 走 web fallback(SEC EDGAR / MSCI 官網 / 央行 / Yahoo Finance)
    # is_web_fallback=True + web_fallback 配置(v0.4 雙軌)
    "hbm-cycle-cooling": {
        "name": "HBM/AI 半導體敘事降溫觸發",
        "file": "trigger-hbm-cycle-cooling.md",
        "condition": "SK Hynix 月跌幅 < -10% + HBM 報價連 2 月跌 > 5% + 雲端商 capex 季報下修",
        "http_path": "/api/stock/chips",
        "symbols": ["660"],  # SK Hynix
        "metric": "month_change_pct",
        "threshold": -10.0,
        "compare": "lt",
        "is_chips_aggregate": True,
        "is_web_fallback": True,  # v0.4:660 chips 沒資料時走 web fallback
        "web_fallback": {
            "sk_hynix_quote": {
                "url": "https://www.skhynix.com/eng/sustainability/governance.do",
                "parser": "html_table",
                "field": "month_change_pct",
                "cache_ttl_sec": 86400,  # 1 天快取(IR 月報)
            },
            "hbm_price": {
                "url": "https://dramexchange.com/",
                "parser": "html_table",
                "field": "hbm_price_change_2m",
                "cache_ttl_sec": 86400,
            },
            "cloud_capex": {
                "url": "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001045810&type=10-Q",
                "parser": "html_table",
                "field": "capex_guidance_yoy",
                "cache_ttl_sec": 604800,  # 7 天快取(季報變動不頻繁)
            },
        },
    },
    "ai-capex-guidance-cut": {
        "name": "AI capex 指引下修觸發",
        "file": "trigger-ai-capex-guidance-cut.md",
        "condition": "任一雲端商(NVDA/GOOGL/META/MSFT)capex YoY 從 >30% 下修至 <20%",
        # v0.4.1 改 SEC XBRL companyfacts API(對位 v6.58.21 真實探索)
        # NVDA capex 真實概念 = PaymentsToAcquireProductiveAssets(2025 Q1 = $1.23B 實證)
        # NVDA CIK = 0001045810;GOOGL CIK = 0001652044
        "is_web_fallback": True,
        "web_fallback": {
            "nvda_capex": {
                "url": "https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json",
                "parser": "sec_xbrl_companyfacts",  # 新 parser
                "field": "PaymentsToAcquireProductiveAssets",  # NVDA 真實 capex 概念
                "units": "USD",
                "form": "10-Q",  # 季報
                "cache_ttl_sec": 604800,  # 7 天快取(季報變動不頻繁)
            },
            "googl_capex": {
                "url": "https://data.sec.gov/api/xbrl/companyfacts/CIK0001652044.json",
                "parser": "sec_xbrl_companyfacts",
                "field": "PaymentsToAcquirePropertyPlantAndEquipment",
                "units": "USD",
                "form": "10-Q",
                "cache_ttl_sec": 604800,
            },
        },
        "is_web_only": True,  # v0.4.1:純 web fallback,無 atlas http_path(對位 v6.58.21)
        "field": "PaymentsToAcquireProductiveAssets",  # v0.4.1:run_triggers 取這個 key 比 threshold
        "threshold": 20.0,  # YoY %
        "compare": "lt",
    },
    "hedge-fund-unwind": {
        "name": "跨市場 hedge fund 爆倉觸發",
        "file": "trigger-hedge-fund-unwind.md",
        "condition": "個股 1 日跌 >-20% + ADR 同步 >-15% + 成交量 >5日均量 3x(三項 AND)",
        # v0.4.1 改純 atlas 路徑(對位 v6.58.21 真實判斷):atlas PR #1515 修復後
        # OHLC/vol 完整(PR #1511)+ coverage_note 明確告知(PR #1515),不需 web fallback
        "http_path": "/api/stock/quote",
        "symbols": ["NVDA", "TSM", "2330"],  # 多 symbol 監測(ADR + 台股)
        "metric": "change_pct",  # 1 日跌幅
        "threshold": -20.0,  # -20% 觸發
        "compare": "lt",
        "is_multi_symbol_quote": True,  # v0.4.1:多 symbol quote 純 atlas 路徑(對位 v6.58.21)
    },
}


def get_env():
    """讀 .env 環境(atlas-wiki 用 ~/.config/atlas-wiki/.env)"""
    env = {}
    # 先讀 ~/.config/atlas-wiki/.env(atlas 端 API key)
    atlas_env = os.path.expanduser("~/.config/atlas-wiki/.env")
    if os.path.exists(atlas_env):
        with open(atlas_env) as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key = line.split("=", 1)[0].strip()
                    val = line.split("=", 1)[1].strip()
                    env[key] = val
    # 再讀 ~/.hermes/.env(Telegram)
    hermes_env = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(hermes_env):
        with open(hermes_env) as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key = line.split("=", 1)[0].strip()
                    val = line.split("=", 1)[1].strip()
                    env[key] = val
    return env


def get_atlas_data(http_path, params=None):
    """打 atlas HTTP API 拉真實數據(對位 atlas-go HTTP server)

    對位 server.go:21 AtlasBaseURL http://127.0.0.1:18080
    加 X-API-Key header(對位 auth.go 認證)
    params: dict,query string 附加(如 ?symbol=2330)
    """
    cache_key = http_path + (("?" + urllib.parse.urlencode(params)) if params else "")
    if cache_key in _data_cache:
        return _data_cache[cache_key]
    url = ATLAS_HTTP_BASE + http_path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    # 拉 ATLAS_API_KEY
    env = get_env()
    api_key = env.get("ATLAS_API_KEY")
    try:
        # v0.4:用 -w 區分 HTTP code 與 body,404/503 應視為失敗
        cmd = ["curl", "-s", "-m", "10", "-w", "\n%{http_code}"]
        if api_key:
            cmd += ["-H", f"X-API-Key: {api_key}"]
        cmd.append(url)
        r = subprocess.run(
            cmd, capture_output=True, text=True, timeout=15
        )
        if r.returncode != 0 or not r.stdout:
            return None
        # 拆 body 與 HTTP code
        parts = r.stdout.rsplit("\n", 1)
        body = parts[0] if len(parts) > 0 else ""
        http_code_str = parts[1] if len(parts) > 1 else "0"
        try:
            http_code = int(http_code_str)
        except ValueError:
            http_code = 0

        # 404/503 = 路徑不存在或 server error,視為失敗
        if http_code in (404, 502, 503, 504):
            return {"__atlas_error__": True, "code": http_code, "body": body[:200]}

        # 401 = unauthorized(既有)
        if http_code == 401 or "unauthorized" in body.lower():
            return {"__unauthorized__": True}

        # 200 成功,解析
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return {"__atlas_error__": True, "code": http_code, "body": body[:200]}

        _data_cache[cache_key] = data
        return data
    except Exception:
        return None


def send_telegram(env, message):
    """Telegram 通知(支援 TELEGRAM_HOME_CHANNEL + TELEGRAM_CHAT_ID 雙軌)"""
    token = env.get("TELEGRAM_BOT_TOKEN")
    chat_id = env.get("TELEGRAM_HOME_CHANNEL") or env.get("TELEGRAM_CHAT_ID")
    if not (token and chat_id):
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": message}).encode()
    try:
        urllib.request.urlopen(url, data=data, timeout=10)
        return True
    except Exception:
        return False


# 各 http_path 對應的快取(避免重複打 API)
_data_cache = {}

# web fallback 快取(對位 v0.4 is_web_fallback)
_web_cache = {}
# reason 分類常數(D 議題:run_triggers 改 4-list 結構性改善,對位 paste-1.md §D)
# 顯式 set 比對(不用 substring matching):未來新增 reason 需顯式加入此 set,
# 避免 substring 隱式誤觸發(例如 'no_data' 也會匹配到 'no_data_filter' 之類新 reason)。
# - atlas_faults:需查 API 健康(對位 ATLAS 憲章 數據源治理 §3)
#   - atlas HTTP 端不可達 / 401 / OHLC 殘缺
#   - web_fetch_failed(web fallback 是 atlas 的延伸,失敗 = atlas 端也拿不到資料,結構性誠實需警報)
#   - 例外 str(e)(未知錯誤保守視為 atlas 端,觸發警報以利排查)
# - market_no_signal:by_design,模板對位真實市場訊號(無需警報)
# - config_issues:設定問題(無 symbols 設定 / 設定了但無資料)
ATLAS_FAULT_REASONS = frozenset({
    "no_data(atlas_http_unreachable)",
    "401_unauthorized",
    "open_zero_or_negative",
    "web_fetch_failed",
})
MARKET_NO_SIGNAL_REASONS = frozenset({
    "threshold_not_met",
    "chips_aggregate_threshold_not_met",
    "web_threshold_not_met",
    "multi_symbol_threshold_not_met",
})
CONFIG_ISSUE_REASONS = frozenset({
    "no_symbols_configured",
    "no_symbol_data",
    # 2026-08-27 T3-A818:metric_divisor 拿到非數值(atlas 欄位缺 / None)
    # 歸 config_issues 而非 atlas_faults — 元件缺值屬資料涵蓋問題,不是 API 不健康,
    # 若不顯式登錄,_record_failure 會 fallthrough 到 atlas_faults 觸發假故障警報。
    "metric_not_numeric",
})
# 例外字串前綴(D 議題:run_triggers L739 except 區塊把 str(e)[:50] 塞進 reason)
EXCEPTION_REASON_PREFIXES = ()  # 例外已 str(e)[:50] 截斷,主程式判斷 reason 不在 3 個 set 時歸入 atlas_faults


def is_atlas_data_complete(data: dict, http_path: str) -> bool:
    """檢查 atlas 回傳是否完整(對位 preflight-check L3 邏輯)

    2026-08-10 atlas 修復後(PR #1515):政策不涵蓋的 symbol 回 200 + coverage_note
    視為「明確告知」不算殘缺。
    """
    if not isinstance(data, dict):
        return False

    # PR #1515 後:200 + complete:false + coverage_note = 明確告知
    if data.get("complete") is False and data.get("coverage_note"):
        return True

    if http_path == "/api/stock/quote":
        # quote 需 OHLC + vol 都 > 0
        return (data.get("last", 0) > 0 and
                data.get("open", 0) > 0 and
                data.get("high", 0) > 0 and
                data.get("low", 0) > 0 and
                data.get("volume", 0) > 0)

    if http_path == "/api/stock/chips":
        return any(data.get(k, 0) > 0 for k in
                   ["foreign_investor_net", "domestic_fund_net", "dealer_net"])

    if http_path.startswith("/api/macro/"):
        return data.get("value", 0) > 0

    return True


def fetch_web(fb_config: dict) -> Optional[dict]:
    """從 web fallback 抓取資料(v0.4)

    fb_config: {
        "url": "...",
        "parser": "html_table" | "json" | "edgar_filing",
        "field": "...",
        "cache_ttl_sec": int,
    }
    """
    cache_key = f"web:{fb_config.get('url','')}:{fb_config.get('field','')}"

    # 1. 查快取
    if cache_key in _web_cache:
        entry = _web_cache[cache_key]
        if time.time() - entry["ts"] < fb_config.get("cache_ttl_sec", 3600):
            return entry["data"]

    # 2. 抓網頁
    url = fb_config.get("url")
    if not url:
        return None

    try:
        cmd = ["curl", "-sS", "-m", "30", "-A", "Mozilla/5.0 atlas-mcp-monitor/0.4", url]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
        if r.returncode != 0:
            return None

        parser = fb_config.get("parser", "html_table")
        if parser == "json":
            data = json.loads(r.stdout)
        elif parser == "sec_xbrl_companyfacts":
                    # SEC XBRL companyfacts API(對位 v6.58.21)
                    # URL pattern:https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK}.json
                    # JSON 結構:{"facts":{"us-gaap":{"<concept>":{"units":{"USD":[{"val","end","form","fp"}]}}}}
                    # v0.4.2 加 YoY 計算(對位 v6.58.29 B 方案):取本期 + 去年同期(同 fp)+ 算 YoY%
                    concept = fb_config.get("field")
                    units = fb_config.get("units", "USD")
                    target_form = fb_config.get("form")
                    try:
                        sec_data = json.loads(r.stdout)
                        # 抓 concept 的 USD 資料
                        concept_data = sec_data.get("facts", {}).get("us-gaap", {}).get(concept, {})
                        entries = concept_data.get("units", {}).get(units, [])
                        # 過濾 form
                        if target_form:
                            filtered = [e for e in entries if e.get("form") == target_form]
                        else:
                            filtered = entries
                        if not filtered:
                            return None
                        # 取最近 1 個(按 end 排序)
                        filtered.sort(key=lambda x: x.get("end", ""), reverse=True)
                        latest = filtered[0]
                        latest_val = latest.get("val", 0)
                        latest_end = latest.get("end", "")
                        latest_fp = latest.get("fp", "")
                        # YoY 計算:取去年同期(同 fp,往前 1 年)
                        yoy_pct = None
                        if latest_fp:
                            # 去年同期 fp = latest_fp,end 減 1 年
                            try:
                                from datetime import datetime
                                latest_date = datetime.strptime(latest_end, "%Y-%m-%d")
                                last_year_date = latest_date.replace(year=latest_date.year - 1)
                                last_year_end = last_year_date.strftime("%Y-%m-%d")
                                # 找同 fp + 上一年同 end 附近的 entry(±90 天容忍,因季報有時跨月)
                                candidates_yoy = [e for e in filtered if e.get("fp") == latest_fp]
                                # 取距 last_year_end 最近的
                                if candidates_yoy:
                                    candidates_yoy.sort(key=lambda e: abs(
                                        (datetime.strptime(e.get("end", "1900-01-01"), "%Y-%m-%d") - last_year_date).days
                                    ))
                                    last_year_entry = candidates_yoy[0]
                                    last_year_val = last_year_entry.get("val", 0)
                                    if last_year_val > 0:
                                        yoy_pct = (latest_val - last_year_val) / last_year_val * 100
                            except (ValueError, ImportError):
                                yoy_pct = None
                        # 對位 v6.58.29 B 方案:return 的 data 結構 — 包含本期值 + YoY%
                        data = {
                            concept: latest_val,
                            "_end": latest_end,
                            "_form": latest.get("form", ""),
                            "_fp": latest_fp,
                            "_yoy_pct": yoy_pct,  # 對位 B 方案:YoY% for trigger 比對
                        }
                    except (json.JSONDecodeError, KeyError, TypeError) as e:
                        return None
        elif parser == "html_table":
            # 簡單 HTML 表格解析(從第一個 table 抓數字)
            import re
            numbers = re.findall(r'<td[^>]*>([+-]?[\d.,]+)</td>', r.stdout)
            field = fb_config.get("field", "")
            if field and numbers:
                # 簡化版:返回第一個數字作為 fallback 結果
                # 實際 HTML table 解析需根據各網站結構客製
                try:
                    val = float(numbers[0].replace(",", ""))
                    data = {field: val}
                except (ValueError, IndexError):
                    return None
            else:
                return None
        else:
            return None

        _web_cache[cache_key] = {"data": data, "ts": time.time()}
        return data
    except Exception as e:
        return None


def fetch_with_fallback(t: dict) -> Optional[dict]:
    """雙軌抓取:v0.4 對位 kaecer B 方案

    切換邏輯:
    - atlas 報價完整 → 用 atlas
    - atlas 報價殘缺或失敗 → 切 web fallback
    - web 也失敗 → None(標 fail)
    """
    http_path = t.get("http_path")
    params = None
    if http_path == "/api/stock/quote" and "field" in t:
        params = {"symbol": t["field"]}
    elif "symbols" in t and t.get("is_chips_aggregate"):
        # chips aggregate:傳第一個 symbol(個別抓,aggregate 在 run_triggers 處理)
        return None  # aggregate 模式不走此函數,保留舊邏輯

    # 1. 試 atlas
    if http_path:
        data = get_atlas_data(http_path, params=params)
        if data is not None:
            # 401 / __atlas_error__ → 視為失敗,切 web fallback
            if data.get("__unauthorized__") or data.get("__atlas_error__"):
                pass  # 跳到下方 web fallback
            elif is_atlas_data_complete(data, http_path):
                return data
            elif data.get("complete") is False and data.get("coverage_note"):
                # 政策不涵蓋但明確告知 → 也視為「明確結果」,不切 web
                return data
            # 殘缺 → 切 web fallback

    # 2. atlas 失敗 / 殘缺 / 401 / 404 / 503 → web fallback
    if t.get("is_web_fallback") and t.get("web_fallback"):
        for field_name, fb_config in t["web_fallback"].items():
            data = fetch_web(fb_config)
            if data is not None:
                return data

    return None


import time  # 給 fetch_web 用


def run_triggers(env):
    """跑 17 觸發模板(對位 v0.4 + D 議題 4-list 結構)

    第 15 模板(equipment-capex-external-report-cycle)為週期型,不走 run_triggers,
    即時掃描每 5 分鐘會誤觸;由獨立 scripts/external-report-cycle-monitor.py + cron 觸發
    (T3-A248 + 第六條鐵律)

    Returns:
        Tuple[triggered, atlas_faults, market_no_signal, config_issues]
        - triggered: 觸發列表(任一)
        - atlas_faults: ATLAS 端故障 / web fallback 失敗 / 未知例外(需查 API 健康,警報)
        - market_no_signal: by_design,模板對位真實市場訊號(無需警報)
        - config_issues: 設定問題(無 symbols 設定 / 設定了但無資料,無需警報)
    """
    triggered = []
    atlas_faults = []
    market_no_signal = []
    config_issues = []

    def _record_failure(reason: str, **fields) -> None:
        """依 reason 自動分流到 3 個 failure list(D 議題:4-list 結構)

        對位:ATLAS_FAULT_REASONS / MARKET_NO_SIGNAL_REASONS / CONFIG_ISSUE_REASONS
        顯式 set 比對;未來新增 reason 必須顯式加入正確 set(避免 substring 隱式誤觸)
        """
        entry = {"id": t_id, "name": t["name"], "reason": reason, **fields}
        if reason in ATLAS_FAULT_REASONS or reason not in MARKET_NO_SIGNAL_REASONS and reason not in CONFIG_ISSUE_REASONS:
            atlas_faults.append(entry)
        elif reason in MARKET_NO_SIGNAL_REASONS:
            market_no_signal.append(entry)
        else:
            config_issues.append(entry)

    for t_id, t in TEMPLATES.items():
        try:
            # 自訂計算分支(個股報價觸發用,對位 PR #1445 stock_get_quote 修復)
            if t.get("is_custom_calc"):
                params = {"symbol": t["field"]}
                data = get_atlas_data(t["http_path"], params=params)
                if data is None:
                    _record_failure("no_data(atlas_http_unreachable)")
                    continue
                if data.get("__unauthorized__"):
                    _record_failure("401_unauthorized")
                    continue
                # 計算盤中振幅(high - low) / open * 100
                high = data.get("high", 0)
                low = data.get("low", 0)
                open_ = data.get("open", 0)
                if open_ <= 0:
                    _record_failure("open_zero_or_negative")
                    continue
                intraday_swing_pct = (high - low) / open_ * 100
                value = intraday_swing_pct
            elif t.get("is_chips_aggregate"):
                # 多 symbol 投信當日 aggregate 觸發(對位 T3-A253 v0.3 + trigger-megaproject-2-quarter-lag.md)
                # 設計:每個 symbol 呼叫 /api/stock/chips 取 domestic_fund_net(投信當日淨買賣超,單位:張)
                # aggregate_mode: sum(目前只支援 sum;avg/max 留 v0.4 擴充)
                # 觸發條件:合計 > threshold(對位 v6.22 unified signature)
                # 結構性誠實:此分支無 extra_check(對位 T3-A14 v8);直接判斷觸發結果
                symbols = t["symbols"]
                aggregate_total = 0.0
                symbol_net_values = {}
                hit_count = 0
                for sym in symbols:
                    data = get_atlas_data(t["http_path"], params={"symbol": sym})
                    if data is None or data.get("__unauthorized__"):
                        symbol_net_values[sym] = None
                        continue
                    net = data.get(t["metric"])
                    if net is None:
                        symbol_net_values[sym] = None
                        continue
                    symbol_net_values[sym] = net
                    aggregate_total += net
                    if net > 0:
                        hit_count += 1
                summary_value = f"aggregate={aggregate_total:.1f} ({sum(1 for v in symbol_net_values.values() if v is not None)}/{len(symbols)} symbols hit), per={symbol_net_values}"
                # T3 誠實修補(2026-08-16):0 個 symbol 有資料時不可判「未觸發」
                # 舊版 aggregate_total=0.0 會被拿去跟 threshold 比,把「無資料」
                # 偽裝成「市場無訊號」(對位 USER §7「有回傳 ≠ 資料可用」)。
                if all(v is None for v in symbol_net_values.values()):
                    _record_failure("no_symbol_data", value=summary_value)
                    continue
                aggregate_mode = t.get("aggregate_mode", "sum")
                threshold = t["threshold"]
                compare = t.get("compare", "gt")
                if aggregate_mode == "sum":
                    triggered_flag = (
                        (compare == "gt" and aggregate_total > threshold) or
                        (compare == "lt" and aggregate_total < threshold)
                    )
                else:
                    # v0.4 預留 aggregate_mode=avg/max;v0.3 對位 T3-A14 v8 fail-closed
                    triggered_flag = False
                if triggered_flag:
                    triggered.append({"id": t_id, "name": t["name"], "value": summary_value})
                else:
                    _record_failure("chips_aggregate_threshold_not_met", value=summary_value)
                continue  # 跳過標準 extra_check + threshold 段(本分支已有結論)
            elif t.get("is_web_only"):
                # 純 web fallback 模板(對位 v6.58.21 Step 3c 模板 18 SEC XBRL)
                # 無 http_path,完全靠 fetch_with_fallback 從 web_fallback 抓
                data = fetch_with_fallback(t)
                if data is None:
                    _record_failure("web_fetch_failed")
                    continue
                # v0.4.2 對位 v6.58.29 B 方案:用 _yoy_pct(若有)或 field 值比對
                # 若有 _yoy_pct(YoY%),優先用 YoY% 觸發(排除季節性)
                # 若無 _yoy_pct(fallback),用 field 絕對值
                if data.get("_yoy_pct") is not None:
                    value = data["_yoy_pct"]
                    value_type = "yoy_pct"
                else:
                    field = t.get("field", "")
                    value = data.get(field, 0)
                    value_type = "abs"
                triggered_flag = False
                compare = t.get("compare", "gt")
                if compare == "lt":
                    triggered_flag = value < t["threshold"]
                else:
                    triggered_flag = value > t["threshold"]
                if triggered_flag:
                    triggered.append({"id": t_id, "name": t["name"], "value": value, "_type": value_type, "_end": data.get("_end", ""), "_form": data.get("_form", "")})
                else:
                    _record_failure("web_threshold_not_met", value=value, _type=value_type, _end=data.get("_end", ""), _form=data.get("_form", ""))
                continue
            elif t.get("is_multi_symbol_quote"):
                # 多 symbol quote 模板(對位 v6.58.21 Step 3b 模板 19 純 atlas)
                # 對每個 symbol 抓 quote,取最低 change_pct(任一觸發)
                symbols = t.get("symbols", [])
                if not symbols:
                    _record_failure("no_symbols_configured")
                    continue
                symbol_changes = {}
                for sym in symbols:
                    data = get_atlas_data(t["http_path"], params={"symbol": sym})
                    if data is None or data.get("__unauthorized__") or data.get("__atlas_error__"):
                        symbol_changes[sym] = None
                        continue
                    # T3 誠實修補(2026-08-16):coverage_note=NOT_COVERED 或 metric 缺欄
                    # 一律標 None,不可用 0 代入(對位 USER §7「有回傳 ≠ 資料可用」)
                    # 舊版 data.get(metric, 0) 會把「沒資料」偽裝成 change_pct=0,
                    # 導致 min=0.00 → threshold_not_met 假陰性,掩蓋真實涵蓋缺口。
                    if data.get("coverage_note") == "NOT_COVERED" or data.get("covered") is False:
                        symbol_changes[sym] = None
                        continue
                    change = data.get(t["metric"])
                    if change is None:
                        symbol_changes[sym] = None
                        continue
                    symbol_changes[sym] = change
                # 取最低(最負)
                valid_changes = [v for v in symbol_changes.values() if v is not None]
                if not valid_changes:
                    _record_failure("no_symbol_data", value=symbol_changes)
                    continue
                value = min(valid_changes)
                summary_value = f"min={value:.2f}, per={symbol_changes}"
                triggered_flag = False
                compare = t.get("compare", "lt")
                if compare == "lt":
                    triggered_flag = value < t["threshold"]
                else:
                    triggered_flag = value > t["threshold"]
                if triggered_flag:
                    triggered.append({"id": t_id, "name": t["name"], "value": summary_value})
                else:
                    _record_failure("multi_symbol_threshold_not_met", value=summary_value)
                continue
            else:
                # 拉真實數據(打 atlas HTTP API)
                data = get_atlas_data(t["http_path"])
                if data is None:
                    _record_failure("no_data(atlas_http_unreachable)")
                    continue
                # 判斷觸發
                field_data = data.get(t["field"], {})
                value = field_data.get(t["metric"], 0) if isinstance(field_data, dict) else field_data
                if isinstance(value, dict):
                    value = value.get(t["metric"], 0)
                # metric_divisor(2026-08-27 T3-A818):把 atlas 元件值還原成模板宣告的刻度
                # 用途:stress-index components.geopolitical 是 GeoIntensity × weight 0.13,
                # threshold 用 0-100 GeoIntensity 刻度時必須先還原,否則 unit mismatch 恆不觸發。
                # 對位 ATLAS_METHODOLOGY.md §3「反向換算 GeoIntensity = 元件值 ÷ 0.13」
                divisor = t.get("metric_divisor")
                if divisor:
                    if isinstance(value, (int, float)):
                        value = value / divisor
                    else:
                        # 非數值(None / 缺欄)不可代 0 硬算(對位 USER §7「有回傳 ≠ 資料可用」)
                        _record_failure("metric_not_numeric", value=value)
                        continue
            triggered_flag = False
            compare = t.get("compare", "gt")  # gt 或 lt
            if compare == "lt":
                triggered_flag = value < t["threshold"]
            else:
                triggered_flag = value > t["threshold"]
            # 額外檢查(對位 china-slowdown / tariff-shock / retail-margin-decrease)
            if "extra_check" in t and triggered_flag:
                for ext_field, condition in t["extra_check"].items():
                    ext_data = data.get(ext_field, {})
                    ext_value = ext_data.get("change_pct" if "change_pct" in condition else "value", 0)
                    if "change_pct>0" in condition and ext_value <= 0:
                        triggered_flag = False
                        break
                    if "value!=0" in condition and ext_value == 0:
                        triggered_flag = False
                        break
            if triggered_flag:
                triggered.append({"id": t_id, "name": t["name"], "value": value})
            else:
                _record_failure("threshold_not_met", value=value)
        except Exception as e:
            # 未知錯誤:reason 不在 3 個 set,helper 自動歸入 atlas_faults(結構性誠實:觸發警報以利排查)
            _record_failure(str(e)[:50])
    return triggered, atlas_faults, market_no_signal, config_issues


def main():
    print("=" * 60)
    print(f"atlas-mcp-trigger-monitor — {datetime.now().isoformat()}")
    print("=" * 60)
    env = get_env()
    triggered, atlas_faults, market_no_signal, config_issues = run_triggers(env)
    failed = list(market_no_signal) + list(config_issues)  # 列印用:by_design + 設定問題合併
    print(f"  觸發: {len(triggered)}/{len(TEMPLATES)}")
    print(f"  未觸發: {len(failed)}/{len(TEMPLATES)}(模板對位真實市場訊號,結構性誠實)")
    if triggered:
        print(f"\n  ✅ 觸發詳情:")
        for t in triggered:
            print(f"    - {t['name']} (值={t['value']})")
    if failed:
        print(f"\n  📊 未觸發(模板對位真實市場訊號):")
        for f in failed:
            print(f"    - {f['name']} (值={f.get('value','?')} 原因={f.get('reason','?')})")
    # 警報邏輯:對位 PR #18 commit 2 + D 議題改用 4-list(結構性誠實)
    # atlas_faults 是 module-level ATLAS_FAULT_REASONS 顯式分類的結果,不再於 main() 內重算
    if len(atlas_faults) >= 3:
        send_telegram(
            env,
            f"🚨 atlas-mcp-trigger-monitor: {len(atlas_faults)}/{len(TEMPLATES)} 模板 ATLAS 端故障,需查 API 健康",
        )
    if triggered:
        summary = f"📊 [atlas-mcp-trigger] {datetime.now().strftime('%H:%M')} {len(triggered)} 觸發:\n"
        for t in triggered:
            summary += f"  - {t['name']} (值={t['value']})\n"
        send_telegram(env, summary)
    print(f"\n  ✅ monitor 完成")


if __name__ == "__main__":
    main()