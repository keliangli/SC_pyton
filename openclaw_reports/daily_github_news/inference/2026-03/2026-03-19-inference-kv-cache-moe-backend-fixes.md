---
title: "GitHub 大模型推理日报（2026-03-19）- KV Cache 正确性、MoE 内核与异构后端修补"
date: 2026-03-19
track: 大模型推理
slug: kv-cache-moe-backend-fixes
source_report: /home/li/.openclaw/workspace/reports/github_inference_news_2026-03-19.md
repo_path: openclaw_reports/daily_github_news/inference/2026-03/2026-03-19-inference-kv-cache-moe-backend-fixes.md
generated_by: openclaw
---

# GitHub 大模型推理日报（2026-03-19）

## 今日要点

1. **今天的有效更新主线，不是新版本 release，而是推理热路径的“正确性补洞 + 特化 kernel + 异构后端补齐”。** 过去 24 小时里，最有价值的改动大多直接落在 KV cache 量化比例、CUDA graph padding、MoE/router/top-k kernel，以及 CANN/ROCm/Blackwell 等后端实现上。
2. **KV cache 正确性今天非常值得重视。** vLLM 修掉了 fp8 MLA / FlashInfer 在 `kv_cache_dtype="auto"` 下因 scale 处理不一致导致的乱码输出；FlashInfer 则把 NVFP4 paged KV cache quantization 正式接到 SM100 路径，说明缓存精度与缓存格式已经成为核心竞争点。
3. **MoE / sparse attention 的性能优化继续往“小而关键的热点算子”深入。** SGLang 开始按 expert 数量切到更合适的 AMD router GEMM kernel；TensorRT-LLM 直接把 CuteDSL `indexer_top_k` 接进模型配置；这类变化虽然不一定体现在 headline feature 上，但往往直接影响 decode 热路径延迟。
4. **异构后端成熟度仍在快速拉开差距。** llama.cpp 在 CANN 上补齐“head dim 非 16 对齐”场景的 flash attention，并修复 ALiBi slope offset；这类底层兼容性修复，决定了新模型能否真正跑到更多设备上，而不是只在理想 shape 上可用。

## 项目速递（含链接）

- **vLLM：修复 fp8 MLA / FlashInfer 在 `kv_cache_dtype="auto"` 下的 KV scales 不一致，避免输出乱码**
  - 变更点：统一 `bmm1_scale` 计算逻辑，修正 MLA 后端中 q/k/v scale 处理不一致的问题，并补上针对不同 `kv_cache_dtype`、tensor parallel 规模与 block size 的测试。
  - 技术意义：这不是普通的数值微调，而是直接修复 **KV 反量化比例错误导致的生成结果失真**。对 FP8 KV cache、FlashInfer 后端和长上下文场景都很关键。
  - 链接：https://github.com/vllm-project/vllm/commit/577df69b26491aaa8f3fef2ea44d6ac256172032

- **vLLM：对 MLA attention 输出 buffer 做 zero-init，避免 CUDA graph padding 位置污染出 NaN**
  - 变更点：在 Cutlass MLA / FlashInfer MLA 路径中引入懒分配且显式 zero-init 的预分配输出 buffer，避免 capture/replay 场景下 padding slot 残留脏值。
  - 技术意义：这类 bug 很隐蔽，但一旦触发就是线上稳定性问题。它说明 **CUDA graph 兼容不仅是“能 capture”，还要保证 padding/token 对齐区域不会把脏数据带进后续计算**。
  - 链接：https://github.com/vllm-project/vllm/commit/ef2c4f778df5aa07a44e663330e2dfdc16927d2a

- **SGLang：继续优化 GPT-OSS / MoE decode 热路径，AMD 路由 kernel 选择更细化**
  - 变更点：`gpt-oss decode performance optimization` 这次大改把 `reshape_and_cache_flash` 等逻辑下沉到 Triton/后端实现里，减少 decode 阶段的 reshape/cache 开销；同时在 DeepSeek V3 路径中，当 expert 数量 `<=256` 时切到 `aiter_dsv3_router_gemm` kernel。
  - 技术意义：说明 SGLang 正在把优化重心放到 **decode 时的 KV cache 写入/整理** 和 **MoE router 小矩阵 kernel 选择** 上，这两块都比“主干 attention 再提一点”更贴近真实线上收益。
  - 链接：
    - https://github.com/sgl-project/sglang/commit/126cd5cfae7afbc9c7efb2b00dd52807ff17b842
    - https://github.com/sgl-project/sglang/commit/85fe8c6793a0b2bf8d5b2e98c88a8630515b0ac6

- **FlashInfer：为 SM100 新增 NVFP4 paged KV cache quantization 支持**
  - 变更点：新增 `nvfp4_quantize_paged_kv_cache`，并把 key/value block scales 接入 prefill、decode 与 TRTLLM FMHA 路径；benchmark 也同步补上 `nvfp4` 类型。
  - 技术意义：这一步很重要，因为它把 **低比特 KV cache 压缩** 从离散实验函数推进到更完整的运行时路径。对 Blackwell/SM100 上长上下文显存占用、带宽压力和 cache 容量都直接相关。
  - 链接：https://github.com/flashinfer-ai/flashinfer/commit/fc4e70fd67d8e60c5e24bd4ce576532a7849d38a

- **TensorRT-LLM：把 CuteDSL `indexer_top_k` 正式接进模型配置，推进 sparse attention / indexer 热点算子优化**
  - 变更点：新增 `single_pass_multi_cta_radix_topk` 内核与对应 custom op，在 `DeepSeekSparseAttentionConfig` 中暴露 `use_cute_dsl_topk` 配置，并把 indexer top-k 路径接入模型侧。
  - 技术意义：这说明 TensorRT-LLM 正在继续把 **稀疏注意力里的 top-k 选择** 从通用实现替换成更贴 Blackwell 的特化 kernel。对于 DSA / 稀疏 indexer，top-k 往往是不可忽视的延迟热点。
  - 链接：https://github.com/NVIDIA/TensorRT-LLM/commit/e940e58eb92c67c5fcad069c22469f605cdaabe3

- **llama.cpp：CANN 后端支持 head dim 非 16 对齐的 flash attention，并修复 ALiBi slope offset**
  - 变更点：去掉原先对 head dim 对齐的严格限制，修正 CANN 路径里 ALiBi slope buffer 的偏移处理。
  - 技术意义：这类改动虽然不如新模型支持显眼，但很实在：它提升了 **华为昇腾 / CANN 后端对更多模型 shape 的可用性与正确性**，减少“某些模型能编译但跑不准 / 跑不了”的尴尬。
  - 链接：https://github.com/ggml-org/llama.cpp/commit/07ba6d275b0f5c138c72f75d7f3df2661f17c27a

## 工程启发

1. **KV cache 已经从“存不存”演进到“怎么量化、怎么标定、怎么搬运还不出错”。** 今天 vLLM 和 FlashInfer 的更新都说明，缓存路径里的 scale、layout、block metadata 正在变成一等公民。
2. **推理性能的下一段增量，越来越来自 router/top-k/reshape/cache 这些边缘热点。** 如果只盯 attention GEMM，很容易错过真正影响 P99 的小算子。
3. **CUDA graph / 异构后端 / 低比特缓存三者叠加后，正确性比纸面性能更稀缺。** 后续做 benchmark 时，建议把 NaN、乱码、长上下文回归、不同 block size/TP 组合回归单独拉成测试矩阵。
4. **后端适配价值越来越高。** CANN、ROCm、Blackwell 这些路径一旦补齐关键 kernel 或 correctness fix，往往比再加一条“新模型支持”更能影响真实部署选择。

## 明日跟踪建议

1. 跟进 **vLLM FP8 MLA / FlashInfer KV scale 修复** 后续是否补 benchmark 或更多 regression case，尤其是长上下文与不同 TP 配置下的行为。
2. 跟进 **SGLang GPT-OSS decode optimization** 是否很快给出吞吐 / 延迟数字；如果补 benchmark，这条线的参考价值会非常高。
3. 跟进 **FlashInfer NVFP4 paged KV cache** 是否被更快接入上层框架（如 TensorRT-LLM / vLLM 的特定路径），以及是否补显存/速度对比。
4. 跟进 **TensorRT-LLM CuteDSL top-k** 是否扩展到更多 sparse attention / DeepSeek 变体，并观察其对 Blackwell 路径的实际收益。
5. 跟进 **llama.cpp CANN flash attention** 后续是否补更多 shape benchmark，尤其是非规则 head dim 场景下的精度与吞吐结果。
