# GitHub 智能体日报（2026-05-12）

## 今日要点

- **LangGraph 1.2.0 正式发布**：核心新特性包括跨主机崩溃的持久化错误处理器恢复（durable error-handler resume）、StateGraph 新增 `set_node_defaults()`、Delta Channel 快照与退出模式增强、checkpoint-sqlite 流式遍历覆盖——标志着 LangGraph 在生产级 durable execution 方向迈出重要一步。
- **OpenAI Agents Python v0.17.2 发布**：修复 Conversations reasoning 持久化、realtime 工具自动响应、tracing 关闭时重试退避、AsyncSQLiteSession 设置丢失等问题；v0.17.1（5月11日）则修复了 sandbox 归档限制、Git 仓库子路径校验、tracing 最佳努力关闭等——连续两天密集修复，框架稳定性持续提升。
- **Mastra @mastra/core@1.32.0 发布**（5月4日）：新增细粒度授权（FGA）支持，可在 agent 执行/工具调用/工作流/内存线程访问前强制鉴权；新增 WorkOS FGA Provider；Scheduled Workflows 支持 cron 原生调度；MCP Apps 支持 `ui://` HTML 资源发布；可观测性升级含 Datadog Bridge——这是智能体框架在多租户和企业级场景的重大突破。

## 项目速递

### 1. LangGraph 1.2.0
- **版本**：1.2.0（正式版，5月12日发布）
- **链接**：https://github.com/langchain-ai/langgraph/releases/tag/1.2.0
- **核心更新**：
  - 🔥 **Durable error-handler resume**：跨主机崩溃后可恢复错误处理器执行，提升生产环境可靠性
  - `set_node_defaults()` 方法：为 StateGraph 节点设置默认配置
  - Delta Channel：强制在最大 supersteps 后进行快照，修复 exit mode
  - checkpoint-sqlite：新增 `get_delta_channel_history` 流式遍历覆盖
  - 依赖升级：langchain-core 1.4.0, urllib3 2.7.0, mistune 3.2.1
- **配套发布**：langgraph-prebuilt 1.1.0, langgraph-cli 0.4.26, checkpoint-sqlite 3.1.0

### 2. OpenAI Agents Python v0.17.2
- **版本**：v0.17.2（5月12日发布）
- **链接**：https://github.com/openai/openai-agents-python/releases/tag/v0.17.2
- **核心更新**：
  - 修复 Conversations reasoning 持久化问题（#3268）
  - 修复未知 realtime 工具的自动响应行为（#3287）
  - Tracing 关闭时中断重试退避（#3354）
  - 保留本地 approval 拒绝原因（#3359）
  - AsyncSQLiteSession 遵守会话设置（#3361）
  - 避免空 chat tool outputs（#3310）
- **v0.17.1（5月11日）**：
  - Sandbox 归档提取限制、Git 仓库子路径校验、tracing 最佳努力关闭
  - Session 修复：保留 hosted tool IDs、跳过损坏 items、corrupt 项处理

### 3. Mastra @mastra/core@1.32.0
- **版本**：@mastra/core@1.32.0（5月4日发布）
- **链接**：https://github.com/mastra-ai/mastra/releases/tag/%40mastra%2Fcore%401.32.0
- **核心更新**：
  - 🔥 **细粒度授权（FGA）**：基于关系的资源级访问控制，在 agent generate/stream、工具执行、工作流执行、内存线程访问前自动鉴权
  - **WorkOS FGA Provider**：`MastraFGAWorkos` 实现 WorkOS Authorization API 集成，支持多租户场景
  - 🔥 **Scheduled Workflows**：cron 原生调度，自动提升为事件驱动引擎，含 WorkflowScheduler、存储适配器（PG/LibSQL/MongoDB）、Studio UI
  - **MCP Apps**：MCP 服务器可发布 `ui://` HTML 应用资源，支持 `listResources()/readResource()` API
  - **可观测性升级**：嵌套 run 查询、高基数指标 TopK、DatadogBridge 自动嵌套
- **Breaking Changes**：schedules 存储 schema 变更，client-js Vector 返回类型变更

### 4. Pydantic AI v1.93.0
- **版本**：v1.93.0（5月9日发布）
- **链接**：https://github.com/pydantic/pydantic-ai/releases/tag/v1.93.0
- **核心更新**：
  - 新增 `tool_choice` 设置支持
  - Output tool call 事件流式输出（OutputToolCallEvent/OutputToolResultEvent）
  - Agent 取消时清理 spawned tasks
- **v1.92.0（5月8日）**：Anthropic task budget 支持、运行时 output_retries 覆盖、MCP session 修复

### 5. CrewAI 1.14.5a4
- **版本**：1.14.5a4（5月8日，pre-release）
- **链接**：https://github.com/crewAIInc/crewAI/releases/tag/1.14.5a4
- **核心更新**：
  - CLI 提取为独立 `crewai-cli` 包
  - 修复依赖问题（textual 迁移、certifi 添加）
  - 1.14.5a2 多项 bug 修复：task output 恢复、异步路径 acall、stop words 突变、BaseModel 输入转换

## 对我工作的启发

1. **Durable Execution 是智能体框架的下一个竞争焦点**：LangGraph 1.2.0 的持久化错误恢复 + Mastra 的 Scheduled Workflows 表明，生产级智能体需要"不丢状态"的执行保证。在推理加速场景中，长时运行 agent 的 checkpoint/resume 机制与推理引擎的 KV cache 管理有相似的设计哲学，值得交叉思考。

2. **FGA（细粒度授权）进入主流**：Mastra 引入 FGA 并提供 WorkOS 集成，说明多租户智能体部署已成刚需。这对推理服务同样有启示——模型推理 API 的 RBAC/ABAC 可以借鉴 FGA 的关系型权限模型。

3. **MCP 协议持续扩展**：Mastra 的 MCP Apps（`ui://` 资源）让 MCP 服务器不仅能暴露工具，还能发布交互式 UI。这对 agent-tool 生态的完整性是重要补充，后续 MCP 的资源发现与渲染可能成为新的优化点。

4. **SGLang + vLLM 的推理引擎迭代与智能体框架协同**：SGLang v0.5.11 的 Spec V2 默认开启 + Decode Radix Cache，vLLM v0.20.2 的 DeepSeek V4 修复，直接服务于智能体推理后端的吞吐与延迟。框架层的 durable execution + 推理层的 spec decoding，构成端到端的优化链路。

## 明日跟踪建议

- [ ] LangGraph 1.2.0 的 durable error-handler 在多节点部署下的实际表现与 benchmark
- [ ] Mastra FGA 的 `IFGAProvider` 接口是否会被其他框架（如 CrewAI、Pydantic AI）借鉴或标准化
- [ ] OpenAI Agents Python 的 session 稳定性修复是否影响 Conversations API 的推理性能特性
- [ ] MCP Apps `ui://` 资源规范的具体协议定义，以及与 OpenAI Responses API 的工具调用差异
- [ ] CrewAI 1.14.5 正式版发布时间与 CLI 独立化后的生态影响
