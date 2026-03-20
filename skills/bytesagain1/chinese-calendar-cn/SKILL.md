---
version: "3.0.0"
name: Chinese Calendar
description: "Look up Chinese lunar calendar dates, festivals, and auspicious days. Use when checking holidays, converting lunar dates, or planning traditional events."
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
---

# Chinese Calendar Cn — 生产力与日程管理工具

全功能的日程规划与任务追踪工具。添加任务、制定计划、追踪进度、设置提醒、查看时间线、生成报告 —— 全部通过命令行完成。

A full-featured productivity and scheduling toolkit. Add tasks, plan ahead, track progress, set reminders, review streaks, prioritize, archive, tag, view timelines, generate reports, and run weekly reviews — all from the command line.

## Commands

| 命令 | 说明 |
|------|------|
| `chinese-calendar-cn add <input>` | 添加新任务或日程条目 |
| `chinese-calendar-cn plan <input>` | 创建或记录计划 |
| `chinese-calendar-cn track <input>` | 追踪进度或习惯 |
| `chinese-calendar-cn review <input>` | 记录复盘内容 |
| `chinese-calendar-cn streak <input>` | 记录连续打卡/习惯追踪 |
| `chinese-calendar-cn remind <input>` | 设置提醒事项 |
| `chinese-calendar-cn prioritize <input>` | 标记或调整优先级 |
| `chinese-calendar-cn archive <input>` | 归档已完成的条目 |
| `chinese-calendar-cn tag <input>` | 给条目添加标签 |
| `chinese-calendar-cn timeline <input>` | 查看或添加时间线条目 |
| `chinese-calendar-cn report <input>` | 生成或记录报告 |
| `chinese-calendar-cn weekly-review <input>` | 执行每周复盘 |
| `chinese-calendar-cn stats` | 显示所有日志的汇总统计 |
| `chinese-calendar-cn export <fmt>` | 导出数据（json、csv、txt 格式） |
| `chinese-calendar-cn search <term>` | 跨所有日志搜索关键词 |
| `chinese-calendar-cn recent` | 显示最近 20 条活动记录 |
| `chinese-calendar-cn status` | 健康检查 — 版本、数据量、最后活动 |
| `chinese-calendar-cn help` | 显示帮助 |
| `chinese-calendar-cn version` | 显示版本号 |

所有数据命令（add、plan、track、review、streak、remind、prioritize、archive、tag、timeline、report、weekly-review）工作方式一致：
- **带参数：** 保存带时间戳的条目到对应日志文件，并记录到 history.log
- **不带参数：** 显示该命令日志的最近 20 条记录

## Data Storage / 数据存储

- **存储位置：** `~/.local/share/chinese-calendar-cn/`
- 每个命令写入独立的日志文件（如 `add.log`、`plan.log`、`remind.log`）
- 统一的 `history.log` 跟踪所有命令的活动
- 导出支持 JSON、CSV、纯文本三种格式
- 所有数据本地存储 — 无外部 API、无网络请求

## Requirements / 系统要求

- bash 4+（使用 `set -euo pipefail`）
- 标准 Unix 工具（`date`、`wc`、`du`、`grep`、`head`、`tail`）
- 无需外部依赖或 API 密钥

## When to Use / 使用场景

1. **日常任务管理** — 用 `add` 记录待办事项，用 `prioritize` 设置优先级，用 `archive` 归档已完成任务。
2. **习惯追踪与打卡** — 用 `streak` 和 `track` 记录每日习惯完成情况，通过 `stats` 查看坚持天数。
3. **项目计划与复盘** — 用 `plan` 制定阶段目标，用 `review` 和 `weekly-review` 定期回顾执行情况。
4. **时间线管理** — 用 `timeline` 记录关键里程碑，用 `report` 生成阶段性总结。
5. **团队协作数据共享** — 用 `export` 将所有记录导出为 JSON/CSV/TXT，方便分享或导入其他工具。

## Examples / 使用示例

```bash
# 添加一个任务
chinese-calendar-cn add "完成 Q1 季度报告"

# 制定计划
chinese-calendar-cn plan "本周目标：完成前端重构 + 写单元测试"

# 追踪进度
chinese-calendar-cn track "前端重构完成 60%"

# 设置提醒
chinese-calendar-cn remind "周五下午 3 点团队会议"

# 标记优先级
chinese-calendar-cn prioritize "P0: 修复生产环境内存泄漏"

# 记录连续打卡
chinese-calendar-cn streak "晨跑 Day 15"

# 添加标签
chinese-calendar-cn tag "重构任务 #frontend #refactor"

# 每周复盘
chinese-calendar-cn weekly-review "本周完成 8 个任务，2 个延期"

# 查看统计
chinese-calendar-cn stats

# 导出为 JSON
chinese-calendar-cn export json

# 搜索关键词
chinese-calendar-cn search "重构"

# 查看最近活动
chinese-calendar-cn recent

# 系统状态检查
chinese-calendar-cn status
```

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
