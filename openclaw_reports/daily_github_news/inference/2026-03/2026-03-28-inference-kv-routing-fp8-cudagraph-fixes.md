---
title: "GitHub 大模型推理日报（2026-03-28）- KV 路由、FP8 与 CUDA Graph 修复"
date: 2026-03-28
track: 大模型推理
slug: kv-routing-fp8-cudagraph-fixes
source_report: /home/li/.openclaw/workspace/reports/github_inference_news_2026-03-28.md
repo_path: openclaw_reports/daily_github_news/inference/2026-03/2026-03-28-inference-kv-routing-fp8-cudagraph-fixes.md
generated_by: openclaw
---

# GitHub 大模型推理日报（2026-03-28）

> 统计窗口：过去 24 小时（截至 2026-03-28 14:50 Asia/Shanghai / 06:50 UTC）  
> 筛选口径：只保留有实质技术更新的 release / 重要 commit / 新功能 / 性能优化 / 关键正确性修复。

## 今日要点

1. **今天最强的主线是“KV 感知的调度/路由”开始进入推理服务核心路径。** TensorRT-LLM 在 24 小时内连续合入 FlexKV、KV cache-aware ADP router、request priority，说明调度层已经不满足于“排队发请求”，而是开始直接消费 cache 命中与优先级信息。
2. **FP8 / 低比特路径继续从“能跑”走向“能稳定跑”。** vLLM 修 Marlin float16 下的 NaN/Inf、把 TRTLLM MoE 的 pack-topk 用 torch.compile 做融合，又放开 FP8 KV cache 下跳过 sliding-window attention；LMDeploy 也在同一天修 Qwen3.5 FP8 支持，表明低精度推理仍在密集收口。
3. **SGLang 把 piecewise CUDA Graph 正式推到默认执行模式后，马上继续补 mixed-chunk 崩溃修复。** 这类节奏很重要：先把高收益路径默认打开，再追打稳定性问题，意味着项目已经把图执行当成主线能力而不是实验特性。
4. **缓存/稀疏/布局优化仍在继续下沉。** SGLang 的 HiCache page-first layout + MLA JIT kernel，不只是“多了个 kernel”，而是在改 host/device 分层缓存和热点 kernel 的数据布局。
5. **端侧异构后端依然值得盯。** llama.cpp 为 Hexagon 补 IQ4_NL 与 MXFP4，不是表面兼容性，而是直接往移动/嵌入式低比特推理的真实可用性推进。

## 项目速递（含链接）

- **SGLang：发布 v0.5.10rc0，Piecewise CUDA Graph 默认开启**
  - 关键变化：release note 明确把 **Piecewise CUDA Graph Enabled by Default** 列为第一亮点，同时还打包了 Elastic EP、HiSparse、FlashInfer MXFP8、Qwen3.5 GDN/KDA 优化、FA4 官方库支持等一批推理主线能力。
  - 判断：这不是普通 RC 打包，而是一次 **把图执行、稀疏注意力、MoE 容错和低精度 kernel 正式推进到可消费版本窗口** 的信号。
  - 链接：
    - https://github.com/sgl-project/sglang/releases/tag/v0.5.10rc0

- **SGLang：HiCache 支持 page-first layout，并补 MLA JIT kernel；随后修 mixed-chunk 下的 Piecewise CUDA Graph 崩溃**
  - 关键变化 1：`[Hicache & JIT_kernel] Support page first layout & mla jit kernel` 一次性修改 `hicache.cuh`、`hicache.py`、`memory_pool_host.py` 与测试，属于 600+ 行级别的大改。
  - 关键变化 2：`Fix Piecewise CUDA Graph crash with -enable-mixed-chunk` 直接修补默认图执行路径在 mixed chunk 场景下的稳定性。
  - 判断：这组提交一起看，说明 SGLang 正在 **同时推进缓存布局、JIT kernel 与 capture-safe correctness**，而不是只做单点算子优化。
  - 链接：
    - https://github.com/sgl-project/sglang/commit/d864622a682494b3332f6b850dc6115221db232c
    - https://github.com/sgl-project/sglang/commit/daf02bde3306863ca4478a905b9ffa90e9332dac

- **TensorRT-LLM：FlexKV、KV cache-aware ADP router、request priority 三连发**
  - 关键变化 1：`Add support for FlexKV` 把 FlexKV 接到 `llmRequest`、`kv_cache_connector` 与 pyexecutor。
  - 关键变化 2：`KV cache-aware ADP router for prefix-affinity request routing` 新增 `scheduler/adp_router.py` 和大批单测，把路由逻辑直接建立在 KV cache 感知之上。
  - 关键变化 3：`Adding support for request priority in LLM API` 为 waiting queue / executor / LLM API 补 priority 语义。
  - 判断：这不是孤立功能，而是在把 **“前缀亲和 + cache 命中 + 请求优先级”** 合并成更像生产系统的调度控制面。
  - 链接：
    - https://github.com/NVIDIA/TensorRT-LLM/commit/789494fcfe75d130a9c79cc781d9628426b51835
    - https://github.com/NVIDIA/TensorRT-LLM/commit/3318aca3f4cabf71a323c6e2868f6586817d03cb
    - https://github.com/NVIDIA/TensorRT-LLM/commit/069afcdced22d4bcb210be9345cf746fea58dadb

- **vLLM：围绕 FP8 / MoE / KV path 连续补性能与正确性**
  - 关键变化 1：`Use torch compile to fuse pack topk in trtllm moe`，修改 `trtllm_fp8_moe.py`、`trtllm_nvfp4_moe.py` 与 `fused_moe/utils.py`，直接落在 MoE 热路径。
  - 关键变化 2：`fix output Nan/Inf in marlin if dtype=float16`，涉及 Marlin quantization / MoE CUDA 代码与 Python util，属于高价值正确性修复。
  - 关键变化 3：`enable skipping of SW attention layers when using FP8 KV cache`，让 FP8 KV cache 与 sliding-window attention 的组合更可控。
  - 判断：vLLM 今天的重点很明确：**一边给低比特/MoE 热路径做融合，一边清理 FP8/float16 correctness 边角问题**。
  - 链接：
    - https://github.com/vllm-project/vllm/commit/b69bf2f0b170ac5b43f72f4dd4139c5388fa5de8
    - https://github.com/vllm-project/vllm/commit/148a5c1226f8668cb52c4900b5ff2c80344e78f2
    - https://github.com/vllm-project/vllm/commit/98e7f223b9fb03537adc856e594a34a3cd018536

- **LMDeploy：修复 Qwen3.5 FP8 支持，补齐模型定义、kernel 与 runtime quant 细节**
  - 关键变化：`fix qwen3.5 fp8 support` 一次性修改 `qwen3_5.py`、`qwen3_5_moe.py`、`gated_delta.py`、`causal_conv1d.py` 与对应测试，还显式提到 runtime quant / loader 修复。
  - 判断：这不是小 patch，而是在 **把 Qwen3.5 FP8 路径从“不稳定/不完整”往可用状态拉齐**。
  - 链接：
    - https://github.com/InternLM/lmdeploy/commit/d4e83e160eee52a66e103cbe8f2e042854cfc993

- **llama.cpp：Hexagon 后端补 IQ4_NL 与 MXFP4**
  - 关键变化：`hexagon: support for IQ4_NL and MXFP4` 新增 IQ4_NL quant type 支持、HVX vec_dot kernel，以及 MXFP4 HMX dequant path，同时统一 DMA fetch 路径里的量化 row/scale 逻辑。
  - 判断：这是很典型的 **端侧/异构后端底层补强**，对 Qualcomm/Hexagon 场景的低比特推理价值高于表面看起来的“多支持了两个格式”。
  - 链接：
    - https://github.com/ggml-org/llama.cpp/commit/ee051c1e4e6ceddc2fa516eb067496328ac1a2dd

## 工程启发

1. **调度器正在“读懂 cache”，而不只是管理队列。** TensorRT-LLM 今天的三条提交说明，后续 prefix-affinity、priority、FlexKV 这类能力会一起决定真实服务收益。
2. **低精度支持的门槛越来越像“系统工程”而不是单 kernel 优化。** vLLM 和 LMDeploy 的改动都覆盖模型定义、kernel、cache 路径与测试，说明 FP8/低比特要想真正上线，必须端到端收口。
3. **图执行默认开启之后，稳定性回归集必须升级。** mixed-chunk、spec decode、分块 prefill、异构 batch 这些组合，都应该单独成为 CUDA Graph 回归矩阵的一部分。
4. **缓存布局与 page 策略是下一波性能分水岭。** SGLang 的 page-first layout 说明热点已经从“有没有 cache”转向“cache 如何布局、如何换页、如何被 kernel 消费”。
5. **端侧后端不要只看 API 兼容，要看量化格式和 kernel completeness。** Hexagon 的 IQ4_NL/MXFP4 这类支持，才真正决定低比特模型能否落到移动/嵌入式设备上。

## 明日跟踪建议

1. 跟进 **TensorRT-LLM 的 KV-aware ADP router** 是否很快给出 prefix-affinity / 命中率 / 吞吐收益数据，以及与 request priority 叠加后的调度行为。
2. 跟进 **SGLang v0.5.10rc0** 发布后是否继续出现 piecewise CUDA Graph 的 hotfix；如果 RC 后连续补 crash/fallback，说明默认图执行仍在收口期。
3. 跟进 **vLLM 的 trtllm MoE torch.compile 融合** 是否补 benchmark，重点看 pack-topk 这类热点融合在不同 GPU / MoE 配置下是否稳定收益。
4. 跟进 **LMDeploy Qwen3.5 FP8** 是否补更多 e2e 验证，特别是 dense / MoE / hybrid attention 混合路径下的 correctness 和性能数字。
5. 跟进 **llama.cpp Hexagon IQ4_NL / MXFP4** 是否很快出现移动端 benchmark；没有数字前，这类后端支持还只能算“能力已接入”。
