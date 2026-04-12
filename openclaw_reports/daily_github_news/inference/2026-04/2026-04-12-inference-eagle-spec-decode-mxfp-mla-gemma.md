---
title: "GitHub inference daily 2026-04-12 EAGLE3 dynamic tree MXFP8 MLA Gemma4"
date: 2026-04-12
track: 大模型推理
slug: eagle-spec-decode-mxfp-mla-gemma
source_report: /home/li/.openclaw/workspace/reports/github_inference_news_2026-04-12.md
repo_path: openclaw_reports/daily_github_news/inference/2026-04/2026-04-12-inference-eagle-spec-decode-mxfp-mla-gemma.md
generated_by: openclaw
---

# GitHub 大模型推理日报 — 2026-04-12

> 抓取时间：2026-04-12 14:50 CST | 覆盖范围：过去 24h GitHub 推理相关项目

---

## 📌 今日要点

1. **TensorRT-LLM 引入 EAGLE3 动态树投机解码**（`#12062`），这是 TRT-LLM 首次支持 EAGLE3 动态树策略，标志投机解码从静态 top-k 升级到动态树搜索，有望进一步降低推理延迟。
2. **vLLM 新增 MXFP8 量化支持**（`#38815`），为 CompressedTensors 格式的 W8A8 MXFP8 量化在 linear / MoE 层面落地，量化精度与效率有望提升。
3. **SGLang 解耦 LoRA MoE 后端并引入 Marlin 支持**（`#21858`），为 MoE 模型 + LoRA 场景提供独立的量化后端路径。
4. **Gemma 4 生态加速成熟**：vLLM 修复 LoRA 加载；TRT-LLM AutoDeploy 上线 Gemma-4-31B dense + NVFP4。
5. **MLA 注意力机制持续演进**：TRT-LLM 在 flashinfer_mla 中支持 rank 256（`#12519`），为 DeepSeek 系列模型提供更灵活的 MLA 配置。

---

## 🚀 项目速递

### vLLM
| 提交/PR | 摘要 | 链接 |
|---------|------|------|
| `#39344` | fix(kimi_k25): 修复 media_placeholder_token_id 解析 | [GitHub](https://github.com/vllm-project/vllm/pull/39344) |
| `#37731` | **FP8 KVCache on XPU**：Intel GPU 上支持 FP8 KV Cache | [GitHub](https://github.com/vllm-project/vllm/pull/37731) |
| `#38815` | **CompressedTensors W8A8 MXFP8**：新增 MXFP8 量化 linear + MoE 层 | [GitHub](https://github.com/vllm-project/vllm/pull/38815) |
| `#39547` | **Perf: Fuse Zero Initializer for FP8 DeepGemm Block Quant Kernel** | [GitHub](https://github.com/vllm-project/vllm/pull/39547) |
| `#38844` | Gemma4 LoRA adapter 加载修复 | [GitHub](https://github.com/vllm-project/vllm/pull/38844) |
| `#39064` | GDN FLA kernel CUDA graph padding crash 修复 | [GitHub](https://github.com/vllm-project/vllm/pull/39064) |
| `#38316` | XPU per-channel quantization in FP8 linear method | [GitHub](https://github.com/vllm-project/vllm/pull/38316) |

### SGLang
| 提交/PR | 摘要 | 链接 |
|---------|------|------|
| `#21986` | AMD fused allreduce + RMSNorm 简化，移除 hidden_dim allowlist | [GitHub](https://github.com/sgl-project/sglang/pull/21986) |
| `#22361` | Whisper batch encoder forward：支持并发 prefill | [GitHub](https://github.com/sgl-project/sglang/pull/22361) |
| `#22567` | **Tokenizer O(n²) copy 消除**（非增量 streaming） | [GitHub](https://github.com/sgl-project/sglang/pull/22567) |
| `#21858` | **LoRA MoE 后端解耦 + Marlin 支持** | [GitHub](https://github.com/sgl-project/sglang/pull/21858) |
| `#22562` | Memory checkers 重构为可组合的 per-pool invariant checks | [GitHub](https://github.com/sgl-project/sglang/pull/22562) |
| `#22439` | Diffusion: 支持 ERNIE-Image 模型 | [GitHub](https://github.com/sgl-project/sglang/pull/22439) |

### TensorRT-LLM
| 提交/PR | 摘要 | 链接 |
|---------|------|------|
| `#12062` | **EAGLE3 动态树投机解码**（重大特性） | [GitHub](https://github.com/NVIDIA/TensorRT-LLM/pull/12062) |
| `#12955` | AutoDeploy: 修复 Gemma4 MoE config（disable multi_stream_moe） | [GitHub](https://github.com/NVIDIA/TensorRT-LLM/pull/12955) |
| `#12847` | multi_stream_moe 精度修复（MLIR + piecewise cudagraphs） | [GitHub](https://github.com/NVIDIA/TensorRT-LLM/pull/12847) |
| `#12519` | **flashinfer_mla 支持 rank 256 MLA** | [GitHub](https://github.com/NVIDIA/TensorRT-LLM/pull/12519) |
| `#12866` | AutoDeploy: 上线 Gemma-4-31B dense + NVFP4 | [GitHub](https://github.com/NVIDIA/TensorRT-LLM/pull/12866) |

### llama.cpp
| 提交/PR | 摘要 | 链接 |
|---------|------|------|
| `#21768` | CUDA: 跳过编译冗余 Flash Attention kernels（构建加速） | [GitHub](https://github.com/ggml-org/llama.cpp/pull/21768) |
| `#21756` | MERaLiON-2 多模态音频支持 | [GitHub](https://github.com/ggml-org/llama.cpp/pull/21756) |
| `#21593` | OpenCL: 基本 q5_k 量化支持 | [GitHub](https://github.com/ggml-org/llama.cpp/pull/21593) |
| `#21732` | TP: 修复 Qwen 3 Next data split | [GitHub](https://github.com/ggml-org/llama.cpp/pull/21732) |

### LMDeploy
| 提交/PR | 摘要 | 链接 |
|---------|------|------|
| `#4518` | 新增 FP32 MAMBA SSM_DTYPE 环境变量控制 recurrent state 精度 | [GitHub](https://github.com/InternLM/lmdeploy/pull/4518) |

---

## 💡 工程启发

1. **投机解码成为推理框架必争之地**：TRT-LLM 引入 EAGLE3 动态树，vLLM 早已在 v0.19.0 支持 zero-bubble async + spec decode。工程上应关注动态树策略的 acceptance rate 实测收益，而不仅仅是理论加速比。
2. **MXFP8 量化落地加速**：vLLM 和 SGLang 同步推进 MXFP8，这种 microscaling 格式在 Blackwell 上有原生硬件支持，未来 3-6 个月会成为 W8A8 量化的主流选择之一。建议在 CUDA/Triton 学习中关注 MXFP4/MXFP8 的 block scaling 机制。
3. **MLA rank 扩展性**：TRT-LLM 支持 rank 256 MLA 意味着 DeepSeek 系列模型的 KV cache 压缩可以更激进。工程上可关注 MLA 对不同 batch size 下 KV cache 节省的实测数据。
4. **跨平台推理持续发力**：vLLM XPU FP8、SGLang AMD fused allreduce、llama.cpp OpenCL q5_k — 非 NVIDIA 平台的推理优化正在从"能用"走向"好用"。

---

## 🔭 明日跟踪建议

- [ ] **TRT-LLM EAGLE3 动态树 vs 静态 top-k**：关注 benchmark 数据对比，特别是 acceptance rate 和端到端延迟
- [ ] **vLLM MXFP8 在 MoE 模型上的精度/性能表现**：是否有 accuracy regression
- [ ] **SGLang LoRA MoE + Marlin 解耦后**：是否能与其他推理框架的 MoE + LoRA 方案拉开差距
- [ ] **llama.cpp CUDA FA kernel 编译优化**：构建时间减少了多少，是否有运行时性能影响
- [ ] 继续跟踪 FlashInfer v0.6.7 nightly 版本更新（Blackwell SM120 适配进展）

---

*报告自动生成 by OpenClaw Cron | 数据来源：GitHub API + Releases*
