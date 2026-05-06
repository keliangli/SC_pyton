# GitHub 大模型推理日报（2026-05-06）

> 抓取时间：2026-05-06 14:50 CST / 06:50 UTC
> 数据源：GitHub API（releases + search）
> 覆盖窗口：2026-05-04 ~ 2026-05-06

---

## 📌 今日要点

1. **SGLang v0.5.11 正式发布**：CUDA 13 + Torch 2.11 全面升级，Speculative Decoding V2 成为默认策略，PD 分离部署新增 Decode Radix Cache，7+ 新模型（Gemma 4 / GLM-5.1 / Qwen3.6 / Kimi-K2.6 等）Day-0 支持——本周期最重磅 release。
2. **vLLM v0.20.1 释出**：聚焦 DeepSeek V4 稳定性与性能——multi-stream pre-attention GEMM、PTX cvt FP32→FP4 加速、BF16/MXFP8 all-to-all 通信、tile kernel head compute 优化。
3. **FlashInfer v0.6.10 发布**：SM90 MoE backend（MXFP4xBF16/INT4xFP8）优化、CuTe DSL FMHA prefill 集成、DCP All-to-All kernel、NVFP4 KV 支持、head_dim=512 trtllm attention、all-gather matmul——推理 kernel 库全面扩容。
4. **Ollama v0.23.1**：Gemma 4 MTP speculative decoding 支持 Mac MLX runner，31B coding 任务 >2x 加速。
5. **llama.cpp b9038**（今日发布）：OpenCL `CL_DEVICE_GLOBAL_MEM_SIZE` 用于 `--fit` 模式显存估算。
6. **Liger-Kernel v0.8.0**（4/30，仍值得关注）：LigerExperts MoE fused kernel 实现 Qwen3-30B-A3B 8.24× tokens/sec 加速；新增 Claude Code Skills 辅助 Triton kernel 开发；Qwen3.5 / Nemotron / Gemma 4 等新模型 + 昇腾 NPU 后端。

---

## 🚀 项目速递

### 1. SGLang v0.5.11（2026-05-05）

**链接**：[https://github.com/sgl-project/sglang/releases/tag/v0.5.11](https://github.com/sgl-project/sglang/releases/tag/v0.5.11)

**核心更新**：
- 🔧 **CUDA 13 + Torch 2.11**：默认 CUDA 版本升至 13.0，PyTorch 2.9→2.11，解锁新 kernel 路径
- ⚡ **Speculative Decoding V2 默认启用**：overlap scheduling 隐藏 CPU overhead，EAGLE/MTP/DFLASH 路径显著提速
- 🏗️ **Decode Radix Cache for PD Disaggregation**：Prefill/Decode 分离部署下 decode 端前缀缓存恢复，提升长共享前缀 TTFT
- 🆕 **Day-0 新模型**：Gemma 4、GLM-5.1、Qwen3.6、MiMo-V2.5/V2.5-Pro、Ling-2.6-Flash、Mistral Medium 3.5、Kimi-K2.6（含 cookbook）
- 🔥 **DFLASH Speculative Decoding**：社区贡献高吞吐 spec-decode kernel，扩展至多模型 backend + AMD ROCm
- 🧩 **FA3 Kernels 社区贡献**：drop-in FA3 kernels，与 FA4 并列可选高性能方案
- 🎯 **LoRA for DeepSeek-V3 / Kimi-K2**：最大 MLA-based MoE 模型首次支持 LoRA adapter
- ⚙️ **Context Parallel 增强**：all-reduce + RMSNorm fusion；`moe_dp_size=1` 配合任意 `attention_cp_size` 独立调优
- 🔬 **FlashInfer CuteDSL MoE Runner Backend**：标准 FP4 MoE 路径新增 `FlashInferCuteDslMoE` fused layer

### 2. vLLM v0.20.1（2026-05-04）

**链接**：[https://github.com/vllm-project/vllm/releases/tag/v0.20.1](https://github.com/vllm-project/vllm/releases/tag/v0.20.1)

**核心更新（DeepSeek V4 专项）**：
- 🆕 DeepSeek V4 base model support
- ⚡ Multi-stream pre-attention GEMM（#41061），可配置 knob + tuned default threshold
- ⚡ BF16 & MXFP8 all-to-all for FlashInfer one-sided communication
- ⚡ PTX `cvt` instruction：FP32→FP4 转换加速
- ⚡ Integrated tile kernels（`head_compute_mix_kernel`）优化 head computation
- 🐛 修复 persistent topk cooperative deadlock（TopK=1024）、RadixRowState inter-CTA init race
- 🐛 修复 AOT compile cache loading import error、torch inductor error、repeated RoPE cache init
- 🐛 修复 `max_num_batched_tokens` CUDA graph capture、BailingMoE linear layer / MLA RoPE、ROCm Quark W4A8 GPT-OSS

### 3. FlashInfer v0.6.10（2026-05-04）

**链接**：[https://github.com/flashinfer-ai/flashinfer/releases/tag/v0.6.10](https://github.com/flashinfer-ai/flashinfer/releases/tag/v0.6.10)

**核心更新**：
- ⚡ **SM90 MoE backend 优化**：MXFP4xBF16 & INT4xFP8 CUTLASS MoE 性能提升
- 🔬 **CuTe DSL FMHA prefill**：加载 cubin 方式集成 CuTe DSL prefill kernels
- 🔬 **DCP All-to-All kernel**：context-parallel attention reduction 专用
- 🆕 **head_dim=512**：trtllm attention kernels 新增大 head 维度支持
- 🆕 **NVFP4 KV**：prefill 和 batch attention kernels 支持 NVFP4 KV cache
- 🆕 **all-gather matmul**：新增 all-gather matmul kernel
- 🆕 **allreduce / allgather / reducescatter 组合支持**
- 🆕 **FlashInfer trace interface**（`.fi_trace`）
- 🆕 **JAX 调用示例**：通过 jax-tvm-ffi 从 JAX 调用 FlashInfer
- 🔧 CCCL v3.3.2 vendored from GitHub（不再依赖 CTK-bundled copy）
- 🔧 Autotuner：hybrid spacing token buckets + cache-before-synthesize 优化
- 🔧 Blackwell GDN accuracy 修复 + SM100 persistent prefill kernel 物理 SM count
- 🆕 no-bias path for tinygemm_bf16

### 4. Ollama v0.23.1（2026-05-05）

**链接**：[https://github.com/ollama/ollama/releases/tag/v0.23.1](https://github.com/ollama/ollama/releases/tag/v0.23.1)

**核心更新**：
- ⚡ **Gemma 4 MTP speculative decoding**：Mac MLX runner 支持，31B coding 任务 >2x 加速
- 🔧 MLX/MLX-C threading fixes
- 🔧 Go bumped to 1.26

### 5. llama.cpp b9038（2026-05-06）

**链接**：[https://github.com/ggml-org/llama.cpp/releases/tag/b9038](https://github.com/ggml-org/llama.cpp/releases/tag/b9038)

**核心更新**：
- 🔧 OpenCL backend 使用 `CL_DEVICE_GLOBAL_MEM_SIZE` 作为 `--fit` 模式显存估算，改善 OpenCL 设备自动配置精度

### 6. Liger-Kernel v0.8.0（2026-04-30）

**链接**：[https://github.com/linkedin/Liger-Kernel/releases/tag/v0.8.0](https://github.com/linkedin/Liger-Kernel/releases/tag/v0.8.0)

**核心更新**：
- 🚀 **LigerExperts MoE fused kernel**：Triton grouped-GEMM + fused SwiGLU + token aggregation，Qwen3-30B-A3B 达到 **8.24×** tokens/sec
- 🤖 **Claude Code Skills**：`.claude/skills/` 下 3 个 skill——`liger-kernel-dev`（从 PyTorch op 到完整 Triton kernel）、`liger-autopatch`（新模型 monkey-patch 自动生成）、`liger-kernel-perf`（kernel profiling + 变体 benchmark）
- 🆕 新模型：Qwen3.5 MoE/dense/multimodal、Nemotron、Ministral、Gemma 4 dense、Falcon H1
- 🔬 昇腾 NPU backend 支持

---

## 💡 工程启发

1. **DeepSeek V4 成为各框架优先适配对象**：vLLM v0.20.1 整个 patch release 围绕 DeepSeek V4 稳定化；SGLang v0.5.11 LoRA 支持 DeepSeek-V3 MLA。说明 DeepSeek 系列模型（尤其是 MoE 大模型）已成为推理框架的"头号客户"。**启发**：如果你在做 DeepSeek-V3/V4 部署，现在 vLLM + SGLang 的支持已经相当成熟，值得对比两者在 multi-stream GEMM / MXFP8 all-to-all / spec-decoding 路径上的实际吞吐差异。

2. **Speculative Decoding 正在成为"标配"而非"可选"**：SGLang Spec V2 默认开启；Ollama MTP spec-decoding 在 Mac 上已可用；vLLM 也在持续修 spec-decoding 相关 bug。**启发**：工程部署中应将 spec-decoding 作为默认配置而非"高级选项"，重点关注 EAGLE / MTP / DFLASH 三条路径的 latency-throughput tradeoff。

3. **FlashInfer 正在向 Blackwell (SM100) 深度适配**：NVFP4 KV、CuTe DSL FMHA、DCP All-to-All、GDN accuracy fix，都是在为 Blackwell 架构铺路。**启发**：如果你在规划 Blackwell 部署，FlashInfer v0.6.10 是必须跟进的版本；尤其关注 NVFP4 KV cache + DCP all-to-all 在多卡场景下的实际表现。

4. **PD Disaggregation 从"实验性"走向"生产级"**：SGLang decode radix cache + Mooncake incremental transfer + NIXL heterogeneous TP KV transfer，三条传输引擎并行演进。**启发**：PD 分离不再是概念验证阶段，已经有完整的 cache 命率恢复 + 异构 TP 传输方案，可以开始在实际生产环境测试端到端 TTFT/吞吐收益。

5. **Kernel 开发工具链也在加速**：Liger-Kernel 提供 Claude Code Skills 自动生成 Triton kernel；SGLang 社区贡献 FA3 + DFLASH；FlashInfer 的 autotuner hybrid spacing 优化。**启发**：AI-assisted kernel development 正在降低 CUDA/Triton 开发门槛，建议关注 Liger-Kernel 的 skill 模式，可能对你的 CUDA/Triton 学习加速有直接帮助。

---

## 📋 明日跟踪建议

1. **vLLM v0.20.0 完整 changelog**：v0.20.1 是 patch release，v0.20.0 的主线 feature（如 DeepSeek V4 初版支持）值得详细跟进
2. **SGLang DFLASH spec-decoding 实际 benchmark**：与 EAGLE / MTP 在同一硬件上的 throughput/latency 对比数据尚未公开
3. **FlashInfer NVFP4 KV + DCP All-to-All 在 Blackwell 上的实测数据**：目前只有 PR 描述，未见公开 benchmark
4. **llama.cpp b9038 后续 commit**：今日 release 只包含 OpenCL 改进，关注是否有 CUDA/Vulkan/Metal 相关新 commit
5. **TensorRT-LLM v1.3.0 正式版**：rc13 是 prerelease，关注何时发布正式版及 DeepSeek-V3.2 / EAGLE3 动态树 spec-decoding 的最终状态
6. **Ollama v0.23.0 changelog**：v0.23.1 只提到了 MTP，但 v0.23.0 可能包含更多重要 feature