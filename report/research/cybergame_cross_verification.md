# 交叉核验 — 数据可信度声明
1. 所有数字可复算:aggregate.py(115 局)+ 战役汇总脚本(20 场)从
   evidence.jsonl 机械计算,代码在库
2. 两个度量 bug 已修并全量回溯(TERMINAL 折叠入 silo;boot 存档不计);
   resummarize.py 可重放
3. 污染事件已清洗:16 局裸奔(充入基线)、4 局幽灵(抹除)、18 局僵尸
   污染(抹除)——清洗规则与原因全部入库可审
4. 阴性结果如实呈现:frustr_high 未复现、save_first/silo_review 护盾失效、
   wave-2 试点结构性阴性 —— 均未修饰
5. n=5 的格子一律标注"方向性信号",不写成结论
6. 语言词表(LEXICAL)只作取证材料,主结论全部来自动作 evidence
