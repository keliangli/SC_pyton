# GitHub 大模型推理技术日报 — 2026-05-03

> 数据窗口：2026-05-02 14:50 ~ 2026-05-03 14:50 (Asia/Shanghai)
> 数据源：GitHub REST API（releases + commits）

---

## 今日要点

| # | 要点 | 重要度 |
|---|------|--------|
| 1 | **llama.cpp b9010 发布**：修复多 GPU PCI bus ID 去重 OOM，新增 CUDA 13.1 / openEuler 910b ACL Graph 等平台支持 | 🔴 高 |
| 2 | **vLLM 新增 Humming MXFP4 MoE 量化后端**（#41083），蚂蚁集团贡献，面向 MoE 模型的低精度推理 | 🔴 高 |
| 3 | **SGLang 升级 Torch 2.11.0**（#21247）并新增 **LoRADrainer** 优化 P99 TTFT（#17913） | 🟡 中 |
| 4 | **TensorRT-LLM 修复 V2 KV cache extra_tokens 问题**（#13619），优化 Sliding Window Attention radix tree（#13346） | 🟡 中 |
| 5 | **llama.cpp OpenCL Adreno MoE MxFP4 优化**（#22301），移动端推理加速 | 🟡 中 |
| 6 | **vLLM 持续迭代 DeepSeek V4 支持**：multi-stream GEMM token threshold 调优（#41526）、MegaMoE + Pure TP 守卫（#41522） | 🟡 中 |

---

## 项目速递

### 1. llama.cpp — b9010
- **发布时间**：2026-05-02 22:08 UTC（05-03 06:08 CST）
- **Release 链接**：https://github.com/ggml-org/llama.cpp/releases/tag/b9010
- **核心变更**：
  - 修复 CUDA 设备 PCI bus ID 去重导致多 GPU 场景 OOM 的问题（#22533）
  - `server: avoid checkpoint data host copies`（#22558）— 减少 checkpoint 加载时的 host 内存拷贝
  - `ggml-virtgpu: fix circular dependency in headers`（#22557）
  - `opencl: Adreno optimization for MoE - MxFP4`（#22301）— Adreno GPU 上 MoE 推理 + MxFP4 量化优化
  - `convert: disable uint types`（#18908）
- **平台扩展**：新增 CUDA 13.1 Windows 构建、openEuler 310p/910b + ACL Graph 构建、HIP Radeon Windows 构建

### 2. vLLM — post-v0.20.0 开发主线
- **最新 Release**：v0.20.0（2026-04-27），752 commits / 320 contributors
- **Release 链接**：https://github.com/vllm-project/vllm/releases/tag/v0.20.0
- **v0.20.0 核心亮点**：
  - DeepSeek V4 初始支持
  - CUDA 13.0 成为默认构建
  - PyTorch 2.11 + Python 3.14 + Transformers v5
  - FlashAttention 4 默认 MLA prefill 后端
  - TurboQuant 2-bit KV cache（4× 容量提升）
  - 在线量化前端（统一 FP8/MXFP8/experts_int8）
  - vLLM IR 初始骨架（rms_norm op + OOT kernel 导入）
  - Model Runner V2：Eagle prefill 全 CUDA graph、fused rejection-sample kernels
  - MoE 大规模重构（Oracle Flow、SharedExperts class、MoE LoRA）
  - 性能：fused RMS norm batch invariant 优化 → 2.1% E2E 延迟降低
- **过去 24h 新增 commits**：
  - `[Quantization] add humming mxfp4 moe backend`（#41083）— 蚂蚁集团贡献的 MoE 量化后端
  - `[DSv4] Tune VLLM_MULTI_STREAM_GEMM_TOKEN_THRESHOLD`（#41526）
  - `[DSV4] Guard megamoe flag with Pure TP`（#41522）
  - `[MRV2] Add shutdown() method`（#41297）— Woosuk Kwon
  - `[Build] Switch CUDA 13.0 wheel builds to PyTorch manylinux_2_28 base`（#41416）

### 3. SGLang — v0.5.10.post1+
- **最新 Release**：v0.5.10.post1（2026-04-09），仅升级 FlashInfer
- **Release 链接**：https://github.com/sgl-project/sglang/releases/tag/v0.5.10.post1
- **过去 24h 新增 commits**：
  - `[Feature] add LoRADrainer to address high P99 TTFT`（#17913）— 通过 LoRA 训练优化 P99 首 token 延迟
  - `[Dependency] Upgrade to Torch 2.11.0`（#21247）— 与 vLLM 对齐
  - `Update kernel installation instructions after shifting default cuda to 13`（#24181）
  - `[gateway] Align /v1/loads and /model_info with sglang server; drop dead /rerank`（#24167）
  - `throw ValueError for DoRA adapters`（#22125）

### 4. TensorRT-LLM — v1.3.0rc13
- **最新 Release**：v1.3.0rc13（2026-04-29，pre-release）
- **Release 链接**：https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc13
- **v1.3.0rc13 核心亮点**：
  - Nemotron 3 Nano Omni 初始优化
  - GLM-4.7 / GLM-5 tool parser
  - DeepSeek-V3.2 / V3-Lite Blackwell + SM100 性能优化
  - VisualGen Cache-DiT + 统一 cache accelerator
  - Sparse MQA/GQA attention + 新 sharding 基础设施
  - EAGLE3 动态树投机解码恢复
  - FP4 残差量化、SageAttention kernels 更新
  - 大量 KV cache / scheduler 正确性修复
- **过去 24h 新增 commits**：
  - `[fix] Fix extra_tokens in V2 KV cache`（#13619）
  - `[feat] Clean up SWA work-arounds with the new radix search`（#13346）
  - `[fix] write per-rank torch profile traces`（#13536）

### 5. FlashInfer — nightly v0.6.9-20260501
- **最新构建**：nightly-v0.6.9-20260501（2026-05-01）
- **Release 链接**：https://github.com/flashinfer-ai/flashinfer/releases/tag/nightly-v0.6.9-20260501
- 说明：自动 nightly 构建，为 vLLM / SGLang 等项目提供底层 attention kernel

### 6. DeepSpeed — v0.18.9
- **最新 Release**：v0.18.9（2026-03-30）
- **Release 链接**：https://github.com/deepspeedai/DeepSpeed/releases/tag/v0.18.9
- **核心变更**：
  - AutoSP 合并入 DeepSpeed（#7860）— 自动序列并行
  - Muon Optimizer 支持 ZeRO Stage 3（#7919）
  - HuggingFace tp_plan 支持 AutoTP（#7901）
  - Universal Checkpoint for AutoTP（#7908）
  - Triton autotune cache NFS 路径修复

### 7. LMDeploy — v0.12.3
- **最新 Release**：v0.12.3（2026-04-08）
- **Release 链接**：https://github.com/InternLM/lmdeploy/releases/tag/v0.12.3
- **核心变更**：视频输入支持、TurboMind compressed-tensors gs32 实现、Qwen3.5 支持

---

## 工程启发

1. **MXFP4 量化成 MoE 推理新焦点**：vLLM 的 Humming MXFP4 MoE 后端（蚂蚁）和 llama.cpp 的 OpenCL Adreno MxFP4 优化都指向同一趋势——MoE 模型的 sub-8bit 量化正成为推理成本优化的关键路径。值得关注的是两种实现路径：vLLM 在 GPU 端做 kernel-level 量化，llama.cpp 在移动端 Adreno GPU 做CL kernel 优化。

2. **Torch 2.11 成推理框架统一基线**：vLLM v0.20.0 和 SGLang 都已升级到 Torch 2.11，CUDA 13.0 成为默认构建。这对下游用户意味着：升级 torch 是硬性依赖变更，需要同步更新 CUDA 驱动。

3. **KV Cache 正确性问题持续暴露**：TensorRT-LLM 修复 V2 KV cache extra_tokens 问题、vLLM 在 v0.20.0 修复多个 KV cache/scheduler 正确性 bug。说明 KV cache 管理仍是工程难点，特别是在 chunked prefill + sliding window + speculative decoding 组合场景下。

4. **vLLM IR 的战略意义**：vLLM IR skeleton 的引入（rms_norm op + OOT kernel import hooks）标志着 vLLM 开始构建自己的 IR 层，未来可能支持跨硬件 kernel 代码生成和优化，类似 XLA/Torch-Inductor 的思路但更轻量。

5. **LoRA 在线训练优化 TTFT**：SGLang 的 LoRADrainer 是一个有趣的方向——用 LoRA 微调来优化 serving 路径的 P99 首 token 延迟，将模型适配从离线搬到在线。

---

## 明日跟踪建议

| 优先级 | 项目 | 关注点 |
|--------|------|--------|
| P0 | vLLM | Humming MXFP4 MoE 后端性能数据；DeepSeek V4 支持稳定性 |
| P0 | llama.cpp | b9010 后续 CUDA 13.1 生态适配；MoE + MxFP4 在更多平台的扩散 |
| P1 | SGLang | v0.5.11 或 v0.6.0 是否发布；LoRADrainer 技术细节 |
| P1 | TensorRT-LLM | v1.3.0 正式版发布时间；EAGLE3 + sparse attention 稳定性 |
| P2 | FlashInfer | v0.6.9 正式版；FA4 kernel 更新对 vLLM/SGLang 的下游影响 |
| P2 | DeepSpeed | AutoSP 实际推理场景表现 |

---

*报告生成时间：2026-05-03 14:50 CST*
