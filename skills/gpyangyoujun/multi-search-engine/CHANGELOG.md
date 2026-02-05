# v2.0.0 更新日志

## 🎉 重大更新：新增国际搜索引擎支持

### 新增搜索引擎（7个国际引擎）

| 引擎 | 类型 | 特点 |
|------|------|------|
| **Google** | 综合搜索 | 全球最大搜索引擎 |
| **Google香港** | 综合搜索 | 中文友好版本 |
| **DuckDuckGo** | 隐私搜索 | 不追踪用户 |
| **Yahoo** | 综合搜索 | 老牌搜索引擎 |
| **Startpage** | 隐私搜索 | Google结果+隐私保护 |
| **Brave Search** | 隐私搜索 | 独立索引，隐私优先 |
| **Ecosia** | 环保搜索 | 搜索同时植树 |
| **Qwant** | 欧洲搜索 | GDPR合规 |
| **WolframAlpha** | 知识计算 | 结构化数据查询 |

### 现有国内引擎（8个）
- 百度、必应（国内/国际版）、360搜索、搜狗
- 搜狗微信、头条搜索、集思录

### 总计：17个搜索引擎！

---

## ✨ 新功能

### 1. Google高级搜索参数
- 站内搜索：`site:github.com`
- 文件类型：`filetype:pdf`
- 时间筛选：`tbs=qdr:w` (本周)
- 精确匹配：`"精确短语"`
- 排除关键词：`-排除词`

### 2. DuckDuckGo Bang快捷命令
- `!g` - 跳转到Google
- `!w` - Wikipedia
- `!gh` - GitHub
- `!yt` - YouTube

### 3. WolframAlpha知识计算
- 数学计算、单位换算
- 股票数据、天气查询
- 人口数据、化学元素

### 4. 国际引擎分类
- **隐私保护**：DuckDuckGo、Startpage、Brave、Qwant
- **环保理念**：Ecosia
- **知识计算**：WolframAlpha
- **综合搜索**：Google、Yahoo

---

## 📖 使用示例

```javascript
// Google国际搜索
web_fetch({"url": "https://www.google.com/search?q=python+tutorial&hl=en"})

// 隐私保护搜索
web_fetch({"url": "https://duckduckgo.com/html/?q=privacy+tools"})

// 知识计算查询
web_fetch({"url": "https://www.wolframalpha.com/input?i=100+USD+to+CNY"})

// Google本周新闻
web_fetch({"url": "https://www.google.com/search?q=AI&tbs=qdr:w"})
```

---

## 🔧 配置文件

新增 `config.json` 包含所有17个搜索引擎的配置信息：
- 名称、URL模板
- 地区（cn/global）
- 类型（general/privacy/knowledge等）

---

## 📅 更新时间

2026-02-06

## 📝 版本

v2.0.0 - 从8个引擎扩展到17个引擎，新增国际搜索引擎支持
