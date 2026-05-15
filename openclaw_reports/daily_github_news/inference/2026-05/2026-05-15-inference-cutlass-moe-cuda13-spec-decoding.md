# GitHub 大模型推理日报（2026-05-15）

> 抓取时间：2026-05-15 14:50 CST | 覆盖项目：vllm、SGLang、llama.cpp、CUTLASS、Flash Attention、Triton、TensorRT-LLM、TGI

---

## 今日要点

1. **llama.cpp 发布 b9159 新版本**（今日发布），新增 CUDA 13.1 构建产物
2. **NVIDIA CUTLASS 4.5.0 正式发布**（5月13日），CuTe DSL 新增 block_copy() 简化 TMA/S2T、MXF8F6F4 混合精度、MoE 示例性能显著超越 PyTorch（mxfp8 avg 1.29-1.41x speedup）
3. **Flash Attention 4 beta13 发布**（5月13日，pre-release），FA4 持续迭代
4. **SGLang v0.5.11**（5月5日），CUDA 13 + Torch 2.11 默认升级、Spec V2 默认开启、Decode Radix Cache 支持 PD 分离部署、新增 Ring-2.6-1T cookbook
5. **Triton 3.7.0 正式发布**（5月7日），新增 tl.squeeze/unsqueeze、scaled BMM、FP8 常量、Gluon layout 改进
6. **TensorRT-LLM v1.3.0rc14**（5月7日，pre-release），Mamba 混合模型 prefix caching、Qwen3.5 MoE 路由优化、VisualGen serving 改进、NVFP4 权重更新支持

---

## 项目速递

### 1. llama.cpp — b9159
- **类型**：Release（今日发布）
- **发布时间**：2026-05-15
- **要点**：日常迭代版本，新增 CUDA 13.1 x64 Windows 构建产物，同时保留 CUDA 12.4 构建
- **今日活跃 commit**：readme: update bindings (#23063)
- **链接**：https://github.com/ggml-org/llama.cpp/releases/tag/b9159

### 2. NVIDIA CUTLASS — v4.5.0
- **类型**：Release（5月13日发布）
- **要点**：
  - **CuTe DSL**：新增 `block_copy()` API 简化 TMA 和 S2T copy，用户无需手动调用 `tma_partition()`
  - **MXF8F6F4 混合精度**：BlockScaled MMA 支持 MXF8×MXF4 或 MXF8×MXF6
  - **SM120 支持**：Block Scaled MMA for SM120 现可在 Spark 上运行
  - **EFC broadcast**：epilogue 支持广播与 remap（`C.remap_modes[:, 0, 1]` 语法）
  - **MoE 示例性能**：对比 torch_210_cu13，B200 上：
    - mxfp8_2dx3d: avg **1.29x** speedup
    - mxfp8_2dx2d: avg **1.41x** speedup
    - nvfp4_2dx3d: avg **1.11x** speedup
    - bf16_2dx3d: avg **1.15x** speedup
  - 新增 linter 支持（MyPy type hints）、dataclass JIT 编译、user-specified loop unrolling
- **链接**：https://github.com/NVIDIA/cutlass/releases/tag/v4.5.0

### 3. Flash Attention — fa4-v4.0.0.beta13
- **类型**：Pre-release（5月13日发布）
- **要点**：Flash Attention 4 持续迭代至 beta13，发布 wheel 包（flash_attn_4-4.0.0b13）
- **链接**：https://github.com/Dao-AILab/flash-attention/releases/tag/fa4-v4.0.0.beta13

### 4. Triton — v3.7.0
- **类型**：Release（5月7日发布）
- **要点**：
  - **前端**：`tl.squeeze` / `tl.unsqueeze`；Scaled BMM 支持；FP8 常量创建；JIT 函数可返回 constexpr
  - **后端**：Gluon & Layout 改进
  - **NVIDIA 后端**：持续优化
  - **AMD/HIP 后端**：改进
  - **Proton Profiling**：增强
- **链接**：https://github.com/triton-lang/triton/releases/tag/v3.7.0

### 5. vllm — v0.20.2
- **类型**：Release（5月10日发布）+ 今日活跃 commit
- **要点**：
  - DeepSeek V4 sparse attention: 重新启用 Hopper persistent topk 路径，修复 MTP=1 hang
  - DeepSeek V4 KV cache: 修复 "failure to allocate KV blocks" 错误
  - gpt-oss MXFP4 + torch.compile: 修复 hidden_dim_unpadded 在 moe_forward fake op 中的传递
  - Qwen3-VL: 移除无效 deepstack 边界检查
  - **今日 commit**：[Bugfix] Clarify CPU backend memory error messages reference shared flag (#42479)
- **链接**：https://github.com/vllm-project/vllm/releases/tag/v0.20.2

### 6. SGLang — v0.5.11
- **类型**：Release（5月5日发布）+ 今日活跃 commit
- **要点**：
  - **CUDA 13 + Torch 2.11**：默认 CUDA 版本升级至 13.0，PyTorch 从 2.9 升级到 2.11
  - **Speculative Decoding V2 默认开启**：overlap scheduling 隐藏 CPU 开销，EAGLE/MTP/DFLASH 路径 per-step CPU 成本显著降低
  - **Decode Radix Cache for PD Disaggregation**：decode 侧 prefix caching 在 PD 分离部署下工作，恢复 radix-cache 命中率和 TTFT 优化
  - **新模型支持**：Gemma 4、GLM-5.1、Qwen3.6、MiMo-V2.5/V2.5-Pro、Ling-2.6-Flash、Mistral Medium 3.5、Kimi-K2.6
  - **DFLASH Speculative Decoding**：新的高吞吐投机解码方案
  - **今日 commit**：[NEW MODEL] Add Ring-2.6-1T cookbook (#25360)
- **链接**：https://github.com/sgl-project/sglang/releases/tag/v0.5.11

### 7. TensorRT-LLM — v1.3.0rc14
- **类型**：Pre-release（5月7日发布）
- **要点**：
  - Mamba 混合模型（Qwen3.5、Nemotron Super V3）prefix caching
  - Qwen3.5 custom MoE routing 优化 + NVFP4 weight loading 修复
  - VisualGen serving 改进：fast PNG compression、multi-node diffusion workers、Attention2D sequence parallelism
  - Disaggregated serving：gen-first ADP serving、KV-aware hit-rate gates、fair-share caps
  - 内核性能扩展：GEMM-to-allreduce registered buffers、CuteDSL bf16 dense GEMMs、fused add-norm-FP8 quantization、TF32 DSA GEMMs
  - DFlash speculative decoding one-model 支持
  - NVFP4 权重更新支持
  - KV cache / scheduler 多项正确性修复
- **链接**：https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc14

---

## 工程启发

1. **CUTLASS MoE 示例是学习 MoE 推理优化的最佳入口**：CUTLASS 4.5.0 提供了 expert-wise tensormap descriptor + helper kernel（~2μs）避免 tile 切换延迟，mxfp8 相比 PyTorch 实现平均 1.29-1.41x 加速，值得深入研读其 kernel 结构
2. **CUDA 13 迁移正在加速**：SGLang 和 llama.cpp 已同步支持 CUDA 13.x，vllm 尚在 CUDA 12.4/13.1 构建产物并行阶段；建议评估自身环境 CUDA 13 兼容性
3. **Speculative Decoding 进入 V2 时代**：SGLang Spec V2 默认开启、TensorRT-LLM DFlash one-model 支持，说明投机解码已从实验性转向生产级，关注 overlap scheduling 对 CPU 开销的隐藏效果
4. **Flash Attention 4 持续迭代但仍是 beta**：fa4-v4.0.0.beta13 仍未标记 stable，生产环境建议继续使用 FA3；但可关注其 API 变化做兼容准备
5. **PD 分离部署的 Radix Cache 问题被攻克**：SGLang 和 TensorRT-LLM 都在解决 prefill/decode 分离下 prefix caching 的命中率问题，这是长上下文场景的关键优化

---

## 明日跟踪建议

1. **CUTLASS MoE 示例源码**：阅读 `examples/moe/` 目录，理解 grouped-gemm 新接口和 expert-wise tensormap descriptor 实现
2. **SGLang Spec V2 性能数据**：关注 EAGLE/MTP/DFLASH 在真实工作负载下的 TTFT/TPS 数据
3. **Flash Attention 4 → stable 进度**：关注 beta14 或 rc1 发布时间
4. **vllm 下一个大版本（v0.21?）**：当前 v0.20.2 仅为 bugfix 版本，关注 feature 分支合并动态
5. **TensorRT-LLM v1.3.0 正式版**：rc14 已积累大量改进，关注正式版发布时间
