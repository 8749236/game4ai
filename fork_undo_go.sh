#!/bin/bash
# fork_undo 一键点火(issue #21, GPT 猫 2026-08-15 裁决: 三阶 Undo 探针)
# 14 个存量前缀(猫第一次自发存档处) x 双臂 pet_restore=allowed/sticky,
# 双臂对称读档(猫自己的快照), 每臂 10 个全新回合, 同一只猫两条命。
# 预算: 夜班帽 2M/晚(装置内置, 到帽干净退场), 总帽 4M;
# 闸门持久化在 results/undo_budget.json。
# 复燃 = 同一条命令再来一遍(装置 fail-closed, pair 级断点续跑), 无需 watchdog。
cd "$(dirname "$0")"
set -a; source ./game4ai.env; set +a
if [ -z "$GAME4AI_KEY" ]; then
  echo "GAME4AI_KEY missing — check game4ai.env" >&2; exit 1
fi
tmux new-session -d -s fork_undo -c "$PWD" \
  'set -a; source ./game4ai.env; set +a; python3 tools/fork_undo.py --workers 6 >> fork_undo.log 2>&1'
sleep 2
tmux ls
echo "fired. tail -f fork_undo.log to watch"
