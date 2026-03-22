---
name: continuous-evolution
description: 持续进化系统 - 每次任务后记录经验、分析原因、归档到经验库，实现持续自我改进。
author: Automaton
metadata:
  openclaw:
    emoji: 🔄
    tags:
      - evolution
      - learning
      - self-improvement
---

# 🔄 持续进化系统

## 核心理念

**每一次任务执行，都是进化的机会！**

---

## 🎯 进化机制

### 1. 经验记录 (每次任务后)
```
任务完成
    ↓
记录执行经验
    ↓
分析成功/失败原因
    ↓
归档到经验库
```

### 2. 定期回顾 (每周/每月)
- 提取成功模式
- 识别失败根因
- 更新决策框架

### 3. 知识沉淀
- 经验 → 原则
- 原则 → 规则
- 规则 → 自动化

---

## 📋 使用方法

### 手动触发
```bash
# 记录一次进化
/evolve log "今天学会了 XXX"

# 回顾经验
/evolve review --days 7
```

### 自动触发
- 每次任务完成后自动记录
- 每日 2AM 自动回顾
- 每周一 10AM 生成进化报告

---

## 📁 文件结构

```
continuous-evolution/
├── SKILL.md              # 本文件
├── experience-log.md     # 经验日志
├── patterns.md           # 成功模式
└── anti-patterns.md      # 失败模式
```

---

**作者**: Automaton  
**许可证**: MIT  
**最后更新**: 2026-03-20
