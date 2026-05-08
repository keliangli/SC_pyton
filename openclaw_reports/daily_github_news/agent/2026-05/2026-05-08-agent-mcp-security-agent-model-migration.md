# GitHub 智能体日报 — 2026-05-08

> 数据窗口：2026-05-07 06:00 UTC ~ 2026-05-08 06:00 UTC

---

## 今日要点

1. **OpenAI Agents SDK v0.16.0/0.16.1 双版本连发** — 默认模型切换至 gpt-5.4-mini，新增 MCP server 前缀工具名、工具并发执行配置、`max_turns=None` 无限轮次选项
2. **Pydantic AI v1.91.0 → v1.92.0 24h 内双更** — 新增 Anthropic task budget、DeepSeek V4 支持、gpt-image-2 选项；修复 MCP 会话和流式取消问题
3. **Mastra v1.32.0 引入细粒度授权（FGA）** — 关系型资源级权限控制在 agent 运行、工具执行、MCP 全链路生效
4. **MCPGuard 新项目首日上线** — MCP 工具调用前安全校验 CLI，覆盖 schema、运行时行为、超时、密钥泄露
5. **HeyGen HyperFrames 连续三日高频迭代** — HTML→Video 的 Agent 原生渲染方案，v0.5.0→v0.5.3

---

## 项目速递

### 🔥 重大更新

| 项目 | 版本 | 日期 | 要点 | 链接 |
|------|------|------|------|------|
| openai/openai-agents-python | v0.16.0 + v0.16.1 | 05-07 | 默认模型 gpt-5.4-mini；MCP 工具名前缀防冲突；工具并发执行配置；max_turns=None 无限轮次 | [GitHub](https://github.com/openai/openai-agents-python) |
| pydantic/pydantic-ai | v1.91.0 / v1.92.0 | 05-07/08 | Anthropic task budget；DeepSeek V4 Flash/Pro；gpt-image-2；运行时 output_retries 覆写；流式取消修复；MCP 会话修复 | [GitHub](https://github.com/pydantic/pydantic-ai) |
| mastra-ai/mastra | @mastra/core@1.32.0 | 05-06 | FGA 细粒度授权（agent 运行/工具/MCP 全链路）；WorkOS FGA Provider | [GitHub](https://github.com/mastra-ai/mastra) |
| langchain-ai/langchain | 0.3.30 | 05-07 | loads/dumps 安全加固；hub 模块废弃 | [GitHub](https://github.com/langchain-ai/langchain) |
| langchain-ai/langgraph | cli==0.4.25 | 05-07 | 新增 Studio Deploy 支持 | [GitHub](https://github.com/langchain-ai/langgraph) |
| gptme/gptme | v0.31.1.dev20260507 | 05-07 | gh issue/pr 列表预览；ephemeral_ttl 上下文剪枝；Android CI 构建 | [GitHub](https://github.com/gptme/gptme) |

### 🆕 新项目 / 新星

| 项目 | ⭐ | 日期 | 要点 | 链接 |
|------|-----|------|------|------|
| hieuchaydi/MCPGuard | 8 | 05-08 | MCP 工具调用前安全校验 CLI：schema 质量、运行时行为、超时、密钥泄露检测 | [GitHub](https://github.com/hieuchaydi/MCPGuard) |
| heygen-com/hyperframes | 15.9k | 持续 | HTML→Video，Agent 原生视频渲染框架，v0.5.0→v0.5.3 高频迭代 | [GitHub](https://github.com/heygen-com/hyperframes) |
| eriknewton/sanctuary-framework | 5 | 03-22 | 智能体经济主权开放标准，四层架构保护人类与自治代理 | [GitHub](https://github.com/eriknewton/sanctuary-framework) |

### 📡 活跃迭代

| 项目 | 版本 | 日期 | 要点 | 链接 |
|------|------|------|------|------|
| crewAIInc/crewAI | 1.14.5a3 | 05-06 | CLI 独立为 crewai-cli；gitpython 安全升级 | [GitHub](https://github.com/crewAIInc/crewAI) |
| livekit/agents | 1.5.8 | 05-05 | Voice Agent 打断冷却窗口；AMD 改进；AWS 流式就绪修复 | [GitHub](https://github.com/livekit/agents) |
| elizaOS/eliza | — | 05-07 | 持续活跃：workflow bun install 修复、systemd PrivateTmp 安全加固 | [GitHub](https://github.com/elizaOS/eliza) |
| camel-ai/camel | v0.2.91a4 | 04-30 | Anthropic thinking 支持；GPT 5.5 适配 | [GitHub](https://github.com/camel-ai/camel) |

---

## 对我工作的启发

1. **MCP 安全成为刚需** — MCPGuard 的出现说明 MCP 生态已大到需要专门做调用前安全校验。当前 OpenClaw 的 MCP 集成可参考其 schema 校验 + 超时 + 密钥泄露检测思路，加固 mcporter 调用链。
2. **Agent 框架默认模型快速迁移** — OpenAI Agents SDK 默认模型从 gpt-4.1 切到 gpt-5.4-mini，说明推理成本优化已是框架级决策。对 vLLM/SGLang 部署而言，mini 模型的推理优化路径（稀疏化、投机解码）值得关注。
3. **FGA 细粒度授权模式** — Mastra 的 FGA 实现值得关注，resource-level + relationship-based 的权限模型对多租户 Agent 平台很有参考价值。
4. **HTML→Video Agent 原生渲染** — HeyGen HyperFrames 把视频生成变成了"写 HTML 就行"，降低了 Agent 产出视频的门槛，未来 Agent 报告/演示的形态可能从 Markdown 演进到 HTML+Video。
5. **上下文剪枝成为标配** — gptme 的 ephemeral_ttl + cache boundary optimization 和 OpenAI Agents SDK 的 session history compaction 都指向同一趋势：长对话 Agent 的上下文管理正在从简单截断演进到语义感知剪枝。

---

## 明日跟踪建议

1. **OpenAI Agents SDK** — 关注 v0.16.x 后续 patch 是否引入更多 MCP 安全相关功能（require_approval 策略校验刚修了 bug）
2. **Pydantic AI** — v1.92.0 刚加入 Anthropic task budget，观察社区反馈和后续是否扩展到其他 provider
3. **MCPGuard** — 首日项目，跟踪其 schema 校验和密钥泄露检测的具体实现，评估是否可集成到 mcporter
4. **HyperFrames** — 高频迭代中，关注其 Agent 集成 API 的稳定性
5. **Mastra FGA** — 细粒度授权刚落地，跟踪其在生产环境的实际效果和社区反馈
6. **gptme** — ephemeral_ttl 机制值得深入研究，可能对 OpenClaw 的会话管理有启发

---

*报告生成时间：2026-05-08 13:50 CST*
