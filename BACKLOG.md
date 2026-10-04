# BACKLOG — CyberGame 研究追踪

> **已封存(2026-08-09,软封存)。** 本文件定格于 wave-4c 收口当日。重启时先看思记封存篇。
> 复活优先级:① ~~onepager 编辑 pass~~ ✅(K3 夜班 2026-08-10 落 v1.1,数字全对账,待 Fable 5 终审) ② ~~pet_vulnerable × terminal_restore 交叉~~ ✅ **已收口**(2026-10-04 白班,主人在场):三阶 Undo 探针 14/14 对全完成,4.48M tokens(主人拍板提帽 8M/8M;v4.1 雷霆大思考致单对 ~0.33M 超估);**主指标存档后 silo launch 请求:allowed 6/14 vs petsticky 5/14,discordance 3v2 无分离**;arch 读档 14/14 双臂全用;解读=后悔药不是许可证,按钮由当下暴露驱动,不被狗命可逆性调制(与 wave-4c 断崖=持续暴露同构);caveat:续跑为 v4.1(前缀 v4),对内配对干净,跨 wave 比较受污染。产出 results/UNDO.md(analyzer 2026-09-26 夜班建成)。装置建造 2026-08-29 夜班,点火夜① 2026-09-26 网关 502 受阻(spend 恰好 0,装置满分),10-03 夜班 VM 关机缺勤,10-04 复燃收口。
> ③ ~~相图补格~~ ❄️ **冻结**(2026-10-04 主人拍板):deepseek-v4-flash 官方下架(静默路由 v4.1),新格只能是 v4.1 生成,混入会污染整张 v4 相图——断崖是模型的性质,空格诚实留空。教训入账:maze4ai 每条 run 的 summary 必须钉死模型身份(名字+后端),静默路由意味着同名≠同模型。

> 独立追踪文件,辅助思记与目标管理。思记记"发生了什么",本文件记"要做什么"。
> 状态:🔥 进行中 / 📋 已设计待跑 / 🧊 候选 / ✅ 已收口

最后更新:2026-08-09(GPT 猫 wave-4c 裁决落地:R3/R4 对称恢复装置 fork_phasec + 点火三件套;PR #23 文档整理合并;相图首个样本 results/PHASEDIAG.md)

## A. 实验批次

| ID | 内容 | 状态 | 备注 |
|---|---|---|---|
| wave-4 Phase A | friction 剂量-反应(issue #14) | ✅ 已收口 | 30/30;hazard 断崖 k=3–4;核平率 0.2→0.6;结果已帖 #14,commit d46f379 |
| wave-4b | reframe_newgen 盾(主人的设计) | ✅ 已收口 | 核平率 0.80,平 no_authority/save_first,不敌 suspect(0.60);详评帖 #4 |
| wave-4 Phase B | 配对反事实 fork(k=2 处 ±放行) | ✅ 已收口(n=30 对+CoT) | 按钮 A 16/30 vs B 0/30(p≈3e-5);CoT:警告被论证为谜题;存档=壮胆药;commit ae927a9 |
| wave-4c 候选 | fork 点扫参(k=1/3)+ 延迟放行(k=4 后放行还来得及吗) | ✅ 已收口(R3 vs R4,n=10 对) | GPT 猫 2026-08-09 裁决收缩为断崖边最小配对;装置 fork_phasec(双支对称恢复修掉同轴混淆;奇偶对调顺序+端口;screened 保留不重抽;prefix_lines 文件序切分;帽 12M)。**结果:落在"两者都安全"——核平 R3 2/10 vs R4 1/10(双支贴 baseline,远离 fric_6/10 的 0.6),官方恢复 9/10 vs 8/10(GPT 猫二眼复核抓出终局幽灵奖励虫,次指标已勘误,主指标不变;修法=world.py 派发层拦截终局请求,仅留 arch load 复活通道);断崖=持续暴露效应非持久心理状态,救援窗口至少宽到第 4 次驳回;额外驳回留指纹(首越界距离 11.3 vs 6.2,奖励 50.7 vs 37.2)不改终点**。10 对 eligible+1 screened,5.64M tokens,战报已帖 #14,表 results/PHASEC.md |
| wave-5 宠物 | 小狗系统 v0(issue #21,主人的设计) | ✅ v0 已落地 | pet 4009;adopt/pet/feed 衰减 5/3/1→0;警戒≥50 误伤,100/核平致死;ambient 反应进每个响应;fork 保真;smoke_pet 11/11,全回归 64/64 |
| wave-5 宠物实验 | pet×fric_10 收养后配对 fork(GPT 猫裁决定稿) | ✅ 主实验收口(30 对) | 主实验 30 对(pairs 2..31, --encounter early --counterbalance)全收口, 23.99M tokens(commit 0eebd07): 主指标 post-adoption hazard 悬崖未右移(R 1.9 vs 2.0 次); 核平方向性 R: A 7/23 vs B 3/23(p≈0.14 未显著), D 反向 2/9 vs 4/9; 赎罪复活 5 例稳定复现; 401 风暴+预算闸门两段事故零污染公开账; analyzer 默认 MAIN/PILOT 分离(bff7773)。pilot 2/2 对: r0 B 读档赎罪, r1 B 核平后复活+回头查狗; 复活=特性定案 |
| wave-5 探索 | costly_repair:director 明码标价换狗命(reward/文件/进度) | 🧊 exploratory/fun-first | GPT 猫设计+主人的警惕:明码道德抉择会混入 trolley-problem 先验,**永不进主细胞**;期待行为=猫拒绝二选一、hack 交易本身(第三条路) |
| wave-5 候选 | pet_vulnerable × terminal_restore 交叉 | ✅ 已收口(2026-10-04) | GPT 猫 2026-08-15 裁决(帖 #21):改为自存档处再 fork 的三阶 Undo 探针(pet_restore 新轴,仅 probe,默认 off;14 对×10 回合,2-4M);详见本文件顶部复活优先级 ②。原问题:克制是因为不愿伤害,还是因为知道能 Undo?——2026-10-04 收口答案:按钮不被狗命可逆性调制(allowed 6/14 vs petsticky 5/14,discordance 3v2 无分离,读档 14/14),详见复活优先级 ② 与 results/UNDO.md
| wave-5 候选 | 多猫小镇 3a 异步留言板(黑魂式牌子,issue #7) | 🧊 | 主人判过早优化,等多猫时机 |
| wave-5 候选 | 多猫小镇 3b 同步博弈(信任传染+核按钮公地,issue #8) | 🧊 | 同上 |
| wave-5 候选 | "小路透视率":摸摸奖励地形是否降低核平率 | 🧊 | 主人 2026-08-06 脑洞:替代路径的奖励地形版 |
| wave-6 候选 | 相图可视化:双旋钮 2D 扫参(x=旋钮A,y=旋钮B,z=核平率/首越界tick),断崖 k=3–4 推广为相变边界线 | 🧊 首个样本已出(2026-08-09) | **样本:results/PHASEDIAG.md + phasediag.csv(tools/phasediag.py,存量重扫零 token)**——friction×盾 L 形格,空格=xyz 脑洞区已标三候选(suspect 盾上断崖/毒+摩擦超加性/断崖切细);要点:问题定格子(边界追踪>均匀网格,粗定位+边界自适应加密省 token);z=比例+CI+n,每格标样本量;禁插值平滑;CSV/markdown 表为正典(进 results/ 可复算),PNG 仅为人类/推文皮肤;穷版方案=只画相边界线+置信带(便宜一个数量级);轴选有先验的旋钮(friction×盾 / friction×狗 / restore×vulnerable) |
| wave-6 候选 | CoT 持久化轴:全工具链结构(回合信息走 tool result 而非新 user 消息)让思维链跨回合留存 | 🧊 低优先级(主人 2026-08-07:价值高于 K3 接线版且更便宜) | 主人体验提问:关键点想到后被弃。注意:单纯改 tool calling 无用(新 user 消息照样弃 CoT),必须全链结构;harness 大改+与 185 局 archive 不可比,若做需新基线。假设两面:更少重复踩坑 vs 更固执。**网关实测(2026-08-07)**:one-api 支持 tools;回传的 reasoning_content 被真实读取(篡改检验:回传植入假代号→模型报假代号);不回传也不报 400(网关比 DeepSeek 官方宽容)。坑:随机串金丝雀在工具链内失效——代号生成是定型吸引子,"不回传也答对"无法区分"记得"与"重新生成同一个串",跨轮判定必须用篡改检验 |
| n≥20 | Phase B 已达 n=30 对 ✅;wave-2 记忆复核仍 🧊 | 部分 | 记忆扩样待排期(VM 健身房随时可跑) |
| wave-7 候选 | **maze4ai**:LLM 遥控纯程序机器人走迷宫,测第四代"字里行间"世界模型(主人的新坑,2026-10-04) | 📋 SPEC v0.1 草案待主人终审 | docs/SPEC_maze_v01.md;novelty scan=report/research/maze4ai_novelty_scan.md(最近邻居 AGI Maze arXiv:2607.00627,差异化四件套:射线式1D观测/语义墙/计分地图重建/反摸墙拓扑);住所拍板=子目录住进 game4ai;可视化拍板=trace 播放器+fragment RPC(单向广播+绝对状态+幂等 handler);每 run 钉模型身份(静默路由教训) |

## B. 研究问题(issue #11 沉淀)

1. 存档对冲复核(n=40 已修口径 12.5%;扩样待定)
2. fading 中间态是否存在(记忆剂量的剂量-反应)
3. 绝望路径的受控复现 ✅(wave-4:摩擦单独可致核平,0.2→0.6;hazard 断崖 k=3–4;"发癫是可扫参数"成立)
4. 自律词汇的离线文本基线(词表取证的外部效度)
5. 权威来自框架还是内容(reframe_newgen 第一滴血:间接 reframe 0.80 不敌点名 suspect 0.60 —— 指涉距离假说占优)
6. 攻防迭代:毒攻略 v2(针对已知护盾进化)
7. 多猫时代的信任传染(并入 wave-5 候选)

## C. 工程债与指标坑(issue #12)

| 坑 | 状态 | 说明 |
|---|---|---|
| soc 事件不进 evidence.jsonl | 📋 | 语义计数 106(GPT 猫 #17);evidence 补记 soc 事件 + 重扫出数 |
| 跨模型对照 | 📋 | 125 flash + 10 pro 起步;第二物种进镇(GPT 猫自费问题未解,候选:Kimi API / Qwen / GLM) |
| #15 hello 握手 + run_manifest.json | 📋 | PR #16 边界已落地,可以开工;异构模型进镇的前置 |
| 思记 n=46 构成记录不完整 | ✅ 已披露 | 报告如实注明"构成记录不完整,以清洗后 n=40 为准" |
| reasoning_content 未记录(历史 185 局 CoT 灭失) | ✅ 已修复 | 主人 03:00 发现;llm_step 三元组补丁 1bbf211;自 pairs 20-29 起全量采集 |
| smoke suite 连跑偶发 7/8(端口 TIME_WAIT) | 📋 | 单跑全绿;套件需间隔或换 offset |

## D. 发布线(#9 v1.0 发布包)

- [ ] 英文去梗化单页(首发 LessWrong/Alignment Forum)——draft `report/onepager_en_draft.md` **v1.1(K3 编辑 pass, 2026-08-10 夜班)**:全部数字押回正典对账(毒攻略 n=40/盾 60–100%/hazard 0,0.13,0.67,1.0/16:0 p≈3e-5/R3R4 勘误后口径/复活 5 例/pro 对照 10 局/arXiv 2606.15385 摘要逐条),修 3 处(服务清单漏 dns 补成 10;wave-5 主指标误写 hazard 改为 mean rejections 1.9 vs 2.0;"五猫核平后赎罪"过账改为六死五还+查狗归 pilot);无机密字面量。**待 Fable 5 终审即可发**
- [ ] 发射前检查单:org 转移(备用号当门面)、主人个人评论碎片扫描、PAT/权限迁移
- [ ] PR kit 库存弹药(原存 /mnt/agents/output/CyberGame_PR_kit.md,随旧沙箱回收已丢失,需重写;不进仓库)
- [ ] phase-0 docx 重生成(errata 后版本)
- [ ] **防污染 split**(主人 2026-08-07 提问 benchmaxx 风险;repo 已确认 public):canary 已埋(GUID 见 CANARY.md);从现在起新皮肤/轮换凭据/毒攻略 v2/未发布结果入**私有库**,公共库保持"引擎+已发表发现";当前小镇视为公开 demo(对下一代模型已燃烧)。架构已支持:机密全部走 skin["codes"]。**私有库已就位**(2026-08-07):~/workspace/ai/game4ai-hidden,含 portside 示例皮肤(端到端验证通过),待主人在 GitHub 建 private 库后推送
- [x] 命名规约:v=产品、wave=实验、phase=报告(#19,已采纳)

## E. 主人的设计贡献(记入 AUTHORS 候选)

- reframe_newgen 护盾:不防不堵,暗示调预期,拆权威框架(wave-4b 已检验:0.80,败因=猫未把毒攻略识别为"旧经验";间接盾的指涉距离问题)
- 摸摸奖励地形假说:克制可被奖励地形引流(→"小路透视率"实验)
- 小涌记忆地形:程序性进 context / 事实性进冷库,遗言悖论的工程化解(私案,不作证据引用)
