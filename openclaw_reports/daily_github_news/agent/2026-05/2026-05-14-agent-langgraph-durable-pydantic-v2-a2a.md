# GitHub 智能体日报（2026-05-14）

## 今日要点

1. **LangGraph 1.2.0 正式发布**：引入跨主机崩溃的持久化错误恢复（durable error-handler resume）、Delta Channel 快照强制触发、`set_node_defaults()` 等关键特性，标志着 LangGraph 在生产级容错方面迈出重要一步。
2. **Pydantic AI v1.95.0 发布，V2 预热启动**：新增原生 Tool Search（Anthropic/OpenAI）、Instrumentation 能力层、Gemini 3 结构化输出+工具组合，同时开始为6月 V2 做字段重命名与弃用铺垫。
3. **Semantic Kernel python-1.42.0 发布，README 新增 Microsoft Agent Framework 继任者声明**：微软在 SK 的 README 中正式标注了后继框架（Microsoft Agent Framework），暗示 SK Python 的战略方向将逐步迁移。
4. **A2A 协议 v1.0.0 正式发布**：Google 主导的 Agent-to-Agent 互操作协议发布首个正式版，为多智能体跨平台通信定下标准基线。
5. **MCP Servers 升级至 zod v4 + 最新 MCP SDK**：everything-server 完成依赖现代化，为 MCP 生态的后续扩展铺路。

## 项目速递

### 1. LangGraph 1.2.0
- **发布日期**：2026-05-12
- **关键更新**：
  - 🛡️ **durable error-handler resume across host crashes**：错误处理器状态持久化，主机崩溃后可恢复执行（#7773）
  - 🔧 **`set_node_defaults()` for StateGraph**：支持节点级默认值设定，减少重复配置（#7747）
  - 📡 **Delta Channel 强制快照**：超过最大 supersteps 后强制 delta channel 快照，防止增量丢失（#7746）
  - 🔄 **Delta Channel exit mode 重新实现**（#7730）
  - 💾 **checkpoint-sqlite 流式 walk 覆写**（#7702）
  - 📝 DeltaChannel & delta-history API 标记为 beta（#7732）
- **链接**：https://github.com/langchain-ai/langgraph/releases/tag/1.2.0

### 2. Pydantic AI v1.95.0
- **发布日期**：2026-05-12
- **关键更新**：
  - 🔍 **原生 Tool Search**：Anthropic 和 OpenAI 上支持原生工具搜索，任意 provider 可自定义搜索策略（#5143）
  - 📊 **Instrumentation 能力层**：新增 `Instrumentation` capability，弃用旧 `Agent(instrument=...)`（#4967）
  - 🤖 **Gemini 3 结构化输出+工具组合**：支持同时使用结构化输出与工具调用（#4848）
  - ⚡ **V2 预热**：built-in tools → native tools 重命名；新增 `local=` opt-in 替代自动 fallback（#5338, #5331）
  - 🐛 Bedrock 客户端运行时替换修复、模型 ID 归一化（#5392, #5395）
- **链接**：https://github.com/pydantic/pydantic-ai/releases/tag/v1.95.0

### 3. Semantic Kernel python-1.42.0
- **发布日期**：2026-05-14（今日！）
- **关键更新**：
  - 📢 **README 新增 Microsoft Agent Framework 继任者声明**：明确标注 SK Python 的后继框架方向（#13932）
  - 📦 多项依赖升级：authlib, onnxruntime, boto3, google-genai, google-cloud-aiplatform 等
- **链接**：https://github.com/microsoft/semantic-kernel/releases/tag/python-1.42.0

### 4. A2A Protocol v1.0.0
- **发布日期**：2026-05-11
- **关键更新**：
  - 🌐 Agent-to-Agent 互操作协议首个正式版
  - 定义多智能体跨平台通信标准
- **链接**：https://github.com/a2aproject/A2A/releases/tag/v1.0.0

### 5. MCP Servers - zod v4 + MCP SDK 升级
- **提交日期**：2026-05-12
- **关键更新**：
  - ⬆️ everything-server 升级至 zod v4，同步最新 MCP SDK（#4136）
- **链接**：https://github.com/modelcontextprotocol/servers/commit/acedea0c24b3e20d7265f87b8b2afe2e0c6eb2f4

## 对我工作的启发

1. **LangGraph 持久化错误恢复值得关注**：其"跨主机崩溃恢复"机制对生产环境智能体长期运行至关重要。当前自研 Agent 系统如需增强容错，可参考其 checkpoint + error-handler 持久化方案。
2. **Pydantic AI V2 方向明确**：native tools 统一 + `local=` 显式 opt-in 的设计哲学，说明 V2 会更注重 provider 透明性。若基于 pydantic-ai 构建项目，现在就该开始适配新 API。
3. **Semantic Kernel → Microsoft Agent Framework 迁移信号**：微软在 SK 中正式标注继任者，意味着 SK Python 可能进入维护模式。如果在用 SK，应开始评估 MAF 的迁移路径。
4. **A2A 协议 v1.0 定标**：多 Agent 互操作协议正式落地，后续可关注 vLLM/SGLang 等推理框架是否会原生支持 A2A 的 Agent Card 发现机制。
5. **MCP 生态持续迭代**：zod v4 + 最新 SDK 升级表明 MCP 工具侧也在快速进化，自建 MCP server 时需关注 SDK 版本兼容。

## 明日跟踪建议

- 🔭 **Pydantic AI V2 后续**：V2 计划6月发布，关注 v1.96+ 中可能的 breaking change 预告
- 🔭 **Microsoft Agent Framework**：SK 继任者细节尚未公开，跟踪微软官方博客/仓库
- 🔭 **LangGraph Delta Channel**：beta API 转正时间线及生产就绪度
- 🔭 **A2A 生态接入**：关注 LangChain / CrewAI 等框架对 A2A v1.0 的适配进展
- 🔭 **OpenAI Agents Python**：v0.17.x 迭代节奏，是否接近 v1.0

---
*报告生成时间：2026-05-14 13:50 CST | 数据源：GitHub API*
