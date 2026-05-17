# GitHub 智能体日报（2026-05-17）

## 今日要点

1. **LangGraph 正式发布 1.2.0**：引入 durable error-handler（跨宿主崩溃恢复）、StateGraph `set_node_defaults()`、delta channel 快照增强，标志着 Agent 编排框架在容错与状态管理上的重大进步
2. **OpenAI Agents SDK v0.17.2**：集中修复 Conversations reasoning 持久化、realtime tool 自动响应、tracing retry backoff、AsyncSQLiteSession 等关键 bug，稳定性显著提升
3. **SGLang v0.5.12 发布**：DeepSeek-V4 全推理路径支持（含 TP/EP/CP/DP、PD 分离、W4A4 MegaMoE、TokenSpeed MLA 后端），对 Agent 推理部署直接利好
4. **vLLM v0.21.0 发布**：KV Offload + HMA、Speculative Decoding 支持 thinking budget、TOKENSPEED_MLA Blackwell 后端、transformers v5 迁移，Agent 推理基础设施全面升级
5. **crewAI 1.14.5a5/a6**：废弃 CrewAgentExecutor 默认切 AgentExecutor、Daytona sandbox 改进、安全补丁，架构迁移进行中
6. **mem0 CLI v0.2.5**：新增 Agent Mode（`mem0 init --agent` 5 秒创建身份）、插件同步 Claude settings，Agent 记忆层工具链日趋成熟

## 项目速递

### 🔷 LangGraph 1.2.0（2026-05-12）

- **durable error-handler resume**：Agent 执行跨宿主崩溃可恢复，提升长时任务可靠性
- **`set_node_defaults()`**：StateGraph 支持节点默认配置，减少重复代码
- **delta channel snapshot**：checkpoint 在 max supersteps 后强制快照，避免状态丢失
- **exit mode 重实现**：delta channel 退出逻辑优化
- **langchain-core 升级至 1.4.0**
- 🔗 https://github.com/langchain-ai/langgraph/releases/tag/1.2.0

### 🔷 OpenAI Agents Python v0.17.2（2026-05-12）

- 修复 OpenAI Conversations reasoning 持久化问题
- 修复 unknown realtime tools 自动响应行为
- 修复 tracing retry backoff 在 shutdown 时中断
- 修复 AsyncSQLiteSession 忽略 session settings
- 修复空 chat tool outputs
- 🔗 https://github.com/openai/openai-agents-python/releases/tag/v0.17.2

### 🔷 SGLang v0.5.12（2026-05-16）

- **DeepSeek-V4 全推理支持**：TP/EP/CP/DP 并行、PD 分离、HiSparse CPU offload、reasoning/tool call parser
- **TokenSpeed MLA 后端**：Blackwell SM100 专用 MLA prefill/decode + FP8 KV cache
- **W4A4 MegaMoE kernels**：近乎无损精度下更快 MoE 推理
- **Marlin/FlashInfer W4A8 MoE kernels**：Hopper 架构优化
- **Pipeline Parallelism + PD**：DeepSeek-V4 PP 支持
- **HiCache + UnifiedRadixTree**：统一 KV cache 管理
- 🔗 https://github.com/sgl-project/sglang/releases/tag/v0.5.12

### 🔷 vLLM v0.21.0（2026-05-15）

- **KV Offload + HMA**：KV offloading 与 Hybrid Memory Allocator 集成，支持 sliding window group
- **Speculative Decoding + thinking budget**：推理模型的 spec decode 现在尊重 thinking budget
- **TOKENSPEED_MLA 后端**：Blackwell 上 DeepSeek-R1/Kimi-K25 的 MLA 注意力后端
- **Transformers v4 废弃**：正式要求迁移至 transformers v5
- **C++20 编译要求**：破坏性构建变更
- **DeepSeek-V4**：AMD/ROCm 支持、pipeline parallelism、max reasoning effort、分离式服务修复
- 🔗 https://github.com/vllm-project/vllm/releases/tag/v0.21.0

### 🔷 crewAI 1.14.5a5 / 1.14.5a6（2026-05-12 ~ 05-15）

- **废弃 CrewAgentExecutor**：默认切换为 AgentExecutor，架构统一
- **Daytona sandbox 改进**：sandbox 工具增强
- **安全补丁**：langsmith ≥0.8.0、urllib3、gitpython
- **流式 tool call 修复**：available_functions 为空时的流式调用问题
- 🔗 https://github.com/crewAIInc/crewAI/releases/tag/1.14.5a6

### 🔷 mem0 CLI v0.2.5（2026-05-14）

- **Agent Mode**：`mem0 init --agent` 5 秒内创建未认领 key
- **`--agent-caller` 标志** + `mem0 identify` 自声明身份
- **插件同步**：自动同步 `~/.claude/settings.json` 与 shell rc 到 config.json
- **Claim flow**：`mem0 init --email` 原地升级 shadow account
- 🔗 https://github.com/mem0ai/mem0/releases/tag/cli-v0.2.5

## 对我工作的启发

1. **推理加速直接受益**：SGLang/vLLM 本周密集更新，DeepSeek-V4 推理路径日趋成熟（W4A4 MegaMoE、TokenSpeed MLA、PP+PD），可作为 benchmark 和部署参考
2. **Agent 容错能力提升**：LangGraph 1.2.0 的 durable error-handler 是长时 Agent 任务的关键基础设施，值得在编排层引入类似机制
3. **Speculative Decoding + thinking**：vLLM 支持 thinking budget 下的 spec decode，对 reasoning model 推理加速有直接参考价值
4. **KV Offload + HMA**：vLLM 的 KV offload 与 HMA 集成方案，对长上下文 Agent 推理的内存管理有启发
5. **Agent 记忆层工具化**：mem0 Agent Mode 的快速身份创建 + 插件同步，展示了 Agent 记忆层向「开箱即用」演化的趋势
6. **架构迁移趋势**：crewAI 废弃 CrewAgentExecutor → AgentExecutor，OpenAI Agents SDK 持续修复 session/reasoning，行业正收敛到统一 Agent 执行模型

## 明日跟踪建议

- [ ] **SGLang v0.5.12**：测试 DeepSeek-V4 W4A4 MegaMoE + TokenSpeed MLA 性能数据，对比 vLLM v0.21.0
- [ ] **vLLM v0.21.0**：验证 KV Offload + HMA 在长上下文 Agent 场景的效果
- [ ] **LangGraph 1.2.0**：评估 durable error-handler 对多步 Agent 工作流可靠性的实际影响
- [ ] **crewAI 1.14.5 正式版**：跟踪 AgentExecutor 迁移完成后的稳定版本
- [ ] **OpenAI Agents SDK**：关注 v0.18 是否引入新特性（当前 v0.17.x 集中修 bug）
