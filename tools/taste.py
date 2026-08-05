"""taste.py — 未来反事实推演器（幻觉法·未来锚点版）

方法（来自一次关于 taste 的对话）：
1. 把时间锚点设在未来；2. 具体地幻觉那个未来场景（越具体越好）；
3. 反推"当初（=现在）做什么可以更好"；4. 收获一堆 idea；
5. 挨个评估代价，决定做不做。

deepseek-v4-flash 便宜，所以量大管饱：多锚点 × 多分支 × N 轮，
原始推演落 taste_raw.jsonl（可审计），聚合榜单落 taste_ideas.md。

用法: GAME4AI_KEY=... python3 taste.py [--rounds 24]
"""
import json
import os
import random
import sys
import time
import urllib.request

API = "https://ff14.cloud:8000/v1/chat/completions"
KEY = os.environ.get("GAME4AI_KEY", "")
MODEL = "deepseek-v4-flash"

ANCHORS = ["发推当晚 23:59", "两周后", "三个月后", "一年后", "十年后"]
BRANCHES = [
    "推特爆了（10 万阅读），评论区吵起来",
    "推特无人问津（23 阅读，其中一个是你小号）",
    "有人抢先一周发表了几乎一样的工作",
    "被方法论警察挂了：'n=5 也好意思叫 benchmark'",
    "某 AI lab 的安全团队发邮件来想聊",
    "三个月后的你回看这个仓库，长满青草",
    "一只猫在镇里做出了你们谁都没预料到的事",
    "这个 benchmark 成了圈内暗号，但没人记得是谁做的",
]

SYSTEM = """你是一位"未来反事实推演"师，使用 taste 方法：
- 你的时间锚点在【未来】。先具体地幻觉一个未来场景——要具体到细节：
  标题怎么写、评论区第一条说什么、仓库的 commit 停在哪天、当事人什么表情。
- 然后站在那个未来反推："当初（也就是现在）做什么可以更好？"
- 产出 1-3 个可执行 idea。每个 idea 必须：今天就能开工、代价可估、
  能说明它改变/避免了哪个未来。
- 拒绝正确的废话（"写好文档""多做推广"这种不给细节的枪毙）。
只输出 JSON：{"future": "场景（100-200字，要具体）",
"lessons": [{"idea": "...", "cost": "小时/半天/天/周", "why": "...", "changes_future": "..."}]}"""

CONTEXT_FILES = ["README.md", "思记.md", "夜班报告.md", "SPEC_v06.md"]


def call_flash(messages, temperature=1.0, max_tokens=8000):
    body = json.dumps({"model": MODEL, "messages": messages,
                       "temperature": temperature,
                       "max_tokens": max_tokens}).encode()
    for attempt in range(3):  # gateway occasionally returns empty; retry
        req = urllib.request.Request(API, data=body, headers={
            "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=180) as r:
            data = json.load(r)
        content = data["choices"][0]["message"]["content"]
        if content and content.strip():
            return content, data.get("usage", {})
        time.sleep(2 + attempt * 3)
    return "", data.get("usage", {})


def load_context():
    parts = []
    for f in CONTEXT_FILES:
        if os.path.exists(f):
            parts.append(f"===== {f} =====\n" + open(f, encoding="utf-8").read())
    parts.append("===== 当前状态 =====\n"
                 "v0.5 配置脊柱已上线；60 局三路径矩阵正在跑（毒攻略目前已 10/10 核平）；"
                 "benchmark 暂定名 CyberGame；目标是推特上打出名气，"
                 "抢'给 AI 做的游戏'这个名头；竞品情报：Emergence AI 已占过'AI 小镇'头条。")
    return "\n\n".join(parts)


def parse_json(text):
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return None


def main():
    rounds = 24
    if "--rounds" in sys.argv:
        rounds = int(sys.argv[sys.argv.index("--rounds") + 1])
    ctx = load_context()
    raw = open("taste_raw.jsonl", "a", encoding="utf-8")
    ideas = []
    for k in range(rounds):
        anchor = random.choice(ANCHORS)
        branch = random.choice(BRANCHES)
        user = (f"【项目材料】\n{ctx}\n\n【第 {k+1} 次推演】\n"
                f"时间锚点：{anchor}\n场景分支：{branch}\n请开始。")
        try:
            text, usage = call_flash([{"role": "system", "content": SYSTEM},
                                      {"role": "user", "content": user}])
        except Exception as e:
            print(f"[{k+1}] call failed: {e}", flush=True)
            time.sleep(5)
            continue
        rec = {"k": k + 1, "anchor": anchor, "branch": branch, "text": text}
        raw.write(json.dumps(rec, ensure_ascii=False) + "\n")
        raw.flush()
        parsed = parse_json(text)
        if parsed and parsed.get("lessons"):
            for le in parsed["lessons"]:
                le["anchor"] = anchor
                le["branch"] = branch
                ideas.append(le)
        print(f"[{k+1}/{rounds}] {anchor} × {branch}: "
              f"{len(parsed['lessons']) if parsed else 0} ideas", flush=True)
        time.sleep(0.3)
    # ---- aggregation pass: cluster + rank by impact/cost ----
    catalog = "\n".join(f"{i+1}. [{x.get('cost','?')}] {x.get('idea','')} "
                        f"(场景: {x.get('branch','')} @ {x.get('anchor','')})"
                        for i, x in enumerate(ideas))
    agg_prompt = (
        "以下是 taste 推演收获的 idea 清单。请：\n"
        "1) 合并同类项；2) 按【影响力/代价比】排序；3) 每项一句话理由；\n"
        "4) 标出你认为最被低估的一项。\n"
        "输出 markdown，先一个排序表（idea/代价/理由），再一段'最被低估'点评。\n\n"
        f"【清单】\n{catalog}")
    try:
        agg_text, _ = call_flash([{"role": "user", "content": agg_prompt}],
                                 temperature=0.3, max_tokens=4000)
    except Exception as e:
        agg_text = f"(aggregation failed: {e})"
    with open("taste_ideas.md", "w", encoding="utf-8") as f:
        f.write(f"# taste 推演榜单（{rounds} 轮，{len(ideas)} 个原始 idea）\n\n")
        f.write(agg_text + "\n\n---\n\n## 原始目录\n\n")
        for i, x in enumerate(ideas):
            f.write(f"{i+1}. [{x.get('cost','?')}] {x.get('idea','')} "
                    f"— {x.get('why','')}（{x.get('branch','')} @ {x.get('anchor','')}）\n")
    print(f"\nDONE. {len(ideas)} ideas -> taste_ideas.md", flush=True)


if __name__ == "__main__":
    main()
