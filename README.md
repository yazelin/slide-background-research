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
- **我們自己跑的對照實驗**：十九張自己生的圖加一支自己寫的 WebGL 背景，全部機械量測「還放不放得下字」。含一次抓錯視覺語言再修正的完整過程
- **開源網頁簡報生態盤點**：36 個 repo 分四類，含授權地雷與怎麼選
- 我們為什麼自製 slide-deck-skill，需求是什麼，跟 dashi-ppt-skill 差在哪

## experiments/

```bash
python3 verify.py --self-check                 # 工具本身的負控制
python3 verify.py raw/*.png r2-16x9/*.png      # 量測，寫出 verify-result.json
bash gen.sh          # 第一輪六張，攝影風（依 prompts.txt）
bash gen2.sh         # 第二輪四張，深色超現實（依 prompts-r2.txt）
bash gen3.sh         # 隨機性三張加配色三張（依 prompts-r3.txt）
bash gen-retouch.sh  # 修丑圖三步，image-edit 模式
bash motion.sh       # 從靜圖做無縫循環的運鏡影片（純 ffmpeg，不用生圖額度）
```

`motion.sh` 的重點是把所有運鏡參數寫成 `1-cos(2*PI*on/N)`：這個式子首尾同值，所以第一幀跟最後一幀由結構保證一致，循環播放不會跳。實測首尾幀平均色差 0.46 與 2.54（滿分 255）。

原片畫面上打出來的兩段完整提示詞逐字收在 `原片提示詞-第4集.md`，第二輪的配方就是從那裡拆出來的。

`raw/` 與各個 16:9 裁切目錄都沒有進 git（原圖 1.6 到 2.6 MB 一張）。repo 裡只放縮過的 JPEG：投影片用的在 `demo/assets/`，筆記頁用的在 `img/`。

`verify.py` 把畫面切成六個候選文字區，每區量亮度標準差（要小於 0.12）與白字或黑字的 WCAG 對比度（至少一種要大於 5.0）。門檻訂 5.0 是因為任何平坦色塊都過得了 4.5，那條線擋不住東西。

## 做法

兩支影片都沒有字幕軌，逐字稿是本機跑 whisper large-v3-turbo 轉的；文件版照原文整理。生態盤點是 2026-09-01 用 GitHub search API 撈的，星數與更新日期都是當天的值。

## 出處

影片與文件的方法、案例、提示詞塊，著作權屬於原作者「大师的AI小灶」，來源連結列在筆記第 14 節。這個 repo 只有整理、分析，以及我們自己生成的圖與程式。

## 授權

MIT，版權所有 林亞澤。
