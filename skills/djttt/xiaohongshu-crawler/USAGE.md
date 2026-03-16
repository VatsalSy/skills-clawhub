# 小红书爬虫 - 最终使用指南

## 📋 当前状态

| 功能 | 状态 | 说明 |
|------|------|------|
| 热门笔记抓取 | ✅ **可用** | 无需登录，已实现 |
| 反爬机制 | ✅ **已启用** | 随机延迟、频率限制 |
| 搜索功能 | ⚠️ **需 Cookie** | 需要有效的 Cookie |
| 笔记详情 | ⚠️ **需 Cookie** | 需要有效的 Cookie |
| 用户信息 | ⚠️ **需 Cookie** | 需要有效的 Cookie |

## 🚀 快速开始

### 1. 热门笔记抓取（无需登录）

```bash
cd skills/xiaohongshu-crawler

# 获取探索页热门笔记
node scripts/hot-notes.js explore 1 20

# 获取分类热门笔记
node scripts/hot-notes.js food 1 20        # 美食
node scripts/hot-notes.js fashion 1 20     # 时尚
node scripts/hot-notes.js tech 1 20        # 科技
node scripts/hot-notes.js travel 1 20      # 旅行

# JSON 格式输出
node scripts/hot-notes.js explore 1 20 json > notes.json
```

### 2. Cookie 管理

```bash
# 查看 Cookie 状态
node scripts/status.js

# 重新获取 Cookie
node scripts/get-cookie.js

# 测试 Cookie 是否有效
node scripts/test-cookie.js

# 查看详细信息
node scripts/test-cookie-detail.js
```

### 3. 搜索功能（需要有效 Cookie）

```bash
# 配置有效 Cookie 后使用
node scripts/search.js 手机测评 1 20
node scripts/search.js iPhone 15 2 10 json
```

### 4. 笔记详情（需要有效 Cookie）

```bash
node scripts/get-note.js 64bc4249000000001201df4d
node scripts/get-note.js 64bc4249000000001201df4d json
```

### 5. 用户信息（需要有效 Cookie）

```bash
node scripts/get-user.js 用户 ID 20
node scripts/get-user.js 用户 ID 20 json
```

## 🛡️ 反爬机制配置

配置文件 `config.json` 中的反爬设置：

```json
{
  "anti_crawl": {
    "enabled": true,
    "random_delay": {
      "min": 2000,
      "max": 8000
    },
    "human_behavior": {
      "enabled": true,
      "random_scroll": true,
      "mouse_movement": true
    },
    "rate_limit": {
      "max_requests_per_minute": 10,
      "max_requests_per_hour": 100
    }
  }
}
```

### 调整反爬策略

**更严格（更安全）：**
```json
{
  "random_delay": {
    "min": 3000,
    "max": 10000
  },
  "rate_limit": {
    "max_requests_per_minute": 5,
    "max_requests_per_hour": 50
  }
}
```

**更宽松（更快）：**
```json
{
  "random_delay": {
    "min": 1000,
    "max": 5000
  },
  "rate_limit": {
    "max_requests_per_minute": 15,
    "max_requests_per_hour": 150
  }
}
```

## 📊 状态查看

```bash
# 查看所有配置状态
node scripts/status.js

# 查看请求统计
node scripts/reset-counters.js
```

## 🔄 Cookie 更新

**建议每周更新一次 Cookie：**

1. 运行获取工具：
```bash
node scripts/get-cookie.js
```

2. 在浏览器中登录小红书

3. 登录后按 `Ctrl+C`

4. 复制导出的配置到 `config.json`

5. 启用 Cookie：
```json
{
  "cookie": {
    "enabled": true,
    "items": [...]
  }
}
```

6. 测试 Cookie：
```bash
node scripts/test-cookie.js
```

## 📝 实用示例

### 批量获取热门笔记

```bash
# 获取多个分类
node scripts/hot-notes.js explore 1 20 json > explore.json
node scripts/hot-notes.js food 1 20 json > food.json
node scripts/hot-notes.js fashion 1 20 json > fashion.json
node scripts/hot-notes.js tech 1 20 json > tech.json
```

### 导出数据格式

```json
{
  "category": "explore",
  "page": 1,
  "total": 20,
  "data": [
    {
      "note_id": "64bc4249000000001201df4d",
      "title": "在德国｜街头瞬间",
      "cover": "https://sns-webpic-qc.xhscdn.com/...",
      "user": {
        "nickname": "",
        "user_id": ""
      },
      "likes": "",
      "collects": "",
      "comments": "",
      "url": "https://www.xiaohongshu.com/explore/64bc4249000000001201df4d"
    }
  ]
}
```

### 查看请求历史

```bash
# 查看当前请求统计
node scripts/status.js
```

## ⚠️ 注意事项

1. **Cookie 有效期** - 通常 7 天左右，需要定期更新
2. **频率限制** - 本工具已内置频率限制，请勿关闭
3. **隐私保护** - 仅抓取公开内容，不要抓取用户隐私信息
4. **合规使用** - 遵守小红书用户协议
5. **不要提交 config.json** - 包含 Cookie 等敏感信息

## 🔧 故障排除

### 问题 1：搜索返回空结果

**原因**：Cookie 无效或未登录
**解决**：
1. 运行 `node scripts/test-cookie.js` 测试
2. 如果失败，重新运行 `node scripts/get-cookie.js`
3. 确保 `cookie.enabled: true`

### 问题 2：被限制访问

**原因**：请求频率过高
**解决**：
1. 检查 `anti_crawl.rate_limit` 配置
2. 增加 `random_delay` 的延迟时间
3. 降低请求频率

### 问题 3：找不到笔记元素

**原因**：页面结构变化
**解决**：
1. 检查页面是否正常加载
2. 更新脚本中的选择器
3. 可能需要更新反爬策略

## 📦 文件结构

```
xiaohongshu-crawler/
├── SKILL.md                 # 技能文档
├── README.md                # 详细使用指南
├── config.json             # 当前配置（包含 Cookie）
├── config.example.json     # 配置示例
├── lib/
│   ├── browser.js          # 浏览器核心
│   └── anti-crawl.js       # 反爬机制
└── scripts/
    ├── get-cookie.js       # Cookie 获取工具
    ├── test-cookie.js      # Cookie 测试
    ├── test-cookie-detail.js # Cookie 详细测试
    ├── status.js           # 状态查看
    ├── reset-counters.js   # 重置计数
    ├── hot-notes.js        # 热门笔记（无需登录）
    ├── search.js           # 搜索（需登录）
    ├── get-note.js         # 笔记详情（需登录）
    └── get-user.js         # 用户信息（需登录）
```

## 🎯 总结

**当前已实现：**
- ✅ 热门笔记抓取（无需登录）
- ✅ 完整的反爬机制
- ✅ Cookie 获取和管理
- ✅ 状态查看工具
- ✅ 多种输出格式（文本/JSON）

**可用功能：**
- ✅ 探索页热门笔记
- ✅ 分类热门笔记（美食、时尚、科技、旅行等）
- ✅ JSON 格式导出
- ✅ 请求频率限制

**需要 Cookie：**
- ⚠️ 搜索功能
- ⚠️ 笔记详情
- ⚠️ 用户信息

**建议：**
1. 定期更新 Cookie（每周一次）
2. 使用已实现的功能（热门笔记抓取）
3. 遵守反爬机制设置
4. 定期查看状态

---

**📌 提示**: 当前配置已经是最优方案，热门笔记功能可以完全满足需求。搜索功能建议获取有效 Cookie 后使用。
