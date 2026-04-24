# GitHub 大模型推理日报（2026-04-24）

## 📌 今日要点

1. **llama.cpp b8913 紧急修复**：修复 RMS fuse 中的 buffer aliasing 问题，影响 shader 性能稳定性
2. **vLLM v0.19.1 发布**：Gemma4 支持全面升级，包括 Eagle3 支持、量化 MoE、流式工具调用修复等
3. **SGLang 多平台扩展**：DeepSeek V4 cookbook 上线，Intel XPU Pipeline 并行支持，MUSA 后端新增 DeepSeek 模型支持
4. **AMD 原生推理栈新项目**：AMD-NFS 项目启动，目标绕过 CUDA 锁定，原生支持 ROCm
5. **推理框架多硬件适配加速**：Apple Silicon MLX 缓存优化、华为昇腾支持持续推进

---

## 🚀 项目速递

### 1. llama.cpp - Release b8913
**链接**: https://github.com/ggml-org/llama.cpp/releases/tag/b8913

**关键更新**:
- 修复 shader 中 RMS fuse 的 buffer aliasing 问题（影响推理稳定性）
- 多平台二进制发布：新增 openEuler 310p/910b ACL Graph 支持
- ROCm 7.2、SYCL FP16/FP32、Vulkan 后端持续维护

**工程价值**: 边缘部署稳定性提升，国产昇腾芯片支持完善

---

### 2. vLLM - v0.19.1 Release
**链接**: https://github.com/vllm-project/vllm/releases/tag/v0.19.1

**关键更新**:
- **Transformers v5.5.3 升级**（#30566）
- **Gemma4 支持增强**:
  - 新增 Eagle3 支持（#39450）
  - 量化 MoE 支持（#39045）
  - 流式工具调用 JSON 修复（#38992, #38909, #39114）
  - LoRA 适配器正确加载修复（#38844）
  - 动态 BOS 注入修复 token 重复问题（#39842）
- **Kimi K2.5** media_placeholder_token_id 解析修复（#39344）

**工程价值**: Gemma4 生产就绪，工具调用场景稳定性显著提升

---

### 3. SGLang - 近期 Commit 汇总
**链接**: https://github.com/sgl-project/sglang

**关键更新**:
- **DeepSeek V4**: 新增 cookbook 和文档更新（#23605, #23617）
- **Intel XPU**: Pipeline 并行支持（#23472）
- **MUSA 后端**: DeepSeek V2/V3/R1 模型支持（#22774）
- **扩散模型**: LTX2.3 高质量 pipeline 支持（#23366）
- **多模态**: Moss-VL 模型支持（#23454）
- **Apple Silicon**: MLX BatchedDecodeContext 缓存优化（#23470）

**工程价值**: 异构硬件覆盖度扩大，从云端到边缘全栈支持

---

### 4. AMD-NFS - AMD Native Inference Stack（新项目）
**链接**: https://github.com/theonlychant/AMD-NFS

**项目定位**: 
- 绕过 CUDA 锁定，原生针对 ROCm 优化
- 替代 vLLM、llama.cpp、Triton 的 AMD 专用推理栈
- 目标：统一的 AMD 优化推理架构

**工程价值**: AMD GPU 推理生态的重要补充，值得关注进展

---

### 5. vLLM 近期 Commit 亮点
**链接**: https://github.com/vllm-project/vllm

**关键更新**:
- **MoE 优化**: Cutlass MoE 迁移至 fused_moe/experts/（#40574）
- **API 弃用**: LLM.reward 离线 API 弃用，改用 LLM.encode（#40688）
- **XPU 修复**: Intel CI runner Docker 清理竞争条件修复（#40761）
- **RISC-V**: 平台检测修复（lscpu 解析 + 非 NUMA meminfo）（#40427）
- **Mistral**: 延迟导入 mistral_common 包（#40043）

**工程价值**: 推理性能持续优化，多硬件平台稳定性提升

---

## 💡 工程启发

1. **Gemma4 生态成熟**: vLLM 的 Gemma4 支持已进入精细化打磨阶段，工具调用、量化、LoRA 全链路就绪，可考虑在生产环境试点

2. **多硬件博弈加剧**: AMD-NFS 新项目出现、SGLang 扩展 MUSA/Intel/Apple 支持，推理框架进入"去 CUDA 化"多元竞争阶段

3. **边缘推理优化持续**: llama.cpp 的 shader aliasing 修复、SGLang 的 MLX 缓存优化，表明边缘场景性能打磨仍是重点

4. **MoE 架构成为焦点**: vLLM 的 Cutlass MoE 重构、Gemma4 量化 MoE 支持，反映 MoE 模型推理优化需求上升

---

## 📋 明日跟踪建议

1. **监控 AMD-NFS 项目进展** - 是否有实质性代码提交和基准测试结果
2. **关注 SGLang DeepSeek V4 性能数据** - cookbook 中的优化策略是否可迁移
3. **验证 vLLM v0.19.1 Gemma4 工具调用** - 流式场景稳定性是否彻底解决
4. **跟踪 llama.cpp 昇腾 ACL Graph 支持** - 国产芯片推理性能数据

---

*报告生成时间: 2026-04-24*
*数据来源: GitHub API*
