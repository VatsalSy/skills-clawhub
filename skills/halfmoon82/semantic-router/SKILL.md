---
name: semantic-router
description: Auto-routing skill with configurable model pools and task type matching. Includes interactive setup wizard for customizing pools to your available models.
version: 2.0.0
author: halfmoon82
tags: [semantic, routing, model-pools, task-classification, fallback]
---

# Semantic Router

**ClawHub**: https://clawhub.ai/halfmoon82/semantic-router  
**Version**: 2.0.0

Auto-routing skill with configurable model pools and task type matching. Includes interactive setup wizard for customizing pools to your available models.

## 🆕 Setup Wizard (New in v2.0)

Configure your model pools interactively:

```bash
# Run the setup wizard
python3 ~/.openclaw/workspace/skills/semantic-router/scripts/setup_wizard.py
```

**Wizard Steps:**
1. **Define Task Types** - Specify your main task categories
2. **Scan Available Models** - Automatically detect your configured models
3. **Get Smart Recommendations** - AI-suggested pool configurations
4. **Customize & Confirm** - Modify and approve your setup

## Quick Start

```bash
# Run semantic check
python3 ~/.openclaw/workspace/skills/semantic-router/scripts/semantic_check.py "帮你写一段代码" "Highspeed"

# Output:
# {"priority": "P1", "action": "开发任务", "model": "openai-codex/gpt-5.3-codex", "need_reset": true}
```

## Two-Step Detection (强制规范)

### Step 1: Semantic Continuity Check

判断用户输入与当前会话的语义关联性。

**延续信号 (B分支) → 跳过 Step 2：**
- 明确延续词："继续"、"接着"、"刚才"、"下一步"、"然后呢"
- 指代前文：使用"这个"、"那个"、"它"等指代当前话题
- 逻辑接续：回答或追问与前文直接相关内容

**新会话信号 → 执行 Step 2：**
- 话题切换：全新主题
- 领域切换：从开发切换到查询
- 明确问候："Hi"、"在吗"、"hello"

### Step 2: Task Type & Model Pool Selection

**三池架构：**

| 池 | 任务类型 | Primary | Fallback 1 | Fallback 2 |
|---|---------|---------|------------|-------------|
| **Highspeed** | 信息检索、网页搜索 | openai/gpt-4o-mini | glm-4.7-flashx | MiniMax-M2.5 |
| **Intelligence** | 开发、自动化、系统运维 | openai-codex/gpt-5.3-codex | kimi-k2.5 | MiniMax-M2.5 |
| **Humanities** | 内容生成、多模态、问答 | openai/gpt-4o | kimi-k2.5 | MiniMax-M2.5 |

### 关键词优先级矩阵

| 优先级 | 类型 | 关键词示例 | 动作 |
|--------|------|------------|------|
| **P0** | 延续 | 继续、接着、刚才、下一步 | 强制延续 |
| **P1** | 开发 | 开发、写代码、调试、修复、部署 | Intelligence 池 |
| **P2** | 查询 | 查一下、搜索、找、天气 | Highspeed 池 |
| **P3** | 内容 | 写文章、总结、解释、教育 | Humanities 池 |
| **P4** | 新会话 | hi、在吗、hello | 高速池默认 |

## Force Trigger via Message Injector

通过 message injector 插件强制每次消息都触发语义检查：

```json
{
  "plugins": {
    "entries": {
      "message-injector": {
        "enabled": true,
        "trigger": "always",
        "script": "python3 ~/.openclaw/workspace/skills/semantic-router/scripts/semantic_check.py"
      }
    }
  }
}
```

## Fallback 回路 (半自动化)

所有子代理统一使用 Primary → Fallback1 → Fallback2 回路：

```
主模型失败 (429/Timeout/Error)
    ↓
Fallback 1 (同池或跨池)
    ↓
Fallback 2 (跨池)
    ↓
全部失败 → 暂停 → 报告主代理
```

**当前实现**：
- 脚本自动检测任务类型并输出 `fallback_chain`
- Agent 读取 `fallback_chain` 并自动执行切换
- 回切机制：每2小时自动回切到主模型

**回切机制**：
- 每2小时自动回切到主模型
- 记录 fallback 到 `memory/model-fallback.log`

## Usage Examples

### 1. 基础检测
```bash
python3 semantic_check.py "查一下天气" "Intelligence"
# Output: {"branch": "C", "task_type": "info_retrieval", "pool": "Highspeed", "primary_model": "openai/gpt-4o-mini", ...}
```

### 2. 带上下文的检测
```bash
python3 semantic_check.py "继续" "Intelligence" "帮我写个函数" "谢谢"
# Output: {"branch": "B", "task_type": "continue", ...} # 保持当前池
```

### 3. Fallback 模式 (手动指定模型链)
```bash
python3 semantic_check.py --fallback openai-codex/gpt-5.3-codex kimi-k2.5 minimax-cn/MiniMax-M2.5
# Output: {"attempted": [...], "success": bool, "current_model": str}
```

## Configuration

Edit `config/pools.json` to customize model pools:

```json
{
  "Intelligence": {
    "name": "智能池",
    "primary": "openai-codex/gpt-5.3-codex",
    "fallback_1": "kimi-k2.5",
    "fallback_2": "minimax-cn/MiniMax-M2.5"
  },
  "Highspeed": {
    "name": "高速池", 
    "primary": "openai/gpt-4o-mini",
    "fallback_1": "glm-4.7-flashx",
    "fallback_2": "minimax-cn/MiniMax-M2.5"
  }
}
```

Edit `config/tasks.json` to customize task type keywords:

```json
{
  "development": {
    "keywords": ["开发", "写代码", "编程"],
    "pool": "Intelligence"
  },
  "content_generation": {
    "keywords": ["写文章", "创作"],
    "pool": "Humanities"
  }
}
```

## Files

- `scripts/semantic_check.py` - Core script with auto-switch support
- `config/pools.json` - Model pool config
- `config/tasks.json` - Task type keywords
- `references/flow.md` - Detailed flow chart
