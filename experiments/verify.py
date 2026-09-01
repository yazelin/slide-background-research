#!/usr/bin/env python3
"""機械驗收：一張背景圖到底還放不放得下字。

判準跟人眼無關，只看兩件事：
  平坦度 —— 候選文字區的亮度標準差。花紋太多，字就會被吃掉。
  對比度 —— 該區平均亮度對白字或黑字的 WCAG 對比度，至少要有一邊過 5.0。

候選區是九宮格外圈的六塊（避開正中央，標題很少放正中），
每塊佔畫面寬 44%、高 30%。任何一塊過關，這張圖就算能用，
並回報過關的那一塊在哪、留多少餘裕。

用法：python3 verify.py raw/*.png
"""
import sys
import json
import numpy as np
from PIL import Image

FLAT_MAX = 0.12      # 亮度標準差上限
CONTRAST_MIN = 5.0   # 比 WCAG AA 的 4.5 再嚴一點：任何平坦色塊都過得了 4.5，
                     # 門檻拉到 5.0 才擋得住「既不夠亮也不夠暗」的中間調

ZONES = {
    "左上": (0.04, 0.08), "中上": (0.28, 0.08), "右上": (0.52, 0.08),
    "左下": (0.04, 0.60), "中下": (0.28, 0.60), "右下": (0.52, 0.60),
}
ZONE_W, ZONE_H = 0.44, 0.30


def relative_luminance(rgb):
    """WCAG 相對亮度，輸入是 0..1 的 sRGB 三通道。"""
    c = np.where(rgb <= 0.03928, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def contrast(l1, l2):
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def measure(path):
    im = Image.open(path).convert("RGB")
    arr = np.asarray(im, dtype=np.float64) / 255.0
    lum = relative_luminance(arr)
    h, w = lum.shape

    zones = []
    for name, (zx, zy) in ZONES.items():
        x0, y0 = int(zx * w), int(zy * h)
        x1, y1 = int((zx + ZONE_W) * w), int((zy + ZONE_H) * h)
        patch = lum[y0:y1, x0:x1]
        mean, std = float(patch.mean()), float(patch.std())
        c_white = contrast(1.0, mean)
        c_black = contrast(0.0, mean)
        best_ink = "白字" if c_white >= c_black else "黑字"
        best_c = max(c_white, c_black)
        ok = std <= FLAT_MAX and best_c >= CONTRAST_MIN
        zones.append({
            "zone": name, "mean": round(mean, 4), "std": round(std, 4),
            "ink": best_ink, "contrast": round(best_c, 2), "ok": ok,
        })

    passed = [z for z in zones if z["ok"]]
    # 過關的區裡，挑對比度最高的當代表
    best = max(passed, key=lambda z: z["contrast"]) if passed else \
        min(zones, key=lambda z: z["std"])
    return {
        "file": path,
        "size": [w, h],
        "pass": bool(passed),
        "pass_count": len(passed),
        "best": best,
        "zones": zones,
    }


def main(paths):
    results = [measure(p) for p in paths]
    for r in results:
        mark = "可用" if r["pass"] else "不可用"
        b = r["best"]
        print(f"{mark}  {r['file']}")
        print(f"      過關區塊 {r['pass_count']}/6　代表區「{b['zone']}」"
              f"　平坦度 std={b['std']}（上限 {FLAT_MAX}）"
              f"　{b['ink']}對比 {b['contrast']}（下限 {CONTRAST_MIN}）")
    with open("verify-result.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n寫入 verify-result.json，共 {len(results)} 張，"
          f"{sum(1 for r in results if r['pass'])} 張可用")
    return 0


def _self_check():
    """跑得動的自我檢查：純黑圖必過、雜訊圖必不過。"""
    import tempfile
    import os
    ok = True
    with tempfile.TemporaryDirectory() as d:
        flat = os.path.join(d, "flat.png")
        Image.new("RGB", (640, 360), (10, 10, 12)).save(flat)
        r = measure(flat)
        assert r["pass"] and r["pass_count"] == 6, "純黑圖應該六區全過"

        noisy = os.path.join(d, "noisy.png")
        rng = np.random.default_rng(0)
        Image.fromarray(rng.integers(0, 256, (360, 640, 3), dtype=np.uint8)).save(noisy)
        r = measure(noisy)
        assert not r["pass"], "隨機雜訊圖應該一區都不過"

        # 亮度落在 0.16 到 0.20 之間的中間調，白字黑字都不夠對比
        dead = os.path.join(d, "deadzone.png")
        Image.new("RGB", (640, 360), (117, 117, 117)).save(dead)
        r = measure(dead)
        assert not r["pass"], "中間調死區平坦但兩種字色都不夠對比，應該不過"

        # 稍微暗一點就過得了，黑字可讀
        usable = os.path.join(d, "usable.png")
        Image.new("RGB", (640, 360), (128, 128, 128)).save(usable)
        r = measure(usable)
        assert r["pass"] and r["best"]["ink"] == "黑字", "中灰應該以黑字過關"
    print("self-check 通過：純黑過、雜訊不過、中間調死區不過、中灰以黑字過")
    return 0 if ok else 1


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "--self-check":
        sys.exit(_self_check())
    sys.exit(main(args))
