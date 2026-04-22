# GitHub 大模型推理日报（2026-04-22）

> 覆盖过去24小时与LLM推理相关的核心进展

---

## 📌 今日要点

| 类别 | 关键进展 |
|------|----------|
| **vLLM** | 合并Gemma3 block-local attention支持；MLA+FP8融合编译优化落地；多组worker KV传输增强 |
| **SGLang** | 发布v0.5.10，Elastic EP实现部分故障容错；GPU Staging Buffer将PD分离RDMA请求降低1000倍 |
| **llama.cpp** | WebGPU后端新增Conv2D内核支持；Reka Edge 2603多模态模型适配完成 |
| **TensorRT-LLM** | v0.22.0预发布，LTX-2视频生成两阶段流水线、生产级Prometheus监控上线 |

---

## 🚀 项目速递

### vLLM (v0.19.x 系列更新)

**已合并核心PR（4月21-22日）：**

| PR | 标题 | 技术价值 |
|----|------|----------|
| [#39823](https://github.com/vllm-project/vllm/pull/39823) | Add block-local attention and YaRN for Gemma3 | 为Gemma3添加块级局部注意力与YaRN长上下文扩展，支持滑动窗口注意力变体 |
| [#38877](https://github.com/vllm-project/vllm/pull/38877) | [compile] mla + group fp8 fusion | MLA注意力与FP8量化融合编译优化，降低内存带宽压力 |
| [#38453](https://github.com/vllm-project/vllm/pull/38453) | [kv_offload+HMA][8/N]: Support multi-group worker transfer | HMA分层内存架构支持多组worker并行KV传输，提升异构推理吞吐 |
| [#39986](https://github.com/vllm-project/vllm/pull/39986) | Add PyAV video backend | PyAV视频解码后端，支持并发视频处理，VLM视频理解性能提升 |

**版本发布：**
- [v0.19.1](https://github.com/vllm-project/vllm/releases/tag/v0.19.1) (4月18日) - Transformers v5.5.3升级，修复Gemma4流式工具调用bug
- [v0.19.0](https://github.com/vllm-project/vllm/releases/tag/v0.19.0) (4月3日) - 448 commits/197贡献者，含Gemma4全架构支持、零气泡异步调度+投机解码、ViT完整CUDA Graph

---

### SGLang (v0.5.10 发布)

**核心亮点：**

| 特性 | 描述 | 性能提升 |
|------|------|----------|
| **Elastic EP** | 部分故障容错：GPU故障时自动重分布专家权重，无需全量重启 | DeepSeek MoE部署可靠性提升 |
| **GPU Staging Buffer** | PD分离场景下聚集分散头切片至连续内存，批量RDMA传输 | RDMA请求数降低~1000x，TPS/GPU提升~5x (Qwen3.5 TP4+DEP4) |
| **HiSparse** | 稀疏注意力后端集成，通过稀疏性感知注意力降低长上下文计算 | 长序列推理效率显著提升 |
| **MXFP8支持** | FlashInfer MXFP8内核集成GEMM与MoE操作 | 混合精度FP8推理精度更高 |
| **MLX后端** | Apple Silicon原生MLX执行后端 | Mac本地推理无需CUDA |

**新模型支持：** Nemotron-3-Super、Mistral Small 4 (Pixtral)、LFM2-VL、Voxtral、GLM-5、Helios/LTX-2/Hunyuan3D-2 (扩散模型)

---

### llama.cpp (b8882/b8875 更新)

**今日合并：**
- [#21964](https://github.com/ggml-org/llama.cpp/pull/21964) - **WebGPU后端Conv2D内核支持**：浏览器端推理新增卷积层能力，f16/f32双精度通过测试
- [#21616](https://github.com/ggml-org/llama.cpp/pull/21616) - **Reka Edge 2603支持**：新增Yasa2视觉编码器、Reka-Edge对话模板、GGUF转换脚本

**发布构建：**
- b8882 (4月22日) - WebGPU Conv2D + Emscripten busy-poll修复
- b8875 (4月21日) - Reka Edge多模态完整支持

---

### TensorRT-LLM (v0.22.0 预发布)

**关键更新（4月17日）：**

| 类别 | 更新内容 |
|------|----------|
| **模型** | LTX-2两阶段流水线、Nemotron Nano/RADIO视频时序压缩、Qwen-Next缓存收发器、CuteDSL MoE后端 |
| **LoRA** | 支持FP8权重加载、投机解码兼容、大规模adapter OOM修复 |
| **监控** | 生产级Prometheus指标（迭代统计、token计数器、阶段直方图）、NvTelemetry/GXT遥测合规 |
| **PD分离** | 对话亲和性路由、块复用启用、HMAC认证、ZMQ异步poller替换busy-poll |
| **性能** | Qwen3.5解码delta内核优化、DSA MLA注意力host开销降低、AllReduce后端benchmark覆盖 |

---

## 💡 工程启发

### 1. 稀疏注意力成为长上下文标配
- **HiSparse**在SGLang的集成表明，稀疏性感知注意力正从研究走向生产，长序列推理不再受限于稠密注意力的O(n²)复杂度。
- **启发**：对于128K+上下文场景，优先考虑稀疏注意力架构（NSA/HiSparse）而非暴力堆算力。

### 2. PD分离架构进入精细化优化阶段
- **SGLang GPU Staging Buffer**通过聚集分散头切片降低RDMA请求1000倍，说明PD分离的瓶颈已从"能不能做"转向"如何做更高效"。
- **TensorRT-LLM conversation-affinity routing**进一步引入对话亲和性路由，减少跨节点KV传输。
- **启发**：PD分离架构需关注微观数据布局（tensor layout）对网络传输效率的影响。

### 3. 多模态推理统一框架成型
- vLLM/SGLang/TensorRT-LLM同步加强VLM支持（PyAV后端、chunk-aware ViT、LTX-2流水线），视觉编码器优化策略（CUDA Graph、torch.compile）向语言模型对齐。
- **启发**：多模态推理的优化方法论正在收敛，ViT编码器的CUDA Graph捕获将成为标配。

### 4. FP8/MXFP8量化生态成熟
- vLLM MLA+FP8融合、SGLang MXFP8内核、TensorRT-LLM FP8 LoRA支持，表明FP8已从"实验特性"变为"生产就绪"。
- **启发**：H100/H200/Blackwell平台应默认开启FP8，配合microscaling格式（MXFP8）平衡精度与效率。

---

## 📋 明日跟踪建议

| 优先级 | 跟踪项 | 理由 |
|--------|--------|------|
| **P0** | vLLM Gemma3 block-local attention性能benchmark | 验证长上下文下的实际吞吐提升 |
| **P0** | SGLang Elastic EP故障恢复延迟指标 | 评估MoE部署的容错SLA |
| **P1** | TensorRT-LLM v0.22.0正式版发布 | 生产环境升级评估 |
| **P1** | llama.cpp WebGPU Conv2D端到端性能 | 浏览器端多模态可行性验证 |
| **P2** | vLLM HMA多组worker传输吞吐测试 | 异构推理（CPU offload）场景收益量化 |

---

## 🔗 原文链接合集

- **vLLM Releases**: https://github.com/vllm-project/vllm/releases
- **vLLM Commits**: https://github.com/vllm-project/vllm/commits/main
- **SGLang Releases**: https://github.com/sgl-project/sglang/releases
- **llama.cpp Releases**: https://github.com/ggml-org/llama.cpp/releases
- **TensorRT-LLM Releases**: https://github.com/NVIDIA/TensorRT-LLM/releases

---

*报告生成时间: 2026-04-22 14:50 CST*
