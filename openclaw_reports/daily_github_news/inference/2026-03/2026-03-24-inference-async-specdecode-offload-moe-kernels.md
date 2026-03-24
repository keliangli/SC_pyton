---
title: "GitHub 大模型推理日报（2026-03-24）- 异步SpecDecode、Offload 与 MoE Kernel 进展"
date: 2026-03-24
track: 大模型推理
slug: async-specdecode-offload-moe-kernels
source_report: /home/li/.openclaw/workspace/reports/github_inference_news_2026-03-24.md
repo_path: openclaw_reports/daily_github_news/inference/2026-03/2026-03-24-inference-async-specdecode-offload-moe-kernels.md
generated_by: openclaw
---

# GitHub 大模型推理日报（2026-03-24）

> 统计窗口：过去 24 小时（截至 2026-03-24 14:50 Asia/Shanghai / 06:50 UTC）  
> 筛选口径：只保留有实质技术更新的 release / 重要 commit / 新功能 / 性能优化 / 关键正确性修复。

## 今日要点

1. **异步调度与 speculative decoding 开始真正合流。** vLLM 把 zero-bubble async scheduling 接到 spec decoding 路径上，说明服务端框架已经不满足于“异步”和“投机解码”各自存在，而是在推进两者共同工作。
2. **缓存/状态 offload 正在从单一 KV 问题演进为策略层与混合状态层问题。** vLLM 将 CPU offload 重构为可插拔 `CachePolicy`，SGLang 则把 HiCache 扩展到 hybrid model 的 mamba state offloading，表明 offload 已经从“搬 KV”升级到“管理不同状态对象”。
3. **MoE 推理优化今天最活跃。** TensorRT-LLM 在 routing kernel 里加入 Dynamic SMEM block routing，ExecuTorch 则在 Qwen3.5 MoE 上同时做 fused MoE kernel 和多处 kernel launch 消减，MoE 正在从模型支持竞争转向更深的 kernel/访存竞争。
4. **通信-计算重叠仍是高并行推理的核心收益点。** SGLang 针对 DeepSeek-V3.2 的 NSA-CP，把 key all-gather 与 query 计算做 overlap；这类更新虽然体量不大，但很接近真实吞吐优化的“最后一公里”。
5. **边缘/异构后端的可用性还在持续补全。** llama.cpp 一边给 Adreno 的 OpenCL 补 q6_K GEMM/GEMV，一边为 CANN 图捕获预热 RoPE cache，说明“让更多后端真正跑顺”仍是本地与端侧推理的重要主线。

## 项目速递（含链接）

- **vLLM：zero-bubble async scheduling 正式接入 speculative decoding**
  - 关键变化：`[Async][Spec Decoding] Zero-bubble async scheduling + spec decoding` 把 async scheduler 与 draft/verify 路径打通，补了 batch 变化下的 `num_computed_tokens` 更新逻辑，`prepare_next_token_ids` 改为直接用 `seq_lens_cpu`，并在组合模式下自动关闭暂不兼容的 cascade attention。
  - 判断：这不是小修小补，而是 **把“异步调度 + 投机解码”从并存推进到可协同运行**，后续值得重点看吞吐、TPOT 和稳定性数据。
  - 链接：
    - https://github.com/vllm-project/vllm/commit/fafe76b4af175d48b9b69204c995ee167b46aca1

- **vLLM：CPU KV offload 重构为可插拔策略层**
  - 关键变化：`[KV Offload] Refactor CPU offloading` 移除了旧的 `Backend` 抽象，新增 `cpu/manager.py` 与 `cpu/policies/` 目录，将 ARC/LRU 统一到 `CachePolicy` 接口下。
  - 判断：短期看不到 benchmark，但这类改动的意义在于 **把 offload 从“某一种实现”改成“可替换的策略框架”**，为后续更多冷热分层/命中策略留出了工程接口。
  - 链接：
    - https://github.com/vllm-project/vllm/commit/e3c6c10cad9b0f9c36b4ca58933316b3e400f1cf

- **SGLang：DeepSeek-V3.2 的 NSA-CP 开始显式做通信-计算 overlap**
  - 关键变化：`[Perf] Overlap NSA-CP key all-gather with query computation for DeepSeek-V3.2` 在 alt stream 上安排 key all-gather，并与 query 侧 rotate/compute 交叠。
  - 判断：这类 commit 很“窄”，但通常直接对应真实线上收益；它反映的是 **长上下文/并行注意力路径已经在啃 comm/compute overlap 这种硬骨头**。
  - 链接：
    - https://github.com/sgl-project/sglang/commit/649172879778646a8574525448734b95a55b6739

- **SGLang：HiCache 扩到 hybrid model，开始支持 mamba state offloading**
  - 关键变化：`[HiCache][HybridModel]: Support mamba state offloading & HybridCacheController` 新增 hybrid cache controller、调度侧输入初始化与 host hit bookkeeping 调整，并把 offload 范围从纯 KV 扩展到 mamba state。
  - 判断：这是 **“缓存系统开始理解模型内部状态类型差异”** 的信号；后续 hybrid attention / SSM 模型的 serving 能力会越来越依赖这种状态分层管理。
  - 链接：
    - https://github.com/sgl-project/sglang/commit/0986bed8e279ce67659e4e473300fc3c5c717d6a

- **TensorRT-LLM：MoE routing kernel 新增 Dynamic SMEM block routing**
  - 关键变化：`add Dynamic SMEM block routing in MOE` 为小 token / 中等 expert 数场景加入动态 block kernel 路径（`<=16 tokens && <=512 experts`），并通过双 warp exclusive prefix scan 降低同步开销。
  - 判断：这条更新的方向非常明确：**继续压缩 MoE routing 的 shared-memory 和同步成本**，属于高并行 MoE 推理里非常硬核的热点优化。
  - 链接：
    - https://github.com/NVIDIA/TensorRT-LLM/commit/c42e86eaa9f2439657e1864e27fb601faa687d6f

- **TensorRT-LLM：新增 Qwen3.5 的 NVFP4 支持，且补了 dense/MoE 识别与量化映射**
  - 关键变化：`Add Qwen 3.5 supporting(NVFP4)` 新增 `Qwen3_5ForCausalLM`，补了 HF checkpoint 到 TRT-LLM 模块命名空间的 exclude-pattern 归一化，并在 accuracy reference 中加入 `Qwen/Qwen3.5-397B-A17B` 的 NVFP4 + FP8 KV 配置。
  - 判断：这不是简单“能加载模型”而已，而是 **把 Qwen3.5 的低精度推理接入做得更像可落地产品支持**。
  - 链接：
    - https://github.com/NVIDIA/TensorRT-LLM/commit/6c0328c47c2803e4656612dc1790e1023f147d88

- **llama.cpp：Adreno OpenCL 补齐 q6_K GEMM/GEMV，继续强化移动端量化内核可用性**
  - 关键变化：`opencl: add q6_K gemm and gemv kernels for Adreno` 新增 q6_K 的 gemm/gemv、transpose 与相关 host 侧逻辑。
  - 判断：这类更新很接地气，说明 llama.cpp 仍在通过 **把量化格式真正落到具体硬件内核** 来扩大端侧覆盖面。
  - 链接：
    - https://github.com/ggml-org/llama.cpp/commit/1772701f99dd3fc13f5783b282c2361eda8ca47c

- **llama.cpp：为 CANN 图捕获预热 RoPE cache，减少图捕获阶段的 host/device 操作**
  - 关键变化：`CANN: add RoPE cache preload before ACL graph capture` 把 host-to-device memcpy、device malloc/free 和 cache metadata 初始化前移到 capture 之外，让图捕获阶段只记录 device 计算。
  - 判断：这是 **把 Ascend/CANN 后端从“能跑”往“能做 graph capture”再推进一步**，对稳定低开销执行很关键。
  - 链接：
    - https://github.com/ggml-org/llama.cpp/commit/07ff000551fffd99a4d481c1dc5b05abdbce7fb4

- **ExecuTorch：Qwen3.5 MoE 连做两层优化，A100 上 decode 吞吐从 12.4 提到 58.5 tok/s**
  - 关键变化 1：`Fuse linear projections, SiLU activation, and replace conv1d to reduce kernel launches` 同时融合 QKV、GDN 输入投影、shared expert 的 gate/up，并用手写 depthwise conv 替换灾难性慢的 `conv1d->conv2d` 分解；commit 中给出 A100 数据：decode `12.41 -> 58.5 tok/s`，prefill `47.3 -> 96 tok/s`。
  - 关键变化 2：`Enable fused MoE kernel for Qwen 3.5 MoE model` 用 fused MoE Triton kernel 替换 compute-all-gather 路径，decode 时每层只需从 HBM 加载 `8/256` 个 expert 的权重，访存量显著下降。
  - 判断：今天最值得盯 benchmark 的项目之一；它表明 **端到端速度提升往往来自“图结构改写 + 融合内核 + 访存剪裁”一起做**。
  - 链接：
    - https://github.com/pytorch/executorch/commit/f479ecff9f4d3de59930784177bf6e9156bd58b4
    - https://github.com/pytorch/executorch/commit/acf15bfbe0d4e7d85db627f104e45d5456bbf253

## 工程启发

1. **异步调度、spec decode、graph capture、offload 不该再分开看。** 今天多条更新都在说明：真正成熟的 serving 系统优化，已经从单点能力竞争变成跨模块协同。
2. **Offload 的下一步不是“多搬一点”，而是“按状态类型和策略去搬”。** vLLM 的策略抽象和 SGLang 的 mamba state offloading 都在往这条路上走。
3. **MoE 的性能上限越来越受路由与访存支配。** TensorRT-LLM 和 ExecuTorch 今天的改动都在围绕 routing、HBM traffic、kernel launch 数量做文章，说明 dense 模型时代的许多直觉在 MoE 上不再够用。
4. **边缘/端侧推理的真正门槛仍是 backend completeness。** llama.cpp 的 Adreno/CANN 路径、ExecuTorch 的模型图重写都表明，是否“有某个后端”不重要，重要的是这个后端在常见量化格式与关键算子上是否补齐。
5. **commit 级别的性能数字要重点标记可迁移性。** ExecuTorch 给出的数字很亮眼，但要继续区分它们是特定模型/特定 shape 成立，还是对更一般的 Qwen3.5 MoE serving 都有帮助。

## 明日跟踪建议

1. 跟进 **vLLM zero-bubble async + spec decode** 是否很快补出公开 benchmark，重点看吞吐、TPOT、request churn 下的稳定性，以及 cascade attention 何时恢复兼容。
2. 跟进 **vLLM KV offload 重构** 后是否紧接着出现新策略或性能数据；如果只是架构改造没有后续策略，很容易停在“好扩展但没收益”。
3. 跟进 **SGLang NSA-CP overlap** 是否在 DeepSeek-V3.2 / 长上下文场景下给出 comm overlap 的量化收益；同时观察 hybrid mamba state offload 是否伴随更多 scheduler/eviction 策略提交。
4. 跟进 **TensorRT-LLM** 后续是否给出 Dynamic SMEM block routing 的覆盖范围与性能收益，以及 Qwen3.5 NVFP4 在更大模型上的精度/吞吐取舍。
5. 跟进 **llama.cpp** 的 Adreno q6_K benchmark 与 CANN graph capture 后续提交；如果两条线都持续推进，说明移动端与 Ascend 都在被当成一等后端维护。
6. 跟进 **ExecuTorch** 这组优化是否从 `nano_qwen35_moe` 推广到更通用的 Qwen3.5/Qwen3.5-MoE 导出与运行路径，避免“只在 demo 模型上特别快”。
