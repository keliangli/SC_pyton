# GitHub 智能体技术日报 — 2026-05-23

> 抓取时间：2026-05-23 14:32 CST | 覆盖范围：过去 24h 内 AI Agent 相关 release/重大更新

---

## 今日要点

1. **OpenAI Codex v0.133.0 发布**：Goals 系统默认开启、remote-control 改为前台模式、权限配置文件支持继承与运行时刷新
2. **Claude Code v2.1.149 发布**：/usage 分项统计、多个 PowerShell 沙箱逃逸修复、git worktree 写入白名单修正
3. **SWE-agent v1.1.0 发布**：推出 SWE-smith 训练轨迹生成器，SWE-agent-LM-32b 达成 SWE-bench Verified 开源 SotA
4. **Gemini CLI v0.44.0-preview.0 发布**：Agent 注册改为 first-wins 策略、合并 Auto 模式
5. **Agent 安全加固密集期**：Codex、Claude Code、OpenAI Agents Python 本周均发布安全修复

---

## 项目速递

### 1. OpenAI Codex — v0.133.0
- **发布时间**：2026-05-21
- **链接**：https://github.com/openai/codex/releases/tag/rust-v0.133.0
- **核心更新**：
  - Goals 功能默认启用，含专用存储 + 跨 turn 进度跟踪
  - `codex remote-control` 改为前台命令模式，等待就绪、报告状态，保留 daemon 式 start/stop
  - Permission Profiles 新增 list API、继承、managed requirements.toml、运行时刷新、Windows 沙箱强化
  - Plugin Discovery 更易检查：marketplace-aware list、已安装版本、远程 collection 支持
  - Extension 可观察更多生命周期事件（subagent start/stop、tool 执行、turn 元数据、异步审批）
  - 修复 TUI 启动工作目录错误、plan-mode Shift+Enter 意外提交、app-server 启停竞态等

### 2. Claude Code — v2.1.149
- **发布时间**：2026-05-22
- **链接**：https://github.com/anthropics/claude-code/releases/tag/v2.1.149
- **核心更新**：
  - `/usage` 按类别（skills/subagents/plugins/per-MCP-server）展示用量分项
  - `/diff` 详情视图支持键盘滚动（方向键/j/k/PgUp/PgDn/Space/Home/End）
  - Markdown 输出渲染 GFM 任务列表复选框
  - Enterprise 新增 `allowAllClaudeAiMcps` 设置，可加载 claude.ai 云端 MCP 连接器
  - **安全修复**：PowerShell `cd..`/`cd\`/`cd~`/`X:` 绕过检测 → 修复；git worktree 写入白名单覆盖整个仓库根目录 → 收窄；PowerShell 前缀/通配符 allow 规则未生效 → 修复；`find` 在 macOS 大目录耗尽 file descriptor → 修复

### 3. SWE-agent — v1.1.0
- **发布时间**：2026-05-22
- **链接**：https://github.com/SWE-agent/SWE-agent/releases/tag/v1.1.0
- **核心更新**：
  - 发布 [SWE-smith](https://swesmith.com/)：可生成数万条 SWE agent 训练轨迹
  - 使用该训练数据，**SWE-agent-LM-32b 在 SWE-bench Verified 上达成开源权重 SotA**
  - v1.1.0 主要为修复版本 + 训练数据基础设施

### 4. Gemini CLI — v0.44.0-preview.0
- **发布时间**：2026-05-22
- **链接**：https://github.com/google-gemini/gemini-cli/releases/tag/v0.44.0-preview.0
- **核心更新**：
  - Agent 注册改为 first-wins 策略，project 级优先
  - 合并多种 Auto 模式为单一 Auto mode
  - 修复 OAuth refresh token 轮换与获取时的丢失问题
  - 严格类型校验消除 no-unsafe-return 抑制

### 5. LangGraph SDK — v0.3.15
- **发布时间**：2026-05-22
- **链接**：https://github.com/langchain-ai/langgraph/releases/tag/sdk%3D%3D0.3.15
- **核心更新**：
  - URL 路径中用户提供的标识符改为 percent-encode（安全修复）
  - Crons search/count 支持 metadata filter
  - LangGraph 主包升级至 1.2.1，langchain-core 升级至 1.4.0
  - 多项依赖安全更新（idna 3.15、urllib3 2.7.0）

### 6. OpenAI Agents Python — v0.17.3
- **发布时间**：2026-05-19
- **链接**：https://github.com/openai/openai-agents-python/releases/tag/v0.17.3
- **核心更新**：
  - 修复沙箱命令中泄露 mountpoint 凭证的问题
  - 统一 memory 可选依赖的 import 错误提示
  - FunctionTool params_json_schema 不可变保护
  - Output guardrail count 加入 RunErrorDetails

### 7. CrewAI — v1.14.6a1 (pre-release)
- **发布时间**：2026-05-21
- **链接**：https://github.com/crewAIInc/crewAI/releases/tag/1.14.6a1
- **核心更新**：
  - 新增 Skills Repository（含 registry、cache、CLI、SDK 集成）
  - 企业版分类 release notes 生成
  - RuntimeState 序列化加固
  - 安全更新：idna 升级至 3.15

---

## 对我工作的启发

| 维度 | 启发 |
|------|------|
| **安全** | 本周 Codex / Claude Code / OpenAI Agents 三大框架集中修复沙箱逃逸和权限绕过，说明 Agent 安全是当前工程热点。我们做推理服务部署时也需关注 tool-use 场景下的权限边界 |
| **训练数据** | SWE-smith 证明"用 agent 轨迹训练 agent"可行且效果显著（开源 SotA），这对我们做推理加速 benchmark/trace 收集有借鉴价值 |
| **Goals 系统** | Codex Goals 默认开启 = Agent 从"单轮执行"到"多轮目标跟踪"的演进，与推理加速场景中多 step 编排思路一致 |
| **用量分项** | Claude Code /usage 分项统计 = Agent 运行时成本透明化趋势，推理服务也需 finer-grained 的 token/latency/cost 可观测性 |
| **插件生态** | Codex Plugin Discovery + Claude Code MCP 企业管理 = Agent 可扩展性从"能用"进入"可治理"阶段 |

---

## 明日跟踪建议

1. **SWE-smith**：跟踪 https://swesmith.com/ 后续论文/数据集发布，评估对 SWE-bench 评测方法的影响
2. **Codex Goals 存储**：关注 Goals 的持久化机制是否开放 API，可能影响 subagent 编排设计
3. **Claude Code PowerShell 安全**：持续关注 Windows 沙箱攻防，后续版本可能有更深层修复
4. **Gemini CLI Auto mode 合并**：观察社区对简化后的 Auto 模式反馈，可能预示 agent 自主决策范式的收敛
5. **CrewAI Skills Repository**：跟踪正式版发布，评估与 MCP 工具生态的竞合关系

---

*本报告由 OpenClaw 自动生成，数据来源为 GitHub Releases 页面。*
