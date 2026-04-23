# GitHub 智能体日报（2026-04-23）

## 今日要点

- **Coding Agent 上下文增强成热点**：claude-context（Zilliz）日增 871 star，用向量检索为 Coding Agent 提供全代码库语义搜索，已适配 Claude Code、Codex CLI、Gemini CLI、Cursor、Qwen Code 等 10+ Agent 框架，MCP 协议成标配。
- **Vercel 开源 Agent Skills 工具链**：vercel-labs/skills 日增 333 star，发布 v0.8.x 系列——支持快照下载替代 git clone、LFS 跳过、--json 输出、40+ Agent 框架适配（含 OpenClaw），形成跨框架 Skill 标准化生态。
- **AI 自动渗透测试 Agent Shannon 升级 v1.1.0**：KeygraphHQ/shannon 4/21 发布 v1.1.0——新增 pipeline 核心库抽取（可被第三方消费）、结构化输出漏洞队列、Docker overlay 挂载只读+写层、provider 扩展与 claude-code-router 模式移除、debug 日志增强。
- **Langfuse v3.169 发布**：新增 QueueMetricsRunner 队列指标采集、AWS Bedrock Bearer Token 支持、OCI Object Storage 集成、L1 缓存模型匹配、Claude Opus 4.7 价格录入——Agent 可观测性基础设施持续完善。
- **FinceptTerminal v4.0.2 发布**：C++20 + Qt6 原生金融终端，内嵌 37 个 AI Agent（巴菲特/格雷厄姆/林奇等风格），16 家券商实时交易集成，MCP 工具接入——金融领域 Agent 应用纵深加速。
- **RAG-Anything 多模态知识图谱升级**：HKUDS/RAG-Anything 发布 VLM-Enhanced Query 模式，图片自动注入 VLM 做多模态分析，+context 配置模块——为 Agent 的检索增强提供全模态支持。

## 项目速递

### 1. claude-context — Coding Agent 全代码库语义搜索 MCP
- **链接**：https://github.com/zilliztech/claude-context
- **Stars**：7,791（日增 871）
- **核心更新**：MCP 协议集成向量数据库（Zilliz/Milvus），为 Coding Agent 提供百万行代码语义检索，避免全量目录加载的高成本；已适配 Claude Code、Codex CLI、Gemini CLI、Cursor、Windsurf、VS Code、Cherry Studio 等 10+ 编码 Agent。
- **配套**：memsearch Claude Code 插件（markdown-first 跨 session 持久记忆）。

### 2. vercel-labs/skills — 开源 Agent Skills 生态 CLI
- **链接**：https://github.com/vercel-labs/skills
- **Stars**：15,624（日增 333）
- **核心更新**：
  - v0.8.x：快照下载替代全量 git clone（#853），LFS 跳过带宽膨胀（#952），--json 机器可读输出（#558）
  - 支持 40+ Agent 框架（含 OpenClaw），统一 SKILL.md + YAML frontmatter 规范
  - skills.sh 发现平台上线
  - OpenClaw 因恶意/重复 skill 被标注警告（#865）

### 3. Shannon v1.1.0 — 自主 AI 渗透测试 Agent
- **链接**：https://github.com/KeygraphHQ/shannon
- **Stars**：39,745（日增 372）
- **核心更新**（v1.1.0, 4/21）：
  - pipeline 核心库抽取为独立模块（#282），可被外部工具消费
  - 结构化输出漏洞利用队列（#267），从自由文本改为 JSON schema
  - Docker overlay 挂载：用户代码只读 + Shannon 写层分离（#273）
  - provider 扩展 + 移除 claude-code-router 模式（#295）
  - --debug flag + Docker 错误可见化（#299）

### 4. Langfuse v3.169 — LLM/Agent 可观测性平台
- **链接**：https://github.com/langfuse/langfuse
- **Stars**：25,751（日增 149）
- **核心更新**：
  - QueueMetricsRunner：定时采集队列指标+分片聚合（#13231）
  - AWS Bedrock Bearer Token API 支持（#13098）
  - OCI Object Storage IAM 集成（#12379）
  - L1 本地缓存模型匹配（#12977），减少数据库查询
  - Claude Opus 4.7 价格录入（#13214）
  - Slack prompt 变更通知显示作者（#13149）

### 5. FinceptTerminal v4.0.2 — 金融 Agent 终端
- **链接**：https://github.com/Fincept-Corporation/FinceptTerminal
- **Stars**：13,365（日增 1,772）
- **核心更新**：
  - C++20 + Qt6 原生二进制，无 Electron overhead
  - 37 个 AI Agent（巴菲特/格雷厄姆/林奇等投资风格框架）
  - 16 家券商实时 WebSocket 交易（含 Zerodha, IBKR, Alpaca 等）
  - MCP 工具集成 + 可视化工作流节点编辑器

### 6. RAG-Anything — 多模态 RAG 框架
- **链接**：https://github.com/HKUDS/RAG-Anything
- **核心更新**：
  - VLM-Enhanced Query：文档图片自动注入 VLM 做多模态分析
  - context 配置模块：智能整合上下文增强多模态处理
  - MinerU 高保真文档抽取 + 多模态知识图谱构建

### 7. WorldMonitor — AI 全球情报仪表盘
- **链接**：https://github.com/koala73/worldmonitor
- **Stars**：51,820
- **核心特性**：500+ 新闻源 AI 合成简报，3D globe + WebGL 双引擎，跨流信号关联（军事/经济/灾难），本地 Ollama 运行，5 个站点变体，Tauri 2 原生桌面。

### 8. Pixelle-Video — AI 全自动短视频引擎
- **链接**：https://github.com/AIDC-AI/Pixelle-Video
- **Stars**：5,892（日增 308）
- **核心特性**：LLM 生成文案 → ComfyUI 生图 → TTS 配音 → 模板合成，支持 Edge-TTS / Index-TTS / 声音克隆，Windows 一键整合包。

## 对我工作的启发

1. **MCP 正成为 Agent 互操作标准**：claude-context 和 vercel-labs/skills 都以 MCP 为核心协议，Agent 工具链标准化趋势明确。对推理加速场景，应关注 MCP 在推理 Agent 中的应用（如 vLLM/SGLang 的 MCP 集成）。

2. **Skill 标准化生态加速**：vercel-labs/skills 已适配 40+ Agent 框架，SKILL.md + YAML frontmatter 成跨框架通用格式。OpenClaw 已在列表中被警告恶意 skill——说明 skill 质量审计需重视。

3. **Agent 安全测试自动化**：Shannon v1.1.0 将 pipeline 核心库抽取为可消费模块，结构化输出取代自由文本——这为 Agent 安全审计的可复现性和工具链集成提供了范式。

4. **金融领域 Agent 深度应用**：FinceptTerminal 用 37 个风格化 Agent 做投资决策，原生 C++ 高性能+MCP 集成——垂直领域 Agent 的工程化路径值得参考。

5. **可观测性持续下沉**：Langfuse 新增 Bedrock Bearer Token、OCI 存储、L1 缓存、队列指标——Agent 可观测性从 trace 收集下沉到基础设施层优化。

## 明日跟踪建议

- claude-context 是否发布正式 release（目前无 release，仅 npm 包发布）
- vercel-labs/skills 对 OpenClaw 恶意 skill 标注后续进展
- Shannon v1.1.0 pipeline 核心库被第三方消费情况
- Langfuse v3.170（预发布版 4/22 已发布）最终 release 内容
- FinceptTerminal Q2 路线图：50+ AI Agent 扩展进展