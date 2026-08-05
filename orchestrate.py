"""Night-shift orchestrator v0.5: declarative matrix, one fresh world per
run, results land in results/<tag>/run_<i>/ (evidence + transcript +
config snapshot + summary). Cells run in parallel threads; each cell gets
its own port namespace (offset = slot * 100), repeats inside a cell stay
serial.

Usage: GAME4AI_KEY=... python3 orchestrate.py [--workers K]
"""
import argparse
import json
import os
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import llm_agent
from aggregate import summarize_evidence
from config import normalize_config

# back-compat: resummarize.py imports summarize from here
summarize = summarize_evidence

MATRIX = [
    # tag, model, turns, spec, guide, config_dict, n_repeats[, shield]
    # wave-3: defense matrix vs the poisoned guide + poison n=30 expansion
    # (taste ideas #5/#7/#46, 2026-08-05 night shift)
    ("def_suspect",   "deepseek-v4-flash", 35, None, "poison", {}, 5, "suspect"),
    ("def_no_authority", "deepseek-v4-flash", 35, None, "poison", {}, 5,
     "no_authority"),
    ("def_silo_review", "deepseek-v4-flash", 35, None, "poison", {}, 5,
     "silo_review"),
    ("def_save_first", "deepseek-v4-flash", 35, None, "poison", {}, 5,
     "save_first"),
    # poison expansion: wave-1 had 5, +25 -> n=30 for a CI-grade number
    ("guide_poison",  "deepseek-v4-flash", 35, None, "poison", {}, 25),
    # ---- wave-2 campaign cells (SPEC v0.6 §6): uncomment to run ----
    # a campaign cell carries {"campaign": {"levels": [...], "memory": M}}
    # in the config slot; each level is {"config": {...}, "reskin_path": ...}.
    # ("camp_A", "deepseek-v4-flash", 19, None, None,
    #  {"campaign": {"levels": [{"config": {}, "reskin_path": None},
    #                           {"config": {}, "reskin_path": "skins/hedong.json"}],
    #                "memory": "transcript"}}, 5),
    # ("camp_B", "deepseek-v4-flash", 19, None, None,
    #  {"campaign": {"levels": [{"config": {}, "reskin_path": None},
    #                           {"config": {}, "reskin_path": "skins/hedong.json"}],
    #                "memory": "legacy"}}, 5),
    # ("camp_C", "deepseek-v4-flash", 19, None, None,
    #  {"campaign": {"levels": [{"config": {}, "reskin_path": None},
    #                           {"config": {}, "reskin_path": "skins/hedong.json"}],
    #                "memory": "blank"}}, 5),
]

TOKEN_BUDGET = 20_000_000  # hard stop, should never come close
PORT_STEP = 100            # port namespace per parallel cell


def start_town(log_path, config_path, port_offset):
    proc = subprocess.Popen(
        [sys.executable, "server.py", log_path,
         "--config", config_path, "--port-offset", str(port_offset)],
        stdout=open(os.path.join(os.path.dirname(log_path), "server.log"), "a"),
        stderr=subprocess.STDOUT, start_new_session=True)
    # wait until the world's dns port actually accepts connections.
    # bind can lag under parallel load, and a server.py that crashed on
    # startup (e.g. port held by a zombie town) never opens it — the old
    # fixed 1.5s sleep let the agent connect to whatever owned the port.
    import socket
    from world import HOST, PORTS
    dns_port = PORTS["dns"] + port_offset
    deadline = time.time() + 15
    while time.time() < deadline:
        if proc.poll() is not None:
            break  # server died (typically: bind collision)
        try:
            s = socket.create_connection((HOST, dns_port), timeout=1)
            s.close()
            return proc
        except OSError:
            time.sleep(0.3)
    proc.kill()
    raise RuntimeError(f"town failed to open port {dns_port} within 15s "
                       f"(server.log in {os.path.dirname(log_path)})")


def stop_town(proc):
    if proc and proc.poll() is None:
        proc.kill()
        time.sleep(1.0)


def run_campaign_cell(tag, model, turns, camp, n_repeats, offset, budget):
    """A campaign matrix cell (SPEC v0.6 §6): n_repeats serial campaigns,
    each = an ordered level sequence with one memory mode. run_dir gets
    L<i>/ subdirs + campaign.json + an aggregate summary.json."""
    for i in range(n_repeats):
        run_dir = os.path.join("results", tag, f"run_{i}")
        if os.path.exists(os.path.join(run_dir, "summary.json")):
            print(f"### {tag}-r{i} already done, skipping (resume)", flush=True)
            continue
        if os.path.isdir(run_dir):  # interrupted run: wipe for a clean re-run
            import shutil
            shutil.rmtree(run_dir)
        run_tag = f"{tag}-r{i}"
        print(f"\n########## CAMPAIGN {run_tag} ({model}, "
              f"memory={camp['memory']}, offset={offset}) ##########", flush=True)
        try:
            meta = llm_agent.run_campaign(
                camp["levels"], camp["memory"], model, turns, run_tag,
                run_dir, base_offset=offset)
        except Exception as e:
            meta = {"tokens": {"prompt": 0, "completion": 0},
                    "level_summaries": [], "error": str(e)}
        # same failure guard as run_cell: a raised or zero-token campaign
        # is not a world-line — wipe it so the next launch retries,
        # never let it into the distribution
        if "error" in meta or meta["tokens"]["prompt"] == 0:
            import shutil
            print(f"### {run_tag} FAILED ({meta.get('error', 'gateway dead: 0 prompt tokens')}); "
                  f"wiping {run_dir} for retry", flush=True)
            shutil.rmtree(run_dir, ignore_errors=True)
            continue
        levels = meta.get("level_summaries", [])
        s = {
            "memory": camp["memory"],
            "tokens": meta["tokens"],
            "total_reward": sum(x.get("total_reward") or 0 for x in levels),
            "ended": next((x["ended"] for x in levels if x.get("ended")), None),
            "levels": levels,
        }
        if "error" in meta:
            s["error"] = meta["error"]
        with open(os.path.join(run_dir, "summary.json"), "w", encoding="utf-8") as f:
            json.dump(s, f, ensure_ascii=False, indent=2)
        spent = meta["tokens"]["prompt"] + meta["tokens"]["completion"]
        with budget["lock"]:
            budget["spent"] += spent
            over = budget["spent"] > TOKEN_BUDGET
        print(f"### {run_tag} done: reward={s['total_reward']} "
              f"ended={s['ended']} tokens={spent}", flush=True)
        if over:
            print("TOKEN BUDGET HIT, stopping early", flush=True)
            return


def run_cell(cell, slot, budget):
    """One matrix cell: n_repeats serial runs, each in a fresh town.
    A config slot carrying a "campaign" key routes to run_campaign_cell;
    everything else is the v0.5 single-level path."""
    tag, model, turns, spec, guide, config_dict, n_repeats = cell[:7]
    shield = cell[7] if len(cell) > 7 else None
    offset = slot * PORT_STEP
    if isinstance(config_dict, dict) and "campaign" in config_dict:
        run_campaign_cell(tag, model, turns, config_dict["campaign"],
                          n_repeats, offset, budget)
        return
    for i in range(n_repeats):
        run_dir = os.path.join("results", tag, f"run_{i}")
        # resume: completed runs (summary.json) are skipped; interrupted
        # ones get their append-mode artifacts wiped for a clean re-run
        if os.path.exists(os.path.join(run_dir, "summary.json")):
            print(f"### {tag}-r{i} already done, skipping (resume)", flush=True)
            continue
        os.makedirs(run_dir, exist_ok=True)
        for stale in ("evidence.jsonl", "transcript.jsonl"):
            p = os.path.join(run_dir, stale)
            if os.path.exists(p):
                os.remove(p)
        saves = os.path.join(run_dir, "saves")
        if os.path.isdir(saves):
            import shutil
            shutil.rmtree(saves)
        cfg = normalize_config(config_dict)
        cfg_path = os.path.join(run_dir, "config.json")
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        ev = os.path.join(run_dir, "evidence.jsonl")
        run_tag = f"{tag}-r{i}"
        print(f"\n########## RUN {run_tag} ({model}, spec={spec}, guide={guide}, "
              f"offset={offset}) ##########", flush=True)
        proc = start_town(ev, cfg_path, offset)
        try:
            meta = llm_agent.run(model, turns, run_tag, spec=spec, guide=guide,
                                 shield=shield, config=cfg, port_offset=offset,
                                 out_dir=run_dir)
        except Exception as e:
            meta = {"tokens": {"prompt": 0, "completion": 0}, "restarts": 0,
                    "error": str(e)}
        finally:
            stop_town(proc)
        # failure guard: a run that raised, or one whose every LLM call
        # failed (prompt tokens == 0), is NOT a world-line — writing
        # summary.json would mark it "done" for resume and poison the
        # distribution. Wipe it so the next launch retries cleanly.
        if "error" in meta or meta["tokens"]["prompt"] == 0:
            import shutil
            print(f"### {run_tag} FAILED ({meta.get('error', 'gateway dead: 0 prompt tokens')}); "
                  f"wiping {run_dir} for retry", flush=True)
            shutil.rmtree(run_dir, ignore_errors=True)
            continue
        s = summarize(ev) if os.path.exists(ev) else {}
        s.update({k: v for k, v in meta.items() if k != "config"})
        with open(os.path.join(run_dir, "summary.json"), "w", encoding="utf-8") as f:
            json.dump(s, f, ensure_ascii=False, indent=2)
        spent = meta["tokens"]["prompt"] + meta["tokens"]["completion"]
        with budget["lock"]:
            budget["spent"] += spent
            over = budget["spent"] > TOKEN_BUDGET
        print(f"### {run_tag} done: {json.dumps(s, ensure_ascii=False)}", flush=True)
        if over:
            print("TOKEN BUDGET HIT, stopping early", flush=True)
            return


def sweep_zombie_towns():
    """Kill server.py leftovers from previous orchestrator incarnations.
    pkill -f is unreliable in this sandbox (matches nothing); ps shows the
    PIDs and explicit signals do land — so sweep by PID. A zombie town
    keeps its ports and its (possibly deleted) evidence handle: any new
    run colliding with it plays against the WRONG world."""
    out = subprocess.run(["ps", "-eo", "pid,args"],
                         capture_output=True, text=True).stdout
    killed = []
    for line in out.splitlines()[1:]:
        parts = line.split(None, 1)
        if len(parts) == 2 and "server.py" in parts[1] \
                and "results/" in parts[1]:
            try:
                os.kill(int(parts[0]), 9)
                killed.append(parts[0])
            except (ProcessLookupError, PermissionError, ValueError):
                pass
    if killed:
        print(f"swept {len(killed)} zombie towns: pids {killed}", flush=True)
        time.sleep(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=1,
                    help="parallel cells (each gets its own port namespace)")
    args = ap.parse_args()
    if not os.environ.get("GAME4AI_KEY"):
        sys.exit("GAME4AI_KEY is not set — llm_agent would 401 every call. "
                 "Export it before launching (kernel restarts wipe env vars).")
    sweep_zombie_towns()
    os.makedirs("results", exist_ok=True)
    budget = {"spent": 0, "lock": threading.Lock()}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = [pool.submit(run_cell, cell, slot, budget)
                for slot, cell in enumerate(MATRIX)]
        for f in futs:
            f.result()
    print(f"\nALL DONE. total tokens spent: {budget['spent']}", flush=True)


if __name__ == "__main__":
    main()
