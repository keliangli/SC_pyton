# GitHub 智能体日报 — 2026-05-03

> 数据窗口：2026-05-02 ~ 2026-05-03（过去 24h 内发布的 release/重要更新）

---

## 📌 今日要点

1. **OpenAI Agents SDK v0.15.1**（5月2日）：暴露 Responses WebSocket keepalive 配置，修复 UnixLocal PTY 子进程 SIGINT 信号处理，改善 Windows 文档。
2. **ElizaOS v2.0.0-alpha.535**（5月2日）：连续 3 天高频 alpha 迭代（526→535），新增 n8n-workflow plugin vendor 化、依赖批量更新，2.0 正式版临近。
3. **Pydantic AI v1.89.1**（5月1日）：集成 Library Skills（library-skills.io）增强 coding-agent 能力；修复 ToolManager 校验和 anyio.Lock 事件循环绑定。
4. **LangGraph 1.2.0a5**（5月1日）：修复 `_messages_delta_reducer` 类型强制转换；prebuilt 同步升级至 1.1.0a2，1.2.0 正式版临近。
5. **crewAI 1.14.5a1**（5月1日）：新增 `restore_from_state_id` kickoff 参数；ExaSearchTool 重命名+highlights；修复 skills loading events for traces。
6. **Agno v2.6.4**（4月28日）：新增 WikiContextProvider（filesystem+git 后端、web ingestion、read/write flags），Agent 上下文管理再升级。
7. **新项目 BlameBot**（5月2日）：AI on-call agent，自动检测部署失败→解释故障→分页通知→回滚，TypeScript，18★。
8. **新项目 AIDE**（5月2日）：AI agent 递归自我改进框架，agent 住进自己的源码中持续优化，TypeScript，9★。

---

## 🚀 项目速递

### 1. OpenAI Agents Python — v0.15.1
- **链接**: https://github.com/openai/openai-agents-python/releases/tag/v0.15.1
- **发布日期**: 2026-05-02
- **核心更新**:
  - 🆕 暴露 Responses WebSocket keepalive 配置选项
  - 🐛 修复 UnixLocal PTY 子进程 SIGINT 信号默认值恢复（#3082, #3074）
  - 📝 改善 Windows 用户快速入门文档
  - 🧪 Guardrail name fallback 测试覆盖

### 2. ElizaOS — v2.0.0-alpha.535
- **链接**: https://github.com/elizaOS/eliza/releases/tag/v2.0.0-alpha.535
- **发布日期**: 2026-05-02
- **核心更新**:
  - 🔄 高频 alpha 迭代（526→535，3天9个版本）
  - 🆕 plugin-n8n-workflow vendor 化（非 submodule 管理）
  - 📦 依赖批量更新（form-data, @walletconnect/logger 等）
  - ⚠️ v2.0.0 正式版信号渐强

### 3. Pydantic AI — v1.89.1
- **链接**: https://github.com/pydantic/pydantic-ai/releases/tag/v1.89.1
- **发布日期**: 2026-05-01
- **核心更新**:
  - 🆕 集成 Library Skills（library-skills.io）增强 coding-agent 体验
  - 🐛 修复 ToolManager function-tool 方法 `wrap_validation_errors` 丢失
  - 🐛 修复 `anyio.Lock` 事件循环绑定（延迟创建 via `cached_property`）

### 4. LangGraph — 1.2.0a5
- **链接**: https://github.com/langchain-ai/langgraph/releases/tag/1.2.0a5
- **发布日期**: 2026-05-01
- **核心更新**:
  - 🐛 修复 `_messages_delta_reducer` 中 dict/str 写入的类型强制转换（#7680）
  - 📦 prebuilt 同步升级至 1.1.0a2（ToolCallTransformer namespace 隔离）

### 5. crewAI — 1.14.5a1
- **链接**: https://github.com/crewAIInc/crewAI/releases/tag/1.14.5a1
- **发布日期**: 2026-05-01
- **核心更新**:
  - 🆕 `restore_from_state_id` kickoff 参数（状态恢复）
  - 🆕 ExaSearchTool 重命名 + highlights 功能
  - 🐛 修复 skills loading events for traces

### 6. Agno — v2.6.4
- **链接**: https://github.com/agno-agi/agno/releases/tag/v2.6.4
- **发布日期**: 2026-04-28
- **核心更新**:
  - 🆕 WikiContextProvider：filesystem + git 后端，web ingestion，read/write flags
  - 🆕 WorkspaceContextProvider（v2.6.3）：项目级上下文，排除 .context/.venv 等 agent 噪声

### 7. BlameBot（新项目）
- **链接**: https://github.com/huseynovvusal/blamebot
- **创建日期**: 2026-05-02
- **简介**: AI on-call agent，自动检测部署失败 → 解释故障原因 → 分页通知责任团队 → 自动回滚。TypeScript，18★。

### 8. AIDE（新项目）
- **链接**: https://github.com/hibbault/aide
- **创建日期**: 2026-05-02
- **简介**: AI agent 递归自我改进框架——agent 住进自己的源码中，持续迭代优化自身代码。TypeScript，9★。

### 9. OpenPawlet（持续活跃）
- **链接**: https://github.com/JackLuguibin/OpenPawlet
- **简介**: 单进程 agent runtime + HTTP API + 浏览器 UI + OpenAI 兼容 /v1/* 接口。Python，101★，37 forks。

### 10. Continuo（新项目）
- **链接**: https://github.com/getcontinuo/continuo
- **创建日期**: 2026-04-15
- **简介**: 跨 agent 记忆联邦（Cross-agent memory federation），基于 recognition-first 运行时模型。MCP 兼容，local-first。

---

## 💡 对我工作的启发

1. **Coding Agent 生态加速**：Pydantic AI 集成 Library Skills——coding agent 正从"能用"走向"好用"，对推理加速场景下的 agent 开发工具链选型有参考价值。
2. **MCP 工具集成成标配**：crewAI You.com MCP 工具、Continuo MCP 兼容——MCP 协议正在成为 agent 外部能力接入的事实标准，后续做 agent 工具层设计时应优先考虑 MCP 兼容。
3. **Agent 自我改进范式**：AIDE 展示了 agent 递归自我改进的可能性，虽然尚处早期，但方向值得关注——推理加速框架本身能否 self-tune？
4. **WebSocket 长连接优化**：OpenAI Agents SDK 暴露 keepalive 配置——推理加速场景下 agent-to-model 的长连接稳定性值得关注。
5. **On-call Agent 自动化**：BlameBot 将 agent 引入 SRE/on-call 流程（检测→解释→通知→回滚），与推理服务的运维自动化方向契合。
6. **ElizaOS 2.0 临近**：高频 alpha 迭代 + plugin vendor 化，区块链/Crypto agent 框架的成熟度在快速提升。

---

## 📋 明日跟踪建议

1. **LangGraph 1.2.0 正式版**：当前 alpha5，关注是否本周发布 stable，重点看消息 reducer 变更对现有 graph 的影响。
2. **ElizaOS v2.0.0 正式版**：alpha 版本号已到 535，关注是否本周发布正式版。
3. **Pydantic AI Library Skills 深度**：library-skills.io 具体提供了哪些技能包，对 coding agent 的能力边界有多大提升。
4. **AIDE 自我改进机制**：关注该项目的 agent 自修改架构细节，评估其安全性和实用性。
5. **Agno ContextProvider 体系**：WikiContextProvider + WorkspaceContextProvider 的组合对 agent 长期上下文管理有何启发。

---

*报告生成时间：2026-05-03 13:50 CST*
