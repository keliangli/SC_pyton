# GitHub 智能体日报 — 2026-05-06

## 今日要点

1. **Hermes Agent v0.12.0 发布「Curator」版本**：135k ⭐ 的 NousResearch/hermes-agent 推出自主后台 Curator，可按计划自动评分、修剪、合并技能库，自改进循环大幅升级
2. **Gemini CLI v0.42.0-preview 发布**：103k ⭐ 的 google-gemini/gemini-cli 重构 ACP 客户端为模块化架构，新增 A2A 协议推送、OAuth 子代理解析修复
3. **claude-mem v12.6.5 连续更新**：72.6k ⭐ 的 thedotmack/claude-mem 新增网关环境变量支持（ANTHROPIC_AUTH_TOKEN），修复代理池超时和观察者响应死循环
4. **Cherry Studio v1.9.4 支持新一代模型**：45.1k ⭐ 的 CherryHQ/cherry-studio 添加 DeepSeek V4+ 和 Kimi K2.6 支持，移除 MCP 自动注入
5. **OpenHands v1.7.0 支持 KVM 沙箱**：新增 /dev/kvm 直通，沙箱可运行硬件加速虚拟机；暴露 SDK 设置 Schema

## 项目速递

### 1. NousResearch/hermes-agent — v0.12.0 (2026-04-30)
- ⭐ 135k | 🔗 https://github.com/NousResearch/hermes-agent/releases/tag/v2026.4.30
- **自主 Curator**：后台代理按 7 天周期自动评分/合并/修剪技能库，归档分「合并」vs「修剪」两类
- **自改进循环升级**：从 free-form 改为 class-first rubric 评分，偏好 active-update，支持 templates/ 子文件继承
- **集成扩展**：ComfyUI v5、TouchDesigner-MCP 从可选升级为默认捆绑；新增 Spotify + Google Meet 原生集成
- **性能**：TUI 冷启动速度降低约 57%
- 1,096 commits / 550 PRs / 213 社区贡献者

### 2. google-gemini/gemini-cli — v0.42.0-preview (2026-05-05)
- ⭐ 103k | 🔗 https://github.com/google-gemini/gemini-cli/releases/tag/v0.42.0-preview.1
- ACP 客户端从单体重构为模块化文件
- 新增 OAuth 字段支持子代理解析
- A2A pushMessage 增加空日志守卫
- `/exit` 命令新增 `--delete` 标志用于会话删除
- 修复终端 DECKPAM 键盘 Enter 序列处理

### 3. thedotmack/claude-mem — v12.6.5 (2026-05-05)
- ⭐ 72.6k | 🔗 https://github.com/thedotmack/claude-mem/releases/tag/v12.6.5
- 安装器统一以 Claude Agent SDK 为唯一 memory-agent 路径
- 新增 ANTHROPIC_AUTH_TOKEN 网关环境变量支持
- 移除固定 agent-pool 槽位超时，排队任务等待而非丢弃
- v12.6.4 修复无效 XML 观察者响应导致无限重试的问题

### 4. crewAIInc/crewAI — v1.14.5a2 (2026-05-04)
- ⭐ 50.7k | 🔗 https://github.com/crewAIInc/crewAI/releases/tag/1.14.5a2
- 新增 `restore_from_state_id` kickoff 参数，支持从状态恢复
- 修复异步批量刷新时任务输出丢失
- 修复跨代理共享 LLM stop words 互变异问题
- 修复 `result_as_answer` 返回钩子阻塞消息或错误作为最终答案

### 5. CherryHQ/cherry-studio — v1.9.4 (2026-04-30)
- ⭐ 45.1k | 🔗 https://github.com/CherryHQ/cherry-studio/releases/tag/v1.9.4
- 新增 DeepSeek V4+ 模型支持（含 reasoning_effort）
- 新增 Kimi K2.6 模型支持（禁用 temperature/top_p）
- 移除 @cherry/browser MCP 自动注入
- 修复 gpt-image-2 / gpt-image-1.5 生成失败和挂起问题
- DeepSeek DSML 标签解析修复

### 6. OpenHands/OpenHands — v1.7.0 (2026-05-01)
- 🔗 https://github.com/OpenHands/OpenHands/releases/tag/1.7.0
- 新增 SANDBOX_KVM_ENABLED 环境变量，沙箱可运行 KVM 加速虚拟机
- 暴露 SDK 设置 Schema 给智能体
- Tavily 搜索 key 迁移至 MCP 设置
- 多项 CVE 修复和 UI 修复

### 7. browser-use/browser-use — v0.12.6 (2026-04-02)
- 🔗 https://github.com/browser-use/browser-use/releases/tag/0.12.6
- **性能**：修复 DOM 捕获 O(n²) 瓶颈，重页面性能大幅提升
- 修复 Anthropic action 字段双重序列化
- 修复 MCP browser_click schema 中 oneOf 导致 Claude API 客户端崩溃
- 修复 daemon 孤儿进程和 CDP 导航超时
- 关闭 httpx 客户端池防止 Lambda OOM

### 8. inclusionAI/AReaL — v1.0.3 (2026-04-16)
- 🔗 https://github.com/inclusionAI/AReaL/releases/tag/v1.0.3
- 新增 Agent Service 微服务基础设施
- 新增 Rollout Gateway（控制器 + 路由器 + 数据代理）
- 新增 NUMA CPU 亲和性绑定
- 新增 BailingMoeV2.5 支持（Lightning Attention + MLA + MoE + CP）
- 修复流式 chat/completions 响应处理

## 对我工作的启发

1. **自主 Curator 模式值得关注**：Hermes Agent 的后台 Curator 机制（自动评分/修剪/合并技能）与 OpenClaw 的 skill 管理场景高度契合，可借鉴其 rubric 评分 + 分类归档思路
2. **ACP 模块化是趋势**：Gemini CLI 将 ACP 客户端拆分为专业化文件，说明智能体间通信协议正从单体走向模块化，A2A 协议开始进入实际产品
3. **DOM 捕获性能优化有参考价值**：browser-use 的 O(n²) → 线性修复思路，对自研浏览器自动化工具的性能优化有直接参考意义
4. **KVM 沙箱直通思路**：OpenHands 的 /dev/kvm 方案让沙箱内可跑硬件加速 VM，对推理服务隔离部署有启发
5. **网关认证标准化**：claude-mem 引入 ANTHROPIC_AUTH_TOKEN 环境变量，说明智能体记忆系统正在标准化网关认证流程

## 明日跟踪建议

1. **跟踪 Hermes Agent v0.12.0 落地反馈**：Curator 机制在实际使用中的效果和边界情况
2. **关注 Gemini CLI ACP/A2A 进展**：模块化重构后是否会加速 A2A 协议在更多智能体框架中的采纳
3. **观察 crewAI v1.14.5 正式版**：当前为 alpha 预发布，`restore_from_state_id` 功能可能对有状态智能体编排产生较大影响
4. **留意 DeepSeek V4+ 生态适配**：Cherry Studio 已率先支持，其他框架跟进速度值得关注
5. **关注 AReaL Agent Service 架构**：其微服务化 Agent Service + Rollout Gateway 的设计可能在 RL 训练推理一体化场景中有更多进展
