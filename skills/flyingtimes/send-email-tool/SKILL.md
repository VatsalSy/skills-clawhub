---
name: send-email
description: 邮件发送工具。配置 SMTP 发件人后，通过脚本发送纯文本或 HTML 邮件，支持附件、抄送、密送。在需要发送邮件通知、报告、自动化邮件时触发。
---

# Send Email

通过 SMTP 发送邮件的工具。

## 功能

- ✅ 支持 SMTP 邮件发送（Gmail、QQ 邮箱、163 邮箱等）
- ✅ 支持纯文本和 HTML 格式邮件
- ✅ 支持附件（文档、图片等）
- ✅ 支持抄送（CC）和密送（BCC）
- ✅ 配置持久化，避免重复输入

---

## 快速开始

### 1. 首次配置

```bash
cd $CLAWD/skills/send-email/scripts

# 配置 SMTP 服务器（Gmail 示例）
python3 send_email.py smtp --host smtp.gmail.com --port 587

# 配置发件人信息
python3 send_email.py sender --email your-email@gmail.com --name "Your Name"

# 查看当前配置
python3 send_email.py config
```

**常用 SMTP 配置：**

| 邮箱服务 | SMTP 服务器 | 端口 | TLS |
|---------|-----------|------|-----|
| Gmail | smtp.gmail.com | 587 | ✅ |
| QQ 邮箱 | smtp.qq.com | 587 | ✅ |
| 163 邮箱 | smtp.163.com | 465 | ❌ (SSL) |
| Outlook | smtp-mail.outlook.com | 587 | ✅ |

**重要提示：** 如果使用 Gmail，需要生成「应用专用密码」（App Password），而不是使用账户密码。

---

### 2. 发送邮件

#### 基础发送（纯文本）

```bash
python3 send_email.py send \
  --to recipient@example.com \
  --subject "邮件主题" \
  --body "邮件正文内容" \
  --password "your-password"
```

#### HTML 邮件

```bash
python3 send_email.py send \
  --to recipient@example.com \
  --subject "HTML 邮件" \
  --body "<h1>标题</h1><p>正文内容</p>" \
  --html \
  --password "your-password"
```

#### 带附件的邮件

```bash
python3 send_email.py send \
  --to recipient@example.com \
  --subject "带附件的邮件" \
  --body "请查看附件" \
  --attachments "/path/to/file1.pdf" "/path/to/file2.png" \
  --password "your-password"
```

#### 抄送和密送

```bash
python3 send_email.py send \
  --to recipient@example.com \
  --cc cc1@example.com cc2@example.com \
  --bcc bcc@example.com \
  --subject "多人邮件" \
  --body "邮件正文" \
  --password "your-password"
```

---

## 参数说明

### 发送命令 (`send`)

| 参数 | 说明 | 必填 |
|------|------|------|
| `--to` | 收件人邮箱 | ✅ |
| `--to-name` | 收件人名称 | ❌ |
| `--subject` | 邮件主题 | ✅ |
| `--body` | 邮件正文 | ✅ |
| `--html` | 使用 HTML 格式 | ❌ |
| `--attachments` | 附件路径（可多个） | ❌ |
| `--cc` | 抄送邮箱（可多个） | ❌ |
| `--bcc` | 密送邮箱（可多个） | ❌ |
| `--password` | 邮箱密码或应用专用密码 | ❌ (未提供时交互输入) |

---

## 配置文件

配置文件保存在：`~/.send_email_config.json`

示例配置：
```json
{
  "smtp": {
    "host": "smtp.gmail.com",
    "port": 587,
    "use_tls": true
  },
  "sender": {
    "email": "your-email@gmail.com",
    "name": "Your Name"
  }
}
```

---

## 使用建议

1. **密码安全：** 不要在命令行直接传递密码，使用 `--password` 参数或环境变量 `EMAIL_PASSWORD`

2. **应用专用密码：** Gmail 等服务需要生成「应用专用密码」，访问：https://myaccount.google.com/apppasswords

3. **HTML 邮件：** 使用 HTML 格式时，建议添加内联样式以确保兼容性

4. **附件路径：** 使用绝对路径或相对于执行目录的路径

5. **测试：** 首次使用时，建议先发送测试邮件给自己
