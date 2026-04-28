# GitHub 大模型推理日报（2026-04-28）

## 今日要点

📌 **vLLM v0.20.0 重磅发布**：752 commits、320 位贡献者，这是 vLLM 今年以来规模最大的版本。核心变化：DeepSeek V4 初始支持、CUDA 13.0 成为默认编译目标、PyTorch 2.11 / Transformers v5 升级、FlashAttention 4 重回默认 MLA Prefill 后端、TurboQuant 2-bit KV Cache（4× 容量）、在线量化前端统一、vLLM IR 骨架启动、Model Runner V2 多项推进。

📌 **llama.cpp 连续 3 个 tag**（b8951→b8953）：WebGPU Q1_0 量化支持落地，i-quants 快速 mat-vec kernel，服务端 form-data 转发能力补齐。

---

## 项目速递

### 🔥 vLLM — v0.20.0（2026-04-27）

- **Release 链接**：[vllm-project/vllm/releases/tag/v0.20.0](https://github.com/vllm-project/vllm/releases/tag/v0.20.0)
- **对比基准**：[v0.19.0...v0.20.0](https://github.com/vllm-project/vllm/compare/v0.20.0...main)（main 已领先 30 commits）

#### 🆕 新模型支持
- **DeepSeek V4**：初始支持落地 [#40860](https://github.com/vllm-project/vllm/pull/40860)，含 DSML token 泄露修复 [#40806](https://github.com/vllm-project/vllm/pull/40806)、DSA + MTP IMA 修复 [#40772](https://github.com/vllm-project/vllm/pull/40772)、shared expert silu clamp [#40950](https://github.com/vllm-project/vllm/pull/40950)
- **Hunyuan v3 (Hy3) Preview** [#40681](https://github.com/vllm-project/vllm/pull/40681) + reasoning parser [#40713](https://github.com/vllm-project/vllm/pull/40713)
- **Granite 4.1 Vision** [#40282](https://github.com/vllm-project/vllm/pull/40282)（内置多模态）
- **EXAONE-4.5** [#39388](https://github.com/vllm-project/vllm/pull/39388)、**Phi-4-reasoning-vision-15B** [#38306](https://github.com/vllm-project/vllm/pull/38306)、**BharatGen Param2MoE** [#38000](https://github.com/vllm-project/vllm/pull/38000)
- **Nemotron-v3 VL Nano/Super** [#39747](https://github.com/vllm-project/vllm/pull/39747)、**jina-reranker-v3** [#38800](https://github.com/vllm-project/vllm/pull/38800)、**Jina Embeddings v5** [#39575](https://github.com/vllm-project/vllm/pull/39575)

#### ⚡ Attention / KV Cache 重大升级
- **FlashAttention 4 回归默认 MLA Prefill 后端** [#38819](https://github.com/vllm-project/vllm/pull/38819)，SM90+ 支持 head-dim 512 + paged-KV [#38835](https://github.com/vllm-project/vllm/pull/38835)
- **TurboQuant 2-bit KV Cache** [#38479](https://github.com/vllm-project/vllm/pull/38479)：2-bit 压缩，**4× 容量**，已集成 FA3/FA4 prefill [#40092](https://github.com/vllm-project/vllm/pull/40092)

#### 🔧 量化 / 编译基础设施
- **在线量化前端统一** [#38138](https://github.com/vllm-project/vllm/pull/38138)：experts_int8 合并到 FP8 在线路径 [#38463](https://github.com/vllm-project/vllm/pull/38463)，MXFP8 迁移到新前端 [#40152](https://github.com/vllm-project/vllm/pull/40152)
- **vLLM IR 骨架** [#33825](https://github.com/vllm-project/vllm/pull/33825)：首个 op 为 rms_norm，OOT 平台 kernel import [#38807](https://github.com/vllm-project/vllm/pull/38807)，gemma_rms_norm 已在 IR 上重写 [#39014](https://github.com/vllm-project/vllm/pull/39014)，benchmark infra 就绪 [#40167](https://github.com/vllm-project/vllm/pull/40167)

#### 🚀 性能优化
- **Fused RMS Norm** 优化 batch invariant → **2.1% E2E 延迟降低** [#40413](https://github.com/vllm-project/vllm/pull/40413)
- 避免 seq_lens_cpu GPU→CPU 同步 [#40654](https://github.com/vllm-project/vllm/pull/40654)
- CUDAGraph 内存分析默认开启，启动内存更清晰 [#38284](https://github.com/vllm-project/vllm/pull/38284)
- FX-graph 反序列化跳过，加速 warm compile [#40151](https://github.com/vllm-project/vllm/pull/40151)

#### 🔄 Model Runner V2 推进
- Eagle prefill 全 CUDA Graph [#37588](https://github.com/vllm-project/vllm/pull/37588)
- 自动解析 cudagraph mode/sizes [#32936](https://github.com/vllm-project/vllm/pull/32936)
- 融合概率拒绝采样 kernel [#38496](https://github.com/vllm-project/vllm/pull/38496)
- 多 prompt-logprobs 支持 [#39937](https://github.com/vllm-project/vllm/pull/39937)

#### 🔬 MoE 重构系列
- Unquantized → Full Oracle Flow [#36286](https://github.com/vllm-project/vllm/pull/36286)，CT W8A8 → Oracle [#39187](https://github.com/vllm-project/vllm/pull/39187)
- SharedExperts class 引入 [#35153](https://github.com/vllm-project/vllm/pull/35153)，SharedFusedMoE 移除 [#35782](https://github.com/vllm-project/vllm/pull/35782)
- DefaultMoERunner 拆分/合并 [#35326](https://github.com/vllm-project/vllm/pull/35326) [#40560](https://github.com/vllm-project/vllm/pull/40560)
- MoE LoRA 重构 [#40338](https://github.com/vllm-project/vllm/pull/40338)，MoE DP chunking 移除 [#39107](https://github.com/vllm-project/vllm/pull/39107)

---

### 🦙 llama.cpp（ggml-org）— b8951 / b8952 / b8953

| Tag | 时间 | 内容 |
|-----|------|------|
| [b8953](https://github.com/ggml-org/llama.cpp/releases/tag/b8953) | 04-28 | **WebGPU：Q1_0 量化支持**，GGML WebGPU 后端矩阵乘法补齐 |
| [b8952](https://github.com/ggml-org/llama.cpp/releases/tag/b8952) | 04-27 | server：router 支持 forward form-data 请求 |
| [b8951](https://github.com/ggml-org/llama.cpp/releases/tag/b8951) | 04-27 | **i-quants 快速 mat-vec kernel** [#22344](https://github.com/ggml-org/llama.cpp/pull/22344)，加速整数量化推理 |

---

## 工程启发

1. **2-bit KV Cache 是 2026 上半年最值得关注的方向之一**。vLLM TurboQuant 的 4× KV 容量意味着在同等显存下可支撑 4 倍 context length 或 batch size，对长上下文推理和批处理场景的工程收益极高。建议跟踪 FlashAttention / PagedAttention 生态中其他 KV 压缩方案的进展（如 llama.cpp 社区是否有对标方案）。

2. **在线量化前端统一是工程成熟信号**。vLLM 将 experts_int8、MXFP8、FP8 等多条量化路径收敛到统一前端，减少了后续维护成本和用户配置复杂度。这个模式在自研推理框架的场景中值得借鉴：先单点突破，再统一接口。

3. **vLLM IR 骨架启动，标志着推理框架进入「IR 时代」**。与 PyTorch 2 的 Dynamo/Inductor 生态对齐后，vLLM 有望实现更灵活的多硬件后端算子调度。这对 CUDA 之外的硬件（AMD、Intel、Apple Silicon）是重大利好。

4. **CUDA 13.0 + PyTorch 2.11 + Transformers v5 三件套升级**意味着社区已进入新一轮依赖链升级周期。如果你的推理部署环境还在 CUDA 12.x，现在是评估升级窗口的合适时机——但要注意 vLLM 明确建议 `--torch-backend=cu129` 来兼容 CUDA 12.9。

---

## 明日跟踪建议

- 🔭 vLLM v0.20.0 main 分支已领先 release 30 commits，关注是否有 hotfix 或 v0.20.1 point release。
- 🧪 **DeepSeek V4 的 vLLM 适配仍在快速迭代中**（DSML leak fix、MTP fix 已入），关注后续多节点 TP/EP 配置指南是否成熟。
- 🖥️ llama.cpp 的 WebGPU 支持刚刚起步（目前仅 Q1_0），跟踪后续 Q4_0/K-quant/FP16 在 WebGPU 上的推进节奏。
- 📊 关注社区对 TurboQuant 2-bit KV 的实际吞吐/精度 benchmark 报告。
- 🔍 SGLang 社区已静默近 3 周（上次 release v0.5.10 在 04-06），关注是否有大版本在酝酿中。
