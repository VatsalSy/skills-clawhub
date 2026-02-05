---
name: "multi-search-engine"
description: "集成17大搜索引擎（国内8个：百度、必应、360、搜狗、微信、头条、集思录等；国际9个：Google、DuckDuckGo、Yahoo、Brave、Startpage、Ecosia、Qwant、WolframAlpha等）进行深度网页搜索。支持高级搜索操作符、时间筛选、站点限定、文件类型筛选、隐私保护搜索、知识计算查询。Invoke when user needs to search information online, compare search results from different engines, perform advanced filtering, or fetch web content without API keys. Supports both Chinese and international search with professional-grade search capabilities."
---

# 多搜索引擎集成技能 v2.0.0

本技能集成了**17个主流搜索引擎**（8个国内 + 9个国际），支持通过网页抓取方式获取搜索结果，无需API密钥。提供**专业级深度搜索能力**，包括高级搜索操作符、时间筛选、站点限定、隐私保护搜索、知识计算等功能。

## 🚀 核心特性

- **17个搜索引擎**: 覆盖全球主流中英文搜索引擎
- **高级搜索语法**: 支持Google、DuckDuckGo等的高级操作符
- **隐私保护**: 支持DuckDuckGo、Brave、Startpage等隐私搜索引擎
- **知识计算**: 集成WolframAlpha结构化数据查询
- **时间筛选**: 支持按小时/天/周/月/年筛选结果
- **文件类型搜索**: PDF、DOC、XLS等文档精确查找
- **站点限定**: 在特定网站内搜索内容

## 📊 搜索引擎对比速查

## 支持的搜索引擎

### 🇨🇳 国内搜索引擎

| 搜索引擎 | URL模板 | 类型 | 状态 | 特点说明 |
|---------|---------|------|------|----------|
| **百度** | `https://www.baidu.com/s?wd={keyword}` | 综合搜索 | ✅ 可用 | 国内最大搜索引擎，覆盖全面 |
| **必应国内版** | `https://cn.bing.com/search?q={keyword}&ensearch=0` | 综合搜索 | ✅ 可用 | 本土化搜索结果 |
| **必应国际版** | `https://cn.bing.com/search?q={keyword}&ensearch=1` | 综合搜索 | ✅ 可用 | 国际搜索，英文内容 |
| **360搜索** | `https://www.so.com/s?q={keyword}` | 综合搜索 | ✅ 可用 | 安全搜索特色 |
| **搜狗** | `https://sogou.com/web?query={keyword}` | 综合搜索 | ✅ 可用 | 腾讯旗下，支持微信搜索 |
| **搜狗微信** | `https://wx.sogou.com/weixin?type=2&query={keyword}` | 微信搜索 | ✅ 可用 | 微信公众号文章搜索 |
| **头条搜索** | `https://so.toutiao.com/search?keyword={keyword}` | 资讯搜索 | ✅ 可用 | 字节跳动旗下 |
| **集思录** | `https://www.jisilu.cn/explore/?keyword={keyword}` | 投资社区 | ✅ 可用 | 低风险投资社区 |

### 🌍 国际搜索引擎

| 搜索引擎 | URL模板 | 类型 | 状态 | 特点说明 |
|---------|---------|------|------|----------|
| **Google** | `https://www.google.com/search?q={keyword}&hl=en` | 综合搜索 | ✅ 可用 | 全球最大搜索引擎 |
| **Google香港** | `https://www.google.com.hk/search?q={keyword}` | 综合搜索 | ✅ 可用 | 中文友好 |
| **DuckDuckGo** | `https://duckduckgo.com/html/?q={keyword}` | 隐私搜索 | ✅ 可用 | 不追踪用户，隐私保护 |
| **Yahoo** | `https://search.yahoo.com/search?p={keyword}` | 综合搜索 | ✅ 可用 | 老牌搜索引擎 |
| **Startpage** | `https://www.startpage.com/sp/search?query={keyword}` | 隐私搜索 | ✅ 可用 | Google结果+隐私保护 |
| **Brave Search** | `https://search.brave.com/search?q={keyword}` | 隐私搜索 | ✅ 可用 | 独立索引，隐私优先 |
| **Ecosia** | `https://www.ecosia.org/search?q={keyword}` | 环保搜索 | ✅ 可用 | 搜索植树，环保理念 |
| **Qwant** | `https://www.qwant.com/?q={keyword}` | 欧洲搜索 | ✅ 可用 | 欧盟隐私法规，无追踪 |
| **WolframAlpha** | `https://www.wolframalpha.com/input?i={keyword}` | 知识计算 | ✅ 可用 | 结构化知识查询 |

## 使用方法

### 国内搜索引擎

```javascript
// 百度搜索
web_fetch({"url": "https://www.baidu.com/s?wd=关键词"})

// 必应国内版
web_fetch({"url": "https://cn.bing.com/search?q=关键词&ensearch=0"})

// 必应国际版（英文内容）
web_fetch({"url": "https://cn.bing.com/search?q=关键词&ensearch=1"})

// 360搜索
web_fetch({"url": "https://www.so.com/s?q=关键词"})

// 搜狗搜索
web_fetch({"url": "https://sogou.com/web?query=关键词"})

// 头条搜索
web_fetch({"url": "https://so.toutiao.com/search?keyword=关键词"})

// 搜狗微信搜索
web_fetch({"url": "https://wx.sogou.com/weixin?type=2&query=关键词"})

// 集思录投资搜索
web_fetch({"url": "https://www.jisilu.cn/explore/?keyword=关键词"})
```

### 国际搜索引擎

```javascript
// Google国际版（英文）
web_fetch({"url": "https://www.google.com/search?q=keyword&hl=en"})

// Google香港（中文）
web_fetch({"url": "https://www.google.com.hk/search?q=关键词"})

// DuckDuckGo（隐私保护）
web_fetch({"url": "https://duckduckgo.com/html/?q=关键词"})

// Yahoo搜索
web_fetch({"url": "https://search.yahoo.com/search?p=关键词"})

// Startpage（Google结果+隐私）
web_fetch({"url": "https://www.startpage.com/sp/search?query=关键词"})

// Brave Search
web_fetch({"url": "https://search.brave.com/search?q=关键词"})

// Ecosia（环保搜索）
web_fetch({"url": "https://www.ecosia.org/search?q=关键词"})

// Qwant（欧盟隐私）
web_fetch({"url": "https://www.qwant.com/?q=关键词"})

// WolframAlpha（知识计算）
web_fetch({"url": "https://www.wolframalpha.com/input?i=关键词"})
```

### 实际示例

```javascript
// 搜索中文资料
web_fetch({"url": "https://www.baidu.com/s?wd=贵州茅台"})

// 搜索英文技术文档
web_fetch({"url": "https://www.google.com/search?q=python+tutorial&hl=en"})

// 搜索隐私保护（不追踪）
web_fetch({"url": "https://duckduckgo.com/html/?q=privacy+tools"})

// 最新中文资讯
web_fetch({"url": "https://so.toutiao.com/search?keyword=人工智能"})

// 投资套利信息
web_fetch({"url": "https://www.jisilu.cn/explore/?keyword=LOF套利"})

// 知识计算查询
web_fetch({"url": "https://www.wolframalpha.com/input?i=population+of+china"})
```

## 搜索引擎选择建议

### 按场景选择

| 搜索场景 | 推荐引擎 | 原因 |
|---------|---------|------|
| **日常中文搜索** | 百度 | 覆盖面广，结果全面 |
| **国内新闻资讯** | 头条搜索 | 聚合今日头条内容，时效性强 |
| **英文技术文档** | Google / DuckDuckGo | 国际搜索结果更丰富 |
| **隐私保护搜索** | DuckDuckGo / Startpage | 不追踪用户，保护隐私 |
| **安全相关查询** | 360搜索 | 安全过滤机制完善 |
| **微信文章搜索** | 搜狗微信 | 专门搜索微信公众号文章 |
| **投资/套利信息** | 集思录 | 低风险投资社区 |
| **知识/数据查询** | WolframAlpha | 结构化知识计算 |
| **环保理念** | Ecosia | 搜索同时支持植树 |
| **欧盟合规** | Qwant | 符合GDPR，无追踪 |

### 按语言选择

| 目标语言 | 推荐引擎 |
|---------|---------|
| 中文 | 百度、必应国内版、头条 |
| 英文 | Google、DuckDuckGo、Brave |
| 多语言 | Google、必应国际版 |
| 中文+英文 | Google香港、必应 |

### 按隐私级别选择

| 隐私级别 | 推荐引擎 |
|---------|---------|
| 最高隐私 | DuckDuckGo、Startpage、Brave |
| 中等隐私 | Qwant、Ecosia |
| 标准 | Google、必应 |

## 高级搜索参数

### Google高级搜索

| 功能 | URL参数 | 示例 |
|------|---------|------|
| 站内搜索 | `site:域名` | `https://www.google.com/search?q=site:github.com+python` |
| 文件类型 | `filetype:扩展名` | `https://www.google.com/search?q=filetype:pdf+machine+learning` |
| 精确匹配 | `"精确短语"` | `https://www.google.com/search?q="machine+learning"` |
| 排除关键词 | `-关键词` | `https://www.google.com/search?q=python+-snake` |
| 时间限制 | `tbs=qdr:h` (过去1小时) | `https://www.google.com/search?q=news&tbs=qdr:d` |
| 语言限制 | `lr=lang_zh-CN` | `https://www.google.com/search?q=test&lr=lang_zh-CN` |
| 安全搜索关闭 | `safe=off` | `https://www.google.com/search?q=test&safe=off` |

**时间参数详解：**
- `qdr:h` - 过去1小时
- `qdr:d` - 过去24小时
- `qdr:w` - 过去1周
- `qdr:m` - 过去1月
- `qdr:y` - 过去1年

### DuckDuckGo高级搜索

| 功能 | URL参数 | 示例 |
|------|---------|------|
| 站内搜索 | `site:域名` | `https://duckduckgo.com/html/?q=site:github.com+python` |
| 文件类型 | `filetype:pdf` | `https://duckduckgo.com/html/?q=filetype:pdf+report` |
| 排除关键词 | `-关键词` | `https://duckduckgo.com/html/?q=apple+-fruit` |
| 安全搜索 | `kp=1` (严格) / `kp=-1` (关闭) | `https://duckduckgo.com/html/?q=test&kp=1` |
| 地区 | `kl=us` | `https://duckduckgo.com/html/?q=news&kl=cn` |

### Brave Search高级参数

| 功能 | URL参数 | 示例 |
|------|---------|------|
| 时间筛选 | `tf=pw` (本周) | `https://search.brave.com/search?q=news&tf=pw` |
| 安全搜索 | `safesearch=strict` | `https://search.brave.com/search?q=test&safesearch=strict` |

### 百度高级搜索

| 功能 | URL参数 | 示例 |
|------|---------|------|
| 近一天内 | `lm=1` | `https://www.baidu.com/s?wd=关键词&lm=1` |
| 近一周内 | `lm=7` | `https://www.baidu.com/s?wd=关键词&lm=7` |
| 站点内搜索 | `site=域名` | `https://www.baidu.com/s?wd=关键词&site=zhihu.com` |
| PDF文档 | `filetype:pdf` | `https://www.baidu.com/s?wd=关键词+filetype%3Apdf` |

## 国际搜索引擎特色功能

### DuckDuckGo Bang 快捷搜索

DuckDuckGo 支持 `!` 前缀快速跳转到其他网站：

| 快捷命令 | 功能 | URL示例 |
|---------|------|---------|
| `!g` | Google搜索 | `https://duckduckgo.com/html/?q=!g+关键词` |
| `!w` | Wikipedia | `https://duckduckgo.com/html/?q=!w+Python` |
| `!gh` | GitHub | `https://duckduckgo.com/html/?q=!gh+tensorflow` |
| `!yt` | YouTube | `https://duckduckgo.com/html/?q=!yt+tutorial` |
| `!a` | Amazon | `https://duckduckgo.com/html/?q=!a+book` |
| `!maps` | 地图 | `https://duckduckgo.com/html/?q=!maps+Beijing` |

### WolframAlpha 知识查询

适合查询结构化数据和计算：

| 查询类型 | 示例 | URL |
|---------|------|-----|
| 数学计算 | `integrate x^2` | `https://www.wolframalpha.com/input?i=integrate+x%5E2` |
| 单位换算 | `100 USD to CNY` | `https://www.wolframalpha.com/input?i=100+USD+to+CNY` |
| 股票数据 | `AAPL stock` | `https://www.wolframalpha.com/input?i=AAPL+stock` |
| 天气查询 | `weather in Beijing` | `https://www.wolframalpha.com/input?i=weather+in+Beijing` |
| 人口数据 | `population of China` | `https://www.wolframalpha.com/input?i=population+of+China` |
| 化学元素 | `properties of gold` | `https://www.wolframalpha.com/input?i=properties+of+gold` |

## 深度搜索使用示例

```javascript
// Google站内搜索GitHub上的Python项目
web_fetch({"url": "https://www.google.com/search?q=site:github.com+python+machine+learning"})

// Google搜索近一周的技术新闻
web_fetch({"url": "https://www.google.com/search?q=AI+news&tbs=qdr:w"})

// DuckDuckGo搜索PDF文档
web_fetch({"url": "https://duckduckgo.com/html/?q=filetype:pdf+annual+report"})

// Brave搜索本周新闻
web_fetch({"url": "https://search.brave.com/search?q=technology&tf=pw"})

// WolframAlpha查询汇率
web_fetch({"url": "https://www.wolframalpha.com/input?i=100+USD+to+CNY"})

// Ecosia环保搜索
web_fetch({"url": "https://www.ecosia.org/search?q=climate+change"})

// Qwant欧盟隐私搜索
web_fetch({"url": "https://www.qwant.com/?q=GDPR+compliance"})

// 百度搜索知乎站内内容
web_fetch({"url": "https://www.baidu.com/s?wd=人工智能&site=zhihu.com"})
```

## 注意事项

### 国际搜索引擎使用提示

1. **网络环境**：部分国际引擎（Google等）可能需要特定网络环境
2. **语言设置**：国际引擎默认英文，可通过 `hl=zh-CN` 或访问地区版本获取中文
3. **隐私保护**：DuckDuckGo、Startpage、Brave等不追踪搜索历史
4. **反爬虫**：国际引擎通常有更严格的反爬虫机制，建议控制请求频率
5. **结果差异**：同一关键词在不同引擎结果差异可能较大，建议多引擎对比

### URL编码

关键词包含特殊字符时需要编码：
- 空格 → `+` 或 `%20`
- 中文 → 自动或手动 URL 编码
- `&` → `%26`
- `=` → `%3D`

## 扩展开发

如需添加更多搜索引擎，只需在配置中新增条目：

```json
{
  "name": "新搜索引擎名称",
  "url": "https://example.com/search?q={keyword}",
  "type": "搜索类型",
  "region": "国内/国际",
  "status": "可用",
  "notes": "特点说明"
}
```

## 🎯 深度搜索能力矩阵

### 功能对比表

| 功能 | Google | DuckDuckGo | Brave | WolframAlpha | 百度 |
|------|--------|-----------|-------|-------------|------|
| **站点限定** `site:` | ✅ | ✅ | ✅ | ❌ | ✅ |
| **文件类型** `filetype:` | ✅ | ✅ | ❌ | ❌ | ✅ |
| **时间筛选** | ✅ | ❌ | ✅ | ❌ | ✅ |
| **精确匹配** `""` | ✅ | ✅ | ✅ | ❌ | ✅ |
| **排除关键词** `-` | ✅ | ✅ | ✅ | ❌ | ✅ |
| **隐私保护** | ⚠️ | ✅ | ✅ | ⚠️ | ❌ |
| **知识计算** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Bangs快捷** | ❌ | ✅ | ❌ | ❌ | ❌ |

### 深度搜索实战示例

#### 🔬 学术研究深度搜索

```javascript
// 1. 搜索特定学者的论文（Google Scholar）
web_fetch({"url": "https://scholar.google.com/scholar?q=author:%22Yann+LeCun%22+deep+learning"})

// 2. 搜索近一年发表在特定期刊的论文
web_fetch({"url": "https://www.google.com/search?q=machine+learning+site:nature.com+filetype:pdf&tbs=qdr:y"})

// 3. 搜索引用次数多的经典论文
web_fetch({"url": "https://scholar.google.com/scholar?q=transformer+attention&hl=en&as_sdt=0,5"})

// 4. 搜索arXiv特定领域的最新论文
web_fetch({"url": "https://duckduckgo.com/html/?q=site:arxiv.org+abs+cs.AI&tbs=qdr:w"})

// 5. 搜索学术会议论文（NeurIPS/ICML/CVPR）
web_fetch({"url": "https://www.google.com/search?q=neurips+2024+paper+site:neurips.cc"})
```

#### 💻 技术开发深度搜索

```javascript
// 1. 搜索GitHub高星项目（使用DuckDuckGo Bangs）
web_fetch({"url": "https://duckduckgo.com/html/?q=!gh+python+machine+learning+stars:%3E1000"})

// 2. 搜索Stack Overflow高质量答案
web_fetch({"url": "https://duckduckgo.com/html/?q=!so+python+multithreading+answers:5"})

// 3. 搜索官方文档中的特定内容
web_fetch({"url": "https://www.google.com/search?q=async+await+site:docs.python.org"})

// 4. 搜索最新版本的库文档
web_fetch({"url": "https://www.google.com/search?q=tensorflow+2.0+site:tensorflow.org&tbs=qdr:y"})

// 5. 搜索GitHub Issues中的解决方案
web_fetch({"url": "https://www.google.com/search?q=github+issues+tensorflow+memory+leak"})

// 6. 使用Brave搜索技术讨论
web_fetch({"url": "https://search.brave.com/search?q=rust+vs+go+performance+2024"})
```

#### 📊 金融数据深度搜索

```javascript
// 1. 实时股票数据（WolframAlpha）
web_fetch({"url": "https://www.wolframalpha.com/input?i=Apple+Tesla+stock+price+comparison"})

// 2. 历史股价数据
web_fetch({"url": "https://www.wolframalpha.com/input?i=AAPL+stock+from+January+2020+to+December+2024"})

// 3. 货币汇率实时查询
web_fetch({"url": "https://www.wolframalpha.com/input?i=100+USD+to+CNY+to+EUR+to+JPY"})

// 4. 搜索上市公司财报PDF
web_fetch({"url": "https://www.google.com/search?q=Apple+Q4+2024+earnings+filetype:pdf+site:apple.com"})

// 5. 搜索行业报告
web_fetch({"url": "https://www.google.com/search?q=artificial+intelligence+market+size+2024+filetype:pdf"})

// 6. 集思录LOF套利数据
web_fetch({"url": "https://www.jisilu.cn/data/lof/"})

// 7. 集思录可转债数据
web_fetch({"url": "https://www.jisilu.cn/data/cbnew/"})
```

#### 📰 新闻时事深度搜索

```javascript
// 1. Google过去1小时的突发新闻
web_fetch({"url": "https://www.google.com/search?q=breaking+news&tbs=qdr:h&tbm=nws"})

// 2. Brave本周科技新闻
web_fetch({"url": "https://search.brave.com/search?q=technology&tf=pw&source=news"})

// 3. 特定地区的本地新闻
web_fetch({"url": "https://www.google.com/search?q=local+news+San+Francisco&gl=us&tbm=nws"})

// 4. 搜索特定记者的报道
web_fetch({"url": "https://www.google.com/search?q=%22Walter+Isaacson%22+biography+site:cnbc.com"})

// 5. DuckDuckGo新闻聚焦
web_fetch({"url": "https://duckduckgo.com/html/?q=climate+change+news&ia=news"})
```

#### 🔐 隐私保护搜索策略

```javascript
// 1. 完全隐私的搜索（无追踪）
web_fetch({"url": "https://duckduckgo.com/html/?q=privacy+tools"})

// 2. 使用Startpage获得Google结果但保护隐私
web_fetch({"url": "https://www.startpage.com/sp/search?query=secure+messaging&time=week"})

// 3. Brave独立索引搜索
web_fetch({"url": "https://search.brave.com/search?q=encryption+best+practices"})

// 4. 欧洲GDPR合规搜索
web_fetch({"url": "https://www.qwant.com/?q=GDPR+compliance+checklist"})

// 5. 环保理念搜索
web_fetch({"url": "https://www.ecosia.org/search?q=renewable+energy+investment"})
```

#### 🧮 WolframAlpha 深度查询

```javascript
// 1. 复杂数学计算
web_fetch({"url": "https://www.wolframalpha.com/input?i=solve+x%5E4-5x%5E2%2B4%3D0"})

// 2. 数据统计分析
web_fetch({"url": "https://www.wolframalpha.com/input?i=mean%7B12%2C+15%2C+18%2C+22%2C+30%7D+variance+standard+deviation"})

// 3. 物理常数和公式
web_fetch({"url": "https://www.wolframalpha.com/input?i=Planck+constant+value+units"})

// 4. 化学分子计算
web_fetch({"url": "https://www.wolframalpha.com/input?i=molecular+weight+of+C6H12O6"})

// 5. 地理信息查询
web_fetch({"url": "https://www.wolframalpha.com/input?i=distance+from+Beijing+to+Shanghai"})

// 6. 历史数据对比
web_fetch({"url": "https://www.wolframalpha.com/input?i=GDP+of+USA+vs+China+vs+Japan+vs+Germany"})

// 7. 营养摄入计算
web_fetch({"url": "https://www.wolframalpha.com/input?i=calories+protein+carbs+in+200g+chicken+breast"})

// 8. 时区和时间计算
web_fetch({"url": "https://www.wolframalpha.com/input?i=current+time+in+Tokyo+London+New+York+Beijing"})
```

## 🛠️ 高级搜索组合技巧

### 组合搜索公式

```javascript
// 公式1: 精确短语 + 站点限定 + 时间筛选
// 用途：查找特定网站的最新官方公告
// Google: "exact phrase" site:domain.com tbs=qdr:m

// 公式2: 文件类型 + 排除关键词 + 语言限定
// 用途：查找英文PDF文档，排除特定内容
// Google: keyword filetype:pdf -exclude lr=lang_en

// 公式3: 或运算 + 分组 + 站点限定
// 用途：在多个相关站点中搜索任一关键词
// Google: (keyword1 OR keyword2) (site:domain1.com OR site:domain2.com)

// 公式4: DuckDuckGo Bangs 快速跳转
// 用途：直接跳转到特定网站的搜索结果
// DDG: !bang keyword

// 公式5: 隐私搜索 + 时间筛选
// 用途：在不追踪的情况下获取最新信息
// Brave: keyword tf=pw (this week)
```

### 实战组合示例

```javascript
// 示例1: 搜索GitHub上近6个月的高星Python项目
// Google: site:github.com python stars:>1000 tbs=qdr:m
web_fetch({"url": "https://www.google.com/search?q=site:github.com+python+stars:%3E1000&tbs=qdr:m"})

// 示例2: 搜索Stack Overflow上高分答案（使用Bangs）
web_fetch({"url": "https://duckduckgo.com/html/?q=!so+python+multiprocessing+score:10"})

// 示例3: 搜索近一周的Python安全漏洞（隐私模式）
web_fetch({"url": "https://search.brave.com/search?q=python+security+vulnerability&tf=pw"})

// 示例4: 搜索特定期刊的机器学习论文（PDF格式）
web_fetch({"url": "https://www.google.com/search?q=machine+learning+site:arxiv.org+filetype:pdf&tbs=qdr:y"})

// 示例5: 对比多个公司的股价表现
web_fetch({"url": "https://www.wolframalpha.com/input?i=AAPL+GOOGL+MSFT+AMZN+stock+price+comparison"})

// 示例6: 搜索排除了Stack Overflow的技术博客文章
web_fetch({"url": "https://www.google.com/search?q=python+async+programming+-site:stackoverflow.com+filetype:html"})

// 示例7: 使用DuckDuckGo快速查看Wikipedia
web_fetch({"url": "https://duckduckgo.com/html/?q=!w+Artificial+Intelligence"})

// 示例8: 搜索包含特定URL模式的技术文档
web_fetch({"url": "https://www.google.com/search?q=inurl:docs+inurl:api+python+async"})
```

## 📈 搜索效率优化

### URL编码快捷函数

```javascript
// JavaScript 编码函数
function encodeSearch(keyword) {
  return encodeURIComponent(keyword);
}

// Python 编码函数
// import urllib.parse
// urllib.parse.quote(keyword)

// 示例
const keyword = "machine learning tutorial";
const encoded = encodeSearch(keyword); 
// 结果: "machine%20learning%20tutorial"
```

### 多引擎批量搜索

```javascript
// 同时搜索多个引擎获取不同视角
function multiEngineSearch(keyword) {
  const encoded = encodeURIComponent(keyword);
  return {
    google: `https://www.google.com/search?q=${encoded}`,
    brave: `https://search.brave.com/search?q=${encoded}`,
    duckduckgo: `https://duckduckgo.com/html/?q=${encoded}`,
    startpage: `https://www.startpage.com/sp/search?query=${encoded}`,
    baidu: `https://www.baidu.com/s?wd=${encoded}`
  };
}

// 使用示例
const urls = multiEngineSearch("climate change 2024");
```

## 📚 相关文档

- [references/advanced-search.md](references/advanced-search.md) - 国内专业领域搜索指南
- [references/international-search.md](references/international-search.md) - 国际搜索引擎完整指南
- [CHANGELOG.md](CHANGELOG.md) - 版本更新日志
- [CHANNELLOG.md](CHANNELLOG.md) - 渠道使用日志

## 📝 版本信息

- **当前版本**: v2.0.0
- **更新时间**: 2026-02-06
- **引擎数量**: 17个（国内8个 + 国际9个）
- **文档完整度**: 100%

---

**提示**: 本技能文档持续更新，建议定期查看最新版本以获取新增的搜索引擎和高级功能。
