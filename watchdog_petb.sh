#!/bin/bash
# 保姆 petb 版:fork_pet 死而复燃,直到 32 对全部"完整"
# (完整 = pair_status ∈ {done, censored}:fail-closed 校验——summary 必须
#  可 parse、tokens>0、branch/fork_turn 一致;只凭文件存在不算)
# 预算闸门持久化在 fork_pet 侧;闸门耗尽时保姆退休,不再空转复燃
cd "$(dirname "$0")"
set -a; source ./game4ai.env; set +a
# TARGET 数的是 pairs 2..31(pilot 0/1 已收口,不在复燃范围)
TARGET=30
LOG=petb.log
while true; do
  out=$(python3 - <<'EOF'
import sys
sys.path.insert(0, "tools")
import fork_pet
if not fork_pet._budget_room(fork_pet.load_budget()):
    print("BUDGET_EXHAUSTED")
else:
    done = sum(1 for i in range(2, 32)
               if fork_pet.pair_status(i) in ("done", "censored"))
    print(done)
EOF
)
  if [ "$out" = "BUDGET_EXHAUSTED" ]; then
    echo "[watchdog $(date '+%T')] token budget gate closed, retiring" >> "$LOG"
    break
  fi
  n="$out"
  if [ "$n" -ge "$TARGET" ] 2>/dev/null; then
    echo "[watchdog $(date '+%T')] $n/$TARGET petb pairs complete, retiring" >> "$LOG"
    break
  fi
  if ! ps -eo args | grep -q "[f]ork_pet.py --workers"; then
    echo "[watchdog $(date '+%T')] fork_pet gone ($n/$TARGET done), relaunching" >> "$LOG"
    python3 tools/fork_pet.py --workers 6 --pairs 32 --start 2 >> "$LOG" 2>&1 &
    sleep 5
  fi
  sleep 45
done
