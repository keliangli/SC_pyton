# GitHub 大模型推理日报（2026-05-05）

> 数据来源：GitHub Trending / Releases / Topics · 覆盖时间 2026-05-04 ~ 2026-05-05

---

## 今日要点

1. **vLLM v0.20.1 发布（May 4）**：DeepSeek V4 稳定性补丁，含多流 pre-attention GEMM、PTX 加速 FP32→FP4 转换、tile kernel 优化 head 计算，修复 persistent topk 死锁和 BailingMoE 兼容问题。
2. **llama.cpp b9028 发布（May 5）**：新增设备缓冲区内存节省选项，CUDA 13.1 Windows 构建支持，OpenVINO 2026.0 集成。
3. **vLLM v0.20.0 大版本回顾（Apr 27）**：752 commits / 320 贡献者，含 DeepSeek V4 初始支持、CUDA 13.0 默认切换、PyTorch 2.11、FlashAttention 4 默认 MLA prefill、TurboQuant 2-bit KV cache（4× 容量）、在线量化前端、vLLM IR 初始骨架。
4. **SGLang v0.5.10（Apr 6）**：Piecewise CUDA Graph 默认启用、Elastic EP 部分容错、GPU Staging Buffer 使 PD 分离大并发 TPS 提升 ~5×、HiSparse 稀疏注意力、FlashInfer MXFP8 kernel、Transformers 5.3.0 升级、DeepSeek V3.2 / GLM-5 / Qwen3.5 专项优化。
5. **TensorRT-LLM v1.3.0rc13（Apr 29）**：Nemotron 3 Nano Omni 初始优化、GLM-4.7/GLM-5 tool parser、DeepSeek-V3.2/Lite 在 Blackwell/SM100 上的 chunked-prefill 修复、Async RL abort/resume。

---

## 项目速递

### 1. vLLM — v0.20.1 / v0.20.0

| 项目 | 版本 | 日期 | 类型 |
|------|------|------|------|
| [vllm-project/vllm](https://github.com/vllm-project/vllm) | v0.20.1 | 2026-05-04 | Patch Release |
| [vllm-project/vllm](https://github.com/vllm-project/vllm) | v0.20.0 | 2026-04-27 | Major Release |

**v0.20.1 关键变更：**
- DeepSeek V4：多流 pre-attention GEMM（#41061）、可配置 pre-attn GEMM knob（#41443）、BF16/MXFP8 all-to-all FlashInfer 单边通信（#40960）
- PTX cvt 指令加速 FP32→FP4 转换（#41015）
- 集成 tile kernel（head_compute_mix_kernel）优化 head 计算（#41255）
- 修复 persistent topk cooperative 死锁（#41189, #41442）、inter-CTA init race（#41444）
- 修复 BailingMoE linear layer（#40859）和 MLA RoPE rotation（#41185）
- 修复 CUDA graph 中 max_num_batched_token 未捕获（#40734）

**v0.20.0 关键变更：**
- DeepSeek V4 初始支持（#40860）
- CUDA 13.0 默认切换（#39878）、PyTorch 2.11 升级（#34644）
- Transformers v5 兼容（#30566）、Python 3.14 支持（#34770）
- FlashAttention 4 默认 MLA prefill（#38819）
- **TurboQuant 2-bit KV cache**：4× 容量提升（#38479, #40092）
- 在线量化前端（#38138）、MXFP8 在线量化迁移（#40152）
- vLLM IR 初始骨架（#33825）
- 新模型：Hunyuan v3（#40681）、Granite 4.1 Vision（#40282）

### 2. llama.cpp (ggml-org) — b9028

| 项目 | 版本 | 日期 | 类型 |
|------|------|------|------|
| [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | b9028 | 2026-05-05 | Release |

- 新增设备缓冲区内存节省选项（#22679）
- CUDA 13.1 Windows 构建支持
- OpenVINO 2026.0 集成
- ROCm 7.2 Ubuntu 构建
- 多平台二进制持续更新（macOS/iOS/Linux/Android/Windows/openEuler）

### 3. SGLang — v0.5.10 / v0.5.10.post1

| 项目 | 版本 | 日期 | 类型 |
|------|------|------|------|
| [sgl-project/sglang](https://github.com/sgl-project/sglang) | v0.5.10.post1 | 2026-04-09 | Patch |
| [sgl-project/sglang](https://github.com/sgl-project/sglang) | v0.5.10 | 2026-04-06 | Feature Release |

**v0.5.10 关键变更：**
- Piecewise CUDA Graph 默认启用，减少内存开销（#16331）
- **Elastic EP 部分容错**：DeepSeek MoE 部署中 GPU 故障自动重分布，无需全量重启（#19248, blog）
- **GPU Staging Buffer for PD 分离**：GQA 模型 RDMA 请求量减少 ~1000×，Qwen3.5 大并发 TPS/GPU 提升 ~5×（#19890）
- HiSparse 稀疏注意力集成（#20343）
- FlashInfer MXFP8 kernel 支持 GEMM/MoE（#19537）
- Transformers 5.3.0 升级，GLM-5 主线支持（#17784）
- DeepSeek V3.2 / GLM-5：fused Triton kernel prefill KV fetch、NSA fuse store indexer、TRT-LLM DSA kernel（SM100/SM103 默认）、IndexCache 高负载吞吐 +10%（#19319 等）
- SGLang-Diffusion：LTX-2 / Hunyuan3D-2 / Helios 支持，macOS 平台，Cache-DiT 集成

### 4. TensorRT-LLM — v1.3.0rc13

| 项目 | 版本 | 日期 | 类型 |
|------|------|------|------|
| [NVIDIA/TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) | v1.3.0rc13 | 2026-04-29 | Pre-release |

- Nemotron 3 Nano Omni 初始优化：音频提取、ViT attention 优化、初始化内存缩减
- GLM-4.7 / GLM-5 tool parser（#13150）
- DeepSeek-V3.2 / V3-Lite：Blackwell/SM100 专项性能和 chunked-prefill 修复
- Async RL abort/resume 支持
- VisualGen 逐模型示例脚本和配置

### 5. 其他值得关注

| 项目 | 版本 | 日期 | 说明 |
|------|------|------|------|
| [HuggingFace TGI](https://github.com/huggingface/text-generation-inference) | v3.3.7 | 2025-12-19 | ⚠️ 项目已于 2026-03-21 归档（read-only） |
| [LightLLM](https://github.com/ModelTC/LightLLM) | v1.1.0 | 2025-09-03 | CPU-GPU 统一 Folding、DeepEP/DeepGEMM 集成、Triton autotuner |
| [DeepSpeed](https://github.com/deepspeedai/DeepSpeed) | v0.18.9 | 2026-03-30 | Universal Checkpoint for AutoTP、HF tp_plan 支持 |
| [Vortex (Infini-AI-Lab)](https://github.com/Infini-AI-Lab/vortex_torch) | v0.3 | — | 灵活高效的稀疏注意力框架 |

---

## 工程启发

1. **MoE 部署进入"容错时代"**：SGLang 的 Elastic EP 和 vLLM 的 persistent topk 死锁修复，说明 MoE 大规模部署的核心矛盾已从"能不能跑"转向"怎样稳定跑"。部分容错能力将是生产级 MoE 服务的基本要求。
2. **FP4/MXFP8 量化加速落地**：vLLM 的 PTX cvt FP4 转换、SGLang 的 FlashInfer MXFP8 kernel、vLLM 的在线量化前端，三条路径同时推进，低精度推理生态正在快速成熟。关注 MXFP8 在 RL 场景的实际精度表现。
3. **KV cache 压缩从理论到工程**：vLLM TurboQuant 2-bit KV cache 实现 4× 容量提升，且已与 FA3/FA4 prefill 对接，标志着 KV cache 压缩从论文走向生产。对长上下文场景（128K+）的直接利好。
4. **PD 分离架构持续深化**：SGLang 的 GPU Staging Buffer 将 RDMA 请求量降低 ~1000×，vLLM 的 FlashAttention 4 默认 MLA prefill 也在优化 prefill 路径。PD 分离正在从"能用"向"高效率"演进。
5. **CUDA 13.0 / PyTorch 2.11 生态切换**：vLLM v0.20.0 默认 CUDA 13.0 + PyTorch 2.11，这是重要的环境基线变化，新部署需注意兼容性。
6. **TGI 归档的信号**：HuggingFace TGI 归档意味着推理框架竞争格局进一步集中到 vLLM / SGLang / TRT-LLM 三强，小众框架需找差异化定位。

---

## 明日跟踪建议

1. 🔍 **vLLM DeepSeek V4 后续补丁**：v0.20.1 修复了多个 V4 死锁和精度问题，关注 main 分支是否还有后续修复。
2. 🔍 **llama.cpp 内存优化细节**：b9028 的设备缓冲区内存节省选项值得关注具体实现，对边缘部署场景有参考价值。
3. 🔍 **SGLang Elastic EP 生产验证**：关注社区对 Elastic EP 部分容错的实测反馈，特别是多卡故障场景下的恢复延迟。
4. 🔍 **TensorRT-LLM v1.3.0 正式版**：rc13 已包含大量新功能，关注正式版发布时间和 Stability 承诺。
5. 🔍 **TurboQuant 2-bit KV 实测精度**：2-bit KV cache 在不同模型/任务上的精度退化情况，是否可接受。

---

*报告生成时间：2026-05-05 14:50 CST*
