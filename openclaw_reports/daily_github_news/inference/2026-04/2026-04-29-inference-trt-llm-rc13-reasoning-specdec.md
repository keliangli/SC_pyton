# GitHub 大模型推理日报（2026-04-29）

## 今日要点

📌 **TensorRT-LLM v1.3.0rc13 今日发布**：53 commits 大版本预发布，核心看点：DeepSeek-V3.2/V3-Lite 在 Blackwell/SM100 上的专项优化、EAGLE3 动态树投机解码恢复、GLM-4.7/GLM-5 tool parser 支持、VisualGen Cache-DiT 视频生成缓存加速器、FP4 残差量化、Sparse MQA/GQA attention、SageAttention 内核刷新。这是 TRT-LLM 在 1.3 系列 RC 中 feature 最密集的一个版本。

📌 **vLLM main 分支密集修复（v0.20.0 发布后 2 天）**：投机解码支持「推理思考预算（thinking budget）」、KV Cache CPU offload 的 per-job store completion、2 个 DeepSeek V4 紧急修复（inductor 错误 + AOT 编译缓存导入）、Torch 2.12 兼容性准备。v0.20.1 point release 的征兆明显。

📌 **ktransformers AMX MoE SFT + Qwen3 修复**：SFT 训练侧新增 AMX MoE 后端并支持 LoRA、GPTQ INT4 新增 vnni-256 加速路径、Qwen3 RoPE 写入修复解决乱码问题。

---

## 项目速递

### 🔥 TensorRT-LLM — v1.3.0rc13（2026-04-29）

- **Release 链接**：[NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc13](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc13)
- **对比基准**：[main 领先 53 commits](https://github.com/NVIDIA/TensorRT-LLM/compare/v1.3.0rc13...main)

#### 🆕 模型支持
- **DeepSeek-V3.2 / V3-Lite**：Blackwell & SM100 专项优化 + chunked-prefill 修复 [#13142](https://github.com/NVIDIA/TensorRT-LLM/pull/13142) [#13257](https://github.com/NVIDIA/TensorRT-LLM/pull/13257)
- **GLM-4.7 / GLM-5**：tool parser 支持 [#13150](https://github.com/NVIDIA/TensorRT-LLM/pull/13150)
- **Nemotron / Nemotron Nano VL**：视频音频提取、ViT attention 优化、初始化内存降低 [#12921](https://github.com/NVIDIA/TensorRT-LLM/pull/12921) [#12911](https://github.com/NVIDIA/TensorRT-LLM/pull/12911) [#13283](https://github.com/NVIDIA/TensorRT-LLM/pull/13283)
- **VisualGen**：per-model 示例脚本 + 共享配置 + 默认参数 [#12992](https://github.com/NVIDIA/TensorRT-LLM/pull/12992) [#12862](https://github.com/NVIDIA/TensorRT-LLM/pull/12862)

#### ⚡ 内核 & 性能
- **VisualGen Cache-DiT**：视频生成缓存加速器 + 统一缓存框架 [#12548](https://github.com/NVIDIA/TensorRT-LLM/pull/12548)
- **FP4 残差量化** [#12937](https://github.com/NVIDIA/TensorRT-LLM/pull/12937)
- **SageAttention 内核刷新** [#12937](https://github.com/NVIDIA/TensorRT-LLM/pull/12937)
- **RMSNorm 扩展覆盖** [#13033](https://github.com/NVIDIA/TensorRT-LLM/pull/13033)
- **Causal-Conv1d 优化**：prefill & decode 双阶段优化 [#13103](https://github.com/NVIDIA/TensorRT-LLM/pull/13103) [#13117](https://github.com/NVIDIA/TensorRT-LLM/pull/13117)
- **Sparse MQA / GQA attention** + 新 sharding 基础设施 [#12470](https://github.com/NVIDIA/TensorRT-LLM/pull/12470) [#12419](https://github.com/NVIDIA/TensorRT-LLM/pull/12419)

#### 🔄 投机解码
- **EAGLE3 动态树投机解码恢复** [#13081](https://github.com/NVIDIA/TensorRT-LLM/pull/13081)
- **Perfect Router 集成 & 验证** [#13250](https://github.com/NVIDIA/TensorRT-LLM/pull/13250)
- **EAGLE3 LoRA 投机解码修复** [#13005](https://github.com/NVIDIA/TensorRT-LLM/pull/13005)

#### 🏗️ 工程改进
- **Modular logger**：自动模块检测 + per-module 过滤 [#13202](https://github.com/NVIDIA/TensorRT-LLM/pull/13202)
- **Async RL abort/resume**：veRL 集成 [#12272](https://github.com/NVIDIA/TensorRT-LLM/pull/12272)
- **Batched addSequence**：两阶段 claim + 统一 VSWA [#13029](https://github.com/NVIDIA/TensorRT-LLM/pull/13029)
- **Padding-aware CUDA graph tuning** [#13412](https://github.com/NVIDIA/TensorRT-LLM/pull/13412)
- **Async media loading** + 更快视频帧解码 [#13034](https://github.com/NVIDIA/TensorRT-LLM/pull/13034) [#12677](https://github.com/NVIDIA/TensorRT-LLM/pull/12677)

#### 🐛 关键修复
- KV Cache 调度器多项正确性修复（SWA 兼容、token accounting、VSWA+EAGLE 过度分配） [#12968](https://github.com/NVIDIA/TensorRT-LLM/pull/12968) [#12976](https://github.com/NVIDIA/TensorRT-LLM/pull/12976) [#12855](https://github.com/NVIDIA/TensorRT-LLM/pull/12855)
- FMHA full-mask skip-softmax 修复 [#13120](https://github.com/NVIDIA/TensorRT-LLM/pull/13120)
- Vision encoder KV 量化泄露修复 [#13181](https://github.com/NVIDIA/TensorRT-LLM/pull/13181)
- Super V3 多流 MoE 稳定性修复 [#13122](https://github.com/NVIDIA/TensorRT-LLM/pull/13122)
- Qwen3 mrope cache 处理 [#13269](https://github.com/NVIDIA/TensorRT-LLM/pull/13269)

---

### 🏗️ vLLM — main 分支（post-v0.20.0，2026-04-29）

- **Release 链接**：[vllm-project/vllm/commits/main](https://github.com/vllm-project/vllm/commits/main)
- **状态**：v0.20.0 发布后 main 已领先 61+ commits，4月29日当日新增至少 9 commits

#### 📍 4月29日关键 commits
| PR | 标题 | 类型 |
|-----|------|------|
| [#34668](https://github.com/vllm-project/vllm/pull/34668) | **投机解码支持推理思考预算（thinking budget）** | 🆕 Feature |
| [#39186](https://github.com/vllm-project/vllm/pull/39186) | KV Offload：per-job store completion for CPU offloading connector | 🆕 Feature |
| [#41135](https://github.com/vllm-project/vllm/pull/41135) | 修复 DeepSeek V4 inductor 错误 | 🐛 Bugfix |
| [#41090](https://github.com/vllm-project/vllm/pull/41090) | 修复 DeepSeek V4 AOT 编译缓存导入错误 | 🐛 Bugfix |
| [#40845](https://github.com/vllm-project/vllm/pull/40845) | **移除 Torch 2.12 之前的 cublas workaround 代码** | 🔧 兼容性 |
| [#40734](https://github.com/vllm-project/vllm/pull/40734) | 修复 max_num_batched_token 未捕获到 CUDA graph | 🐛 Bugfix |
| [#41113](https://github.com/vllm-project/vllm/pull/41113) | 修复 RoPE 错误 | 🐛 Bugfix |
| [#40422](https://github.com/vllm-project/vllm/pull/40422) | 添加 cohere reasoning & tool parsers | 🆕 Feature |
| [#41034](https://github.com/vllm-project/vllm/pull/41034) | 修复 CPU runner shutdown 错误 | 🐛 Bugfix |

#### 🔍 重点解读
- **投机解码 thinking budget**：这是本月 vLLM 在推理+推理链优化方向上的重要进展，允许在投机解码中为思考 token 分配显式预算，对 DeepSeek-V4 等 reasoning 模型的部署体验提升显著
- **KV Offload per-job store completion**：CPU offloading 的工程完善，多任务共享 KV cache 场景下的生命周期管理更可靠
- **Torch 2.12 准备**：vLLM 已开始清理 Torch 2.12 兼容性代码，意味着下一轮环境升级已在路上

---

### 🧩 ktransformers — AMX MoE SFT + Qwen3 修复（2026-04-22 ~ 04-27）

- **仓库链接**：[kvcache-ai/ktransformers](https://github.com/kvcache-ai/ktransformers)

| 日期 | 内容 | 链接 |
|------|------|------|
| 04-27 | 修复 Qwen3 系列 RoPE 写入导致乱码 | [#1959](https://github.com/kvcache-ai/ktransformers/commit/9f34ef46e664ded0d4c03bbe3070601f1c9e6862) |
| 04-25 | 扁平化 ktransformers 包 shim | [#1955](https://github.com/kvcache-ai/ktransformers/commit/07e274467a71ab1c33ab2f121b6a8dfa60c5a0a2) |
| 04-24 | kt-kernel torch 支持对齐 v0.6.1 release | [#1948](https://github.com/kvcache-ai/ktransformers/commit/eeaeb7bfd7b166ab6252b21b74f6ee1d8a02dbf1) |
| 04-22 | **AMX MoE SFT 后端 + LoRA 支持** | [#1936](https://github.com/kvcache-ai/ktransformers/commit/9544a8960d4dcc3db6046fc7d2a963b48136f72e) |
| 04-13 | GPTQ INT4 新增 vnni-256 加速 | [#1926](https://github.com/kvcache-ai/ktransformers/commit/a9411f1d729b61bdda14ba4490005be3849ff5a3) |

#### 重点
- **AMX MoE SFT**：利用 Intel AMX 指令集加速 MoE 模型 SFT 训练，并原生支持 LoRA——CPU 端大模型微调的重要技术路线
- **GPTQ INT4 vnni-256**：CPU 推理侧 INT4 量化再加速，利用 VNNI-256 指令集提升吞吐

---

### 🧮 DeepGEMM — Mega MoE 基准测试（2026-04-24）

- **Commit 链接**：[deepseek-ai/DeepGEMM@891d57b](https://github.com/deepseek-ai/DeepGEMM/commit/891d57b4db1071624b5c8fa0d1e51cb317fa709f)
- 新增各种优化 + Mega MoE 基准测试，是 04-17 发布的 FP4 Indexer + Mega MoE 功能的后续补强

---

## 工程启发

1. **TensorRT-LLM 的「everything stack」趋势明显**：v1.3.0rc13 从 LLM（DeepSeek V3.2、GLM-5、Nemotron）到 VLM（Nemotron Nano VL、VisualGen）再到 RL（veRL abort/resume），一站式覆盖。如果你的部署环境已经绑定 NVIDIA 生态，TRT-LLM 正在变成「推理+视频生成+RL」的统一 runtime——值得评估其与 vLLM/SGLang 在混合工作负载场景下的差异。

2. **投机解码 + 推理预算的结合是 2026 Q2 的新范式**：vLLM 的「thinking budget」+ TRT-LLM 的 EAGLE3 恢复，说明推理模型（reasoning models）的 speculative decoding 正在从单纯的 token 猜测升级为「理解何时该猜、何时该让模型自己思考」。这个方向对于 DeepSeek-V4 / Qwen3-thinking 等推理模型的实际部署延迟优化非常关键。

3. **CPU 端推理训练基础设施在加速**：ktransformers 的 AMX MoE SFT + GPTQ INT4 vnni-256 说明 CPU 侧的推理和训练能力正在被严肃对待。对于边缘设备 / 成本敏感场景，关注 Intel AMX + ARM SME 的推理加速生态可能比追逐 GPU 更务实。

4. **FP4 量化从实验走向生产**：TensorRT-LLM 的 FP4 残差量化 + DeepGEMM 的 FP4 Indexer 同期出现，标志着 FP4 不再是学术 novelty。预计 Q3 会有更多 FP4 在 MoE 和 KV Cache 中的 benchmark 结果出炉。

---

## 明日跟踪建议

- 🔭 **TensorRT-LLM v1.3.0rc13 → 正式版**：RC 版本历来距离正式 release 不远，关注 v1.3.0 GA 的时间和 changelog 增量。
- 🧪 **vLLM v0.20.1 point release**：DeepSeek V4 的 2 个紧急修复 + RoPE/CUDA graph 修复已有 4 个 bugfix，v0.20.1 可能在周末前发布。
- 📊 关注 TensorRT-LLM FP4 残差量化 + DeepGEMM FP4 Indexer 的实际表现数据。
- 🔍 验证 ktransformers AMX MoE SFT 的实际微调吞吐与 GPU 方案的对比。
- 📌 SGLang 已静默近一个月（上次 release v0.5.10 在 04-06），关注是否在酝酿大版本——Elastic EP 和稀疏注意力方向仍值得跟踪。
