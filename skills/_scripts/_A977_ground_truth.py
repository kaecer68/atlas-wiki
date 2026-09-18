#!/usr/bin/env python3
"""A977 ground truth check — agent 親跑 importlib 雙副本 + curl atlas-mcp (Pitfall 33 對位)"""
import os, sys, hashlib, json, subprocess

WIKI_PATH = '/Users/kk/workspace/atlas-wiki/skills/_scripts/atlas-mcp-trigger-monitor.py'
CRON_PATH = os.path.expanduser('~/.hermes/scripts/atlas-mcp-trigger-monitor.py')

def md5_of(p):
    with open(p, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

print('=== WIKI 副本 ===')
print(f'path: {WIKI_PATH}')
print(f'exists: {os.path.exists(WIKI_PATH)}')
print(f'md5: {md5_of(WIKI_PATH)}')
print(f'size: {os.path.getsize(WIKI_PATH)}')
print(f'mtime epoch: {os.path.getmtime(WIKI_PATH)}')

print()
print('=== CRON 部署本 ===')
print(f'path: {CRON_PATH}')
print(f'exists: {os.path.exists(CRON_PATH)}')
if os.path.exists(CRON_PATH):
    print(f'md5: {md5_of(CRON_PATH)}')
    print(f'size: {os.path.getsize(CRON_PATH)}')
    print(f'mtime epoch: {os.path.getmtime(CRON_PATH)}')

# Atlas-mcp ground truth
print()
print('=== ATLAS-MCP GROUND TRUTH (curl) ===')
try:
    r = subprocess.run(['curl', '-sS', '-m', '10', 'http://127.0.0.1:18080/api/taiwan/stress-index'],
                       capture_output=True, text=True, timeout=15)
    print(f'stress-index exit: {r.returncode}')
    if r.returncode == 0:
        try:
            d = json.loads(r.stdout)
            print(f'components.geopolitical: {d.get("components", {}).get("geopolitical")}')
            print(f'date: {d.get("date")}')
            print(f'timestamp: {d.get("timestamp")}')
            print(f'score: {d.get("score")}')
        except Exception as e:
            print(f'parse err: {e}')
            print(f'raw (first 500): {r.stdout[:500]}')
except Exception as e:
    print(f'curl err: {e}')

try:
    r = subprocess.run(['curl', '-sS', '-m', '10', 'http://127.0.0.1:18080/api/macro/snapshot/latest'],
                       capture_output=True, text=True, timeout=15)
    print(f'macro snapshot exit: {r.returncode}')
    if r.returncode == 0:
        try:
            d = json.loads(r.stdout)
            print(f'data_status: {d.get("data_status")}')
            print(f'recorded_at: {d.get("recorded_at")}')
            # 列 macro fields
            for k, v in d.items():
                if k not in ('data_status', 'recorded_at') and not k.startswith('_'):
                    print(f'  {k}: {v}')
        except Exception as e:
            print(f'parse err: {e}')
            print(f'raw (first 500): {r.stdout[:500]}')
except Exception as e:
    print(f'curl err: {e}')

# 跑 importlib 兩副本
print()
print('=== WIKI 副本 run_triggers({}) ===')
import importlib.util
try:
    spec_w = importlib.util.spec_from_file_location('trigger_wiki_aw977', WIKI_PATH)
    mod_w = importlib.util.module_from_spec(spec_w)
    spec_w.loader.exec_module(mod_w)
    triggered, atlas_faults, market_no_signal, config_issues = mod_w.run_triggers({})
    print(f'triggered ({len(triggered)}): {triggered}')
    print(f'atlas_faults ({len(atlas_faults)}): {atlas_faults}')
    print(f'market_no_signal ({len(market_no_signal)}): {market_no_signal}')
    print(f'config_issues ({len(config_issues)}): {config_issues}')
    print(f'triggered_ids: {sorted([t.get("id") if isinstance(t, dict) else t for t in triggered])}')
except Exception as e:
    print(f'wiki run_triggers err: {type(e).__name__}: {e}')
    import traceback
    traceback.print_exc()

if os.path.exists(CRON_PATH):
    print()
    print('=== CRON 部署本 run_triggers({}) ===')
    try:
        spec_c = importlib.util.spec_from_file_location('trigger_cron_aw977', CRON_PATH)
        mod_c = importlib.util.module_from_spec(spec_c)
        spec_c.loader.exec_module(mod_c)
        triggered, atlas_faults, market_no_signal, config_issues = mod_c.run_triggers({})
        print(f'triggered ({len(triggered)}): {triggered}')
        print(f'atlas_faults ({len(atlas_faults)}): {atlas_faults}')
        print(f'market_no_signal ({len(market_no_signal)}): {market_no_signal}')
        print(f'config_issues ({len(config_issues)}): {config_issues}')
        print(f'triggered_ids: {sorted([t.get("id") if isinstance(t, dict) else t for t in triggered])}')
    except Exception as e:
        print(f'cron run_triggers err: {type(e).__name__}: {e}')
        import traceback
        traceback.print_exc()

# 跟 pre-run 對位
print()
print('=== PRE-RUN 對位 ===')
print('pre-run 報 4 觸發: DXY 弱/融資 3500 億/ETF 換股/散戶融資大減')
print('pre-run 報 13 未觸發, 0 atlas_faults')
print('pre-run 報台海緊張值=13 (預期 stale state 沿袭, 實際真實值應為 < 5)')
print('pre-run 報 NVDA+TSM=-4.57 / USD_TWD=31.628 / 外資買超=4.568 / SOX=-3.47')
print('pre-run 報中國需求強=44.69 / 對中關稅=31.628 / 央行防線=31.628')
print('pre-run 報 2330 swing=1.43 / Megaproject agg=-224.6 (2/3 hit) / HBM agg=0.0 (0/1)')
print('pre-run 報 AI capex=42.02 / cross_hedge min=0.00')
