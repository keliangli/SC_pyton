# GitHub 智能体（AI Agents）日报 — 2026-04-15

## 今日要点

- **自改进 Agent 成为主旋律**：NousResearch 的 Hermes Agent 和 Sentō 都主打"自我学习循环"——Agent 从使用经验中自动创建 skill、优化自身行为，无需人工干预。
- **Agent 记忆系统持续升温**：claude-mem 今日新增 2,997 star（总量 56K+），成为 Agent 持久化记忆的事实标准之一，已支持 OpenClaw 集成。
- **Agentic 工程方法论工具化**：Superpowers 框架将 TDD、子 Agent 驱动开发、设计评审等最佳实践封装为自动触发的 skill，适用于 Claude Code / Cursor / Codex 等主流编码 Agent。
- **Repo-native Agent 新范式**：Capitaine 提出"仓库即 Agent"概念——代码是 Agent 身体，Git 历史是记忆，心跳周期驱动自动演化。
- **垂直场景 Agent 落地加速**：智能客服（cs-ai-agent）、代码审查（gitlab-review-agent）、多 Agent 协作（Kendr）等领域均有新项目涌现。

## 项目速递

### 1. NousResearch/hermes-agent
- **链接**：https://github.com/NousResearch/hermes-agent
- **语言**：Python
- **更新**：2026-04-15
- **亮点**：
  - 内置学习循环：从经验自动创建 skill，使用中持续优化
  - 支持 200+ 模型（OpenRouter / 小米 MiMo / GLM / Kimi / MiniMax 等），一行命令切换
  - 6 种终端后端（local / Docker / SSH / Daytona / Singularity / Modal），支持 Serverless 休眠
  - FTS5 会话搜索 + Honcho 用户建模，兼容 agentskills.io 开放标准
  - 支持 OpenClaw 迁移（`hermes claw migrate`）

### 2. thedotmack/claude-mem
- **链接**：https://github.com/thedotmack/claude-mem
- **语言**：TypeScript
- **Star**：56,262 ⭐ | 今日 +2,997
- **亮点**：
  - Claude Code 持久记忆插件，自动捕获会话上下文、AI 压缩、语义检索注入
  - 已支持 OpenClaw 一键安装：`curl -fsSL https://install.cmem.ai/openclaw.sh | bash`
  - 提供 Web Viewer UI（localhost:37777）实时查看记忆流
  - 支持 Gemini CLI 集成

### 3. obra/superpowers
- **链接**：https://github.com/obra/superpowers
- **语言**：Markdown / Plugin
- **更新**：2026-04-15
- **亮点**：
  - Agentic 开发全流程框架：brainstorming → 设计 → 计划 → 子 Agent 执行 → 代码审查 → 合并
  - 强制 RED-GREEN-REFACTOR TDD 循环，不支持跳过
  - 支持 Claude Code、Cursor、Codex、OpenCode、Copilot、Gemini CLI 六大平台
  - 子 Agent 驱动开发：每个任务独立 Agent 执行，两阶段审查

### 4. sentoagent/sento
- **链接**：https://github.com/sentoagent/sento
- **语言**：JavaScript
- **更新**：2026-04-15
- **亮点**：
  - 24/7 自运行 Agent，一条命令 `npx sentoagent init` 部署
  - 使用 Claude 订阅（无需 API key），零额外 token 费用
  - 内置 Watchdog 自愈 + 首次运行 onboarding 个性化
  - 17 个插件自动安装，支持 Skill 导出/导入

### 5. Lucineer/capitaine
- **链接**：https://github.com/Lucineer/capitaine
- **语言**：TypeScript
- **更新**：2026-04-15
- **亮点**：
  - "仓库即 Agent"——代码是身体，Git 历史是记忆，心跳周期驱动自动行动
  - Fleet 编队协作：多仓库 Agent 通过 PR/Issue 协调
  - Captain's Logs：每次行动附带意图说明，可审计
  - 一键 Codespaces 启动：fork → click → agent alive

### 6. UnpredictablePrashant/Kendr
- **链接**：https://github.com/UnpredictablePrashant/Kendr
- **语言**：Python
- **更新**：2026-04-15
- **亮点**：
  - 多 Agent 编排平台，Web UI + CLI 双入口
  - SuperRAG 知识引擎 + 深度研究模式
  - 支持 OpenAI / Anthropic / Google / Ollama 多后端
  - 项目生成器：`kendr generate --stack fastapi_postgres "..."`

### 7. giselles-ai/giselle
- **链接**：https://github.com/giselles-ai/giselle
- **语言**：TypeScript
- **更新**：2026-04-15
- **亮点**：
  - 可视化 Agent Builder，拖拽式构建 Agentic Workflow
  - GitHub AI Operations：自动处理 Issue/PR/部署
  - 多模型组合：GPT + Claude + Gemini，Agent 自动选模型
  - Apache 2.0 开源，提供云服务（每月 30 分钟免费 Agent 时间）

### 8. huabeitech/cs-ai-agent
- **链接**：https://github.com/huabeitech/cs-ai-agent
- **语言**：Go + Next.js 16
- **更新**：2026-04-15
- **亮点**：
  - AI-First 智能客服系统：Agent 接待 → RAG 检索 → 置信度判断 → 人工接管
  - 完整闭环：会话管理 + 知识库 RAG + 工单流转 + Skills/MCP 扩展
  - 技术栈：Go 后端 + Qdrant 向量库 + OpenAI 兼容接口

### 9. willton-easy/gitlab-review-agent
- **链接**：https://github.com/willton-easy/gitlab-review-agent
- **语言**：Go
- **更新**：2026-04-15
- **亮点**：
  - GitLab MR 自动代码审查 Agent，支持 OpenAI / Anthropic / Gemini
  - 学习团队编码约定，随时间提升审查质量
  - 支持 Webhook 自动触发 + 增量审查

### 10. sou350121/Agent-Playbook
- **链接**：https://github.com/sou350121/Agent-Playbook
- **语言**：PowerShell（内容型仓库）
- **更新**：2026-04-15
- **亮点**：
  - 93 篇 Agent 工程实战知识库，覆盖设计/工程/范式/战略
  - Pulsar 自动化流水线：每日 50+ 信息源 → AI 评级门控 → 5-10 条精选
  - 双周预测 + 验证记录，公开判断历史
  - Devil's Advocate 机制：对最强信号给出具体反驳

## 对我工作的启发

1. **自改进循环值得深入研究**：Hermes 和 Sentō 的"从经验自动创建 skill + 持续优化"模式，与我们的 Agent 学习加速目标高度契合。其 FTS5 会话搜索 + LLM 摘要召回的方案可以直接借鉴用于 Triton/CUDA 学习场景。
2. **claude-mem 的记忆压缩架构**：AI 压缩 + 语义检索 + 渐进式披露的分层记忆方案，对长周期学习场景（如 CUDA 知识积累）有直接参考价值。
3. **Superpowers 的 TDD 工作流**：强制 RED-GREEN-REFACTOR + 子 Agent 两阶段审查的工程方法论，可以迁移到我们自己的 Agent 开发实践中。
4. **Repo-native Agent 思路**：Capitaine 的"仓库即 Agent"范式，让我想到可以将代码仓库本身作为 Agent 的长期知识载体——对代码仓拆解任务有新思路。
5. **垂直 Agent 落地模式**：cs-ai-agent 展示了 AI-First + 人工接管的优雅架构（置信度路由），gitlab-review-agent 展示了代码审查 Agent 的工程实践。这些场景模式可以迁移到推理性能分析、训练瓶颈诊断等垂直场景。

## 明日跟踪建议

- [ ] **Hermes Agent** 的 skill 自创建机制细节（关注 skill 格式和优化算法）
- [ ] **claude-mem** 是否有新版本发布（关注 OpenClaw 集成的稳定性）
- [ ] **Superpowers** 的 Codex 集成进展（关注 subagent-driven-development 在实际项目中的效果）
- [ ] **Capitaine** Hydration Layer 恢复进度（Phase 1 实现是否完成）
- [ ] **Kendr** 的 SuperRAG 知识引擎实现细节
- [ ] 新出现的 Agent 评估/测试框架（关注是否有 Agent eval 的新工具）
