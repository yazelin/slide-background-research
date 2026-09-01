# 簡報背景研究筆記

拆兩支「用 AI 做簡報」的影片與三份對照文件，加上我們自己跑的對照實驗與開源生態盤點。

線上閱讀：https://yazelin.github.io/slide-background-research/
對照實驗投影片：https://yazelin.github.io/slide-background-research/demo/

## 內容

- 判準：什麼樣的圖能當簡報背景（留白、單一視覺中心、可控對比、敘事張力）
- 方法一　尺度失衡：把主體放進不屬於它的宏大情境
- 方法二　光：在平淡畫面加一個發光元素製造視覺中心
- 提示詞的四段結構，附中英提示詞塊對照表
- 靜態圖轉動態背景的運鏡公式與無限循環做法
- 手上已有醜圖的三步搶救法，以及整份簡報沒有圖的時候怎麼辦
- **我們自己跑的 A/B 對照實驗**：六張自己生的圖，機械量測「還放不放得下字」
- **開源網頁簡報生態盤點**：36 個 repo 分四類，含授權地雷與怎麼選
- 我們為什麼自製 slide-deck-skill，需求是什麼，跟 dashi-ppt-skill 差在哪

## experiments/

```bash
python3 verify.py --self-check     # 工具本身的負控制
python3 verify.py raw/*.png        # 量測，寫出 verify-result.json
bash gen.sh                        # 依 prompts.txt 重生六張圖（走 Codex CLI $imagegen）
```

`raw/` 沒有進 git（原圖 1.6 到 1.8 MB 一張），repo 裡只放縮到 1600×900 的 JPEG，在 `demo/assets/`。

`verify.py` 把畫面切成六個候選文字區，每區量亮度標準差（要小於 0.12）與白字或黑字的 WCAG 對比度（至少一種要大於 5.0）。門檻訂 5.0 是因為任何平坦色塊都過得了 4.5，那條線擋不住東西。

## 做法

兩支影片都沒有字幕軌，逐字稿是本機跑 whisper large-v3-turbo 轉的；文件版照原文整理。生態盤點是 2026-09-01 用 GitHub search API 撈的，星數與更新日期都是當天的值。

## 出處

影片與文件的方法、案例、提示詞塊，著作權屬於原作者「大师的AI小灶」，來源連結列在筆記第 14 節。這個 repo 只有整理、分析，以及我們自己生成的圖與程式。

## 授權

MIT，版權所有 林亞澤。
