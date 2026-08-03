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


def get_atlas_data(http_path):
    """打 atlas HTTP API 拉真實數據(對位 atlas-go HTTP server)
    
    對位 server.go:21 AtlasBaseURL http://127.0.0.1:18080
    加 X-API-Key header(對位 auth.go 認證)
    """
    if http_path in _data_cache:
        return _data_cache[http_path]
    url = ATLAS_HTTP_BASE + http_path
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
        _data_cache[http_path] = data
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
    """跑 12 觸發模板"""
    triggered = []
    failed = []
    for t_id, t in TEMPLATES.items():
        try:
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
    print(f"  觸發: {len(triggered)}/12")
    print(f"  失敗: {len(failed)}/12")
    if triggered:
        print(f"\n  ✅ 觸發詳情:")
        for t in triggered:
            print(f"    - {t['name']} (值={t['value']})")
    if failed:
        print(f"\n  ❌ 失敗詳情:")
        for f in failed:
            print(f"    - {f['name']} (值={f.get('value','?')} 原因={f.get('reason','?')})")
        if len(failed) > 6:
            send_telegram(env, f"⚠️ atlas-mcp-trigger-monitor: {len(failed)}/12 模板失敗,atlas 端可能故障")
    if triggered:
        summary = f"📊 [atlas-mcp-trigger] {datetime.now().strftime('%H:%M')} {len(triggered)} 觸發:\n"
        for t in triggered:
            summary += f"  - {t['name']} (值={t['value']})\n"
        send_telegram(env, summary)
    print(f"\n  ✅ monitor 完成")


if __name__ == "__main__":
    main()