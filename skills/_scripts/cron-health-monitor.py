#!/usr/bin/env python3
"""
cron-health-monitor.py — cron job 健康監控
對位 kaecer v6.6 派工:2 條 cron TimeoutError 即時偵測

每 5 分鐘跑(由 hermes cron 觸發):
- 讀 ~/.hermes/cron/jobs.json
- 看 last_status=error 的 jobs
- 觸發 → Telegram 通知(不需改 daemon timeout)

注意:不觸發 daemon 改動,純監控 + 通知。
"""
import json
import os
import urllib.request
import urllib.parse
from datetime import datetime

def send_telegram(message):
    """發 Telegram 通知"""
    env_path = os.path.expanduser("~/.hermes/.env")
    if not os.path.exists(env_path):
        return False
    with open(env_path) as f:
        content = f.read()
    token = None
    chat_id = None
    for line in content.split("\n"):
        if line.startswith("TELEGRAM_BOT_TOKEN="):
            token = line.split("=", 1)[1].strip()
        if line.startswith("TELEGRAM_CHAT_ID=") or line.startswith("TELEGRAM_HOME_CHANNEL="):
            chat_id = line.split("=", 1)[1].strip()
    if not (token and chat_id):
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": message}).encode()
    try:
        urllib.request.urlopen(url, data=data, timeout=10)
        return True
    except Exception as e:
        return f"failed: {e}"


def main():
    print("=" * 60)
    print(f"cron 健康監控 — {datetime.now().isoformat()}")
    print("=" * 60)

    jobs_path = os.path.expanduser("~/.hermes/cron/jobs.json")
    if not os.path.exists(jobs_path):
        print(f"# {jobs_path} 不存在")
        return

    with open(jobs_path) as f:
        data = json.load(f)

    jobs = data.get("jobs", data) if isinstance(data, dict) else data
    error_jobs = []
    for j in jobs:
        if j.get("last_status") == "error":
            error_jobs.append(j)

    if error_jobs:
        summary = f"""
# cron 錯誤監控({datetime.now().isoformat()})

**{len(error_jobs)} 個 jobs 錯誤**:

"""
        for j in error_jobs:
            summary += f"- **{j.get('name', j.get('id', '?'))}**"
            if j.get("last_error"):
                summary += f":{j.get('last_error')[:80]}"
            summary += "\n"

        print(summary)
        result = send_telegram(summary)
        print(f"# Telegram 通知:{result}")
    else:
        ok_count = len(jobs)
        print(f"# 全 {ok_count} 個 jobs 健康")

    return len(error_jobs)


if __name__ == "__main__":
    main()