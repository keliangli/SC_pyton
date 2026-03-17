---
title: "GitHub 智能体日报（2026-03-17）- 治理模块、评测闭环与浏览器运行时强化"
date: 2026-03-17
track: 智能体
slug: governance-eval-browser-runtime
source_report: /home/li/.openclaw/workspace/reports/github_agent_news_2026-03-17.md
repo_path: openclaw_reports/daily_github_news/agent/2026-03/2026-03-17-agent-governance-eval-browser-runtime.md
generated_by: openclaw
---

# GitHub 智能体日报（2026-03-17）

## 今日要点
1. **治理能力开始模块化落地**：`microsoft/agent-governance-toolkit` 在过去 24 小时新增 **Scope Guard、Promotion Gates、Drift Detector** 三类治理模块，并补了 `Conversation Guardian` 的交互式演示，说明 agent 治理正从“策略概念”走向可部署组件。
2. **Agent 评测从单轮成功率升级到多轮轨迹评测**：`google/adk-python` 连续加入 **MultiTurn Task Success / Task Trajectory / Tool Trajectory** 指标，并给 `UnsafeLocalCodeExecutor` 增加超时控制，评测与沙箱安全一起增强。
3. **生产级多智能体编排继续补安全边界**：`crewAI` 发布 `1.11.0rc1`，同时引入 **A2A enterprise 的 Plus API token 鉴权**、**plan-execute pattern**，并修复 **code interpreter sandbox escape**，方向很明确：不是只拼能力，而是补企业接入和隔离面。
4. **浏览器/工具型 agent 的运行时工程化还在加速**：`browser-use` 加入 **LiteLLM provider** 并修复慢页面下截图链路被高亮清理阻塞的问题；`dspy-go` 则继续补 **TBLite 任务切片** 与 **GEPA optimizer winner selection**，都在朝“更稳的评测闭环 + 更可控的运行时”收敛。

## 项目速递（含链接）
- **Microsoft Agent Governance Toolkit**
  - 更新：新增 `Scope Guard`、`Promotion Gates`、`Drift Detector` 模块，并增加 `Conversation Guardian` 交互式 show & tell demo。
  - 技术意义：治理层开始细化为“范围约束 / 发布闸门 / 漂移检测”三段式模块，更接近企业 agent 平台真正需要的控制面。
  - 链接：
    - https://github.com/microsoft/agent-governance-toolkit/commit/4f00ca3f282267bcc1cce6c8680fe321008ebf79
    - https://github.com/microsoft/agent-governance-toolkit/commit/0d77b28b5b41b04fc9da4c39157e4222aca14013

- **Google ADK (`google/adk-python`)**
  - 更新：新增 `MultiTurn Task Success`、`MultiTurn Task Trajectory`、`Tool Trajectory` 指标，并为 `UnsafeLocalCodeExecutor` 增加 timeout 支持。
  - 技术意义：开始把 agent 评估从“最终答对没”扩展到“中间路径是否稳、工具使用是否合理”，这对评测自动化非常关键。
  - 链接：
    - https://github.com/google/adk-python/commit/9a75c06873b79fbd206b3712231c0280fb2f87ca
    - https://github.com/google/adk-python/commit/38bfb4475406d63af3111775950d9c25acf17ed2
    - https://github.com/google/adk-python/commit/71d26ef7b90fe25a5093e4ccdf74b103e64fac67

- **crewAI 1.11.0rc1**
  - 更新：release 中明确加入 **Plus API token authentication for A2A enterprise**、**plan execute pattern**，并修复 **code interpreter sandbox escape**。
  - 技术意义：这不是普通小修，直接覆盖了多 agent 企业接入、任务规划模式和代码执行隔离三个核心面。
  - 链接：
    - https://github.com/crewAIInc/crewAI/releases/tag/1.11.0rc1

- **browser-use**
  - 更新：加入 **LiteLLM provider**；同时修复慢页面下 `remove_highlights()` 阻塞 screenshot handler 的问题。
  - 技术意义：一边补多模型接入，一边补浏览器观测链路稳定性，说明浏览器 agent 的主战场已转向 provider 抽象和 runtime 工程质量。
  - 链接：
    - https://github.com/browser-use/browser-use/commit/90cb6e8b7d03f6203735d4e05eb006e540a5cce1
    - https://github.com/browser-use/browser-use/commit/c8380d12e75a5789780e61f6f6e56b7a3d8de54c

- **dspy-go**
  - 更新：新增 **curated TBLite task slices**，并修复 **GEPA validation winner** 在 agent optimizer 中的使用逻辑。
  - 技术意义：继续强化 benchmark 数据集与 optimizer 闭环，属于“让 agent 优化流程更可复现”的实质进展。
  - 链接：
    - https://github.com/XiaoConstantine/dspy-go/commit/9de49f51c905f36dac9939a637a08a47927fc8de
    - https://github.com/XiaoConstantine/dspy-go/commit/2b95284bfe66271b7437dc871ada1666b9e472fd

## 对我工作的启发
1. **Agent 平台不能只盯推理吞吐，还要预留治理控制面**：Scope Guard / Promotion Gates / Drift Detector 这类模块，未来大概率会像 tracing/metrics 一样成为标配；如果后面做 agent runtime，建议一开始就留策略挂点与回滚闸门。
2. **评测体系要从“结果分”升级到“过程分”**：ADK 把 multi-turn success、task trajectory、tool trajectory 拉进来，说明只看最终成功率已经不够。你后面做智能体评测时，也该把工具调用路径、轮次成本、失败回退轨迹纳入指标。
3. **多智能体企业化落地，安全边界和鉴权是第一层门槛**：crewAI 这次把 A2A enterprise token auth 与 sandbox escape fix 放到同一个 release，非常说明问题——agent 互联和代码执行一旦进入生产，身份与隔离必须先行。
4. **浏览器/工具 agent 的性能瓶颈越来越像推理系统问题**：provider 抽象、非阻塞截图链路、慢页面处理，本质上都在解决延迟抖动和上下文/观测成本；这和你做推理侧 runtime 稳定性优化是同类问题。

## 明日跟踪建议
1. 跟进 `microsoft/agent-governance-toolkit` 新治理模块是否继续补 SDK/API 文档与接入示例，尤其是 `Promotion Gates` 和 `Drift Detector` 是否会暴露可编排接口。
2. 跟进 `google/adk-python` 是否把这些 multi-turn / trajectory 指标快速整理进 release note、样例 notebook 或 dashboard；如果有，值得借鉴到你的 agent benchmark 体系。
3. 跟进 `crewAI` 的 `1.11.0` 正式版是否保留当前的 A2A enterprise 鉴权方案，以及 sandbox escape 修复是否附带更明确的隔离策略说明。
4. 跟进 `browser-use` 的 LiteLLM 接入范围（是否只补 provider 还是连配置/streaming 一起完善），以及 `dspy-go` 后续是否公布更具体的 TBLite benchmark 结果。