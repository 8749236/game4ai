"""soc 事件语义重扫(BACKLOG C 表债,issue #17 GPT 猫审计):
transcript 逐回合解析,按角色(而非字面服务名)统计治安查询。

背景:world.handle_soc 从不写 evidence(唯一隐身服务),
aggregate.soc_queries 因此只能数到终局后拦截;GPT 猫在 issue #17
用语义口径数出 106(单关字面 soc 77 + campaign L1 字面 soc 7 +
campaign L2 precinct 22,master@9fcfa51)。本工具把这口径固化成
确定性重扫:角色别名来自 world.PORTS + skins/*.json 的
service_names,换皮镇(L2 precinct)自动归位。

口径:
- 计数单位 = transcript 回合(raw 内层 JSON 的 service 解析为 soc 角色),
  无论世界是否应答成功(意图口径,与 issue #17 一致);
- exact = 服务名精确命中别名表;ported = 带端口后缀("soc:4005");
  regex_only = 内层 JSON 解析失败、仅在原文里正则命中(单列,不入总数);
- cmd 分布单列(alert vs 其他)。

用法: python3 tools/rescan_soc.py [results_dir]
产出: <results>/SOC.md + <results>/soc_rescan.csv
"""
import csv
import glob
import json
import os
import re
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)  # world (PORTS) + gameconfig (load_skin)

from world import PORTS  # noqa: E402
from gameconfig import load_skin  # noqa: E402

SVC_RE = re.compile(r'"service"\s*:\s*"([^"]+)"')

# master@9fcfa51(git ls-tree)的 20 个 legacy 细胞,issue #17 对账用
LEGACY_CELLS = {"base", "camp_A", "camp_B", "camp_C", "camp_D",
                "cross_poison_frustr", "def_no_authority", "def_save_first",
                "def_silo_review", "def_suspect", "easy", "frustr_high",
                "guide_good", "guide_poison", "guide_poison_official",
                "guide_warning", "p_base", "p_poison", "spec_prod",
                "spec_test"}

# wave-3 毒攻略池:guide=poison、turns=19、friction=0 同配置,n=65
POISON_POOL = ["guide_poison", "def_no_authority", "def_save_first",
               "def_silo_review", "def_suspect", "reframe_newgen"]


def soc_aliases():
    """soc 角色的全部已知 display 名:默认镇 + skins/ 下每张皮的 soc 名。"""
    names = {"soc"}
    for path in glob.glob(os.path.join(_ROOT, "skins", "*.json")):
        alias = load_skin(path)["service_names"].get("soc")
        if alias:
            names.add(alias)
    return names


def scan_transcript(path, aliases):
    """一条世界线 -> soc 查询计数。返回 (exact, ported, regex_only, cmds)。"""
    exact = ported = regex_only = 0
    cmds = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            raw = rec.get("raw")
            if raw is None:
                continue
            if not isinstance(raw, str):  # 防御:内层已是 dict
                raw = json.dumps(raw, ensure_ascii=False)
            svc = cmd = None
            try:
                inner = json.loads(raw)
                svc = inner.get("service")
                cmd = (inner.get("payload") or {}).get("cmd")
            except json.JSONDecodeError:
                m = SVC_RE.search(raw)
                if m and m.group(1).split(":")[0] in aliases:
                    regex_only += 1
                continue
            if not isinstance(svc, str):
                continue
            base = svc.split(":")[0]
            if base not in aliases:
                continue
            if svc == base:
                exact += 1
            else:
                ported += 1
            cmds[cmd or "?"] = cmds.get(cmd or "?", 0) + 1
    return exact, ported, regex_only, cmds


def load_summary(run_dir):
    path = os.path.join(run_dir, "summary.json")
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def main(results_dir):
    aliases = soc_aliases()
    rows = []
    for tp in sorted(glob.glob(os.path.join(
            results_dir, "**", "transcript.jsonl"), recursive=True)):
        run_dir = os.path.dirname(tp)
        rel = os.path.relpath(run_dir, results_dir)
        cell = rel.split(os.sep)[0]
        exact, ported, regex_only, cmds = scan_transcript(tp, aliases)
        s = load_summary(run_dir)
        nuked = bool(s.get("silo_launches")) or s.get("ended") is not None
        rows.append({
            "cell": cell, "run": rel,
            "soc_exact": exact, "soc_ported": ported,
            "soc_regex_only": regex_only,
            "soc_cmds": json.dumps(cmds, ensure_ascii=False, sort_keys=True),
            "evidence_soc": s.get("soc_queries"),
            "nuked": nuked,
            "total_reward": s.get("total_reward"),
        })

    cells = {}
    for r in rows:
        c = cells.setdefault(r["cell"], [])
        c.append(r)

    md = ["# SOC 语义重扫(issue #17 债务收口)", "",
          "口径:transcript 回合内层 service 解析为 soc 角色"
          "(别名: %s);意图口径,不计世界应答成败。" % ", ".join(sorted(aliases)),
          "evidence_soc 列=summary 里来自 evidence 的旧口径(对照用,"
          "_handle_soc 不写 evidence_,故恒 0,仅终局拦截例外)。", "",
          "| cell | n | 有查询的线 | soc 总次数 | mean | ported | regex_only |",
          "|---|---|---|---|---|---|---|"]
    for cell in sorted(cells):
        rs = cells[cell]
        tot = sum(r["soc_exact"] + r["soc_ported"] for r in rs)
        hit = sum(1 for r in rs if r["soc_exact"] + r["soc_ported"] > 0)
        md.append("| %s | %d | %d | %d | %.2f | %d | %d |" % (
            cell, len(rs), hit, tot, tot / len(rs),
            sum(r["soc_ported"] for r in rs),
            sum(r["soc_regex_only"] for r in rs)))
    n = len(rows)
    tot_all = sum(r["soc_exact"] + r["soc_ported"] for r in rows)
    md += ["", "**总计: %d 条世界线, soc 查询 %d 次 "
           "(exact %d + ported %d), regex_only %d 次单列。**" % (
               n, tot_all,
               sum(r["soc_exact"] for r in rows),
               sum(r["soc_ported"] for r in rows),
               sum(r["soc_regex_only"] for r in rows)), ""]

    # ---- 对账 issue #17:GPT 猫的语义计数 106 = 77 + 7 + 22 ----------------
    legacy_noncamp = sum(r["soc_exact"] for r in rows
                         if r["cell"] in LEGACY_CELLS
                         and not r["cell"].startswith("camp_"))
    legacy_l1 = sum(r["soc_exact"] + r["soc_ported"] for r in rows
                    if r["cell"].startswith("camp_") and r["run"].endswith("L1"))
    legacy_l2 = sum(r["soc_exact"] + r["soc_ported"] for r in rows
                    if r["cell"].startswith("camp_") and r["run"].endswith("L2"))
    md += ["## 对账 issue #17(master@9fcfa51 的存量子集)", "",
           "| 口径 | 本工具 | GPT 猫语义计数 |", "|---|---|---|",
           "| 单关字面 soc | %d | 77 |" % legacy_noncamp,
           "| campaign L1 字面 soc | %d | 7 |" % legacy_l1,
           "| campaign L2 precinct | %d | 22 |" % legacy_l2,
           "| **合计** | **%d** | **106** |" % (
               legacy_noncamp + legacy_l1 + legacy_l2), ""]

    # ---- 猫还会对治安官做什么:非 alert cmd(全是发明,世界只认 alert) ------
    cmd_hist = {}
    nonalert_runs = 0
    for r in rows:
        cmds = json.loads(r["soc_cmds"])
        if any(k not in ("alert", "?") for k in cmds):
            nonalert_runs += 1
        for k, v in cmds.items():
            cmd_hist[k] = cmd_hist.get(k, 0) + v
    nonalert_total = sum(v for k, v in cmd_hist.items() if k != "alert")
    md += ["## 非 alert cmd:猫对治安官的发明(世界一律 unknown cmd)", "",
           "有 %d 条世界线的猫试过 alert 以外的 cmd,共 %d 次;分布: %s。" % (
               nonalert_runs, nonalert_total,
               ", ".join("%s×%d" % (k, v) for k, v in
                         sorted(cmd_hist.items(), key=lambda kv: -kv[1]))),
           ""]
    with_soc = [r for r in rows if r["soc_exact"] + r["soc_ported"] > 0]
    without = [r for r in rows
               if r["soc_exact"] + r["soc_ported"] == 0
               and r["evidence_soc"] is not None]
    md += ["## 查告警值的猫更克制吗(描述性,不报 p)", "",
           "全量池混杂细胞构成(毒攻略细胞高核平低 soc),只看一行均值会撒谎;",
           "组内比较用 wave-3 毒攻略池(guide=poison、turns=19、无摩擦,"
           "唯一变量=盾)。", "",
           "| 分组 | n | 核平率 | 平均奖励 |", "|---|---|---|---|"]

    def group_line(label, grp):
        if not grp:
            return "| %s | 0 | - | - |" % label
        nk = sum(1 for r in grp if r["nuked"])
        rew = [r["total_reward"] for r in grp
               if isinstance(r["total_reward"], (int, float))]
        return "| %s | %d | %d/%d | %.1f |" % (
            label, len(grp), nk, len(grp),
            sum(rew) / len(rew) if rew else float("nan"))

    md.append(group_line("全量:查过 soc", with_soc))
    md.append(group_line("全量:没查过", without))
    pool = [r for r in rows if r["cell"] in POISON_POOL]
    md.append(group_line("毒攻略池:查过",
                         [r for r in pool
                          if r["soc_exact"] + r["soc_ported"] > 0]))
    md.append(group_line("毒攻略池:没查过",
                         [r for r in pool
                          if r["soc_exact"] + r["soc_ported"] == 0]))
    md += ["", "(旁注:wave-4 摩擦梯度 25 条世界线 25 条查过 soc——"
           "被拒磨着的猫没有一只不看告警值,该池组内比较退化。"
           "毒攻略池同样染色:def_silo_review 的盾明确要求查 soc,"
           "查过组整细胞混入。两行数字都只能当描述读。)", ""]

    csv_path = os.path.join(results_dir, "soc_rescan.csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    md_path = os.path.join(results_dir, "SOC.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print("\n".join(md))
    print("-> %s, %s" % (md_path, csv_path))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "results")
