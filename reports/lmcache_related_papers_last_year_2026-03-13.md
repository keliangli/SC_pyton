# 与 LMCache 类似的近一年论文整理

- 整理时间：2026-03-13
- 统计区间：2025-03-13 ~ 2026-03-13
- 主题口径：与 **LMCache** 相近的 LLM serving / KV cache 系统方向，重点关注：
  - KV cache 分层 / tiered storage / hierarchical cache
  - prefix cache / context cache 共享与池化
  - KV cache 外存卸载 / offloading
  - disaggregated serving 下的 KV 传输与管理
  - cache-aware 路由与调度
- 说明：以下列表优先覆盖 **“和 LMCache 系统问题最接近”** 的论文，而不是所有 KV cache 压缩 / 剪枝 / eviction 工作。

---

## 1. 一句话结论

近一年里，和 LMCache 最接近的论文主要集中在 4 个方向：

1. **分层 / tiered KV cache**
2. **外存 / SSD / disaggregated memory 下的 KV cache 管理**
3. **prefix cache 共享 / 池化**
4. **cache-aware 调度 / 路由**

如果要找 **“LMCache 的直接同类工作”**，最值得优先看的论文是：

- Strata
- TokenLake
- Adaptive Multi-Objective Tiered Storage Configuration for KV Cache in LLM Service
- PrefillShare
- ContiguousKV
- DualPath
- InferSave
- MOM

---

## 2. 最像 LMCache 的核心论文

### 2.1 Strata: Hierarchical Context Caching for Long Context Language Model Serving
- **时间**：2025-08-26
- **链接**：https://arxiv.org/abs/2508.18572
- **关键词**：hierarchical context caching, long-context serving, multi-tier cache
- **为什么像 LMCache**：
  - 明确聚焦 **hierarchical context caching**
  - 问题定义和 LMCache 非常接近：GPU 放不下长上下文 KV cache，需要做多层级缓存管理
  - 更适合拿来和 LMCache 做“分层缓存设计”对照
- **推荐度**：非常高

### 2.2 TokenLake: A Unified Segment-level Prefix Cache Pool for Fine-grained Elastic Long-Context LLM Serving
- **时间**：2025-08-24
- **链接**：https://arxiv.org/abs/2508.17219
- **关键词**：prefix cache pool, segment-level sharing, cluster-level serving
- **为什么像 LMCache**：
  - 直接做 **prefix cache pool**
  - 关注集群级别的 cache 复用、数据冗余、负载不均、内存碎片
  - 和 LMCache 一样，不再把 cache 视为单引擎内部细节，而是系统级资源
- **推荐度**：非常高

### 2.3 Adaptive Multi-Objective Tiered Storage Configuration for KV Cache in LLM Service
- **时间**：2026-02-25
- **链接**：https://arxiv.org/abs/2603.08739
- **关键词**：tiered storage, KV cache, multi-objective optimization
- **为什么像 LMCache**：
  - 直接聚焦 **KV cache 的分层存储配置**
  - 优化目标与工业缓存层很一致：**成本 / 吞吐 / 延迟**
  - 适合拿来和 LMCache 的 storage-tier 设计放在一起看
- **推荐度**：非常高

### 2.4 PrefillShare: A Shared Prefill Module for KV Reuse in Multi-LLM Disaggregated Serving
- **时间**：2026-02-12
- **链接**：https://arxiv.org/abs/2602.12029
- **关键词**：shared prefill, KV reuse, multi-LLM, disaggregated serving
- **为什么像 LMCache**：
  - 直接研究 **shared prefill + KV reuse**
  - 场景在 **multi-LLM / disaggregated serving** 下，很接近 LMCache 的传输模式
  - 和 LMCache 形成一个很自然的对照：LMCache 更像 cache layer，本工作更强调共享 prefill 模块
- **推荐度**：非常高

### 2.5 ContiguousKV: Accelerating LLM Prefill with Granularity-Aligned KV Cache Management
- **时间**：2026-01-20
- **链接**：https://arxiv.org/abs/2601.13631
- **关键词**：persistent prefix KV cache, offloading, granularity-aligned management
- **为什么像 LMCache**：
  - 关注 **persistent prefix KV cache**
  - 讨论了 prefix KV cache offload 到二级存储后的 I/O 瓶颈
  - 非常接近 LMCache 的工程核心问题：不仅要复用，还要高效加载
- **推荐度**：高

### 2.6 DualPath: Breaking the Storage Bandwidth Bottleneck in Agentic LLM Inference
- **时间**：2026-02-25
- **链接**：https://arxiv.org/abs/2602.21548
- **关键词**：agentic inference, disaggregated architecture, storage bandwidth, KV-cache I/O
- **为什么像 LMCache**：
  - 关注 disaggregated 架构下 **KV-cache 外存加载的 I/O 瓶颈**
  - 更偏系统论文，问题设定与 LMCache 高度同域
  - 适合和 LMCache 一起看“KV 层做大以后，系统瓶颈如何转移”
- **推荐度**：高

### 2.7 Cost-Efficient LLM Serving in the Cloud: VM Selection with KV Cache Offloading
- **时间**：2025-04-16
- **链接**：https://arxiv.org/abs/2504.11816
- **别名**：InferSave
- **关键词**：cloud serving, KV cache offloading, cost optimization
- **为什么像 LMCache**：
  - 直接围绕 **KV cache offloading** 展开
  - 但更偏云上 VM 选择 / 成本优化，而不是完整缓存层设计
  - 属于“问题域很近，但系统层级略不同”的工作
- **推荐度**：中高

### 2.8 MOM: Memory-Efficient Offloaded Mini-Sequence Inference for Long Context Language Models
- **时间**：2025-04-16
- **链接**：https://arxiv.org/abs/2504.12526
- **关键词**：long-context inference, offloading, memory-efficient inference
- **为什么像 LMCache**：
  - 明确支持 **KV cache offloading**
  - 更偏 memory-efficient inference 方法，而不是 serving cache layer
  - 可作为 LMCache 的“同问题域邻近工作”参考
- **推荐度**：中高

---

## 3. 次一级相关：更偏调度 / 路由 / 场景化 cache reuse

### 3.1 DualMap: Enabling Both Cache Affinity and Load Balancing for Distributed LLM Serving
- **时间**：2026-02-06
- **链接**：https://arxiv.org/abs/2602.06502
- **关键词**：cache affinity, load balancing, distributed serving
- **看点**：
  - 讨论 **cache affinity** 和 **load balancing** 的冲突
  - 如果想研究 LMCache 在集群调度层如何发挥作用，这篇很有参考价值

### 3.2 GORGO: Maximizing KV-Cache Reuse While Minimizing Network Latency in Cross-Region LLM Load Balancing
- **时间**：2026-02-12
- **链接**：https://arxiv.org/abs/2602.11688
- **关键词**：KV reuse, cross-region routing, network latency
- **看点**：
  - 更偏 **cache-aware global routing**
  - 适合和 LMCache 的 control plane / placement 思路结合看

### 3.3 From Prefix Cache to Fusion RAG Cache: Accelerating LLM Inference in Retrieval-Augmented Generation
- **时间**：2026-01-19
- **链接**：https://arxiv.org/abs/2601.12904
- **关键词**：RAG cache, prefix cache, chunk-level reuse
- **看点**：
  - 把 prefix cache 的思路扩展到 **RAG chunk-level cache reuse**
  - 如果关注 LMCache 在 RAG 方向的延展，这篇值得补读

### 3.4 TableCache: Primary Foreign Key Guided KV Cache Precomputation for Low Latency Text-to-SQL
- **时间**：2026-01-13
- **链接**：https://arxiv.org/abs/2601.08743
- **关键词**：precomputed KV cache, Text-to-SQL, repeated schema context
- **看点**：
  - 典型的任务场景化 KV cache 复用
  - 说明 prefix/KV cache reuse 已经开始往垂直任务里落地

---

## 4. 相关但不算 LMCache 直接同类：更偏压缩 / 剪枝 / eviction / retrieval

这些论文与 KV cache 高度相关，但路线更偏 **压缩、检索、剪枝、驱逐策略**，不是 LMCache 这种“系统层 KV cache layer”主线。

### 4.1 ParisKV: Fast and Drift-Robust KV-Cache Retrieval for Long-Context LLMs
- **时间**：2026-02-07
- **链接**：https://arxiv.org/abs/2602.07721
- **备注**：偏 **KV-cache retrieval framework**，支持 CPU-offloaded KV + UVA，相关但不完全同类

### 4.2 Fast KVzip: Efficient and Accurate LLM Inference with Gated KV Eviction
- **时间**：2026-01-25
- **链接**：https://arxiv.org/abs/2601.17668
- **备注**：偏 **gated KV eviction**

### 4.3 KVzap: Fast, Adaptive, and Faithful KV Cache Pruning
- **时间**：2026-01-12
- **链接**：https://arxiv.org/abs/2601.07891
- **备注**：偏 **adaptive pruning**

### 4.4 HeteroCache: A Dynamic Retrieval Approach to Heterogeneous KV Cache Compression for Long-Context LLM Inference
- **时间**：2026-01-20
- **链接**：https://arxiv.org/abs/2601.13684
- **备注**：偏 **heterogeneous KV compression / retrieval**

### 4.5 CacheSolidarity: Preventing Prefix Caching Side Channels in Multi-tenant LLM Serving Systems
- **时间**：2026-03-11
- **链接**：https://arxiv.org/abs/2603.10726
- **备注**：不是提效论文，而是 **prefix caching side channel** 安全论文；如果做企业级 KV 层，这篇很值得关注

---

## 5. 推荐阅读顺序

如果目标是做 **LMCache 相关调研 / 对标表 / 技术路线梳理**，建议按这个顺序看：

1. **Strata**
2. **TokenLake**
3. **Adaptive Multi-Objective Tiered Storage Configuration for KV Cache in LLM Service**
4. **PrefillShare**
5. **ContiguousKV**
6. **DualPath**
7. **DualMap / GORGO**
8. **Fusion RAG Cache / TableCache**

这样读的好处是：
- 前半段先把 **cache layer / tiered storage / shared prefill** 主线建立起来
- 后半段再看 **routing / scheduling / 场景化 cache reuse**

---

## 6. 更实用的技术分类

如果后续要写综述 / 对比表，可以直接按下面的结构分：

### 6.1 Tiered / hierarchical KV cache
- Strata
- Adaptive Multi-Objective Tiered Storage Configuration for KV Cache in LLM Service
- ContiguousKV

### 6.2 Prefix cache pooling / sharing
- TokenLake
- PrefillShare
- From Prefix Cache to Fusion RAG Cache
- TableCache

### 6.3 Disaggregated / offloaded serving
- DualPath
- InferSave
- MOM

### 6.4 Cache-aware routing / scheduling
- DualMap
- GORGO

### 6.5 Safety / side channel
- CacheSolidarity

---

## 7. 总结判断

### 7.1 最像 LMCache 的论文
如果只挑最像的 4 篇：
- **Strata**
- **TokenLake**
- **Adaptive Multi-Objective Tiered Storage Configuration for KV Cache in LLM Service**
- **PrefillShare**

### 7.2 最适合工程对标的论文
如果从工程系统视角挑：
- **ContiguousKV**
- **DualPath**
- **DualMap**
- **GORGO**

### 7.3 最值得作为补充方向的论文
如果想扩展 LMCache 的应用边界：
- **From Prefix Cache to Fusion RAG Cache**
- **TableCache**
- **CacheSolidarity**

---

## 8. 后续可继续补充的方向

如果后面继续扩展这份整理，建议补两块：

1. **正式会议版本补全**
   - MLSys / NSDI / OSDI / EuroSys / ASPLOS / SOSP / ACL
   - 当前版本以 arXiv / 近一年公开论文为主

2. **加入对比表**
   - 论文
   - 核心问题
   - 方法关键词
   - 与 LMCache 的相同点
   - 与 LMCache 的差异点
   - 是否值得精读

---

## 9. 附：快速索引

| 论文 | 时间 | 方向 | 链接 |
|---|---|---|---|
| Strata | 2025-08-26 | hierarchical context caching | https://arxiv.org/abs/2508.18572 |
| TokenLake | 2025-08-24 | segment-level prefix cache pool | https://arxiv.org/abs/2508.17219 |
| Adaptive Multi-Objective Tiered Storage Configuration for KV Cache in LLM Service | 2026-02-25 | tiered KV storage | https://arxiv.org/abs/2603.08739 |
| PrefillShare | 2026-02-12 | shared prefill / KV reuse | https://arxiv.org/abs/2602.12029 |
| ContiguousKV | 2026-01-20 | persistent prefix KV / offloading | https://arxiv.org/abs/2601.13631 |
| DualPath | 2026-02-25 | disaggregated KV I/O bottleneck | https://arxiv.org/abs/2602.21548 |
| InferSave | 2025-04-16 | KV offloading / VM selection | https://arxiv.org/abs/2504.11816 |
| MOM | 2025-04-16 | offloaded long-context inference | https://arxiv.org/abs/2504.12526 |
| DualMap | 2026-02-06 | cache-aware scheduling | https://arxiv.org/abs/2602.06502 |
| GORGO | 2026-02-12 | cross-region cache-aware routing | https://arxiv.org/abs/2602.11688 |
| From Prefix Cache to Fusion RAG Cache | 2026-01-19 | RAG cache reuse | https://arxiv.org/abs/2601.12904 |
| TableCache | 2026-01-13 | Text-to-SQL KV precompute | https://arxiv.org/abs/2601.08743 |
| ParisKV | 2026-02-07 | KV retrieval | https://arxiv.org/abs/2602.07721 |
| Fast KVzip | 2026-01-25 | KV eviction | https://arxiv.org/abs/2601.17668 |
| KVzap | 2026-01-12 | KV pruning | https://arxiv.org/abs/2601.07891 |
| HeteroCache | 2026-01-20 | KV compression / retrieval | https://arxiv.org/abs/2601.13684 |
| CacheSolidarity | 2026-03-11 | prefix cache side-channel security | https://arxiv.org/abs/2603.10726 |

---

## 10. 最后一句

如果把 LMCache 看成 **“企业级 LLM serving 的 KV cache layer”**，那么近一年最相关的新工作已经明显从“单点 prefix cache”演进到：

- **多层存储**
- **共享 prefill / cache pool**
- **disaggregated KV transport**
- **cache-aware routing / scheduling**
- **安全与多租户隔离**

这说明 KV cache 正在从 inference engine 的内部优化，逐步变成独立的系统层对象。
