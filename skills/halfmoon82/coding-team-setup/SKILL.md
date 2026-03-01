# Coding Team Setup v2.0 — Flexible Multi-Agent Development Team

> 灵活搭建 2–10 位子代理开发团队，支持多团队命名、自定义协作流程
> Flexible setup for 2–10 agent collaborative teams on OpenClaw.

## What's New in v2.0

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Team size | Fixed 7 | **2–10 agents** |
| Team naming | Single team | **Multiple named teams** |
| Roles | 7 preset only | **10 preset + custom roles** |
| Workflow | Fixed 9-step | **4 templates + fully custom** |
| Model assignment | Hardcoded | **Auto-detect + manual override** |

## When to Use

- 搭建一个多角色协作开发团队（2–10人）
- 需要多个团队并行工作，各自独立配置
- 需要自定义协作流程（不限于标准9步）
- 需要灵活的角色组合和模型分配

## Quick Start

### 交互式配置向导（推荐）

```bash
# 默认团队
node <skill-dir>/wizard/setup.js

# 命名团队（支持多个团队并存）
node <skill-dir>/wizard/setup.js --team alpha
node <skill-dir>/wizard/setup.js --team beta
```

向导会引导你完成：
1. **团队命名** — 给团队一个名字（支持多团队）
2. **选择角色** — 从10个预设角色中选2–10个，或添加自定义角色
3. **分配模型** — 自动检测已注册模型，或手动指定
4. **选择协作流程** — 4个预设模板或完全自定义
5. **写入配置** — 自动更新 openclaw.json + 创建 workspace

## Available Role Templates (10)

| Role | ID | Emoji | Category | Default Model Type |
|------|----|-------|----------|--------------------|
| Product Manager | `pm` | 📋 | Management | Balanced |
| Architect | `architect` | 🏗️ | Engineering | Strongest |
| Frontend | `frontend` | 🎨 | Engineering | Code |
| Backend | `backend` | ⚙️ | Engineering | Code |
| QA | `qa` | 🔍 | Quality | Balanced |
| DevOps | `devops` | 🚀 | Operations | Strongest |
| Code Artisan | `code-artisan` | 🛠️ | Quality | Code |
| Data Engineer | `data-engineer` | 📊 | Engineering | Code |
| Security | `security` | 🔒 | Quality | Strongest |
| Tech Writer | `tech-writer` | 📝 | Management | Balanced |

**Custom roles:** 向导支持添加完全自定义的角色（ID、名称、emoji、职责、模型类型）。

## Workflow Templates (4)

### 1. 标准9步协作流程 (`standard-9step`)
```
PM → Architect评审 → Frontend + Backend并行 → Code Review → QA → 确认 → 部署
```
适合：完整项目开发，需要严格流程控制

### 2. 快速3步流程 (`quick-3step`)
```
直接开发 → Code Review → 部署
```
适合：小型功能、hotfix、快速迭代

### 3. 全栈独角兽 (`fullstack-solo`)
```
需求设计 → 全栈开发 → 测试部署
```
适合：2–3人精简团队

### 4. 完全自定义 (`custom`)
- 自由定义步骤数量
- 每步指定角色（支持多角色并行）
- 可设置 feedback loop
- 可标记可选步骤

## Multi-Team Support

一个 OpenClaw 实例可以运行多个团队：

```bash
# 团队 alpha：前端团队
node setup.js --team alpha
# 选择: frontend, qa, devops

# 团队 beta：后端团队
node setup.js --team beta
# 选择: backend, architect, qa, devops

# 团队 gamma：全栈
node setup.js --team gamma
```

每个团队的 agent ID 带团队前缀：`alpha-frontend`, `beta-backend` 等。

团队配置存储在：`teamtask/teams/<team-name>.json`

## Architecture

```
~/.openclaw/
├── openclaw.json              # 所有团队的 agent 配置
├── workspace/
│   └── teamtask/
│       ├── teams/             # 团队 manifest
│       │   ├── default.json
│       │   ├── alpha.json
│       │   └── beta.json
│       └── tasks/             # 项目任务目录
└── agents/                    # 子代理目录
    ├── pm/                    # default team
    ├── alpha-frontend/        # alpha team
    ├── beta-backend/          # beta team
    └── ...
```

## Model Assignment

向导自动检测 `openclaw.json` 中已注册的模型，按类型匹配：

| Model Type | Best For | Auto-detect Pattern |
|-----------|----------|---------------------|
| Strongest Reasoning | Architect, DevOps, Security | `/opus/i` |
| Code Specialized | Frontend, Backend, Code Artisan | `/codex/i` |
| Balanced | PM, QA, Tech Writer | `/sonnet/i` |
| Fast | Simple tasks | `/haiku/i` |
| Long Context | Cross-file analysis | `/gemini.*pro/i` |

Fallback chains are auto-generated based on model type relationships.

## Collaboration Workflow

### 唤醒协议

```
@codingteam wake up              — 激活默认团队全体
@codingteam <team-name> wake up  — 激活指定团队
@codingteam <role>               — 激活指定角色
@codingteam 收工                 — 全员休眠
```

### 调度方式

```javascript
// Spawn by agent ID
sessions_spawn({
  task: "Implement user auth API",
  agentId: "backend"        // default team
  // agentId: "alpha-backend"  // named team
})
```

## File Structure

```
skills/coding-team-setup/
├── SKILL.md               # This file
├── README.md              # Public description
├── clawhub.yaml           # ClawHub metadata
├── config/
│   └── roles.json         # Role templates + workflow templates + model types
├── templates/
│   └── SOUL-template.md   # SOUL.md template
└── wizard/
    └── setup.js           # Interactive setup wizard (v2.0)
```

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `agents_list` 只显示 main | `allowAgents` 缺少 agent ID | 重新运行向导或手动添加 |
| Spawn 超时 | Rate Limit / 模型不可用 | 检查 fallback 链 |
| 多团队 ID 冲突 | 未使用 --team 参数 | 用 `--team <name>` 区分 |
| Workspace 文件缺失 | 手动删除了目录 | 重新运行向导 |

## Lessons Learned

1. **`allowAgents` 必须在 main agent 的 `subagents` 下** — 不是 `defaults.subagents`
2. **模型 ID 必须完整** — 包含 provider 前缀
3. **Gateway 必须重启** — 修改 openclaw.json 后 `openclaw gateway restart`
4. **并发控制** — 同时 spawn 太多会触发 Rate Limit，建议分批
5. **团队前缀** — 多团队时 agent ID 自动带前缀，spawn 时要用完整 ID
