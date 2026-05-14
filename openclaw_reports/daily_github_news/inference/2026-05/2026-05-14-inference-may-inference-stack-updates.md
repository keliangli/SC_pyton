# GitHub 大模型推理日报（2026-05-14）

## 今日要点

1. **FlashInfer v0.6.11.post2 今日发布** — 推理注意力内核库发布 bugfix 版本，修复 v0.6.11.post1 引入的问题，发布 CUBIN 和 JIT Cache 预编译包
2. **llama.cpp b9144 今日发布** — 边缘/本地推理引擎例行构建更新，新增 CUDA 13.1 预编译二进制，适配 openEuler aarch64 平台
3. **vLLM 主干活跃开发** — 回退了 routing replay 替换方案（#39917 → #42434），device cache + async D2H pipeline 方案暂停，routing 逻辑暂回稳定版
4. **SGLang v0.5.11 大版本（5月5日）** — CUDA 13 + Torch 2.11 全面升级、Spec V2 默认开启、PD 分离解码端 radix cache、DFLASH 投机解码、FA3 内核、DeepSeek-V3/Kimi-K2 LoRA 支持
5. **Triton v3.7.0（5月7日）** — 新增 tl.squeeze/unsqueeze、scaled BMM、FP8 常量、Plugin Hooks & Out-of-Tree 方言、JIT 开销优化

## 项目速递

### FlashInfer v0.6.11.post2（5月14日）
- **类型**：Bugfix Release
- **关键变更**：修复 v0.6.11.post1 引入的回归问题；发布 CUBIN wheel（361MB）和 JIT Cache 预编译包（cu128 aarch64 + x86）
- **链接**：https://github.com/flashinfer-ai/flashinfer/releases/tag/v0.6.11.post2

### llama.cpp b9144（5月14日）
- **类型**：Daily Build
- **关键变更**：新增 CUDA 13.1 Windows x64 预编译包；openEuler aarch64 构建支持；仓库已迁移至 ggml-org 组织
- **链接**：https://github.com/ggml-org/llama.cpp/releases/tag/b9144

### vLLM v0.20.2（5月10日）+ 主干动态
- **类型**：Stable Release + Active Development
- **关键变更**：
  - v0.20.2 为当前最新稳定版（5月10日发布）
  - 5月14日回退 PR #39917（device cache + async D2H pipeline 替换 routing replay），说明该优化路径暂不稳定
- **链接**：
  - https://github.com/vllm-project/vllm/releases/tag/v0.20.2
  - https://github.com/vllm-project/vllm/commit/8c79ad65804d

### SGLang v0.5.11（5月5日）
- **类型**：Major Release
- **关键变更**：
  - CUDA 13 + PyTorch 2.11 全面升级，更新构建矩阵
  - Speculative Decoding V2 默认启用（overlap scheduling 降低 CPU 开销）
  - PD 分离架构支持 decode 端 radix cache，长前缀场景 TTFT 优化
  - DFLASH 投机解码内核，扩展至 AMD ROCm
  - FA3 社区内核集成（与 FA4 并列的高性能选项）
  - DeepSeek-V3 MLA LoRA + Kimi-K2 LoRA（前沿 MoE 模型适配器微调）
  - Context Parallel：all-reduce + RMSNorm 融合 + MoE/Attention 独立并行度调节
  - FlashInfer CuteDSL MoE Runner（FP4 MoE 路径高性能融合）
  - 新模型：Gemma 4、GLM-5.1、Qwen3.6、MiMo-V2.5、Ling-2.6-Flash、Mistral Medium 3.5、Kimi-K2.6
- **链接**：https://github.com/sgl-project/sglang/releases/tag/v0.5.11

### Triton v3.7.0（5月7日）
- **类型**：Major Release
- **关键变更**：
  - 前端新增 `tl.squeeze`/`tl.unsqueeze`、scaled BMM、FP8 常量直接创建
  - Plugin Hooks & Out-of-Tree 方言支持（#8401, #8523）
  - JIT 开销优化：预计算 inspect.signature、惰性 tuple 类型名、移除 catch_warnings
  - `tl.cat(can_reorder=False)` 非重排序变体 + 广播支持
  - `make_block_ptr` 废弃警告
  - AMD/HIP 后端改进、Proton profiling 更新
- **链接**：https://github.com/triton-lang/triton/releases/tag/v3.7.0

### DeepSpeed v0.19.0（5月6日）
- **类型**：Stable Release
- **关键变更**：
  - Zero3 碎片整理工具（defragment utility）
  - SP deny list 替代 allow list
  - FPQuantizer 构建修复
  - Process-group shutdown 挂起修复
  - Zero3 flat buffer detach 修复（防止 autograd inplace 错误）
- **链接**：https://github.com/deepspeedai/DeepSpeed/releases/tag/v0.19.0

## 工程启发

1. **CUDA 13 迁移潮**：SGLang v0.5.11 和 llama.cpp 同时适配 CUDA 13，说明 CUDA 13 已进入生产可用阶段；推理框架升级时应同步考虑 CUDA 版本切换
2. **投机解码走向默认化**：SGLang Spec V2 默认开启、vLLM 也在推进 routing 优化，投机解码不再是实验性功能，而是标准吞吐/延迟优化手段
3. **PD 分离架构的 cache 一致性**：SGLang decode 端 radix cache 支持说明 PD 分离后缓存命中率问题已被社区重视并解决，部署长前缀场景可直接受益
4. **Triton 生态开放性**：Plugin Hooks 和 Out-of-Tree 方言支持意味着自定义 kernel 开发者可以更灵活地扩展 Triton，不必等待上游合并
5. **vLLM routing 优化回退**：device cache + async D2H pipeline 方案被回退，说明 GPU 端路由优化需谨慎验证稳定性，生产环境应锁定 v0.20.2 稳定版

## 明日跟踪建议

1. 关注 vLLM routing replay 替换方案的后续修复进展，以及 v0.20.3 是否发布
2. 跟踪 FlashInfer v0.6.11.post2 在 vLLM/SGLang 中的集成状态
3. 观察 SGLang DFLASH 投机解码在更多模型上的 benchmark 数据
4. 关注 Triton v3.7.0 在 CUDA 13 下的编译兼容性
5. 检查 DeepSpeed Zero3 defragment utility 对大模型训练性能的实际影响
