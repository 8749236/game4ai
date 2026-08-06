#!/bin/bash
# 保姆:fork_phaseb 死而复燃,直到 Phase B 的 10 对(20 个 branch summary)齐
# (不以日志 ALL PAIRS DONE 为准 —— append 日志里躺着上一轮的,会误判)
cd /mnt/agents/game4ai
export GAME4AI_KEY=sk-xUbJx0h35abFPF2b94A46b7aD00d44DdBfA6747132BfAd81
TARGET=20
while true; do
  n=$(ls results/forkb_*/run_*/summary.json 2>/dev/null | wc -l)
  if [ "$n" -ge "$TARGET" ]; then
    echo "[watchdog $(date '+%T')] $n/$TARGET fork branches done, retiring" >> phaseb.log
    break
  fi
  if ! ps -eo args | grep -q "[f]ork_phaseb.py --workers"; then
    echo "[watchdog $(date '+%T')] fork_phaseb gone ($n/$TARGET done), relaunching" >> phaseb.log
    python3 tools/fork_phaseb.py --workers 5 >> phaseb.log 2>&1 &
    sleep 5
  fi
  sleep 45
done
