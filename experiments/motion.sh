#!/usr/bin/env bash
# 從一張靜圖做無縫循環的運鏡影片。
# 首尾幀相同是「結構上保證」的：所有運鏡參數都寫成 1-cos(2*PI*on/N) 的形式，
# on=0 與 on=N 時值相同，所以最後一幀接回第一幀不會跳。
set -e
N=288          # 12 秒 x 24 fps
FPS=24
OUT=motion

mk() {  # mk <輸入> <輸出名> <z 表達式> <x 表達式> <y 表達式>
  ffmpeg -y -loglevel error -loop 1 -i "$1" \
    -vf "scale=2400:-2,zoompan=z='$3':x='$4':y='$5':d=$N:s=1600x900:fps=$FPS" \
    -frames:v $N -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p \
    -movflags +faststart -an "$OUT/$2.mp4"
  printf '%-28s %s KB\n' "$2.mp4" "$(( $(stat -c%s "$OUT/$2.mp4") / 1024 ))"
}

# 緩慢推近，中心固定：一進一出，回到原點
PUSH="1+0.10*(1-cos(2*PI*on/$N))/2"
CX="iw/2-(iw/zoom/2)"
CY="ih/2-(ih/zoom/2)"
mk r2-16x9/r2-galaxy-sailboat.png galaxy-push "$PUSH" "$CX" "$CY"

# 推近加橫移：往右飄再飄回來
DX="iw/2-(iw/zoom/2)+(iw*0.055)*(1-cos(2*PI*on/$N))/2"
mk r2-16x9/r2-glowing-horse.png horse-drift "$PUSH" "$DX" "$CY"
