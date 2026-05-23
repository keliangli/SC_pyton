# GitHub 大模型推理日报（2026-05-23）

> 抓取时间：2026-05-23 14:14 CST | 覆盖范围：过去 24h 内活跃更新

---

## 今日要点

1. **SGLang v0.5.12 发布**：DeepSeek V4 全链路 Day-0 支持（TP/EP/CP/DP + PD 分离 + HiSparse + HiCache），TokenSpeed MLA 后端登陆 Blackwell，W4A4 MegaMoE 内核首发，EAGLE-3 Spec V2 趋于成熟。
2. **vLLM v0.21.0 发布**：367 commits / 202 contributors，Transformers v4 正式废弃、C++20 编译要求、TOKENSPEED_MLA 后端（Blackwell DSR1/Kimi-K25）、KV Offload + HMA 集成、Spec Decoding 支持 thinking budget。
3. **TensorRT-LLM v1.3.0rc15**：Gemma4 多模态、Kimi K2.5 视觉、DSV4/V3.2 新注意力内核、MegaMoE DeepGEMM / CUTEDSL MoE、FP4/FP8 decode 内核。
4. **FlashInfer v0.6.12rc1**：DSV4 稀疏 MLA TRTLLM-GEN 内核、Kimi K2.5 CuTe DSL MLA decode、SM120 W4A16 b12x 内核、FP8 CUTLASS MLA paged attention。
5. **llama.cpp 日更密集**：SYCL MoE prefill 吞吐优化（计数排序替代 O(n²) 遍历）、Adreno MoE 通用化、ZenDNN Q8_0 支持。
6. **Mooncake v0.3.11.post1**：RDMA QP 路径多样性（UDP sport + LAG 负载均衡）、TENT 增强QoS、结构化对象存储。

---

## 项目速递

### vLLM v0.21.0（2026-05-15）

- 🔗 <https://github.com/vllm-project/vllm/releases/tag/v0.21.0>
- **核心变更**：
  - Transformers v4 废弃，迁移至 v5；C++20 编译器硬性要求
  - KV Offload + HMA 集成：调度器侧 sliding window group、全量 HMA 启用、多连接器 HMA
  - TOKENSPEED_MLA 后端：Blackwell 上 DeepSeek-R1/Kimi-K25 prefill+decode
  - Spec Decoding 支持 reasoning/thinking budget
  - DeepSeek V4：AMD/ROCm、Pipeline Parallelism、max reasoning effort、PD 分离修复
  - Blackwell 性能：FP8 per-token group quant packed kernel、FP8 on Thor/SM110、CUTLASS scaled mm
  - AMD ROCm 7.2.2、AITER Fused Allreduce+RMSNorm、FSE for Qwen3-Next
  - CPU：FP8 attention (AMX/AVX-512)、FP8 W8A16 linear/MoE、DNNL AVX2 W8A8 Int8
  - NVFP4：KV cache、Triton dequant/QDQ、all-gather GEMM fusion for AsyncTP
  - Disaggregated Serving：双向 KV cache 转移、NIXL transfer 重设计、EPLB 内存优化
  - XGrammar 0.2.0：structural tags for strict tool calling + reasoning

### SGLang v0.5.12（2026-05-16）

- 🔗 <https://github.com/sgl-project/sglang/releases/tag/v0.5.12>
- **核心变更**：
  - DeepSeek V4 Day-0 支持：TP/EP/CP/DP + PD 分离 + HiSparse CPU KV offload + DeepGemm/FlashMLA/MegaMoE
  - W4A4 MegaMoE 内核：更高速度 + 几乎无损精度；Marlin/FlashInfer W4A8 MoE on Hopper
  - TokenSpeed MLA 后端（Blackwell, FP8 KV cache）
  - DSv3.2 / GLM-5 FP4 低延迟：PDL 启用、torch.mm Indexer GEMM、Cute-DSL FP4 dense GEMM
  - HiCache + UnifiedRadixTree：DSV4 HiCache、SSD offload via Mooncake store、cascade eviction/tombstone 修复
  - Spec V2 趋于成熟：Adaptive Spec V2、EAGLE-3 SWA、Kimi K2.5 EAGLE-3 MLA、Gemma 3/4 + EAGLE-3
  - CUDA 13 DeepEP 迁移：官方 deepseek-ai/DeepEP@hybrid-ep
  - 新模型：Intern-S2-Preview、MiniCPM-V 4.6、Laguna-XS.2、Ring-2.6-1T、Gemma 4 MTP
  - 性能：TMA bulk-store set_mla_kv_buffer（最高 12×）、Kimi tokenizer TTFT 优化、DeepseekV2MoE defer shared experts

### TensorRT-LLM v1.3.0rc15（2026-05-21）

- 🔗 <https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc15>
- **核心变更**：
  - Gemma4 多模态：text/vision/audio/chunked prefill
  - Kimi K2.5 多模态视觉 + reasoning parser
  - MoE 性能：MegaMoE DeepGEMM、CUTEDSL MoE、shared-expert SwiGLU quant、GDN fusion、bf16 FlashInfer MoE
  - FP4/FP8 decode 内核、FP4 DSA indexing、DSV4 attention 内核、FMHA head_dim 80 cubins
  - Spec Decoding：fractional synthetic acceptance、MTP block reuse、EAGLE3 rejection sampling
  - KV reuse + disaggregated serving：transceiver v2 KV reuse、multi-threaded KV transfer、TRTLLM-Gen routing
  - VisualGen/SageAttention for Wan/FLUX

### FlashInfer v0.6.12rc1（2026-05-22）

- 🔗 <https://github.com/flashinfer-ai/flashinfer/releases/tag/v0.6.12rc1>
- **核心变更**：
  - DSV4 稀疏 MLA TRTLLM-GEN 内核
  - Kimi K2.5 H64 CuTe DSL MLA decode
  - SM120 W4A16 b12x MoE 内核
  - FP8 CUTLASS MLA paged attention 输出支持
  - CuTe DSL grouped-gemm + combine 融合
  - NVFP4 per-token 量化内核优化
  - RMSNorm + RoPE fusion for WAN
  - GLM5 router GEMM 启用
  - sccache-backed JIT-cache builds + AOT 诊断

### llama.cpp（2026-05-22 ~ 05-23 日更）

- 🔗 <https://github.com/ggml-org/llama.cpp/releases>
- **核心变更**：
  - b9294：Adreno MoE 内核通用化（OpenCL）
  - b9291：SYCL MoE prefill 吞吐优化 — 计数排序 O(n+s) 替代 O(n·as) 遍历
  - b9289：SYCL gated_delta_net K>1 支持
  - b9286：ggml-zendnn Q8_0 量化支持
  - b9284：HybridDNA tokenizer BPE token 冲突修复

### LMDeploy v0.13.0（2026-05-12）

- 🔗 <https://github.com/InternLM/lmdeploy/releases/tag/v0.13.0>
- **核心变更**：
  - TurboQuant（quant_policy=42）KV Cache 量化
  - Qwen3.5 MoE Blackwell 推理（cublasGemmGroupedBatchedEx）
  - Anthropic 兼容 serving 端点
  - Intern-S2 Preview 支持

### Mooncake v0.3.11.post1（2026-05-23）

- 🔗 <https://github.com/kvcache-ai/Mooncake/releases/tag/v0.3.11.post1>
- **核心变更**：
  - RDMA QP 路径多样性：UDP sport + LAG port balance
  - TENT 增强 QoS 和 Slice Spraying
  - 结构化对象存储 helper
  - HA backend 抽象 + Redis leadership backend

---

## 工程启发

1. **Blackwell 生态全面铺开**：vLLM、SGLang、TRT-LLM、FlashInfer 四大框架均已落地 Blackwell 专用内核（TOKENSPEED_MLA、SM120 内核、FP8 KV cache），DeepSeek V4 成为首个全面覆盖 Blackwell 的 MoE 模型。**行动**：如有 B200/B300 硬件，应优先评估 SGLang v0.5.12 的 DSV4 一体化方案。

2. **MoE 内核竞争白热化**：W4A4 MegaMoE（SGLang）、CUTEDSL MoE（TRT-LLM/FlashInfer）、Marlin W4A8（SGLang）三条路线并行。**行动**：跟踪 SGLang 的 W4A4 精度-速度 trade-off 数据，对比 TRT-LLM 的 CUTEDSL MoE 吞吐。

3. **PD 分离 + KV 迁移走向工程化**：NIXL connector 在 vLLM/SGLang 双双升级，Mooncake 增量传输 + SSD offload 成熟，TRT-LLM transceiver v2 KV reuse。**行动**：多节点 PD 分离不再是实验特性，可开始生产环境验证。

4. **Spec Decoding V2 成熟**：SGLang Adaptive Spec V2、EAGLE-3 多模型适配（Kimi K2.5 MLA、Gemma 3/4）、TRT-LLM fractional acceptance。**行动**：在长上下文场景测试 EAGLE-3 + thinking budget 组合效果。

5. **量化格式多元化**：NVFP4（KV cache + GEMM fusion）、MXFP4（Humming MoE）、W4A4（MegaMoE）、TurboQuant（LMDeploy KV cache）。**行动**：梳理各量化格式在不同推理框架的覆盖矩阵，选择最稳妥的生产方案。

---

## 明日跟踪建议

1. 🔍 **SGLang W4A4 MegaMoE 详细 benchmark**：关注 LMSYS blog 和 DSV4 cookbook 更新
2. 🔍 **vLLM v0.21.0 升级路径**：Transformers v5 + C++20 对现有部署的影响评估
3. 🔍 **TRT-LLM v1.3.0 正式版**：rc15 已大量功能合入，关注正式发布时间线
4. 🔍 **FlashInfer v0.6.12 正式版**：rc1 内核变更量大，关注稳定性测试
5. 🔍 **DeepEP v1.2.1 topk10 低延迟内核**：SGLang 已迁移至官方 DeepEP 分支，关注 EP 通信性能数据

---

*本报告由 OpenClaw 自动生成 | 数据来源：GitHub Releases*
