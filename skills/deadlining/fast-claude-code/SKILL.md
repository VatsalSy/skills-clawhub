---
name: fast-claude-code
description: >
  Claude Code 任务完成回调 Runtime。支持 Single / Interactive / Team 三种模式，
  通过回调机制自动通知任务完成，无需轮询。
  Use when: 需要运行 Claude Code 任务并在完成时获得通知。
  NOT for: 简单的文件读写（直接用 read/write 工具）。
metadata:
  {
    "openclaw": {
      "emoji": "⚡",
      "os": ["darwin", "linux"],
      "requires": {
        "bins": ["bash", "claude"],
        "anyBins": ["openclaw"],
        "optionalBins": ["tmux", "jq"]
      }
    }
  }
---

# Fast Claude Code ⚡

Claude Code 任务完成自动通知 Runtime。

## 快速决策树

```
用户任务需要 Claude Code？
├─ 是 → 任务类型？
│   ├─ 一次性任务（单个文件/简单操作）→ Single 模式
│   ├─ 需要多轮对话/长时间运行 → Interactive 模式
│   └─ 需要多 Agent 协作/复杂分析 → Team 模式
└─ 否 → 不使用此 skill
```

## 三种模式选择指南

### Single 模式（一次性任务）

**使用场景**：
- 单个文件的重构/修改
- 简单的代码审查
- 一次性分析任务

**调用方式**：
```bash
{baseDir}/bin/fast-claude-code.sh single \
  --task "任务描述" \
  --project "/path/to/project" \
  --permission-mode auto
```

**参数**：
- `--task`（必需）：任务描述
- `--project`（必需）：项目路径
- `--permission-mode`（可选）：`auto`（默认）或 `plan`

**返回**：
- 任务完成后自动回调
- 回调包含任务输出

### Interactive 模式（长时运行/多轮对话）

**使用场景**：
- 需要多轮对话的任务
- 长时间运行的会话
- 需要人工干预的复杂任务

**调用方式**：
```bash
{baseDir}/bin/fast-claude-code.sh interactive \
  --project "/path/to/project" \
  --label "session-name"
```

**参数**：
- `--project`（必需）：项目路径
- `--label`（必需）：会话标识符
- `--task`（可选）：初始任务
- `--permission-mode`（可选）：`auto`（默认）或 `plan`

**返回**：
- 会话创建成功
- 后续通过 `send-task` 发送任务，每次完成都会回调

**发送后续任务**：
```bash
{baseDir}/bin/fast-claude-code.sh send-task \
  --session "session-name" \
  --task "后续任务描述"
```

### Team 模式（多 Agent 协作）

**使用场景**：
- 复杂的代码审查（多视角）
- 需要并行分析的任务
- 架构决策（需要辩论）
- 性能瓶颈分析（跨域）

**模板选择**：

| 模板 | 适用场景 | 判断关键词 |
|------|----------|-----------|
| `parallel-review` | 代码审查 | "审查"、"安全"、"性能"、"测试" |
| `competing-hypotheses` | 问题诊断 | "调试"、"问题"、"原因"、"为什么" |
| `fullstack-feature` | 功能开发 | "开发"、"实现"、"功能"、"全栈" |
| `architecture-decision` | 架构决策 | "架构"、"选择"、"对比"、"决策" |
| `bottleneck-analysis` | 性能分析 | "慢"、"性能"、"瓶颈"、"优化" |
| `inventory-classification` | 批量处理 | "分析"、"分类"、"评估"（多个独立项） |

**调用方式**：
```bash
{baseDir}/bin/fast-claude-code.sh team \
  --project "/path/to/project" \
  --template "模板名称" \
  --task "任务描述"
```

**参数**：
- `--project`（必需）：项目路径
- `--template`（必需）：模板名称
- `--task`（必需）：任务描述
- `--permission-mode`（可选）：`auto`（默认）或 `plan`

**超时设置**（根据任务复杂度调整）：

| 复杂度 | 超时设置 | 判断依据 |
|--------|----------|----------|
| 简单 | 不设置（默认 1h） | 单文件、单模块 |
| 中等 | 不设置（默认 1h） | 少量文件、标准任务 |
| 复杂 | `TEAM_TIMEOUT=7200` | 多模块、跨功能 |
| 超复杂 | `TEAM_TIMEOUT=10800` | 全项目、架构级 |

**判断依据**：
- 包含"整个项目"、"所有模块"、"全栈" → 考虑 2-3h
- 包含"重构"、"迁移"、"架构" → 考虑 2h
- 单文件/单功能 → 默认 1h

**返回**：
- Team 完成后自动回调
- 回调包含所有 Agent 的输出文件
- 输出文件格式：
  - `parallel-review`: findings-*.md + synthesis-*.md
  - `competing-hypotheses`: hypothesis-*-investigation.md + root-cause-conclusion.md
  - `fullstack-feature`: *-implementation.md + integration-summary.md
  - `architecture-decision`: proposal-option-*.md + architecture-decision.md
  - `bottleneck-analysis`: *-analysis.md + root-cause-conclusion.md
  - `inventory-classification`: *-results.md + aggregated-results.md

## 回调消息格式

所有模式完成后的回调格式：

```
fast-claude-code:done | mode=<MODE> | task=<TASK_ID> | msg=<MESSAGE>

--- Response ---
<OUTPUT_CONTENT>
```

- **STATUS**: `done` | `error` | `progress`
- **MODE**: `single` | `interactive` | `team`
- **OUTPUT_CONTENT**:
  - Single: 任务输出
  - Interactive: 任务输出
  - Team: 所有输出文件的内容

## 调用示例

### 示例 1：代码重构（Single）
```
用户：帮我重构 auth.js 的 JWT 验证逻辑
→ 调用 Single 模式
```

### 示例 2：多轮分析（Interactive）
```
用户：分析这个项目，然后重构核心模块
→ 调用 Interactive 模式，发送初始任务
→ 后续可发送更多任务
```

### 示例 3：安全审查（Team）
```
用户：审查整个项目的安全性
→ 判断：需要多视角分析
→ 选择模板：parallel-review
→ 调用 Team 模式
→ 超时：默认 1h（单个审查任务）
```

### 示例 4：架构决策（Team）
```
用户：我们应该用 PostgreSQL 还是 MongoDB？
→ 判断：需要架构级别的决策分析
→ 选择模板：architecture-decision
→ 调用 Team 模式
→ 超时：默认 1h
```

### 示例 5：复杂功能开发（Team）
```
用户：实现完整的用户认证系统（前端+后端+测试）
→ 判断：全栈功能，涉及多个模块
→ 选择模板：fullstack-feature
→ 调用 Team 模式
→ 超时：设置 3h（超复杂任务）
→ TEAM_TIMEOUT=10800 {baseDir}/bin/fast-claude-code.sh team ...
```

## 重要提示

1. **环境变量**：Team 模式需要 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
2. **依赖检查**：调用前确保 `claude` 命令可用
3. **超时设置**：根据任务复杂度智能调整 TEAM_TIMEOUT
4. **模板选择**：根据任务关键词自动选择最合适的模板
5. **回调处理**：监听回调消息，任务完成后会自动通知
