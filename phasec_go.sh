#!/bin/bash
# wave-4c 一键点火(issue #14, GPT 猫 2026-08-09 裁决: R3 vs R4 最小配对)
# 目标: 10 对 eligible( screened 不计数 ), 最多 25 次尝试, workers 6
# 预算帽 12M(主人 2026-08-09 拍板 "10M+ 量大管饱"), 闸门持久化在
# results/phasec_budget.json; 预估 6-9M, ~1.5-2.5h
# 注意: watchdog_phasec.sh 的复燃命令必须与下面完全一致(smoke_phasec_go 把关)
cd "$(dirname "$0")"
set -a; source ./game4ai.env; set +a
if [ -z "$GAME4AI_KEY" ]; then
  echo "GAME4AI_KEY missing — check game4ai.env" >&2; exit 1
fi
tmux new-session -d -s phasec -c "$PWD" \
  'set -a; source ./game4ai.env; set +a; python3 tools/fork_phasec.py --workers 6 --eligible 10 --attempts 25 >> phasec.log 2>&1'
tmux new-session -d -s phasec-watchdog -c "$PWD" 'bash watchdog_phasec.sh'
sleep 2
tmux ls
echo "fired. tail -f phasec.log to watch; analysis: python3 tools/analyze_phasec.py"
