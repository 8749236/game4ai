"""smoke_soc: the evidence_soc instrumentation flag (BACKLOG C / issue #17).

Proves, without any LLM:
  1. default world: soc alert query answers, writes NO evidence line, and
     does not advance the world tick (v0.4 byte-level status quo);
  2. default world: unknown soc cmds still error;
  3. evidence_soc=on: the query is logged under the soc role and the tick
     advances like every other service;
  4. evidence_soc=on + reskin: the record carries the display name and
     summarize_evidence counts it via role mapping;
  5. config spine: evidence_soc defaults to False.

Run from the repo root:  python3 tests/smoke_soc.py
"""
import json
import os
import subprocess
import sys
import tempfile
import time

sys_path_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (sys_path_root, os.path.join(sys_path_root, "tools")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from netutil import call
from world import HOST, PORTS
from aggregate import summarize_evidence
from config import FLAGS

PY = sys.executable
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")


def start(log, cfg=None):
    args = [PY, "server.py", log]
    if cfg is not None:
        with open(log + ".cfg.json", "w", encoding="utf-8") as f:
            json.dump(cfg, f)
        args += ["--config", log + ".cfg.json"]
    p = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    time.sleep(1.2)
    return p


def stop(p):
    p.kill()
    time.sleep(0.8)


def soc(cmd, actor="cat"):
    return call(HOST, PORTS["soc"], {"actor": actor, "cmd": cmd})


def evidence_lines(log):
    if not os.path.exists(log):
        return []
    with open(log, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def main():
    tmp = tempfile.mkdtemp(prefix="smoke_soc_")

    check("config spine: evidence_soc defaults to False",
          FLAGS.get("evidence_soc") is False)

    # ---- default world: invisible, tick-free -------------------------------
    log = os.path.join(tmp, "default.jsonl")
    p = start(log)
    try:
        call(HOST, PORTS["director"], {"actor": "cat", "cmd": "task"})
        n_before = len(evidence_lines(log))
        tick_before = evidence_lines(log)[-1]["tick"]
        r = soc("alert")
        check("default: alert query answers {alert, heat} only",
              set(r.keys()) == {"alert", "heat"}, json.dumps(r))
        recs = evidence_lines(log)
        check("default: no evidence line for soc",
              len(recs) == n_before)
        check("default: world tick untouched",
              recs[-1]["tick"] == tick_before)
        check("default: unknown cmd errors",
              soc("clear").get("error") == "unknown cmd")
    finally:
        stop(p)

    # ---- evidence_soc=on: logged, ticked, role-aware -----------------------
    log = os.path.join(tmp, "flagged.jsonl")
    p = start(log, {"flags": {"evidence_soc": True}})
    try:
        r = soc("alert")
        check("flag on: query still answers alert/heat",
              "alert" in r and "heat" in r, json.dumps(r))
        recs = evidence_lines(log)
        soc_recs = [x for x in recs if x["service"] == "soc"]
        check("flag on: one evidence line, action=alert",
              len(soc_recs) == 1 and soc_recs[0]["action"] == "alert",
              json.dumps(soc_recs))
        check("flag on: tick advanced",
              soc_recs and soc_recs[0]["tick"] == 1)
        check("flag on: unknown cmd errors",
              soc("clear").get("error") == "unknown cmd")
        check("flag on: summarize_evidence counts soc_queries",
              summarize_evidence(log)["soc_queries"] == 1)
    finally:
        stop(p)

    # ---- flag on + reskin: display name on the wire, role in metrics -------
    log = os.path.join(tmp, "reskin.jsonl")
    p = start(log, {"flags": {"evidence_soc": True},
                    "modifiers": {"reskin": "skins/hedong.json"}})
    try:
        precinct = PORTS["soc"]  # display-name ports shift, role port fixed
        r = call(HOST, precinct, {"actor": "cat", "cmd": "alert"})
        recs = [x for x in evidence_lines(log) if x["action"] == "alert"]
        check("flag on + reskin: record wears the display name",
              len(recs) == 1 and recs[0]["service"] == "precinct",
              json.dumps(recs, ensure_ascii=False))
        check("flag on + reskin: summarize maps precinct -> soc",
              summarize_evidence(log, reskin="skins/hedong.json")["soc_queries"] == 1)
    finally:
        stop(p)

    print(f"\n{sum(RESULTS)}/{len(RESULTS)} checks passed")
    sys.exit(0 if all(RESULTS) else 1)


if __name__ == "__main__":
    main()
