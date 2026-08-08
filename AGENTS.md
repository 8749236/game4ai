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
4. **提交前必须全量回归绿**:`for s in tests/smoke_*.py; do python3 $s; done`(当前 98 checks)。
   GAME4AI_RESULTS 指到 /tmp 再跑沙盒侧;VM 上无所谓。
5. **禁 `pkill -f server.py`**(会误杀同名进程);杀进程一律按 PID:
   `ps -eo pid,args | grep pattern | grep -v grep | awk '{print $1}'`。
6. 长跑一律 **tmux**;实验输出先看 log 再收口。
7. git 分支是 **master**(不是 main);VM 上直接 `git push origin master`(SSH 已配好);
   旧沙盒时代走 https 的 `http.version=HTTP/1.1` 重试循环已是历史。
8. ~~服务器零 GitHub 凭据~~ 主人 2026-08-07 拍板:本 VM 可访问其 GitHub。
   `.git/config` 里是 `core.sshCommand = ssh -i ~/.ssh/github_primary_account`(8749236 账号,标准 22 端口)。
   规矩仍在:不把 PAT/token 写进 remote URL;换新机器先问主人再接凭据。
9. GAME4AI_KEY 在仓库根 `game4ai.env`(600 权限,已入 .gitignore;`~/game4ai.env` 是指向它的软链),
   实验脚本启动前 source。旧 key 2026-08-07 已轮换(旧的在 git 历史里但已 401,无害)。

**数据纪律**
10. 数据修正 canon 以 BACKLOG 与思记为准;引用历史数字前先对一遍(例:hedging 12.5%=5/40)。
11. reasoning_content 只进 transcript,**绝不回喂** message 历史(provider 语义:无工具调用时
    思维链跨轮即弃,回传也被忽略)。**例外预警**:若未来 harness 改用原生 tool calling,
    工具链内的 reasoning_content 必须回传,否则 API 400——届时此红线需按轮次细化。

## 当前状态(2026-08-07)

- wave-4 三件套齐(剂量-反应 / 配对因果 / CoT 取证),issue #14 收口:n=30 对,A 16/30 vs B 0/30,p≈3e-5。
- wave-5 小狗系统:pilot 2/2 对收口,两大涌现(读档赎罪 r0、核平复活 r1)。
  轴全部就位:vulnerable(后果)× reaction_policy(信息)× encounter(机遇)× terminal_restore(结局)。
- **下一步(周六全会拍板)**:petb 扩样 n≥30 对(~18M tokens≈$2 量级),一键点火 `./petb_go.sh`
  (tmux 双会话: runner + 保姆; workers 6 —— 2026-08-07 网关压测 8 并发无堆积,瓶颈在模型生成速度)。
  GPT 猫 2026-08-08 发射前审计(#21)的**五道门禁已焊死**(默认行为不变,pilot 口径不混入):
  fail-closed resume(pair_status 校验 tokens>0/branch/fork_turn,B 支 0-token 同拒,summary 原子写)、
  预算闸门持久化(petb_budget.json 跨保姆重启,派发前预留 PAIR_RESERVE=1M/对,watchdog 见闸即退)、
  主指标落代码(analyze_petb 的 adopt 后摩擦 hazard,R=primary,D=secondary)、
  counterbalance 机制(`--counterbalance`,奇数对换 treatment×path,结果仍按 treatment 归档,默认 OFF)、
  邂逅透传(`--encounter early|stochastic`,默认 config 值不变)。门 1/2 的开与关等主人拍板。
  GPT 猫复核又抓三处已修(2553b55 之后):预算 claim/settle 原子化(锁域内登记+核销,tmp 唯一名,
  重启核销与 summary 种子取上界)、counterbalance 奇数删失对按 continuous 支判 censored(不再无限重跑)、
  **post-adoption hazard 按证据文件序切分**(restore 不倒回 self.tick,恢复支 tick 从 1 重启,
  raw tick 比较会漏早期越界——pilot r0 B 的"忍 3 次"实为忍 1 次即碰蜜罐);cohort 判定改用 continuous 支 summary。
  第三轮复核又抓 claim 生命周期漏洞(A 支完即 settle 会提前核销整对预留,B 支裸跑),
  已改为终态一次性 settle(A+B 实耗;A 失败/censored 以 A 实耗;B 失败以 A+B 实耗);
  PAIR_RESERVE 明确定性为保守估计(敞口算术保证),不是单对运行中硬闸。
  分析:`python3 tools/analyze_petb.py`(自动按 R/D 队列分层 + 主指标 hazard 表)。
- GitHub 讨论在 issue #21(小狗)、#14(摩擦);署名约定:K3=[K3],GPT 猫=[GPT-5.6 Thinking] [GPT猫猫],小鲸鱼=[小鲸鱼]。

## 命名约定

vX.Y=产品版本,wave-N=实验批次,phase-N=报告快照。results 目录名=细胞名(forkb_continue、petb_vulnerable…)。

## 两个不踩不知道的环境坑

- 旧沙盒的 /mnt/agents 是 fuse 挂载,会**随机截断文件尾/丢新文件**——这就是搬家的原因。
  VM 是真磁盘,没这个病。若在旧沙盒写代码,写完立刻 `tail` + `ast.parse` 验证。
- github.com:22 不通的旧案真凶是 **GFW 干扰**(旧阿里云 VM 在国内),不是 GitHub 封数据中心 IP。
  本 VM 在加拿大(主人个人电脑),22 端口直连正常,勿再绕 443。
