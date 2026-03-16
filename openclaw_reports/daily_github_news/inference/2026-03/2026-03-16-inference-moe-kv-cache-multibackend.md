---
title: "GitHub 大模型推理日报（2026-03-16）- MoE 通信、KV Cache 与多后端演进"
date: 2026-03-16
track: 大模型推理
slug: moe-kv-cache-multibackend
source_report: /home/li/.openclaw/workspace/reports/github_inference_news_2026-03-16.md
repo_path: openclaw_reports/daily_github_news/inference/2026-03/2026-03-16-inference-moe-kv-cache-multibackend.md
generated_by: openclaw
---

# GitHub 大模型推理日报（2026-03-16）

## 今日要点

1. **过去 24 小时没有看到推理框架的大版本 release，主线是“MoE / KV cache / 多后端 / 分布式稳定性”继续往深处打。** 这不是表面功能堆料，而是把高吞吐、多卡、多模态、推测解码这些真正上线会疼的路径继续补齐。
2. **vLLM 今天最重磅的是 FlashInfer MoE A2A kernel 落地。** 它把原来的 `flashinfer_all2allv` 路径拆成 **NVLink one-sided / two-sided** 两套后端，并同步更新 EP 部署与 modular MoE 配置，属于典型的 **MoE 通信后端能力扩展**。同一窗口里，vLLM 还新增了 **XPU DeepSeek scaling RoPE fused kernel**，并把 **AMD Zen CPU + zentorch** 作为 in-tree backend 接进主线，说明它正在同时扩展 GPU 异构后端与 CPU serving 路径。
3. **SGLang 的更新集中在 cache 与 EPD 多模态。** 一条线是 **预计算 SWA cache location**，把 hybrid SWA 层与 piecewise CUDA graph 路径的 cache index 提前算好；另一条线是 **HiCache 在 decode 阶段及时释放 write-through lock_ref**，减少不可驱逐节点；再加上 **EPD/VLM 正式支持 video/audio input**，意味着它在“分离式推理 + 多模态”路径上走得更完整。
4. **llama.cpp 今天的变化依旧很工程：** CUDA 侧给 **GDN kernel** 做了 hide memory latency 的调度优化，同时对 **Flash Attention stream-k block 数量** 做上界控制，并且避免在 device init 阶段强行创建 CUDA context。整体指向很明确：**减少冷启动/调度副作用，把端侧与本地部署的运行时行为打磨得更可控。**
5. **TensorRT-LLM 与 LMCache 则继续补“生产级推理系统的边角”。** TensorRT-LLM 修了 **KV cache V2 在 separate draft KV cache（EAGLE3/MTP）下的 OOM 估算问题**，并让 **DSA attention 走 MLA custom op** 以兼容 `torch.compile`，同时给 **Qwen3-Next 打开 attention DP**；LMCache 则把 **PD backend 的 store / retrieve backend 解耦**，允许“从 PD 拿、往 Remote 存”的非对称配置，并给 **Valkey connector** 增加 database 选项。

## 项目速递

- **vLLM：FlashInfer MoE A2A kernel 落地，拆成 NVLink one-sided / two-sided 两套后端**  
  变更点：新增 `flashinfer_nvlink_one_sided` / `flashinfer_nvlink_two_sided`，把 EP/MoE all-to-all 路径从旧 alias 升级成更明确的后端模型，并同步接入 `fused_moe`、通信层和部署文档。  
  链接：https://github.com/vllm-project/vllm/commit/2754231ba3a72f41e62922d1552c33e8f3f6a9d1

- **vLLM：AMD Zen CPU backend via zentorch 进主线**  
  变更点：新增 `vllm[zen]`、`ZenCpuPlatform`、weight prepack 与 `zentorch_linear_unary` 路径，目标很直接——让 CPU serving 不只是“能跑”，而是把 AMD Zen 上的 GEMM/权重布局真正优化起来。  
  链接：https://github.com/vllm-project/vllm/commit/7acaea634c53c6786c04c97e39f9c169f5fbddf9

- **vLLM：XPU 增加 DeepSeek scaling RoPE fused kernel**  
  变更点：在 XPU 自定义 op 中注册 `deepseek_scaling_rope`，把 DeepSeek 这类位置编码路径下沉到 fused kernel。  
  链接：https://github.com/vllm-project/vllm/commit/68e1b711f1cfcc90c9e576cd1df3ec7bb3cb3e5d

- **SGLang：预计算 SWA cache location，直接打到 hybrid SWA + piecewise CUDA graph 路径**  
  变更点：把 `out_cache_loc_swa` 提前计算并在 `model_runner` / `piecewise_cuda_graph_runner` 里复用，减少 decode/replay 阶段重复转换。  
  链接：https://github.com/sgl-project/sglang/commit/39336f5812901b4af3f46b1a5752a7061e9d311e

- **SGLang：HiCache decode 路径释放 write-through lock_ref，提升可驱逐性与调度空间**  
  变更点：在 scheduler 中新增 `flush_write_through_acks()`，对完成 write-through 的 radix-tree 节点及时解锁，属于典型的 cache 生命周期正确性修复。  
  链接：https://github.com/sgl-project/sglang/commit/42f18fe560886ac83caada75a4e38e7d7bedbb2d

- **SGLang：EPD/VLM 支持 video/audio input**  
  变更点：从 encode server、tokenizer manager、multimodal processor 到 embedding cache controller 全链路扩展，正式把图像之外的 video/audio 模态接入 EPD-disaggregated inference。  
  链接：https://github.com/sgl-project/sglang/commit/135af6dc92aadbb226d111e4add0a757060fc10f

- **llama.cpp：CUDA GDN kernel 继续做延迟隐藏**  
  变更点：给 `gated_delta_net_cuda` 加 `launch_bounds`，并调整 `curr_state` 访问布局，目的就是更好地 hide memory latency。  
  链接：https://github.com/ggml-org/llama.cpp/commit/34818ea6c0e91a2fa245ce866f7e002a4a9cd381

- **llama.cpp：Flash Attention stream-k blocks 限流 + device init 避免强建 CUDA context**  
  变更点：前者按 KV cache 长度约束并行 block 上界，后者把 init 阶段的 `cudaMemGetInfo` / `cudaSetDevice` 副作用拿掉，更利于冷启动和多设备管理。  
  链接：https://github.com/ggml-org/llama.cpp/commit/ae40cd27c85aa30b9cd56033da1d6a954290f7ea ；https://github.com/ggml-org/llama.cpp/commit/ceef6b5233c3b31f454632c48fb42af16944bc5b

- **TensorRT-LLM：修复 separate draft KV cache 下的 KV cache V2 OOM（EAGLE3/MTP）**  
  变更点：把 draft model 的 layer 计数与 PP 分布逻辑算正确，避免 speculative decode / one-model drafter 场景 KV 预算失真。  
  链接：https://github.com/NVIDIA/TensorRT-LLM/commit/fc2bf2790d6e02e7028f0b51cf967f41d7df45f3

- **TensorRT-LLM：DSA attention 改走 MLA custom op，补 torch.compile 兼容性**  
  变更点：DSA 分支调用 `forward_impl_with_dsa()`，并补了一组 DeepSeekV3.2 NVFP4 / piecewise CUDA graph 测试。  
  链接：https://github.com/NVIDIA/TensorRT-LLM/commit/b72ee4fd89979bf280d3377a78d509a1243f278a

- **TensorRT-LLM：Qwen3-Next 打开 attention DP**  
  变更点：在 Qwen3-Next 权重映射、distributed op、linear reduce 路径与测试矩阵里加入 attention DP，直接提高这条模型线在多卡下的扩展弹性。  
  链接：https://github.com/NVIDIA/TensorRT-LLM/commit/677cdf673ae21120ba9e175bcd921724df67acc2

- **LMCache：PD backend 支持非对称 store / retrieve backend**  
  变更点：新增 `store_location` 与 `retrieve_locations`，允许 prefill/decode 两侧走不同存储目标，例如“从 PDBackend 取，但写回 RemoteBackend”。  
  链接：https://github.com/LMCache/LMCache/commit/9d413181c30ec2ec97bcb6b17defa7c5f9f8e36e

- **LMCache：Valkey connector 增加 database 选项**  
  变更点：连接器和 cluster config 都接入 `database_id`，方便把 KV cache 隔离到指定 DB。  
  链接：https://github.com/LMCache/LMCache/commit/d6661f1c58aa441806315a6337a567425b3ecc0f

## 工程启发

1. **MoE 的竞争点正在从“算子快不快”转成“通信后端怎么选”。** vLLM 今天把 FlashInfer A2A 明确拆成 one-sided / two-sided，说明 MoE 服务性能越来越依赖底层互联语义与 prepare/finalize 设计，而不是只看 GEMM。
2. **KV cache 系统已经明显进入“分层存储 + 分离式推理”的第二阶段。** SGLang 在修 decode 阶段的 cache 生命周期，TensorRT-LLM 在修 speculative draft KV 预算，LMCache 在做 PD backend 非对称读写——这几个项目其实都在回答同一个问题：**长上下文与分布式 serving 下，cache 怎么既省又稳。**
3. **多后端与异构设备支持，正在从“补适配”转向“补高性能路径”。** vLLM 的 XPU fused rope、Zen CPU backend，llama.cpp 的 CUDA kernel 调度优化，都说明框架不再满足于单纯兼容，而是在积极榨不同硬件的真实可用性能。
4. **生产推理越来越依赖“正确性补丁”而不是炫技功能。** draft KV cache OOM、write-through lock_ref 释放、device init 创建 CUDA context 这些问题都不是 benchmark 首页上的 headline，但它们决定系统是否能稳定跑一周。

## 明日跟踪建议

1. 继续盯 **vLLM 的 FlashInfer MoE A2A** 是否很快补 benchmark，尤其是 one-sided / two-sided 在不同 NVLink / MNNVL 拓扑上的吞吐和尾延迟差异。
2. 跟踪 **SGLang 的 EPD 多模态支持** 是否马上补完整 benchmark，特别是 video/audio 输入在 encoder transfer、embedding cache 和调度延迟上的开销。
3. 关注 **TensorRT-LLM 的 Qwen3-Next attention DP** 是否很快出现更明确的多卡规模测试，以及 separate draft KV cache 修复后是否还会继续补 EAGLE3/MTP 的回归用例。
4. 继续看 **LMCache 非对称 store/retrieve** 会不会进一步放出典型 PD 拓扑示意和性能数据；如果有，这条线很值得单独拆成“分离式推理缓存架构”专题。
5. 观察 **llama.cpp** 是否继续围绕 GDN / Flash Attention 给出更直接的 perf 数据；如果没有数字，说明它还处在 runtime 行为打磨阶段，不宜过早高估收益。
