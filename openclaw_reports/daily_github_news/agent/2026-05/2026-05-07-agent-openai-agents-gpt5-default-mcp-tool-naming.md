# GitHub 智能体日报 — 2026-05-07

## 今日要点

1. **OpenAI Agents SDK v0.16.0 发布**：默认模型切换为 `gpt-5.4-mini`，新增函数工具并发控制配置、MCP 工具名服务端前缀防冲突、`max_turns=None` 无限轮次支持
2. **Pydantic-AI v1.91.0 发布**：新增 DeepSeek v4（flash/pro）模型支持、gpt-image-2 图像选项，修复 MCP 历史回放问题
3. **Chrome DevTools MCP v0.25.0 发布**：支持第三方开发者工具扩展，修复原生 select 控件交互超时
4. **LangGraph 1.2.0 alpha 持续推进**：新增 DeltaChannel（增量通道）降低长线程 checkpoint 开销，流式 API v3 支持
5. **CrewAI 1.14.5 alpha 连续迭代**：CLI 独立为 crewai-cli 包，修复任务输出恢复与 LLM stop words 共享突变问题
6. **Hermes Agent v0.12.0（4/30）**：自治 Curator 后台 agent 自动评分/裁剪/整合技能库，自改进循环大幅升级

---

## 项目速递

### 1. OpenAI Agents Python — v0.16.0
- **发布日期**：2026-05-07
- **核心变更**：
  - 默认模型从 `gpt-4.1` → `gpt-5.4-mini`（含 GPT-5 默认 reasoning.effort="none"、verbosity="low"）
  - 新增 `ToolExecutionConfig(max_function_tool_concurrency=...)` 本地函数工具并发控制
  - 新增 `mcp_config={"include_server_in_tool_names": True}` MCP 服务端工具名前缀防冲突
  - 新增 `max_turns=None` 支持禁用轮次限制
  - 修复：chat completions tool call 输出索引稳定化、symlink 安全加固
- **链接**：https://github.com/openai/openai-agents-python/releases/tag/v0.16.0

### 2. Pydantic-AI — v1.91.0
- **发布日期**：2026-05-07
- **核心变更**：
  - 新增 `deepseek-v4-flash` 和 `deepseek-v4-pro` 模型支持
  - 新增 OpenAI `gpt-image-2` 图像选项
  - 修复：MCP history replay 空 tool arguments 崩溃、Unicode YAML 数据集兼容性
- **链接**：https://github.com/pydantic/pydantic-ai/releases/tag/v1.91.0

### 3. Chrome DevTools MCP — v0.25.0
- **发布日期**：2026-05-06
- **核心变更**：
  - 支持第三方开发者工具扩展（agent 可调用非 Chrome 内置的 DevTools）
  - 修复原生 select 选项点击超时、环境变量解析不一致
- **链接**：https://github.com/ChromeDevTools/chrome-devtools-mcp/releases/tag/chrome-devtools-mcp-v0.25.0

### 4. LangGraph — 1.2.0a6/1.2.0a7
- **发布日期**：2026-05-04~05
- **核心变更**：
  - **DeltaChannel（beta）**：增量通道类型，仅存储增量 delta，大幅降低长运行线程的 checkpoint 开销
  - 流式 API v3：content-block-centric，per-channel typed projections
  - SDK 0.3.14：新增 `return_minimal` threads update 选项
  - ToolNode 工具可返回 `list[Command | ToolMessage]`
- **链接**：https://github.com/langchain-ai/langgraph/releases

### 5. CrewAI — 1.14.5a1~a3
- **发布日期**：2026-05-01~06
- **核心变更**：
  - CLI 独立为 `crewai-cli` 包（解耦主框架与命令行）
  - 新增 `restore_from_state_id` kickoff 参数
  - 修复：task output 在 finally block 中丢失、LLM stop words 跨 agent 共享突变、async 路径中 `acall` 输出转换
  - gitpython 安全依赖升级 ≥3.1.47
- **链接**：https://github.com/crewAIInc/crewAI/releases

### 6. Hermes Agent — v0.12.0
- **发布日期**：2026-04-30
- **核心变更**：
  - **自治 Curator**：后台 agent 自动评分/整合/裁剪技能库（7 天周期），比人工维护更持续
  - 自改进循环升级为 class-first rubric-based，active-update biased
  - ComfyUI v5 + TouchDesigner-MCP 内置化
  - TUI 冷启动时间减少 ~57%
  - 4 个新推理 provider、第 18/19 个消息平台
- **链接**：https://github.com/NousResearch/hermes-agent/releases/tag/v2026.4.30

### 7. Dify — v1.14.0 + 活跃开发
- **发布日期**：2026-04-29（release）/ 2026-05-07（持续提交）
- **核心变更**：
  - 协作编辑模式：多人同时编辑同一 workflow，实时同步
  - 今日提交：dify-ui autocomplete/combobox 组件、dev-proxy 包初始化、KB metadata filter 修复
- **链接**：https://github.com/langgenius/dify/releases/tag/1.14.0

### 8. Google ADK Python — v1.32.0
- **发布日期**：2026-04-30
- **核心变更**：
  - 原生 OpenTelemetry agentic metrics + tracing
  - Anthropic thinking blocks 支持
  - MCP credential_key 自定义、GcpAuthProvider 2LO/3LO/API Key 示例
  - BigQuery analytics LLM cache metadata 日志
- **链接**：https://github.com/google/adk-python/releases/tag/v1.32.0

### 9. AstrBot — v4.24.2
- **发布日期**：2026-05-03
- **核心变更**：
  - 插件自定义 WebUI 页面（Plugin Pages）能力
  - 插件国际化 i18n 支持
  - 插件技能 skills 目录支持
- **链接**：https://github.com/AstrBotDevs/AstrBot/releases/tag/v4.24.2

---

## 对我工作的启发

1. **OpenAI Agents SDK 默认模型切换到 GPT-5.4-mini** — 标志性事件：GPT-5 系列正式成为 agent 开发默认基线。推理加速需同步适配 GPT-5 系列（reasoning.effort / verbosity 新参数），vLLM/SGLang 需要跟进这些参数的解析和优化路径。
2. **MCP 工具名前缀防冲突** — agent 调用多 MCP server 时工具名冲突是实际问题。OpenAI 的 `include_server_in_tool_names` 方案简单有效，自建 agent 框架可参考。
3. **LangGraph DeltaChannel** — 增量 checkpoint 对长运行 agent 意义重大。类似思路可迁移到推理框架的 KV cache 管理：只存增量而非全量，减少显存占用。
4. **Hermes Agent 自治 Curator** — agent 自维护技能库是"agent 自我进化"方向的重要实验。对大模型智能体方向有参考：agent 不应只执行任务，还应持续优化自身能力库。
5. **Google ADK OpenTelemetry 原生集成** — agentic metrics 标准化正在发生。推理服务监控可提前对接 OTel agentic metrics 规范，为可观测性统一铺路。

---

## 明日跟踪建议

1. **OpenAI Agents SDK** — v0.16.0 后续 patch：关注 tool call output index 稳定化是否引入行为变更
2. **LangGraph 1.2.0 正式版** — DeltaChannel + streaming v3 合并进度，预计近期正式发布
3. **Dify 协作编辑** — 自部署稳定性，可能影响 agentic workflow 团队开发模式
4. **DeepSeek v4 在 Pydantic-AI 中的集成** — deepseek-v4-flash/pro 的推理成本/延迟表现，如可用作推理加速 benchmark 新基准
5. **Chrome DevTools MCP 第三方工具扩展** — 对 browser-use agent 生态的影响
