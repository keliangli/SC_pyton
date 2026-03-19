# 大模型评测基准：逻辑推理测试数据集总结

> 更新时间：2026-03-19  
> 主题：大模型逻辑推理（Logical Reasoning）常见 benchmark / dataset 梳理

---

## 1. 一句话结论

逻辑推理评测的核心不是“会不会答题”，而是模型能否在自然语言、规则约束、因果关系和多步条件之间，做出 **一致、可追踪、可验证** 的推断。

逻辑推理 benchmark 通常覆盖：

- **自然语言逻辑推理**：论证、条件关系、蕴含、矛盾、假设
- **因果推理**：原因、结果、反事实
- **隐式逻辑 / 常识推理**：事件流程、代词指代、常识排除
- **数学与多步推理**：文字题、符号运算、多步计算
- **形式逻辑与规则推理**：命题逻辑、一阶逻辑、链式规则证明
- **中文考试型推理**：逻辑阅读、行测/考试风格推理题

如果把常见逻辑推理 benchmark 压缩成一句话：

- **LogiQA / ReClor / ANLI**：自然语言逻辑与论证推理
- **COPA / e-CARE**：因果推理
- **HellaSwag / Winogrande / WSC / CommonsenseQA / PIQA**：隐式逻辑与常识推理
- **GSM8K / MATH / AQUA-RAT / SVAMP**：数学与多步推理
- **ProofWriter / PrOntoQA / FOLIO / CLUTRR / bAbI**：严格规则与形式逻辑
- **MMLU / AGIEval / C-Eval / CMMLU**：综合考试型推理

---

## 2. 逻辑推理到底在测什么？

### 2.1 演绎推理（Deductive Reasoning）
从已知规则推出必然结论。
例如：
- 所有 A 都是 B
- x 是 A
- 推出 x 是 B

### 2.2 归纳 / 类比推理（Inductive / Analogical Reasoning）
从样例中归纳规则，或者在不同对象之间做结构映射。

### 2.3 因果推理（Causal Reasoning）
判断什么是原因，什么是结果，或者在反事实条件下是否仍成立。

### 2.4 多步组合推理（Multi-step Compositional Reasoning）
需要连续维护中间状态，而不是只凭一句话局部匹配。

### 2.5 形式逻辑 / 程序化逻辑（Formal / Symbolic Reasoning）
更偏规则、变量、命题与约束求解。

### 2.6 自然语言中的隐式逻辑
题目表面看起来是阅读理解、常识选择题，但真正区分模型的地方在于逻辑链是否成立。

---

## 3. 常见逻辑推理 benchmark 分类

### A. 自然语言推理 / 演绎推理
- LogiQA
- LogiQA 2.0
- ReClor
- ANLI
- RTE / CB（较轻量）

### B. 因果与反事实推理
- COPA
- e-CARE
- bAbI（部分任务）

### C. 常识逻辑 / 隐式推理
- HellaSwag
- Winogrande
- WSC
- CommonsenseQA
- PIQA

### D. 数学与符号逻辑推理
- GSM8K
- MATH
- AQUA-RAT
- SVAMP
- ASDiv
- MAWPS

### E. 复杂规则推理 / 形式逻辑
- ProofWriter
- PrOntoQA
- FOLIO
- CLUTRR
- BBH（部分任务）

### F. 中文逻辑推理 / 考试型推理
- LogiQA（中文背景）
- AGIEval（中文逻辑相关子任务）
- C-Eval
- CMMLU

---

## 4. 详细数据集说明（含任务内容 + 例子）

---

# 4.1 LogiQA

## 定位
LogiQA 是逻辑推理 benchmark 里非常经典的一类，核心是 **自然语言逻辑选择题**。

## 测什么
- 读懂短论证
- 分析条件关系
- 判断支持、削弱、假设、结论是否成立

## 内容形式
- 一段短文
- 一个问题
- 四个选项中选一个

## 例子（仿写）
- 段落：`所有通过资格审查的人都必须参加面试。张明已经参加了面试。`
- 问题：`以下哪项一定成立？`
- 选项：
  - A. 张明通过了资格审查
  - B. 张明申请了这个岗位
  - C. 张明未必通过资格审查
  - D. 张明一定被录取
- **分析**：规则是“通过审查 -> 参加面试”，不是双向，因此不能推出 A。更合理理解是 **C**。

## 总结
LogiQA 很适合测：
- 论证结构理解
- 条件逻辑
- 选项排除能力

---

# 4.2 LogiQA 2.0

## 定位
LogiQA 2.0 是 LogiQA 的增强版本，目标是提高逻辑题质量与难度。

## 测什么
- 更复杂的论证分析
- 更贴近考试/逻辑阅读里的推断题

## 内容形式
- 段落 + 问题 + 多选项

## 例子（仿写）
- 段落：`如果一个项目延期，就一定会增加预算。只有通过审批的项目才能获得增加后的预算。某项目没有获得增加后的预算。`
- 问题：`以下哪项最可能成立？`
- 正确思路通常不是直接推出“没延期”，而是分析审批和预算之间的关系。

## 总结
比起 LogiQA 1.0，更适合作为现代 LLM 逻辑阅读 benchmark 的一部分。

---

# 4.3 ReClor

## 定位
ReClor（Reading Comprehension dataset for Logical Reasoning）是专门为 **逻辑阅读理解** 设计的数据集。

## 测什么
- 读懂论证
- 区分前提与结论
- 找出论证依赖的假设
- 判断什么是支持、削弱或最合理结论

## 内容形式
- 一段 argument
- 一个问题
- 四个选项

## 例子（仿写）
- 段落：`某城市开通地铁后，市中心拥堵下降。因此，只要扩建地铁就总能降低拥堵。`
- 问题：`该论证依赖哪项假设？`
- 关键假设可能是：`拥堵下降主要由地铁导致，而不是远程办公、限行等其他因素。`

## 总结
ReClor 非常适合测：
- argument understanding
- 逻辑漏洞识别
- 假设抽取能力

---

# 4.4 ANLI

## 定位
ANLI（Adversarial NLI）是自然语言推断 benchmark 的对抗增强版。

## 测什么
- entailment / contradiction / neutral
- 在对抗样本上仍保持稳定推断

## 内容形式
- premise + hypothesis
- 三分类

## 例子（仿写）
- 前提：`The boy was too tired to finish his homework.`
- 假设：`The boy finished his homework.`
- → contradiction

## 总结
ANLI 比传统 NLI 更难，不容易靠表面模式取巧。

---

# 4.5 COPA

## 定位
COPA（Choice of Plausible Alternatives）是经典因果推理 benchmark。

## 测什么
- 判断事件的合理原因或结果
- 方向性因果推理

## 内容形式
- 一个前提
- 问原因或结果
- 两个选项二选一

## 例子（仿写）
- 前提：`杯子掉在地上后碎了。`
- 问：`更可能的原因是什么？`
  - A. 杯子是玻璃做的
  - B. 杯子被放进洗碗机
- → `A`

## 总结
COPA 小而精，适合快速测因果方向判断。

---

# 4.6 e-CARE

## 定位
e-CARE 是更细粒度的因果推理 benchmark。

## 测什么
- 事件之间的 cause / effect 关系
- 细粒度因果选择

## 例子（仿写）
- 事件：`道路结冰，交通事故增多。`
- 问：`更可能的原因是？`
  - A. 夜间气温降到零下
  - B. 市民买了更多雨伞
- → `A`

---

# 4.7 HellaSwag

## 定位
HellaSwag 表面是常识续写，实际高度依赖 **事件流程逻辑**。

## 测什么
- 事件顺序是否合理
- 常识续写是否连贯
- 伪合理选项识别

## 内容形式
- 给一段上下文
- 多个候选后续
- 选最合理续写

## 例子（仿写）
- 上下文：`一个人把面糊倒进平底锅。`
- A：`他开始翻面煎饼。`
- B：`他把电视搬进浴室。`
- → `A`

## 总结
适合测：
- 事件流程理解
- 常识 + 隐式逻辑

---

# 4.8 Winogrande

## 定位
Winogrande 是 Winograd 风格指代消解 benchmark 的大规模扩展版。

## 测什么
- 指代消解
- 借助上下文与常识判断隐含逻辑关系

## 例子（仿写）
- `小李给小王递伞，因为他要出门。`
- `他` 更可能指谁？
- 这类题需要综合语义和情境理解。

---

# 4.9 WSC / WSC273

## 定位
WSC（Winograd Schema Challenge）是最经典的指代消解 benchmark 之一。

## 测什么
- 代词指向
- 常识 + 语言逻辑

## 例子（仿写）
- `The trophy didn't fit in the suitcase because it was too big.`
- `it` 指 `trophy`

## 总结
数据量不大，但非常能测“理解深度”。

---

# 4.10 CommonsenseQA

## 定位
CommonsenseQA 主要是常识问答，但很多题本质上也是逻辑筛选题。

## 测什么
- 概念关系
- 常识推断
- 排除明显不合理选项

## 例子（仿写）
- `通常在哪里能借到书？`
  - A. 冰箱
  - B. 图书馆
  - C. 公路
- → `图书馆`

---

# 4.11 PIQA

## 定位
PIQA 是物理常识推理 benchmark。

## 测什么
- 日常物理问题中的合理方案选择
- 方案是否符合现实世界约束

## 例子（仿写）
- 问：`怎样让饮料更久保持冷？`
  - A. 用隔热材料包住
  - B. 放在热灯下
- → `A`

---

# 4.12 GSM8K

## 定位
GSM8K 是最经典的多步数学文字题数据集之一。

## 测什么
- 多步算术推理
- 自然语言转数学过程
- chain-of-thought 稳定性

## 例子（仿写）
- `小王有 3 个苹果，又买了 5 个，送给同学 2 个，还剩多少个？`
- 推理：`3 + 5 - 2 = 6`
- → `6`

## 总结
GSM8K 对测试多步推理稳定性非常重要。

---

# 4.13 MATH

## 定位
MATH 是比 GSM8K 更难的数学推理 benchmark。

## 测什么
- 高难度公式推导
- 多步数学逻辑
- 更复杂的中间状态控制

## 例子（仿写）
- `解方程：2x + 3 = 11`
- 推理：`2x = 8 -> x = 4`
- → `4`

---

# 4.14 AQUA-RAT

## 定位
AQUA-RAT 是数学逻辑推理数据集，并强调 rationale（推理解释）。

## 测什么
- 数学题中的推理链
- 最终答案之外的 reasoning 质量

## 例子（仿写）
- `某商品打八折后是 80 元，原价是多少？`
- 选项：90 / 100 / 110 / 120
- → `100`

---

# 4.15 SVAMP / ASDiv / MAWPS

## 定位
这些都属于数学文字题数据集。

## 测什么
- 语言描述解析
- 条件提取
- 算术逻辑

## 例子（仿写）
- `箱子里有 12 个球，拿走 4 个，又放进去 3 个，还剩多少个？`
- → `11`

## 总结
这类数据集很适合看模型是否能把自然语言稳定转成运算步骤。

---

# 4.16 ProofWriter

## 定位
ProofWriter 更接近形式逻辑证明。

## 测什么
- 显式规则链演绎
- 判断某个命题是否能被证明/证伪/未知

## 内容形式
- 一组规则
- 一组事实
- 一个待验证命题

## 例子（仿写）
- 规则：
  - `所有鸟都会飞。`
  - `麻雀是鸟。`
- 问题：`麻雀会飞吗？`
- → `True`

## 总结
适合测严格规则推理，而不是开放常识。

---

# 4.17 PrOntoQA

## 定位
PrOntoQA 是偏程序化、多跳规则推理 benchmark。

## 测什么
- 多层规则链
- 中间状态一致性
- 长 reasoning chain 稳定性

## 例子（仿写）
- 规则：
  - `如果 A，则 B`
  - `如果 B，则 C`
  - `A 成立`
- 问：`C 是否成立？`
- → `是`

---

# 4.18 FOLIO

## 定位
FOLIO 是一阶逻辑风格的推理 benchmark。

## 测什么
- 量词、集合、命题之间的逻辑关系
- 自然语言与形式逻辑之间的映射

## 例子（仿写）
- 前提：
  - `所有教授都是老师。`
  - `有些老师会编程。`
- 命题：`有些教授会编程。`
- → 不一定成立

## 总结
很适合测模型是否真正理解量词和蕴含关系。

---

# 4.19 CLUTRR

## 定位
CLUTRR 是关系链推理 benchmark，重点是家族关系多跳推理。

## 测什么
- 多跳关系组合
- 链式逻辑推理

## 例子（仿写）
- `A 是 B 的母亲，B 是 C 的父亲。`
- 问：`A 和 C 是什么关系？`
- → `祖母`

## 总结
非常适合测多跳关系推理的一致性。

---

# 4.20 bAbI（部分任务）

## 定位
bAbI 是早期人工构造 reasoning benchmark 的代表。

## 测什么
- 状态追踪
- 多跳问答
- 简单逻辑关系

## 例子（仿写）
- `John went to the kitchen.`
- `John picked up the apple.`
- `John went to the garden.`
- 问：`Where is the apple?`
- → `garden`

---

# 4.21 BIG-bench / BBH

## 定位
BIG-bench 是大规模任务集合，BBH 是困难子集。

## 测什么
- 多类逻辑推理任务
- 复杂规则
- 隐式模式
- 多步 reasoning

## 例子（仿写）
- 给一组规则，判断哪个对象满足全部约束
- 或根据一个隐藏模式推导最后结果

## 总结
它更像 reasoning 能力总盘点，而不是单点逻辑 benchmark。

---

# 4.22 MMLU / AGIEval / C-Eval / CMMLU 中的逻辑推理成分

这些 benchmark 不是专门做“逻辑推理”的，但包含大量逻辑相关子领域。

## MMLU
- 含逻辑、法学、哲学、数学等推理题
- 本质是“读懂题目 + 逻辑分析 + 选项判断”

## AGIEval
- 很多标准化考试题本质就是逻辑推理题
- 如法律推断、论证、定量/文字逻辑

## C-Eval / CMMLU
- 中文考试 benchmark 中包含不少行测、法学、逻辑学风格题

### 总结
这些 benchmark 更像“综合推理能力”测试，逻辑推理只是其中一部分。

---

## 5. 如何按用途选择逻辑推理 benchmark？

### 如果你要测“自然语言逻辑阅读”
优先：
- LogiQA
- LogiQA 2.0
- ReClor
- ANLI

### 如果你要测“因果逻辑”
优先：
- COPA
- e-CARE
- HellaSwag（部分）

### 如果你要测“隐式逻辑 + 常识”
优先：
- HellaSwag
- Winogrande
- WSC
- CommonsenseQA
- PIQA

### 如果你要测“数学与多步推理”
优先：
- GSM8K
- MATH
- AQUA-RAT
- SVAMP
- ASDiv

### 如果你要测“形式逻辑 / 严格规则推理”
优先：
- ProofWriter
- PrOntoQA
- FOLIO
- CLUTRR
- bAbI

### 如果你要测“中文逻辑推理”
优先：
- LogiQA
- AGIEval（中文逻辑相关任务）
- C-Eval
- CMMLU

---

## 6. 我建议的实际 benchmark 组合

### 组合 A：通用大模型逻辑推理轻量版
- LogiQA
- COPA
- HellaSwag
- Winogrande
- GSM8K
- MMLU（逻辑相关子域）

### 组合 B：逻辑阅读 + 常识推理版
- LogiQA / LogiQA 2.0
- ReClor
- COPA
- HellaSwag
- Winogrande
- CommonsenseQA

### 组合 C：严格规则 / 可验证推理版
- ProofWriter
- PrOntoQA
- FOLIO
- CLUTRR
- bAbI

### 组合 D：中文逻辑推理版
- LogiQA
- AGIEval（中文逻辑/考试部分）
- C-Eval
- CMMLU

---

## 7. 看逻辑推理 benchmark 时要注意什么？

### 7.1 不要把“常识题”和“逻辑题”混为一谈
- 有些题看起来是常识题，本质上靠逻辑排除
- 有些题看起来是逻辑题，其实被知识记忆影响很大

### 7.2 不要只看最终 accuracy
逻辑推理特别要关注：
- 多步是否稳定
- 中间状态会不会漂
- 是否容易被干扰项误导
- chain-of-thought 是否只是“像在推理”

### 7.3 自然语言逻辑 ≠ 形式逻辑
- LogiQA / ReClor 更偏自然语言论证推理
- ProofWriter / FOLIO / PrOntoQA 更偏严格规则和命题逻辑

### 7.4 数学推理 ≠ 全部逻辑推理
- GSM8K 非常重要，但只覆盖逻辑推理的一部分
- 如果只跑数学题，会漏掉 argument reasoning / causal reasoning / symbolic reasoning

### 7.5 中文逻辑评测不能只靠英文 benchmark 代替
- 英文逻辑强，不代表中文考试与逻辑阅读一定强
- 中文长句、论证表述和题面风格差异很大

---

## 8. 最后的总结

真正做“大模型逻辑推理评测”时，建议不要只跑单一 benchmark，而要至少同时覆盖：

- **一组自然语言逻辑任务**：LogiQA / ReClor / ANLI
- **一组因果/常识逻辑任务**：COPA / HellaSwag / Winogrande / CommonsenseQA
- **一组数学与多步任务**：GSM8K / MATH / AQUA-RAT
- **一组严格规则/形式逻辑任务**：ProofWriter / FOLIO / PrOntoQA / CLUTRR

只有这样，才能比较完整地判断模型的逻辑推理能力，而不是只看某个单点分数。
