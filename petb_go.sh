#!/bin/bash
# petb 扩样一键点火(issue #21)
# 批次: pairs 2..31(pilot 0/1 已收口), 30 对, workers 6
# 门 1/2 主人 2026-08-08 拍板 ON: --encounter early --counterbalance
# (pilot 0/1 为旧口径 service+固定映射, analyzer 以 path=None 区分, 不混入)
# workers=6 的依据: 2026-08-07 网关压测 8 并发仅轻微劣化, one-api 不限流;
# 瓶颈是 reasoning 模型生成速度, 不在网关。
# 预估: ~18M tokens ≈ $2 量级; ~15-20 min/对 ÷ 6 路 ≈ 1.5-2h
# 注意: watchdog_petb.sh 的复燃命令必须与下面完全一致(smoke_petb_go 把关)
cd "$(dirname "$0")"
set -a; source ./game4ai.env; set +a
if [ -z "$GAME4AI_KEY" ]; then
  echo "GAME4AI_KEY missing — check game4ai.env" >&2; exit 1
fi
tmux new-session -d -s petb -c "$PWD" \
  'set -a; source ./game4ai.env; set +a; python3 tools/fork_pet.py --workers 6 --pairs 32 --start 2 --encounter early --counterbalance >> petb.log 2>&1'
tmux new-session -d -s petb-watchdog -c "$PWD" 'bash watchdog_petb.sh'
sleep 2
tmux ls
echo "fired. tail -f petb.log to watch; analysis: python3 tools/analyze_petb.py"
