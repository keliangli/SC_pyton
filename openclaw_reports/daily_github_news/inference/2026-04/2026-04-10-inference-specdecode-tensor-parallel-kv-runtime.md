---
title: "GitHub 大模型推理日报（2026-04-10）- CPU SpecDecode、张量并行与 KV 运行时收口"
date: 2026-04-10
track: 大模型推理
slug: specdecode-tensor-parallel-kv-runtime
source_report: /home/li/.openclaw/workspace/reports/github_inference_news_2026-04-10.md
repo_path: openclaw_reports/daily_github_news/inference/2026-04/2026-04-10-inference-specdecode-tensor-parallel-kv-runtime.md
generated_by: openclaw
---

# GitHub 大模型推理日报（2026-04-10）

> 统计窗口：过去 24 小时（截至 2026-04-10 14:50 Asia/Shanghai / 06:50 UTC）  
> 筛选口径：只保留有实质技术更新的 release / 重要 commit / 新功能 / 性能优化 / 关键正确性修复。

## 今日要点

1. **过去 24 小时的主线很明确：多卡/分布式推理开始从“功能拼装”进入“系统级收口”。** TensorRT-LLM v1.3.0rc11 同时推进了 gen-first disaggregated scheduling、MoE inference 的 DWDP、AutoDeploy Triton paged attention、MLIR 自动生成 elementwise fusion；llama.cpp 则把 experimental backend-agnostic tensor parallelism 合进主干，说明开源推理栈都在往更统一的多卡运行时走。

2. **CPU 与异构推理继续往前推。** vLLM 给 draft-model speculative decoding 补齐了 CPU 路径，把原本更偏 GPU 的加速手段带到了 CPU serving；LMDeploy 则把 cache manager block size 与 kernel block size 解耦，避免大 block 直接撞上 Triton shared-memory 上限。

3. **KV/缓存边界正确性还是高频风险面。** SGLang 今天修的是 SWA eviction boundary 与 chunked prefill 的页对齐问题，属于典型“平时不显眼、一出事就变成负 usage / double-free / 长上下文异常”的系统 bug；LMCache 则继续把 MLA 多 worker 下的缓存请求风暴压下去。

4. **本地/边缘推理 backend 仍在快速进化。** llama.cpp 同一天合入 Vulkan Q1_0 支持与 CUDA fused muls；前者扩大了低比特量化在 Vulkan 路径的可用性，后者在 Gemma4 上给出约 1.03x-1.06x 的预填充侧收益，说明“本地 inference 的热路径优化”远没有见顶。

## 项目速递（含链接）

- **vLLM：CPU draft-model speculative decoding 正式落地**
  - 关键变化：为 CPU 路径补齐 Triton kernel 的 PyTorch fallback，让 draft model speculative decoding 能在 CPU worker 上工作。
  - 已披露结果：在 AMD EPYC 9654 上，用 `Qwen3-32B + Qwen3-1.7B` 组合测试时，PR 给出的结论是 **TTFT 基本持平（高并发下略有波动），但 TPOT 更优，输出 token throughput 与总 token throughput 在各并发档位整体更高**。
  - 工程含义：这不是“小修 CPU 兼容性”，而是把 spec decode 真正推进到 CPU/低成本部署面，后面很值得看 acceptance rate、调度开销和 NUMA 亲和性会不会继续优化。
  - 链接：
    - Commit: https://github.com/vllm-project/vllm/commit/445a2a4d1a3a383a1a36da8acb7800bb85edabeb
    - PR: https://github.com/vllm-project/vllm/pull/32662

- **TensorRT-LLM：v1.3.0rc11 把 AutoDeploy / MoE / disagg / KV cache 多条主线一起推进**
  - 关键变化：本次 release highlights 很密集，直接点名了 **Mistral/Mixtral sliding window attention、MoE inference 的 DWDP、gen-first disaggregated scheduling、AutoDeploy Triton paged attention、MLIR-based auto-generated elementwise fusion、dense GEMM backend for MoE**，同时补了一串 disaggregated serving / KV cache 相关 hang 与计数错误修复。
  - 同窗口的重要 commit：Qwen3.5 MoE AutoDeploy 路径新增 **`lm_head` sharding**，并打开 **TP8 MoE + NVFP4** 相关支持，明显是在朝“大模型多卡高吞吐部署”继续收紧。
  - 工程含义：TensorRT-LLM 最近不是单点提速，而是在把 compiler、runtime、KV cache manager、disagg 调度和 MoE 并行策略一起主线化，节奏很猛。
  - 链接：
    - Release: https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc11
    - Qwen3.5 perf commit: https://github.com/NVIDIA/TensorRT-LLM/commit/19363670eb5b347ff33e20346d396035213a83a2
    - Qwen3.5 perf PR: https://github.com/NVIDIA/TensorRT-LLM/pull/12265

- **SGLang：修 SWA eviction boundary，并把 chunked prefill 对齐到页边界**
  - 关键变化：当 `page_size > sliding_window_size` 时，原逻辑可能把 SWA frontier 直接推到 `page_floor(seq_len)`，导致“将要插入的 token 其实已经全被驱逐”，后续又继续建 node，进而引出 **negative usage** 与潜在 **double-free**。这次 PR 同时做了预防式和防御式修复。
  - 额外值得注意：同一窗口里，SGLang 还给 gRPC mode 补上了 **Prometheus `/metrics` endpoint**，说明可观测性也在被正式纳入服务面。
  - 工程含义：长上下文 + sliding window + chunked prefill 这条线，最怕的就是页边界/回收边界不一致；SGLang 这次修复很典型，也很有参考价值。
  - 链接：
    - SWA fix commit: https://github.com/sgl-project/sglang/commit/722e25a621300b9f6d8f16d51ad19eadc67626a1
    - SWA fix PR: https://github.com/sgl-project/sglang/pull/22470
    - gRPC metrics commit: https://github.com/sgl-project/sglang/commit/89553ff82bfc1b4c6bb960ef9151ebf2bc398368

- **LMDeploy：cache manager block size 与 kernel block size 解耦**
  - 关键变化：此前当 `cache-block-seq-len >= 128` 时，Triton paged attention kernel 可能直接撞上 shared-memory overflow。这个 PR 引入 `manager_block_size` 与 `kernel_block_size` 两套视角：**Block Manager 按管理粒度调度，Kernel 按执行粒度分配与读取**，中间通过 block-id 映射打通。
  - 工程含义：这是非常值得借鉴的 runtime 设计。Prefix cache / block manager 需要较粗粒度，不代表底层 kernel 也必须跟着放大；把“管理粒度”和“执行粒度”拆开，很多系统约束会一下子松很多。
  - 链接：
    - Commit: https://github.com/InternLM/lmdeploy/commit/9f33332a8cc306447ffac3996d714cb703898426
    - PR: https://github.com/InternLM/lmdeploy/pull/4421

- **llama.cpp：experimental backend-agnostic tensor parallelism 合入主干**
  - 关键变化：通过新增一个“meta backend”包装多个 ggml backend，让框架按 compute graph 自动推断张量切分位置，并只在必要点同步，而不是像旧 `row` 模式那样几乎每步都强同步。
  - 当前状态：作者明确说明它还 **不算 production ready**，但 CUDA + NCCL 已经能跑出比 `--split-mode layer` 更有竞争力的结果，而且 **上下文越长，收益越明显**。
  - 工程含义：这说明 llama.cpp 也开始从“本地单机推理工具”往更完整的多 GPU runtime 走，后续如果 CUDA graph、非 CUDA backend 和 stability 补齐，会是很危险的竞争者。
  - 链接：
    - Commit: https://github.com/ggml-org/llama.cpp/commit/d6f3030047f85a98b009189e76f441fe818ea44d
    - PR: https://github.com/ggml-org/llama.cpp/pull/19378

- **llama.cpp：同日继续推进 Vulkan 低比特量化与 CUDA 热路径融合**
  - 关键变化一：Vulkan backend 新增 **Q1_0** 支持，覆盖 `get_rows / set_rows / mul_mat(id)` 等关键路径，意味着更激进量化开始进入 Vulkan 实战面。
  - 关键变化二：CUDA backend 新增 **mul fusion**。作者给的 Gemma4 数据显示，预填充侧大致有 **1.03x-1.06x** 提升，说明这类“少一次 global memory roundtrip”的小 fusion 仍然很值钱。
  - 工程含义：边缘/本地 inference 不只是“模型更小”，而是 backend 越来越像正经 serving runtime：量化格式、kernel fusion、后端并行都在补。
  - 链接：
    - Vulkan Q1_0 commit: https://github.com/ggml-org/llama.cpp/commit/7b69125331d7a69c6ea6349f33f506247bc66127
    - Vulkan Q1_0 PR: https://github.com/ggml-org/llama.cpp/pull/21539
    - CUDA fuse muls commit: https://github.com/ggml-org/llama.cpp/commit/e34f0421544b42cae1a03bab528f571cf49814b0
    - CUDA fuse muls PR: https://github.com/ggml-org/llama.cpp/pull/21665

- **LMCache：MLA 打开后，多 worker 的 store 请求开始去重**
  - 关键变化：在 MLA 场景下，多 worker 其实不需要把同一份 `store`/`retrieve` 请求都发一遍；这次 PR 先处理 `store`，把 multiprocess 缓存请求的 fan-out 压下去。
  - 工程含义：这类优化不一定直接体现在 token/s，但会直接改善多进程 cache server 的请求风暴、锁竞争和协调成本，是典型“系统吞吐隐藏项”。
  - 链接：
    - Commit: https://github.com/LMCache/LMCache/commit/06981d6a31e9564181e63d151d021895809bbf8d
    - PR: https://github.com/LMCache/LMCache/pull/2935

## 工程启发

1. **多卡 inference 的下一阶段，不是继续堆单点 kernel，而是统一 graph / cache / scheduler / parallel runtime 的系统边界。** 今天 TensorRT-LLM、llama.cpp、SGLang 都在证明这一点。

2. **cache block 的“管理粒度”与“执行粒度”应该分离。** LMDeploy 这次做法很值得抄：prefix cache 命中率、block manager 调度颗粒度、kernel shared-memory 上限，本来就是三套不同约束，硬绑在一起迟早出问题。

3. **CPU spec decode 的价值被明显低估了。** 只要 acceptance rate 不太差，它对低成本部署、边缘节点、异构 fallback，甚至离线批处理都可能很有吸引力。

4. **长上下文系统最怕边界条件错位。** 页对齐、驱逐边界、KV 生命周期、worker fan-out 这些地方，一旦定义不清，线上表现往往不是“略慢”，而是直接错、漏、挂。

5. **本地 inference 的优化空间还很多。** Vulkan Q1_0、CUDA mul fusion 这种看起来“偏 backend 细节”的改动，最后都会直接反映到边缘部署的成本/延迟曲线上。

## 明日跟踪建议

1. 跟进 **vLLM CPU speculative decoding** 后续是否补出更完整 benchmark 表（不同并发、不同 draft ratio、不同模型组合）以及 CPU 热点分析。

2. 跟进 **TensorRT-LLM rc11** 里几条最值得盯的主线：AutoDeploy Triton paged attention、MoE DWDP、gen-first disagg scheduling、MLIR fusion，看看有没有新的端到端吞吐/延迟数字释出。

3. 跟进 **SGLang SWA/page-align 修复** 是否带来后续回归或进一步的 long-context cache 管理重构；这类 bug 通常不会只修一处就彻底干净。

4. 跟进 **LMDeploy block-size 解耦** 是否扩展到更多 kernel/backend，并观察这套“manager vs kernel”二层粒度设计会不会被其他推理框架借鉴。

5. 跟进 **llama.cpp tensor parallel** 后续是否尽快解决 CUDA graph 的 VRAM 问题，以及 Vulkan / ROCm / Metal 等非 CUDA backend 的可用性与性能数据。
