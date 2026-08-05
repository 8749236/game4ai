#!/bin/bash
# 保姆:orchestrator 死而复燃,直到 20 场战役 summary 齐(不以日志 ALL DONE
# 为准 —— append 日志里躺着上一轮的 ALL DONE,会误判)
cd /mnt/agents/game4ai
export GAME4AI_KEY=sk-xUbJx0h35abFPF2b94A46b7aD00d44DdBfA6747132BfAd81
TARGET=20
while true; do
  n=$(ls results/camp_*/run_*/summary.json 2>/dev/null | wc -l)
  if [ "$n" -ge "$TARGET" ]; then
    echo "[watchdog $(date '+%T')] $n/$TARGET campaigns done, retiring" >> wave2.log
    break
  fi
  if ! ps -eo args | grep -q "[o]rchestrate.py --workers 4"; then
    echo "[watchdog $(date '+%T')] orchestrator gone ($n/$TARGET done), relaunching" >> wave2.log
    python3 orchestrate.py --workers 4 >> wave2.log 2>&1
    sleep 5
  fi
  sleep 45
done
