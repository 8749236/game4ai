"""smoke_phasec_go: launch wiring for wave-4c (issue #14).

The first fire (phasec_go.sh) and every watchdog relaunch
(watchdog_phasec.sh) must freeze the EXACT same runner flags — a drift
would silently split the batch across two protocols (different eligible
targets or attempt windows).

Run from the repo root:  python3 tests/smoke_phasec_go.py
"""
import os
import re
import sys

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")


go = open(os.path.join(_root, "phasec_go.sh"), encoding="utf-8").read()
wd = open(os.path.join(_root, "watchdog_phasec.sh"), encoding="utf-8").read()

# the frozen launch protocol
PAT = (r"python3 tools/fork_phasec\.py --workers 6 --eligible 10 "
       r"--attempts 25")
go_cmds = re.findall(PAT, go)
wd_cmds = re.findall(PAT, wd)

check("phasec_go.sh: first fire carries the frozen runner flags",
      len(go_cmds) == 1, f"matches={len(go_cmds)}")
check("watchdog_phasec.sh: relaunch carries the same flags",
      len(wd_cmds) == 1, f"matches={len(wd_cmds)}")

# no stray un-flagged fork_phasec invocation left in either script
bare = re.compile(r"python3 tools/fork_phasec\.py(?! --workers 6 "
                  r"--eligible 10 --attempts 25)")
check("no un-flagged fork_phasec invocation anywhere in launch scripts",
      not bare.search(go) and not bare.search(wd), "")

print(f"\n{sum(RESULTS)}/{len(RESULTS)} checks passed")
sys.exit(0 if all(RESULTS) else 1)
