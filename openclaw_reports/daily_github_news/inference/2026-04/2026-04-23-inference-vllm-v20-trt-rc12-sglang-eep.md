# GitHub 大模型推理日报（2026-04-23）

> 覆盖过去24小时与LLM推理相关的核心进展

---

## 📌 今日要点

| 类别 | 关键进展 |
|------|----------|
| **vLLM** | 发布 v0.20.0 正式版（4月22日晚）及 v0.19.1 补丁版；Transformers v5 升级、Gemma4 全系列修复与 Eagle3 spec-dec 支持 |
| **TensorRT-LLM** | 发布 v1.3.0rc12，含 Qwen3.5 CuteDSL MoE 后端、LoRA+Speculative Decoding 组合支持、生产级 Prometheus 监控上线、对话亲和路由、NVFP4 可调量化+FlashInfer |
| **SGLang** | 发布 v0.5.10，Piecewise CUDA Graph 默认启用、Elastic EP 部分故障容错、GPU Staging Buffer RDMA 优化（~5x TPS 提升）、HiSparse 稀疏注意力、FlashInfer MXFP8 内核 |
| **FlashInfer** | 发布 v0.6.8，CuTe-DSL NVFP4 量化后端、MLA decode 内核、MXFP8 GEMM SM120 支持、GDN MTP decode 内核优化 |
| **llama.cpp** | 过去24h密集提交（10+ commits on Apr 22），gpt-oss MXFP4 原生支持持续迭代 |
| **TGI** | 项目已归档（2026-03-21），v3.3.7 为最终版 |

---

## 🚀 项目速递

### 1. vLLM — v0.20.0 正式版 + v0.19.1 补丁

**v0.20.0** 于 2026-04-22 23:15 UTC 发布（前有 rc1 于 22日 09:00），标志着 v0.19 系列的成熟。

**v0.19.1 补丁（同步发布）：**

| PR | 标题 | 技术价值 |
|----|------|----------|
| [#30566](https://github.com/vllm-project/vllm/pull/30566) | Update to Transformers v5 | 核心依赖升级至 Transformers 5，解锁最新模型架构 |
| [#38992](https://github.com/vllm-project/vllm/pull/38992) | Fix invalid JSON in Gemma4 streaming tool calls | 修复 Gemma4 流式工具调用中的 JSON 解析错误 |
| [#38909](https://github.com/vllm-project/vllm/pull/38909) | Fix Gemma4 streaming HTML duplication after tool calls | 修复流式输出中 HTML 重复问题 |
| [#39114](https://github.com/vllm-project/vllm/pull/39114) | Fix Gemma4 streaming tool call corruption for split boolean/number | 修复分割值导致的工具调用数据损坏 |
| [#39045](https://github.com/vllm-project/vllm/pull/39045) | Gemma4 quantized MoE support | Gemma4 MoE 量化推理支持 |
| [#39450](https://github.com/vllm-project/vllm/pull/39450) | Add Gemma4 Eagle3 support | Eagle3 投推测解码支持 Gemma4，推理加速关键 |
| [#38844](https://github.com/vllm-project/vllm/pull/38844) | Gemma4 LoRA adapter loading fix | 修复 Gemma4 LoRA 加载路径错误 |
| [#39842](https://github.com/vllm-project/vllm/pull/39842) | Fix Gemma4 token repetition by dynamic BOS injection | 动态注入 BOS token 解决重复生成问题 |

**🔗 Release**: https://github.com/vllm-project/vllm/releases/tag/v0.19.1 | https://github.com/vllm-project/vllm/releases/tag/v0.20.0

---

### 2. TensorRT-LLM — v1.3.0rc12（近期最重要版本）

| Feature | PR | 技术价值 |
|---------|----|----------|
| Qwen3.5 CuteDSL MoE backend | [#12799](https://github.com/NVIDIA/TensorRT-LLM/pull/12799) | CuteDSL 后端支持 Qwen3.5 MoE，新架构内核优化 |
| LoRA + Speculative Decoding 组合 | [#12661](https://github.com/NVIDIA/TensorRT-LLM/pull/12661) | 首次支持 LoRA 适配器与投机解码同时使用 |
| FP8 LoRA weight loading | [#12848](https://github.com/NVIDIA/TensorRT-LLM/pull/12848) | 支持 FP8 精度 LoRA 权重加载 |
| Conversation-affinity routing (disagg) | [#12526](https://github.com/NVIDIA/TensorRT-LLM/pull/12526) | 分离式服务中的对话亲和路由，减少 KV 迁移 |
| Production Prometheus metrics | [#12545](https://github.com/NVIDIA/TensorRT-LLM/pull/12545) | 生产级监控指标（迭代统计、配置、token计数、阶段直方图） |
| Block reuse + overlap scheduler | [#12816](https://github.com/NVIDIA/TensorRT-LLM/pull/12816) | overlap 调度器支持 block reuse，内存效率提升 |
| Tunable NVFP4 quantization + FlashInfer | [#12126](https://github.com/NVIDIA/TensorRT-LLM/pull/12126) | 可调 NVFP4 量化方案 + FlashInfer 后端双路径 |
| Qwen3.5 decode delta kernel优化 | [#12740](https://github.com/NVIDIA/TensorRT-LLM/pull/12740) | Qwen3.5 解码 delta 内核性能优化 |
| GDN prefill indexed in-kernel update | [#12791](https://github.com/NVIDIA/TensorRT-LLM/pull/12791) | GDN 预填充内核内状态更新优化 |
| Attention developer guide | [#12693](https://github.com/NVIDIA/TensorRT-LLM/pull/12693) | 注意力机制开发者指南（文档） |

**🔗 Release**: https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc12

---

### 3. SGLang — v0.5.10（重大版本）

| Feature | PR | 技术价值 |
|---------|----|----------|
| Piecewise CUDA Graph 默认启用 | [#16331](https://github.com/sgl-project/sglang/pull/16331) | 默认分段 CUDA 图捕获，减少内存开销、提升复杂模型吞吐 |
| Elastic EP 部分故障容错 | [#19248](https://github.com/sgl-project/sglang/pull/19248) | GPU 故障时自动重分配专家权重继续服务，无需全量重启 |
| GPU Staging Buffer (PD disaggregation) | [#19890](https://github.com/sgl-project/sglang/pull/19890) | GQA 模型 RDMA 请求量降低 ~1000x，大并发 TPS/GPU 提升 ~5x |
| HiSparse 稀疏注意力 | [#20343](https://github.com/sgl-project/sglang/pull/20343) | 稀疏注意力后端，长上下文推理减少计算量 |
| FlashInfer MXFP8 kernels | [#19537](https://github.com/sgl-project/sglang/pull/19537) | MXFP8 GEMM/MoE 内核，RL 和通用推理精度+速度兼得 |
| Transformers 5.3.0 升级 | [#17784](https://github.com/sgl-project/sglang/pull/17784) | 升级至 Transformers 5.3.0，解锁 GLM-5 等新模型 |
| DeepSeek V3.2 优化群 | [#19319](https://github.com/sgl-project/sglang/pull/19319) 等 | 融合 Triton KV cache 内核、NSA fuse store indexer、TRT-LLM DSA 内核 |
| LoRA for MoE layers | [#19710](https://github.com/sgl-project/sglang/pull/19710) 等 | MoE 层 LoRA 支持（JIT alignment、融合 Triton、TP、CUDA graph） |
| Prefill Context Parallel (Qwen3) | [#18233](https://github.com/sgl-project/sglang/pull/18233) | Qwen3 MoE 预填充阶段上下文并行，跨 GPU 分配长序列 |
| FlashAttention 4 official | [#20303](https://github.com/sgl-project/sglang/pull/20303) | 升级至官方 FA4 库，Blackwell GPU 支持 |
| Spec-dec with FA4 backend | [#21080](https://github.com/sgl-project/sglang/pull/21080) | FA4 + 投推测解码组合 |
| sglang-kernel 0.4.1 | [#20440](https://github.com/sgl-project/sglang/pull/20440) | 内核包重命名+清理，版本 0.4.1 |
| MLX backend (Apple Silicon) | [#20342](https://github.com/sgl-project/sglang/pull/20342) | 原生 MLX 后端，Apple Silicon 上无需 CUDA 即可推理 |
| SGLang-Diffusion 更新 | 多个 PR | 支持 LTX-2/Hunyuan3D-2/Helios，Qwen-image/Z-image 性能 1.5x |

**🔗 Release**: https://github.com/sgl-project/sglang/releases/tag/v0.5.10

---

### 4. FlashInfer — v0.6.8

| Feature | PR | 技术价值 |
|---------|----|----------|
| CuTe-DSL NVFP4 quantization backend | [#2838](https://github.com/flashinfer-ai/flashinfer/pull/2838) | CuTe-DSL 实现 NVFP4 量化，新精度路径 |
| CuTe-DSL MLA decode op | [#2743](https://github.com/flashinfer-ai/flashinfer/pull/2743) | MLA 解码内核的 CuTe-DSL 实现 |
| MXFP4 + NVFP4 group GEMM (GeForce/Spark) | [#2738](https://github.com/flashinfer-ai/flashinfer/pull/2738) | 消费级 GPU + Spark 上 MXFP4/NVFP4 群组 GEMM |
| MXFP8 GEMM for SM120 | [#2902](https://github.com/flashinfer-ai/flashinfer/pull/2902) | SM120（下一代架构）MXFP8 GEMM |
| GDN MTP decode kernel optimization | [#2842](https://github.com/flashinfer-ai/flashinfer/pull/2842) | GDN MTP 解码内核消除 ilp=1 回退 |
| GDN non-contiguous state decoding | [#2727](https://github.com/flashinfer-ai/flashinfer/pull/2727) | 非连续状态解码支持，灵活 KV cache layout |
| FP8 EP32+ int32 overflow fix | [#2853](https://github.com/flashinfer-ai/flashinfer/pull/2853) | 修复 EP32+ 配置中 int32 溢出导致的 shape 错误 |
| PDL support for CuTe-DSL MLA decode | [#2901](https://github.com/flashinfer-ai/flashinfer/pull/2901) | CUDA PDL 优化 CuTe-DSL MLA 解码内核 |

**🔗 Release**: https://github.com/flashinfer-ai/flashinfer/releases/tag/v0.6.8

---

### 5. llama.cpp — 高频迭代（Apr 22 共 10+ commits）

过去24小时 llama.cpp 有密集提交活动（无正式 release tag），主要围绕 gpt-oss MXFP4 原生格式支持和日常迭代。近期重要里程碑：

- **gpt-oss MXFP4 原生格式支持** — [#15091](https://github.com/ggml-org/llama.cpp/pull/15091)，与 NVIDIA 合作
- **llama-server 多模态支持** — [#12898](https://github.com/ggml-org/llama.cpp/pull/12898)
- **HuggingFace cache 迁移** — 标准 HF cache 目录共享

**🔗 Repo**: https://github.com/ggml-org/llama.cpp

---

### 6. TGI — 项目归档，v3.3.7 最终版

HuggingFace TGI 于 2026-03-21 归档，v3.3.7（2025-12-19）为最终版本。推理框架赛道格局已定：vLLM / SGLang / TensorRT-LLM 三强争霸，TGI 退出。

**🔗 Archive**: https://github.com/huggingface/text-generation-inference/releases/tag/v3.3.7

---

## 🔧 工程启发

1. **PD 分离 RDMA 优化成热点**：SGLang GPU Staging Buffer（~5x TPS）和 TensorRT-LLM conversation-affinity routing 都在解决同一问题 — PD 分离场景下的 KV 迁移效率。GQA 模型是主要受益者（Qwen3.5/DeepSeek），值得在我们的部署中评估。

2. **LoRA + Speculative Decoding 组合**：TensorRT-LLM 首次支持两者同时启用，这是推理服务实用化的关键一步 — 多租户场景下 LoRA 适配器 + 投推测码加速可同时生效。

3. **新精度格式集体落地**：NVFP4/MXFP4/MXFP8 在 FlashInfer、TensorRT-LLM、SGLang 三框架同步推进，下一代 Blackwell/SM120 架构的量化生态正在成型。消费级 GPU（GeForce/Spark）也获支持，边缘推理成本有望大幅下降。

4. **框架竞争格局变化**：TGI 归档、vLLM 升级到 Transformers v5、SGLang 推出 Elastic EP — 推理框架从"功能完备"走向"容错+弹性"阶段，生产级特性（Prometheus 监控、部分故障容错）成为新竞争力。

5. **Eagle3 投推测解码扩展**：vLLM 为 Gemma4 添加 Eagle3 支持，与 SGLang FA4+spec-dec、TensorRT-LLM LoRA+spec-dec 形成三框架投机解码全面覆盖态势。

---

## 📋 明日跟踪建议

| 项目 | 关注点 | 原因 |
|------|--------|------|
| **vLLM** | v0.20.0 正式版详细 release notes | rc1 已出，正式版 release notes 待发布，可能有更多新功能 |
| **TensorRT-LLM** | v1.3.0 正式版进度 | rc12 功能丰富，正式版时间线待关注 |
| **SGLang** | Elastic EP 实际部署 benchmark | 部分故障容错的实际性能影响需要实测数据 |
| **FlashInfer** | SM120 MXFP8 内核基准测试 | 下一代架构性能数据值得关注 |
| **llama.cpp** | gpt-oss MXFP4 性能基准 | 与 NVIDIA 合作的消费级 GPU 推理新路径 |

---

*报告生成时间：2026-04-23 14:50 CST*