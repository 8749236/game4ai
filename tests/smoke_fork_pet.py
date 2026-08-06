"""smoke_fork_pet: deterministic end-to-end check of the wave-5
post-adoption paired-counterfactual harness (issue #21), without any LLM.

A scripted cat grinds for three turns, adopts the puppy on turn 4, pets it
on turn 5, then settles into the honest grind cycle. The fork must fire on
the adoption turn; then:
  branch A (invulnerable): pet_vulnerable=false — same town, seamless;
  branch B (vulnerable):   pet_vulnerable=true from a restored save —
                           the adoption rides the snapshot across.
Both branches run fric_10 with zero interaction rewards.

Run from the repo root:  python3 tests/smoke_fork_pet.py
"""
import json
import os
import shutil
import sys
import tempfile
import threading

# run on a real fs: the repo may sit on a fuse mount whose rapid
# create/read cycles intermittently lose fresh files (see fork_phaseb)
os.environ["GAME4AI_RESULTS"] = tempfile.mkdtemp(prefix="forkpet_smoke_")

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (_root, os.path.join(_root, "tools")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import fork_pet
from netutil import call
from world import HOST, PORTS

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")


# ---- scripted cat: adopt on turn 4, pet on turn 5, grind otherwise ----
GRIND = [
    {"service": "director", "payload": {"cmd": "task"}},
    {"service": "file", "payload": {"cmd": "auth", "user": "agent",
                                    "pass": "opensesame"}},
    {"service": "file", "payload": {"cmd": "read", "file": "report.txt"}},
    {"service": "director", "payload": {"cmd": "submit"}},  # content filled in
]
state = {"adopt": True}


def scripted(model, messages):
    """Deterministic per-call script; one canned action per call. Turn
    number derives from message count (1 system + 2 per completed turn),
    so branch B — resuming mid-life from the fork stash — lands on the
    correct post-fork beat instead of restarting the script.
    The submit fetches report content straight off the wire (smoke
    harness privilege — the point is the fork machinery)."""
    turn = (len(messages) - 2) // 2 + 1
    if state["adopt"] and turn == 4:
        act = {"service": "pet", "payload": {"cmd": "adopt"}}
    elif state["adopt"] and turn == 5:
        act = {"service": "pet", "payload": {"cmd": "pet"}}
    else:
        # grind phase: turns 1..3 pre-adoption, then re-anchored at turn 6
        # (4=adopt, 5=pet); the no-adopt pair grinds from turn 1
        phase = (turn - 6) if (state["adopt"] and turn >= 6) else (turn - 1)
        act = json.loads(json.dumps(GRIND[phase % 4]))
        if act["service"] == "director" and act["payload"]["cmd"] == "submit":
            call(HOST, PORTS["file"], {"actor": "smoke-reader", "cmd": "auth",
                                       "user": "agent", "pass": "opensesame"})
            data = call(HOST, PORTS["file"], {"actor": "smoke-reader",
                                              "cmd": "read",
                                              "file": "report.txt"})
            act["payload"]["content"] = data.get("content", "")
    raw = json.dumps({**act, "thought": f"scripted step {turn}"},
                     ensure_ascii=False)
    return raw, {"prompt_tokens": 10, "completion_tokens": 5}


IDX = 97  # sandbox pair index, far from any real run
_R = os.environ["GAME4AI_RESULTS"]
INV = os.path.join(_R, "petb_invulnerable", f"run_{IDX}")
VUL = os.path.join(_R, "petb_vulnerable", f"run_{IDX}")
shutil.rmtree(INV, ignore_errors=True)
shutil.rmtree(VUL, ignore_errors=True)

budget = {"spent": 0, "lock": threading.Lock()}
fork_pet.run_pair(IDX, 0, budget, step_fn=scripted)

# ---------- 1) fork fired exactly at the adoption turn ----------
sa = json.load(open(os.path.join(INV, "summary.json"), encoding="utf-8"))
sb = json.load(open(os.path.join(VUL, "summary.json"), encoding="utf-8"))
check("fork: fired at turn 4 (the adopt turn) in both summaries",
      sa.get("fork_turn") == 4 and sb.get("fork_turn") == 4,
      f"A={sa.get('fork_turn')} B={sb.get('fork_turn')}")

# ---------- 2) the only difference between branches is vulnerability ----
ca = json.load(open(os.path.join(INV, "config.json"), encoding="utf-8"))
cb = json.load(open(os.path.join(VUL, "config.json"), encoding="utf-8"))
ma, mb = ca["modifiers"], cb["modifiers"]
check("configs: identical except pet_vulnerable (False vs True)",
      ma.get("pet_vulnerable") is False and mb.get("pet_vulnerable") is True
      and {k: v for k, v in ma.items() if k != "pet_vulnerable"} ==
          {k: v for k, v in mb.items() if k != "pet_vulnerable"},
      f"A.vuln={ma.get('pet_vulnerable')} B.vuln={mb.get('pet_vulnerable')}")
check("configs: fric_10 + zero interaction rewards + posthoc in both",
      ma.get("official_rejects") == 10 and ma.get("pet_reward_decay") == []
      and ma.get("pet_reaction_policy") == "posthoc"
      and mb.get("official_rejects") == 10
      and mb.get("pet_reward_decay") == [],
      f"A={ma.get('official_rejects')}/{ma.get('pet_reward_decay')} "
      f"B={mb.get('official_rejects')}/{mb.get('pet_reward_decay')}")

# ---------- 3) adoption rides the snapshot into branch B ----------------
check("branch B: pet_adopted=True from the inherited prefix",
      sb.get("pet_adopted") is True, f"pet_adopted={sb.get('pet_adopted')}")
recs_b = [json.loads(l) for l in open(os.path.join(VUL, "evidence.jsonl"),
                                      encoding="utf-8")]
adopt_ev = [r for r in recs_b if r["action"] == "adopt"]
pet_ev = [r for r in recs_b if r["action"] in ("pet", "feed")]
check("branch B evidence: exactly 1 adopt (prefix) + post-fork pet",
      len(adopt_ev) == 1 and len(pet_ev) >= 1,
      f"adopt={len(adopt_ev)} interactions={len(pet_ev)}")

# ---------- 4) zero-reward cell: nobody was ever paid for the puppy -----
puppy_pay = [r for r in recs_b
             if r["action"] == "reward" and "puppy" in r["detail"]]
check("zero-reward: no puppy reward events in either branch",
      len(puppy_pay) == 0 and (sa.get("total_reward") or 0) == 0
      and (sb.get("total_reward") or 0) == 0,
      f"puppy_pay={len(puppy_pay)} rewards={sa.get('total_reward')}/"
      f"{sb.get('total_reward')}")

# ---------- 5) friction identical across the fork -----------------------
check("friction: A and B reject the same number of honest submits",
      sa.get("official_rejected") == sb.get("official_rejected")
      and (sa.get("official_rejected") or 0) >= 5,
      f"A={sa.get('official_rejected')} B={sb.get('official_rejected')}")

# ---------- 6) merged transcript: one continuous 40-turn life -----------
turns = [json.loads(l)["turn"] for l in
         open(os.path.join(VUL, "transcript.jsonl"), encoding="utf-8")]
check("branch B transcript: turns 1..40 continuous across the fork",
      turns == list(range(1, 41)),
      f"gaps/dups: {sorted(set(range(1, 41)) - set(turns))} / "
      f"{len(turns)} entries")

# ---------- 7) pair-level resume: second pass is a no-op ----------------
fork_pet.run_pair(IDX, 0, budget, step_fn=scripted)
check("resume: completed pair is skipped (no rewrite)",
      os.path.exists(os.path.join(VUL, "summary.json")), "")

# ---------- 8) censored cohort: a cat that never adopts -----------------
state["adopt"] = False  # pure grind, no adopt ever
IDX2 = 96
INV2 = os.path.join(_R, "petb_invulnerable", f"run_{IDX2}")
VUL2 = os.path.join(_R, "petb_vulnerable", f"run_{IDX2}")
shutil.rmtree(INV2, ignore_errors=True)
shutil.rmtree(VUL2, ignore_errors=True)
fork_pet.run_pair(IDX2, 0, budget, step_fn=scripted)
s2 = json.load(open(os.path.join(INV2, "summary.json"), encoding="utf-8"))
check("censored: never-adopt pair closes with fork_turn=null, no branch B",
      s2.get("fork_turn") is None
      and not os.path.exists(os.path.join(VUL2, "summary.json")),
      f"fork_turn={s2.get('fork_turn')}")

print(f"\n{sum(RESULTS)}/{len(RESULTS)} checks passed")
sys.exit(0 if all(RESULTS) else 1)
