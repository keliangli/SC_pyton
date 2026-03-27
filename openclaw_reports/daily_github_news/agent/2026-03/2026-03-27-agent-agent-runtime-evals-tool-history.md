---
title: "GitHub 智能体日报（2026-03-27）- 运行时状态、轨迹评测与工具历史修复"
date: 2026-03-27
track: 智能体
slug: agent-runtime-evals-tool-history
source_report: /home/li/.openclaw/workspace/reports/github_agent_news_2026-03-27.md
repo_path: openclaw_reports/daily_github_news/agent/2026-03/2026-03-27-agent-agent-runtime-evals-tool-history.md
generated_by: openclaw
---

# GitHub 智能体日报（2026-03-27）

## 今日要点

- **agent runtime 正在从“能跑”转向“可恢复、可回退、可持久化”**：Microsoft Agent Framework 今天的重点不是再加一个新 demo，而是把 **skills 装载架构、多 agent handoff 回退、approval + persistence 正确性** 一起往运行时内核里收。说明多 agent 编排的竞争点，已经在往 workflow 状态机与会话一致性下沉。
- **agent eval 开始进入“执行路径评测”阶段**：PydanticAI 的 `CaseLifecycle` hooks、Mastra 的 unified trajectory scorer 与 review dashboard，都在把 agent 评测从“看最终答案”升级成“看中间轨迹、重试、预算、review 流程”。这对后续做 benchmark / regression / tracing 一体化很关键。
- **工具调用历史与外部信息访问成为稳定性焦点**：OpenAI Agents Python 给 `WebSearchTool` 新增 `external_web_access`，Agno 修复 Claude server tools 历史块丢失问题，本质上都在补同一件事：**tool 调用上下文必须可控且可重建**，否则多轮 agent 非常容易在第二轮开始失真。
- **评测与运营控制面正在融合**：Mastra 今天同时推进 experiment storage、review summary、dashboard 与 dataset-level review，说明 agent 平台正在把“开发、评测、人工审核、回归追踪”并到同一个操作面板，不再是松散脚本拼装。

## 项目速递（含链接）

1. **microsoft / agent-framework**  
   - 重要更新：`.NET` 侧合入一个 **breaking 级别的 Agent Skills multi-source architecture 重构**，把 skills 从单一文件/样例式能力，推进为可多来源装载的正式架构；同时新增 **handoff workflow 的 return-to-previous routing**，并修复 **per-service-call persistence + approvals** 组合下的对话历史重复注入问题。  
   - 技术判断：这三笔更新合在一起看，不是“加 feature”，而是在补 agent runtime 最难的三层：**能力装载、跨 agent 路由、会话一致性**。尤其 approval/persistence 修复，直接对应生产环境里最难查的一类状态错乱问题。  
   - 链接：  
     - skills multi-source architecture：https://github.com/microsoft/agent-framework/commit/0fcbe7e10553d901cc4969eef5c61532846f93e0  
     - handoff return-to-previous routing：https://github.com/microsoft/agent-framework/commit/5530bc536bc6d163625980f0245e35b5a2a4d2f0  
     - persistence + approvals 修复：https://github.com/microsoft/agent-framework/commit/3585581c7a6415db08832736b1d7a09cae6fcf22

2. **pydantic / pydantic-ai**  
   - 重要更新：发布 **v1.73.0**，核心内容包括：给 `Dataset.evaluate()` 增加 **`CaseLifecycle` hooks**；允许 hooks 抛出 `ModelRetry` 控制重试流；允许 before/wrap request hooks 通过 `ModelRequestContext` **动态切换模型**；并修复 capability schema 生成时参数类型不完整的问题。  
   - 技术判断：PydanticAI 正在把 agent eval 从“跑 case 出分”升级成“**每个 case 都可编排、可重试、可换模型、可挂上下文**”的执行框架。这对搭建系统级 benchmark、失败复现和 cost-aware eval 非常有价值。  
   - 链接：  
     - v1.73.0 release：https://github.com/pydantic/pydantic-ai/releases/tag/v1.73.0  
     - `ModelRetry` in hooks：https://github.com/pydantic/pydantic-ai/commit/f82046b87573155567b718dab369716214b18db4  
     - model swap via `ModelRequestContext`：https://github.com/pydantic/pydantic-ai/commit/f1260dfe09907f17688eee1646daf898fc428d4c

3. **mastra-ai / mastra**  
   - 重要更新：发布 **`@mastra/core@1.16.0`**，把 observational memory 的 observer/reflector 路由升级为 **按输入 token 阈值动态选模型**，并补上 **MongoDB-backed datasets / experiments**、`tool_suspended` / `respondToToolSuspension()` 等挂起恢复能力；同日又合入 **unified trajectory scorer** 与 **evaluation dashboard + review pipeline**，开始系统化评测 agent / workflow 的执行轨迹。  
   - 技术判断：Mastra 今天最值得注意的不是单个 feature，而是它在把 **memory、HITL suspension、trajectory eval、review pipeline** 串成同一条平台化链路。这意味着 agent 平台的重点正从“构建 agent”转向“运营 agent”。  
   - 链接：  
     - `@mastra/core@1.16.0` release：https://github.com/mastra-ai/mastra/releases/tag/%40mastra%2Fcore%401.16.0  
     - unified trajectory scorer：https://github.com/mastra-ai/mastra/commit/dc9fc19da4437f6b508cc355f346a8856746a76b  
     - evaluation dashboard / review pipeline：https://github.com/mastra-ai/mastra/commit/260fe1295fe7354e39d6def2775e0797a7a277f0

4. **openai / openai-agents-python**  
   - 重要更新：发布 **v0.13.2**。本次新增 `WebSearchTool.external_web_access`，允许显式声明是否访问实时外网；修复 persisted session items 中夹带私有 tool metadata 的问题；继续增强 LiteLLM `reasoning_effort` 的 provider portability，并临时 pin 上界缓解供应链风险。  
   - 技术判断：这版虽然不是大版本，但信号非常清晰：**web access policy、session hygiene、provider portability、dependency safety** 已经成为 agent SDK 的一线工程问题，不再只是外围运维细节。  
   - 链接：  
     - v0.13.2 release：https://github.com/openai/openai-agents-python/releases/tag/v0.13.2  
     - `external_web_access` for `WebSearchTool`：https://github.com/openai/openai-agents-python/commit/c52d25f4f93c5ac3c8021b3846d5800b829eeaa9  
     - strip private tool metadata from persisted session：https://github.com/openai/openai-agents-python/commit/c2f6690ff242bd990c031dbc9701370b34a3b559

5. **agno-agi / agno**  
   - 重要更新：修复 Claude server tools（`web_search` / `web_fetch` / `code_execution` 等）在多轮对话中 **server tool blocks 被历史层静默丢弃** 的问题；新实现会把相关 block 保存在 `provider_data` 中，并在后续轮次重建完整消息内容，避免第二轮请求因缺失 tool 结果而失败。  
   - 技术判断：这是典型的“**第一轮成功、第二轮翻车**”型 agent 基础设施 bug。它说明 Anthropic server tools / MCP / provider-native tools 的历史保真，已经是多轮 agent 成败的关键约束。  
   - 链接：  
     - preserve server tool blocks in Claude history：https://github.com/agno-agi/agno/commit/91ab3b431fcb3b84d7e8135f40b824c33200111d

## 对我工作的启发

- **把“执行轨迹”纳入智能体 benchmark 主指标**：今天 PydanticAI 和 Mastra 都在强化 trajectory / lifecycle / review pipeline。这对你后面做 agent 评测很重要：不要只测最终 answer，还要测 tool path、重试次数、budget 消耗、HITL 插入点和失败聚类。
- **agent runtime 的正确性测试要覆盖多轮历史重放**：Agno 和 Microsoft Agent Framework 的更新都说明，很多 bug 不出在首轮，而出在 approval 后恢复、handoff 后回退、tool result 回写后的第二/第三轮。后续做框架选型或自建 runtime，建议单列一组“multi-turn state correctness”回归集。
- **技能/工具装载要往“多来源 + repo-local 规则”设计**：Microsoft Agent Framework 的 multi-source skills 方向值得重点跟踪。对你后面做代码代理或仓库拆解工具，这意味着能力源应该支持 file / package / workspace / remote registry 多层装载，而不是只靠 prompt 拼接。
- **外网访问策略需要显式配置，而不是默认放开**：OpenAI Agents Python 把 `external_web_access` 直接拉成一等参数，这对做生产 agent 很有参考价值。后续你如果做 browsing / retrieval agent，最好把“实时外网 / 仅索引 / 内网检索”做成显式策略位，而不是隐藏在 provider 默认行为里。
- **评测、记忆、人工审核会逐步收敛成同一控制面**：Mastra 这波更新对平台设计很有启发——未来真正能落地的 agent 平台，大概率不是“一个 SDK + 一堆脚本”，而是把 eval、review、trace、memory、suspension/handoff 都收在统一工程面里。

## 明日跟踪建议

- 跟踪 **microsoft/agent-framework** 后续是否继续把 multi-source skills 扩到 Python 侧，或补更多 handoff / approval / checkpoint 测试；如果继续高频推进，说明它在冲刺可生产化 runtime。
- 跟踪 **pydantic-ai** 的 `CaseLifecycle` 是否很快接上 artifacts、trace hooks、成本统计或失败回放；这决定它能否真正成为系统级 agent eval 框架。
- 跟踪 **Mastra** 的 trajectory scorer 与 review dashboard 是否继续向“可批量回归 + 可人工复核 + 可自动打标签”收敛；如果是，这条线很适合借鉴到你的 benchmark 平台设计。
- 跟踪 **openai-agents-python** 是否继续把外网访问、session persistence、provider portability 做成统一 policy 层；这会影响其是否能从 SDK 走向通用 agent runtime。
- 跟踪 **Agno / Anthropic server tools** 相关生态是否出现更多“历史块保真、tool result replay、server tool trace”修复；如果频繁出现，说明这会是 2026 年多轮 agent 可靠性的高发坑位。