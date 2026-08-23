---
title: 台股金融領域模型：十類核心術語與體系
created: 2026-08-02
updated: 2026-08-02
type: concept
tags: [framework, methodology]
sources:
  - atlas-mcp:macro_get_snapshot_latest
  - atlas-mcp:strategy_list_active
  - concepts/taiwan-money-flow-seven-institutional-buckets.md
confidence: medium
contested: false
contradictions: []
---

# 金融領域模型字典（台股 / atals 平台）

> **一句話**：本頁統整台股投資所需的 10 類核心金融術語（市場結構、交易制度、指數、法人參與者、基本面、技術面、籌碼面、總經、國際關聯、atals 平台專有名詞），作為知識庫的基礎字典，確保所有概念有一致的命名與定義。

> 本文件為機器人智能體（hermes agent、openclaw、codex 等）在輔助台股散戶投資人使用 atals 平台時的**領域基礎字典**。所有後續知識庫文件（指標說明、策略規則、API 契約、提示詞模板等）都應以本文件的術語定義為唯一依據。
>
> 命名規範：所有實體與指標以「中文名稱（英文／縮寫）」標記，便於跨文件引用與 LLM 解析。關聯欄位以 `→` 表示依賴或組成關係。

---

## 1. 市場結構類（Market Structure）

定義台灣資本市場的板塊切分與商品分類。

| 中文名稱 | 英文／縮寫 | 簡短定義 | 關聯術語 |
|---|---|---|---|
| 集中市場 | TWSE（Taiwan Stock Exchange） | 台灣證券交易所掛牌的主板市場，上市公司資本規模較大、掛牌條件嚴格 | → 加權指數、→ 上市股票、→ 漲跌幅 10% |
| 櫃檯市場 | TPEx（Taipei Exchange）／ OTC | 上櫃股票交易市場，多為中小型企業與成長型產業 | → 櫃買指數、→ 上櫃股票 |
| 興櫃市場 | ESM（Emerging Stock Market） | 未上市上櫃公司的股票議價買賣市場，資訊揭露強度介於兩者之間 | → 議價交易、→ 登錄股票 | [2026-08-22 驗證:Emerving→Emerging 拼字修正]
| 創櫃板 | Go Incubation Board | 提供微型創新企業股權籌資的板塊，掛牌門檻較低但無次級市場交易 | → 登錄股票、→ 籌資 |
| 期貨市場 | TAIFEX（Taiwan Futures Exchange） | 提供台股期貨、選擇權、小型台指等衍生性商品的交易所 | → 台指期、→ 選擇權、→ 保證金 |
| 權證 | Warrant（Call/Put） | 發行人（多為券商）發行的「可在到期前以約定價格買賣標的股票」的憑證 | → 標的股票、→ 發行券商、→ 行使比例 |
| 認購（售）權證 | Call / Put Warrant | 看好標的買 Call、看空標的買 Put，分為歐式與美式（台股權證歐式/美式並存，非全歐式；外國標的權證限歐式） | → 權證、→ 時間價值 | [2026-08-22 驗證:TWSE 官方 FAQ「持有人有權利在特定期間內(美式)或到期日(歐式)」;https://www.twse.com.tw/zh/page/products/securities/warrant/faq.html]
| ETF | Exchange-Traded Fund | 在交易所掛牌、被動追蹤指數或產業的基金，提供分散投資與流動性 | → 被動追蹤指數、→ 受益憑證、→ 折溢價 |
| 特別股 | Preferred Stock | 享有固定配息、但表決權有限的股票，常見於金融業 | → 普通股、→ 配息 |
| 普通股 | Common Stock | 標準上市公司股權，具有表決權與剩餘分配請求權 | → 每股盈餘、→ 股東會 |

---

## 2. 交易制度類（Trading Mechanism）

定義台股的交易與交割規則，這些制度直接影響策略可執行性。

| 中文名稱 | 英文／縮寫 | 簡短定義 | 關聯術語 |
|---|---|---|---|
| T+2 交割 | T+2 Settlement | 成交日後第二個營業日完成款券交割（買方付款、賣方交付股票） | → 交割風險、→ 違約 |
| 當沖 | Day Trading（Intra-day） | 同一交易日內買進與賣出同一標的，賺取價差；分為「現股當沖」與「資券當沖」 | → T+2 交割、→ 當沖保證金 |
| 融資 | Margin Buying | 向券商借錢買股，需自備一定成數的保證金；融資餘額代表槓桿買進意願 | → 融資成數、→ 維持率、→ 追繳 |
| 融券 | Short Selling（透過券商） | 向券商借股票賣出，看空後回補；融券餘額代表看空意願 | → 融券保證金、→ 回補 |
| 借券 | Securities Lending | 借出方把持有的股票借給借券方（多為避險或造市用途），借券賣出餘額為籌碼面訊號 | → 借券費率、→ 借券餘額 |
| 撮合制度 | Order Matching | 台股採「集合競價 + 逐筆撮合」混合制：開盤集合競價，盤中逐筆撮合 | → 集合競價、→ 逐筆撮合 |
| 漲跌幅限制 | Price Limit | 一般股票 10%、ETF 10%、權證依標的與到期日不同；處置股另計 | → 處置股、→ 熔斷 |
| 處置股票 | Disposition Stock | 異常交易被主管機關列管，採取分盤撮合或加嚴保證金 | → 異常交易、→ 警示股 |
| 盤中零股交易 | Odd-lot Trading | 盤中以不足一張（1000 股）為單位交易，便利小額投資人 | → 零股、→ 定期定額 |
| 競價交易 | Auction | 開盤與收盤前以集合競價決定開盤價與收盤價 | → 開盤價、→ 收盤價 |

---

## 3. 指數類（Indices）

台股用於衡量市場或產業表現的指數，是策略回測與訊號計算的標的。

| 中文名稱 | 英文／縮寫 | 簡短定義 | 關聯術語 |
|---|---|---|---|
| 加權指數 | TAIEX（Taiwan Capitalization Weighted Stock Index） | 集中市場所有上市股票依市值加權的綜合指數，台股最重要大盤指標 | → 集中市場、→ 市值加權 |
| 電子類指數 | TAIEX Electronics Index | 集中市場電子股族群加權指數，半導體與電子五哥占比高 | → 半導體、→ 台積電權值 |
| 金融類指數 | TAIEX Finance Index | 金融股族群加權指數，含金控、銀行、保險、證券 | → 金控、→ 金融股 |
| 傳產類指數 | TAIEX Non-Financial & Non-Electronics | 扣除電子與金融後的傳統產業指數 | → 塑化、→ 紡織、→ 鋼鐵 |
| 櫃買指數 | TPEx Index | 櫃檯市場上櫃股票的綜合指數，反映中小型股表現 | → 櫃檯市場、→ 上櫃股票 |
| 台灣 50 | FTSE Taiwan 50 Index | 由富時編製、涵蓋台股市值前 50 大成分股，被元大台灣 50 ETF（0050）追蹤 | → ETF、→ 0050、→ 被動追蹤指數 |
| 中型 100 | FTSE Taiwan Mid-Cap 100 Index | 由富時編製的台股中型股指數，被元大台灣中型 100 ETF（0051）追蹤 | → ETF、→ 0051 |
| MSCI 台灣指數 | MSCI Taiwan Index | 摩根士丹利編製、國際資金追蹤的台股指數，是外資被動配置的基準 | → 外資、→ 被動型 ETF |
| 臺灣永續指數 | TIP（FTSE4Good TIP） | 強調 ESG 篩選的台股指數，被 ESG ETF 追蹤 | → ESG、→ ETF |
| 台灣加權股價報酬指數 | TAIEX Total Return Index | 含現金股利再投資的報酬指數，用於計算長期投資總報酬 | → 現金股利、→ 殖利率 |

---

## 4. 法人與參與者類（Market Participants）

市場買賣的「誰」分類，影響籌碼面解讀與策略訊號。

| 中文名稱 | 英文／縮寫 | 簡短定義 | 關聯術語 |
|---|---|---|---|
| 外資 | Foreign Institutional Investors | 國外機構投資人（含 QFII 與外資自然人），買賣超金額為每日市場焦點 | → 三大法人、→ 匯率、→ MSCI 權重 |
| 投信 | Investment Trust（Domestic Funds） | 國內投信基金公司操作的共同基金，買賣超反映投信作帳與調倉行為 | → 三大法人、→ 基金規模、→ 投信作帳 |
| 自營商 | Proprietary Trader（Dealers） | 券商以自有資金在市場操作的部門，多為避險或造市部位 | → 三大法人、→ 避險、→ 造市 |
| 政府基金 | Government Fund（Labor Pension / Pension Fund） | 勞退基金、勞保基金、國安基金等政府操盤的長期資金 | → 國安基金護盤、→ 退撫基金 |
| 散戶 | Retail Investors | 自然人投資人，整體交易占比約 6 成；是市場流動性主要提供者 | → 自然人、→ 定期定額、→ 零股 |
| 主力 | Major Players | 市場口語，指大額交易人或具備資訊優勢的群體 | → 大額交易人、→ 主力指標 |
| 大額交易人 | Block Trader | 單筆成交達一定金額（如 100 萬以上）的買賣方，常見於董監事或法人交易 | → 主力、→ 內部人持股 |
| 內部人 | Insider | 公司董監事、經理人、大股東，受《證交法》規範持股異動申報 | → 內部人持股、→ 申報 |
| [[concepts/taiwan-money-flow-seven-institutional-buckets\|三大法人]] | Three Major Institutional Investors | 外資 + 投信 + 自營商 的合稱，每日買賣超合計為籌碼面核心訊號 | → 法人、→ 買賣超 |

---

## 5. 基本面指標（Fundamentals）

用於評估公司財務體質與合理股價的[[concepts/taiwan-fundamental-analysis-guide|基本面指標]]。

| 中文名稱 | 英文／縮寫 | 簡短定義 | 關聯術語 |
|---|---|---|---|
| 每股盈餘 | EPS（Earnings Per Share） | 稅後淨利 ÷ 流通在外加權平均股數；獲利能力的核心指標 | → 本益比、→ ROE、→ 配息 |
| 本益比 | PE Ratio（Price-to-Earnings Ratio） | 股價 ÷ EPS（或市值 ÷ 稅後淨利），衡量股價相對獲利的倍數 | → EPS、→ 估值 |
| 股東權益報酬率 | ROE（Return on Equity） | 稅後淨利 ÷ 平均股東權益，衡量公司用股東資金賺錢的效率 | → EPS、→ 杜邦分析 |
| 資產報酬率 | ROA（Return on Assets） | 稅後淨利 ÷ 平均總資產，衡量整體資產運用效率 | → ROE、→ 總資產週轉率 |
| 股價淨值比 | PB Ratio（Price-to-Book Ratio） | 股價 ÷ 每股淨值（或市值 ÷ 股東權益），常用於評價金融與傳產股 | → 每股淨值、→ 估值 |
| 殖利率 | Dividend Yield | 現金股利 ÷ 股價，反映現金回報率 | → 配息、→ 股利政策 |
| 營收成長率 | YoY Revenue Growth | 本期營收 ÷ 去年同期營收 − 1，反映業務動能 | → 營收、→ 月營收 |
| 毛利率 | Gross Margin | （營收 − 營業成本）÷ 營收，反映產品定價能力與成本結構 | → 營業利益率、→ 競爭優勢 |
| 自由現金流 | FCF（Free Cash Flow） | 營業現金流 − 資本支出，可用於配息、還債或再投資 | → 現金股利、→ 資本支出 |
| 每股淨值 | BVPS（Book Value Per Share） | 股東權益 ÷ 流通在外股數，PB 的分母 | → PB Ratio |

---

## 6. 技術面指標（Technicals）

由價格與成交量衍生、用於判斷趨勢、動能與反轉的[[concepts/taiwan-technical-analysis-guide|技術面指標]]。

| 中文名稱 | 英文／縮寫 | 簡短定義 | 關聯術語 |
|---|---|---|---|
| 移動平均線 | MA（Moving Average） | 過去 N 日收盤價的平均，常用 SMA（簡單）與 EMA（指數） | → 黃金交叉、→ 死亡交叉 |
| 黃金交叉 / 死亡交叉 | Golden / Death Cross | 短期 MA 向上穿越長期 MA 為黃金交叉，反之為死亡交叉 | → MA、→ 趨勢翻轉 |
| MACD | MACD（Moving Average Convergence Divergence） | 由 12 日 EMA − 26 日 EMA 衍生，包含 MACD 線、訊號線、柱狀圖 | → EMA、→ 動能 |
| RSI | RSI（Relative Strength Index） | 14 日漲跌幅推導的 0–100 動能指標，> 70 超買、< 30 超賣 | → 動能、→ 反轉 |
| KD 隨機指標 | KD（Slow Stochastic） | 反映當前收盤在近期高低區間的相對位置，含 K 值與 D 值 | → 動能、→ 交叉 |
| 布林通道 | Bollinger Bands | 由 N 日 SMA ± K 倍標準差構成，反映波動區間 | → 波動率、→ 均值回歸 |
| 均量 | Average Volume | 過去 N 日平均成交量，用於判斷量能是否擴張 | → 量價、→ 爆量 |
| 成交量 | Volume | 單日成交股數或金額，搭配價格拉升／下跌構成「量價」訊號 | → 量價背離 |
| 量價背離 | Volume-Price Divergence | 價格創新高但量未跟上，或反之，常視為趨勢動能減弱訊號 | → RSI、→ MACD |
| 趨勢線 / 支撐壓力 | Trendline / Support & Resistance | 從歷史高低點繪製的技術線，用於判斷趨勢與反轉區間 | → 突破、→ 回測 |

---

## 7. 籌碼面指標（Market Microstructure / Chips）

追蹤「誰在買、誰在賣、槓桿程度」的[[concepts/taiwan-chip-flow-analysis|籌碼面指標]]，是台股特有訊號來源。

| 中文名稱 | 英文／縮寫 | 簡短定義 | 關聯術語 |
|---|---|---|---|
| 三大法人買賣超 | Net Buy/Sell by Three Majors | 每日外資 + 投信 + 自營商買進金額 − 賣出金額的合計 | → 三大法人、→ 籌碼 |
| 外資買賣超 | Foreign Net Buy/Sell | 外資當日淨買入（正值）或淨賣出（負值）的金額 | → 外資、→ 匯率、→ MSCI 調權重 |
| 投信買賣超 | Investment Trust Net Buy/Sell | 投信當日淨買賣超，常用於觀察投信作帳行情 | → 投信、→ 季底作帳 |
| 自營商買賣超 | Dealer Net Buy/Sell | 自營商當日淨買賣超，含避險與造市部位 | → 自營商、→ 避險 |
| 融資餘額 | Margin Balance | 整體市場未償還的融資金額，視為槓桿買進意願指標 | → 融資、→ 維持率 |
| 融券餘額 | Short Balance | 整體市場未回補的融券張數，視為看空意願指標 | → 融券、→ 回補 |
| 借券賣出餘額 | Securities Lending Balance | 借券賣出未回補的數量，反映中性偏空訊號（避險與造市） | → 借券、→ 避險 |
| 大額交易人 | Large Trader | 單筆大額成交者，集中度常用來偵測主力動向 | → 主力、→ 集中度 |
| 主力集中度 | Major Holder Concentration | 前幾大買賣券商占比，常用以判斷籌碼是否集中 | → 主力、→ 分點 |
| 集保戶股權分散 | TDCC Distribution | 每週集保戶持股分散表，反映散戶與大戶持股分布變化 | → 散戶、→ 大戶 |
| 董監持股比例 | Insider Holding Ratio | 董監事與大股東持股比例，愈高代表與公司利益綁定愈深 | → 內部人、→ 申報 |

---

## 8. 總體經濟指標（Macro）

影響整體市場資金面與景氣循環的宏觀變數。

| 中文名稱 | 英文／縮寫 | 簡短定義 | 關聯術語 |
|---|---|---|---|
| 國內生產毛額 | GDP（Gross Domestic Product） | 一國一定期間內生產的所有最終商品與服務市場價值，反映景氣規模 | → 經濟成長率、→ 景氣循環 |
| 經濟成長率 | GDP Growth YoY | 名目或實質 GDP 較去年同期成長率 | → GDP、→ 景氣對策信號 |
| 消費者物價指數 | CPI（Consumer Price Index） | 衡量一般家庭購買商品與服務的價格變動 | → 通膨、→ 升息 |
| 核心物價指數 | Core CPI（Ex-Food & Energy） | 扣除食物與能源後的物價指數，反映長期通膨趨勢 | → CPI、→ 通膨預期 |
| 採購經理人指數 | PMI（Purchasing Managers' Index） | 50 為榮枯線，反映製造業景氣擴張或收縮 | → 景氣、→ 製造業 |
| 匯率 | FX（Foreign Exchange） | 新台幣對美元（USD/TWD）為主要參考匯率 | → 外資、→ 進出口、→ 央行 |
| 利率 | Policy Rate（央行重貼現率） | 央行政策利率，影響資金成本與股市估值 | → CPI、→ 升息、→ 降息 |
| M1B 貨幣供給 | M1B Money Supply | 活期存款 + 活期儲蓄存款 + 支票存款 + 通貨淨額，與台股相關性高 | → M2、→ 資金動能 |
| M2 貨幣供給 | M2 Money Supply | M1B + 定期存款 + 活期 + 外幣存款等，廣義貨幣總量 | → M1B、→ 貨幣政策 |
| 景氣對策信號 | Monitoring Indicator | 國發會發布的 9 顆燈號綜合判斷景氣（藍、黃藍、綠、黃紅、紅） | → GDP、→ PMI |
| 失業率 | Unemployment Rate | 勞動市場閒置指標，落後於景氣循環 | → 景氣、→ 內需 |

---

## 9. 國際關聯指標（International Linkages）

影響台股但由外部市場驅動的指標，台股具高度國際連動性。

| 中文名稱 | 英文／縮寫 | 簡短定義 | 關聯術語 |
|---|---|---|---|
| S&P 500 指數 | S&P 500 | 美國 500 大市值股票加權指數，全球最重要風險指標 | → 美元指數、→ 美債殖利率 |
| 那斯達克指數 | NASDAQ Composite | 美國科技股加權指數，與台股電子類高度連動 | → 電子類指數、→ 美股科技七雄 |
| 道瓊工業指數 | Dow Jones Industrial Average | 美國 30 檔藍籌股價格加權指數，反映成熟產業 | → 美股、→ S&P 500 |
| 標普 500 等權重 | S&P 500 Equal Weight | 不以市值加權的 S&P 500 版本，反映內部廣度 | → S&P 500、→ 市場廣度 |
| 費城半導體指數 | SOX（Philadelphia Semiconductor Index） | 美國 30 大半導體股加權指數，與台股半導體高度連動 | → 電子類指數、→ 台積電 ADR |
| 美元指數 | DXY（U.S. Dollar Index） | 美元對一籃子主要貨幣的綜合強度指數 | → 新台幣匯率、→ 新興市場資金流 |
| 新台幣匯率 | USD/TWD | 1 美元可兌換的新台幣金額，數字愈小代表新台幣愈強 | → 外資、→ 出口股 |
| 美國 10 年期公債殖利率 | U.S. 10Y Treasury Yield | 全球無風險利率基準，影響股票估值折現率 | → PE Ratio、→ 升息循環 |
| VIX 恐慌指數 | VIX（CBOE Volatility Index） | S&P 500 選擇權隱含波動率，> 30 視為市場恐慌 | → S&P 500、→ 避險情緒 |
| 台積電 ADR | TSM（Taiwan Semiconductor ADR） | 台積電在美掛牌的存託憑證，與台股現股高度連動 | → 台積電、→ 費半 |
| 標普 500 風險評價 | ERP（Equity Risk Premium） | 股票盈殖利率 − 公債殖利率，反映股票相對吸引力 | → 殖利率、→ 美債 |

---

## 10. atals 平台專有名詞（Platform Vocabulary）

atals 平台內部使用的概念，是策略、訊號、模擬相關對話的核心詞彙。

> 注：atals 平台為台股 AI 輔助投資工具，本節定義其內部術語，便於 LLM agent 在與平台 API 或 MCP 工具互動時精準對齊語意。

> 對齊 atlas internal/strategy_techniques/enums.go canonical 定義（L1 全球流動性 / L2 外資行為 / L3 產業催化 / L4 匯率籌碼 / L5 地緣政治）[2026-08-22 iter2]

| 中文名稱 | 英文／縮寫 | 簡短定義 | 關聯術語 |
|---|---|---|---|
| 策略 | Strategy | atals 平台對外提供的「可被啟用、評分、淘汰」的訊號組合單元；一個策略包含一組進入與退出規則 | → 策略層級、→ 回測 |
| 策略層級 L1–L5 | Strategy Layer L1–L5 | 平台將策略依「時間尺度 × 訊號來源」分為五層：L1 全球流動性、L2 外資行為、L3 產業催化、L4 匯率籌碼、L5 地緣政治 | → 策略、→ Darwinian 權重 |
| 訊號偵測器 | Signal Detector | 從原始市場資料（價格、法人、宏觀、新聞）萃取單一訊號的最小運算單元 | → 策略、→ 模板偵測器 |
| 模板偵測器 | Template Detector | 多個訊號偵測器組成的「主題型」觸發器（例如「外資連三買」+「融資增加」合併觸發） | → 訊號偵測器、→ 鏈式訊號 |
| 回測 | Backtest | 在歷史資料上重現策略以驗證績效，平台提供 Sharpe、最大回撤、勝率等指標 | → 策略、→ 模擬 |
| 模擬 | Simulation / Paper Trading | 在當前市場環境下，以虛擬資金執行策略的即時驗證 | → 回測、→ 滑價 |
| Darwinian 權重 | Darwinian Weight | 平台依策略近期表現動態調整其在組合中的權重，類似遺傳演算法的「適者生存」 | → 策略、→ 達爾文權重狀態 |
| 達爾文權重狀態 | Darwinian Status | 查詢目前哪些策略被加權、減碼或暫停的快照 | → Darwinian 權重、→ 策略暫停 |
| 風險暴露 | Risk Exposure | 投資組合目前的波動、VaR、最大回撤、集中度等風險指標 | → VaR、→ 集中度 |
| VaR | Value at Risk | 在給定信心水準（如 95%、99%）下，組合可能承受的最大損失 | → 風險暴露 |
| 壓力指數 | Stress Index（Taiwan Stress Index） | 平台根據多項宏觀與籌碼變數綜合出的台灣市場「壓力」分數，用於判斷風險胃納 | → 風險暴露、→ 宏觀 |
| 產業分類 | Sector | 台股產業分類，平台使用 20 大產業（如半導體、金融、塑膠等） | → ETF、→ 產業配置 |
| 板塊配置 | Sector Allocation | 投資組合中各產業的權重分配，平台提供目標／實際／差異的快照 | → 產業、→ 風險暴露 |
| 投資組合 | Portfolio | atals 帳號下管理的倉位，可分為模擬組合與實盤組合 | → 板塊配置、→ 風險暴露 |
| 訊號鏈 | Signal Chain | 多個訊號偵測器之間的因果觸發關係（例如：CPI 上升 → 央行升息 → 銀行股利多） | → 模板偵測器、→ 敘事模型 |
| 敘事模型 | Narrative Model | 平台把多個訊號鏈組合成「為什麼現在這樣」的宏觀故事模板 | → 訊號鏈、→ 事件 |
| 事件 | Event | 影響市場的重大事件（ETF 換股、MSCI 調權重、央行決策、財報等），平台以行事曆形式提供 | → 事件日曆、→ 預測 |
| 事件預測 | Event Forecast | 平台針對未來事件預測的資金流向（例如 ETF 換股可能買超 / 賣超個股） | → 事件、→ 資金流 |
| 信心分數 | Confidence Score | 訊號或預測的可信度數值，0–100；用於組合加權與否決門檻 | → 訊號、→ 風險 |
| 滑價 | Slippage | 實際成交價與預期價格的差異，回測與模擬的常見成本項 | → 模擬、→ 交易成本 |
| API 契約 | API Contract | atals 平台對外（HTTP 或 MCP）公開的介面定義，包含欄位、型別與意義 | → MCP、→ 工具 |
| MCP 工具 | MCP Tool | atals 平台以 Model Context Protocol 對外暴露的工具（`atlas-mcp_*` 命名空間），LLM agent 可直接呼叫 | → API 契約、→ 工具 |

---

## 領域關係圖（Domain Relationship Map）

以下以文字描述本字典中各概念間的層級與依賴關係。閱讀時請從宏觀往微觀、由「定義」走向「應用」。

### 上層：市場與制度

```
總體經濟（GDP / CPI / 利率 / M1B）
  │
  ├─→ 國際關聯（S&P 500 / 費半 / 美元指數 / 美債）
  │      │
  │      └─→ 外資買賣超 ─→ 集中市場 / 櫃買指數
  │
  ├─→ 匯率與利率 ─→ 資金成本 ─→ 估值（PE、PB）
  │
  └─→ 景氣循環 ─→ 企業獲利（EPS、ROE）
                       │
                       └─→ 個股基本面 → 合理股價 → 殖利率 → 投資組合
```

**說明**：宏觀變數決定資金面與景氣方向；國際市場決定外部風險偏好；兩者共同影響估值倍數（PE/PB）與企業獲利（EPS），進而決定個股的合理股價區間與最終投資組合報酬。

### 中層：市場結構與參與者

```
集中市場（TWSE） ─┬─→ 加權指數（TAIEX）
                 ├─→ 上市普通股
                 └─→ ETF ─→ 0050（追蹤台灣 50）

櫃檯市場（TPEx） ──→ 櫃買指數 ─→ 上櫃股票

期貨市場（TAIFEX）─→ 台指期 ─→ 避險 / 投機

參與者：
  外資 ─┐
  投信 ─┼─→ 三大法人買賣超 ─→ 籌碼面訊號
  自營商┘

  散戶 ──→ 量價、零股、定期定額

  政府基金 ──→ 護盤（國安基金）──→ 系統性風險介入
```

**說明**：市場結構決定標的可得性與流動性；參與者決定籌碼流向。籌碼面訊號與技術面訊號結合後，產生可執行的進出場訊號。

### 下層：指標層

```
基本面（EPS / PE / ROE / 殖利率）
  ├─→ 估值模型（合理價區間）
  └─→ 選股（體質過濾）

技術面（MA / MACD / RSI / KD / 布林通道）
  ├─→ 趨勢判斷
  └─→ 進出場時機

籌碼面（三大法人 / 融資融券 / 借券 / 大額交易人）
  ├─→ 主力動向
  └─→ 反轉訊號（領先基本面）
```

**說明**：基本面、技術面、籌碼面三類指標在策略中互補：基本面選股、技術面擇時、籌碼面避險。

### 平台層：atals

```
原始市場資料（價格、法人、宏觀、新聞）
  │
  ├─→ 訊號偵測器（Signal Detector）──→ 模板偵測器（Template Detector）
  │                                          │
  │                                          └─→ 訊號鏈（Signal Chain）
  │                                                     │
  │                                                     └─→ 敘事模型（Narrative Model）
  │
  ├─→ 策略層級 L1–L5 ──→ 回測（Backtest）──→ 模擬（Simulation）
  │                                              │
  │                                              └─→ Darwinian 權重 ──→ 投資組合（Portfolio）
  │
  └─→ 風險暴露（Risk Exposure）──→ 板塊配置（Sector Allocation）
                                          │
                                          └─→ 信心分數 / VaR / 壓力指數
```

**說明**：atals 平台以原始資料為輸入，經由「訊號偵測器 → 模板偵測器 → 訊號鏈 → 敘事模型」逐層抽象化產出市場觀點；策略層級與 Darwinian 權重把這些觀點轉換為可投資的組合；風險暴露與板塊配置則是投資組合的監控與調整介面。MCP 工具則是上述所有概念對外（對 LLM agent）暴露的介面層。

### 跨層依賴關係速查

| 來源層 | 影響層 | 典型傳導路徑 |
|---|---|---|
| 宏觀（升息） | 估值 | CPI ↑ → 央行升息 → 公債殖利率 ↑ → 股票 PE 下修 |
| 國際（費半） | 籌碼 | 費半 ↑ → 台積電 ADR ↑ → 台積電現股 ↑ → 電子類指數 ↑ |
| 籌碼（融資餘額） | 風險 | 融資餘額創高 → 維持率下降 → 追繳潮 → 系統性賣壓 |
| 基本面（殖利率） | 估值 | 殖利率 > 10 年期公債 → 股債利差擴大 → 資金轉進高息股 |
| 訊號偵測器（外資連買） | 策略 | 外資連三買 → 模板偵測器觸發 → 策略 L3 進場訊號 → 投資組合加碼 |
| 事件（MSCI 調權重） | 籌碼 | MSCI 調升 → 被動 ETF 買盤 → 個股量價齊揚 → 策略 L4 進場 |

---

## 使用規約

1. **唯一正本**：本文件是 `~/.config/opencode/knowledge/` 知識庫的基礎字典，所有後續文件（指標說明、策略規則、API 契約、提示詞模板）都應引用本文件的術語定義，不得自行創造同義詞。
2. **術語衝突優先序**：若其他文件定義與本文件不一致，**以本文件為準**；需修改時，請更新本文件後再傳播至下游。
3. **新增術語流程**：發現新術語時，請先判斷歸入哪一分類（1–10），補入對應表格並於「領域關係圖」中補上依賴邊。
4. **LLM agent 引用慣例**：在對話或工具呼叫中使用 `「中文名稱（英文／縮寫）」` 完整格式，便於跨上下文對齊。

---

## 參見

- [[concepts/taiwan-stock-market-structure]]
- [[concepts/taiwan-money-flow-seven-institutional-buckets]]
- [[concepts/taiwan-chip-flow-analysis]]
- [[concepts/taiwan-technical-analysis-guide]]
- [[concepts/taiwan-fundamental-analysis-guide]]
- [[concepts/atals-platform-overview]]
- [[concepts/atals-strategy-taxonomy]]
- [[concepts/atals-mcp-tools-reference]]

---

*本文件版本：v1.0  初稿*
*維護者：hermes agent / openclaw / codex 協作維護*
*適用範圍：atals 台股投資平台知識庫*