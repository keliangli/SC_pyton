# GitHub 智能体日报 — 2026-05-13

---

## 今日要点

1. **Dify v1.14.1 发布**（5月12日）— 安全加固版，自托管部署不再依赖公开默认 SECRET_KEY，IDOR 修复，LiteLLM CVE 升级，工作流稳定性改进。
2. **Gemini CLI v0.43.0 发布**（5月12日）— 引导模型优先使用 edit tool 做精准编辑；ACP 工具调用说明从 thought stream 移至 tool call content；A2A server 修复竞态条件；新增 shell 命令安全 eval。
3. **Hermes Agent 持续高密度迭代**— v0.13.0（5月7日）"Tenacity Release"已上线多智能体 Kanban 板、/goal 持久化目标、Checkpoints v2、Gateway 自动恢复；近 24h 内修复 prompt cache 布局（system prompt 字节稳定性）、统一 Portal client 标签、重命名 Alibaba Cloud 为 Qwen Cloud。
4. **Deer Flow（字节跳动）工程深化**— 元数据过滤从 Python 端推至 SQL 端（性能提升）；修复 update_agent 用户隔离 bug（setup_agent 已在先前修复，本次补齐另一半）。
5. **LobeHub Agent Signal 修复**— skill bundle/index 均视为主要 skill 文档；tool outcome 中 user id context 缺失修复。

---

## 项目速递

| 项目 | 更新类型 | 关键变化 | 链接 |
|------|----------|----------|------|
| **langgenius/dify** v1.14.1 | Release | SECRET_KEY 运行时生成、IDOR 修复、LiteLLM CVE 升级、内部指标端点保护 | [GitHub](https://github.com/langgenius/dify/releases/tag/1.14.1) |
| **google-gemini/gemini-cli** v0.43.0 | Release | edit tool 引导、ACP tool call 语义修正、A2A 竞态修复、shell 安全 eval | [GitHub](https://github.com/google-gemini/gemini-cli/releases/tag/v0.43.0-preview.0) |
| **NousResearch/hermes-agent** v0.13.0 | Release (5/7) + 活跃开发 | 多智能体 Kanban、/goal 持久目标、prompt cache 重构、Qwen Cloud 重命名 | [GitHub](https://github.com/NousResearch/hermes-agent) |
| **bytedance/deer-flow** | 重要 Commit | 元数据过滤 SQL 下推、update_agent 用户隔离修复、LangGraph 兼容入口文档 | [GitHub](https://github.com/bytedance/deer-flow) |
| **OpenHands/OpenHands** v1.7.0 | Release (5/1) + 开发 | Org 隔离、BitBucket API 替换、App Tab 移除 | [GitHub](https://github.com/OpenHands/OpenHands) |
| **infiniflow/ragflow** | 修复 | GraphRAG UI 删除修复、Baidu Encode 错误处理、embedding 空块防护 | [GitHub](https://github.com/infiniflow/ragflow) |
| **mem0ai/mem0** v2.0.2 | Release (5/7) + 文档 | 时序推理 cookbook、plugin v0.1.2、SQL 注入防护 | [GitHub](https://github.com/mem0ai/mem0) |
| **lobehub/lobehub** | 修复 | Agent Signal skill 判断逻辑修正、user id context 传递修复 | [GitHub](https://github.com/lobehub/lobehub) |

---

## 对我工作的启发

1. **Prompt Cache 稳定性是推理优化的隐性问题** — Hermes Agent 发现 system prompt 的 volatile tier 每轮变化导致 prefix cache 失效，回退到单 block 布局后 within-session 缓存命中率反而提升。这提醒我们：推理框架的 cache 设计需要和上层 agent 框架的 prompt 构造对齐，否则 KV cache 优化可能被上层破坏。
2. **多智能体协作走向"看板化"** — Hermes 的 Kanban board + heartbeat + zombie detection 模式、Deer Flow 的子 agent 生命周期管理，都说明多 agent 编排正从"链式调用"演变为"持久化任务板 + 监督回收"。这对我们做 agent 编排框架选型有参考。
3. **安全加固成为 release 主旋律** — Dify、Mem0、OpenHands 近期版本都把安全修复放在首位（IDOR、SQL 注入、CVE 升级、SECRET_KEY 硬化）。自研/内部 agent 平台同样需要关注 API 边界校验和依赖安全。
4. **Agent Memory 持久化方案日趋成熟** — Mem0 的时序推理 + claude-mem 的跨 session 压缩注入，都在解决 agent 记忆问题。对推理加速场景，记忆层的设计也会影响 prompt 长度和 cache 策略。

---

## 明日跟踪建议

- [ ] 关注 Hermes Agent 下一个 release 是否引入 provider 插件化的更多细节
- [ ] Dify v1.14.1 的安全加固模式是否被其他 agentic 平台跟进（特别是 SECRET_KEY 运行时生成方案）
- [ ] Gemini CLI ACP 协议的 tool call 语义变化是否影响 OpenClaw 等 ACP 客户端
- [ ] Deer Flow 的 SQL 元数据过滤方案是否开源了通用 JsonMatch 组件
- [ ] Mem0 时序推理能力对 agent 记忆架构的长期影响
