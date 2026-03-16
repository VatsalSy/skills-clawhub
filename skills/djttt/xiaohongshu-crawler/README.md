# 小红书爬虫使用指南

## 📋 功能概览

| 功能 | 需要登录 | 状态 |
|------|---------|------|
| 热门笔记 | ❌ 否 | ✅ 可用 |
| 搜索笔记 | ✅ 是 | ⚠️ 需 Cookie |
| 笔记详情 | ✅ 是 | ⚠️ 需 Cookie |
| 用户信息 | ✅ 是 | ⚠️ 需 Cookie |

## 🔑 获取 Cookie

### 方法 1：使用自动工具

```bash
node scripts/get-cookie.js
```

按提示操作：
1. 浏览器会打开并跳转到小红书
2. 登录你的小红书账号
3. 按 Ctrl+C 停止脚本
4. Cookie 会自动导出到控制台

### 方法 2：手动获取

1. 浏览器访问 https://www.xiaohongshu.com
2. 登录账号
3. 按 F12 打开开发者工具
4. 切换到 **Application** 或 **Storage** 标签
5. 展开 **Cookies** -> **https://www.xiaohongshu.com**
6. 找到 `web_session` 等 cookie
7. 复制 name 和 value

## ⚙️ 配置 Cookie

编辑 `config.json`：

```json
{
  "cookie": {
    "enabled": true,
    "items": [
      {
        "name": "web_session",
        "value": "你的 cookie 值",
        "domain": ".xiaohongshu.com",
        "path": "/"
      }
    ]
  }
}
```

## 🚀 使用示例

### 1. 获取热门笔记（无需登录）

```bash
# 获取探索页热门笔记
node scripts/hot-notes.js explore 1 10

# 获取美食类热门笔记
node scripts/hot-notes.js food 1 20 json

# JSON 格式导出
node scripts/hot-notes.js tech 1 20 json > tech_notes.json
```

### 2. 搜索笔记（需要登录）

```bash
node scripts/search.js 手机测评 1 20
node scripts/search.js iPhone 15 2 10 json
```

### 3. 获取笔记详情（需要登录）

```bash
node scripts/get-note.js 64bc4249000000001201df4d
node scripts/get-note.js 64bc4249000000001201df4d json
```

### 4. 获取用户信息（需要登录）

```bash
node scripts/get-user.js 5f6g7h8i9j0k1l2m3n4o5p6q
node scripts/get-user.js 5f6g7h8i9j0k1l2m3n4o5p6q 20 json
```

### 5. 测试 Cookie

```bash
node scripts/test-cookie.js
```

验证 Cookie 是否有效。

## 📊 输出格式

### 文本格式（默认）

```
1. 在德国｜街头瞬间
   ID: 64bc4249000000001201df4d
   👤 待登录获取
   ❤️ ? | 💾 ? | 💬 ?
   🔗 https://www.xiaohongshu.com/explore/64bc4249000000001201df4d
```

### JSON 格式

```json
{
  "category": "explore",
  "page": 1,
  "total": 10,
  "data": [
    {
      "note_id": "64bc4249000000001201df4d",
      "title": "在德国｜街头瞬间",
      "cover": "https://sns-webpic-qc.xhscdn.com/...",
      "user": {
        "nickname": "",
        "user_id": ""
      },
      "url": "https://www.xiaohongshu.com/explore/64bc4249000000001201df4d"
    }
  ]
}
```

## ⚠️ 注意事项

1. **频率限制** - 建议每次查询间隔至少 2 秒
2. **缓存机制** - 相同查询会在 1 小时内自动使用缓存
3. **Cookie 有效期** - Cookie 会过期，需要定期更新
4. **隐私保护** - 仅抓取公开内容，不要抓取用户隐私信息
5. **合规使用** - 遵守小红书用户协议

## 🛠️ 故障排除

### 问题 1：搜索返回空结果

**原因**：未登录或 Cookie 过期
**解决**：
1. 检查 config.json 中 `cookie.enabled` 是否为 `true`
2. 运行 `node scripts/test-cookie.js` 测试
3. 如果失败，重新运行 `node scripts/get-cookie.js`

### 问题 2：找不到笔记元素

**原因**：页面结构变化
**解决**：
1. 查看最新的页面结构
2. 更新脚本中的选择器

### 问题 3：被限流

**原因**：请求过于频繁
**解决**：
1. 增加请求间隔时间
2. 使用代理 IP
3. 减少抓取量

## 📝 版本信息

- **版本**: 1.0.0
- **作者**: Dj
- **License**: MIT

---

**📌 提示**: 这是一个开源项目，欢迎提交 Issue 和 PR！
