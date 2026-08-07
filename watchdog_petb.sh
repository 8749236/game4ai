#!/bin/bash
# 保姆 petb 版:fork_pet 死而复燃,直到 32 对全部"完整"
# (完整 = A支 summary 存在 且 (B支 summary 存在 或 A支 fork_turn=null 删失))
# 不以日志 ALL PAIRS DONE 为准;不数 summary 总数(删失对没有 B支,数不准)
cd "$(dirname "$0")"
set -a; source ./game4ai.env; set +a
TARGET=32
LOG=petb.log
while true; do
  n=$(python3 - <<'EOF'
import json, glob
done = 0
for a in glob.glob("results/petb_invulnerable/run_*/summary.json"):
    try:
        s = json.load(open(a))
    except Exception:
        continue
    b = a.replace("petb_invulnerable", "petb_vulnerable")
    import os
    if s.get("fork_turn") is None or os.path.exists(b):
        done += 1
print(done)
EOF
)
  if [ "$n" -ge "$TARGET" ]; then
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
