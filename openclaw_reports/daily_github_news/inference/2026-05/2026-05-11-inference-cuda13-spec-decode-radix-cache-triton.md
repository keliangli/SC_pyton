# GitHub 大模型推理日报（2026-05-11）

## 今日要点

1. **vLLM v0.20.2 发布**：修复 DeepSeek V4 稀疏注意力 persistent topk 路径（Hopper）与 KV cache 分配问题，解决 MTP=1 hang；gpt-oss MXFP4 + torch.compile 兼容性修复；Qwen3-VL deepstack 边界检查修复。
2. **SGLang v0.5.11 发布（重大版本）**：默认升级 CUDA 13 + PyTorch 2.11；Speculative Decoding V2 成为默认（overlap scheduling 隐藏 CPU 开销）；Decode 侧 Radix Cache 支持 PD 分离部署；新增 FA3 社区 kernel、DFLASH spec-decode、FlashInfer CuteDSL MoE Runner；LoRA 支持 DeepSeek-V3 / Kimi-K2（MLA MoE）；新增 Gemma 4 / GLM-5.1 / Qwen3.6 / MiMo-V2.5 等模型。
3. **llama.cpp b9102 发布**：新增 SYCL im2col_3d 算子；全面支持 CUDA 13.1 构建（Windows/Linux）。
4. **Triton v3.7.0 发布**：新增 tl.squeeze/unsqueeze、scaled BMM、FP8 常量支持、Gluon & Layout 改进；后端编译器与 AMD/HIP 优化。
5. **DeepSpeed v0.19.0 发布**：新增 Zero3 碎片整理工具；序列并行改用 deny list；FPQuantizer 构建修复。
6. **FlashInfer v0.6.11rc1 发布**：新 RC 版本，nightly 构建持续迭代。

## 项目速递

| 项目 | 版本 | 日期 | 关键更新 | 链接 |
|------|------|------|----------|------|
| vLLM | v0.20.2 | 2026-05-10 | DeepSeek V4 sparse attention 修复、KV cache 分配修复、gpt-oss MXFP4 torch.compile 修复 | [Release](https://github.com/vllm-project/vllm/releases/tag/v0.20.2) |
| SGLang | v0.5.11 | 2026-05-05 | CUDA 13 + Torch 2.11 默认、Spec V2 默认、Decode Radix Cache for PD 分离、FA3 kernel、DFLASH spec-decode、FlashInfer CuteDSL MoE、DeepSeek-V3/Kimi-K2 LoRA、Gemma 4/GLM-5.1/Qwen3.6 等新模型 | [Release](https://github.com/sgl-project/sglang/releases/tag/v0.5.11) |
| llama.cpp | b9102 | 2026-05-11 | SYCL im2col_3d 算子、CUDA 13.1 构建支持 | [Release](https://github.com/ggml-org/llama.cpp/releases/tag/b9102) |
| Triton | v3.7.0 | 2026-05-07 | tl.squeeze/unsqueeze、scaled BMM、FP8 常量、Gluon & Layout 改进、AMD/HIP 后端优化 | [Release](https://github.com/triton-lang/triton/releases/tag/v3.7.0) |
| DeepSpeed | v0.19.0 | 2026-05-06 | Zero3 碎片整理工具、SP deny list、FPQuantizer 修复 | [Release](https://github.com/deepspeedai/DeepSpeed/releases/tag/v0.19.0) |
| FlashInfer | v0.6.11rc1 | 2026-05-09 | 新 RC 版本，nightly 持续迭代 | [Release](https://github.com/flashinfer-ai/flashinfer/releases/tag/v0.6.11rc1) |
| TensorRT | v10.16 | 2026-03-25 | CUDA 13.2 默认、DistCollective 多设备执行 | [Release](https://github.com/NVIDIA/TensorRT/releases/tag/v10.16) |

## 工程启发

1. **CUDA 13 生态加速迁移**：SGLang、llama.cpp、TensorRT 近期版本均已默认或支持 CUDA 13.x。升级到 CUDA 13 是当前推理框架的必经之路，新 kernel 特性（如 Hopper 优化）依赖新 CUDA 版本。
2. **Speculative Decoding 成熟化**：SGLang Spec V2 默认开启（overlap scheduling），DFLASH 作为新 spec-decode kernel 被集成。Speculative Decoding 从实验走向生产默认，是延迟优化的关键路径。
3. **PD 分离部署持续演进**：SGLang Decode 侧 Radix Cache 支持 PD 分离，意味着 prefill/decode 分离场景下长前缀缓存命中率问题得到解决，对长上下文多租户部署有直接价值。
4. **MLA MoE 的 LoRA 支持突破**：DeepSeek-V3 / Kimi-K2 等大规模 MLA MoE 模型首次支持 LoRA，adapter 微调在最前沿架构上成为可能。
5. **Triton 前端能力扩展**：v3.7.0 新增 scaled BMM、FP8 常量、squeeze/unsqueeze 等前端特性，降低自定义 kernel 编写门槛，对推理 kernel 开发者友好度提升。
6. **DeepSeek V4 推理稳定性修复**：vLLM 连续两个 patch 修复 DeepSeek V4 sparse attention 与 KV cache 问题，反映新模型上线初期的工程打磨仍是主旋律。

## 明日跟踪建议

1. **vLLM DeepSeek V4 后续**：观察是否有更多 sparse attention / KV cache 相关修复或性能优化 PR。
2. **SGLang v0.5.11 实测**：关注社区对 Spec V2 默认、Decode Radix Cache for PD 分离的性能反馈。
3. **Triton v3.7.0 kernel 生态**：跟踪 scaled BMM / FP8 常量在推理 kernel 中的实际采用情况。
4. **FlashInfer v0.6.11 正式版**：RC1 已出，关注正式版发布节奏与 changelog。
5. **CUDA 13 兼容性**：跟踪各框架在 CUDA 13 上的 CI/CD 与用户反馈。
