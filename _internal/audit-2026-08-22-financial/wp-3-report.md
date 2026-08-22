# WP-3 跨頁口徑矛盾修復報告

- 執行時間: 2026-08-22 (audit-fix)
- 分支: feat/20260822-financial-audit-fixes (主 agent 統一 commit,本 worker 未跑任何 git)
- 備份: 11 檔均已 cp 為 `<file>.bak.20260822-audit-fix`
- 對應審計: child-A-sk-quant.md (C1–C7 全數處理)

## 逐檔修改點 + bytes

| 檔案 | 修正項 | before (B) | after (B) | 說明 |
|------|--------|-----------|-----------|------|
| SK-01-factor-library.md | C1 | 8896 | 8996 | 一句話定位後加壓縮單行口徑註: 336 月 vs 理論 340 月差額 + 60-70%/90%+ 兩口徑,定義待註 |
| SK-06-elastic-net.md | C1+C2 | 3125 | 3449 | 60 月樣本口徑註(滾動 window 語意,全樣本 336 月) + Step 3 預期排名 vs 合成資料實測註 |
| SK-08-pcr.md | C2 | 2640 | 2817 | Step 3 加「PLS>PCR>OLS 僅小樣本弱訊號成立」口徑註 |
| SK-09-pls.md | C1+C2 | 4562 | 4886 | 12 月樣本口徑註(滾動 window 語意) + Step 3 預期排名口徑註 |
| SK-10-random-forest.md | C2 | 3005 | 3182 | Step 3 加「RF 優 10-20% 僅小樣本弱訊號成立」口徑註 |
| SK-11-neural-network.md | C3 | 3039 | 3201 | Step 1 隨機 6:2:2 前視洩漏警示(正式評估走 SK-03) |
| SK-13-permutation-importance.md | C3 | 5266 | 5428 | Step 1 隨機 8:2 前視洩漏警示(正式評估走 SK-03) |
| SK-17-portfolio-weighting.md | C4 | 4421 | 4460 | 學術發現改為「文獻口徑分歧」(等權毛 Sharpe 通常較高;value-weighted 換手低/可執行性高) + G 段殘留矛盾句一併修正 |
| SK-20-size-group-robustness.md | C5+C6 | 6266 | 6640 | PB/PE 非規模代理警示(待 atlas 暴露市值欄位) + 18 vs 38 vs 47 產業口徑註 |
| SK-32-reward-sensitivity.md | C7 | 3280 | 3355 | experiment_diff 400 敘述改為 2026-08-07 SK-22 參數名誤判更新,端點可用 |
| SK-36-sl-vs-rl.md | C7 | 3551 | 3605 | 同上,experiment_diff 400 敘述改為可用性更新 |

## 驗收
- 全部一行式口徑註記落地,含 [2026-08-22 audit-fix] timestamp。
- 全部 ≤ 9000 B: SK-01=8996 B(最緊),其餘最大 SK-20=6640 B。

## 偏離任務書之處(均為容量/一致性必要調整,已標註)
1. **SK-01 註記壓縮**:任務書建議 ≤150B,但 SK-01 原 8896B、硬上限 9000B 只剩 104B headroom;依任務書「該頁註記必須單行精簡」原則,壓縮為 97B 單行,保留全部事實元素(336 vs 理論 340 差額、60-70%/90%+ 兩口徑、定義待註)。
2. **SK-17 G 段加改一句**:C4 修正後,G 段殘留「學術研究 value-weighted 勝率較高」會與修正後文獻口徑矛盾,一併改為「文獻結論分歧(見論文版概念)」,消除頁內自相矛盾(即 C4 目標本身)。
3. **C7 採「替換」而非「並存」**:原 400 錯誤敘述已證實為誤判,若並存註記會留下矛盾;直接替換原 claim 為可用性更新,保留「需真 experiment_id / client 4 輪 experiment」等仍有效之細節。

## 未處理(超出白名單/任務書)
- SK-21/23 的 38/47 產業數字本身不在白名單,僅在 SK-20 加交叉口徑註。
- SK-20 表格內「用 PB 估值反推市值分組」工作描述保留(警示行已標明正確做法);表格行改寫屬段落重寫,超出契約範圍,如需改可另派。
