---
name: moltbot-plugin-2do
description: Create tasks from natural language and send to 2Do app via email. Use when user wants to add a task, create a todo, or set a reminder.
emoji: ✅
version: 1.0.0
author: chuckiefan
homepage: https://github.com/chuckiefan/moltbot-plugin-2do
metadata:
  {"openclaw": {"requires": {"env": ["TWODO_EMAIL", "SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS"], "bins": ["node"]}}}
---

# 2Do Task Email

通过自然语言创建任务并自动发送到你的 2Do app。

## 使用方式

### 基本用法

用户说: "添加任务：明天下午3点开会"

执行:
```bash
bash {baseDir}/scripts/send-task.sh --raw "添加任务：明天下午3点开会"
```

### 指定列表

用户说: "添加任务到工作列表：完成项目报告"

执行:
```bash
bash {baseDir}/scripts/send-task.sh --raw "添加任务到工作列表：完成项目报告"
```

### 指定标签

用户说: "添加任务：买菜，标签是家务和购物"

执行:
```bash
bash {baseDir}/scripts/send-task.sh --raw "添加任务：买菜，标签是家务和购物"
```

### 使用结构化参数

如果已从用户输入中提取了任务信息，可以直接传递结构化参数:

```bash
bash {baseDir}/scripts/send-task.sh --title "完成季度报告" --list "工作" --tags "紧急,财务"
```

## 参数说明

| 参数 | 说明 | 必需 |
|------|------|------|
| `--raw` | 原始自然语言输入，自动解析 | 与 --title 二选一 |
| `--title` | 任务标题 | 与 --raw 二选一 |
| `--list` | 目标列表名 | 否 |
| `--tags` | 标签，逗号分隔 | 否 |

## 输出

成功时输出: `✅ 任务已发送到 2Do: {任务标题}`

失败时输出错误信息并以非零状态码退出。

## 配置

需要以下环境变量:

- `TWODO_EMAIL` - 2Do 中配置的接收邮箱地址
- `SMTP_HOST` - SMTP 服务器地址（如 smtp.gmail.com）
- `SMTP_PORT` - SMTP 端口（587 或 465）
- `SMTP_USER` - SMTP 用户名
- `SMTP_PASS` - SMTP 密码（推荐使用应用专用密码）
