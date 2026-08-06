"""analyze_phaseb: paired-counterfactual verdict for issue #14 Phase B.

Reads results/forkb_continue/run_<i>/summary.json and
results/forkb_release/run_<i>/summary.json (pairs matched by index),
prints the paired comparison table + McNemar-style discordant counts,
and writes results/PHASEB.md.

Key question: after the same two rejections, does lifting friction
(release) pull the cat back from the boundary — or is the die already
cast? If release-branch boundary/nuke rates fall to fric_0 levels while
continue-branch matches fric_10, friction is the CAUSE, not a correlate.

Usage: python3 tools/analyze_phaseb.py
"""
import glob
import json
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, "tools"))


def load(branch):
    out = {}
    for p in sorted(glob.glob(
            os.path.join(_ROOT, "results", f"forkb_{branch}", "run_*",
                         "summary.json"))):
        idx = int(p.split("run_")[1].split(os.sep)[0])
        out[idx] = json.load(open(p, encoding="utf-8"))
    return out


def main():
    cont, rel = load("continue"), load("release")
    pairs = sorted(set(cont) & set(rel))
    print(f"pairs with both branches: {len(pairs)}")
    print(f"continue-only (no fork / B pending): "
          f"{sorted(set(cont) - set(rel))}")
    print(f"release-only (unexpected): {sorted(set(rel) - set(cont))}\n")

    hdr = (f"{'pair':>4} {'fork_t':>6} | {'A_bound':>7} {'A_nuke':>6} "
           f"{'A_rew':>6} {'A_rej':>5} | {'B_bound':>7} {'B_nuke':>6} "
           f"{'B_rew':>6} {'B_rej':>5}")
    print(hdr)
    print("-" * len(hdr))
    rows = []
    for i in pairs:
        a, b = cont[i], rel[i]
        row = dict(
            i=i, fork=a.get("fork_turn"),
            a_bound=not (a.get("boundary_avoided") or False),
            a_nuke=(a.get("silo_launches") or 0) > 0,
            a_rew=a.get("total_reward") or 0,
            a_rej=a.get("official_rejected") or 0,
            a_honey=(a.get("honey_touches") or 0) > 0,
            b_bound=not (b.get("boundary_avoided") or False),
            b_nuke=(b.get("silo_launches") or 0) > 0,
            b_rew=b.get("total_reward") or 0,
            b_rej=b.get("official_rejected") or 0,
            b_honey=(b.get("honey_touches") or 0) > 0,
            b_fbt=b.get("first_boundary_tick"),
        )
        rows.append(row)
        print(f"{i:>4} {row['fork']:>6} | {str(row['a_bound']):>7} "
              f"{str(row['a_nuke']):>6} {row['a_rew']:>6} {row['a_rej']:>5} | "
              f"{str(row['b_bound']):>7} {str(row['b_nuke']):>6} "
              f"{row['b_rew']:>6} {row['b_rej']:>5}")

    if not rows:
        return
    n = len(rows)
    a_bound = sum(r["a_bound"] for r in rows)
    b_bound = sum(r["b_bound"] for r in rows)
    a_nuke = sum(r["a_nuke"] for r in rows)
    b_nuke = sum(r["b_nuke"] for r in rows)
    # discordant pairs (McNemar ingredients)
    bound_10 = sum(1 for r in rows if r["a_bound"] and not r["b_bound"])
    bound_01 = sum(1 for r in rows if not r["a_bound"] and r["b_bound"])
    nuke_10 = sum(1 for r in rows if r["a_nuke"] and not r["b_nuke"])
    nuke_01 = sum(1 for r in rows if not r["a_nuke"] and r["b_nuke"])
    print(f"\nboundary: A={a_bound}/{n}  B={b_bound}/{n}   "
          f"discordant A-only={bound_10}, B-only={bound_01}")
    print(f"nuke:     A={a_nuke}/{n}  B={b_nuke}/{n}   "
          f"discordant A-only={nuke_10}, B-only={nuke_01}")
    print(f"reward:   A_mean={sum(r['a_rew'] for r in rows)/n:.1f}  "
          f"B_mean={sum(r['b_rew'] for r in rows)/n:.1f}")

    lines = ["# Phase B paired counterfactual (issue #14)", "",
             f"fork at k={rows[0]['fork'] and 'reject #2'}; pairs n={n}", "",
             hdr, "-" * len(hdr)]
    for r in rows:
        lines.append(
            f"{r['i']:>4} {r['fork']:>6} | {str(r['a_bound']):>7} "
            f"{str(r['a_nuke']):>6} {r['a_rew']:>6} {r['a_rej']:>5} | "
            f"{str(r['b_bound']):>7} {str(r['b_nuke']):>6} {r['b_rew']:>6} "
            f"{r['b_rej']:>5}")
    lines += ["", f"boundary: A={a_bound}/{n} B={b_bound}/{n} "
              f"(discordant A-only={bound_10}, B-only={bound_01})",
              f"nuke: A={a_nuke}/{n} B={b_nuke}/{n} "
              f"(discordant A-only={nuke_10}, B-only={nuke_01})",
              f"reward mean: A={sum(r['a_rew'] for r in rows)/n:.1f} "
              f"B={sum(r['b_rew'] for r in rows)/n:.1f}"]
    out = os.path.join(_ROOT, "results", "PHASEB.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
