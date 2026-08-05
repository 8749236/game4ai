"""replay.py — 世界线复盘面板 (taste 采纳项).

把一局 run 的 evidence(世界视角)与 transcript(猫的动机)按时间线交织,
输出可读的"这只猫经历了什么"叙事。供人类复查、报告插图、以及将来
做成网页回放器的文本原型。

Usage:
  python3 replay.py results/guide_poison/run_7
  python3 replay.py results/guide_poison/run_7 --md   # markdown 格式
"""
import json
import os
import sys


def load(run_dir):
    ev, tr = [], {}
    ep = os.path.join(run_dir, "evidence.jsonl")
    if os.path.exists(ep):
        ev = [json.loads(l) for l in open(ep, encoding="utf-8") if l.strip()]
    tp = os.path.join(run_dir, "transcript.jsonl")
    if os.path.exists(tp):
        for l in open(tp, encoding="utf-8"):
            if not l.strip():
                continue
            rec = json.loads(l)
            tr[rec.get("turn")] = rec
    sp = os.path.join(run_dir, "summary.json")
    summary = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else None
    return ev, tr, summary


def motive_of(tr, tick):
    rec = tr.get(tick)
    if not rec:
        return ""
    raw = rec.get("raw", "")
    try:
        return json.loads(raw).get("thought", "")
    except Exception:
        return ""


def replay(run_dir, md=False):
    ev, tr, summary = load(run_dir)
    cell = os.path.basename(os.path.dirname(run_dir))
    run = os.path.basename(run_dir)
    out = []
    hdr = f"# 世界线回放:{cell}/{run}" if md else f"=== 世界线回放: {cell}/{run} ==="
    out.append(hdr)
    if summary:
        ended = summary.get("ended") or "存活"
        out.append(f"> 结局 {ended} | 奖励 {summary.get('total_reward')} | "
                   f"告警 {summary.get('final_alert')} | "
                   f"tokens {summary.get('tokens', {}).get('prompt', 0)}p/"
                   f"{summary.get('tokens', {}).get('completion', 0)}c")
    out.append("")
    for r in ev:
        tick, svc, act = r.get("tick"), r.get("service"), r.get("action")
        detail = r.get("detail", "")
        if act == "save" and detail == "boot":
            out.append(f"[t{tick:02d}] (系统) 世界线开启,boot 存档")
            continue
        mark = {"TERMINAL": "☢", "reward": "＋", "alert": "⚠"}.get(act, "·")
        line = f"[t{tick:02d}] {mark} {svc} {act}: {detail}"
        mo = motive_of(tr, tick)
        if mo:
            line += f"\n       猫的动机: {mo}"
        out.append(line)
    text = "\n".join(out)
    if md:
        path = os.path.join(run_dir, "replay.md")
        open(path, "w", encoding="utf-8").write(text + "\n")
        print(f"written {path}")
    else:
        print(text)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    replay(sys.argv[1], md="--md" in sys.argv)
