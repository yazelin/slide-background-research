#!/usr/bin/env bash
set -u
S="$HOME/.claude/skills/codex-imagegen/codex-imagegen.sh"
R="$PWD/raw"

src="$R/fix0-source.png"
if [ ! -f "$src" ]; then
  echo "=== 0 source"
  bash "$S" "A casually shot photo of a mid-rise office building on an overcast grey day, taken from street level. Distracting clutter fills the frame: parked cars along the kerb, traffic cones, a rubbish bin, overhead power cables crossing the sky, a lamp post cutting across the facade. Flat dull grey light, low contrast, slightly crooked framing, amateur smartphone snapshot with no artistic intent. Wide 16:9 landscape. No text, no letters, no watermark, no logos." "$src" </dev/null 2>&1 | tail -2
fi

step() {
  local out="$R/$1.png"; local ref="$2"; local prompt="$3"
  [ -f "$out" ] && { echo "skip $1"; return; }
  [ -f "$ref" ] || { echo "MISSING REF for $1"; return; }
  echo "=== $1"
  bash "$S" "$prompt" "$out" "$ref" </dev/null 2>&1 | tail -2
}

step fix1-weather "$src" "replace the overcast grey sky in image 1 with a clear late-afternoon sky, a warm low sun raking across the building facade, cool blue gradient higher up. Keep the building geometry, the camera angle and the framing exactly unchanged."
step fix2-declutter "$R/fix1-weather.png" "remove the distracting clutter from image 1: the parked cars, traffic cones, rubbish bin, overhead power cables and the lamp post. Keep the building, the sky and the framing exactly unchanged."
step fix3-focus "$R/fix2-declutter.png" "darken the surroundings and the foreground in image 1 so the building stays the single bright focus, and extend the frame upward to add clean empty sky above the building leaving room for a title. Wide 16:9 composition. Keep the building itself unchanged."
