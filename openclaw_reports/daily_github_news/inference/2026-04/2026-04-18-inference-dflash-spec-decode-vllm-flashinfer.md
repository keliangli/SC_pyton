---
title: "GitHub 大模型推理日报（2026-04-18）- DFlash投机解码+vLLM v0.19.1+FlashInfer v0.6.8"
date: 2026-04-18
track: 大模型推理
slug: dflash-spec-decode-vllm-flashinfer
source_report: /home/li/.openclaw/workspace/reports/github_inference_news_2026-04-18.md
repo_path: openclaw_reports/daily_github_news/inference/2026-04/2026-04-18-inference-dflash-spec-decode-vllm-flashinfer.md
generated_by: openclaw
---

# GitHub 大模型推理技术日报 — 2026-04-18

## 今日要点

1. **vLLM v0.19.1 正式发布**（今日），补丁版本升级 Transformers 至 v5.5.4，修复 Gemma4 流式工具调用 Bug，新增 Gemma4 Eagle3 投机解码支持与 MoE 量化支持
2. **DFlash（Block Diffusion for Flash Speculative Decoding）冲上 GitHub Trending**，287 stars/day，已原生集成 vLLM nightly + SGLang，支持 10+ 主流模型
3. **llama.cpp 连发 10+ 构建**，含 CUDA Graph LRU 淘汰、Gemma4 模型检测、Hexagon HMX matmul 优化、OpenCL Adreno q8_0 重构
4. **FlashInfer v0.6.8 发布**，新增 CuTe-DSL MLA decode 内核、NVFP4 量化、MXFP4 group GEMM 支持（GeForce/Spark）
5. **SGLang v0.5.10 持续发酵**（4月6日发布，近期热度高），Piecewise CUDA Graph 默认启用、Elastic EP、DFlash 投机解码、Flash Attention 4 等重磅特性

---

## 项目速递

### 1. vLLM v0.19.1
- **链接**: https://github.com/vllm-project/vllm/releases/tag/v0.19.1
- **发布日期**: 2026-04-18
- **核心更新**:
  - 升级 Transformers 至 v5.5.4
  - Gemma4 流式 tool call 修复（HTML 重复 / JSON 损坏 / split boolean-number）
  - **新增 Gemma4 Eagle3 投机解码支持**（#39450）
  - Gemma4 MoE 量化支持（#39045）
  - Gemma4 LoRA 加载修复
  - Kimi-K2.5 media_placeholder_token_id 修复

### 2. vLLM v0.19.0（回顾，4月3日发布）
- **链接**: https://github.com/vllm-project/vllm/releases/tag/v0.19.0
- **核心更新**（448 commits / 197 contributors）:
  - **零气泡异步调度 + 投机解码**：大幅提升吞吐
  - **通用 CPU KV Cache Offloading**：可插拔 CachePolicy + 块级抢占
  - **NVIDIA B300/GB300 (SM 10.3) 支持**：Allreduce fusion 默认开启
  - **ViT Full CUDA Graph**：视觉编码器开销大幅降低
  - **DBO 通用化**：双批次重叠扩展到通用模型
  - FlashInfer sparse MLA 成为 FP8 KV cache 默认后端
  - SM120 CUTLASS blockwise FP8 GEMM 优化
  - ROCm 7.2.1 + DeepEP all2all + AITER persistent MLA

### 3. DFlash — Block Diffusion for Flash Speculative Decoding
- **链接**: https://github.com/z-lab/dflash
- **热度**: 1,830 stars（287 stars today），GitHub Trending
- **核心**: 用 Block Diffusion 模型替代传统小模型做投机解码 draft，支持并行高质量 drafting
- **已适配模型**: Qwen3.5-4B/9B/27B/35B-A3B, Qwen3-4B/8B, Kimi-K2.5, Qwen3-Coder, gpt-oss-20b/120b, LLaMA3.1-8B 等
- **后端支持**: vLLM（nightly）、SGLang、Transformers、MLX（Apple Silicon）
- **论文**: arXiv:2602.06036
- **亮点**: 已获 vLLM + SGLang 官方集成支持（NVIDIA @benchislett / Modal Labs @dcw02 @gongy）

### 4. llama.cpp b8824–b8833（4月17日连发）
- **链接**: https://github.com/ggml-org/llama.cpp/releases/tag/b8833
- **关键更新**:
  - **b8832**: CUDA Graph LRU 淘汰策略（#21611）— 用 LRU 替换 ring-buffer，支持 128 graph 容量
  - **b8828**: Gemma4 模型类型检测（#22027）
  - **b8827**: OpenCL q8_0 mul_mat 重构优化（Adreno GPU）
  - **b8824**: Hexagon HMX matmul 优化
  - **b8833**: WebGPU FlashAttention 重构与精度修复

### 5. FlashInfer v0.6.8
- **链接**: https://github.com/flashinfer-ai/flashinfer/releases/tag/v0.6.8
- **发布日期**: 2026-04-16
- **核心更新**:
  - CuTe-DSL MLA decode 内核（Blackwell 优化）
  - NVFP4 量化后端（CuTe-DSL）
  - MXFP4/NVFP4 group GEMM 支持（GeForce 和 Spark 平台）
  - GDN non-contiguous state 解码支持
  - TRT-LLM FP4 block scale MoE int32 overflow 修复（EP32+）
  - cutlass-dsl 升级至 >=4.4.2

### 6. SGLang v0.5.10（4月6日发布，持续关注）
- **链接**: https://github.com/sgl-project/sglang/releases/tag/v0.5.10
- **核心更新**:
  - **Piecewise CUDA Graph 默认启用**
  - **Elastic EP**：DeepSeek MoE 部分故障容错
  - **GPU Staging Buffer**：PD 分离部署 RDMA 请求减少 ~1000x
  - **HiSparse 稀疏注意力**：长上下文推理优化
  - **FlashInfer MXFP8 内核**：GEMM + MoE 混合精度
  - **Flash Attention 4 官方库**：Blackwell GPU 支持
  - **DeepSeek V3.2 / GLM-5 专用优化**：TRT-LLM DSA 内核、IndexCache 10%+ 吞吐提升
  - **Qwen3.5 GDN/KDA 优化**：Triton 内核 + CuTeDSL
  - **LoRA for MoE**：JIT alignment + fused Triton + TP
  - **Native MLX Backend**：Apple Silicon 原生推理
  - **Prefill Context Parallel (MHA)**：Qwen3 MoE 长序列并行

---

## 工程启发

1. **投机解码进入 Block Diffusion 时代**：DFlash 用扩散模型替代小 LM 做 draft，在 SGLang/vLLM 双引擎同时落地，这是投机解码路径的重大变化。值得评估 DFlash 在自用模型上的加速效果。
2. **CUDA Graph 管理走向 LRU 淘汰**：llama.cpp 引入 LRU 替代 ring-buffer 管理 CUDA Graph，上限扩到 128。这对多 batch / 多模型场景的 Graph 内存管理有参考价值。
3. **CPU KV Cache Offloading 成为标配**：vLLM v0.19.0 引入通用 offloading + 可插拔 CachePolicy，SGLang 也有类似 PD 分离方案。长上下文场景下 offloading 策略值得深入研究。
4. **NVFP4/MXFP4 量化加速落地**：FlashInfer、vLLM、SGLang 都在推进 NVFP4/MXFP4 支持，Blackwell (SM100/SM120) 上 blockwise FP8 GEMM 和 NVFP4 GEMM 优化密集。如果目标平台包含 B200/B300，需要跟进量化对齐。
5. **Elastic EP 为 MoE 大规模部署提供容错**：SGLang 的 Elastic NIXL-EP 让 DeepSeek MoE 在单 GPU 故障时自动重分布专家权重继续服务，生产环境价值极高。

---

## 明日跟踪建议

1. **vLLM v0.19.0 详细性能数据**：关注零气泡调度 + 投机解码的端到端吞吐/延迟 benchmark
2. **DFlash 在 Qwen3.5-27B + vLLM nightly 上的实际加速比**：官方 benchmark 数据待出
3. **FlashInfer CuTe-DSL MLA decode kernel 在 Blackwell 上的性能**：对比 FA3/FA4 的 decode 延迟
4. **llama.cpp CUDA Graph LRU 淘汰**的内存节省与命中率数据
5. **SGLang v0.5.11 动向**：v0.5.10 已两周，关注是否有新 release 或 DFlash spec v2 稳定化进展
