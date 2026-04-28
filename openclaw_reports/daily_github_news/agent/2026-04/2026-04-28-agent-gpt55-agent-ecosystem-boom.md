# GitHub 智能体日报（2026-04-28）

> 统计时段：2026-04-27 ~ 2026-04-28（UTC+8）

## 📌 今日要点

1. **GPT-5.5 全面渗透智能体生态** — LangChain、LlamaIndex、Hermes Agent 三大框架同步支持 GPT-5.5，标志着推理模型正式进入 Agent 主流工具链。
2. **Agno 24 小时内双发版（v2.6.2 → v2.6.3）** — 新增 Workspace 工具集 + HITL 确认门、WorkspaceContextProvider，本地 Agent 工具链日臻完善。
3. **LangGraph 三件套更新** — v1.1.10 支持 ToolNode 返回 `list[Command | ToolMessage]`，Agent 图编排灵活性大幅提升。
4. **Agent 安全成焦点** — Deer Flow 集中修复沙箱逃逸漏洞；Agno 为 Workspace 破坏性操作加 HITL 门。
5. **MCP 生态持续扩展** — Google MCP Toolbox 新增 Cloud Storage 工具、CrewAI 接入 You.com + Tavily MCP。

---

## 🚀 项目速递

### 1. Agno v2.6.2 → v2.6.3 ⭐ 新发版

**仓库**: [agno-agi/agno](https://github.com/agno-agi/agno)  
**更新**: v2.6.2 (Apr 27) → v2.6.3 (Apr 28)

**v2.6.2 亮点**:
- 🛠 **Workspace Tools**: 本地文件系统工具集（read/list/search/write/edit/move/delete/shell），破坏性操作默认带 HITL 确认门
- 🔄 多个模型 provider 默认 ID 迁移到最新模型，避免弃用

**v2.6.3 亮点**:
- 📁 **WorkspaceContextProvider**: 项目感知的上下文提供器，中央排除模式（.context、.venvs 等）
- 💬 SlackContextProvider 简化，新增 `enable_workspace_search` 参数

### 2. LangGraph v1.1.10 + prebuilt v1.0.12 + checkpoint v4.0.3

**仓库**: [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)  
**更新**: 2026-04-27 三包齐发

- ✨ **feat(prebuilt)**: ToolNode tools 可返回 `list[Command | ToolMessage]`，支持单工具调用产出多个下游消息/命令
- 🩹 **fix(checkpoint)**: 恢复 lc=2 JSON blob 兼容性
- 🔄 Node-level timeouts（已 revert，等待更稳定方案）

### 3. Hermes Agent v0.11.0「The Interface Release」

**仓库**: [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)  
**发布**: 2026-04-23（v0.9.0 以来累计 1556 commits / 761 merged PRs）

- 🖥 **全新 Ink-based TUI**: React/Ink 重写交互式 CLI，含 Python JSON-RPC 后端
- 🔌 **Transport ABC + AWS Bedrock**: 可插拔传输层抽象，原生 Bedrock Converse API
- 🧠 **GPT-5.5 via Codex OAuth**: 实时模型发现，无需手动更新 catalog
- 🐧 **QQBot**: 第 17 个消息平台，QR 扫码配置
- 🎛 **/steer**: 运行时注入提示指导正在运行的 Agent，不中断 turn
- 🔗 **Shell hooks**: 无需写 Python 插件即可挂载生命周期钩子
- 🏗 **Smarter delegation**: Subagent 支持 orchestrator 角色 + 可配置 spawn 深度

### 4. LangChain — GPT-5.5 + content-block 流式

**仓库**: [langchain-ai/langchain](https://github.com/langchain-ai/langchain)  
**近期发布**: langchain-core v1.3.2, langchain-openai v1.2.1

- 🧠 **GPT-5.5 Pro** 支持加入 Responses API
- 📡 **Content-block-centric streaming (v2)**: 新版流式架构，以内容块为粒度
- ⚡ **perf**: 停止将 agent 状态内联到 tool-dispatch `Send` 消息中，减少 token 开销

### 5. CrewAI — MCP 工具扩展

**仓库**: [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)  
**更新**: 2026-04-27

- 🔍 新增 [You.com MCP](https://you.com) 工具支持（搜索、研究、内容提取）
- 🔬 新增 Tavily Research 集成

### 6. Deer Flow — 安全加固

**仓库**: [bytedance/deer-flow](https://github.com/bytedance/deer-flow)  
**更新**: 2026-04-28

- 🛡 修复沙箱 host bash 遍历逃逸、本地自定义挂载符号链接逃逸
- 🔍 新增 skill 归档文件安装前扫描
- 🔒 容器日志中敏感环境变量值脱敏

### 7. LlamaIndex — GPT-5.5 模型支持

**仓库**: [run-llama/llama_index](https://github.com/run-llama/llama_index)  
**更新**: 2026-04-27

- 🧠 新增 GPT-5.5 / GPT-5.5-2026-04-23 模型支持
- 🩹 修复 Google GenAI streaming 时 thought output 输出问题

### 8. Google MCP Toolbox — Cloud Storage 工具

**仓库**: [googleapis/mcp-toolbox](https://github.com/googleapis/mcp-toolbox)  
**更新**: 2026-04-28

- ☁️ 新增 Cloud Storage bucket 和 object 管理工具
- 📐 Prebuilt config 格式扁平化

### 9. Page Agent v1.8.1

**仓库**: [alibaba/page-agent](https://github.com/alibaba/page-agent)  
**更新**: 2026-04-27

- 🧠 支持 GPT-5.4 模型，刷新模型推荐列表

### 10. LobeHub — 模型扩展

**仓库**: [lobehub/lobehub](https://github.com/lobehub/lobehub)  
**更新**: 2026-04-28

- 🎨 新增 GPT-image-2 和 Grok 4.20 模型支持

---

## 💡 对我工作的启发

| 方向 | 启发 |
|------|------|
| **GPT-5.5 推理模型集成** | 各框架几乎同时适配 GPT-5.5，说明推理模型对 Agent 的收益已被广泛认可。建议评估 GPT-5.5 在推理加速场景下的 Agent 任务表现（特别是复杂多步推理），对比 GPT-5 的延迟/成本/准确率。 |
| **Agent 安全工程** | Deer Flow 和 Agno 同时聚焦安全——沙箱逃逸修复、HITL 确认门。对于生产 Agent 部署，安全机制不再是可选项。可参考 Agno 的 Workspace HITL 门设计思路。 |
| **MCP 工具生态加速** | Google（Cloud Storage）、CrewAI（You.com + Tavily）、Agno（Parallel MCP）都在快速接入 MCP。MCP 已成为 Agent 工具互联的事实标准，建议关注 MCP server 开发与性能优化机会。 |
| **LangGraph ToolNode 增强** | ToolNode 支持返回 `list[Command | ToolMessage]` 意味着单工具调用可触发多分支图执行，Agent 工作流编排从「线性」走向「扇出」。可用于推理 pipeline 的并行化设计。 |
| **Agent 传输层抽象化** | Hermes Agent 的 Transport ABC 设计（Anthropic/ChatCompletions/ResponsesAPI/Bedrock 各自独立）值得参考——在推理加速场景中，类似的多后端抽象可降低切换成本。 |

---

## 📅 明日跟踪建议

- [ ] **GPT-5.5 在 Agent 场景的 benchmark 数据** — 关注各框架是否发布对比评测
- [ ] **Agno Workspace Tools HITL 机制** — 深入研究其确认门实现，评估可否迁移到推理工作流
- [ ] **LangChain content-block streaming v2** — 新的流式 API 设计对 Agent 实时交互的影响
- [ ] **MCP Toolbox Cloud Storage** — 关注 GCP 场景的 Agent 数据管道集成模式
- [ ] **Deer Flow 安全修复细节** — 沙箱逃逸修复方案是否有通用参考价值

---

> 📊 数据来源: GitHub API / Releases / Commits | 生成时间: 2026-04-28 13:50 CST
