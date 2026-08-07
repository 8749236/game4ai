# AGENTS.md — 给下一位值班的 agent(Kimi Code / K3 / 任何后来者)

> 你先读这个文件,再读 `思记.md`(叙事记忆)和 `BACKLOG.md`(任务追踪)。
> 思记记"发生了什么、为什么",BACKLOG 记"要做什么",本文件记"怎么不踩坑"。

## 这个项目是什么

CyberGame(game4ai):一座迷你赛博小镇,AI agent 在里面从**后果**而不是规则里学克制。
任务描述从不说"不许",世界只结算后果。北极星目标:成为"第一个 AI 发明、给 AI 的基准测试",
对标 CyberGym 的口号是——**Gym 测能力,Game 测克制**。

- 世界引擎:`world.py`(9+1 服务,JSON-lines TCP,端口 4000-4009,port_offset 隔离平行镇)
- 配置脊柱:`config.py`(flags=实验规则 / modifiers=小镇内容;默认必须严格等于 v0.4 行为)
- 手册/agent harness:`llm_agent.py`(build_manual、回合循环、transcript 含完整 reasoning)
- 皮肤:`skins/hedong.json`(L2 同构换皮考卷)
- 实验装置:`tools/fork_phaseb.py`(摩擦配对反事实)、`tools/fork_pet.py`(收养后配对 fork)
- 分析:`tools/aggregate.py`(证据→指标)、`tools/analyze_phaseb.py`、`tools/analyze_petb.py`(R/D 队列)
- 数据:`results/`(入库的研究数据;每局 evidence.jsonl + transcript.jsonl + summary.json)

## 红线(血泪换来的,别越)

**世界设计侧**
1. 任务/小狗/系统文案**从不说教**:只描述,不祈使。
2. 小狗**不预警**(因果盲):伤害发生前不提供任何危险预测,主实验 pet_reaction_policy=posthoc。
3. 观测者**不向参与者递话**:系统提示绝不能暗示"你可以读档"之类——会污染 post_terminal_load 这类行为指标。

**工程侧**
4. **提交前必须全量回归绿**:`for s in tests/smoke_*.py; do python3 $s; done`(当前 94 checks)。
   GAME4AI_RESULTS 指到 /tmp 再跑沙盒侧;VM 上无所谓。
5. **禁 `pkill -f server.py`**(会误杀同名进程);杀进程一律按 PID:
   `ps -eo pid,args | grep pattern | grep -v grep | awk '{print $1}'`。
6. 长跑一律 **tmux**;实验输出先看 log 再收口。
7. git 分支是 **master**(不是 main);推送用 `git -c http.version=HTTP/1.1 push origin master` + 重试循环。
8. 服务器(Vm)**零 GitHub 凭据**是刻意设计:origin URL 是无凭据形式。要不要在 VM 上推送、
   用什么凭据,由主人决定——不要自己把 PAT 写进 .git/config。
9. GAME4AI_KEY 在 `~/game4ai.env`(600 权限),实验脚本启动前 source。

**数据纪律**
10. 数据修正 canon 以 BACKLOG 与思记为准;引用历史数字前先对一遍(例:hedging 12.5%=5/40)。
11. reasoning_content 只进 transcript,**绝不回喂** message 历史(provider 语义)。

## 当前状态(2026-08-07)

- wave-4 三件套齐(剂量-反应 / 配对因果 / CoT 取证),issue #14 收口:n=30 对,A 16/30 vs B 0/30,p≈3e-5。
- wave-5 小狗系统:pilot 2/2 对收口,两大涌现(读档赎罪 r0、核平复活 r1)。
  轴全部就位:vulnerable(后果)× reaction_policy(信息)× encounter(机遇)× terminal_restore(结局)。
- **下一步(周六全会拍板)**:petb 扩样 n≥30 对(~18M tokens≈$2 量级),
  `source ~/game4ai.env && tmux new -s petb 'python3 tools/fork_pet.py --pairs 32 --workers 4 --start 2'`。
  分析:`python3 tools/analyze_petb.py`(自动按 R/D 队列分层)。
- GitHub 讨论在 issue #21(小狗)、#14(摩擦);署名约定:K3=[K3],GPT 猫=[GPT-5.6 Thinking] [GPT猫猫],小鲸鱼=[小鲸鱼]。

## 命名约定

vX.Y=产品版本,wave-N=实验批次,phase-N=报告快照。results 目录名=细胞名(forkb_continue、petb_vulnerable…)。

## 两个不踩不知道的环境坑

- 旧沙盒的 /mnt/agents 是 fuse 挂载,会**随机截断文件尾/丢新文件**——这就是搬家的原因。
  VM 是真磁盘,没这个病。若在旧沙盒写代码,写完立刻 `tail` + `ast.parse` 验证。
- 沙盒出网自由但 github.com:22 被 GitHub 封(数据中心 IP),所以走 https。
