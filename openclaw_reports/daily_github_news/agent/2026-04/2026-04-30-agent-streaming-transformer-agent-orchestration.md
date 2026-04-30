# GitHub 智能体日报 — 2026-04-30

> 数据窗口：2026-04-29 06:00 UTC ~ 2026-04-30 06:00 UTC
> 采集时间：2026-04-30 13:50 CST

---

## 今日要点

1. **LangGraph 1.2.0a1 进入 Alpha**：引入 Streaming Transformer 基础设施、DeltaChannel、优雅关停/排空机制，为下一代流式 Agent 执行铺路。
2. **Pydantic AI v1.88.0 发布**：跨 Provider `service_tier` 支持（Anthropic + Gemini + Vertex Priority PayGo）、output validate/process hooks、OpenAI Responses `phase` 支持。
3. **OpenAI Agents Python v0.14.7/0.14.8 连续更新**：GPT-5.5 别名与沙箱压缩适配、工具调用便捷属性（tool_name/call_id）、MCP 重导出错误修复。
4. **CrewAI 1.14.4a2**：Azure OpenAI Responses API 支持、自定义持久化键、MCP 原生服务器空工具降级。
5. **Dify v1.14.0 正式发布**：多人实时协作编辑工作流，WebSocket 同步 + 在线状态感知。
6. **Claude Code 密集更新（v2.1.121~v2.1.123）**：MCP `alwaysLoad` 配置、Bedrock Service Tier 选择、PostToolUse hooks 替换工具输出、Vim 可视模式。
7. **Google ADK v2.0.0b1 进入 Beta**：Workflow 图编排核心落地、ReAct 循环节点、HITL 事件重建恢复。

---

## 项目速递

### 1. LangGraph — 1.2.0a1 & prebuilt==1.0.13

- **仓库**：[langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)
- **关键变更**：
  - `StreamingTransformer` 基础设施与测试（#7519）
  - `DeltaChannel`：在 blob 中存储哨兵值，从 checkpoint_writes 重建（#7586）
  - 优雅关停/排空：cooperative drain by request（#7274）
  - 原生 v2 projections：custom / updates / checkpoints / debug / tasks（#7640）
  - EventLog 合并进 StreamChannel（#7637）
  - 节点级错误处理器（#7233，4/30 commit）
  - 定时器 alpha 版（#7647）
- **影响**：流式 Agent 执行架构重大升级，为复杂工作流的实时观察和恢复奠定基础。

### 2. Pydantic AI — v1.88.0

- **仓库**：[pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai)
- **关键变更**：
  - `output validate/process hooks`：拆分 `prepare_tools` 范围至 function tools，新增 `prepare_output_tools`（#4859）
  - 跨 Provider `service_tier` 模型设置：Anthropic + Gemini API + Vertex Priority PayGo（#4926）
  - Anthropic speed / `fast` mode for opus 4.6（#4300）
  - OpenAI Responses `phase` 支持（#5229）
  - `UIAdapter.sanitize_messages` + `allowed_file_url_schemes`（#5228）
  - 修复 `anthropic_cache_messages` per-block `cache_control`（#5227）
- **影响**：多 Provider 统一能力层进一步完善，服务等级选择为推理成本/延迟优化提供更细粒度控制。

### 3. OpenAI Agents Python — v0.14.7 & v0.14.8

- **仓库**：[openai/openai-agents-python](https://github.com/openai/openai-agents-python)
- **关键变更**：
  - v0.14.8：修复 MCP 重导出 import 错误保留（#3048）、沙箱 prompt 指令段分隔（#3047）
  - v0.14.7：`tool_name` / `call_id` 便捷属性（#3027）、memory consolidation turn limit 提高（#3038）、GPT-5.5 别名加入沙箱压缩（#3039）、tar/zip 成员校验收紧（#3040）
- **影响**：GPT-5.5 适配推进中，沙箱安全持续加固。

### 4. CrewAI — 1.14.4a2

- **仓库**：[crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)
- **关键变更**：
  - `@persist` 自定义持久化键（#5649）
  - Azure OpenAI Responses API 支持（#5201）
  - MCP 原生服务器无工具时降级为空列表+警告（#5657）
  - Azure credential_scopes 转发（#5661）
- **影响**：Azure 生态集成加深，持久化灵活性提升。

### 5. Dify — v1.14.0

- **仓库**：[langgenius/dify](https://github.com/langgenius/dify)
- **关键变更**：
  - **Collaboration**：多人实时协作编辑同一工作流，WebSocket 同步图更新 + 在线状态 + 可见性共享
  - 自部署默认关闭，需设置 `ENABLE_COLLABORATION_MODE = true` + `SERVER_WORKER_CLASS = geventwebsocket...`
- **影响**：Agent 工作流平台从单人构建走向团队协作，降低 Agent 应用开发的组织门槛。

### 6. Claude Code — v2.1.121 ~ v2.1.123

- **仓库**：[anthropics/claude-code](https://github.com/anthropics/claude-code)
- **关键变更**：
  - MCP `alwaysLoad`：工具跳过搜索延迟，始终可用（v2.1.121）
  - `claude plugin prune`：清理孤立自动安装插件依赖（v2.1.121）
  - PostToolUse hooks 可替换所有工具输出（非仅 MCP）（v2.1.121）
  - Bedrock Service Tier 环境变量选择（v2.1.122）
  - `/resume` 搜索框粘贴 PR URL 自动定位会话（v2.1.122）
  - OAuth 401 重试循环修复（v2.1.123）
  - Vim 可视模式 v/V（v2.1.118，4/23）
- **影响**：Coding Agent 工具链成熟度持续提升，MCP 生态和权限模型更完善。

### 7. Google ADK — v2.0.0b1（Beta）

- **仓库**：[google/adk-python](https://github.com/google/adk-python)
- **关键变更**（4/21 发布，本周持续活跃）：
  - Workflow(BaseNode) 图编排实现落地
  - ReAct 循环节点替代传统单 Agent 流程
  - HITL 事件重建恢复
  - NodeRunner 节点级执行隔离
  - 修复 YAML 嵌套配置 RCE 漏洞
- **影响**：ADK 2.0 架构从"单 Agent 封装"进化为"图编排 + 节点隔离"范式，值得关注 v2 正式版。

---

## 对我工作的启发

| 维度 | 启发 |
|------|------|
| **流式架构** | LangGraph 的 StreamingTransformer + DeltaChannel 表明流式 Agent 执行正成为标配。推理加速需关注流式场景下的 TTFT/TBT 优化。 |
| **多 Provider 统一层** | Pydantic AI 的 `service_tier` 抽象值得关注——未来推理部署可能需要根据成本/延迟/优先级动态选择 Provider 和服务层级。 |
| **Agent 安全** | OpenAI Agents 的 tar/zip 校验收紧、Google ADK 的 YAML RCE 修复，说明 Agent 沙箱安全是持续战场。与推理加速相关的沙箱开销值得评估。 |
| **图编排范式** | LangGraph v2 projections + Google ADK Workflow 共同指向"图编排"成为 Agent 框架核心抽象。推理引擎可能需要适配图结构的批调度。 |
| **协作化** | Dify 的实时协作意味着 Agent 开发将从个人走向团队，推理服务也需要考虑多用户并发和资源隔离。 |

---

## 明日跟踪建议

1. **LangGraph 1.2.0 正式版**：关注 StreamingTransformer 和 DeltaChannel 稳定化进度。
2. **Google ADK v2.0.0 正式版**：Beta 阶段迭代节奏，Workflow 编排实际性能表现。
3. **Pydantic AI `service_tier` 演进**：是否成为多 Provider 调度的标准抽象。
4. **Dify Collaboration 稳定性**：多用户场景下的性能和一致性表现。
5. **OpenAI Agents GPT-5.5 深度适配**：后续 release 是否暴露 GPT-5.5 特有能力（如 reasoning effort）。
