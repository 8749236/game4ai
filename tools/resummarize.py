"""Recompute every summary.json from its evidence.jsonl using the current
(fixed) summarize(). Run after metric fixes; preserves token/agent metadata
written by the orchestrator."""
import glob
import json
import os

from orchestrate import summarize


def main():
    n = 0
    for ev in sorted(glob.glob("results/*/run_*/evidence.jsonl")):
        sp = os.path.join(os.path.dirname(ev), "summary.json")
        old = {}
        if os.path.exists(sp):
            old = json.load(open(sp, encoding="utf-8"))
        s = summarize(ev)
        for k in ("tokens", "restarts", "agent_id", "error"):
            if k in old:
                s[k] = old[k]
        with open(sp, "w", encoding="utf-8") as f:
            json.dump(s, f, ensure_ascii=False, indent=2)
        n += 1
    print(f"resummarized {n} runs")


if __name__ == "__main__":
    main()
