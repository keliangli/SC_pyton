# GitHub 智能体日报 — 2026-05-15

---

## 📌 今日要点

1. **Pydantic-AI v1.96.1 发布，V2 架构预告**：废弃 `Agent` 构造器旧参数，引入 `PrepareTools` / `PrepareOutputTools` / `ProcessEventStream` 能力模型，V2 预计六月落地。
2. **Claude Code v2.1.142 密集更新**：`claude agents` 新增 `--add-dir` / `--model` / `--permission-mode` 等 flag 配置后台会话；Fast Mode 默认升级到 Opus 4.7；Plugin SKILL.md 自动发现。
3. **LangGraph 1.2.0 正式版**：新增 durable error-handler 跨崩溃恢复、`set_node_defaults()`、Delta Channel 快照强制刷新，checkpoint 层面健壮性大幅提升。
4. **Mastra 1.33.0 — Push PubSub + ResponseCache**：workflow 事件支持 HTTP push 推送（GCP Pub/Sub / SNS / EventBridge），新增 `ResponseCache` 可跳过相同 LLM 步骤的重复调用。
5. **Hermes Agent ACP Registry 切换到 uvx 分发**：放弃 npm launcher，支持 Zed 编辑器 ACP 元数据注册，ACP 生态在多编辑器间加速统一。
6. **OpenAI Agents Python v0.17.2**：修复 Conversations reasoning 持久化、realtime tools 未知工具自动响应、tracing 重试退避等问题。
7. **Mem0 CLI v0.2.5**：新增 `mem0 init --agent` 一键生成未绑定密钥、`--agent-caller` 自声明身份、Plugin 自动同步。

---

## 🚀 项目速递

### 框架 & 平台

| 项目 | 版本 | 日期 | 核心变更 | 链接 |
|------|------|------|----------|------|
| Pydantic-AI | v1.96.1 | 05-15 | V2 预备：废弃旧 Agent 参数，引入能力模型；修复 OpenAI 模型兼容 | [GitHub](https://github.com/pydantic/pydantic-ai) |
| LangGraph | 1.2.0 | 05-12 | durable error-handler、set_node_defaults()、Delta Channel 快照 | [GitHub](https://github.com/langchain-ai/langgraph) |
| LangChain | 1.3.0 | 05-12 | stream_events / astream_events v3 支持 | [GitHub](https://github.com/langchain-ai/langchain) |
| Mastra | @mastra/core@1.33.0 | 05-13 | Push PubSub + HTTP workflow 事件；ResponseCache 跳过重复 LLM 调用 | [GitHub](https://github.com/mastra-ai/mastra) |
| Dify | 1.14.1 | 05-12 | SECRET_KEY 硬化、workflow 稳定性、自部署清理 | [GitHub](https://github.com/langgenius/dify) |
| CrewAI | 1.14.5a5 | 05-12 | 废弃 CrewAgentExecutor，默认 AgentExecutor；Daytona sandbox 改进 | [GitHub](https://github.com/crewAIInc/crewAI) |
| OpenAI Agents Python | v0.17.2 | 05-12 | 修复 reasoning 持久化、realtime tools、tracing 重试 | [GitHub](https://github.com/openai/openai-agents-python) |

### Agent 工具 & 编辑器集成

| 项目 | 版本 | 日期 | 核心变更 | 链接 |
|------|------|------|----------|------|
| Claude Code | v2.1.142 | 05-14 | agents 后台会话配置 flag；Opus 4.7 Fast Mode；Plugin SKILL.md 发现 | [GitHub](https://github.com/anthropics/claude-code) |
| Gemini CLI | v0.44.0-nightly | 05-15 | RAG snippets 本地调试日志；ACP auth 企业网关修复；NO_PROXY 支持 | [GitHub](https://github.com/google-gemini/gemini-cli) |
| Hermes Agent | ACP Registry 更新 | 05-15 | uvx 分发替代 npm；Zed ACP 注册；移除 Atropos RL | [GitHub](https://github.com/NousResearch/hermes-agent) |
| Mem0 CLI | v0.2.5 | 05-14 | Agent Mode 快速初始化；自声明身份；Plugin 自动同步 | [GitHub](https://github.com/mem0ai/mem0) |

### 新星项目

| 项目 | ⭐ | 日期 | 简介 | 链接 |
|------|------|------|------|------|
| agent-study | 90 | 05-14 | 28 章 AI Agent 全栈课程：ReAct → MCP/A2A → DSPy → 可观测性，全可运行 Python | [GitHub](https://github.com/Callous-0923/agent-study) |
| SDAR | 33 | 05-14 | Self-Distilled Agentic Reinforcement Learning（浙大）| [GitHub](https://github.com/ZJU-REAL/SDAR) |
| llm-anr | 13 | 05-14 | Agent 驱动的 Android ANR 证据提取与 AI 辅助根因分析 | [GitHub](https://github.com/yuchuangu85/llm-anr) |

### 值得关注的活跃提交

| 项目 | 提交 | 说明 |
|------|------|------|
| Deer Flow (字节) | `fix(memory): isolate queued memory updates by agent` | 多 agent 记忆隔离 |
| Deer Flow (字节) | `fix(runtime): avoid postgres aggregate row lock` | PG 运行时锁优化 |

---

## 💡 对我工作的启发

1. **Pydantic-AI V2 能力模型值得关注**：从构造器参数迁移到 `Capability` 模式，和 vLLM/SGLang 的 plugin 体系思路一致——用声明式能力代替命令式配置。做推理加速框架时，也该考虑类似模式。
2. **LangGraph durable error-handler**：跨崩溃恢复对长时 agent workflow 极其关键。推理服务同样需要 checkpoint 级别的容错——可参考 LangGraph 的实现思路（delta channel + superstep 快照）。
3. **Mastra ResponseCache**：用缓存跳过相同 LLM 步骤，核心是"幂等推理"思路。在推理加速场景中，prefix caching / KV cache 复用本质上是一类问题，Mastra 的 per-step cache key 设计值得参考。
4. **Claude Code agents 配置增强**：`claude agents` 新增 `--permission-mode` / `--model` flag，说明 sub-agent 调度正在走向精细化权限控制。这与 OpenClaw ACP 的 `permission-mode` 理念一致，后续可对比实现。
5. **Hermes Agent uvx 分发**：从 npm 切到 uvx，说明 Python 生态的 agent 工具链正在收敛到 uv/uvx 分发模式，值得跟踪工具链简化趋势。
6. **SDAR（浙大）**：Self-Distilled Agentic RL 是"智能体自蒸馏强化学习"，与推理加速的 RLHF/GRPO 训练加速有交叉，后续可深入看论文。

---

## 📋 明日跟踪建议

1. **Pydantic-AI V2 alpha**：关注 V2 正式 preview 分支，能力模型 API 可能成为 Python agent 框架新范式。
2. **Claude Code v2.1.143+**：`claude agents` 后台会话仍在快速迭代，跟踪权限模型和 sub-agent orchestration 的进展。
3. **Mastra Slack Channel**：1.31.0 已支持 Slack channel，后续可关注 Teams / Discord 等 channel 扩展。
4. **SDAR 论文**：等代码完善后复现核心实验，评估对 RL 训练加速的参考价值。
5. **LangGraph Delta Channel**：beta 标记的 API 变化频繁，关注 checkpoint 压缩与快照策略的后续演进。

---

> 报告生成时间：2026-05-15 13:50 CST  
> 数据来源：GitHub API（releases / commits / search）
