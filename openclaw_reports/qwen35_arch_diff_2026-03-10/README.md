# Qwen3-32B vs Qwen3.5-27B：架构与算子差异总结

日期：2026-03-10

## 一句话结论
Qwen3.5-27B 虽然名义上还是 dense 模型，但它并不是 Qwen3-32B 的“小改版”。
对推理后端来说，最大的变化不是参数量，而是 **token mixer、cache 结构、prefill/decode 路径和 kernel 依赖都变了**，所以很多平台适配工作量会明显大于传统 dense 模型升级。

---

## 1. 两个模型的核心差异

### Qwen3-32B
- 架构：`Qwen3ForCausalLM`
- 主干仍然是 **标准 Attention / GQA**
- HF 实现是典型的：
  - `Qwen3Attention`
  - `DynamicCache`
  - `create_causal_mask` / `create_sliding_window_causal_mask`
- 模型卡关键点：
  - 64 层
  - GQA：Q=64，KV=8
  - 原生上下文 32,768，YaRN 扩到 131,072

本质上，它还是“标准 attention + KV cache”范式。

### Qwen3.5-27B
- 模型族：`qwen3_5`
- ModelScope 卡上显示架构：`Qwen3_5ForConditionalGeneration`
- 官方模型卡明确给出了 hidden layout：
  - `16 × (3 × (Gated DeltaNet → FFN) → 1 × (Gated Attention → FFN))`
- 换句话说，64 层里大致是：
  - **48 层 Gated DeltaNet / linear attention**
  - **16 层 Gated Attention / full attention**
- 模型卡关键点：
  - Gated DeltaNet：V 头数 48，QK 头数 16，head dim=128
  - Gated Attention：Q 头数 24，KV 头数 4，head dim=256，rotary dim=64
  - 原生上下文 262,144，可扩到 1,010,000

所以 Qwen3.5-27B 的主干不再是“纯 attention”，而是 **hybrid token mixer**。

---

## 2. 为什么 Qwen3.5-27B 的适配工作量会大很多

## 2.1 token mixer 从纯 attention 变成 hybrid
Qwen3-32B 的后端假设通常是：
- 每层都是 attention
- decode = KV cache 追加 + attention kernel

Qwen3.5-27B 不是这样。
在 HF `qwen3_5` 实现里：
- `linear_attention` 层走 `Qwen3_5GatedDeltaNet`
- `full_attention` 层走 `Qwen3_5Attention`

也就是说，runtime 需要在同一个模型里同时支持两套 token mixer。

这会影响：
- layer dispatch
- graph lowering
- kernel 调度
- runtime planner

后端已经不能再假设“所有层都是 attention 层”。

## 2.2 cache 不再只有 KV cache
Qwen3-32B 基本是标准 KV cache。

但 Qwen3.5-27B 在 HF 里专门定义了 `Qwen3_5DynamicCache`，同时维护：
- `key_cache`
- `value_cache`
- `conv_states`
- `recurrent_states`

含义是：
- full attention 层仍用 KV cache
- linear attention 层使用 conv state + recurrent state

这会直接带来工程复杂度：
- request merge/split 时怎么搬运 recurrent state
- beam reorder 时怎么一起重排 KV / conv / recurrent
- paged KV cache 机制还能复用多少
- continuous batching 怎么管理混合状态

所以这已经不是“cache 结构小改”，而是整个 cache manager 需要升级。

## 2.3 prefill 和 decode 路径分裂
Qwen3.5-27B 的 Gated DeltaNet 有两条典型路径：
- prefill：`chunk_gated_delta_rule(...)`
- decode：`recurrent_gated_delta_rule(...)`

这和 Qwen3-32B 的标准 attention prefill/decode 不同。

影响包括：
- continuous batching
- prefix cache 复用
- chunked prefill
- speculative decoding
- CUDA graph capture

很多后端原来只极致优化了“attention prefill + attention decode”，
现在需要额外支持一条 **recurrent linear path**。

## 2.4 新依赖不再是传统 attention 栈
HF `qwen3_5` 里直接用到了：
- `causal_conv1d`
- `flash-linear-attention`（FLA）
  - `chunk_gated_delta_rule`
  - `fused_recurrent_gated_delta_rule`
  - `FusedRMSNormGated`

这意味着：
- 不是只靠 FlashAttention / SDPA / xFormers 就能高效支持
- 后端要么直接集成这些库
- 要么自己实现等价 CUDA/Triton kernel

还要处理：
- bf16/fp16/fp8/fp4/int4 等 dtype
- TP/PP 切分
- Hopper / Blackwell / AMD 等不同硬件后端
- kernel 数值稳定性

## 2.5 linear attention 前面还带 causal depthwise conv
在 `Qwen3_5GatedDeltaNet` 中，线性路径不是纯线性 attention，而是还包含：
- `in_proj_qkv`
- `conv1d(groups=self.conv_dim, kernel_size=...)`
- decode 时维护 `conv_state`

所以它不是“把 softmax attention 换掉”那么简单，
而是 **causal depthwise conv + recurrent update + gated delta rule** 一整套 token mixer。

后端额外要补：
- conv kernel
- conv state 更新
- 与 batching/padding 的兼容
- 与 graph capture / paged scheduling 的兼容

## 2.6 mask / padding 语义也不同
HF 实现里，Qwen3.5 对 linear path 单独做了 `_update_linear_attn_mask`。

这意味着：
- linear attention 和 full attention 对 mask 的处理不完全一致
- 原来统一的 causal mask 流程不能直接复用

这会影响：
- 动态 batch 拼接
- left padding / right padding
- prefix sharing
- cached forward 的行为

## 2.7 量化适配难度更高
Qwen3-32B 的量化重点主要是：
- attention matmul
- qkv / o_proj
- mlp up/down/gate

Qwen3.5-27B 还新增了：
- linear attention 内部投影
- depthwise conv1d
- recurrent state update
- gated rmsnorm / 特殊 norm
- FLA 相关 kernel 的混精与量化兼容

所以 AWQ / GPTQ / FP8 / FP4 / W4A8 等路线，
不只是做线性层替换，还要重新验证 kernel 的数值稳定性和 layout。

---

## 3. 为什么很多平台会出现“能加载，但没完全适配好”
模型卡里常常会写“兼容 vLLM / SGLang / Transformers / KTransformers”，
但这通常只表示：
- 基础加载已打通，或
- 某条 dev 路线可以跑，或
- 有 fallback 路径能工作

距离真正生产可用，还经常差这些：
- 并发稳定性
- 混合状态管理
- 长上下文内存控制
- 量化 kernel 覆盖
- benchmark 调优
- TP/PP/EP 组合验证

所以“很多平台还没完全适配完”的体感，是符合工程现实的。

---

## 4. 最后的工程判断
可以把两者的差别概括成一句话：

- **Qwen3-32B** 的难点，是把 attention 引擎做快。
- **Qwen3.5-27B** 的难点，是把 serving runtime 从“纯 attention 引擎”升级成“hybrid token-mixer 引擎”。

这就是为什么 Qwen3.5-27B 虽然是 dense 27B，但适配成本不一定比传统 30B dense 更低，反而往往更高。

---

## 5. 对后端团队的实际工作拆解
如果是 vLLM / SGLang / LMDeploy / TensorRT-LLM 这类推理后端团队，通常要补：
1. 新 model executor / model runner
2. hybrid cache manager
3. linear attention prefill/decode kernel
4. conv1d state 管理
5. scheduler / batching 兼容
6. quantization & mixed precision 验证
7. 长上下文 / prefix cache / speculative decode 回归测试

---

## 参考依据
- ModelScope: `Qwen/Qwen3.5-27B`
- ModelScope: `Qwen/Qwen3-32B`
- Hugging Face Transformers:
  - `src/transformers/models/qwen3/modeling_qwen3.py`
  - `src/transformers/models/qwen3_5/modeling_qwen3_5.py`
  - `src/transformers/models/qwen3_5/configuration_qwen3_5.py`
