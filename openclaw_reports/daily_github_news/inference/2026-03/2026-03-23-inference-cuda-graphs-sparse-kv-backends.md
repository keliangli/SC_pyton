---
title: "GitHub 大模型推理日报（2026-03-23）- CUDA Graph、稀疏KV与多后端提速"
date: 2026-03-23
track: 大模型推理
slug: cuda-graphs-sparse-kv-backends
source_report: /home/li/.openclaw/workspace/reports/github_inference_news_2026-03-23.md
repo_path: openclaw_reports/daily_github_news/inference/2026-03/2026-03-23-inference-cuda-graphs-sparse-kv-backends.md
generated_by: openclaw
---

# GitHub 大模型推理日报（2026-03-23）

> 统计窗口：过去 24 小时（截至 2026-03-23 14:50 Asia/Shanghai / 06:50 UTC）  
> 筛选口径：只保留有实质技术更新的 release / 重要 commit / 新功能 / 性能优化 / 关键正确性修复。

## 今日要点

1. **CUDA Graph 正在从纯 decode 热路径扩展到更复杂的推理执行面。** vLLM 今天同时推进了 **pipeline parallel 场景下的 piecewise CUDA graph**，以及 **多模态 ViT encoder 的 full CUDA graph**，说明主流 serving 框架正在把 graph capture 从“单一路径加速”升级成“跨阶段、跨模态”的系统级优化。
2. **稀疏 KV / 分层缓存开始进入更工程化阶段。** SGLang 引入 **HiSparse**，把 host/device 分层 KV、top-k page swap-in、解码期 staging/ack 流程和 NSA sparse attention 连成一套，表明“只算重要 token、只换需要的页”正在从论文概念转向可运行的服务端实现。
3. **Blackwell / GB 系统的软件栈仍在快速修正确性细节。** SGLang 为 FlashInfer unified transport 在 GB200/GB300 上加临时规避，TensorRT-LLM 修 ADP 打开时的 KV token 估算偏大问题；这类更新虽然不花哨，但直接决定复杂并行配置能否稳定上线。
4. **多后端推理优化继续下沉到 kernel 细节。** llama.cpp 一天内同时推进了 **CUDA 原生 BF16 flash attention、OpenCL 的 Q4_K kernel 扩展，以及 SYCL 对 BF16/量化类型的放行**，说明本地/边缘推理框架的竞争点依然是“更多硬件路径可用 + 更低层热点打磨”。
5. **端侧后端开始更明确地区分“能跑”和“应该委托给硬件跑”。** ExecuTorch 在 Arm Ethos-U55 后端明确拒绝 INT16 matmul，把支持范围收窄到 int8，本质上是在用更严格的 operator support 边界换取可预测性和正确性。

## 项目速递（含链接）

- **vLLM：把 CUDA graph 从 decode 热路径扩展到 PP 和多模态 encoder**
  - 关键变化 1：`[Model Runner V2] Enable piecewise CUDA graphs for pipeline parallelism` 为非首个 PP rank 引入 persistent `intermediate_tensors`，并把 PP rank 间传递的中间张量纳入 graph capture / replay，使 pipeline parallel 不再默认退回 eager-only。
  - 关键变化 2：`[Feature] ViT Full CUDA Graph` 新增 `EncoderCudaGraphManager`、budget-based token capture、自动推断 token budgets / max images，以及 Qwen3-VL 等视觉编码器的 replay buffer 机制，把 vision encoder 前向也纳入 CUDA graph。
  - 判断：这不是单个 kernel 优化，而是 **graph capture 覆盖面在扩张**。后续多模态 serving、PP 场景的冷启动和 steady-state latency 都可能受益。
  - 链接：
    - https://github.com/vllm-project/vllm/commit/63f49b8bd46b477da384c2cdd6613bf45ed3d515
    - https://github.com/vllm-project/vllm/commit/f85e479e66167532feddc9aafd56562402def9d9

- **SGLang：HiSparse 落地，把 sparse attention、host/device 分层 KV 与 decode swap-in 串起来**
  - 关键变化：新增 `HiSparseCoordinator`、`HiSparseNSATokenToKVPool`、JIT kernel `load_cache_to_device_buffer`，在 decode 过程中按 top-k token / page 把 host 侧缓存页换入 device buffer，并与 NSA backend 的 top-k transform、scheduler staging、request 生命周期联动。
  - 判断：这条更新的价值在于 **把稀疏注意力从算子级优化推进到缓存/调度/生命周期一体化实现**，非常值得跟踪后续 benchmark。
  - 链接：
    - https://github.com/sgl-project/sglang/commit/13f4f010d8ea7fbf628cd3b5313a73cac6c0285e

- **SGLang：为 GB200/GB300 上的 FlashInfer unified transport 加安全兜底，规避数据损坏风险**
  - 关键变化：在 `flashinfer_comm_fusion.py` 中检测 aarch64 + sm10x（Blackwell/GB）组合，临时强制从 Fabric handle exchange 切回 PosixFD symmetric-memory handle exchange，并暴露 `SGLANG_FLASHINFER_FORCE_POSIX_FD_TRANSPORT` 开关。
  - 判断：这类 commit 直接反映 **新一代硬件平台 bring-up 期最真实的工程问题：不是“跑不跑得快”，而是“先别 silently corrupt data”**。
  - 链接：
    - https://github.com/sgl-project/sglang/commit/d8a5b1dbafc59fa82979a2ff6de4e44d88375299

- **TensorRT-LLM：修复 Attention DP 打开时的 KV token 估算偏差，避免每 rank 过度预留 KV cache**
  - 关键变化：在 `_get_token_num_for_estimation()` 中，当 `enable_attention_dp=True` 且 `tp_size>1` 时，把 dummy warmup request 复制导致的 cache block 总量按 TP rank 数均分；并补上 `test_kv_cache_estimation.py` 覆盖不同 TP 配置。
  - 判断：这条更新虽然改动面不大，但它影响的是 **KV cache 容量估算、warmup graph token 上限与显存预留**，属于生产环境非常关键的“隐性正确性修复”。
  - 链接：
    - https://github.com/NVIDIA/TensorRT-LLM/commit/9194e9e9f8962227475a420f06c2f92a80141867

- **llama.cpp：多后端并进——CUDA 补 BF16 FA，OpenCL 扩 Q4_K kernel，SYCL 放开 BF16/量化类型**
  - 关键变化 1：`ggml-cuda: native bf16 flash attention for vec kernel` 新增 BF16 的 K/Q dot、V dequantize 及 template instances，让 CUDA vector flash attention 支持 BF16 与多种量化 V/K 组合。
  - 关键变化 2：`opencl: add flattened Q4_K mv and general Q4_K mm` 新增 OpenCL 下的 `mul_mv_q4_K_f32_flat` 与 `mul_mm_q4_k_f32_l4_lm`，把 Q4_K 的 matvec / matmul 路径补齐到更可用状态。
  - 关键变化 3：`support bf16 and quantized type` 删除 SYCL backend 中对 BF16 与若干量化类型的硬编码拒绝条件，释放更多 oneDNN / SYCL 路径的可用性。
  - 判断：这组提交共同表明 **llama.cpp 仍在通过“更多类型 + 更多后端 + 更低层 kernel”扩大硬件覆盖面**。
  - 链接：
    - https://github.com/ggml-org/llama.cpp/commit/db9d8aa428012cc5593e18635d4c3c54095f5138
    - https://github.com/ggml-org/llama.cpp/commit/84ffd0c192b120495fd5eb7e922aa7e857304fb2
    - https://github.com/ggml-org/llama.cpp/commit/f40a80b4f3cd00c4c405c45b7f316f7e77352323

- **ExecuTorch：Arm Ethos-U55 收紧 matmul 支持边界，只接受 int8，明确拒绝 INT16**
  - 关键变化：`ethos_u55_support.py` 将 matmul 输入 dtype 支持从 `(torch.int8, torch.int16)` 收窄为 `torch.int8`，同时新增 / 重构大量测试样例，区分 2D mm、bmm、mul+sum fallback 以及 U55/U85 不同 delegate 行为。
  - 判断：这是典型的 **端侧后端 contract 收敛**：宁可少接一些 case，也要让 delegated / non-delegated 行为更稳定、结果更可预测。
  - 链接：
    - https://github.com/pytorch/executorch/commit/f7977a6c152d9498e6520de0d6c27c4f3f8e67a4

## 工程启发

1. **下一阶段的 CUDA graph 优化要按“执行面”来设计，而不只是按 kernel 来设计。** vLLM 已经把 PP 中间张量和视觉 encoder 都纳入 graph capture，说明后续自研推理框架若只优化 decode kernel，很容易落后于系统级调度优化。
2. **KV cache 的优化正在从“更省”走向“更会搬”。** SGLang 的 HiSparse 和 TensorRT-LLM 的估算修正都在提醒：KV 的容量、页粒度、交换时机、预估模型要单独建模，不能继续当成黑箱附属品。
3. **新硬件 bring-up 期必须把“数据正确性”放在 headline benchmark 前面。** GB 平台 transport workaround 就是典型例子；后续如果做 Blackwell / Grace-Blackwell 测试矩阵，建议优先覆盖 allreduce-fusion、symmetric memory、paged KV、FlashInfer 组合路径。
4. **多后端部署的真实门槛不在 API，而在 kernel completeness。** llama.cpp 一天内同时补 CUDA / OpenCL / SYCL，说明想要真正覆盖边缘、桌面、异构 GPU，必须持续把 BF16、量化 block format、matvec/matmul 这些底层组合补齐。
5. **端侧 delegate 的能力边界要显式写清。** ExecuTorch 对 U55 的收口很值得借鉴：比起模糊支持，不如明确哪些 dtype / op 组合走 delegate、哪些直接 fallback，这样测试矩阵和线上行为都更可控。

## 明日跟踪建议

1. 跟进 **vLLM** 是否很快补出 PP CUDA graph 与 ViT encoder CUDA graph 的公开 benchmark（吞吐、首 token 延迟、显存占用、graph hit rate）。
2. 跟进 **SGLang HiSparse** 是否出现首批性能数字，重点看长上下文 decode、host/device KV 命中率、swap-in 开销、与常规 NSA/HiCache 的对比。
3. 跟进 **SGLang GB transport workaround** 后续是否上游到 FlashInfer 或被更底层修复替代；若只是临时规避，需要持续观察是否影响带宽或尾延迟。
4. 跟进 **TensorRT-LLM ADP KV estimation 修复** 是否牵出更多 warmup / KV capacity / CUDA graph capture 相关修复，这通常意味着 ADP 仍在快速演进。
5. 跟进 **llama.cpp** 的 OpenCL Q4_K 路径是否马上补 benchmark；如果数字好看，这对非 CUDA 本地推理设备会是很实际的利好。
6. 跟进 **ExecuTorch Arm backend** 是否继续细化 U55/U85 的 operator support matrix，尤其是 A16W8、bmm 与 fallback 路径的划分。