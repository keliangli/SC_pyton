# GitHub 智能体日报（2026-05-11）

## 今日要点

1. **Hermes Agent v0.13.0 发布** — "The Tenacity Release"，864 commits 大版本，核心推出多 Agent Kanban 看板（含心跳/僵尸检测/幻觉门控）和 /goal 持续目标锁定机制
2. **OpenAI Agents SDK v0.17.0** — RealtimeAgent 默认模型升级为 gpt-realtime-2，沙箱本地源物化安全边界收紧
3. **CopilotKit v1.57.1** — 新增 React Native 支持，推出 registerProxiedAgent 前端工具挂载模式
4. **Agno v2.6.5** — Gemini 多模态文件搜索、Gmail/Calendar 上下文提供者、Mongo 调度器，修复 MCP IDOR 跨租户漏洞
5. **Mem0 v2.0.2** — SQL 注入 + 提示注入加固，新增 decay 参数暴露和搜索决策透传

## 项目速递

### 1. NousResearch/hermes-agent — v0.13.0 (The Tenacity Release)
- 🔗 https://github.com/NousResearch/hermes-agent/releases/tag/v2026.5.7
- **多 Agent Kanban 看板**：多 worker 拾取任务、心跳检测、僵尸回收、重试预算、幻觉门控
- **/goal 命令**：跨轮次锁定目标（Ralph Loop），防止 Agent 偏离任务
- **video_analyze 工具**：原生视频理解（Gemini 及兼容多模态模型）
- **xAI Custom Voices**：语音克隆 TTS 提供者
- **7 语种 i18n**：中文/日文/德文/西班牙文/法文/乌克兰文/土耳其文
- **安全加固**：8 个 P0 修复，默认开启脱敏，Discord 角色白名单改为 guild 级，WhatsApp 默认拒绝陌生人
- **Google Chat** 成为第 20 个支持平台
- 864 commits / 588 PRs / 829 files changed / 295 社区贡献者

### 2. openai/openai-agents-python — v0.17.0
- 🔗 https://github.com/openai/openai-agents-python/releases/tag/v0.17.0
- **RealtimeAgent 默认模型升级**：gpt-realtime-2（原 gpt-realtime）
- **沙箱安全边界收紧**：LocalFile.src / LocalDir.src 限制在 base_dir 内，需显式 SandboxPathGrant 授权外部路径
- 影响：此前依赖沙箱读取宿主外部文件的应用需迁移

### 3. CopilotKit/CopilotKit — v1.57.1
- 🔗 https://github.com/CopilotKit/CopilotKit/releases/tag/v1.57.1
- **@copilotkit/react-native**：全新包，支持 React Native 应用使用 CopilotKit hooks
  - 轻量 CopilotKitProvider（无 DOM/CSS/Radix 依赖）
  - installStreamingFetch() XHR shim + ReadableStream/TextEncoder 等 polyfill
- **registerProxiedAgent**：前端工具/上下文挂载到单个 runtime agent
- **MCP Server per-call getHeaders**：BuiltInAgent 的 MCP 配置支持每次调用动态解析 headers

### 4. agno-agi/agno — v2.6.5
- 🔗 https://github.com/agno-agi/agno/releases/tag/v2.6.5
- **Gemini 多模态文件搜索**：支持图片上传 + File Search API（google-genai≥1.75.0）
- **GmailContextProvider / CalendarContextProvider**：新增 OAuth 支持的上下文提供者
- **Mongo/AsyncMongo 调度器**：AgentOS 支持 cron 定时运行 Agent/Team/Workflow
- **Workflow Condition on_error**：条件步骤支持错误处理控制
- **MCP IDOR 修复**：绑定 user_id 到 JWT subject，防止跨租户读写

### 5. mem0ai/mem0 — v2.0.2 (Python) / ts-v3.0.3 (Node)
- 🔗 https://github.com/mem0ai/mem0/releases/tag/v2.0.2
- **安全加固**：SQL 注入 + 提示注入防护
- **project.update 暴露 decay 参数**：可控制记忆衰减
- **搜索决策透传**：将 mem0 的搜索决策信息传递给调用 Agent

### 6. browser-use/browser-use — v0.12.6
- 🔗 https://github.com/browser-use/browser-use/releases/tag/0.12.6
- Gemini-3 默认 temperature 设为 1.0
- Bedrock structured output schema 扁平化修复
- 修复 daemon 孤儿进程（外部浏览器断开时）
- 修复 httpx client 连接池未关闭导致 Lambda OOM
- MCP browser_click schema 修复（移除 oneOf，兼容 Claude API）
- 修复超时后 history 残留和步骤计数卡住

### 7. crewAIInc/crewAI — v1.14.5a4 (Pre-release)
- 🔗 https://github.com/crewAIInc/crewAI/releases/tag/1.14.5a3
- CLI 独立为 crewai-cli 包
- 修复异步批量刷新时 task output 丢失
- 修复 shared LLM stop words 跨 Agent 污染
- gitpython 依赖升级 ≥3.1.47（安全合规）

### 8. langchain-ai/langgraph — cli==0.4.25 / sdk==0.3.14
- 🔗 https://github.com/langchain-ai/langgraph/releases
- **CLI 支持 Studio Deploy**：新增 langgraph studio deploy 命令
- SDK 常规版本更新

## 对我工作的启发

1. **多 Agent 编排是主战场**：Hermes 的 Kanban + /goal + Checkpoints v2 体系，说明"多 Agent 协作 + 持久状态 + 自动恢复"正在成为 Agent 框架的标配能力。我们的推理加速工作可关注多 Agent 场景下的调度开销优化。

2. **安全从"可选项"变成"必选项"**：Hermes 8 个 P0 安全修复 + 默认脱敏、Agno MCP IDOR 修复、Mem0 SQL/提示注入加固、OpenAI 沙箱边界收紧 —— 本周安全议题集中爆发，说明 Agent 系统在接入真实环境后安全风险正在被系统性暴露。

3. **跨平台扩展加速**：CopilotKit 进 React Native、Hermes 加 Google Chat（第 20 平台）、Agno 加 Gmail/Calendar —— Agent 框架都在往"无处不在"方向走，推理引擎需要适配更多异构部署场景。

4. **记忆系统成熟化**：Mem0 的 decay 参数暴露和搜索决策透传，说明 Agent 记忆从"存取"走向"可控衰减 + 可解释检索"，对长对话推理优化有参考价值。

## 明日跟踪建议

- [ ] 关注 Hermes v0.13.0 的 Kanban 看板在实际场景中的性能开销（864 commits 的大型重构）
- [ ] 跟踪 OpenAI Agents SDK gpt-realtime-2 的延迟和吞吐基准数据
- [ ] 观察 CopilotKit React Native 在移动端 Agent 场景的落地反馈
- [ ] 持续关注 Agno v2.6.5 的 MCP IDOR 修复是否引发其他框架跟进审计
- [ ] 检查 CrewAI v1.14.5 正式版是否发布（当前仍为 alpha）
