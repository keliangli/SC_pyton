# ModelScope 量化模型分析汇总（2026-03-09）

## 1. 任务范围
本次汇总包含三部分：
1. Qwen3-32B 官方量化模型梳理
2. Qwen3-32B 量化模型得分/benchmark 可见性检查
3. ModelScope 全站模型的量化类型分布统计与图表

---

## 2. Qwen3-32B 官方量化模型梳理
已确认的官方相关模型：
- `Qwen/Qwen3-32B`
- `Qwen/Qwen3-32B-AWQ`
- `Qwen/Qwen3-32B-FP8`
- `Qwen/Qwen3-32B-GGUF`
- `Qwen/Qwen3-32B-MLX-bf16`
- `Qwen/Qwen3-32B-MLX-4bit`
- `Qwen/Qwen3-32B-MLX-6bit`
- `Qwen/Qwen3-32B-MLX-8bit`

结论：
- AWQ / GGUF / MLX-4bit / FP8 等官方版本均可在 ModelScope 上查到。
- 但 ModelScope 并没有统一结构化的“量化模型评分字段”。

相关报告：
- `reports/modelscope_quant_scores_2026-03-09.txt`

---

## 3. AWQ Int4 benchmark 可见性检查
在 `Qwen/Qwen3-32B-AWQ` 的 README 中，官方直接给出了 AWQ-int4 与 bf16 的对比性能表。

### Thinking 模式
- bf16: LiveBench 74.9 / GPQA 68.4 / MMLU-Redux 90.9 / AIME24 81.4
- AWQ-int4: LiveBench 73.1 / GPQA 69.0 / MMLU-Redux 90.8 / AIME24 79.4

### Non-Thinking 模式
- bf16: LiveBench 59.8 / GPQA 54.6 / MMLU-Redux 85.7
- AWQ-int4: LiveBench 59.8 / GPQA 53.1 / MMLU-Redux 85.6

观察：
- AWQ-int4 相比 bf16，整体精度损失不大。
- ModelScope 平台字段 `Metrics` 本身并未统一填充，上述分数来自 README 内容，而非平台统一评分系统。

---

## 4. ModelScope 全站量化类型分布统计
数据源：ModelScope 官方列表接口 `api/v1/models`

### 总览
- 全部模型数：175,269
- 识别为量化相关的模型数：35,901
- 量化相关模型占比：20.48%

### 主类别分布（互斥口径）
- GGUF：17,325（48.26% 量化模型）
- int3：4,254（11.85%）
- int4：3,116（8.68%）
- AWQ：2,004（5.58%）
- GPTQ：1,900（5.29%）
- int8：1,674（4.66%）
- FP8：1,500（4.18%）
- EXL2：781（2.18%）
- q2：774（2.16%）

### 关键结论
- GGUF 是当前 ModelScope 上最主流的量化模型发布形态。
- 社区中大量模型并不是严格按 AWQ/GPTQ 命名，而是直接按 int3/int4/int8/4bit/8bit 命名。
- AWQ 与 GPTQ 规模接近，AWQ 略高于 GPTQ。
- EXL2/HQQ/AQLM/EETQ 等属于长尾量化生态。

详细报告：
- `reports/modelscope_quant_type_distribution_2026-03-09.json`
- `reports/modelscope_quant_type_distribution_2026-03-09.md`
- `reports/modelscope_quant_type_distribution_summary_2026-03-09.md`

---

## 5. 图表结果
已生成两类图：

### 原始主类别 Top10 图
- SVG：`reports/modelscope_quant_type_distribution_top10_2026-03-09.svg`
- HTML：`reports/modelscope_quant_type_distribution_top10_2026-03-09.html`

### 按大类 / bit-width 归并图
- SVG：`reports/modelscope_quant_type_distribution_bitwidth_2026-03-09.svg`
- HTML：`reports/modelscope_quant_type_distribution_bitwidth_2026-03-09.html`

图表索引：
- `reports/modelscope_quant_type_charts_index_2026-03-09.md`

---

## 6. 统计口径说明
本次分类基于以下字段进行规则匹配：
- `Name`
- `ChineseName`
- `Tags`
- `OfficialTags`
- `Libraries`
- `Frameworks`
- `ModelType`
- `Description`

并输出两套口径：
1. 互斥主类别统计：每个模型只归一个主类
2. 多标签统计：一个模型可以同时命中多个量化标签

注意：
- 这份统计反映的是 ModelScope 平台模型命名/标签层面的量化生态分布
- 不是官方 benchmark / 精度排行榜

---

## 7. 建议的 GitHub 上传内容
建议上传以下文件：
- 本汇总：`reports/modelscope_quant_analysis_bundle_2026-03-09.md`
- 全站统计摘要：`reports/modelscope_quant_type_distribution_summary_2026-03-09.md`
- 原始详细统计：`reports/modelscope_quant_type_distribution_2026-03-09.json`
- 图表：
  - `reports/modelscope_quant_type_distribution_top10_2026-03-09.svg`
  - `reports/modelscope_quant_type_distribution_bitwidth_2026-03-09.svg`
- Qwen3-32B 量化检查：`reports/modelscope_quant_scores_2026-03-09.txt`

如果要对外展示，推荐目录结构：
- `reports/modelscope-quant-2026-03-09/summary.md`
- `reports/modelscope-quant-2026-03-09/distribution.json`
- `reports/modelscope-quant-2026-03-09/top10.svg`
- `reports/modelscope-quant-2026-03-09/bitwidth.svg`
- `reports/modelscope-quant-2026-03-09/qwen3-32b-quant-notes.txt`
