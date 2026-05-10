# GitHub 智能体日报 — 2026-05-10

> 数据窗口：2026-05-09 05:50 UTC ~ 2026-05-10 05:50 UTC（含 5 月 7-8 日重大 release 回溯）

---

## 一、今日要点

1. **Hermes Agent v0.13.0 "The Tenacity Release" 重磅发布** — 多 Agent Kanban 看板、`/goal` 目标锁定、Checkpoints v2 状态持久化、安全加固 8 个 P0，是本周智能体领域最大 release。
2. **OpenAI Agents Python v0.17.0** — RealtimeAgent 默认模型升级到 gpt-realtime-2；Sandbox 沙箱本地源物化策略收紧，引入 `SandboxPathGrant` 安全边界。
3. **LangChain v1.2.18** — 撤回 `ls_agent_type` 标签、弃用 hub、`create_agent` 废弃路径重定向。
4. **Hermes Agent 持续活跃**：24h 内修复 background reviewer 误将临时环境故障固化为"技能"的问题（#23004），对 Agent 自学习可靠性有重要启发。
5. **CrewAI v1.14.5a4**（pre-release）— 依赖修复 + LLM 列表更新，稳定版待发。

---

## 二、项目速递

### 1. Hermes Agent — v0.13.0 "The Tenacity Release"

- **发布日期**：2026-05-07
- **规模**：864 commits / 588 merged PRs / 829 files changed / 128K+ insertions / 282 issues closed / 295 community contributors
- **核心特性**：
  - 🔥 **Multi-agent Kanban**：持久化多 Agent 看板，支持 heartbeat、reclaim、zombie detection、auto-block on incomplete exit、per-task retries、hallucination recovery
  - 🎯 **`/goal` 命令**：跨 turn 目标锁定（Ralph loop），Agent 不再遗忘任务
  - 💾 **Checkpoints v2**：状态持久化 + 真正 pruning
  - 🔄 **Gateway auto-resume**：中断后重启自动恢复会话
  - ⏰ **Cron `no_agent` watchdog mode**
  - 🔒 **安全加固**：8 P0 修复 — redaction 默认开启、Discord role-allowlists guild-scoped、WhatsApp 拒绝陌生人、TOCTOU 窗口关闭
  - 🌐 **Google Chat 成为第 20 个平台**
  - 🔌 **Providers 可插拔化**
  - 🗣️ **7 个 i18n locale**
- **24h 内新 commit**：
  - `fix(review): tell background reviewer not to capture transient env failures as skills (#23004)` — 修复 Agent 将"Playwright 未安装"等临时故障固化为"浏览器工具不可用"技能、导致长期拒绝使用的问题
- **链接**：[Release](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.5.7) | [Commit #23004](https://github.com/NousResearch/hermes-agent/pull/23004)

### 2. OpenAI Agents Python — v0.17.0

- **发布日期**：2026-05-08
- **核心变更**：
  - 🎙️ **RealtimeAgent 默认模型 → gpt-realtime-2**
  - 🏖️ **Sandbox 本地源物化收紧**：`LocalFile.src` / `LocalDir.src` 现在限制在 `base_dir` 内，超出需 `Manifest.extra_path_grants`（`SandboxPathGrant`）显式授权，修复本地 artifact 边界漏洞
- **24h 内新 commit**：
  - `feat: improve examples auto-run coverage and artifact handling (#3328)`
  - `fix: include sandbox provider error details (#3326)`
- **链接**：[Release](https://github.com/openai/openai-agents-python/releases/tag/v0.17.0) | [Commit #3328](https://github.com/openai/openai-agents-python/pull/3328) | [Commit #3326](https://github.com/openai/openai-agents-python/pull/3326)

### 3. LangChain — v1.2.18

- **发布日期**：2026-05-08
- **核心变更**：
  - 🔙 **撤回** `ls_agent_type` tag on `create_agent` calls（#37249 revert）
  - 🚫 **弃用 hub**，限制 `loads`/`dumps`（#37234）
  - 🔄 `create_agent` 废弃路径重定向（#37164）
  - 🔥 **Fireworks provider** 1.2.1（#37113）
- **24h 内新 commit**：
  - `fix(core): avoid eager pydantic.v1 import in @deprecated (#37308)` — 修复 Python 3.14+ 下 Pydantic v1 兼容警告
- **链接**：[Release](https://github.com/langchain-ai/langchain/releases/tag/langchain%3D%3D1.2.18) | [Commit #37308](https://github.com/langchain-ai/langchain/pull/37308)

### 4. CrewAI — v1.14.5a4 (pre-release)

- **发布日期**：2026-05-08
- **核心变更**：
  - 📋 更新 LLM listings
  - 🔧 依赖修复：`textual` 移至 `crewai-cli`，新增 `certifi`
- **链接**：[Release](https://github.com/crewAIInc/crewAI/releases/tag/1.14.5a4)

### 5. LangGraph — CLI v0.4.25 + SDK v0.3.14

- **CLI v0.4.25**（2026-05-07）：新增 **Studio Deploy** 支持（#7394）
- **SDK v0.3.14**（2026-05-05）：`return_minimal` 参数、`stream_events(version='v3')`、streaming transformer 基础设施、ToolNode 支持 `list[Command | ToolMessage]` 返回
- **链接**：[CLI Release](https://github.com/langchain-ai/langgraph/releases/tag/cli%3D%3D0.4.25) | [SDK Release](https://github.com/langchain-ai/langgraph/releases/tag/sdk%3D%3D0.3.14)

### 6. SGLang — v0.5.11（推理加速相关，跨赛道参考）

- **发布日期**：2026-05-05
- **亮点**：CUDA 13 + Torch 2.11、Speculative Decoding V2 默认开启、PD Disaggregation decode radix cache、新模型支持（Gemma 4 / GLM-5.1 / Qwen3.6 / Kimi-K2.6 等）、DeepSeek-V3 & Kimi-K2 LoRA
- **链接**：[Release](https://github.com/sgl-project/sglang/releases/tag/v0.5.11)

---

## 三、对我工作的启发

1. **Agent 自学习的可靠性是核心挑战**：Hermes Agent #23004 暴露了一个典型问题 — Agent 的 skill review 机制将临时环境故障固化为"此工具不可用"的持久认知，导致长期拒绝使用已修复的工具。**启发**：在设计 Agent 记忆/学习系统时，必须区分"持久知识"和"临时状态"，自学习写入需加"不要捕获"过滤，且对负面断言需设置衰减/验证机制。

2. **Sandbox 安全边界收紧趋势**：OpenAI Agents Python v0.17.0 引入 `SandboxPathGrant`，限制沙箱对宿主文件系统的默认访问。**启发**：在构建 Agent 工具执行环境时，安全边界设计应从"默认开放、按需限制"转向"默认封闭、按需授权"。

3. **多 Agent 协作走向持久化看板**：Hermes Agent 的 Kanban 是首个将多 Agent 协作模式做实为持久化看板 + 故障恢复的方案。**启发**：在做推理服务编排时，可借鉴其 heartbeat / zombie detection / reclaim 机制，增强推理 pipeline 的鲁棒性。

4. **Agent 框架普遍在加固安全与稳定性**：Hermes 8 P0 修复、OpenAI Sandbox 边界、LangChain Python 3.14 兼容 — 说明 Agent 框架正从"功能扩展期"进入"工程可靠性期"，这与推理加速的稳定化趋势一致。

---

## 四、明日跟踪建议

| 优先级 | 项目 | 关注点 |
|--------|------|--------|
| 🔴 高 | Hermes Agent | 关注 v0.13.0 后续 patch，特别是 Kanban 在大规模任务下的稳定性 |
| 🔴 高 | OpenAI Agents Python | v0.17.0 后续版本是否进一步完善 Sandbox 和 RealtimeAgent |
| 🟡 中 | LangChain | `create_agent` 废弃路径重定向的迁移影响 |
| 🟡 中 | CrewAI | v1.14.5 稳定版何时发布 |
| 🟡 中 | LangGraph | Studio Deploy 实际体验 + streaming transformer 后续 |
| 🟢 低 | SGLang / vLLM | 跟踪推理框架最新 patch 对 Agent serving 场景的优化 |

---

*报告自动生成于 2026-05-10 13:50 CST | 数据源：GitHub API*
