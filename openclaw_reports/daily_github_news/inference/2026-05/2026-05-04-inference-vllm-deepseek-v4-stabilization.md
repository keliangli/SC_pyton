# GitHub 大模型推理技术日报 — 2026-05-04

> 数据窗口：2026-05-03 14:50 ~ 2026-05-04 14:50 (Asia/Shanghai)
> 数据源：GitHub Releases + Commits（vLLM / llama.cpp / SGLang / TensorRT-LLM / FlashInfer / LMDeploy）

---

## 今日要点

| # | 要点 | 重要度 |
|---|------|--------|
| 1 | **vLLM v0.20.1 发布**：DeepSeek V4 稳定化补丁版，含多流 pre-attention GEMM、MXFP8 all-to-all、PTX cvt FP32→FP4、tile kernel 融合、TopK 死锁修复 | 🔴 高 |
| 2 | **SGLang MoE LoRA 新后端**：csgmv + virtual experts 支持 MoE LoRA (#24007)，扩展 MoE 服务化灵活性 | 🔴 高 |
| 3 | **llama.cpp b9014 发布**：WebGPU layer norm op + Kahan summation，推进浏览器端推理精度 | 🟡 中 |
| 4 | **TensorRT-LLM AutoDeploy MLA PWCG**：DeepSeek R1 MLA 自动部署支持 PWCG (#13497)，优化 EP 部署 | 🟡 中 |
| 5 | **FlashInfer nightly 0503**：持续迭代 v0.6.9 分支，配合 vLLM MXFP8 all-to-all | 🟢 低 |

---

## 项目速递

### 1. vLLM — v0.20.1 Release

**发布时间**：2026-05-03 16:24 CST

核心变更（聚焦 DeepSeek V4 稳定化）：

| 分类 | 变更 | PR |
|------|------|----|
| 🔥 DeepSeek V4 | Base model 支持 | [#41006](https://github.com/vllm-project/vllm/pull/41006) |
| 🔥 性能 | 多流 pre-attention GEMM + 可配置 knob | [#41061](https://github.com/vllm-project/vllm/pull/41061) [#41443](https://github.com/vllm-project/vllm/pull/41443) [#41526](https://github.com/vllm-project/vllm/pull/41526) |
| 🔥 性能 | BF16 & MXFP8 all-to-all (FlashInfer) | [#40960](https://github.com/vllm-project/vllm/pull/40960) |
| 🔥 性能 | PTX cvt 指令加速 FP32→FP4 转换 | [#41015](https://github.com/vllm-project/vllm/pull/41015) |
| 🔥 性能 | tile kernel (head_compute_mix_kernel) 融合 | [#41255](https://github.com/vllm-project/vllm/pull/41255) |
| 🐛 Bugfix | Persistent TopK cooperative 死锁 (TopK=1024) + 临时禁用 workaround | [#41189](https://github.com/vllm-project/vllm/pull/41189) [#41442](https://github.com/vllm-project/vllm/pull/41442) |
| 🐛 Bugfix | 退化 KV cache stride 导致 TMA cudaErrorIllegalInstruction | [#40737](https://github.com/vllm-project/vllm/pull/40737) |
| 🐛 Bugfix | FP8 bias loading 修复 | [#41424](https://github.com/vllm-project/vllm/pull/41424) |
| 🐛 Bugfix | RayExecutorV2 actor name collision (DP>1) | [#40398](https://github.com/vllm-project/vllm/pull/40398) |
| 🐛 Bugfix | BailingMoE linear layer + MLA RoPE rotation | [#40859](https://github.com/vllm-project/vllm/pull/40859) [#41185](https://github.com/vllm-project/vllm/pull/41185) |
| 🐛 Bugfix | max_num_batched_token CUDA graph 未捕获 | [#40734](https://github.com/vllm-project/vllm/pull/40734) |

🔗 [Release 页](https://github.com/vllm-project/vllm/releases/tag/v0.20.1)

---

### 2. llama.cpp — b9014 + b9012

**b9014**（2026-05-04 13:25 CST）：
- **WebGPU layer norm ops** (#22406)：Shader 实现 LayerNorm，使用 Kahan summation 提升浮点精度；移除非连续 stride 支持
- Vulkan: 删除废弃 `GGML_VK_MAX_NODES` def (#22621)

**b9012**（2026-05-04 04:49 CST）：
- **Mistral 格式 yarn apply_scale** (#22612)：修复 Mistral 模型格式转换时 RoPE scaling 参数处理

其他 24h commits：
- NVFP4 repack path 中 Q/K RoPE permutation (#22611)
- Generation prompt 最长公共前缀推断 (#22657)
- Speculative decoding 参数文档更新 (#22539)

🔗 [b9014](https://github.com/ggml-org/llama.cpp/releases/tag/b9014) · [b9012](https://github.com/ggml-org/llama.cpp/releases/tag/b9012)

---

### 3. SGLang — MoE LoRA + DeepSeek V32 alias

24h 重要 commits（无新 release）：

| 变更 | PR |
|------|----|
| **feat(lora): csgmv backend + virtual experts for MoE LoRA** | [#24007](https://github.com/sgl-project/sglang/pull/24007) |
| Register deepseek_v32 alias（不改 config.json） | [#24295](https://github.com/sgl-project/sglang/pull/24295) |
| nextn subclass owns post_load_weights | [#24333](https://github.com/sgl-project/sglang/pull/24333) |
| dedup state_kv_args setup | [#24340](https://github.com/sgl-project/sglang/pull/24340) |
| extract adjust_hybrid_swa_layers_for_pp | [#24334](https://github.com/sgl-project/sglang/pull/24334) |
| Diffusion: disable VAE CPU offload by default | [#24315](https://github.com/sgl-project/sglang/pull/24315) |

🔗 [Commits](https://github.com/sgl-project/sglang/commits/main)

---

### 4. TensorRT-LLM — AutoDeploy MLA PWCG

24h 重要 commits（无新 release，最新 v1.3.0rc13 Apr 29）：

| 变更 | PR |
|------|----|
| **[feat] AutoDeploy MLA with PWCG on DeepSeek R1** | [#13497](https://github.com/NVIDIA/TensorRT-LLM/pull/13497) |
| [fix] V2 KV cache extra_tokens 修复 (test unwaive) | [#13709](https://github.com/NVIDIA/TensorRT-LLM/pull/13709) |
| [fix] AutoDeploy: skip nvfp4 test pre-blackwell | [#13494](https://github.com/NVIDIA/TensorRT-LLM/pull/13494) |
| [docs] GVR Top-K 技术博客 | [#13714](https://github.com/NVIDIA/TensorRT-LLM/pull/13714) |

🔗 [Commits](https://github.com/NVIDIA/TensorRT-LLM/commits/main)

---

### 5. FlashInfer — nightly 0503

- **nightly-v0.6.9-20260503**（May 3）：持续 nightly 构建，配合 vLLM MXFP8 all-to-all 需求
- **v0.6.10rc1**（Apr 30）：下一个稳定版候选

🔗 [Releases](https://github.com/flashinfer-ai/flashinfer/releases)

---

## 工程启发

### 1. DeepSeek V4 稳定化信号明确
vLLM v0.20.1 用 181 commits 打稳定化补丁，重点落在：
- **多流 GEMM 融合**：pre-attention 阶段并行化是 MoE 大模型 throughput 关键路径
- **PTX 内联指令**：FP32→FP4 转换用 `cvt` 指令替代通用路径，说明低精度量化 kernel 优化已深入到 PTX 层
- **TopK 死锁**：persistent TopK cooperative 方案在 TopK=1024 触发 CTA 间竞争，临时禁用后需要重新设计调度策略

**启发**：MoE 大模型推理的 kernel 融合与调度是当前最活跃的工程方向，TopK 路径的 CTA 协调问题是关键难点。

### 2. MoE LoRA 服务化进展
SGLang 的 csgmv backend + virtual experts (#24007) 让 MoE 模型也能用 LoRA 做 multi-tenant serving，这意味着：
- MoE 的 expert 可以在 serving 时动态组合 virtual expert + LoRA adapter
- csgmv (cutlass-style grouped GEMM) 后端为 MoE LoRA 提供高效分组计算

**启发**：MoE LoRA 是下一个服务化热点，csgmv 的分组 GEMM 思路可借鉴到自定义 kernel。

### 3. WebGPU 推理精度提升
llama.cpp WebGPU layer norm 用 Kahan summation 处理浮点精度——浏览器端推理的数值稳定性问题开始被重视。

**启发**：边缘/浏览器推理场景下，数值稳定性与性能的平衡是独立优化方向，Kahan summation 是通用手法。

### 4. TensorRT-LLM MLA AutoDeploy
AutoDeploy MLA with PWCG（Piecewise Continuous Graph）支持 DeepSeek R1，说明 TRT-LLM 正在自动化 MLA 模型的 EP 部署流程。

**启发**：AutoDeploy + PWCG 是 TRT-LLM 的差异化能力，关注其 MLA 自动编译流程对国产 MoE 模型的适用性。

---

## 明日跟踪建议

| # | 主题 | 原因 |
|---|------|------|
| 1 | **vLLM Persistent TopK 重新设计** | 当前 workaround 禁用，需关注后续修复方案 |
| 2 | **SGLang MoE LoRA 性能数据** | csgmv backend 合入后，关注 benchmark 数据和吞吐对比 |
| 3 | **TensorRT-LLM GVR Top-K 博客内容** | 刚合入 docs PR，关注 Top-K 优化技术细节 |
| 4 | **FlashInfer v0.6.10 正式版** | rc1 已发布，关注正式版时间点和 MXFP8 支持 |
| 5 | **llama.cpp WebGPU 后续 op** | layer norm 已落地，关注后续 softmax / attention 等 op 补齐 |

---

> 报告生成时间：2026-05-04 14:50 CST
> 本报告由 OpenClaw cron 任务自动生成