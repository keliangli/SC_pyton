# GitHub 大模型推理日报（2026-05-10）

## 今日要点

1. **NVFP4 量化生态加速落地**：vLLM 正式合并 ModelOpt NVFP4 W4A16 量化支持 + NVFP4 all-gather GEMM 融合（AsyncTP）；SGLang Reland Cute-DSL FP4 dense GEMM——三大框架同步推进 FP4 路线，Blackwell 量产前的软件栈准备加速。
2. **DeepSeek V4 内核密集迭代**：vLLM 修复 DSv4 topk 数值问题 + fused Indexer Q quant kernel 优化 + PD 分离式部署 fix；SGLang cherry-pick DSv4 分支关键 commit 并增强测试；TensorRT-LLM 新增 DeepSeekV4 attention kernels——三线并行打磨 DSv4 推理。
3. **MoE 后端多元化**：TensorRT-LLM 新增 CUTEDSL MoE backend（nemotron-h）；SGLang 启用 trtllm-gen BF16 MoE for MTP + 修复 SM90 上 triton moe-runner 性能回退；vLLM 修复 routed-experts hot path 跳过逻辑。
4. **投机解码生态扩展**：vLLM 新增 MiMo 2.5 MTP 支持 + Gemma 4 speculative decoding 文档；SGLang 支持 Gemma3/4 + Eagle3 + EAGLE3 topk>1 spec metadata 修复；SGLang 重构 verified_id 为 bonus_tokens/accept_tokens 双路。

---

## 项目速递

### vLLM
| 更新 | PR | 关键词 |
|------|-----|--------|
| ModelOpt NVFP4 W4A16 量化支持 | [#41769](https://github.com/vllm-project/vllm/pull/41769) | NVFP4, 量化 |
| NVFP4 all-gather GEMM fusion for AsyncTP | [#41882](https://github.com/vllm-project/vllm/pull/41882) | NVFP4, GEMM融合, TP |
| Batch KV cache swap 优化（CU_MEMCPY_SRC_ACCESS_ORDER_ANY） | [#39306](https://github.com/vllm-project/vllm/pull/39306) | KV Cache, CUDA Memcpy |
| DSv4 topk 数值修复（unaligned max-model-len） | [#42169](https://github.com/vllm-project/vllm/pull/42169) | DeepSeek V4, Bugfix |
| DSv4 improved fused Indexer Q quant kernel | [#41428](https://github.com/vllm-project/vllm/pull/41428) | DeepSeek V4, Kernel |
| DSv4 Disaggregated PD fix | [#41957](https://github.com/vllm-project/vllm/pull/41957) | DeepSeek V4, PD分离 |
| SpecDecoding MTP for MiMo 2.5 | [#41905](https://github.com/vllm-project/vllm/pull/41905) | 投机解码, MTP |
| LoRA Initial EP support | [#40867](https://github.com/vllm-project/vllm/pull/40867) | LoRA, Expert Parallel |
| GDN KKT precision loss fix on Hopper（WGMMA layout 对齐） | [#42076](https://github.com/vllm-project/vllm/pull/42076) | Hopper, WGMMA, Triton |
| Cohere Eagle + MoE fix | [#42078](https://github.com/vllm-project/vllm/pull/42078) | Cohere, MoE |
| SP + PP residual handling fix for multimodal | [#33322](https://github.com/vllm-project/vllm/pull/33322) | 序列并行, 流水并行 |
| KV Transfer NIXL: pre-admission rejection 通知 P node | [#41269](https://github.com/vllm-project/vllm/pull/41269) | KV Transfer, NIXL |
| NIXL util lazy init refactor | [#41392](https://github.com/vllm-project/vllm/pull/41392) | NIXL, 重构 |
| KV Connector 移除 v0.12.0 前兼容代码 | [#39832](https://github.com/vllm-project/vllm/pull/39832) | KV Connector, 清理 |
| ROCm aiter 升级 v0.1.13-rc5 | [#42113](https://github.com/vllm-project/vllm/pull/42113) | ROCm, aiter |
| C++20 要求 | [#40380](https://github.com/vllm-project/vllm/pull/40380) | C++20, 编译 |

### SGLang
| 更新 | PR | 关键词 |
|------|-----|--------|
| Reland Cute-DSL FP4 dense GEMM | [#23590](https://github.com/sgl-project/sglang/pull/23590) | FP4, Cute-DSL, GEMM |
| TRT-LLM Gen BF16 MoE for MTP | [#24260](https://github.com/sgl-project/sglang/pull/24260) | MoE, TRT-LLM, MTP |
| PDL for DSV32/GLM5 kernels | [#23965](https://github.com/sgl-project/sglang/pull/23965) | PDL, GLM5, DSv3.2 |
| DSv3 triton moe-runner SM90 性能回退修复 | [#24562](https://github.com/sgl-project/sglang/pull/24562) | MoE, 性能, SM90 |
| DSV4 cherry-pick + 测试增强 | [#24793](https://github.com/sgl-project/sglang/pull/24793) | DeepSeek V4, 测试 |
| Gemma3/4 + Eagle3 投机解码 | [#23976](https://github.com/sgl-project/sglang/pull/23976) | 投机解码, Eagle3 |
| KDA: prefill kernel 对角线 + recompute 融合优化 | [#24271](https://github.com/sgl-project/sglang/pull/24271) | Kernel, Prefill优化 |
| PrefillDelayer NCCL all-gather 跨 DP 同步 | [#24768](https://github.com/sgl-project/sglang/pull/24768) | NCCL, Prefill, DP |
| NUMA+Ray: CUDA_VISIBLE_DEVICES shuffle 下 NVML 修复 | [#24766](https://github.com/sgl-project/sglang/pull/24766) | NUMA, Ray, NVML |
| Spec verified_id 拆分为 bonus_tokens/accept_tokens | [#24724](https://github.com/sgl-project/sglang/pull/24724) | 投机解码, 重构 |
| SGLANG_RADIX_FORCE_MISS 环境变量 | [#24726](https://github.com/sgl-project/sglang/pull/24726) | Radix Cache, 调试 |
| GLM-5.1: 多项修复 | [#23550](https://github.com/sgl-project/sglang/pull/23550) | GLM-5.1, Bugfix |
| UnifiedRadixTree cache_empty_result 对齐 | [#24779](https://github.com/sgl-project/sglang/pull/24779) | RadixTree, 重构 |
| Device cache emptying 重构 | [#24861](https://github.com/sgl-project/sglang/pull/24861) | 显存管理 |

### llama.cpp
| 更新 | PR | 关键词 |
|------|-----|--------|
| Flash attention MMA/Tiles 支持 MiMo-V2.5 | [#22812](https://github.com/ggml-org/llama.cpp/pull/22812) | Flash Attention, MiMo |
| SYCL: flash attention 分配开销优化 | [#22732](https://github.com/ggml-org/llama.cpp/pull/22732) | SYCL, Flash Attention |
| SYCL: BF16 GET_ROWS 支持 | [#21391](https://github.com/ggml-org/llama.cpp/pull/21391) | SYCL, BF16 |
| SYCL: Battlemage AOT build（spir64_gen + MMQ subgroup） | [#22147](https://github.com/ggml-org/llama.cpp/pull/22147) | SYCL, Intel Battlemage |
| Hexagon: HTP kernel for GATED_DELTA_NET | [#22837](https://github.com/ggml-org/llama.cpp/pull/22837) | Hexagon, HTP, DeltaNet |
| sarvam_moe 架构支持 | [#20275](https://github.com/ggml-org/llama.cpp/pull/20275) | MoE, 新架构 |
| granite/llama3 & deepseek2/glm4.7lite 模型类型检查修复 | [#22870](https://github.com/ggml-org/llama.cpp/pull/22870) | Bugfix |

### TensorRT-LLM
| 更新 | PR | 关键词 |
|------|-----|--------|
| CUTEDSL MoE backend for nemotron-h | [#12884](https://github.com/NVIDIA/TensorRT-LLM/pull/12884) | CUTEDSL, MoE, Nemotron |
| DeepSeekV4 attention kernels | [#13652](https://github.com/NVIDIA/TensorRT-LLM/pull/13652) | DeepSeek V4, Attention |
| Cute DSL FP8 paged MQA logits decode kernel | [#13219](https://github.com/NVIDIA/TensorRT-LLM/pull/13219) | FP8, MQA, Cute-DSL |
| Gemma4 multimodal（text+vision+audio） | [#12932](https://github.com/NVIDIA/TensorRT-LLM/pull/12932) | Gemma4, 多模态 |
| Scaffolding: agent 应用 + TRT-LLM 联合优化 | [#11173](https://github.com/NVIDIA/TensorRT-LLM/pull/11173) | Agent, Scaffolding |
| Disagg conversation ID headers 扩展 | [#13656](https://github.com/NVIDIA/TensorRT-LLM/pull/13656) | PD分离, Disaggregated |
| Blackwell MoE backend mismatch 修复 | [#13470](https://github.com/NVIDIA/TensorRT-LLM/pull/13470) | Blackwell, MoE |

### FlashInfer
| 更新 | PR | 关键词 |
|------|-----|--------|
| CI: sm110 builds 限制 aarch64 | [#3275](https://github.com/flashinfer-ai/flashinfer/pull/3275) | CI, sm110 |

---

## 工程启发

1. **NVFP4 量化已进入"全栈落地"阶段**：vLLM 的 NVFP4 W4A16 + all-gather GEMM fusion、SGLang 的 Cute-DSL FP4 GEMM、TRT-LLM 的 FP8 paged MQA decode kernel——低精度推理的 kernel 层和框架层同时成熟，Blackwell GPU 量产后可快速启用。**建议**：提前在当前项目中规划 FP4/FP8 模型量化流水线，关注 ModelOpt 工具链。

2. **DeepSeek V4 三框架并行打磨，进入"稳定性攻坚期"**：vLLM 修 topk 数值 + PD 分离 fix，SGLang 补 commit + 增强测试，TRT-LLM 新增 attention kernel——各框架重点从"跑通"转向"跑稳跑快"。**建议**：如已在用 DSv4，优先升级到最新 nightly 以获取这些修复。

3. **投机解码成为标配功能，Eagle3/MTP 成为主流方案**：vLLM 支持 MiMo 2.5 MTP，SGLang 支持 Gemma3/4+Eagle3，TRT-LLM 也在 MoE for MTP 上发力。投机解码不再是实验性功能。**建议**：在延迟敏感场景评估 Eagle3/MTP 方案的加速比，注意 topk>1 场景的 metadata 正确性。

4. **KV Cache 管理持续优化**：vLLM 的 batch KV cache swap CUDA 优化、NIXL lazy init、KV Transfer pre-admission rejection 通知；SGLang 的 RadixTree 对齐 + RADIX_FORCE_MISS 调试工具——长上下文场景的 KV 管理仍在快速迭代。**建议**：关注 NIXL 生态成熟度，为多节点 KV 共享场景做技术储备。

5. **SYCL/Intel 生态推进明显**：llama.cpp 本周密集合并 SYCL 相关 PR（flash attention 优化、BF16、Battlemage AOT、Q5_K/Q8_0 reorder），Intel GPU 推理栈在加速追赶。**建议**：如有 Intel GPU 部署需求，跟进 Battlemage AOT 构建路径。

---

## 明日跟踪建议

1. **NVFP4 端到端 benchmark**：vLLM NVFP4 W4A16 全链路打通后，关注是否有 latency/throughput 对比数据流出。
2. **TRT-LLM CUTEDSL MoE**：nemotron-h 的 MoE 后端是否有性能数据，对比现有 cublas/cutlass 后端。
3. **SGLang KDA prefill 优化**：对角线 + recompute 融合的实际加速比待观察。
4. **vLLM DSv4 PD 分离**：pre-admission rejection 修复后，多节点 PD 部署稳定性是否改善。
5. **TGI / HuggingFace 推理栈**：本日抓取失败，明日需补查 TGI 最新 release 和 commit。
