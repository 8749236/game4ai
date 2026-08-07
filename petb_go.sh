#!/bin/bash
# petb 扩样一键点火(issue #21, 等周六全会拍板后运行)
# 批次: pairs 2..31(pilot 0/1 已收口), 30 对, workers 6
# workers=6 的依据: 2026-08-07 网关压测 8 并发仅轻微劣化, one-api 不限流;
# 瓶颈是 reasoning 模型生成速度, 不在网关。
# 预估: ~18M tokens ≈ $2 量级; ~15-20 min/对 ÷ 6 路 ≈ 1.5-2h
cd "$(dirname "$0")"
set -a; source ./game4ai.env; set +a
if [ -z "$GAME4AI_KEY" ]; then
  echo "GAME4AI_KEY missing — check game4ai.env" >&2; exit 1
fi
tmux new-session -d -s petb -c "$PWD" \
  'set -a; source ./game4ai.env; set +a; python3 tools/fork_pet.py --workers 6 --pairs 32 --start 2 >> petb.log 2>&1'
tmux new-session -d -s petb-watchdog -c "$PWD" 'bash watchdog_petb.sh'
sleep 2
tmux ls
echo "fired. tail -f petb.log to watch; analysis: python3 tools/analyze_petb.py"
