---
title: "GitHub 智能体日报（2026-03-19）- MCP 稳定性、运行时可观测与多沙箱增强"
date: 2026-03-19
track: 智能体
slug: mcp-runtime-sandbox-updates
source_report: /home/li/.openclaw/workspace/reports/github_agent_news_2026-03-19.md
repo_path: openclaw_reports/daily_github_news/agent/2026-03/2026-03-19-agent-mcp-runtime-sandbox-updates.md
generated_by: openclaw
---

# GitHub 智能体日报（2026-03-19）

## 今日要点
1. **MCP / 工具调用稳定性是今天最明确的主线**：`openai/openai-agents-python` 发布 `v0.12.4`，重点修复 cancelled MCP 调用归一化、isolated session 下 streamable-http MCP 瞬态失败重试，以及 SQLite session 表名兼容；`mastra-ai/mastra` 则直接补掉 MCP HTTP transport 在客户端断连时导致 Node 进程崩溃的问题。
2. **Agent runtime 开始原生暴露“执行态元信息”**：`langchain-ai/langgraph` 新增 `Runtime.execution_info`，把 `node_attempt`、`node_first_attempt_time` 注入节点与重试链路，为 retry-aware agent、节点级 tracing、失败复盘打基础。
3. **自托管 / 多沙箱后端适配继续加速**：`langchain-ai/open-swe` 把 sandbox provider 切换统一到 `SANDBOX_TYPE`，新增 Daytona / Runloop / Modal / Local 后端，并补了路径解析与 clone 安全处理，明显是在给多环境部署扫雷。
4. **Agent framework 正在集中补云兼容与企业落地短板**：`pydantic/pydantic-ai` 的 `v1.70.0` 新增 Bedrock inference profile，并强化 tool-calling / retry 健壮性；`crewAIInc/crewAI` 的 `1.11.0` 正式版则把 plan-execute、A2A enterprise 鉴权、安全修补收进稳定分支。

## 项目速递（含链接）
- **OpenAI Agents Python `v0.12.4`**
  - 更新：将 cancelled MCP invocation 统一规范为 tool error；为 isolated session 下的 streamable-http MCP 瞬态失败加入 retry；`AdvancedSQLiteSession` 支持自定义表名；jittered retry delay 增加上限保护。
  - 技术意义：MCP 工具调用从“能跑”升级到“失败可归因、可恢复”，这对生产级 agent 非常关键。
  - 链接：
    - https://github.com/openai/openai-agents-python/releases/tag/v0.12.4
    - https://github.com/openai/openai-agents-python/compare/v0.12.3...v0.12.4

- **LangGraph：执行态元信息进入 runtime**
  - 更新：`Runtime` 新增 `ExecutionInfo`，节点现在可读取 `node_attempt` 与 `node_first_attempt_time`；retry path 会自动在每次重试前更新这些字段。
  - 技术意义：节点级重试、退避策略、profiling 和 tracing 终于有了原生“第几次执行 / 首次执行时间”数据面，不必再靠业务侧自行打补丁。
  - 链接：
    - https://github.com/langchain-ai/langgraph/pull/7143

- **Open-SWE：多 sandbox provider 与可移植路径解析增强**
  - 更新：通过 `SANDBOX_TYPE` 统一切换 LangSmith / Daytona / Runloop / Modal / Local sandbox；新增 sandbox work dir / repo dir 解析；修复写死 `/workspace` 的路径假设，并对 clone 参数做 `shlex.quote` 处理。
  - 技术意义：这让 Open-SWE 更容易迁移到自有沙箱、第三方 devbox 或本地开发环境，自托管 agent 的环境适配成本明显下降。
  - 链接：
    - https://github.com/langchain-ai/open-swe/pull/1071

- **PydanticAI `v1.70.0`**
  - 更新：新增 `bedrock_inference_profile`；修复 Bedrock tool name sanitize、Anthropic malformed tool args retry、thinking-only response 文本恢复、OpenRouter Anthropic dotted model 匹配等问题。
  - 技术意义：多云模型路由与 tool-calling 健壮性同步加强，说明 agent 框架的竞争点正在从“接入更多模型”转向“复杂 provider 组合下仍然稳定工作”。
  - 链接：
    - https://github.com/pydantic/pydantic-ai/releases/tag/v1.70.0
    - https://github.com/pydantic/pydantic-ai/compare/v1.69.0...v1.70.0

- **crewAI `1.11.0` 正式版**
  - 更新：正式 release 在过去 24 小时发布；从 `1.11.0rc1/rc2` 进入稳定版的核心变化包括：加入 `plan execute pattern`、A2A enterprise 的 Plus API token authentication，增强 LLM response handling / serialization，替换 unsafe mode 下的 `os.system` 调用，并修复 code interpreter sandbox escape。
  - 技术意义：不是单点补丁，而是同时覆盖规划模式、企业身份、代码执行隔离与序列化健壮性，明显是朝生产落地方向收敛。
  - 链接：
    - https://github.com/crewAIInc/crewAI/releases/tag/1.11.0
    - https://github.com/crewAIInc/crewAI/releases/tag/1.11.0rc2
    - https://github.com/crewAIInc/crewAI/releases/tag/1.11.0rc1

- **Mastra：修复 MCP HTTP transport 断连崩溃**
  - 更新：给 `fetch-to-node@2.1.0` 打补丁，在客户端中途断开流式连接时，避免 `ReadableStream` 已关闭后再次 `controller.close()/enqueue()` 触发 `ERR_INVALID_STATE`，从而防止 Node.js 进程崩溃。
  - 技术意义：对依赖流式返回、MCP HTTP transport、browser / tool agent 的服务部署尤其重要，本质上是在补“长连接场景下的运行时稳定性”。
  - 链接：
    - https://github.com/mastra-ai/mastra/pull/13904

## 对我工作的启发
1. **智能体评测要把 MCP 失败类型和恢复能力纳入指标**：今天多个项目都在补“取消、断连、瞬态失败、错误归一化”。后面你如果做 agent benchmark，不能只看成功率，还要记录 tool error taxonomy、重试是否成功、重试额外时延与代价。
2. **运行时应像推理系统一样暴露 execution info**：`node_attempt`、`first_attempt_time` 这类字段非常适合迁移到你后面自己的 agent runtime / benchmark 脚手架里，用于分析抖动、回退、尾延迟与失败重试。
3. **多环境部署能力要靠 provider-neutral 抽象，不要写死路径/沙箱假设**：Open-SWE 这次的路径解析和多 provider 工程，和推理侧适配不同集群/设备/容器环境是同类问题，值得直接借鉴其“工位目录解析 + provider factory”思路。
4. **企业级 agent 的优先级已经不是“再多一个能力”，而是“身份、隔离、兼容、稳定”**：crewAI 与 PydanticAI 的更新都说明，到了真实落地阶段，系统工程质量比炫技能力更重要。

## 明日跟踪建议
1. 跟进 `openai/openai-agents-python` 是否继续把 MCP failure taxonomy、retry 策略和 observability 暴露到更高层 API / tracing 中；如果有，值得直接借鉴到你自己的 agent 基建设计。
2. 跟进 `langchain-ai/langgraph` 的 `execution_info` 是否继续扩展到 step latency、attempt reason、resume source 等字段；一旦继续扩展，参考价值会很高。
3. 跟进 `langchain-ai/open-swe` 是否补更多 provider 的配置示例与 benchmark，尤其是 Daytona / Runloop 的启动延迟、文件系统语义和成本差异。
4. 跟进 `crewAI` `1.11.0` 正式版后续是否补更明确的 plan-execute 文档与 sandbox security 说明；如果补出来，适合拆成一份“企业 agent 运行时 checklist”。
5. 跟进 `pydantic/pydantic-ai` Bedrock inference profile 是否进一步影响 agent benchmark 的路由配置、吞吐稳定性和多区域部署策略。