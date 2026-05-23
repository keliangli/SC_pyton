# GitHub 大模型推理日报（2026-05-23）

> 抓取时间：2026-05-23 14:50 CST | 覆盖范围：过去 24-48h GitHub releases & trending

---

## 📌 今日要点

1. **vLLM v0.21.0 正式发布**（5月15日 tag，近日持续热更）— 367 commits，核心升级：Transformers v4 废弃、C++20 强制、KV Offload + HMA 混合内存分配器、TOKENSPEED_MLA Blackwell 后端、Speculative Decoding 支持 thinking budget。
2. **SGLang v0.5.12 发布**（5月16日）— DeepSeek V4 完整推理链路（TP/EP/CP/DP + PD 分离 + HiSparse + W4A4 MegaMoE）、TokenSpeed MLA Blackwell FP8 KV Cache、DSv3.2/GLM-5 FP4 低延迟优化。
3. **llama.cpp build b9294 发布**（5月23日 今天）— OpenCL 通用化 Adreno MoE 内核、新增 CUDA 13.1 Windows 构建。
4. **TensorRT-LLM v1.3.0rc15**（5月21日）— Gemma4 多模态、Kimi K2.5 视觉+推理、DeepSeek V4/V3.2 新注意力内核。
5. **新兴项目观察**：Rapid-MLX（Apple Silicon 4.2x Ollama）、xinfer（纯 Rust 推理无 Python）、KVBoost（chunk 级 KV cache 复用）、Kiln（LoRA 热切换在线学习推理服务器）。

---

## 🚀 项目速递

### vLLM v0.21.0
- **链接**：https://github.com/vllm-project/vllm/releases/tag/v0.21.0
- **核心更新**：
  - 🔴 **Breaking**：Transformers v4 正式废弃，必须迁移 v5；C++20 编译器强制要求
  - 🧠 **KV Offload + HMA**：KV offloading 子系统集成混合内存分配器，支持 sliding window group
  - ⚡ **TOKENSPEED_MLA 后端**：Blackwell GPU 上 DeepSeek-R1 / Kimi-K25 的 prefill + decode 专用 MLA attention
  - 🔮 **Speculative Decoding + Thinking Budget**：推理模型 spec decode 现已支持 thinking budget
  - 🏗️ **DeepSeek V4**：AMD/ROCm 支持、Pipeline Parallelism、max reasoning effort、disagg serving 修复
  - 🆕 **新架构支持**：MiMo-V2.5、Laguna XS.2、Moondream3、Qianfan-OCR、Cohere MoE/Eagle
  - 🔧 **Spec Dec 扩展**：EAGLE for Mistral、Gemma4 MTP、MTP for MiMo-V2.5

### SGLang v0.5.12
- **链接**：https://github.com/sgl-project/sglang/releases/tag/v0.5.12
- **核心更新**：
  - 🐉 **DeepSeek V4 完整支持**：Day-0 即覆盖 TP/EP/CP/DPA + PD 分离 + HiSparse offload + DeepGemm/FlashMLA/MegaMoE 内核
  - ⚡ **TokenSpeed MLA 后端**：SM100 Blackwell FP8 KV Cache 低延迟 MLA serving
  - 🔥 **W4A4 MegaMoE 内核**：速度提升显著，精度损失可忽略
  - 🧪 **Marlin/FlashInfer W4A8 MoE**：Hopper 平台优化
  - 🚀 **DSv3.2 / GLM-5 FP4 低延迟**：PDL 启用 + Cute-DSL FP4 dense GEMM
  - 🗂️ **HiCache + UnifiedRadixTree**：统一前缀树下的 KV 缓存层级管理，SSD offload via Mooncake
  - 🆕 **新模型**：Intern-S2-Preview、MiniCPM-V 4.6、Laguna-XS.2、Ring-2.6-1T、Gemma 4 MTP
  - 🐳 **统一 Docker tag**：`lmsysorg/sglang:v0.5.12` 覆盖所有 NVIDIA GPU

### llama.cpp b9294
- **链接**：https://github.com/ggml-org/llama.cpp/releases/tag/b9294
- **核心更新**：
  - 📱 **OpenCL**：通用化 Adreno MoE 内核（移动端 MoE 模型推理改善）
  - 🖥️ **CUDA 13.1**：Windows 构建 now 支持 CUDA 13.1
  - 🔧 **OpenVINO 2026.0**：新增 Ubuntu x64 OpenVINO 构建
  - 🏗️ **SYCL**：持续提供 FP32/FP16 构建

### TensorRT-LLM v1.3.0rc15
- **链接**：https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc15
- **核心更新**：
  - 🖼️ **Gemma4 多模态**：text + vision + audio + chunked prefill
  - 👁️ **Kimi K2.5**：多模态视觉支持 + reasoning parser
  - 🐉 **DeepSeek V4/V3.2**：新注意力内核、路由更新、tokenizer 加载、AutoConfig 注册
  - 🆕 **新模型**：GPT-OSS、Ministral3、Nemotron-H、Nemotron Nano
  - 🏗️ **API**：typed exception hierarchy

### 新兴项目

| 项目 | 描述 | 链接 |
|------|------|------|
| **Rapid-MLX** | Apple Silicon 最快本地推理引擎，4.2x Ollama，0.08s cached TTFT，17 tool parsers，兼容 Claude Code/Cursor/Aider | https://github.com/raullenchai/Rapid-MLX |
| **xinfer** | 纯 Rust LLM 推理，零 Python/PyTorch 依赖，可移植生产级 | https://github.com/guoqingbao/xinfer |
| **KVBoost** | chunk 级 KV cache 复用，加速本地 LLM 推理 | https://github.com/pythongiant/KVBoost |
| **Kiln** | 推理服务 + LoRA 热切换在线学习，边服务边训练 | https://github.com/ericflo/kiln |

---

## 💡 工程启发

1. **Blackwell MLA 成为标配**：vLLM 和 SGLang 同步上线 TokenSpeed MLA 后端，Blackwell GPU 的 MLA prefill/decode 专用内核已从实验走向生产。如果团队有 B200/B300 资源，现在是切换 MLA serving 的窗口期。

2. **DeepSeek V4 推理生态成熟度**：三大框架（vLLM/SGLang/TRT-LLM）均已完整支持 DS-V4，SGLang 最激进（W4A4 MegaMoE、HiCache+SSD offload、TP16 on H100/H20）。选型时 SGLang 在 DS-V4 场景领先半步。

3. **HMA 混合内存分配器**：vLLM 的 KV Offload + HMA 标志着 GPU/CPU/SSD 三级内存管理从手工调参走向框架自动调度，对长上下文场景（>128K）是重大利好。

4. **Speculative Decoding + Thinking**：vLLM 让 spec decode 兼容 reasoning/thinking budget，意味着推理模型不再需要关闭 spec decode，吞吐提升空间重新打开。

5. **纯 Rust 推理引擎崛起**：xinfer 代表"去 Python 化"趋势——部署无依赖、冷启动极快、适合边缘/嵌入式场景。值得关注是否支持更多量化格式。

6. **KV Cache 复用粒度细化**：KVBoost 的 chunk-level 复用是对 prefix caching 的补充思路，本地推理场景（重复 system prompt）可能有显著 TTFT 收益。

---

## 🔭 明日跟踪建议

1. **vLLM v0.21 后续补丁**：刚发大版本，后续几天可能有 hotfix（特别是 HMA 和 MLA 后端的稳定性修复）。
2. **SGLang DS-V4 cookbook 更新**：docs.sglang.io/cookbook 的 DeepSeek-V4 部署命令可能持续更新。
3. **llama.cpp Adreno MoE 性能数据**：移动端 MoE 推理 benchmark 是否有实质提升，需要等待社区反馈。
4. **Rapid-MLX eval 报告**：4.2x Ollama 的声明需要独立验证，关注其 evals/ 目录更新。
5. **Kiln LoRA hot-swap 稳定性**：在线学习 + 推理同服的延迟抖动数据，目前缺公开 benchmark。
