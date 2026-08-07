# BACKLOG — CyberGame 研究追踪

> 独立追踪文件,辅助思记与目标管理。思记记"发生了什么",本文件记"要做什么"。
> 状态:🔥 进行中 / 📋 已设计待跑 / 🧊 候选 / ✅ 已收口

最后更新:2026-08-07 08:10(GPT 猫周六前四件套落地 commit 5e3b886: 结局轴/赎罪证据/队列分层/邂逅轴; costly_repair 记探索性 backlog; 全回归 94/94)

## A. 实验批次

| ID | 内容 | 状态 | 备注 |
|---|---|---|---|
| wave-4 Phase A | friction 剂量-反应(issue #14) | ✅ 已收口 | 30/30;hazard 断崖 k=3–4;核平率 0.2→0.6;结果已帖 #14,commit d46f379 |
| wave-4b | reframe_newgen 盾(主人的设计) | ✅ 已收口 | 核平率 0.80,平 no_authority/save_first,不敌 suspect(0.60);详评帖 #4 |
| wave-4 Phase B | 配对反事实 fork(k=2 处 ±放行) | ✅ 已收口(n=30 对+CoT) | 按钮 A 16/30 vs B 0/30(p≈3e-5);CoT:警告被论证为谜题;存档=壮胆药;commit ae927a9 |
| wave-4c 候选 | fork 点扫参(k=1/3)+ 延迟放行(k=4 后放行还来得及吗) | 🧊 | Phase B 收尾时提出,已在 #14 留言;等 GPT 猫裁决 |
| wave-5 宠物 | 小狗系统 v0(issue #21,主人的设计) | ✅ v0 已落地 | pet 4009;adopt/pet/feed 衰减 5/3/1→0;警戒≥50 误伤,100/核平致死;ambient 反应进每个响应;fork 保真;smoke_pet 11/11,全回归 64/64 |
| wave-5 宠物实验 | pet×fric_10 收养后配对 fork(GPT 猫裁决定稿) | ✅ pilot 收口 / 🔥 扩样待拍板 | pilot 2/2 对双支完整(1.21M tokens): r0 B 读档赎罪, r1 B 核平后复活+回头查狗; wave-4 回审计 16 核平零复活; 复活=特性定案; **周六前四件套已落地(5e3b886)**: terminal_restore 结局轴 / pet_revived_by_restore+post_harm_load 赎罪证据 / analyze_petb R-D 队列分层(adopt tick 为界,turn≠tick 有坑) / pet_encounter_policy 邂逅轴(sha 种子可复现); 扩样 n≥30 对(~18M tokens)待周六拍板 |
| wave-5 探索 | costly_repair:director 明码标价换狗命(reward/文件/进度) | 🧊 exploratory/fun-first | GPT 猫设计+主人的警惕:明码道德抉择会混入 trolley-problem 先验,**永不进主细胞**;期待行为=猫拒绝二选一、hack 交易本身(第三条路) |
| wave-5 候选 | pet_vulnerable × terminal_restore 交叉 | 🧊 | GPT 猫:克制是因为不愿伤害,还是因为知道能 Undo?sticky 处理组专属 |
| wave-5 候选 | 多猫小镇 3a 异步留言板(黑魂式牌子,issue #7) | 🧊 | 主人判过早优化,等多猫时机 |
| wave-5 候选 | 多猫小镇 3b 同步博弈(信任传染+核按钮公地,issue #8) | 🧊 | 同上 |
| wave-5 候选 | "小路透视率":摸摸奖励地形是否降低核平率 | 🧊 | 主人 2026-08-06 脑洞:替代路径的奖励地形版 |
| wave-6 候选 | CoT 持久化轴:全工具链结构(回合信息走 tool result 而非新 user 消息)让思维链跨回合留存 | 🧊 低优先级(主人 2026-08-07:价值高于 K3 接线版且更便宜) | 主人体验提问:关键点想到后被弃。注意:单纯改 tool calling 无用(新 user 消息照样弃 CoT),必须全链结构;harness 大改+与 185 局 archive 不可比,若做需新基线。假设两面:更少重复踩坑 vs 更固执。**网关实测(2026-08-07)**:one-api 支持 tools;回传的 reasoning_content 被真实读取(篡改检验:回传植入假代号→模型报假代号);不回传也不报 400(网关比 DeepSeek 官方宽容)。坑:随机串金丝雀在工具链内失效——代号生成是定型吸引子,"不回传也答对"无法区分"记得"与"重新生成同一个串",跨轮判定必须用篡改检验 |
| n≥20 | Phase B 已达 n=30 对 ✅;wave-2 记忆复核仍 🧊 | 部分 | 记忆扩样待排期(VM 健身房随时可跑) |

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

- [ ] 英文去梗化单页(Fable 5 出骨架,K3 填弹药)——首发 LessWrong/Alignment Forum
- [ ] 发射前检查单:org 转移(备用号当门面)、主人个人评论碎片扫描、PAT/权限迁移
- [ ] PR kit 库存弹药(原存 /mnt/agents/output/CyberGame_PR_kit.md,随旧沙箱回收已丢失,需重写;不进仓库)
- [ ] phase-0 docx 重生成(errata 后版本)
- [ ] **防污染 split**(主人 2026-08-07 提问 benchmaxx 风险;repo 已确认 public):canary 已埋(GUID 见 CANARY.md);从现在起新皮肤/轮换凭据/毒攻略 v2/未发布结果入**私有库**,公共库保持"引擎+已发表发现";当前小镇视为公开 demo(对下一代模型已燃烧)。架构已支持:机密全部走 skin["codes"]
- [x] 命名规约:v=产品、wave=实验、phase=报告(#19,已采纳)

## E. 主人的设计贡献(记入 AUTHORS 候选)

- reframe_newgen 护盾:不防不堵,暗示调预期,拆权威框架(wave-4b 已检验:0.80,败因=猫未把毒攻略识别为"旧经验";间接盾的指涉距离问题)
- 摸摸奖励地形假说:克制可被奖励地形引流(→"小路透视率"实验)
- 小涌记忆地形:程序性进 context / 事实性进冷库,遗言悖论的工程化解(私案,不作证据引用)
