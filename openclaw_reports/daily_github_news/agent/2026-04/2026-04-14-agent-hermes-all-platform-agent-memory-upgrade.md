---
title: "GitHub 智能体日报（2026-04-14）- Hermes全平台+Mem0 v2+Agno llms.txt"
date: 2026-04-14
track: 智能体
slug: hermes-all-platform-agent-memory-upgrade
source_report: /home/li/.openclaw/workspace/reports/github_agent_news_2026-04-14.md
repo_path: openclaw_reports/daily_github_news/agent/2026-04/2026-04-14-agent-hermes-all-platform-agent-memory-upgrade.md
generated_by: openclaw
---

# GitHub 智能体日报 — 2026-04-14

---

## 📌 今日要点

| # | 要点 | 来源 |
|---|------|------|
| 1 | **Hermes Agent v0.9.0 发布** — 全平台大版本：新增本地 Web Dashboard、WeChat/WeCom/iMessage 接入、Android Termux 原生支持、Fast Mode 低延迟推理、后台进程监控，487 commits、24 贡献者 | NousResearch/hermes-agent |
| 2 | **Mem0 v2.0.0 Beta 发布** — Agent 记忆层大版本重构，移除大量废弃 API，修复 LLM 幻觉 ID 导致的崩溃 | mem0ai/mem0 |
| 3 | **Agno v2.5.16 发布** — 新增 llms.txt 标准支持、Salesforce CRM 工具、Azure AI Foundry Claude Provider、OpenAI Responses API 后台模式 | agno-agi/agno |
| 4 | **LangGraph 1.1.7a1 发布** — 新增 graph lifecycle callback handler、CLI validate 命令 | langchain-ai/langgraph |
| 5 | **ByteDance DeerFlow 持续迭代** — 修复 todo-middleware 提前退出问题，memory updater 迁移到 async LLM 调用 | bytedance/deer-flow |

---

## 🚀 项目速递

### 1. NousResearch/hermes-agent — v0.9.0 (2026-04-13)
- **Stars:** ★79,519
- **链接:** https://github.com/NousResearch/hermes-agent
- **核心更新:**
  - 🔥 **Local Web Dashboard** — 浏览器端本地管理面板，无需终端操作
  - ⚡ **Fast Mode (`/fast`)** — OpenAI GPT-5.4 / Codex / Claude 优先队列低延迟路由
  - 📱 **Termux/Android 原生支持** — 移动端直接运行 Hermes
  - 💬 **WeChat & WeCom 接入** — 通过 iLink Bot API 实现微信/企业微信原生集成
  - 🍎 **iMessage via BlueBubbles** — Apple 消息生态打通
  - 🔍 **Background Process Monitoring** — 后台进程输出模式匹配实时通知
  - 🤖 **原生 xAI (Grok) & Xiaomi MiMo Provider** — 新增两大模型提供商
- **规模:** 487 commits · 269 PRs · 167 issues · 63,281 行变更

### 2. mem0ai/mem0 — v2.0.0b0 (2026-04-13)
- **Stars:** ★52,969
- **链接:** https://github.com/mem0ai/mem0
- **核心更新:**
  - 💥 **Breaking Changes:** 移除废弃的 `enable_graph` 参数及 LLM/embeddings/vector stores 相关旧接口
  - 🐛 修复 LLM 幻觉 ID 导致的 `temp_uuid_mapping` 崩溃 (#4674)
  - 🔧 Azure OpenAI `response_format` 转发修复，支持结构化输出
  - 📊 遥测采样率降至 10% 降低 PostHog 负载

### 3. agno-agi/agno — v2.5.16 (2026-04-10)
- **Stars:** ★39,407
- **链接:** https://github.com/agno-agi/agno
- **核心更新:**
  - 📄 **LLMsTxtTools / LLMsTxtReader** — 支持 [llms.txt](https://llmstxt.org/) 标准，为 Agent 提供 LLM 友好的文档索引
  - 🏢 **SalesforceTools** — 新增 Salesforce CRM 集成工具
  - ☁️ **Azure AI Foundry Claude Provider** — 新增模型提供商
  - 🔄 **OpenAI Responses API 后台模式** — 支持异步后台处理
  - 🐛 修复 AGUI reasoning 事件、TeamSession 反序列化、workflow 图片路径等问题

### 4. langchain-ai/langgraph — 1.1.7a1 (2026-04-10)
- **Stars:** ★29,181
- **链接:** https://github.com/langchain-ai/langgraph
- **核心更新:**
  - 🔌 **Graph Lifecycle Callback Handlers** — 图生命周期回调
  - ✅ **CLI validate 命令** — 部署前配置校验
  - 🐛 修复 `assistant_id` 从 config configurable 填充问题

### 5. code-yeongyu/oh-my-openagent — v3.17.2 (2026-04-13)
- **Stars:** ★51,363
- **链接:** https://github.com/code-yeongyu/oh-my-openagent
- **核心更新:** 兼容性修复和稳定性加固，包检测与插件配置适配更新

### 6. crewAIInc/crewAI — 1.14.2a3 (2026-04-13)
- **Stars:** ★48,822
- **链接:** https://github.com/crewAIInc/crewAI
- **核心更新:** 最新 alpha 版本发布

### 7. bytedance/deer-flow — 活跃开发中
- **Stars:** ★61,252
- **链接:** https://github.com/bytedance/deer-flow
- **核心更新 (2026-04-14 commits):**
  - 🐛 修复 todo-middleware 导致 Agent 在 todo 未完成时提前退出
  - ⚡ Memory Updater 迁移到 async LLM 调用，提升并发性能
  - 🔧 修复 mounted sandbox providers 的文件上传问题

### 8. saltbo/agent-kanban — 快速增长中
- **Stars:** ★188
- **链接:** https://github.com/saltbo/agent-kanban
- **简介:** Agent-First 任务看板，AI 工作力的任务管控中心
- **近期更新:** Daemon 全生命周期 smoke test、worktree 保留逻辑修复

---

## 💡 对我工作的启发

1. **Agent 全平台部署已成趋势** — Hermes 同时覆盖 Android/iMessage/WeChat/WeCom，说明 Agent 不再限于 Web/CLI，而是向全渠道渗透。对于推理加速工作，需要关注跨端推理的性能优化（移动端量化、延迟敏感场景）。
2. **Agent 记忆层进入 2.0 时代** — Mem0 v2.0 Beta 标志着 Agent 记忆系统从实验走向工程化，移除废弃 API 暗示 API 稳定性需求上升。RAG + Agent Memory 的结合值得关注。
3. **llms.txt 标准化值得关注** — Agno 新增 llms.txt 支持，为 Agent 提供标准化的文档索引方式。这对 Agent 工具调用和知识获取的工程化有直接参考价值。
4. **DeerFlow 的 async LLM 调用迁移** — 字节跳动将 memory updater 迁移到异步 LLM 调用，说明多 Agent 系统中并发 LLM 调用已成为性能瓶颈之一，与推理加速方向高度相关。
5. **Agent 任务编排工具成熟** — agent-kanban 这类 Agent-first 任务看板的出现，说明多 Agent 编排的工程管理需求在上升。

---

## 📋 明日跟踪建议

| 优先级 | 项目 | 跟踪理由 |
|--------|------|----------|
| ⭐⭐⭐ | Hermes Agent v0.9.0 后续 | 首个同时打通微信 + iMessage 的开源 Agent，用户增长和社区反馈值得持续跟踪 |
| ⭐⭐⭐ | Mem0 v2.0 正式版进展 | Beta 发布后正式版可能很快，关注 API 稳定性和 Graph Memory 能力 |
| ⭐⭐ | Agno OpenAI Responses 后台模式 | 异步 Agent 工作流模式可能成为主流范式 |
| ⭐⭐ | DeerFlow async LLM 迁移 | 跟踪字节在多 Agent 并发推理上的工程实践 |
| ⭐ | crewAI 1.14.x 稳定版 | Alpha 版密集发布，稳定版可能近期落地 |
| ⭐ | agent-kanban 功能演进 | Agent 任务编排赛道的早期项目 |

---

*报告生成时间: 2026-04-14 13:50 CST*
*数据来源: GitHub API (repositories, releases, commits)*
