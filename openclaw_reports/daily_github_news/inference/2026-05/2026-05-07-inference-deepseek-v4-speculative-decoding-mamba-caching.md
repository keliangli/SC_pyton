# GitHub 大模型推理日报（2026-05-07）- DeepSeek V4 稳定化 + Spec V2 默认 + Mamba 前缀缓存

## 今日要点

1. **vLLM v0.20.1 发布**：DeepSeek V4 专项补丁，含多流 pre-attention GEMM、MXFP8 all-to-all、PTX FP32→FP4 快速转换、tile kernel 优化及 persistent topk 死锁修复
2. **SGLang v0.5.11 发布**：Spec V2（overlap scheduling）默认开启；PD 分离部署支持 Decode 侧 Radix Cache；新增 Gemma 4 / Qwen3.6 / Kimi-K2.6 等 Day-0 模型；DFLASH speculative decoding 上线
3. **TensorRT-LLM v1.3.0rc14 发布**：Mamba 混合模型前缀缓存（Qwen3.5 / Nemotron Super V3）；DFlash 单模型 speculative decoding；NVFP4 权重热更新；CuteDSL bf16 dense GEMM
4. **llama.cpp b9049 发布**：MiniCPM-V 4.6 多模态视觉支持
5. **新项目 arle**：Rust 原生推理运行时，面向 Qwen3/Qwen3.5，CUDA + Metal，推理路径无 PyTorch 依赖
6. **新项目 llm-d batch-gateway**：Go 实现的 OpenAI Batch API 兼容网关，Kubernetes 原生，支持 5 万请求/作业

---

## 项目速递

### 🔥 vLLM v0.20.1（2026-05-04）

[Release Notes](https://github.com/vllm-project/vllm/releases/tag/v0.20.1)

- **DeepSeek V4 专项优化**：
  - Multi-stream pre-attention GEMM + 可配置 GEMM knob（[#41061](https://github.com/vllm-project/vllm/pull/41061), [#41443](https://github.com/vllm-project/vllm/pull/41443)）
  - BF16 / MXFP8 all-to-all FlashInfer 单边通信（[#40960](https://github.com/vllm-project/vllm/pull/40960)）
  - PTX cvt 指令加速 FP32→FP4 转换（[#41015](https://github.com/vllm-project/vllm/pull/41015)）
  - 集成 tile kernel（head_compute_mix_kernel）优化 head 计算（[#41255](https://github.com/vllm-project/vllm/pull/41255)）
- **Bug 修复**：
  - 修复 persistent topk cooperative deadlock @ TopK=1024（[#41189](https://github.com/vllm-project/vllm/pull/41189)）
  - 修复 inter-CTA init race on RadixRowState（[#41444](https://github.com/vllm-project/vllm/pull/41444)）
  - 修复 BailingMoE linear layer（[#40859](https://github.com/vllm-project/vllm/pull/40859)）
  - 修复 CUDA graph 中 max_num_batched_token 未捕获（[#40734](https://github.com/vllm-project/vllm/pull/40734)）

> 注：v0.20.0（4 月 27 日）为大版本，含 DeepSeek V4 初始支持、CUDA 13.0 默认、PyTorch 2.11、FA4 默认 MLA prefill、TurboQuant 2-bit KV cache（4× 容量）、在线量化前端、vLLM IR 骨架。

---

### 🔥 SGLang v0.5.11（2026-05-05）

[Release Notes](https://github.com/sgl-project/sglang/releases/tag/v0.5.11)

- **Spec V2 默认开启**：overlap scheduling 隐藏 CPU 开销，EAGLE/MTP/DFLASH 路径每步 CPU 成本显著降低（[#21062](https://github.com/sgl-project/sglang/pull/21062)）
- **PD 分离 Decode Radix Cache**：decode 侧前缀缓存现在在 prefill/decode 分离部署下生效，恢复 radix-cache 命中率和 TTFT 节省（[#19746](https://github.com/sgl-project/sglang/pull/19746)）
- **DFLASH Speculative Decoding**：社区贡献的高吞吐 spec-decode kernel，已扩展到多模型后端及 AMD ROCm（[#22077](https://github.com/sgl-project/sglang/pull/22077)）
- **Day-0 新模型**：Gemma 4、GLM-5.1、Qwen3.6、MiMo-V2.5/V2.5-Pro、Ling-2.6-Flash、Mistral Medium 3.5、Kimi-K2.6
- **LoRA for DeepSeek-V3 / Kimi-K2**：MLA-based MoE 模型上支持 LoRA adapter（[#22323](https://github.com/sgl-project/sglang/pull/22323)）
- **FlashInfer CuteDSL MoE Runner**：新增 FP4 MoE 高性能 fused-MoE 选项（[#21339](https://github.com/sgl-project/sglang/pull/21339)）
- **Context Parallel 增强**：all-reduce + RMSNorm fusion；MoE 与 attention 并行度独立可调（[#21249](https://github.com/sgl-project/sglang/pull/21249)）
- **CUDA 13 + Torch 2.11**：默认 CUDA 版本升级到 13.0

---

### 🔥 TensorRT-LLM v1.3.0rc14（2026-05-07）

[Release Notes](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc14)

- **Mamba 混合模型前缀缓存**：Qwen3.5 / Nemotron Super V3 支持 prefix caching（[#12185](https://github.com/NVIDIA/TensorRT-LLM/pull/12185)）
- **Qwen3.5 定制 MoE 路由**：custom MoE routing + dense/NVFP4 权重加载修复（[#13433](https://github.com/NVIDIA/TensorRT-LLM/pull/13433)）
- **DFlash 单模型 speculative decoding**（[#12794](https://github.com/NVIDIA/TensorRT-LLM/pull/12794)）
- **NVFP4 权重热更新**（[#12320](https://github.com/NVIDIA/TensorRT-LLM/pull/12320)）
- **llm.encode() 快速路径**：encoder-only 模型专用（[#12801](https://github.com/NVIDIA/TensorRT-LLM/pull/12801)）
- **Kernel 性能**：CuteDSL bf16 dense GEMM、sparse-attention GVR Top-K dispatcher、fused add-norm-FP8 quantization、TF32 DSA GEMM、sampler 优化
- **分離式服務增强**：gen-first ADP serving、KV-aware hit-rate gates、fair-share caps

---

### 🆕 llama.cpp b9049（2026-05-06）

[Release](https://github.com/ggml-org/llama.cpp/releases/tag/b9049)

- **MiniCPM-V 4.6 多模态支持**：新增 vision model 支持，含 flash attention 兼容、n_merge slice 对齐、vit_merger 插入点优化（[#22529](https://github.com/ggml-org/llama.cpp/pull/22529)）
- b9048：修复不支持的架构不再 crash（[#22742](https://github.com/ggml-org/llama.cpp/pull/22742)）

---

### 🆕 vllm-project/speculators

[GitHub](https://github.com/vllm-project/speculators)

- vLLM 官方 speculative decoding 统一库，用于构建、评估和存储 speculative decoding 算法
- 独立仓库，含 examples / scripts / tests / docs，支持 ReadTheDocs 构建
- 面向 vLLM 推理生态的 spec-decode 标准化基础设施

---

### 🆕 cklxx/arle

[GitHub](https://github.com/cklxx/arle)

- **Rust 原生推理运行时**，面向 Qwen3 / Qwen3.5
- CUDA + Metal 后端，推理路径无 PyTorch 依赖
- OpenAI 兼容 serving + 集成 agent / train / self-evolution 工作流
- Cargo workspace 结构，含 benchmarks / examples / tests
- 亮点：Rust 全栈推理框架，绕过 Python 生态的启动和调度开销

---

### 🆕 llm-d-incubation/batch-gateway

[GitHub](https://github.com/llm-d-incubation/batch-gateway)

- Go 实现的 OpenAI Batch API 兼容网关（`/v1/batches` + `/v1/files`）
- 支持单作业 50,000 请求，model-aware 调度，intelligent flow control
- 三组件架构：API Server、Batch Processor、Data Layer（PostgreSQL + Redis/Valkey + S3）
- Batch Dispatcher 监控下游指标，动态调整 batch 请求流，最小化对交互式请求的干扰
- Kubernetes 原生，Helm charts + OpenShift 兼容，Prometheus / OTel 可观测性

---

### 🆕 raketenkater/llm-server

[GitHub](https://github.com/raketenkater/llm-server)

- llama.cpp / ik_llama.cpp 智能启动器
- 自动检测 GPU、优化 MoE 模型放置、crash recovery
- 含 benchmark-ai-tune.py 自动调优、systemd 服务集成
- 面向本地/边缘部署的零配置推理服务管理

---

## 工程启发

1. **Speculative Decoding 成为主战场**：vLLM speculators 独立仓库、SGLang Spec V2 默认、TRT-LLM DFlash 单模型支持——三大框架都在加码投机解码，意味着这不再只是实验性优化，而是生产级标配。工程上应关注 spec-decode 对 CUDA graph 和 memory pool 的交互影响。

2. **DeepSeek V4 适配加速**：vLLM 专门发 patch release 做 DSV4 稳定化（multi-stream GEMM、MXFP8 all-to-all、PTX FP4 转换），SGLang 也加了 DSV3.2/V4 的 token-leakage 修复。对于使用 DeepSeek 系列模型的团队，升级到 vLLM 0.20.1 或 SGLang 0.5.11 是必须的。

3. **Mamba/Hybrid 模型推理基础设施成熟**：TRT-LLM 为 Mamba 混合模型加入 prefix caching，这对 Qwen3.5 等 Mamba-attention 混合架构的推理效率至关重要。此前这类模型缺乏 KV cache 复用，长上下文场景成本高。

4. **Rust 推理运行时出现**：arle 项目代表了绕过 Python/PyTorch 栈的尝试。虽然生态还早期，但 Rust 全栈 + CUDA/Metal 直连的模式值得关注，尤其是对边缘设备和低延迟场景。

5. **Batch 推理标准化**：llm-d batch-gateway 实现了 OpenAI Batch API 兼容，为批量推理（评估、embedding 生成、离线处理）提供了标准化接口，与交互式推理共存时通过 flow control 最小化干扰。

---

## 明日跟踪建议

1. **vLLM Speculators 仓库进展**：关注其与 vLLM 主仓库的集成方式和 spec-decode benchmark 结果
2. **SGLang DFLASH 性能数据**：社区 kernel 的实际加速比和与 EAGLE/MTP 的对比
3. **TRT-LLM v1.3.0 正式版**：当前 rc14，关注 Mamba prefix caching 的生产稳定性
4. **arle 项目成熟度**：Rust 推理运行时的 benchmark 和模型支持范围
5. **llama.cpp 对更多视觉模型的支持**：MiniCPM-V 4.6 后是否有更多多模态模型跟进
6. **CUDA 13.0 生态迁移**：vLLM 和 SGLang 都已默认 CUDA 13，关注驱动兼容性和 kernel 性能差异

---

*数据来源：GitHub Releases / Trending / Search，抓取时间 2026-05-07 14:50 CST*
