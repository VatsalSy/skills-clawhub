---
name: crawl-from-x
description: X/Twitter 帖子抓取与管理工具。用于管理关注的 X 用户列表，并自动抓取这些用户当天发布的最新帖子 URL 和完整内容。支持用户列表的增删改查、批量抓取、容错重试、详细日志记录、Markdown 格式导出。使用场景：需要定期跟踪特定 X 用户的最新动态、收集特定话题相关的帖子、社交媒体监控等。
---

# Crawl From X

X/Twitter 帖子抓取与管理工具。

## 安装

**通过 ClawHub 安装（推荐）：**
```bash
npx clawhub@latest install crawl-from-x
```

安装后，文件会位于：
- `$CLAWD/skills/crawl-from-x/scripts/craw_hot.py` - 主脚本
- `$CLAWD/skills/crawl-from-x/users.txt` - 用户列表
- `$CLAWD/skills/crawl-from-x/results/` - 抓取结果

---

## 新功能 ✨

**v2.4 新增：**
- 🔒 进程锁机制：防止多个实例同时运行，避免重复抓取
- 🛑 智能检测：检测到已有实例时友好提示
- 🧹 自动清理：程序退出时自动清理锁文件

**v2.3 功能：**
- 💾 增量写入：每抓取一个用户就立即写入文件，避免故障导致数据丢失
- 📊 实时进度：文件中显示当前进度 [X/Y]，方便监控
- 🔒 数据安全：使用 `flush()` 立即写入磁盘，确保数据不丢失

**v2.2 功能：**
- ⚡ 智能跳过：当用户24小时内没有发新帖时，不再反复重试，直接处理下一个用户
- 🎯 精准重试：使用 `NoPostsFoundError` 异常区分"真正失败"和"没有帖子"的情况

**v2.1 功能：**
- 🔄 浏览器自动恢复：检测到 `tab not found` 错误时自动重启浏览器服务并继续任务
- 🛡️ 智能重试：区分浏览器错误和网络错误，采用不同的恢复策略
- ⚡ 任务连续性：重启后无需手动干预，自动继续抓取

**v2.0 功能：**
- 📝 完整内容获取：通过 fxtwitter API 和 syndication API 获取帖子完整内容
- 📄 Markdown 导出：自动生成格式化的 Markdown 文件
- 🎬 媒体支持：自动提取图片、视频链接
- 📊 互动数据：点赞、转发、浏览、回复数
- 📰 X Article 支持：完整提取长文章内容

---

## 概述

Crawl From X 是一个专注于 X (Twitter) 帖子抓取的自动化工具，可以：

- **管理用户列表**：增删改查需要关注的 X 用户名
- **批量抓取**：自动访问用户主页，抓取当天发布的所有帖子 URL
- **完整内容获取**：通过 fxtwitter API 和 syndication API 获取帖子完整内容
- **Markdown 导出**：自动生成格式化的 Markdown 文件，包含帖子文本、媒体和互动数据
- **容错机制**：浏览器连接失败自动重试，网络故障随机延迟后重试（最多 5 次）
- **详细日志**：完整的操作日志记录，便于调试和追踪

---

## 快速开始

### 1. 管理用户列表

**进入脚本目录：**
```bash
cd skills/crawl-from-x/scripts
```

**添加用户：**
```bash
python3 craw_hot.py add vista8
```

**删除用户：**
```bash
python3 craw_hot.py remove vista8
```

**列出所有用户：**
```bash
python3 craw_hot.py list
```

### 2. 抓取帖子

**抓取单个用户的当天帖子：**
```bash
python3 craw_hot.py crawl vista8
```

**抓取所有用户的当天帖子：**
```bash
python3 craw_hot.py crawl
```

### 3. 查看结果

抓取结果会自动保存到 `results/` 目录：
- `posts_YYYYMMDD_HHMMSS.txt` - URL 列表
- `posts_YYYYMMDD_HHMMSS.md` - 完整内容（Markdown 格式）

---

## 核心功能

### 内容获取 API

**fxtwitter API (主要)**
- URL: `https://api.fxtwitter.com/...`
- 优势：支持 X Article 长文章、媒体、完整互动数据

**syndication API (备用)**
- URL: `https://cdn.syndication.twimg.com/tweet-result?id=...`
- 优势：官方 API，稳定性高

**使用逻辑：**
1. 优先使用 fxtwitter API
2. 失败后使用 syndication API
3. 两次都失败则保留 URL 并标记为获取失败

### Markdown 输出格式

每个帖子包含：
- 标题和作者信息
- 发布时间和原文链接
- 完整文本内容
- 媒体文件（图片、视频）
- 互动数据（点赞、转发、浏览、回复）

X Article 长文章：
- 完整文章内容
- 标题结构化（h1/h2/h3）
- 封面图
- 修改时间

---

## 使用场景

### 定期跟踪行业动态

```bash
# 1. 添加关注的技术博主
python3 craw_hot.py add vista8
python3 craw_hot.py add elonmusk
python3 craw_hot.py add openai

# 2. 每天运行抓取
python3 craw_hot.py crawl

# 3. 查看 Markdown 结果
# 路径：results/posts_YYYYMMDD_HHMMSS.md
```

### 监控特定话题相关账号

```bash
# 编辑 users.txt
vim skills/crawl-from-x/users.txt

# 运行抓取
cd skills/crawl-from-x/scripts
python3 craw_hot.py crawl

# 查看 Markdown 文件
cat skills/crawl-from-x/results/posts_*.md
```

---

## 故障排查

### 多实例运行

**进程锁机制（v2.4+）：**

如果尝试启动多个 crawl-from-x 实例，会看到以下错误：
```
❌ Error: Another crawl-from-x instance is already running!
   Lock file: /path/to/.crawl-from-x.lock
   If you believe this is an error, delete the lock file and try again.
   Command: rm /path/to/.crawl-from-x.lock
```

**解决方案：**
1. 等待当前实例完成
2. 或删除锁文件手动强制启动（谨慎使用）

### 浏览器自动恢复（v2.1+）

**v2.1 新增自动恢复功能：**

当脚本检测到浏览器连接问题（如 `tab not found` 错误）时，会自动：
1. 🔧 重启浏览器服务（`openclaw browser stop` + `start`）
2. ⏳ 等待 30 秒让浏览器完全初始化
3. 🔄 自动重试刚才失败的操作
4. 📊 整个任务最多自动重启 10 次

**日志示例：**
```
[2026-02-28 11:04:10] [WARN] Detected 'tab not found' error, attempting recovery...
[2026-02-28 11:04:11] [INFO] Attempting browser service restart (1/2)...
[2026-02-28 11:04:11] [INFO] Stopping browser...
[2026-02-28 11:04:14] [INFO] Starting browser...
[2026-02-28 11:04:15] [INFO] Waiting 30s for browser to fully initialize...
[2026-02-28 11:04:45] [INFO] ✅ Browser service restarted successfully
[2026-02-28 11:04:46] [DEBUG] Attempt 2/5
```

**注意事项：**
- 自动恢复不会中断任务，脚本会在重启后继续抓取
- 如果重启 2 次后仍然失败，脚本会停止并记录错误
- 每次重启大约需要 30-35 秒（包含等待时间）

### 浏览器连接失败（手动处理）

如果自动恢复失败，可以手动处理：

```bash
# 检查状态
openclaw browser status

# 重启浏览器服务
openclaw gateway restart

# 重新运行抓取
cd skills/crawl-from-x/scripts
python3 craw_hot.py crawl
```

### 内容获取失败

查看 `craw_hot.log` 获取详细错误信息。常见原因：
- API 速率限制
- 帖子已被删除
- 私密账号

---

## 注意事项

1. **浏览器要求**：必须安装 OpenClaw 浏览器扩展
2. **登录状态**：浏览器必须登录 X 账号
3. **速率限制**：脚本已内置随机延迟（0.5-1.5秒）
4. **私密账号**：无法抓取私密账号内容

---

## 许可与支持

本技能是 OpenClaw 生态系统的一部分。

有问题？查看日志文件 `skills/crawl-from-x/craw_hot.log` 获取详细信息。
