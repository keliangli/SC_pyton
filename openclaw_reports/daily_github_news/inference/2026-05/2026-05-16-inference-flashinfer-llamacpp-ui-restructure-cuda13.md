# GitHub 大模型推理日报（2026-05-16）- FlashInfer密集迭代与llama.cpp UI重构

## 今日要点

1. **llama.cpp b9174 发布**：完成 WebUI → UI 大规模重构，CLI 参数、CMake 变量、CI 流程全部重命名，保持向后兼容
2. **FlashInfer v0.6.11.post3 发布**（5月15日）：v0.6.11 系列第三个补丁，密集迭代持续中；同日发布 nightly-20260516
3. **TGI（text-generation-inference）已归档**：HuggingFace 于 3 月 21 日将 TGI 仓库归档为只读，v3.3.2 为最终版本
4. **SGLang v0.5.11 升级 CUDA 13 + Torch 2.11**：Spec V2 默认启用，新增 Decode Radix Cache 支持 PD 分离部署
5. **TensorRT-LLM v1.3.0rc14**：Qwen3.5/Nemotron 前缀缓存、VisualGen 多节点扩散、大量 kernel 性能优化

## 项目速递

### llama.cpp
- **版本**：b9174（2026-05-16，Latest）
- **更新**：WebUI 全面重构为 UI 模块
  - 代码迁移：`tools/server/webui/` → `tools/ui/`
  - CLI 参数：`--webui` → `--ui`（旧参数保留为 deprecated alias）
  - CMake 变量：`LLAMA_BUILD_WEBUI` → `LLAMA_BUILD_UI`（旧变量自动转发 + DEPRECATION 警告）
  - CI/CD：webui-build.yml → ui-build.yml，artifact 重命名
  - 新增环境变量：`LLAMA_ARG_UI`、`LLAMA_ARG_UI_CONFIG`、`LLAMA_ARG_UI_MCP_PROXY`
  - JSON API 同时输出 `ui`/`ui_settings` 和 `webui`/`webui_settings` 键
- **链接**：https://github.com/ggml-org/llama.cpp/releases/tag/b9174

### FlashInfer
- **版本**：v0.6.11.post3（2026-05-15，Latest Stable）；nightly-v0.6.11-20260516（2026-05-16）
- **更新**：v0.6.11 系列密集补丁迭代（post1/post2/post3 相继发布于 5/13、5/14、5/15）
- **链接**：https://github.com/flashinfer-ai/flashinfer/releases/tag/v0.6.11.post3

### SGLang
- **版本**：v0.5.11（2026-05-05）
- **更新**：
  - CUDA 13 + PyTorch 2.11 全面升级（默认 CUDA 版本从 12 升至 13）
  - Speculative Decoding V2 默认启用（overlap scheduling 隐藏 CPU 开销）
  - Decode Radix Cache 支持 Prefill/Decode 分离部署
  - 新模型 Day-0 支持：Gemma 4、GLM-5.1、Qwen3.6、MiMo-V2.5/V2.5-Pro、Ling-2.6-Flash、Mistral Medium 3.5、Kimi-K2.6
- **链接**：https://github.com/sgl-project/sglang/releases/tag/v0.5.11

### TensorRT-LLM
- **版本**：v1.3.0rc14（2026-05-07，Pre-release）
- **更新**：
  - Mamba 混合模型前缀缓存（Qwen3.5、Nemotron Super V3）
  - Qwen3.5 自定义 MoE routing + NVFP4 权重加载修复
  - VisualGen 多节点 diffusion workers + 2D 序列并行
  - Disaggregated serving：gen-first ADP、KV-aware hit-rate gates
  - Kernel 优化：GEMM-to-allreduce registered buffers、CuteDSL bf16、fused add-norm-FP8、TF32 DSA GEMMs
  - Speculative decoding：DFlash one-model、Mamba-2 rollback replay
  - NVFP4 权重热更新支持
- **链接**：https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc14

### TGI (Text Generation Inference)
- **状态**：已归档（2026-03-21）
- **最终版本**：v3.3.2
- **最后更新**：Qwen3 支持、fp8 w8a8 compressed_tensors、Gaudi Llama-4 Scout/Maverick 修复
- **链接**：https://github.com/huggingface/text-generation-inference/releases/tag/v3.3.2

### Unsloth
- **版本**：v0.1.39-beta（2026-05-05）
- **更新**：新增本地 API Inference Endpoint
  - 自修复 Tool Calling（减少 50% 畸形调用）
  - 代码执行（Bash/Python）
  - 高级 Web Search（实际访问网页读取内容）
  - 同时支持 Anthropic /v1/messages 和 OpenAI /v1/chat/completions
  - 新模型：Nemotron 3 Nano Omni、Granite 4.1、Mistral 3.5
- **链接**：https://github.com/unslothai/unsloth/releases/tag/v0.1.39-beta

### vLLM
- **版本**：v0.9.1（近期发布）
- **更新**：274 commits、123 contributors
  - DP Attention + Expert Parallelism CUDA graph 支持
  - DeepEP dispatch-combine kernel、batched/masked DeepGEMM kernel
  - CUTLASS MoE kernel（与 PPLX 合作）
  - 异构 TP、NixlConnector FlashInfer 后端
  - Data Parallel：API-server scaleout、Ray 集成、指定 DP rank
- **链接**：https://github.com/vllm-project/vllm/releases/tag/v0.9.1

## 工程启发

1. **CUDA 13 迁移潮**：SGLang 已将默认 CUDA 版本升级至 13.0 + PyTorch 2.11，后续 vLLM/TensorRT-LLM 等预计跟进，建议提前验证现有 CUDA 12 kernel 的兼容性
2. **PD 分离部署持续演进**：SGLang 新增 Decode 侧 Radix Cache，TensorRT-LLM 推出 gen-first ADP + KV-aware 路由，PD 分离场景的 KV 复用率正在从"基本可用"走向"高命中率"
3. **FlashInfer 迭代节奏**：v0.6.11 三天三个 post 补丁，说明 attention kernel 层仍有活跃 bug 修复，生产环境建议跟踪 nightly 一周后再升级 stable
4. **TGI 归档的信号**：HuggingFace 归档 TGI 意味着官方推理服务方向转向 vLLM 或内部方案，TGI 用户需规划迁移
5. **Speculative Decoding 成为主流**：SGLang Spec V2 默认启用、TensorRT-LLM 新增 DFlash/Mamba-2 rollback，投机解码从实验性功能变为生产标配

## 明日跟踪建议

- [ ] 关注 FlashInfer v0.6.11.post3 的具体 changelog（当前 release note 仅显示 compare link）
- [ ] llama.cpp UI 重构后 server 端行为的回归测试情况
- [ ] SGLang CUDA 13 + Torch 2.11 的 Docker 镜像可用性及 sgl-kernel 兼容性
- [ ] TensorRT-LLM v1.3.0 正式版发布时间（当前 rc14）
- [ ] vLLM DP Attention + EP 的性能基准测试数据
