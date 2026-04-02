---
title: "GitHub 大模型推理日报（2026-04-02）- MoE预填充、调度与边缘后端修复"
date: 2026-04-02
track: 大模型推理
slug: moe-prefill-scheduler-edge-fixes
source_report: /home/li/.openclaw/workspace/reports/github_inference_news_2026-04-02.md
repo_path: openclaw_reports/daily_github_news/inference/2026-04/2026-04-02-inference-moe-prefill-scheduler-edge-fixes.md
generated_by: openclaw
---

# GitHub 大模型推理日报（2026-04-02）

> 统计窗口：过去 24 小时（截至 2026-04-02 14:50 Asia/Shanghai / 06:50 UTC）  
> 筛选口径：只保留有实质技术更新的 release / 重要 commit / 新功能 / 性能优化 / 关键正确性修复。

## 今日要点

1. **MoE 推理是今天最强的主线。** TensorRT-LLM 合入 DWDP（Distributed Weight Data Parallelism）以加速分离式 MoE inference 的 context/prefill 阶段；SGLang 则为 MiniMax-M2.5 routed MoE 打开 fp8 `flashinfer_trtllm` 路径，并给出 4xGB200 上 **5.48%~9.04%** 的吞吐提升。

2. **SGLang 今天同时补了调度器与 speculative decoding 的关键正确性缺口。** `prefill-only` batch 与普通生成 batch 混合合并时，调度器此前会错误跳过 decode，并误触发 idle/leak 检查；同时 Ngram speculative decoding 去掉 `min/max_match_window_size`，改为匹配 Trie 的所有 suffix，长上下文行为更稳定。

3. **异构后端稳定性继续收口。** vLLM 为 `cpu_fused_moe` 补上 GELU activation 支持，并修复 ROCm 路径的缺失 symbol 导致的 runtime import failure；llama.cpp 则连续修复 CUDA Flash Attention kernel 选择逻辑、Adreno q8_0 OpenCL 泄漏，并在 Hexagon 后端新增 `cumsum` op 支持。

4. **今天的更新很“工程现实主义”。** 不是单纯卷新模型支持，而是围绕 MoE 热路径、scheduler correctness、ROCm/Adreno/Hexagon 这些真实部署痛点持续补强，说明推理系统优化正从“能跑”进入“能稳定规模化跑”。

## 项目速递（含链接）

- **TensorRT-LLM：为分离式 MoE inference 引入 DWDP（Distributed Weight Data Parallelism）**
  - 关键变化：新增针对 **context/prefill 阶段** 的 DWDP 设计，核心思路是把 data parallelism 与基于 NVLink 的权重搬运结合起来，通过 ping-pong buffering 和更细粒度的 expert-to-worker assignment，减少跨 rank 同步开销。
  - 工程含义：这不是单点 kernel 优化，而是 **跨 rank 的异步执行与权重调度机制升级**，目标直指 workload imbalance 下的 GPU 利用率问题。
  - 链接：
    - https://github.com/NVIDIA/TensorRT-LLM/pull/12136
    - https://github.com/NVIDIA/TensorRT-LLM/commit/e92ee4fe550783a5f3a51cd690d89d1fe18ea30b

- **SGLang：为 MiniMax-M2.5 routed MoE 启用 fp8 `flashinfer_trtllm` 路径**
  - 关键变化：启用 `align_fp8_moe_weights_for_flashinfer_trtllm` 的 routed 版本，复用 non-routed fused path，并处理 kernel 输出固定为 bf16 时的 dtype cast。
  - 已公开结果：PR 描述给出 **4xGB200** 上的 benchmark，`TP4` 相比默认 Triton MoE **加速 9.04%**，`TEP4` **加速 5.48%**。
  - 工程含义：SGLang 正把 routed MoE 从通用 Triton 路径推进到更贴近硬件的 fp8 fused path，说明 MoE serving 热点已经进入更深的 vendor-specific 优化阶段。
  - 链接：
    - https://github.com/sgl-project/sglang/pull/20394
    - https://github.com/sgl-project/sglang/commit/d24ea24e18ccce7265065dea9d9364758ce848b1

- **SGLang：补 scheduler 与 Ngram speculative decoding 的两个关键收口点**
  - 关键变化 1：`scheduler: add prefill-only update in merge batch` 修复 `prefill-only` batch 先合入后，`running_batch.is_prefill_only` 不会被普通 generation batch 纠正的问题；此前这会导致 decode 被跳过，并在 KV cache 仍占用时误走 idle/leak 检查路径。
  - 关键变化 2：`[Spec][Ngram] ... matching all suffixes of the Trie` 移除 `min_match_window_size` / `max_match_window_size` 两个窗口参数，改为匹配所有 suffix，并补上 long-context 测试。
  - 工程含义：一个指向 **scheduler correctness**，一个指向 **specdecode 搜索空间和配置复杂度收敛**，两者都属于会直接影响线上稳定性与可维护性的改动。
  - 链接：
    - https://github.com/sgl-project/sglang/pull/21840
    - https://github.com/sgl-project/sglang/commit/f30df723bf146d4a8037010b0b11939a601df423
    - https://github.com/sgl-project/sglang/pull/21225
    - https://github.com/sgl-project/sglang/commit/f836658077003a1b5b027cef3abfeedf6c6f2c5b

- **vLLM：CPU / ROCm 路径继续补能力与稳定性**
  - 关键变化 1：`[CPU] Support gelu act in cpu_fused_moe`，为 `cpu_fused_moe` 增补 GELU activation 支持，意味着 CPU 侧 MoE 路径的 activation 覆盖更完整。
  - 关键变化 2：`[ROCm][Bugfix] Fix ROCm runtime failure due to missing symbol`，修复 `vllm._C` 在 ROCm 环境下因未构建文件暴露缺失 symbol 而直接 import 失败的问题。
  - 工程含义：这两条都不算“炫技功能”，但对 **非 CUDA 环境可部署性** 很关键；如果 CPU/ROCm 路径不稳，很多混合部署和 CI 回归都会被卡死。
  - 链接：
    - https://github.com/vllm-project/vllm/pull/38770
    - https://github.com/vllm-project/vllm/commit/c6f722b93e8e795065751172812ee6a5540e5901
    - https://github.com/vllm-project/vllm/pull/38750
    - https://github.com/vllm-project/vllm/commit/3aab680e3e261e04c188b3015611f2947465d33b

- **llama.cpp：边缘与异构后端连续修补热路径问题**
  - 关键变化 1：`CUDA: fix FA kernel selection logic`，修复此前误把 unpadded KV cache 场景下的 CUDA Flash Attention 选择逻辑关掉的问题。
  - 关键变化 2：`opencl: fix leak in Adreno q8_0 path`，修复 Adreno q8_0 GEMM 路径里 subbuffer / image1d_buffer 未释放的问题；PR 明确指出这在 Windows + Adreno 驱动上会导致明显 slowdown，并让 `llama-bench` 与真实 completion 表现出现偏差。
  - 关键变化 3：release `b8628` 为 Hexagon 后端新增 `cumsum` op，并启用 DMA。
  - 工程含义：llama.cpp 今天的价值不在“多一个 feature”，而在 **端侧真实运行时的稳定性、基准可信度和算子完整性**。
  - 链接：
    - https://github.com/ggml-org/llama.cpp/pull/21271
    - https://github.com/ggml-org/llama.cpp/commit/86221cf6dace86f47d896a38e0de652db4aa81a8
    - https://github.com/ggml-org/llama.cpp/pull/21212
    - https://github.com/ggml-org/llama.cpp/commit/95a6ebabb277c4cc18247e7bc2a5502133caca63
    - https://github.com/ggml-org/llama.cpp/releases/tag/b8628

## 工程启发

1. **MoE 的下一阶段优化重点，已经从“单 kernel 更快”转向“跨 rank / 跨阶段 orchestration 更聪明”。** TensorRT-LLM 的 DWDP 很典型：它优化的是权重移动、同步时机和 rank 间异步性，而不是只在算子层抠几个百分点。

2. **Speculative decoding 的工程方向正在从“多调参”转向“少旋钮 + 更确定的匹配语义”。** SGLang 把 Ngram 匹配从窗口限制改成所有 suffix 匹配，长期看更利于长上下文和复杂前缀场景下的稳定表现。

3. **Scheduler correctness 修复的价值不低于性能优化。** `prefill-only` / `generation` 混合 batch 这种问题，表面上只是一个 flag 没更新，实质上会直接污染 decode 调度、idle 检查和 KV cache 生命周期管理。

4. **异构后端必须纳入主回归矩阵，而不是“有空再看”。** ROCm import failure、CPU fused MoE activation 缺口、Adreno OpenCL 对象泄漏，这些问题都会在真实部署时把系统可用性直接打穿。

5. **边缘设备基准先要“可信”，再谈“更快”。** llama.cpp 的 Adreno 修复说明，如果对象生命周期没管好，`bench` 数字甚至可能比真实 completion 更乐观或更悲观，导致错误的优化判断。

## 明日跟踪建议

1. 跟进 **TensorRT-LLM DWDP** 是否很快补更多 benchmark，尤其是 DeepSeek / Mixtral / MiniMax 类 MoE 模型在不同 batch、不同 imbalance 情况下的吞吐和延迟数据。

2. 跟进 **SGLang 的 MiniMax-M2.5 fp8 routed MoE 路径** 是否推广到更多 routed MoE 模型，以及 FlashInfer 侧 autotune blocker 解决后能否继续抬高收益。

3. 跟进 **SGLang scheduler** 后续是否继续围绕 `prefill-only`、`max_new_tokens=0`、logprob-only request、mixed batch 等组合场景补回归用例。

4. 跟进 **vLLM 的 CPU / ROCm 路径** 是否继续出现配套补丁；如果接下来还有 activation、kernel coverage 或 import/load 层面的修复，说明非 CUDA 路径仍处在快速收口期。

5. 跟进 **llama.cpp 的 Adreno / Hexagon 后端** 是否很快给出更可信的 benchmark 或端侧样例；没有数字前，这些修复和新 op 更适合视为“能力到位”，还不能算“性能已兑现”。
