# Xiaohongshu Crawler Skill

小红书（Xiaohongshu）内容爬取工具。支持搜索、获取笔记详情、用户主页等。

## 🚀 快速开始

### 安装依赖
```bash
cd /Users/dengjun/.openclaw/workspace/skills/xiaohongshu-crawler
npm install
```

### Cookie 配置（必需）

小红书搜索功能需要登录才能使用。必须先配置有效的 Cookie。

#### 方法 1：使用交互式脚本获取 Cookie（推荐）

```bash
cd /Users/dengjun/.openclaw/workspace/skills/xiaohongshu-crawler
node scripts/get-cookie.js
```

**步骤说明：**
1. 脚本会自动打开浏览器并跳转到小红书登录页
2. **扫码登录**你的小红书账号
3. 登录成功后，在**终端输入 `save` 并回车**
4. Cookie 会自动保存到 `config.json`

**注意：** 如果浏览器没有自动弹出，请检查系统权限设置或手动打开浏览器。

#### 方法 2：手动复制 Cookie

1. 打开浏览器（保持已登录小红书状态）
2. 按 **F12** 打开开发者工具
3. 切换到 **Network（网络）** 标签页
4. 刷新页面或访问任意小红书页面
5. 点击任意请求，找到 **Request Headers**
6. 复制 **Cookie** 这一行的值
7. 在终端输入：

```bash
# 将你的 Cookie 粘贴到这里
paste-to-terminal
```

然后手动编辑 `config.json` 更新 Cookie 项。

### 测试 Cookie

```bash
node scripts/test-cookie.js
```

测试通过后会显示登录状态并截图保存到 `test-screenshot.png`。

---

## 📋 可用脚本

### 1. Cookie 获取

```bash
node scripts/get-cookie.js
```

交互式获取 Cookie，登录成功后输入 `save` 自动保存。

### 2. Cookie 测试

```bash
node scripts/test-cookie.js
```

验证 Cookie 是否有效，检查登录状态。

### 3. 快速搜索

```bash
node scripts/quick-search.js "搜索关键词" [结果数量]
```

**示例：**
```bash
# 搜索"四川旅游"，最多 30 条结果
node scripts/quick-search.js "四川旅游" 30

# 搜索"成都美食"，默认 20 条结果
node scripts/quick-search.js "成都美食"
```

**输出：**
- 搜索结果会显示在终端
- 数据保存为 `sichuan-travel-{timestamp}.json`
- 页面截图保存为 `search-result.png`

### 4. 深度爬取

```bash
node scripts/deep-crawl.js "搜索关键词" [结果数量]
```

**示例：**
```bash
# 爬取 20 条笔记的详细信息
node scripts/deep-crawl.js "四川旅游" 20
```

**输出：**
- `sichuan-travel-results.json` - 搜索结果列表
- `sichuan-travel-detailed.json` - 包含详细内容的笔记
- `search-detail.png` - 页面截图

### 5. 获取笔记详情

```bash
node scripts/get-note.js "笔记 URL"
```

获取单条笔记的详细内容。

### 6. 获取用户信息

```bash
node scripts/get-user.js "用户 ID"
```

获取指定用户的资料。

### 7. 热门笔记

```bash
node scripts/hot-notes.js
```

获取小红书热门笔记（无需登录）。

---

## 📝 Cookie 配置详情

### Cookie 结构

`config.json` 中的 Cookie 配置结构如下：

```json
{
  "cookie": {
    "enabled": true,
    "items": [
      {
        "name": "web_session",
        "value": "040069b04a6c475841ea944e8d3b4beaf35195",
        "domain": ".xiaohongshu.com",
        "path": "/"
      },
      {
        "name": "id_token",
        "value": "VjEAAAJoLik2stTHiMaQ1axwUoxU1Sa1T2ZNcXqRWE8tAMf3Cp1w6qqac2xivS1z5BYxBgO6QsUAFgRh7j6PUeMLUi50z3aK9cnn9Flzh5ac8mUu00fXyrh3VXKECOW70pUyfLRX",
        "domain": ".xiaohongshu.com",
        "path": "/"
      },
      {
        "name": "acw_tc",
        "value": "0ad5406817736680717796292e50dd85e7bbf503b28c41f8df906bc96c8a77",
        "domain": ".xiaohongshu.com",
        "path": "/"
      },
      // ... 更多 Cookie
    ]
  }
}
```

### 关键 Cookie 字段

| 字段名 | 说明 | 必需 |
|--------|------|------|
| `web_session` | 会话标识，核心认证字段 | ✅ |
| `id_token` | 用户身份令牌 | ✅ |
| `acw_tc` | 反爬验证令牌 | ✅ |
| `webId` | 设备标识 | ✅ |
| `websectiga` | 安全验证令牌 | ✅ |
| `abRequestId` | 请求追踪 ID | ✅ |
| `sec_poison_id` | 风控验证 ID | ✅ |
| `loadts` | 时间戳 | ✅ |
| `webBuild` | 客户端版本 | - |
| `xsecappid` | 应用标识 | ✅ |
| `unread` | 未读消息状态 | - |

### Cookie 有效期

- **有效期：** 通常 1-3 天
- **失效原因：**
  - Cookie 过期
  - IP 地址变化
  - 小红书风控检测
  - 用户在其他设备登录

**建议：** 如果遇到"需要登录"错误，请重新获取 Cookie。

---

## 🔧 配置选项

### config.json 完整配置

```json
{
  "playwright": {
    "headless": false,
    "browser": "chromium",
    "timeout": 30000,
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
  },
  "xhs": {
    "base_url": "https://www.xiaohongshu.com",
    "api_delay": 2000,
    "cache_duration": 3600000,
    "max_pages": 50
  },
  "cookie": {
    "enabled": true,
    "items": [...]
  },
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

### 反爬设置说明

| 配置项 | 说明 | 推荐值 |
|--------|------|--------|
| `anti_crawl.enabled` | 是否启用反爬保护 | `true` |
| `random_delay.min` | 最小请求间隔（毫秒） | `2000` |
| `random_delay.max` | 最大请求间隔（毫秒） | `8000` |
| `rate_limit.max_requests_per_minute` | 每分钟最大请求数 | `10` |
| `rate_limit.max_requests_per_hour` | 每小时最大请求数 | `100` |

---

## 🛠️ 故障排查

### 问题 1: 需要登录才能搜索

**错误信息：** `❌ 查询失败：需要登录后才能搜索`

**解决方法：**
1. 运行 `node scripts/get-cookie.js` 获取最新 Cookie
2. 确保 `config.json` 中 `cookie.enabled` 为 `true`
3. 检查 Cookie 是否过期（重新获取）

### 问题 2: Cookie 已过期

**错误信息：** `⚠️ Cookie 可能已过期，显示登录按钮`

**解决方法：**
1. 重新运行 `node scripts/get-cookie.js`
2. 登录时建议勾选"记住我"
3. 清除浏览器缓存后重新获取

### 问题 3: 被风控检测

**错误信息：** `⚠️ 页面状态异常，可能被风控`

**解决方法：**
1. 检查网络连接
2. 降低请求频率（增大 `random_delay`）
3. 使用代理 IP（如需要）
4. 更换浏览器指纹

### 问题 4: 找不到搜索结果

**错误信息：** `⚠️ 未找到搜索结果`

**可能原因：**
- 搜索关键词过于特殊
- 小红书风控拦截
- 网络连接问题

**解决方法：**
1. 更换关键词重试
2. 检查 Cookie 是否有效
3. 检查网络代理设置

---

## 📚 脚本文件说明

| 文件 | 功能 | 依赖 |
|------|------|------|
| `scripts/get-cookie.js` | 交互式获取 Cookie | 无 |
| `scripts/test-cookie.js` | 测试 Cookie 有效性 | 无 |
| `scripts/quick-search.js` | 快速搜索笔记 | Cookie |
| `scripts/deep-crawl.js` | 深度爬取笔记详情 | Cookie |
| `scripts/search.js` | 搜索脚本（旧版） | Cookie |
| `scripts/get-note.js` | 获取单条笔记详情 | Cookie |
| `scripts/get-user.js` | 获取用户信息 | Cookie |
| `scripts/hot-notes.js` | 获取热门笔记 | 可选 Cookie |

---

## 🎯 使用示例

### 示例 1: 搜索并导出报告

```bash
# 1. 确保 Cookie 已配置
node scripts/test-cookie.js

# 2. 搜索关键词
node scripts/quick-search.js "四川旅游" 30

# 3. 深度爬取
node scripts/deep-crawl.js "四川旅游" 20

# 4. 查看生成的报告
cat reports/sichuan-travel-report.md
```

### 示例 2: 批量爬取多个关键词

```bash
# 创建批量脚本
cat > batch-crawl.sh << 'EOF'
#!/bin/bash
keywords=("四川旅游" "成都美食" "川西自驾")

for keyword in "${keywords[@]}"; do
  echo "爬取：$keyword"
  node scripts/deep-crawl.js "$keyword" 20
  sleep 5
done
EOF

chmod +x batch-crawl.sh
./batch-crawl.sh
```

---

## ⚠️ 使用规范

### 合规使用

本工具仅限学习和研究使用，请遵守以下规则：

- ✅ **允许：**
  - 个人学习和研究
  - 公开内容爬取
  - 小批量数据获取

- ❌ **禁止：**
  - 商业用途
  - 大规模高频次爬取
  - 爬取私人/隐私内容
  - 绕过付费内容
  - 分发爬取数据

### 反爬保护

- 默认启用随机延迟（2-8 秒）
- 限制每分钟最多 10 个请求
- 模拟人类浏览行为

### 法律责任

使用本工具产生的数据仅供个人学习研究，请遵守：
- 小红书用户协议
- 相关法律法规
- 知识产权规定

---

## 📖 技术说明

### 依赖项

- Node.js >= 18
- Playwright (Chromium)
- axios
- cheerio

### 安装

```bash
npm install
```

### 首次使用

```bash
# 1. 安装依赖
npm install

# 2. 下载浏览器
npx playwright install chromium

# 3. 配置 Cookie
node scripts/get-cookie.js

# 4. 测试
node scripts/test-cookie.js
```

---

## 🔄 更新日志

### v2.0.0 (2026-03-16)
- ✨ 新增 `quick-search.js` - 快速搜索脚本
- ✨ 新增 `deep-crawl.js` - 深度爬取脚本
- 🔧 重构 `get-cookie.js` - 支持交互式保存
- 🔧 重构 `test-cookie.js` - 增强测试结果
- 📝 添加详细 Cookie 配置说明
- 📝 添加故障排查指南
- 🔒 优化反爬保护机制

### v1.0.0
- 初始版本发布

---

## 📞 技术支持

遇到问题请检查：
1. Cookie 是否有效
2. 网络连接是否正常
3. 反爬设置是否合理
4. 查看错误截图

---

**重要提示：** Cookie 有效期较短，建议定期更新。遇到任何问题先尝试重新获取 Cookie。
