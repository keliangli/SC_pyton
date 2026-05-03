# GitHub 大模型推理日报（2026-05-03）

> 抓取时间：2026-05-03 11:52 CST | 覆盖范围：近一周重大 release 及 commit

---

## 📌 今日要点

1. **vLLM v0.20.0 正式发布** — DeepSeek V4 初步支持、CUDA 13.0 默认切换、PyTorch 2.11 + Transformers v5 升级，320 位贡献者提交 752 commits，是本周期最大版本更新。
2. **TensorRT-LLM v1.3.0rc13** — DeepSeek-V3.2/V3-Lite Blackwell 优化、Nemotron 3 Nano Omni 初步支持、FP4 残差量化、稀疏 MQA/GQA 注意力，内核与 serving 双线推进。
3. **FlashInfer v0.6.10rc1** — CCCL v3.3.2 独立引入、head_dim=512 trtllm attention kernel 支持，为超长上下文及大 head 模型铺路。
4. **llama.cpp 连发 b9009/b9010** — server checkpoint 数据零拷贝优化 + CUDA 多卡 PCI bus ID 去重 OOM 修复，边缘推理稳定性提升。

---

## 🚀 项目速递

### vLLM — v0.20.0 (Apr 27)

- 🔗 <https://github.com/vllm-project/vllm/releases/tag/v0.20.0>
- DeepSeek V4 初始支持 (#40860)，含 DSML token-leakage 修复及 DSA+MTP IMA 修正
- CUDA 13.0 成为默认编译目标 (#39878)，CUDA 13.0.2 对齐 PyTorch 2.11.0
- PyTorch 2.11 升级 (#34644)，XPU 也从 2.10 升至 2.11
- Python 3.14 加入支持列表 (#34770)
- Transformers v5 兼容 (#30566)
- 752 commits / 320 contributors (123 new)

### TensorRT-LLM — v1.3.0rc13 (Apr 29)

- 🔗 <https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc13>
- Nemotron 3 Nano Omni 初步支持及 ViT attention 优化 (#12921, #12911)
- GLM-4.7 / GLM-5 tool parser 支持 (#13150)
- DeepSeek-V3.2 / V3-Lite Blackwell & SM100 性能优化及 chunked-prefill 修复 (#13142, #13257)
- FP4 残差量化、RMSNorm 扩展覆盖、SageAttention 内核刷新 (#13033, #13103, #12937)
- 稀疏 MQA/GQA 注意力 + 新分片基础设施 (#12470, #12419)
- VisualGen Cache-DiT 统一缓存加速器 (#12548)
- Serving：异步媒体加载、视频帧解码加速、CUDA graph padding-aware tuning (#13034, #12677)

### FlashInfer — v0.6.10rc1 (Apr 30)

- 🔗 <https://github.com/flashinfer-ai/flashinfer/releases/tag/v0.6.10rc1>
- CCCL v3.3.2 从 GitHub 独立引入，不再依赖 CTK 内置版本 (#3091)
- head_dim=512 支持 trtllm attention kernel (#3091)
- Nightly v0.6.9-20260501 持续更新

### llama.cpp — b9010 (May 2) / b9009 (May 2)

- 🔗 <https://github.com/ggml-org/llama.cpp/releases/tag/b9010>
- 🔗 <https://github.com/ggml-org/llama.cpp/releases/tag/b9009>
- b9010：CUDA 多卡 PCI bus ID 去重 OOM 修复 (#22533)
- b9009：server checkpoint 数据避免 host copies，减少内存拷贝 (#22558)

### SGLang — v0.5.10 (Apr 6) / v0.5.10.post1 (Apr 9)

- 🔗 <https://github.com/sgl-project/sglang/releases/tag/v0.5.10>
- Piecewise CUDA Graph 默认启用，降低显存开销并提升复杂控制流吞吐 (#16331)
- Elastic EP (NIXL-EP) 集成，DeepSeek MoE 部分容错——GPU 故障后自动重分配专家权重 (#19248)
- GPU Staging Buffer 优化 PD 分离部署中 GQA 模型 RDMA 传输

### Triton Inference Server — v2.68.0 (Apr 28)

- 🔗 <https://github.com/triton-inference-server/server/releases/tag/v2.68.0>
- ⚠️ Breaking：客户端共享内存默认禁用，需 `--allow-client-shm=true` 显式启用
- max_inflight_requests 跨 ensemble 请求强制限制
- OpenAI 兼容前端新增模型控制模式

### TGI (HuggingFace) — 已归档

- 🔗 <https://github.com/huggingface/text-generation-inference>
- 于 2026-03-21 归档为只读，最后版本 v3.3.7 (Dec 2025)，不再有活跃更新

---

## 💡 工程启发

1. **CUDA 13.0 生态迁移已启动**：vLLM 率先默认 CUDA 13.0 + PyTorch 2.11，TensorRT-LLM 也持续推进 Blackwell/SM100 优化。生产环境应开始评估 CUDA 13 兼容性，尤其注意 cuDNN/cuBLAS 版本对齐。
2. **DeepSeek V4 已进入框架支持阶段**：vLLM 首发 V4 支持，TRT-LLM 持续优化 V3.2/V3-Lite。MoE 模型的 token-leakage 修复和 DSA+MTP IMA 修正说明 DeepSeek 架构细节仍在快速迭代，跟进时需注意 commit 级别的 bugfix。
3. **FP4 量化从实验走向产品**：TRT-LLM v1.3.0rc13 引入 FP4 残差量化，配合 Blackwell 硬件，4-bit 推理精度与吞吐的工程平衡点正在被重新定义。
4. **FlashInfer head_dim=512 的信号**：超长上下文 + 大 head 维度模型（如部分 ViT / 多模态架构）需要更大 head_dim 支持，FlashInfer 此举预示多模态推理内核需求上升。
5. **TGI 归档后的生态替代**：TGI 归档意味着 HuggingFace 推理栈重心转移，vLLM / SGLang / TRT-LLM 将成为主要生产级选项，迁移规划宜早不宜迟。

---

## 🔭 明日跟踪建议

- [ ] vLLM v0.20.1 补丁进展（DeepSeek V4 修复可能快速跟进）
- [ ] SGLang 下一版本动态——v0.5.10 已近一月，可能接近 v0.5.11 或 v0.6
- [ ] TensorRT-LLM v1.3.0 正式版（当前 rc13，关注 rc→GA 时间线）
- [ ] FlashInfer v0.6.10 正式版发布节奏
- [ ] llama.cpp 后续版本——b9010/b9009 间隔仅数小时，观察是否连续修复模式
- [ ] mistral.rs / candle 等轻量推理框架近期 release
