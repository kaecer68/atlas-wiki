#!/usr/bin/env python3
"""gate-review-decision.py — 治理閘門的 review 判定核心（2026-10-26 新增）

為什麼要這支（§QC-11／§QC-12「approve-then-push」）：
  `.github/workflows/validate-wiki.yml` 的 `governance-review-gate` 原本只判斷
  「有沒有 `state=='APPROVED'` 的 review（且 reviewer 是 App bot）」，
  **沒有綁該 review 的 `commit_id` 與 PR 當前 `head.sha`** ⇒
    App 對 commit A 送出 APPROVED → 同一 PR 再 push commit B → 閘門仍看到 APPROVED ⇒ 綠燈。
  同時它只認 APPROVED 的最後一筆 ⇒ `CHANGES_REQUESTED`／`DISMISSED` 都不會撤銷既有核准。

判定規則（任何一步不確定都 fail-closed ⇒ 不通過）：
  1. `head.sha` 取 API 現值（`GET /pulls/{n}`），不取事件 payload
     —— `pull_request_review` 事件的 payload 可能落後於最新一次 push。
  2. 每位 reviewer 只取**最後一筆** review（REST reviews 端點回傳為時間序：舊→新）。
     任一 reviewer 的最後一筆是 `CHANGES_REQUESTED` 或 `DISMISSED` ⇒ **一律否決**
     （否決優先於任何核准與標籤）。
  3. App bot 的最後一筆 review = `APPROVED` 且 `commit_id == head.sha` ⇒ 通過。
  4. 否則：`qc-reviewed` 標籤存在且最後一次貼標 actor = App bot ⇒ 通過
     （標籤路徑沒有 commit_id 可綁，屬已知殘留缺口，見 PR body 的「殘留風險」段）。
  5. 其餘一律不通過。解析失敗（讀不到檔／非 JSON／型別不符）亦不通過，
     不得退化成空值放行。

用法（CI 內由 workflow 呼叫；本機可餵 fixture 測）：
  python3 skills/_scripts/gate-review-decision.py \
      --app-login 'atlas-qc-reviewer[bot]' --has-label 1 \
      --pull /tmp/pull.json --reviews /tmp/reviews.json --timeline /tmp/timeline.json

exit 0 = 通過（仍需人工執行 merge）；exit 1 = 不通過（訊息含 `::error::` 供 Actions 標註）。
"""
import argparse
import json
import sys
from typing import NoReturn

LABEL_NAME = "qc-reviewed"


def die(msg) -> NoReturn:
    """不通過 ⇒ 印 ::error:: 並 exit 1（GitHub Actions 會標成 annotation）。"""
    print("::error::%s" % msg)
    sys.exit(1)


def load(path, what):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:  # 讀不到／不是合法 JSON ⇒ fail-closed
        die("PARSE_ERROR %s（%s）⇒ fail-closed：%s" % (what, path, exc))


def short(sha):
    return sha[:12] if sha else "（無）"


def main(argv=None):
    ap = argparse.ArgumentParser(description="治理閘門 review 判定（commit 綁定 ＋ CHANGES_REQUESTED／DISMISSED）")
    ap.add_argument("--app-login", required=True, help="審查身分 login（atlas-qc-reviewer[bot]）")
    ap.add_argument("--has-label", default="0", help="PR 目前是否帶 qc-reviewed 標籤（1／0）")
    ap.add_argument("--pull", required=True, help="GET /repos/{repo}/pulls/{n} 的 JSON")
    ap.add_argument("--reviews", required=True, help="GET /pulls/{n}/reviews 的 JSON（時間序）")
    ap.add_argument("--timeline", required=True, help="GET /issues/{n}/timeline 的 JSON")
    a = ap.parse_args(argv)

    pull = load(a.pull, "PR")
    reviews = load(a.reviews, "reviews")
    timeline = load(a.timeline, "timeline")
    if not isinstance(pull, dict) or not isinstance(reviews, list) or not isinstance(timeline, list):
        die("PARSE_ERROR API 回應型別不符（pull 需 object、reviews／timeline 需 array）⇒ fail-closed")

    head_obj = pull.get("head")
    head_sha = (head_obj.get("sha") if isinstance(head_obj, dict) else "") or ""

    # 最後一次貼 qc-reviewed 的 actor（判斷標籤是否由 App 身分貼上）
    labeler = ""
    for ev in timeline:
        if not isinstance(ev, dict) or ev.get("event") != "labeled":
            continue
        lbl = ev.get("label")
        name = lbl.get("name") if isinstance(lbl, dict) else lbl
        if name == LABEL_NAME:
            actor = ev.get("actor")
            labeler = (actor.get("login") if isinstance(actor, dict) else "") or ""

    # 每位 reviewer 只留最後一筆：後續核准覆蓋先前異議，後續異議亦覆蓋先前核准
    latest = {}
    for rv in reviews:
        if not isinstance(rv, dict):
            continue
        user = rv.get("user")
        login = (user.get("login") if isinstance(user, dict) else "") or ""
        if login:
            latest[login] = rv

    app_rv = latest.get(a.app_login) or {}
    app_state = (app_rv.get("state") or "").upper()
    app_commit = app_rv.get("commit_id") or ""
    changes = sorted(k for k, v in latest.items() if (v.get("state") or "").upper() == "CHANGES_REQUESTED")
    dismissed = sorted(k for k, v in latest.items() if (v.get("state") or "").upper() == "DISMISSED")

    print("  標籤存在=%s｜標籤 actor=%s｜PR head.sha=%s" % (a.has_label.strip(), labeler or "（無）", short(head_sha)))
    print("  %s 最新 review=%s｜commit_id=%s" % (a.app_login, app_state or "（無）", short(app_commit)))
    if changes:
        print("  最新為 CHANGES_REQUESTED：%s" % ", ".join(changes))
    if dismissed:
        print("  最新為 DISMISSED：%s" % ", ".join(dismissed))

    if not head_sha:
        die("取不到 PR 最新 head.sha ⇒ 無法把核准綁到 commit，fail-closed")
    if changes:
        die("最新 review 為 CHANGES_REQUESTED（%s）⇒ 不得合併，需重新審查" % ", ".join(changes))
    if dismissed:
        die("核准已被 DISMISSED 撤銷（%s）⇒ 不得沿用舊核准，需重新審查" % ", ".join(dismissed))

    if app_state == "APPROVED":
        if app_commit and app_commit == head_sha:
            print("✅ %s 的 APPROVED 綁在當前 head.sha %s ⇒ 通過（仍需人工執行 merge）" % (a.app_login, short(head_sha)))
            return 0
        die("%s 的 APPROVED 綁在 %s，但 PR 最新 head.sha 是 %s ⇒ 核准後又有新 commit（approve-then-push），需重新審查"
            % (a.app_login, short(app_commit), short(head_sha)))

    if a.has_label.strip() == "1" and labeler == a.app_login:
        print("✅ %s 貼上 %s ⇒ 通過（標籤路徑無 commit_id 可綁；仍需人工執行 merge）" % (a.app_login, LABEL_NAME))
        return 0

    die("觸碰治理檔需由 %s 貼 %s 或對**當前 head.sha** 核准（§6.4.2）；作者側自貼不算"
        % (a.app_login, LABEL_NAME))


if __name__ == "__main__":
    sys.exit(main())
