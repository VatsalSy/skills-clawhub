# use-openclaw-manual - OpenClaw 文档管理技能

## 描述

在配置 OpenClaw 前自动查阅本地官方文档，确保配置操作准确、规范。支持文档同步、快速搜索、文件阅读。

**特点**: 零依赖、快速、简洁 —— 直接使用脚本，无需通过 clawhub CLI 调用。

## 核心功能

| 功能 | 命令 | 说明 |
|------|------|------|
| 文档同步 | `--init` / `--sync` | 从 GitHub 同步官方文档 |
| 内容搜索 | `--search <词>` | 搜索文档内容 |
| 标题搜索 | `--title <词>` | 搜索文档标题 |
| 文件搜索 | `--file <词>` | 搜索文件名 |
| 阅读文档 | `--read <文件>` | 阅读指定文档 |
| 统计信息 | `--stats` | 显示文档统计 |

## 快速开始

### 1. 安装（可选）

通过 ClawHub 安装技能：

```bash
clawhub skill install use-openclaw-manual
```

或直接克隆使用：

```bash
# 技能目录：~/.openclaw/workspace/skills/use-openclaw-manual/
```

### 2. 初始化文档

首次使用需同步文档：

```bash
cd ~/.openclaw/workspace/skills/use-openclaw-manual
./run.sh --init
```

**同步内容**:
- 从 `github.com/openclaw/openclaw/docs/` 克隆
- 保存到 `~/.openclaw/workspace/docs/openclaw_manual/`
- 约 700+ 文件，耗时约 30 秒

### 3. 使用技能

```bash
# 搜索内容
./run.sh --search "agent binding"

# 搜索标题
./run.sh --title "cron"

# 搜索文件名
./run.sh --file "gateway"

# 阅读文档
./run.sh --read concepts/agent.md

# 查看统计
./run.sh --stats
```

## 环境变量（可选）

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `OPENCLAW_MANUAL_PATH` | `~/.openclaw/workspace/docs/openclaw_manual` | 文档存储路径 |
| `LAST_COMMIT_FILE` | `$OPENCLAW_MANUAL_PATH/.last-docs-commit` | 同步基线文件路径 |
| `DOC_UPDATE_LOG` | 技能目录内 `docs-update.log` | 日志文件路径 |

## 前置依赖

确保系统已安装以下工具：

| 工具 | 用途 | 检查命令 |
|------|------|----------|
| `git` | 克隆文档仓库 | `git --version` |
| `curl` | 调用 GitHub API | `curl --version` |
| `python3` | 解析 JSON 响应 | `python3 --version` |

## 调用方式对比

### ✅ 推荐：直接执行脚本

```bash
# 快速、无额外开销
./run.sh --search "binding"
./scripts/search-docs.sh --search "binding"
./scripts/sync-docs.sh --sync
```

**优点**: 
- 启动快（~0.8 秒）
- 零额外依赖
- 输出简洁，便于 Agent 处理
- 可管道组合

### ⚠️ 可选：通过 clawhub 调用

```bash
clawhub skill run use-openclaw-manual --search "binding"
```

**缺点**: 
- 启动慢（~3 秒，含 CLI 加载）
- 依赖 clawhub CLI
- 输出格式化，不利于程序处理

## Agent 集成

在 AGENTS.md 中添加：

```markdown
## 文档查阅

配置 OpenClaw 前必须查阅文档：

1. 搜索相关文档
   ```bash
   ~/.openclaw/workspace/skills/use-openclaw-manual/run.sh --search "<关键词>"
   ```

2. 阅读具体文档
   ```bash
   ./run.sh --read <文件路径>
   ```

3. 配置方案必须引用文档来源
   ```
   根据 docs/openclaw_manual/gateway/config.md 第 45 行...
   ```
```

## 输出格式

### 搜索输出

```
🔍 搜索内容：'binding'
📁 路径：/home/claw/.openclaw/workspace/docs/openclaw_manual
---
channels/channel-routing.md:62
  1. **Exact peer match** (`bindings` with `peer.kind` + `peer.id`).

automation/cron-jobs.md:105
  - optional **agent binding** (`agentId`): run the job under a specific agent
---
共 15 个匹配（显示前 10 个）
```

### 统计输出

```
📊 文档统计
---
路径：/home/claw/.openclaw/workspace/docs/openclaw_manual

文件：713 个 (Markdown: 689 个)
目录：44 个
总行数：45230
总词数：312450

主要目录:
  📁 automation/ (89 个文件)
  📁 channels/ (52 个文件)
  📁 concepts/ (34 个文件)
  ...
```

## 文件结构

```
use-openclaw-manual/
├── SKILL.md              # 技能文档
├── run.sh                # 主入口脚本
├── LICENSE.txt           # MIT 许可证
├── docs-update.log       # 同步日志（运行时生成）
├── _meta.json            # ClawHub 元数据
└── scripts/
    ├── sync-docs.sh      # 文档同步脚本
    └── search-docs.sh    # 文档搜索脚本
```

## 高级用法

### 管道组合

```bash
# 搜索并提取文件名
./run.sh --search "binding" | grep "\.md:" | cut -d: -f1 | sort -u

# 搜索并统计
./run.sh --search "agent" | grep -c "^  "
```

### 定期检查更新

```bash
# 添加到 cron，每日检查
0 9 * * * cd ~/.openclaw/workspace/skills/use-openclaw-manual && ./run.sh --sync
```

### 自定义文档路径

```bash
export OPENCLAW_MANUAL_PATH=/custom/path/docs
./run.sh --search "binding"
```

## 故障排除

### 文档未同步

```
❌ 文档未同步，请先运行：./run.sh --init
```

**解决**: 运行初始化命令

### 同步失败

```
❌ 获取 commit 失败，请检查网络连接
```

**解决**: 检查网络连接，确保可访问 GitHub API

### 搜索无结果

```
未找到匹配项
```

**解决**: 尝试其他关键词，或使用 `--stats` 查看文档结构

## 许可证

MIT License - 与 OpenClaw 相同

## 更新日志

### 1.0.2 (2026-03-11)
- 重构：简化调用方式，直接执行脚本
- 移除：clawhub CLI 依赖（改为可选）
- 优化：输出格式更简洁，便于 Agent 处理
- 修复：元数据声明不一致问题

### 1.0.1 (2026-03-10)
- 添加：前置依赖和环境变量声明
- 修复：元数据与实际依赖不一致问题

### 1.0.0 (2026-03-05)
- 初始版本
