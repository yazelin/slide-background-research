#!/usr/bin/env bash
S="$HOME/.claude/skills/codex-imagegen/codex-imagegen.sh"
while IFS='|' read -r name prompt; do
  [ -z "$name" ] && continue
  out="$PWD/raw/$name.png"
  [ -f "$out" ] && { echo "skip $name"; continue; }
  echo "=== $name"
  bash "$S" "$prompt" "$out" </dev/null 2>&1 | tail -2
done < prompts-r2.txt
