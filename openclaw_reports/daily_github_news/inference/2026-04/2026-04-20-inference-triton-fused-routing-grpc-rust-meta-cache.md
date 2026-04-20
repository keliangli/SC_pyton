---
title: "GitHub 大模型推理日报（2026-04-20）- Triton 融合路由 / Rust gRPC / meta 后端缓存优化"
date: 2026-04-20
track: 大模型推理
slug: triton-fused-routing-grpc-rust-meta-cache
source_report: /home/li/.openclaw/workspace/reports/github_inference_news_2026-04-20.md
repo_path: openclaw_reports/daily_github_news/inference/2026-04/2026-04-20-inference-triton-fused-routing-grpc-rust-meta-cache.md
generated_by: openclaw
---

# GitHub 大模型推理日报 — 2026-04-20

## 今日要点

1. **vLLM Gemma4 融合路由 Triton 内核合并**（#39083）：将 Gemma4 的路由函数用 Triton 融合实现，消除多次全局内存读写和同步点，且可被 torch.compile 捕获，A100/H100/MI300X/B60 均验证通过。
2. **SGLang 原生 gRPC 服务端起步**（#22736）：RFC Phase 1 落地，定义 25 个 RPC 的 proto + Rust crate 脚手架 + 服务端参数，为 Rust 高性能 gRPC 服务铺路。
3. **TensorRT-LLM Minimax RMS Norm 优化**（#12163）：新增 allreduce RMS 内核，避免 all-gather→norm→slice 的冗余通信与全张量物化，TP 场景通信量显著降低。
4. **llama.cpp meta 后端 CPU 开销优化**（#22041）：缓存子图切分结果，CUDA fast uid check 路径命中，Qwen3.5-MoE tg128 提速 ~16%。
5. **SGLang StreamingSession 常驻化**（#23202）：将 StreamingSession 嵌入 UnifiedRadixCache，非流式请求零开销短路返回，简化缓存层。

## 项目速递

### vLLM
| PR | 要点 | 链接 |
|---|---|---|
| #39083 | **[Perf] Gemma4 融合路由 Triton 内核** — 减少 sync/GMEM 访问，torch.compile 友好 | [PR](https://github.com/vllm-project/vllm/pull/39083) |
| #40283 | **[Perf] Nemotron VL 预处理优化** — resize+normalize+cast 融合至 torch.compile，减少 CPU/内存 | [PR](https://github.com/vllm-project/vllm/pull/40283) |
| #40245 | **[Bugfix] Qwen RMSNormGated sigmoid 修复** — forward_native 缺少 sigmoid 激活 | [PR](https://github.com/vllm-project/vllm/pull/40245) |
| #40273 | **[Bugfix] MoE 后端选择修复（LoRA 场景）** — 未量化 MoE + LoRA 时后端选择错误 | [PR](https://github.com/vllm-project/vllm/pull/40273) |
| #38579 | **[Bugfix] Kimi-K2 工具解析流式修复** — token 泄露、参数截断、内容丢失 | [PR](https://github.com/vllm-project/vllm/pull/38579) |
| #39478 | **[Feat] RISC-V 多 VLEN 编译时分发** | [PR](https://github.com/vllm-project/vllm/pull/39478) |
| #39120 | **[Bugfix] ROCm AITER FA 投机解码 cu_seqlens 偏移** | [PR](https://github.com/vllm-project/vllm/pull/39120) |
| #39977 | **[XPU] torch.compile 跳过 CUDA graph 内存估算** | [PR](https://github.com/vllm-project/vllm/pull/39977) |

> 注：v0.19.1 于 4/18 发布，含 Gemma4 Eagle3 支持、量化 MoE 支持及多项 bugfix。

### SGLang
| PR | 要点 | 链接 |
|---|---|---|
| #22736 | **[gRPC] 原生 Rust gRPC 服务端 proto + 脚手架** — 25 RPC，Phase 1 不影响运行时 | [PR](https://github.com/sgl-project/sglang/pull/22736) |
| #23202 | **[Core] StreamingSession 常驻化** — 非流式请求零开销 | [PR](https://github.com/sgl-project/sglang/pull/23202) |
| #21249 | **[Perf] allreduce fusion 支持 context parallel** | [PR](https://github.com/sgl-project/sglang/pull/21249) |
| #23185 | **[Bugfix] DeepEP + DeepGeMM EP+DP+TP 编译超时** | [PR](https://github.com/sgl-project/sglang/pull/23185) |
| #22598 | **[AMD] TBO 运行时元数据初始化错误修复** | [PR](https://github.com/sgl-project/sglang/pull/22598) |
| #23159 | **[Revert] PCG inductor FP8 优化回退** — 存在回归 | [PR](https://github.com/sgl-project/sglang/pull/23159) |
| #21388 | **[Feat] 多平台 Plugin 机制** | [PR](https://github.com/sgl-project/sglang/pull/21388) |

### TensorRT-LLM
| PR | 要点 | 链接 |
|---|---|---|
| #12163 | **[Perf] Minimax RMS Norm allreduce 优化** — 避免全量 all-gather，本地分片计算方差 | [PR](https://github.com/NVIDIA/TensorRT-LLM/pull/12163) |
| #12882 | **[Feat] Gen-only 同步 KV 传输 v2 + 管理器 v2** — 分离式服务阻塞 KV 接收 | [PR](https://github.com/NVIDIA/TensorRT-LLM/pull/12882) |
| #13032 | **[Perf] Nemotron-H Python 层优化** — 更多 C++ 路由组合 + Mamba 张量预计算 | [PR](https://github.com/NVIDIA/TensorRT-LLM/pull/13032) |

> 注：v1.3.0rc12 于 4/17 发布，含 LTX-2 支持、CuteDSL MoE for Qwen3.5、FP8 LoRA 等。

### llama.cpp
| PR | 要点 | 链接 |
|---|---|---|
| #22041 | **[Perf] meta 后端 CPU 开销优化** — 缓存子图切分，tg128 提速 16% | [PR](https://github.com/ggerganov/llama.cpp/pull/22041) |
| #21741 | **[API] --clear-idle → --cache-idle-slots 重命名** | [PR](https://github.com/ggerganov/llama.cpp/pull/21741) |
| #22051 | **[CUDA] AMD MMA 数据加载重构** | [PR](https://github.com/ggerganov/llama.cpp/pull/22051) |
| #22102 | **[Bugfix] GLM-DSA vocab_only tokenize 崩溃** | [PR](https://github.com/ggerganov/llama.cpp/pull/22102) |

### 其他
| 项目 | 要点 | 链接 |
|---|---|---|
| ms-swift #9151 | [Megatron] 支持 mtp_shared_weights | [PR](https://github.com/modelscope/ms-swift/pull/9151) |
| unsloth | Qwen3.6 支持 + README 更新 | [Repo](https://github.com/unslothai/unsloth) |

## 工程启发

1. **Triton 融合内核是 MoE 路由优化的关键路径**：vLLM Gemma4 路由融合消除多次 global sync，SGLang PCG inductor FP8 优化被回退说明自动融合不一定稳定——手写 Triton 内核更可控。
2. **TP 场景的 Norm 优化需要避免 all-gather**：TRT-LLM Minimax RMS Norm 用 allreduce 替代 all-gather→slice，思路可推广到其他 TP Norm 场景。
3. **llama.cpp 侧 cache 子图切分思路值得借鉴**：推理框架中重复计算子图结构是常见浪费，缓存策略在 decode 阶段收益明显（16% tg 提升）。
4. **gRPC + Rust 是推理服务新方向**：SGLang 走 Rust gRPC 路线，与 vLLM gRPC（Python）形成对比，值得持续关注性能对比。
5. **SGLang StreamingSession 常驻化是好的架构实践**：零开销短路模式，避免 feature flag 污染核心路径。

## 明日跟踪建议

- 🔍 **vLLM Gemma4 fused routing 合入后性能基准**：观察 A100/H100 端到端吞吐变化。
- 🔍 **SGLang gRPC Phase 2 进展**：关注 Rust 运行时实现 PR。
- 🔍 **TRT-LLM v1.3.0 正式版发布时间线**：rc12 已出，关注 rc13 或正式版。
- 🔍 **llama.cpp meta 后端优化后续**：观察是否扩展到更多模型的 tg 提速。
- 🔍 **SGLang PCG inductor FP8 优化重提**：revert 后是否会有修复版重新合入。
