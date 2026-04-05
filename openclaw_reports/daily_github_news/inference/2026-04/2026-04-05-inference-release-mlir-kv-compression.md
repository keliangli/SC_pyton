---
title: "GitHub 大模型推理日报（2026-04-05）- vLLM 0.19、MLIR 融合与 KV 压缩"
date: 2026-04-05
track: 大模型推理
slug: release-mlir-kv-compression
source_report: /home/li/.openclaw/workspace/reports/github_inference_news_2026-04-05.md
repo_path: openclaw_reports/daily_github_news/inference/2026-04/2026-04-05-inference-release-mlir-kv-compression.md
generated_by: openclaw
---

# GitHub 大模型推理日报（2026-04-05）

> 统计窗口：过去 24 小时（截至 2026-04-05 14:50 Asia/Shanghai / 06:50 UTC）  
> 筛选口径：只保留有实质技术更新的 release / 重要 commit / 新功能 / 性能优化 / 关键正确性修复。

## 今日要点

1. **vLLM 用 v0.19.0 把系统级推理栈又往前推了一大步。** 这不是单个模型 support 的 release，而是把 zero-bubble async scheduling + speculative decoding、general CPU KV cache offloading、ViT full CUDA graph、PP piecewise CUDA graphs、DBO generalization 与 B300/GB300 support 一次性整合进稳定版本，说明 vLLM 正在把调度、cache 和 graph execution 统一到主干交付面。

2. **KV / state memory 是今天最强的主线。** SGLang 在 AMD 路径把 MLA 扩到 `nhead < 16` 并支持 TP=8 的 FP8 KV cache；ExecuTorch 把 Qwen3.5 MoE 的 KV cache 压成 TQ4，PR 给出 **3.8x** 内存压缩；TensorRT-LLM 则把 KVCacheManagerV2 的 reuse 逻辑扩到 SSM。长上下文成本优化开始从 transformer KV cache 扩展到更广泛的 state 管理。

3. **推理编译器在从手写 fusion 走向自动生成。** TensorRT-LLM 为 AutoDeploy 引入 MLIR-based auto-generated elementwise fusion，新增完整 dialect、FX↔MLIR 转换、subgraph discovery 与 Triton emitter，意味着 post-sharding fusion 逐步进入可扩展编译链路，而不再只靠定制 kernel。

4. **今天的信号不是“某个 kernel 又快一点”，而是“推理系统的 memory / compiler / runtime 三层一起升级”。** 这对推理基础设施的意义更大：后续胜负更可能由 cache 治理、编译自动化和特定硬件路径稳定性决定，而不是单点算子 micro-opt。

## 项目速递（含链接）

- **vLLM：发布 v0.19.0，正式把 async scheduling、spec decode、general CPU KV offload 等系统能力打包落版**
  - 关键变化：release highlights 包括 Gemma 4 full support、zero-bubble async scheduling + speculative decoding、Model Runner V2 成熟化、ViT full CUDA graph capture、general CPU KV cache offloading、DBO 对通用模型泛化、B300/GB300 support、Transformers v5 compatibility。
  - 工程含义：这是一个典型的 **runtime 能力整合型 release**，重点不在单模型，而在 **调度 + graph + cache + hardware bring-up** 的系统收敛。
  - 链接：
    - https://github.com/vllm-project/vllm/releases/tag/v0.19.0

- **SGLang：AMD MLA 支持小 head 数 + FP8 KV cache for TP=8（Kimi K2.5 路径）**
  - 关键变化：AITER MLA backend 现在允许 `num_head` 为 4 / 8 或 `[16, 128]` 的 16 倍数；对 `<16` 的场景自动 pad 到 16，并引入 `head_repeat_factor`；同时补测 MI35x / Kimi K2.5 的 MXFP4 与 FP8 KV cache 场景。
  - 工程含义：这不是普通兼容 patch，而是把 AMD 上 MLA + FP8 KV cache 的可运行配置空间明显扩大，直接服务 TP=8 长上下文 / 大模型部署。
  - 链接：
    - https://github.com/sgl-project/sglang/commit/dd49127fe612800d2f2aa258c9b7086043f103fa

- **TensorRT-LLM：AutoDeploy 接入 MLIR-based auto-generated elementwise fusion**
  - 关键变化：一次性引入 MLIR dialect、FX↔MLIR roundtrip、subgraph discovery / replace、Triton emitter、kernel cache 与 E2E tests；PR 过程中还处理了 64-arg custom op 限制、placement-aware splitting、multimodal attr copy、gated RMSNorm 等真实部署 bug。
  - 工程含义：这说明 TensorRT-LLM 正把 post-sharding fusion 从“人工堆特例”升级为 **可持续扩展的 compiler pipeline**，对多层模型和 multi-stream MoE 更关键。
  - 链接：
    - https://github.com/NVIDIA/TensorRT-LLM/pull/12427
    - https://github.com/NVIDIA/TensorRT-LLM/commit/173b350b74133ecd6d24617d2633c1c7357c799c

- **TensorRT-LLM：KVCacheManagerV2 扩展到 SSM cache reuse**
  - 关键变化：主干合入 `Support cache reuse for SSM in KVCacheManagerV2`，把 cache reuse 能力从传统 transformer KV 管理推进到 state-space model。
  - 工程含义：统一 cache manager 若能同时覆盖 KV cache 与 SSM state，后续 disaggregated serving / hybrid models 的 state lifecycle 管理会更顺。
  - 链接：
    - https://github.com/NVIDIA/TensorRT-LLM/commit/fd7cc851629e42c555e431598c7ae9a3d599bacf

- **ExecuTorch：Qwen3.5 MoE 接入 TurboQuant TQ4 KV cache compression**
  - 关键变化：CUDA backend 新增 TurboQuant KV cache 压缩，使用 nibble-packed uint8 indices + bf16 norms 替代 bf16 KV tensors；fused Triton SDPA kernel 在 attention inner loop 内按 tile 解压；PR 给出 **KV cache memory 3.8x 压缩**，A100 上 e2e decode **59.8 tok/s**（baseline 70.6 tok/s）。
  - 工程含义：这是很有代表性的 **“以内存换少量算力开销”** 路线，说明长上下文部署已经愿意为大幅节省 KV 内存接受可控的 decode overhead。
  - 链接：
    - https://github.com/pytorch/executorch/pull/18687
    - https://github.com/pytorch/executorch/commit/afc998987419b4cef026e9436e0c1a79216ae5e5

## 工程启发

1. **长上下文优化已从“KV cache 更省”升级到“统一 state memory engineering”。** 今天同时看到 FP8 KV cache、TQ4 KV compression、SSM cache reuse，说明 cache manager 不再只服务 transformer。

2. **compiler automation 将成为推理基础设施下一波护城河。** TensorRT-LLM 这类 MLIR auto-fusion 不只是性能问题，更是减少 hand-written kernel 维护成本、加快新模型接入速度。

3. **特定硬件路径要把“能跑”升级成“配置空间足够宽”。** SGLang 支持小 head 数 MLA 的意义，在于真实 TP 配置不再被 head 形状卡死；这比单点 benchmark 更接近生产可用性。

4. **release 价值要看系统面，而不是 feature 数量。** vLLM 0.19.0 最值得跟的是 async scheduling + spec decode + CPU KV offload + broader CUDA graphs 是否真的在主线部署里稳定协同。

5. **KV 压缩路线值得尽快自建 benchmark。** ExecuTorch 已经给出一个很清楚的 tradeoff：3.8x memory reduction 换有限 decode overhead。对长上下文 / 边缘设备场景，很可能是值得单独评估的方向。

## 明日跟踪建议

1. 跟进 **vLLM v0.19.0** 发布后是否很快出现针对 async scheduling + spec decode / CPU KV offload 的独立 benchmark 与 hotfix。

2. 跟进 **SGLang AMD MLA** 这条 FP8 KV cache 路径是否扩到更多模型 / 更多 TP 配置，并观察 MI300 / MI35x 实测数字是否公开。

3. 跟进 **TensorRT-LLM MLIR auto-fusion** 是否从 opt-in / prototype 继续走向默认路径，以及是否补更明确的端到端吞吐收益。

4. 跟进 **TensorRT-LLM SSM cache reuse** 是否很快配套 hybrid model / Mamba 类 serving 示例或 benchmark。

5. 跟进 **TurboQuant TQ4 KV compression** 是否被更多 runtime 借鉴；优先盯 memory footprint、TTFT、decode tok/s、long-context 质量回退四个指标。
