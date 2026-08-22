---
title: 審計 child-B — concepts / entities / queries / templates 金融事實盤查
auditor: prime-agent 子代理（台股金融工程審計員）
date: 2026-08-22
scope: concepts/(19 檔) + entities/(7 檔) + queries/(8 檔) + templates/(21 檔，含 audit-report 範本)
method: 逐檔抽出帶數字/日期的台灣市場制度與歷史宣稱 → 對照台股制度知識判定 [正確/錯誤/需驗證]；2026 年內事件資料（霍爾木茲、五鏈、韓股崩盤等）本審計員無法獨立核實，一律 [需驗證]，不硬判。
note: taiwan-stock-market-structure.md 由主 agent 深審，本檔只記錄它與其他檔的交叉矛盾。
---

# 事實錯誤/疑點總表（依嚴重度）

## HIGH（錯誤事實，會直接誤導制度認知或投資決策）

| # | 檔案 | 原文摘要 | 判定 | 理由 |
|---|------|---------|------|------|
| H1 | concepts/taiwan-stock-market-structure.md §5.2 + concepts/atals-risk-management-framework.md §3.1 | 「追繳門檻 120%」「斷頭（處分）門檻 120%」「維持率 130% 追繳、120% 處分」 | 錯誤（舊制殘留） | 證交所 2022-04-01 起整戶擔保維持率低於 **130%** 即通知追繳，期限內未補足即處分，**現制已無 120% 門檻**；120% 是 2022 年前的舊追繳門檻。且 market-structure 同表前一行已寫「跌破 130% 通知追繳」，表內自相矛盾（risk-mgmt 檔同病）。 |
| H2 | concepts/taiwan-chip-flow-analysis.md §4.4 | 「20%：上市櫃公司外資持股上限（多數公司）」「50%：達到此水位 → 可能被特殊列管」 | 錯誤（舊制殘留） | 外資個別持股 20% 上限是 2000 年前舊制，2000-12 起已取消（多數公司可至 100%）；「50% 特殊列管」無此規定。同檔自己寫「100%：理論上限」，表內自相矛盾。 |
| H3 | concepts/taiwan-fundamental-analysis-guide.md §6.2 | 「注意在 2024 年起，Q2 為 60 天」 | 錯誤（方向相反） | 半年報期限是**縮短**：2022 起資本額百億以上公司、2023 起全體上市櫃公司，Q2 半年報改為 45 天內（8/14 前）；60 天是舊制。同檔速查表又寫「45–60 天內」，自相矛盾。 |

## MED（錯誤/矛盾/過時，需修正或校準）

| # | 檔案 | 原文摘要 | 判定 | 理由 |
|---|------|---------|------|------|
| M1 | concepts/taiwan-stock-market-structure.md §8.1 | 台指期「契約月份：月、季月（3、6、9、12 月）、連續 8 個月」 | 錯誤 | 台指期契約為「當月起**連續 2 個月** + 3、6、9、12 月**3 個季月**」共 5 個契約月，非 8 個月。 |
| M2 | concepts/taiwan-stock-market-structure.md §5.3 | 「融資買進 100 萬 → 股票下跌後市值 80 萬 → 維持率 80%」 | 錯誤（算式） | 依同檔公式（擔保品市值÷融資金額），融資 6 成下 80 萬市值/60 萬融資 = 133%，非 80%；且 133% 未破 130%，不會觸發追繳。範例會誤導。 |
| M3 | concepts/taiwan-stock-market-structure.md §10.2 | 「權證 價格漲跌 50%（標的漲跌 7%）」 | 需驗證（疑似舊制） | 「標的漲跌 7%」是 2015-06 前的舊漲跌幅；現制普通股 10%。權證漲跌幅公式為標的漲跌幅衍生，50% 表述需查證交所營業細則現行公式。 |
| M4 | concepts/t1-t4-signal-light.md | 「T2 外資……佔台股 4 成成交」 | 需驗證（疑錯誤） | 與同知識庫 taiwan-chip-flow-analysis §3.1「外資單日成交值佔大盤 25–35%」矛盾；官方統計外資成交比重約 3 成。「持股約 4 成」與「成交 4 成」疑被混淆。 |
| M5 | concepts/taiwan-stock-market-structure.md §3.1 | 「T+3 → 2014 年起改為 T+2」 | 需驗證（疑錯誤） | 2014 年的制度改革是開放現股當沖；台股 T+2 交割行之多年，非 2014 年由 T+3 改制。無記憶依據支持此變革年份。 |
| M6 | concepts/taiwan-stock-market-structure.md §4.4 | 「2008–2017：當沖稅率 0.25% → 0.2% → 2017 起降為 0.15%」 | 需驗證（疑錯誤） | 記憶中證交稅 1993 起即 0.3%（賣方），2017-04-28 當沖優惠 0.15%（多次展延）；無 0.25%/0.2% 兩段的依據。 |
| M7 | concepts/taiwan-chip-flow-analysis.md §4.2 | 「外資期貨淨多單 > 10 萬口 = 多頭氣勢」 | 需驗證（疑過高） | 台指期外資淨多單歷史多在 ±3 萬口內（高點約 6–7 萬口），10 萬口門檻恐永難觸發，喪失訊號意義。 |
| M8 | concepts/taiwan-fundamental-analysis-guide.md §5.2 + concepts/taiwan-technical-analysis-guide.md §5.1 | 「大盤站穩 MA60 月線」「股價站上 MA60 月線才稱多頭」 | 錯誤（用語） | 同檔表格已定義 MA20=月線、MA60=季線；「MA60 月線」為標籤錯誤（季線誤標月線），兩檔同病。 |
| M9 | templates/trigger-foreign-3day-inflow.md | 觸發條件「foreign_investor_net > +20 億（單日）」 | 過時/矛盾 | (a) 檔名與 strategy 名為「3day」但條件是單日；(b) 2026-08-03 快照當日外資 +21.83 億即觸發，2026 年外資單日常態百億級、日成交 7000 億，+20 億門檻幾乎恆觸發，無鑑別力（hit_rate 0.37 佐證）；(c) 與同庫 chip-flow「單日 100 億以上為大動作」矛盾。 |
| M10 | templates/trigger-etf-rebalance.md | 觸發條件「市場成交量 > 0」 | 無鑑別力 | 「成交量 > 0」恆真，形同無條件觸發；且 etf_net_subscription 標 0（API 未提供），模板實質無法驗證 ETF 換股訊號。 |
| M11 | templates/trigger-msci-rebalance-pressure.md | 「Samsung/SK Hynix 權重飆升 → 被動 ETF 被迫減持 → 結構性賣壓」；「MSCI 季度再平衡公告日(2/8/11 月)」「2026/8 公告 = 11月生效」 | 需驗證/邏輯矛盾 | (a) 反向機制敘述與本模板自己的正向觸發（權重升→被動增持買盤）自相矛盾——權重升 ETF 是被迫**增持**而非減持；(b) MSCI 季度檢討為 2/5/8/11 月，漏 5 月；(c) 8 月檢討於 8 月底生效，非「11 月生效」。 |
| M12 | templates/trigger-tariff-shock.md | 觸發條件「USD_TWD > 32 + 出口電子指數 > 0」 | 需驗證/邏輯缺口 | 名為「對中/台晶片關稅」模板，但觸發條件不含任何關稅變數（關稅新聞/費率/豁免清單），名實不符。 |
| M13 | templates/trigger-china-slowdown.md | 「TSMC 月營收 YoY > +50% = 中國需求強」「半導體 40%+ 出口到中國」「需求強→加碼半導體至 60% + 減塑化/出口股」 | 需驗證/邏輯弱 | (a) TSMC 營收驅動是全球 AI 需求，中國僅佔其營收約 1 成，拿來當「中國需求」代理錯位；(b) 月營收 YoY >+50% 為極端門檻（2024–2025 常態多在 ±40% 內）；(c)「需求強卻減出口股」方向矛盾。 |
| M14 | templates/trigger-retail-margin-decrease.md | 標題「散戶融資大減」，觸發條件「融資 > 5000 億（高水位）」 | 矛盾 | 標題/檔名語意（融資大減）與觸發條件（融資過高）方向相反；內容實為 margin-350b 的複製品，非「大減」模板。 |
| M15 | entities/l1-t-overview.md | 「L1-T.1 美國 3 支柱」「L1-T.4/5/6 待補」 | 過時 | 實際 entity 檔：l1-t1 = 能源轉型（非美國 3 支柱）、l1-t4/5/6 均已存在（critical-minerals / ai-semiconductor / demographic-turning-point）。overview 未隨 Day 4–6 更新，與 week-1-summary「Day 4–6 已抽出 T.1/T.2/T.4/T.5/T.6」矛盾。 |
| M16 | concepts/taiwan-financial-domain-model.md §10 vs concepts/atals-simulation-guide.md §2 + atals-strategy-taxonomy.md §4 | L1–L5 定義 | 矛盾 | domain-model 定義 L1 極短線…L5 總體經濟（時間尺度）；simulation-guide/strategy-taxonomy 定義 L1 總經…L5 地緣風險（訊號來源）。同知識庫平台詞彙互相矛盾，agent 引用會錯層。 |
| M17 | concepts/taiwan-financial-domain-model.md §10 | 「信心分數 0–100」 | 矛盾 | 其他檔（money-flow、interpretation-guide、H1-H2-H3）的 confidence 都是 0–1（0.95、0.664、0.5）。 |
| M18 | templates/trigger-cb-fx-intervention.md + trigger-usd-twd-32.md | 「USD_TWD > 32.3（接近台灣央行防線 32.5）」 | 需驗證 | 「32.5 央行防線」是 2024 年市場語意；2025 年現匯已曾破 32.5 見 33.0。2026 年 32.3 門檻合理性取決於 2026 匯率分布，無法由本審計員核實；且 2026-08-03 現匯 32.38 已貼近門檻，觸發頻率需校準。央行防線本非官方公布值。 |
| M19 | entities/l1-t2-petrodollar-hormuz.md | 「2010 中國超越美國成為全球最大石油進口國」 | 需驗證（疑錯誤） | 記憶中中國原油進口在 2017 年前後超越美國；2010 年超越的是能源消費總量。因果鏈敘事（薩達姆歐元計價 → 2003 入侵）屬爭議敘事，非事實判定。 |
| M20 | entities/l1-t1-energy-transition.md | 「台灣 2030 燃氣 50% 目標」 | 需驗證 | 燃氣 50% 是 2025 年能源結構目標（燃氣 50/燃煤 30/再生 20）；2030 標的需查 2026 年版能源政策。 |
| M21 | templates/trigger-2330-tsmc-swing.md | 「2329 + 2363 + 2379 矽晶圓 / 封測 / 光罩」 | 錯誤（分類） | 2363 矽統、2379 瑞昱為 IC 設計公司，非矽晶圓/封測/光罩；2329 華泰為封測。產業標籤錯植。 |

## LOW（微瑕/時效/一致性）

| # | 檔案 | 原文摘要 | 判定 | 理由 |
|---|------|---------|------|------|
| L1 | concepts/taiwan-financial-domain-model.md | 興櫃「ESM（Emerving Stock Market）」 | 錯誤（拼字） | 應為 Emerging。 |
| L2 | concepts/taiwan-financial-domain-model.md §1 | 權證「分為歐式與美式」 | 需驗證 | 台股掛牌權證以歐式為主，實務上無美式掛牌權證。 |
| L3 | concepts/taiwan-chip-flow-analysis.md §4.4 | 「集保 400 張以上大戶 / 20 張以下散戶」 | 大致正確 | 對應集保戶數統計分級界線，非官方「大戶/散戶」定義，屬研究慣例。 |
| L4 | concepts/taiwan-stock-market-structure.md §7.1 | 「國內 ETF 總資產規模超過 4 兆」「受益人數突破千萬」「投信持有市值 5–8 兆」 | 需驗證 | 2026 規模數字無法獨立核實（2025 記憶值：台股 ETF 規模約 3.6 兆、受益人數約千萬，投信持有約 4–5 兆）；量級合理但需以最新官方統計校準。 |
| L5 | concepts/taiwan-stock-market-structure.md §10.3 | 「瞬間價格穩定措施：3 分鐘內漲跌幅超過 3.5% → 冷卻 2 分鐘、每 30 秒試撮」 | 需驗證 | 一般股 3.5%/2 分鐘大方向正確；試撮間隔（20 秒 vs 30 秒）需查證交所現行營業細則。 |
| L6 | concepts/taiwan-fundamental-analysis-guide.md §5.2 | 前十大權值股表（台積電 30%+、國巨 <1% 等） | 大致正確 | 2024–2025 權重量級合理；排名細節（國巨是否前十）需按最新市值更新。 |
| L7 | entities/l1-t1-energy-transition.md | 「2024 全球新增再生能源 ~510 GW、光伏 ~450 GW」 | 大致正確 | IRENA 2025 統計為再生 ~585 GW、光伏 ~453 GW；510 略低，可校準。 |
| L8 | entities/l1-t1-energy-transition.md | 「2024 全球 EV 佔比 ~20%（中 ~50/歐 ~22/美 ~9）」；「1973 油價 $3→$12」「1979 $40」「1985 $10」「2008 $147」「2020 負油價」 | 正確 | 與公認歷史數據一致（EV 佔比為年末近似值）。 |
| L9 | entities/l1-t1-energy-transition.md | 「COP29（2024）再生能源三倍目標承諾」 | 需驗證 | 三倍目標 2023 COP28 拍板、COP29 重申；年份歸屬有偏移。 |
| L10 | entities/l1-t5-ai-semiconductor.md | 「TSMC 2027 規劃 1.4nm」；「Stargate 5 年 $5000 億」 | 需驗證 | 記憶值：A14（1.4nm）目標 2028；Stargate 公告為「4 年內 $500B」。 |
| L11 | entities/l1-t6-demographic-turning-point.md | 「日本 2024 出生率 ~1.2」「台灣 2024 出生率 0.865」 | 需驗證 | 記憶值：日本 2024 TFR 約 1.10（2023 為 1.20）；台灣 0.865 是 2023 值，2024 約 0.8x。年份標籤疑錯置。 |
| L12 | entities/l1-t4-critical-minerals.md | 「鋰：智利+澳洲+中國 ~75%」「再生銅 ~17%」 | 需驗證 | USGS 記憶值鋰礦三國合計約 85–90%；再生銅全球佔比常引 ~30%。 |
| L13 | templates/trigger-margin-350b.md | 檔名/標題「融資 3500 億」，觸發條件「retail_margin_balance > 5000 億」 | 過時（檔名） | 內容已更新為 5000 億門檻（2026-08-03 實值 5074.63 億），檔名與標題未同步。5000 億門檻本身：以 2026 市值（約 100–110 兆）與現代融資/市值比（約 0.5%）衡量，屬合理過熱線（2007 年 4129 億/23 兆 ≈ 1.8% 時代結構已不同）。 |
| L14 | templates 目錄 | 模板自述數量互不一致：「現有 12/13/14/16 模板」「第 14/16/17/18/20 模板」各檔不同 | 不一致 | 目錄紀律問題，非金融事實；但會干擾 monitor 對位。 |
| L15 | concepts/ 檔名 | atals-*（5 檔）與 atlas-*（3 檔）混用；domain-model §10「atals 平台」 | 不一致 | 命名不統一（atals vs atlas），跨檔 wikilink 亦混用。 |
| L16 | templates/trigger-taiwan-strait-tension.md | 「stress score -7.66 low」 | 需驗證 | 其他檔 stress 為 29.92–34.74（alert/low），-7.66 尺度不一致，疑為不同指標或資料異常。 |
| L17 | concepts/atals-mcp-tools-reference.md §8.3 vs atals-strategy-taxonomy.md §5.3 | `regime_get_history` 工具在 taxonomy/simulation-guide 出現，但 tools-reference 全表未列 | 不一致 | 工具清單缺漏或別名，內部文件不一致。 |
| L18 | entities/l1-t2-petrodollar-hormuz.md | 「霍爾木茲佔全球貿易 20% 石油 + 20% LNG + 35% 尿素 + 30% 磷酸鹽 + 50% 硫黃」「CIPS 月結算 ~RMB 11 兆」「央行美元儲備 58%（vs 2000 71%）」「央行黃金 2022 1136/2023 1037 噸」「G7 油價上限 $60」「上海原油期貨 2018」「沙國入 BRICS+ 2023」「CBAM 2026、EU ETS2 2027」 | 正確 | 與公認數據/事件一致（CIPS 為近似值；黃金連 3 年 >1000 噸正確）。 |
| L19 | entities/l1-t3-five-chains.md + t1-t4-signal-light.md | 「2024/8/2-5 三大法人賣超 1231 億」「2025/5/4-7 外資連 3 日買超 1460 億、量 1.52 兆」 | 需驗證 | 2024/8/2 外資單日 -966 億為記憶中事實，但「三大法人合計 1231 億」需查證（疑含其他口徑）；2025/5 數字無法核實。2024/9/4 SOX -7.75%、2025/2/3 DeepSeek 台股 -830 點為正確。 |
| L20 | entities/l1-t3-five-chains.md / l1-t2 / trigger-hbm / trigger-msci | 「2026/2/28 美以攻伊 + 霍爾木茲封鎖」「IEA -1100 萬桶/日」「SK Hynix -52%」「MSCI Taiwan 24.8% / Korea ~27%」「TSMC 2026 月營收 +67.87%」「2330 = 2370 元」等全部 2026 年內資料 | 需驗證 | 本審計員無法獨立核實 2026 年事件/點位；多檔互相引用、內部一致，但外部核實為空白。建議列為「2026 資料外部核實清單」。 |

---

# 憲章一致性問題

| # | 位置 | 問題 | 判定 |
|---|------|------|------|
| C1 | templates/trigger-megaproject-2-quarter-lag.md §7 | 「策略三分類 | 對位 Aggressive(押 AI 供應鏈)，不用於 Defensive / Tactical」 | **違背憲章**：AGENTS.md §12 明示策略三分類 archetype 中文正本 = 跟隨聰明錢/事件套利/資金對抗；Defensive/Aggressive/Tactical 是 E5a 策略類別分類，非 archetype。模板把兩者混為一談。 |
| C2 | concepts/funding-forces-taxonomy-e05-pending-approval.md（contested，待簽核） | 5 主體共振把憲章「行為層」（官股/散戶）與「官方層」（外資/投信/自營）同層計票 | **潛在衝突（未生效）**：憲章要求七維 3+2+2 三層分開、不可加權平均；E05 若簽核通過，其共振模型將混合行為層與官方層。檔內已自行標「待業主簽核」，且其核心訴求（代理不得冒充主體、缺資料不補零）與憲章精神一致。建議簽核時明確認定與 3+2+2 分層的關係。 |
| C3 | concepts/taiwan-financial-domain-model.md §10 vs atals-simulation-guide/strategy-taxonomy | L1–L5 平台詞彙定義互相矛盾（時間尺度 vs 訊號來源） | 內部矛盾（見 M16），需統一；不直接違背憲章但影響 agent 引用一致性。 |
| C4 | concepts/taiwan-stock-market-structure.md | 「2026/8 加權指數 43,119，市場處於 RISK_ON 盤整格局」 | 通過（雙層使用合法）：七時期（盤整）為真值、RISK_ON 為向下相容層，並列表述符合憲章。 |
| C5 | 七時期 | 本範圍 19+7 檔中幾乎沒有檔直接用七時期七名（低迷/轉折開高/上升/高原/盤整/轉折下壓/黑天鵝）；多用 RISK_ON/OFF/NEUTRAL/TRANSITIONAL 平台標籤 | 通過（未違背，但覆蓋不足）：平台檔使用向下相容層標籤可接受；trigger-megaproject §7 有「black_swan 時期 trigger 不主動推」的七時期對位，方向正確。 |
| C6 | 七維錢潮雷達 3+2+2 | taiwan-chip-flow-analysis §2、atals-mcp-tools-reference、atals-platform-overview §2.2/§6 均正確使用「3 官方 + 2 行為代理 + 2 領先訊號」且用「共識投票」非加權平均 | 通過。 |
| C7 | 六大觀測指標 | 模板群覆蓋：美台資金開關（DXY/US10Y/usd-twd）、美股科技動能（SOX/NVDA/TSM）、外資期現貨（foreign-3day、外資期貨 OI）、內資抗衡（投信/自營/官股）、散戶情緒（margin/retail）、事件觸發（MSCI/ETF/關稅/台海） | 通過，無衝突。 |

---

# trigger 模板合理性表

| 模板 | 觸發核心 | 判定 | 理由 |
|------|---------|------|------|
| trigger-2330-tsmc-swing | 2330 盤中振幅或 (last-open)/open > ±3% | 合理 | 權值股單日 ±3% 為顯著波動；檔內自警「(last-open)/open 不能冒充昨收漲跌幅」，誠實。 |
| trigger-ai-capex-guidance-cut | 雲端商 capex 指引從 >30% 下修至 <20%（任一）；反向 4 家同步 >50% | 合理（需驗證） | 事件型結構合理；atlas 欄位未驗證、需 web fallback（檔內已標）。2026 資料（NVDA +154% 等）需外部核實。 |
| trigger-cb-emergency-intervention | 任一亞洲央行單日匯市操作 > 50 億 USD | 合理 | 1997 IMF 韓國 584 億美元紓困金額正確；2022 BOK 干預約 400 億美元量級正確；50 億單日門檻可辨識「非常規操作」。 |
| trigger-cb-fx-intervention | USD_TWD > 32.3（近央行防線 32.5） | 需驗證 | 「32.5 防線」為 2024 語意；2026 現匯 32.38 貼近門檻，觸發頻率與 2026 匯率分布需校準（見 M18）。 |
| trigger-china-slowdown | TSMC 月營收 YoY > +50% + 出口電子月增 > 0 | 需驗證（邏輯弱） | 代理錯位 + 門檻極端 + 建議方向矛盾（見 M13）。 |
| trigger-dxy-us10y-weak | DXY < 100 | 合理 | 2024–2026 DXY 區間約 95–110，<100 屬弱美元、可作為亞洲重估觸發；hit_rate 0.68 為群組最佳。 |
| trigger-equipment-capex-external-report-cycle | 外部權威報告（WIR/HAI/BIS/IMF WEO）週期對位 | 合理 | UNCTAD WIR、Stanford HAI（4 月）、BIS 年報（6 月）、IMF WEO（4/10 月）時點正確；週期型設計與即時型分離正確。 |
| trigger-etf-rebalance | 成交量 > 0 | 過時/無鑑別力 | 恆真條件 + ETF 申購欄位為 0（見 M10）。 |
| trigger-foreign-3day-inflow | 外資單日 > +20 億 | 過時 | 門檻過低、名稱與條件不符、與庫內「100 億大動作」矛盾（見 M9）。 |
| trigger-hbm-cycle-cooling | SK Hynix 月跌 < -10% + HBM 連 2 月跌 < -5% + 雲端 capex 下修（AND） | 合理（需驗證） | 三項 AND 避免假警報，設計正確；SK Hynix -52%、TSMC↔SKH 連動 0.95 等 2026 數據需外部核實。 |
| trigger-hedge-fund-unwind | 個股 1 日 < -20% + ADR < -15% + 量 > 5 日均量 3x | 合理 | Archegos 案例正確（ViacomCBS/Discovery 2021/3/26 -27%、prime broker 拋售 $30B+）；三條件雙市場確認設計穩健。 |
| trigger-margin-350b | retail_margin_balance > 5000 億 | 內容合理 / 檔名過時 | 5000 億在 2026 年（市值 ~100–110 兆）≈ 融資/市值 0.5%，與 ETF 時代結構一致，屬合理過熱線；檔名/標題 3500 億未同步（見 L13）。 |
| trigger-megaproject-2-quarter-lag | 設備鏈月營收連 3 月 YoY > +30% + 投信連 5 日 > +20 億 | 合理（需驗證） | 設備 lag 6–18 月→量產 12–24 月邏輯成立；「投信連 5 日 >20 億」門檻偏高（投信單日 >20 億已屬強作帳日）；v0.3 已誠實 pivot 至 chips aggregate。 |
| trigger-msci-rebalance-pressure | MSCI Taiwan 單季 > +2pp 或 >30% 絕對值；Korea/Taiwan 下調 > 1.5pp | 需驗證（邏輯矛盾） | 反向機制敘述自相矛盾 + MSCI 檢討月份錯誤（見 M11）；MSCI Taiwan 24.8% 等 2026 權重需外部核實。 |
| trigger-nvda-tsm | NVDA 單日 > +2.0% | 需驗證 | 2025–2026 NVDA 日常波動 ±2–4%，+2% 門檻偏低；檔名 NVDA+TSM 但條件僅 NVDA（TSM 0.3% 未入條件）。 |
| trigger-retail-margin-decrease | 融資 > 5000 億（高水位） | 矛盾 | 標題「融資大減」與條件「融資過高」方向相反（見 M14）。 |
| trigger-sox-foreignflow | SOX change > 0% + 當日外資買超 | 過時 | SOX >0% 為擲硬幣級門檻，無鑑別力（hit_rate 0.33 佐證）。 |
| trigger-taiwan-strait-tension | geopolitical 評分 > 4 | 合理（需驗證） | 內部 scale 無法外部核實；同檔 stress -7.66 與其他檔尺度不一致（見 L16）。 |
| trigger-tariff-shock | USD_TWD > 32 + 出口電子 > 0 | 需驗證（邏輯缺口） | 無關稅變數（見 M12）。 |
| trigger-usd-twd-32 | USD_TWD > 32.3 | 需驗證 | 見 M18；方向邏輯（貶破 32.3 → 減半導體/加金融）需以 2026 匯率分布與外資行為校準。 |

---

# 各檔一句健康度

## concepts/（19 檔）
- atals-mcp-tools-reference.md：平台工具清單，市場事實極少；`regime_get_history` 等工具與其他檔清單不一致（L17）。健康度：中。
- atals-platform-overview.md：架構描述，無市場事實問題；「官方法人 T86 為主」為內部通道名。健康度：良。
- atals-risk-management-framework.md：**維持率 120% 處分門檻錯誤（H1）**；2008 台股 -50%+、2011/2015/2018/2020/2022 事件描述正確。健康度：差（1 個 HIGH）。
- atals-simulation-guide.md：L1–L5 定義與 domain-model 矛盾（M16）；其餘為流程描述。健康度：中。
- atals-strategy-taxonomy.md：L1–L5 定義與 domain-model 矛盾（M16）；其餘為通用分類學，無事實錯誤。健康度：良。
- atlas-mcp-failover-policy.md：fail-over 政策，無市場事實宣稱。健康度：良。
- atlas-mcp-interpretation-guide.md：解讀紀律，無市場事實宣稱；confidence 0–1 用法正確。健康度：良。
- atlas-three-paradigms-v0.2-summary.md：與 s-paradigm-redefinition 互相對位一致（S 不等於盤整期）。健康度：良。
- content-attribution-policy-2026-07-20.md：治理/歸屬守則，無市場事實宣稱（不評論治理流程）。健康度：良。
- funding-forces-taxonomy-e05-pending-approval.md：待簽核提案，自我標記完整；與憲章 3+2+2 分層有潛在衝突需簽核時裁決（C2）。健康度：中。
- s-paradigm-redefinition.md：kaecer 拍板定義，內部一致；2024/8、2025/2 案例正確，2026/6-7 案例需外部核實。健康度：良。
- t1-t4-signal-light.md：**外資「4 成成交」疑誤（M4）**；2024/9/4 SOX -7.75% 正確；2024/8/2 賣超 1231 億、2025/5 買超 1460 億需驗證（L19）。健康度：中。
- taiwan-chip-flow-analysis.md：**外資持股 20% 上限/50% 列管錯誤（H2）**、期貨淨多 10 萬口疑過高（M7）；3+2+2 分層與憲章一致；外資成交 25–35% 正確。健康度：差（1 個 HIGH）。
- taiwan-financial-domain-model.md：L1–L5 與信心分數 0–100 與他檔矛盾（M16/M17）；興櫃 ESM 拼字（L1）、權證美式（L2）；制度類定義（T+2、漲跌幅、融資成數 6 成）正確。健康度：中。
- taiwan-fundamental-analysis-guide.md：**半年報 Q2 60 天錯誤（H3）**、MA60 誤標月線（M8）；電子佔市值 70%、自然人成交 50–60%、殖利率 3–4% 大致正確；前十大權重表需更新（L6）。健康度：差（1 個 HIGH）。
- taiwan-money-flow-seven-institutional-buckets.md：研究草圖，自我標 low confidence；無市場事實錯誤；與 E05 互為 contested 對照（設計內）。健康度：良。
- taiwan-stock-market-structure.md：主 agent 深審中；本檔記錄其交叉矛盾：維持率 120%（H1）、台指期 8 契約月（M1）、維持率範例算式（M2）、權證 7%（M3）、T+3→2014 T+2（M5）、當沖稅 0.25/0.2%（M6）、ETF 規模需驗證（L4）。健康度：差（多項，主審處理）。
- taiwan-technical-analysis-guide.md：MA60 誤標月線（M8）；RSI 80/20、除權息計算、日均量 2500–4500 億等正確。健康度：良（1 個 LOW）。

## entities/（7 檔）
- l1-t-overview.md：**過時**（L1-T.1 內容錯位、T.4-6 標待補但已存在，M15）。健康度：差。
- l1-t1-energy-transition.md：歷史事件正確（1973/1979/1985/2008/2020/2022）；COP29 年份偏移（L9）、2030 燃氣 50%（M20）、再生 510 GW 略低（L7）；2025–2026 數字檔內自標「需逐項重查」。健康度：中。
- l1-t2-petrodollar-hormuz.md：石油美元歷史軌跡與全球數據多數正確（L18）；2010 石油進口國（M19）；2026 霍爾木茲事件鏈全部需外部核實（L20）。健康度：中。
- l1-t3-five-chains.md：海洋吸熱 91%、2010 稀土禁運等正確；2026 五鏈事件全部需外部核實（L20）；檔內已標 contested/待驗證。健康度：中。
- l1-t4-critical-minerals.md：稀土 60/90%、鈷 DRC 70%、鎵鍺銻石墨 2024 禁令正確；鋰 75%、再生銅 17% 需驗證（L12）。健康度：中。
- l1-t5-ai-semiconductor.md：2024 NVIDIA $3T/TSMC $1T、2022 ChatGPT 等正確；1.4nm 2027、Stargate 5 年需驗證（L10）。健康度：中。
- l1-t6-demographic-turning-point.md：中國 2022 負成長、印度 2023 超中國、非洲 2050 25 億、日本 1995 老齡化 24 年正確；日本/台灣出生率年份標籤疑錯置（L11）。健康度：中。

## queries/（8 檔）
- H1-H2-H3-replay-2026-07-17.md：事件回放，自我標 low/contested，誠實度佳；7/17 資料屬 2026 需外部核實。健康度：良。
- H1-H2-H3-extending-or-distributing-2026-07-18.md：D+1 回放，明確標 snapshot 延遲疑慮，資料衛生佳。健康度：良。
- atlas-mcp-capital-flow-history-truth-seeking-2026-07-19.md：程式碼層真相盤查，無市場事實宣稱；證據鏈完整。健康度：良。
- day-2-L1T3-three-dimensions-2026-07-17.md：MCP 補驗，結論保守（S 紊亂而非確認），符合紀律。健康度：良。
- e05-data-gap-research-2026-07-18.md：資料斷層研究，unknown≠neutral 原則正確。健康度：良。
- money-flow-research-card-2026-07-18.md：研究排程卡，無事實宣稱。健康度：良。
- regime-flip-confirmation-2026-07-19.md：regime 翻多檢驗，H4 可反駁假說設計正確。健康度：良。
- week-1-summary-2026-07-21.md：彙整頁，正確反映「Day 4–6 已建 T.1-T.6 頁」——與 l1-t-overview 的「待補」狀態矛盾（M15 佐證）。健康度：良。

## templates/（21 檔，含 audit-report 範本）
- audit-report.md：範本，n/a。健康度：良。
- trigger-2330-tsmc-swing.md：觸發設計合理；產業標籤錯植（M21）。健康度：中。
- trigger-ai-capex-guidance-cut.md：設計合理；2026 數據需核實。健康度：中。
- trigger-cb-emergency-intervention.md：設計與歷史金額正確。健康度：良。
- trigger-cb-fx-intervention.md：32.5 防線語意需校準（M18）。健康度：中。
- trigger-china-slowdown.md：代理錯位+方向矛盾（M13）。健康度：差。
- trigger-dxy-us10y-weak.md：門檻合理。健康度：良。
- trigger-equipment-capex-external-report-cycle.md：週期錨點正確。健康度：良。
- trigger-etf-rebalance.md：恆真條件，實質失效（M10）。健康度：差。
- trigger-foreign-3day-inflow.md：門檻過低+名實不符（M9）。健康度：差。
- trigger-hbm-cycle-cooling.md：AND 設計合理；2026 數據需核實。健康度：中。
- trigger-hedge-fund-unwind.md：Archegos 案例正確、三條件穩健。健康度：良。
- trigger-margin-350b.md：內容 5000 億合理、檔名過時（L13）。健康度：中。
- trigger-megaproject-2-quarter-lag.md：lag 邏輯合理；憲章誤用「Aggressive」（C1）；投信門檻偏高。健康度：中。
- trigger-msci-rebalance-pressure.md：機制敘述矛盾+MSCI 月份錯誤（M11）。健康度：差。
- trigger-nvda-tsm.md：門檻偏低、條件與檔名不符。健康度：中。
- trigger-retail-margin-decrease.md：標題與條件方向相反（M14）。健康度：差。
- trigger-sox-foreignflow.md：SOX >0% 無鑑別力。健康度：差。
- trigger-taiwan-strait-tension.md：設計可；stress 尺度異常（L16）。健康度：中。
- trigger-tariff-shock.md：無關稅變數（M12）。健康度：差。
- trigger-usd-twd-32.md：32.3 門檻需以 2026 分布校準（M18）。健康度：中。

---

# 審計員附註
- 本審計只對「台灣市場制度/歷史/全球已知數據」做判定；**2026 年內事件資料（霍爾木茲、五鏈耦合、韓股崩盤、MSCI 24.8%、2330=2370 等）全部標 [需驗證]**，因本審計員無法取得外部一手來源核實，且多檔互相引用造成「內部一致性 ≠ 外部真實性」的假象。
- 建議後續：把 L20 清單列為「2026 資料外部核實清單」，逐項以公開源（TWSE/TAIFEX/MSCI/IEA/公司月報）回填。
