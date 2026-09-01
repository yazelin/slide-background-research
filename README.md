# 簡報背景怎麼做

一張 AI 生的背景圖好不好看，跟能不能拿來當簡報封面，是兩件事。這個 repo 講後面那件。

- **主頁**：https://yazelin.github.io/slide-background-research/
- **對照實驗投影片**：https://yazelin.github.io/slide-background-research/demo/
- **開源網頁簡報生態盤點**：https://yazelin.github.io/slide-background-research/ecosystem/

## 主頁講什麼

判準（什麼樣的圖能當背景）、提示詞的六段結構、三招各自的代價、讓背景動起來、手上有爛圖或完全沒有圖、用程式畫背景、檢查清單、驗證狀態。

每一節開頭有一句話的重點，每一個數字都出自 `experiments/verify.py`。

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

`verify.py` 把畫面切成六塊候選文字區，每塊量亮度標準差（要小於 0.12）與白字或黑字的 WCAG 對比度（至少一種要大於 5.0）。門檻訂 5.0 是因為任何平坦色塊都過得了 4.5，那條線擋不住東西。

`motion.sh` 的重點是把運鏡參數寫成 `1-cos(2*PI*on/N)`：這個式子首尾同值，所以第一幀跟最後一幀由結構保證一致，循環播放不會跳。實測首尾幀平均色差 0.46 與 2.54（滿分 255）。

原片畫面上打出來的兩段完整提示詞逐字收在 `原片提示詞-第4集.md`，第二輪的配方就是從那裡拆出來的。

`raw/` 與各個裁切目錄都沒有進 git。repo 裡只放縮過的 JPEG：投影片用的在 `demo/assets/`，筆記頁用的在 `img/`。

## 做法

兩支影片都沒有字幕軌，逐字稿是本機跑 whisper large-v3-turbo 轉的；文件版照原文整理。生態盤點是 2026-09-01 用 GitHub search API 撈十四組關鍵字，去重 289 個再人工篩成 36 個。

## 出處

影片與文件的方法、案例、提示詞塊，著作權屬於原作者「大师的AI小灶」，來源連結列在主頁第 10 節。這個 repo 只有整理、分析，以及我們自己生成的圖與程式。

## 授權

MIT，版權所有 林亞澤。
