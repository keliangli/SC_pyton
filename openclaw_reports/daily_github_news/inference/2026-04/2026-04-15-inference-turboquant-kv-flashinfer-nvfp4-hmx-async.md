---
title: "GitHub 大模型推理日报（2026-04-15）- TurboQuant KV压缩 + FlashInfer NVFP4 + HMX异步"
date: 2026-04-15
track: 大模型推理
slug: turboquant-kv-flashinfer-nvfp4-hmx-async
source_report: reports/github_inference_news_2026-04-15.md
repo_path: openclaw_reports/daily_github_news/inference/2026-04/2026-04-15-inference-turboquant-kv-flashinfer-nvfp4-hmx-async.md
generated_by: openclaw
---

# GitHub 大模型推理日报 — 2026-04-15

> 抓取时间：2026-04-15 15:05 CST | 覆盖范围：GitHub 过去 ~24h 活跃提交 + 近期重大 Release

---

## 📌 今日要点

| # | 要点 | 影响评估 |
|---|------|----------|
| 1 | **vLLM 引入 TurboQuant 2-bit KV cache 压缩**：PolarQuant（WHT 旋转 + Lloyd-Max 标量量化）在线压缩 KV cache，最高 4.9x 压缩，NIAH 100% 保持，长上下文场景吞吐仅损失 5-7% | 🔴 极高 |
| 2 | **FlashInfer v0.6.8rc1 发布**：CuTe-DSL NVFP4 量化后端、MLA decode op、GDN 非连续状态解码、CUTLASS MoE Relu2 激活 + PDL SM12x 修复 | 🔴 极高 |
| 3 | **llama.cpp 一日三更（b8795→b8797）**：Hexagon HMX 异步矩阵乘、Vulkan NVFP4 支持、WebGPU f32 累加修复、ARM NEON nvfp4 dot product 修正 | 🟡 高 |
| 4 | **SGLang AMD 生态密集优化**：Qwen3.5 MoE 融合 Triton kernel（shared expert fusion + topk append）、O(n²)→O(1) streaming 优化 | 🟡 高 |
| 5 | **TensorRT-LLM 回退 EAGLE3 动态树投机解码**：revert + 新增 tunable NVFP4 量化 + CUTLASS 4.4.2 升级 | 🟡 高 |
| 6 | **xllm（京东）+ rtp-llm（阿里）国产栈持续演进**：xllm 新增 tilelang-ascend GDN kernel + MLU Mooncake PD；rtp-llm 去 sampler device sync + 引入 trtallreduce | 🟡 中高 |

---

## 🚀 项目速递

### 1. vLLM — TurboQuant KV 压缩 + MoE 重构 + Mamba FlashInfer
- **链接**: https://github.com/vllm-project/vllm
- **日期**: 2026-04-14 ~ 04-15
- **核心更新**:
  - **TurboQuant: 2-bit KV cache compression with 4x capacity** (`#38479`)：在线 KV cache 压缩，Key 用 PolarQuant（WHT + Lloyd-Max）、Value 用 uniform 量化，store 时 fused Triton kernel 完成，无需离线校准或模型修改。`--kv-cache-dtype turboquant_k8v4` 即可启用
    - turboquant_k8v4：2.6x 压缩，GSM8K 0.860（基线 0.900）
    - turboquant_3bit_nc：4.9x 压缩，GSM8K 0.720，NIAH 100%
    - 长上下文 prefill 吞吐保持 93-100%，decode 吞吐约 65-80%
  - **Disable piecewise cudagraph fallback for eagle draft decodes** (`#39773`)：修复 eagle spec decode 在 piecewise cudagraph 模式下 FlashInfer 后端 num_tokens ≠ num_reqs 导致的 OOB
  - **Disable FlashInfer CUTLASS MoE on SM121** (`#39825`)：DGX Spark 上 Nemotron-H MTP drafter 遇到 Relu2 模板缺失的 workaround
  - **Fix Mooncake NVLink _send_blocks CUDA context** (`#39548`)：ThreadPoolExecutor 线程默认 device 0，导致 TP>0 时 NVLink 传输失败
  - **Refactor ZeroExpertFusedMoE** (`#35549`)：将零专家逻辑迁移到 FusedMoE + ZeroExpertRouter 新框架
  - **Mamba FlashInfer selective_state_update** (`#36162`)：新增 FlashInfer 后端，Nemotron-3-Nano 验证通过，可 triton/flashinfer 切换
  - **Fix LMCache store for cached requests with prefix cache** (`#39719`)
  - **Add PyTorch nightly build and test pipeline** (`#37226`)

### 2. FlashInfer v0.6.8rc1 — CuTe-DSL NVFP4 + MLA Decode + MoE 增强
- **链接**: https://github.com/flashinfer-ai/flashinfer
- **日期**: 2026-04-14（Release）
- **核心更新**:
  - **CuTe-DSL NVFP4 量化后端** (`#2838`)：Blackwell NVFP4 量化用 CuTe-DSL 实现
  - **CuTe-DSL MLA decode op** (`#2743`)：MLA 解码算子
  - **MXFP4/NVFP4 group GEMMs on GeForce and Spark** (`#2738`)：消费级显卡低精度 MoE 支持
  - **GDN non-contiguous state for decoding** (`#2727`)：GatedDeltaNet 解码支持非连续状态
  - **CUTLASS MoE Relu2 激活** (`#2926`)：支持 squared ReLU 激活
  - **Fix CUTLASS fused MoE PDL on SM12x** (`#2913`)：防止 SM120/SM121 随机崩溃
  - **trtllm_fp4_block_scale_moe int32 overflow fix** (`#2853`)：EP32+ 配置下修复
  - **In-place update for trtllm_fp8_block_scale_moe** (`#2739`)
  - **Optimize CuTe-DSL fp4/fp8 quantization kernels** (`#2904`)
  - **PDL support for CuTe-DSL MLA decode** (`#2901`)
  - **Dynamic shape unified API** (`#2910`)

### 3. llama.cpp — b8795→b8797 一日三更
- **链接**: https://github.com/ggml-org/llama.cpp
- **日期**: 2026-04-14 ~ 04-15
- **核心更新**:
  - **b8797 — Hexagon HMX 异步矩阵乘** (`#21554`)：HMX 计算异步化，与 HVX dequant/DMA 流水线重叠；新增 cost-based VTCM chunk search 替代简单 mc×nc 最大化策略
  - **b8796 — 移除 ggml-ext.h** (`#21869`)：代码清理
  - **b8795 — Metal FA 支持逻辑修复** (`#21898`)
  - **Vulkan NVFP4 量化支持** (`#21455`)：get_rows + dequant + mul_mat，fp16/fp32 路径（非 dp4a）
  - **WebGPU f32 累加 matmul** (`#21644`)：修复 Qwen 模型 NaN 问题，shader batching 提升至 64
  - **Vulkan RoundingModeRTE 自动注入** (`#21572`)
  - **ARM NEON nvfp4 dot product 修正** (`#21559`)：非 dotprod 目标平台修复
  - **OAI /v1/audio/transcriptions API** (`#21863`)
  - **Metal XIELU unary op** (`#20802`)

### 4. SGLang — AMD Qwen3.5 优化 + Streaming 性能修复
- **链接**: https://github.com/sgl-project/sglang
- **日期**: 2026-04-14 ~ 04-15
- **核心更新**:
  - **Qwen3.5 MoE fused Triton kernel for _append_shared_to_topk_output** (`#22844`)：4 个 kernel launch 合并为 1 个，MoE routing 关键路径加速
  - **Enable shared expert fusion with router experts for Qwen3.5** (`#20736`)：当 shared_expert_intermediate_size == moe_intermediate_size 时，shared expert 融入 topk+1 单次 MoE dispatch（ROCm/Aiter）
  - **Replace O(n²) stream_buffer string concat with integer offset** (`#22606`)：流式响应 delta 计算从 O(n²) 降至 O(1)
  - **Fix LFM2-VL offline inference + GPU JPEG decode** (`#22448`)
  - **Move ptxas sm_103a workaround into CUDA 13 section** (`#22852`)
  - **Fix streaming session busy-check double-counting** (`#22753`)

### 5. TensorRT-LLM — EAGLE3 Revert + NVFP4 量化 + CUTLASS 升级
- **链接**: https://github.com/NVIDIA/TensorRT-LLM
- **日期**: 2026-04-14 ~ 04-15
- **核心更新**:
  - **Revert EAGLE3 dynamic tree speculative decoding** (`#13006`)：回退 EAGLE3 动态树投机解码支持，需关注后续重新引入
  - **Add tunable nvfp4 quantize with FlashInfer backend** (`#12126`)：NVFP4 量化新增可调参数 + FlashInfer 后端
  - **Update CUTLASS C++ to 4.4.2** (`#12897`)：底层 CUTLASS 升级
  - **AutoDeploy Qwen3.5 NVFP4 accuracy test** (`#13014`)
  - **Unify KV cache manager reuse/non-reuse code path** (`#10437`)

### 6. xllm（京东开源）— Ascend GDN + MLU Mooncake
- **链接**: https://github.com/jd-opensource/xllm
- **日期**: 2026-04-14 ~ 04-15
- **核心更新**:
  - **tilelang-ascend fused_gdn_gating kernel** (`#1267`)：昇腾 NPU 上 GDN gating 融合
  - **MLU mooncake PD push support** (`#1246`)：寒武纪 MLU 设备支持 Mooncake PD
  - **gemma_rms_norm + fused_qkvzba_split_reshape_cat** (`#1170`)：新增算子
  - **Separate kv_cache_transfer from kv_cache** (`#1283`)：KV cache 传输逻辑解耦
  - **torch::empty → torch::zeros for kvcache allocation** (`#1281`)：零初始化避免脏数据

### 7. rtp-llm（阿里）— Sampler 优化 + TRT AllReduce
- **链接**: https://github.com/alibaba/rtp-llm
- **日期**: 2026-04-14 ~ 04-15
- **核心更新**:
  - **Add trtallreduce**：引入 TensorRT AllReduce 通信原语
  - **Remove cuda fused rope kvcache**：移除 CUDA fused rope kvcache
  - **Move sample tensors to CUDA to remove device sync in sampler**：消除 sampler 中的 GPU→CPU 同步

### 8. LMCache — L1 订阅 + LRU 模拟器
- **链接**: https://github.com/LMCache/LMCache
- **日期**: 2026-04-14 ~ 04-15
- **核心更新**:
  - **L1 Subscriber** (`#2986`)：L1 缓存订阅机制
  - **LRU cache simulator for lookup-hash JSONL logs** (`#3021`)：离线缓存行为模拟
  - **Skip locked keys during LRU eviction** (`#2978`)：跳过锁定的 key 提高淘汰效率
  - **Add cache_salt parameter** (`#3029`, `#3032`)：缓存隔离

### 9. Mooncake — 跨传输 Failover + 昆鹏 UB
- **链接**: https://github.com/kvcache-ai/Mooncake
- **日期**: 2026-04-14 ~ 04-15
- **核心更新**:
  - **Cross-transport failover with safety limits** (`#1878`)：跨传输层自动故障切换
  - **SSD Metrics** (`#1879`)：SSD 存储层可观测性
  - **Kunpeng SuperNode UB Transport Phase 2** (`#1855`)：鲲鹏超节点 UB 传输第二阶段

---

## 🔧 工程启发

1. **KV cache 压缩正从"离线量化"走向"在线压缩"**：vLLM TurboQuant 不改模型权重、无需校准数据，store 时 Triton kernel 完成，工程集成门槛极低。对于长上下文场景（NIAH 100% 保持），这是比 FP8 KV cache 更激进的路线，值得评估是否适合生产环境
2. **Hexagon HMX 异步化思路可复用**：llama.cpp 将 HMX 计算异步化与 HVX/DMA 流水线重叠，这种"计算-通信重叠"的思路在 GPU 端已常见（如 vLLM 的 overlap scheduler），但在 NPU/移动端场景是新范式
3. **FlashInfer v0.6.8 的 CuTe-DSL 路线值得关注**：NVFP4 量化、MLA decode、PDL 加速都走 CuTe-DSL，意味着 Blackwell 生态正从 CUTLASS 手写 kernel 向更高层 DSL 迁移，后续自定义 kernel 开发可能也需要跟进
4. **TRT-LLM 回退 EAGLE3 动态树投机解码**：说明动态树 spec decode 的工程稳定性仍有挑战，vLLM/SGLang 此方向也在持续迭代，短期内 spec decode 仍以静态树为主
5. **rtp-llm 去 sampler device sync 是典型 latency 优化手段**：将 sample 相关张量保持在 CUDA 端，避免每步采样都做 GPU→CPU 同步，这是 decode 路径延迟优化的关键一环

---

## 📋 明日跟踪建议

1. 🔍 **TurboQuant 生产化进度**：跟踪 vLLM 后续是否将 TurboQuant 作为默认 KV cache 压缩选项，以及与 FP8 KV cache 的性能对比
2. 🔍 **FlashInfer v0.6.8 正式版发布**：rc1 已出，关注正式版发布时间及 vLLM/SGLang 集成进度
3. 🔍 **TRT-LLM EAGLE3 动态树 re-landing**：revert 后的重新引入时间线
4. 🔍 **SGLang AMD Qwen3.5 性能数据**：shared expert fusion + fused topk append 的具体 benchmark
5. 🔍 **xllm Ascend GDN kernel 端到端性能**：tilelang-ascend 路线在昇腾 910B 上的实测数据

---

*数据来源：GitHub API + Releases + Commits，抓取时间 2026-04-15 15:05 CST*
