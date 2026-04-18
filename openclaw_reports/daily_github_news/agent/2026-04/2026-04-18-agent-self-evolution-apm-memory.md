# GitHub 智能体日报 — 2026-04-18

## 今日要点

1. **智能体自演化成为当日最强主题**：EvoMap/evolver（GEP 基因组演化协议）和 lsdefine/GenericAgent（3.3K 行种子代码自生长技能树）双双登上 GitHub 全站 Trending Top 3，合计日增 1500+ stars，标志着 Agent 自演化/自进化范式正在从概念走向工程化。
2. **Agent 包管理标准之争开启**：Microsoft 发布 APM（Agent Package Manager），类似 npm/pip 但面向 Agent 配置和技能依赖，支持传递依赖解析、安全审计和跨平台安装——这是 Agent 生态走向可复现、可组合的关键基础设施。
3. **云原生 Agent 模板加速**：Vercel Labs 开源 open-agents，提供 Web→Agent Workflow→Sandbox VM 三层架构模板，日增 470 stars，强调 Agent 执行与沙箱分离、可持久化恢复。
4. **Agent 记忆系统爆发**：claude-mem（61K⭐，日增 2,161）和 cognee 分别从会话级压缩和知识图谱两个方向解决 Agent 跨会话记忆问题，这是 Agent 长期可用的核心瓶颈。
5. **Anthropic 官方发布 Agent Skills 仓库**：anthropics/skills 公开发布，包含 SKILL.md 规范、文档生成技能、MCP 服务器生成技能等，与 agentskills.io 标准联动。

---

## 项目速递

### 🔥 EvoMap/evolver — GEP 自演化引擎
- **链接**: https://github.com/EvoMap/evolver
- **Stars**: 4,477 (+737 today)
- **语言**: JavaScript
- **核心**: 基于基因组演化协议（GEP）的 Agent 自演化引擎。将 prompt 微调转化为可审计、可复用的演化资产（Gene/Capsule），支持 `--review` 人工确认和 `--loop` 持续演化。采用 git 做回滚和影响半径计算。
- **注意**: 正从 GPL-3.0 开源转向 source-available 模式（因同类项目抄袭设计）。

### 🔥 lsdefine/GenericAgent — 自生长技能树 Agent
- **链接**: https://github.com/lsdefine/GenericAgent
- **Stars**: 3,837 (+845 today)
- **语言**: Python
- **核心**: 仅 3.3K 行核心代码，通过 9 个原子工具 + 100 行 Agent Loop 实现系统级控制（浏览器、终端、文件系统、ADB）。每完成一个任务自动结晶为技能，token 消耗降低 6 倍。已支持 Claude/Gemini/Kimi 等多模型。
- **最新**: 2026-04-11 引入 L4 会话归档记忆和 scheduler cron 集成。

### 🔥 microsoft/apm — Agent 包管理器
- **链接**: https://github.com/microsoft/apm
- **Stars**: 1,830 (+206 today)
- **语言**: Python
- **核心**: 面向 AI Agent 的依赖管理器，类似 package.json 但管理 instructions/skills/prompts/hooks/plugins/MCP servers。支持从 GitHub/GitLab/Bitbucket 安装，传递依赖解析，`apm audit` 安全扫描，CI/CD Action 集成。
- **配套**: agentrc 工具可从代码库自动生成 agent 指令。

### 🔥 vercel-labs/open-agents — 云端 Agent 模板
- **链接**: https://github.com/vercel-labs/open-agents
- **Stars**: 3,629 (+470 today)
- **语言**: TypeScript
- **核心**: Web→Agent Workflow→Sandbox VM 三层分离架构。Agent 在 Vercel Workflow 上持久运行，沙箱可独立休眠/恢复，支持快照恢复、自动 commit/PR、会话分享、语音输入。

### thedotmack/claude-mem — Claude Code 会话记忆
- **链接**: https://github.com/thedotmack/claude-mem
- **Stars**: 61,672 (+2,161 today)
- **语言**: TypeScript
- **核心**: 自动捕获 Claude Code 会话中的工具使用行为，AI 压缩后注入后续会话，实现跨会话上下文延续。一条命令 `npx claude-mem install` 即可安装。

### anthropics/skills — Anthropic 官方 Agent Skills 仓库
- **链接**: https://github.com/anthropics/skills
- **核心**: 公开发布 Agent Skills 规范和示例技能集（docx/pdf/pptx/xlsx 文档生成、MCP 服务器生成、品牌设计等）。可通过 Claude Code Plugin Marketplace 安装。源码分 Apache 2.0 和 source-available 两种许可。

### topoteretes/cognee — Agent 记忆知识引擎
- **链接**: https://github.com/topoteretes/cognee
- **核心**: 6 行代码即可使用的 Agent 记忆引擎。结合向量搜索 + 图数据库，提供 remember/recall/forget/improve 四个原语。支持会话记忆和知识图谱双层存储。已有 OpenClaw 插件和 Claude Code 插件。

### Tracer-Cloud/opensre — AI SRE Agent 框架
- **链接**: https://github.com/Tracer-Cloud/opensre
- **Stars**: 1,550 (+184 today)
- **语言**: Python
- **核心**: 面向生产事故响应的 AI SRE Agent 框架。连接 60+ 运维工具，提供合成 RCA 评测套件和端到端云场景测试（K8s/EC2/CloudWatch/Lambda/ECS/Flink）。目标是成为 AI SRE 的 SWE-bench。

### lukilabs/craft-agents-oss — Craft Agents
- **链接**: https://github.com/lukilabs/craft-agents-oss
- **Stars**: 4,328 (+110 today)
- **语言**: TypeScript
- **核心**: 同时使用 Claude Agent SDK 和 Pi SDK 的多任务 Agent 客户端。支持自然语言接入任意 API/MCP 服务器，文档驱动的 Agent 原生工作流。可用 Craft Agents 本身来开发 Craft Agents。

### obra/superpowers — Agent 技能框架与开发方法论
- **链接**: https://github.com/obra/superpowers
- **核心**: 完整的 Agent 驱动开发方法论：需求澄清→设计文档→实施计划→子 Agent 驱动开发（TDD/YAGNI/DRY）。支持 Claude Code/Codex/Cursor/OpenCode/Gemini CLI/Copilot 等全平台。

### Donchitos/Claude-Code-Game-Studios — 49 Agent 游戏工作室
- **链接**: https://github.com/Donchitos/Claude-Code-Game-Studios
- **核心**: 将 Claude Code 变成完整游戏开发工作室：49 个专业化 Agent（3 层导演/部门/专员层级）、72 个工作流技能、12 个自动验证 Hook、39 个文档模板。

### ChromeDevTools/chrome-devtools-mcp — 浏览器调试 Agent
- **链接**: https://github.com/ChromeDevTools/chrome-devtools-mcp
- **Stars**: 35,938 (+196 today)
- **核心**: Chrome DevTools 的 MCP 服务器，让编码 Agent 可直接操控浏览器调试。

---

## 对我工作的启发

1. **Agent 自演化方向值得深入跟踪**：EvoMap/evolver 的 GEP 协议和 GenericAgent 的技能结晶机制，与推理加速中的"自适应优化"思路有共通之处——都是在运行时根据反馈自动改进。可关注其 token 效率优化策略（GenericAgent 声称 6x token 节省）。
2. **APM 标准化是基础设施信号**：Microsoft 的 APM 意味着 Agent 技能/配置即将进入"可打包、可分发、可审计"阶段。对于构建 Agent 应用的团队，这意味着配置管理成本将大幅下降。
3. **Agent 记忆系统是工程化瓶颈**：claude-mem 的爆发式增长（61K stars）说明跨会话记忆是当前 Agent 最大的痛点。cognee 的 remember/recall/forget 四原语设计值得关注，可能在推理服务中也有应用（如 KV Cache 的智能复用）。
4. **云原生 Agent 架构模式趋于收敛**：Vercel open-agents 的 Web→Workflow→Sandbox 三层分离已成为事实标准模式，这与 vLLM/SGLang 的分离式推理架构有相似的解耦思想。
5. **开源与 source-available 之争升温**：EvoMap 因抄袭转向 source-available，这预示着 Agent 框架领域可能出现开源商业模式重塑。

---

## 明日跟踪建议

1. **EvoMap/evolver 的 GEP 协议细节**：深入阅读其 assets/gep/ 目录下的 Gene/Capsule 定义，理解其演化审计机制。
2. **GenericAgent 的技能结晶机制**：关注其如何从任务执行路径自动提取可复用技能，尤其是 token 压缩策略。
3. **microsoft/apm 的传递依赖解析**：测试 apm install 的实际体验，评估其作为 Agent 技能管理基础设施的成熟度。
4. **cognee vs claude-mem 的记忆架构对比**：两者分别从知识图谱和会话压缩切入，值得做详细的架构对比分析。
5. **open-agents 的 Sandbox 休眠/恢复机制**：与推理服务的 prefix caching 做类比分析，看是否可借鉴到 vLLM 的调度策略中。
