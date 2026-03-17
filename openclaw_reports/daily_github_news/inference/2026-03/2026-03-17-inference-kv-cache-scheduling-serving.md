---
title: "GitHub 大模型推理日报（2026-03-17）- KV Cache、调度与服务指标进展"
date: 2026-03-17
track: 大模型推理
slug: kv-cache-scheduling-serving
source_report: /home/li/.openclaw/workspace/reports/github_inference_news_2026-03-17.md
repo_path: openclaw_reports/daily_github_news/inference/2026-03/2026-03-17-inference-kv-cache-scheduling-serving.md
generated_by: openclaw
---

# GitHub 大模型推理日报（2026-03-17）

## 今日要点

1. **过去 24 小时的推理主线，不是大版本 release，而是“KV cache 正确性 + 调度冷启动 + 服务可观测性”继续收紧。** 这类更新不一定抢 headline，但都直接影响线上可用性：要么避免 cache/accounting 算错，要么减少首请求抖动，要么补齐服务侧指标与错误传播。
2. **vLLM 今天最值得看的是两条 KV cache 修正。** 一条是在 `TRTLLM fp8 dequant kernel` 中补上 **non-contiguous KV cache** 支持，说明它开始更认真地兼容跨层统一/非连续布局；另一条是修复 **multiple KV-cache groups** 下的最大显存占用估算，把原先“只看第一组 spec”改成“对所有 group 求和”，这属于典型的容量预算正确性补丁。
3. **SGLang 的更新集中在“把分布式/分层缓存系统变稳”。** 一方面新增 **NCCL/RCCL pre-warm**，目标非常明确：直接压低多卡首请求的 P99 TTFT 冷启动尖峰；另一方面修复 **scheduler idle 时 write-through 事件不处理** 的问题，并在 PD disaggregation decode 侧强制要求配置 `hicache-storage-backend`，避免把解码侧 KV offload 路径配成“逻辑打开、后端缺失”的半失效状态。
4. **TensorRT-LLM 今天是“内核路径 + 服务指标”双线推进。** 它一边给 **Trtllm-Gen attention backend** 正式接入 KV cache，一边把 **DeepSeek-V3.2 NVFP4** 路径里的 `indexer.wk` 从 attention GEMM 中拆出来，以便短上下文 skip / FP8 KV cache / 精度回归更可控；同时还把 **energy metrics** 打进 `trtllm-serve` 和 benchmark，开始把“性能”扩展到“能耗”维度。
5. **Ollama 今天最有技术含量的是 MLX 调度器能力补齐。** 新提交把 **MLX 模型纳入与普通 LLM 一致的 fit / eviction 决策链**，不再把 MLX 作为一条旁路 runner；再配合修复 `allocModel` graph reservation 报错被吞的问题，说明它正在补 Apple/MLX 路径上的调度可靠性，而不仅仅是做桌面端功能堆叠。

## 项目速递（含链接）

- **vLLM：TRTLLM FP8 dequant kernel 支持 non-contiguous KV cache**  
  变更点：在 `vllm/v1/attention/backends/flashinfer.py` 中引入更细的源/目标 stride 参数，并新增 400+ 行单测，覆盖 contiguous 与 cross-layer unified 的 non-contiguous KV cache 布局。这个改动的意义不在“多了个 case”，而在于 **KV cache 布局从默认连续，扩展到真正可兼容更复杂的统一分页/跨层组织方式**。  
  链接：https://github.com/vllm-project/vllm/commit/6c1cfbad325067c4afa12c87992f45a58ce0614b

- **vLLM：修复 multiple KV-cache groups 下的最大显存占用估算**  
  变更点：`_max_memory_usage_bytes_from_groups()` 从“取首个 group 的 max usage”改为“对所有 KV cache group 的 block 需求求和”，并补了包含 `MambaSpec` 的测试。它解决的是 **多组 cache/speculative/mamba 混合场景下显存预算低估** 的问题。  
  链接：https://github.com/vllm-project/vllm/commit/45f526d65237d9073a5f3be166b306580687f210

- **SGLang：NCCL/RCCL pre-warm，直接瞄准多卡冷启动 P99 TTFT**  
  变更点：在 model runner 初始化阶段增加一次 communicator 预热 `all_reduce`，并新增 `--pre-warm-nccl` 参数（AMD/HIP 默认开启）。这是很典型的 **把首次请求冷启动成本前移**：牺牲一点启动时初始化，换取在线首请求尾延迟更平滑。  
  链接：https://github.com/sgl-project/sglang/commit/943f34f6426f5801e483bd68cfd02d23271692b3

- **SGLang：修复 scheduler idle 时 HiCache write-through 事件不被处理**  
  变更点：把 `tree_cache.check_hicache_events()` 前移到 idle / 无 batch 的路径，避免 decode/prefill 队列为空时 write-through ack 一直不被消费。这个 patch 虽小，但本质上是在修 **分层缓存系统的事件驱动死角**。  
  链接：https://github.com/sgl-project/sglang/commit/079a1fd35e8d13c20f474f76f9fc2dca9ed51e29

- **SGLang：PD disaggregation 的 decode 侧 KV offload 增加配置硬校验**  
  变更点：当开启 `disaggregation-decode-enable-offload-kvcache` 时，若未提供 `hicache-storage-backend` 直接抛错。它不提升 benchmark 数字，但能避免 **decode 侧 cache offload 进入“开关已开、后端没配”的隐性错误状态**。  
  链接：https://github.com/sgl-project/sglang/commit/855ec7017d430f196a4f5da6123399b1f67c10c6

- **TensorRT-LLM：Trtllm-Gen attention backend 正式接入 KV cache**  
  变更点：涉及 `attentionOp`、`trtllm_gen.py`、TH op 和 KV block array 构建逻辑的大改，新增专门的 `trtllmGenQKVProcessOp.cpp`。这说明 **Trtllm-Gen 不再只是“无 cache / 轻 cache”的独立路径，而是在向生产级 attention backend 对齐**。  
  链接：https://github.com/NVIDIA/TensorRT-LLM/commit/5003d383e3305e7b96fb386a8083975bcd2352ae

- **TensorRT-LLM：DeepSeek-V3.2 NVFP4 路径把 `indexer.wk` 从 attention GEMM 中拆出**  
  变更点：`forward_impl_with_dsa()` 不再把 `indexer_k` 与 `kv_a_proj_with_mqa` 一起融合，而是延后 indexer 投影，配套补上 NVFP4 + FP8 KV cache 的精度测试。这个方向很关键：**把融合边界收窄，换取短上下文 skip、量化组合和精度回归更可控**。  
  链接：https://github.com/NVIDIA/TensorRT-LLM/commit/2f45640c19910eff463b4d65b8f2b0345cdeff9e

- **TensorRT-LLM：`trtllm-serve` 与 benchmark 开始内建 energy metrics**  
  变更点：把 NVML energy monitor 下沉到公共工具层，新增 `enable_energy_metrics`，服务侧暴露 `/energy_metrics` 端点，benchmark 侧也能直接统计 Joules。对推理团队来说，这等于开始把 **吞吐/延迟/显存** 之外的 **能耗** 纳入一线指标体系。  
  链接：https://github.com/NVIDIA/TensorRT-LLM/commit/a064a9b99579930ba9b72259d2662b1c14b5071c

- **Ollama：MLX 模型纳入统一 fit / eviction 调度链**  
  变更点：`sched.go` 不再把 MLX / image generation 作为旁路 `loadMLX()` 处理，而是在统一 `load()` 流程里做 metadata / 显存估算 / requireFull 检查；`x/mlxrunner/client.go` 与 `x/imagegen/server.go` 也改成先构造、后 `Load()`，支持在启动子进程前判断是否需要 eviction。核心价值是：**MLX runner 首次拥有与普通模型一致的调度/驱逐语义**。  
  链接：https://github.com/ollama/ollama/commit/bbbad97686205cfd897a9e4e931889a3598a0652

- **Ollama：修复 graph reservation 错误被吞，避免模型分配失败静默化**  
  变更点：`allocModel()` 里 `reserveWorstCaseGraph(true)` 失败时，原先错误被直接吞掉，现在改为向上返回。这种 patch 很小，但对线上排障价值很高：**模型图预留失败终于会变成显式错误，而不是“看起来没事，实际上没分到”**。  
  链接：https://github.com/ollama/ollama/commit/810d4f9c22319491cd3ac360afed6d2cae6be99a

## 工程启发

1. **KV cache 正在从“有就行”转到“布局正确、容量算准、后端一致”。** vLLM 今天两条更新都在打这个点：一条解决复杂布局兼容，一条解决多 group 容量预算；TensorRT-LLM 则把 KV cache 接进 Trtllm-Gen attention backend。结论很明确：**未来缓存系统的竞争点，会越来越偏向 layout/allocator/accounting，而不是单纯的 cache 命中率故事。**
2. **冷启动尾延迟终于开始被当成一等公民处理。** SGLang 直接预热 NCCL/RCCL communicator，本质上是在承认“多卡首请求抖一下”不是小问题，而是会直接破坏线上体验的 P99 事件。后面无论是 vLLM、TensorRT-LLM 还是自研服务，**都值得把 communicator / graph / kernel cache pre-warm 系统化。**
3. **推理服务指标体系正在从“快不快”扩展到“耗不耗电”。** TensorRT-LLM 把 energy metrics 暴露到服务端点，说明成熟推理栈已经开始把 **TPS、TTFT、TPOT、显存占用、能耗** 放到同一个面板里看。对做工程选型的人，这比单跑 throughput benchmark 更接近真实生产评估。
4. **异构后端真正难的不是“能跑”，而是“调度语义要一致”。** Ollama 的 MLX 调度改造很说明问题：如果 Apple/MLX 路径永远靠特殊分支处理，就很难拥有稳定的 fit / eviction / 报错行为；一旦纳入统一调度链，后续才有可能把不同后端的资源管理做成同一套语言。

## 明日跟踪建议

1. 继续盯 **vLLM non-contiguous KV cache** 后续是否马上补更多 backend/benchmark，特别是 unified KV layout 对长上下文、多层共享分页的实际收益。
2. 跟踪 **SGLang NCCL/RCCL pre-warm** 会不会很快放出更明确的 cold-start TTFT 对比数据，尤其是 AMD 多卡场景下 P95/P99 改善幅度。
3. 关注 **TensorRT-LLM Trtllm-Gen + KV cache** 是否会追加针对 FP8 / FP4 KV cache、speculative decode、DSA/MLA 的性能或精度数据；这条线很可能会继续演化成更主流的 serving backend。
4. 继续观察 **energy metrics** 会不会从 TensorRT-LLM 扩散到其他推理框架；如果 vLLM / SGLang 也跟进，说明“能耗可观测”会成为推理基础设施标配。
5. 看 **Ollama MLX eviction** 是否很快补更多资源回收/并发加载案例；如果后续继续沿这个方向推进，Apple 端本地推理的调度成熟度会明显提升。
