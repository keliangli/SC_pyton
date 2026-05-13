# GitHub 大模型推理日报（2026-05-13）

> 聚焦 LLM 推理加速栈的最新 Release / 重要 Commit / 新功能 / 性能优化

---

## 📌 今日要点

1. **llama.cpp b9128 今日发布**：Hexagon HVX 优化消除标量 VTCM 加载、HMX 算子优化；前一日 b9127 新增 OpenCL Adreno F16xF32 GEMM prefill 加速；正式支持 CUDA 13.1 和 OpenVINO 2026.0
2. **vLLM v0.20.2 发布**（5月10日）：DeepSeek V4 sparse attention 修复、KV cache 分配修复、gpt-oss MXFP4 torch.compile 修复；v0.20.1（5月4日）为 DeepSeek V4 带来 multi-stream pre-attention GEMM、PTX FP4 转换、tile kernels 等重大优化
3. **SGLang v0.5.11 发布**（5月5日）：CUDA 13 + Torch 2.11 默认升级；Speculative Decoding V2 成为默认；DFLASH spec-decode 集成；FA3 社区内核；Decode Radix Cache 支持 PD 分离部署；新增 Gemma 4 / GLM-5.1 / Qwen3.6 等模型
4. **Lucebox Hub 开源**：手写调优 LLM 推理内核，Megakernel 将 Qwen 3.5-0.8B 全部 24 层合入单次 CUDA dispatch；DFlash+PFlash 在 RTX 3090 上 Qwen 3.6-27B 达到 10.4× TTFT 加速、3× decode 加速；RTX 5090 上 4.84× 加速（205 tok/s）
5. **MNN 3.5.0 大版本**（4月7日）：Vulkan 后端全面支持 LLM 推理；摩尔线程 MUSA 后端；TurboQuant TQ3/TQ4 KV Cache 量化；Tokenizer 重构加载速度 20×+；多轮对话 Prompt Cache
6. **TensorRT-LLM v1.3.0rc14**（5月7日）：Mamba 混合模型 prefix caching、Qwen3.5 自定义 MoE 路由、disaggregated serving 增强、CuteDSL bf16 dense GEMM / fused add-norm-FP8 量化等内核优化
7. **ONNX Runtime 1.26.0**（5月8日）：RISC-V RVV CPU EP、CUDA 13 迁移预告、WebGPU GridSample/Split-K、.ort 模型内存映射加载

---

## 🚀 项目速递

### llama.cpp — b9128 (2026-05-13)

- **Hexagon HVX 优化**：消除标量 VTCM 加载，新增 hvx_vec_repl 辅助函数；HMX-MM 优化 per-group scale 处理；HMX-FA 优化 slope 加载和对齐访问
- **OpenCL Adreno**：b9127 新增 opt-in F16xF32 GEMM for prefill（#22755）
- **平台扩展**：正式发布 CUDA 13.1 / OpenVINO 2026.0 / SYCL FP16 / ROCm 7.2 / HIP Radeon 构建
- 🔗 https://github.com/ggml-org/llama.cpp/releases/tag/b9128

### vLLM — v0.20.2 (2026-05-10)

- **DeepSeek V4 稳定化**：修复 sparse attention persistent topk 路径在 Hopper 上的 MTP=1 hang；KV cache manager 分配修复
- **gpt-oss MXFP4**：修复 torch.compile 下 MXFP4 的 hidden_dim_unpadded 传递
- **Qwen3-VL**：移除 deepstack 边界检查（重负载下失败）
- 🔗 https://github.com/vllm-project/vllm/releases/tag/v0.20.2

### vLLM — v0.20.1 (2026-05-04)

- **DeepSeek V4 核心优化**：multi-stream pre-attention GEMM、BF16/MXFP8 all-to-all for FlashInfer、PTX cvt FP32→FP4 转换、integrated tile kernels (head_compute_mix_kernel)
- **BailingMoE 支持**：修复 BailingMoE 线性层和 MLA RoPE 旋转
- **ROCm**：修复 Quark W4A8 GPT-OSS input_ids/expert_map
- 🔗 https://github.com/vllm-project/vllm/releases/tag/v0.20.1

### SGLang — v0.5.11 (2026-05-05)

- **CUDA 13 + Torch 2.11**：全栈默认升级到 CUDA 13.0 和 PyTorch 2.11
- **Speculative Decoding V2 默认开启**：overlap scheduling 隐藏 CPU 开销，降低 EAGLE/MTP/DFLASH 每 step CPU 成本
- **Decode Radix Cache for PD 分离**：decode 端 prefix caching 在 prefill/decode 分离部署下恢复 radix-cache 命中率
- **DFLASH Speculative Decoding**：来自 kernel 社区的高吞吐 spec-decode，扩展至 AMD ROCm
- **FA3 社区内核**：drop-in FA3 内核，与 FA4 并行提供高性能易维护选项
- **LoRA for DeepSeek-V3 / Kimi-K2**：最大规模 MLA-based MoE 模型 LoRA 支持
- **Context Parallel 增强**：all-reduce + RMSNorm 融合；moe_dp_size 与 attention_cp_size 独立调优
- **FlashInfer CuteDSL MoE Runner**：新增专用 FlashInferCuteDslMoE 层
- **新模型**：Gemma 4、GLM-5.1、Qwen3.6、MiMo-V2.5/V2.5-Pro、Ling-2.6-Flash、Mistral Medium 3.5、Kimi-K2.6
- 🔗 https://github.com/sgl-project/sglang/releases/tag/v0.5.11

### Lucebox Hub — 开源发布

- **Megakernel Qwen3.5 0.8B**：24 层全部合入单次 CUDA dispatch，RTX 3090 上 1.87 tok/J，2× vs F16
- **DFlash + DDTree**：Qwen 3.5-27B Q4_K_M 在 RTX 3090 上 3.43× vs AR；RTX 5090 上 4.84× vs AR（205 tok/s）
- **DFlash + PFlash**：Qwen 3.6-27B Q4_K_M 在 RTX 3090 上 TTFT 10.4× @ 128K，decode ~3× vs AR
- **Ryzen AI MAX+ 395 (HIP)**：Qwen 3.5-27B Q4_K_M 上 2.24× TTFT @ 16K、3.08× vs llama.cpp HIP AR
- 🔗 https://github.com/Luce-Org/lucebox-hub

### MNN — 3.5.0 (2026-04-07)

- **Vulkan LLM 推理**：Vulkan 后端全面支持 LLM 模型推理
- **MUSA 后端**：全新接入摩尔线程 MUSA GPU，支持国产 GPU 推理
- **RISC-V RVV**：CPU 后端新增 RISC-V 向量扩展支持
- **TurboQuant TQ3/TQ4**：全新 KV Cache 量化方案，降内存保质量
- **Sampler Pipeline 重构**：采样器重构为流水线架构，新增 Penalty 机制
- **多轮对话 Prompt Cache**：文本级别 Prompt Cache，显著加速多轮对话首 Token
- **Tokenizer 重构**：minja → jinja 迁移 + 二进制 tokenizer.mtok 格式，加载速度 20×+
- **异步 Token2Wav 三阶段流水线**：DiT 与 Vocoder 并行，大幅提升语音合成吞吐
- **智能语音打断（AEC Barge-in）**：回声消除智能打断
- 🔗 https://github.com/alibaba/MNN/releases/tag/3.5.0

### TensorRT-LLM — v1.3.0rc14 (2026-05-07)

- **Mamba 混合模型 prefix caching**：支持 Qwen3.5 和 Nemotron Super V3
- **Qwen3.5 支持增强**：自定义 MoE 路由、dense/NVFP4 权重加载修复
- **Disaggregated serving 增强**：gen-first ADP serving、KV-aware hit-rate gates、fair-share caps
- **内核优化**：GEMM-to-allreduce 注册缓冲、CuteDSL bf16 dense GEMMs、sparse-attention GVR Top-K、fused add-norm-FP8 量化、TF32 DSA GEMMs
- 🔗 https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc14

### ONNX Runtime — 1.26.0 (2026-05-08)

- **RISC-V RVV**：CPU EP 新增 RISC-V 向量扩展支持
- **CUDA 13 迁移预告**：1.27.0 将移除 CUDA 12 支持，CUDA runtime 迁移为独立 EP
- **WebGPU**：GridSample 支持 + Split-K 改进
- **.ort 模型内存映射**：可选 mmap 加载
- **安全加固**：Python setattr 白名单、多处 OOB/溢出修复
- 🔗 https://github.com/microsoft/onnxruntime/releases/tag/v1.26.0

### llm-d — CNCF Sandbox

- **K8s 推理编排**：由 Red Hat / Google Cloud / IBM / CoreWeave / NVIDIA 联合发起的 CNCF sandbox 项目
- **智能路由**：prefix-cache + load-aware 负载均衡，实验性预测延迟调度
- **高级 KV-Cache 管理**：tiered KV-cache 扩展多轮请求有效工作集
- 🔗 https://github.com/llm-d/llm-d

---

## 💡 工程启发

1. **Speculative Decoding 进入 V2 时代**：SGLang 将 SpecV2 设为默认，DFLASH 从社区内核演进为多框架集成选项——spec-decoding 正从实验性优化走向生产标配，对 decode 密集型场景（长输出、代码生成）吞吐提升显著
2. **CUDA 13 成为新基线**：SGLang 默认 CUDA 13、llama.cpp 发布 CUDA 13.1 构建、ONNX Runtime 预告 CUDA 12 移除——生态正全面迁移到 CUDA 13，新项目应直接基于 CUDA 13 开发
3. **手写内核 → Megakernel 范式**：Lucebox 的做法（单次 CUDA dispatch 覆盖全模型）与 FlashAttention 的"fuse everything"理念一脉相承，但尺度更大——将整个模型视为一个 kernel。这对延迟敏感场景有极大价值，但可维护性是隐患
4. **多后端 LLM 推理加速**：MNN 的 Vulkan/MUSA/QNN/RISC-V 全覆盖、llama.cpp 的 OpenCL Adreno / Hexagon HVX / SYCL——推理优化不再局限于 CUDA，国产 GPU 和移动端正在获得一流支持
5. **PD 分离部署持续演进**：SGLang Decode Radix Cache for PD disaggregation、TensorRT-LLM gen-first ADP serving——PD 分离已从概念验证走向工程化，长前缀共享场景的 TTFT 优化是核心卖点

---

## 🔭 明日跟踪建议

1. **llama.cpp b9129+**：关注 Hexagon HMX 优化后续是否带来 Qualcomm 端侧推理性能数据
2. **vLLM DeepSeek V4**：v0.20.1/2 已密集修复，关注后续是否有 V4 性能基准数据和 best-practice 文档更新
3. **Lucebox PFlash 论文**：10.4× TTFT @ 128K 数据如果伴随 paper-style writeup，值得深入研读其 prefix-cache 算法
4. **SGLang DFLASH on ROCm**：DFLASH spec-decode 扩展到 AMD ROCm 的性能数据待公布
5. **MNN Vulkan LLM 基准**：3.5.0 已发布一个月，关注社区实测 Vulkan 后端在 Intel Arc / AMD GPU 上的 LLM 推理数据
6. **TensorRT-LLM v1.3.0 正式版**：当前 rc14，关注正式版发布节奏和 Mamba hybrid prefix caching 的生产就绪度

---

*报告生成时间：2026-05-13 14:50 CST*
*数据来源：GitHub Releases / README（web_fetch 抓取）*
