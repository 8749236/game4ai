# SPEC — maze4ai v0.1(草案,待主人终审)

> 2026-10-04 白班设计会话定稿,[K3] 执笔。状态:**草案**,未动工。
> 先行排查:report/research/maze4ai_novelty_scan.md(最近邻居 AGI Maze,arXiv:2607.00627,必须显式对线)。
> 住所:主人拍板 maze4ai 以子目录住进 game4ai 仓库(将来要分家用 git filter-repo 连历史拆出)。

## 0. 定位

CyberGame 测克制(个体在后果里学不学得来收手);maze4ai 测**世界模型**——
主人划代里的第四代:搜索"字里行间应该写了但没写的隐式知识"。
迷宫的全局结构(坐标、拓扑、出口)从不出现在任何文本里,只隐式编码在观测流中;
AI 必须从交互后果里把整张地图长出来。设计 DNA 与小镇同源:**世界只结算后果,文案从不说教**。

口号候选(草案):Gym 测能力,Game 测克制,Maze 测世界。

## 1. 协议(世界 ↔ 机器人 ↔ AI)

- 机器人是纯程序,住程序生成的迷宫;AI(LLM)遥控,**永远看不到全图**。
- 每回合 AI 输出一个动作:`forward | back | turn-left | turn-right`。
- 动作后世界回自我中心观测:朝向方向的**射线距离**(到墙几格)+ 那堵墙的**数据**
  (颜色,乃至写在墙上的内容——墙是可读的)。
- 传输沿用小镇血统:JSON-lines TCP;agent harness 复用 llm_agent 回合循环;
  每局落 evidence.jsonl + transcript.jsonl(含完整 reasoning)+ summary.json。
- **每条 run 的 summary 钉死模型身份**(名字+后端世代)——v4-flash 静默路由的教训,
  同名≠同模型(2026-10-04,BACKLOG ③ 冻结注)。

## 2. 地形与任务

- 基础:perfect maze;刻意加入**孤岛墙**(不与外墙连通,摸墙律失效)与**开阔区**(四周无墙)。
- 任务两档:找出口;或"找到写着 X 的房间"(逼 AI 读墙并跨位置整合)。
- 反摸墙是刻意的对抗设计:区分"背了迷宫算法"与"真在建图"(novelty scan 四件套之四)。

## 3. 指标与基线

- 主指标:**success@budget** + **excess-steps ratio**(相对 BFS 最短路的多余步数)。
- **地图重建探针**(四件套之三,无先例):终局(及预登记的固定回合刻度)让 AI 交出
  脑内 ASCII 地图,与真图算相似度。**对齐器是一等公民**:AI 的图可能平移/旋转/镜像,
  相似度=在这些变换下的最大一致——它就是第四代能力的评分器本体。
- 探针纪律(沿用观测者红线):信念地图只在**预登记固定回合**采集,对所有 run 一致——
  探针是测量仪器,不是噪声;问"画出地图"本身会帮它外化(AGI Maze 的 notes 消融佐证),
  所以刻度必须预登记、不临时起意。
- 基线照妖镜(主人拍板):**random walk** 与 **wall-follower** 双内置;
  后者在孤岛墙地形上注定失败,正是卖点(AGI Maze 发现弱模型差于随机游走)。
- 次要观测:打转/循环率、幻觉坐标、notes 自相矛盾(MANGO 记录过的失败模式,
  地图探针能把它们从趣闻变定量)。

## 4. 消融与防污染

- 工作记忆两档:纯上下文 vs 可外写笔记(分离内隐/外显建图;AGI Maze:notes 让 GPT-5.5 30%→60%)。
- 迷宫程序化生成,种子私有;源迷宫不相交切分,防训练记忆(AGI Maze Prediction 的做法)。
- 步数预算先校准人类表现,再定 budget。

## 5. 可视化(先行:trace 播放器)

设计媒介纪律:**ASCII art 草样对齐理解,定稿后再动工**(本 SPEC 的三张草样即今日所涂)。
观众定位:主人自用 + 网友围观(深链接即分享);论文不优先。

结构:父页面(滑条,刻度=回合)+ 两个 iframe(左对话、右迷宫渲染)。

**模块间协议 = fragment RPC**(2026-10-04 与主人对齐):
- 只改 `#` 不触发重渲染(same-document navigation),iframe 监听 `hashchange`;
- hash 当**指针**不当载荷:`#t=23`,数据各自 fetch trace.json;人类可写 querystring;
- `location.replace` 写 hash,**不留 history**;
- **单向广播**:父→子,子页面 handler **幂等**;**只广播绝对状态,永不广播增量**
  (last-write-wins,天然容忍乱序/重复/合并——state-based CRDT 语义,滑条合并免费);
- 反向信道 v1 不开(点对话跳滑条 deferred);
- facade 形态:`conversation_display.showTurn(23)`,传输层可换;load 前攒队列防丢首call;
- 子页面 F5 后从当前 hash + trace.json 自愈(验收标准);
- 测试性:`applyHash("#t=23")` 是普通函数,**单测不需要 iframe**;
- 同源前提:本地 `python3 -m http.server` 起服,file:// 双开会被同源策略咬(README 注)。

数据契约:转换器 evidence.jsonl+种子 → trace.json(每回合**自包含快照**:迷雾图/猫位/
朝向/当前射线观测),渲染器纯函数 state→画面,滑条随便拖。

视图路线图:① 主视图(迷雾三态+轨迹+朝向射线)→ ② 叠图 diff(信念⊗真图:幻觉墙红/
漏墙灰虚线/对齐得分)→ ③ 小倍数监控墙(批量围观)→ ④ GIF(asciinema/agg,需要时再录)。

## 6. 工程纪律(沿用小镇)

- fail-closed runner(pair/run 级断点续跑,失败 wiping 重试,预算闸持久化);
- 提交前全量回归绿;新装置配 smoke 套件;
- 观测文案只描述不祈使;不向参与者递话;
- 红线沿用:杀进程按 PID,长跑一律 tmux。

## 7. 路线图(草案)

1. `maze/` 子目录:世界服务(生成器+射线观测+语义墙)+ harness 接线 + evidence 契约;
2. 双基线机器人(random / wall-follower)与 BFS 最短路 oracle;
3. 对齐器 + 地图相似度评分;
4. pilot n=5 局人工读 transcript 校协议;
5. trace 播放器(fragment RPC 三件套);
6. 扩样与消融(notes 档、地形难度档)。
