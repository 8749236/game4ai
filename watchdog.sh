#!/bin/bash
# 保姆:fork_phaseb 死而复燃。Phase B n=30 对已收口(2026-08-07),本脚本保留作模板。
# (不以日志 ALL PAIRS DONE 为准 —— append 日志里躺着上一轮的,会误判)
# 下一批(petb 扩样)复用时:改 TARGET/进程探针/复燃参数三处即可。
cd "$(dirname "$0")"
set -a; source ./game4ai.env; set +a
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
