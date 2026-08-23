# WP-8 外部來源校準驗證報告（VERIFICATION-BACKLOG C 類 10 條 + 快照標註）

- 驗證日期：2026-08-22
- 驗證方式：httpx 直抓官方/權威來源（irena.org / unfccc.int / pr.tsmc.com / openai.com / mhlw.go.jp / moi.gov.tw / icsg.org / pubs.usgs.gov / openapi.twse.com.tw），web_browser (Playwright) 輔助 JS 頁面；Wayback Machine 補 TSMC 官方新聞稿
- 檔案性質：證據檔（結論 + 直接引文 + URL + 抓取日）

---

## 1. l1-t1 2024 再生能源裝置容量 510 GW → **585 GW（IRENA）** — ✅ 已改

- wiki 原文：「2024 全球新增 ~510 GW(IEA),光伏單年新增 ~450 GW」
- 官方結論：2024 全球再生能源新增 **585 GW**（IRENA Renewable Capacity Statistics 2025）；光伏單年新增 **451.9 GW**（~450 GW 正確）；總裝置 4,448 GW；新增佔全球電力擴張 92.5%
- 直接引文：「With 585 GW of capacity additions, renewables accounted for over 90% of total power expansion globally in 2024… reaching 4 448 gigawatts (GW). The 585 GW addition last year indicates a 92.5% share of the total capacity expansion, and a record rate of annual growth (15.1%)… solar photovoltaics increased by 451.9 GW last year.」
- 來源：IRENA 新聞稿「Record-Breaking Annual Growth in Renewable Power Capacity」2025-03-26
- URL：https://www.irena.org/News/pressreleases/2025/Mar/Record-Breaking-Annual-Growth-in-Renewable-Power-Capacity
- 解讀：原「~510 GW」為 2023 年（IEA Renewables 2023 報導 ~507 GW）數字誤植至 2024；2024 官方 = 585 GW（IRENA）/ ~590 GW（IEA 預估）
- 套用：entities/l1-t1-energy-transition.md Step 1 改為「~585 GW、總裝置 4,448 GW（IRENA 2025，光伏 +451.9 GW）」

## 2. l1-t1 COP29 vs COP28 三倍目標年份 — **COP28（2023-12-13，Dubai）** — ✅ 已改

- wiki 原文：「2024 | COP29,再生能源三倍目標承諾」
- 官方結論：三倍再生能源目標出自 **COP28 全球盤點決議（UAE Consensus）**，2023-12-13 於杜拜通過；COP29（2024 Baku）主題為氣候金融（NCQG），非三倍目標
- 直接引文：「The stocktake calls on Parties to take actions towards achieving, at a global scale, a tripling of renewable energy capacity and doubling energy efficiency improvements by 2030.」
- 來源：UNFCCC 新聞稿「COP28 Agreement Signals 'Beginning of the End' of the Fossil Fuel Era」2023-12-13
- URL：https://unfccc.int/news/cop28-agreement-signals-beginning-of-the-end-of-the-fossil-fuel-era
- 套用：entities/l1-t1-energy-transition.md Step 2 表格改為「2023 | COP28(UAE Consensus),再生能源三倍目標承諾」

## 3. l1-t5 TSMC 1.4nm 目標年 2027 → **2028（A14 量產）** — ✅ 已改

- wiki 原文：「TSMC 2025 量產 2nm、2027 規劃 1.4nm」
- 官方結論：TSMC A14（1.4nm）**2028 量產**（2025-04-23 北美技術論壇宣布，2026-07-16 法說重申）
- 直接引文（TSMC 官方新聞稿）：「TSMC … today unveiled its next cutting-edge logic process technology, A14… Planned to enter production in 2028, the current A14 development is progressing smoothly with yield performance ahead of schedule.」
- 來源：TSMC 新聞稿「TSMC Unveils Next-Generation A14 Process at North America Technology Symposium」2025-04-23（pr.tsmc.com Cloudflare 擋直接抓取，經 Wayback Machine 快照 20260210192427 取證）
- URL：https://pr.tsmc.com/english/news/3228（快照：https://web.archive.org/web/20260210192427/https://pr.tsmc.com/english/news/3228）
- 次要佐證（[次要來源]）：Taiwan Wire 2026-07-16「Mass Production of A14 Process Slated for 2028: TSMC」（引述董事長劉德音法說：A14 商轉 2028、A13/A12 2029）https://taiwanwire.com/mass-production-of-a14-process-slated-for-2028-tsmc/
- 套用：entities/l1-t5-ai-semiconductor.md Step 1 改為「2028 規劃 1.4nm(A14 量產)」

## 4. l1-t5 Stargate 投資 5 年 $500B → **4 年 $500B** — ✅ 已改

- wiki 原文：「OpenAI Stargate 計畫 2025 起 5 年 $5000 億」
- 官方結論：Stargate 宣布 **$500B / 4 年**（2025-01-21），首期 $100B 立即部署；初始股東 SoftBank/OpenAI/Oracle/MGX
- 直接引文：「The Stargate Project is a new company which intends to invest $500 billion over the next four years building new AI infrastructure for OpenAI in the United States. We will begin deploying $100 billion immediately.」
- 來源：OpenAI 官網「Announcing The Stargate Project」2025-01-21
- URL：https://openai.com/index/announcing-the-stargate-project/
- 套用：entities/l1-t5-ai-semiconductor.md Step 1 改為「2025-01 宣布 4 年 $5000 億(首期 $1000 億)」

## 5. l1-t6 日本 2024 TFR ~1.2 → **1.15** — ✅ 已改

- wiki 原文：「日本 2024 出生率 ~1.2」
- 官方結論：日本 2024 合計特殊出生率（TFR）= **1.15**（較 2023 的 1.20 下降）；2024 出生數 686,061 人（史上最少）；粗出生率 5.7‰
- 直接引文（確定數 概況 PDF 15_gaikyouR06.pdf）：「また、合計特殊出生率 は 1.15 で、前年の1.20より低下している。」「出生数は 68万 6061人で…」
- 佐證（TFR 參考 PDF 18_tfrR06.pdf）：「令和６年の期間合計特殊出生率（1.15）」
- 來源：厚生労働省「令和6年(2024)人口動態統計（確定数）の概況」令和7年9月16日公布
- URL：https://www.mhlw.go.jp/toukei/saikin/hw/jinkou/kakutei24/index.html （PDF: /dl/15_gaikyouR06.pdf、/dl/18_tfrR06.pdf）
- 解讀：原「~1.2」是 2023 值（1.20）誤植到 2024
- 套用：entities/l1-t6-demographic-turning-point.md Step 1 改為「日本 2024 出生率 1.15（2023=1.20）」

## 6. l1-t6 台灣 2024 出生率 0.865 → **0.87（0.865 為 2023 值）** — ✅ 已改

- wiki 原文：「台灣 2024 出生率 ~0.865」
- 官方結論：台灣 2024（113年）總生育率 = **0.87**、粗出生率 **5.76‰**、出生數 13.49 萬人；**0.865 是 2023（112年）值**
- 直接引文（內政統計年報 113年 PDF）：「112 年 為 0.87 人…為歷年最低」「113 年粗出生率 5.76‰ 為歷年次低」「113 年嬰兒出生數 13 萬 4,769 人」
- 來源：內政部統計年報 113年「四、出生數、出生率及總生育率」（表 1-10/1-11；按發生日期）
- URL：https://www.moi.gov.tw/cl.aspx?n=15370（出生頁；PDF 經 ws.moi.gov.tw Download.ashx 取 22758 檔案）
- 佐證：中央社 2025-01-10「2024年全年新生兒數13萬4856人…年粗出生率千分之5.76」https://www.cna.com.tw/news/aipl/202501100114.aspx [次要來源]
- 套用：entities/l1-t6-demographic-turning-point.md Step 1/表格 改為「台灣 2024 出生率 0.87（2023 為 0.865）」

## 7. l1-t4 鋰礦三國佔比 ~75% → **維持（USGS 2024 = 74.2%）** — ✅ 驗證通過

- wiki 原文：「智利 + 澳洲 + 中國合計 ~75%(USGS 2024)」
- 官方結論：USGS MCS 2025（2024 產量）：澳洲 88,000 t + 智利 49,000 t + 中國 41,000 t = **178,000 / 240,000 t = 74.2% ≈ 75%**（wiki 值正確）
- 直接引文：「World Mine Production and Reserves: … Australia 91,700/88,000… Chile 41,400/49,000… China e35,700/41,000… World total (rounded) 204,000/240,000」
- 來源：USGS Mineral Commodity Summaries 2025（January 2025），LITHIUM 章
- URL：https://pubs.usgs.gov/periodicals/mcs2025/mcs2025-lithium.pdf
- 註：backlog 問「USGS 85-90%?」——該數字不符 2024 產量口徑（前三國 74.2%）；85-90% 可能混淆稀土加工（中國 ~85-90%）或 2023 產量口徑（前三國 82.7%）。wiki 維持 ~75%，補精確值 74.2%

## 8. l1-t4 再生銅佔比 ~17% → **~31%（ICSG Recycling Input Rate）** — ✅ 已改

- wiki 原文：「再生銅 ~17%(ICA)」
- 官方結論：ICSG World Copper Factbook 2025（2020 全球銅流模型）：**Recycling input rate (RIR) = 31%**；EoL recycling input rate = 16%（~17% 可能是此值之誤）；常引「~30% 再生」正確
- 直接引文：「10-yr avg Recycling indicator 31% | Recycling input rate 16% | EoL recycling input rate…」——注意 PDF 排版：31% 屬 recycling input rate（表頭 INDUSTRY GLOBAL FLOWS OF COPPER (2020) AND DERIVED RECYCLING RATES）
- 來源：ICSG World Copper Factbook 2025, Chapter 8 Copper Recycling, p.59
- URL：https://icsg.org/copper-factbook/（PDF 下載：https://icsg.org/download/2025-10-the-world-copper-factbook/…Factbook2025.pdf）
- 套用：entities/l1-t4-critical-minerals.md 改為「再生銅 ~31%(ICSG 2025 RIR)」

## 9. taiwan-fundamental-analysis-guide §5.2 前十大權值股 — **重算；國巨不在前十；台積電 ~43%** — ✅ 已改

- wiki 原文：前十表含「國巨 <1%」第 10 名、台積電 30%+
- 官方結論（證交所 2026-08-21 收盤價 × 已發行股數計算）：
  1. 台積電 2330 ~42.9%（**30%+ 成立**）
  2. 聯發科 2454 ~4.2%
  3. 台達電 2308 ~3.1%
  4. 鴻海 2317 ~2.4%
  5. 日月光投控 3711 ~1.8%
  6. 台光電 2383 ~1.4%
  7. 富邦金 2881 ~1.3%
  8. 南亞科 2408 ~1.3%
  9. 欣興 3037 ~1.2%
  10. 南亞 1303 ~1.0%
- **國巨（2327）市值排名約 60+（正確股本 5.15 億股 × 554 = 2,851 億），不在前十**
- 資料來源（官方 openapi）：
  - 收盤價：https://openapi.twse.com.tw/v1/exchangeReport/BWIBBU_d?response=json （Date 20260821）
  - 股本：https://openapi.twse.com.tw/v1/opendata/t187ap03_L?response=json （出表日期 1150822）
  - 計算：市值 = 收盤價 × 已發行普通股數（排除股本欄位異常/DR/特別股列）
- 套用：concepts/taiwan-fundamental-analysis-guide.md §5.2 表替換為 2026-08-21 快照排名，附驗證註記

## 10. SK-02/SK-20 2330 PE/PB 快照標註 — ✅ 已標（不改值）

- 現況：SK-02 frontmatter「stock_get_fundamentals (2330 PE 30.19/PB 9.57)」；SK-20「stock_get_quote(2330 現價 2425, 2026-08-01 23:42) + stock_get_fundamentals(PE 30.19/PB 9.57, 7/30)」
- 處理：不改數字（對位第五條鐵律——時點資料不得當當下值），加註 [2026-08-22 官方驗證:此為 2026-07-30~08-01 時點快照]
- 兩檔皆 < 9000B（SK-02 3296B、SK-20 4420B），可內聯標註
- 套用：skills/SK-02-feature-macro-interaction.md、skills/SK-20-size-group-robustness.md

---

## 未驗證/無來源項目（本批無）
- 無（C 類 10 條全數有官方來源結案）

## 給主 agent 的注意
- l1-t1「~510 GW(IEA)」誤植（2023 值）；l1-t5「2027 1.4nm」「5 年 Stargate」誤植；l1-t6 日本/台灣出生率年份誤植——均已改並標官方來源
- 鋰礦三國佔比維持原值（USGS 2024 = 74.2%，wiki ~75% 正確），backlog 提示的「85-90%」不成立
- 再生銅改為 ~31%（ICSG RIR）；原 ~17% 疑似 EoL recycling input rate 16% 之誤
- §5.2 前十表為 2026-08-21 快照（市值隨股價變動），國巨確定不在前十
