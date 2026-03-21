# Browser Automation Skill

浏览器自动化工具箱 - 模拟登录、点击、填表、数据采集

## 功能

| 功能 | 说明 |
|------|------|
| 浏览器控制 | 打开网页、点击、输入、截图 |
| 验证码识别 | OCR识别数字、字母、中文 |
| 数据采集 | 采集淘宝、京东、抖音等平台 |
| 账号管理 | 多账号管理、Cookie保持 |
| 自动化运营 | 自动发帖、回复、批量操作 |

## 安装依赖

```bash
# 安装 Selenium
pip3 install selenium webdriver-manager pillow pytesseract --break-system-packages

# 安装 OCR (Linux)
apt install -y tesseract-ocr tesseract-ocr-chi-sim chromium-browser chromium-chromedriver
```

## 命令

### 浏览器控制
```bash
python browser.py navigate <URL>     # 打开网页
python browser.py click <选择器>     # 点击元素
python browser.py input <选择器> <内容> # 输入文本
python browser.py screenshot [名称]   # 截图
```

### 验证码识别
```bash
python captcha.py recognize <图片>   # 识别数字+字母
python captcha.py number <图片>      # 识别纯数字
python captcha.py chinese <图片>     # 识别中文
```

### 数据采集
```bash
python collector.py taobao <关键词> [页数]  # 淘宝采集
python collector.py jd <关键词> [页数]      # 京东采集
python collector.py douyin <关键词>        # 抖音采集
```

### 账号管理
```bash
python account.py add <名称> <平台> <用户名> <密码>
python account.py list
python account.py login <名称>
```

### 自动化运营
```bash
python poster.py douyin <内容>         # 抖音发帖
python poster.py weibo <内容>          # 微博发帖
python poster.py reply <关键词> <回复>  # 自动回复
```

## 使用示例

### 模拟登录
```python
from browser import Browser

b = Browser()
b.navigate("https://example.com/login")
b.input("#username", "myuser")
b.input("#password", "mypass")
b.click("button[type='submit']")
b.screenshot("login_result.png")
b.close()
```

### 验证码识别
```python
from captcha import CaptchaSolver

solver = CaptchaSolver()
# 截图验证码
b = Browser()
b.navigate("https://example.com/captcha")
b.screenshot("captcha.png")
# 识别
code = solver.recognize("captcha.png")
print(f"识别结果: {code}")
```

### 数据采集
```python
from collector import DataCollector

c = DataCollector()
c.init_browser()
c.collect_taobao_products("白酒", pages=3)
c.close()
```

## 文件结构

```
browser-auto/
├── SKILL.md           # 本文件
├── browser.py         # 浏览器控制
├── captcha.py        # 验证码识别
├── collector.py      # 数据采集
├── account.py        # 账号管理
├── poster.py        # 自动化运营
└── tool.py          # 统一入口
```

## 注意事项

1. 部分网站需要登录后才能采集
2. 遵守网站robots.txt和使用条款
3. 建议设置适当的请求间隔
4. 验证码识别准确率取决于图片质量
