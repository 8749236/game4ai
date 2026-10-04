#!/bin/bash
# drift_go.sh — wave-6b 断崖漂移对照一键点火(主人 2026-10-04 拍板)
# drift_fric_3 / drift_fric_6 各 5 局,deepseek-v4-flash(静默路由 v4.1f),
# 配置逐项对齐历史 fric 行。复燃 = 同一条命令(orchestrate run 级断点续跑,
# 失败局 wiping 重试,同 fork 系纪律)。
cd "$(dirname "$0")"
set -a; source ./game4ai.env; set +a
if [ -z "$GAME4AI_KEY" ]; then
  echo "GAME4AI_KEY missing — check game4ai.env" >&2; exit 1
fi
tmux new-session -d -s drift -c "$PWD" \
  'set -a; source ./game4ai.env; set +a; python3 orchestrate.py --matrix drift --workers 2 >> drift.log 2>&1'
sleep 2
tmux ls
echo "fired. tail -f drift.log to watch"
