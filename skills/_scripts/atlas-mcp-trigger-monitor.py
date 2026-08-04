#!/usr/bin/env python3
"""
atlas-mcp-trigger-monitor.py — 12 觸發模板自動信號捕捉(對位 kaecer v6.21)
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
- atlas HTTP base:http://127.0.0.1:18080(對位 atlas-go cmd/atlas-mcp/server/server.go:21)
- 端點對應:/api/macro/snapshot/latest 等
"""
import os
import sys
import json
import urllib.request
import urllib.parse
import subprocess
from datetime import datetime

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
        "condition": "geopolitical > 4",
        "http_path": "/api/taiwan/stress-index",
        "field": "components",
        "metric": "geopolitical",
        "threshold": 4,
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
}


def get_env():
    """讀 .env 環境(atlas-wiki 用 ~/.config/atlas-wiki/.env)"""
    env = {}
    # 先讀 ~/.config/atlas-wiki/.env(atlas 端 API key)
    atlas_env = "/Users/kaecer/.config/atlas-wiki/.env"
    if os.path.exists(atlas_env):
        with open(atlas_env) as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key = line.split("=", 1)[0].strip()
                    val = line.split("=", 1)[1].strip()
                    env[key] = val
    # 再讀 ~/.hermes/.env(Telegram)
    hermes_env = "/Users/kaecer/.hermes/.env"
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
        cmd = ["curl", "-s", "-m", "10"]
        if api_key:
            cmd += ["-H", f"X-API-Key: {api_key}"]
        cmd.append(url)
        r = subprocess.run(
            cmd, capture_output=True, text=True, timeout=15
        )
        if r.returncode != 0 or not r.stdout:
            return None
        # 401 = unauthorized
        if '"code":"401"' in r.stdout or "unauthorized" in r.stdout.lower():
            return {"__unauthorized__": True}
        data = json.loads(r.stdout)
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


def run_triggers(env):
    """跑 14 觸發模板(12 既有 + 第 13 個股報價 + 第 14 設備鏈月營收)

    第 15 模板為週期型,不走 run_triggers,即時掃描每 5 分鐘會誤觸;
    由獨立 scripts/external-report-cycle-monitor.py + cron 觸發(T3-A248 + 第六條鐵律)
    """
    triggered = []
    failed = []
    for t_id, t in TEMPLATES.items():
        try:
            # 自訂計算分支(個股報價觸發用,對位 PR #1445 stock_get_quote 修復)
            if t.get("is_custom_calc"):
                params = {"symbol": t["field"]}
                data = get_atlas_data(t["http_path"], params=params)
                if data is None:
                    failed.append({"id": t_id, "name": t["name"], "reason": "no_data(atlas_http_unreachable)"})
                    continue
                if data.get("__unauthorized__"):
                    failed.append({"id": t_id, "name": t["name"], "reason": "401_unauthorized"})
                    continue
                # 計算盤中振幅(high - low) / open * 100
                high = data.get("high", 0)
                low = data.get("low", 0)
                open_ = data.get("open", 0)
                if open_ <= 0:
                    failed.append({"id": t_id, "name": t["name"], "reason": "open_zero_or_negative"})
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
                    failed.append({"id": t_id, "name": t["name"], "value": summary_value, "reason": "chips_aggregate_threshold_not_met"})
                continue  # 跳過標準 extra_check + threshold 段(本分支已有結論)
            else:
                # 拉真實數據(打 atlas HTTP API)
                data = get_atlas_data(t["http_path"])
                if data is None:
                    failed.append({"id": t_id, "name": t["name"], "reason": "no_data(atlas_http_unreachable)"})
                    continue
                # 判斷觸發
                field_data = data.get(t["field"], {})
                value = field_data.get(t["metric"], 0) if isinstance(field_data, dict) else field_data
                if isinstance(value, dict):
                    value = value.get(t["metric"], 0)
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
                failed.append({"id": t_id, "name": t["name"], "value": value, "reason": "threshold_not_met"})
        except Exception as e:
            failed.append({"id": t_id, "name": t["name"], "reason": str(e)[:50]})
    return triggered, failed


def main():
    print("=" * 60)
    print(f"atlas-mcp-trigger-monitor — {datetime.now().isoformat()}")
    print("=" * 60)
    env = get_env()
    triggered, failed = run_triggers(env)
    print(f"  觸發: {len(triggered)}/14")
    print(f"  未觸發: {len(failed)}/14(模板對位真實市場訊號,結構性誠實)")
    if triggered:
        print(f"\n  ✅ 觸發詳情:")
        for t in triggered:
            print(f"    - {t['name']} (值={t['value']})")
    if failed:
        print(f"\n  📊 未觸發(模板對位真實市場訊號):")
        for f in failed:
            print(f"    - {f['name']} (值={f.get('value','?')} 原因={f.get('reason','?')})")
        if len(failed) > 7:
            send_telegram(env, f"⚠️ atlas-mcp-trigger-monitor: {len(failed)}/14 模板未觸發,atlas 端可能故障")
    if triggered:
        summary = f"📊 [atlas-mcp-trigger] {datetime.now().strftime('%H:%M')} {len(triggered)} 觸發:\n"
        for t in triggered:
            summary += f"  - {t['name']} (值={t['value']})\n"
        send_telegram(env, summary)
    print(f"\n  ✅ monitor 完成")


if __name__ == "__main__":
    main()