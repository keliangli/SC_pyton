# GitHub 大模型推理日报（2026-05-08）

> 抓取时间：2026-05-08 14:50 CST | 覆盖范围：过去 24-96h 主要 release/commit

---

## 一、今日要点

| # | 要点 | 重要性 |
|---|------|--------|
| 1 | **TensorRT-LLM v1.3.0rc14** 发布：Qwen3.5 MoE 路由 + NVFP4 权重加载 + Mamba 混合前缀缓存 + 解耦服务 KV 感知路由 | ⭐⭐⭐ |
| 2 | **FlashInfer v0.6.11** 预发布：DiT 导向内核 + FMHA-v2 HND/NHD 分页 KV 布局 + TRT-LLM-gen 优化 | ⭐⭐⭐ |
| 3 | **llama.cpp b9070** 发布：OpenCL Q4_0 MoE GEMM for Adreno，MoE 推理首次落地高通移动端 | ⭐⭐ |
| 4 | **kekzl/imp** 新项目曝光：C++/CUDA 推理引擎，专为 Blackwell (RTX 5090) 优化 | ⭐⭐ |
| 5 | **SGLang v0.5.11** 上线：CUDA 13 + Torch 2.11、Spec V2 默认、Decode Radix Cache 解耦 | ⭐⭐ |

---

## 二、项目速递

### 1. NVIDIA/TensorRT-LLM → v1.3.0rc14（2026-05-07）

🔗 https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc14

**核心更新：**

- **模型支持**：
  - Mamba 混合模型前缀缓存（Qwen3.5、Nemotron Super V3）— [#12185](https://github.com/NVIDIA/TensorRT-LLM/pull/12185)
  - Qwen3.5 自定义 MoE 路由 + dense/NVFP4 权重加载修复 — [#13433](https://github.com/NVIDIA/TensorRT-LLM/pull/13433), [#13090](https://github.com/NVIDIA/TensorRT-LLM/pull/13090), [#13716](https://github.com/NVIDIA/TensorRT-LLM/pull/13716)
  - Nemotron GEMM 调优 + 多模态 placeholder 扩展 — [#13160](https://github.com/NVIDIA/TensorRT-LLM/pull/13160)
  - Wan 2.2 5B TI2V 支持 — [#13256](https://github.com/NVIDIA/TensorRT-LLM/pull/13256)

- **API**：
  - `llm.encode()` 快速路径支持 encoder-only 模型 — [#12801](https://github.com/NVIDIA/TensorRT-LLM/pull/12801)
  - AGSI middleware 支持 Serve — [#13378](https://github.com/NVIDIA/TensorRT-LLM/pull/13378)
  - InflightBatchingStats 每 iteration 请求聚合计数器 — [#13199](https://github.com/NVIDIA/TensorRT-LLM/pull/13199)

- **Feature / 性能**：
  - 解耦服务改进：gen-first ADP、KV 感知命中率门控 + 公平共享上限 — [#13112](https://github.com/NVIDIA/TensorRT-LLM/pull/13112), [#13198](https://github.com/NVIDIA/TensorRT-LLM/pull/13198)
  - VisualGen 服务优化：快速 PNG 压缩、多节点 diffusion worker、非连续多模态 chunked prefill、Attention2D 序列并行 — [#13074](https://github.com/NVIDIA/TensorRT-LLM/pull/13074), [#12943](https://github.com/NVIDIA/TensorRT-LLM/pull/12943)
  - 内核性能：GEMM-to-allreduce 注册缓冲、CuteDSL bf16 dense GEMM、sparse-attention GVR Top-K、fused add-norm-FP8 量化、TF32 DSA GEMM、sampler 优化 — 多个 PR

### 2. flashinfer-ai/flashinfer → v0.6.11（2026-05-07, pre-release）

🔗 https://github.com/flashinfer-ai/flashinfer/releases/tag/v0.6.11

**核心更新：**

- **DiT 导向内核**：Qk (Bmm1) 类型可重解释为 Int8 或 BFloat16 — [#2711](https://github.com/flashinfer-ai/flashinfer/pull/2711)
- **FMHA-v2**：支持 HND 和 NHD 分页 KV cache 布局 + 条件 stride 处理 — [#2799](https://github.com/flashinfer-ai/flashinfer/pull/2799)
- **TRT-LLM-gen Per-token 优化**（PR 被截断，推测为 per-token 级别的 TRT-LLM kernel 生成改进）
- **CuteDSL MoE**：修复 tile_size=256 gemm2 tactic 枚举 — [#3171](https://github.com/flashinfer-ai/flashinfer/pull/3171)
- **构建修复**：git submodule update 加入 build_backend.py — [#3190](https://github.com/flashinfer-ai/flashinfer/pull/3190)

### 3. ggml-org/llama.cpp → b9070（2026-05-08）

🔗 https://github.com/ggml-org/llama.cpp/releases/tag/b9070

**核心更新：**

- **OpenCL Q4_0 MoE GEMM for Adreno**：首次在 Qualcomm Adreno GPU 上实现 MoE 模型的 Q4_0 量化 GEMM — [#22731](https://github.com/ggml-org/llama.cpp/pull/22731)
- 标志着 llama.cpp MoE 推理能力从 CUDA/Vulkan/Metal 扩展到移动端 GPU

### 4. kekzl/imp（新项目）

🔗 https://github.com/kekzl/imp

- **定位**：高性能 LLM 推理引擎，C++/CUDA 实现，**专为 NVIDIA Blackwell GPU (RTX 5090) 优化**
- 包含完整的 cmake 构建系统、benchmark 框架、docs、测试
- 使用 `.claude/skills` 目录，说明项目已接入 AI 辅助开发
- 值得持续跟踪 Blackwell 架构专用优化思路

### 5. sgl-project/sglang → v0.5.11（2026-05-05）

🔗 https://github.com/sgl-project/sglang/releases/tag/v0.5.11

**核心更新：**

- **CUDA 13 + Torch 2.11**：全面升级构建矩阵，解锁新内核 — [#21247](https://github.com/sgl-project/sglang/pull/21247)
- **Speculative Decoding V2 默认启用**：overlap scheduling 隐藏 CPU 开销，EAGLE/MTP/DFLASH 路径 CPU 成本显著降低 — [#21062](https://github.com/sgl-project/sglang/pull/21062)
- **Decode Radix Cache for PD Disaggregation**：Decode 侧前缀缓存在 prefill/decode 解耦下可用，恢复 radix-cache 命中率 — [#19746](https://github.com/sgl-project/sglang/pull/19746)
- **新模型**：Gemma 4, GLM-5.1, Qwen3.6, MiMo-V2.5/V2.5-Pro, Ling-2.6-Flash, Mistral Medium 3.5, Kimi-K2.6

### 6. vllm-project/vllm → v0.20.1（2026-05-04）

🔗 https://github.com/vllm-project/vllm/releases/tag/v0.20.1

**核心更新（DeepSeek V4 稳定化）：**

- Multi-stream pre-attention GEMM — [#41061](https://github.com/vllm-project/vllm/pull/41061)
- BF16/MXFP8 all-to-all for FlashInfer one-sided communication — [#40960](https://github.com/vllm-project/vllm/pull/40960)
- PTX cvt 指令加速 FP32→FP4 转换 — [#41015](https://github.com/vllm-project/vllm/pull/41015)
- 集成 tile kernels (head_compute_mix_kernel) 优化 head 计算 — [#41255](https://github.com/vllm-project/vllm/pull/41255)
- 修复 persistent topk cooperative deadlock (TopK=1024) — [#41189](https://github.com/vllm-project/vllm/pull/41189)

---

## 三、工程启发

1. **MoE 路由优化成为主战场**：TensorRT-LLM 为 Qwen3.5 定制 MoE routing，FlashInfer 修复 CuteDSL MoE tile tactic，vLLM 修 TopK=1024 死锁——三大框架同时聚焦 MoE，说明 MoE 部署仍是推理工程核心挑战。

2. **Blackwell 专用优化起步**：kekzl/imp 专为 RTX 5090 构建，TensorRT-LLM 加入 TF32 DSA GEMM 和 NVFP4 支持，CUDA 13 成为主流——Blackwell 架构的推理优化窗口已经打开。

3. **解耦服务 (Disaggregated Serving) 持续演进**：TensorRT-LLM 的 gen-first ADP + KV 感知门控、SGLang 的 Decode Radix Cache for PD——生产环境下 prefill/decode 分离的工程细节在快速收敛。

4. **FlashInfer DiT 内核信号**：DiT (Diffusion Transformer) 导向内核进入 FlashInfer，意味着注意力内核不再只服务 LLM decode，视频生成推理的 kernel 复用正在发生。

5. **移动端推理扩展**：llama.cpp OpenCL Adreno MoE GEMM 让 MoE 模型在手机端 GPU 上可用，边缘推理的模型覆盖面扩大。

---

## 四、明日跟踪建议

| 优先级 | 跟踪项 | 原因 |
|--------|--------|------|
| P0 | TensorRT-LLM v1.3.0 正式版 | rc14 已包含大量 MoE + 解耦服务特性，正式版可能本周发布 |
| P0 | kekzl/imp Blackwell 内核实现 | 首个专门面向 Blackwell 的开源推理引擎，跟踪其 GEMM/attention kernel 设计 |
| P1 | FlashInfer v0.6.11 正式版 | 当前为 pre-release，关注 DiT 内核 + HND/NHD KV cache 稳定性 |
| P1 | vLLM DeepSeek V4 后续 patch | v0.20.1 仍有多项 TopK/MegaMoE 问题待修 |
| P2 | SGLang Spec V2 生产反馈 | Spec V2 默认启用后，长上下文场景的延迟/吞吐实测数据 |

---

*本报告由 OpenClaw 自动抓取生成，数据来源：GitHub Releases 页面*
