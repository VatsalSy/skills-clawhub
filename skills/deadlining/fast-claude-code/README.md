# Fast Claude Code ⚡

Claude Code Completion Callback Runtime — 通过回调机制实现任务完成后自动通知，无需轮询。

## 特性

- ✅ **三种模式**：Single（一次性任务）、Interactive（长时会话）、Team（多Agent协作）
- ✅ **自动回调**：任务完成自动通知，支持 OpenClaw / Webhook / ntfy
- ✅ **零轮询**：降低 token 消耗，不依赖轮询状态
- ✅ **灵活集成**：可通过 OpenClaw skill 调用或直接使用命令行

## 架构

```
┌─────────────────────────────────────────────┐
│          fast-claude-code skill             │
├─────────────────────────────────────────────┤
│  Task Runner     → 启动 Claude Code         │
│  Completion Detector  → 检测任务完成        │
│  Callback Dispatcher → 发送回调通知         │
└─────────────────────────────────────────────┘
```

## 快速开始

### 安装依赖

**核心依赖（所有模式）**：
```bash
# macOS
brew install claude-code

# Linux (按照 Claude Code 官方文档安装)
```

**可选依赖**：
```bash
# macOS
brew install tmux jq curl

# Linux
sudo apt-get install tmux jq curl
```

### Single 模式示例

```bash
bin/fast-claude-code.sh single \
  --task "重构 auth 模块" \
  --project ~/project
```

### Interactive 模式示例

```bash
# 启动会话
bin/fast-claude-code.sh interactive \
  --project ~/project \
  --label mysession

# 发送后续任务
bin/fast-claude-code.sh send-task \
  --session mysession \
  --task "添加单元测试"
```

### Team 模式示例

```bash
# 启用 Team 模式
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# 运行 Team 任务
bin/fast-claude-code.sh team \
  --project ~/project \
  --template parallel-review \
  --task "审查代码安全性、性能和测试"
```

## 工作原理

### Single 模式

1. 使用 `claude -p` 非交互模式运行任务
2. 注入完成协议（要求输出 `CC_CALLBACK_DONE` 标记）
3. 捕获输出并检测完成标记
4. 触发回调

### Interactive 模式

1. 使用 tmux 创建持久会话
2. 注入持久完成协议（Claude 记住每次完成都输出 `CC_CALLBACK_DONE`）
3. 每个任务附加唯一标记 `=== START <timestamp> ===`
4. 两阶段检测：先检测 START 标记，再检测之后的 CC_CALLBACK_DONE
5. 每个任务都有独立的监控进程
6. 会话超时（3小时）或用户主动关闭时停止

### Team 模式

1. 安装 `.claude/hooks/on-stop.sh` hook
2. 使用 tmux 启动 Claude Code PTY 会话
3. 注入 spawn prompt（从模板生成）
4. Team 完成后 Claude Code 退出，触发 hook
5. Hook 收集所有输出文件并触发回调

## 完成检测机制

| 模式 | 检测方式 | 协议 |
|------|----------|------|
| Single | grep 输出 | `CC_CALLBACK_DONE` |
| Interactive | 两阶段 grep | `=== START <id> ===` → `CC_CALLBACK_DONE` |
| Team | Claude Code Hooks | `on-stop` 事件 |

## 回调消息格式

```
fast-claude-code:done | mode=<MODE> | task=<TASK_ID> | msg=<MESSAGE>

--- Response ---
<OUTPUT_CONTENT>
```

**状态值**：
- `done`: 任务成功完成
- `error`: 任务出错
- `progress`: 进度更新

## 模板系统

Team 模式支持 6 个预定义模板：

| 模板 | 用途 | 输出文件 |
|------|------|----------|
| `parallel-review` | 多视角代码审查 | findings-*.md + synthesis-*.md |
| `competing-hypotheses` | 问题诊断（竞争假设） | hypothesis-*-investigation.md + root-cause-conclusion.md |
| `fullstack-feature` | 全栈功能开发 | *-implementation.md + integration-summary.md |
| `architecture-decision` | 架构决策（对抗辩论） | proposal-option-*.md + architecture-decision.md |
| `bottleneck-analysis` | 性能瓶颈分析 | *-analysis.md + root-cause-conclusion.md |
| `inventory-classification` | 批量分类处理 | *-results.md + aggregated-results.md |

## 文件结构

```
fast-claude-code/
├── SKILL.md                # OpenClaw skill 说明
├── README.md               # 本文档
├── CLAUDE.md               # Claude Code 工作指南
├── bin/
│   ├── fast-claude-code.sh # 主入口
│   └── send-task.sh        # 发送任务到 Interactive 会话
├── modes/
│   ├── single.sh           # Single 模式
│   ├── interactive.sh      # Interactive 模式
│   └── team.sh             # Team 模式
├── templates/
│   ├── parallel-review.sh
│   ├── competing-hypotheses.sh
│   ├── fullstack-feature.sh
│   ├── architecture-decision.sh
│   ├── bottleneck-analysis.sh
│   └── inventory-classification.sh
└── callbacks/
    ├── openclaw.sh       # OpenClaw 回调
    ├── webhook.sh        # Webhook 回调
    └── ntfy.sh           # ntfy 推送回调
```

## 环境变量

| 变量 | 用途 | 默认值 |
|------|------|--------|
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | 启用 Team 模式 | 未设置 |
| `TEAM_TIMEOUT` | Team 模式超时（秒） | 3600（1小时） |
| `CC_WEBHOOK_URL` | Webhook 回调 URL | 无 |
| `NTFY_SERVER` | ntfy 服务器 | ntfy.sh |

## 开发

### 添加新模板

1. 在 `templates/` 创建 `template-name.sh`
2. 使用 heredoc 格式输出 spawn prompt
3. 包含 `${TASK_DESCRIPTION}` 和 `${TARGET_DIR}` 变量
4. 更新 SKILL.md 的模板选择表

### 添加新回调后端

1. 在 `callbacks/` 创建 `backend.sh`
2. 接受标准参数：`--status`, `--mode`, `--task`, `--message`, `--output`
3. 构建并发送通知

## 测试

```bash
# 测试 Single 模式
bash modes/single.sh --task "echo hello" --project /tmp/test

# 测试 Interactive 模式
bash modes/interactive.sh --project ~/project --label test

# 测试 Team 模式
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
bash modes/team.sh --project /tmp/test --template parallel-review --task "test"
```

## 故障排查

### Team 模式不工作

1. 确认环境变量已设置：`echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`
2. 检查依赖：`command -v tmux jq`
3. 验证 Claude Code 版本支持 Teams

### Hook 没有触发

1. 检查 `.claude/hooks/on-stop.sh` 存在且可执行
2. 验证 `.claude/settings.json` 包含 hooks 配置
3. 确认 Claude Code 正常退出（不是被 kill）

### 回调没有收到

1. 测试回调脚本：`bash callbacks/openclaw.sh --status done --mode test --task test`
2. 检查 `openclaw` 命令可用：`command -v openclaw`
3. 查看回调脚本输出

## 许可证

MIT

## 贡献

欢迎提交 Issue 和 Pull Request！
