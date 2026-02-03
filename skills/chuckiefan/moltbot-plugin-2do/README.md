# moltbot-plugin-2do

一个 [Moltbot (OpenClaw)](https://docs.openclaw.ai) 插件，通过自然语言创建任务并发送到 [2Do](https://www.2doapp.com) app。

支持所有 Moltbot 消息渠道（QQ、企业微信、Slack、Telegram、WhatsApp、Discord 等），利用 2Do 的 [Email to 2Do](https://www.2doapp.com/kb/category/ios/email-to-2do/44/) 功能自动捕获邮件为任务。

## 功能

- 解析中文自然语言任务描述
- 支持指定目标列表和标签
- 通过 SMTP 邮件发送到 2Do
- 支持所有 Moltbot 消息渠道

## 使用示例

**基本任务：**

> 添加任务：明天去超市买牛奶

**指定列表：**

> 添加任务到工作列表：完成项目报告

**指定标签：**

> 添加任务：买菜，标签是家务和购物

**列表 + 标签：**

> 添加任务：周五前完成季度报告，列表是工作，标签是紧急和财务

## 安装

### 前置条件

- Node.js >= 22
- Moltbot (OpenClaw) 已安装
- 2Do app 已配置 Email to 2Do 功能
- 可用的 SMTP 邮箱账户

### 安装到 Moltbot

将本项目克隆到 Moltbot 的 skills 目录：

```bash
cd ~/.openclaw/skills
git clone https://github.com/chuckiefan/moltbot-plugin-2do.git
cd moltbot-plugin-2do
npm install
npm run build
```

### 配置

在 `~/.openclaw/openclaw.json` 中添加环境变量：

```json
{
  "skills": {
    "entries": {
      "moltbot-plugin-2do": {
        "enabled": true,
        "env": {
          "TWODO_EMAIL": "your-2do-email@example.com",
          "SMTP_HOST": "smtp.gmail.com",
          "SMTP_PORT": "587",
          "SMTP_USER": "your-email@gmail.com",
          "SMTP_PASS": "your-app-specific-password"
        }
      }
    }
  }
}
```

| 环境变量 | 说明 |
|---------|------|
| `TWODO_EMAIL` | 2Do 中配置的接收邮箱地址 |
| `SMTP_HOST` | SMTP 服务器地址 |
| `SMTP_PORT` | SMTP 端口（587 为 STARTTLS，465 为 SSL） |
| `SMTP_USER` | SMTP 用户名 |
| `SMTP_PASS` | SMTP 密码（推荐使用[应用专用密码](https://support.google.com/accounts/answer/185833)） |

### 配置 2Do App

1. 购买并启用 **Email to 2Do** 插件（iOS/Mac 应用内购买）
2. 在 2Do 设置 > Email to 2Do > Add Account 中添加邮箱
3. 配置捕获规则（推荐设置特定发件人规则）

详细指南参考 [2Do Email to 2Do 知识库](https://www.2doapp.com/kb/category/ios/email-to-2do/44/)。

## 项目状态

### 当前版本：v1.0.0（已发布）

**发布日期**：2026年2月4日

**已完成功能**：

- ✅ 核心 MVP 功能
  - 自然语言任务解析（支持多种中文表达方式）
  - 列表指定（"到X列表"、"列表是X"）
  - 标签指定（"标签是X和Y"）
  - 2Do 邮件格式构造
  - SMTP 邮件发送（支持 TLS/SSL）

- ✅ 测试覆盖
  - 14 个单元测试全部通过
  - 覆盖任务解析、邮件构造等核心功能

- ✅ 项目完善
  - TypeScript 类型安全
  - 完整的文档和使用示例
  - 符合 AgentSkills 规范
  - MIT 开源协议

**代码质量**：
- 构建产物：5.02 KB (dist/main.js)
- 测试覆盖率：核心功能 100%
- 无已知 bug

### 未来规划

#### Phase 2：增强解析（计划中）

- [ ] 日期/时间提取
  - 支持相对时间表达（"明天"、"下周五"、"下周三下午3点"）
  - 自动设置任务 due date

- [ ] 中英文双语支持
  - 英文命令前缀（"add task", "create todo", "remind me"）
  - 混合语言输入处理

- [ ] 优先级提取
  - 识别"紧急"、"重要"等关键词
  - 自动设置 2Do 优先级

#### Phase 3：高级功能（规划中）

- [ ] 任务确认交互
  - 发送前预览任务详情
  - 支持修改后再发送

- [ ] 批量任务添加
  - 一次解析多个任务
  - 支持列表格式（"1. 任务一 2. 任务二"）

- [ ] 自定义邮件模板
  - 支持用户自定义邮件正文格式
  - 添加任务来源、时间戳等信息

- [ ] 配置验证命令
  - 测试 SMTP 连接
  - 验证 2Do 邮箱配置

#### Phase 4：生态完善（长期）

- [ ] 发布到 ClawHub 技能市场
- [ ] 添加更多使用示例和文档
- [ ] 国际化支持（i18n）
- [ ] Web Dashboard 配置界面

---

## 开发

```bash
# 安装依赖
pnpm install

# 运行测试
pnpm test

# 构建
pnpm build

# 类型检查
pnpm typecheck
```

## License

[MIT](LICENSE)
