# GitHub 大模型推理日报（2026-05-09）— 推理框架全线升级：CUDA 13 / Spec V2 / DeepSeek V4 稳定化

## 今日要点

1. **SGLang v0.5.11 正式发布**：CUDA 13 + Torch 2.11 成为默认构建；Speculative Decoding V2 设为默认（overlap scheduling 隐藏 CPU 开销）；Decode 侧 Radix Cache 支持 PD 分离部署；新增 Gemma 4 / GLM-5.1 / Qwen3.6 / MiMo-V2.5 / Kimi-K2.6 等模型。
2. **vLLM v0.20.1 热修复**：专注 DeepSeek V4 稳定化与性能——多流 pre-attention GEMM、PTX cvt 指令加速 FP32→FP4 转换、head_compute_mix_kernel 优化；修复 persistent topk 死锁。
3. **llama.cpp 日更 b9082–b9085**：新增 MiMo-V2.5 flash attention MMA/Tiles；Hexagon 端 Gated Delta Net HTP 内核；SYCL flash attention 分配开销优化 + BF16 GET_ROWS。
4. **TensorRT-LLM v1.3.0rc14**：Mamba 混合模型前缀缓存；Qwen3.5 MoE 路由 + NVFP4 修复；新增 CuteDSL FP8 paged MQA decode kernel。
5. **SGLang 当日重要 commit**：KDA prefill kernel 对角线 + recompute 融合优化；MORI-IO 状态迁移补齐（Mamba/SWA/NSA）；自适应 prefill delayer 调度器（OSL 方差导致吞吐腰斩问题的对策）。
6. **vLLM 当日重要 commit**：Cohere Eagle speculative decoding 支持；tree attention 移除（清理 spec-decode 后端）；显式 weight update API；CUTLASS MXFP4-MXFP8 MoE scale 修复。

## 项目速递

### vLLM
- **v0.20.1** — DeepSeek V4 稳定化 + 性能 | [Release](https://github.com/vllm-project/vllm/releases/tag/v0.20.1)
- Cohere Eagle spec-decode 支持 (#42078) | [PR](https://github.com/vllm-project/vllm/pull/42078)
- 移除 TreeAttention，简化 attention 后端重构 (#42121) | [PR](https://github.com/vllm-project/vllm/pull/42121)
- 显式 `/start_weight_update` / `/finish_weight_update` API (#39212)
- CUTLASS scaled mm 支持非兼容尺寸 (#41868)
- CUTLASS MXFP4-MXFP8 MoE swizzled scale 修复 (#42089)

### SGLang
- **v0.5.11** — CUDA 13 / Spec V2 默认 / Decode Radix Cache | [Release](https://github.com/sgl-project/sglang/releases/tag/v0.5.11)
- KDA prefill kernel 对角线 + recompute 融合 (#24271)
- MORI-IO 状态迁移（Mamba/SWA/NSA）+ 高并发修复 (#22665) | [PR](https://github.com/sgl-project/sglang/pull/22665)
- 自适应队列 prefill delayer 触发器——解决 OSL 方差致吞吐暴跌 (#23189) | [PR](https://github.com/sgl-project/sglang/pull/23189)
- Laguna-XS.2 混合 SWA MoE 原生支持 (#24204) | [PR](https://github.com/sgl-project/sglang/pull/24204)
- Speculative decoding 命名规范 (#24094)
- `SGLANG_RADIX_FORCE_MISS` 环境变量调试前缀缓存 (#24726)

### llama.cpp (ggml-org)
- **b9085** — MiMo-V2.5 flash attention MMA/Tiles (#22812)
- **b9084** — Hexagon Gated Delta Net HTP 内核 (#22837)
- **b9082** — Hexagon L2_NORM HVX 内核 (#22816)
- Gemma4_26B_A4B_NVFP4 量化支持 (#22804)
- Vertex AI 兼容 API (#22545)
- SYCL: flash attention 分配开销缩减 (#22732)，BF16 GET_ROWS (#21391)
- CUDA: fuse snake activation 内核 (#22667)

### TensorRT-LLM
- **v1.3.0rc14** — Mamba 混合模型前缀缓存 / Qwen3.5 MoE 优化 | [Release](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc14)
- CuteDSL FP8 paged MQA logits decode kernel (#13219)
- AutoDeploy: DeepSeek-R1 性能优化 (#12946)
- TRTLLM MoE autotune 改进 (#13667)
- per-rank iteration stats `/metrics` 端点 (#13221)

### ktransformers
- AMX FP4 MoE guard 修复 + AMXINT4 CPU 权重转换路径 (#1980, #1986)

### MNN (Alibaba)
- 推理投机解码 cache mismatch + mrope 修复 (#4421, #4410)
- QNN 离线图导出多进程并行 (#4414)

## 工程启发

1. **OSL 方差是吞吐杀手**：SGLang 的 prefill delayer 分析表明，输出长度方差（而非输入）是聚合推理吞吐从 7830 tok/s 跌至 3846 tok/s 的根因——decode batch 被小 prefill backfill 碎片化。调度层需主动延迟 prefill 入场以保护 decode batch 完整性。
2. **Spec V2 成为工业标配**：SGLang 默认启用 overlap scheduling spec-decode；vLLM 持续扩展 Eagle/MTP 路径。投机解码不再是实验功能，而是延迟-吞吐权衡的标配工具。
3. **PD 分离部署持续成熟**：SGLang Decode 侧 Radix Cache、MORI-IO 状态迁移、vLLM NixlConnector 修复——PD 分离从"可用"走向"好用"，长前缀复用和跨节点状态迁移是关键突破点。
4. **CUDA 13 迁移窗口**：SGLang 和 vLLM 相继默认 CUDA 13 + Torch 2.11，新一代内核（CuteDSL、FA3/FA4）依赖新工具链，生产环境需规划迁移。
5. **端侧推理持续下沉**：llama.cpp 的 Hexagon/Qualcomm 内核、MNN 的 QNN 多进程导出、ktransformers 的 AMX INT4/FP4 CPU 路径——边缘和手机端推理加速是当前活跃赛道。

## 明日跟踪建议

- 🔍 **SGLang Spec V2 在生产 workload 下的实测数据**：关注社区 benchmark 复现
- 🔍 **vLLM DeepSeek V4 + MXFP8 all-to-all 在多卡场景的性能基线**
- 🔍 **TensorRT-LLM v1.3.0 正式版发布时间线**（当前 rc14）
- 🔍 **llama.cpp MiMo-V2.5 在端侧的推理性能**：新 flash attention kernel 实际加速比
- 🔍 **ktransformers AMXINT4 CPU 推理路径**：Intel 平台纯 CPU MoE 推理是否可用
