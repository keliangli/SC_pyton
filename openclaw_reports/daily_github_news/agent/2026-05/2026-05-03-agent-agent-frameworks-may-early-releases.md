# GitHub 智能体日报 — 2026-05-03

> 数据窗口：2026-04-29 ~ 2026-05-02（过去 ~72h 内发布的 release/重要更新）

---

## 📌 今日要点

1. **OpenAI Agents SDK v0.15.1** 发布（5月2日）：新增 Responses WebSocket keepalive 配置，修复 UnixLocal PTY 子进程信号处理，改善 Windows 快速入门文档。
2. **Claude Code v2.1.126** 发布（5月1日）：重大更新——模型选择器支持自定义 gateway 的 `/v1/models`；新增 `claude project purge` 命令；WSL2/SSH 下 OAuth 码可终端粘贴；PowerShell 优先 shell 支持；移除 Read 工具的恶意软件误报提醒。
3. **Pydantic AI v1.89.1** 发布（5月1日）：集成 Library Skills（library-skills.io）增强 coding-agent 能力；修复 ToolManager 校验和 anyio.Lock 事件循环绑定问题。
4. **LangGraph 1.2.0a5** alpha 发布（5月1日）：修复 `_messages_delta_reducer` 中 dict/str 写入的类型强制转换。
5. **crewAI 1.14.4** 发布（4月30日）：重要功能更新——Azure OpenAI Responses API 支持、Vertex AI workload identity、Tavily Research 工具、You.com MCP 工具；修复 litellm SSTI 安全漏洞。
6. **AutoGPT platform beta v0.6.58** 发布（4月29日）：动态 COST_USD 计费、Settings V2 全套页面、Claude Opus 4.7 模型支持、Web Push 通知（VAPID）、Redis Cluster 支持、Discord Copilot bot。

---

## 🚀 项目速递

### 1. OpenAI Agents Python — v0.15.1
- **链接**: https://github.com/openai/openai-agents-python/releases/tag/v0.15.1
- **发布日期**: 2026-05-02
- **核心更新**:
  - 🆕 暴露 Responses WebSocket keepalive 配置选项
  - 🐛 修复 UnixLocal PTY 子进程 SIGINT 信号默认值恢复
  - 📝 改善 Windows 用户快速入门文档
  - 🧪 Guardrail name fallback 测试覆盖

### 2. Claude Code — v2.1.126
- **链接**: https://github.com/anthropics/claude-code/releases/tag/v2.1.126
- **发布日期**: 2026-05-01
- **核心更新**:
  - 🆕 `/model` 选择器支持自定义 gateway 的 `/v1/models` 端点
  - 🆕 `claude project purge` 命令（支持 `--dry-run`、`-y`、`-i`、`--all`）
  - 🆕 `--dangerously-skip-permissions` 扩展至 `.claude/`、`.git/`、`.vscode/` 等路径
  - 🆕 WSL2/SSH/容器场景下 OAuth 码可终端粘贴
  - 🆕 `claude_code.skill_activated` OpenTelemetry 事件（含 `invocation_trigger` 属性）
  - 🆕 Windows PowerShell 7 检测 & PowerShell 优先 shell
  - 🗑️ 移除 Read 工具的恶意软件误报提醒
  - 🔧 Auto mode 权限阻塞时 spinner 变红

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
  - 🐛 修复 `_messages_delta_reducer` 中 dict/str 写入的类型强制转换
  - 📦 Alpha 阶段，prebuilt 同步升级至 1.1.0a2

### 5. crewAI — 1.14.4
- **链接**: https://github.com/crewAIInc/crewAI/releases/tag/1.14.4
- **发布日期**: 2026-04-30
- **核心更新**:
  - 🆕 Azure OpenAI Responses API 支持
  - 🆕 Vertex AI workload identity 配置指南
  - 🆕 Tavily Research & Get Research 工具
  - 🆕 You.com MCP 工具（搜索、研究、内容提取）
  - 🆕 自定义 persistence key（`@persist`）
  - 🐛 修复 litellm SSTI 漏洞 + 忽略不可修复 pip CVE
  - 🐛 修复 JSON regex 解析、tool_calls 保留、MCP server 空工具返回等 10+ 项

### 6. AutoGPT Platform — beta v0.6.58
- **链接**: https://github.com/Significant-Gravitas/AutoGPT/releases/tag/autogpt-platform-beta-v0.6.58
- **发布日期**: 2026-04-29
- **核心更新**:
  - 🆕 动态 BlockCostType（SECOND/ITEMS/COST_USD/TOKENS）+ E2B/FAL 迁移
  - 🆕 MAX 订阅层 + LD 可配置定价 + 动态 COST_USD 计费
  - 🆕 Settings V2（API Keys / Integrations / Profile / Preferences / Creator Dashboard）
  - 🆕 Claude Opus 4.7 模型支持
  - 🆕 Web Push 通知（VAPID）后台推送
  - 🆕 Redis Cluster 客户端支持
  - 🆕 Discord Copilot Bot（Python / discord.py）
  - 🆕 Inline picker-backed inputs via run_block

---

## 💡 对我工作的启发

1. **Coding Agent 生态加速**：Pydantic AI 集成 Library Skills、Claude Code 大幅增强 WSL/SSH 体验——coding agent 正从"能用"走向"好用"，对推理加速场景下的 agent 开发工具链选型有参考价值。
2. **MCP 工具集成成标配**：crewAI 新增 You.com MCP 工具、Tavily Research——MCP 协议正在成为 agent 外部能力接入的事实标准，后续做 agent 工具层设计时应优先考虑 MCP 兼容。
3. **计费 & 限流模型精细化**：AutoGPT 动态 COST_USD + 8 处计费泄漏修复 + 限流乘数可配置——多租户 agent 平台的计费基础设施正在成熟，对自建 agent 服务有借鉴意义。
4. **WebSocket 长连接优化**：OpenAI Agents SDK 暴露 keepalive 配置——推理加速场景下 agent-to-model 的长连接稳定性值得关注。
5. **PTY/Shell 信号处理**：OpenAI Agents SDK 修复 SIGINT 默认值、Claude Code PowerShell 优先——agent 操控终端/Shell 的信号处理细节正在被主流框架重视，自定义 agent 运行时需注意此类边界。

---

## 📋 明日跟踪建议

1. **LangGraph 1.2.0 正式版**：当前为 alpha5，关注是否在本周发布 stable，重点看消息 reducer 的变更对现有 graph 的影响。
2. **Pydantic AI Library Skills 深度**：library-skills.io 具体提供了哪些技能包，对 coding agent 的能力边界有多大提升。
3. **Claude Code 自定义 gateway 模型**：`/v1/models` 端点接入后，自部署模型（如 vLLM/SGLang 后端）与 Claude Code 的集成路径是否通畅。
4. **crewAI MCP 生态扩展**：You.com MCP 工具的实际效果，以及后续是否会有更多第三方 MCP server 集成。
5. **AutoGPT 计费基础设施**：动态 COST_USD 模型的具体实现方式，对开源 agent 平台的商业化路径参考。

---

*报告生成时间：2026-05-03 11:47 CST*
