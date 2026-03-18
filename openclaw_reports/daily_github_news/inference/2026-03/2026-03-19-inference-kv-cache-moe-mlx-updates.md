---
title: "GitHub 大模型推理日报（2026-03-19）- KV Cache、MoE 内核与 MLX 量化链路进展"
date: 2026-03-19
track: 大模型推理
slug: kv-cache-moe-mlx-updates
source_report: /home/li/.openclaw/workspace/reports/github_inference_news_2026-03-19.md
repo_path: openclaw_reports/daily_github_news/inference/2026-03/2026-03-19-inference-kv-cache-moe-mlx-updates.md
generated_by: openclaw
---

# GitHub 大模型推理日报（2026-03-19）

## 今日要点

1. **过去 24 小时的大模型推理主线，明显在往“KV cache / offload 正确性 + MoE 特化内核 + 本地 MLX 量化链路”三个方向收敛。** 不是那种只改文档或杂项修补，而是直接碰缓存布局、router kernel、量化导入与运行时稳定性的工程更新。
2. **vLLM 今天最值得盯的是 KV offload 与 GPT-OSS MoE 两条线同时推进。** 一条把 `GPULoadStoreSpec` 扩成支持 multiple KV groups 和逻辑 block index，对异构/分组缓存搬运更关键；另一条则连续上了 GPT-OSS Router GEMM 特化内核，以及 MXFP4/MXFP8 MoE 路径去掉前向 padding / slicing 的优化。
3. **SGLang 的有效更新集中在 PD disaggregation 的稳定性。** `ensure_prefill_info()` 加入按 bootstrap 地址节流的 retry interval，不再在 decode 侧无脑高频重试，这对分离式 prefill/decode 部署的尾延迟和失败放大都更友好。
4. **TensorRT-LLM 的 `v1.3.0rc8` 是今天最完整的一次“成体系 release”。** 里面同时覆盖 KVCacheManagerV2 的基础 SSM 支持、KV event batching、动态 speculative draft length、FusedMoE/DSA kernel 优化、Qwen3.5 性能优化，说明它在把缓存、投机解码、MoE 和 kernel/tooling 一起往前推。
5. **Ollama 今天的技术含量主要来自 Apple/MLX 路径补齐。** 一边支持把预量化 safetensors（先从 Qwen3.5 开始）直接导入 `ollama create`，另一边给 MLX runner 引入 quantized embedding、tied output projection 和 fast SwiGLU；这意味着本地推理不再只是“能跑”，而是在补模型导入和算子路径的完整性。

## 项目速递（含链接）

- **vLLM：KV offload 支持 multiple KV groups**
  - 变更点：`GPULoadStoreSpec` 新增 `group_sizes` 与 `block_indices`，并在 offloading scheduler 里显式按 group 构造 GPU load/store spec。
  - 技术意义：这不是简单的接口改名，而是在为 **多组 KV cache / 分组 offload / 非对齐块搬运** 补足描述能力，避免 CPU↔GPU KV 迁移只适配单一连续布局。
  - 链接：https://github.com/vllm-project/vllm/commit/5dd8df070172ac20e99a7dbd3d96cb6b054f0f57

- **vLLM：新增 GPT-OSS Router GEMM 特化 CUDA kernel**
  - 变更点：新增 `gpt_oss_router_gemm.cu/cuh`、torch binding 和 benchmark；针对 GPT-OSS 的 `num_experts in {32,128}`、`hidden_size=2880`，在 Hopper/Blackwell 上走专门的 bf16 router GEMM 路径。
  - 技术意义：MoE 的 router 计算原来常被当作“小矩阵边角料”，现在开始被单独做 kernel specialization。对于 GPT-OSS 这类专家数固定、形状稳定的模型，这通常意味着 **路由阶段的算子开销与调度抖动会继续下降**。
  - 链接：https://github.com/vllm-project/vllm/commit/b1169d7be8add20ab1db4bc93c2b5c6336ef9754

- **vLLM：GPT-OSS 的 FlashInfer MXFP4/MXFP8 MoE 去掉前向 padding / slicing**
  - 变更点：为 `SM100_FI_MXFP4_MXFP8_TRTLLM` backend 增加 `skip_forward_padding` 能力，量化时显式指定 `alignment=256`，并允许直接写回原始未 padding 的输出 buffer。
  - 技术意义：这类 patch 看起来不大，但本质是在减少 **前向额外内存流量与张量整形开销**。对高频 decode / MoE token path 来说，这种“少一次 pad + 少一次 slice”通常比纸面代码改动更值钱。
  - 链接：https://github.com/vllm-project/vllm/commit/296839a1b07e63daecca67bfce80375614b5b863

- **SGLang：PD disaggregation 的 `ensure_prefill_info()` 加入 retry interval**
  - 变更点：decode 侧新增 `_ensure_last_attempt_time` 与 `_ensure_retry_interval=1.0s`，同一 bootstrap 地址在短时间内不再反复 `try_ensure_parallel_info()`；最大重试次数也从 30 个 scheduling cycles 降到 20。
  - 技术意义：这在抑制 **prefill/decode 分离部署中的忙等重试、瞬时抖动与失败风暴**。如果你后面做 disaggregated serving，这种“按地址节流重试”很值得直接借鉴。
  - 链接：https://github.com/sgl-project/sglang/commit/8b46f1f4ecd22e08eb3e33e0665aecf5e43bd38b

- **TensorRT-LLM：发布 `v1.3.0rc8`，继续把 KV / speculative / MoE 一起往前推**
  - 变更点：release highlights 包含 **KVCacheManagerV2 基础 SSM 支持、KV event batching、动态 speculative draft length、FlashInfer API for TRTLLMGenFusedMoE、DSA indexer fused cat+fp8_quantize、Qwen3.5 性能优化** 等。
  - 技术意义：这不是单点补丁，而是一次典型的 **面向生产栈的成体系推进**：缓存管理、投机解码、MoE kernel、benchmark 和服务端接口一起演化，说明 TensorRT-LLM 正在把“高性能能力”打包成更完整的 serving 平台能力。
  - 链接：https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc8

- **Ollama：支持预量化 safetensors 直导入 `ollama create`，先打通 Qwen3.5**
  - 变更点：新增 `tensorImportTransform` 框架、`qwen35` 专用导入转换逻辑、source quant metadata 解析，以及预量化 companion tensors（scales/biases）的打包流程。
  - 技术意义：这让 **HF 标准权重** 和 **mlx-community 风格的预量化 safetensors** 能更直接进入 Ollama 的模型创建链路，减少“先转格式、再重打包”的工程损耗，对本地部署和边缘分发都更实用。
  - 链接：https://github.com/ollama/ollama/commit/fa69b833cd1323b2d96b80da9e38cadc7e8fe97a

- **Ollama：MLX runner 补齐 quantized embedding、tied output projection 与 fast SwiGLU**
  - 变更点：引入 `EmbeddingLayer` / `QuantizedEmbedding` 接口，多个模型（Gemma3、Llama、Qwen3、Qwen3.5、GLM4-MoE-Lite）切到统一 embedding 抽象，并让量化 embedding 可以直接复用为 tied LM head；同时补了额外 MLX ops 和 runtime 修正。
  - 技术意义：这一步很关键，因为它把 **量化 embedding → 推理 lookup → tied output** 串成一条完整链路，本地 Apple/MLX 路径终于不只是“线性层量化”，而是开始补齐模型结构级能力。
  - 链接：https://github.com/ollama/ollama/commit/d727aacd04e531db9fe2a797b31c032d626b69ef

## 工程启发

1. **KV cache 的竞争点已经从“有没有”转向“布局表达力够不够”。** vLLM 的 multiple KV groups、TensorRT-LLM release 里的 KVCacheManagerV2 / KV event batching，本质都在往更复杂、更生产化的缓存编排迈。后面做长上下文和异构内存分层时，`layout metadata + allocator/accounting + offload protocol` 会比单纯 cache hit rate 更关键。
2. **MoE 的下一个性能增量，越来越来自“小算子专门优化”。** GPT-OSS Router GEMM 特化、FlashInfer MXFP4/MXFP8 路径去 padding，说明真正拖慢线上 latency 的常常不是 attention 主体，而是 router、quantize、reshape、pack/unpack 这些“边缘热点”。
3. **分离式 serving 需要把 retry 设计成调度层能力，而不是请求层自旋。** SGLang 这次给 bootstrap 地址加 retry interval，解决的是工程上的“坏风暴”问题：失败时系统不要因为重试过快而把自己打爆。
4. **本地推理栈的门槛正在从“算子跑通”升级为“导入链路 + 权重格式 + 结构复用”一起成熟。** Ollama 这两条 MLX 更新非常说明问题：如果预量化权重不能直导、embedding 不能和 LM head 复用，最终还是会卡在模型适配上，而不是卡在理论算力上。

## 明日跟踪建议

1. 跟踪 **vLLM multiple KV groups** 后续是否继续扩展到更完整的 offload benchmark、跨层 unified KV layout 和异构内存场景；如果后续补 benchmark，参考价值会非常高。
2. 继续盯 **vLLM GPT-OSS Router GEMM** 是否很快给出实际吞吐/延迟收益数据，特别是小 batch decode 与大专家数场景下的增益。
3. 关注 **TensorRT-LLM v1.3.0rc8** 中与 KVCacheManagerV2、speculative decode、FusedMoE 相关的后续 issue/benchmark；release 已经放出方向，后面很可能继续补实测数字。
4. 观察 **Ollama 预量化导入** 会不会从 Qwen3.5 扩展到更多模型族，以及是否继续补模型转换校验与精度回归；这决定它能不能真正变成稳定的本地量化分发入口。
5. 跟踪 **SGLang PD disaggregation** 是否继续补更多 backoff / timeout / bootstrap observability 字段；如果补上，这条线会更适合作为分离式 serving 的工程参考样板。
