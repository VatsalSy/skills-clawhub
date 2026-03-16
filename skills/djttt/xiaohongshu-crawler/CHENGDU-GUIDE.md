# 成都旅游笔记抓取指南

## 📊 当前状态

通过测试发现：

1. ✅ **探索页抓取** - 可以正常工作
2. ❌ **搜索功能** - 需要登录（Cookie 无效）
3. ⚠️ **关键词筛选** - 探索页内容不专门针对成都

## 💡 解决方案

### 方案 A：使用热门笔记分类

```bash
# 从探索页获取各类热门笔记
node scripts/hot-notes.js travel 1 20    # 旅行
node scripts/hot-notes.js food 1 20      # 美食
node scripts/hot-notes.js fashion 1 20   # 时尚
```

然后在这些笔记中筛选成都相关内容。

### 方案 B：配置有效 Cookie

如果获取了有效的 Cookie，可以使用：

```bash
node scripts/search.js 成都旅游 1 20
```

### 方案 C：使用外部工具

参考 `xiaohongshu-cli` 工具：
```bash
pipx install xiaohongshu-cli
xhs login
xhs search "成都旅游"
```

## 📝 实际测试结果

**探索页内容**（无需登录）：
- 返回的是通用热门笔记，不专门针对特定关键词
- 需要手动筛选成都相关内容

**搜索功能**（需登录）：
- 可以精确搜索特定关键词
- 返回该关键词下的所有笔记
- 需要有效的 Cookie

## 🔧 实用脚本

已创建 `scripts/chengdu-travel.js` 脚本，可以从探索页抓取并筛选成都相关内容：

```bash
node scripts/chengdu-travel.js 50
```

## 💭 建议

1. **当前可用** - 探索页热门笔记功能可以正常使用
2. **需要搜索** - 获取有效 Cookie 后使用搜索功能
3. **批量处理** - 可以多次运行热门笔记脚本收集数据

## 🎯 下一步

如果需要使用搜索功能获取成都旅游笔记：

1. 运行 `node scripts/get-cookie.js`
2. 在浏览器中登录小红书
3. 按 Ctrl+C 导出 Cookie
4. 配置到 config.json
5. 启用 cookie.enabled: true
6. 使用 `node scripts/search.js 成都旅游 1 20`
