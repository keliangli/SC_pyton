# GitHub 智能体日报 — 2026-05-09

> 抓取时间：2026-05-09 13:50 CST | 覆盖范围：过去 24h 内有实质技术更新的 AI Agent 项目

---

## 📌 今日要点

1. **OpenAI Agents SDK v0.17.0** — RealtimeAgent 默认升级到 `gpt-realtime-2`，同时收紧沙箱本地源物化安全边界
2. **Pydantic AI 三连发 (v1.91→v1.93)** — 3 天 3 个版本，新增 `tool_choice`、Anthropic task budget、gpt-image-2 / DeepSeek V4 支持，多项 MCP / 流式取消修复
3. **Google ADK v1.33.0** — 新增 `BufferableSessionService`、Apigee 凭证注入、adk web 热重载，A2A 元数据重构
4. **MCP Python SDK v1.27.1** — 修复 Pydantic 2.13 兼容性 + OAuth 空字符串问题
5. **Claude Code v2.1.136** — 修复 MCP 服务器 `/clear` 后消失、OAuth refresh token 竞态，新增 `worktree.baseRef` 与 `hard_deny` 规则
6. **OpenAI Codex v0.130.0** — 新增 `codex remote-control` 入口、插件 hooks 共享、Bedrock 认证、线程分页

---

## 🚀 项目速递

### 1. [openai/openai-agents-python](https://github.com/openai/openai-agents-python) — v0.17.0 (2026-05-08)

| 变更 | 详情 |
|------|------|
| 🆕 RealtimeAgent 默认模型 | 从 `gpt-realtime` 升级为 `gpt-realtime-2` |
| 🔒 沙箱安全收紧 | `LocalFile.src`/`LocalDir.src` 默认限定在 `base_dir` 内，超出需 `SandboxPathGrant` 授权 |
| 🐛 修复 | Responses 上下文管理 `extra_args` 冲突 |
| 📝 迁移注意 | 若应用曾从 base_dir 外拷贝可信文件进沙箱，需显式添加 `extra_path_grants` |

---

### 2. [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) — v1.91.0 → v1.93.0 (2026-05-07~09)

**v1.93.0:**
- 🆕 `tool_choice` 设置项，支持控制模型工具选择策略
- 🆕 `OutputToolCallEvent`/`OutputToolResultEvent` 事件输出
- 🐛 修复 agent 取消时 spawned tasks 未 drain

**v1.92.0:**
- 🆕 Anthropic task budget 支持（token 预算控制）
- 🆕 运行时 `output_retries` 覆盖 + 废弃 `retries` 字段
- 🐛 流式响应取消清理、MCP 会话专用 task 修复、eval teardown 保证

**v1.91.0:**
- 🆕 `gpt-image-2` 选项支持、`deepseek-v4-flash` / `deepseek-v4-pro` 模型接入
- 🐛 OpenAI 空 `ModelResponse` 映射修复、MCP 历史 replay 空 tool arguments 修复

---

### 3. [google/adk-python](https://github.com/google/adk-python) — v1.33.0 (2026-05-08)

| 变更 | 详情 |
|------|------|
| 🆕 BufferableSessionService | 可缓冲的会话服务，优化多轮对话状态管理 |
| 🆕 Apigee 凭证注入 | 支持将 Apigee 凭证注入 ApigeeLlm |
| 🆕 环境工具截断限制可配 | ADK environment tools truncation limit 可配置 |
| 🆕 LlmResponse 扩展 | 新增 `get_function_calls` / `get_function_responses` |
| 🔧 adk web 热重载 | 修改 agent 后无需重启 |
| 🔧 A2A 元数据 | `a2a_metadata` 字符串提取为常量，便于扩展 |
| 🐛 多项修复 | sandbox 缺失错误捕获、video inline data 过滤、BigQuery fork 检测、state_delta 覆盖、asyncio 阻塞等 |

---

### 4. [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) — v1.27.1 (2026-05-08)

- 🐛 Pydantic 2.13 兼容性修复（`PydanticUserError` 捕获）
- 🐛 OAuth 空字符串可选 URL 字段 coerce 为 None
- 🔧 限制 `httpx < 1.0.0`
- 🔧 SSEError 从 `httpx_sse` 公共 API 导入

---

### 5. [anthropics/claude-code](https://github.com/anthropics/claude-code) — v2.1.136~137 (2026-05-08~09)

- 🐛 **重要**：MCP 服务器在 `.mcp.json` / 插件 / claude.ai connectors 中配置后 `/clear` 不再消失
- 🐛 **重要**：多个远程 MCP 服务器并发刷新 OAuth token 不再丢失，无需每日重认证
- 🆕 `worktree.baseRef` 设置（`fresh` | `head`），控制 worktree 分支基点
- 🆕 `autoMode.hard_deny` — 无条件阻止的自动模式规则
- 🆕 Hooks 接收 `effort.level` 输入 / `$CLAUDE_EFFORT` 环境变量
- 🐛 WSL2 图片粘贴、并行会话 401 竞态等修复

---

### 6. [openai/codex](https://github.com/openai/codex) — v0.130.0 (2026-05-08)

- 🆕 `codex remote-control` 命令 — 更简单的无头远程控制入口
- 🆕 插件详情展示 bundled hooks + 共享元数据
- 🆕 App-server 线程分页（unloaded/summary/full turn views）
- 🆕 Bedrock 认证支持 `aws login` profile
- 🐛 Live app-server 线程热更新配置、apply-patch diff 准确性、compaction 修复等

---

### 7. [Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) — v0.6.59 (2026-05-07)

- 🆕 Settings v2 billing 页（订阅 + 自动化积分）
- 🆕 基于层级的文件存储限制
- 🆕 SDK 动态 `max_budget_usd` + 基线预算提示
- 🆕 `get_platform_info` 工具（tier-aware AutoPilot）
- 🆕 年度 Stripe 计费

---

### 8. [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) — v0.0.75 (2026-05-07)

- 🐛 `--isolated` 模式下共享浏览器启动序列化
- 🐛 Extension 模式下浏览器级 CDP 命令转发

---

### 9. [agentscope-ai/QwenPaw](https://github.com/agentscope-ai/QwenPaw) — v1.1.6-beta.1 (2026-05-08)

- 🆕 语音输入从 Web Speech API 替换为 Whisper 转录
- 🆕 火山引擎 (Volcengine) provider
- 🆕 Token 使用趋势可视化
- 🆕 批量启用/禁用技能
- 🆕 GPT Image 2 工具插件

---

### 10. [langchain-ai/langchain](https://github.com/langchain-ai/langchain) — v1.2.18 (2026-05-08)

- 🔧 Agent `ls_agent_type` tag on `create_agent` calls（后回退）
- 🔧 `langchain-core 0.3.86` 修复路径遍历安全漏洞 (CVE-2026-34070)
- 🔧 v1.3.0a2 预览：`stream_events(v3)` 协议、HITL middleware `respond` 决策

---

## 💡 对我工作的启发

1. **沙箱安全是趋势**：OpenAI Agents SDK 收紧本地文件物化边界 → 自研 agent 框架应尽早考虑 artifact 隔离与显式授权模型
2. **task budget 走向标配**：Pydantic AI 引入 Anthropic task budget → 推理加速方向可关注 token 预算与延迟/吞吐的联合优化
3. **MCP 生态持续成熟**：Claude Code 修复 MCP 服务器生命周期问题 + Python SDK 兼容性修复 → MCP 作为 agent 工具层标准地位更稳固，值得持续跟踪
4. **DeepSeek V4 已进主流框架**：Pydantic AI 同步支持 deepseek-v4-flash/pro → 国产模型在 agent 框架中的适配度快速提升
5. **热重载成为刚需**：Google ADK adk web 热重载、Codex app-server 线程热更新 → agent 开发调试体验在快速迭代
6. **remote-control / headless 模式**：Codex 新增 `remote-control` → agent 编排场景中无头控制需求增长，与 ACP 协议方向一致

---

## 📋 明日跟踪建议

| 项目 | 关注点 |
|------|--------|
| Pydantic AI | v1.93.0 刚发布，`tool_choice` 实际使用体验 + 后续 MCP 改进 |
| Google ADK | `BufferableSessionService` 实现细节 + A2A 元数据扩展方向 |
| Claude Code | `hard_deny` 规则 + effort level hooks 的实际安全效果 |
| OpenAI Codex | `remote-control` 协议细节，是否可被第三方 agent 编排复用 |
| AutoGPT | v0.6.59 billing 体系变化对开源自部署的影响 |
| LangChain | v1.3.0a2 的 `stream_events(v3)` 进展 |

---

*报告自动生成 by OpenClaw · 数据来源：GitHub API*
