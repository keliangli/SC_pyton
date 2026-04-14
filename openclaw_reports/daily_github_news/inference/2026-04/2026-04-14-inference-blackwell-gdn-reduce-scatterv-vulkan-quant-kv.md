---
title: "Inference Report 2026-04-14"
date: 2026-04-14
track: 大模型推理
slug: blackwell-gdn-reduce-scatterv-vulkan-quant-kv
source_report: /home/li/.openclaw/workspace/reports/github_inference_news_2026-04-14.md
repo_path: openclaw_reports/daily_github_news/inference/2026-04/2026-04-14-inference-blackwell-gdn-reduce-scatterv-vulkan-quant-kv.md
generated_by: openclaw
---

# GitHub 大模型推理日报 — 2026-04-14

> 抓取时间：2026-04-14 14:50 CST | 覆盖范围：GitHub 过去 ~24h 活跃提交 + 近期重大 Release

---

## 📌 今日要点

| # | 要点 | 影响评估 |
|---|------|----------|
| 1 | **FlashInfer 新增 Blackwell GDN prefill kernel**：基于 cutedsl 编写，Qwen3.5 全系列（0.8B~397B）在 B200 上大幅加速，标志着 Blackwell 推理生态进一步成熟 | 🔴 极高 |
| 2 | **SGLang 爆发式更新**（15+ commits/天）：reduce_scatterv 融合通信替代 DP Attention 的 all-reduce + dp_scatter、SiMM 分布式 HiCache 后端、Mooncake 支持 DSA & Mamba 混合模型 | 🔴 极高 |
| 3 | **llama.cpp 一日三更**（b8779 → b8781 → b8783）：Vulkan Flash Attention DP4A 量化 KV cache、DeepSeek v3.2 专用 parser、Gemma4 解析边界修复 | 🟡 高 |
| 4 | **vLLM Eagle SpecDecode prefill CUDA Graph 全覆盖**：将 CUDA graph 扩展到 Eagle prefill 路径，减少 CPU dispatch 开销，多模型/TP/EP 配置均验证 | 🟡 高 |
| 5 | **candle 新增 CUDA MMVQ GGUF 快速解码 kernel**：原生 BF16 输入输出（无需 F32 中转）、on-the-fly Q8_1 量化，HuggingFace Rust 推理栈补齐 CUDA GGUF 解码短板 | 🟡 高 |
| 6 | **xllm（京东）+ rtp-llm（阿里）同步推进国产推理栈**：xllm 新增 Mooncake PD 支持 + tilelang-ascend GDN kernel；rtp-llm 去除 sampler 中的 device sync | 🟡 中高 |

---

## 🚀 项目速递

### 1. FlashInfer — Blackwell GDN Prefill Kernel + FP8 MoE 修复
- **链接**: https://github.com/flashinfer-ai/flashinfer
- **日期**: 2026-04-13 ~ 04-14
- **核心更新**:
  - **Blackwell GDN prefill kernel** (`#3001`)：使用 cutedsl 编写，在 B200 (SM100) 上 Qwen3.5 全系列实测，支持 FLA/Triton 对比加速
  - **Fix silent FP8 per-tensor MoE bug** (`#2882`)：修复 TRT-LLM MoE FP8 non-gated 模型（Nemotron）强制回退到慢路径的问题
  - **MXFP4/MXFP8 SM120 FAST_BUILD 修复** (`04f4c0c`)
  - **MoE alltoall top-k 扩展** (`#3021`)
  - **Blackwell GDN 代码所有者 @qsang-nv** (`#3055`)

### 2. SGLang v0.5.10 — 持续高频更新
- **链接**: https://github.com/sgl-project/sglang
- **日期**: 2026-04-13 ~ 04-14（15+ commits）
- **核心更新**:
  - **reduce_scatterv 融合通信** (`#22642`)：DP Attention + EP 场景下，用单次 `reduce_scatterv` 替代 `all-reduce + dp_scatter`，减少通信开销
  - **SiMM HiCache Storage 后端** (`#18016`)：Scitix In-Memory Middleware，支持 zero-copy page layout + NUMA-aware RDMA
  - **Mooncake 后端支持 DSA & Mamba** (`#21259`)：HiCache + HybridModel 扩展，Mooncake 传输层适配
  - **HiSparse 稀疏注意力** (`#22331`)：decode token usage 日志优化
  - **KV cache pool Prometheus 指标** (`#22726`)：暴露原始 KV cache token 计数
  - **AMD CI 调度优化** (`#22489`)：替换 push trigger 为 scheduled runs + 并行 stage
  - **GB200 nightly pipeline** (`#22733`)：添加 workflow_dispatch + environment gate

### 3. llama.cpp — 一日三版本
- **链接**: https://github.com/ggml-org/llama.cpp
- **日期**: 2026-04-13 ~ 04-14（b8779 → b8781 → b8783）
- **核心更新**:
  - **Vulkan Flash Attention DP4A shader for quantized KV cache** (`#20797`)：使用 integer dot product 进行量化 KV Flash Attention，vulkan 后端量化推理提速
  - **DeepSeek v3.2 专用 parser + "official" template** (`#21785`)
  - **Gemma4 解析边界修复** (`#21760`)
  - **Qwen3-ASR / Qwen3-Omni 支持列表更新** (`#21857`)
  - **下载取消 + 临时文件清理** (`#21813`)
  - **Router mode build_info 暴露** (`#21835`)
  - **CUDA DeviceSegmentedSort immediate mode 限制** (`#21718`)

### 4. vLLM — Eagle CUDA Graph + LMCache MLA 优化
- **链接**: https://github.com/vllm-project/vllm
- **日期**: 2026-04-13 ~ 04-14（10+ commits）
- **核心更新**:
  - **Eagle prefill full CUDA graph** (`#37588`)：将 FULL CUDA graph 扩展到 Eagle prefill 路径，H200 多模型验证（Llama3/Qwen3/Mimo/GLM4.7Flash + TP/EP/DP + Eagle-1/3/MTP）
  - **LMCache MLA 多 worker 优化** (`#38810`)：MLA 启用时 store 请求只发一次，大幅减少 server 端请求数
  - **parse_delta 重构** (`#39446`, `#39728`)：chat completion auto-tool/reasoning/plain streaming 统一到 parse_delta
  - **Gemma4 tool parser 修复** (`#39679`)：修复 bare `null` 被转为字符串 `"null"` 的问题
  - **MinimaxM2ToolParser 缺失 tools 参数修复** (`#39683`)
  - **Pooling buffer-reuse 权重损坏修复** (`#39650`)

### 5. TensorRT-LLM v1.3.0rc11 — 持续打磨
- **链接**: https://github.com/NVIDIA/TensorRT-LLM
- **日期**: 2026-04-13 ~ 04-14（6+ commits）
- **核心更新**:
  - **KV cache manager 统一** (`#10437`)：reuse/non-reuse 路径统一
  - **Qwen3.5 NVFP4 精度测试** (`#13014`)：AutoDeploy 新增 Qwen3.5 NVFP4 量化精度验证
  - **Warmup 编排重构** (`#12407`)
  - **AutoDeploy Model Onboarding Sprint** (`#12708`)
  - **AutoDeploy registry accuracy tests 修复** (`#12942`)

### 6. xllm（京东开源）— Mooncake + Ascend kernel
- **链接**: https://github.com/jd-opensource/xllm
- **日期**: 2026-04-13 ~ 04-14
- **核心更新**:
  - **Mooncake PD push 支持** (`#1246`)：MLU 设备 Mooncake 传输层集成
  - **tilelang-ascend fused_gdn_gating kernel** (`#1267`)：Ascend NPU 上 GDN gating 融合 kernel
  - **FBCache residual 复用修复** (`#1265`)
  - **Server 启动路由简化** (`#1243`)

### 7. rtp-llm（阿里）— Sampler device sync 消除
- **链接**: https://github.com/alibaba/rtp-llm
- **日期**: 2026-04-13 ~ 04-14
- **核心更新**:
  - **Sampler tensor 移至 CUDA**：移除 sampler 中的 device sync，减少 GPU-CPU 同步开销
  - **ROCm graph 后端重构**：支持 ROCm 后端的 graph 捕获

### 8. MNN（阿里）— 多后端优化
- **链接**: https://github.com/alibaba/MNN
- **日期**: 2026-04-13 ~ 04-14
- **核心更新**:
  - **Gemma4 k_eq_v / head_dim 自动检测隔离** (`efdf7c2`)：修复 Gemma4 参数检测冲突
  - **Vulkan persistent state 跨响应复用** (`0bc61dd`)
  - **LinearAttention decode 快速路径** (`#4356`)：L=1 decode 专用优化
  - **CUDA Eagle spec-decode 优化** (`b63c33d`)
  - **KV cache reuse 重构** (`c2df159`)：通过 onClone 统一替代 per-backend 逻辑

### 9. candle（HuggingFace）— CUDA GGUF 快速解码
- **链接**: https://github.com/huggingface/candle
- **日期**: 2026-04-13
- **核心更新**:
  - **Fast CUDA MMVQ GGUF kernel** (`#3463`)：原生 BF16 输入输出（无 F32 中转），on-the-fly Q8_1 量化，per-device scratch workspace 懒分配复用

### 10. zinc — Zig 推理引擎（AMD + Apple Silicon）
- **链接**: https://github.com/zolotukhin/zinc
- **日期**: 2026-04-13 ~ 04-14（⭐310，2026-03 创建）
- **核心更新**:
  - **Gemma 4 MoE Vulkan 支持**：CPU-routed path + sqrt scale + post_ffw_norm（3 个连续提交）

### 11. ollama v0.20.8-rc0
- **链接**: https://github.com/ollama/ollama
- **日期**: 2026-04-14
- **核心更新**:
  - **ROCm 7.2.1 升级** (`#15483`)
  - **Gemma4 nothink renderer 修复 + compiler error 修复** (`#15553`, `#15550`)
  - **MLX mixed-precision quant + capability detection 改进**

### 12. ONNX Runtime — CUDA EP Plugin 资源管理
- **链接**: https://github.com/microsoft/onnxruntime
- **日期**: 2026-04-14
- **核心更新**:
  - **CUDA EP Plugin ResourceAccountant 集成** (`#28028`)：type-erased arithmetic for resource accounting，plugin EP 资源预算管理

---

## 🔧 工程启发

| # | 启发点 | 来源 | 可借鉴方向 |
|---|--------|------|-----------|
| 1 | **reduce_scatterv 融合通信**：将 all-reduce + scatter 两步合为一步，在 DP Attention + EP 场景下直接减少通信量 | SGLang `#22642` | 自研 MoE 推理框架的通信优化可参考此模式 |
| 2 | **Eagle prefill CUDA graph 全覆盖**：不只优化 decode path，prefill 也能 graph 化，CPU dispatch 开销是隐藏瓶颈 | vLLM `#37588` | Speculative decoding 的 prefill 路径应纳入 graph 优化范围 |
| 3 | **Vulkan Flash Attention DP4A 量化 KV**：integer dot product 用于量化 KV flash attention，低精度推理在 GPU 端也能加速 | llama.cpp `#20797` | 非 CUDA 后端（Vulkan/OpenCL）的量化推理优化思路 |
| 4 | **Sampler 去除 device sync**：将 sample 相关 tensor 放在 CUDA 上避免 GPU→CPU 同步 | rtp-llm | 推理框架中每个 device sync 都是延迟热点，逐个消除 |
| 5 | **cutedsl 编写 Blackwell kernel**：FlashInfer 用 cutedsl（非 CUTLASS）为 Blackwell 写 GDN kernel，代表新一代 kernel 开发范式 | FlashInfer `#3001` | Blackwell 专用 kernel 开发可考虑 cutedsl 路线 |
| 6 | **KV cache reuse via onClone**：通过统一的 clone 接口替代 per-backend 逻辑，降低后端适配复杂度 | MNN `c2df159` | 多后端推理框架的 cache 管理设计可参考 |

---

## 📋 明日跟踪建议

| 优先级 | 跟踪项 | 预期 |
|--------|--------|------|
| 🔴 P0 | **FlashInfer Blackwell GDN kernel 性能细节**：等待 PR `#3001` 合并后的完整 benchmark 数据 | Qwen3.5 397B B200 实测数据 |
| 🔴 P0 | **SGLang reduce_scatterv 合并效果**：关注 DP Attention + EP 场景下的实际吞吐提升 | 通信量减半验证 |
| 🟡 P1 | **vLLM Eagle prefill CUDA graph 基准数据**：PR `#37588` Google Sheets 链接中的完整 benchmark | 多模型/TP/EP 配置下的延迟改善 |
| 🟡 P1 | **TensorRT-LLM v1.3.0 正式版**：rc11 之后是否进入 rc12 或直接 release | 新功能锁定期 |
| 🟡 P1 | **xllm tilelang-ascend GDN kernel**：Ascend NPU 上 GDN gating 融合的实测算力表现 | 国产 NPU 推理栈进展 |
| 🔵 P2 | **zinc Gemma4 MoE 完整支持**：Zig 语言推理引擎在 AMD GPU 上的 MoE 推理进展 | 新语言/新硬件推理方案 |

---

*报告生成时间：2026-04-14 14:50 CST | 数据来源：GitHub API (vllm, sglang, llama.cpp, TensorRT-LLM, FlashInfer, MNN, xllm, rtp-llm, candle, zinc, ollama, ONNX Runtime)*
