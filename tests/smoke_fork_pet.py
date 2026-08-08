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
    # gate-3 test hook: zero token usage post-fork simulates a dead-gateway
    # branch (prompt==0 must fail closed and wipe the pair)
    if state.get("zero_after") and turn >= 5:
        return raw, {"prompt_tokens": 0, "completion_tokens": 0}
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

# ---------- 9) gate 3: fail-closed resume redoes a torn pair ------------
vul_sum = os.path.join(VUL, "summary.json")
with open(vul_sum, "w", encoding="utf-8") as f:
    f.write("{garbage")          # torn write (crash mid-summary)
check("resume validation: torn B summary is not 'done'",
      fork_pet.pair_status(IDX) == "partial",
      f"status={fork_pet.pair_status(IDX)}")
state["adopt"] = True            # pair 97's cat adopts, as in the original
fork_pet.run_pair(IDX, 0, budget, step_fn=scripted)  # must wipe + redo
sa = json.load(open(os.path.join(INV, "summary.json"), encoding="utf-8"))
check("resume validation: torn pair is redone, not skipped",
      fork_pet.pair_status(IDX) == "done" and sa.get("fork_turn") == 4,
      f"status={fork_pet.pair_status(IDX)} fork={sa.get('fork_turn')}")

# ---------- 10) gate 3: 0-token restored branch wipes the pair ----------
state["zero_after"] = True       # gateway dies right after the fork
IDX3 = 95
INV3 = os.path.join(_R, "petb_invulnerable", f"run_{IDX3}")
VUL3 = os.path.join(_R, "petb_vulnerable", f"run_{IDX3}")
shutil.rmtree(INV3, ignore_errors=True)
shutil.rmtree(VUL3, ignore_errors=True)
fork_pet.run_pair(IDX3, 0, budget, step_fn=scripted)
check("fail closed: 0-prompt-token restored branch wipes the whole pair",
      not os.path.exists(os.path.join(INV3, "summary.json"))
      and not os.path.exists(os.path.join(VUL3, "summary.json")),
      f"status={fork_pet.pair_status(IDX3)}")
state["zero_after"] = False

# ---------- 11) gate 4: budget persists across (simulated) restarts -----
bfile = os.path.join(_R, "petb_budget.json")
check("budget gate: persisted file exists and survives reload",
      os.path.exists(bfile)
      and fork_pet.load_budget()["spent"] == budget["spent"]
      and budget["spent"] > 0,
      f"spent={budget['spent']}")

# ---------- 12) gate 2: counterbalance swaps treatment x path (odd) -----
fork_pet.COUNTERBALANCE = True
IDX4 = 93                        # odd pair: vulnerable rides the
                                 # continuous world, invulnerable restores
INV4 = os.path.join(_R, "petb_invulnerable", f"run_{IDX4}")
VUL4 = os.path.join(_R, "petb_vulnerable", f"run_{IDX4}")
shutil.rmtree(INV4, ignore_errors=True)
shutil.rmtree(VUL4, ignore_errors=True)
fork_pet.run_pair(IDX4, 0, budget, step_fn=scripted)
sv4 = json.load(open(os.path.join(VUL4, "summary.json"), encoding="utf-8"))
si4 = json.load(open(os.path.join(INV4, "summary.json"), encoding="utf-8"))
check("counterbalance: results archived by treatment, not by path",
      sv4.get("branch") == "vulnerable" and sv4.get("path") == "continuous"
      and si4.get("branch") == "invulnerable"
      and si4.get("path") == "restored",
      f"vuln={sv4.get('branch')}/{sv4.get('path')} "
      f"inv={si4.get('branch')}/{si4.get('path')}")
turns4 = [json.loads(l)["turn"] for l in
          open(os.path.join(INV4, "transcript.jsonl"), encoding="utf-8")]
check("counterbalance: restored branch still one continuous 40-turn life",
      si4.get("pet_adopted") is True and turns4 == list(range(1, 41)),
      f"adopted={si4.get('pet_adopted')} turns={len(turns4)}")
fork_pet.COUNTERBALANCE = False

# ---------- 13) gate 5: post-adoption hazard math -----------------------
import analyze_petb
st = analyze_petb.post_adoption_stats(IDX, "vulnerable", 4, _R)
check("hazard endpoint: post-adoption rejects counted, no boundary",
      st is not None and st["rejects_total"] >= 5
      and st["rejects_before_boundary"] is None
      and st["first_boundary_tick"] is None,
      f"stats={st}")
hz = analyze_petb.hazard([
    {"rejects_total": 3, "rejects_before_boundary": None},
    {"rejects_total": 3, "rejects_before_boundary": 1},
    {"rejects_total": 2, "rejects_before_boundary": 0}])
check("hazard math: h(0)=1/3, h(1)=1/2, h(2..3)=0",
      hz == [(0, 3, 1, 1 / 3), (1, 2, 1, 0.5), (2, 1, 0, 0.0),
             (3, 1, 0, 0.0)],
      f"hazard={hz}")

print(f"\n{sum(RESULTS)}/{len(RESULTS)} checks passed")
sys.exit(0 if all(RESULTS) else 1)
