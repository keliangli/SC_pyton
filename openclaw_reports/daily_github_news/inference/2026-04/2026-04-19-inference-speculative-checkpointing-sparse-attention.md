---
title: "GitHub 大模型推理日报（2026-04-19）- 投机解码checkpointing与稀疏注意力"
date: 2026-04-19
track: 大模型推理
slug: speculative-checkpointing-sparse-attention
source_report: /home/li/.openclaw/workspace/reports/github_inference_news_2026-04-19.md
repo_path: openclaw_reports/daily_github_news/inference/2026-04/2026-04-19-inference-speculative-checkpointing-sparse-attention.md
generated_by: openclaw
---

# GitHub 大模型推理日报 — 2026-04-19

> 抓取时间：2026-04-19 16:46 CST | 覆盖范围：过去 24h GitHub 活动

---

## 📌 今日要点

1. **vLLM v0.19.1 发布**（4-18）：Gemma4 修复补丁 + Transformers v5.5.4 升级 + 量化 MoE / Eagle3 支持
2. **llama.cpp 合入 speculative checkpointing**（PR #19493，4-19 merge）：基于 checkpoint 的投机解码，支持循环模块，quicksort 场景大幅加速
3. **TensorRT-LLM v1.3.0rc12**（4-17）：新增稀疏 MQA/GQA 注意力、CuteDSL MoE for Qwen3.5、FP8 LoRA、对话亲和性路由
4. **SGLang 持续迭代**：AMD NSA indexer kernel fusion、Qwen3next flashinfer allreduce 自动开启、HunyuanVideo GroupNorm+SiLU fast path
5. **清华 chitu 新增 GLM4.7-FP8 支持**：面向 DeepSeek-V3.2 的 indexer 权重合并优化

---

## 🚀 项目速递

### vLLM — v0.19.1 Patch Release
- **版本**：v0.19.1（2026-04-18）
- **关键更新**：
  - Transformers 升级至 v5.5.4
  - Gemma4 流式 tool call 修复（JSON 拆分、HTML 重复、boolean/number 截断）
  - Gemma4 量化 MoE 支持（#39045）
  - 新增 Gemma4 Eagle3 投机解码支持（#39450）
  - Kimi-K2 tool parser 修复
- **近期主分支 commit**：
  - KV Offload 传递 request context（#39185）
  - KV Connector 多连接器同类 metrics（#40010）
  - TurboQuant 移除冗余随机符号（#40194）
  - ND×ND 通用矩阵乘法（#39909）
- 🔗 https://github.com/vllm-project/vllm/releases/tag/v0.19.1

### llama.cpp — Speculative Checkpointing 合入
- **关键 PR**：#19493（2026-04-19 merge）
- **内容**：server 端新增基于 checkpoint 的投机解码，支持循环模块（recurrent modules）。使用 `--spec-type ngram-map-k --spec-ckpt-num-tries 2 --ctx-checkpoints 16` 参数。在重复性场景（如 quicksort）观察到显著加速
- **日构建**：b8836–b8840（4-18），包含：
  - media_tag 暴露到 /props 端点（#22028）
  - bias tensor 变量名重构（#22079）
  - Android libcommon→libllama-common 重命名（#22076）
  - ggml-backend 多段 tensor 读取（#22063）
  - Vulkan SPIR-V headers（#22109）
  - sentence-transformer 5.4 配置兼容（#22087）
- 🔗 https://github.com/ggml-org/llama.cpp/pull/19493

### TensorRT-LLM — v1.3.0rc12
- **版本**：v1.3.0rc12（2026-04-17）
- **关键更新**：
  - **稀疏 MQA/GQA 注意力**（#12470）：长上下文推理新优化路径
  - **CuteDSL MoE backend for Qwen3.5**（#12799）
  - **FP8 LoRA 权重加载**（#12848）+ 投机解码 + LoRA 组合（#12661）
  - **对话亲和性路由**（#12526）：disagg serving 优化
  - **KV cache 统计监控增强**（#12413）
  - **Prometheus 生产级指标**：iteration stats、token counters、phase histograms
  - **block reuse + overlap scheduler**（#12816）
  - LTX-2 两阶段 pipeline + CUDA graph 支持
- 🔗 https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc12

### SGLang — 主分支活跃
- **近期 commit**：
  - **AMD NSA indexer kernel fusion**：weights_proj + k-cache store 融合（#22850）
  - **Qwen3next flashinfer allreduce 自动启用**（#22664）
  - **HunyuanVideo GroupNorm+SiLU fast path**（#22814）
  - **LoRA MoE bias 支持**（#22169）
- **v0.5.10**（4-06）要点回顾：
  - Piecewise CUDA Graph 默认开启
  - Elastic EP 部分故障容错
  - GPU Staging Buffer for PD Disaggregation（RDMA 请求量降低 ~1000x）
  - HiSparse 稀疏注意力集成
  - FlashInfer MXFP8 kernel 支持
- 🔗 https://github.com/sgl-project/sglang

### chitu（清华大学）— GLM4.7-FP8 + DeepSeek-V3.2 优化
- **新增**：GLM4.7-FP8 量化推理支持
- **优化**：DeepSeek-V3.2 indexer 中权重合并、FA3+MixedHopper 修改
- 🔗 https://github.com/thu-pacman/chitu

### LMCache — 多进程连接器修复
- **修复**：mp connector 缓存请求存储逻辑（#3012）
- **清理**：移除 mp adapter 中冗余代码（#2994）
- 🔗 https://github.com/LMCache/LMCache

---

## 💡 工程启发

| 启发点 | 说明 |
|--------|------|
| **Speculative Checkpointing** | llama.cpp 新合入的基于 checkpoint 投机解码思路值得 vLLM/SGLang 参考：对循环/状态式模型（如 RNN-style）可大幅提升推理效率，尤其在重复 pattern 场景 |
| **稀疏 MQA/GQA 注意力** | TRT-LLM 的 sparse MQA/GQA attention 是长上下文推理的关键路径，结合 GQA 模型（Qwen3.5/DeepSeek）可直接降低 attention 计算量 |
| **FP8 LoRA + 投机解码** | TRT-LLM 将 FP8 LoRA 与 spec decode 组合，说明量化与投机解码不再是互斥路径，工程上可并行使用 |
| **对话亲和性路由** | TRT-LLM disagg serving 的 conversation-affinity routing 是生产环境 PD 分离的关键优化，减少跨节点 KV 传输 |
| **AMD NSA kernel fusion** | SGLang 在 AMD 平台持续优化 NSA indexer，说明 ROCm 生态在推理侧的成熟度在提升 |
| **CuteDSL MoE** | NVIDIA 用 CuteDSL 写 MoE kernel for Qwen3.5，暗示 Blackwell 原生 MoE kernel 路线正在成型 |

---

## 🔭 明日跟踪建议

1. **vLLM v0.19.x 后续 patch**：关注 KV Offload 机制是否进一步成熟（block-level preemption → production-ready）
2. **llama.cpp speculative checkpointing 性能数据**：等 PR 作者补充更多 benchmark（非 quicksort 场景的加速比）
3. **TRT-LLM v1.3.0 正式版**：rc12 已接近 release，关注稀疏注意力 + CuteDSL MoE 在生产环境的稳定性
4. **SGLang Elastic EP**：部分故障容错的 DeepSeek MoE 部署方案，待社区实际验证
5. **chitu GLM4.7-FP8**：关注 FP8 量化精度与吞吐数据
