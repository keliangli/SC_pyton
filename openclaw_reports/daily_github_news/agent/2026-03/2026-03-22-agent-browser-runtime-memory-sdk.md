---
title: "GitHub 智能体日报（2026-03-22）- 浏览器执行修复与记忆栈补强"
date: 2026-03-22
track: 智能体
slug: browser-runtime-memory-sdk
source_report: /home/li/.openclaw/workspace/reports/github_agent_news_2026-03-22.md
repo_path: openclaw_reports/daily_github_news/agent/2026-03/2026-03-22-agent-browser-runtime-memory-sdk.md
generated_by: openclaw
---

# GitHub 智能体日报（2026-03-22）

## 今日要点
1. **Browser agent runtime 进入“修正确保可执行”阶段**：`browser-use/browser-use` 在过去 24 小时连续补了 cross-origin iframe DOM 索引、点击后新标签页自动切换、checkbox/radio toggle fallback、Selenium `wss://` 兼容与 webhook JSON 守卫，明显是在集中清理浏览器智能体的长尾正确性问题。
2. **Agent memory / data plane 继续补“少出错、能扩容”**：`mem0ai/mem0` 新增 Turbopuffer 向量库接入，同时修正 MCP `search_memory` 过滤优先级、OpenSearch 向量合法性校验、graph store 的 LLM 配置回退逻辑，重点不是炫新能力，而是减少 silent failure。
3. **框架侧开始把 agent 能力往更标准的 SDK / 查询接口收敛**：`OpenBMB/ChatDev` 宣布 `chatdev 0.1.0` Python SDK，可直接在 Python 中执行 YAML workflow 与多智能体任务；`microsoft/semantic-kernel` 则删掉旧式向量过滤分支，继续向单一表达式过滤路径收敛。
4. **今天不是“大版本发布日”，而是“工程质量日”**：最值得关注的不是 flashy feature，而是浏览器执行正确性、记忆检索边界条件、向量存储兼容性、查询路径性能这些真正决定 agent 能不能稳定上线的点。

## 项目速递（含链接）
- **browser-use：集中修补浏览器智能体执行正确性**
  - 更新：
    - 修复 cross-origin iframe DOM 索引，增加按 `src` URL 回退匹配 frame、并在目标 frame 可用时递归拉取 DOM；
    - 点击后自动切换新标签页，并为 checkbox/radio 增加“状态未翻转时回退到 JS `element.click()`”机制；
    - Selenium 接入同时兼容 `ws://` / `wss://` CDP 地址，并为 webhook 验签增加 JSON parse guard。
  - 技术意义：这是 browser agent 从“能点”走向“复杂网页里也能稳定点”的典型补丁，尤其针对嵌套 iframe、弹新页、表单控件这三类最常见失效点。
  - 链接：
    - https://github.com/browser-use/browser-use/commit/f66dc67553d28c479593e85d73bbc535af987735
    - https://github.com/browser-use/browser-use/commit/6bc09a21bf7dc9d1be42fa2b1b1bfaa42543c71e
    - https://github.com/browser-use/browser-use/commit/318eb3b41e409d0b1e2cd41927652bbaa8109e92

- **mem0：把 memory layer 的可用性问题一口气补厚**
  - 更新：
    - 新增 Turbopuffer 作为 serverless vector database provider；
    - 修复 MCP `search_memory` 过滤条件中的运算符优先级错误，避免 allowlist 失真；
    - 给 OpenSearchDB 增加向量非空、非 null、维度匹配校验；
    - graph store 在未显式指定 `graphStore.llm` 时，改为正确回退到 root `llm` 配置，而不是硬编码默认 provider。
  - 技术意义：这组更新同时覆盖“扩容新后端 + 修 retrieval 逻辑 + 防向量脏数据 + 修 provider 配置传播”，对 production agent memory 非常关键。
  - 链接：
    - https://github.com/mem0ai/mem0/commit/bf9a5703b1ddf3bc0c0bfef53f74ba6b6f9e341e
    - https://github.com/mem0ai/mem0/commit/ec326f0f925fa1c2c4bc4dcbc51d3cfe4373813d
    - https://github.com/mem0ai/mem0/commit/eb780f488062e56cf9ebf95307d7a1b47c5779b1
    - https://github.com/mem0ai/mem0/commit/06c25eb00bca4e9d7b12e9dd9d70378b464a294e

- **ChatDev：Python SDK 正式进入主仓信号位**
  - 更新：仓库 README / README-zh 在过去 24 小时加入 `chatdev` Python SDK 发布说明，给出 `chatdev 0.1.0` 安装入口，主打“直接在 Python 中运行 YAML workflow 与多智能体任务”。
  - 技术意义：这意味着 ChatDev 不再只是一个 demo / 平台入口，而是在补“可嵌入 Python 工程”的二次开发接口，方便把多智能体编排纳入现有代码栈。
  - 链接：
    - https://github.com/OpenBMB/ChatDev/commit/5e6a0c337ae5e97bf743c11544494fa8e251f9af
    - https://github.com/OpenBMB/ChatDev/commit/5ed6dfeea669a2b18c5382503a3d0d9d12475455
    - https://pypi.org/project/chatdev/0.1.0/

- **Semantic Kernel：向量检索过滤接口继续去历史包袱**
  - 更新：`.NET` 侧移除了 MEVD provider 中对已废弃 `VectorSearchFilter` 的兼容分支，统一走新的表达式过滤翻译路径，不再维护 old/new filter 双轨逻辑。
  - 技术意义：Agent framework 一旦进入长期演化阶段，最怕的不是功能不够，而是 API 分叉导致的维护负担和行为不一致；这次更新是在主动收敛技术债。
  - 链接：
    - https://github.com/microsoft/semantic-kernel/commit/082e28e52ec2b45ad8cf287176d844150617e8b5

- **Dify：标注会话查询改成 selectinload + distinct**
  - 更新：在 console 侧 conversation 查询中，把 `joinedload(Conversation.message_annotations)` 改为 `selectinload(...)`，并在 annotation join 路径上补 `distinct()`。
  - 技术意义：这不是表面重构，而是在降低带 annotation 的对话列表查询放大效应，属于 agent 应用平台向“高并发 / 大规模会话管理”继续打磨的信号。
  - 链接：
    - https://github.com/langgenius/dify/commit/18e4ec73d6b144636a069ed4229f8a52b6ab9d3d

## 对我工作的启发
1. **做 agent benchmark 时，应该补一套“浏览器执行正确性回归集”**：至少覆盖 cross-origin iframe、点击弹新页、checkbox/radio 切换、CDP `wss://` 兼容、webhook 异常输入这几类 case。它们对 agent 是否可落地，重要性不亚于模型成功率。
2. **memory 层要像推理系统一样做严格输入校验与 provider 回退测试**：运算符优先级、向量维度合法性、provider fallback 这些 bug 一旦漏掉，表面看是“偶发错检”，本质上会污染长期记忆和评测结论。
3. **如果后面你自己沉淀 agent runtime / toolkit，优先考虑“Python SDK + 配置式 workflow”双入口**：ChatDev 的动作说明，框架竞争点正在从“能不能跑”转向“能不能嵌进现有工程、能不能自动化集成”。
4. **框架长期维护上，要尽量避免 old/new API 双轨并行**：Semantic Kernel 的做法很值得借鉴——一旦新抽象成熟，就尽快收敛到单路径，否则后面性能、行为和文档都会持续分叉。

## 明日跟踪建议
1. 跟进 `browser-use` 是否把这轮 iframe / 新标签页 / checkbox 修复打进正式 release，并补成稳定回归测试；如果补齐，这套 case 值得直接借鉴到你的 agent browser benchmark 中。
2. 跟进 `mem0` 是否很快发布包含 Turbopuffer 与 MCP 过滤修复的新版本；如果 release 出来，值得单独拆一次“agent memory 后端选型”对比。
3. 跟进 `ChatDev` Python SDK 是否继续补示例、执行模型说明和工作流 API；如果文档完整，适合拿来做一次源码级仓库拆解。
4. 跟进 `Semantic Kernel` 后续是否发布明确 migration note，说明旧 filter API 的替换路径；这对判断其 agent 检索抽象是否足够稳定很关键。
5. 跟进 `Dify` 这类查询层改造是否继续扩展到 workflow run / trace / annotation 后台；如果连续几天都在补数据库访问路径，说明它正进入 agent 平台工程化提速阶段。
