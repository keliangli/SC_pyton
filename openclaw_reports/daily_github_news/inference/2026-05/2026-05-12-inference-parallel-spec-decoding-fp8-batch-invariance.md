# GitHub 大模型推理日报 — 2026-05-12

---

## 今日要点

1. **llama.cpp 并行投机解码落地** — `b9109` 引入 parallel drafting support，draft context 可同时为多条 sequence 生成投机 token，支持 ngram + MTP 链式组合，标志着 llama.cpp 投机解码从单序列走向多序列并行。
2. **vLLM 批次不变性 + Cutlass FP8 取得 28.9% E2E 延迟收益** — PR #40408 用 Cutlass FP8 替代量化/反量化路径，在 Qwen3-1.7B FP8 延迟基准上取得显著提升；同时 #41429 开始消除 GPU↔CPU 同步点的系列优化。
3. **SGLang EAGLE-3 + SWA 支持 & PD 状态迁移重构** — 新增 EAGLE-3 drafter 的滑动窗口注意力支持，解决短上下文训练模型长序列推理问题；PD disaggregation 状态迁移重构为可扩展的 state_type 列表架构。
4. **FlashInfer SM120 fmha_v2 内核 & Blackwell GDN 修复** — 持续推进 Blackwell/SM120 架构内核适配，新增 AOT pip wheel 构建。
5. **TensorRT-LLM Multi-K GVR Top-K & VisualGen 批量推理** — GVR Top-K 扩展至多 K 值（512/1024/2048）和多精度，稀疏注意力能力增强。

---

## 项目速递

### vLLM
| 更新 | 链接 |
|------|------|
| v0.20.2 发布：DeepSeek V4 稀疏注意力修复、Qwen3-VL 修复 | [v0.20.2](https://github.com/vllm-project/vllm/releases/tag/v0.20.2) |
| 批次不变性 + Cutlass FP8，E2E 延迟 -28.9% | [#40408](https://github.com/vllm-project/vllm/pull/40408) |
| 消除 GPU↔CPU 不必要同步点 (1/n) | [#41429](https://github.com/vllm-project/vllm/pull/41429) |
| VLLM_USE_SPINLOOP_EXT：高效忙等轮询（monitorx/mwaitx） | [#36517](https://github.com/vllm-project/vllm/pull/36517) |
| ROCm DSv4 flash sparse MLA Triton kernel | [#41812](https://github.com/vllm-project/vllm/pull/41812) |
| DeepGEMM SiLU/mul FP8 Triton kernel int32 溢出修复 | [#42201](https://github.com/vllm-project/vllm/pull/42201) |
| Gemma4 混合分辨率图像共批崩溃修复 | [#42217](https://github.com/vllm-project/vllm/pull/42217) |
| Apple Silicon (vLLM-Metal) 文档 | [#41987](https://github.com/vllm-project/vllm/pull/41987) |

### SGLang
| 更新 | 链接 |
|------|------|
| EAGLE-3 SWA（滑动窗口注意力）支持 | [#24664](https://github.com/sgl-project/sglang/pull/24664) |
| 支持更新版 EAGLE-3 drafter | [#24663](https://github.com/sgl-project/sglang/pull/24663) |
| PD 状态迁移重构（可扩展 state_type 架构） | [#24932](https://github.com/sgl-project/sglang/pull/24932) |
| Linear Attn 自定义内核后端插件化 | [#24937](https://github.com/sgl-project/sglang/pull/24937) |
| DeepSeek-V4-Pro shared expert TP1 | [#24949](https://github.com/sgl-project/sglang/pull/24949) |
| Spec V2 Mamba scatter 清理 & 多层 bug 修复 | [#25029](https://github.com/sgl-project/sglang/pull/25030) |
| HiCache 默认存储预取超时 | [#23309](https://github.com/sgl-project/sglang/pull/23309) |
| Kimi K2.5 MLA EAGLE + DP attention 修复 | [#25033](https://github.com/sgl-project/sglang/pull/25033) |

### llama.cpp
| 更新 | 链接 |
|------|------|
| **并行投机解码支持** — 多序列并行 draft | [b9109](https://github.com/ggml-org/llama.cpp/releases/tag/b9109) |
| OpenCL Q4_1 MoE for Adreno | [b9113](https://github.com/ggml-org/llama.cpp/releases/tag/b9113) |
| CUDA im2col OW>65535 修复（1D 音频编码器） | [b9112](https://github.com/ggml-org/llama.cpp/releases/tag/b9112) |
| Vulkan 非对称 FA 支持 | [b9106](https://github.com/ggml-org/llama.cpp/releases/tag/b9106) |
| Metal mul_mv/mul_mm batch divisor 提升为函数常量 | latest main |

### TensorRT-LLM
| 更新 | 链接 |
|------|------|
| Multi-K/Multi-dtype GVR Top-K | [#13948](https://github.com/NVIDIA/TensorRT-LLM/commit/de190a0) |
| VisualGen 批量推理 | [#12350](https://github.com/NVIDIA/TensorRT-LLM/commit/defc515) |
| V2 delay batching KV page 释放修复 | [#13805](https://github.com/NVIDIA/TensorRT-LLM/commit/7bc328f) |
| SageAttention for Wan/FLUX | [#13570](https://github.com/NVIDIA/TensorRT-LLM/commit/bf4a843) |
| Mamba SSD prefill 优化 + FlashInfer dispatch 扩展 | [#12731](https://github.com/NVIDIA/TensorRT-LLM/commit/da321a2) |

### FlashInfer
| 更新 | 链接 |
|------|------|
| SM120 fmha_v2 内核加入 AOT pip wheel | [#2885](https://github.com/flashinfer-ai/flashinfer/pull/2885) |
| Blackwell GDN decode int64 溢出修复 | [#3230](https://github.com/flashinfer-ai/flashinfer/pull/3230) |
| 移除 over-strict K%4 assert | [#3163](https://github.com/flashinfer-ai/flashinfer/pull/3163) |

### LMCache
| 更新 | 链接 |
|------|------|
| 多设备 torch.device 全局抽象 | [#3091](https://github.com/LMCache/LMCache/pull/3091) |
| GPU mode test-cache CLI | [#3013](https://github.com/LMCache/LMCache/pull/3013) |
| Fast-path L2 store throughput 可观测性修复 | [#3257](https://github.com/LMCache/LMCache/pull/3257) |

### Mooncake
| 更新 | 链接 |
|------|------|
| DSA-like workload allocation 策略 | [#2080](https://github.com/kvcache-ai/Mooncake/commit/8a5dd54) |
| SpinLock 内存序修复（弱序架构） | [#2076](https://github.com/kvcache-ai/Mooncake/commit/ef0f40c) |
| MACA/MetaX GPU 支持 + RDMA dmabuf 注册修复 | [#2002](https://github.com/kvcache-ai/Mooncake/commit/6caf412) |

---

## 工程启发

1. **投机解码进入并行时代** — llama.cpp 的 parallel drafting 和 SGLang 的 EAGLE-3 + SWA 说明投机解码已从单序列串行演化为多序列并行 + 多种投机策略链式组合。工程上需关注 draft context 管理和序列同步开销。
2. **FP8 路径深化** — vLLM 的 Cutlass FP8 batch invariance、DeepGEMM int32 溢出修复、FlashInfer MXFP8/SM120 适配，表明 FP8 推理正在从"能用"走向"好用"，但数值稳定性问题（溢出、assert）仍需持续关注。
3. **GPU↔CPU 同步消除是低垂果实** — vLLM #41429 系列说明即使成熟框架，仍然存在大量不必要的 GPU↔CPU 同步点，逐个消除即可获得可观延迟收益，值得在其他框架中系统性排查。
4. **PD 分离部署架构持续演进** — SGLang 的 hybrid state transfer 重构、Mooncake 的 DSA-like workload allocation、LMCache 的多设备抽象，都在为更灵活的 PD 分离部署打基础。
5. **异构硬件适配加速** — OpenCL Q4_1 MoE for Adreno、Vulkan asymmetric FA、Mooncake MACA/MetaX GPU、vLLM Apple Silicon 文档 — 推理框架的硬件覆盖面从 NVIDIA 扩展到 AMD/Qualcomm/Apple/MetaX。

---

## 明日跟踪建议

- [ ] **vLLM GPU↔CPU sync 消除系列** — #41429 标注 1/n，后续 PR 持续跟进
- [ ] **llama.cpp parallel drafting 性能基准** — 多序列并行 draft 的 acceptance rate 和吞吐收益待社区 benchmark
- [ ] **SGLang EAGLE-3 SWA 长上下文效果** — 论文即将发布，关注 acceptance length 提升数据
- [ ] **FlashInfer SM120 fmha_v2** — Blackwell 原生内核的 AOT 构建，后续性能数据
- [ ] **TensorRT-LLM Mamba SSD prefill 优化** — 混合架构模型的 prefill 路径优化进展
