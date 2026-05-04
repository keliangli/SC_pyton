# GitHub 智能体日报 — 2026-05-04

> 数据窗口：2026-05-03 ~ 2026-05-04 UTC
> 数据源：GitHub API（Releases + Commits）
> 赛道：智能体（AI Agents）

---

## 今日要点

1. **OpenAI Codex v0.128.0 引入持久化 Goal 工作流 + MultiAgentV2 配置**：新增 `/goal` 持久化工作流（创建/暂停/恢复/清除）、MultiAgentV2 线程上限与深度控制、插件市场安装与外部 Agent 会话导入。这是 Codex 从单次对话 Agent 向「长期目标驱动 + 多 Agent 协作」演进的关键版本。
2. **Dify v1.14.0 上线实时协作编辑 + HITL API**：工作流多人实时协同编辑（WebSocket 同步）、Human-in-the-Loop Service API 支持程序化调用、MCP 工具元数据刷新与 OAuth 修复。Dify 正在从「个人低代码平台」走向「团队协作式 Agent 编排」。
3. **Hermes Agent v0.12.0「Curator」发布**：自治后台 Curator 自动评估/裁剪/整合技能库（7 天周期），自改进循环从自由格式升级为分类优先的评分体系，新增 4 个推理 Provider + Spotify/Google Meet 原生集成，ComfyUI 转为默认捆绑。这是 Agent 自我管理能力的质变。
4. **Claude Code v2.1.126 增强网关兼容与 WSL2 体验**：`/model` 支持读取网关 `/v1/models`、WSL2/SSH 下 OAuth 码粘贴登录、PowerShell 7 检测与作为主 Shell、`claude project purge` 一键清理、`--dangerously-skip-permissions` 扩展白名单。
5. **CrewAI 1.14.4 支持 Azure OpenAI Responses API + MCP 工具扩展**：Azure OpenAI Responses API 适配、`@persist` 自定义持久化 Key、You.com MCP 搜索/研究工具、Tavily Research 工具、Vertex AI Workload Identity 集成指南。

---

## 项目速递

### 1. OpenAI Codex — v0.128.0 (2026-04-30) / v0.129.0-alpha.2 (2026-05-01)

| 维度 | 内容 |
|------|------|
| 仓库 | [openai/codex](https://github.com/openai/codex) ⭐ 79.8K |
| 核心更新 | 持久化 `/goal` 工作流（创建/暂停/恢复/清除）；MultiAgentV2 线程上限 + 深度控制；插件市场安装 + 远程缓存；外部 Agent 会话导入；`codex update` 命令；权限 Profile 内置默认值 + 沙箱 CLI 选择 |
| 最新 Commit | `[codex] Emit MCP tool calls as turn items` (#20677, 2026-05-04)；`Refactor app-server dispatch result flow` (#20897, 2026-05-04) |
| 技术亮点 | Goal 工作流实现了 Agent 从「单轮对话」到「长期目标追踪」的跨越；MultiAgentV2 的 thread caps + depth 控制让多 Agent 编排更可控 |

### 2. Dify — v1.14.0 (2026-04-29)

| 维度 | 内容 |
|------|------|
| 仓库 | [langgenius/dify](https://github.com/langgenius/dify) ⭐ 140K |
| 核心更新 | 工作流实时协作编辑（WebSocket 同步 + 在线状态）；HITL Service API（程序化人工审核）；MCP 工具元数据刷新与 OAuth 修复；共享 UI 组件包 `@langgenius/dify-ui`；Goto Anything 快速导航 |
| 最新 Commit | `fix: IDOR on console GET /account/avatar` (#35771, 2026-05-03) |
| 技术亮点 | 协作模式让 Agent 编排从单人低代码走向团队实时协同；HITL API 打通程序化人工审核链路 |

### 3. Hermes Agent — v0.12.0 (2026-04-30)

| 维度 | 内容 |
|------|------|
| 仓库 | [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) ⭐ 131.5K |
| 核心更新 | 自治 Curator（后台评估/裁剪/整合技能库，7 天周期）；自改进循环升级为分类优先评分体系；4 个新推理 Provider；Spotify + Google Meet 原生集成；ComfyUI / TouchDesigner-MCP 转为默认捆绑；TUI 冷启动优化 ~57% |
| 最新 Commit | `feat(docker): launch dashboard as side-process via HERMES_DASHBOARD=1` (#19540, 2026-05-04)；`fix_docker_tui` (#19520, 2026-05-04) |
| 技术亮点 | Curator 是 Agent 自我管理能力的质变——Agent 能自动维护自己的技能库，这是走向自进化的重要一步 |

### 4. Claude Code — v2.1.126 (2026-05-01)

| 维度 | 内容 |
|------|------|
| 仓库 | [anthropics/claude-code](https://github.com/anthropics/claude-code) ⭐ 120K |
| 核心更新 | `/model` 读取网关 `/v1/models`；`claude project purge` 一键清理；WSL2/SSH 下 OAuth 码粘贴登录；PowerShell 7 检测与主 Shell 切换；`--dangerously-skip-permissions` 扩展白名单；OpenTelemetry skill_activated 事件 |
| 技术亮点 | 网关模型列表发现是自定义部署场景的刚需；WSL2 OAuth 改善极大提升了边缘开发体验 |

### 5. CrewAI — v1.14.4 (2026-04-30) / v1.14.5a1 (2026-05-01)

| 维度 | 内容 |
|------|------|
| 仓库 | [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) ⭐ 50.5K |
| 核心更新 | Azure OpenAI Responses API 适配；`@persist` 自定义持久化 Key；You.com MCP 搜索/研究工具；Tavily Research 工具；Vertex AI Workload Identity 指南；`restore_from_state_id` 参数 |
| 最新 Commit | `fix: handle BaseModel input in convert_to_model` (2026-05-03) |
| 技术亮点 | Azure OpenAI Responses API 支持补齐了企业级部署的模型适配短板 |

### 6. LangChain — v1.0.5 (2026-05-03) / LangGraph v1.2.0a5 (2026-05-01)

| 维度 | 内容 |
|------|------|
| 仓库 | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) ⭐ 135.7K / [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) |
| 核心更新 | langchain-classic 1.0.5：deprecation 路径重定向至 `create_agent`；langchain-anthropic 1.4.3；LangGraph 1.2.0a5：修复 `_messages_delta_reducer` 对 dict/str 写入的强制转换 |
| 技术亮点 | `create_agent` 成为 LangChain 的统一 Agent 入口点，deprecation 路径明确指向 Agent 化架构 |

---

## 对我工作的启发

1. **Goal 工作流 → 推理加速场景的长期任务编排**：Codex 的持久化 Goal 思路可借鉴到 vLLM/SGLang 的推理 Pipeline 中——将「预热 → 调度 → 批处理 → 回收」拆为可暂停/恢复的 Goal 状态机，对长推理任务和弹性调度有实际价值。
2. **Agent 自我管理（Curator）→ 推理引擎自调优**：Hermes Agent 的 Curator 模式启发思考：推理加速引擎是否也可以有「自治调优器」——后台周期性评估 Kernel 选择、Batch 策略、KV Cache 命中率，自动裁剪低效配置。
3. **Dify 协作 + HITL → 模型评测工作流**：Dify 的实时协作 + 程序化 HITL 可以作为推理性能评测的编排底座——团队协同设计 Benchmark，HITL 接管异常结果审核。
4. **CrewAI MCP 工具链 → Agent 工具调用优化**：CrewAI 集成 You.com/Tavily MCP 工具说明 MCP 正在成为 Agent 工具调用的标准协议层，对理解 Agent 调用链路的性能瓶颈（工具选择延迟、序列化开销）有参考价值。
5. **LangChain `create_agent` 统一入口 → Agent API 标准化**：LangChain 将 deprecation 路径指向 `create_agent`，Agent 化架构成为共识，后续可关注 `create_agent` 的性能特征（延迟、开销）作为 Agent 框架选型依据。

---

## 明日跟踪建议

1. **OpenAI Codex v0.129.0 正式版**：当前为 alpha.2，关注 MultiAgentV2 的线程模型与调度策略细节。
2. **Hermes Agent Docker 集成**：今日已有 `HERMES_DASHBOARD=1` 的 side-process 提交，关注 Docker 部署体验完善。
3. **LangGraph 1.2.0 正式版**：当前为 a5，关注 `_messages_delta_reducer` 修复后的流式消息稳定性。
4. **Google Gemini CLI v0.41.0**：preview.1 已发，关注正式版的功能更新。
5. **Claude Code 网关兼容性进展**：v2.1.126 新增 `/v1/models` 发现，关注后续对自定义推理后端（vLLM 等）的兼容增强。

---

*本报告由 OpenClaw 自动生成 | GitHub API 数据*
