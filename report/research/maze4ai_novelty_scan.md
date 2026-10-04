# maze4ai 先行技术扫描(novelty scan)

> 2026-10-04,[K3] 受主人委托所做,零 token(纯公网检索)。
> 目的:确定 maze4ai 协议是否已被做过,防止重新发明轮子。

**结论先行:没有完全撞车,但有一个非常近的邻居——AGI Maze(Potapov 2026)。** maze4ai 的核心框架(文本介导的 POMDP 迷宫 + "测世界模型构建"的定位)已存在;仍有 3-4 个协议级要素未见于任何现有工作,可作为差异化立足点。

## maze4ai 待查协议(主人的设计)

LLM 遥控一个纯程序机器人探索迷宫。每回合 LLM 下达 forward / back / turn-left / turn-right 之一;动作后收到自我中心观测:朝向方向能看多远(到墙距离)+ 那堵墙的数据(颜色、甚至墙上的内容)。**LLM 永远看不到完整地图**。任务:找出口,或找到写着特定内容的房间。地形可有孤岛墙(与外墙不连通,摸墙律失效)与开阔区。终局探针:让 AI 交出脑内自建地图,与真图算相似度。设计意图:测第四代能力——全局结构全部"应该写但没写",只能从观测流的字缝里重建。

## 最接近的现有工作

| 工作 | 年份/出处 | 一句话 | 与 maze4ai 的重合度 |
|---|---|---|---|
| **AGI Maze** [arXiv:2607.00627](https://arxiv.org/pdf/2607.00627) | Potapov, 2026-07 | 网格 POMDP,LLM 只收到局部文本观测("你往右走,墙挡住了"),不给出地图,需找钥匙/宝箱,显式以"测世界模型构建"为定位 | **最近**:部分可观测✓ 每步自我中心文本感知✓ 不给全图✓ "测 world model"叙事✓。无:射线式距离观测、墙面语义内容、地图重建计分、反 wall-follower 设计(它用河流/传送坑制造不确定性) |
| AGI Maze Prediction Datasets [arXiv:2609.02339](https://arxiv.org/pdf/2609.02339) | Potapov, 2026-09 | 同一世界转监督预测:从 action-observation 对推断位置与拓扑;证明 2D 结构化工作记忆远优于纯 byte-Transformer | 离线数据集版,非交互 agent;佐证"文本历史≠内部空间表征"这一动机已被占用 |
| LLMs for Text-Based Exploration and Navigation under Partial Observability [arXiv:2604.09604](https://arxiv.org/html/2604.09604v1) | 2026-03 | LLM 逐回合控制 ASCII 网格机器人,每步只揭示 5×5 局部窗口,含 oracle 定位对照 | 部分可观测✓ 交互逐回合✓;但观测是 2D 局部窗口(非 1D 射线),无地图重建探针、无语义墙 |
| Memory-Maze(DeepMind 2022;被 [arXiv:2511.04235](https://arxiv.org/html/2511.04235v2) 等沿用) | 2022 | 3D 第一人称部分可观测迷宫,程序化生成,**墙面颜色/视觉线索承载语义**(需记"哪种颜色的墙对应目标方位") | 语义墙内容✓ 部分可观测✓;但它是视觉 RL 基准,非 LLM、非文本 |
| MANGO [arXiv:2403.19913](https://arxiv.org/html/2403.19913v1)(ACL 2024) | 2024 | 53 个迷宫(含 Zork-I)的文本 mapping+navigation 基准;模型读 walkthrough 后回答拓扑问题,最好模型表现差且随难度骤降 | "mapping"能力被测✓;但非交互式(静态 QA),无探索动作、无射线观测 |
| BabyAI/MiniGrid + GLAM [arXiv:1810.08272](https://www.alphaxiv.org/overview/1810.08272v4) | 2019/2023 | 7×7 自我中心部分观测 gridworld,GLAM 用 LLM 做策略 | 自我中心部分观测✓;观测是符号化 2D 窗口,任务是指令执行非建图 |
| CogEval [arXiv:2309.15129](https://arxiv.org/html/2309.15129v1)(NeurIPS 2023) | 2023 | Tolman 式"认知地图"评测:给图结构的文本描述,测 LLM 规划;结论:LLM 不理解认知地图 | 认知地图叙事✓;非交互、非探索,图是描述出来的而非探出来的 |
| MazeBench / AlphaMaze [arXiv:2502.14669](https://arxiv.org/html/2502.14669) | 2025 | 全图 ASCII 迷宫直接给模型解,GRPO 训练 | **全可观测**,恰是 maze4ai 要排除的设定;同名需避雷 |
| Can LLMs Learn to Map the World from Local Descriptions? [arXiv:2505.20874](https://arxiv.org/html/2505.20874v1) | 2025 | 从局部相对描述构建全局空间认知 | 静态描述流,非交互探索 |
| EvoEmpirBench | 2026-08 | 局部可观测迷宫导航 + 动态变化,测空间理解/记忆利用 | 部分可观测✓;细节未深查,协议不同 |

## 裁决:这个 exact thing 做过吗?

**没有。** 但"LLM + 部分可观测文本迷宫 + 世界模型叙事"这一**生态位已被 AGI Maze(2026)占住**,maze4ai 必须在协议层与它对线,否则会被视为重复。扫描后仍保持新颖的要素:

1. **1D 射线式观测协议**(朝向四动作 forward/back/turn-left/turn-right + "前方距离 + 墙面属性")。所有现有 LLM 迷宫要么给 2D 局部窗口(BabyAI、2604.09604),要么给动作结果文本(AGI Maze);没有任何一家给"距离到墙"的射线观测。这个协议迫使模型自己维护 heading 并做积分定位,且**观测带宽极低**——比窗口观测更纯粹地考验"从字缝里重建全局结构"。
2. **带语义内容的墙 + 跨位置整合任务**("找到写着 X 的房间")。语义线索只在视觉 RL 的 Memory-Maze 里出现过,LLM 文本基准里空白。
3. **地图重建作为计分终局输出**(draw-the-map probe vs ground truth)。MANGO 测"mapping"但只是 QA;AGI Maze 里模型自发在 notes 里画坐标地图却**无人对其计分**。把内隐世界模型显式读出来打分,未见先例。
4. **反 wall-follower 拓扑**(孤岛墙/开放空间作为刻意的算法陷阱)。现有基准的迷宫都是标准 perfect maze,没人针对"模型可能在跑教科书算法而非建世界模型"做对抗性设计。这一点能区分"背了迷宫算法"和"真在建图"。

## 可偷的设计经验

- **随机游走基线是照妖镜**:AGI Maze 发现 GPT-4o Mini 统计上**差于无信息随机游走**。maze4ai 应内置 random 与 wall-follower 两条基线(后者在孤岛墙迷宫上注定失败,正好成为设计卖点)。
- **步数预算校准人类表现**(AGI Maze 做法)+ success@budget、excess-steps ratio(相对最短路的多余步数)作主指标。
- **工作记忆消融**(AGI Maze:允许写 notes 后 GPT-5.5 从 30%→60%)——maze4ai 可分"纯上下文"与"可外写笔记"两档,分离内隐/外显建图。
- **源迷宫不相交切分 + exact-match**(AGI Maze Prediction)防止记布局。
- **已记录的失败模式**:原地打转/循环、幻觉坐标、notes 里坐标自相矛盾、长 horizon 下状态跟踪崩溃(MANGO 报告难度陡增时骤降)。地图重建探针恰好能把"幻觉地图"从定性趣闻变成定量指标。
- **命名避雷**:"MazeBench"已被占用至少两次(AlphaMaze 2025、视觉版 2026),maze4ai 这个名字本身没撞车。

**一句话**:协议骨架(部分可观测文本迷宫测世界模型)= AGI Maze 已占位;新颖性必须押在 ①射线式 1D 观测+朝向积分、②语义墙内容、③计分地图重建、④反 wall-follower 拓扑这四件套上,且论文/文档里需要显式与 AGI Maze(arXiv:2607.00627)做对比定位。
