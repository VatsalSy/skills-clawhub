# 专业领域深度搜索指南

## 一、行业资讯与新闻热点搜索

### 1.1 专业财经资讯平台

| 平台名称 | 搜索URL/方法 | 内容特点 | 适用场景 |
|---------|-------------|---------|---------|
| **东方财富网** | `https://search.eastmoney.com/search/web?q={keyword}` | 股票、基金、财经新闻 | 个股研究、市场动态 |
| **同花顺财经** | `https://basic.10jqka.com.cn/{stock_code}/` | 个股基本面、财务数据 | 股票分析、财报查询 |
| **财新网** | `https://search.caixin.com/search/search.jsp?keyword={keyword}` | 深度财经报道、调查新闻 | 深度分析、政策解读 |
| **第一财经** | `https://www.yicai.com.cn/search?keys={keyword}` | 财经视频、直播、数据 | 实时财经资讯 |
| **华尔街见闻** | `https://wallstreetcn.com/search?q={keyword}` | 全球金融市场资讯 | 国际金融动态 |
| **雪球** | `https://xueqiu.com/k?q={keyword}` | 投资者社区、个股讨论 | 投资观点、市场情绪 |
| **集思录** | `https://www.jisilu.cn/explore/?keyword={keyword}` | 低风险投资、套利策略 | 可转债/LOF/ETF套利数据 |

### 1.2 行业研究报告搜索

| 来源类型 | 搜索方法 | 获取渠道 |
|---------|---------|----------|
| **券商研报** | `{行业名称}+研报+filetype:pdf` | 东方财富、同花顺iFinD、慧博投研 |
| **咨询机构报告** | `{行业}+报告+site:iresearch.cn` | 艾瑞咨询、易观分析、QuestMobile |
| **政府行业报告** | `{行业}+发展报告+site:gov.cn` | 工信部、统计局、行业协会官网 |
| **国际组织报告** | `World Bank+{topic}+report` | 世界银行、IMF、WTO官网 |

**搜索示例**：
```javascript
// 搜索新能源汽车行业研报
web_fetch({"url": "https://www.baidu.com/s?wd=新能源汽车+研报+filetype:pdf&lm=30"})

// 搜索艾瑞咨询行业报告
web_fetch({"url": "https://www.baidu.com/s?wd=人工智能+报告+site:iresearch.cn"})
```

## 二、财务数据与金融数据搜索

### 2.1 股票财务数据查询

| 数据类型 | 查询平台 | URL模板 | 说明 |
|---------|---------|---------|------|
| **个股行情** | 东方财富 | `https://quote.eastmoney.com/{code}.html` | code格式：sh600519/sz000001 |
| **财务报表** | 同花顺 | `https://basic.10jqka.com.cn/{code}/finance.html` | 资产负债表、利润表、现金流 |
| **龙虎榜数据** | 东方财富 | `https://data.eastmoney.com/stock/lhb.html` | 营业部买卖数据 |
| **资金流向** | 东方财富 | `https://data.eastmoney.com/zjlx/detail.html` | 主力资金流向 |
| **估值分析** | 理杏仁 | `https://www.lixinger.com/analytics/company/sheet/{code}` | PE/PB/PS等估值指标 |
| **LOF套利数据** | 集思录 | `https://www.jisilu.cn/data/lof/` | LOF溢价率、成交额、份额变化 |
| **可转债数据** | 集思录 | `https://www.jisilu.cn/data/cbnew/` | 可转债行情、转股溢价率、强赎 |
| **ETF数据** | 集思录 | `https://www.jisilu.cn/data/etf/` | ETF净值、溢价率、申赎清单 |

### 2.2 宏观经济数据搜索

| 数据类型 | 官方来源 | 搜索方法 |
|---------|---------|----------|
| **GDP/CPI/PPI** | 国家统计局 | `site:stats.gov.cn+{指标名称}+{时间}` |
| **货币供应量(M2)** | 中国人民银行 | `site:pbc.gov.cn+货币供应量+{年月}` |
| **进出口数据** | 海关总署 | `site:customs.gov.cn+进出口+{年月}` |
| **PMI指数** | 国家统计局 | `site:stats.gov.cn+PMI+制造业` |
| **利率/LPR** | 中国人民银行 | `site:pbc.gov.cn+LPR+{日期}` |

**搜索示例**：
```javascript
// 搜索贵州茅台财务数据
web_fetch({"url": "https://quote.eastmoney.com/sh600519.html"})

// 搜索2025年1月CPI数据
web_fetch({"url": "https://www.baidu.com/s?wd=CPI+2025年1月+site:stats.gov.cn"})
```

## 三、政策信息与法规搜索

### 3.1 政府官方政策搜索

| 政策类型 | 官方来源 | URL/搜索方法 |
|---------|---------|-------------|
| **国务院政策** | 中国政府网 | `site:gov.cn+{关键词}+政策` |
| **部委政策** | 各部委官网 | `site:mof.gov.cn+财税政策` |
| **地方政策** | 省政府官网 | `site:gov.cn+{省份}+产业政策` |
| **法律法规** | 国家法律法规数据库 | `https://flk.npc.gov.cn/search.html?keyword={keyword}` |
| **证监会公告** | 证监会官网 | `site:csrc.gov.cn+{关键词}+公告` |

### 3.2 政策文件类型筛选

| 文件类型 | 搜索关键词 | 说明 |
|---------|-----------|------|
| **法律法规** | `{主题}+法+条例+规定` | 法律、行政法规、部门规章 |
| **规划文件** | `{领域}+规划+纲要+2025` | 五年规划、行业规划 |
| **指导意见** | `{行业}+指导意见+通知` | 政策指导、实施意见 |
| **标准规范** | `{行业}+标准+GB/T` | 国家标准、行业标准 |

**搜索示例**：
```javascript
// 搜索新能源汽车政策
web_fetch({"url": "https://www.baidu.com/s?wd=新能源汽车+政策+site:gov.cn&lm=30"})

// 搜索证监会最新公告
web_fetch({"url": "https://www.baidu.com/s?wd=证监会+公告+site:csrc.gov.cn&lm=7"})
```

## 四、经济数据深度搜索策略

### 4.1 数据聚合平台

| 平台名称 | 网址 | 数据类型 | 特点 |
|---------|------|---------|------|
| **国家统计局** | stats.gov.cn | 宏观统计数据 | 官方权威 |
| **CEIC数据库** | ceicdata.com | 全球经济数据 | 历史数据完整 |
| **Wind资讯** | wind.com.cn | 金融数据终端 | 专业级数据 |
| **同花顺iFinD** | ifind.com | 金融数据终端 | 性价比高 |
| **萝卜投研** | robo.datayes.com | 投研数据平台 | 免费基础功能 |
| **巨潮资讯网** | cninfo.com.cn | 上市公司公告 | 信息披露官方平台 |

### 4.2 行业数据搜索技巧

```javascript
// 搜索行业市场规模数据
web_fetch({"url": "https://www.baidu.com/s?wd=人工智能+市场规模+亿元+2024"})

// 搜索行业增长率数据
web_fetch({"url": "https://www.baidu.com/s?wd=新能源汽车+增长率+同比+site:stats.gov.cn"})

// 搜索行业竞争格局
web_fetch({"url": "https://www.baidu.com/s?wd={行业}+市场份额+CR5+研报"})
```

## 五、高级搜索技巧汇总

### 5.1 组合搜索策略

| 搜索目标 | 组合关键词 | 示例 |
|---------|-----------|------|
| **最新财报** | `{公司}+2024年报+PDF` | 贵州茅台+2024年报+filetype:pdf |
| **行业白皮书** | `{行业}+白皮书+2024` | 人工智能+白皮书+2024 |
| **政策解读** | `{政策}+解读+影响分析` | 新国九条+解读+影响 |
| **专家观点** | `{主题}+专家+访谈` | 宏观经济+专家+访谈 |

### 5.2 时效性筛选技巧

```javascript
// 搜索近一周的行业动态
web_fetch({"url": "https://www.baidu.com/s?wd=半导体+行业动态&lm=7"})

// 搜索近一月的政策变化
web_fetch({"url": "https://www.baidu.com/s?wd=房地产+政策&lm=30&site:gov.cn"})

// 搜索微信近三天热点
web_fetch({"url": "https://wx.sogou.com/weixin?type=2&query=A股&tsn=1"})
```

### 5.3 权威性验证方法

| 验证维度 | 检查要点 | 工具/方法 |
|---------|---------|----------|
| **来源可靠性** | 是否官方机构/权威媒体 | 查看域名后缀(.gov.cn/.edu.cn) |
| **数据准确性** | 是否标注数据来源 | 交叉验证多个来源 |
| **时效性** | 发布/更新时间 | 检查页面时间戳 |
| **专业性** | 作者资质/机构背景 | 搜索作者/机构背景 |

## 六、集思录低风险投资搜索策略

### 6.1 集思录核心数据页面

| 数据页面 | URL | 适用场景 | 关键指标 |
|---------|-----|---------|---------|
| **LOF数据** | `https://www.jisilu.cn/data/lof/` | LOF基金套利 | 溢价率、成交额、份额变化 |
| **可转债数据** | `https://www.jisilu.cn/data/cbnew/` | 可转债投资 | 转股溢价率、到期收益率、强赎 |
| **ETF数据** | `https://www.jisilu.cn/data/etf/` | ETF套利 | 净值、溢价率、申赎清单 |
| **封闭式基金** | `https://www.jisilu.cn/data/cls/` | 封基投资 | 折价率、到期时间 |
| **分级基金** | `https://www.jisilu.cn/data/sfnew/` | 分级套利 | 整体溢价率、A类收益率 |
| **QDII数据** | `https://www.jisilu.cn/data/qdii/` | QDII套利 | 溢价率、外汇额度 |
| **AH股比价** | `https://www.jisilu.cn/data/ah/` | AH套利 | A/H溢价率 |
| **讨论区** | `https://www.jisilu.cn/explore/?keyword={keyword}` | 策略讨论 | 用户分享、经验交流 |

### 6.2 集思录套利搜索技巧

| 套利类型 | 搜索关键词 | 数据来源 |
|---------|-----------|---------|
| **LOF套利** | `LOF套利`、`溢价套利`、`折价套利` | 讨论区 + LOF数据页 |
| **可转债套利** | `可转债套利`、`下修博弈`、`强赎` | 讨论区 + 可转债数据页 |
| **ETF套利** | `ETF套利`、`瞬时套利`、`延时套利` | 讨论区 + ETF数据页 |
| **跨市场套利** | `AH套利`、`QDII套利` | 讨论区 + AH/QDII数据页 |
| **打新策略** | `打新`、`新股`、`新债` | 讨论区 |
| **低风险理财** | `逆回购`、`货基`、`短期理财` | 讨论区 |

**集思录搜索示例**：
```javascript
// 搜索LOF套利相关讨论
web_fetch({"url": "https://www.jisilu.cn/explore/?keyword=LOF套利"})

// 搜索白银LOF相关讨论
web_fetch({"url": "https://www.jisilu.cn/explore/?keyword=白银LOF"})

// 搜索可转债下修机会
web_fetch({"url": "https://www.jisilu.cn/explore/?keyword=下修"})

// 查看LOF实时套利数据
web_fetch({"url": "https://www.jisilu.cn/data/lof/"})

// 查看可转债双低策略
web_fetch({"url": "https://www.jisilu.cn/data/cbnew/"})
```

### 6.3 集思录数据解读要点

| 指标 | 含义 | 套利信号 |
|------|------|---------|
| **溢价率** > 3% | 场内价格 > 净值 | 申购-卖出套利机会 |
| **折价率** > 1% | 场内价格 < 净值 | 买入-赎回套利机会 |
| **成交额** 大 | 流动性好 | 适合大资金套利 |
| **份额变化** 增加 | 套利者持续申购 | 关注溢价收敛风险 |

## 七、专业搜索使用示例

```javascript
// 示例1：搜索贵州茅台最新研报
web_fetch({"url": "https://search.eastmoney.com/search/web?q=贵州茅台+研报"})

// 示例2：搜索2025年货币政策
web_fetch({"url": "https://www.baidu.com/s?wd=货币政策+2025+site:pbc.gov.cn"})

// 示例3：搜索人工智能行业报告
web_fetch({"url": "https://www.baidu.com/s?wd=人工智能+行业报告+filetype:pdf&lm=30"})

// 示例4：搜索最新财经新闻
web_fetch({"url": "https://www.so.com/s?q=财经新闻&tn=news&lm=1"})

// 示例5：搜索上市公司公告
web_fetch({"url": "http://www.cninfo.com.cn/new/information/topSearch/query?keyWord=贵州茅台"})

// 示例6：集思录搜索LOF套利机会
web_fetch({"url": "https://www.jisilu.cn/explore/?keyword=LOF套利"})

// 示例7：集思录查看白银LOF实时数据
web_fetch({"url": "https://www.jisilu.cn/data/lof/"})

// 示例8：集思录查看可转债低溢价机会
web_fetch({"url": "https://www.jisilu.cn/data/cbnew/"})
```
