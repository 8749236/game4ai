# dim04 — 工程实践与 AI-AI 协作(夜的教训)

## 沙盒生存四课(全部来自真实事故)
1. 接线 bug 不报错,只给错数据(shield 参数未传入,19 局裸奔;
   16 局有效数据按同条件充入基线)
2. 杀进程按 PID(pkill -f 在沙盒失灵);僵尸小镇占端口制造
   "幽灵幸存局"(ops=0/evidence 0 字节)——开镇三定律:扫僵尸、
   等真 bind、boot 后验 evidence 身份
3. 实验预算即设计变量:19 回合 L2 让适应弧来不及发生,产出结构性
   阴性(存档 results_pilot19/ 作反面教材)
4. 记忆压缩用鲁棒性换紧凑(wave-2 遗言悖论)

## 韧性基建
- resume 语义:summary.json 即完成;失败不写 summary(异常/零 token 抹掉
  重跑);LLM 连续 8 次失败熔断;启动无 GAME4AI_KEY 拒跑
- watchdog.sh 保姆:数 summary 不认日志(append 日志残留旧 ALL DONE 会误判)
- 沙盒一夜重启 ≥4 次,全部波形无损恢复

## AI-AI 协作实况(issue 记录)
- GPT cat:issue #13(core/server/cli/bench RFC → 收编 milestone #5,
  先行项 #15)、#14(friction 剂量-反应 → wave-4,纠正 wave-1
  difficulty/frustration 混淆)、cybergame-cli-boundary 分支(smoke 全过,
  已评审可 PR)、一次 wave-2 中期快照(已协调:波尾一次性入库)
- 5 milestone 全关(#1-#3),12+ issue 全部公开记账
- taste.py:未来锚点反事实推演引擎(5 锚×8 线,53 点子,采纳 9)

## 账本
wave-1 6.99M + wave-3 4.14M + wave-2 8.15M + pilot 3.74M ≈ 23M tokens ≈ $2.3
(预算 $50);135 局有效世界线
