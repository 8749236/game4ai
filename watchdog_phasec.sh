#!/bin/bash
# 保姆 phasec 版:fork_phasec 死而复燃,直到 10 对 eligible 全部"完整"
# (完整 = pair_status == "done":fail-closed 校验——summary 必须可 parse、
#  tokens>0、branch/path/fork_turn 一致;只凭文件存在不算)
# 预算闸门持久化在 fork_phasec 侧;闸门耗尽时保姆退休,不再空转复燃
cd "$(dirname "$0")"
set -a; source ./game4ai.env; set +a
TARGET=10
LOG=phasec.log
while true; do
  out=$(python3 - <<'EOF'
import sys
sys.path.insert(0, "tools")
import fork_phasec
if not fork_phasec._budget_room(fork_phasec.load_budget()):
    print("BUDGET_EXHAUSTED")
else:
    print(fork_phasec.count_eligible(0, 25))
EOF
)
  if [ "$out" = "BUDGET_EXHAUSTED" ]; then
    echo "[watchdog $(date '+%T')] token budget gate closed, retiring" >> "$LOG"
    break
  fi
  n="$out"
  if [ "$n" -ge "$TARGET" ] 2>/dev/null; then
    echo "[watchdog $(date '+%T')] $n/$TARGET eligible pairs complete, retiring" >> "$LOG"
    break
  fi
  if ! ps -eo args | grep -q "[f]ork_phasec.py --workers"; then
    echo "[watchdog $(date '+%T')] fork_phasec gone ($n/$TARGET done), relaunching" >> "$LOG"
    # 复燃命令必须与 phasec_go.sh 完全一致(smoke_phasec_go 把关)
    python3 tools/fork_phasec.py --workers 6 --eligible 10 --attempts 25 >> "$LOG" 2>&1 &
    sleep 5
  fi
  sleep 45
done
