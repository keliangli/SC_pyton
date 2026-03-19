# 大模型评测基准：语言理解测试数据集总结

> 更新时间：2026-03-19  
> 主题：大模型语言理解（Language Understanding）常见 benchmark / dataset 梳理

---

## 1. 一句话结论

大模型里的“语言理解评测”并不是一个单独数据集，而是一组能力集合。通常要联合评估：

- **基础 NLU**：句法、情感、相似度、自然语言推断
- **阅读理解**：段落问答、抽取、无答案判断、长文选择题
- **常识与隐式推理**：因果、事件流程、指代消解、物理常识
- **综合知识理解**：多学科考试题、专业题
- **中文专项理解**：中文分类、匹配、阅读、成语、考试

如果把最常见的 benchmark 压缩成一句话：

- **GLUE / SuperGLUE / CLUE**：基础 NLU
- **SQuAD / DROP / RACE / C3**：阅读理解
- **HellaSwag / PIQA / CommonsenseQA / Winogrande / COPA**：常识与隐式推理
- **MMLU / AGIEval / C-Eval / CMMLU**：综合知识型理解

---

## 2. 语言理解到底在测什么？

### 2.1 句子级理解
测模型是否能理解一句话或两句话的语义关系，例如：
- 情感分类
- 语法可接受性判断
- 句子相似度
- 自然语言推断（entailment / contradiction / neutral）

### 2.2 篇章级理解
测模型是否能读懂一段文本，并完成：
- 答案抽取
- 文中定位
- 判断文中是否给出答案
- 长文主旨与细节理解

### 2.3 推理型理解
测模型是否能在语言表面之外做进一步判断，例如：
- 因果关系推断
- 常识补全
- 代词指代消解
- 词义消歧

### 2.4 知识型理解
测模型是否能把语言理解和学科知识结合起来，例如：
- 选择题
- 学科考试题
- 专业知识问答

### 2.5 中文理解
测中文语境下的：
- 分类
- 匹配
- 阅读
- 推断
- 成语语义
- 中文考试能力

---

## 3. 常见 benchmark 分类总览

### A. 通用自然语言理解（General NLU）
- GLUE
- SuperGLUE
- CLUE（中文）

### B. 阅读理解 / 问答（Reading Comprehension & QA）
- SQuAD
- DROP
- RACE
- ReCoRD
- BoolQ
- MultiRC
- C3（中文）

### C. 常识与推理理解（Commonsense & Reasoning）
- COPA
- HellaSwag
- PIQA
- CommonsenseQA
- Winogrande
- ARC
- OpenBookQA
- WSC / Wino 类数据集

### D. 综合知识与考试型理解（Knowledge + Exam-style Understanding）
- MMLU
- AGIEval
- BIG-bench / BBH
- C-Eval
- CMMLU

### E. 中文专项理解
- CLUE 各子任务
- C-Eval
- CMMLU
- CHID
- CSL
- TNEWS
- IFLYTEK

---

## 4. 详细数据集说明（含任务内容 + 例子）

---

# 4.1 GLUE

GLUE（General Language Understanding Evaluation）不是单个数据集，而是一个英文基础语言理解任务集合。

## CoLA
- **任务类型**：语法可接受性判断
- **测什么**：句子语法是否自然
- **内容**：输入一句话，输出 acceptable / unacceptable
- **例子**：
  - `The boy is eating an apple.` → acceptable
  - `The boy eating is apple.` → unacceptable

## SST-2
- **任务类型**：情感分类
- **测什么**：句子情感正负面理解
- **内容**：电影评论短句二分类
- **例子**：
  - `This movie is surprisingly moving.` → positive

## MRPC
- **任务类型**：句子对语义等价判断
- **测什么**：两句话是不是在说同一件事
- **内容**：新闻句对 paraphrase / not paraphrase
- **例子**：
  - `The company reported higher profits this quarter.`
  - `This quarter the firm posted increased profits.`
  - → paraphrase

## STS-B
- **任务类型**：语义相似度回归
- **测什么**：两句话相似程度有多高
- **内容**：输出连续分数
- **例子**：
  - `A child is playing in the snow.`
  - `A kid is outdoors in snowy weather.`
  - → 高相似度

## QQP
- **任务类型**：问题重复判断
- **测什么**：两个问题是不是在问同一件事
- **内容**：Quora 问题对
- **例子**：
  - `How can I learn Python fast?`
  - `What is the fastest way to study Python?`
  - → duplicate

## MNLI
- **任务类型**：自然语言推断（NLI）
- **测什么**：前提与假设是蕴含 / 矛盾 / 中立
- **内容**：多领域文本推断
- **例子**：
  - 前提：`A man is riding a bicycle outdoors.`
  - 假设：`A person is riding a bike outside.`
  - → entailment

## QNLI
- **任务类型**：问句-句子蕴含判断
- **测什么**：句子是否能回答该问题
- **例子**：
  - 问：`Where was Marie Curie born?`
  - 句子：`Marie Curie was born in Warsaw.`
  - → entailment

## RTE
- **任务类型**：文本蕴含
- **测什么**：较小规模的经典 entailment 判断
- **例子**：
  - 前提：`The Nile is a river in Africa.`
  - 假设：`The Nile is in Africa.`
  - → entailment

## WNLI
- **任务类型**：代词指代与歧义理解
- **测什么**：复杂指代消解
- **例子**：
  - `Tom told Jerry that he was late.`
  - `he` 指谁？

### GLUE 总结
GLUE 更像“基础 NLU 体检”。适合做传统语言理解能力对照，但对现代强大 LLM 已经偏简单，且任务多为短文本。

---

# 4.2 SuperGLUE

SuperGLUE 是 GLUE 的升级版，更难、更强调真正的理解与推理。

## BoolQ
- **任务类型**：是/否问答
- **测什么**：是否能基于段落回答 yes/no 问题
- **例子**：
  - 段落：`Penguins are flightless birds.`
  - 问题：`Can penguins fly?`
  - → No

## CB（CommitmentBank）
- **任务类型**：三分类推断
- **测什么**：细粒度 entailment / contradiction / neutral
- **例子**：
  - 前提：`The editor believes the article may be inaccurate.`
  - 假设：`The article is definitely inaccurate.`
  - → neutral

## COPA
- **任务类型**：因果推断二选一
- **测什么**：选择最合理的原因或结果
- **例子**：
  - 前提：`The ground was wet in the morning.`
  - 选项A：`It rained overnight.`
  - 选项B：`The sun was shining brightly.`
  - → A

## MultiRC
- **任务类型**：多句阅读理解，多答案判断
- **测什么**：综合多句文本后判断多个选项
- **例子**：
  - 给一段关于动物习性的说明
  - 问：哪些说法成立？
  - 对每个选项分别判断对/错

## ReCoRD
- **任务类型**：实体填空 / 篇章完形理解
- **测什么**：从文章中定位正确实体
- **例子**：
  - 文本：`Alice visited Paris after leaving London.`
  - 填空：`@placeholder visited Paris after leaving London.`
  - → Alice

## WiC
- **任务类型**：词义消歧
- **测什么**：同一个词在不同句子里是不是同一意思
- **例子**：
  - `bank of the river`
  - `bank to deposit money`
  - → 不同词义

## WSC
- **任务类型**：Winograd 风格指代消解
- **测什么**：代词到底指谁，需要语义 + 常识共同判断
- **例子**：
  - `The trophy didn't fit in the suitcase because it was too big.`
  - `it` → trophy

### SuperGLUE 总结
SuperGLUE 比 GLUE 更能体现“真正理解”，适合测歧义、因果、词义、指代和细粒度阅读推断。

---

# 4.3 SQuAD

## SQuAD 1.1
- **任务类型**：抽取式阅读理解
- **测什么**：答案是否能从原文直接抽取出来
- **内容**：段落 + 问题 → 原文片段答案
- **例子**：
  - 文本：`The Eiffel Tower is located in Paris.`
  - 问：`Where is the Eiffel Tower located?`
  - → `Paris`

## SQuAD 2.0
- **新增能力**：无答案判断
- **测什么**：模型是否知道“文中没说”
- **例子**：
  - 文本没有提及设计师
  - 问：`Who designed the lighting system?`
  - → `No answer`

### SQuAD 总结
SQuAD 是经典阅读理解 benchmark，但偏抽取式，对现代大模型的复杂推理和开放生成不够敏感。

---

# 4.4 DROP
- **任务类型**：离散推理阅读理解
- **测什么**：在阅读基础上做计数、比较、日期/数字推理
- **例子**：
  - 文本：`Team A scored 14 and 10. Team B scored 12 and 9.`
  - 问：`How many more points did Team A score than Team B?`
  - → `3`

### DROP 总结
很适合测“阅读 + 简单算术推理”。

---

# 4.5 RACE
- **任务类型**：考试型阅读理解（选择题）
- **来源**：英语考试阅读题
- **测什么**：主旨、细节、上下文理解与选项排除
- **例子**：
  - 给一篇短文
  - 问：`What is the main idea of the passage?`
  - 四选一

### RACE 总结
它更接近“人类考试式阅读理解”，是测试篇章级理解的经典集合。

---

# 4.6 HellaSwag
- **任务类型**：常识续写选择
- **测什么**：在给定上下文后选择最合理的后续事件
- **例子**：
  - 上下文：`A person cracks eggs into a bowl and starts mixing.`
  - A：`They pour it into a pan to cook.`
  - B：`They drive the car to the airport.`
  - → A

### HellaSwag 总结
非常适合测事件流程理解和常识判断。

---

# 4.7 PIQA
- **任务类型**：物理常识问答
- **测什么**：模型对日常物理世界的基本理解
- **例子**：
  - 问：`How do you keep a drink cold longer?`
  - A：`Wrap it in insulating material.`
  - B：`Put it under a heat lamp.`
  - → A

---

# 4.8 CommonsenseQA
- **任务类型**：概念型常识问答
- **测什么**：概念之间的日常常识关系
- **例子**：
  - `Where would you usually borrow books?`
  - A：`library`
  - B：`refrigerator`
  - → A

---

# 4.9 Winogrande
- **任务类型**：代词消解 / 常识填空
- **测什么**：根据上下文和常识判断代词指向
- **例子**：
  - `Sam watered the plant because it was dry.`
  - `it` → plant

---

# 4.10 ARC

ARC 分为：
- ARC-Easy
- ARC-Challenge

- **任务类型**：基础科学选择题
- **测什么**：科学概念理解 + 常识 + 简单推理
- **例子**：
  - `What gas do plants absorb from the atmosphere?`
  - → `carbon dioxide`

---

# 4.11 OpenBookQA
- **任务类型**：开放书本式科学问答
- **测什么**：将已知科学事实迁移到具体场景
- **例子**：
  - 已知：`Metal conducts heat well.`
  - 问：`Why does a metal spoon get hot in soup?`
  - → 因为金属导热

---

# 4.12 MMLU
- **全称**：Massive Multitask Language Understanding
- **任务类型**：多学科选择题
- **覆盖**：法律、医学、历史、计算机、数学、物理等
- **测什么**：广义知识型语言理解
- **例子**：
  - `Which OSI layer handles routing?`
  - → `Network`

### MMLU 总结
MMLU 是 LLM 时代最常见的综合 benchmark 之一。本质是“读懂题目 + 调用知识 + 做出判断”。

---

# 4.13 AGIEval
- **任务类型**：标准化考试风格理解与推理
- **内容**：法律、逻辑、数学、中文考试等
- **测什么**：更接近真实考试场景下的综合语言理解
- **例子**：
  - 给一段法条或论证材料
  - 选出最合理结论

---

# 4.14 BIG-bench / BBH
- **任务类型**：综合困难任务集合
- **测什么**：语言理解、逻辑规则、歧义、符号处理、常识推理等
- **例子**：
  - 给复杂说明
  - 问隐含规则或多步推理结果

### 总结
它更像一张“能力雷达图”，而不是单点语言理解 benchmark。

---

# 4.15 CLUE（中文语言理解评测）

CLUE 是中文领域最常见的综合 benchmark 之一，类似中文版 GLUE / SuperGLUE。

## TNEWS
- **任务类型**：新闻分类
- **测什么**：中文主题理解
- **例子**：
  - `某新能源车企发布新款车型，续航提升。`
  - → `汽车`

## IFLYTEK
- **任务类型**：应用描述分类
- **测什么**：App / 场景描述理解
- **例子**：
  - `一款帮助用户记录运动轨迹和热量消耗的软件。`
  - → `运动健身`

## AFQMC
- **任务类型**：句子匹配
- **测什么**：中文句子是否语义相近
- **例子**：
  - `今天天气不错，适合出去玩。`
  - `今天阳光很好，可以出门散步。`
  - → 相似

## CMNLI
- **任务类型**：中文自然语言推断
- **测什么**：中文蕴含 / 矛盾 / 中立判断
- **例子**：
  - 前提：`他昨天去了北京出差。`
  - 假设：`他昨天不在上海。`
  - → 通常偏蕴含或中立，需要看题设

## CSL
- **任务类型**：关键词与摘要匹配
- **测什么**：摘要内容与关键词是否一致
- **例子**：
  - 摘要讲图像分类
  - 关键词是 `自然语言处理`
  - → 不匹配

## CHID
- **任务类型**：成语填空
- **测什么**：中文成语语义与上下文理解
- **例子**：
  - `面对复杂局面，他处理得____。`
  - → `游刃有余`

## C3
- **任务类型**：中文阅读理解（选择题）
- **测什么**：对话或短文阅读后的理解能力
- **例子**：
  - 给一段中文对话
  - 问：`小明为什么迟到？`
  - 选择正确原因

## WSC（中文版）
- **任务类型**：中文指代消解
- **测什么**：代词和实体之间的对应关系
- **例子**：
  - `小王告诉小李他明天出差。`
  - `他` 指谁？

### CLUE 总结
CLUE 对中文基础语言理解非常有代表性，但对现代超大模型来说也存在容易饱和的问题。

---

# 4.16 C-Eval
- **任务类型**：中文学科考试
- **测什么**：中文环境下的知识型理解与考试能力
- **例子**：
  - `ACID 中的 I 指什么？`
  - → `Isolation`

---

# 4.17 CMMLU
- **任务类型**：中文版 MMLU 风格综合评测
- **测什么**：中文语境下的多学科知识理解
- **例子**：
  - `中国古代“科举”主要用于选拔什么？`
  - → `官员`

---

## 5. 如何按用途选择 benchmark？

### 5.1 如果你要测“基础语言理解”
优先看：
- GLUE
- SuperGLUE
- CLUE

### 5.2 如果你要测“阅读理解能力”
优先看：
- SQuAD 2.0
- DROP
- RACE
- ReCoRD
- C3

### 5.3 如果你要测“常识和隐式理解”
优先看：
- HellaSwag
- PIQA
- CommonsenseQA
- Winogrande
- COPA

### 5.4 如果你要测“综合知识理解 / 考试型表现”
优先看：
- MMLU
- AGIEval
- C-Eval
- CMMLU

### 5.5 如果你要测“中文语言理解”
优先看：
- CLUE
- C-Eval
- CMMLU
- CHID
- C3

---

## 6. 我建议的实际 benchmark 组合

### 组合 A：轻量快速版
适合快速看一个模型大概水平：
- BoolQ
- HellaSwag
- PIQA
- ARC-Challenge
- Winogrande
- MMLU

### 组合 B：英文语言理解完整版
适合做较完整英文 benchmark：
- GLUE（挑代表任务）
- SuperGLUE（BoolQ / COPA / WiC / WSC / MultiRC）
- SQuAD 2.0
- DROP
- HellaSwag
- MMLU

### 组合 C：中文语言理解完整版
适合中文模型评测：
- CLUE（AFQMC / CMNLI / TNEWS / IFLYTEK / CHID / C3）
- C-Eval
- CMMLU

---

## 7. 看这些 benchmark 时要注意什么？

### 7.1 不要只看总分
高分并不代表“所有理解都强”，必须看是：
- 分类强
- 阅读强
- 常识强
- 还是考试题强

### 7.2 看任务和目标场景是否一致
- 聊天机器人
- Agent
- RAG
- Tool-use 前理解
这些场景需要的语言理解能力并不一样。

### 7.3 注意 benchmark 饱和
像 GLUE、SQuAD 这种经典集合，很多现代 LLM 已经很接近天花板，不一定还能有效区分模型差距。

### 7.4 注意数据污染
尤其是：
- GLUE
- SQuAD
- MMLU
- ARC
这类经典 benchmark 很容易在预训练语料里出现过。

### 7.5 英文强不等于中文强
如果目标场景是中文，不做 CLUE / C-Eval / CMMLU，很容易误判。

---

## 8. 最后的总结

真正做“大模型语言理解评测”时，建议不要只跑一个 benchmark，而要按能力组合：

- **基础 NLU**：GLUE / SuperGLUE / CLUE
- **阅读理解**：SQuAD / DROP / RACE / C3
- **常识推理**：HellaSwag / PIQA / CommonsenseQA / Winogrande / COPA
- **综合知识理解**：MMLU / AGIEval / C-Eval / CMMLU

如果目标是现代通用大模型，建议至少使用：
- 一组基础理解任务
- 一组阅读任务
- 一组常识任务
- 一组综合考试任务

而不是只盯一个分数。
