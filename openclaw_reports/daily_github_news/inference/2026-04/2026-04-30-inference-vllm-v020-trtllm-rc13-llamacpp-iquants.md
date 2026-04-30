# GitHub 大模型推理日报（2026-04-30）

> 采集时间窗口：2026-04-29 06:50 UTC — 2026-04-30 06:50 UTC

---

## 今日要点

1. **vLLM v0.20.0 重大版本发布**（4月27日）—— 752 commits / 320 contributors，核心更新：DeepSeek V4 初步支持、CUDA 13.0 默认切换、PyTorch 2.11 升级、FlashAttention 4 默认 MLA prefill、TurboQuant 2-bit KV cache、在线量化前端、vLLM IR 骨架
2. **TensorRT-LLM v1.3.0rc13 发布**（4月29日）—— Nemotron 3 Nano Omni 支持、稀疏 MQA/GQA 注意力、EAGLE3 投机解码恢复、FP4 残差量化、VisualGen Cache-DiT
3. **llama.cpp b8981 + fast matmul iquants**（4月29日-30日）—— 新增 reasoning budget sampler 修复、fast matmul iquants 内核（#22504）
4. **SGLang 主线活跃修复**—— Qwen3.5 FP8 per-tensor scale 广播修复、XPU deterministic 模式、moss-vl Conv3dLayer 修复

---

## 项目速递

### vLLM v0.20.0

- **链接**：[Release v0.20.0](https://github.com/vllm-project/vllm/releases/tag/v0.20.0)
- **发布日期**：2026-04-27
- **核心更新**：
  - 🔥 **DeepSeek V4**：初步支持（#40860），含 DSML token-leakage 修复（#40806）、DSA + MTP IMA 修复（#40772）、shared expert silu clamp（#40950）
  - 🔧 **CUDA 13.0 默认**：PyPI wheel 和 Docker 镜像默认 CUDA 13.0（#39878），升级至 CUDA 13.0.2 匹配 PyTorch 2.11（#40669）；建议 CUDA 12.9 用户用 `uv --torch-backend=cu129`
  - 🚀 **PyTorch 2.11 升级**：CUDA/XPU 均切换至 torch 2.11（#34644, #37947），**breaking change**
  - 🐍 **Python 3.14**：加入支持列表（#34770）
  - 🤗 **Transformers v5**：支持 transformers>=5（#30566），兼容 v4/v5
  - ⚡ **FlashAttention 4 默认 MLA prefill**：head-dim 512 + paged-KV 支持 SM90+（#38819, #38835）
  - 🗜️ **TurboQuant 2-bit KV cache**：4× 容量压缩，已支持 FA3/FA4 prefill（#38479, #40092）
  - 📦 **在线量化前端**：统一 FP8/MXFP8/experts_int8 在线量化入口（#38138, #38463, #40152）
  - 🏗️ **vLLM IR 骨架**：rms_norm op + OOT-platform kernel import + benchmark 基础设施（#33825, #38807, #40167）
  - 🏃 **Model Runner V2**：Eagle prefill full-CUDA-graph、fused rejection sample kernels、多 prompt-logprobs（#37588, #38496, #39937）
  - 🔀 **MoE 大重构**：Full Oracle Flow 迁移、SharedExperts class、MoERunnerBase 统一（#36286, #35153, #40560 等）
  - 📈 **性能**：fused rms norm batch invariant 优化 → E2E 延迟降低 2.1%（#40413）；避免 seq_lens_cpu GPU→CPU sync（#40654）
  - 🆕 **新模型**：DeepSeek V4、Hunyuan v3、Granite 4.1 Vision、EXAONE-4.5、Phi-4-reasoning-vision、Nemotron-v3 VL 等 12+ 新架构
- **24h 内最新 commits**：
  - Fix Cohere ASR after HF upgrade（#40582）
  - Add `VLLM_SKIP_MODEL_NAME_VALIDATION` 环境变量（#34676）

### TensorRT-LLM v1.3.0rc13

- **链接**：[Release v1.3.0rc13](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc13)
- **发布日期**：2026-04-29
- **核心更新**：
  - 🎯 **Nemotron 3 Nano Omni**：初始支持 + 优化；ViT attention 优化、音频提取、初始化内存降低（#12921, #12911, #13283）
  - 🤖 **GLM-4.7 / GLM-5 tool parser**：新增工具解析器（#13150）
  - 📊 **DeepSeek-V3.2 / V3-Lite**：Blackwell + SM100-class GPU 上的性能和 chunked-prefill 修复（#13142, #13257）
  - 🖼️ **VisualGen Cache-DiT + 统一缓存加速器**（#12548）
  - 🔍 **稀疏 MQA/GQA 注意力** + 新分片基础设施（#12470, #12419）
  - 🦅 **EAGLE3 投机解码恢复** + perfect-router 集成（#13081, #13250）
  - 🧮 **内核扩展**：RMSNorm 更广覆盖、causal-conv1d prefill/decode 优化、FP4 残差量化、SageAttention 刷新（#13033, #13103, #13117, #12937）
  - ⚡ **服务性能优化**：异步媒体加载、视频帧解码加速、文本计算缓存复用、CUDA graph padding-aware 调优（#13034, #12677, #12895, #13412）
  - 🔧 **大量修复**：KV cache/scheduler 正确性、FMHA SM90 dispatch、vision encoder KV cache 量化泄漏、Qwen3 mrope cache 处理（#12968, #13120, #13181, #13269）

### llama.cpp b8981

- **链接**：[Release b8981](https://github.com/ggml-org/llama.cpp/releases/tag/b8981)
- **发布日期**：2026-04-29
- **核心更新**：
  - 🔧 **reasoning budget sampler 修复**：不再将 prompt tokens 传递给 reasoning budget sampler（#22488）
  - ⚡ **fast matmul iquants**：新增 iquants 快速矩阵乘法内核（#22504），预计显著提升整数量化推理速度
  - 🛠️ **开发工具**：新增 `wc2wt.sh` 脚本从当前 HEAD 创建 worktree（#22513）
  - 📦 **CUDA 13.1 构建**：Windows CUDA 13 构建支持

### SGLang（主线 commits）

- **链接**：[sgl-project/sglang](https://github.com/sgl-project/sglang)
- **24h 内关键 commits**：
  - 🐛 **Qwen3.5 FP8 修复**：per-tensor scale 在 `_make_packed_weight_loader` 中广播问题（#23062）
  - 🔒 **XPU deterministic 模式**：Intel Habana GPU 可复现推理（#16793）
  - 🖼️ **moss-vl 修复**：使用 Conv3dLayer 替换并移除 no-op flat_encoder_result（#23932）

---

## 工程启发

1. **CUDA 13 生态全面铺开**：vLLM 默认 CUDA 13.0、llama.cpp 提供 CUDA 13.1 构建、PyTorch 2.11 同步跟进 —— 升级 CUDA 版本已从"可选"变为"必须"，建议尽早验证 CUDA 13 兼容性
2. **2-bit KV cache 压缩进入实战**：vLLM TurboQuant 提供 2-bit KV cache（4× 容量），TensorRT-LLM 的 FP4 残差量化 —— 极低比特 KV 压缩正从论文走向生产，长上下文场景的吞吐收益值得评估
3. **FA4 作为 MLA prefill 默认后端**：vLLM 将 FlashAttention 4 设为默认 MLA prefill，head-dim 512 + paged-KV —— 对 DeepSeek 系列 MLA 架构是关键性能提升，实际 benchmark 需要关注 SM90+ 的覆盖率
4. **稀疏注意力 + 投机解码**：TensorRT-LLM 稀疏 MQA/GQA + EAGLE3 恢复 —— 投机解码 + 稀疏注意力的组合是延迟优化的重要方向
5. **在线量化统一前端**：vLLM 将 FP8/MXFP8/experts_int8 统一到单一入口 —— 量化部署工作流大幅简化，对 MoE 模型推理有直接收益
6. **llama.cpp iquants 加速**：fast matmul for iquants 对 CPU/边缘端整数量化模型有直接性能提升，值得跟踪 PR #22504 的 benchmark 数据

---

## 明日跟踪建议

1. **vLLM v0.20.0 后续**：关注 DeepSeek V4 完整支持进度、TurboQuant 2-bit KV cache benchmark 数据、vLLM IR 内核开发走向
2. **TensorRT-LLM v1.3.0 正式版**：当前为 rc13，跟踪 Nemotron 3 Nano Omni 已知问题（audio-from-video / chunked prefill）修复进度
3. **llama.cpp iquants**：跟踪 #22504 PR 的性能数据，对比不同量化类型的 matmul 加速比
4. **SGLang Qwen3.5 支持**：Qwen3.5 是新模型，FP8 weight loading 修复暗示该模型正在积极适配中，关注后续更新
5. **CUDA 13 兼容性**：跟踪各框架在 CUDA 13 上的稳定性报告，特别是 vLLM 对 CUDA 12.9 的回退方案
