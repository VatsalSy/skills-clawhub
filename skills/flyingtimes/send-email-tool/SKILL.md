---
name: send-email
description: 邮件发送工具。配置 SMTP 发件人后，通过脚本发送纯文本或 HTML 邮件，支持附件、抄送、密送。在需要发送邮件通知、报告、自动化邮件时触发。
---

# Send Email

通过 SMTP 发送邮件的工具，支持 keyring 密钥管理。

## 功能

- ✅ 支持 SMTP 邮件发送（Gmail、QQ 邮箱、163 邮箱等）
- ✅ 支持纯文本和 HTML 格式邮件
- ✅ 支持附件（文档、图片等）
- ✅ 支持抄送（CC）和密送（BCC）
- ✅ 配置持久化，避免重复输入
- ✅ **密钥管理**：支持 keyring 安全存储密码（推荐）

## 密钥管理

### ⚠️ 重要：密码安全

本技能**强制使用 keyring** 管理发件人邮箱和密码，避免敏感信息暴露在命令行或上下文中。

### 安装 keyring

```bash
pip install keyring
```

如果 keyring 未安装，脚本会自动使用备用存储方案（base64 编码的本地文件）。

### 首次使用：保存发件人邮箱

在发送邮件前，必须先保存发件人邮箱到 keyring：

```bash
# 保存发件人邮箱（会提示输入）
python3 send_email.py username --save --email your-email@gd.chinamobile.com

# 或只运行 --save，然后交互输入
python3 send_email.py username --save
```

### 保存密码

```bash
# 保存密码（会提示输入）
python3 send_email.py password --save
```

### 删除密钥

```bash
# 删除发件人邮箱
python3 send_email.py username --delete

# 删除密码
python3 send_email.py password --delete
```

### 查看密钥状态

```bash
# 查看发件人邮箱
python3 send_email.py username

# 查看密码状态
python3 send_email.py password
```

### ⚠️ 安全提醒

- **不要**在命令行参数中传递邮箱或密码
- **不要**使用 `--email` 参数直接指定发件人
- 始终通过 `username --save` 和 `password --save` 命令管理密钥
- 邮箱和密码会自动从 keyring 读取，无需每次输入
- 默认邮箱：user@gd.chinamobile.com

---

## 快速开始

### 1. 首次配置

```bash
cd $CLAWD/skills/send-email/scripts

# 配置 SMTP 服务器（中国移动邮箱默认配置）
python3 send_email.py smtp --host smtp.gd.chinamobile.com --port 587

# 配置发件人名称
python3 send_email.py sender --name "Your Name"

# 保存发件人邮箱到 keyring
python3 send_email.py username --save --email your-email@gd.chinamobile.com

# 查看当前配置
python3 send_email.py config
```

**中国移动邮箱默认配置：**

| 配置项 | 值 |
|-------|-----|
| SMTP 服务器 | smtp.gd.chinamobile.com |
| 端口 | 587 |
| TLS | ✅ |
| 默认邮箱 | user@gd.chinamobile.com |

**重要提示：** 如果使用 Gmail，需要生成「应用专用密码」（App Password），而不是使用账户密码。

---

### 2. 发送邮件

#### 首次使用：保存密码

```bash
python3 send_email.py password --save
# 按提示输入密码
```

#### 基础发送（纯文本）

```bash
python3 send_email.py send \
  --to recipient@example.com \
  --subject "邮件主题" \
  --body "邮件正文内容"
```

#### HTML 邮件

```bash
python3 send_email.py send \
  --to recipient@example.com \
  --subject "HTML 邮件" \
  --body "<h1>标题</h1><p>正文内容</p>" \
  --html
```

#### 带附件的邮件

```bash
python3 send_email.py send \
  --to recipient@example.com \
  --subject "带附件的邮件" \
  --body "请查看附件" \
  --attachments "/path/to/file1.pdf" "/path/to/file2.png"
```

#### 抄送和密送

```bash
python3 send_email.py send \
  --to recipient@example.com \
  --cc cc1@example.com cc2@example.com \
  --bcc bcc@example.com \
  --subject "多人邮件" \
  --body "邮件正文"
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

### 发件人邮箱管理命令 (`username`)

| 参数 | 说明 |
|------|------|
| `--save` | 保存发件人邮箱到 keyring（会提示输入） |
| `--delete` | 删除保存的发件人邮箱 |

### 密码管理命令 (`password`)

| 参数 | 说明 |
|------|------|
| `--save` | 保存密码到 keyring（会提示输入） |
| `--delete` | 删除保存的密码 |

---

## 配置文件

配置文件保存在：`~/.send_email_config.json`

示例配置：
```json
{
  "smtp": {
    "host": "smtp.gd.chinamobile.com",
    "port": 587,
    "use_tls": true
  },
  "sender": {
    "name": "Your Name"
  }
}
```

**注意：** 发件人邮箱通过 `username --save` 命令存储在 keyring 中，不在配置文件中。

---

## 使用建议

1. **密钥管理（强制）：** 首次使用前必须运行 `python send_email.py username --save` 和 `python send_email.py password --save` 分别保存发件人邮箱和密码。这些信息会安全存储在 keyring 中，不会暴露在命令行或上下文中。

2. **不要传递密钥：** 发送邮件时**不要**使用 `--email` 或 `--password` 参数，这些信息会自动从 keyring 读取。这是为了保护密钥安全。

3. **中国移动邮箱：** 默认配置为 `smtp.gd.chinamobile.com:587`，默认发件人邮箱为 `user@gd.chinamobile.com`。

4. **HTML 邮件：** 使用 HTML 格式时，建议添加内联样式以确保兼容性

5. **附件路径：** 使用绝对路径或相对于执行目录的路径

6. **测试：** 首次使用时，建议先发送测试邮件给自己

7. **keyring 备用方案：** 如果 keyring 不可用，密钥会保存在 `~/.send_email_password` 和 `~/.send_email_username`（base64 编码），文件权限为 600。注意这不是加密，仅避免明文存储。

## 安全流程

```
1. 首次配置（中国移动邮箱）：
   - python send_email.py smtp --host smtp.gd.chinamobile.com --port 587
   - python send_email.py sender --name "Your Name"
   - python send_email.py username --save --email your-email@gd.chinamobile.com
   - python send_email.py password --save  ← 输入密码

2. 后续发送：
   - python send_email.py send --to to@example.com --subject "..." --body "..."
     邮箱和密码自动从 keyring 读取
```
