"""smoke_petb_go: launch wiring (issue #21, GPT cat's launch gate).

The first fire (petb_go.sh) and every watchdog relaunch
(watchdog_petb.sh) must freeze the EXACT same runner flags — a drift
would silently flip the batch back to the pilot-compatible defaults
(service encounter, fixed treatment x path) or split the batch across
two protocols.

Run from the repo root:  python3 tests/smoke_petb_go.py
"""
import os
import re
import sys

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")


go = open(os.path.join(_root, "petb_go.sh"), encoding="utf-8").read()
wd = open(os.path.join(_root, "watchdog_petb.sh"), encoding="utf-8").read()

# the frozen launch protocol (master's 2026-08-08 ruling: gates 1/2 ON)
PAT = (r"python3 tools/fork_pet\.py --workers 6 --pairs 32 --start 2 "
       r"--encounter early --counterbalance")
go_cmds = re.findall(PAT, go)
wd_cmds = re.findall(PAT, wd)

check("petb_go.sh: first fire carries encounter+counterbalance flags",
      len(go_cmds) == 1, f"matches={len(go_cmds)}")
check("watchdog_petb.sh: relaunch carries the same flags",
      len(wd_cmds) == 1, f"matches={len(wd_cmds)}")

# no stray un-flagged fork_pet invocation left in either script
bare = re.compile(r"python3 tools/fork_pet\.py(?! --workers 6 --pairs 32 "
                  r"--start 2 --encounter early --counterbalance)")
check("no un-flagged fork_pet invocation anywhere in launch scripts",
      not bare.search(go) and not bare.search(wd), "")

print(f"\n{sum(RESULTS)}/{len(RESULTS)} checks passed")
sys.exit(0 if all(RESULTS) else 1)
